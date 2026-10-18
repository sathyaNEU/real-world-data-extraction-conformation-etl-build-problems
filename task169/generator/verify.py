"""verify.py: an independent reader of the shipped bundle. It imports nothing from the generator: its own csv,
pyarrow, openpyxl and pypdf readers, its own clock conversion, its own regression and its own replay,
then compares what it finds with figures.json, the golden workbook and note, and submission.md.

    python3 verify.py <target>"""
import csv
import json
import math
import os
import re
import sys
from datetime import date, datetime, timedelta, timezone

import numpy as np
import openpyxl
import pyarrow.parquet as pq
from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
OK = []


def ok(label, cond, detail=""):
    OK.append((label, bool(cond)))
    print("%s  %-70s %s" % ("PASS" if cond else "FAIL", label[:70], detail))


def bst(dt_utc):
    """Europe/London for any instant: BST from 01:00 UTC on the last Sunday of March to 01:00 UTC on the last Sunday
    of October"""
    y = dt_utc.year
    def last_sun(m):
        d = date(y, m, 31)
        while d.weekday() != 6:
            d -= timedelta(days=1)
        return datetime(d.year, d.month, d.day, 1, 0)
    a, b = last_sun(3), last_sun(10)
    return dt_utc + timedelta(hours=1) if a <= dt_utc < b else dt_utc


def summer(y):
    return [date(y, 6, 1) + timedelta(days=i) for i in range(92)]


def main(target):
    # ---------------------------------------------------------------- the documents
    def pdf(name):
        return "\n".join(p.extract_text() for p in PdfReader(os.path.join(target, name)).pages)
    pol = re.sub(r"\s+", " ", pdf("cycleway_widening_allocation_policy_2026.pdf"))
    guide = pdf("cycle_design_guide_2023_section4.pdf")
    bands = [(float(a), float(b), int(c.replace(",", ""))) for a, b, c in
             re.findall(r"(\d\.\d) to under (\d\.\d)\s+([\d,]+)", guide)]
    ok("policy files the crowded day and the three-summer replay",
       "06:00 to 22:00 local time" in pol and "mean, over those three summers" in pol)
    ok("guide Table 4.3 read by a second PDF reader", len(bands) == 6 and bands[1] == (2.5, 3.0, 650), str(bands[:2]))
    # ---------------------------------------------------------------- register, inventory, calendar, weather
    reg = list(openpyxl.load_workbook(os.path.join(target, "counter_register.xlsx"), read_only=True)["Register"]
               .iter_rows(values_only=True))
    rh = reg[0]
    reg = [dict(zip(rh, r)) for r in reg[1:]]
    inv = list(openpyxl.load_workbook(os.path.join(target, "cycleway_path_inventory_2026.xlsx"), read_only=True)["Segments"]
               .iter_rows(values_only=True))
    ih = inv[0]
    inv = [dict(zip(ih, r)) for r in inv[1:]]
    cap, cw_of = {}, {}
    for s in inv:
        if s["counter_id"]:
            w = float(s["min_width_m"])
            cap[s["segment_ref"]] = [c for a, b, c in bands if a <= w < b][0]
            cw_of[s["segment_ref"]] = s["cycleway"]
    seg_by_id = {r["counter_id"]: r["segment_ref"] for r in reg}
    seg_by_site = {r["legacy_site_name"]: r["segment_ref"] for r in reg}
    hol, bank = [], set()
    for r in csv.DictReader(open(os.path.join(target, "school_term_dates_2023-2027.csv"))):
        if r["type"] == "school holiday":
            hol.append((date.fromisoformat(r["first_day"]), date.fromisoformat(r["last_day"])))
        if r["type"] == "bank holiday":
            bank.add(date.fromisoformat(r["first_day"]))
    weekend = lambda d: d.weekday() >= 5 or d in bank
    term = lambda d: not weekend(d) and not any(a <= d <= b for a, b in hol)
    wx = {}
    for r in csv.DictReader(open(os.path.join(target, "weather_station_daily_2024-01-01_2026-09-30.csv"))):
        if r["tmax_c"]:
            wx[date.fromisoformat(r["date"])] = (float(r["tmax_c"]), float(r["rain_mm"]))
    # ---------------------------------------------------------------- the counts on local clock hours
    flows = {s: {y: np.full((92, 24), np.nan) for y in (2024, 2025, 2026)} for s in cap}
    with open(os.path.join(target, "counts_summer2024_legacy.csv"), encoding="utf-8") as fh:
        lines = fh.read().splitlines()[2:]
    for line in lines:
        site, d, h, c1, c2 = line.split(";")
        if c1 and c2:
            dd = datetime.strptime(d, "%d/%m/%Y").date()
            flows[seg_by_site[site]][2024][(dd - date(2024, 6, 1)).days, int(h[:2])] = int(c1) + int(c2)
    t = pq.read_table(os.path.join(target, "counts_summer2025_2026.parquet")).to_pandas()
    t["local"] = [bst(x.to_pydatetime().replace(tzinfo=None)) for x in t["timestamp_utc"]]
    ok("platform timestamps are hour beginnings in UTC covering each summer's local days",
       min(t["local"]).date() == date(2025, 6, 1) and max(t["local"]).date() == date(2026, 8, 31))
    acc = {}
    for cid, loc, c, st in zip(t["counter_id"], t["local"], t["count"], t["status"]):
        k = (seg_by_id[cid], loc.year, (loc.date() - date(loc.year, 6, 1)).days, loc.hour)
        a = acc.setdefault(k, [0, True])
        a[0] += int(c)
        a[1] = a[1] and st == "ok"
    for (s, y, i, h), (v, good) in acc.items():
        if good:
            flows[s][y][i, h] = v
    # ---------------------------------------------------------------- growth by counter, weekday or weekend, hour
    def fit(code, wkend, h, weather=True):
        X, Y = [], []
        for y in (2024, 2025, 2026):
            for i, d in enumerate(summer(y)):
                if weekend(d) != wkend or d not in wx or np.isnan(flows[code][y][i, h]) or flows[code][y][i, h] <= 0:
                    continue
                tm, rn = wx[d]
                X.append([1, y - 2026] + ([1.0 if rn >= 1.0 else 0.0, tm - 20.0] if weather else []))
                Y.append(math.log(flows[code][y][i, h]))
        b = np.linalg.lstsq(np.array(X), np.array(Y), rcond=None)[0]
        return math.exp(b[1])

    def crowded(gfun):
        out = {}
        for cw in sorted(set(cw_of.values())):
            segs = [s for s in cap if cw_of[s] == cw]
            tot = 0
            for y in (2024, 2025, 2026):
                days = summer(y)
                hit = np.zeros(92, bool)
                for s in segs:
                    for i, d in enumerate(days):
                        for h in range(6, 22):
                            v = flows[s][y][i, h]
                            if not np.isnan(v) and v * gfun(s, weekend(d), h) ** (2027 - y) > cap[s]:
                                hit[i] = True
                tot += int(hit.sum())
            out[cw] = tot / 3
        return out
    G = {(s, we, h): fit(s, we, h) for s in cap for we in (False, True) for h in range(24)}
    res = crowded(lambda s, we, h: G[(s, we, h)])
    call = max(res, key=res.get)
    ok("independent golden names CW1 Tolland Road", call == "CW1", str({k: round(v, 1) for k, v in res.items()}))
    hits = {}
    for y in (2024, 2025, 2026):
        for i, d in enumerate(summer(y)):
            for h in range(6, 22):
                v = flows["CW1-03"][y][i, h]
                if not np.isnan(v) and v * G[("CW1-03", weekend(d), h)] ** (2027 - y) > cap["CW1-03"]:
                    hits[(term(d), h)] = hits.get((term(d), h), 0) + 1
    ok("Tolland Bridge crowds only from 08:00, mostly on term weekdays",
       {h for (tm, h) in hits} == {8} and hits.get((True, 8), 0) >= 0.95 * sum(hits.values()), str(hits))
    # positive control: the default path (each counter's 2025-26 growth in total riders) files another cycleway
    tot = {s: (np.nansum(flows[s][2026]) / np.nansum(flows[s][2025])) for s in cap}
    dft = crowded(lambda s, we, h: tot[s])
    ok("positive control: the default path files Estuary Path (CW3)", max(dft, key=dft.get) == "CW3",
       str({k: round(v, 1) for k, v in dft.items()}))
    # ---------------------------------------------------------------- ask A
    cw = {}
    for r in csv.DictReader(open(os.path.join(target, "count_week_15min_2026-05-11_15.csv"))):
        st = datetime.strptime(r["timestamp_utc"], "%Y-%m-%dT%H:%M:%SZ")
        loc = st if r["counter_id"] in ("CVC-1112", "CVC-1207") else bst(st)
        k = (r["counter_id"], loc - timedelta(minutes=15))
        cw[k] = cw.get(k, 0) + int(r["count"])
    wb = openpyxl.load_workbook(os.path.join(target, "volunteer_count_may2026.xlsx"), read_only=True)
    ask_a = {}
    for ws in wb.worksheets:
        rows = list(ws.iter_rows(values_only=True))
        cid = re.search(r"CVC-\d{4}", rows[1][1]).group(0)
        day = datetime.strptime(rows[2][1], "%A %d %B %Y")
        C = V = 0
        for r in rows:
            m = re.match(r"^(\d\d):(\d\d)-(\d\d):(\d\d)$", str(r[0] or ""))
            if not m:
                continue
            a = day.replace(hour=int(m.group(1)), minute=int(m.group(2)))
            b = day.replace(hour=int(m.group(3)), minute=int(m.group(4)))
            qs = [a + timedelta(minutes=15 * k) for k in range(int((b - a).total_seconds() // 900))]
            if all((cid, q) in cw for q in qs):
                C += sum(cw[(cid, q)] for q in qs)
                V += int(r[1]) + int(r[2])
        ask_a[cid] = (C, round(100.0 * (V - C) / V, 1))
    # ---------------------------------------------------------------- ask B
    log = list(csv.DictReader(open(os.path.join(target, "counter_maintenance_log_2024-2026.csv"))))
    cur = {r["legacy_site_name"]: r["counter_id"] for r in reg if r["type"] == "dashboard" and not r["unit_of_record_to"]}
    jobs = {r["job_no"]: r for r in log}
    spans = {}
    for r in log:
        if r["site"] not in cur or not r["downtime"]:
            continue
        if r["parent_job"] and r["downtime"] == jobs[r["parent_job"]]["downtime"]:
            continue
        a = datetime.strptime(r["reported"], "%d/%m/%Y %H:%M")
        b = datetime.strptime(r["closed"], "%d/%m/%Y %H:%M")
        spans.setdefault(cur[r["site"]], []).append((a, b))

    def utc(local):            # local wall clock to UTC (the log's times are local)
        return local - timedelta(hours=1) if bst(local - timedelta(hours=1)) == local else local
    ask_b = {}
    for cid, sp in spans.items():
        sp.sort()
        merged = []
        for a, b in sp:
            if merged and a <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], b)
            else:
                merged.append([a, b])
        mins, n = 0, 0
        for a, b in merged:
            lo, hi = max(a, datetime(2025, 1, 1)), min(b, datetime(2026, 1, 1))
            if lo < hi:
                mins += (utc(hi) - utc(lo)).total_seconds() / 60
                n += 1
        ask_b[cid] = (round(mins / 60.0, 1), n)
    # ---------------------------------------------------------------- against figures.json, the goldens and the write-up
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    ok("figures.json call and segment", fig["call"] == call and fig["segment"] == "CW1-03" and fig["capacity"] == cap["CW1-03"])
    ok("figures.json ask A equals the independent read",
       all((fig["ask_a"][c]["counter"], fig["ask_a"][c]["shortfall"]) == v for c, v in ask_a.items()), str(ask_a))
    ok("figures.json ask B equals the independent read",
       all((fig["ask_b"][c]["hours"], fig["ask_b"][c]["stoppages"]) == v for c, v in ask_b.items()), str(ask_b))
    gw = openpyxl.load_workbook(os.path.join(TASK, "golden", "cycleway_widening_2027.xlsx"), read_only=True)
    va = [r for r in gw["Volunteer count check"].iter_rows(min_row=2, values_only=True) if r[1] and str(r[1]).startswith("CVC")]
    ok("golden workbook carries every ask A figure", all((r[4], r[6]) == ask_a[r[1]] for r in va) and len(va) == 6)
    vb = [r for r in gw["Counter downtime 2025"].iter_rows(min_row=2, values_only=True) if r[0] and str(r[0]).startswith("CVC")]
    ok("golden workbook carries every ask B figure", all((r[2], r[3]) == ask_b[r[0]] for r in vb) and len(vb) == 6)
    rec = [r for r in gw["Recommendation"].iter_rows(values_only=True) if r[0]]
    ok("golden workbook states the cycleway, segment and hours",
       any("Tolland Road (CW1)" in str(r[1]) for r in rec) and any("Tolland Bridge (CW1-03)" in str(r[1]) for r in rec) and
       any("08:00 to 09:00" in str(r[1]) for r in rec))
    note = " ".join(" ".join(pg.extract_text() for pg in PdfReader(os.path.join(TASK, "golden", "widening_note_2027.pdf"),
                                                                     strict=True).pages).split())
    ok("golden note recommends Tolland Road at Tolland Bridge, 08:00 to 09:00", "Tolland Road (CW1)" in note and
       "Tolland Bridge" in note and "08:00 and 09:00" in note)
    sub = open(os.path.join(TASK, "submission.md")).read()
    lines_a = re.findall(r"- (.+?) \((CVC-\d{4})\): ([\d,]+) riders, shortfall ([\d.]+) per cent", sub)
    ok("submission ask A lines equal the independent read", len(lines_a) == 6 and all(
        (int(n.replace(",", "")), float(s)) == ask_a[c] for _, c, n, s in lines_a))
    lines_b = re.findall(r"- (CVC-\d{4}) \(.+?\): ([\d.]+) hours, (\d+) stoppages", sub)
    ok("submission ask B lines equal the independent read", len(lines_b) == 6 and all(
        (float(h), int(n)) == ask_b[c] for c, h, n in lines_b))
    fails = [x for x in OK if not x[1]]
    print("\nverify: %d checks, %d FAIL" % (len(OK), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")))
