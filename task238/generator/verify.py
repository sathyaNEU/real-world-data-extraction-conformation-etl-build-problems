"""Independent verifier: reads every shipped file back on its own code path (the csv module for CSV, the workbook
XML straight from the zip, json for the printer log, its own ASCII85 and Flate decoder for the PDF) and recomputes
the call and every graded figure without importing analysis.py, world.py, pack.py or params.py.

    python3 task238/generator/verify.py           # exit 1 on any mismatch with figures.json
"""
import base64
import csv
import datetime as dt
import json
import os
import re
import sys
import zipfile
import zlib
import xml.etree.ElementTree as ET
from collections import defaultdict
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
HFX = ZoneInfo("America/Halifax")
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
FAIL = []


def say(cond, what, detail=""):
    print("%-4s %s %s" % ("OK" if cond else "FAIL", what, detail))
    if not cond:
        FAIL.append(what)


def half_up(x, nd=0):
    from decimal import Decimal, ROUND_HALF_UP
    q = Decimal(1).scaleb(-nd)
    v = Decimal(repr(float(x))).quantize(q, rounding=ROUND_HALF_UP)
    return float(v) if nd else int(v)


# ------------------------------------------------------------------------------------------------ readers
def csv_rows(name):
    with open(os.path.join(T, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def xlsx_sheets(name):
    """every sheet as a list of rows (lists of cell strings), read from the OOXML parts directly"""
    out = {}
    with zipfile.ZipFile(os.path.join(T, name)) as z:
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
                shared.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        rmap = {r.get("Id"): r.get("Target") for r in rels}
        for sh in wb.find("m:sheets", NS):
            rid = sh.get("{%s}id" % NS["r"])
            path = "xl/" + rmap[rid].lstrip("/").replace("xl/", "")
            root = ET.fromstring(z.read(path))
            rows = []
            for row in root.iter("{%s}row" % NS["m"]):
                cells = {}
                for c in row.findall("m:c", NS):
                    ref = c.get("r")
                    col = 0
                    for ch in re.match(r"[A-Z]+", ref).group(0):
                        col = col * 26 + ord(ch) - 64
                    v = c.find("m:v", NS)
                    t = c.get("t")
                    if t == "s":
                        val = shared[int(v.text)]
                    elif t == "inlineStr":
                        val = "".join(x.text or "" for x in c.iter("{%s}t" % NS["m"]))
                    else:
                        val = v.text if v is not None else None
                    cells[col] = val
                if cells:
                    rows.append([cells.get(i) for i in range(1, max(cells) + 1)])
            out[sh.get("name")] = rows
    return out


def excel_date(v):
    x = float(v)
    return dt.datetime(1899, 12, 30) + dt.timedelta(days=x)


def pdf_text(name):
    raw = open(os.path.join(T, name), "rb").read()
    chunks = []
    for m in re.finditer(rb"stream\r?\n", raw):
        start = m.end()
        end = raw.find(b"endstream", start)
        head = raw[max(0, m.start() - 200):m.start()]
        body = raw[start:end].rstrip(b"\r\n")
        try:
            if b"ASCII85Decode" in head:
                body = base64.a85decode(body.rstrip(b"~>") if body.endswith(b"~>") else body, adobe=False)
            if b"FlateDecode" in head:
                body = zlib.decompress(body)
        except Exception:
            continue
        chunks.append(body.decode("latin-1"))
    pieces = re.findall(r"\(((?:\\.|[^\\)])*)\)", " ".join(chunks))
    return re.sub(r"\s+", " ", " ".join(p.replace("\\(", "(").replace("\\)", ")") for p in pieces))


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    files = meta["files"]
    name = {v["source"].split(",")[0]: k for k, v in files.items()}

    def find(pat):
        return [f for f in files if re.search(pat, f)][0]

    # --- the standard (PDF): the definition, the line, the effective time
    std = pdf_text(find(r"^PI-2"))
    say(len(std) > 500, "pdf.extracted", "%d chars" % len(std))
    say("rang up at the price shown on the item's shelf-edge label at the moment of the scan" in std,
        "pdf.accuracy_sentence")
    say("below 99.0 per cent goes on Price Watch" in std, "pdf.watch_line")
    say("00:00 on the Thursday that opens the flyer week" in std, "pdf.effect_time")
    line = 99.0

    # --- directory (XLSX)
    sh = xlsx_sheets(find(r"^store_directory"))
    dir_rows = sh["Stores"][1:]
    by_name = {r[2]: int(float(r[0])) for r in dir_rows}
    by_dev = {r[6]: int(float(r[0])) for r in dir_rows}
    stores = sorted(by_name.values())
    say(len(stores) == 14, "xlsx.directory", "%d stores" % len(stores))

    # --- hourly scans (CSV)
    hourly = defaultdict(dict)
    total = defaultdict(int)
    for r in csv_rows(find(r"^pos_hourly")):
        s, d, h, n = int(r["store_no"]), r["business_date"], int(r["hour_start"][:2]), int(r["item_scans"])
        hourly[(s, d)][h] = n
        total[s] += n

    # --- movement (CSV)
    U = defaultdict(int)
    changed = defaultdict(set)
    for r in csv_rows(find(r"^price_change_item_movement")):
        U[(int(r["store_no"]), r["changeover_date"])] += int(r["units_changeover_thursday"])
        changed[(int(r["store_no"]), r["changeover_date"])].add(r["upc"])
    cos = sorted({d for (_, d) in U})

    # --- printer fleet (JSON lines)
    batch = {}
    with open(os.path.join(T, find(r"^label_printer")), encoding="utf-8") as f:
        for line_ in f:
            j = json.loads(line_)
            m = re.match(r"PCB (\d{2})([A-Z]{3})(\d{2})", j["job_name"])
            if not m or j["status"] != "COMPLETED":
                continue
            mon = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"].index(m.group(2))
            d = dt.date(2000 + int(m.group(3)), mon + 1, int(m.group(1))).isoformat()
            t = dt.datetime.fromisoformat(j["printed_local"])
            batch[(by_dev[j["device"]], d)] = (t, int(j["labels"]))
    say(len(batch) == 14 * len(cos), "jsonl.batches", "%d batches" % len(batch))

    # --- checks (XLSX, three monthly sheets, December with one more column)
    checks = []
    for nm, rows in xlsx_sheets(find(r"^thursday_changeover")).items():
        hdr = rows[2]
        ix = {h: i for i, h in enumerate(hdr)}
        for r in rows[3:]:
            if not r or r[0] is None:
                continue
            d = excel_date(r[ix["Visit date"]]).date()
            hh, mm = r[ix["Time checked"]].split(":")
            t = dt.datetime(d.year, d.month, d.day, int(hh), int(mm), tzinfo=HFX)
            checks.append((by_name[r[ix["Store"]]], t, float(r[ix["Label price"]]), float(r[ix["Register price"]])))
    say(len(checks) == 14 * 20 * len(cos), "xlsx.checks", "%d labels" % len(checks))

    # pace: least squares on the share still old against minutes since print over the batch size
    import numpy as np
    obs = []
    for (s, t, lab, reg) in checks:
        P_, L = batch[(s, t.date().isoformat())]
        m = (t - P_).total_seconds() / 60
        if m > 0:
            obs.append((m / L, abs(lab - reg) > 0.004))
    x = np.array([o[0] for o in obs])
    y = np.array([o[1] for o in obs], float)
    best, bl = None, 1e18
    for rr in np.arange(1.0, 12.0, 0.01):
        q = np.clip(1 - x * rr, 0, 1)
        sse = float(np.sum((y - q) ** 2))
        if sse < bl:
            bl, best = sse, rr
    rate = best

    # --- audits (CSV): stray labels outside changeover windows
    num = den = 0
    for r in csv_rows(find(r"^price_audit")):
        s = by_name[r["store"]]
        t = dt.datetime.strptime(r["audit_started"], "%Y-%m-%d %H:%M").replace(tzinfo=HFX)
        wk = max(c for c in cos if c <= t.date().isoformat())
        if r["ean"][1:] in changed[(s, wk)]:
            P_, L = batch[(s, wk)]
            if (t - P_).total_seconds() / 60 < L / rate + 5:
                continue
        den += 1
        num += abs(float(r["shelf_price"]) - float(r["register_price"])) > 0.004
    stray = num / den

    # --- the call
    acc = {}
    for s in stores:
        st = 0.0
        for d in cos:
            hrs = hourly[(s, d)]
            P_, L = batch[(s, d)]
            day = sum(hrs.values())
            frac = 0.0
            for h, n in hrs.items():
                q = 0.0
                for k in range(60):
                    tau = dt.datetime.fromisoformat(d).replace(hour=h, minute=k, second=30, tzinfo=HFX)
                    m = (tau - P_).total_seconds() / 60
                    q += 1.0 if m < 0 else max(0.0, 1 - m * rate / L)
                frac += n / day * q / 60
            st += U[(s, d)] * frac
        acc[s] = 100 * (1 - (st + stray * (total[s] - st)) / total[s])
    watch = sorted(s for s in stores if acc[s] < line)
    say(watch == sorted(F["watch"]), "call.watch_set", str(watch))
    for s in F["watch"]:
        say(half_up(acc[s], 1) == F["accuracy"][str(s)], "figure.accuracy.%d" % s,
            "%.3f vs %.1f" % (acc[s], F["accuracy"][str(s)]))
    near = min((s for s in stores if s not in watch), key=lambda s: acc[s])
    say(near == F["nearest_off"] and half_up(acc[near], 1) == F["nearest_off_acc"], "figure.nearest_off")
    for s in stores:
        say(abs(acc[s] - line) >= 0.3, "margin.%d" % s, "%.3f" % (acc[s] - line))

    # --- ask A: Scanner Code payouts
    till = {}
    pay = defaultdict(float)
    for r in csv_rows(find(r"^pos_price_overrides")):
        if r["reason_code"] != "SC":
            continue
        u = dt.datetime.strptime(r["override_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=ZoneInfo("UTC"))
        t = u.astimezone(HFX)
        if not (dt.date(2026, 10, 1) <= t.date() <= dt.date(2026, 12, 31)):
            continue
        s = int(r["store_no"])
        amt = (int(r["orig_price_cents"]) - int(r["override_price_cents"])) / 100
        pay[s] += amt
        till[(s, int(r["register"]), int(r["transaction"]), r["upc"])] = amt
    for nm, rows in xlsx_sheets(find(r"^service_desk")).items():
        for r in rows[1:]:
            if r[5] != "Scanner Code":
                continue
            when = excel_date(r[1])
            if not (dt.datetime(2026, 10, 1) <= when < dt.datetime(2027, 1, 1)):
                continue
            s = by_name[r[0]]
            rec = str(r[2])
            if "/" in rec:
                txn, reg = map(int, rec.split("/"))
            else:
                parts = rec.split("-")
                reg, txn = (int(parts[-2]), int(parts[-1]))
            amt = round(float(r[6]), 2)
            key = (s, reg, txn, str(r[3])[1:])
            if key in till and abs(till[key] - amt) < 0.005:
                continue
            pay[s] += amt
    for s in stores:
        say(half_up(pay.get(s, 0.0), 0) == F["payouts"][str(s)], "askA.%d" % s,
            "%.2f vs %d" % (pay.get(s, 0.0), F["payouts"][str(s)]))

    # --- ask B: flyer prices
    rel = xlsx_sheets(find(r"^weekly_price_change"))["REVISED"]
    keyed = {}
    adstart = defaultdict(dict)
    for r in rel[1:]:
        d = excel_date(r[2]).date().isoformat()
        u11 = str(r[3])[1:12]
        keyed[(d, u11, int(float(r[5])))] = (int(float(r[8])), float(r[7]))
        if r[6] == "AD START" and int(float(r[5])) == 1:
            adstart[d][u11] = str(r[4]).split()
    fixes = defaultdict(list)
    for r in csv_rows(find(r"^price_corrections")):
        fixes[(r["ean"][1:12], int(r["zone"][-1]))].append((r["effective_at_open"], int(r["price_qty"]),
                                                           float(r["price"])))
    units = defaultdict(int)
    for r in csv_rows(find(r"^flyer_item_daily")):
        units[(r["flyer_start"], r["sales_date"], r["upc"][:11], int(r["price_zone"][1:]))] += int(r["units"])
    cnt = defaultdict(int)
    over = defaultdict(float)
    for r in csv_rows(find(r"^flyer_ad_plan")):
        d = r["flyer_start"]
        txt = r["ad_price"]
        m = re.match(r"^\$([\d.]+)$", txt) or re.match(r"^(\d)/\$([\d.]+)$", txt) or re.match(r"^(\d) for \$(\d+)$", txt)
        q, p = (1, float(m.group(1))) if txt.startswith("$") else (int(m.group(1)), float(m.group(2)))
        mem = [r["upc_11"]]
        if r["ad_copy"].endswith(", assorted"):
            lead = adstart[d][r["upc_11"]]
            mem = [u for u, toks in adstart[d].items() if len(toks) == 4 and toks[0] == lead[0] and
                   toks[1] == lead[1] and toks[3] == lead[3]]
        for u in mem:
            bad = False
            d0 = dt.date.fromisoformat(d)
            for z in (1, 2):
                kq0, kp0 = keyed[(d, u, z)]
                fx = [f for f in fixes.get((u, z), []) if d0.isoformat() < f[0] <= (d0 + dt.timedelta(days=6)).isoformat()]
                for j in range(7):
                    day = (d0 + dt.timedelta(days=j)).isoformat()
                    kq, kp = (fx[-1][1], fx[-1][2]) if fx and day >= fx[-1][0] else (kq0, kp0)
                    if abs(kp / kq - p / q) > 0.004:
                        bad = True
                        if kp / kq > p / q:
                            over[d] += (kp / kq - p / q) * units[(d, day, u, z)]
            cnt[d] += bad
    for d in sorted(F["flyer_count"]):
        say(cnt[d] == F["flyer_count"][d], "askB.count.%s" % d, "%d" % cnt[d])
        say(half_up(over[d], 0) == F["flyer_over"][d], "askB.dollars.%s" % d, "%.2f" % over[d])

    print("\n%d failures" % len(FAIL))
    if FAIL:
        sys.exit(1)


if __name__ == "__main__":
    main()
