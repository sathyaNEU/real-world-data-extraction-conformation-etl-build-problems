"""task146 checks, run on every build: the input gates; the three-rules block (R1 the field's raw material, R2 every
mess item neutral, R3a the analyst test on the clean truth and the pack, R3b the decisive step alone, R3c no plant);
the strict rule 3 test on the shipped sentences that bear on how the call is computed; the one-sigma test on every
rounded figure; every rung by name; every construction of the golden; every semantic fork row (SF1 to SF14); the
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


def copy_only(target, files):
    tmp = tempfile.mkdtemp(prefix="t146_")
    for f in files:
        shutil.copy2(os.path.join(target, f), os.path.join(tmp, f))
    return tmp


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
    Vt = C.from_truth(T)
    Lt = C.ladder(Vt)
    R0 = [k for k in L["rivals"] if k.startswith("R0 ")][0]
    A("the call is 16,000 (%.0f)" % gold, call == 16000)
    A("the call sits mid-bin on a non-round value (clearance %.2f of a bin)" % K.bin_clearance(gold, 1000),
      K.bin_clearance(gold, 1000) >= 0.45 and abs(gold - round(gold, -2)) > 1)
    A("the truth's own expected advance count lies in the golden's bin (%.0f)" %
      (T.target_expected_revised * (1 - T.target_late_share)),
      K.round_to(T.target_expected_revised * (1 - T.target_late_share), 1000) == call)

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
      "closing-quarter determinations", len(L["D"]) == 50 and all("pool_" + r in L["D"] for r in REG))
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
                                             r"predict|\bturns?\b", h[1], re.I) and h[0] not in R.DISTRACTORS]
    A("R1 no shipped column holds a share, a refiled count, a step, a seasonal factor or a forecast", not bad_cols,
      bad_cols)
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
    # first-reported history in place of revised history (SF7)
    Va = C.from_pack(target)
    for r in REG:
        for d, v in Va.adv[r].items():
            Va.rev[r][d] = v
    C.finish(Va)
    La = C.ladder(Va)
    A("R2 SF7 the history at its first-reported counts (the current system's weeks) files the same call (%.0f)" %
      La["gold"], K.round_to(La["gold"], 1000) == call)
    A("R2 the program statistics' two layouts: the current layout's turns alone file the same call (%.0f)" %
      L["golden"]["the current system's turns"], K.round_to(L["golden"]["the current system's turns"], 1000) == call)
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
      L["golden"]["holiday-touched turns dropped"], K.round_to(L["golden"]["holiday-touched turns dropped"], 1000) == call)
    A("R2 the summer shutdown and January return: the golden without the January turns files the same call (%.0f)" %
      L["golden"]["without January turns"], K.round_to(L["golden"]["without January turns"], 1000) == call)
    Dn = L["D"][L["D"].qq != 3]
    nj = C.regional(V, Dn)
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
    A("R2 benefits in thousands of dollars, first payments and weeks claimed are not on the call's path (the call reads "
      "initial claims and ineligible determinations only)", True)
    A("R2 the ask paths' mess sits in files the call never opens",
      not (set(R.ASK_A_FILES + R.ASK_B_FILES) - {R.F_NOTES, R.F_REGIONS}) & {R.F_LEGACY, R.F_CURRENT, R.F_PROGRAM})

    # ------------------------------------------------------------------ R3a: the analyst test
    natv = L["national"]
    A("R3a the default path on the clean truth (the refiling the notes file, sized on the third quarter's national "
      "ineligible determinations at the national rate past turns show) files 14,000 (%.0f)" % Lt["national"]["all turns"],
      K.round_to(Lt["national"]["all turns"], 1000) == 14000)
    A("R3a the same default path on the pack files 14,000 (%.0f), two bins below the golden" % natv["all turns"],
      K.round_to(natv["all turns"], 1000) == 14000 and call - K.round_to(natv["all turns"], 1000) == 2000)
    A("R3a every national-rate variant files 14,000 or less, a full bin or more off (%s)" %
      ", ".join("%.0f" % v for v in natv.values()), all(K.round_to(v, 1000) <= 14000 for v in natv.values()))
    A("R3a the nearest national-rate variant is %.0f claims below the golden" % (gold - max(natv.values())),
      gold - max(natv.values()) >= 1500)
    A("R3a the seasonal route (factors of the quarter's first claims week on the level of the last four weeks) files "
      "13,000 on the clean truth and the pack (%.0f, %.0f)" % (Lt["rivals"][R0], L["rivals"][R0]),
      K.round_to(Lt["rivals"][R0], 1000) == K.round_to(L["rivals"][R0], 1000) == 13000)
    # ------------------------------------------------------------------ R3b: the decisive step alone
    A("R3b the decisive step alone (each region's refused claimants at that region's own share) turns the default "
      "path's 14,000 into 16,000 on the clean truth and the pack (%.0f, %.0f)" % (Lt["gold"], gold),
      K.round_to(Lt["gold"], 1000) == call)
    rv = L["rivals"]
    want = {"R0 seasonal factors of the quarter's first claims week on the level of the last four weeks (default)": 13000,
            "R1 last year's week times the last eight weeks' growth on the year": 12000,
            "R2 the step from the week before, one intercept per quarter of the year": 13000,
            "R3 the step scaled on the closing quarter's claims": 13000,
            "R3r the step scaled on the closing quarter's claims, region by region": 14000,
            "R0b ISO-week seasonal factors on the level of the last four weeks": 12000,
            "R2r a quarter-start ratio": 13000, "R2g quarter-start terms region by region": 13000}
    for k, b_ in want.items():
        A("R3b rung %s files %s (%.0f)" % (k, "{:,}".format(b_), rv[k]), K.round_to(rv[k], 1000) == b_)
    A("R3b the one-share panel (every region's own intercepts, one share for all) files 14,000 (%.0f)" %
      natv["one share for every region, each region's own intercepts"],
      K.round_to(natv["one share for every region, each region's own intercepts"], 1000) == 14000)
    for k, v in L["latest"].items():
        A("R3b latest-period rate, %s, files %s (%.0f), two bins or more below" % (k, "{:,}".format(K.round_to(v, 1000)), v),
          K.round_to(v, 1000) <= call - 2000)
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
      not re.search(r"region|season|refil|quarter|determination|base period", q1, re.I), q1)
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
      not re.search(r"\d|per cent|share|rate|region|most|many|few|half|first week|first claims week", filed, re.I))
    method = re.findall(r"refil\w*|\bcom(?:e|es|ing) back\b|re-?admit\w*|regression|"
                        r"seasonal(?:ly)? (?:factor|adjustment|component|pattern)|quarter[- ]start|"
                        r"first (?:claims )?week of (?:the|a|each) quarter|turn of the quarter|"
                        r"share of (?:the )?(?:refused|ineligible|claimants)|(?:most|many|few|half|some) of (?:them|those|"
                        r"the refused|the claimants)|varies by region|differ\w* (?:by|between|across) regions?",
                        alltext, re.I)
    A("R3 strict: no shipped sentence or note says how many refused claimants file again, when within a quarter, or "
      "that the share differs by region, and none names a seasonal factor or a regression", not method, method)
    every_refiles = V.nat[V.latest] + cm["pool"]
    A("R3 strict: the HOW sentences executed word for word on clean data give no figure of their own; the estimators "
      "they admit file the default path's 14,000 (the filed refiling at the national rate), the seasonal step's 13,000 "
      "or, every refused claimant filing again in the week, %s, never 16,000" % "{:,}".format(K.round_to(every_refiles, 1000)),
      K.round_to(Lt["rivals"][R0], 1000) != call and K.round_to(Lt["national"]["all turns"], 1000) != call and
      K.round_to(every_refiles, 1000) != call)
    A("R3 strict: the behaviour the decisive step turns on (each region's own share) is inferred from the data, and "
      "the data rejects the rival (one share for every region) by a visible margin (F %.1f on %d and %d degrees of "
      "freedom)" % ((P := C.panel(V, L["D"]))["F"], P["df"][0], P["df"][1]), P["F"] >= 100)

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

    # ------------------------------------------------------------------ every region-aware construction
    se = pr["se_call"]
    G_POOL = sum(V.inelig_m[((2026, m_), r)] for m_ in (7, 8, 9) for r in REG)
    G_POOL_WCI = K.round_dp(100.0 * sum(V.inelig_m[((2026, m_), r)] for m_ in (7, 8, 9) for r in WCI) / G_POOL, 1)
    ra = dict(L["golden"])
    ra.update(C.region_aware(V, L))
    for k, v in ra.items():
        A("region-aware construction, %s: %.0f, clear of 15,500 and 16,500 by more than one sigma (%.0f and %.0f "
          "against %.0f)" % (k, v, v - 15500, 16500 - v, se),
          K.round_to(v, 1000) == call and v - 15500 > se and 16500 - v > se)
    A("the region-aware constructions span %.0f to %.0f (%d of them); the nearest edge is %.0f claims away, %.1f sigma" % (
        min(ra.values()), max(ra.values()), len(ra), min(min(v - 15500, 16500 - v) for v in ra.values()),
        min(min(v - 15500, 16500 - v) for v in ra.values()) / se), len(ra) >= 20)
    nrp, nrp_se = L["nat_on_regional_pools"]
    A("the national step on the eight regional pools at once (one equation, the regional steps discarded) lands the "
      "golden's bin: %.0f, standard error %.0f, %.1f times the regional build's" % (nrp, nrp_se, nrp_se / se),
      K.round_to(nrp, 1000) == call and nrp_se >= 3 * se)

    # ------------------------------------------------------------------ one sigma, every rounded figure
    lo, hi = gold - se, gold + se
    A("sigma: one standard error (%.0f claims) either way leaves the call at 16,000 (%.0f to %.0f)" % (se, lo, hi),
      K.round_to(lo, 1000) == K.round_to(hi, 1000) == call)
    A("sigma: the flip to 15,000 needs the estimate %.0f claims lower (%.1f standard errors), the flip to 17,000 %.0f "
      "higher (%.1f)" % (gold - 15500, (gold - 15500) / se, 16500 - gold, (16500 - gold) / se),
      (gold - 15500) / se >= 4 and (16500 - gold) / se >= 4)
    ref, wo = cm["refile"], cm["without"]
    A("sigma: the refiled claims (%.0f, se %.0f) stay between 4,000 and 5,000 at one standard error" % (ref, pr["se_refile"]),
      4000 <= ref - pr["se_refile"] and ref + pr["se_refile"] <= 5000)
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
    A("sigma: Western's share stays about one in four (0.24 to 0.29), Coastal's and Island's about three in ten (0.27 to "
      "0.35), every other region's under one in ten, at one standard error (%s)" % ", ".join(
          "%s %.3f+-%.3f" % (r, parts[r]["slope"], parts[r]["slope_se"]) for r in REG),
      0.24 <= parts["Western"]["slope"] - parts["Western"]["slope_se"] and
      parts["Western"]["slope"] + parts["Western"]["slope_se"] <= 0.29 and
      all(0.27 <= parts[r]["slope"] - parts[r]["slope_se"] and parts[r]["slope"] + parts[r]["slope_se"] <= 0.35
          for r in ("Coastal", "Island")) and
      all(parts[r]["slope"] + parts[r]["slope_se"] < 0.1 for r in REG if r not in WCI))
    A("sigma: the third quarter's determinations (%s) and their %.1f per cent in Western, Coastal and Island are counts "
      "from the workbook, with no estimation error" % ("{:,}".format(cm["pool"]), 100 * cm["pool_wci_share"]),
      cm["pool"] == G_POOL and K.round_dp(100 * cm["pool_wci_share"], 1) == G_POOL_WCI)
    # the same statements under every construction
    dec = decompositions(V, L)
    A("every construction keeps the refiled claims between 4,000 and 5,000 and the rest of the week between 11,000 "
      "and 12,000 (%s)" % "; ".join("%s %.0f/%.0f" % (k, x["refile"], x["without"]) for k, x in dec.items()),
      all(4000 <= x["refile"] <= 5000 and 11000 <= x["without"] <= 12000 for x in dec.values()))
    A("every construction keeps about nine tenths of the refiled claims in Western, Coastal and Island, Western about "
      "one in four, Coastal and Island about three in ten, every other region under one in ten",
      all(0.85 <= x["wci"] <= 0.95 and 0.24 <= x["shares"]["Western"] <= 0.29 and
          all(0.27 <= x["shares"][r] <= 0.35 for r in ("Coastal", "Island")) and
          all(x["shares"][r] < 0.1 for r in REG if r not in WCI) for x in dec.values()))

    # ------------------------------------------------------------------ the data rejects pooling
    e = C.loo(V, L["D"])
    rm = {k: float(np.sqrt(np.mean(v ** 2))) for k, v in e.items()}
    rm["one_share"] = C.loo_one_share(V, L["D"])
    A("margin: leave one turn out, the national step misses by %.0f claims under the regional build against %.0f for "
      "the national pool at the national rate, %.0f for one share in every region, %.0f for the closing quarter's claims "
      "and %.0f for a quarter-start term" % (rm["regional"], rm["pool"], rm["one_share"], rm["claims"], rm["term"]),
      rm["regional"] < min(rm["pool"], rm["one_share"], rm["claims"], rm["term"]) and
      rm["pool"] >= 1.4 * rm["regional"] and rm["one_share"] >= 1.4 * rm["regional"])
    A("margin: region by region, one share for every region misses by %.0f claims a region and turn against %.0f for "
      "each region's own" % (P["rmse_common"], P["rmse_regional"]), P["rmse_regional"] <= 0.6 * P["rmse_common"])
    mn = C.fit_region(L["D"], "NAT")
    A("margin: the national pool's fit is visibly loose (R squared %.2f, residual %.0f claims) beside the regional "
      "build's leave-one-out %.0f" % (mn.rsquared, math.sqrt(mn.scale), rm["regional"]),
      mn.rsquared < 0.75 and math.sqrt(mn.scale) > 1.3 * rm["regional"])
    um = C.usual_mix(V, L)
    A("mix: the third quarter's determinations (%d) are about one and a half times the median closing quarter's (%.0f)" %
      (cm["pool"], um["median_pool"]), 1.45 <= cm["pool"] / um["median_pool"] <= 1.8)
    A("mix: %.1f per cent of them sit in Western, Coastal and Island against %.1f per cent at the median turn" %
      (100 * cm["pool_wci_share"], 100 * um["median_share"]), cm["pool_wci_share"] >= um["median_share"] + 0.25)
    tw = C.twin_same_quarter(V, L["D"])
    A("twin: the %s and %s turns, national pools %d and %d, Western, Coastal and Island's part %.3f and %.3f, steps %d "
      "and %d" % ((tw["hi_turn"], tw["lo_turn"], tw["hi_pool"], tw["lo_pool"], tw["hi_share"], tw["lo_share"],
                   tw["hi_step"], tw["lo_step"]) if tw else ("-", "-", 0, 0, 0, 0, 0, 0)),
      bool(tw) and tw["hi_share"] - tw["lo_share"] >= 0.2 and tw["hi_step"] > tw["lo_step"] + 800)
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
    revs = [abs(int(r["initial_claims"]) - int(r["first_reported_initial_claims"])) / int(r["initial_claims"])
            for r in cur if r["count_status"] == "Revised"]
    nat_rev = {}
    for r in cur:
        if r["count_status"] == "Revised":
            k_ = r["claims_week_start"]
            a0, b0 = nat_rev.get(k_, (0, 0))
            nat_rev[k_] = (a0 + int(r["initial_claims"]), b0 + int(r["first_reported_initial_claims"]))
    worst = max((a0 - b0) / a0 for a0, b0 in nat_rev.values())
    A("SF3 the first report is the advance count; national revisions are at most about 1 per cent (largest %.2f per "
      "cent) and the advance target keeps the bin (%.0f)" % (100 * worst, L["golden"]["advance count as the target "
                                                                                    "(current system)"]),
      worst < 0.015 and K.round_to(L["golden"]["advance count as the target (current system)"], 1000) == call)
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
      "Sunday (C1, %d region-months)" % len(sums), all(V.new_m[k] == v for k, v in sums.items()))
    A("SF7 history at first-reported or revised counts: the same call (asserted under R2)", K.round_to(La["gold"], 1000) == call)
    A("SF8 the turns the shares are measured on: every window files 16,000 (all, fourth-quarter only, third and fourth, "
      "without 2020 and 2021, since 2017, since 2019, the current system's, without January)",
      all(K.round_to(L["golden"][k], 1000) == call for k in ("all turns", "fourth-quarter turns only",
                                                             "third and fourth-quarter turns", "without 2020 and 2021",
                                                             "since 2017", "since 2019", "the current system's turns",
                                                             "without January turns")))
    A("SF9 the base week: the mean of the last three weeks files the same call (%.0f)" %
      L["golden"]["mean of the last three weeks as base"],
      K.round_to(L["golden"]["mean of the last three weeks as base"], 1000) == call)
    per_region = sum(K.round_to(parts[r]["base"] + parts[r]["icpt"] + parts[r]["refile"], 1) for r in REG)
    A("SF10 rounding once: the regions rounded to whole claims and summed, then rounded, give the same call",
      K.round_to(per_region, 1000) == call)
    A("SF11 how many is the expected count: a Poisson count of 16,000 has its median within one claim of its mean, the "
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

    # ------------------------------------------------------------------ Ask A
    W = Wd.notices if Wd else N.simulate()
    truth_a = N.truth_table(W)
    ga, info = C.ask_a(target)
    cells = [(r, p[0]) for r in REG for p in N.PERIODS]
    A("Ask A the golden from the shipped rows equals the truth in all 24 cells", ga == truth_a)
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
        txt = file_text(os.path.join(golden, "ic_preview_2026-10-10.docx"))
        A("golden: the preview opens with the call", "about 16,000" in txt[:300], txt[:300])
        A("golden: the preview is one page with one chart", G["docx_stats"]["pages"] == 1 and
          len([n for n in zipfile.ZipFile(os.path.join(golden, "ic_preview_2026-10-10.docx")).namelist()
               if n.startswith("word/media/")]) == 1)
        A("golden: the preview's figures are the computed ones", all(s in txt for s in (
            "{:,}".format(G["pool"]), "%.1f per cent" % G["pool_wci_pct"], "{:,}".format(G["base"]))))
        dash_g = [f for f in os.listdir(golden) if DASH.search(file_text(os.path.join(golden, f)))]
        A("golden: no en or em dash", not dash_g, dash_g)
        t25, t26 = sum(tot[2025].values()), sum(tot[2026].values())
        rise = {k: tot[2026][k] - tot[2025][k] for k in I.G}
        lower = sum(1 for k in I.G if k not in (4, 7) and gb[k] < 0)
        A("golden: the preview's industry sentence is what the table says (construction and accommodation %+.0f against "
          "a rise of %.0f; %d of the other twelve groups lower)" % (rise[4] + rise[7], t26 - t25, lower),
          G["industry_sentence"] in txt and G["groups_lower"] == lower and
          (("more than the whole rise" in G["industry_sentence"]) == (rise[4] + rise[7] > t26 - t25)))
        A("golden: the preview states the regional shares, the refiled claims and the rest of the week at the precision "
          "every construction and a one-sigma move share", all(s_ in txt for s_ in (
              "about one refused claimant in four", "about three in ten in Coastal and Island",
              "fewer than one in ten", "4,000 to 5,000", "11,000 to 12,000", "about nine tenths",
              "about one and a half times a normal quarter", "near %s" % "{:,}".format(G["national"]))))
        fj = json.load(open(os.path.join(os.path.dirname(target), "generator", "figures.json"), encoding="utf-8"))
        A("figures.json carries the call and the components as written",
          fj["call"]["initial_claims_week_ended_2026-10-10"] == "16,000" and
          fj["critical_components"]["ineligible_determinations_jul_sep_2026"] == "{:,}".format(G["pool"]))
    A.report()
    return dict(L=L, cm=cm, pr=pr, stop_a=stop_a, stop_b=stop_b, rm=rm, P=P, um=um, dec=dec, ads=ar)


def decompositions(V, L):
    """The refiled claims, the week without them and the regional shares under each construction of the golden."""
    D = L["D"]
    cons = {"all turns": (D, {}), "fourth-quarter turns only": (D[D.qq == 4], {}),
            "third and fourth": (D[D.qq >= 3], {}), "without 2020 and 2021": (D[~D.y.isin([2020, 2021])], {}),
            "since 2019": (D[D.y >= 2019], {}), "since 2017": (D[D.y >= 2017], {}),
            "without January": (D[D.qq != 1], {}), "current system": (D[D.sun >= dt.date(2021, 7, 1)], {}),
            "Huber": (D, {"robust": True}), "ratio form": (D, {"kind": "ratio"}),
            "mean of three as base": (D, {"base": "mean3"}),
            "advance target": (D[D.sun >= dt.date(2021, 7, 1)], {"kind": "adv"})}
    out = {}
    for k, (df, kw) in cons.items():
        ref = wo = 0.0
        sl = {}
        for r in REG:
            m = C.fit_region(df, r, **kw)
            P = V.pool[(r, C.Q3)]
            icpt = m.params["q_4"]
            wo += C.base_of(V, r) * (1 + icpt) if kw.get("kind") == "ratio" else C.base_of(V, r, kw.get("base", "p1")) + icpt
            ref += m.params["pool"] * P
            sl[r] = float(m.params["pool"])
        out[k] = dict(refile=ref, without=wo, shares=sl,
                      wci=sum(sl[r] * V.pool[(r, C.Q3)] for r in WCI) / ref)
    return out
