"""Independent verification of task456 from the shipped bundle alone, on its own code path (pandas readers and a
latent class fit by EM over flag-pattern counts), against generator/figures.json and the golden files.

    python3 task456/generator/verify.py [target] [golden]
"""
import json
import os
import sys
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
WIN = (pd.Timestamp("2025-12-22"), pd.Timestamp("2026-01-18"))
PRIOR = (pd.Timestamp("2025-11-24"), pd.Timestamp("2025-12-21"))
ICU = {"Adult ICU", "ICU", "MICU/SICU", "Critical Care Unit", "Adult Critical Care", "Intensive Care"}
ED = {"Emergency Department", "ED", "Emergency Dept"}


def load(target):
    p = lambda n: os.path.join(target, n)
    xw = pd.read_csv(p("facility_crosswalk.csv"), dtype=str)
    rg = pd.read_csv(p("compact_regions_counties.csv"), dtype=str)
    xw = xw.merge(rg[["county", "region_code", "region_name"]], on="county", how="left")
    return p, xw, rg


def census_flags(p, xw):
    new = pd.read_csv(p("capacity_survey_2025-12-01_2026-01-19.csv"), dtype={"licence_no": str})
    new["t"] = pd.to_datetime(new.submitted_at, utc=True)
    new = new.rename(columns={"report_date": "date", "staffed_adult_icu_beds": "staffed",
                              "adult_icu_patients": "patients"})
    old = pd.read_csv(p("capacity_survey_2025-11.csv"), dtype={"FacLicense": str})
    tzs = dict(zip(xw.licence_no, xw.time_zone))
    old["t"] = [pd.Timestamp(s).tz_localize(ZoneInfo(tzs[k])).tz_convert("UTC")
                for s, k in zip(pd.to_datetime(old.SubmitTime, format="%m/%d/%Y %H:%M"), old.FacLicense)]
    old = old.rename(columns={"FacLicense": "licence_no", "AdultICU_Staffed": "staffed", "AdultICU_Census": "patients"})
    old["date"] = pd.to_datetime(old.RptDate, format="%m/%d/%Y").dt.strftime("%Y-%m-%d")
    s = pd.concat([new[["licence_no", "date", "t", "staffed", "patients"]],
                   old[["licence_no", "date", "t", "staffed", "patients"]]])
    s = s.sort_values("t").groupby(["licence_no", "date"]).tail(1)
    s["A"] = (s.patients >= s.staffed).astype(int)
    return s.set_index(["licence_no", "date"])["A"]


def board(p, xw):
    ev = pd.read_json(p("bed_status_events_2025-11-01_2026-01-20.jsonl"), lines=True, dtype={"facility_code": str})
    ev["t"] = pd.to_datetime(ev.logged_utc, utc=True)
    mig = ev.loc[ev.set_by == "system migration", "t"].unique()
    assert len(mig) == 1
    cur, prev = dict(zip(xw.board_code, xw.licence_no)), dict(zip(xw.board_code_previous, xw.licence_no))
    ev["licence_no"] = [prev[c] if t < mig[0] else cur[c] for c, t in zip(ev.facility_code, ev.t)]
    ev = ev.sort_values(["licence_no", "unit", "t"], kind="mergesort")
    ev["t_next"] = ev.groupby(["licence_no", "unit"]).t.shift(-1).fillna(pd.Timestamp("2026-01-20 12:00", tz="UTC"))
    return ev


def intervals(ev, units, keep):
    e = ev[ev.unit.isin(units)]
    return e[[keep(s, r) for s, r in zip(e.status, e.reason)]]


def hours_by_region(iv, xw, lo_day, hi_day):
    tz = dict(zip(xw.licence_no, xw.time_zone))
    reg = dict(zip(xw.licence_no, xw.region_code))
    out = {}
    for lic, a, b in zip(iv.licence_no, iv.t, iv.t_next):
        z = ZoneInfo(tz[lic])
        lo = pd.Timestamp(lo_day).tz_localize(z)
        hi = (pd.Timestamp(hi_day) + pd.Timedelta(days=1)).tz_localize(z)
        x = (min(b, hi) - max(a, lo)).total_seconds() / 3600
        if x > 0:
            out[reg[lic]] = out.get(reg[lic], 0.0) + x
    return out


def closed_days(ev, xw):
    tz = dict(zip(xw.licence_no, xw.time_zone))
    iv = intervals(ev, ICU, lambda s, r: s == "Closed")
    out = set()
    for lic, a, b in zip(iv.licence_no, iv.t, iv.t_next):
        z = ZoneInfo(tz[lic])
        d0 = a.tz_convert(z).normalize().tz_localize(None)
        d1 = (b - pd.Timedelta(microseconds=1)).tz_convert(z).normalize().tz_localize(None)
        for d in pd.date_range(d0, d1):
            out.add((lic, d.strftime("%Y-%m-%d")))
    return out


def calls(p, xw):
    sheets = pd.read_excel(p("transfer_center_calls_2025-11-01_2026-01-04.xlsx"), sheet_name=None)
    o = pd.concat(sheets.values(), ignore_index=True)
    ct = ZoneInfo("America/Chicago")
    by_name = dict(zip(xw.facility_name, xw.licence_no))
    old = pd.DataFrame({"case": o["Request #"].astype(int).astype(str), "legacy": "",
                        "opened": [pd.Timestamp(x).tz_localize(ct, ambiguous=True) for x in o["Opened (CT)"]],
                        "sender": o["Sending facility"], "patient": o["Patient ref"],
                        "level": o["Level of care"].map({"Adult ICU": "ADULT_ICU", "Step-down/PCU": "STEP_DOWN",
                                                         "Pediatric ICU": "PEDS_ICU"}),
                        "seq": o["Call"], "called": o["Facility called"].map(by_name),
                        "at": [pd.Timestamp(x).tz_localize(ct, ambiguous=True) for x in o["Called at (CT)"]],
                        "outcome": o["Response"].map({"Accepted": "ACCEPTED", "Declined": "DECLINED",
                                                      "Cancelled": "CANCELLED", "No placement": "UNPLACED"}),
                        "code": o["Reason"].fillna("")})
    n = pd.read_csv(p("transfer_center_calls_2026-01-05_2026-01-19.csv"), dtype=str, keep_default_na=False)
    by_tc = dict(zip(xw.center_code, xw.licence_no))
    new = pd.DataFrame({"case": n.request_id, "legacy": n.legacy_case,
                        "opened": pd.to_datetime(n.opened_utc, utc=True), "sender": n.sending_facility_text,
                        "patient": n.patient_ref, "level": n.care_level, "seq": n.seq.astype(int),
                        "called": n.called_facility_id.map(by_tc), "at": pd.to_datetime(n.called_utc, utc=True),
                        "outcome": n.outcome, "code": n.decline_code})
    new["opened"] = new.opened.dt.tz_convert(ct)
    new["at"] = new["at"].dt.tz_convert(ct)
    allc = pd.concat([old, new], ignore_index=True)
    allc["key"] = np.where(allc.legacy != "", allc.legacy, allc.case)
    return allc


def decline_days(c, xw):
    tz = dict(zip(xw.licence_no, xw.time_zone))
    d = c[(c.level == "ADULT_ICU") & (c.outcome == "DECLINED") & c.code.isin(["CAP", "NB", "NS"]) & c.called.notna()]
    return {(lic, t.tz_convert(ZoneInfo(tz[lic])).strftime("%Y-%m-%d")) for lic, t in zip(d.called, d["at"])}


def em(df, groups, iters=50000, tol=1e-13):
    """two-class latent class model over flag-pattern counts: share by group, feed rates common"""
    pat = df.groupby(["g", "A", "B", "C"], dropna=False).size().reset_index(name="n")
    A = pat.A.to_numpy(dtype=float)
    B = pat.B.to_numpy(dtype=float)
    C = pat.C.to_numpy(dtype=float)
    n = pat.n.to_numpy(dtype=float)
    g = pat.g.to_numpy()
    pi = {k: 0.4 for k in groups}
    s, f = np.array([0.4, 0.85, 0.3]), np.array([0.03, 0.3, 0.03])
    ll0 = None
    for _ in range(iters):
        def lk(r):
            la = np.where(np.isnan(A), 1.0, np.where(A == 1, r[0], 1 - r[0]))
            return la * np.where(B == 1, r[1], 1 - r[1]) * np.where(C == 1, r[2], 1 - r[2])
        l1, l0 = lk(s), lk(f)
        pr = np.array([pi[k] for k in g])
        w = pr * l1 / (pr * l1 + (1 - pr) * l0)
        ll = float((n * np.log(pr * l1 + (1 - pr) * l0)).sum())
        pi = {k: float((n * w)[g == k].sum() / n[g == k].sum()) for k in groups}
        oa = ~np.isnan(A)
        s = np.array([(n * w * np.nan_to_num(A))[oa].sum() / (n * w)[oa].sum(), (n * w * B).sum() / (n * w).sum(),
                      (n * w * C).sum() / (n * w).sum()])
        f = np.array([(n * (1 - w) * np.nan_to_num(A))[oa].sum() / (n * (1 - w))[oa].sum(),
                      (n * (1 - w) * B).sum() / (n * (1 - w)).sum(), (n * (1 - w) * C).sum() / (n * (1 - w)).sum()])
        if ll0 is not None and abs(ll - ll0) < tol:
            break
        ll0 = ll
    return pi, s, f


def placements(c, xw, rg, p):
    al = pd.read_csv(p("transfer_center_name_aliases.csv"), dtype=str, keep_default_na=False)
    reg = dict(zip(rg.county, rg.region_code))
    xreg = dict(zip(xw.licence_no, xw.region_code))
    out = {}
    for key, cs in c.groupby("key"):
        cs = cs.sort_values(["at", "seq"])
        if cs.level.iloc[0] != "ADULT_ICU":
            continue
        a = al[al.typed_name == cs.sender.iloc[0]].iloc[0]
        sreg = reg[a.county] if a.state == "TN" else None
        d = cs.opened.iloc[0].tz_convert(ZoneInfo(a.time_zone)).tz_localize(None).normalize()
        if not (WIN[0] <= d <= WIN[1]):
            continue
        acc = None
        for o, h in zip(cs.outcome, cs.called):
            if o == "ACCEPTED":
                acc = h
            elif o == "CANCELLED":
                acc = None
        if acc is not None and sreg is not None and xreg[acc] != sreg:
            out[sreg] = out.get(sreg, 0) + 1
    return out


def main(target=None, golden=None):
    target = target or os.path.join(TASK, "target")
    golden = golden or os.path.join(TASK, "golden")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    p, xw, rg = load(target)
    name = dict(zip(rg.region_code, rg.region_name))
    codes = ["NE", "ET", "SE", "UC", "MS", "SC", "WT", "MD"]
    cen = census_flags(p, xw)
    ev = board(p, xw)
    cd = closed_days(ev, xw)
    c = calls(p, xw)
    dd = decline_days(c, xw)
    rows = []
    for lic, r in zip(xw.licence_no, xw.region_code):
        for d in pd.date_range(*WIN):
            k = d.strftime("%Y-%m-%d")
            rows.append({"g": r, "lic": lic, "date": k, "A": cen.get((lic, k), np.nan), "B": int((lic, k) in cd),
                         "C": int((lic, k) in dd)})
    df = pd.DataFrame(rows)
    pi, s, f = em(df, codes)
    act = [name[g] for g in codes if pi[g] >= 1 / 3]
    tenth = {name[g]: int(10 * np.floor(10 * pi[g] + 0.5)) for g in codes}
    a = placements(c, xw, rg, p)
    b = hours_by_region(intervals(ev, ED, lambda st, r: st == "Divert" or (st == "Advisory" and r == "EMS diversion")),
                        xw, *WIN)
    cc = hours_by_region(intervals(ev, ICU, lambda st, r: st == "Closed"), xw, *PRIOR)
    res = []
    chk = lambda lab, cond, det="": res.append((lab, bool(cond), det))
    chk("verify: 2,100 hospital-days", len(df) == 2100 == fig["hospital_days_all"])
    chk("verify: the regions activated", act == fig["activated"], act)
    chk("verify: the shares to the nearest ten per cent", tenth == fig["share_pct"], tenth)
    chk("verify: the unrounded shares", all(abs(round(pi[g], 3) - fig["share_unrounded"][name[g]]) < 0.0015
                                            for g in codes), {g: round(v, 4) for g, v in pi.items()})
    chk("verify: the feed rates", round(100 * s[1]) == fig["feed_full_day_rate_pct"]["board"] and
        round(100 * f[1]) == fig["feed_ordinary_day_rate_pct"]["board"], (s, f))
    chk("verify: out-of-region placements", {name[g]: a.get(g, 0) for g in codes} == fig["placements_out_of_region"], a)
    chk("verify: diversion hours", {name[g]: int(np.floor(b.get(g, 0) + 0.5)) for g in codes} ==
        fig["diversion_hours"], {g: round(v, 2) for g, v in b.items()})
    chk("verify: adult ICU closed hours before the window", {name[g]: int(np.floor(cc.get(g, 0) + 0.5)) for g in codes}
        == fig["closed_hours"], {g: round(v, 2) for g, v in cc.items()})
    conf = pd.read_csv(os.path.join(golden, "hospital_days_conformed_2025-12-22_2026-01-18.csv"),
                       dtype={"licence_no": str})
    m = conf.merge(df, left_on=["licence_no", "date"], right_on=["lic", "date"])
    chk("verify: the conformed file's feeds equal the independent conformance on every hospital-day",
        len(m) == 2100 and (m.board_adult_icu_closed == m.B).all() and (m.transfer_center_no_bed_decline == m.C).all()
        and ((m.census_full_at_0700.isna() & m.A.isna()) | (m.census_full_at_0700 == m.A)).all())
    for lab, okk, det in res:
        print(("ok  " if okk else "FAIL"), lab, "" if okk else det)
    print("verify: %d of %d agree" % (sum(1 for r in res if r[1]), len(res)))
    if not all(r[1] for r in res):
        raise SystemExit("verify failed")


if __name__ == "__main__":
    main(*(sys.argv[1:3]))
