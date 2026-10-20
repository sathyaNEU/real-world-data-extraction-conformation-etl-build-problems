"""The independent verifier: every graded figure recomputed from the shipped files with pandas and its own EM, sharing
no code with the generator, the pack reader or the analysis. Exit 0 when every figure in figures.json reproduces."""
import datetime as dt
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = dict(sample="mwis_2026_sample.csv", dialer="kestrelby_mwis_dialer_export.csv",
             crm="trevanna_msc_mwis_activity.xlsx", interviews="mwis_2026_interviews.csv",
             regions="apple_health_regions.xlsx", roster="trevanna_expansion_roster_20261019.csv",
             changes="trevanna_enrollment_changes_20261001_20261019.txt", cases="hca_household_composition_20261015.csv")
DAY = pd.Timestamp("2026-10-01")


def histories(t):
    s = pd.read_csv(os.path.join(t, FILES["sample"]), dtype=str)
    d = pd.read_csv(os.path.join(t, FILES["dialer"]), dtype=str)
    d = d[d.case_id.isin(s.case_id)].copy()
    ts = pd.to_datetime(d.call_start, utc=True).dt.tz_convert("America/Los_Angeles").dt.tz_localize(None)
    d["when"] = ts
    d["kind"] = np.where(ts.dt.dayofweek == 5, 3, np.where(ts.dt.hour * 60 + ts.dt.minute >= 17 * 60 + 30, 2, 1))
    d["res"] = d.disposition.map({"1100": 1, "2110": 2}).fillna(0).astype(int)
    c = pd.read_excel(os.path.join(t, FILES["crm"]), sheet_name="Activity", dtype={"Member ID": str})
    c = c[c["Activity Type"] == "MWIS outbound call"].copy()
    c["when"] = pd.to_datetime(c["Activity Date"].astype(str).str[:10] + " " + c["Activity Time"], format="%Y-%m-%d %I:%M %p")
    c["case_id"] = c["Member ID"].map(dict(zip(s.member_id, s.case_id)))
    c["kind"] = 0
    c["res"] = c.Result.map({"Spoke to member - survey completed": 1, "Spoke to member - declined survey": 2}).fillna(0)
    calls = pd.concat([d[["case_id", "when", "kind", "res"]], c[["case_id", "when", "kind", "res"]]])
    calls["res"] = calls.res.astype(int)
    calls = calls.sort_values(["case_id", "when", "kind"])
    calls["first_hit"] = calls.groupby("case_id").res.transform(lambda r: (r > 0).cumsum().shift(fill_value=0))
    calls = calls[calls.first_hit == 0]
    i = pd.read_csv(os.path.join(t, FILES["interviews"]), dtype=str)
    i = i[i.case_id.isin(s.case_id)]
    y = pd.Series(np.where(i.status == "Complete", pd.to_numeric(i.total_hours_march, errors="coerce") >= 80,
                           i.key_80_hours_march == "Yes").astype(int), index=i.case_id)
    return s, calls, y


def em(s, calls, y, tol=1e-12):
    cases = s.case_id.tolist()
    ix = {c: k for k, c in enumerate(cases)}
    n = len(cases)
    win = {0: 0, 1: 0, 2: 1, 3: 2}
    fails = np.zeros((n, 3))
    hitw = np.full(n, -1)
    out = np.zeros(n, int)
    for row in calls.itertuples(index=False):
        k = ix[row.case_id]
        if row.res:
            hitw[k] = win[row.kind]
            out[k] = row.res
        else:
            fails[k, win[row.kind]] += 1
    reg = pd.Categorical(s.region).codes
    regs = list(pd.Categorical(s.region).categories)
    cls = np.array([y.get(c, -1) for c in cases])
    known = cls >= 0
    pi = np.full(len(regs), 0.5)
    pr = np.array([[0.3, 0.3, 0.3], [0.2, 0.2, 0.2]])
    for _ in range(50000):
        lik = []
        for k in (0, 1):
            l = (fails * np.log(1 - pr[k])).sum(1)
            l = l + np.where(hitw >= 0, np.log(pr[k][np.maximum(hitw, 0)]), 0)
            lik.append(l)
        a1 = np.log(pi[reg]) + lik[1]
        a0 = np.log(1 - pi[reg]) + lik[0]
        w = np.where(known, cls, 1 / (1 + np.exp(a0 - a1)))
        pi2 = np.array([w[reg == r].mean() for r in range(len(regs))])
        pr2 = np.zeros_like(pr)
        for k, wk in ((1, w), (0, 1 - w)):
            for j in range(3):
                h = (wk * (hitw == j)).sum()
                pr2[k, j] = h / (h + (wk * fails[:, j]).sum())
        done = max(abs(pi2 - pi).max(), abs(pr2 - pr).max()) < tol
        pi, pr = pi2, pr2
        if done:
            break
    return {r: float(w[reg == k].mean()) for k, r in enumerate(regs)}


def age(born, on=DAY):
    return on.year - born.dt.year - ((born.dt.month > on.month) | ((born.dt.month == on.month) & (born.dt.day > on.day)))


def planning(t):
    reg = pd.read_excel(os.path.join(t, FILES["regions"]), sheet_name="Counties")
    region_of = dict(zip(reg.County, reg["Region code"]))
    ro = pd.read_csv(os.path.join(t, FILES["roster"]), dtype=str)
    lg = pd.read_csv(os.path.join(t, FILES["changes"]), sep="|", dtype=str, keep_default_na=False)
    hh = pd.read_csv(os.path.join(t, FILES["cases"]), dtype=str, keep_default_na=False)
    ro["born"] = pd.to_datetime(ro.birth_date, format="%m/%d/%Y")
    ro["begin"] = pd.to_datetime(ro.enrollment_begin)
    ro["end"] = pd.to_datetime(ro.scheduled_end)
    lg["eff"] = pd.to_datetime(lg.effective_date, format="%Y%m%d")
    lg["at"] = pd.to_datetime(lg.logged_at)
    lg["born"] = pd.to_datetime(lg.birth_date, format="%Y%m%d")
    # spans: a member covered on the day is on the roster with an enrollment begun by it and not ended before it (a
    # termination before it reinstated), or was terminated with a last day on or after it before any October add
    first_add = lg[lg.change == "ADD"].groupby("member_id").at.min()
    late_term = lg[(lg.change == "TERM") & (lg.eff >= DAY)]
    first_term = late_term.groupby("member_id").at.min()
    reinst = set(lg[lg.change == "REINSTATE"].member_id)
    early = set(lg[(lg.change == "TERM") & (lg.eff < DAY)].member_id)
    ro_ok = (ro.begin <= DAY) & (ro.end.isna() | (ro.end >= DAY)) & (~ro.member_id.isin(early) | ro.member_id.isin(reinst))
    churn = ro.member_id.map(first_term).notna() & ro.member_id.map(first_add).notna() & \
        (ro.member_id.map(first_term) < ro.member_id.map(first_add))
    a = ro[ro_ok | churn][["member_id", "p1_client_id", "born", "county"]].copy()
    mv = lg[(lg.change == "ADDRESS") & (lg.eff > DAY)].sort_values("eff").groupby("member_id").county_before.first()
    a["county"] = a.member_id.map(mv).fillna(a.county)
    gone = late_term[~late_term.member_id.isin(ro.member_id) & ~late_term.member_id.isin(first_add.index)]
    gone = gone.sort_values("at").groupby("member_id").first().reset_index()
    a = pd.concat([a, gone.rename(columns={"county_before": "county"})[["member_id", "p1_client_id", "born", "county"]]])
    a = a[(age(a.born) >= 19) & (age(a.born) <= 64)].copy()
    a["region"] = a.county.map(region_of)
    hh["born"] = pd.to_datetime(hh.birth_date, format="%m/%d/%Y")
    hh["b"] = pd.to_datetime(hh.member_begin)
    hh["e"] = pd.to_datetime(hh.member_end.replace("", None))
    on = (hh.b <= DAY) & (hh.e.isna() | (hh.e >= DAY))
    kids = hh[on & (hh.case_role == "CHILD") & (hh.born <= DAY) & (age(hh.born) < 14)]
    with_kid = set(kids.case_id)
    par = hh[on & hh.case_role.isin(["HOH", "SPOUSE", "CARETAKER_RELATIVE"]) & hh.case_id.isin(with_kid)]
    a["parent"] = a.p1_client_id.isin(set(par.p1_client_id))
    return a.groupby("region").size().to_dict(), a[a.parent].groupby("region").size().to_dict()


def run(task):
    t = os.path.join(task, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    names = dict(pd.read_excel(os.path.join(t, FILES["regions"]), sheet_name="Regions")[["Code", "Apple Health region"]]
                 .itertuples(index=False))
    s, calls, y = histories(t)
    sh = em(s, calls, y)
    bad = []
    for code, v in sh.items():
        n = names[code]
        if abs(v - fig["share_unrounded"][n]) > 5e-6:
            bad.append(("share", n, v, fig["share_unrounded"][n]))
        if int(np.floor(v * 100 + 0.5)) != fig["share"][n]:
            bad.append(("share pct", n, v))
    four = sorted(sorted(sh, key=sh.get)[:4], key=sh.get)
    if [names[c] for c in four] != fig["call"]["regions"]:
        bad.append(("four", four))
    if names[sorted(sh, key=sh.get)[4]] != fig["call"]["first_below"]:
        bad.append(("first below",))
    a, b = planning(t)
    for code in a:
        if a[code] != fig["ask_a"][names[code]]:
            bad.append(("ask a", code, a[code], fig["ask_a"][names[code]]))
        if b.get(code, 0) != fig["ask_b"][names[code]]:
            bad.append(("ask b", code, b.get(code, 0), fig["ask_b"][names[code]]))
    print("VERIFY %s: shares, the four, the first below, %d planning figures" % ("PASS" if not bad else "FAIL", 2 * len(a)))
    for x in bad:
        print("  ", x)
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(run(os.path.dirname(HERE)))
