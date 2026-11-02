"""Independent verifier: reads only the shipped bundle through its own readers (CSV module, raw OOXML,
raw PDF streams) and recomputes the call, the credit and every ask figure against figures.json.

    python3 verify.py <target_dir> <golden_dir> <figures.json>
"""
import base64
import csv
import datetime as dt
import json
import re
import sys
import zipfile
import zlib
from collections import defaultdict
from xml.etree import ElementTree as ET

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
FAILS = []


def check(name, cond, detail=""):
    print("%s  %s  %s" % ("PASS" if cond else "FAIL", name, detail))
    if not cond:
        FAILS.append(name)


# readers ---------------------------------------------------------------------------------------
def xlsx_sheets(path):
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
        xml = ET.fromstring(z.read("xl/" + target[rid].lstrip("/").replace("xl/", "")))
        rows = []
        for row in xml.iter("{%s}row" % NS["m"]):
            vals = {}
            for c in row.findall("m:c", NS):
                ref = re.match(r"([A-Z]+)", c.get("r")).group(1)
                col = 0
                for ch in ref:
                    col = col * 26 + ord(ch) - 64
                v = c.find("m:v", NS)
                t = c.get("t")
                if t == "s":
                    val = shared[int(v.text)]
                elif t == "inlineStr":
                    val = "".join(x.text or "" for x in c.iter("{%s}t" % NS["m"]))
                elif v is None:
                    val = None
                else:
                    val = float(v.text)
                vals[col] = val
            if vals:
                rows.append([vals.get(i) for i in range(1, max(vals) + 1)])
            else:
                rows.append([])
        out[s.get("name")] = rows
    return out


def excel_date(v):
    if isinstance(v, float):
        return dt.date(1899, 12, 30) + dt.timedelta(days=int(v))
    return dt.datetime.strptime(v.strip(), "%d/%m/%Y").date()


def pdf_strings(path):
    data = open(path, "rb").read()
    out = []
    for m in re.finditer(rb"stream\r?\n(.*?)endstream", data, re.S):
        raw = m.group(1).strip()
        try:
            if raw.endswith(b"~>"):
                raw = base64.a85decode(raw[:-2], adobe=False)
            raw = zlib.decompress(raw)
        except Exception:
            try:
                raw = zlib.decompress(raw)
            except Exception:
                pass
        out += [s.decode("latin-1") for s in re.findall(rb"\(((?:[^()\\]|\\.)*)\)\s*Tj", raw)]
    return " ".join(out).replace("\\(", "(").replace("\\)", ")")


def rows_csv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


# the verifier's own computation ---------------------------------------------------------------
def main(t, g, figpath):
    fig = json.load(open(figpath))
    reg = xlsx_sheets(t + "/cpi_outlet_register_2026-10.xlsx")
    out_rows = reg["Outlets"]
    H = out_rows[0]
    outlets = [dict(zip(H, list(r) + [None] * (len(H) - len(r)))) for r in out_rows[1:] if r]
    code = {o["Outlet code"]: o for o in outlets}
    tnum = {o["Contractor outlet no."]: o for o in outlets}
    regions = [r[0] for r in reg["Regions"][1:] if r]
    rname = {r[0]: r[1] for r in reg["Regions"][1:] if r}
    area = {r[2]: r[0] for r in reg["Regions"][1:] if r}
    check("V1 register read back (OOXML)", len(outlets) > 300 and len(regions) == 14, "%d outlets" % len(outlets))
    item_class = {r["item_code"]: r["coicop_class"] for r in rows_csv(t + "/cpi_item_list_2026.csv")}
    db = {}
    for r in rows_csv(t + "/cpi_field_quotes_2025-10_2026-09.csv"):
        db.setdefault((r["quote_id"], r["ref_month"]), r)
    check("V2 price database read back (CSV)", len(db) > 50000, "%d quote-months" % len(db))
    months = sorted({m for _, m in db})
    # monthly change frequency by COICOP class and outlet type
    n, c = defaultdict(int), defaultdict(int)
    for (q, m), r in db.items():
        i = months.index(m)
        if i == 0 or r["status"] not in ("P", "10"):
            continue
        prev = db.get((q, months[i - 1]))
        if prev is None or prev["status"] not in ("P", "R", "10", "30"):
            continue
        key = (item_class[r["item_code"]], code[r["outlet_code"]]["Outlet type"])
        n[key] += 1
        c[key] += float(prev["price"]) != float(r["price"])
    freq = {k: c[k] / n[k] for k in n}
    # visit dates
    visits = defaultdict(list)
    for v in rows_csv(t + "/tallis_visit_log_2026-07_2026-09.csv"):
        if int(v["prices_entered"]) > 0:
            visits[(v["outlet_no"], v["started"][:7])].append(dt.date(int(v["started"][:4]), int(v["started"][5:7]), int(v["started"][8:10])))
    check("V3 visit log read back (CSV)", len(visits) > 800)
    # back-checks
    bc = xlsx_sheets(t + "/fqt_backcheck_register_2026q3.xlsx")
    check("V4 back-check register read back (OOXML), three monthly sheets", len(bc) == 3, ",".join(bc))
    agree, denom, raw = defaultdict(int), defaultdict(float), defaultdict(int)
    for name, rows in bc.items():
        month = dt.datetime.strptime(name, "%b %Y").strftime("%Y-%m")
        hi = next(i for i, r in enumerate(rows) if r and r[0] == "Region")
        hdr = rows[hi]
        for r in rows[hi + 1:]:
            if not r or r[0] is None:
                continue
            d = dict(zip(hdr, list(r) + [None] * (len(hdr) - len(r))))
            if d["Found"] != "Y":
                continue
            o = code[d["Outlet"]]
            when = excel_date(d["Re-collected on"])
            vd = visits[(o["Contractor outlet no."], month)]
            lag = (when - vd[0]).days
            f = freq[(item_class[d["Item"]], o["Outlet type"])]
            hit = abs(float(d["Collector price"]) - float(d["FQT price"])) < 0.005
            agree[d["Region"]] += hit
            raw[d["Region"]] += 1
            denom[d["Region"]] += (1 - f) ** (lag / 30.4)
    acc = {r: 100.0 * agree[r] / denom[r] for r in regions}
    pcqs = pdf_strings(t + "/pcqs_price_collection_quality_standard_v3.pdf")
    check("V5 PCQS read back (PDF streams), positive control", "at the time the collector recorded it" in pcqs and "95.5 per cent" in pcqs)
    fees_txt = pdf_strings(t + "/pcsa_schedule4_collection_fees.pdf")
    fees = {m.group(1): int(m.group(2).replace(",", "")) for m in re.finditer(r"(CR\d\d)\s+\S.*?\s(\d\d,\d\d\d)", fees_txt)}
    check("V6 Schedule 4 read back (PDF streams)", len(fees) == 14, str(len(fees)))

    def band(a):
        return "Compliant" if a >= 98.0 else ("Corrective action" if a >= 95.5 else "Service credit")
    outs = {r: band(acc[r]) for r in regions}
    for r in regions:
        check("V7 %s outcome %s" % (r, outs[r]), fig["deliverables"][r]["outcome"] == outs[r], "%.2f" % acc[r])
    credit = sum(0.04 * fees[r] for r in regions if outs[r] == "Service credit")
    check("V8 service credit", "{:,}".format(int(round(credit))) == fig["call"]["credit_dollars"], "%.2f" % credit)
    # timeliness and missed visits
    cal = rows_csv(t + "/nso_collection_calendar_2026.csv")
    hol = {r["date"] for r in cal if r["event"] == "Public holiday"}
    idx = {r["date"][:7]: r["date"] for r in cal if r["event"] == "Index day"}

    def window(month):
        d = dt.date.fromisoformat(idx[month])
        days = []
        while len(days) < 5:
            if d.weekday() < 5 and d.isoformat() not in hol:
                days.append(d)
            d += dt.timedelta(days=1)
        return days[0], days[-1]
    done, tot, miss = defaultdict(int), defaultdict(int), defaultdict(int)
    for s in rows_csv(t + "/tallis_collection_schedule_2026q3.csv"):
        o = tnum[s["outlet_no"]]
        r = area[s["area"]]
        tn = s["outlet_no"]
        if o["In sample to"] is not None and excel_date(o["In sample to"]) < dt.date.fromisoformat(s["month"] + "-01"):
            nxt = [x for x in outlets if x["Address"] == o["Address"] and x["In sample from"] is not None
                   and excel_date(x["In sample from"]) == excel_date(o["In sample to"]) + dt.timedelta(days=1)]
            if nxt:
                tn = nxt[0]["Contractor outlet no."]
        days = visits.get((tn, s["month"]), [])
        tot[r] += 1
        a, b = window(s["month"])
        if not days:
            miss[r] += 1
        elif all(a <= d <= b for d in days):
            done[r] += 1
    for r in regions:
        tim = "%.1f" % (100.0 * done[r] / tot[r])
        check("V9 %s timeliness %s, missed %d" % (r, tim, miss[r]),
              fig["deliverables"][r]["timeliness"] == tim and fig["deliverables"][r]["missed_visits"] == miss[r])
    # replacement acceptance
    events = defaultdict(list)
    for (q, m), r in db.items():
        if r["status"] in ("R", "30") and m >= "2026-06":
            o = code[r["outlet_code"]]
            vd = sorted(visits.get((o["Contractor outlet no."], m), [])) or [dt.date.fromisoformat(m + "-01")]
            events[q].append((vd[0], m, o["Region"]))
    dec = xlsx_sheets(t + "/commodity_replacement_decisions_2026.xlsx")["Decisions"]
    dh = dec[0]
    last = {}
    for row in sorted((dict(zip(dh, r)) for r in dec[1:] if r), key=lambda x: (excel_date(x["Decided on"]), x["Review no."])):
        if row["Decision"] == "Query to contractor":
            continue
        when = excel_date(row["Decided on"])
        prior = sorted(e for e in events.get(str(row["Quote"]), []) if e[0] < when)
        if prior:
            last[(str(row["Quote"]), prior[-1][1])] = row["Decision"]
    acc_n, acc_d = defaultdict(int), defaultdict(int)
    for q, evs in events.items():
        for d0, m, r in evs:
            if m in ("2026-07", "2026-08", "2026-09"):
                acc_d[r] += 1
                acc_n[r] += last.get((q, m)) == "Comparable"
    for r in regions:
        share = "%.1f" % (100.0 * acc_n[r] / acc_d[r])
        check("V10 %s replacement acceptance %s" % (r, share), fig["deliverables"][r]["replacement_acceptance"] == share)
    # the golden deliverables read back
    gw = xlsx_sheets(g + "/pcqs_2026q3_assessment.xlsx")["Assessment"]
    gh = next(i for i, r in enumerate(gw) if r and r[0] == "Region")
    grows = {r[0]: r for r in gw[gh + 1:] if r and r[0] in regions}
    check("V11 golden workbook carries every region's outcome and figures",
          all(grows[r][2] == outs[r] and "%.1f" % grows[r][3] == fig["deliverables"][r]["timeliness"]
              and int(grows[r][4]) == fig["deliverables"][r]["missed_visits"]
              and "%.1f" % grows[r][5] == fig["deliverables"][r]["replacement_acceptance"] for r in regions))
    letter = pdf_strings(g + "/pcqs_2026q3_contractor_letter.pdf")
    check("V12 golden letter states the credit and every flagged region",
          "$" + fig["call"]["credit_dollars"] in letter and all(rname[r] in letter for r in regions if outs[r] != "Compliant"))
    print("%d failed" % len(FAILS))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3]))
