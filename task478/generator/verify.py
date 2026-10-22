"""verify.py: recompute every graded figure from the shipped bundle alone, on its own code path (no generator module),
and compare with generator/figures.json and the golden files. Reads every format the pack ships, each through one
extractor with a positive control.

    python3 task478/generator/verify.py [target]
"""
import csv
import datetime as dt
import json
import os
import re
import statistics
import sys
import zipfile
from collections import defaultdict
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
ET = ZoneInfo("America/New_York")
UTC = dt.timezone.utc
OK = []
LB_PER_KG = 1 / 0.45359237


def ok(name, cond):
    OK.append((name, bool(cond)))
    print("%s  %s" % ("PASS" if cond else "FAIL", name))


def rows(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def sheet(path, name):
    """A worksheet's rows through the workbook's XML: shared strings and inline values, no spreadsheet library."""
    import xml.etree.ElementTree as ET_
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    with zipfile.ZipFile(path) as z:
        wb = ET_.fromstring(z.read("xl/workbook.xml"))
        names = [s.get("name") for s in wb.find("m:sheets", ns)]
        idx = names.index(name) + 1
        sst = []
        if "xl/sharedStrings.xml" in z.namelist():
            for si in ET_.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", ns):
                sst.append("".join(t.text or "" for t in si.iter("{%s}t" % ns["m"])))
        data = ET_.fromstring(z.read("xl/worksheets/sheet%d.xml" % idx))
    out = []
    for r in data.find("m:sheetData", ns):
        vals = {}
        for c in r.findall("m:c", ns):
            col = re.match(r"[A-Z]+", c.get("r")).group(0)
            v = c.find("m:v", ns)
            if v is None:
                continue
            vals[col] = sst[int(v.text)] if c.get("t") == "s" else v.text
        out.append(vals)
    return out


def table(raw, header_row=0):
    head = raw[header_row]
    cols = sorted(head, key=lambda c: (len(c), c))
    return [{head[c]: r.get(c) for c in cols} for r in raw[header_row + 1:]]


def pdf_text(path):
    import pdfplumber
    with pdfplumber.open(path) as pdf:
        return "\n".join(pg.extract_text() or "" for pg in pdf.pages)


def half_up(x):
    return int(x + 0.5)


def main(target=None):
    T = target or os.path.join(TASK, "target")
    j = lambda n: os.path.join(T, n)
    fig = json.load(open(os.path.join(HERE, "figures.json")))

    prog = pdf_text(j("ctpa_freight_compliance_program_2027.pdf"))
    flat = re.sub(r"\s+", " ", prog)
    ok("pdf read back: the program's limit (control)", "gross vehicle weight above 80,000 lb" in flat)
    secs = [(m.group(1), m.group(2), float(m.group(3)), float(m.group(4)))
            for m in re.finditer(r"^(\d\d) ([A-Z][A-Za-z ]+?) (\d+\.\d) (\d+\.\d)$", prog, re.M)]
    ok("pdf read back: the program's section table has twelve sections", len(secs) == 12)
    name = {c: n for c, n, a, b in secs}

    def section_at(mp):
        return next(c for c, n, a, b in secs if a <= mp < b)
    dic = re.sub(r"\s+", " ", pdf_text(j("ctpa_data_exports_dictionary.pdf")))
    ok("pdf read back: the dictionary's piezo layout (control)", "31-35 gross weight, tens of pounds" in dic)
    sched = re.sub(r"\s+", " ", pdf_text(j("ctpa_toll_schedule_2025.pdf")))
    ok("pdf read back: the 2025 schedule's P23 (control)", "P23 Brannock Road 38.1" in sched)

    st = {r["station_id"]: section_at(float(r["milepost"])) for r in rows(j("ctpa_wim_stations.csv"))}
    ok("csv read back: the station list places twelve stations, one a section", sorted(st.values()) == sorted(name))
    recs = defaultdict(list)                  # section -> (gross lb, steer lb)
    with open(j("ctpa_wim_piezo_2026.txt"), encoding="ascii") as fh:
        n_pz = 0
        for ln in fh:
            n_pz += 1
            if ln[26:28] != "09" or ln[95] != "0":
                continue
            recs[st[ln[0:4].strip()]].append((int(ln[30:35]) * 10, int(ln[35:39]) * 10))
    ok("fixed-width read back: %d piezo records (control: first station 511)" % n_pz, "511" in st and n_pz > 100000)
    n_bp = 0
    for r in rows(j("ctpa_wim_bendingplate_2026.csv")):
        n_bp += 1
        if r["fhwa_class"] != "9" or r["status"] != "OK":
            continue
        recs[st[r["site"]]].append((int(r["gvw_kg"]) * LB_PER_KG, int(r["ax1_kg"]) * LB_PER_KG))
    ok("csv read back: %d bending-plate records" % n_bp, n_bp > 50000)

    tk = table(sheet(j("ctpa_scale_house_tickets_2026.xlsx"), "Tickets 2026"))
    ok("xlsx read back: %d tickets with five axles each (control)" % len(tk), len(tk) == 2600 and
       all(r["Axle 5 (lb)"] for r in tk))
    t_loaded = [float(r["Axle 1 (lb)"]) for r in tk if sum(float(r["Axle %d (lb)" % i]) for i in range(1, 6)) > 50000]
    ref = statistics.median(t_loaded)
    share = {}
    for c in name:
        f = statistics.median([s for g, s in recs[c] if g > 50000]) / ref
        share[c] = 100.0 * sum(1 for g, s in recs[c] if g / f > 80000) / len(recs[c])
    five = sorted(sorted(share, key=lambda c: -share[c])[:5])
    ok("the five recompute: %s" % [name[c] for c in five],
       [name[c] for c in five] == fig["call"]["equip"])
    ok("the twelve shares recompute at whole per cent",
       all(half_up(share[c]) == fig["sections"][name[c]]["share_pct"] for c in name))
    ok("the tickets' loaded steer median recomputes (%d lb)" % ref,
       int(round(ref)) == fig["components"]["ticket_loaded_steer_lb"])

    # ask B: weekday entries
    pl = rows(j("ctpa_toll_plazas.csv"))
    since = {r["plaza"]: (section_at(float(r["milepost"])), r["in_service_from"]) for r in pl}
    old_code = {m.group(1): section_at(float(m.group(2)))
                for m in re.finditer(r"(P\d\d) [A-Z][A-Za-z0-9 ]+? (\d+\.\d) ", sched)}

    def sec_of(code, day):
        s, frm = since[code]
        if frm and day < dt.date.fromisoformat(frm):
            return old_code[code]
        return s
    ent = rows(j("ctpa_toll_entries_5axle_2026.csv"))
    ok("csv read back: %d toll entries (control: an old-host id)" % len(ent), ent[0]["txn_id"].isdigit())
    # the old host's rows (numeric ids) carry its local receipt stamp to the minute; a new-host row stamped within 16
    # minutes before (or the minute after) an old-host row of the same tag and plaza is the backfill of that entry
    parse = lambda t: dt.datetime.strptime(t, "%Y-%m-%d %H:%M:%S" if len(t) > 16 else "%Y-%m-%d %H:%M")
    olds = defaultdict(list)
    for r in ent:
        if r["txn_id"].isdigit():
            olds[(r["tag_id"], r["plaza"])].append(parse(r["entry_utc"]))
    keep = []
    for r in ent:
        t = parse(r["entry_utc"])
        if r["txn_id"].isdigit():
            keep.append((r["tag_id"], r["plaza"], t))
            continue
        if any(-60 <= (o - t).total_seconds() <= 960 for o in olds.get((r["tag_id"], r["plaza"]), ())):
            continue
        keep.append((r["tag_id"], r["plaza"], t.replace(tzinfo=UTC).astimezone(ET).replace(tzinfo=None)))
    wk = defaultdict(int)
    for tag, p, loc in keep:
        if loc.year == 2026 and loc.weekday() < 5:
            wk[sec_of(p, loc.date())] += 1
    days = sum(1 for k in range(365) if (dt.date(2026, 1, 1) + dt.timedelta(days=k)).weekday() < 5)
    ok("261 weekdays in 2026 (%d)" % days, days == 261)
    ok("ask B recomputes: every section's weekday entries",
       all(half_up(wk[c] / days) == fig["sections"][name[c]]["weekday_entries"] for c in name))

    # ask A: gross citations by the trip's entry
    by_tag = defaultdict(list)
    for tag, p, loc in keep:
        by_tag[tag].append((loc, p))
    for v in by_tag.values():
        v.sort()
    cit = rows(j("ctpa_citations_2026.csv"))
    ok("csv read back: %d citation rows (control: violation codes G and T)" % len(cit),
       {r["violation"] for r in cit} == {"G", "T"})
    ca = defaultdict(int)
    for r in cit:
        if r["violation"] != "G":
            continue
        when = dt.datetime.strptime(r["issued"], "%m/%d/%Y %H:%M")
        loc, p = [x for x in by_tag[r["tag_id"]] if x[0] <= when][-1]
        ca[sec_of(p, loc.date())] += 1
    ok("ask A recomputes: every section's gross citations",
       all(ca[c] == fig["sections"][name[c]]["gross_citations"] for c in name))

    # the golden files read back
    gx = os.path.join(TASK, "golden", "ctpa_vws_sections_2027.xlsx")
    s2 = table(sheet(gx, "Sections"))
    body = [r for r in s2 if r.get("Section") in name]
    ok("golden xlsx read back: twelve sections, the shares, entries and citations as recomputed",
       len(body) == 12 and all(half_up(float(r["Share of class 9 trucks over 80,000 lb"]) * 100) == half_up(share[r["Section"]])
                               and int(r["Five-axle entries a weekday"]) == half_up(wk[r["Section"]] / days)
                               and int(r["Gross overweight citations"]) == ca[r["Section"]] for r in body))
    ok("golden xlsx: the five marked Yes are the recomputed five",
       sorted(r["Section"] for r in body if r["Equip 2027"] == "Yes") == five)
    s1 = sheet(gx, "Sites 2027")
    sites = [r.get("A") for r in s1 if r.get("A") in name]
    ok("golden xlsx: the Sites sheet lists the five", sorted(sites) == five)
    gc = rows(os.path.join(TASK, "golden", "ctpa_section_overweight_2026.csv"))
    ok("golden csv read back: twelve rows matching the recomputed shares",
       [(r["section"], int(r["share_over_80000_lb_pct"])) for r in gc] == [(c, half_up(share[c])) for c in sorted(name)])
    svg = open(os.path.join(TASK, "golden", "ctpa_overweight_share_2026.svg"), encoding="utf-8").read()
    ok("golden svg read back: an SVG with every section's name", svg.lstrip().startswith("<?xml") and
       all(name[c] in svg for c in name))
    n_fail = sum(1 for _, c in OK if not c)
    print("%s  task478 verify: %d checks, %d failed" % ("PASS" if not n_fail else "FAIL", len(OK), n_fail))
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
