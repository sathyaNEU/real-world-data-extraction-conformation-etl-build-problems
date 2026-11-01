"""Independent verifier: reads only the shipped files under target/ (and the golden workbook), on its own code path
(pandas for the CSVs, its own XLSX and PDF readers, a day-by-day tablet count with the median refill rate), and
recomputes every graded figure against generator/figures.json and the golden workbook. Exit 1 on any mismatch."""
import base64
import collections
import datetime as dt
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
import zlib

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK_DIR = os.path.dirname(HERE)
T = os.path.join(TASK_DIR, "target")
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
OUT = []


def ok(label, cond, detail=""):
    OUT.append((label, bool(cond), detail))


# ---------------------------------------------------------------- readers
def xlsx_rows(path, sheet_name):
    z = zipfile.ZipFile(path)
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
            shared.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    rid = [s.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
           for s in wb.find("m:sheets", NS) if s.get("name") == sheet_name][0]
    target = [r.get("Target") for r in rels if r.get("Id") == rid][0]
    target = target.lstrip("/")
    if not target.startswith("xl/"):
        target = "xl/" + target
    root = ET.fromstring(z.read(target))
    rows = []
    for row in root.iter("{%s}row" % NS["m"]):
        vals = {}
        for c in row.findall("m:c", NS):
            ref = re.match(r"([A-Z]+)", c.get("r")).group(1)
            col = 0
            for ch in ref:
                col = col * 26 + ord(ch) - 64
            t = c.get("t")
            v = c.find("m:v", NS)
            if t == "s":
                val = shared[int(v.text)]
            elif t == "inlineStr":
                val = "".join(x.text or "" for x in c.iter("{%s}t" % NS["m"]))
            elif v is None:
                val = None
            else:
                val = float(v.text) if re.fullmatch(r"-?\d+(\.\d+)?(E-?\d+)?", v.text) else v.text
            vals[col] = val
        if vals:
            rows.append([vals.get(i) for i in range(1, max(vals) + 1)])
    return rows


def table(rows, first_col):
    """Rows after the header row whose first cell is first_col."""
    for i, r in enumerate(rows):
        if r and r[0] == first_col:
            hdr = r
            return hdr, [x for x in rows[i + 1:] if x and x[0] is not None]
    raise ValueError(first_col)


def pdf_strings(path):
    data = open(path, "rb").read()
    out = []
    for m in re.finditer(rb"stream\r?\n(.*?)endstream", data, re.S):
        raw = m.group(1).strip()
        try:
            if raw.endswith(b"~>"):
                body = raw[2:-2] if raw.startswith(b"<~") else raw[:-2]
                raw = base64.a85decode(re.sub(rb"\s", b"", body))
            raw = zlib.decompress(raw)
        except Exception:
            continue
        for s in re.findall(rb"\(((?:\\.|[^\\)])*)\)\s*Tj", raw):
            s = re.sub(rb"\\([0-7]{3})", lambda x: bytes([int(x.group(1), 8)]), s)
            s = s.replace(rb"\(", b"(").replace(rb"\)", b")").replace(b"\\\\", b"\\")
            out.append(s.decode("latin-1"))
    return " ".join(out)


# ---------------------------------------------------------------- the call
def to_date(s):
    return dt.datetime.strptime(s, "%d-%m-%Y").date() if s[2] == "-" else dt.date.fromisoformat(s)


def main_call():
    disp = pd.read_csv(os.path.join(T, "statin_dispensings_202401_202612.csv"), dtype=str)
    prods = pd.read_csv(os.path.join(T, "statin_products.csv"), dtype=str)
    prods["tabs"] = prods["pack_size_tablets"].astype(int)
    disp = disp.merge(prods[["product_number", "tabs", "atc_code", "strength"]], on="product_number", how="left")
    ok("V1 every dispensing's product number is in the product list", disp["tabs"].notna().all())
    disp["d"] = disp["dispensing_date"].map(to_date)
    disp["tablets"] = disp["packs"].astype(int) * disp["tabs"]
    reg = xlsx_rows(os.path.join(T, "practice_register_2026.xlsx"), "Practices")
    hdr, prs = table(reg, "provider_number")
    practices = {str(r[0]): r[1] for r in prs}
    w0, w1 = dt.date(2025, 7, 1), dt.date(2025, 12, 31)
    status, practice_of = {}, {}
    for pid, g in disp.sort_values(["d", "product_number"]).groupby("personal_number_pseudonym", sort=True):
        dates = list(g["d"])
        inwin = [i for i, d in enumerate(dates) if w0 <= d <= w1]
        if not inwin:
            continue
        i0 = inwin[0]
        start = dates[i0]
        if any(0 < (start - d).days <= 365 for d in dates[:i0]):
            continue
        presc = g["prescriber_id"].iloc[i0]
        if presc not in practices:
            continue
        tabs = list(g["tablets"])[i0:]
        ds = dates[i0:]
        rates = [tabs[j] / (ds[j + 1] - ds[j]).days for j in range(len(ds) - 1) if (ds[j + 1] - ds[j]).days > 0]
        rates.sort()
        if rates:
            mid = len(rates) // 2
            dose = rates[mid] if len(rates) % 2 else (rates[mid - 1] + rates[mid]) / 2
        else:
            dose = 1.0
        add = collections.Counter()
        for d, t in zip(ds, tabs):
            add[(d - start).days] += t
        stock, run, worst = 0.0, 0, 0
        for day in range(365):
            stock += add.get(day, 0)
            if stock > 1e-9:
                stock = max(0.0, stock - dose)
                run = 0
            else:
                run += 1
                worst = max(worst, run)
        status[pid] = worst <= 30
        practice_of[pid] = presc
    n, k = collections.Counter(), collections.Counter()
    for pid, s in status.items():
        n[practice_of[pid]] += 1
        k[practice_of[pid]] += s
    share = {c: 100.0 * k[c] / n[c] for c in n}
    return share, sorted(c for c, v in share.items() if v < 60), disp, practices


# ---------------------------------------------------------------- the asks
def payments():
    rows = xlsx_rows(os.path.join(T, "pilot_conversations_2026.xlsx"), "Conversations")
    hdr, conv = table(rows, "conversation_no")
    conv = [dict(zip(hdr, r)) for r in conv]
    for c in conv:
        c["date"] = dt.date.fromisoformat(str(c["conversation_date"])[:10])
        c["canc"] = dt.date.fromisoformat(str(c["cancelled_date"])[:10]) if c.get("cancelled_date") else None
    txt = pdf_strings(os.path.join(T, "pilot_statements_2026.pdf"))
    stm = re.findall(r"\((A\d{3})\)\s+(\d{2})\.(\d{2})\.(\d{4})\s+([\d.]+,\d{2})", txt)
    ok("V2 the statements PDF decodes to 32 statements", len(stm) == 32, "%d" % len(stm))
    due, paid = {}, collections.Counter()
    rates = collections.defaultdict(set)
    for ph, dd, mm, yy, amt in stm:
        sd = dt.date(int(yy), int(mm), int(dd))
        amount = int(amt.replace(".", "").split(",")[0])
        paid[ph] += amount
        q0 = dt.date(sd.year, sd.month - 2, 1)
        cnt = sum(1 for c in conv if c["pharmacy_id"] == ph and q0 <= c["date"] <= sd and (c["canc"] is None or c["canc"] > sd))
        rates[ph].add(amount / cnt)
    for ph, rs in rates.items():
        ok("V3 %s: one rate across its four statements" % ph, len(rs) == 1 and list(rs)[0] == int(list(rs)[0]),
           "%s" % sorted(rs))
        due[ph] = int(list(rs)[0]) * sum(1 for c in conv if c["pharmacy_id"] == ph and c["canc"] is None)
    return due, paid


def continuing(disp, practices):
    first = disp.groupby("personal_number_pseudonym")["d"].min()
    last = disp.groupby("personal_number_pseudonym")["d"].max()
    key = disp.groupby("personal_number_pseudonym")[["birth_date", "sex"]].first()
    person = {pid: pid for pid in key.index}
    for (b, s), grp in key.groupby(["birth_date", "sex"]):
        pids = sorted(grp.index, key=lambda p: (first[p], p))
        for a, c in zip(pids, pids[1:]):
            if last[a] < first[c]:
                person[c] = person[a]
    d26 = disp[disp["d"].map(lambda d: d.year == 2026)].copy()
    d26["person"] = d26["personal_number_pseudonym"].map(person)
    d26["q"] = d26["d"].map(lambda d: (d.month - 1) // 3)
    out = collections.Counter()
    for p, g in d26.sort_values(["d", "product_number"]).groupby("person"):
        if set(g["q"]) == {0, 1, 2, 3}:
            out[g["prescriber_id"].iloc[-1]] += 1
    return {c: out.get(c, 0) for c in practices}


def main():
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    share, joins, disp, practices = main_call()
    gold = xlsx_rows(os.path.join(TASK_DIR, "golden", "statinprogram_2027.xlsx"), "Programme 2027")
    hdr, prow = table(gold, "Provider no.")
    g_pct = {r[0]: int(round(float(r[4]) * 100)) for r in prow if r[0] and re.fullmatch(r"\d{6}", str(r[0]))}
    g_join = sorted(r[0] for r in prow if r[0] and r[5] == "Yes")
    ok("V4 the call recomputed: the same joining practices as the golden workbook", joins == g_join, "%s" % joins)
    for c in sorted(share):
        ok("V5 %s persistence %d per cent" % (c, round(share[c])), round(share[c]) == g_pct[c] and round(share[c]) in figs,
           "%.2f" % share[c])
    due, paid = payments()
    gold = xlsx_rows(os.path.join(TASK_DIR, "golden", "statinprogram_2027.xlsx"), "Pilot settlement 2026")
    hdr, rows = table(gold, "Pharmacy")
    g_due = {r[0]: int(r[4]) for r in rows if r[0] and re.fullmatch(r"A\d{3}", str(r[0]))}
    for ph in sorted(due):
        ok("V6 %s entitled DKK %d" % (ph, due[ph]), due[ph] == g_due[ph] and due[ph] in figs)
    cu = continuing(disp, practices)
    gold = xlsx_rows(os.path.join(TASK_DIR, "golden", "statinprogram_2027.xlsx"), "Continuing users 2026")
    hdr, rows = table(gold, "Provider no.")
    g_cu = {r[0]: int(r[2]) for r in rows if r[0] and re.fullmatch(r"\d{6}", str(r[0]))}
    for c in sorted(cu):
        ok("V7 %s continuing users %d" % (c, cu[c]), cu[c] == g_cu[c] and cu[c] in figs)
    prog = pdf_strings(os.path.join(T, "statin_followup_programme_2027.pdf"))
    ok("V8 the programme PDF decodes and files the line and the persistence definition",
       "fewer than 60 per cent" in prog and "more than 30 days in a row without" in prog)
    agr = pdf_strings(os.path.join(T, "pharmacy_pilot_agreement_2026.pdf"))
    ok("V9 the agreement PDF decodes and files payment per conversation held, cancelled not paid",
       "A conversation that is cancelled is not paid" in agr)
    note = pdf_strings(os.path.join(TASK_DIR, "golden", "statinprogram_2027.pdf"))
    ok("V10 the golden note names every joining practice", all(practices[c] in note for c in joins))
    ok("V11 the CSVs read back (dispensings, products, pharmacies)", len(disp) > 25000 and len(
        pd.read_csv(os.path.join(T, "pharmacies.csv"))) == 8)
    bad = [x for x in OUT if not x[1]]
    for label, good, detail in OUT:
        print("%s  %s%s" % ("PASS" if good else "FAIL", label, ("  [" + detail + "]") if detail else ""))
    print("verify: %d checks, %d failed" % (len(OUT), len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
