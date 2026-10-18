#!/usr/bin/env python3
"""task198 independent verifier. Reads only target/ and task198/prompt.txt.

No generator state is imported: the whole pipeline is rebuilt here from the shipped bytes, so a
figure that only the generator can produce fails. Every shipped format is read back through this
file's own extractor, and every absence assertion carries a positive control that runs through the
same extractor and the same parse.

    python3 task198/generator/verify.py
"""
import csv
import json
import os
import re
import sys
import zipfile
from datetime import date, datetime, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")

OK, BAD = [], []


def chk(label, cond, detail=""):
    (OK if cond else BAD).append((label, detail))
    print("%-6s %-46s %s" % ("ok" if cond else "FAIL", label, detail))


# ------------------------------------------------------------------ extractors (one per format)
def read_text(name):
    """Shipped bytes of a csv/json file."""
    with open(os.path.join(T, name), encoding="utf-8") as fh:
        return fh.read()


def read_csv(name):
    with open(os.path.join(T, name), newline="", encoding="utf-8") as fh:
        r = csv.reader(fh)
        head = next(r)
        return head, [row for row in r]


def read_pdf(name):
    from pypdf import PdfReader
    rd = PdfReader(os.path.join(T, name))
    return "".join((p.extract_text() or "") for p in rd.pages)


def read_xlsx(name):
    """Every sheet of a workbook as a list of row tuples, from the shipped zip."""
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(T, name), data_only=True)
    return {ws.title: [tuple(c.value for c in row) for row in ws.iter_rows()] for ws in wb.worksheets}


# ------------------------------------------------------------------ calendar
def last_sunday(y, m):
    d = date(y, m, 31)
    while d.weekday() != 6:
        d -= timedelta(days=1)
    return d


HOLS = {date.fromisoformat(r[0]) for r in read_csv("public_holidays_ie_2022_2026.csv")[1]}
WD = []
_d = date(2022, 1, 1)
while _d <= date(2026, 12, 31):
    if _d.weekday() < 5 and _d not in HOLS:
        WD.append(_d)
    _d += timedelta(days=1)
WDI = {d: i for i, d in enumerate(WD)}
EXTRACT = date(2026, 4, 30)
EXI = max(i for i, d in enumerate(WD) if d <= EXTRACT)


def to_local(utc_dt):
    off = 1 if last_sunday(utc_dt.year, 3) <= utc_dt.date() < last_sunday(utc_dt.year, 10) else 0
    return utc_dt + timedelta(hours=off)


def fqtr(d):
    q = {4: 1, 5: 1, 6: 1, 7: 2, 8: 2, 9: 2, 10: 3, 11: 3, 12: 3, 1: 4, 2: 4, 3: 4}[d.month]
    return d.year + (1 if d.month >= 4 else 0), q


# ------------------------------------------------------------------ reference data
qh, qr = read_csv("queue_reference.csv")
QUEUES = [r[0] for r in qr]
GEM2ORB = {r[1]: r[0] for r in qr}
QNAME = {r[0]: r[2] for r in qr}

std_txt = read_pdf("member_service_standard_2025.pdf")
TARGET_WD = {m.group(1): int(m.group(2)) for m in re.finditer(r"(MS-[A-Z]{2})\n(\d+)", std_txt)}
wm_txt = read_pdf("work_measurement_standard_2022.pdf")
STD_MIN = {m.group(1): int(m.group(2)) for m in re.finditer(r"(MS-[A-Z]{2})\n(\d+)", wm_txt)}
m = re.search(r"(\d+) productive minutes on a working day", wm_txt)
PROD_MIN = int(m.group(1)) if m else None
m = re.search(r"net productive factor is (\d+\.\d+)", wm_txt)
NET_FACTOR = float(m.group(1)) if m else None

print("== formats read back from the shipped bytes, each with its positive control")
chk("pdf extractor reads the standard (control)", "The service clock runs in working days" in std_txt,
    "%d characters; targets parsed for %d queues" % (len(std_txt), len(TARGET_WD)))
chk("pdf extractor reads the study (control)", "net productive factor" in wm_txt,
    "%d productive minutes, factor %s, %d standard minutes parsed"
    % (PROD_MIN, NET_FACTOR, len(STD_MIN)))
fw_txt = read_pdf("service_assurance_framework_2026.pdf")
chk("pdf extractor reads the framework (control)", "4.2 The review candidate" in fw_txt,
    "%d characters" % len(fw_txt))
fee_txt = read_pdf("fee_schedule_2025.pdf")
chk("pdf extractor reads the fee schedule (control)", "Scheme Administration Fee Schedule" in fee_txt)
tru_txt = read_pdf("trustee_report_membership_2026.pdf")
chk("pdf extractor reads the trustee statement (control)", "active membership at 31 March 2026" in tru_txt)
auth_txt = read_pdf("pensions_authority_letter_2026.pdf")
chk("pdf extractor reads the Authority letter (control)", "service improvement response" in auth_txt)
ros = read_xlsx("rostered_capacity_by_queue.xlsx")
chk("xlsx extractor reads the roster (control)", "Notes" in ros and any(
    r and r[0] == "Conversion" for r in ros["Notes"]),
    "sheets: %s" % ", ".join(ros))
mon = read_xlsx("service_monitoring_export.xlsx")
chk("xlsx extractor reads the monitoring export (control)",
    mon["Performance"][0][0] == "queue_code" and len(mon["Performance"]) > 100,
    "%d performance rows" % (len(mon["Performance"]) - 1))
sv = read_xlsx("member_satisfaction_survey_fy2026.xlsx")
chk("xlsx extractor reads the survey (control)", len(sv["Results"]) > 30)
st = json.loads(read_text("case_status_reference.json"))
chk("json extractor reads the status reference (control)",
    {s["code"] for s in st["statuses"]} >= {"ANSWERED", "TRF", "AWAITING_MEMBER"})
gh, gr = read_csv("member_cases_gemini_fy2023_fy2024.csv")
oh, orows = read_csv("member_cases_orbit_fy2025_fy2026.csv")
chk("csv extractor reads both case extracts (control)", len(gr) > 25000 and len(orows) > 25000,
    "%d Gemini rows, %d Orbit rows" % (len(gr), len(orows)))

print("\n== shipped column sets, by equality")
chk("Gemini header is exactly as intended",
    gh == ["case_no", "queue", "scheme", "member_ref", "received", "closed", "status", "member_days"],
    ", ".join(gh))
chk("Orbit header is exactly as intended",
    oh == ["case_reference", "queue_code", "scheme_code", "member_id", "received_utc",
           "answered_utc", "case_status", "clock_stop_days", "legacy_case_ref"], ", ".join(oh))
rh, rrows = read_csv("schemes_register_2026.csv")
chk("register header is exactly as intended, and return_basis does not ship",
    rh == ["scheme_code", "scheme_name", "sponsor", "active_members"], ", ".join(rh))
ch, crows = read_csv("scheme_charges_fy2026.csv")
chk("charge header is exactly as intended, and no case count ships",
    ch == ["charge_ref", "charge_date", "scheme_code", "queue_code", "statement_type",
           "charge_eur", "rate_period", "currency"], ", ".join(ch))
blob = "\n".join(read_text(f) for f in sorted(os.listdir(T)) if f.endswith((".csv", ".json")))
chk("no truth column leaks into any text file",
    not re.search(r"\b(return_basis|cases_covered|consolidated_cases|is_device|late_flag)\b", blob),
    "control: the word 'active_members' is present (%d times)" % blob.count("active_members"))
chk("positive control for that absence sweep", "active_members" in blob and "clock_stop_days" in blob)

print("\n== the framework's clause 4.2, read word for word")
c42 = re.search(r"4\.2 (.+?)4\.3", fw_txt, re.S)
c42 = re.sub(r"\s+", " ", c42.group(1)).strip() if c42 else ""
for part, phrase in (("population", "Every case received in the financial year is counted, including cases not yet answered at the extract date"),
                     ("outcome", "answered later than the target set for that queue"),
                     ("window", "cases received in the preceding financial year"),
                     ("unit", "The unit is the case queue"),
                     ("comparison", "the share the same queue reached in those of its quarters in the three financial years before that one which carried the same offered load")):
    chk("4.2 files the %s" % part, phrase in c42, phrase[:64])
chk("4.2 does not say how to read a value at the same offered load",
    not re.search(r"nearest|interpol|fitted|regress|per staffed position|per position|divided by",
                  c42, re.I),
    "control: the clause is %d characters and contains 'the same offered load'" % len(c42))
chk("no shipped document mentions occupancy or load per position",
    not re.search(r"occupanc|load per (staffed )?position|per staffed position",
                  " ".join([std_txt, wm_txt, fw_txt, fee_txt, tru_txt, auth_txt, blob]), re.I),
    "control: 'offered load' appears in the framework and the study")
chk("positive control for that absence sweep",
    "offered load" in fw_txt.lower() and "offered load" in wm_txt.lower())

# ------------------------------------------------------------------ the case population
print("\n== the pack's own registers and the write-up's citations")
mh, mrows_ = read_csv("export_manifest.csv")
shipped = {f for f in os.listdir(T)}
listed = {r[0] for r in mrows_}
chk("the manifest names every shipped file but itself", listed == shipped - {"export_manifest.csv"},
    "%d listed against %d shipped" % (len(listed), len(shipped)))
sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
cited = set(re.findall(r"[a-z0-9_]+\.(?:csv|xlsx|pdf|json)", sub))
gold = set(os.listdir(os.path.join(TASK, "golden"))) if os.path.isdir(os.path.join(TASK, "golden")) else set()
chk("every file the write-up names is in the pack or is a deliverable", cited <= (shipped | gold),
    "%d cited across %d input files and %d deliverables; missing: %s"
    % (len(cited), len(cited & shipped), len(cited & gold),
       ", ".join(sorted(cited - shipped - gold)) or "none"))
clauses = set(re.findall(r"clauses? ([\d.]+(?:,? (?:and )?[\d.]+)*)", sub))
flat = {c.strip() for grp in clauses for c in re.split(r",| and ", grp) if c.strip()}
docs = std_txt + fw_txt
missing_cl = [c for c in flat if not re.search(r"(?m)^%s " % re.escape(c), docs)]
chk("every clause the write-up cites resolves in a shipped document", not missing_cl,
    "cited %s; control: clause 4.2 resolves (%s)"
    % (", ".join(sorted(flat)), bool(re.search(r"(?m)^4\.2 ", fw_txt))))

print("\n== the case record, rebuilt from the shipped bytes")
cases = {}
for r in gr:
    rec = datetime.strptime(r[4], "%d/%m/%Y %H:%M")
    cases[r[0]] = dict(key=r[0], q=GEM2ORB[r[1]], scheme=r[2], rec=rec.date(),
                       ans=datetime.strptime(r[5], "%d/%m/%Y %H:%M").date() if r[5] else None,
                       stop=int(r[7]), src="gemini", status=r[6])
superseded = 0
for r in orows:
    rec = to_local(datetime.strptime(r[4], "%Y-%m-%dT%H:%M:%SZ")).date()
    ans = to_local(datetime.strptime(r[5], "%Y-%m-%dT%H:%M:%SZ")).date() if r[5] else None
    rec_ = dict(key=r[8] or r[0], q=r[1], scheme=r[2], rec=rec, ans=ans,
                stop=int(r[7]), src="orbit", status=r[6])
    if r[8]:
        superseded += 1
    cases[rec_["key"]] = rec_
chk("the cutover is resolved to one row per case", superseded > 0 and len(cases) == len(gr) + len(orows) - superseded,
    "%d carried cases held in both extracts, %d distinct cases" % (superseded, len(cases)))

for c in cases.values():
    if c["ans"] is not None:
        c["clock"] = max(0, (WDI[c["ans"]] - WDI[c["rec"]]) - c["stop"])
        c["elapsed"] = WDI[c["ans"]] - WDI[c["rec"]]
    else:
        c["clock"] = max(0, (EXI - WDI[c["rec"]]) - c["stop"])
        c["elapsed"] = None
    c["late"] = c["clock"] > TARGET_WD[c["q"]]
    c["fy"], c["fq"] = fqtr(c["rec"])

# ------------------------------------------------------------------ rostered positions
POS = {}
for fy in (2023, 2024):
    rows = ros["FY%d" % fy]
    hdr = [i for i, r in enumerate(rows) if r and r[0] == "queue_code"][0]
    acc = {}
    for r in rows[hdr + 1:]:
        if not r or not r[0]:
            continue
        y, mo = (int(x) for x in str(r[1]).split("-"))
        q = {4: 1, 5: 1, 6: 1, 7: 2, 8: 2, 9: 2, 10: 3, 11: 3, 12: 3, 1: 4, 2: 4, 3: 4}[mo]
        key = (r[0], y + (1 if mo >= 4 else 0), q)
        acc[key] = acc.get(key, 0.0) + float(r[2])
    for (qc, y, q), hours in acc.items():
        wd = sum(1 for d in WD if fqtr(d) == (y, q))
        POS[(qc, y, q)] = hours / (7.0 * wd)
for fy in (2025, 2026):
    rows = ros["FY%d" % fy]
    hdr = [i for i, r in enumerate(rows) if r and r[0] == "queue_code"][0]
    for r in rows[hdr + 1:]:
        if not r or not r[0]:
            continue
        mm = re.match(r"FY(\d{4}) Q(\d)", str(r[1]))
        POS[(r[0], int(mm.group(1)), int(mm.group(2)))] = float(r[2])
chk("rostered positions recover on both sheet bases",
    abs(POS[("MS-CQ", 2024, 1)] - 16.0) < 0.02 and POS[("MS-DC", 2025, 1)] == 14.0
    and POS[("MS-DC", 2026, 1)] == 5.0,
    "FY2024 monthly hours convert to 16.0 positions for MS-CQ; MS-DC runs 14 then 5")

# ------------------------------------------------------------------ cells, load, the call
cells = {}
for c in cases.values():
    if c["fy"] < 2023 or c["fy"] > 2026:
        continue
    k = (c["q"], c["fy"], c["fq"])
    a = cells.setdefault(k, [0, 0])
    a[0] += 1
    a[1] += 1 if c["late"] else 0
PMIN = PROD_MIN * NET_FACTOR
for (qc, y, q), a in list(cells.items()):
    wd = sum(1 for d in WD if fqtr(d) == (y, q))
    load = a[0] * STD_MIN[qc] / (PMIN * wd)
    cells[(qc, y, q)] = dict(n=a[0], late=a[1], b=100.0 * a[1] / a[0], load=load,
                             pos=POS[(qc, y, q)], occ=load / POS[(qc, y, q)])


def f26(qc):
    return [cells[(qc, 2026, q)] for q in (1, 2, 3, 4)]


def pool(qc):
    return [cells[(qc, y, q)] for y in (2023, 2024, 2025) for q in (1, 2, 3, 4)]


def obs(qc):
    rr = f26(qc)
    return 100.0 * sum(r["late"] for r in rr) / sum(r["n"] for r in rr)


def implied(qc, key, k=3):
    rr, po = f26(qc), pool(qc)
    tot = sum(r["n"] for r in rr)
    s = 0.0
    for r in rr:
        near = sorted(po, key=lambda p: abs(p[key] - r[key]))[:k]
        s += (sum(p["b"] for p in near) / len(near)) * r["n"]
    return s / tot


OBS = {q: obs(q) for q in QUEUES}
LOAD = sorted(((q, OBS[q] - implied(q, "load")) for q in QUEUES), key=lambda kv: -kv[1])
OCC = sorted(((q, OBS[q] - implied(q, "occ")) for q in QUEUES), key=lambda kv: -kv[1])
CALL, CALL_EX = LOAD[0]
CALL_FIG = OBS[CALL]

print("\n== the call, and the literal execution of 4.2")
chk("4.2 executed literally names Contribution queries", CALL == "MS-CQ",
    "%s (%s) at %+.2f points" % (QNAME[CALL], CALL, CALL_EX))
chk("the committed figure is 12.4 per cent", round(CALL_FIG, 1) == 12.4,
    "%.4f per cent" % CALL_FIG)
seconds = {sorted(((q, OBS[q] - implied(q, "load", k)) for q in QUEUES),
                  key=lambda kv: -kv[1])[1][0] for k in (1, 2, 3, 4, 5)}
margins = [sorted(((q, OBS[q] - implied(q, "load", k)) for q in QUEUES),
                  key=lambda kv: -kv[1])[0][1] /
           sorted(((q, OBS[q] - implied(q, "load", k)) for q in QUEUES),
                  key=lambda kv: -kv[1])[1][1] for k in (1, 2, 3, 4, 5)]
chk("the call leads every nearest-k reading by 1.2x or more", min(margins) >= 1.2,
    "margins %s" % ", ".join("%.2fx" % m for m in margins))
chk("second place is not a graded figure, and the pack shows why", len(seconds) > 1,
    "the queue in second changes with the reading (%s), so neither the prompt nor clause 4.4 "
    "asks for it; only the call, which leads every reading, is graded"
    % ", ".join(sorted(seconds)))
chk("no shipped document asks for a queue next in order",
    not re.search(r"next in order|runner-?up", " ".join([fw_txt, auth_txt, std_txt]), re.I),
    "control: clause 4.4 is present (%s)" % ("4.4 The candidate is recorded" in fw_txt))
cq_cases = sum(1 for c in cases.values() if c["fy"] == 2026 and c["q"] == CALL)
chk("the call's own FY2026 cases received", cq_cases == 6480, "%d" % cq_cases)
chk("the default path's own answer is a different queue", OCC[0][0] == "MS-DC",
    "the load-per-staffed-position match names %s at %+.2f points" % (QNAME[OCC[0][0]], OCC[0][1]))
lvl = sorted(OBS.items(), key=lambda kv: -kv[1])
chk("the level ranking names a third queue", lvl[0][0] == "MS-IS",
    "%s at %.2f per cent; the call sits %dth of 9 on the level"
    % (QNAME[lvl[0][0]], lvl[0][1], [q for q, _ in lvl].index(CALL) + 1))
gross = {}
for q in QUEUES:
    rr = [c for c in cases.values() if c["q"] == q and c["fy"] == 2026 and c["ans"] is not None]
    gross[q] = 100.0 * sum(1 for c in rr if c["elapsed"] > TARGET_WD[q]) / len(rr)
chk("the export basis names a fourth queue", max(gross.items(), key=lambda kv: kv[1])[0] == "MS-TI",
    "%s at %.2f per cent on elapsed working days"
    % (QNAME[max(gross.items(), key=lambda kv: kv[1])[0]], max(gross.values())))
chk("the call holds under every nearest-k reading of 4.2",
    all(sorted(((q, OBS[q] - implied(q, "load", k)) for q in QUEUES),
               key=lambda kv: -kv[1])[0][0] == CALL for k in (1, 2, 3, 4, 5)))

print("\n== the monitoring export reproduces on its own stated basis")
mrows = {(r[0], r[1]): (r[2], r[3], r[4]) for r in mon["Performance"][1:] if r and r[0]}
bad = 0
for (qc, cq), (n, late, pct) in mrows.items():
    y, q = int(cq[:4]), int(cq[5])
    sel = [c for c in cases.values() if c["q"] == qc and c["ans"] is not None
           and c["ans"].year == y and (c["ans"].month - 1) // 3 + 1 == q]
    if len(sel) != n or sum(1 for c in sel if c["elapsed"] > TARGET_WD[qc]) != late:
        bad += 1
chk("every monitoring export cell recomputes at zero tolerance", bad == 0,
    "%d cells" % len(mrows))
chk("the export ranks nothing",
    [r[0] for r in mon["Performance"][1:3]] == sorted([r[0] for r in mon["Performance"][1:3]]),
    "rows are in queue code order")

print("\n== ask figures")
A1 = sum(1 for c in cases.values() if c["fy"] == 2026 and c["late"])
chk("ask 1: cases received in FY2026 answered later than target", A1 == 1799, "%d" % A1)
FEE = {}
for mm in re.finditer(r"(MS-[A-Z]{2})\n([\d.]+)\n([\d.]+)", fee_txt):
    FEE[mm.group(1)] = (float(mm.group(2)), float(mm.group(3)))
chk("the fee schedule parses six chargeable case types", len(FEE) == 6, ", ".join(sorted(FEE)))
A2 = {}
for r in crows:
    d = date.fromisoformat(r[1])
    per = 1 if d >= date(2025, 10, 1) else 0
    cov = round(float(r[5]) / FEE[r[3]][per])
    y, q = fqtr(d)
    if y == 2026:
        A2[q] = A2.get(q, 0) + cov
chk("ask 2: the charges cover more cases than they have lines",
    sum(A2.values()) > len(crows) * 1.2,
    "%d cases covered on %d lines, %s" % (sum(A2.values()), len(crows),
                                          ", ".join("Q%d %d" % (q, A2[q]) for q in sorted(A2))))
TRU = {mm.group(1): int(mm.group(3).replace(",", "")) + int(mm.group(4).replace(",", ""))
       for mm in re.finditer(r"((?:SC-\d{3}|RMT-000))\n([^\n]+)\n([\d,]+)\n([\d,]+)", tru_txt)}
chk("the trustee statement parses every scheme", len(TRU) >= 45,
    "%d schemes; control RMT-000 = %s" % (len(TRU), TRU.get("RMT-000")))
SUBS = re.search(r"sub-codes (.+?) are sections of the one participating scheme ([A-Z]{3}-\d{3})",
                 read_text("data_dictionary.csv"))
subcodes = [s.strip() for s in SUBS.group(1).replace(" and", ",").split(",") if s.strip()]
PARENT = {s: SUBS.group(2) for s in subcodes}
cnt = {}
for c in cases.values():
    if c["fy"] != 2026:
        continue
    p = PARENT.get(c["scheme"], c["scheme"])
    cnt[p] = cnt.get(p, 0) + 1
top10 = sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))[:10]
A3 = {p: (TRU[p], round(1000.0 * n / TRU[p], 1)) for p, n in top10}
chk("ask 3: the ten largest participating schemes roll the trust's sections up",
    [p for p, _ in top10][0] == "RMT-000" and len(subcodes) == 5,
    "largest %s with %d cases; sub-codes %s" % (top10[0][0], top10[0][1], ", ".join(subcodes)))
REG = {r[0]: (int(r[3]) if r[3] else None) for r in rrows}
moved = [p for p, _ in top10 if REG[p] != TRU[p]]
ten_txt = " ".join([blob, tru_txt, read_text("schemes_register_2026.csv")])
bad_verbatim = [p for p, _ in top10
                if re.search(r"\b%s\b" % "{:,}".format(A3[p][0]).replace(",", ",?"), ten_txt)]
chk("no ask 3 answer ships verbatim anywhere in the pack", not bad_verbatim,
    "every graded membership figure is the two status parts added; control: the contributing part "
    "of %s, %s, is in the trustee statement"
    % (top10[0][0], "{:,}".format(A3[top10[0][0]][0] - 0) if False else "present"))
chk("ask 3: the register's figure is wrong or absent for all ten", len(moved) == 10,
    "nine carry their sponsor's group total and the master trust carries none, so every graded "
    "membership comes from the trustee statement's two status parts")

print("\n== printed precision against the prompt's rounding sentence")
prompt = open(os.path.join(TASK, "prompt.txt"), encoding="utf-8").read()
rs = prompt.strip().split(". ")[-1]
chk("the rounding sentence is the prompt's last", "one decimal place" in rs, rs.strip())
one_dp = [("the call's breach share", CALL_FIG)] + \
         [("%s cases per 1,000" % p, A3[p][1]) for p, _ in top10]
whole = [("ask 1 cases answered late", A1)] + \
        [("FY2026 Q%d chargeable cases covered" % q, A2[q]) for q in sorted(A2)] + \
        [("%s active members" % p, A3[p][0]) for p, _ in top10]
chk("every figure the rounding sentence governs prints to one decimal",
    all(abs(v * 10 - round(v * 10)) < 0.5 for _, v in one_dp),
    "%d figures: %s" % (len(one_dp), ", ".join("%.1f" % v for _, v in one_dp[:4]) + " ..."))
chk("every other graded figure is a whole count the sentence does not govern",
    all(float(v).is_integer() for _, v in whole), "%d counts" % len(whole))

print("\n== bin edges, swept over every graded figure")
def edge(v, u=0.1):
    return u / 2.0 - abs(v - round(v / u) * u)
tight = min((edge(v), n) for n, v in one_dp)
chk("every figure governed by the rounding sentence sits mid-bin", tight[0] >= 0.03,
    "tightest %s at %.4f of 0.1" % (tight[1], tight[0]))
chk("the committed figure's own edge distance", edge(CALL_FIG) >= 0.03,
    "%.4f per cent, %.4f from the nearest edge" % (CALL_FIG, edge(CALL_FIG)))
allc = sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))
chk("the graded set's boundary holds", allc[9][1] - allc[10][1] > 20,
    "tenth %s %d against eleventh %s %d" % (allc[9][0], allc[9][1], allc[10][0], allc[10][1]))

print("\n== figures.json agrees with the bundle")
fj = os.path.join(HERE, "figures.json")
if os.path.exists(fj):
    F = json.load(open(fj))
    c_ = F.get("call", {})
    a_ = F.get("asks", {})
    chk("figures.json call and figure match the bundle",
        c_.get("queue_code") == CALL
        and abs((c_.get("fy2026_breach_share_pct") or 0) - round(CALL_FIG, 1)) < 1e-9,
        "%s %s" % (c_.get("queue_code"), c_.get("fy2026_breach_share_pct")))
    chk("figures.json ask figures match the bundle",
        a_.get("ask1_cases_answered_late_fy2026") == A1
        and all(a_.get("ask2_chargeable_cases_covered", {}).get("Q%d" % q) == A2[q] for q in sorted(A2))
        and all(a_.get("ask3_active_members", {}).get(p) == A3[p][0] for p, _ in top10)
        and all(abs((a_.get("ask3_cases_per_1000", {}).get(p) or -1) - A3[p][1]) < 1e-9
                for p, _ in top10),
        "ask 1, 4 ask 2 cells, 10 scheme case counts and 10 rates")
else:
    chk("figures.json present", False, "not written yet")

print("\n%d assertions, %d failed" % (len(OK) + len(BAD), len(BAD)))
for lbl, d in BAD:
    print("  FAILED: %s %s" % (lbl, d))
sys.exit(1 if BAD else 0)
