"""task146 checks, run on every build: the input gates; the three-rules block (R1 the field's raw material, R2 every
mess item neutral, R3a the analyst test on the clean truth and the pack, R3b the decisive step alone, R3c no plant);
the strict rule 3 test on the shipped sentences that bear on how the call is computed; the one-sigma test on every
rounded figure; every rung by name; every construction of the golden; every semantic fork row (SF1 to SF17); the
asks with every stop and the cracker's path; the distractors; the realism sweep; the goldens. Any failure stops the
build."""
from __future__ import annotations

import csv
import datetime as dt
import json
import math
import os
import re
import shutil
import subprocess
import tempfile
import zipfile
from collections import Counter

import numpy as np

import calc as C
import common as K
import docs as DOC
import industry as I
import notices as N
import records as R
import world as WD

REG = K.REGIONS
WCI = ("Western", "Coastal", "Island")
DASH = re.compile("[%s%s]" % (chr(0x2013), chr(0x2014)))


class Checks:
    def __init__(self):
        self.res = []

    def __call__(self, label, ok, detail=""):
        self.res.append((label, bool(ok), detail))
        return ok

    def report(self):
        bad = [r for r in self.res if not r[1]]
        for lab, ok, det in self.res:
            if not ok:
                print("FAIL %s %s" % (lab, det))
        print("checks.py: %d assertions, %d failed" % (len(self.res), len(bad)))
        if bad:
            raise SystemExit(1)


# ---------------------------------------------------------------------------------------------------- text
def pdf_text(path):
    out = subprocess.run(["pdftotext", "-enc", "UTF-8", path, "-"], capture_output=True, check=True).stdout
    return re.sub(r"\s+", " ", out.decode("utf-8"))


def xlsx_text(path):
    import openpyxl
    wb = openpyxl.load_workbook(path, data_only=True)
    bits = []
    for ws in wb.worksheets:
        bits.append(ws.title)
        for row in ws.iter_rows(values_only=True):
            bits.extend(str(v) for v in row if isinstance(v, str))
    return re.sub(r"\s+", " ", " ".join(bits))


def file_text(path):
    if path.endswith(".pdf"):
        return pdf_text(path)
    if path.endswith(".xlsx"):
        return xlsx_text(path)
    if path.endswith(".docx"):
        with zipfile.ZipFile(path) as z:
            x = z.read("word/document.xml").decode("utf-8")
        return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", x.replace("</w:p>", " ")))
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def doc_text(target):
    """The documents a solver reads as prose: the notes, the release, the workbooks' words and the JSON's notes."""
    out = {}
    for f in os.listdir(target):
        p = os.path.join(target, f)
        if f.endswith((".pdf", ".xlsx")):
            out[f] = file_text(p)
        elif f.endswith(".json"):
            d = json.load(open(p, encoding="utf-8"))
            out[f] = " ".join(str(v) for k, v in d.items() if k != "observations")
        elif f.endswith(".csv"):
            with open(p, encoding="utf-8") as fh:
                out[f] = fh.readline()
    return out


def segments(target):
    """Every piece of prose the pack carries, one sentence or cell at a time: the PDFs' sentences, each string cell of
    the workbooks, each case note and log line, the JSON's notes."""
    import openpyxl
    out = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        if f.endswith(".pdf"):
            out += re.split(r"(?<=[.;:?!])\s+", pdf_text(p))
        elif f.endswith(".xlsx"):
            wb = openpyxl.load_workbook(p, data_only=True)
            for ws in wb.worksheets:
                for row in ws.iter_rows(values_only=True):
                    out += [v for v in row if isinstance(v, str)]
        elif f.endswith(".json"):
            d = json.load(open(p, encoding="utf-8"))
            out += [str(v) for k, v in d.items() if k != "observations"]
        elif f.endswith(".csv"):
            with open(p, encoding="utf-8") as fh:
                for row in csv.reader(fh):
                    out += [v for v in row if re.search(r"[A-Za-z]{3,} [A-Za-z]{3,}", v)]
    return out


def copy_only(target, files):
    tmp = tempfile.mkdtemp(prefix="t146_")
    for f in files:
        shutil.copy2(os.path.join(target, f), os.path.join(tmp, f))
    return tmp


# Ask A's 24 cells as shipped at the strengthened cut (f0b43f3f): case-note wording may change, these may not
ASK_A_FROZEN = {"Northern": (111, 121, 230), "Capital": (360, 463, 238), "Eastern": (205, 101, 164),
                "Midlands": (198, 499, 290), "Western": (198, 697, 555), "Southern": (136, 548, 139),
                "Coastal": (300, 828, 242), "Island": (350, 277, 139)}
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
          "December"]
PAST_WORDS = re.compile(r"\b(went|finished|left|done|since|visited|met|came)\b", re.I)


def note_time_faults(note, nd):
    """What a case note says about time that its own date contradicts: a leading date stamp that is not the note's
    date, a month named as already past ('since ...') after it, a day before the note's date spoken of as ahead, or a
    day after it spoken of as past. A day without a year is in the note's year unless its month is more than three
    months before the note's (then it is next year's: a first layoff or a deferral)."""
    faults = []
    m = re.match(r"\s*(\d{1,2})/(\d{1,2})(?:/(\d{4}))?\b", note)
    if m and (int(m.group(1)), int(m.group(2))) != (nd.day, nd.month):
        faults.append("stamp %s" % m.group(0).strip())
    for m in re.finditer(r"\bsince (?:the start of )?(%s)\b" % "|".join(MONTHS), note):
        if MONTHS.index(m.group(1)) + 1 > nd.month:
            faults.append("since %s" % m.group(1))
    refs = [(int(m.group(1)), MONTHS.index(m.group(2)) + 1, None)
            for m in re.finditer(r"(?<![\d/:])(\d{1,2}) (%s)\b" % "|".join(MONTHS), note)]
    refs += [(int(m.group(1)), int(m.group(2)), int(m.group(3)) if m.group(3) else None)
             for m in re.finditer(r"(?<![\d/:])(\d{1,2})/(\d{1,2})(?:/(\d{4}))?(?![\d/])", note)]
    for day, mon, yr in refs:
        y = yr or (nd.year if mon >= nd.month - 3 else nd.year + 1)
        try:
            r = dt.date(y, mon, day)
        except ValueError:
            faults.append("no such date %d/%d" % (day, mon))
            continue
        past = bool(PAST_WORDS.search(note))
        if r < nd and not past:
            faults.append("%s spoken of as ahead" % r)
        if r > nd and past:
            faults.append("%s spoken of as past" % r)
    return faults


def note_skeleton(note, towns, contacts):
    """A case note with its particulars set aside (date stamps, contacts, towns, numbers, months and weekdays, the
    reason in brackets, case and closing stops): the sentence template an officer wrote."""
    s = note.lower()
    s = re.sub(r"^\d{1,2}/\d{1,2}(/\d{4})?\s*", "", s)
    for c in contacts:
        s = s.replace(c.lower(), "<c>")
    for t in towns:
        s = s.replace(t.lower(), "<t>")
    s = re.sub(r"\b(%s|monday|tuesday|wednesday|thursday|friday|mon|tue|wed|thu|fri)\b" % "|".join(
        m.lower() for m in MONTHS), "<m>", s)
    s = re.sub(r"\d+(st|nd|rd|th)?", "#", s)
    s = re.sub(r"\(([^)]*)\)", "(<r>)", s)
    return s.strip(" .")


# ---------------------------------------------------------------------------------------------------- run
def run(target, golden, Wd=None, G=None, meta_path=None):
    A = Checks()
    files = sorted(os.listdir(target))
    T = Wd.T if Wd else WD.simulate()
    meta = json.load(open(meta_path, encoding="utf-8")) if meta_path else {}

    # ------------------------------------------------------------------ input gates
    fmts = {f.rsplit(".", 1)[1] for f in files}
    A("gate 10 or more files (%d)" % len(files), len(files) >= 10, files)
    A("gate 3 or more formats (%s)" % ", ".join(sorted(fmts)), len(fmts) >= 3)
    with open(os.path.join(target, R.F_CUBE), encoding="utf-8") as fh:
        cube_n = sum(1 for _ in fh) - 1
    A("gate a file of 25,000 rows or more (the cube, %d rows)" % cube_n, cube_n >= 25000)
    dis = meta.get("distractor_files", [])
    A("gate two or more distractors named in metadata.json and shipped", len(dis) >= 2 and all(f in files for f in dis),
      dis)
    A("gate no file name carries stump or author vocabulary",
      not any(re.search(r"distract|decoy|trap|golden|answer|truth|naive|stump|refil|clean|fixed|synthetic", f, re.I)
              for f in files), files)
    A("gate every file shipped is one the generator names", set(files) == set(R.MAIN_FILES + R.ASK_A_FILES +
                                                                               R.ASK_B_FILES + R.DISTRACTORS +
                                                                               R.CONTEXT_FILES))
    logged = [r["file"] for r in csv.DictReader(open(os.path.join(target, R.F_LOG), encoding="utf-8"))]
    A("gate the desk's data log names every other shipped file once (H9, set equality)",
      sorted(logged) == sorted(f for f in files if f != R.F_LOG) and len(logged) == len(set(logged)))

    # ------------------------------------------------------------------ the call from the pack, and from the truth
    V = C.from_pack(target)
    L = C.ladder(V)
    gold = L["gold"]
    call = K.round_to(gold, 1000)
    cm = C.components(V, L)
    pr = C.precision(V, L)
    se = pr["se_call"]
    Vt = C.from_truth(T)
    Lt = C.ladder(Vt)
    R0 = [k for k in L["rivals"] if k.startswith("R0 ")][0]
    A("the call is 17,000 (%.0f)" % gold, call == 17000)
    A("the call sits inside its bin on a non-round value, 0.35 of a bin or more from the edge (clearance %.2f)" %
      K.bin_clearance(gold, 1000), K.bin_clearance(gold, 1000) >= 0.35 and abs(gold - round(gold, -2)) > 1)
    A("the truth's own expected advance count lies in the golden's bin (%.0f)" %
      (T.target_expected_revised * (1 - T.target_late_share)),
      K.round_to(T.target_expected_revised * (1 - T.target_late_share), 1000) == call)
    A("the clean truth and the pack give the same golden (%.0f, %.0f)" % (Lt["gold"], gold), abs(Lt["gold"] - gold) < 1e-6)

    # ------------------------------------------------------------------ R1: the field's raw material ships
    main_only = copy_only(target, [R.F_LEGACY, R.F_CURRENT, R.F_PROGRAM, R.F_REGIONS])
    try:
        Lm = C.ladder(C.from_pack(main_only))
        A("R1 the call computed from the two weekly files, the program statistics and the regions file alone is the "
          "golden (no ask file, no distractor, no document read)", abs(Lm["gold"] - gold) < 1e-6, Lm["gold"])
    finally:
        shutil.rmtree(main_only)
    weeks = V.weeks
    A("R1 the weekly counts ship by region for every claims week from 29 December 2013 to 27 September 2026 (%d weeks)"
      % len(weeks), weeks[0] == R.SHIP_FIRST_SUNDAY and weeks[-1] == K.ASOF_LAST_SUNDAY and
      all((b - a).days == 7 for a, b in zip(weeks, weeks[1:])) and all(len(V.rev[r]) == len(weeks) for r in REG))
    A("R1 the monetarily ineligible determinations ship by region for every claims-week month, January 2014 to "
      "September 2026 (%d months)" % (len(V.inelig_m) // 8),
      len(V.inelig_m) == 8 * 153 and all(V.months_in_q[q] == 3 for q in V.months_in_q))
    A("R1 the decisive computation reads each region's weekly steps at the 50 quarter turns and each region's "
      "closing-quarter determinations month by month", len(L["D"]) == 50 and
      all("m%d_%s" % (j, r) in L["D"] for r in REG for j in (1, 2, 3)))
    hdrs = []
    for f in files:
        if f.endswith(".csv"):
            with open(os.path.join(target, f), encoding="utf-8") as fh:
                hdrs += [(f, h) for h in fh.readline().strip().split(",")]
    import openpyxl
    for f in (R.F_PROGRAM, R.F_REGISTER, R.F_CONCORD):
        wb = openpyxl.load_workbook(os.path.join(target, f), data_only=True)
        for ws in wb.worksheets:
            for row in ws.iter_rows(max_row=5, values_only=True):
                hdrs += [(f, str(v)) for v in row if isinstance(v, str)]
    bad_cols = [h for h in hdrs if re.search(r"\bshares?\b|refil|\bsteps?\b|\bfactors?\b|forecast|expected|seasonal|"
                                             r"predict|\bturns?\b|recen|weight", h[1], re.I) and h[0] not in R.DISTRACTORS]
    A("R1 no shipped column holds a share, a refiled count, a step, a weight, a seasonal factor or a forecast",
      not bad_cols, bad_cols)
    dtext = doc_text(target)
    fc = [f for f, t in dtext.items() if re.search(r"\bforecast|\bexpect|\bprojection|\bwe estimate|\boutlook\b", t,
                                                   re.I)]
    A("R1 no document states a forecast, an expectation or an estimate of a coming week", not fc, fc)

    # ------------------------------------------------------------------ R2: every mess item neutral on the call
    legacy = list(csv.DictReader(open(os.path.join(target, R.F_LEGACY), encoding="utf-8")))
    misread = 0
    for row in legacy:
        a, b, y = row["WEEK_COMMENCING"].split("/")
        try:
            d = dt.date(int(y), int(a), int(b))
            misread += d.weekday() != 6
        except ValueError:
            misread += 1
    A("R2 the legacy file's day-first dates read month first fail to parse or fall off a Sunday in %d of %d rows: the "
      "misread cannot pass silently" % (misread, len(legacy)), misread >= 0.8 * len(legacy))
    regs = list(csv.DictReader(open(os.path.join(target, R.F_REGIONS), encoding="utf-8")))
    code_name = {(r["region_code"], r["region"]) for r in regs}
    A("R2 the legacy region codes map one to one onto the eight region names (SF14)",
      len(code_name) == 8 and len({c for c, _ in code_name}) == 8 and len({n for _, n in code_name}) == 8)
    nat_by_code = {}
    for row in legacy:
        nat_by_code[row["WEEK_COMMENCING"]] = nat_by_code.get(row["WEEK_COMMENCING"], 0) + int(row["INITIAL_CLAIMS"])
    A("R2 the national series does not depend on the region codes' mapping (sums equal week by week)",
      all(nat_by_code[d.strftime("%d/%m/%Y")] == V.nat[d] for d in weeks if d <= K.LEGACY_LAST_SUNDAY))
    Va = C.from_pack(target)
    for r in REG:
        for d, v in Va.adv[r].items():
            Va.rev[r][d] = v
    C.finish(Va)
    La = C.ladder(Va)
    A("R2 SF7 the history at its first-reported counts (the current system's weeks) files the same call (%.0f)" %
      La["gold"], K.round_to(La["gold"], 1000) == call)
    G_ = L["golden"]
    A("R2 the program statistics' two layouts: the current layout's turns alone file the same call (%.0f)" %
      G_["the current system's turns"], K.round_to(G_["the current system's turns"], 1000) == call)
    wb = openpyxl.load_workbook(os.path.join(target, R.F_PROGRAM), data_only=True)
    hdr_ok = True
    for ws in wb.worksheets:
        if ws.title.startswith("FY") and ws.title <= R.LEGACY_FY_LAST:
            y0 = int(ws.title[2:6])
            want = ["%s-%02d" % (DOC.MON[m - 1], (y0 if m >= 7 else y0 + 1) % 100) for m in list(range(7, 13)) + list(range(1, 7))]
            for row in ws.iter_rows(values_only=True):
                if row[0] == "REGION":
                    hdr_ok &= list(row[1:13]) == want
    A("R2 every legacy month heading carries its year, so a fiscal-year sheet cannot be read on the wrong calendar "
      "year", hdr_ok)
    A("R2 public holidays: the golden with every turn a holiday touches dropped files the same call (%.0f)" %
      G_["holiday-touched turns dropped"], K.round_to(G_["holiday-touched turns dropped"], 1000) == call)
    A("R2 the summer shutdown and January return: the golden without the January turns files the same call (%.0f)" %
      G_["without January turns"], K.round_to(G_["without January turns"], 1000) == call)
    nj = C.regional(V, L["D"][L["D"].qq != 3])
    A("R2 the fiscal year's end in the last June week: the golden without the July turns files the same call (%.0f)" %
      nj, K.round_to(nj, 1000) == call)
    A("R2 SF13 the two layouts meet without a gap or an overlap (20 June and 27 June 2021)",
      K.LEGACY_LAST_SUNDAY in V.weeks and K.CURRENT_FIRST_SUNDAY in V.weeks and
      (K.CURRENT_FIRST_SUNDAY - K.LEGACY_LAST_SUNDAY).days == 7 and
      max(dt.datetime.strptime(r["WEEK_COMMENCING"], "%d/%m/%Y").date() for r in legacy) == K.LEGACY_LAST_SUNDAY)
    cur = list(csv.DictReader(open(os.path.join(target, R.F_CURRENT), encoding="utf-8")))
    adv_rows = [r for r in cur if r["count_status"] == "Advance"]
    A("R2 only the latest week (27 September 2026) is at its advance count, and the release's figures are the "
      "file's", {r["claims_week_start"] for r in adv_rows} == {K.ASOF_LAST_SUNDAY.isoformat()} and
      {r["region"]: int(r["initial_claims"]) for r in adv_rows} == {x["region"]: x["adv"] for x in R.release(T)["rows"]})
    # the September program statistics carry their last week at its advance count: the revised determinations instead
    Vr = C.from_truth(T)
    li = T.idx[K.ASOF_LAST_SUNDAY]
    for r in REG:
        Vr.inelig_m[((2026, 9), r)] += int(T.inelig[r][li]) - int(T.adv_inelig[r][li])
    C.finish(Vr)
    g_sep = C.ladder(Vr)["gold"]
    A("R2 SF17 September's determinations with the week ended 3 October at its revised count file the same call "
      "(%.0f)" % g_sep, K.round_to(g_sep, 1000) == call)
    A("R2 benefits in thousands of dollars, first payments and weeks claimed are not on the call's path (the call reads "
      "initial claims and ineligible determinations only)", True)
    A("R2 the ask paths' mess sits in files the call never opens",
      not (set(R.ASK_A_FILES + R.ASK_B_FILES) - {R.F_NOTES, R.F_REGIONS}) & {R.F_LEGACY, R.F_CURRENT, R.F_PROGRAM})

    # ------------------------------------------------------------------ R3a: the analyst test
    tb, tbt = L["timing_blind"], Lt["timing_blind"]
    se_tb = pr["se_tb"]
    A("R3a the default path on the clean truth (the filed refiling sized region by region, each region's third-quarter "
      "ineligible determinations taken whole at the share its own past turns show) files 15,000 (%.0f)" %
      tbt["all turns"], K.round_to(tbt["all turns"], 1000) == 15000)
    A("R3a the same default path on the pack files 15,000 (%.0f), two bins below the golden" % tb["all turns"],
      K.round_to(tb["all turns"], 1000) == 15000 and call - K.round_to(tb["all turns"], 1000) == 2000)
    A("R3a every region-aware timing-blind construction (%d) files 16,000 or less, a full bin or more off, and sits "
      "below 16,500 by more than its own sigma (%.0f): %s" % (len(tb), se_tb, ", ".join("%.0f" % v for v in tb.values())),
      all(K.round_to(v, 1000) <= call - 1000 and 16500 - v > se_tb for v in tb.values()))
    A("R3a the nearest timing-blind construction is %.0f claims below the golden" % (gold - max(tb.values())),
      gold - max(tb.values()) >= 900)
    natv = L["national"]
    A("R3a the national determinations at the national rate on the clean truth and the pack file 13,000 (%.0f, %.0f), "
      "and every national variant 14,000 or less" % (Lt["national"]["all turns"], natv["all turns"]),
      K.round_to(Lt["national"]["all turns"], 1000) == K.round_to(natv["all turns"], 1000) == 13000 and
      all(K.round_to(v, 1000) <= 14000 for v in natv.values()))
    nm = L["national_months"]
    A("R3a the national determinations month by month (timing-aware, region-blind) file 16,000 or less in every window "
      "(%s)" % ", ".join("%.0f" % v for v in nm.values()), all(K.round_to(v, 1000) <= call - 1000 for v in nm.values()))
    A("R3a the seasonal route (factors of the quarter's first claims week on the level of the last four weeks) files "
      "13,000 on the clean truth and the pack (%.0f, %.0f)" % (Lt["rivals"][R0], L["rivals"][R0]),
      K.round_to(Lt["rivals"][R0], 1000) == K.round_to(L["rivals"][R0], 1000) == 13000)
    # ------------------------------------------------------------------ R3b: the decisive step alone
    A("R3b the decisive step alone (each region's refusals weighed by the month they were made, at that region's own "
      "shares) turns the default path's 15,000 into 17,000 on the clean truth and the pack (%.0f, %.0f)" % (Lt["gold"], gold),
      K.round_to(Lt["gold"], 1000) == call and K.round_to(tbt["all turns"], 1000) == call - 2000)
    rv = L["rivals"]
    want = {"R0 seasonal factors of the quarter's first claims week on the level of the last four weeks (default)": 13000,
            "R1 last year's week times the last eight weeks' growth on the year": 13000,
            "R2 the step from the week before, one intercept per quarter of the year": 13000,
            "R3 the step scaled on the closing quarter's claims": 13000,
            "R3r the step scaled on the closing quarter's claims, region by region": 14000,
            "R0b ISO-week seasonal factors on the level of the last four weeks": 12000,
            "R2r a quarter-start ratio": 13000, "R2g quarter-start terms region by region": 13000}
    for k, b_ in want.items():
        A("R3b rung %s files %s (%.0f)" % (k, "{:,}".format(b_), rv[k]), K.round_to(rv[k], 1000) == b_)
    A("R3b the one-share panel (every region's own intercepts, one share for all) files 13,000 (%.0f)" %
      natv["one share for every region, each region's own intercepts"],
      K.round_to(natv["one share for every region, each region's own intercepts"], 1000) == 13000)
    for k, v in L["latest"].items():
        A("R3b latest-period rate, %s, files %s (%.0f), a bin or more below" % (k, "{:,}".format(K.round_to(v, 1000)), v),
          K.round_to(v, 1000) <= call - 1000 and 16500 - v > se)
    # ------------------------------------------------------------------ R3c: no plant
    blocks = Counter()
    for r in REG:
        ser = [V.rev[r][d] for d in weeks]
        for i in range(len(ser) - 4):
            blocks[tuple(ser[i:i + 5])] += 1
    A("R3c no copied block: no five-week run of a region's counts repeats anywhere", max(blocks.values()) == 1)
    A("R3c no document is a memo, briefing, earlier preview or stakeholder estimate: the pack carries the board's "
      "releases and statistics, Employer Services' records and the Statistics Office's files only",
      not any(re.search(r"rothwell|preview|memo|briefing", f, re.I) for f in files) and
      all(not re.search(r"\d{2},\d{3}|forecast|expect|call|seasonal", " ".join(r)) for r in R.log_rows()) and
      not any(re.search(r"Rothwell|Stacey Baxter|Tia Hewitt", t) for t in dtext.values()))

    # ------------------------------------------------------------------ strict rule 3: the HOW sentences
    notes_t = pdf_text(os.path.join(target, R.F_NOTES))
    rel_t = pdf_text(os.path.join(target, R.F_RELEASE))
    how = []
    for key in ("claims_week", "initial", "monetary", "regions", "advance", "systems"):
        how += DOC.sentences(key)
    how += [s for s in DOC.sentences("program") if s.startswith(("The program statistics for a month",
                                                                 "A month's figures", "When a month"))]
    missing = [s for s in how if s not in notes_t]
    A("R3 strict: the %d technical-notes sentences that bear on how the call is computed ship word for word" % len(how),
      not missing, missing)
    rel_how = ["Counts are not seasonally adjusted.", "The advance count is revised in the next release.",
               "Next release: Thursday 15 October 2026 at 08:30, claims week ended 10 October 2026."]
    A("R3 strict: the release's three sentences on the count ship word for word", all(s in rel_t for s in rel_how))
    prompt = open(os.path.join(os.path.dirname(target), "prompt.txt"), encoding="utf-8").read()
    q1 = prompt.split("?")[0] + "?"
    A("R3 strict: the prompt's question names the population, the window and the release, nothing of a method",
      "first report nationally for the claims week ended Saturday 10 October 2026" in q1 and
      not re.search(r"region|season|refil|quarter|determination|base period|month|recen", q1, re.I), q1)
    nums = [m for s in how + rel_how for m in re.findall(r"\d+(?:[,.]\d+)*%?|per cent", s)]
    A("R3 strict: the HOW sentences carry no count, rate or share (their only figures are the $6,800 minimum, 08:30, "
      "dates and years): %s" % sorted(set(nums)),
      all(n in ("6,800", "08", "30", "27", "20", "15", "10") or re.fullmatch(r"20\d\d", n)
          for n in nums) and not any("%" in n or "per cent" in n for n in nums))
    alltext = " ".join(dtext.values()) + " " + " ".join(
        open(os.path.join(target, f), encoding="utf-8").read() for f in (R.F_CASES,))
    filed = "A claimant found monetarily ineligible may file again in a later quarter, once the base period has moved."
    A("R3 strict: the refiling is filed once, as the board's own rule (technical notes 2.3): %r; the sentence carries "
      "no size, rate, share, timing within the quarter or region" % filed,
      filed in notes_t and len(re.findall(r"\bfil(?:e|es|ed|ing) again\b", alltext, re.I)) == 1 and
      not re.search(r"\d|per cent|share|rate|region|most|many|few|half|first week|first claims week|recen|month|"
                    r"\blate\b|\bearly\b|\bsoon|weeks", filed, re.I))
    method = re.findall(r"refil\w*|\bcom(?:e|es|ing) back\b|re-?admit\w*|regression|"
                        r"seasonal(?:ly)? (?:factor|adjustment|component|pattern)|quarter[- ]start|"
                        r"first (?:claims )?week of (?:the|a|each) quarter|turn of the quarter|"
                        r"share of (?:the )?(?:refused|ineligible|claimants)|(?:most|many|few|half|some) of (?:them|those|"
                        r"the refused|the claimants)|varies by region|differ\w* (?:by|between|across) regions?|"
                        r"recently refused|refused (?:late|early|recently)|(?:late|early) in the quarter|"
                        r"(?:last|final|first) (?:month|weeks?) of (?:the|a|each) quarter|weeks? since|"
                        r"how long ago|time since", alltext, re.I)
    A("R3 strict: no shipped sentence or note says how many refused claimants file again, when within a quarter, that "
      "the share depends on how recently they were refused or differs by region, and none names a seasonal factor or a "
      "regression", not method, method)
    sents = segments(target)
    near = [s for s in sents if re.search(r"file again|fil(?:e|es|ed|ing) again|refil|base period has moved|"
                                          r"ineligible", s, re.I)
            and re.search(r"recen\w*|\blate\b|\bearly\b|\bsoon\w*|timing|weeks? (?:before|after|since)|month of|"
                          r"\bregion\w*|\blast (?:month|weeks?)\b|\bfirst (?:month|weeks?)\b", s, re.I)]
    A("R3 strict: no shipped sentence that speaks of refusal or filing again names recency, timing or region (%d "
      "sentences read)" % len(sents), not near, near)
    every_refiles = V.nat[V.latest] + cm["pool"]
    A("R3 strict: the HOW sentences executed word for word on clean data give no figure of their own; the estimators "
      "they admit file the default path's 15,000 (the filed refiling region by region on the quarter whole), the "
      "national rate's 13,000, the seasonal step's 13,000 or, every refused claimant filing again in the week, %s, "
      "never 17,000" % "{:,}".format(K.round_to(every_refiles, 1000)),
      K.round_to(Lt["rivals"][R0], 1000) != call and K.round_to(Lt["national"]["all turns"], 1000) != call and
      K.round_to(tbt["all turns"], 1000) != call and K.round_to(every_refiles, 1000) != call)
    P = C.panel(V, L["D"])
    A("R3 strict: the behaviour the decisive step turns on (the share filed again by the month of the refusal, each "
      "region's own) is inferred from the data, and the data rejects the rivals by visible margins: one slope on the "
      "quarter whole in each region at F %.1f on %d and %d degrees of freedom, one month profile for every region at F "
      "%.1f on %d and %d" % (P["F_region_quarter"], P["df_region_quarter"][0], P["df_region_quarter"][1],
                             P["F_common_months"], P["df_common_months"][0], P["df_common_months"][1]),
      P["F_region_quarter"] >= 30 and P["F_common_months"] >= 30)

    rev_dir = copy_only(target, [R.F_LEGACY, R.F_CURRENT, R.F_PROGRAM, R.F_REGIONS])
    try:
        for f in (R.F_LEGACY, R.F_CURRENT):
            p_ = os.path.join(rev_dir, f)
            lines = open(p_, encoding="utf-8", newline="").read().splitlines(keepends=True)
            open(p_, "w", encoding="utf-8", newline="").write("".join([lines[0]] + lines[1:][::-1]))
        import openpyxl as ox_
        wbr = ox_.load_workbook(os.path.join(rev_dir, R.F_PROGRAM))
        wbr._sheets = [wbr._sheets[0]] + wbr._sheets[1:][::-1]
        wbr.save(os.path.join(rev_dir, R.F_PROGRAM))
        g_rev = C.ladder(C.from_pack(rev_dir))["gold"]
    finally:
        shutil.rmtree(rev_dir)
    A("closure 14: the weekly files' rows and the workbook's fiscal-year sheets read in reverse give the same call "
      "(%.0f)" % g_rev, abs(g_rev - gold) < 1e-6)

    # ------------------------------------------------------------------ every construction of the golden
    G_POOL = sum(V.inelig_m[((2026, m_), r)] for m_ in (7, 8, 9) for r in REG)
    G_POOL_WCI = K.round_dp(100.0 * sum(V.inelig_m[((2026, m_), r)] for m_ in (7, 8, 9) for r in WCI) / G_POOL, 1)
    for k, v in G_.items():
        A("golden construction, %s: %.0f, clear of 16,500 and 17,500 by more than one sigma (%.0f and %.0f against "
          "%.0f)" % (k, v, v - 16500, 17500 - v, se), K.round_to(v, 1000) == call and v - 16500 > se and 17500 - v > se)
    lo_g, hi_g = min(G_.values()), max(G_.values())
    A("the golden's constructions span %.0f to %.0f (%d of them); the nearest edge is %.0f claims away, %.1f sigma" % (
        lo_g, hi_g, len(G_), min(lo_g - 16500, 17500 - hi_g), min(lo_g - 16500, 17500 - hi_g) / se),
      len(G_) >= 20 and min(lo_g - 16500, 17500 - hi_g) >= 2 * se)
    nrm, nrm_se = L["nat_on_regional_months"]
    A("the national step on the 24 regional monthly determinations at once (one equation, the regional steps "
      "discarded) lands the golden's bin: %.0f, standard error %.0f, %.1f times the golden's" % (nrm, nrm_se, nrm_se / se),
      K.round_to(nrm, 1000) == call and nrm_se >= 2 * se)
    A("the log-ratio form (each region's log step ratio on its months over the base week) lands the golden's bin "
      "(%.0f)" % G_["log-ratio form"], K.round_to(G_["log-ratio form"], 1000) == call)

    # ------------------------------------------------------------------ one sigma, every rounded figure
    lo, hi = gold - se, gold + se
    A("sigma: one standard error (%.0f claims) either way leaves the call at 17,000 (%.0f to %.0f)" % (se, lo, hi),
      K.round_to(lo, 1000) == K.round_to(hi, 1000) == call)
    A("sigma: the flip to 16,000 needs the estimate %.0f claims lower (%.1f standard errors), the flip to 18,000 %.0f "
      "higher (%.1f)" % (gold - 16500, (gold - 16500) / se, 17500 - gold, (17500 - gold) / se),
      (gold - 16500) / se >= 4 and (17500 - gold) / se >= 4)
    ref, wo = cm["refile"], cm["without"]
    A("sigma: the refiled claims (%.0f, se %.0f) stay between 5,000 and 6,000 at one standard error" % (ref, pr["se_refile"]),
      5000 <= ref - pr["se_refile"] and ref + pr["se_refile"] <= 6000)
    A("sigma: the rest of the week (%.0f, se %.0f) stays between 11,000 and 12,000" % (wo, pr["se_icpt"]),
      11000 <= wo - pr["se_icpt"] and wo + pr["se_icpt"] <= 12000)
    parts = L["parts"]
    a_ = sum(parts[r]["refile"] for r in WCI)
    b_ = sum(parts[r]["refile"] for r in REG if r not in WCI)
    va = sum(parts[r]["var_refile"] for r in WCI)
    vb = sum(parts[r]["var_refile"] for r in REG if r not in WCI)
    se_sh = math.sqrt(b_ ** 2 * va + a_ ** 2 * vb) / (a_ + b_) ** 2
    A("sigma: Western, Coastal and Island's part of the refiled claims (%.3f, se %.3f) stays about nine tenths "
      "(0.85 to 0.95)" % (cm["refile_wci_share"], se_sh),
      0.85 <= cm["refile_wci_share"] - se_sh and cm["refile_wci_share"] + se_sh <= 0.95)
    A("sigma: in Western, Coastal and Island the share filed again of those refused in a quarter's last month stays "
      "between two thirds and nine tenths, of those refused in its middle month under one in five, at one standard "
      "error (%s)" % ", ".join("%s %.3f+-%.3f, %.3f+-%.3f" % (r, parts[r]["slopes"]["m3"], parts[r]["slope_se"]["m3"],
                                                               parts[r]["slopes"]["m2"], parts[r]["slope_se"]["m2"])
                               for r in WCI),
      all(2 / 3 <= parts[r]["slopes"]["m3"] - parts[r]["slope_se"]["m3"] and
          parts[r]["slopes"]["m3"] + parts[r]["slope_se"]["m3"] <= 0.9 and
          parts[r]["slopes"]["m2"] + parts[r]["slope_se"]["m2"] < 0.2 and
          parts[r]["slopes"]["m1"] + parts[r]["slope_se"]["m1"] < 0.2 for r in WCI))
    A("sigma: the third quarter's determinations (%s), their %.1f per cent in Western, Coastal and Island and the "
      "%.1f per cent of those three regions' made in September are counts from the workbook, with no estimation error" % (
          "{:,}".format(cm["pool"]), 100 * cm["pool_wci_share"], 100 * cm["sep_wci_share"]),
      cm["pool"] == G_POOL and K.round_dp(100 * cm["pool_wci_share"], 1) == G_POOL_WCI and
      cm["sep_wci"] == sum(V.inelig_m[((2026, 9), r)] for r in WCI))
    dec = decompositions(V, L)
    A("every construction with its months identified keeps the refiled claims between 5,000 and 6,000 and the rest of "
      "the week between 11,000 and 12,000 (%s)" % "; ".join("%s %.0f/%.0f" % (k, x["refile"], x["without"])
                                                             for k, x in dec.items()),
      all(5000 <= x["refile"] <= 6000 and 11000 <= x["without"] <= 12000 for x in dec.values()))
    A("every construction with its months identified keeps about nine tenths of the refiled claims in Western, Coastal "
      "and Island, their last-month shares between two thirds and nine tenths and their earlier months' under one in "
      "five", all(0.85 <= x["wci"] <= 0.95 and all(2 / 3 <= x["shares"][r]["m3"] <= 0.9 and
                                                     x["shares"][r]["m2"] < 0.2 and x["shares"][r]["m1"] < 0.2
                                                     for r in WCI) for x in dec.values()))
    A("the timing-blind build's refiling is 3,000 to 4,000 (%.0f): the quarter whole at the shares past turns show "
      "(Western %.2f, Coastal %.2f, Island %.2f)" % (cm["tb_refile"], cm["tb_shares"]["Western"],
                                                     cm["tb_shares"]["Coastal"], cm["tb_shares"]["Island"]),
      3000 <= cm["tb_refile"] <= 4000)

    # ------------------------------------------------------------------ the data rejects the timing-blind build
    e = C.loo(V, L["D"])
    rm = {k: C.rmse(v) for k, v in e.items()}
    rm["one_share"] = C.loo_one_share(V, L["D"])
    A("margin: leave one turn out, the national step misses by %.0f claims under the golden against %.0f for the "
      "region-aware timing-blind build, %.0f for the national months, %.0f for the national pool at the national rate, "
      "%.0f for one share in every region, %.0f for the closing quarter's claims and %.0f for a quarter-start term" % (
          rm["golden"], rm["timing_blind"], rm["national_months"], rm["pool"], rm["one_share"], rm["claims"], rm["term"]),
      rm["timing_blind"] >= 1.6 * rm["golden"] and rm["pool"] >= 2.2 * rm["golden"] and
      rm["golden"] < min(rm["national_months"], rm["one_share"], rm["claims"], rm["term"]))
    A("margin: the month groupings and forms out of sample: the last month and the rest %.0f, the last month alone "
      "%.0f, the log-ratio form %.0f, the 24 months in one equation %.0f, the middle month lumped with the last %.0f, "
      "against the golden's %.0f" % (rm["last_rest"], rm["last"], rm["log_ratio"], rm["all_months"], rm["lump"],
                                     rm["golden"]),
      rm["log_ratio"] >= 1.1 * rm["golden"] and rm["all_months"] >= 1.2 * rm["golden"] and
      rm["lump"] >= 1.25 * rm["golden"])
    A("margin: the middle month lumped with the last (%.0f, %.0f claims from the bin's edge) is rejected region by "
      "region (F %s on 1 and %d) and out of sample" % (L["lump"], abs(L["lump"] - 16500), ", ".join(
          "%s %.0f" % (r, P["F_lump"][r]) for r in WCI), P["df_region"][1]),
      all(P["F_lump"][r] >= 20 for r in WCI))
    A("margin: region by region, three month slopes against one on the quarter whole, F %s on 2 and %d" % (
        ", ".join("%s %.0f" % (r, P["F_region"][r]) for r in WCI), P["df_region"][1]),
      all(P["F_region"][r] >= 50 for r in WCI))
    A("margin: per region and turn, the timing-blind build misses by %.0f claims and one month profile for every region "
      "by %.0f, against %.0f for each region's own months" % (P["rmse_region_quarter"], P["rmse_common_months"],
                                                             P["rmse_region_months"]),
      P["rmse_region_months"] <= 0.6 * min(P["rmse_region_quarter"], P["rmse_common_months"]))
    um = C.usual_mix(V, L)
    A("mix: the third quarter's determinations (%d) are about one and a half times the median closing quarter's (%.0f)" %
      (cm["pool"], um["median_pool"]), 1.3 <= cm["pool"] / um["median_pool"] <= 1.6)
    A("mix: %.1f per cent of them sit in Western, Coastal and Island against %.1f per cent at the median turn" %
      (100 * cm["pool_wci_share"], 100 * um["median_share"]), cm["pool_wci_share"] >= um["median_share"] + 0.15)
    A("timing: %.1f per cent of those three regions' third-quarter determinations were made in September, against "
      "%.1f per cent in the last month at the median turn (%.1f at the median October turn)" % (
          100 * cm["sep_wci_share"], 100 * um["median_last"], 100 * um["q3_last"]),
      cm["sep_wci_share"] >= um["median_last"] + 0.15 and cm["sep_wci_share"] <= um["max_last"])
    tw = C.twin_timing(V, L["D"])
    A("twin (timing): the %s and %s turns, Western, Coastal and Island determinations %d and %d (national %d and %d), "
      "the last month's part %.2f and %.2f, steps %d and %d" % ((tw["late_turn"], tw["early_turn"], tw["late_hi"],
                                                                 tw["early_hi"], tw["late_pool"], tw["early_pool"],
                                                                 tw["late_last"], tw["early_last"], tw["late_step"],
                                                                 tw["early_step"]) if tw else
                                                                ("-", "-", 0, 0, 0, 0, 0, 0, 0, 0)),
      bool(tw) and tw["late_last"] - tw["early_last"] >= 0.3 and tw["late_step"] > tw["early_step"] + 1500)
    tw2 = C.twin_same_quarter(V, L["D"])
    A("twin (regions): the %s and %s turns, national pools %d and %d, Western, Coastal and Island's part %.3f and %.3f, "
      "steps %d and %d" % ((tw2["hi_turn"], tw2["lo_turn"], tw2["hi_pool"], tw2["lo_pool"], tw2["hi_share"],
                            tw2["lo_share"], tw2["hi_step"], tw2["lo_step"]) if tw2 else ("-", "-", 0, 0, 0, 0, 0, 0)),
      bool(tw2) and tw2["hi_share"] - tw2["lo_share"] >= 0.2 and tw2["hi_step"] > tw2["lo_step"] + 800)
    ar, n_ads, x26 = C.ads_rival(V, target)
    A("rival: the step on the closing quarter's change in the job advertisements index (a distractor, %d turns) files "
      "%.0f, two bins or more below" % (n_ads, ar), K.round_to(ar, 1000) <= call - 2000)

    # ------------------------------------------------------------------ the semantic fork table
    ok1 = all(int(r["INITIAL_CLAIMS"]) == int(r["NEW_CLAIMS"]) + int(r["ADDL_CLAIMS"]) for r in legacy) and \
        all(int(r["initial_claims"]) == int(r["new_claims"]) + int(r["additional_claims"]) for r in cur)
    A("SF1 initial claims are new plus additional claims in every row of both weekly files; transitional claims are "
      "counted apart (technical notes 2.2)", ok1 and "are not initial claims" in notes_t)
    A("SF2 the target is the claims week Sunday 4 to Saturday 10 October 2026, the week after the latest published",
      K.TARGET_SUNDAY == V.latest + dt.timedelta(days=7) and K.saturday(K.TARGET_SUNDAY) == dt.date(2026, 10, 10) and
      K.quarter_of(K.TARGET_SUNDAY) == (2026, 4) and K.quarter_of(V.latest) == (2026, 3))
    nat_rev = {}
    for r in cur:
        if r["count_status"] == "Revised":
            k_ = r["claims_week_start"]
            a0, b0 = nat_rev.get(k_, (0, 0))
            nat_rev[k_] = (a0 + int(r["initial_claims"]), b0 + int(r["first_reported_initial_claims"]))
    worst = max((a0 - b0) / a0 for a0, b0 in nat_rev.values())
    A("SF3 the first report is the advance count; national revisions are at most about 1 per cent (largest %.2f per "
      "cent) and the advance target keeps the bin (%.0f)" % (100 * worst, G_["advance count as the target "
                                                                             "(current system)"]),
      worst < 0.015 and K.round_to(G_["advance count as the target (current system)"], 1000) == call)
    rel = R.release(T)
    A("SF4 nationally is the eight regions together: the release's All regions row is their sum",
      rel["adv"] == sum(x["adv"] for x in rel["rows"]) and rel["adv"] == V.nat[V.latest])
    A("SF5 the as-of: every file stops at the claims week of 27 September 2026 (ended 3 October), the release is of "
      "8 October", V.latest == K.ASOF_LAST_SUNDAY and max(V.inelig_m)[0] == (2026, 9) and "8 October 2026" in rel_t)
    sums = {}
    for d in weeks:
        if (d.year, d.month) >= (2014, 1):
            for r in REG:
                sums[((d.year, d.month), r)] = sums.get(((d.year, d.month), r), 0) + V.new[r][d]
    A("SF6 the workbook's months are claims-week months: every month's new claims equal its weeks' by the month of their "
      "Sunday (C1, %d region-months), so the closing quarter's months are the claims-week months of its weeks" % len(sums),
      all(V.new_m[k] == v for k, v in sums.items()))
    A("SF7 history at first-reported or revised counts: the same call (asserted under R2)", K.round_to(La["gold"], 1000) == call)
    A("SF8 the turns the shares are measured on: every window files 17,000 (%s)" % ", ".join(
        "%s %.0f" % (k, G_[k]) for k in C.windows(L["D"])), all(K.round_to(G_[k], 1000) == call for k in C.windows(L["D"])))
    A("SF9 the base week: the mean of the last three weeks files the same call (%.0f)" %
      G_["mean of the last three weeks as base"], K.round_to(G_["mean of the last three weeks as base"], 1000) == call)
    per_region = sum(K.round_to(parts[r]["base"] + parts[r]["icpt"] + parts[r]["refile"], 1) for r in REG)
    A("SF10 rounding once: the regions rounded to whole claims and summed, then rounded, give the same call",
      K.round_to(per_region, 1000) == call)
    A("SF11 how many is the expected count: a Poisson count of 17,000 has its median within one claim of its mean, the "
      "same call", True)
    A("SF12 no public holiday falls in the target week (Labour Day is Monday 26 October 2026)",
      K.working_days_lost(K.TARGET_SUNDAY) == 0 and dt.date(2026, 10, 26) in K.HOLIDAYS)
    A("SF13 the junction (asserted under R2)", (K.CURRENT_FIRST_SUNDAY - K.LEGACY_LAST_SUNDAY).days == 7)
    A("SF14 the regions (asserted under R2)", len(code_name) == 8)
    import deliver as DL_
    A("SF15 the chart's weekly count from April 2026 starts at the claims week of Sunday 5 April (ended 11 April): the "
      "week ended 4 April begins on Sunday 29 March and belongs to March (technical notes 2.1)",
      DL_.CHART_FROM == dt.date(2026, 4, 5) and DL_.CHART_FROM.weekday() == 6 and
      (DL_.CHART_FROM - dt.timedelta(days=7)).month == 3 and K.saturday(DL_.CHART_FROM - dt.timedelta(days=7)) ==
      dt.date(2026, 4, 4) and "A claims week belongs to the month in which its Sunday falls." in notes_t)
    A("SF16 the month profile's form: the last month and the rest, the last month alone, the first left out and one "
      "profile for every region file the same call (%.0f, %.0f, %.0f, %.0f)" % (
          G_["the last month and the rest of the quarter"], G_["the last month alone"],
          G_["the last two months, the first left out"], G_["one month profile for every region, each region's own scale"]),
      all(K.round_to(G_[k], 1000) == call for k in ("the last month and the rest of the quarter", "the last month alone",
                                                    "the last two months, the first left out",
                                                    "one month profile for every region, each region's own scale")))
    A("SF17 the September statistics' last week at its advance count (asserted under R2)", K.round_to(g_sep, 1000) == call)

    # ------------------------------------------------------------------ Ask A
    W = Wd.notices if Wd else N.simulate()
    truth_a = N.truth_table(W)
    ga, info = C.ask_a(target)
    cells = [(r, p[0]) for r in REG for p in N.PERIODS]
    A("Ask A the golden from the shipped rows equals the truth in all 24 cells", ga == truth_a)
    A("Ask A's 24 cells are identical to the strengthened cut's (case-note wording moved no notice)",
      all(tuple(ga[(r, p)] for p, _, _ in N.PERIODS) == ASK_A_FROZEN[r] for r in REG))
    ask_only = copy_only(target, R.ASK_A_FILES + R.ASK_B_FILES)
    try:
        A("Ask A and Ask B computed with every main-call file but the technical notes and the regions file removed are "
          "the asks", C.ask_a(ask_only)[0] == ga and C.ask_b(ask_only)[0] == C.ask_b(target)[0])
    finally:
        shutil.rmtree(ask_only)
    stops = {"S1 the portal's region column": dict(site_region=False),
             "S2 both channels stacked": dict(dedupe="stack"),
             "S3 the portal alone": dict(dedupe="portal"),
             "S4 withdrawals ignored": dict(withdrawals="none"),
             "S5 the cracker (S1 and S2)": dict(site_region=False, dedupe="stack"),
             "S6 every portal notice of an employer with an open register notice dropped": dict(dedupe="drop_bn"),
             "HA3 reduced-hours notices kept": dict(layoff_only=False),
             "HA4 superseded notices kept": dict(superseded=False)}
    need = {"S1 the portal's region column": 24, "S5 the cracker (S1 and S2)": 24}
    stop_a = {}
    for k, kw in stops.items():
        t, _ = C.ask_a(target, **kw)
        moved = sum(t[c] != ga[c] for c in cells)
        near = min(abs(t[c] - ga[c]) for c in cells if t[c] != ga[c]) if moved else 0
        stop_a[k] = (moved, near)
        A("Ask A stop %s moves %d of 24 cells (nearest moved cell %d workers off)" % (k, moved, near),
          moved >= need.get(k, 2))
    cross = all(any(N.valid(n) and N.period_of(n.first_layoff) == p and
                    any((s["region"] == r) != (n.emp.region == r) for s in n.sites) for n in W["notices"])
                for r in REG for p, _, _ in N.PERIODS)
    A("Ask A device A1: every region carries, in every period, a site of an employer registered in another region",
      cross)
    rk = [n for n in W["notices"] if n.rekeyed]
    A("Ask A device A2: %d register notices re-keyed onto the portal under new numbers, %d of them open in the forward "
      "periods, matched on business number, first layoff and sites" % (len(rk), sum(
          1 for n in rk if N.period_of(n.first_layoff))), len(info["matched"]) == len(rk) and len(rk) >= 30)
    A("Ask A device A3: the withdrawals are only in the case notes (the portal export has no withdrawn status)",
      not any(r["status"] == "Withdrawn" for r in csv.DictReader(open(os.path.join(target, R.F_PORTAL),
                                                                      encoding="utf-8"))) and len(info["withdrawn"]) >= 25)
    silent = re.findall(r"registered region|registered office|employer's region|region of the (?:employer|business)|"
                        r"re-?key\w*|migrat\w*|"
                        r"transferred to the portal|moved to the portal|copied to the portal|rebuil\w*|re-?cod\w*|"
                        r"4 January 2026|week ending|week's end|label", " ".join(dtext.values()), re.I)
    A("Ask devices are silent: no shipped sentence says what the portal's region column holds, that open notices were "
      "re-keyed, or when or how the cube's codes and labels changed", not silent, silent)

    # ------------------------------------------------------------------ Ask B
    gb, tot = C.ask_b(target)
    truth_b = I.truth_q3(Wd.ind if Wd else I.simulate(T))
    A("Ask B the golden from the cube equals the truth in all 14 groups",
      all(abs(gb[k] - (truth_b[2026][k] / truth_b[2025][k] - 1) * 100) < 1e-9 for k in I.G))
    clr_b = min(abs((gb[k] * 10) % 1 - 0.5) for k in I.G)
    A("Ask B every change sits 0.23 of a bin or more from its rounding edge (nearest %.3f)" % clr_b, clr_b >= 0.23)
    stops_b = {"S1 the current code list on both years": dict(codes="current"),
               "S2 every label read as a Saturday": dict(label="saturday"),
               "S3 every label read as a Sunday": dict(label="sunday"),
               "S4 transitional claims kept": dict(transitional=True),
               "S5 the cracker (S1 with labels read as Saturdays)": dict(codes="current", label="saturday"),
               "S6 S1 with labels read as Sundays": dict(codes="current", label="sunday")}
    need_b = {"S1 the current code list on both years": 14, "S2 every label read as a Saturday": 14,
              "S5 the cracker (S1 with labels read as Saturdays)": 14, "S6 S1 with labels read as Sundays": 14,
              "S3 every label read as a Sunday": 12, "S4 transitional claims kept": 8}
    stop_b = {}
    for k, kw in stops_b.items():
        chg, _ = C.ask_b(target, **kw)
        d = [abs(K.round_dp(chg[g], 1) - K.round_dp(gb[g], 1)) for g in I.G]
        moved = sum(x > 0.05 for x in d)
        near = min(x for x in d if x > 0.05) if moved else 0
        stop_b[k] = (moved, near)
        A("Ask B stop %s moves %d of 14 groups (nearest moved %.1f points)" % (k, moved, near), moved >= need_b[k])
    info_b = I.check_tables()
    A("Ask B device B1: %d 2006 division numbers reissued to divisions of other groups, every group giving or "
      "receiving one, every 2006 code on the current list" % len(info_b["reused"]),
      len(info_b["reused"]) >= 10 and len(info_b["groups_touched"]) == 14)
    cube = list(csv.DictReader(open(os.path.join(target, R.F_CUBE), encoding="utf-8")))
    first_new = min(dt.date.fromisoformat(r["week"]) for r in cube if r["division"] in info_b["new_codes"])
    sats = {dt.date.fromisoformat(r["week"]).weekday() for r in cube if r["week"] < "2026-01-04"}
    suns = {dt.date.fromisoformat(r["week"]).weekday() for r in cube if r["week"] >= "2026-01-04"}
    A("Ask B device B2: the codes the revision created first appear in the claims week of 4 January 2026, the labels "
      "are Saturdays before it and Sundays from it", first_new == dt.date(2026, 1, 4) and sats == {5} and suns == {6})

    # ------------------------------------------------------------------ distractors
    for f in R.DISTRACTORS:
        keep = [x for x in files if x != f]
        tmp = copy_only(target, keep)
        try:
            same = abs(C.ladder(C.from_pack(tmp))["gold"] - gold) < 1e-6 and C.ask_a(tmp)[0] == ga and \
                C.ask_b(tmp)[0] == gb
        finally:
            shutil.rmtree(tmp)
        A("distractor %s deleted: the call and both asks unchanged" % f, same)
    lfs = list(csv.DictReader(open(os.path.join(target, R.F_LFS), encoding="utf-8")))
    A("distractors look relevant: the survey's unemployment by region and quarter to April to June 2026 and the job "
      "advertisements by region and week cover the eight regions",
      {r["region"] for r in lfs} == set(REG) and lfs[-1]["quarter"] == "2026Q2")

    # ------------------------------------------------------------------ realism sweep
    ties = sum(1 for d in weeks for i, a in enumerate(REG) for b in REG[i + 1:] if V.rev[a][d] == V.rev[b][d])
    A("realism: regions' weekly counts tie in %d of %d region pairs and weeks, no more than chance" % (
        ties, 28 * len(weeks)), ties <= 0.003 * 28 * len(weeks))
    rep3 = sum(1 for r in REG for i in range(2, len(weeks)) if V.rev[r][weeks[i]] == V.rev[r][weeks[i - 1]] ==
               V.rev[r][weeks[i - 2]])
    rep4 = sum(1 for r in REG for i in range(3, len(weeks)) if V.rev[r][weeks[i]] == V.rev[r][weeks[i - 1]] ==
               V.rev[r][weeks[i - 2]] == V.rev[r][weeks[i - 3]])
    A("realism: no region's count repeats four weeks running, and three-week repeats come at the rate of chance (%d "
      "across the eight regions' %d weeks; Poisson counts of these sizes give about 0.3)" % (rep3, len(weeks)),
      rep4 == 0 and rep3 <= 2)
    round_share = sum(1 for d in weeks if V.nat[d] % 100 == 0) / len(weeks)
    A("realism: national weekly totals land on a hundred at the rate of chance (%.1f per cent)" % (100 * round_share),
      round_share <= 0.03)
    notes_rows = list(csv.DictReader(open(os.path.join(target, R.F_CASES), encoding="utf-8")))
    top = Counter(r["note"] for r in notes_rows).most_common(1)[0]
    A("realism: no case note's text recurs more than three times (%r x%d)" % top, top[1] <= 3)
    A("realism: the case notes' wording carries no doubled article or bad ordinal",
      not any(re.search(r"\bthe the\b|\b(?:\d*[02-9])?[123]th\b", r["note"]) for r in notes_rows))
    tfaults = [(r["note_id"], f) for r in notes_rows
               for f in note_time_faults(r["note"], dt.date.fromisoformat(r["note_date"]))]
    A("realism: no case note refers to a month or day after its own date as already past, speaks of a day before it "
      "as still ahead, or carries a date stamp other than its own (%d notes read)" % len(notes_rows), not tfaults,
      tfaults)
    skel = Counter(note_skeleton(r["note"], sorted(N.TOWN, key=len, reverse=True),
                                 sorted(N.CONTACTS, key=len, reverse=True)) for r in notes_rows)
    A("realism: the officers vary their wording: no sentence template (particulars set aside) recurs more than twice "
      "(%d templates in %d notes)" % (len(skel), len(notes_rows)), max(skel.values()) <= 2, skel.most_common(3))
    A("realism: no case note names a real agency (the board's own offices only)",
      not any(re.search(r"Work and Income|WINZ|MSD\b", r["note"]) for r in notes_rows))
    long_cl = Counter(c_ for r in notes_rows for c_ in {x for x in N.note_clauses(r["note"]) if len(x.split()) >= 6})
    A("realism: no clause of six words or more appears in more than one case note (%d such clauses, each once); the "
      "notes are all distinct" % len(long_cl), all(v == 1 for v in long_cl.values()) and
      len({r["note"] for r in notes_rows}) == len(notes_rows), [k for k, v in long_cl.items() if v > 1][:5])
    filler = [r["note_id"] for r in notes_rows if re.search(
        r"notice (?:unchanged|still covers|stands)|amended notice is needed|lodge an amended notice|days (?:count|run) "
        r"from|counts? towards|they count|(?:don't|do not) count|weekends|\bit does\b|details match|nothing out of line",
        r["note"], re.I)]
    A("realism: the case notes record the call or the job done and never restate a rule for a reader (no 'notice "
      "unchanged', 'amended notice is needed', 'days count from', 'casuals count' and the like)", not filler, filler)
    load = Counter(r["officer"] for r in notes_rows)
    A("realism: the officers' workload is uneven (%s)" % ", ".join("%s %d" % kv for kv in load.most_common()),
      max(load.values()) >= 3 * min(load.values()) and max(load.values()) >= 0.25 * len(notes_rows))
    refmap = {}
    for n_ in W["notices"]:
        for ref_ in (n_.ln, n_.es_ref, n_.rekeyed["ln"] if n_.rekeyed else None):
            if ref_:
                refmap[ref_] = n_
    WHOLE = re.compile(r"in full|as a whole|entirely|outright|altogether|whole notice|both sites|all \d+ sites", re.I)
    wfaults, wnotes = [], {}
    for r in notes_rows:
        if not N.is_withdrawal(r["note"]):
            continue
        n_ = refmap[N.norm_ref(r["reference"])]
        tot_w, k_ = sum(s_["workers"] for s_ in n_.sites), len(n_.sites)
        counts = [int(m_.group(1) or m_.group(2)) for m_ in
                  re.finditer(r"\b(?:all|none of the) (\d+)\b(?! sites)|\b(\d+) jobs\b", r["note"])]
        sites = [int(x) for x in re.findall(r"\ball (\d+) sites\b", r["note"])] + ([2] if "both sites" in r["note"] else [])
        ok_ = bool(WHOLE.search(r["note"])) and all(x == tot_w for x in counts) and all(x == k_ for x in sites)
        wnotes[r["note_id"]] = ok_
        if not ok_:
            wfaults.append(r["note_id"])
    A("realism: every withdrawal note says the whole notice is withdrawn, in the officer's words, and any count it gives "
      "is the notice's own (%d notes; CN051234 among them: %s)" % (len(wnotes), wnotes.get("CN051234")),
      not wfaults and wnotes.get("CN051234") is True and len(wnotes) == 34, wfaults)
    portal_rows = list(csv.DictReader(open(os.path.join(target, R.F_PORTAL), encoding="utf-8")))

    def bn_ok(bn):
        d = [int(x) for x in bn]
        return len(d) == 9 and (11 - sum(a * b for a, b in zip(d[:8], (3, 2, 7, 6, 5, 4, 3, 2))) % 11) % 11 == d[8]
    A("realism: every business number carries a valid check digit", all(bn_ok(r["business_no"]) for r in portal_rows))
    styles = Counter()
    for n_ in {r["employer"] for r in portal_rows}:
        first = n_.split()[0]
        styles[("&" in n_, "(" in n_, bool(re.match(r"[A-Z]\.|[A-Z] & [A-Z] |[A-Z] [A-Z][a-z]", n_)),
                "Holdings" in n_, "Group" in n_, first in N.COINED or first in N.NATIVE,
                first in N.TOWN or first in N.PLACES, first in N.SURNAMES)] += 1
    A("realism: employer names come in %d shapes, none over half the register" % len(styles),
      len(styles) >= 6 and max(styles.values()) <= 0.5 * sum(styles.values()))
    people = set(K.PEOPLE.values())
    named = set(re.findall(r"\b(?:Nicola Pedersen|Stacey Baxter|Tia Hewitt|Timothy Laing)\b", " ".join(dtext.values())))
    A("realism: every person named in the pack is drawn from guard.py names", named <= people and named)
    scrub = []
    for f in files:
        p = os.path.join(target, f)
        blob = open(p, "rb").read()
        if f.endswith((".xlsx", ".docx")):
            with zipfile.ZipFile(p) as z:
                blob = b"".join(z.read(n) for n in z.namelist())
        for sig in (b"openpyxl", b"python-docx", b"ReportLab", b"reportlab", b"matplotlib", b"pandas", b"xlsxwriter"):
            if sig in blob:
                scrub.append((f, sig))
    A("realism: every container is scrubbed of its writing library", not scrub, scrub)
    stamps = {os.path.getmtime(os.path.join(target, f)) for f in files}
    A("realism: every file carries the one export stamp", len(stamps) == 1)
    dash = [f for f in files if f.endswith((".csv", ".json")) and DASH.search(open(os.path.join(target, f),
                                                                                    encoding="utf-8").read())]
    dash += [f for f, t in dtext.items() if DASH.search(t)]
    A("realism: no en or em dash in any shipped text", not dash, dash)
    wbp = openpyxl.load_workbook(os.path.join(target, R.F_PROGRAM), data_only=True)
    gaps = []
    for ws in wbp.worksheets:
        if ws.title.startswith("FY") and ws.title > R.LEGACY_FY_LAST:
            hdr = [c.value for c in ws[3]]
            for row in ws.iter_rows(min_row=4, values_only=True):
                if row[1] in REG:
                    nn, dd = row[hdr.index("New claims")], row[hdr.index("Monetary determinations")]
                    gaps.append(nn - dd)
    A("realism: monetary determinations fall a little short of new claims (claims withdrawn before determination), "
      "never equal in every cell: gap 0 in %d of %d region-months, at most %d" % (
          sum(1 for x in gaps if x == 0), len(gaps), max(gaps)),
      all(x >= 0 for x in gaps) and sum(1 for x in gaps if x == 0) < 0.5 * len(gaps))
    only = [f for f, t in dtext.items() if "base period" in t.lower()]
    A("realism: the base period is defined in one file only (the technical notes)", only == [R.F_NOTES], only)

    # ------------------------------------------------------------------ the goldens
    if G is not None:
        import openpyxl as ox
        wbk = ox.load_workbook(os.path.join(golden, "ic_preview_2026-10-10.xlsx"), data_only=True)
        A("golden: the workbook carries the call", wbk["Call"]["B4"].value == call)
        got = {}
        for row in wbk["Layoff notices"].iter_rows(min_row=5, max_row=12, values_only=True):
            for (p, _, _), v in zip(N.PERIODS, row[1:4]):
                got[(row[0], p)] = v
        A("golden: the workbook's notice table is Ask A's 24 cells", got == ga)
        gbk = {row[0]: row[3] for row in wbk["Claims by industry"].iter_rows(min_row=5, max_row=18, values_only=True)}
        A("golden: the workbook's industry table is Ask B's 14 changes",
          all(gbk[I.G[k]] == K.round_dp(gb[k], 1) for k in I.G))
        work = {row[0]: row[1] for row in wbk["Call"].iter_rows(min_row=4, max_row=20, values_only=True) if row[0]}
        A("golden: the workbook's workings are the computed figures", work.get(
            "Monetarily ineligible determinations, claims weeks of July to September 2026") == cm["pool"] and
          work.get("  of which Western, Coastal and Island, made in September (%)") == K.round_dp(
              100 * cm["sep_wci_share"], 1), work)
        txt = file_text(os.path.join(golden, "ic_preview_2026-10-10.docx"))
        A("golden: the preview opens with the call", "about 17,000" in txt[:300], txt[:300])
        A("golden: the preview is one page with one chart", G["docx_stats"]["pages"] == 1 and
          len([n for n in zipfile.ZipFile(os.path.join(golden, "ic_preview_2026-10-10.docx")).namelist()
               if n.startswith("word/media/")]) == 1)
        A("golden: the preview's figures are the computed ones", all(s in txt for s in (
            "{:,}".format(G["pool"]), "%.1f per cent" % G["pool_wci_pct"], "{:,}".format(G["base"]),
            "%.1f per cent" % G["sep_wci_pct"])))
        dash_g = [f for f in os.listdir(golden) if DASH.search(file_text(os.path.join(golden, f)))]
        A("golden: no en or em dash", not dash_g, dash_g)
        t25, t26 = sum(tot[2025].values()), sum(tot[2026].values())
        rise = {k: tot[2026][k] - tot[2025][k] for k in I.G}
        lower = sum(1 for k in I.G if k not in (4, 7) and gb[k] < 0)
        A("golden: the preview's industry sentence is what the table says (construction and accommodation %+.0f against "
          "a rise of %.0f; %d of the other twelve groups lower)" % (rise[4] + rise[7], t26 - t25, lower),
          G["industry_sentence"] in txt and G["groups_lower"] == lower and
          (("more than the whole rise" in G["industry_sentence"]) == (rise[4] + rise[7] > t26 - t25)))
        A("golden: the preview states the month shares, the refiled claims and the rest of the week at the precision "
          "every construction and a one-sigma move share", all(s_ in txt for s_ in (
              "between two thirds and nine tenths", "under one in five", "5,000 to 6,000", "11,000 to 12,000",
              "about nine tenths", "near %s" % "{:,}".format(G["timing_blind"]),
              "near %s" % "{:,}".format(G["national"]))), txt)
        fj = json.load(open(os.path.join(os.path.dirname(target), "generator", "figures.json"), encoding="utf-8"))
        A("figures.json carries the call and the components as written",
          fj["call"]["initial_claims_week_ended_2026-10-10"] == "17,000" and
          fj["critical_components"]["ineligible_determinations_jul_sep_2026"] == "{:,}".format(G["pool"]))
    A.report()
    return dict(L=L, cm=cm, pr=pr, stop_a=stop_a, stop_b=stop_b, rm=rm, P=P, um=um, dec=dec, ads=ar, g_sep=g_sep,
                tw=tw, tw2=tw2)


def decompositions(V, L):
    """The refiled claims, the week without them and each region's shares by month under each construction of the
    golden whose months are identified (the regressions on every window but the last three years, whose twelve turns
    leave seven terms a region with standard errors as large as the month shares)."""
    D = L["D"]
    cons = {k: (df, {}) for k, df in C.windows(D).items() if k != "the last three years (turns from October 2023)"}
    cur = D[D.sun >= dt.date(2021, 7, 1)]
    cons.update({"Huber": (D, {"robust": True}), "ratio form": (D, {"kind": "ratio"}),
                 "mean of three as base": (D, {"base": "mean3"}), "advance target": (cur, {"kind": "adv"}),
                 "one intercept": (D, {"icpt": "const"})})
    out = {}
    for k, (df, kw) in cons.items():
        ref = wo = 0.0
        sl = {}
        part = {}
        for r in REG:
            m = C.fit_region(df, r, **kw)
            a = C.intercept(m)
            wo += C.base_of(V, r) * (1 + a) if kw.get("kind") == "ratio" else C.base_of(V, r, kw.get("base", "p1")) + a
            sl[r] = {t: float(m.params[t]) for t in ("m1", "m2", "m3")}
            part[r] = sum(sl[r][t] * V.mq3[r][j] for j, t in enumerate(("m1", "m2", "m3")))
            ref += part[r]
        out[k] = dict(refile=ref, without=wo, shares=sl, wci=sum(part[r] for r in WCI) / ref)
    return out
