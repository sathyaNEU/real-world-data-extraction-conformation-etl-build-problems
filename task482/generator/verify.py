"""task482 architecture 16: the independent verifier. Reads target.zip only (pypdf for the invoices, its own parsing
and its own day-splitting), recomputes every graded figure and compares it with generator/figures.json.

    python3 task482/generator/verify.py
"""
import csv
import datetime as dt
import io
import json
import os
import re
import sys
import zipfile
from zoneinfo import ZoneInfo

import numpy as np
import openpyxl
from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
LON = ZoneInfo("Europe/London")
Z = zipfile.ZipFile(os.path.join(TASK, "target.zip"))
FIG = json.load(open(os.path.join(HERE, "figures.json")))
FAILS = []


def blob(name):
    return Z.read(name)


def table(name):
    return list(csv.DictReader(io.StringIO(blob(name).decode("utf-8"))))


def utc_of(local):
    return local.replace(tzinfo=LON).astimezone(dt.timezone.utc)


def lday(u):
    return u.astimezone(LON).date()


def same(label, a, b):
    ok = a == b
    print("%s %-58s %s" % ("PASS" if ok else "FAIL", label, a if ok else "%r against figures.json %r" % (a, b)))
    if not ok:
        FAILS.append(label)


# ------------------------------------------------------------------ invoices and the meter
periods = []
for page in PdfReader(io.BytesIO(blob("brackwell_gas_invoices_2026.pdf"))).pages:
    tx = re.sub(r"\s+", " ", page.extract_text())
    st = re.findall(r"(\d{2})/(\d{2})/(\d{4}) (\d{2}):(\d{2})", tx)
    a = dt.datetime(int(st[0][2]), int(st[0][1]), int(st[0][0]), int(st[0][3]), int(st[0][4]))
    b = dt.datetime(int(st[-1][2]), int(st[-1][1]), int(st[-1][0]), int(st[-1][3]), int(st[-1][4]))
    cv = float(re.search(r"Calorific value \(MJ/m3\) ([0-9.]+)", tx).group(1))
    vcf = float(re.search(r"Volume correction factor ([0-9.]+)", tx).group(1))
    periods.append((utc_of(a), utc_of(b), cv, vcf))
periods.sort()
hcf = 2.83
day0 = dt.date(2026, 1, 1)
y = np.zeros(365)
total = 0.0
for r in table("brackwell_site_gas_meter_2026.csv"):
    u = dt.datetime.fromisoformat(r["Interval start (UTC)"]).replace(tzinfo=dt.timezone.utc)
    m3 = float(r["Consumption"]) * (hcf if r["Unit"] == "hcf" else 1.0)
    p = next(p for p in periods if p[0] <= u < p[1])
    k = m3 * p[3] * p[2] / 3.6
    y[(lday(u) - day0).days] += k
    total += k


def spread(a, b, weight, arr):
    """Spread weight over the local days of [a, b) by the hours in each."""
    span = (b - a).total_seconds()
    cur = a
    while cur < b:
        d = lday(cur)
        nxt = utc_of(dt.datetime.combine(d + dt.timedelta(days=1), dt.time()))
        end = min(b, nxt)
        arr[(d - day0).days] += weight * (end - cur).total_seconds() / span
        cur = end


# ------------------------------------------------------------------ the logs
wb = openpyxl.load_workbook(io.BytesIO(blob("brackwell_melting_furnace_logs_2026.xlsx")), read_only=True,
                            data_only=True)
melt, m3d, h1d, t1d, hdd = (np.zeros(365) for _ in range(5))
melted = {"6063": 0.0, "6082": 0.0, "LM25": 0.0}
for sh in ("M1 casthouse", "M2 casthouse"):
    keep = {}
    for r in list(wb[sh].iter_rows(values_only=True))[1:]:
        if r[0] is not None and r[0] not in keep:
            keep[r[0]] = r
    for r in keep.values():
        spread(utc_of(r[2]), utc_of(r[3]), float(r[4]), melt)
        melted[str(r[1])] += float(r[4])
m3_total = 0.0
seen = set()
for r in list(wb["M3 tower melter"].iter_rows(values_only=True))[1:]:
    if r[0] is None or r[0] in seen:
        continue
    seen.add(r[0])
    m3d[(lday(utc_of(r[1])) - day0).days] += r[2] / 1000.0
    m3_total += r[2] / 1000.0
h1_hours = {"6063": 0.0, "6082": 0.0}
for r in table("brackwell_homogenizing_furnace_h1_2026.csv"):
    a = utc_of(dt.datetime.strptime(r["Door closed"], "%d/%m/%Y %H:%M"))
    b = utc_of(dt.datetime.strptime(r["Door opened"], "%d/%m/%Y %H:%M"))
    hrs = (b - a).total_seconds() / 3600.0
    spread(a, b, hrs, h1d)
    h1_hours[r["Alloy"]] += hrs
t1_hours = 0.0
for r in table("brackwell_heat_treatment_oven_t1_2026.csv"):
    a, b = (utc_of(dt.datetime.fromisoformat(r[k])) for k in ("Start", "End"))
    hrs = (b - a).total_seconds() / 3600.0
    spread(a, b, hrs, t1d)
    t1_hours += hrs
for r in table("brackwell_works_weather_2026.csv"):
    hdd[(dt.date.fromisoformat(r["Date"]) - day0).days] = max(0.0, 15.5 - float(r["Mean C"]))
A = np.column_stack([melt, m3d, h1d, t1d, hdd, np.ones(365)])
beta = np.linalg.lstsq(A, y, rcond=None)[0]

# ------------------------------------------------------------------ production, attribution, the premium
last = {}
for r in table("brackwell_production_lots_2026.csv"):
    when = dt.datetime.strptime(r["Inspected"], "%d/%m/%Y %H:%M")
    if r["Lot"] not in last or when >= last[r["Lot"]][0]:
        last[r["Lot"]] = (when, r)
fam_of = {"6063 extrusion billet": "BIL6063", "6082 extrusion billet": "BIL6082", "LM25 foundry ingot": "INGLM25",
          "LM25-TF sand castings": "CSTLM25"}
prod = {f: 0.0 for f in fam_of.values()}
for when, r in last.values():
    if r["Result"] == "PASS":
        prod[fam_of[r["Product"]]] += int(r["Net kg"]) / 1000.0
gas = {"BIL6063": beta[0] * melted["6063"] + beta[2] * h1_hours["6063"],
       "BIL6082": beta[0] * melted["6082"] + beta[2] * h1_hours["6082"],
       "INGLM25": beta[0] * melted["LM25"],
       "CSTLM25": beta[1] * m3_total + beta[3] * t1_hours}
rest = total - sum(gas.values())
allp = sum(prod.values())
inten = {f: (gas[f] + rest * prod[f] / allp) * 0.18296 / 1000.0 / prod[f] for f in gas}
wb2 = openpyxl.load_workbook(io.BytesIO(blob("velden_2027_calloff_schedule.xlsx")), read_only=True, data_only=True)
call = {f: 0 for f in gas}
for r in list(wb2["Call-offs 2027"].iter_rows(values_only=True))[1:]:
    if not r[0]:
        continue
    s = r[1].lower()
    f = "BIL6063" if "6063" in s else "BIL6082" if "6082" in s else "CSTLM25" if "casting" in s else "INGLM25"
    call[f] += sum(int(v) for v in r[3:15])
earning = [f for f in ("BIL6063", "BIL6082", "INGLM25", "CSTLM25") if inten[f] <= 0.235]
same("premium (EUR)", 38 * sum(call[f] for f in earning), FIG["call"]["premium_eur"])
same("families earning the premium", earning, FIG["call"]["earning"])
same("intensities, two decimals", {f: "%.2f" % v for f, v in inten.items()}, FIG["intensity_2dp"])
same("production (t)", {f: int(round(v)) for f, v in prod.items()}, FIG["produced_t"])
same("call-offs (t)", call, FIG["calloff_t"])

# ------------------------------------------------------------------ the asks
visits = {}
for r in table("brackwell_weighbridge_2026.csv"):
    u = dt.datetime.fromisoformat(r["Weighed (UTC)"]).replace(tzinfo=dt.timezone.utc)
    v = visits.setdefault((r["Ticket"], lday(u)), {"w": {}, "mv": r["Movement"], "day": lday(u)})
    v["w"][int(r["Weighing"])] = int(r["Weight kg"])
lines = {}
for r in table("brackwell_scrap_goods_in_2026.csv"):
    day = dt.datetime.strptime(r["Date"], "%d/%m/%Y").date()
    lines.setdefault((r["WB ticket"], day), []).append(r)
qn = lambda d: "Q%d" % ((d.month + 2) // 3)  # noqa: E731
A_ = {g: {q: 0 for q in ("Q1", "Q2", "Q3", "Q4")} for g in ("CST", "EXT", "TRN", "UBC")}
for key, ls in lines.items():
    ws = [visits[key]["w"][k] for k in sorted(visits[key]["w"])]
    if len(ls) == 1:
        nets = [ws[0] - ws[-1]]
    else:
        drops = sorted([ws[0] - ws[1], ws[1] - ws[2]])
        order = sorted(range(2), key=lambda i: int(ls[i]["Declared kg"]))
        nets = [0, 0]
        for rank, i in enumerate(order):
            nets[i] = drops[rank]
    for r, n in zip(ls, nets):
        if r["Status"] == "Accepted" and r["Grade"] in A_:
            A_[r["Grade"]][qn(key[1])] += n
same("ask A, scrap by grade and quarter (t)", {g: {q: int(round(v / 1000.0)) for q, v in A_[g].items()} for g in A_},
     FIG["ask_a"])
B_ = {q: 0 for q in ("Q1", "Q2", "Q3", "Q4")}
for key, v in visits.items():
    if v["mv"] == "Waste out":
        ws = [v["w"][k] for k in sorted(v["w"])]
        B_[qn(v["day"])] += ws[-1] - ws[-2]
same("ask B, dross by quarter (t)", {q: int(round(x / 1000.0)) for q, x in B_.items()}, FIG["ask_b"])
print("verify: %d failed" % len(FAILS))
sys.exit(1 if FAILS else 0)
