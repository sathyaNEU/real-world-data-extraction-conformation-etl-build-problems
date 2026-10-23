"""Independent verifier for task171: reads only target/ and the golden workbook, recomputes every graded figure on its
own code path (csv and pyarrow rows, plain dictionaries) and compares with figures.json. Exit 1 on any mismatch."""
from __future__ import annotations

import calendar
import csv
import datetime as dt
import json
import os
import sys
from bisect import bisect_right
from collections import defaultdict

import pyarrow.parquet as pq

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
ASOF = dt.date(2026, 10, 31)
PROBLEMS = []


def bad(msg):
    PROBLEMS.append(msg); print("PROBLEM", msg)


def d(s):
    return dt.date.fromisoformat(s) if s else None


fig = json.load(open(os.path.join(HERE, "figures.json")))
man = {r["file"]: r for r in csv.DictReader(open(os.path.join(T, "export_manifest.csv")))}
inv = {}
for r in csv.DictReader(open(os.path.join(T, "tbm_invoices_2025-04_2026-10.csv"))):
    r["issued"] = d(r["issued_on"]); r["toll"] = float(r["toll_billed"])
    r["bal"] = r["toll"] + float(r["invoice_fee"]) + float(r["late_fee"]) + float(r["collection_fee"])
    inv[r["invoice_no"]] = r
pays = [r for r in csv.DictReader(open(os.path.join(T, "tbm_payments_2025-04_2026-11.csv"))) if d(r["posted_on"]) <= ASOF]
holds = {r["invoice_no"]: r for r in csv.DictReader(open(os.path.join(T, "dmv_registration_holds_2025-2026.csv")))}
agency = {r["invoice_no"]: r for r in csv.DictReader(open(os.path.join(T, "agency_placements_2025-2026.csv")))}

# plan figures from the programme note
import zipfile, re
with zipfile.ZipFile(os.path.join(T, "aet_cutover_revenue_plan_2027.docx")) as z:
    doc = re.sub(r"<[^>]+>", "", z.read("word/document.xml").decode("utf-8"))
m = re.search(r"\$([\d,]+) on plates registered in this state and \$([\d,]+) on plates registered elsewhere", doc)
plan_is, plan_os = (int(m.group(1).replace(",", "")), int(m.group(2).replace(",", ""))) if m else (None, None)
if plan_is is None:
    bad("plan figures not found in the programme note")

# toll paid per invoice: payments to the records date, toll first; a violation agency remittance above its invoice's
# balance covers the plate's other invoices the agency closed as collected that day, oldest first
got = defaultdict(float); got60 = defaultdict(float)
for r in pays:
    k = r["invoice_no"]
    if not k:
        continue
    a = float(r["amount"])
    got[k] += a
    if (d(r["posted_on"]) - inv[k]["issued"]).days <= 60:
        got60[k] += a
coll_by = defaultdict(list)
for k, r in agency.items():
    if r["status"] == "COLLECTED" and k.startswith("V"):
        coll_by[(inv[k]["plate"], inv[k]["plate_state"], r["closed_on"])].append(k)
for r in pays:
    k = r["invoice_no"]
    if r["channel"] != "AGENCY" or not k.startswith("V"):
        continue
    extra = got[k] - inv[k]["bal"]
    if extra <= 0.01:
        continue
    got[k] = inv[k]["bal"]
    for o in sorted((x for x in coll_by[(inv[k]["plate"], inv[k]["plate_state"], r["posted_on"])] if x != k), key=lambda x: (inv[x]["issued"], x)):
        take = min(extra, max(inv[o]["bal"] - got[o], 0.0))
        got[o] += take; extra -= take
tp = {k: min(max(got[k], 0.0), v["toll"]) for k, v in inv.items()}
tp60 = {k: min(max(got60[k], 0.0), v["toll"]) for k, v in inv.items()}


def expiry_end(mmYYYY):
    mo, yr = int(mmYYYY[:2]), int(mmYYYY[3:])
    return dt.date(yr, mo, calendar.monthrange(yr, mo)[1])


num = defaultdict(float); den = defaultdict(float)
for k, v in inv.items():
    if v["invoice_type"] != "TOLL-BY-MAIL":
        continue
    age = (ASOF - v["issued"]).days
    if v["plate_state"] == "HM":
        if age >= 61:
            num["early"] += tp60[k]; den["early"] += v["toll"]
            if tp60[k] < v["toll"] - 0.005:
                h = holds.get(k)
                if h and h["response"] == "HOLD PLACED":
                    den["unpaid"] += v["toll"]; num["held"] += v["toll"]
                elif h and h["response"] == "NO RECORD":
                    den["unpaid"] += v["toll"]
        h = holds.get(k)
        if h and h["response"] == "HOLD PLACED" and expiry_end(h["reg_expires"]) <= ASOF:
            num["renew"] += tp[k]; den["renew"] += v["toll"]
        if h and h["response"] == "NO RECORD" and age >= 365:
            num["norec"] += tp[k]; den["norec"] += v["toll"]
    elif age >= 365:
        num["os"] += tp[k]; den["os"] += v["toll"]
e = num["early"] / den["early"]; wh = num["held"] / den["unpaid"]
share_is = e + (1 - e) * (wh * num["renew"] / den["renew"] + (1 - wh) * num["norec"] / den["norec"])
share_os = num["os"] / den["os"]
collected = plan_is * share_is + plan_os * share_os
if round(collected / 250_000) * 250_000 != fig["call_collected_toll_2027_usd"]:
    bad("collected toll %.0f against %s" % (collected, fig["call_collected_toll_2027_usd"]))
if round(share_is * 100) != fig["call_share_in_state_pct"] or round(share_os * 100) != fig["call_share_out_of_state_pct"]:
    bad("shares %.2f %.2f" % (share_is * 100, share_os * 100))

# ask A and B: violation lines, straddles and classifier splits
lines = pq.read_table(os.path.join(T, "tbm_invoice_lines_2025-03_2026-09.parquet")).to_pylist()
posts = pq.read_table(os.path.join(T, "marrowpass_commercial_postings_2026-01_2026-09.parquet"),
                      columns=["plaza", "direction", "lane", "posted_at"]).to_pylist()
lane_t = defaultdict(list)
for p in posts:
    lane_t[(p["plaza"], p["direction"], p["lane"])].append(p["posted_at"])
for k in lane_t:
    lane_t[k].sort()
vio = [l for l in lines if l["invoice_no"].startswith("V")]
by_plate = defaultdict(list)
for l in vio:
    by_plate[(l["plate"], l["plate_state"], l["plaza"], l["direction"])].append(l)
drop = set()
for k, L in by_plate.items():
    L.sort(key=lambda l: l["crossed_at"])
    for a, b in zip(L, L[1:]):
        if (b["crossed_at"] - a["crossed_at"]).total_seconds() <= 1.0:
            drop.add(b["line_id"])
for l in vio:
    ts = lane_t.get((l["plaza"], l["direction"], l["lane"]), [])
    i = bisect_right(ts, l["crossed_at"])
    if i and (l["crossed_at"] - ts[i - 1]).total_seconds() <= 0.4:
        drop.add(l["line_id"])
cnt = defaultdict(int); owed_m = defaultdict(float); owed_inv = defaultdict(float)
for l in vio:
    if l["line_id"] in drop:
        continue
    owed_inv[l["invoice_no"]] += l["toll"]
    if dt.datetime(2026, 1, 1) <= l["crossed_at"] < dt.datetime(2026, 10, 1):
        cnt[l["crossed_at"].month] += 1; owed_m[l["crossed_at"].month] += l["toll"]
for mo in range(1, 10):
    if cnt[mo] != fig["a_2026_%02d_crossings" % mo] or abs(round(owed_m[mo], 2) - fig["a_2026_%02d_toll_owed_usd" % mo]) > 0.005:
        bad("ask A month %d: %d, %.2f" % (mo, cnt[mo], owed_m[mo]))
qs = {"2025q2": (dt.date(2025, 4, 1), dt.date(2025, 7, 1)), "2025q3": (dt.date(2025, 7, 1), dt.date(2025, 10, 1)),
      "2025q4": (dt.date(2025, 10, 1), dt.date(2026, 1, 1)), "2026q1": (dt.date(2026, 1, 1), dt.date(2026, 4, 1))}
for q, (a, b) in qs.items():
    n_ = d_ = 0.0
    for k, v in inv.items():
        if v["invoice_type"] == "VIOLATION" and v["plate_state"] != "HM" and a <= v["issued"] < b:
            o = owed_inv.get(k, 0.0)
            n_ += min(tp[k], o); d_ += o
    if round(100 * n_ / d_) != fig["b_%s_collected_pct" % q]:
        bad("ask B %s: %.2f" % (q, 100 * n_ / d_))

# the golden workbook carries the same figures
import openpyxl
wb = openpyxl.load_workbook(os.path.join(TASK, "golden", "aet_2027_toll_by_mail_forecast.xlsx"))
txt = " ".join(str(c.value) for ws in wb for row in ws.iter_rows() for c in row if c.value is not None)
if "{:,}".format(fig["call_collected_toll_2027_usd"]) not in txt:
    bad("the workbook does not state the collected toll")
ws = wb["Violations 2026"]
for mo in range(1, 10):
    if ws.cell(mo + 1, 2).value != fig["a_2026_%02d_crossings" % mo] or abs(ws.cell(mo + 1, 3).value - fig["a_2026_%02d_toll_owed_usd" % mo]) > 0.005:
        bad("workbook month %d" % mo)
print("verify: %d problems (in-state %.2f, out-of-state %.2f, collected %.0f)" % (len(PROBLEMS), share_is * 100, share_os * 100, collected))
sys.exit(1 if PROBLEMS else 0)
