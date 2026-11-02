"""task304 architecture 4: the independent verifier. Reads only the bundle (target/, golden/, figures.json) on its own
code path: CSV through the csv module, XLSX through its XML parts (no openpyxl), PDF through pypdf, JSON, and the
golden deck through its slide XML. Recomputes every graded figure and the job-based easy route. Exit 1 on a mismatch."""
import csv
import datetime as dt
import json
import math
import os
import re
import sys
import zipfile
import zoneinfo
from collections import defaultdict
from xml.etree import ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
OUT = []


def ok(label, cond, detail=""):
    OUT.append((label, bool(cond), detail))


def csv_rows(name):
    with open(os.path.join(T, name), newline="", encoding="utf-8") as f:
        r = list(csv.reader(f))
    return r[0], r[1:]


def xlsx_sheet(name, sheet):
    z = zipfile.ZipFile(os.path.join(T, name))
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        root = ET.fromstring(z.read("xl/sharedStrings.xml"))
        for si in root.findall("m:si", NS):
            shared.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    rid = None
    for s in wb.find("m:sheets", NS):
        if s.get("name") == sheet:
            rid = s.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
    target = None
    for r in rels:
        if r.get("Id") == rid:
            target = r.get("Target")
    path = "xl/" + target.lstrip("/").replace("xl/", "")
    root = ET.fromstring(z.read(path))
    rows = []
    for row in root.iter("{%s}row" % NS["m"]):
        vals = {}
        for cell in row.findall("m:c", NS):
            ref = cell.get("r")
            col = re.match(r"[A-Z]+", ref).group(0)
            ci = 0
            for ch in col:
                ci = ci * 26 + (ord(ch) - 64)
            t = cell.get("t")
            v = cell.find("m:v", NS)
            if t == "s":
                val = shared[int(v.text)]
            elif t == "inlineStr":
                val = "".join(x.text or "" for x in cell.iter("{%s}t" % NS["m"]))
            elif v is None:
                val = None
            else:
                val = v.text
            vals[ci - 1] = val
        if vals:
            n = max(vals) + 1
            rows.append([vals.get(i) for i in range(n)])
    return rows


def xl_date(v):
    return dt.date(1899, 12, 30) + dt.timedelta(days=int(float(v)))


def pdf(name):
    from pypdf import PdfReader
    return " ".join((p.extract_text() or "") for p in PdfReader(os.path.join(T, name)).pages)


def lx(t, Li, Lf, La):
    t = min(max(t, 0.0), 7.0)
    return 10 * math.log10((t * 10 ** (Li / 10) + (7 - t) * 10 ** (Lf / 10) + 10 ** (La / 10)) / 8.0)


def main():
    F = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    hubs = ["Larapinta", "Eastern Creek", "Truganina", "Wingfield", "Kewdale", "Beresfield"]
    # ---- documents
    sv = re.sub(r"\s+", " ", pdf("noise_survey_report_2026.pdf"))
    de = re.sub(r"\s+", " ", pdf("induct_enclosure_design_report_rev2.pdf"))
    un = re.sub(r"\s+", " ", pdf("noise_enforceable_undertaking_schedule_2027.pdf"))
    ok("V-PDF1 the survey reads back (positive control)", "Occupational noise survey 2026" in sv and len(sv) > 800)
    ok("V-PDF2 the design report reads back", "Predicted levels" in de)
    ok("V-PDF3 the undertaking's clauses read back", "85 dB(A) or more" in un and "the places they worked during each shift" in un
       and "retest within 30 days" in un)
    lev = {}
    for hb in hubs:
        i = sv.index(hb + " (")
        nums = re.findall(r"(\d{2,3}\.\d)", sv[i:i + 500])
        lev[hb] = [float(nums[0]), float(nums[1]), float(nums[2])]
        m = re.search(re.escape(hb) + r"\s+(\d+)\s+(\d{2}\.\d)\s+(\d{2}\.\d)", de)
        lev[hb].append(float(m.group(3)))
    ok("V-LEV levels agree with figures.json", all(abs(lev[hb][0] - F["levels"][hb]["Li"]) < 1e-9 and
                                                   abs(lev[hb][3] - F["levels"][hb]["Lp"]) < 1e-9 for hb in hubs))
    # ---- people and shifts
    _, hr = csv_rows("hr_employee_list_20261113.csv")
    title = {r[0]: r[4] for r in hr}
    _, ta = csv_rows("ta_shift_records_20260928_20261108.csv")
    lo, hi = dt.date(2026, 10, 12), dt.date(2026, 11, 8)
    nshift = defaultdict(int)
    site = {}
    for r in ta:
        d = dt.date.fromisoformat(r[1])
        if r[4] == "WORKED" and lo <= d <= hi:
            nshift[r[0]] += 1
            site[r[0]] = r[3]
    tw = xlsx_sheet("labour_hire_timesheets_oct_nov_2026.xlsx", "Tasman Workforce")
    for r in tw[3:]:
        if r and r[0] and r[3]:
            d = xl_date(r[3])
            if lo <= d <= hi:
                nshift[r[0]] += 1
                site[r[0]] = r[2]
                title[r[0]] = "LH"
    mh = xlsx_sheet("labour_hire_timesheets_oct_nov_2026.xlsx", "Meridian Labour Hire")
    for r in mh[2:]:
        if not r or not r[0]:
            continue
        we = xl_date(r[3])
        for k in range(5):
            if k + 4 < len(r) and r[k + 4]:
                d = we - dt.timedelta(days=6 - k)
                if lo <= d <= hi:
                    nshift[r[0]] += 1
                    site[r[0]] = r[2]
                    title[r[0]] = "LH"
    bg = xlsx_sheet("badge_register_20261113.xlsx", "Badges")
    badges = defaultdict(list)
    for r in bg[1:]:
        iss = xl_date(r[5])
        can = xl_date(r[6]) if (len(r) > 6 and r[6]) else None
        badges[r[0]].append((r[1], r[2], iss, can))
    tz = {"BRL-BNE1": "Australia/Brisbane", "BRL-SYD2": "Australia/Sydney", "BRL-MEL1": "Australia/Melbourne",
          "BRL-ADL1": "Australia/Adelaide", "BRL-PER1": "Australia/Perth", "BRL-NTL1": "Australia/Sydney"}
    ih = defaultdict(float)
    with open(os.path.join(T, "wcs_operator_sessions_export_20261116.csv"), newline="", encoding="utf-8") as f:
        rd = csv.DictReader(f)
        n = 0
        for r in rd:
            n += 1
            on = dt.datetime.strptime(r["logon_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
            off = dt.datetime.strptime(r["logoff_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
            loc = on.astimezone(zoneinfo.ZoneInfo(tz[r["site_code"]])).replace(tzinfo=None)
            sd = (loc - dt.timedelta(hours=5)).date()
            if not (lo <= sd <= hi):
                continue
            who = None
            for typ, ref, iss, can in badges.get(r["badge_id"], []):
                if iss <= sd and (can is None or sd < can):
                    who = (typ, ref)
            if who is None or who[0] == "Contractor":
                continue
            ih[who[1]] += (off - on).total_seconds() / 3600.0
    ok("V-SPINE the session export has 25,000 rows or more", n >= 25000, str(n))
    pool = defaultdict(int)
    below = defaultdict(int)
    r0 = defaultdict(int)
    for ref, k in nshift.items():
        hb = site[ref]
        Li, Lf, La, Lp = lev[hb]
        t = ih.get(ref, 0.0) / k
        a, b = lx(t, Li, Lf, La), lx(t, Lp, Lf, La)
        pool[hb] += a >= 85
        below[hb] += (a >= 85) and (b < 85)
        tl = title.get(ref, "")
        seg = ("induct" in tl.lower()) or tl == "Sorter - Relief" or (tl == "LH" and ih.get(ref, 0) > 0)
        t0 = 7.0 if seg else 0.0
        r0[hb] += (lx(t0, Li, Lf, La) >= 85) and (lx(t0, Lp, Lf, La) < 85)
    ok("V-MAIN every hub's pool and count brought below recompute", all(pool[hb] == F["pool"][hb] and below[hb] == F["below"][hb] for hb in hubs),
       "%s %s" % (dict(pool), dict(below)))
    best = max(hubs, key=lambda hb: below[hb])
    ok("V-CALL the call recomputes: %s" % best, best == F["call_hub"])
    ok("V-EASY the job-based easy route files another hub (%s)" % max(hubs, key=lambda hb: r0[hb]),
       max(hubs, key=lambda hb: r0[hb]) != best and r0[best] == 0)
    # ---- ask A
    vend = json.load(open(os.path.join(T, "ppe_vending_transactions_2026q3.json"), encoding="utf-8"))["records"]
    _, vis = csv_rows("ppe_vending_service_visits_2026q3.csv")
    vsite = {"Brolga Larapinta DC": "Larapinta", "Brolga Eastern Creek DC": "Eastern Creek", "Brolga Truganina": "Truganina",
             "Brolga Wingfield": "Wingfield", "Brolga Kewdale DC": "Kewdale", "Brolga Beresfield": "Beresfield"}
    vtz = {"Larapinta": "Australia/Brisbane", "Eastern Creek": "Australia/Sydney", "Truganina": "Australia/Melbourne",
           "Wingfield": "Australia/Adelaide", "Kewdale": "Australia/Perth", "Beresfield": "Australia/Sydney"}
    moves = defaultdict(list)
    first = {}
    change = {}
    for r in sorted(vis, key=lambda r: dt.datetime.strptime(r[0], "%d/%m/%Y")):
        d = dt.datetime.strptime(r[0], "%d/%m/%Y").date()
        if r[1] not in first:
            first[r[1]] = vsite[r[2]]
        if r[3] == "COMMISSION":
            moves[r[1]].append((d, vsite[r[2]]))
        if r[3] == "RANGE CHANGE":
            change[r[1]] = d
    pairs = defaultdict(int)
    for rec in vend:
        if rec["product_code"] != "EP-01":
            continue
        m = rec["machine_id"]
        t = dt.datetime.strptime(rec["vend_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
        s = first[m]
        for d, ns in sorted(moves[m]):
            # a machine stands at its new hub from its commissioning day, local time there
            start = dt.datetime(d.year, d.month, d.day, tzinfo=zoneinfo.ZoneInfo(vtz[ns]))
            if t >= start:
                s = ns
        lt = t.astimezone(zoneinfo.ZoneInfo(vtz[s])).replace(tzinfo=None)
        pairs[(s, lt.month)] += 5 if lt.date() >= change[m] else 1
    ok("V-ASKA every hub's earplug pairs for July, August and September recompute",
       all(pairs[(hb, mo)] == F["pairs"][hb][str(mo)] for hb in hubs for mo in (7, 8, 9)))
    # ---- ask B
    _, au = csv_rows("audiometry_results_2025_2026.csv")
    cl = xlsx_sheet("audiometry_clients_20261106.xlsx", "Clients")
    emp_of = {r[0]: r[1] for r in cl[1:] if r and r[0]}
    _, trf = csv_rows("hr_site_transfers_2026.csv")
    tmap = {r[0]: (dt.datetime.strptime(r[3], "%d/%m/%Y").date(), r[1], r[2]) for r in trf}
    hr_site = {r[0]: r[3] for r in hr}
    tests = defaultdict(list)
    for r in au:
        tests[r[1]].append((dt.date.fromisoformat(r[2]), int(r[0]), r[3], [float(x) for x in r[5:11]]))
    sts = defaultdict(set)

    def sh(a, ref):
        return max(sum(a[i] - ref[i] for i in range(3)) / 3.0, sum(a[3 + i] - ref[3 + i] for i in range(3)) / 3.0)
    for c, ts in tests.items():
        ts.sort()
        ref = ts[0][3]
        for i, (d, tid, typ, th) in enumerate(ts):
            if typ != "ANNUAL" or sh(th, ref) < 10:
                continue
            for d2, tid2, typ2, th2 in ts[i + 1:]:
                if typ2 == "RETEST" and 0 < (d2 - d).days <= 30:
                    if sh(th2, ref) >= 10:
                        emp = emp_of[c]
                        hb = hr_site[emp]
                        if emp in tmap:
                            eff, fr, to = tmap[emp]
                            hb = fr if d2 < eff else to
                        if d2.year == 2026:
                            sts[hb].add(emp)
                        ref = th2
                    break
    ok("V-ASKB every hub's confirmed threshold shifts recompute", all(len(sts[hb]) == F["sts"][hb] for hb in hubs),
       str({hb: len(sts[hb]) for hb in hubs}))
    # ---- goldens
    g = os.path.join(TASK, "golden")
    with open(os.path.join(g, "hearing_program_2026.csv"), newline="", encoding="utf-8") as f:
        gr = list(csv.reader(f))[1:]
    ok("V-GOLD-CSV the asks' CSV carries the recomputed figures",
       all(int(r[1]) == pairs[(r[0], 7)] and int(r[2]) == pairs[(r[0], 8)] and int(r[3]) == pairs[(r[0], 9)]
           and int(r[4]) == len(sts[r[0]]) for r in gr) and len(gr) == len(hubs))
    z = zipfile.ZipFile(os.path.join(g, "induct_enclosure_2027.pptx"))
    s2 = z.read("ppt/slides/slide2.xml").decode("utf-8")
    texts = re.findall(r"<a:t>([^<]*)</a:t>", s2)
    okt = True
    for hb in hubs:
        i = texts.index(hb)
        okt &= texts[i + 1] == str(pool[hb]) and texts[i + 2] == str(below[hb])
    ok("V-GOLD-PPTX the deck's table carries every hub's figures", okt)
    charts = [n for n in z.namelist() if n.startswith("ppt/charts/chart") and n.endswith(".xml")]
    cx = z.read(charts[0]).decode("utf-8")
    vals = [float(v) for v in re.findall(r"<c:v>([0-9.]+)</c:v>", cx.split("<c:val>")[1].split("</c:val>")[0])]
    ok("V-GOLD-CHART the deck's chart plots the counts brought below", vals == [float(below[hb]) for hb in hubs])
    s1 = z.read("ppt/slides/slide1.xml").decode("utf-8")
    ok("V-GOLD-CALL the deck names the hub on its first slide", best in s1)
    fails = [x for x in OUT if not x[1]]
    for label, c_, d in OUT:
        print("%s  %s%s" % ("PASS" if c_ else "FAIL", label, ("  [" + d + "]") if (d and not c_) else ""))
    print("%d checks, %d FAIL" % (len(OUT), len(fails)))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
