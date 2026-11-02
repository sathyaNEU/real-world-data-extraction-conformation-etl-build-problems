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


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    wx = pd.read_csv(pick("weerstation_"))
    cold = set(pd.to_datetime(wx.loc[wx["TG"] <= 0, "YYYYMMDD"].astype(str), format="%Y%m%d").dt.date)
    say(len(cold) == fig["cold_days"], "cold days", len(cold))
    amr = pd.read_csv(pick("amr_warmtemeters_"), dtype={"meternummer": str})
    amr["d"] = pd.to_datetime(amr["datum_utc"]).dt.date
    reg = xlsx(pick("aansluitregister_"))
    conns = table(reg["Aansluitingen"])
    meters = table(reg["Meters"])
    own = {}
    for m in meters:
        own.setdefault(str(m["meternummer"]).split(".")[0], []).append(
            (m["aansluitnummer"], serial(m["geplaatst"]), serial(m["verwijderd"]) if m["verwijderd"] else None))

    def who(s, d):
        for a, g, v in own[s]:
            if g <= d and (v is None or d <= v):
                return a
    c = amr[amr["d"].isin(cold)].copy()
    c["nr"] = [who(s, d) for s, d in zip(c["meternummer"], c["d"])]
    c["dt"] = c["t_aanvoer_gem_c"] - c["t_retour_gem_c"]
    g = c.groupby("nr").agg(tr=("t_retour_gem_c", "mean"), dt=("dt", "mean"))
    srt = g.sort_values("tr")
    gaps = srt["tr"].diff()
    cut = gaps.idxmax()
    pos = srt.index.get_loc(cut)
    lo, hi = float(srt["tr"].iloc[pos - 1]), float(srt["tr"].iloc[pos])
    like = srt[srt["tr"] >= hi].index
    d = float(g.loc[like, "dt"].mean())
    say(len(like) == fig["like_n"], "like installations from the return gap", "%d, gap %.1f to %.1f C" % (len(like), lo, hi))
    say(round(d, 1) == fig["drop_K"], "their cold-day drop", "%.2f K" % d)
    sch = xlsx(pick("weidehaven_aardgasvrij_fasering"))["Fasering"]
    sched = table(sch, "complexnr")
    rev = table(xlsx(pick("warmteverliesberekening_weidehaven_rev2"))["Resultaten"], "complex")
    load = {str(r["complex"]).replace("WH", ""): r["ontwerpwarmteverlies_kw"] for r in rev}
    phase = {str(int(s["complexnr"])): int(s["fase"]) for s in sched}
    pl = {p: sum(load[k] for k in phase if phase[k] == p) for p in range(1, 7)}
    hyd = pdf_text(pick("hydraulische_toets"))
    H = int(re.search(r"=\s*(\d+)\s*m", hyd).group(1))
    proc = pdf_text(pick("procedure_capaciteitstoets"))
    say("1.163" in proc and "or lower" in proc and "added at full value" in proc, "procedure read back (1.163, the window, "
        "full value)")
    KA = sum(pl[p] for p in (1, 2, 3))
    KAB = sum(pl.values())
    f3, f6 = KA / (1.163 * d), KAB / (1.163 * d)
    call = "2027-28" if f3 > H else ("2028-29" if f6 > H else "none")
    say(call == fig["call"], "the call", call)
    say(rnd(f3, 10) == fig["flow_2027_28"] and rnd(f6, 10) == fig["flow_2028_29"], "season flows",
        "%.1f and %.1f against %d" % (f3, f6, H))
    say(rnd(f6 - H, 10) == fig["shortfall_2028_29"], "shortfall", "%.1f" % (f6 - H))
    for p in range(1, 7):
        say(rnd(pl[p] / (1.163 * d), 5) == fig["phase_flow"][str(p)], "phase %d flow" % p, "%.1f" % (pl[p] / (1.163 * d)))
    # ---- gas
    gr = pd.read_csv(pick("gas_telemetrie_"), sep=";", dtype={"ean": str, "meternummer": str}).drop_duplicates()
    gm = xlsx(pick("meterstamgegevens_gas"))
    gconn = table(gm["Aansluitingen"])
    gmet = table(gm["Meters"])
    by_desc = {}
    for r in gconn:
        by_desc.setdefault(r["omschrijving"], []).append(str(r["ean"]))
    desc_of = {str(r["ean"]): r["omschrijving"] for r in gconn}
    gas = {p: 0 for p in range(1, 7)}
    for s in sched:
        code = str(int(s["complexnr"]))
        for ean in by_desc[desc_of[str(s["gas_ean"])]]:
            for m in [m for m in gmet if str(m["ean"]) == ean]:
                ser = str(m["meternummer"])
                rr = gr[(gr["ean"] == ean) & (gr["meternummer"] == ser)].copy()
                rr["t"] = rr["tijdstip"].str[:16]
                rr = rr[(rr["t"] >= "2025-10-01T06:00") & (rr["t"] <= "2026-10-01T06:00")].sort_values("t")
                placed = serial(m["geplaatst"])
                first = int(m["beginstand_m3"]) if placed > dt.date(2025, 10, 1) and m["beginstand_m3"] is not None \
                    else int(rr["meterstand_m3"].iloc[0])
                gone = serial(m["verwijderd"]) if m["verwijderd"] else None
                last = int(m["eindstand_m3"]) if gone and gone < dt.date(2026, 10, 1) and m["eindstand_m3"] is not None \
                    else int(rr["meterstand_m3"].iloc[-1])
                gas[phase[code]] += last - first
    for p in range(1, 7):
        say(rnd(gas[p], 1000) == fig["gas_m3"][str(p)], "gas phase %d" % p, gas[p])
    # ---- heat
    leg = pd.read_csv(pick("driveby_opnames_"), sep=";", dtype={"meternummer": str})
    leg["kwh"] = leg["stand"].str.replace(",", ".").astype(float) * leg["eenheid"].map({"GJ": 277.7778, "MWh": 1000.0})
    leg["d"] = pd.to_datetime(leg["opnamedatum"], format="%d-%m-%Y").dt.date
    cat = {r["aansluitnummer"]: r["categorie"] for r in conns}
    first_amr = amr.sort_values("d").groupby("meternummer").first()
    last_amr = amr.sort_values("d").groupby("meternummer").last()
    y1 = {"Woningen": 0.0, "Utiliteit": 0.0}
    y2 = {"Woningen": 0.0, "Utiliteit": 0.0}
    for nr in cat:
        ms = sorted([m for m in meters if m["aansluitnummer"] == nr], key=lambda m: m["geplaatst"])
        m0 = ms[0]
        s0 = str(m0["meternummer"]).split(".")[0]
        l0 = leg[leg["meternummer"] == s0].sort_values("d")
        start = float(l0[l0["soort"].isin(["J", "A"])]["kwh"].iloc[0])
        amrs = [m for m in ms if str(m["uitlezing"]).startswith("AMR")]
        s1 = str(amrs[0]["meternummer"]).split(".")[0]
        opening = float(first_amr.loc[s1, "telwerk_energie_kwh"] - first_amr.loc[s1, "energie_kwh"])
        if m0["uitlezing"] == "drive-by":
            w = float(l0[l0["soort"] == "W"]["kwh"].iloc[0])
            y1[cat[nr]] += (w - start) + (opening - float(amrs[0]["stand_bij_plaatsing_kwh"]))
        else:
            y1[cat[nr]] += opening - start
        for m in amrs:
            sx = str(m["meternummer"]).split(".")[0]
            op = float(first_amr.loc[sx, "telwerk_energie_kwh"] - first_amr.loc[sx, "energie_kwh"])
            y2[cat[nr]] += float(last_amr.loc[sx, "telwerk_energie_kwh"]) - op
    for k, u in (("Woningen", 1000), ("Utiliteit", 100)):
        a, b = y1[k] / 1000, y2[k] / 1000
        say(rnd(a, u) == fig["heat_2425_MWh"][k], "heat 2024-25 %s" % k, "%.1f MWh" % a)
        say(rnd(b - a, u) == fig["heat_change_MWh"][k], "change %s" % k, "%.1f MWh" % (b - a))
    # ---- the scope and the golden workbook read back
    doc = zipfile.ZipFile(pick("weidehaven_aardgasvrij_scope")).read("word/document.xml").decode("utf-8")
    say("radiators remain in service" in re.sub(r"<[^>]+>", "", doc), "scope read back")
    gold = xlsx(os.path.join(TASK, "golden", "os_west_debiet_2027-2029.xlsx"))
    seas = [r for r in table(gold["Seizoenen"], "Heating season") if r["Heating season"] in ("2027-28", "2028-29")]
    say([r["Design-day flow (m3/h)"] for r in seas] == [fig["flow_2027_28"], fig["flow_2028_29"]] and
        seas[1]["Shortfall (m3/h)"] == fig["shortfall_2028_29"], "golden workbook seasons agree")
    print("%d failed" % len(FAIL))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
