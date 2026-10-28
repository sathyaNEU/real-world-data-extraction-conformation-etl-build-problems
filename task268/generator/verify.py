"""The independent verifier: reads only the bundle (and the goldens), on its own code path with the csv module, and
recomputes every graded figure; each document carrying a filed sentence is read back through its own extractor with a
positive control first.

    python3 task268/generator/verify.py [target_dir] [figures.json]"""
import csv
import datetime as dt
import json
import os
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
REG = ["Mersey", "Pennine", "Wessex", "Fenland", "Severn"]


def _rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _last_sunday(y, m):
    d = dt.date(y, m, 31)
    while d.weekday() != 6:
        d -= dt.timedelta(days=1)
    return d


def uk_date(s):
    if len(s) == 10:
        return dt.date(int(s[:4]), int(s[5:7]), int(s[8:10]))
    t = dt.datetime(int(s[:4]), int(s[5:7]), int(s[8:10]), int(s[11:13]), int(s[14:16]), int(s[17:19]))
    on = dt.datetime.combine(_last_sunday(t.year, 3), dt.time(1))
    off = dt.datetime.combine(_last_sunday(t.year, 10), dt.time(1))
    return (t + dt.timedelta(hours=1)).date() if on <= t < off else t.date()


def counted(rows):
    """one claimant's claim under one head from one accident, once"""
    groups = defaultdict(list)
    for r in rows:
        groups[(r["policy_ref"], r["vrm"], r["accident_date"], r["head_of_claim"])].append(r)
    out = []
    for g in groups.values():
        nums = {}
        for r in sorted(g, key=lambda x: (x["_note"], x["claim_ref"])):
            if r["claimant_no"]:
                nums.setdefault(r["claimant_no"], r)
        if nums:
            out.extend(nums.values())
        else:
            out.append(min(g, key=lambda x: (x["_note"], x["claim_ref"])))
    return out


def run(target, figures_path):
    bad = []
    F = json.load(open(figures_path))
    d2r = {r["postcode_district"]: r["sales_region"] for r in _rows(os.path.join(target, "postcode_district_sales_regions.csv"))}
    ftype = {r["representative_ref"]: r["firm_type"] for r in _rows(os.path.join(target, "claimant_representatives.csv"))}
    claims = _rows(os.path.join(target, "motor_claims_notified_2019_2026.csv"))
    for r in claims:
        r["_note"] = uk_date(r["notified_at"])
        r["_ay"] = int(r["accident_date"][:4])
        r["_reg"] = d2r[r["risk_postcode_district"]]
        r["_route"] = r["notified_by"] if r["notified_by"] != "Representative" else ftype[r["representative_ref"]]
    pc = [r for r in claims if r["product"] == "PC"]
    by_ay = defaultdict(list)
    for r in pc:
        by_ay[r["_ay"]].append(r)
    cnt = {ay: counted(v) for ay, v in by_ay.items()}
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(target, "earned_exposure_2019_2025.xlsx"), read_only=True)
    cy = Counter()
    rows = list(wb["2025"].iter_rows(values_only=True))
    for month, reg, prod, cov, v in rows[1:]:
        if prod == "PC":
            cy[reg] += v

    def at(ay):
        cut = dt.date(ay + 1, 9, 30)
        return [r for r in cnt[ay] if r["_note"] <= cut]

    def fac(years, key):
        n, d = Counter(), Counter()
        for ay in years:
            n.update(key(r) for r in cnt[ay])
            d.update(key(r) for r in at(ay))
        return {k: n[k] / d[k] for k in n if d[k]}

    def est(ay, years, key):
        f = fac(years, key)
        e = Counter()
        for r in at(ay):
            e[r["_reg"]] += f.get(key(r), 1.0)
        return e

    route = lambda r: r["_route"]
    e25 = est(2025, (2019, 2020, 2021, 2022), route)
    fr = {g: 100 * e25[g] / cy[g] for g in REG}
    order = sorted(REG, key=lambda g: -fr[g])
    if order[:2] != F["call"]:
        bad.append("call %s" % order[:2])
    for g in REG:
        if "%.1f" % fr[g] != "%.1f" % F["frequency"][g]:
            bad.append("frequency %s %.3f" % (g, fr[g]))
        if abs(cy[g] - F["earned_car_years"][g]) > 0.006:
            bad.append("car-years %s" % g)
    if "%.1f" % (fr[order[1]] - fr[order[2]]) != "%.1f" % F["gap"]:
        bad.append("gap")
    n25 = Counter(r["_reg"] for r in at(2025))
    if dict(n25) != F["notified_2025"]:
        bad.append("notified 2025")
    # the back-test: route within tolerance everywhere, the extract's own groupings outside it in Wessex
    e22 = est(2022, (2019, 2020, 2021), route)
    f22 = Counter(r["_reg"] for r in cnt[2022])
    worst = max(abs(100 * (e22[g] / f22[g] - 1)) for g in REG)
    if worst > 2.0 or abs(worst - F["backtest_2022_worst_pct"]["route"]) > 0.01:
        bad.append("route back-test %.2f" % worst)
    for nm, key in (("pooled", lambda r: 0), ("head", lambda r: r["head_of_claim"]), ("notified_by", lambda r: r["notified_by"])):
        e = est(2022, (2019, 2020, 2021), key)
        w = 100 * (e["Wessex"] / f22["Wessex"] - 1)
        if w > -2.0:
            bad.append("%s passes the back-test" % nm)
        e5 = est(2025, (2019, 2020, 2021, 2022), key)
        o5 = sorted(REG, key=lambda g: -e5[g] / cy[g])
        if o5[:2] != ["Mersey", "Severn"]:
            bad.append("%s names %s" % (nm, o5[:2]))
    # Ask A
    snap = "2026-09-30"
    vehicles = [v for v in _rows(os.path.join(target, "policy_vehicles_in_force_20260930.csv")) if v["product"] == "PC"
                and v["vehicle_on_cover_from"] <= snap and (not v["vehicle_off_cover_from"] or v["vehicle_off_cover_from"] > snap)
                and (not v["cancelled_from"] or v["cancelled_from"] > snap)]
    start = {v["policy_ref"]: v["term_start"] for v in vehicles}
    dist = {v["policy_ref"]: v["risk_postcode_district"] for v in vehicles}
    cov = {v["policy_ref"]: v["cover"] for v in vehicles}
    chg = [c for c in _rows(os.path.join(target, "policy_changes_2025_2026.csv")) if c["policy_ref"] in start
           and c["change_type"] in ("ADDRESS", "COVER") and start[c["policy_ref"]] <= c["effective_from"] <= snap]
    for c in sorted(chg, key=lambda c: (c["effective_from"], c["processed_on"], c["change_ref"])):
        if c["change_type"] == "ADDRESS":
            dist[c["policy_ref"]] = c["new_postcode_district"]
        else:
            cov[c["policy_ref"]] = c["new_cover"]
    a = Counter((d2r[dist[v["policy_ref"]]], cov[v["policy_ref"]]) for v in vehicles)
    for k, val in F["cars_on_cover"].items():
        g, cv = k.split("|")
        if a[(g, cv)] != val:
            bad.append("cars %s %d" % (k, a[(g, cv)]))
    # the documents, read back: a positive control, then the filed sentences
    from pypdf import PdfReader
    txt = lambda f: re.sub(r"\s+", " ", " ".join(p.extract_text() or "" for p in PdfReader(os.path.join(target, f)).pages))
    terms, std = txt("telematics_pilot_terms_2027.pdf"), txt("motor_reserving_standard_v4.pdf")
    if "Telematics pilot 2027" not in terms or "Motor Claims Reserving Standard" not in std:
        bad.append("PDF control")
    for s in ("the two sales regions whose private-car policies had the highest claim frequency in accident year 2025",
              "per 100 car-years earned in the region in 2025"):
        if s not in terms:
            bad.append("terms: %s" % s[:40])
    for s in ("closed three years after its last day", "measured on the closed accident years of the whole private-car book",
              "within two per cent"):
        if s not in std:
            bad.append("standard: %s" % s[:40])
    # the goldens
    gold = os.path.join(os.path.dirname(target), "golden")
    if os.path.exists(gold):
        g = load_workbook(os.path.join(gold, "telematics_pilot_regions_2027.xlsx"), read_only=True)["Frequency 2025"]
        vals = {row[0]: row[5] for row in g.iter_rows(min_row=5, max_row=9, values_only=True)}
        if any("%.1f" % vals[r] != "%.1f" % F["frequency"][r] for r in REG):
            bad.append("golden workbook frequencies")
        from pptx import Presentation
        deck = " ".join(sh.text_frame.text for s in Presentation(os.path.join(gold, "telematics_pilot_regions_2027.pptx")).slides
                        for sh in s.shapes if sh.has_text_frame)
        if "Mersey and Pennine host the 2027 telematics pilot" not in deck:
            bad.append("deck title")
    return bad


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    fj = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "figures.json")
    b = run(tgt, fj)
    print("verify: %s" % ("PASS" if not b else "FAIL: " + "; ".join(b)))
    sys.exit(1 if b else 0)
