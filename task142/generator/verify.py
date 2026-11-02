"""Independent verifier: reads every shipped file back on its own code path (pandas for the CSVs, the workbook XML read
straight from the zip, its own ASCII85 and Flate decoder for the PDFs, the document XML of the DOCX) and recomputes
the call and every graded figure without importing analysis.py, world.py or params.py.

    python3 task142/generator/verify.py           # exit 1 on any mismatch with figures.json
"""
import base64
import datetime as dt
import json
import os
import re
import sys
import zipfile
import zlib
import xml.etree.ElementTree as ET
from decimal import ROUND_HALF_UP, Decimal

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
FAIL = []


def say(good, what, detail=""):
    print("%-4s %s %s" % ("OK" if good else "FAIL", what, detail))
    if not good:
        FAIL.append(what)


def rnd(x, unit):
    return int((Decimal(repr(float(x))) / Decimal(unit)).quantize(Decimal(1), rounding=ROUND_HALF_UP)) * unit


def pick(prefix):
    return os.path.join(T, [n for n in sorted(os.listdir(T)) if n.startswith(prefix)][0])


def pdf_text(path):
    """Text shown by the Tj operators of every content stream: each object's dictionary is read for its filters, the
    stream decoded from ASCII85 then Flate."""
    raw = open(path, "rb").read()
    out = []
    for m in re.finditer(rb"\d+ 0 obj\s*<<(.*?)>>\s*stream\r?\n", raw, re.S):
        head = m.group(1)
        end = raw.find(b"endstream", m.end())
        body = raw[m.end():end].strip()
        if b"ASCII85Decode" in head:
            if body.endswith(b"~>"):
                body = body[:-2]
            body = base64.a85decode(body)
        if b"FlateDecode" in head:
            try:
                body = zlib.decompress(body)
            except zlib.error:
                continue
        out += [s.decode("latin-1") for s in re.findall(rb"\(((?:[^()\\]|\\.)*)\)\s*Tj", body)]
    return " ".join(out)


def xlsx(path):
    z = zipfile.ZipFile(path)
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
            shared.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    target = {r.get("Id"): r.get("Target") for r in rels}
    out = {}
    for s in wb.find("m:sheets", NS):
        rid = s.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
        xml = ET.fromstring(z.read("xl/" + target[rid].replace("/xl/", "")))
        rows = []
        for row in xml.iter("{%s}row" % NS["m"]):
            vals = {}
            for c in row.findall("m:c", NS):
                col = 0
                for ch in re.match(r"([A-Z]+)", c.get("r")).group(1):
                    col = col * 26 + ord(ch) - 64
                v = c.find("m:v", NS)
                t = c.get("t")
                if t == "s":
                    vals[col] = shared[int(v.text)]
                elif t == "inlineStr":
                    vals[col] = "".join(x.text or "" for x in c.iter("{%s}t" % NS["m"]))
                elif v is not None:
                    vals[col] = float(v.text)
            rows.append([vals.get(k) for k in range(1, max(vals) + 1)] if vals else [])
        out[s.get("name")] = rows
    return out


def serial(x):
    return (dt.datetime(1899, 12, 30) + dt.timedelta(days=float(x))).date()


def table(rows, header_row=0):
    """Rows under a header; a string header_row names a column the header row carries."""
    if isinstance(header_row, str):
        header_row = [i for i, r in enumerate(rows) if header_row in r][0]
    head = rows[header_row]
    return [dict(zip(head, r + [None] * (len(head) - len(r)))) for r in rows[header_row + 1:] if r and r[0] is not None]


def cohort(b):
    y = b.year + 4
    return y if (b.month, b.day) <= (10, 1) else y + 1


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    brp = pd.read_csv(pick("brp_uittreksel"), sep=";", dtype=str).fillna("")
    roll = pd.read_csv(pick("leerlingtellingen"), sep=";", dtype=str).fillna("")
    plan = pdf_text(pick("huisvestingsplan"))
    C = int(re.search(r"capacity of\s*(\d+)\s*pupils", plan.replace("  ", " ")).group(1))
    say(C == fig["capacity"], "capacity read back", C)
    brp["b"] = pd.to_datetime(brp["geboortedatum"], format="%d-%m-%Y").dt.date
    brp["f"] = pd.to_datetime(brp["datum_adres"], format="%d-%m-%Y").dt.date
    brp["t"] = pd.to_datetime(brp["datum_vertrek"], format="%d-%m-%Y", errors="coerce").dt.date
    brp["pc"] = brp["postcode"].str.replace(" ", "")
    brp["ad"] = brp["huisletter"].str.lower().str.replace(r"[^0-9a-z]", "", regex=True)
    brp["k"] = list(zip(brp["b"], brp["pc"], brp["huisnummer"].astype(int), brp["ad"]))
    brp["coh"] = brp["b"].map(cohort)
    roll["y"] = roll["teldatum"].str[-4:].astype(int)
    roll["b"] = pd.to_datetime(roll["geboortedatum"]).dt.date
    roll["ad"] = roll["toevoeging"].str.lower().str.replace(r"[^0-9a-z]", "", regex=True)
    roll["k"] = list(zip(roll["b"], roll["postcode"], roll["huisnummer"].astype(int), roll["ad"]))
    on = {y: dict(zip(g["k"], g["groep"].astype(int))) for y, g in roll.groupby("y")}

    def alive(row, day):
        return row.f <= day and (pd.isna(row.t) or day < row.t)
    hh = {h: g for h, g in brp.groupby("huishoudnummer")}
    cnt = {True: [0, 0], False: [0, 0]}
    outs = []
    for Y in (2022, 2023, 2024, 2025, 2026):
        day = dt.date(Y, 10, 1)
        sel = brp[(brp["coh"] == Y) & brp["pc"].str[:4].isin(["3841", "3842"])]
        for row in sel.itertuples():
            if not alive(row, day):
                continue
            g = hh[row.huishoudnummer]
            sib = any(o.persoonsnummer != row.persoonsnummer and o.b < row.b and alive(o, day) and o.k in on[Y]
                      for o in g.itertuples())
            cnt[sib][0] += 1
            cnt[sib][1] += row.k in on[Y]
        outs.append(sum(1 for k, gr in on[Y].items() if gr == 1 and k[1][:4] not in ("3841", "3842")))
    rs, ro = cnt[True][1] / cnt[True][0], cnt[False][1] / cnt[False][0]
    say(round(100 * rs) == fig["rate_sibling_pct"] and round(100 * ro) == fig["rate_other_pct"], "entry shares",
        "%.1f and %.1f per cent" % (100 * rs, 100 * ro))
    out_avg = sum(outs) / 5
    base = on[2026]
    day26 = dt.date(2026, 10, 1)
    fut = brp[(brp["coh"] >= 2027) & (brp["coh"] <= 2029) & brp["pc"].str[:4].isin(["3841", "3842"])]
    exp = {2027: 0.0, 2028: 0.0, 2029: 0.0}
    nsib = {2027: 0, 2028: 0, 2029: 0}
    for row in fut.itertuples():
        if not alive(row, day26):
            continue
        c = row.coh
        sib = any(o.persoonsnummer != row.persoonsnummer and o.b < row.b and alive(o, day26) and o.k in base and
                  base[o.k] + (c - 2026) <= 8 for o in hh[row.huishoudnummer].itertuples())
        nsib[c] += sib
        exp[c] += rs if sib else ro
    calls = None
    for Y in (2027, 2028, 2029):
        stay = sum(1 for g in base.values() if g + (Y - 2026) <= 8)
        pupils = stay + sum(exp[c] for c in exp if c <= Y) + out_avg * (Y - 2026)
        say(int(np.floor(pupils / 10 + 0.5)) * 10 == fig["pupils"][str(Y)], "pupils %d" % Y, "%.1f" % pupils)
        say(nsib[Y] == fig["future_sibling"][str(Y)], "children with a sibling on the roll, %d" % Y, nsib[Y])
        if calls is None and pupils > C:
            calls = Y
    say(calls == 2029 and fig["call"] == "2029-30", "the call", calls)
    # gas
    gr = pd.read_csv(pick("gas_telemetrie"), sep=";", dtype=str).drop_duplicates()
    gm = xlsx(pick("meterstamgegevens_gas"))
    conn = table(gm["Aansluitingen"], "ean")
    met = table(gm["Meters"], "ean")
    for sy in (2023, 2024, 2025):
        a, b = "%d-08-01T06:00" % sy, "%d-08-01T06:00" % (sy + 1)
        da, db = dt.date(sy, 8, 1), dt.date(sy + 1, 8, 1)
        tot = 0
        for m in met:
            placed = serial(m["geplaatst"])
            gone = serial(m["verwijderd"]) if m["verwijderd"] else None
            if (gone and gone <= da) or placed >= db:
                continue
            rr = gr[(gr["ean"] == str(m["ean"])) & (gr["meternummer"] == str(m["meternummer"]))]
            rr = rr[(rr["tijdstip"].str[:16] >= a) & (rr["tijdstip"].str[:16] <= b)].sort_values("tijdstip")
            first = int(m["beginstand_m3"]) if placed > da and m["beginstand_m3"] is not None else int(rr["meterstand_m3"].iloc[0])
            last = int(m["eindstand_m3"]) if gone and gone < db and m["eindstand_m3"] is not None else int(rr["meterstand_m3"].iloc[-1])
            tot += last - first
        say(int(np.floor(tot / 1000 + 0.5)) * 1000 == fig["gas_m3"][str(sy)], "gas %d" % sy, tot)
    # after-school care
    bl = xlsx(pick("bso_locaties"))
    locs = {r_["locatiecode"] for r_ in table(bl["Locaties"], "locatiecode") if r_["adres"] == "Molenwiek 4"}
    school = {r_["gezinsnummer"]: r_["school"] for r_ in table(bl["Contracten"], "gezinsnummer")}
    att = pd.read_csv(pick("bso_aanwezigheid"), sep=";", dtype=str)
    att = att[att["locatiecode"].isin(locs) & att["gezinsnummer"].map(lambda g: school.get(g) == "De Kwikstaart")]
    att["wd"] = pd.to_datetime(att["datum"], format="%d-%m-%Y").dt.weekday
    sums = att.groupby("wd")["aantal_kinderen"].apply(lambda s: s.astype(int).sum()).to_dict()
    say({str(k): int(v) for k, v in sums.items()} == fig["bso"], "after-school care by weekday", sums)
    # the request and the golden read back
    req = re.sub(r"<[^>]+>", "", zipfile.ZipFile(pick("aanvraag_huisvesting")).read("word/document.xml").decode("utf-8"))
    say("1 August to 1 August" in req and "one attendance being one pupil on one day" in req, "request read back")
    gold = re.sub(r"<[^>]+>", " ", zipfile.ZipFile(os.path.join(TASK, "golden", "kwikstaart_leerlingenprognose_2027-2029.docx"))
                  .read("word/document.xml").decode("utf-8"))
    say(all(str(fig["pupils"][str(Y)]) in gold for Y in (2027, 2028, 2029)) and str(fig["capacity"]) in gold,
        "golden memo agrees")
    print("%d failed" % len(FAIL))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
