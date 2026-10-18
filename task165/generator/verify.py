"""task165 independent verifier. Reads only the shipped bundle (target/), the goldens, figures.json and submission.md,
on its own code path (csv, pyarrow, openpyxl, pypdf and python-docx readers, its own season, clock and regression
code; nothing from the generator), and recomputes the call, both components, the two rivals the write-up names,
every ask figure and each figure's distance to its rounding edge. Every format the pack ships is read back, with a
positive control on the same extractor for each document that carries a filed sentence.

    python3 verify.py [target]"""
from __future__ import annotations

import csv
import datetime as dt
import json
import os
import re
import sys
from zoneinfo import ZoneInfo

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")
TZ = ZoneInfo("America/Toronto")
WINTERS = ["2021-22", "2022-23", "2023-24", "2024-25", "2025-26"]
OUT = []


def ok(label, cond, detail=""):
    OUT.append(bool(cond))
    print("%s %-72s %s" % ("PASS" if cond else "FAIL", label[:72], detail))


def season(d: dt.date):
    if d.month >= 11:
        return "%d-%02d" % (d.year, (d.year + 1) % 100)
    if d.month <= 3:
        return "%d-%02d" % (d.year - 1, d.year % 100)
    return None


def edge(v, u):
    return u / 2 - abs(v - round(v / u) * u)


def rows_csv(name):
    with open(os.path.join(TARGET, name), encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def pdf(name):
    import pypdf
    r = pypdf.PdfReader(os.path.join(TARGET, name))
    return re.sub(r"\s+", " ", " ".join(p.extract_text() for p in r.pages))


def wfit(x, y, w):
    """Weighted least squares line y = a + b x."""
    sw = w.sum()
    mx, my = (w * x).sum() / sw, (w * y).sum() / sw
    b = (w * (x - mx) * (y - my)).sum() / (w * (x - mx) ** 2).sum()
    return my - b * mx, b


def main():
    import openpyxl
    import pyarrow.parquet as pq

    # ---------------------------------------------------------------------------------------- documents
    plan = pdf("winter_maintenance_plan_2026-27.pdf")
    proc = pdf("road_salt_procurement_procedure_RO-PR-07.pdf")
    surv = pdf("dome_stock_survey_2026-09.pdf")
    ok("PDF plan read back (positive control: its title)", "Winter maintenance plan 2026-27" in plan)
    m = re.search(r"planning severity of ([\d.]+) WSI points", plan)
    sev = float(m.group(1)) if m else None
    ok("PDF plan files the planning severity", sev == 61.7, str(sev))
    ok("PDF plan files the dome stock rule and the per lane-km rates",
       "brought forward by the loads weighed in to it and out of it at the scale houses" in plan and
       "set in kilograms per lane-km" in plan)
    m = re.search(r"plant brine at (\d+) litres to the tonne of salt \(23 per cent salt by weight, ([\d.]+) kg a litre\)",
                  plan)
    rate, brine = (float(m.group(1)), float(m.group(2))) if m else (None, None)
    ok("PDF plan files the pre-wet rate and the brine's weight", rate == 40.0 and brine == 1.18, "%s, %s" % (rate, brine))
    ok("PDF procedure read back (positive control: its title)", "Road salt procurement" in proc)
    ok("PDF procedure 4.2 files the estimand and the rounding",
       "the additional rock salt the roads the change moves will need from 1 November to 31 March, over what they "
       "needed before it, in a winter at the planning severity" in proc and "rounded to the nearest 100 t" in proc)
    ok("PDF survey read back (positive control: its title)", "Salt dome stock survey" in surv)

    # ---------------------------------------------------------------------------------------- register, log, WSI
    reg = {r["segment_id"]: r for r in rows_csv("winter_route_register_2026-09-14.csv")}
    rev = rows_csv("route_audit_revision_log.csv")
    moves = [(r["segment_id"], dt.date.fromisoformat(r["effective_date"])) for r in rev
             if r["field"] == "PRIORITY" and r["old_value"] == "2" and r["new_value"] == "1"
             and reg[r["segment_id"]]["func_class"] == "COLLECTOR"]
    new = [s for s, e in moves if e == dt.date(2026, 8, 30)]
    old = [(s, e) for s, e in moves if e < dt.date(2026, 8, 30)]
    lk = {s: float(r["lane_km"]) for s, r in reg.items()}
    figs0 = json.load(open(os.path.join(HERE, "figures.json")))
    ok("CSV register and revision log: the new segments, 424.0 lane-km, and the earlier moves",
       len(new) == figs0["segments"] and abs(sum(lk[s] for s in new) - 424.0) < 1e-6 and
       len(old) == figs0["earlier_moves"], "%d new, %d earlier" % (len(new), len(old)))
    wb = openpyxl.load_workbook(os.path.join(TARGET, "storm_log_2021-22_to_2025-26.xlsx"), read_only=True)
    wsi, season_rows = {}, {}
    for w in WINTERS:
        rows = list(wb[w].iter_rows(values_only=True))
        hi = next(i for i, r in enumerate(rows) if r and any(str(c).strip().lower() in ("points", "wsi_points")
                                                             for c in r if c is not None))
        col = [str(c).strip().lower() if c is not None else "" for c in rows[hi]].index(
            "points" if "points" in [str(c).strip().lower() for c in rows[hi] if c is not None] else "wsi_points")
        tot = 0.0
        for r in rows[hi + 1:]:
            if r[0] is None or str(r[0]).lower().startswith("season"):
                if r[0] is not None:
                    season_rows[w] = float(r[col])
                continue
            tot += float(r[col])
        wsi[w] = round(tot, 6)
    wb.close()
    ok("XLSX storm log: five winters' WSI, Season WSI rows tie",
       all(abs(season_rows[w] - wsi[w]) < 1e-6 for w in season_rows) and len(season_rows) == 3,
       str({w: round(v, 1) for w, v in wsi.items()}))

    # ---------------------------------------------------------------------------------------- salt per segment-winter
    xw = {}
    for r in rows_csv("gis_segment_crosswalk_2023.csv"):
        xw.setdefault(r["legacy_segment_id"], []).append((r["segment_id"], float(r["length_share"])))
    salt = {}
    for r in rows_csv("avl_legacy_segment_shift_2021-11-01_2023-03-31.csv"):
        if r["MATL"] != "SALT":
            continue
        w = season(dt.date.fromisoformat(r["SHIFT_DATE"]))
        if w is None:
            continue
        for sid, sh in xw[r["SEG_ID"]]:
            salt[(sid, w)] = salt.get((sid, w), 0.0) + float(r["KG"]) / 1000.0 * sh
    t = pq.read_table(os.path.join(TARGET, "telematics_segment_passes_2023-10-01_2026-09-23.parquet"))
    cols = {c: t.column(c).to_pylist() for c in t.column_names}
    n_pass = len(cols["segment_id"])
    loc = [e.astimezone(TZ) for e in cols["entry_utc"]]
    for i in range(n_pass):
        if cols["material_code"][i] != "RS" or "-A" in cols["route_code"][i]:
            continue
        w = season(loc[i].date())
        if w is None:
            continue
        k = (cols["segment_id"][i], w)
        salt[k] = salt.get(k, 0.0) + cols["applied_t"][i]
    ok("PARQUET pass export read back (318,889 rows, UTC stamps)", n_pass > 25000 and
       cols["entry_utc"][0].tzinfo is not None, "%d rows" % n_pass)

    def rate(sid, ws):
        return sum(salt.get((sid, w), 0.0) for w in ws) / (lk[sid] * sum(wsi[w] for w in ws))

    # ---------------------------------------------------------------------------------------- the call
    X, G, Wt = [], [], []
    for sid, e in old:
        first = "%d-%02d" % (e.year, (e.year + 1) % 100)
        pre = WINTERS[:WINTERS.index(first)]
        post = WINTERS[WINTERS.index(first):]
        X.append(rate(sid, pre))
        G.append(rate(sid, post) - rate(sid, pre))
        Wt.append(lk[sid])
    X, G, Wt = map(np.array, (X, G, Wt))
    a, b = wfit(X, G, Wt)
    Ln = sum(lk[s] for s in new)
    x0 = sum(rate(s, WINTERS) * lk[s] for s in new) / Ln
    gold = (a + b * x0) * Ln * sev
    call = int(round(gold / 100.0) * 100)
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    ok("CALL the seasonal tonnage recomputes", call == figs["commitment_t"], "%.1f t -> %d" % (gold, call))
    ok("CALL a quarter-bin or more from its rounding edge", edge(gold, 100) >= 25, "%.1f t" % edge(gold, 100))
    own, gain = x0 * sev, gold / Ln
    ok("CALL components recompute (own Priority 2 salt, gain per lane-km)",
       round(own, 1) == figs["own_p2_t_per_lkm"] and round(gain, 1) == figs["gain_t_per_lkm"] and
       edge(own, 0.1) >= 0.015 and edge(gain, 0.1) >= 0.025, "%.4f, %.4f" % (own, gain))
    per_w = [sum(salt.get((s, w), 0.0) for s in new) / (Ln * wsi[w]) * sev for w in WINTERS]
    ok("CALL own Priority 2 salt rounds alike in every winter on its own", all(round(v, 1) == figs["own_p2_t_per_lkm"]
                                                                            for v in per_w),
       str([round(v, 3) for v in per_w]))
    # the rivals block 1 names
    tot = den = 0.0
    oldd = dict(old)
    for sid, r in reg.items():
        if r["func_class"] != "COLLECTOR" or r["priority"] != "1" or sid in new:
            continue
        ws = WINTERS
        if sid in oldd:
            e = oldd[sid]
            ws = WINTERS[WINTERS.index("%d-%02d" % (e.year, (e.year + 1) % 100)):]
        for w in ws:
            tot += salt.get((sid, w), 0.0)
            den += lk[sid] * wsi[w]
    r1 = (tot / den - x0) * Ln * sev
    r2 = (G * Wt).sum() / Wt.sum() * Ln * sev
    ok("RIVAL the Priority 1 collectors' rate less own salt files another bin", round(r1 / 100) * 100 == 2600,
       "%.1f t" % r1)
    ok("RIVAL the earlier moves' average gain files another bin", round(r2 / 100) * 100 == 1500, "%.1f t" % r2)
    ok("RIVAL both rivals at least 250 t from the golden", min(abs(r1 - gold), abs(gold - r2)) >= 250, "")

    # ---------------------------------------------------------------------------------------- Ask A
    yards = ["KLV", "MPF", "RDG", "LKS"]
    names = {"Kelvin Road Yard": "KLV", "Mapleford Yard": "MPF", "Ridge Yard": "RDG", "Lakeshore Yard": "LKS"}
    stock0, sday, cap_end = {}, {}, {}
    for nm, y in names.items():
        m = re.search(re.escape(nm) + r" (\d{1,2} September 2026) [\d,]+ [\d.]+ ([\d,]+\.\d)", surv)
        sday[y] = dt.datetime.strptime(m.group(1), "%d %B %Y").date()
        stock0[y] = float(m.group(2).replace(",", ""))
        m2 = re.search(r"TG-26-\d{3} " + re.escape(nm) + r" (2026-09-\d{2}) (\d{2}:\d{2}) (\d{2}:\d{2})", surv)
        end_utc = dt.datetime.strptime(m2.group(1) + " " + m2.group(3), "%Y-%m-%d %H:%M").replace(tzinfo=dt.timezone.utc)
        cap_end[y] = end_utc.astimezone(TZ).replace(tzinfo=None)
    ok("PDF survey: four domes' stock, survey day and capture end", len(stock0) == 4 and
       all(cap_end[y].date() == sday[y] for y in yards), str({y: str(cap_end[y])[5:16] for y in yards}))
    wb = openpyxl.load_workbook(os.path.join(TARGET, "scale_house_log_2026-08-24_to_2026-09-24.xlsx"), read_only=True)
    st = dict(stock0)
    for y in yards:
        rows = list(wb[y].iter_rows(values_only=True))
        h = list(rows[0])
        for r in rows[1:]:
            rec = dict(zip(h, r))
            when = dt.datetime.combine(rec["Date"].date(), dt.datetime.strptime(rec["Time in"], "%H:%M").time())
            rem = (rec["Remarks"] or "").upper()
            dome = "LKS" if ("LKS" in rem or "LAKESHORE" in rem) else ("MPF" if ("MPF" in rem or "MAPLEFORD" in rem)
                                                                       else y)
            if when <= cap_end[dome]:
                continue
            st[dome] += (1 if rec["Direction"] == "IN" else -1) * rec["Net kg"] / 1000.0
    wb.close()
    for r in rows_csv("northgrit_dispatch_2026-10_issued_2026-09-21.csv"):
        if r["status"] == "BOOKED" and r["delivery_date"][:7] == "2026-10":
            st[r["ship_to"][3:]] += float(r["planned_net_t"])
    capd = {r["yard"]: float(r["rated_capacity_t"]) for r in rows_csv("salt_dome_register.csv")}
    good = all(round(st[y], 1) == figs["stock_%s" % y] and round(capd[y] - st[y], 1) == figs["room_%s" % y]
               for y in yards)
    ok("ASK A every dome's stock and room recompute", good, str({y: round(st[y], 1) for y in yards}))
    ok("ASK A every figure clear of its rounding edge (from the recomputed values)",
       min(min(edge(st[y], 0.1), edge(capd[y] - st[y], 0.1)) for y in yards) >= 0.025,
       "%.4f" % min(min(edge(st[y], 0.1), edge(capd[y] - st[y], 0.1)) for y in yards))

    # ---------------------------------------------------------------------------------------- Ask B
    fleet = rows_csv("fleet_units_2026-09.csv")
    old_ctl = {r["unit_id"]: (dt.date.fromisoformat(r["controller_retrofit"]) if r["controller_retrofit"] else None)
               for r in fleet if r["spreader_controller"] == "M410" or r["controller_retrofit"]}
    art, seen = {}, set()
    for i in range(n_pass):
        rc = cols["route_code"][i]
        if "-A" not in rc or cols["material_code"][i] != "RS":
            continue
        d = loc[i].date()
        w = season(d)
        if w not in ("2023-24", "2024-25", "2025-26"):
            continue
        u = cols["unit_id"][i]
        k = (rc[:3], w)
        if u in old_ctl and (old_ctl[u] is None or d < old_ctl[u]):
            if cols["run_ref"][i] in seen:
                continue
            seen.add(cols["run_ref"][i])
            v = cols["applied_t"][i] - cols["prewet_l"][i] * brine / 1000.0
        else:
            v = cols["applied_t"][i]
        art[k] = art.get(k, 0.0) + v
    wb = openpyxl.load_workbook(os.path.join(TARGET, "kettlewood_material_returns_2023-24_to_2025-26.xlsx"),
                                read_only=True)
    for ws in wb.worksheets:
        rows = list(ws.iter_rows(values_only=True))
        h = list(rows[2])
        for r in rows[3:]:
            rec = dict(zip(h, r))
            if rec["Month"] is None:
                continue
            w = season(dt.date.fromisoformat(rec["Month"] + "-01"))
            if w == ws.title:
                art[(rec["City circuit"][:3], w)] = art.get((rec["City circuit"][:3], w), 0.0) + float(rec["Rock salt (t)"])
    wb.close()
    good = all(int(round(art[(y, w)])) == figs["art_%s_%s" % (y, w)] for y in yards for w in ("2023-24", "2024-25",
                                                                                                "2025-26"))
    ok("ASK B every yard-winter arterial figure recomputes to the tonne", good, "")
    ok("ASK B every figure clear of its whole-tonne rounding edge (from the recomputed values)",
       min(edge(v, 1.0) for v in art.values()) >= 0.25, "%.3f" % min(edge(v, 1.0) for v in art.values()))

    # ---------------------------------------------------------------------------------------- the other formats
    n_csv = sum(1 for f in os.listdir(TARGET) if f.endswith(".csv"))
    for f in sorted(os.listdir(TARGET)):
        if f.endswith(".csv"):
            rows_csv(f)
    ok("CSV every shipped CSV parses with a header", n_csv >= 10, "%d files" % n_csv)
    dic = openpyxl.load_workbook(os.path.join(TARGET, "data_dictionary.xlsx"), read_only=True)
    fields = [r for r in dic["Fields"].iter_rows(values_only=True)]
    dic.close()
    ok("XLSX dictionary read back (legacy KG in kilograms)",
       any(r[1] == "KG" and "kilograms" in r[2] for r in fields[1:]), "%d fields" % (len(fields) - 1))
    qb = openpyxl.load_workbook(os.path.join(TARGET, "qrt_frequent_network_2026_streets.xlsx"), read_only=True)
    streets = {r[1] for r in list(qb.worksheets[0].iter_rows(values_only=True))[4:] if r[1]}
    qb.close()
    ok("XLSX transit street list covers the 216 segments' streets", streets == {reg[s]["street"] for s in new},
       "%d streets" % len(streets))

    # ---------------------------------------------------------------------------------------- goldens and write-up
    gwb = openpyxl.load_workbook(os.path.join(TASK, "golden", "salt_commitment_2026-27.xlsx"), read_only=True)
    vals = [c for r in gwb["Commitment"].iter_rows(values_only=True) for c in r if c is not None]
    domes = [r for r in gwb["Domes 1 Nov 2026"].iter_rows(values_only=True)][1:5]
    arts = [r for r in gwb["Arterial salt"].iter_rows(values_only=True)][1:5]
    gwb.close()
    ok("GOLDEN workbook carries the call, both components and every ask figure as figures.json",
       call in vals and figs["own_p2_t_per_lkm"] in vals and figs["gain_t_per_lkm"] in vals and
       all(r[1] == figs["stock_%s" % y] and r[2] == figs["room_%s" % y] for r, y in zip(domes, yards)) and
       all(list(r[1:4]) == [figs["art_%s_%s" % (y, w)] for w in ("2023-24", "2024-25", "2025-26")]
           for r, y in zip(arts, yards)), "")
    from docx import Document
    memo = " ".join(p.text for p in Document(os.path.join(TASK, "golden",
                                                          "seasonal_salt_commitment_council_report.docx")).paragraphs)
    ok("GOLDEN council report read back: the commitment, its components, one chart",
       "{:,} t of rock salt".format(call) in memo and "%.1f t a lane-km" % figs["gain_t_per_lkm"] in memo and
       len(Document(os.path.join(TASK, "golden", "seasonal_salt_commitment_council_report.docx")).inline_shapes) == 1,
       "")
    sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
    want = ["{:,}".format(call), "%.1f" % figs["own_p2_t_per_lkm"], "%.1f" % figs["gain_t_per_lkm"]] + \
        ["{:,.1f}".format(figs[k]) for k in figs if k.startswith(("stock_", "room_"))] + \
        ["{:,} t".format(figs[k]) for k in figs if k.startswith("art_")]
    ok("WRITEUP every graded figure appears in submission.md at its stated rounding", all(x in sub for x in want),
       str([x for x in want if x not in sub][:4]))

    n_fail = OUT.count(False)
    print("\nverify: %d checks, %d failed" % (len(OUT), n_fail))
    sys.exit(1 if n_fail else 0)


if __name__ == "__main__":
    main()
