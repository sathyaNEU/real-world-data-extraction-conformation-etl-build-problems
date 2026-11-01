"""task146 architecture 3: the independent verifier. Recomputes every owed figure from target/ with pandas and
statsmodels, sharing no code with analysis.py, and compares it with figures.json."""
import json
import os
import sys

import numpy as np
import pandas as pd
import statsmodels.api as sm

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
FIG = json.load(open(os.path.join(HERE, "figures.json")))
DOSE = {"PBO": 0, "HB25": 25, "HB50": 50, "HB100": 100, "HB200": 200}
bad = []


def same(name, a, b):
    good = a == b
    print(("PASS " if good else "FAIL ") + name, "" if good else (a, b))
    if not good:
        bad.append(name)


def dmy(s):
    return pd.to_datetime(s, format="%d.%m.%Y") if "." in s else pd.to_datetime(s, format="%Y-%m-%d")


sub = pd.read_csv(os.path.join(T, "vela2_subjects.csv"))
dose = pd.read_csv(os.path.join(T, "vela2_dosing_log.csv"), parse_dates=["dose_date"])
d1 = dose.groupby("subject_id")["dose_date"].min()
pa = pd.read_csv(os.path.join(T, "vela2_pasi_assessments.csv"), parse_dates=["assessment_date"])
cm = pd.read_csv(os.path.join(T, "vela2_concomitant_medications.csv"), dtype=str).fillna("")
cm["start"] = cm["start_date"].map(dmy)
resc = cm[cm["atc_code"].str.startswith(("D07AC", "D07AD")) |
          cm["medication"].str.lower().str.contains("phototherapy|uvb|puva", regex=True)]

pa["d1"] = pa["subject_id"].map(d1)
base = pa[pa["assessment_date"] <= pa["d1"]].sort_values("assessment_date").groupby("subject_id").last()["pasi_total"]
w16 = pa[pa["visit"] == "Week 16"].set_index("subject_id")


def responder(cut):
    out = {}
    for sid in sub["subject_id"]:
        if sid not in w16.index:
            out[sid] = 0
            continue
        v, dd = w16.loc[sid, "pasi_total"], w16.loc[sid, "assessment_date"]
        r = resc[(resc["subject_id"] == sid) & (resc["start"] > d1[sid]) & (resc["start"] <= dd)]
        out[sid] = int((base[sid] - v) / base[sid] >= cut - 1e-12 and r.empty)
    return pd.Series(out)


r75, r90 = responder(0.75), responder(0.90)
for name, r in (("PASI 75", r75), ("PASI 90", r90)):
    for arm in DOSE:
        ids = sub.loc[sub["arm"] == arm, "subject_id"]
        same("ask A %s %s" % (name, arm), round(100 * r[ids].mean(), 1), FIG["ask_pasi"]["%s|%s" % (name, arm)])

# itch
ep = pd.read_csv(os.path.join(T, "vela2_epro_diary.csv"))
dl = pd.read_csv(os.path.join(T, "vela2_epro_device_log.csv"))
ep = ep.merge(dl[["device_id", "subject_id"]], on="device_id", how="inner")
tz = pd.read_csv(os.path.join(T, "vela2_sites.csv")).set_index("site")["time_zone"]
ep = ep.merge(sub[["subject_id", "site", "arm"]], on="subject_id")
ep["utc"] = pd.to_datetime(ep["entry_utc"], utc=True)
loc = [u.tz_convert(tz[s]) for u, s in zip(ep["utc"], ep["site"])]
ep["day"] = [(x - pd.Timedelta(days=1)).date() if x.hour < 3 else x.date() for x in loc]
ep["d1"] = ep["subject_id"].map(d1).dt.date
ep["sd"] = [(d - a).days + 1 if d >= a else (d - a).days for d, a in zip(ep["day"], ep["d1"])]
for wk, (lo, hi) in (("Week 12", (78, 84)), ("Week 16", (106, 112))):
    for arm in DOSE:
        num = den = 0
        for sid in sub.loc[sub["arm"] == arm, "subject_id"]:
            e = ep[ep["subject_id"] == sid]
            b = e[(e["sd"] >= -7) & (e["sd"] <= -1)]["itch_nrs"]
            if len(b) < 4 or b.mean() < 4:
                continue
            den += 1
            m = e[(e["sd"] >= lo) & (e["sd"] <= hi)]["itch_nrs"]
            last = d1[sid] + pd.Timedelta(days=hi - 1)
            rr = resc[(resc["subject_id"] == sid) & (resc["start"] > d1[sid]) & (resc["start"] <= last)]
            if len(m) >= 4 and b.mean() - m.mean() >= 4 and rr.empty:
                num += 1
        same("ask B %s %s" % (wk, arm), round(100 * num / den, 1), FIG["ask_itch"]["%s|%s" % (wk, arm)])

# the call: a statsmodels route on the same estimand
pk = pd.read_csv(os.path.join(T, "vela2_pk_trough_samples.csv"), dtype=str)
pk = pk[~pk["concentration"].str.startswith("<")].copy()
pk["c"] = pk["concentration"].astype(float) / np.where(pk["unit"] == "ng/mL", 1000.0, 1.0)
pk = pk.merge(sub[["subject_id", "arm", "weight_kg"]], on="subject_id")
pk = pk[pk["arm"] != "PBO"]
pk["y"] = np.log(pk["c"]) - np.log(pk["arm"].map(DOSE))
pk["lw"] = np.log(pk["weight_kg"] / 85.0)
X = pd.get_dummies(pk["visit"]).astype(float)
X["lw"] = pk["lw"]
m = sm.OLS(pk["y"], X).fit()
a16, bw = m.params["Week 16"], m.params["lw"]
act = sub[sub["arm"] != "PBO"].copy()
act["lc"] = np.log(act["arm"].map(DOSE)) + a16 + bw * np.log(act["weight_kg"] / 85.0)
act["y"] = act["subject_id"].map(r75)
lg = sm.Logit(act["y"], sm.add_constant(act["lc"])).fit(disp=0)
feas = pd.concat([pd.read_excel(os.path.join(T, "vela3_feasibility_survey_2026.xlsx"), sheet_name="US sites")
                  .assign(kg=lambda d: d["Weight (lb)"] * 0.45359237),
                  pd.read_excel(os.path.join(T, "vela3_feasibility_survey_2026.xlsx"), sheet_name="Canadian sites")
                  .assign(kg=lambda d: d["Weight (kg)"])])
est = {}
for d in (50, 100, 200):
    lc = np.log(d) + a16 + bw * np.log(feas["kg"] / 85.0)
    est[d] = 100 * float(np.mean(1 / (1 + np.exp(-(lg.params["const"] + lg.params["lc"] * lc)))))
pick = next(d for d in (50, 100, 200) if est[d] >= 70)
same("the call", pick, FIG["call"]["dose_mg"])
for d in (50, 100, 200):
    same("side of the bar at %d mg" % d, "at or above" if est[d] >= 70 else "below", FIG["phase3_side"][str(d)])
    same("expected response at %d mg (one decimal)" % d, round(est[d], 1), FIG["phase3_expected"][str(d)])
same("mean weight phase 3", round(float(feas["kg"].mean()), 1), FIG["mean_weight_kg"]["phase3"])
same("mean weight phase 2b", round(float(sub["weight_kg"].mean()), 1), FIG["mean_weight_kg"]["phase2b"])
print("verify: %d failures" % len(bad))
sys.exit(1 if bad else 0)
