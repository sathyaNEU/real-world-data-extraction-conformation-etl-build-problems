"""task163 independent verifier: reads only the shipped bundle (target/, and the write-up's figures.json to compare),
on its own code path (no import of the generator's modules), and recomputes the call and every ask figure.

    python3 task163/generator/verify.py
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import math
import os
import re
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
FAILS = []


def ok(label, cond, detail=""):
    print("%s  %s  %s" % ("PASS" if cond else "FAIL", label, detail))
    if not cond:
        FAILS.append(label)


def rows(name):
    with open(os.path.join(T, name), encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def rhu(x, nd=0):
    return math.floor(x * 10 ** nd + 0.5 + 1e-9) / 10 ** nd


def nearest(x, step):
    return step * math.floor(x / step + 0.5)


def lstsq2(pairs):
    """Least squares y = a*x1 + b*x2 by the normal equations; returns a, b and the worst absolute residual."""
    sxx = sum(p[0] * p[0] for p in pairs)
    sxy = sum(p[0] * p[1] for p in pairs)
    syy = sum(p[1] * p[1] for p in pairs)
    bx = sum(p[0] * p[2] for p in pairs)
    by = sum(p[1] * p[2] for p in pairs)
    det = sxx * syy - sxy * sxy
    a = (bx * syy - by * sxy) / det
    b = (by * sxx - bx * sxy) / det
    return a, b, max(abs(a * p[0] + b * p[1] - p[2]) for p in pairs)


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    # ------------------------------------------------------------------ the call
    import openpyxl
    weight, fam, cost, size, code_of = {}, {}, {}, {}, {}
    for r in rows("item_master.csv"):
        i = int(r["item_code"])
        weight[i] = float(r["unit_weight"]) * (1000.0 if r["weight_uom"] == "kg" else 1.0)
        fam[i], cost[i], size[i] = r["family"], float(r["std_cost_gbp"]), r["size_class"]
        code_of[r["aubrine_code"]] = i
    face = {}
    for r in rows("location_master.csv"):
        if r["item_code"]:
            face[int(r["item_code"])] = (r["aisle"], r["level"], 3 * (int(r["bay"]) - 1) + int(r["position"]))
    wb = openpyxl.load_workbook(os.path.join(T, "slotting_plan_2027.xlsx"), read_only=True, data_only=True)
    pface, fcast = {}, {}
    for loc, aub, _, _, n in list(wb["Faces 2027"].iter_rows(values_only=True))[1:]:
        z, a, b, lev, p = loc.split(".")
        i = code_of[aub]
        pface[i] = (z + a, lev, 3 * (int(b) - 1) + int(p))
        fcast[i] = int(n)

    def share_alike(faces):
        spot = {v: k for k, v in faces.items()}
        out = {}
        for i, (a, lev, p) in faces.items():
            ns = [spot[(a, lev, q)] for q in (p - 1, p + 1) if (a, lev, q) in spot]
            out[i] = sum(1 for j in ns if abs(weight[j] - weight[i]) <= 15) / len(ns)
        return out
    s_now, s_plan = share_alike(face), share_alike(pface)
    lines = defaultdict(int)
    d0, d1 = dt.date(2025, 9, 22), dt.date(2026, 9, 20)
    for r in rows("pick_velocity_by_week.csv"):
        m = dt.date.fromisoformat(r["week_commencing"])
        if d0 <= m <= d1 - dt.timedelta(6):
            lines[int(r["item_code"])] += int(r["lines_picked"])
    wb = openpyxl.load_workbook(os.path.join(T, "aubrine_claims_register.xlsx"), read_only=True, data_only=True)
    it = wb["Claims"].iter_rows(values_only=True)
    head = next(it)
    ix = {h: k for k, h in enumerate(head)}
    n_claims = 0
    for r in it:
        desp = r[ix["Despatched"]]
        desp = desp.date() if isinstance(desp, dt.datetime) else desp
        if r[ix["Reason"]] == "Wrong item received" and r[ix["Status"]] == "Validated" and d0 <= desp <= d1:
            n_claims += 1
    exposure = sum(lines[i] * s_now[i] for i in face)
    per = n_claims / exposure
    plan_claims = per * sum(fcast[i] * s_plan[i] for i in pface)
    cur_claims = per * sum(fcast[i] * s_now[i] for i in face)
    total27 = sum(fcast.values())
    ok("call: validated wrong-item claims in the 52 weeks", n_claims == fig["base_claims"], n_claims)
    ok("call: lines picked in the 52 weeks", sum(lines.values()) == fig["base_lines"], sum(lines.values()))
    ok("call: claims under the re-slot to the nearest 100", nearest(plan_claims, 100) == fig["call_plan_claims"],
       "%.1f" % plan_claims)
    ok("call: claims per 10,000 lines under the re-slot", rhu(plan_claims / total27 * 1e4, 1) == fig["call_plan_per_10k"],
       "%.4f" % (plan_claims / total27 * 1e4))
    ok("call: claims per 10,000 lines on today's layout", rhu(cur_claims / total27 * 1e4, 1) == fig["call_cur_per_10k"],
       "%.4f" % (cur_claims / total27 * 1e4))
    ok("call: the re-slot is over Schedule 3's 2.5", plan_claims / total27 * 1e4 > 2.5 > cur_claims / total27 * 1e4)
    ok("component: picks beside a face within 15 g, 2026 and plan",
       rhu(100 * exposure / sum(lines.values()), 1) == fig["alike_share_base_pct"] and
       rhu(100 * sum(fcast[i] * s_plan[i] for i in pface) / total27, 1) == fig["alike_share_plan_pct"])
    ok("component: claims per 10,000 such picks", rhu(per * 1e4, 2) == fig["claims_per_10k_alike"], "%.3f" % (per * 1e4))
    from pypdf import PdfReader
    sched = re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(os.path.join(T, "schedule3_service_levels.pdf")).pages))
    ok("document: Schedule 3 reads back with its limit", "shall not exceed 2.5 per 10,000 order lines" in sched)
    sop = re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(os.path.join(T, "pack_bench_procedure.pdf")).pages))
    ok("document: the pack bench procedure reads back with its tolerance", "more than 15 g over or under" in sop)

    # ------------------------------------------------------------------ Ask A: find the window each premium line covers
    night, sunday, worked = defaultdict(float), defaultdict(float), []
    prem = []
    for r in rows("corsley_invoice_lines.csv"):
        if r["line_type"] == "Hours":
            d = dt.date.fromisoformat(r["shift_start_date"])
            night[d] += float(r["night_hours"])
            sunday[d] += float(r["hours"]) if d.weekday() == 6 else 0.0
            worked.append((d, float(r["hours"]), float(r["night_hours"]), float(r["amount_gbp"])))
        else:
            prem.append((dt.date.fromisoformat(r["invoice_date"]), float(r["amount_gbp"])))
    best = None
    for off in range(0, 40):
        for span in (7, 14, 21, 28, 35):
            pairs = []
            for inv, amt in prem:
                end = inv - dt.timedelta(off)
                dd = [end - dt.timedelta(k) for k in range(span)]
                pairs.append((sum(night[x] for x in dd), sum(sunday[x] for x in dd), amt))
            a, b, res = lstsq2(pairs)
            if best is None or res < best[0]:
                best = (res, off, span, a, b)
    res, off, span, un, us = best
    ok("Ask A: one alignment makes the premium lines an identity (28 days ending 9 days before the invoice)",
       off == 9 and span == 28 and res < 0.02, "offset %d, span %d, residual %.4f" % (off, span, res))
    un, us = round(un, 2), round(us, 2)
    bym = defaultdict(lambda: [0.0, 0.0])
    for d, h, nh, amt in worked:
        k = "%d-%02d" % (d.year, d.month)
        bym[k][0] += amt + nh * un + (h * us if d.weekday() == 6 else 0.0)
        bym[k][1] += h
    good = sum(1 for k, v in fig["ask_a"].items() if rhu(bym[k][0] / bym[k][1], 2) == v)
    ok("Ask A: the cost of an agency hour, twelve months to the penny", good == 12, "%d of 12" % good)

    # ------------------------------------------------------------------ Ask B: the grade legend the invoices allow
    latest = {}
    for r in rows("returns_grading_log.csv"):
        if r["return_ref"] not in latest or r["graded_at"] >= latest[r["return_ref"]]["graded_at"]:
            latest[r["return_ref"]] = r
    units = list(latest.values())
    switch = min(dt.date.fromisoformat(u["graded_at"][:10]) for u in units if u["captured_by"] == "Handheld")
    bills = {}
    for page in PdfReader(os.path.join(T, "ravelrig_invoices_2025-26.pdf")).pages:
        txt = page.extract_text()
        m = re.search(r"Aubrine, (\w+) (\d{4})\s+([\d,]+\.\d{2})", txt)
        month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                 "November", "December"].index(m.group(1)) + 1
        bills[(int(m.group(2)), month)] = float(m.group(3).replace(",", ""))

    def counts(repack_code):
        c = defaultdict(lambda: [0, 0])
        for u in units:
            d = dt.date.fromisoformat(u["graded_at"][:10])
            if int(u["grade"]) == repack_code(d):
                c[(d.year, d.month)][0 if size[int(u["item_code"])] == "S" else 1] += 1
        return c
    golden = counts(lambda d: 2 if d < switch else 3)
    literal = counts(lambda d: 2)
    pa, pb, res_g = lstsq2([(golden[m][0], golden[m][1], v) for m, v in bills.items()])
    _, _, res_l = lstsq2([(literal[m][0], literal[m][1], v) for m, v in bills.items()])
    ok("Ask B: the invoices reproduce to the penny when 2 is repack on sheets and 3 is repack on the handheld",
       res_g < 0.005, "prices %.2f %.2f, residual %.4f" % (pa, pb, res_g))
    ok("Ask B: the procedure's legend read all year cannot reproduce them at any constant prices", res_l > 20,
       "residual %.2f" % res_l)
    agg = defaultdict(lambda: [0, 0, 0, 0.0])
    for u in units:
        d = dt.date.fromisoformat(u["graded_at"][:10])
        if not (dt.date(2025, 10, 1) <= d <= dt.date(2026, 9, 30)):
            continue
        i, g = int(u["item_code"]), int(u["grade"])
        fate = {1: "resell", 2: "repack", 3: "scrap"}[g] if d < switch else {1: "resell", 2: "scrap", 3: "repack"}[g]
        a = agg[fam[i]]
        a[0] += 1
        a[1] += fate == "repack"
        a[2] += fate == "scrap"
        a[3] += cost[i] if fate == "scrap" else 0.0
    good = 0
    for f, v in fig["ask_b"].items():
        n, rp, sc, val = agg[f]
        good += rhu(100.0 * rp / n, 1) == v["repack_pct"]
        good += rhu(100.0 * sc / n, 1) == v["scrap_pct"]
        good += int(rhu(val, 0)) == v["scrap_value"]
    ok("Ask B: fifteen family figures", good == 15, "%d of 15" % good)
    print("verify: %d failed" % len(FAILS))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
