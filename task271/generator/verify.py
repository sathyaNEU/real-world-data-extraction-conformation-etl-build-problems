"""task271 independent verifier: reads every shipped file in its own format on its own code path (the xlsx parts as
XML, the PDFs' content streams through their ASCII85 and Flate filters, the csv and json as text) and recomputes the
call and every graded figure without importing the generator's analysis, then compares with figures.json.

    python3 task271/generator/verify.py [target]"""
import base64
import csv
import datetime as dt
import json
import math
import os
import re
import sys
import zipfile
import zlib
from xml.etree import ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
BAD = []


def ok(label, cond, detail=""):
    print("%-4s %-70s %s" % ("ok" if cond else "FAIL", label[:70], detail))
    if not cond:
        BAD.append(label)


# ------------------------------------------------------------------------------------------------- readers
def xlsx_rows(path, sheet_name):
    z = zipfile.ZipFile(path)
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
            shared.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    rid = None
    for s in wb.find("m:sheets", NS):
        if s.get("name") == sheet_name:
            rid = s.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
    target = [r.get("Target") for r in rels if r.get("Id") == rid][0]
    target = target.lstrip("/")
    if not target.startswith("xl/"):
        target = "xl/" + target
    root = ET.fromstring(z.read(target))
    out = []
    for row in root.find("m:sheetData", NS):
        vals = {}
        for c in row:
            ref = c.get("r")
            col = re.match(r"[A-Z]+", ref).group(0)
            idx = 0
            for ch in col:
                idx = idx * 26 + ord(ch) - 64
            t = c.get("t")
            v = c.find("m:v", NS)
            if t == "s":
                val = shared[int(v.text)]
            elif t == "inlineStr":
                val = "".join(x.text or "" for x in c.iter("{%s}t" % NS["m"]))
            elif v is not None:
                val = v.text
            else:
                val = None
            vals[idx] = val
        if vals:
            out.append([vals.get(i) for i in range(1, max(vals) + 1)])
    return out


def pdf_text(path):
    b = open(path, "rb").read()
    out = []
    for m in re.finditer(rb"<<(.*?)>>\s*stream\r?\n(.*?)endstream", b, re.S):
        d, data = m.group(1), m.group(2)
        if b"/Filter" not in d:
            continue
        if b"ASCII85Decode" in d:
            s = data.strip()
            if s.startswith(b"<~"):
                s = s[2:]
            if s.endswith(b"~>"):
                s = s[:-2]
            data = base64.a85decode(s, adobe=False)
        if b"FlateDecode" in d:
            try:
                data = zlib.decompress(data)
            except zlib.error:
                continue
        out.append(data)
    text = b"\n".join(out).decode("latin-1")
    pieces = re.findall(r"\((.*?)(?<!\\)\)\s*Tj|\[(.*?)\]\s*TJ", text, re.S)
    words = []
    for a, bb in pieces:
        if a:
            words.append(a)
        else:
            words.append("".join(re.findall(r"\((.*?)(?<!\\)\)", bb)))
    return " ".join(words).replace("\\(", "(").replace("\\)", ")")


def hhmm(s):
    h, m = s.split(":")
    return int(h) + int(m) / 60.0


def main(target):
    files = sorted(os.listdir(target))
    print("files:", len(files))
    # every format read
    pol = pdf_text(os.path.join(target, "catchable_allocation_policy_2026.pdf"))
    pro = pdf_text(os.path.join(target, "creel_survey_protocol_2026.pdf"))
    ok("PDF policy decodes and files the 500 line", "500 or more angler-hours per" in pol)
    ok("PDF policy files the angling day 05:00 to 22:00", "05:00 to 22:00" in pol)
    ok("PDF protocol decodes and gives the loops' departures", "09:20" in pro and "14:15" in pro)
    reg_rows = xlsx_rows(os.path.join(target, "lake_register_2026.xlsx"), "Lakes")
    hdr = reg_rows[0]
    reg = {}
    for r in reg_rows[1:]:
        d = dict(zip(hdr, r))
        reg[d["PPFS code"]] = {"name": d["Lake"], "vno": int(float(d["Vellacott no."])), "area": float(d["Surface area (ha)"]),
                               "stocked": d["Catchables stocked 2026"] == "yes", "reg": d["Regulation"]}
    ok("XLSX register read as XML: 24 lakes", len(reg) == 24)
    by_vno = {v["vno"]: k for k, v in reg.items()}
    by_tab = {v["name"][:-5]: k for k, v in reg.items()}

    # ---- the call, own code
    counts = {}
    for r in csv.DictReader(open(os.path.join(target, "survey_flight_counts_2026.csv"))):
        if r["boats"] == "":
            continue
        counts.setdefault(by_vno[int(r["lake_no"])], []).append(
            (dt.date.fromisoformat(r["survey_date"]), hhmm(r["time_over"]), int(r["boats"]), int(r["shore_anglers"])))
    parties = {}
    for r in csv.DictReader(open(os.path.join(target, "creel_interviews_2026.csv"))):
        fin = hhmm(r["finished"])
        st = hhmm(r["started"]) if r["started"] else fin - float(r["hours_fished"])
        parties.setdefault(by_tab[r["lake"]], []).append((int(r["party_size"]), r["fished_from"] == "boat", st, fin))
    season = [dt.date(2026, 5, 15) + dt.timedelta(days=i) for i in range(109)]
    hol = {dt.date(2026, 5, 18), dt.date(2026, 7, 1), dt.date(2026, 8, 3)}
    strata = {}
    for d in season:
        strata.setdefault((d.month, d.weekday() >= 5 or d in hol), []).append(d)
    est = {}
    for c, rows in parties.items():
        apb = sum(s for s, b, _, _ in rows if b) / sum(1 for s, b, _, _ in rows if b)
        w = [0.0] * 17
        for s, b, st, fin in rows:
            for h in range(17):
                lo, hi = max(st, 5 + h), min(fin, 6 + h)
                if hi > lo:
                    w[h] += s * (hi - lo)
        tot = sum(w)
        sh = [x / tot for x in w]
        day = {}
        for d, t, bo, so in counts[c]:
            day.setdefault(d, []).append((bo * apb + so) / sh[int(t) - 5])
        season_h = 0.0
        for k, days in strata.items():
            vals = [sum(day[d]) / len(day[d]) for d in days if d in day]
            season_h += len(days) * sum(vals) / len(vals)
        est[c] = season_h / reg[c]["area"]
    high = sorted(c for c in reg if reg[c]["stocked"] and est[c] >= 500)
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    ok("call recomputed on its own path matches figures.json", high == fig["call"]["high_use_codes"], ", ".join(high))
    ok("the golden chart's bars recompute on this path (the drawing, nearest 10)",
       all(int(math.floor(est[c] / 10 + 0.5) * 10) == fig["chart_bars_per_ha"][reg[c]["name"]]
           for c in reg if reg[c]["stocked"]))
    ok("this path keeps every high-use lake above the high band and every standard lake below the standard band",
       all(est[c] > fig["bands"]["high_use_above"] for c in high) and
       all(est[c] < fig["bands"]["standard_below"] for c in reg if reg[c]["stocked"] and c not in high))

    # ---- releases, own code
    tr = xlsx_rows(os.path.join(target, "quillet_creek_trip_sheets_2026.xlsx"), "Trips 2026")
    th = tr[0]
    trips = {}
    for r in tr[1:]:
        d = dict(zip(th, r))
        if not d.get("Trip"):
            continue
        trips.setdefault(d["Trip"], {"date": dt.date.fromisoformat(d["Date"][:10]), "rw": int(float(d["Raceway"])),
                                     "load": float(d["Net load (kg)"]), "tank": d.get("Tank temp (C)") not in (None, "")})
    cw = {}
    for r in csv.DictReader(open(os.path.join(target, "quillet_creek_raceway_numbers.csv"))):
        cw[int(r["old_raceway"])] = int(r["new_raceway"])
        renum = dt.date.fromisoformat(r["from_date"])
    samp = []
    for r in csv.DictReader(open(os.path.join(target, "quillet_creek_raceway_samples_2026.csv"))):
        d = dt.date.fromisoformat(r["sample_date"])
        rw = int(r["raceway"])
        samp.append((d, rw if d >= renum else cw[rw], int(r["fish_counted"]) * 1000.0 / int(r["sample_g"])))
    drops = json.load(open(os.path.join(target, "quillet_creek_drop_tallies_2026.json")))["records"]
    fish = {}
    for tid, t in trips.items():
        rw = t["rw"] if t["tank"] else cw[t["rw"]]
        fpk = max((s for s in samp if s[1] == rw and s[0] <= t["date"]), key=lambda s: s[0])[2]
        ds = [x for x in drops if x["tripId"] == tid]
        nets = sum(x["nets"] for x in ds)
        for x in ds:
            fish[x["lakeCode"]] = fish.get(x["lakeCode"], 0.0) + t["load"] * x["nets"] / nets * fpk - x["doaFish"]
    rel = {reg[c]["name"]: int(math.floor(v / 100 + 0.5) * 100) for c, v in fish.items()}
    ok("JSON drop tallies + XLSX trip sheets: releases recomputed match figures.json", rel == fig["releases_alive"])

    # ---- warm days, own code
    dep = []
    for r in csv.DictReader(open(os.path.join(target, "logger_deployments_2026.csv"))):
        dep.append((r["logger_serial"], r["lake_code"], float(r["depth_m"]),
                    dt.datetime.strptime(r["deployed"], "%Y-%m-%d %H:%M"),
                    dt.datetime.strptime(r["retrieved"], "%Y-%m-%d %H:%M") if r["retrieved"] else None))
    raw = {}
    for r in csv.DictReader(open(os.path.join(target, "lake_temperature_loggers_2026.csv"))):
        raw.setdefault(r["Logger SN"], []).append((dt.datetime.strptime(r["Date Time"], "%Y-%m-%d %H:%M"),
                                                   float(r["Temp (C)"])))
    sums = {}
    for s, recs in raw.items():
        hours = [0.0] * 24
        n = [0] * 24
        for t, v in recs:
            hours[t.hour] += v
            n[t.hour] += 1
        peak = max(range(24), key=lambda h: hours[h] / max(n[h], 1))
        shift = -7 if peak in (21, 22, 23, 0, 1, 2, 3) else 0
        for t, v in recs:
            tl = t + dt.timedelta(hours=shift)
            for ss, lake, depth, a, b in dep:
                if ss == s and a <= tl and (b is None or tl <= b):
                    if depth < 2 and dt.date(2026, 7, 1) <= tl.date() <= dt.date(2026, 8, 31):
                        k = (lake, tl.date())
                        sums.setdefault(k, [0.0, 0])
                        sums[k][0] += v
                        sums[k][1] += 1
                    break
    warm = {}
    for (lake, d), (a, n) in sums.items():
        warm.setdefault(reg[lake]["name"], 0)
        if a / n > 20.0:
            warm[reg[lake]["name"]] += 1
    ok("CSV loggers + deployments: warm days recomputed match figures.json", warm == fig["warm_days"])

    # ---- goldens read back
    g = xlsx_rows(os.path.join(TASK, "golden", "stocking_tiers_2027.xlsx"), "Tiers 2027")
    gh = g[0]
    tiers = {dict(zip(gh, r))["Lake"]: dict(zip(gh, r))["Tier 2027"] for r in g[1:] if r and r[0] and str(r[0]).startswith("PP-")}
    ok("golden workbook's tiers match the call", sorted(n for n, t in tiers.items() if t == "High use") ==
       sorted(fig["call"]["high_use"]))
    z = zipfile.ZipFile(os.path.join(TASK, "golden", "stocking_board_note_2027.docx"))
    body = re.sub(r"<[^>]+>", "", z.read("word/document.xml").decode("utf-8"))
    ok("golden note names every high-use lake", all(n.replace(" Lake", "") in body for n in fig["call"]["high_use"]))
    ok("golden note carries the chart", any(n.startswith("word/media/") for n in z.namelist()))
    print("\nverify: %d failed" % len(BAD))
    return 1 if BAD else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")))
