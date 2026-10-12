"""Independent verifier: reads only target/ and deliverables/, shares no code with the generator, and
recomputes the replay, the tie-outs, the verification outcomes and every graded figure."""
import csv
import datetime as dt
import os
import re
import sys
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
from zoneinfo import ZoneInfo

from openpyxl import load_workbook
from pypdf import PdfReader
from docx import Document

TASK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(TASK, "target")
OUTD = os.path.join(TASK, "deliverables")
D = Decimal
Z = D("0")
C = D("0.01")
SYD = ZoneInfo("Australia/Sydney")
FAILS = []


def ok(name, cond, detail=""):
    if not cond:
        FAILS.append("%s %s" % (name, detail))
        print("FAIL", name, detail)


def q(x):
    return D(x).quantize(C, rounding=ROUND_HALF_UP)


def m_of(d):
    return d.year * 12 + d.month - 1


# ------------------------------------------------------------------ read the files
wb = load_workbook(os.path.join(T, "YCB_asset_register_2026-10-02.xlsx"), data_only=True)
ws = wb["Register"]
hdr = [c.value for c in ws[4]]
REG = []
for row in ws.iter_rows(min_row=5, values_only=True):
    if row[0] is None:
        continue
    r = dict(zip(hdr, row))
    r["Asset No"] = str(r["Asset No"])
    r["Cost (ex GST)"] = q(r["Cost (ex GST)"])
    r["Date Acquired"] = r["Date Acquired"].date() if hasattr(r["Date Acquired"], "date") else r["Date Acquired"]
    if r["Date Disposed"] is not None and hasattr(r["Date Disposed"], "date"):
        r["Date Disposed"] = r["Date Disposed"].date()
    REG.append(r)
SITE_CODE = {"Charlestown": "CHA", "Maitland": "MAI", "Cessnock": "CES", "Raymond Terrace": "RAY"}
LIFE = {"Medical imaging equipment": 120, "Options & accessories": 60, "Ultrasound": 72, "Computer equipment": 48,
        "Leasehold improvements": 180, "Furniture & fittings": 120, "Motor vehicles": 72}
ACC = {"Medical imaging equipment": ("1-6110", "1-6115", "6-2110"), "Equipment upgrades": ("1-6110", "1-6115", "6-2110"),
       "Options & accessories": ("1-6110", "1-6115", "6-2110"), "Ultrasound": ("1-6120", "1-6125", "6-2120"),
       "Computer equipment": ("1-6130", "1-6135", "6-2130"), "Leasehold improvements": ("1-6140", "1-6145", "6-2140"),
       "Furniture & fittings": ("1-6150", "1-6155", "6-2150"), "Motor vehicles": ("1-6160", "1-6165", "6-2160")}

GL = []
with open(os.path.join(T, "YCB_GL_detail_2025-07_to_2026-09.csv"), encoding="utf-8") as fh:
    for r in csv.DictReader(fh):
        r["Debit"] = D(r["Debit"]) if r["Debit"] else Z
        r["Credit"] = D(r["Credit"]) if r["Credit"] else Z
        GL.append(r)
ok("gate: GL detail over 10,000 rows", len(GL) > 10000, len(GL))

APPR = list(csv.DictReader(open(os.path.join(T, "YCB_capital_approvals_2018-2026.csv"), encoding="utf-8")))
SCANS = list(csv.DictReader(open(os.path.join(T, "verification_scans_YCB_2026.csv"), encoding="utf-8")))

tbw = load_workbook(os.path.join(T, "YCB_trial_balance_30-09-2026.xlsx"), data_only=True)
def tb(ws_):
    out = {}
    for row in ws_.iter_rows(min_row=6, values_only=True):
        if row[0]:
            out[row[0]] = q(row[2] or 0) - q(row[3] or 0)
    return out
TB1, TB2 = tb(tbw.worksheets[0]), tb(tbw.worksheets[1])

fy = "\n".join(p.extract_text() for p in PdfReader(os.path.join(T, "YCB_FY2025_financial_statements_extract.pdf")).pages)
imp_amt = D(re.search(r"impairment loss of \$([\d,]+)", fy).group(1).replace(",", ""))
ok("FY2025: impairment stated", imp_amt == D("38000"))
ok("FY2025: computer equipment life change stated", "From 1 July 2025 computer equipment is" in fy.replace("\n", " "))

# ------------------------------------------------------------------ the population
ledger_rows = [r for r in REG if r["Capitalised"] == "Y"]
# repeated invoice lines: same invoice, serial, cost, date and description; keep the lower number
seen_key, dups = {}, set()
for r in sorted(ledger_rows, key=lambda r: int(r["Asset No"])):
    k = (r["Invoice No"], r["Serial No"], r["Cost (ex GST)"], r["Date Acquired"], r["Description"])
    if r["Invoice No"] and k in seen_key:
        dups.add(r["Asset No"])
    else:
        seen_key[k] = r["Asset No"]
ledger_rows = [r for r in ledger_rows if r["Asset No"] not in dups]
BY = {r["Asset No"]: r for r in ledger_rows}
host_of = {}
for a in APPR:
    if a["Request Type"] != "Upgrade" or a["Status"] != "Completed":
        continue
    ok("approvals: an upgrade row carries no Existing Asset key", not a["Existing Asset"], a["Approval Ref"])
    mt = re.match(r"^(.*) for (.+), (Charlestown|Maitland|Cessnock|Raymond Terrace)$", a["Description"])
    ok("approvals: upgrade request text names a system and a site", mt is not None, a["Description"])
    if not mt:
        continue
    system, site = mt.group(2), mt.group(3)
    done = dt.datetime.strptime(a["Date Completed"], "%d/%m/%Y").date()
    pool = [r for r in ledger_rows if r["Category"] == "Medical imaging equipment" and r["Date Acquired"] <= done
            and (r["Date Disposed"] is None or r["Date Disposed"] > done)]
    # three readings of the text: the register's model prefix, a prefix match, a case-blind containment
    readings = [
        [r for r in pool if r["Site"] == site and r["Description"].split(" - ")[0] == system],
        [r for r in pool if r["Site"] == site and r["Description"].startswith(system)],
        [r for r in pool if r["Site"] == site and system.lower() in r["Description"].lower()],
    ]
    ids = [sorted(x["Asset No"] for x in rd) for rd in readings]
    ok("approvals: %s names exactly one in-service system under every reading" % a["Approval Ref"],
       all(len(i) == 1 for i in ids) and len(set(tuple(i) for i in ids)) == 1, ids)
    if ids[0]:
        host_of[a["Approval Ref"]] = ids[0][0]

# the Bremer transfer: brought-forward depreciation and the source's in-service date and life, from the IC journal
tr_line = [r for r in GL if r["Memo"].startswith("IC transfer in") and r["Account No"] == "1-6125"][0]
bf = tr_line["Credit"]
mm = re.search(r"in service (\d\d)/(\d\d)/(\d{4}), (\d+) yr life", tr_line["Memo"])
src_in = dt.date(int(mm.group(3)), int(mm.group(2)), int(mm.group(1)))
src_life = int(mm.group(4)) * 12


def sl(dep, life, start):
    if life <= 0 or dep <= 0:
        return {}
    mon = q(dep / life)
    out, acc = {}, Z
    for k in range(life):
        a = mon if k < life - 1 else dep - acc
        out[start + k] = a
        acc += a
    return out


SCH = {}
IMP_M = 2025 * 12 + 5          # June 2025
CHG = 2025 * 12 + 6            # July 2025
opg = [r for r in ledger_rows if r["Description"].startswith("OPG / CBCT")][0]


def schedule(r):
    no = r["Asset No"]
    if no in SCH:
        return SCH[no]
    cat, cost, st = r["Category"], r["Cost (ex GST)"], m_of(r["Date Acquired"])
    if cat == "Equipment upgrades":
        host = BY[host_of[r["Approval Ref"]]]
        he = max(schedule(host))
        s = sl(cost, he - st + 1, st)
    elif r["Supplier"] and "intercompany" in r["Supplier"]:
        src_end = m_of(src_in) + 1 + src_life - 1
        s = sl(cost - bf, src_end - st + 1, st)
    elif cat == "Computer equipment" and st < CHG:
        old = sl(cost, 36, st)
        before = {k: x for k, x in old.items() if k < CHG}
        if len(before) >= 36:
            s = before
        else:
            s = dict(before)
            s.update(sl(cost - sum(before.values(), Z), 48 - len(before), CHG))
    else:
        s = sl(cost, LIFE[cat], st)
        if r is opg:
            before = {k: x for k, x in s.items() if k <= IMP_M}
            s2 = dict(before)
            s2.update(sl(cost - sum(before.values(), Z) - imp_amt, max(s) - IMP_M, IMP_M + 1))
            s = s2
    if r["Date Disposed"]:
        dm = m_of(r["Date Disposed"])
        s = {k: x for k, x in s.items() if k <= dm}
    SCH[no] = s
    return s


def accum(r, m):
    s = schedule(r)
    a = sum((x for k, x in s.items() if k <= m), Z)
    if r["Supplier"] and "intercompany" in r["Supplier"]:
        a += bf
    if r is opg and m >= IMP_M:
        a += imp_amt
    return a


# ------------------------------------------------------------------ the replay
REPLAY = list(range(2025 * 12 + 6, 2026 * 12 + 9))
posted = defaultdict(lambda: Z)
for r in GL:
    if r["Src"] == "GJ" and r["Memo"].startswith("Depreciation ") and r["Account No"].startswith("6-21"):
        d = dt.datetime.strptime(r["Date"], "%d/%m/%Y").date()
        posted[(r["Account No"], m_of(d))] += r["Debit"]
rebuilt = defaultdict(lambda: Z)
for r in ledger_rows:
    for m, x in schedule(r).items():
        if m in REPLAY:
            rebuilt[(ACC[r["Category"]][2], m)] += x
ok("replay: 90 cells posted", len(posted) == 90, len(posted))
miss = [k for k in posted if posted[k] != rebuilt.get(k, Z)]
ok("replay: every posted cell reproduced to the cent", not miss, miss[:5])

# ------------------------------------------------------------------ tie-outs
SEP26 = 2026 * 12 + 8
DEC26 = 2026 * 12 + 11
cost_b, acc_b = defaultdict(lambda: Z), defaultdict(lambda: Z)
for r in ledger_rows:
    if m_of(r["Date Acquired"]) > SEP26 or (r["Date Disposed"] and m_of(r["Date Disposed"]) <= SEP26):
        continue
    ca, aa, _ = ACC[r["Category"]]
    cost_b[ca] += r["Cost (ex GST)"]
    acc_b[aa] += accum(r, SEP26)
for k in cost_b:
    ok("tie: %s cost to the first TB run" % k, cost_b[k] == TB1.get(k, Z), (cost_b[k], TB1.get(k)))
for k in acc_b:
    ok("tie: %s accumulated to the first TB run" % k, -acc_b[k] == TB1.get(k, Z), (acc_b[k], TB1.get(k)))
moved = TB1["1-6150"] - TB2["1-6150"]
joinery = [r for r in ledger_rows if r["Category"] == "Furniture & fittings" and r["Cost (ex GST)"] == moved]
ok("tie: the second TB run moves exactly one furniture asset's cost to leasehold", len(joinery) == 1 and TB2["1-6140"] - TB1["1-6140"] == moved)
ok("tie: and its accumulated depreciation", len(joinery) == 1 and TB1["1-6155"] - TB2["1-6155"] == -accum(joinery[0], SEP26))
joinery_no = joinery[0]["Asset No"] if joinery else None

# ------------------------------------------------------------------ note 9: the 2025 year and its 2024 comparative
CATS9 = ["Medical imaging equipment", "Ultrasound", "Computer equipment", "Leasehold improvements", "Furniture & fittings", "Motor vehicles"]
SCH5 = {}


def schedule_five(r):
    """The same rebuild with every upgrade on a single five-year life."""
    if r["Category"] != "Equipment upgrades":
        return schedule(r)
    if r["Asset No"] not in SCH5:
        SCH5[r["Asset No"]] = sl(r["Cost (ex GST)"], 60, m_of(r["Date Acquired"]))
    return SCH5[r["Asset No"]]


def accum_on(sched, r, m):
    a = sum((x for k, x in sched(r).items() if k <= m), Z)
    if r["Supplier"] and "intercompany" in r["Supplier"]:
        a += bf
    if r is opg and m >= IMP_M:
        a += imp_amt
    return a


def note9(sched, year):
    y0, y1 = (year - 1) * 12 + 6, year * 12 + 5
    out = {c: [Z, Z, Z] for c in CATS9}               # cost, accumulated, depreciation for the year
    for r in ledger_rows:
        if m_of(r["Date Acquired"]) > y1:
            continue
        c = "Medical imaging equipment" if r["Category"] in ("Medical imaging equipment", "Equipment upgrades", "Options & accessories") else r["Category"]
        s = sched(r)
        in_year = sum((x for k, x in s.items() if y0 <= k <= y1), Z)
        if r["Date Disposed"] and m_of(r["Date Disposed"]) <= y1:
            if m_of(r["Date Disposed"]) >= y0:
                out[c][2] += in_year
            continue
        out[c][0] += r["Cost (ex GST)"]
        out[c][1] += accum_on(sched, r, y1)
        out[c][2] += in_year
    return out


heads = [mt.end() for mt in re.finditer(r"Depreciation for\s+the\s+year", fy)]
ok("note 9: two tables, the 2025 year and the 2024 comparative", len(heads) == 2, len(heads))
pub9 = {}
for year, at in zip((2025, 2024), heads):
    nums = [D(x.replace(",", "")) for x in re.findall(r"\d{1,3}(?:,\d{3})+|\d+", fy[at:])][:28]
    pub9[year] = {c: nums[4 * j:4 * j + 4] for j, c in enumerate(CATS9 + ["Total"])}
for year in (2025, 2024):
    mine = note9(schedule, year)
    for c in CATS9:
        cost_, acc_, dep_ = mine[c]
        p = pub9[year][c]
        ok("note 9 %d: %s reproduces to the dollar" % (year, c),
           abs(cost_ - p[0]) < 1 and abs(acc_ - p[1]) < 1 and abs(cost_ - acc_ - p[2]) < 1 and abs(dep_ - p[3]) < 1, (mine[c], p))
# the five-year reading: the replay and both trial balance runs certify it, and only the 2024 comparative refuses it
reb5 = defaultdict(lambda: Z)
for r in ledger_rows:
    for m, x in schedule_five(r).items():
        if m in REPLAY:
            reb5[(ACC[r["Category"]][2], m)] += x
ok("five-year: every posted cell reproduced to the cent", all(posted[k] == reb5.get(k, Z) for k in posted))
acc5 = defaultdict(lambda: Z)
for r in ledger_rows:
    if m_of(r["Date Acquired"]) > SEP26 or (r["Date Disposed"] and m_of(r["Date Disposed"]) <= SEP26):
        continue
    acc5[ACC[r["Category"]][1]] += accum_on(schedule_five, r, SEP26)
ok("five-year: every accumulated balance ties to the first TB run", all(-acc5[k] == TB1.get(k, Z) for k in acc5))
miss5 = []
for year in (2025, 2024):
    five = note9(schedule_five, year)
    for c in CATS9:
        for j, (got, p) in enumerate(zip([five[c][0], five[c][1], five[c][0] - five[c][1], five[c][2]], pub9[year][c])):
            if abs(got - p) >= 1:
                miss5.append((year, c, j, got - p))
ok("five-year: note 9 refuses it only on the 2024 imaging depreciation",
   [(y, c, j) for y, c, j, _ in miss5] == [(2024, "Medical imaging equipment", 3)], miss5)
ok("five-year: by $5,000 or more", bool(miss5) and abs(miss5[0][3]) >= 5000, miss5)

# ------------------------------------------------------------------ verification
cutoff = dt.datetime(2026, 10, 9, 17, 0, tzinfo=SYD)
wstart = dt.datetime(2026, 9, 28, 0, 0, tzinfo=SYD)
by_tag = {r["Tag"]: r for r in REG if r["Tag"]}
by_ser = {r["Serial No"]: r for r in REG if r["Serial No"] and r["Asset No"] not in dups}
REGD = {r["Asset No"]: r for r in REG}


def utc(x):
    return dt.datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)


# each handheld numbers its scans in the order it takes them: a run whose clock reads earlier than the scan
# before it was taken between that scan and the next one whose clock runs on
by_dev = defaultdict(list)
for s in SCANS:
    by_dev[s["scanner"]].append(s)
inside = {}
reset_runs = []
for devname, rows in by_dev.items():
    rows.sort(key=lambda s: int(s["scan_id"]))
    times = [utc(s["scanned_at_utc"]) for s in rows]
    i, last = 0, None
    while i < len(rows):
        if last is not None and times[i] < last:
            j = i
            while j < len(rows) and times[j] < last:
                j += 1
            nxt = times[j] if j < len(rows) else None
            run = rows[i:j]
            reset_runs.append((devname, run, last, nxt))
            ok_in = nxt is not None and last.astimezone(SYD) >= wstart and nxt.astimezone(SYD) < cutoff
            for s in run:
                inside[s["scan_id"] + devname] = ok_in
            i = j
            continue
        inside[rows[i]["scan_id"] + devname] = wstart <= times[i].astimezone(SYD) < cutoff
        last = times[i]
        i += 1
ok("scans: one run on one handheld reads a clock earlier than the scan before it", len(reset_runs) == 1, [(r[0], len(r[1])) for r in reset_runs])
if reset_runs:
    devname, run, last, nxt = reset_runs[0]
    ok("scans: the run sits between two scans inside the window", inside[run[0]["scan_id"] + devname])
    ok("scans: the run includes an asset bought after the time its clock shows",
       any(r["tag"] in by_tag and by_tag[r["tag"]]["Date Acquired"] > utc(r["scanned_at_utc"]).date() for r in run))
mixed = [s for s in SCANS if s["tag"] and s["serial"] and s["tag"] in by_tag and s["serial"] in by_ser
         and by_tag[s["tag"]]["Asset No"] != by_ser[s["serial"]]["Asset No"]]
ok("scans: one scan reads a tag and a rating plate that belong to different units", len(mixed) == 1, len(mixed))
sighted = {}
for s in sorted(SCANS, key=lambda s: (s["scanner"], int(s["scan_id"]))):
    if not inside[s["scan_id"] + s["scanner"]]:
        continue
    hit = by_ser[s["serial"]] if s["serial"] in by_ser else by_tag.get(s["tag"])
    if hit is not None:
        sighted[hit["Asset No"]] = s["site_code"]
sheet = "\n".join(p.extract_text() for p in PdfReader(os.path.join(T, "RAY_count_sheet_07-10-2026.pdf")).pages)
extra_part = sheet.split("Also found on site, not on sheet:")[1] if "Also found on site" in sheet else ""
lines_ = [x.strip() for x in sheet.split("Also found on site, not on sheet:")[0].splitlines() if x.strip()]
i = 0
while i < len(lines_):
    if re.fullmatch(r"H\d{5}", lines_[i]) and i + 3 < len(lines_) and re.fullmatch(r"\d+", lines_[i + 1]):
        if lines_[i + 3] == "v":
            sighted[by_tag[lines_[i]]["Asset No"]] = "RAY"
        i += 4
    else:
        i += 1
for tag in re.findall(r"(H\d{5})", extra_part):
    sighted[by_tag[tag]["Asset No"]] = "RAY"

# ------------------------------------------------------------------ the load and the figures
MAPV2 = {}
mw = load_workbook(os.path.join(T, "group_asset_class_mapping.xlsx"), data_only=True)
log = {row[0]: row[2] for row in mw["Log"].iter_rows(min_row=2, values_only=True)}
approved = [v for v, st in log.items() if st == "Approved"][0]
for row in mw[approved].iter_rows(min_row=4, values_only=True):
    if row[0] == "YCB":
        MAPV2[row[1]] = row[3]
H2M = list(range(2027 * 12, 2027 * 12 + 6))
Q4M = [2026 * 12 + 9, 2026 * 12 + 10, 2026 * 12 + 11]
load = []
written_off = []
for r in ledger_rows:
    if r["Date Disposed"]:
        continue
    nbv = r["Cost (ex GST)"] - accum(r, DEC26)
    if r["Tag"] and r["Asset No"] not in sighted and nbv == 0:
        written_off.append(r)
        continue
    s = schedule(r)
    end = max(s) if s else DEC26
    rem = max(0, end - DEC26)
    g = sl(nbv, rem, 2027 * 12) if rem > 0 and nbv > 0 else {}
    acct = "1-6140" if r["Asset No"] == joinery_no else ACC[r["Category"]][0]
    load.append(dict(no=r["Asset No"], site=sighted.get(r["Asset No"], SITE_CODE[r["Site"]]), cls=MAPV2[acct], cost=r["Cost (ex GST)"],
                     acc=accum(r, DEC26), nbv=nbv, rem=rem, h2=sum((g[m] for m in H2M if m in g), Z),
                     q4=sum((s[m] for m in Q4M if m in s), Z), sep=r["Cost (ex GST)"] - accum(r, SEP26)))
H2 = sum((x["h2"] for x in load), Z)
print("verifier: H2 %s, %d rows, %d written off" % (H2, len(load), len(written_off)))


def whole(x):
    return int(D(x).quantize(D("1"), rounding=ROUND_HALF_UP))


# ------------------------------------------------------------------ the golden load file
gl_rows = list(csv.DictReader(open(os.path.join(OUTD, "fa_load_2027-01-01.csv"), encoding="utf-8")))
ok("golden load: row count", len(gl_rows) == len(load), (len(gl_rows), len(load)))
L_BY = {x["no"]: x for x in load}
for g in gl_rows:
    x = L_BY.get(g["asset_number"])
    if x is None:
        ok("golden load: asset %s is in the recomputed load" % g["asset_number"], False)
        continue
    for col, key in (("cost", "cost"), ("accumulated_depreciation", "acc"), ("net_book_value", "nbv"), ("depreciation_jan_jun_2027", "h2")):
        ok("golden load: %s %s" % (g["asset_number"], col), D(g[col]) == x[key], (g[col], x[key]))
    ok("golden load: %s remaining" % g["asset_number"], int(g["remaining_life_months"]) == x["rem"])
    ok("golden load: %s site" % g["asset_number"], g["site"] == x["site"], (g["site"], x["site"]))
    ok("golden load: %s class" % g["asset_number"], g["group_asset_class"] == x["cls"])

# ------------------------------------------------------------------ the golden note
doc = Document(os.path.join(OUTD, "cutover_signoff.docx"))
text = "\n".join(p.text for p in doc.paragraphs)
lead = [p.text for p in doc.paragraphs if p.text.startswith("The group ledger will post")]
ok("golden note: the figure leads the note", bool(lead) and "${:,}".format(whole(H2)) in lead[0], whole(H2))
names = {"CHA": "Charlestown", "MAI": "Maitland", "CES": "Cessnock", "RAY": "Raymond Terrace"}
t_sites, t_nil, t_cls = doc.tables[0], doc.tables[1], doc.tables[2]
def money(sv):
    return int(sv.replace("$", "").replace(",", ""))
for row in t_sites.rows[1:5]:
    s = [k for k, v in names.items() if v == row.cells[0].text][0]
    xs = [x for x in load if x["site"] == s]
    for i, key in enumerate(("sep", "q4", "nbv", "h2"), 1):
        ok("golden note: %s %s" % (s, key), money(row.cells[i].text) == whole(sum((x[key] for x in xs), Z)),
           (row.cells[i].text, whole(sum((x[key] for x in xs), Z))))
for row in t_nil.rows[1:5]:
    s = [k for k, v in names.items() if v == row.cells[0].text][0]
    xs = [x for x in load if x["site"] == s and x["nbv"] == 0]
    ok("golden note: %s nil count" % s, int(row.cells[1].text) == len(xs), (row.cells[1].text, len(xs)))
    ok("golden note: %s nil cost" % s, money(row.cells[2].text) == whole(sum((x["cost"] for x in xs), Z)))
for row in t_cls.rows[1:-1]:
    xs = [x for x in load if x["cls"] == row.cells[0].text]
    ok("golden note: class %s" % row.cells[0].text, money(row.cells[1].text) == whole(sum((x["nbv"] for x in xs), Z)))

# H9: the registers name every shipped file
shipped = set(os.listdir(T))
src = open(os.path.join(T, "sources_and_licences.txt"), encoding="utf-8").read()
named = set(re.findall(r"^([A-Za-z0-9_.-]+\.(?:xlsx|csv|pdf|eml|md|txt)):", src, flags=re.M))
ok("H9: sources_and_licences.txt names every other shipped file", named == shipped - {"sources_and_licences.txt"},
   sorted(named ^ (shipped - {"sources_and_licences.txt"})))
notes = open(os.path.join(T, "YCB_extract_notes.md"), encoding="utf-8").read()
in_notes = set(re.findall(r"^\| ([A-Za-z0-9_.-]+\.(?:xlsx|csv|pdf|eml|md|txt)) \|", notes, flags=re.M))
ok("H9: the extract notes list every file but themselves and the sources record",
   in_notes == shipped - {"sources_and_licences.txt", "YCB_extract_notes.md"},
   sorted(in_notes ^ (shipped - {"sources_and_licences.txt", "YCB_extract_notes.md"})))
# H11: one submission and one prompt in the task tree
found = [os.path.join(dp, f) for dp, dn, fn in os.walk(TASK) for f in fn if f in ("submission.md", "prompt.md")]
ok("H11: exactly one submission.md and one prompt.md", sorted(os.path.basename(f) for f in found) == ["prompt.md", "submission.md"], found)
# the write-up's figures recompute
sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
for label, val in (("committed figure", whole(H2)), ("load book value", whole(sum((x["nbv"] for x in load), Z)))):
    ok("submission: %s $%s stated" % (label, "{:,}".format(val)), "${:,}".format(val) in sub)
ok("submission: load rows", "%d assets load" % len(load) in sub)
ok("submission: written off", "%d nil-book-value assets" % len(written_off) in sub)
ok("submission: Oct-Dec total", "${:,}".format(whole(sum((x["q4"] for x in load), Z))) in sub)
for s_, nm in names.items():
    xs = [x for x in load if x["site"] == s_]
    line = "%s: %s" % (nm, ", ".join("${:,}".format(whole(sum((x[k] for x in xs), Z))) for k in ("sep", "q4", "nbv", "h2")))
    ok("submission: site line %s" % nm, line in sub, line)
    nil = [x for x in xs if x["nbv"] == 0]
    ok("submission: nil line %s" % nm, "%s: %d assets, ${:,}".format(whole(sum((x["cost"] for x in nil), Z))) % (nm, len(nil)) in sub)
for cls in sorted({x["cls"] for x in load}):
    ok("submission: class %s" % cls, "%s: ${:,}".format(whole(sum((x["nbv"] for x in load if x["cls"] == cls), Z))) % cls in sub)

print("verifier: %d failures" % len(FAILS))
sys.exit(1 if FAILS else 0)
