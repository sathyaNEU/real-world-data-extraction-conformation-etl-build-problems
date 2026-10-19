"""The independent verifier: every graded figure recomputed from target/ alone, with pandas and numpy only (none of
the generator's modules), and compared with figures.json and the golden workbook."""
import json
import os
import sys
from decimal import ROUND_HALF_UP, Decimal

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
W0, W1 = pd.Timestamp("2022-01-01"), pd.Timestamp("2026-09-30")


def hu(x, nd):
    return float(Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP))


def run(task):
    t = os.path.join(task, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    bad = []

    def ok(label, cond, detail=""):
        print("%s  verify: %s %s" % ("PASS" if cond else "FAIL", label, detail))
        if not cond:
            bad.append(label)
    pmi = pd.read_csv(os.path.join(t, "patient_master_index.csv"), dtype=str, keep_default_na=False)
    pmi["nhs"] = pmi.nhs_number.str.replace(" ", "")
    h2n = dict(zip(pmi.hpn.str.strip(), pmi.nhs))
    reg = pd.read_excel(os.path.join(t, "mas_clinic_register.xlsx"), sheet_name="Clinics", dtype=str)
    code = {**dict(zip(reg["CIS clinic code"].dropna(), reg.loc[reg["CIS clinic code"].notna(), "Clinic"])),
            **dict(zip(reg["EPR site code"], reg["Clinic"]))}
    cis = pd.read_csv(os.path.join(t, "cis_ace3_forms_2014_2023.csv"), dtype=str, keep_default_na=False)
    a = pd.DataFrame({"nhs": cis.hpn.str.strip().map(h2n), "when": pd.to_datetime(cis.assessment_date, dayfirst=True),
                      "clinic": cis.clinic_code.map(code), "done": cis.form_status.eq("C"),
                      "score": cis.total.astype(float), "id": cis.form_id})
    obs = pd.read_csv(os.path.join(t, "epr_cognitive_observations_2024_2026.csv"), dtype=str, keep_default_na=False)
    obs = obs[(obs.item_code == "ACE3_TOTAL") & obs.set_status.isin(["Final", "Incomplete"])]
    b = pd.DataFrame({"nhs": obs.nhs_number, "when": pd.to_datetime(obs.performed_at.str[:10]),
                      "clinic": obs.site_code.map(code), "done": obs.set_status.eq("Final"),
                      "score": obs.value.astype(float), "id": obs.obs_set_id})
    s = pd.concat([a, b]).sort_values(["nhs", "when", "id"])
    s["prior"] = s.groupby("nhs").done.cumsum() - s.done
    # diagnoses on the record
    cd = pd.read_csv(os.path.join(t, "cis_diagnoses_2014_2023.csv"), dtype=str, keep_default_na=False)
    ed = pd.read_csv(os.path.join(t, "epr_problem_list_2024_2026.csv"), dtype=str, keep_default_na=False)
    dx = pd.concat([pd.DataFrame({"nhs": cd.hpn.str.strip().map(h2n), "when": pd.to_datetime(cd.diagnosis_date,
                                                                                            dayfirst=True),
                                  "code": cd.icd10_code, "o": 0}),
                    pd.DataFrame({"nhs": ed.nhs_number, "when": pd.to_datetime(ed.recorded_on), "code": ed.problem_code,
                                  "o": np.where(ed.source.eq("EPR"), 2, 1)})])
    dx = dx[dx.when <= W1].sort_values(["nhs", "when", "o"])
    last = dx.groupby("nhs").code.last()
    scope = last[last.str.match(r"^(F00|G30)") | last.eq("F06.7")].index
    p = s[s.done & (s.when >= W0) & (s.when <= W1) & s.nhs.isin(scope)].copy()
    p = p[p.groupby("nhs").when.transform("size") >= 2]
    p["t"] = (p.when - W0).dt.days / 365.25
    p["st"] = (p.prior > 0).astype(float)
    # the gain within patients: residuals on each patient's own line, three or more sittings
    q = p[p.groupby("nhs").t.transform("size") >= 3]
    tm = q.groupby("nhs").t.transform("mean")
    xt = q.t - tm
    sxx = (xt ** 2).groupby(q.nhs).transform("sum")

    def res(col):
        m = q.groupby("nhs")[col].transform("mean")
        bb = (xt * (q[col] - m)).groupby(q.nhs).transform("sum") / sxx
        return q[col] - m - bb * xt
    ry, rs = res("score"), res("st")
    gain = float((ry * rs).sum() / (rs * rs).sum())
    p["adj"] = p.score - gain * p.st
    g = p.groupby("nhs")
    tm2, am = g.t.transform("mean"), g.adj.transform("mean")
    slope = ((p.t - tm2) * (p.adj - am)).groupby(p.nhs).sum() / ((p.t - tm2) ** 2).groupby(p.nhs).sum()
    where = p.sort_values("when").groupby("nhs").clinic.last()
    dec = -slope.groupby(where).mean()
    order = list(dec.sort_values(ascending=False).index)
    ok("the two sites", order[:2] == fig["call"]["sites"], order[:3])
    ok("the first clinic below", order[2] == fig["call"]["below"])
    ok("the gain to the half point", hu(2 * gain, 0) / 2 == fig["gain"], round(gain, 3))
    for c, v in dec.items():
        ok("%s's decline to the half point" % c, hu(2 * v, 0) / 2 == fig["decline"][c], round(v, 3))
    # B1 and B2
    ep = pd.read_csv(os.path.join(t, "epr_mas_episodes_2024_2026.csv"), dtype=str, keep_default_na=False)
    ep["start"] = pd.to_datetime(ep.episode_start)
    ep["end"] = pd.to_datetime(ep.episode_end.replace("", None))
    op = ep[(ep.start <= W1) & (ep.end.isna() | (ep.end > W1))].copy()
    ap = pd.read_csv(os.path.join(t, "epr_outpatient_appointments_2024_2026.csv"), dtype=str, keep_default_na=False)
    ap["day"] = pd.to_datetime(ap.appointment_start.str[:10])
    gone = ap[ap.outcome.isin(["Attended - discharged from service", "Attended - care passed to care home liaison team",
                               "Attended - diagnosis given, discharged from service"]) & (ap.day <= W1)]
    op = op.merge(gone[["nhs_number", "day"]], on="nhs_number", how="left")
    left = op[(op.day >= op.start) & (op.day <= W1)].nhs_number.unique()
    op = op[~op.nhs_number.isin(left)].drop_duplicates("episode_id")
    act = pmi[pmi.record_status.eq("Active")].set_index("nhs")
    dead = pd.to_datetime(act.date_of_death.replace("", None))
    op = op[~(op.nhs_number.map(dead) <= W1)]
    op = op[op.nhs_number.isin(scope_on(dx, W1))]
    dob = pd.to_datetime(act.date_of_birth)
    born = op.nhs_number.map(dob)
    age = 2027 - born.dt.year - ((born.dt.month > 1) | ((born.dt.month == 1) & (born.dt.day > 1))).astype(int)
    op["clinic"] = op.site_code.map(code)
    for c in fig["ask_a"]["under_follow_up"]:
        k = op[op.clinic == c]
        ok("B1 %s" % c, k.nhs_number.nunique() == fig["ask_a"]["under_follow_up"][c], k.nhs_number.nunique())
        ok("B2 %s" % c, k[age[k.index] <= 85].nhs_number.nunique() == fig["ask_a"]["aged_85_or_under"][c])
    # C1 and C2
    tr = pd.read_excel(os.path.join(t, "mas_pathway_tracker_2024_2026.xlsx"), sheet_name="Pathways",
                       dtype={"NHS number": str})
    given = ap[ap.outcome.str.contains("diagnosis given")].groupby("nhs_number").day.min()
    tr["given"] = tr["NHS number"].map(given)
    tr["ref"] = pd.to_datetime(tr["Referral date"])
    u = tr[(tr.given >= pd.Timestamp("2025-10-01")) & (tr.given <= W1)].copy()
    u["days"] = (u.given - u.ref).dt.days
    for c in fig["ask_b"]["within_42_days_pct"]:
        k = u[u.Clinic == c]
        ok("C1 %s" % c, hu(100 * (k.days <= 42).mean(), 1) == fig["ask_b"]["within_42_days_pct"][c])
        ok("C2 %s" % c, hu(k.days.mean(), 1) == fig["ask_b"]["average_days"][c])
    # the golden workbook carries the same figures
    gw = pd.read_excel(os.path.join(task, "golden", "arv1102_site_selection.xlsx"), sheet_name="Recruiting sites",
                       header=3)
    gw = gw[gw["Clinic"].isin(fig["decline"].keys())]
    ok("the workbook's declines", all(abs(float(r["Decline, ACE-III points a year"]) - fig["decline"][r["Clinic"]]) < 1e-9
                                      for _, r in gw.iterrows()))
    print("verify: %d failed" % len(bad))
    return 0 if not bad else 1


def scope_on(dx, day):
    d = dx[dx.when <= day]
    last = d.groupby("nhs").code.last()
    return set(last[last.str.match(r"^(F00|G30)") | last.eq("F06.7")].index)


if __name__ == "__main__":
    sys.exit(run(os.path.dirname(HERE)))
