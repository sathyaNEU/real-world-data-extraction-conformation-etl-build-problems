"""An independent recomputation of every graded figure from target/ alone (no import of calc.py), checked against
generator/figures.json.  python3 generator/verify.py"""
import json
import os
import re
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(os.path.dirname(HERE), "target")
F = json.load(open(os.path.join(HERE, "figures.json")))
bad = []


def fy(d):
    return d.year if d.month >= 4 else d.year - 1


mp = dict(pd.read_csv(os.path.join(T, "fennick_pas_to_epr_number_map.csv")).values)
ep = pd.read_csv(os.path.join(T, "pas_inpatient_episodes_2021_2026.csv"), dtype=str, keep_default_na=False)
ep = ep[ep.episode_no == "1"]
code = ep.primary_diagnosis.map(lambda c: re.sub(r"[^A-Z0-9]", "", c)[:4])
em = ep.admission_method.map(lambda m: m[:1] == "2" or m.startswith("Emergency"))
line = ep[em & code.map(lambda c: c[:3] in ("K80", "K81") or c in ("K830", "K851"))].copy()
line["pt"] = line.hospital_number.map(lambda h: mp.get(h, h))
line["adm"] = pd.to_datetime(line.admission_date)
ptl = pd.read_parquet(os.path.join(T, "admitted_ptl_snapshots_2021_2026.parquet"))
ptl["pt"] = ptl.hospital_number.map(lambda h: mp.get(h, h))
ch = ptl[ptl.planned_procedure == "Laparoscopic cholecystectomy"].copy()
ch["snap"] = pd.to_datetime(ch.snapshot_date)
ch["add"] = pd.to_datetime(ch.date_added)
spans = ch.groupby(["pt", "add"]).snap.agg(["min", "max"]).reset_index()
by = {k: v for k, v in spans.groupby("pt")}


def listed(pt, adm):
    v = by.get(pt)
    if v is None:
        return False
    prev_me = (adm.replace(day=1) - pd.Timedelta(days=1))
    return bool(((v["add"] < adm) & (v["max"] >= prev_me)).any())


line["listed"] = [listed(p, a) for p, a in zip(line.pt, line.adm)]
line["fyr"] = line.adm.map(fy)
pmon = ch.groupby("snap").size()
pm_hz = pmon[pmon.index >= pd.Timestamp(2022, 4, 1)].sum()
hz = line[line.listed & (line.fyr >= 2022)].shape[0] / pm_hz
bands = ["0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80-84", "85-89", "90+"]


def popn(year, proj):
    tot = {}
    for d in ("Marlstead", "Coldvale"):
        src = pd.read_excel(os.path.join(T, "population_projections_2022_based.xlsx" if proj or year > 2025 else "population_mid_year_estimates_2018_2025.xlsx"), sheet_name=d)
        for s in ("Females", "Males"):
            r = src[(src.mid_year == year) & (src.sex == s)].iloc[0]
            for i, b in enumerate(bands):
                tot[(s[0], i)] = tot.get((s[0], i), 0) + r[b]
    return tot


nl = line[~line.listed & line.fyr.isin([2024, 2025, 2026])]
cnt = nl.groupby([nl.sex.map(lambda s: "F" if s in ("2", "Female") else "M"), nl.age_on_admission.astype(int).map(lambda a: min(a // 5, 18))]).size()
expo = {}
for y, w in ((2024, 1.0), (2025, 1.0), (2026, 7 / 12)):
    for k, v in popn(y, False).items():
        expo[k] = expo.get(k, 0) + v * w
p27 = popn(2027, True)
first = sum(cnt.get(k, 0) / expo[k] * p27[k] for k in expo if expo[k] > 0)
import pdfplumber  # noqa: E402
plan = {}
with pdfplumber.open(os.path.join(T, "elective_capacity_plan_2027_28_general_surgery.pdf")) as pdf:
    for pg in pdf.pages:
        for tb in pg.extract_tables():
            h = [re.sub(r"\s+", " ", c or "") for c in tb[0]]
            if h[0] == "Month end":
                for r in tb[1:]:
                    if (r[0] or "").startswith("Laparoscopic"):
                        plan.update(dict(zip(h[1:], [int(x.replace(",", "")) for x in r[1:]])))
pmf = sum(v for k, v in plan.items() if pd.Timestamp("1 " + k) >= pd.Timestamp(2027, 4, 1))
total = first + hz * pmf
call = int(round(total / 50) * 50)
for k, v in (("call.gallstone_emergency_2027_28", call), ("comp.planned_patient_months", pmf)):
    if F[k] != v:
        bad.append((k, F[k], v))
for k, v in (("call.central_expectation", total), ("comp.not_listed_2027_28", first), ("comp.hazard_per_patient_month", hz)):
    if abs(F[k] - v) > (0.15 if "hazard" not in k else 0.00006):
        bad.append((k, F[k], v))
# ---- the asks, recomputed: clock from e-RS where the pathway carries a UBRN; a pathway opened when its predecessor for
# the same patient and operation left the list carries the predecessor's clock; Fennick rows of pathways Marlstead now holds out
ers = dict(zip(*[pd.read_csv(os.path.join(T, "ers_referrals_general_surgery_2019_2026.csv"), dtype=str)[c] for c in ("ubrn", "referral_received")]))
ptl["add"] = pd.to_datetime(ptl.date_added)
ptl["snap"] = pd.to_datetime(ptl.snapshot_date)
life = ptl.groupby(["pt", "opcs_code", "add"]).agg(last=("snap", "max"), ubrn=("ubrn", "first"), clk=("rtt_clock_start", "first")).reset_index().sort_values(["pt", "opcs_code", "add"])
clock = {}
prev = None
for r in life.itertuples():
    if r.ubrn:
        c = pd.Timestamp(ers[r.ubrn])
    elif prev is not None and prev.pt == r.pt and prev.opcs_code == r.opcs_code and (r.add - prev.last).days <= 40:
        c = clock[(prev.pt, prev.opcs_code, prev.add)]
    else:
        c = pd.Timestamp(r.clk)
    clock[(r.pt, r.opcs_code, r.add)] = c
    prev = r
for d in ("2025-06-30", "2025-09-30", "2025-12-31", "2026-03-31"):
    s = ptl[ptl.snapshot_date == d]
    mg = s[s.site == "MGH"].groupby(["pt", "opcs_code"])["add"].max()
    keep = [not (st == "FEN" and (p, o) in mg.index and mg[(p, o)] > a) for st, p, o, a in zip(s.site, s.pt, s.opcs_code, s["add"])]
    s = s[keep]
    for site in ("MGH", "FEN"):
        x = s[s.site == site]
        a = sum((pd.Timestamp(d) - clock[(p, o, ad)]).days >= 364 for p, o, ad in zip(x.pt, x.opcs_code, x["add"]))
        b = int(x.opcs_code.isin(["T202", "T204", "T241"]).sum())
        for key, v in (("askA.%s.%s" % (d, site), a), ("askB.%s.%s" % (d, site), b)):
            if F[key] != v:
                bad.append((key, F[key], v))
print("call %d (central %.1f, first %.1f, hazard %.5f, patient-months %d)" % (call, total, first, hz, pmf))
print("FAIL" if bad else "PASS", bad)
sys.exit(1 if bad else 0)
