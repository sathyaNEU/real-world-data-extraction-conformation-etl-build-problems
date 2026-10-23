"""Independent verifier: reads only the shipped bundle (target/), with the csv module, openpyxl and pypdf rather
than pandas, shares no state with the generator, and recomputes every graded figure in figures.json.

    python3 verify.py [target]      exit 0 when every figure reproduces"""
from __future__ import annotations

import csv
import datetime as dt
import json
import os
import re
import sys
from collections import defaultdict

import numpy as np
from openpyxl import load_workbook
from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
SEASON = (4, 5, 6, 7, 8, 9)
YEARS = range(2015, 2027)


def rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def sheet_rows(path, name):
    wb = load_workbook(path, read_only=True, data_only=True)
    ws = wb[name]
    it = ws.iter_rows(values_only=True)
    head = [str(h) for h in next(it)]
    out = [dict(zip(head, r)) for r in it]
    wb.close()
    return out


def pdf_text(path):
    return " ".join((p.extract_text() or "") for p in PdfReader(path).pages)


def main(target):
    fails = []
    def ok(cond, msg):
        if not cond:
            fails.append(msg)
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    f = lambda n: os.path.join(target, n)

    # documents carry the sentences the figures stand on (each through the same extractor, with a positive control)
    order = re.sub(r"\s+", " ", pdf_text(f("varner_watermaster_order_2027_season.pdf")))
    ok(len(order) > 500 and "limited, for the 2027 season, to 25 per cent of the season allotment" in order, "order: the limit sentence")
    ok("is suspended for the whole of the 2027 season" in order, "order: the suspension sentence")
    ins = re.sub(r"\s+", " ", pdf_text(f("hpa_member_load_forecast_instructions_2027.pdf")))
    ok("in service on 30 September 2026" in ins and "20 seasons 2007 to 2026" in ins, "instructions: class and normal")
    rate = re.sub(r"\s+", " ", pdf_text(f("hpa_wholesale_rate_schedule_w2_excerpt.pdf")))
    ok("All times in this schedule are Pacific prevailing time" in rate, "rate: prevailing time")

    # ---- weather
    eto = defaultdict(float)
    for r in rows(f("station247_daily_eto_2007-2026.csv")):
        d = dt.date.fromisoformat(r["date"])
        if d.month in SEASON:
            eto[d.year] += float(r["eto_in"])
    etn = sum(eto[y] for y in range(2007, 2027)) / 20.0

    # ---- bills
    xw = {r["legacy_acct_no"]: r["svc_no"] for r in rows(f("vvpud_cis_account_crosswalk_2020.csv"))}
    kwh = defaultdict(float)
    for r in rows(f("vvpud_ip_billing_2015-2026.csv")):
        s = r["svc_no"] or xw.get(r["acct_no"])
        y, m = int(r["bill_month"][:4]), int(r["bill_month"][5:7])
        kwh[(s, y, m)] += float(r["kwh"])
    reg = sheet_rows(f("vvpud_ip_service_register_2026-09-30.xlsx"), "IP services")
    active = {str(r["svc_no"]) for r in reg if r["status"] == "ACTIVE"}
    div = rows(f("varner_watermaster_diversion_statements_2015-2026.csv"))
    sen = {}
    dseas = defaultdict(float)
    for r in div:
        if r["measure"].startswith("VVPUD"):
            sen[r["measure"].split()[1]] = r["right_no"]
            dseas[(r["right_no"], int(r["year"]))] += float(r["af_diverted"])
    allot = {r["right_no"]: float(r["season_allotment_af"]) for r in
             sheet_rows(f("varner_decree_allotment_schedule_2026.xlsx"), "Schedule of allotments")}
    wb = load_workbook(f("vsga_extraction_reports_wy2017-wy2026.xlsx"), read_only=True, data_only=True)
    gsa = defaultdict(float)
    for name in wb.sheetnames:
        m = re.fullmatch(r"WY(\d{4})", name)
        if not m:
            continue
        wy = int(m.group(1))
        it = wb[name].iter_rows(values_only=True)
        head = [str(h) for h in next(it)]
        pcol = head.index("Power Account") if "Power Account" in head else head.index("power_source")
        acol = head.index("Volume (ac-ft)") if "Volume (ac-ft)" in head else head.index("extraction_af")
        for r in it:
            s = re.search(r"(\d{6})", str(r[pcol])).group(1)
            gsa[(s, wy)] += float(r[acol])
    wb.close()
    wells = {s for (s, wy) in gsa}

    def season(s, y):
        return sum(kwh.get((s, y, m), 0.0) for m in SEASON)

    def wyk(s, wy):
        return sum(kwh.get((s, wy - 1, m), 0.0) for m in (10, 11, 12)) + sum(kwh.get((s, wy, m), 0.0) for m in range(1, 10))

    juniors = [s for s in active if s not in sen]
    seniors = [s for s in active if s in sen]
    J = sum(season(s, 2022) for s in juniors) * etn / eto[2022]
    S = 0.0
    well_af = 0.0
    for s in seniors:
        right = sen[s]
        en = np.mean([season(s, y) * etn / eto[y] for y in YEARS])
        dn = np.mean([dseas[(right, y)] * etn / eto[y] for y in YEARS])
        cut = max(dn - 0.25 * allot[right], 0.0)
        if s in wells:
            wys = [wy for wy in range(2017, 2027) if (s, wy) in gsa]
            X = np.array([[dseas[(right, wy)], gsa[(s, wy)]] for wy in wys])
            Y = np.array([wyk(s, wy) for wy in wys])
            kr, kw = np.linalg.lstsq(X, Y, rcond=None)[0]
            S += en + cut * (kw - kr)
            well_af += cut
        else:
            kr = sum(season(s, y) for y in YEARS) / sum(dseas[(right, y)] for y in YEARS)
            S += en - cut * kr
    total = (J + S) / 1000.0
    ok(int(5000 * round(total / 5000)) == fig["call"]["forecast_mwh"], "call %.0f against %s" % (total, fig["call"]["forecast_mwh"]))
    ok(int(1000 * round(J / 1000 / 1000)) == fig["comp_bench_mwh"], "bench %.0f" % (J / 1000))
    ok(int(5000 * round(well_af / 5000)) == fig["comp_bottomland_well_af"], "well af %.0f" % well_af)

    # ---- delivery points: meter clock is standard time; billing months and hours prevailing
    dst0, dst1 = dt.datetime(2026, 3, 8, 2, 0), dt.datetime(2026, 11, 1, 1, 0)
    codes = {"VV-01": "RIVERSIDE", "VV-02": "MILL_SLOUGH", "VV-03": "BENCH", "VV-04": "CORWIN_ROAD"}
    per_day = defaultdict(int)
    A = defaultdict(float)
    hourly = defaultdict(float)
    for r in rows(f("hpa_dp_interval_export_2026.csv")):
        t = dt.datetime.strptime(r["interval_end"], "%Y-%m-%d %H:%M")
        if r["meter_no"] == "81-2207":
            per_day[t.date()] += 1
        if r["meter_no"] in ("81-2251", "81-3362", "81-1988", "81-4107"):
            continue
        if dst0 <= t < dst1:
            t += dt.timedelta(hours=1)
        k = codes[r["dp_code"]]
        tm = t - dt.timedelta(minutes=1)
        if tm.year == 2026 and tm.month in SEASON:
            A[(k, tm.month)] += float(r["kwh"])
        hourly[(k, tm.replace(minute=0))] += float(r["kwh"])
    ok(per_day[dt.date(2026, 3, 8)] == 96, "meter clock: 96 intervals on 8 March")
    for k in codes.values():
        for m in SEASON:
            ok(int(round(A[(k, m)])) == fig["a_" + k]["2026-%02d" % m], "A %s %d" % (k, m))
    for r in rows(f("hpa_2026_monthly_system_peaks.csv")):
        m = int(r["month"][5:7])
        if m not in SEASON:
            continue
        he = int(r["hour_ending"][:2])
        start = dt.datetime.fromisoformat(r["peak_date"]) + dt.timedelta(hours=he - 1)
        for k in codes.values():
            ok(int(round(hourly[(k, start)])) == fig["b_" + k]["2026-%02d" % m], "C %s %d" % (k, m))

    # ---- services by the delivery point their feeder was supplied from in the season
    src = {}
    for r in rows(f("vvpud_oms_feeder_sources.csv")):
        if r["effective_from"] <= "2026-04-01" and (not r["effective_to"] or r["effective_to"] >= "2026-09-30"):
            src[r["feeder"]] = codes[r["source_dp"]]
    nb = defaultdict(int)
    eb = defaultdict(float)
    for r in rows(f("vvpud_gis_service_points_2026-09-30.csv")):
        if r["svc_no"] in active:
            k = src[r["feeder"]]
            nb[k] += 1
            eb[k] += season(r["svc_no"], 2026) / 1000.0
    for k in codes.values():
        ok(nb[k] == fig["c_" + k]["services"], "B services %s" % k)
        ok(round(eb[k], 1) == fig["c_" + k]["billed_mwh"], "B energy %s" % k)

    print("verify: %d failures" % len(fails))
    for x in fails:
        print("  FAIL", x)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")))
