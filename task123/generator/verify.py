"""Independent verifier for task123: reads every shipped file back on its own code path (csv module, raw OOXML
XML through zipfile, a hand-written PDF stream decoder for ASCII85 and Flate) and recomputes every graded figure
of the golden, then checks the golden workbook and note carry exactly those figures. It imports nothing from
analysis.py, golden.py or pack.py."""
import base64
import csv
import datetime as dt
import json
import os
import re
import sys
import zipfile
import zlib
from collections import defaultdict
from xml.etree import ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
DIM = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def xlsx_sheets(path):
    """{sheet name: list of rows (lists of cell values as strings or numbers)} straight from the XML."""
    z = zipfile.ZipFile(path)
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        root = ET.fromstring(z.read("xl/sharedStrings.xml"))
        for si in root.findall("m:si", NS):
            shared.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    target = {r.get("Id"): r.get("Target") for r in rels}
    out = {}
    for sh in wb.find("m:sheets", NS):
        rid = sh.get("{%s}id" % NS["r"])
        p = target[rid].lstrip("/")
        p = p if p.startswith("xl/") else "xl/" + p
        root = ET.fromstring(z.read(p))
        rows = []
        for row in root.iter("{%s}row" % NS["m"]):
            while len(rows) < int(row.get("r")) - 1:
                rows.append([])
            cells = {}
            for c in row.findall("m:c", NS):
                ref = c.get("r")
                col = 0
                for ch in re.match(r"[A-Z]+", ref).group(0):
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
                    val = float(v.text) if re.search(r"[.eE]", v.text) else int(v.text)
                cells[col] = val
            rows.append([cells.get(i) for i in range(1, (max(cells) if cells else 0) + 1)])
        out[sh.get("name")] = rows
    return out


def pdf_strings(path):
    """Every string shown by a Tj or TJ operator, in content-stream order, after ASCII85 and Flate decoding."""
    raw = open(path, "rb").read()
    out = []
    for m in re.finditer(rb"<<((?:(?!<<|stream).)*?)>>\s*stream\r?\n(.*?)\s*endstream", raw, re.S):
        head, data = m.group(1), m.group(2)
        if b"ASCII85Decode" in head:
            data = data.strip()
            if data.endswith(b"~>"):
                data = data[:-2]
            data = base64.a85decode(data)
        if b"FlateDecode" in head:
            try:
                data = zlib.decompress(data)
            except zlib.error:
                continue
        for t in re.finditer(rb"\((.*?)(?<!\\)\)\s*Tj", data, re.S):
            out.append(t.group(1).decode("latin-1").replace("\\(", "(").replace("\\)", ")").replace("\\\\", "\\"))
    return out


def d_it(s):
    return dt.datetime.strptime(s, "%d/%m/%Y").date()


def main():
    T = os.path.join(TASK, "target")
    files = sorted(os.listdir(T))
    fail = []
    # survey: latest submission per establishment-month
    surv = [f for f in files if f.startswith("mov_clienti")][0]
    xw = {}
    with open(os.path.join(T, [f for f in files if f.startswith("tabella_raccordo")][0]), encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter=";"):
            xw[r["CIN"]] = r["CIR"]
    # one return per establishment and month: the last submission, whichever code it was sent under
    best = {}
    with open(os.path.join(T, surv), encoding="utf-8") as f:
        rd = csv.reader(f, delimiter=";")
        head = next(rd)
        for r in rd:
            est = r[0] if "-" in r[0] else xw.get(r[0], r[0])
            key = (est, int(r[1]), int(r[2]))
            when = dt.datetime.strptime(r[7], "%d/%m/%Y %H:%M")
            cur = best.get(key)
            if cur is None or when > cur[0]:
                best[key] = (when, r[0], [])
            if when == best[key][0]:
                best[key][2].append(int(r[6]))
    nights = {}
    for (est, y, m), v in best.items():
        nights[(v[1], y, m)] = nights.get((v[1], y, m), 0) + sum(v[2])
    print("survey rows read, establishment-months:", len(nights))
    reg = xlsx_sheets(os.path.join(T, [f for f in files if f.startswith("registro")][0]))
    rows = reg["STRUTTURE"]
    hdr = rows[0]
    R = [dict(zip(hdr, r)) for r in rows[1:]]
    var = [dict(zip(reg["VARIAZIONI"][0], r)) for r in reg["VARIAZIONI"][1:]]
    pop = {}
    names = {}
    with open(os.path.join(T, [f for f in files if f.startswith("popolazione")][0]), encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter=";"):
            names[r["Codice comune"]] = r["Comune"]
            if r["Data"] == "01/01/2026":
                pop[r["Codice comune"]] = int(r["Totale"])
    code_of = {v: k for k, v in names.items()}
    # declarations, latest filing per comune, quarter, category
    decl = []
    conc = xlsx_sheets(os.path.join(T, [f for f in files if f.startswith("IDS_riepilogo")][0]))
    for nm, rows in conc.items():
        code = str(rows[0][3])
        for r in rows[3:]:
            if r and r[0] is not None:
                decl.append((code, int(r[0]), int(str(r[1])[0]), r[2].lower(), int(r[3]), int(r[5]), d_it(r[7])))
    with open(os.path.join(T, [f for f in files if f.startswith("Comune_Porto")][0]), encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter=";"):
            y, q = r["PERIODO"].split("-T")
            decl.append((code_of["Porto Levarna"], int(y), int(q), r["TIPOLOGIA"].lower(), int(r["PRESENZE_TOTALI"]),
                         int(r["PRESENZE_IMPONIBILI"]), d_it(r["DATA_RICEZIONE"])))
    with open(os.path.join(T, [f for f in files if f.startswith("ids_santelvira")][0]), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            decl.append((code_of["Sant'Elvira a Mare"], int(r["anno"]), int(r["trimestre"]), r["categoria"].lower(),
                         int(r["notti_totali"]), int(r["notti_imponibili"]), dt.date.fromisoformat(r["data_protocollo"])))
    qmap = {"gen-mar": 1, "apr-giu": 2, "lug-set": 3, "ott-dic": 4}
    with open(os.path.join(T, [f for f in files if f.startswith("servizio_tributi")][0]), encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter=";"):
            per, yy = r["Periodo di riferimento"].split()
            decl.append((code_of[r["Ente"].replace("Comune di ", "")], int(yy), qmap[per], r["Tipologia"].lower(),
                         int(r["Presenze dichiarate"]), int(r["Presenze soggette"]), d_it(r["Data"])))
    s = pdf_strings(os.path.join(T, [f for f in files if f.startswith("LidoArzena")][0]))
    i = 0
    while i < len(s):
        if re.fullmatch(r"20\d\d", s[i]) and i + 7 < len(s) and re.fullmatch(r"[1-4]", s[i + 1]):
            num = lambda x: int(x.replace(".", ""))
            decl.append((code_of["Lido di Arzena"], int(s[i]), int(s[i + 1]), s[i + 2].lower(), num(s[i + 3]),
                         num(s[i + 5]), d_it(s[i + 7])))
            i += 8
        else:
            i += 1
    # a later filing far smaller than the one before adds nights; one of about the same size replaces it
    grouped = defaultdict(list)
    for d in decl:
        grouped[d[:4]].append(d)
    last = {}
    for k, ds in grouped.items():
        ds.sort(key=lambda x: x[6])
        cur = list(ds[0])
        for x in ds[1:]:
            if x[4] < 0.5 * cur[4]:
                cur[4] += x[4]
                cur[5] += x[5]
            else:
                cur = list(x)
        last[k] = tuple(cur)
    # main call
    by_cin = {r["CIN"]: r for r in R}
    aug, jul, sep = defaultdict(int), defaultdict(int), defaultdict(int)
    for (code, y, m), n in nights.items():
        if y == 2026 and m in (7, 8, 9) and code in by_cin:
            c = str(by_cin[code]["COD_ISTAT_COMUNE"])
            {7: jul, 8: aug, 9: sep}[m][c] += n
    q3 = defaultdict(int)
    for k, d in last.items():
        if d[1] == 2026 and d[2] == 3:
            q3[d[0]] += d[4]
    golden = {}
    for c in pop:
        golden[c] = (q3[c] - jul[c] - sep[c]) if c in q3 else aug[c]
    npr = {c: golden[c] / pop[c] for c in pop}
    qual = sorted(names[c] for c in pop if npr[c] >= 30)
    # January to April 2026 by the comune code inside each CIR
    ja = defaultdict(int)
    for (code, y, m), n in nights.items():
        if y == 2026 and m <= 4:
            cir = code if "-" in code else xw[code]
            pref = cir.split("-")[0]
            ja["112020" if pref in ("006", "007") else "112" + pref] += n
    # October 2025 occupancy
    susp = {v["CIN"] for v in var if v["TIPO_VARIAZIONE"] == "SOSPENSIONE TEMPORANEA"}
    beds_hist = defaultdict(list)
    for v in var:
        if v["TIPO_VARIAZIONE"] == "POSTI LETTO":   # a correction (RETTIFICA) fixes the record from the start
            beds_hist[v["CIN"]].append((d_it(v["DATA_DECORRENZA"]), int(v["DA"]), int(v["A"])))
    num, den = defaultdict(int), defaultdict(int)
    for r in R:
        if not r["CIR"] or d_it(r["DATA_INIZIO_ATTIVITA"]) > dt.date(2025, 10, 31):
            continue
        per = r["PERIODO_APERTURA"]
        if per == "ANNUALE":
            last_day = 31
        else:
            a, b = per.split("-")
            m1, m2 = int(a[3:5]), int(b[3:5])
            if not (m1 <= 10 <= m2):
                continue
            last_day = int(b[:2]) if m2 == 10 else 31
        if r["CIN"] in susp:
            last_day = 0
        bd = 0
        for d in range(1, last_day + 1):
            day = dt.date(2025, 10, d)
            b = int(r["POSTI_LETTO"])
            for (when, frm, to) in beds_hist.get(r["CIN"], []):
                b = frm if day < when else to
            bd += b
        num[r["TIPOLOGIA"]] += nights.get((r["CIR"], 2025, 10), 0)
        den[r["TIPOLOGIA"]] += bd
    occ = {t: 100.0 * num[t] / den[t] for t in den if den[t]}
    # 2025 tourist tax by quarter
    rates = []
    with open(os.path.join(T, [f for f in files if f.startswith("aliquote")][0]), encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter=";"):
            rates.append((r["COD_ISTAT"], r["CATEGORIA"].lower(), float(r["EURO_PER_PERNOTTAMENTO"].replace(",", ".")),
                          d_it(r["IN_VIGORE_DAL"]), d_it(r["IN_VIGORE_AL"]) if r["IN_VIGORE_AL"] else dt.date(2100, 1, 1)))
    tax = defaultdict(float)
    for k, d in last.items():
        if d[1] != 2025:
            continue
        mid = dt.date(2025, 3 * d[2] - 1, 15)
        rate = [x[2] for x in rates if x[0] == d[0] and x[1] == d[3] and x[3] <= mid <= x[4]]
        if len(rate) != 1:
            fail.append("rate not unique for %s" % (d,))
            continue
        tax[d[2]] += d[5] * rate[0]
    # read the golden back and compare
    g = xlsx_sheets(os.path.join(TASK, "golden", "august_2026_guest_nights.xlsx"))
    rows = g["August 2026"]
    gtab = {r[0]: r for r in rows[4:] if r and r[0] and r[1]}
    for c in pop:
        row = gtab.get(names[c])
        want_n = int(round(golden[c] / 100.0)) * 100
        if row is None or row[3] != want_n or abs(row[4] - round(npr[c], 1)) > 1e-9:
            fail.append("August figure differs for %s: %s vs %s %.1f" % (names[c], row, want_n, npr[c]))
        if row and (row[5] == "Yes") != (npr[c] >= 30):
            fail.append("qualifying flag differs for %s" % names[c])
    qrow = [r for r in rows if r and r[0] == "Qualifying comuni"][0]
    if sorted(x.strip() for x in qrow[1].split(",")) != qual:
        fail.append("qualifying list differs: %s vs %s" % (qrow[1], qual))
    for r in g["Jan-Apr 2026"][3:]:
        if r and r[1]:
            want = int(round(ja[str(r[1])] / 100.0)) * 100
            if r[2] != want:
                fail.append("Jan-Apr differs for %s: %s vs %s" % (r[0], r[2], want))
    for r in g["Occupancy Oct 2025"][3:]:
        if r and r[0]:
            if abs(r[1] - round(occ[r[0]], 1)) > 1e-9:
                fail.append("occupancy differs for %s: %s vs %.2f" % (r[0], r[1], occ[r[0]]))
    for r in g["Tourist tax 2025"][3:]:
        if r and r[0]:
            q = int(r[0][1])
            if r[1] != int(round(tax[q] / 100.0)) * 100:
                fail.append("tax differs for %s: %s vs %.0f" % (r[0], r[1], tax[q]))
    note = " ".join(pdf_strings(os.path.join(TASK, "golden", "peak_cofinancing_2027_note.pdf")))
    for nm in qual:
        if nm not in note.replace("\\'", "'"):
            fail.append("note does not name %s" % nm)
    # every target file readable and counted
    for fn in files:
        p = os.path.join(T, fn)
        if fn.endswith(".xlsx"):
            xlsx_sheets(p)
        elif fn.endswith(".pdf"):
            if not pdf_strings(p):
                fail.append("no text read from %s" % fn)
        else:
            open(p, encoding="utf-8").read()
    print("qualifying:", qual)
    print("closest:", min(pop, key=lambda c: abs(npr[c] - 30)), "files read:", len(files))
    if fail:
        print("VERIFY FAIL")
        for f in fail:
            print("  ", f)
        sys.exit(1)
    print("VERIFY PASS: every graded figure recomputed on an independent path and found in the golden")


if __name__ == "__main__":
    main()
