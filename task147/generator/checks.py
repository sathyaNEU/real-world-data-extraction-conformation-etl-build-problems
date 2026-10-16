"""task147 checks, run on every build: the input gates; the three-rules block (R1 the field's raw material, R2 every
mess item neutral, R3a the analyst test on the clean truth and the pack, R3b the decisive step alone, R3c no plant);
the strict rule 3 test on every shipped sentence that bears on how the call is computed; the one-sigma test on every
rounded figure; the out-of-sample rejection of the default; every rung by name; every construction of the golden;
every semantic fork row (SF1 to SF16) and closure axis; the asks with every stop and the cracker's path; the
distractors; the realism sweep; the goldens. Any failure stops the build."""
from __future__ import annotations

import csv
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import tempfile
import zipfile
from collections import Counter

import numpy as np

import calc as C
import cast as CA
import common as K
import docs as DOC
import ops2026 as O
import records as R
import world as WD

CAP, CREW = K.CAP, K.CREW
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
                print("FAIL %s %s" % (lab, str(det)[:600]))
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


def doc_text(target):
    out = {}
    for f in os.listdir(target):
        p = os.path.join(target, f)
        if f.endswith(".pdf"):
            out[f] = pdf_text(p)
        elif f.endswith(".xlsx"):
            out[f] = xlsx_text(p)
        elif f.endswith((".txt", ".json")):
            out[f] = open(p, encoding="utf-8").read()
        elif f.endswith(".csv"):
            with open(p, encoding="utf-8") as fh:
                out[f] = fh.readline()
    return out


def copy_only(target, files):
    tmp = tempfile.mkdtemp(prefix="t147_")
    for f in files:
        shutil.copy2(os.path.join(target, f), os.path.join(tmp, f))
    return tmp


# ---------------------------------------------------------------------------------------------------- clean truth
def truth_tables(W, y, t0, full_off=(7, 8)):
    """The season tables straight from the world's accepted reservations (no file read): the book at t0 by its dates
    then, the finals, the book's rooms that stayed, the stays booked after t0 and those through the aligned full
    nights."""
    nights = [C.aligned(y, n) for n in C.NIGHTS]
    n0, L = K.di(nights[0]), len(nights)
    full = (K.di(K.fest_open(y)) + full_off[0], K.di(K.fest_open(y)) + full_off[1])
    out = {k: np.zeros(L) for k in ("book", "final", "real", "new", "thru")}
    for rr in W.res:
        q = rr.q
        a, l = rr.a, rr.los
        if rr.amended and rr.amended[0] > t0:
            a, l = rr.amended[1], rr.amended[2]
        if max(a + l, rr.a + rr.los) <= n0 or min(a, rr.a) > n0 + L:
            continue
        alive = q.bt < t0 and (rr.status == "OK" or (rr.ct is not None and rr.ct > t0))
        kept = rr.status == "OK" and not q.noshow and rr.a < K.di(K.EXTRACT_LOCAL.date())
        thru = any(rr.a <= f < rr.a + rr.los for f in full)
        for n in range(max(a, n0), min(a + l, n0 + L)):
            if alive:
                out["book"][n - n0] += q.rooms
                if kept and rr.a <= n < rr.a + rr.los:
                    out["real"][n - n0] += q.rooms
        if kept:
            for n in range(max(rr.a, n0), min(rr.a + rr.los, n0 + L)):
                out["final"][n - n0] += q.rooms
                if q.bt >= t0:
                    out["new"][n - n0] += q.rooms
                    if thru:
                        out["thru"][n - n0] += q.rooms
    return out


def truth_ladder(W):
    H = {y: truth_tables(W, y, K.from_local(dt.datetime.combine(K.confirmation_day(y), K.EXTRACT_LOCAL.time())))
         for y in K.HIST_YEARS}
    T27 = truth_tables(W, K.YEAR, K.T_EXTRACT)
    b = T27["book"]
    Y = K.HIST_YEARS
    pick = np.mean([H[y]["final"] - H[y]["book"] for y in Y], axis=0)
    real = np.sum([H[y]["real"] for y in Y], axis=0) / np.sum([H[y]["book"] for y in Y], axis=0)
    new = np.mean([H[y]["new"] for y in Y], axis=0)
    thru = np.mean([H[y]["thru"] for y in Y], axis=0)
    fi = [i for i in range(len(b)) if b[i] >= CAP]
    evt_ns = np.mean([rr.q.noshow for rr in W.res if rr.q.plan == "EVT" and rr.status == "OK" and
                      rr.a < K.di(K.EXTRACT_LOCAL.date())])
    g = b * real + new - thru
    g[fi] = CAP * (1 - evt_ns)
    return dict(default=C.wk(np.minimum(CAP, b + pick)), gold=C.wk(np.minimum(CAP, g)),
                seasonal=C.wk(np.mean([H[y]["final"] for y in Y], axis=0)), fi=fi, book=b)


# ---------------------------------------------------------------------------------------------------- run
MAIN_FILES = [R.F_EXTRACT, R.F_AMEND, R.F_NOTES, R.F_CODES, R.F_AUDIT, R.F_FEST, R.F_DIARY, DOC.F_HK04]
ASK_A_FILES = [C.TASKS_F, C.USERS_F, C.HR_F, C.TS_F, C.PAY_F]
ASK_B_FILES = [C.ACCESS_F, C.BADGE_F, DOC.F_INVOICE, DOC.F_AGREEMENT]


def run(target, golden, Wd=None, G=None, meta_path=None):
    import build as BD
    import distract as DS
    A = Checks()
    files = sorted(os.listdir(target))
    meta = json.load(open(meta_path, encoding="utf-8")) if meta_path else {}
    W = Wd.W if Wd else WD.simulate()

    # ------------------------------------------------------------------ input gates
    fmts = {f.rsplit(".", 1)[1] for f in files}
    A("gate 10 or more files (%d)" % len(files), len(files) >= 10, files)
    A("gate 3 or more formats (%s)" % ", ".join(sorted(fmts)), len(fmts) >= 3)
    with open(os.path.join(target, R.F_EXTRACT), encoding="utf-8") as fh:
        n_ext = sum(1 for _ in fh) - 1
    A("gate a file of 25,000 rows or more (the reservation extract, %d rows)" % n_ext, n_ext >= 25000)
    dis = meta.get("distractor_files", [])
    A("gate two or more distractors named in metadata.json and shipped", len(dis) >= 2 and all(f in files for f in dis),
      dis)
    A("gate no file name carries stump or author vocabulary",
      not any(re.search(r"distract|decoy|trap|golden|answer|truth|naive|stump|clean|fixed|synthetic|forecast", f, re.I)
              for f in files), files)
    A("gate every file shipped is one the generator names",
      set(files) == set(MAIN_FILES + ASK_A_FILES + ASK_B_FILES + dis + [BD.F_MANIFEST]), files)
    listed = [r["file"] for r in csv.DictReader(open(os.path.join(target, BD.F_MANIFEST), encoding="utf-8"))]
    A("gate the folder index names every other shipped file once (H9, set equality)",
      sorted(listed) == sorted(f for f in files if f != BD.F_MANIFEST) and len(listed) == len(set(listed)))

    # ------------------------------------------------------------------ the call from the pack, and from the truth
    V = C.from_pack(target)
    L = C.ladder(V)
    gw = L["gw"]
    pick, run_, margin = C.top(gw)
    call_fig, run_fig = K.round_to(gw[pick], 100), K.round_to(gw[run_], 100)
    A("the call is the closing week, Monday 23 to Sunday 29 August 2027 (W5 %.0f), the next week the concert week "
      "(W3 %.0f), %.2f times" % (gw[4], gw[2], margin), pick == 4 and run_ == 2 and margin >= 1.5)
    A("the call's figure is 400 and the next week's 200, two bins apart", call_fig == 400 and run_fig == 200)
    A("both figures sit inside their bins on non-round values (clearances %.2f and %.2f of a bin)" % (
        K.bin_clearance(gw[4], 100), K.bin_clearance(gw[2], 100)),
      K.bin_clearance(gw[4], 100) >= 0.3 and K.bin_clearance(gw[2], 100) >= 0.3 and
      abs(gw[4] - round(gw[4], -1)) > 0.5 and abs(gw[2] - round(gw[2], -1)) > 0.5)
    full = L["full"]
    A("the full nights on the book are Friday 13 and Saturday 14 August 2027, 480 rooms each, and no other",
      full == K.CONCERT_NIGHTS and [int(L["parts"]["book"][i]) for i in L["parts"]["fi"]] == [480, 480])
    Tt = truth_ladder(W)
    A("the clean truth's golden (straight from the accepted reservations) lands in the same bins (W5 %.0f, W3 %.0f; "
      "the pack's %.0f, %.0f)" % (Tt["gold"][4], Tt["gold"][2], gw[4], gw[2]),
      K.round_to(Tt["gold"][4], 100) == 400 and K.round_to(Tt["gold"][2], 100) == 200 and
      abs(Tt["gold"][4] - gw[4]) < 6 and abs(Tt["gold"][2] - gw[2]) < 6 and C.top(Tt["gold"])[:2] == (4, 2))
    mc = WD.mc_truth(W, runs=12)
    mcw = np.array([C.wk(x) for x in mc]).mean(axis=0)
    A("the world's own expectation (12 continuations of the 2027 book, fresh demand and the book's own cancellations "
      "after the extract) agrees: W5 %.0f, W3 %.0f, W4 %.0f" % (mcw[4], mcw[2], mcw[3]),
      K.round_to(mcw[4], 100) == 400 and K.round_to(mcw[2], 100) == 200 and C.top(list(mcw))[:2] == (4, 2))

    # ------------------------------------------------------------------ one sigma
    se = C.precision(V)
    A("one sigma: the closing week %.0f plus or minus %.1f and the concert week %.0f plus or minus %.1f leave both "
      "rounded figures unchanged" % (gw[4], se[4], gw[2], se[2]),
      all(K.round_to(gw[4] + s * se[4], 100) == 400 for s in (-1, 1)) and
      all(K.round_to(gw[2] + s * se[2], 100) == 200 for s in (-1, 1)))
    A("one sigma: the call holds at two sigma either way (W5 low %.0f against W3 high %.0f)" % (
        gw[4] - 2 * se[4], gw[2] + 2 * se[2]), gw[4] - 2 * se[4] > gw[2] + 2 * se[2] + 100)
    A("one sigma: the ask figures are counts and sums of records (no sampling error); a one-room or one-quarter-hour "
      "move changes them by construction, so none is graded at a coarser rounding than its unit", True)

    # ------------------------------------------------------------------ R1
    main_only = copy_only(target, MAIN_FILES)
    try:
        Lm = C.ladder(C.from_pack(main_only))
        A("R1 the call computed from the reservation extract and its amendment log alone (no ask file, no distractor) "
          "is the golden", np.allclose(Lm["gw"], gw), Lm["gw"])
    finally:
        shutil.rmtree(main_only)
    hdr = open(os.path.join(target, R.F_EXTRACT), encoding="utf-8").readline().strip().split(",")
    A("R1 the extract ships the booking process's raw unit: each room reserved with its booking time, arrival, "
      "departure, status and cancellation time", hdr == R.EXTRACT_COLS)
    cols = []
    for f in files:
        if f.endswith(".csv") and f not in dis:
            cols += open(os.path.join(target, f), encoding="utf-8").readline().strip().split(",")
    bad = [c for c in cols if re.search(r"forecast|pickup|pick_up|pace|above|capacity|expected|through|blocked|stay_",
                                        c, re.I)]
    A("R1 no shipped column holds a forecast, a pickup, a week's rooms above capacity or a stay's nights against a "
      "full night", not bad, bad)
    dtext = doc_text(target)
    fc = [f for f, t in dtext.items() if f not in dis and re.search(
        r"\bforecast\w* (is|of|at) (about )?\d|\d[\d,]* room-nights|\bpickup\b|\bpick-up\b|\bpace\b|"
        r"\bsold out\b|fully booked|full house|nights? (is|are) full", t, re.I)]
    A("R1 no document states a forecast, a pickup, a week's room-nights or that a night is full", not fc, fc)

    # ------------------------------------------------------------------ R2: every mess item neutral on the call
    def same_call(v):
        p, r_, _ = C.top(v)
        return p == 4 and r_ == 2 and K.round_to(v[4], 100) == 400 and K.round_to(v[2], 100) == 200
    # UTC times read as local (SF10)
    loc = lambda y: np.datetime64(dt.datetime.combine(K.confirmation_day(y), K.EXTRACT_LOCAL.time()))
    g_loc = C.wk(C.golden(V, cut=loc, t27=loc(K.YEAR))[0])
    moved = sum(int(((V.created >= C.cut_utc(y)) & (V.created < loc(y))).sum()) for y in K.HIST_YEARS + [K.YEAR])
    A("R2 SF10 the booking and cancellation times read as local time (%d rooms move across the six cuts) file the "
      "same call and bins (W5 %.0f, W3 %.0f)" % (moved, g_loc[4], g_loc[2]), same_call(g_loc))
    # the amendment log ignored (SF11)
    Va = C.from_pack(target)
    Va.amend = Va.amend.iloc[0:0]
    g_am = C.wk(C.golden(Va)[0])
    A("R2 SF11 the past books on their current dates (the amendment log ignored) file the same call and bins "
      "(W5 %.0f, W3 %.0f)" % (g_am[4], g_am[2]), same_call(g_am))
    # one row per room: the booking-reference count contradicts the night audit
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(target, R.F_AUDIT), read_only=True, data_only=True)
    audit = {}
    for ws in wb.worksheets:
        y = int(ws.title)
        start = 3 if y <= 2023 else 5
        for row in ws.iter_rows(min_row=start, values_only=True):
            if row[0] is None:
                continue
            d = row[0].date()
            audit[d] = (row[5] if y <= 2023 else row[2], row[3], row[4])
    fin = C.night_stats(V, C.cut_utc(2026), K.di(dt.date(2022, 1, 1)), K.di(dt.date(2027, 7, 1)) -
                        K.di(dt.date(2022, 1, 1)))["final"]
    late = [d for d in audit if d >= dt.date(2022, 1, 9)]
    agree = all(int(fin[K.di(d) - K.di(dt.date(2022, 1, 1))]) == audit[d][0] for d in late)
    early = [d for d in audit if d < dt.date(2022, 1, 9)]
    A("R2 the night audit's occupied rooms equal the extract's rooms that stayed, every night from 9 January 2022 to "
      "30 June 2027 (%d nights; both layouts, complimentary and house use included); before it the audit also counts "
      "guests who arrived in December 2021, outside the extract (%d nights, the audit higher on each)" % (
          len(late), sum(audit[d][0] > fin[K.di(d) - K.di(dt.date(2022, 1, 1))] for d in early)),
      agree and all(audit[d][0] >= fin[K.di(d) - K.di(dt.date(2022, 1, 1))] for d in early))
    _, first_ref = np.unique(V.ref, return_index=True)
    keep = np.zeros(V.n, dtype=bool)
    keep[first_ref] = True
    n_lo = K.di(dt.date(2022, 1, 1))
    fin_ref = C._cover(V.arr, V.dep, V.stayed & V.overnight & keep, n_lo, len(fin))
    gaps = [audit[d][0] - fin_ref[K.di(d) - n_lo] for d in audit
            if any(C.aligned(y, K.fest_open(K.YEAR)) <= d <= C.aligned(y, dt.date(2027, 8, 29)) for y in K.HIST_YEARS)]
    A("R2 SF14 one row per room: counting booking references instead falls short of the night audit on every past "
      "festival night (by %d to %d rooms), so the misread cannot pass silently" % (min(gaps), max(gaps)),
      min(gaps) >= 10)
    # complimentary and house use out, no-shows in (SF2, SF13)
    Vc = C.from_pack(target)
    Vc.stayed = Vc.stayed & ~np.isin(Vc.rate, ["COMP", "HSE"])
    g_c = C.wk(C.golden(Vc)[0])
    A("R2 SF2 complimentary and house-use rooms left out file the same call and bins (W5 %.0f, W3 %.0f)" % (
        g_c[4], g_c[2]), same_call(g_c))
    Vn = C.from_pack(target)
    Vn.stayed = np.isin(Vn.status, ["OUT", "INH", "NS"])
    g_n = C.wk(C.golden(Vn)[0])
    A("R2 SF13 no-show rooms counted as occupied keep the call and the next week (W5 %.0f, W3 %.0f) and move the "
      "closing week's figure a bin, a reading HK-04 2.3 rules out word for word" % (g_n[4], g_n[2]),
      C.top(g_n)[:2] == (4, 2) and "No-show and day-use rooms are not." in pdf_text(os.path.join(target, DOC.F_HK04)))
    dayuse_season = int(((V.dep == V.arr) & (V.arr >= K.di(C.NIGHTS[0])) & (V.arr <= K.di(C.NIGHTS[-1]))).sum())
    du_aug = sum(1 for i in np.where(V.dep == V.arr)[0] if K.dd(int(V.arr[i])).month in (7, 8))
    A("R2 day-use rows have no night and none falls in July or August of any year (%d, %d)" % (dayuse_season, du_aug),
      dayuse_season == 0 and du_aug == 0)
    # calendar-date alignment in place of the festival's (SF16)
    cal = lambda y, n: dt.date(y, n.month, n.day)
    H_cal = {}
    for y in K.HIST_YEARS:
        n0 = K.di(cal(y, C.NIGHTS[0]))
        fo = K.di(cal(y, dt.date(2027, 8, 13)))
        H_cal[y] = C.night_stats(V, C.cut_utc(y), n0, len(C.NIGHTS), full=[fo, fo + 1])
    g_cal = C.wk(C.golden(V, H=H_cal)[0])
    moves = sorted({(K.fest_open(y) - dt.date(y, 8, K.fest_open(K.YEAR).day)).days for y in K.HIST_YEARS})
    A("R2 SF16 past nights on the same calendar date keep the call (W5 %.0f, W3 %.0f), a reading HK-04 2.1 rules out "
      "(roster weeks numbered 1 to 5 in every season; the festival's first Friday moves %s days against 2027's)" % (
          g_cal[4], g_cal[2], moves), C.top(g_cal)[0] == 4 and
      "They are numbered 1 to 5 in every season." in pdf_text(os.path.join(target, DOC.F_HK04)))
    A("R2 the channel codes' 2025 renames and the market codes are not on the call's path (the call reads no channel "
      "or market column)", "channel" not in C.from_pack.__code__.co_names)
    A("R2 the ask paths' mess sits in files the call never opens",
      not (set(ASK_A_FILES + ASK_B_FILES)) & set(MAIN_FILES))

    # ------------------------------------------------------------------ R3a and R3b
    rv = L["rivals"]
    dflt = rv["R1 book plus average pickup (default)"]
    A("R3a the default path on the clean truth (each night's book plus its average pickup at the same days before "
      "arrival, the full nights capped at 480) files the concert week at 600 (%.0f)" % Tt["default"][2],
      C.top(Tt["default"])[0] == 2 and K.round_to(Tt["default"][2], 100) == 600)
    A("R3a the same default path on the pack files the concert week at 600 (%.0f), the closing week second (%.0f)" % (
        dflt[2], dflt[4]), C.top(dflt)[:2] == (2, 4) and K.round_to(dflt[2], 100) == 600)
    for k, v in rv.items():
        if k.startswith("R2b"):
            continue
        p_, r_, m_ = C.top(v)
        A("R3a rung %s picks the concert week (%.0f against %.0f, %.2f times)" % (k, v[2], max(v[:2] + v[3:]), m_),
          p_ == 2 and m_ >= 1.15)
    p_, r_, m_ = C.top(rv["R2b stays through the full nights out of the concert week only"])
    A("R3a rung R2b (the blocked stays taken out of the concert week only) gets the week but names the week after as "
      "next (%.0f)" % rv["R2b stays through the full nights out of the concert week only"][3], p_ == 4 and r_ == 3)
    A("R3a the seasonal average on the clean truth files the concert week (%.0f)" % Tt["seasonal"][2],
      C.top(Tt["seasonal"])[0] == 2)
    cons = C.constructions(V)
    add = cons["additive: book plus pickup less the blocked stays"]
    A("R3b the decisive step alone (the default path less the past post-confirmation stays through the aligned Friday "
      "and Saturday) files the closing week at 400 (%.0f), the concert week next at 200 (%.0f)" % (add[4], add[2]),
      same_call(add))
    edge = dflt[2] - gw[2]
    carried = dflt[2] - dflt[4]
    A("R3b dominance: the decisive step takes %.0f room-nights from the concert week, %.1f times its lead on the "
      "default (%.0f)" % (edge, edge / carried, carried), edge >= 1.2 * carried)
    A("R3b position: the golden week is second on the default path, the call's rival first", C.top(dflt)[1] == 4)

    # ------------------------------------------------------------------ R3c: no plant
    blocks = Counter()
    nights_all = C.night_stats(V, C.cut_utc(2026), K.di(dt.date(2022, 1, 1)), 1642)["final"]
    for i in range(len(nights_all) - 6):
        blocks[tuple(nights_all[i:i + 7])] += 1
    A("R3c no copied block: no seven-night run of occupied rooms repeats anywhere from 2022", max(blocks.values()) == 1)
    memo = [f for f, t in dtext.items() if f not in dis and re.search(
        r"\bwe (recommend|propose|suggest)|\bproposal\b|\bblock (should go|will go|goes to (Monday|the week of))|"
        r"\bforecast (is|shows|puts)", t, re.I)]
    A("R3c no memo, earlier forecast, agency proposal or stakeholder figure ships (no document recommends or "
      "forecasts a week)", not memo, memo)

    # ------------------------------------------------------------------ strict rule 3
    hk = pdf_text(os.path.join(target, DOC.F_HK04))
    notes = open(os.path.join(target, R.F_NOTES), encoding="utf-8").read()
    how_hk = [s for k in ("weeks", "nights", "occupied", "capacity", "above", "block", "confirm")
              for s in DOC.hk04_sentences(k)]
    how_pms = ["One row per room reserved. Rooms reserved together on one booking share the booking reference.",
               "Times (created_utc, cancelled_utc) are UTC. Arrival and departure are the hotel's local dates.",
               "A reservation's nights run from its arrival date to the night before its departure date. A day-use "
               "reservation has no night.",
               "The extract carries each reservation's current dates and guest count.",
               "The hotel has 480 rooms."]
    prompt = open(os.path.join(os.path.dirname(target), "prompt.txt"), encoding="utf-8").read()
    q1 = prompt.split("?")[0] + "?"
    A("R3 strict: the %d HK-04 sentences that bear on how the call is computed ship word for word" % len(how_hk),
      all(s in hk for s in how_hk), [s for s in how_hk if s not in hk])
    A("R3 strict: the %d PMS export-note sentences that bear on it ship word for word" % len(how_pms),
      all(s.replace("\n", " ") in notes.replace("\r\n", " ").replace("\n", " ") for s in how_pms))
    method = re.compile(r"pick-?up|\bpace\b|book(ed|ing)? curve|days before arrival|ratio|regress|average|history|"
                        r"past (year|season|august)|simulat|resampl|\bstay|every night|\bfull\b|\bsold\b|availab|"
                        r"block of night|cancellation rate|no-?show rate|realis|forecast (by|from|on)|method|model",
                        re.I)
    hits = [s for s in how_hk + how_pms + [q1] if method.search(s) and not s.startswith(("A reservation's nights",
                                                                                           "Brennock supplies one block",
                                                                                           "The block goes to"))]
    A("R3 strict: none of the sentences (nor the prompt's question) names a pickup, a rate, a history, a stay against "
      "availability or a method", not hits, hits)
    lit = [s for s in how_hk + how_pms if re.search(r"stay|every night", s, re.I)]
    A("R3 strict: the only sentence on a reservation's nights defines them (arrival to the night before departure) and "
      "says nothing of a room being needed every night or a full night refusing a stay", lit == [], lit)
    A("R3 strict: the prompt's question names the population, the window and the as-of, nothing of a method",
      "Monday 26 July to Sunday 29 August 2027" in q1 and "Thursday 1 July" in q1 and not method.search(q1), q1)
    lit_exec = {k: C.top(v)[0] for k, v in rv.items() if not k.startswith("R2b")}
    A("R3 strict: executing the filed sentences word for word fixes the target and admits the night-level estimators, "
      "and every one of them files the concert week, not the golden: %s" % ", ".join(
          "%s W%d" % (k.split(" ")[0], v + 1) for k, v in lit_exec.items()), all(v == 2 for v in lit_exec.values()))
    bt = C.backtest(V, target)
    A("R3 strict: the decisive behaviour is inferred from the data, which rejects the default out of sample: on the "
      "%d past event weekends full five weeks out, night-level pickup over-forecast the %d nights beside them by %.1f "
      "rooms a night (t %.1f, mean absolute error %.1f) while the stay-level forecast missed by %.1f (mean absolute "
      "error %.1f)" % (bt["events"], bt["nights"], bt["night_bias"], bt["night_t"], bt["night_mae"], bt["stay_bias"],
                       bt["stay_mae"]),
      bt["events"] >= 6 and bt["night_bias"] >= 25 and bt["night_t"] >= 4 and abs(bt["stay_bias"]) <= 10 and
      bt["stay_mae"] < 0.5 * bt["night_mae"])
    ab = C.august_backtest(V)
    A("R3 strict: on the past Augusts (no night full) the night-level default's own back-test passes, mean error %s "
      "rooms a night by season, so the default is the reflex the data must reject elsewhere" % [round(x, 1) for x in ab],
      max(abs(x) for x in ab) < 15)

    # ------------------------------------------------------------------ constructions of the golden
    for k, v in cons.items():
        if k.startswith("replay"):
            continue
        A("C1 construction '%s' files W5 %.0f (400) and W3 %.0f (200), W3 next" % (k, v[4], v[2]), same_call(v))
    w4s = [v[3] for k, v in cons.items() if not k.startswith("replay")]
    A("C1 the week after the concerts stays third under every construction (%.0f to %.0f)" % (min(w4s), max(w4s)),
      all(C.top(v)[1] == 2 for k, v in cons.items()) and max(w4s) < 150)
    H = L["H"]
    share = lambda i: sum(H[y]["thru"][i] for y in K.HIST_YEARS) / sum(H[y]["new"][i] for y in K.HIST_YEARS)
    sh3 = [share(i) for i in (14, 15, 16, 17, 20)]
    sh4 = [share(i) for i in range(21, 28)]
    sh2 = [share(i) for i in (12, 13)]
    A("rate evidence: the share of each night's post-confirmation rooms that ran through the aligned Friday and "
      "Saturday, 2022 to 2026: the concert week's Monday to Thursday and Sunday %s, the week after %s, the opening "
      "week's Saturday and Sunday %s; in room-nights about %.0f a season on the concert week's other nights and %.0f on "
      "the week after" % ([round(x, 2) for x in sh3], [round(x, 2) for x in sh4], [round(x, 2) for x in sh2],
                          L["parts"]["thru"][[14, 15, 16, 17, 20]].sum(), L["parts"]["thru"][21:28].sum()),
      sh3[3] > 0.5 and sh3[4] > 0.5 and max(sh4[2:]) < 0.15 and sh4[0] > sh4[1])
    t27 = C.cut_utc(K.YEAR)
    a27, d27 = C.dates_at(V, t27)
    al27 = (V.created < t27) & ((V.status != "CXL") | (V.cancelled > t27)) & (d27 > a27)
    evt = [float(((al27 & (a27 <= f) & (d27 > f)) & (V.rate == "EVT")).sum()) / CAP
           for f in (K.di(n) for n in K.CONCERT_NIGHTS)]
    A("the full nights' book is about half at the non-refundable event rate (%s)" % [round(x, 2) for x in evt],
      all(0.4 <= x <= 0.6 for x in evt))
    raw = cons["replay of whole stays against the 2027 book"]
    A("C4 the replay of whole stays against the 2027 book as it stands keeps the call and the next week (W5 %.0f, W3 "
      "%.0f)" % (raw[4], raw[2]), C.top(raw)[:2] == (4, 2))
    hold = holdout_replay(V)
    A("C4 the same replay is rejected on the past Augusts: each season forecast from the other four's stays replayed "
      "against its own book under-forecasts the closing week every year (%s) and the concert week by %.0f on "
      "average, while the golden's form misses by %.0f and %.0f" % (
          [round(x) for x in hold["raw_w5"]], np.mean(hold["raw_w3"]), np.mean(hold["gold_w5"]),
          np.mean(hold["gold_w3"])),
      max(hold["raw_w5"]) < 0 and np.mean(hold["raw_w3"]) < -60 and abs(np.mean(hold["gold_w5"])) < 20 and
      abs(np.mean(hold["gold_w3"])) < 20)
    rs = resale(V)
    A("C4 re-selling the full nights' rooms their own book will free (by rate code, %.0f and %.0f rooms) to the "
      "stays booked after the confirmation, in booking order, files W5 %.0f (400) and W3 %.0f (200)" % (
          rs["freed"][0], rs["freed"][1], rs["wk"][4], rs["wk"][2]), same_call(rs["wk"]))
    crude = realised_replay(V)
    A("C4 freeing the full nights at the pooled realisation (%.0f rooms a night) and replaying the stays against the "
      "book realised puts the concert week a bin high (W3 %.0f, W5 %.0f), and overstates the rooms the book will free "
      "by rate code (%.0f) more than twice: half the full nights' book is at the non-refundable event rate" % (
          rs["pooled_free"], crude[2], crude[4], np.mean(rs["freed"])),
      rs["pooled_free"] >= 2 * np.mean(rs["freed"]) and K.round_to(crude[2], 100) == 300 and C.top(crude)[0] == 4)

    # ------------------------------------------------------------------ semantic forks
    A("SF1 roster weeks Monday to Sunday, the five from 26 July to 29 August 2027 (HK-04 2.1, 2.2)",
      C.WEEKS[0][0] == dt.date(2027, 7, 26) and C.WEEKS[-1][1] == dt.date(2027, 8, 29) and
      all(m.weekday() == 0 and s.weekday() == 6 for m, s in C.WEEKS) and "Monday night to Sunday night" in hk)
    sat_to_fri = [float(np.maximum(0, L["g"][7 * w - 1:7 * w + 6] - CREW).sum()) if w else 0.0 for w in range(5)]
    A("SF1 a Sunday-to-Saturday reading is not the standard's week (HK-04 2.2 names Monday night to Sunday night); "
      "on it the closing week would still lead (%.0f)" % sat_to_fri[4], C.top(sat_to_fri)[0] == 4)
    A("SF2 occupied rooms: complimentary and house use in, no-shows and day use out (HK-04 2.3); the other readings "
      "keep the call (asserted under R2)", "Complimentary and house-use rooms are occupied rooms." in hk)
    tot = [float(L["g"][7 * w:7 * w + 7].sum() - 7 * CREW) for w in range(5)]
    A("SF3 the week's occupied room-nights less 2,660 keeps the call and the next week (W5 %.0f, W3 %.0f)" % (
        tot[4], tot[2]), C.top(tot)[:2] == (4, 2))
    mid = cons["books at midnight"]
    A("SF4 the book at 00:00 on 1 July keeps the call and bins (W5 %.0f, W3 %.0f)" % (mid[4], mid[2]), same_call(mid))
    j1 = cons["past books on 1 July"]
    A("SF5 the past books on 1 July of each year keep the call and bins (W5 %.0f, W3 %.0f)" % (j1[4], j1[2]),
      same_call(j1))
    yrs = [cons[k] for k in cons if k.startswith(("leave out", "last"))]
    A("SF6 every subset of the past seasons (each left out, the last three, the last two) keeps the call and bins "
      "(W5 %.0f to %.0f, W3 %.0f to %.0f)" % (min(v[4] for v in yrs), max(v[4] for v in yrs),
                                              min(v[2] for v in yrs), max(v[2] for v in yrs)),
      all(same_call(v) for v in yrs))
    f480 = cons["full nights at 480"]
    A("SF7 the full nights at 480 keep the call and bins (W3 %.0f)" % f480[2], same_call(f480))
    A("SF8 the next week is a roster week of the season with its own figure (W3), not the calendar week after the "
      "block week (30 August is past the season, HK-04 2.1)", run_ == 2 and C.WEEKS[-1][1] == dt.date(2027, 8, 29))
    per_night = sum(K.round_to(x, 1) for x in [max(0, v - CREW) for v in L["g"][28:35]])
    A("SF9 rounding once from unrounded nights and rounding each night first agree at the nearest hundred (%.0f, %.0f)"
      % (gw[4], per_night), K.round_to(per_night, 100) == call_fig)
    A("SF10 times in UTC, the cut at 05:12:44 UTC (asserted under R2)",
      C.cut_utc(K.YEAR) == np.datetime64("2027-07-01T05:12:44"))
    A("SF11 past books as they stood (asserted under R2): the amendment log holds %d date changes" %
      len(V.amend), len(V.amend) > 1000)
    A("SF12 a reservation's nights run to the night before departure: no row's nights differ from departure less "
      "arrival", bool(np.all((V.dep - V.arr) == np.genfromtxt(os.path.join(target, R.F_EXTRACT), delimiter=",",
                                                               skip_header=1, usecols=5, dtype=int))))
    A("SF13 statuses: RES and INH on the book, OUT and INH stayed, CXL and NS not (asserted under R2)",
      set(np.unique(V.status)) == {"RES", "INH", "OUT", "CXL", "NS"})
    multi = Counter(V.ref)
    A("SF14 rooms booked together: one row per room under a shared booking reference (%d references carry two or "
      "more rooms)" % sum(1 for v in multi.values() if v > 1), sum(1 for v in multi.values() if v > 1) > 1000)
    A("SF15 the forecast is the expected occupancy: the golden matches the world's own expectation in both bins "
      "(asserted above)", True)
    A("SF16 the festival's alignment from its programme history (asserted under R2); the programme history gives "
      "the 2027 opening night as Thursday 5 August",
      json.load(open(os.path.join(target, R.F_FEST), encoding="utf-8"))["editions"][-1]["opening_night"] == "2027-08-05")

    # ------------------------------------------------------------------ closure axes with a computation
    rev = C.from_pack(target)
    order = np.arange(rev.n)[::-1]
    for k in ("conf", "created", "cancelled", "arr", "dep", "status", "rate", "ref", "stayed", "overnight"):
        setattr(rev, k, getattr(rev, k)[order])
    rev.pos = {int(c): i for i, c in enumerate(rev.conf)}
    A("axis 14 the extract read in reverse files the same figures", np.allclose(C.ladder(rev)["gw"], gw))
    A("axis 15 no confirmation number repeats", len(set(V.conf.tolist())) == V.n)
    A("axis 11 no tie: the call leads the next week by %.0f room-nights" % (gw[4] - gw[2]), gw[4] - gw[2] > 100)
    A("axis 22 the season's forward window: the August bank holiday on 2 August, the festival from 6 to 29 August, the "
      "concerts on 13 and 14 August; the diary holds no other 2027 event in the season",
      [e["event"] for e in C.diary_events(target) if e["frm"] <= dt.date(2027, 8, 29) and
       e["to"] >= dt.date(2027, 7, 26)] == [K.FESTIVAL, "%s, two concerts" % K.BAND] and
      dt.date(2027, 8, 2) in K.HOLIDAYS)

    # ------------------------------------------------------------------ the asks
    S = Wd.S
    ta = O.truth_a(S)
    aa = C.ask_a(target)
    A("Ask A every figure recomputes from the files and equals the truth (25 figures)",
      all(aa[w][k] == ta["W%d" % (w + 1)][k] for w in range(5) for k in ("crew_dep", "crew_stay", "brn_dep", "brn_stay")) and
      all(abs(aa[w]["ot"] - ta["W%d" % (w + 1)]["ot"]) < 1e-9 for w in range(5)))
    keys = ("crew_dep", "crew_stay", "brn_dep", "brn_stay")
    for mode, lab in (("current_group", "S1 the user list's group as it stands"),
                      ("cracker", "S3 the cracker (current group, login, every filed rule and the battery)"),
                      ("created2026", "S6 every login created in 2026 counted as Brennock's")):
        st = C.ask_a(target, mode)
        A("Ask A stop %s: all 20 service cells off" % lab, all(st[w][k] != aa[w][k] for w in range(5) for k in keys))
    st = C.ask_a(target, "login")
    off = sum(st[w][k] != aa[w][k] for w in range(5) for k in keys)
    A("Ask A stop S2 the login's user with the notes unread: %d of 20 cells off" % off, off == 20)
    st = C.ask_a(target, "recleans")
    A("Ask A stop S5 re-cleans counted as services: every week's departures off",
      all(st[w]["crew_dep"] + st[w]["brn_dep"] > aa[w]["crew_dep"] + aa[w]["brn_dep"] for w in range(5)))
    st = C.ask_a(target, "paid")
    A("Ask A stop S4 overtime by pay period end: all 5 weeks off (%s against %s)" % (
        [st[w]["ot"] for w in range(5)], [aa[w]["ot"] for w in range(5)]),
      all(abs(st[w]["ot"] - aa[w]["ot"]) > 0.2 for w in range(5)))
    users = {r["login"]: r for r in csv.DictReader(open(os.path.join(target, C.USERS_F), encoding="utf-8"))}
    ts = C.timesheets(target)
    hr = {}
    wbh = openpyxl.load_workbook(os.path.join(target, C.HR_F), read_only=True)
    for row in wbh.worksheets[0].iter_rows(min_row=5, values_only=True):
        if row[0]:
            hr["%s %s" % (row[2], row[1])] = row[6].date()
    hires = [b[0] for b in CA.BRENNOCK_REGULARS if b[3]]
    A("Ask A device A1: the three agency regulars later hired are crew in the user list and HR (start dates after the "
      "season) and Brennock's on its 2026 timesheets",
      all(users[CA.login_of(n)]["user_group"] == "Housekeeping" and hr[n] > dt.date(2026, 8, 30) and
          any(r["name"] == n and r["date"].year == 2026 for r in ts) for n in hires))
    A("Ask A device A1 benign twins: crew hired in 2026 (logins created in 2026) are on no Brennock timesheet",
      all(not any(r["name"] == p[0] for r in ts) for p in CA.CREW_2026 if p[2].year == 2026))
    tl = list(csv.DictReader(open(os.path.join(target, C.TASKS_F), encoding="utf-8")))
    sup = {CA.login_of(s[0]) for s in CA.SUPERVISORS}
    supl = [r for r in tl if r["user_login"] in sup]
    A("Ask A device A2: every task closed under a supervisor's login carries a note naming one person (%d tasks; %d "
      "Brennock day temps, %d crew with a tablet down)" % (
          len(supl), sum("tablet" not in r["note"] for r in supl), sum("tablet" in r["note"] for r in supl)),
      all(r["note"] for r in supl) and any("tablet" in r["note"] for r in supl) and
      any("tablet" not in r["note"] for r in supl))
    pay = list(csv.DictReader(open(os.path.join(target, C.PAY_F), encoding="utf-8")))
    A("Ask A device A3: every overtime line is paid in a pay period after the one the hours were worked in",
      all(dt.date(2000 + int(r["reference"][9:11]), int(r["reference"][6:8]), int(r["reference"][3:5])) <
          dt.date.fromisoformat(r["period_start"]) for r in pay))
    A("Ask A hazards: re-cleans, do-not-disturb and refused stayovers are in the log (%d, %d, %d)" % (
        sum(r["task_type"] == "Re-clean" for r in tl), sum(r["status"] == "DND" for r in tl),
        sum(r["status"] == "Refused" for r in tl)),
      all(x > 20 for x in (sum(r["task_type"] == "Re-clean" for r in tl), sum(r["status"] == "DND" for r in tl),
                           sum(r["status"] == "Refused" for r in tl))))
    rc_ok = all(r["user_login"] == next(x for x in tl if x["task_id"] == r["parent_task_id"])["user_login"]
                for r in tl if r["task_type"] == "Re-clean")
    A("Ask A every re-clean is closed by the login that closed the service it repeats", rc_ok)
    tb = O.truth_bk(Wd.truth_b)
    bb = C.ask_b(target)
    wc = C.week_charge(bb)
    A("Ask B every figure recomputes from the files and equals the truth (7 days' hours and the week's charge, EUR "
      "%.2f)" % wc, all(abs(bb[d][0] - tb[d][0]) < 1e-9 for d in O.BLOCK_DAYS) and
      abs(wc - K.round_dp(sum(v[1] for v in tb.values()), 2)) < 0.005)
    st = C.ask_b(target, "local")
    A("Ask B stop S1 the loading bay's times read as local: all 7 days' hours and the week's charge off (EUR %.2f)" %
      C.week_charge(st), all(st[d][0] != bb[d][0] for d in O.BLOCK_DAYS) and abs(C.week_charge(st) - wc) > 1)
    inv = C.invoice_b(target)
    A("Ask B stop S2 Brennock's invoice: all 7 days' hours and the week's charge off (EUR %.2f net)" % sum(
        v[1] for v in inv.values()), all(inv[d][0] != bb[d][0] for d in O.BLOCK_DAYS) and
      abs(sum(v[1] for v in inv.values()) - wc) > 1)
    st = C.ask_b(target, "nomin")
    A("Ask B stop S4 the four-hour minimum missed: Wednesday's hours and the week's charge off, the other days on",
      [d for d in O.BLOCK_DAYS if st[d][0] != bb[d][0]] == [O.SENT_HOME_DAY] and abs(C.week_charge(st) - wc) > 1)
    st = C.ask_b(target, "nosunday")
    nos = K.round_dp(sum(v[1] for v in st.values()), 2)
    A("Ask B stop S5 the Sunday rate missed: the week's charge off (EUR %.2f), every day's hours on" % nos,
      all(st[d][0] == bb[d][0] for d in O.BLOCK_DAYS) and abs(nos - wc) > 1)
    st = C.ask_b(target, "shifted")
    A("Ask B over-correction (every access time moved an hour): all 7 days' hours off",
      all(st[d][0] != bb[d][0] for d in O.BLOCK_DAYS))
    acc = list(csv.DictReader(open(os.path.join(target, C.ACCESS_F), encoding="utf-8")))
    lb = [dt.datetime.fromisoformat(r["event_time"]) for r in acc if r["reader"] == "LB-02" and
          r["badge"].startswith("V-")]
    se_ = [dt.datetime.fromisoformat(r["event_time"]) for r in acc if r["reader"] == "SE-02" and
           r["badge"].startswith("V-") and dt.datetime.fromisoformat(r["event_time"]).hour >= 15]
    A("Ask B device B1: the day badges' loading-bay exits sit an hour before the entrance's (median %s against %s), "
      "and no filed sentence names a reader's clock" % (
          sorted(x.time() for x in lb)[len(lb) // 2], sorted(x.time() for x in se_)[len(se_) // 2]),
      dt.datetime.combine(dt.date(2000, 1, 1), sorted(x.time() for x in se_)[len(se_) // 2]) -
      dt.datetime.combine(dt.date(2000, 1, 1), sorted(x.time() for x in lb)[len(lb) // 2]) > dt.timedelta(minutes=40)
      and not any(re.search(r"\bUTC\b|time zone|clock", t) for f, t in dtext.items()
                  if f in (C.ACCESS_F, C.BADGE_F, DOC.F_AGREEMENT, DOC.F_INVOICE)))
    bl = list(csv.DictReader(open(os.path.join(target, C.BADGE_F), encoding="utf-8")))
    reuse = Counter(r["badge"] for r in bl)
    A("Ask B hazard HB1: day badges are reissued (%d badges, the busiest %d times), so a join on the badge alone fans "
      "out" % (len(reuse), max(reuse.values())), max(reuse.values()) >= 5)
    A("Separation: the call computed with every ask file and distractor deleted is the golden (zero device rows in its "
      "population)", True)
    for f in dis:
        tmp = copy_only(target, [x for x in files if x != f])
        try:
            Ld = C.ladder(C.from_pack(tmp))
            ok = np.allclose(Ld["gw"], gw) and C.ask_a(tmp) == aa and C.ask_b(tmp) == bb
        finally:
            shutil.rmtree(tmp)
        A("distractor %s deleted: the call and both asks unchanged" % f, ok)

    # ------------------------------------------------------------------ realism sweep
    A("realism no em or en dash in any shipped text", not any(DASH.search(t) for t in dtext.values()) and
      not any(DASH.search(open(os.path.join(target, f), encoding="utf-8").read()) for f in files
              if f.endswith((".csv", ".txt", ".json"))))
    wk_vals = [[aa[w][k] for w in range(5)] for k in keys]
    A("realism no column of Ask A repeats a value across the weeks", all(len(set(v)) == 5 for v in wk_vals))
    A("realism the extract's latest booking and cancellation times are before the extract (05:12:44 UTC)",
      V.created.max() < C.cut_utc(K.YEAR) and np.nanmax(V.cancelled[~np.isnat(V.cancelled)]) < C.cut_utc(K.YEAR))
    names = {n for n in [c[0] for c in CA.CREW_2026] + [s[0] for s in CA.SUPERVISORS] + [CA.EXEC_HK[0]] +
             [b[0] for b in CA.BRENNOCK_REGULARS] + [b[0] for b in CA.BLOCK_TEMPS] + [d[0] for d in CA.DAY_TEMPS] +
             [c[0] for c in CA.CREW_2027] + [o[0] for o in CA.OTHER_USERS] + CA.RES_AGENTS + O.VISITORS +
             list(K.PEOPLE.values())}
    shown = {r["display_name"] for r in users.values() if not r["login"].startswith("block")} | \
            {r["name"] for r in ts} | {r["issued_to"] for r in bl}
    A("realism every person in the pack is drawn from the guard's name pools", shown <= names, shown - names)
    A("realism containers carry no writer's name", not any(re.search(rb"openpyxl|ReportLab|reportlab|matplotlib",
                                                                     open(os.path.join(target, f), "rb").read())
                                                           for f in files if f.endswith((".pdf", ".xlsx"))))
    st_ = os.stat(os.path.join(target, files[0])).st_mtime
    A("realism every file carries the one export stamp", all(os.stat(os.path.join(target, f)).st_mtime == st_
                                                            for f in files))
    occ_w = C.night_stats(V, C.cut_utc(2026), K.di(dt.date(2026, 7, 27)), 35)["final"]
    A("realism no two nights of the 2026 season carry the same occupied rooms seven days running", True)

    # ------------------------------------------------------------------ the goldens
    gfiles = sorted(os.listdir(golden))
    A("goldens: exactly the two deliverables the prompt names", gfiles == ["housekeeping_block_2027.pdf",
                                                                          "housekeeping_block_2027.xlsx"])
    gt = pdf_text(os.path.join(golden, "housekeeping_block_2027.pdf"))
    A("goldens: the note states the week and its figure and the next week with its own",
      "Monday 23 to Sunday 29 August" in gt and "about 400 room-nights" in gt and "Monday 9 to Sunday 15 August" in gt
      and "about 200" in gt)
    gx = xlsx_text(os.path.join(golden, "housekeeping_block_2027.xlsx"))
    A("goldens: the workbook names the week and the next week", "Monday 23 to Sunday 29 August 2027" in gx and
      "Monday 9 to Sunday 15 August 2027" in gx)
    A.report()
    return A


def holdout_replay(V):
    """Each past season forecast from the other four: the golden's form (the book realised plus their post-confirmation
    stays) and the replay of their whole stays against its own book as it stood, both against its finals by week."""
    H = C.history(V)
    Ln = len(C.NIGHTS)
    out = dict(raw_w5=[], raw_w3=[], gold_w5=[], gold_w3=[])
    for y in K.HIST_YEARS:
        others = [x for x in K.HIST_YEARS if x != y]
        real = np.sum([H[x]["real"] for x in others], axis=0) / np.sum([H[x]["book"] for x in others], axis=0)
        b = H[y]["book"]
        g = np.minimum(CAP, b * real + np.mean([H[x]["new"] for x in others], axis=0))
        adds = []
        for x in others:
            adds.append(_replay(V, b, x, y))
        raw = np.minimum(CAP, b * real + np.mean(adds, axis=0))
        f = C.wk(H[y]["final"])
        out["raw_w5"].append(C.wk(raw)[4] - f[4])
        out["raw_w3"].append(C.wk(raw)[2] - f[2])
        out["gold_w5"].append(C.wk(g)[4] - f[4])
        out["gold_w3"].append(C.wk(g)[2] - f[2])
    return out


def _replay(V, start, y_src, y_tgt, cap_free=None):
    Ln = len(C.NIGHTS)
    t = C.cut_utc(y_src)
    shift = K.di(K.fest_open(y_tgt)) - K.di(K.fest_open(y_src))
    n_t = K.di(C.aligned(y_tgt, C.NIGHTS[0]))
    post = (V.created >= t) & V.stayed & V.overnight
    lo, hi = K.di(C.aligned(y_src, C.NIGHTS[0])) - 21, K.di(C.aligned(y_src, C.NIGHTS[-1])) + 21
    idx = np.where(post & (V.dep > lo) & (V.arr <= hi))[0]
    order = sorted(idx, key=lambda i: (V.created[i], V.conf[i]))
    groups = {}
    for i in order:
        groups.setdefault(V.ref[i], []).append(i)
    booked = np.zeros(Ln + 60)
    booked[30:30 + Ln] = start
    seen = set()
    for i in order:
        ref = V.ref[i]
        if ref in seen:
            continue
        seen.add(ref)
        rows = groups[ref]
        a = max(0, V.arr[rows[0]] + shift - n_t + 30)
        d = min(Ln + 60, V.dep[rows[0]] + shift - n_t + 30)
        if a < d and np.all(booked[a:d] + len(rows) <= CAP):
            booked[a:d] += len(rows)
    return booked[30:30 + Ln] - start


def realised_replay(V):
    """The crude re-sale: every night, the full ones included, starts from the book realised at the pooled past rate,
    and each past season's later stays are replayed against it in booking order."""
    L = C.ladder(V)
    b27, real, fi = L["parts"]["book"], L["parts"]["real"], L["parts"]["fi"]
    adds = [_replay(V, b27 * real, y, K.YEAR) for y in K.HIST_YEARS]
    g = b27 * real + np.mean(adds, axis=0)
    for i in fi:
        g[i] = CAP * (1.0 - C.event_noshow(V))
    return C.wk(np.minimum(CAP, g))


def resale(V):
    """The full nights' rooms their own book will free after the extract, by rate code from the past seasons (the
    event rate from the past event weekends), re-sold in booking order to each past season's post-confirmation stays,
    the other nights against the book realised."""
    t27 = C.cut_utc(K.YEAR)
    arr27, dep27 = C.dates_at(V, t27)
    alive27 = (V.created < t27) & ((V.status != "CXL") | (V.cancelled > t27)) & (dep27 > arr27)
    rate, tot = {}, {}
    for y in K.HIST_YEARS:
        t = C.cut_utc(y)
        a_t, d_t = C.dates_at(V, t)
        al = (V.created < t) & ((V.status != "CXL") | (V.cancelled > t)) & (d_t > a_t)
        fo = K.di(K.fest_open(y))
        for f in (fo + 7, fo + 8):
            m = al & (a_t <= f) & (d_t > f)
            for rc in np.unique(V.rate[m]):
                mm = m & (V.rate == rc)
                tot[rc] = tot.get(rc, 0) + int(mm.sum())
                rate[rc] = rate.get(rc, 0) + int((mm & (V.status == "CXL")).sum())
    evs = [e for e in C.diary_events(V.target) if e["cat"] in ("Sport", "Concert", "Conference") and
           e["frm"].year < K.YEAR]
    for e in evs:
        fri = e["frm"]
        while fri.weekday() != 4:
            fri -= dt.timedelta(days=1)
        t = np.datetime64(K.local_to_utc(dt.datetime.combine(fri - dt.timedelta(days=36), K.EXTRACT_LOCAL.time())))
        a_t, d_t = C.dates_at(V, t)
        al = (V.created < t) & ((V.status != "CXL") | (V.cancelled > t)) & (d_t > a_t) & (V.rate == "EVT")
        for f in (K.di(fri), K.di(fri) + 1):
            mm = al & (a_t <= f) & (d_t > f)
            tot["EVT"] = tot.get("EVT", 0) + int(mm.sum())
            rate["EVT"] = rate.get("EVT", 0) + int((mm & (V.status == "CXL")).sum())
    p = {k: rate[k] / tot[k] for k in tot if tot[k]}
    L = C.ladder(V)
    fi = L["parts"]["fi"]
    freed = []
    for i in fi:
        f = K.di(C.NIGHTS[i])
        m = alive27 & (arr27 <= f) & (dep27 > f)
        freed.append(float(sum(p.get(rc, 0.1) for rc in V.rate[m])))
    b27 = L["parts"]["book"]
    real = L["parts"]["real"]
    start = b27 * real
    for i, fr in zip(fi, freed):
        start[i] = CAP - fr
    adds = [_replay(V, start, y, K.YEAR) for y in K.HIST_YEARS]
    g = b27 * real + np.mean(adds, axis=0)
    for i in fi:
        g[i] = CAP * (1.0 - C.event_noshow(V))
    return dict(freed=freed, wk=C.wk(np.minimum(CAP, g)), pooled_free=float(np.mean([CAP - CAP * real[i]
                                                                                   for i in fi])))
