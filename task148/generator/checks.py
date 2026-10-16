"""task148 checks, run on every build: the input gates, the realism sweep, the three rules on the clean truth (R1 to
R3c), the rule-3 sentence audit, every semantic fork (SF1 to SF24), the ladder and its separation, the golden's
defensible constructions and one sigma, the out-of-sample back-test, and the asks (goldens against the world's truth,
devices, stops, determinism, separation and the distractors)."""
from __future__ import annotations

import datetime as dt
import json
import math
import os
import re
import shutil
import sys
import tempfile
import zipfile

import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as CA           # noqa: E402
import common as K          # noqa: E402
import deliver as DL        # noqa: E402
import docs as DOC          # noqa: E402
import erlang as E          # noqa: E402
import geo as GEO           # noqa: E402
import levels as LV         # noqa: E402
import model as M           # noqa: E402
import records as R         # noqa: E402

TASK = os.path.dirname(HERE)
MAIN_FILES = [R.F_LEGACY, R.F_I3, R.F_ROSTER, R.F_FORECAST, DOC.F_SOP, DOC.F_BUDGET, DOC.F_README]
ASK_FILES = [R.F_CHE, R.F_BOUNDARY, R.F_DIRECTORY, R.F_CALLBACK]
FY28 = K.fy_months(2028)
STUMP_WORDS = ["erlang", "patience", "censor", "reneg", "queueing model", "hang-ups' own", "staffing model",
               "abandonment rate", "kaplan", "likelihood"]


class Ck:
    def __init__(self):
        self.n = 0
        self.fails = []

    def __call__(self, label, ok, detail=""):
        self.n += 1
        if not ok:
            self.fails.append("%s: %s" % (label, detail))
            print("FAIL  %s  %s" % (label, detail))
        else:
            print("ok    %s  %s" % (label, detail))

    def done(self):
        print("checks: %d assertions, %d failed" % (self.n, len(self.fails)))
        if self.fails:
            raise SystemExit("checks failed:\n" + "\n".join(self.fails))


def r0(x):
    return int(K.round_half_up(100.0 * x, 0))


def rounded(comp):
    return {ym: r0(v) for ym, v in comp.items()}


def fmt(comp):
    return " ".join("%.2f" % (100 * comp[ym]) for ym in FY28)


def same_call(comp, gold):
    return CA.short_months(comp) == CA.short_months(gold) and rounded(comp) == rounded(gold)


def run(target, golden, B=None, G=None, meta_path=None):
    ck = Ck()
    W, C, fc = B.W, G["C"], G["fc"]
    busy, pat, wab, nab = G["busy"], G["patience"], G["wab"], G["n_abandoned"]
    gold = G["gold"]
    want = [(2027, 7), (2027, 8), (2028, 6)]

    # ------------------------------------------------------------------------------------------------ input gates
    files = sorted(os.listdir(target))
    meta = json.load(open(meta_path))
    ck("gate files", len(files) >= 10, "%d files" % len(files))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ck("gate formats", len(fmts) >= 3, ", ".join(sorted(fmts)))
    big = max(x["rows"] or 0 for x in meta["files"])
    ck("gate 25,000 rows", big >= 25000, "%d rows in the largest file" % big)
    ck("gate distractors", len(meta["distractor_files"]) >= 2 and all(d in files for d in meta["distractor_files"]),
       ", ".join(meta["distractor_files"]))
    ck("gate no distractor in a file name", not any("distract" in f.lower() for f in files))

    # ------------------------------------------------------------------------------------------------ the golden
    ck("golden months below 90", CA.short_months(gold) == want, CA.label_set(CA.short_months(gold)))
    targets = {ym: LV.TARGET_INT[ym[1]] for ym in FY28}
    ck("golden figures are the design's targets", rounded(gold) == targets, fmt(gold))
    clear = min(0.5 - abs(100 * gold[ym] - LV.TARGET_INT[ym[1]]) for ym in FY28)
    ck("golden figures at least 0.37 from a rounding edge", clear >= 0.37, "least clearance %.3f" % clear)
    offs = sorted(round(100 * gold[ym] - LV.TARGET_INT[ym[1]], 2) for ym in FY28)
    ck("golden figures not all on whole numbers (the unrounded values spread inside their bins)",
       max(offs) - min(offs) > 0.15, " ".join("%+.2f" % x for x in offs))
    margin = min(abs(100 * gold[ym] - 90.0) for ym in FY28)
    ck("every month at least 0.9 from 90 (SF22)", margin >= 0.9, "nearest %.3f" % margin)

    # ------------------------------------------------------------------------------------------------ R1 raw material
    heads = open(os.path.join(target, R.F_LEGACY), encoding="utf-8").readline().strip().split(",")
    i3keys = set()
    with open(os.path.join(target, R.F_I3), encoding="utf-8") as fh:
        for k, line in enumerate(fh):
            i3keys |= set(json.loads(line).keys())
            if k > 4000:
                break
    bad = [h for h in heads + sorted(i3keys) if re.search(r"wait|patien|complian|abandon_rate|service_level|sla", h, re.I)]
    ck("R1 no shipped column holds a wait, a patience or a compliance figure", not bad, ", ".join(bad) or "none")
    ck("R1 the golden reads every 911 call's presentation and answer or hang-up", G["n_911"] > 400000,
       "%d calls, %d abandoned" % (G["n_911"], nab))

    # ------------------------------------------------------------------------------------------------ R3 on the clean truth
    tb = float(np.mean(W.busy[~W.ab]))
    easy = CA.fy2028(fc, tb, pat, model="C")
    ck("R3a the easy route (Erlang C, measured busy time, the board's forecast, four call-takers) files May to September",
       CA.short_months(easy) == [(2027, 7), (2027, 8), (2027, 9), (2028, 5), (2028, 6)],
       CA.label_set(CA.short_months(easy)) + "; July %.2f" % (100 * easy[(2027, 7)]))
    ck("R3a July under the easy route about 83", 82.5 <= 100 * easy[(2027, 7)] <= 84.5, "%.2f" % (100 * easy[(2027, 7)]))
    tp = float(np.sum(W.wait) / W.ab.sum())
    dec = CA.fy2028(fc, tb, tp)
    ck("R3b the decisive step alone (the queue with hang-ups, patience over every wait) files the golden",
       same_call(dec, gold), fmt(dec))
    tw = float(np.mean(W.wait[W.ab]))
    lower = {"R2 the hang-ups' own waits": CA.fy2028(fc, tb, tw),
             "R1b the analyst's own forecast (no Halvorsen move)": CA.fy2028(fc, tb, tp, use_halvorsen=False),
             "R0 with five call-takers": CA.fy2028(fc, tb, tp, model="C", c=5)}
    for k_, v in lower.items():
        ck("R3b %s stays off the golden's months" % k_, CA.short_months(v) != want, CA.label_set(CA.short_months(v)))
    ck("R3b the golden's patience is the world's within its sampling error", abs(pat / K.PATIENCE - 1) < 3.0 / math.sqrt(nab),
       "%.2f against %.1f" % (pat, K.PATIENCE))
    ck("R3b the golden's busy time is the world's within its sampling error", abs(busy / K.AHT - 1) < 0.005,
       "%.2f against %.1f" % (busy, K.AHT))
    texts = {f: open(os.path.join(target, f), encoding="utf-8").read().lower() for f in files
             if f.endswith((".md", ".geojson")) or f == R.F_DIRECTORY or f == R.F_MANIFEST}
    texts[DOC.F_SOP] = " ".join(DOC.sop_sentences()).lower()
    texts[DOC.F_BUDGET] = " ".join([r[0] + " " + r[3] for r in DOC.BUDGET_ROWS] + DOC.BUDGET_TEXT).lower()
    import forecast as FCM
    texts[R.F_FORECAST] = " ".join(FCM.READ_ME).lower()
    hits = [(f, w) for f, t in texts.items() for w in STUMP_WORDS if w in t]
    ck("R3c no plant: no document names a queueing model, a patience or a compliance forecast", not hits, str(hits))
    ck("R3c no staffing study, model output or prior compliance figure ships",
       not any(re.search(r"compliance (forecast|was|of \d)|\d+(\.\d)? ?per cent (answered|compliance)", t) for t in texts.values()))

    # ------------------------------------------------------------------------------------------------ rule-3 sentence audit
    how = DOC.sop_sentences("measure") + DOC.sop_sentences("positions") + DOC.sop_sentences("staffing")
    ck("rule 3 the HOW sentences name no queue, wait distribution or patience",
       not any(re.search(r"queue model|erlang|patience|hold on|wait time distribution", s, re.I) for s in how), "%d sentences" % len(how))
    admitted = {"Erlang C": easy, "Erlang A on the hang-ups' waits": lower["R2 the hang-ups' own waits"]}
    # the observed fiscal 2026 late-shift compliance (five call-takers), carried forward month by month
    loc_fy = G["loc_fy"]
    late = np.array([K.is_frisat_late(K.to_local(x)) for x in C.t])
    G["late_mask"] = late
    nm = np.array([K.night_of(K.to_local(x)).month for x in C.t])
    carried = {}
    for (y, m) in FY28:
        sel = C.is911 & late & (loc_fy == 2026) & (nm == m)
        ok15 = np.sum(sel & ~C.ab & (C.wait <= 15.0))
        ab5 = np.sum(sel & C.ab & (C.wait <= 5.0))
        carried[(y, m)] = ok15 / (sel.sum() - ab5)
    admitted["fiscal 2026 observed, carried forward"] = carried
    for k_, v in admitted.items():
        ck("rule 3 the admitted estimator '%s' files another set" % k_, CA.short_months(v) != want,
           CA.label_set(CA.short_months(v)))
    ck("rule 3 the filed sentences alone give no compliance figure (no number in the measure but the standard's)",
       set(re.findall(r"\d+", " ".join(DOC.sop_sentences("measure")))) <= {"3", "1", "2", "15", "5", "911"},
       ", ".join(sorted(set(re.findall(r"\d+", " ".join(DOC.sop_sentences("measure")))))))

    # ------------------------------------------------------------------------------------------------ semantic forks
    prompt = open(os.path.join(TASK, "prompt.txt"), encoding="utf-8").read()
    sop = " ".join(DOC.sop_sentences())
    ck("SF1 fiscal 2028 fixed by the prompt and SOP 2.10 section 1",
       "fiscal 2028, July 2027 to June 2028" in prompt and "runs from 1 July to 30 June" in sop)
    ck("the asks' calendar: quarters and months are local calendar dates (SOP 2.10 1.2)",
       "quarters starting on 1 July, 1 October, 1 January and 1 April" in sop and "local (Central) calendar dates" in sop)
    cal = {}
    mu, th = 3600.0 / busy, 3600.0 / pat
    for y, m in FY28:
        def lam_cal(dow, h, y=y, m=m):
            return fc[(y, m, dow, h)][0]
        num = den = 0.0
        for nd in K.late_nights(y, m):
            for hh in K.night_hours(nd):
                yy, mm = hh.year, hh.month
                key = (yy, mm, hh.weekday(), hh.hour) if (yy, mm, hh.weekday(), hh.hour) in fc else (y, m, hh.weekday(), hh.hour)
                lam = fc[key][0]
                st, a5 = E.erlang_a(lam, mu, th, 4)[:2]
                num += lam * st
                den += lam * (1 - a5)
        cal[(y, m)] = num / den
    wrong_cells = {}
    for y, m in FY28:
        cells = []
        for nd in K.late_nights(y, m):
            for hh in K.night_hours(nd):
                dow = nd.weekday() if hh.hour >= 22 else nd.weekday()      # the calendar Friday or Saturday for 00:00 too
                cells.append((dow, hh.hour))
        num = den = 0.0
        for dow, h in cells:
            lam = fc[(y, m, dow, h)][0]
            st, a5 = E.erlang_a(lam, mu, th, 4)[:2]
            num += lam * st
            den += lam * (1 - a5)
        wrong_cells[(y, m)] = num / den
    ck("SF2 the late shift's after-midnight hours are Saturday's and Sunday's; the calendar reading files another call",
       "Friday and Saturday late shift, 22:00 to 02:00" in prompt and not same_call(wrong_cells, gold)
       and any("nights starting Friday and Saturday" in r[0] for r in DOC.BUDGET_ROWS), fmt(wrong_cells))
    ck("SF3 each hour on its calendar month's forecast: same call", same_call(cal, gold), fmt(cal))
    ck("SF4 within 15 seconds inclusive or not: same call (the model is continuous)",
       abs(E.erlang_a(30.0, mu, th, 4, t=15.0 / 3600)[0] - E.erlang_a(30.0, mu, th, 4, t=(15.0 - 1e-9) / 3600)[0]) < 1e-9)
    zero = np.mean(C.wait[C.is911 & ~C.ab & (C.layout == "i3")] == 0.0)
    ck("SF5 presentation is the queue entry; an undelayed call is answered on presentation (auto-answer)",
       zero > 0.8 and "auto-answer" in sop, "%.1f%% of i3 answered calls with no wait" % (100 * zero))
    noex = CA.fy2028(fc, busy, pat, excl=False)
    ck("SF6 the denominator without the 5-second exclusion: same months (the figures ruled out by SOP 2.10 3.2 and 3.3)",
       CA.short_months(noex) == want, fmt(noex))
    ck("SF6 the exclusion is filed", "abandoned within 5 seconds of presentation is treated as a misdial" in sop)
    own = CA.fy2028(fc, busy, pat, use_halvorsen=False)
    ck("SF7 the analyst's own arrivals (no Halvorsen move) file another call, ruled out by SOP 2.10 section 5",
       CA.short_months(own) != want and "planned against the Tri-County Regional 911 Board's published hourly volume forecast" in sop,
       CA.label_set(CA.short_months(own)))
    ck("SF8 the forecast's unit is filed in its Read me", any("average number of 911 calls presented" in x for x in FCM.READ_ME))
    five = CA.fy2028(fc, busy, pat, c=5)
    ck("SF9 four call-takers: five file no month short; the supervisor and callback desk take no 911 calls",
       CA.short_months(five) == [] and "do not take calls from the 911 queue" in sop)
    ans = C.is911 & ~C.ab
    talk = float(np.mean(C.rel[ans] - C.ans[ans]))
    talkonly = CA.fy2028(fc, talk, pat)
    ck("SF10 busy time to release (talk only) files another call, ruled out by SOP 2.10 section 4.2",
       CA.short_months(talkonly) != want and "takes no new call until the call-taker sets Ready" in sop,
       "talk %.1f s: %s" % (talk, CA.label_set(CA.short_months(talkonly))))
    windows = {"fiscal 2026": loc_fy == 2026, "January to June 2025": loc_fy == 2025, "fiscal 2027 Q1": loc_fy == 2027,
               "the late shift's calls": late, "legacy layout": C.layout == "legacy", "i3 layout": C.layout == "i3",
               "transfers-in left out": ~C.xin}
    for nm_, msk in windows.items():
        b_, p_, w_, n_ = CA.estimates(C, msk)
        v = CA.fy2028(fc, b_, pat)
        ck("SF11 busy time over %s: same call" % nm_, same_call(v, gold), "%.2f s: %s" % (b_, fmt(v)))
        v = CA.fy2028(fc, busy, p_)
        ck("SF12 patience over %s: same call" % nm_, same_call(v, gold), "%.1f s (%d hang-ups): %s" % (p_, n_, fmt(v)))
    km = km_patience(C)
    v = CA.fy2028(fc, busy, km)
    ck("SF13 Kaplan-Meier on the same waits, an exponential fitted to it: same call", same_call(v, gold),
       "%.1f s: %s" % (km, fmt(v)))
    hz = hazard_patience(C)
    v = CA.fy2028(fc, busy, hz)
    ck("SF13 the hang-up rate over waiting time by 30-second band, pooled: same call", same_call(v, gold),
       "%.1f s: %s" % (hz, fmt(v)))
    for warm in (False, True):
        tr = transient(fc, busy, pat, warm=warm)
        ck("SF14 each night as one continuous queue (%s at 22:00): same call, within 0.4" % (
           "from the evening block's five call-takers" if warm else "empty"),
           CA.short_months(tr) == want and all(abs(tr[ym] - gold[ym]) < 0.004 for ym in FY28) and rounded(tr) == rounded(gold),
           fmt(tr) + "; largest move %.2f" % max(abs(100 * (tr[ym] - gold[ym])) for ym in FY28))
    flat = CA.fy2028(fc, busy, pat, flat=True)
    ck("SF15 the shift's average rate for its hours: same call", same_call(flat, gold), fmt(flat))
    mh = mean_of_hours(fc, busy, pat)
    ck("SF16 the forecast-weighted mean of hourly figures: same call", same_call(mh, gold), fmt(mh))
    ck("SF17 transfers-in in the estimates or not: same call (asserted under SF11 and SF12)", True)
    C2 = with_tests(C)
    b_, p_, w_, n_ = CA.estimates(C2)
    v = CA.fy2028(fc, b_, p_)
    ck("SF18 test calls counted as 911 calls: same call", same_call(v, gold), "%.2f s, %.1f s: %s" % (b_, p_, fmt(v)))
    keep = first_of_redials(C)
    b_, p_, w_, n_ = CA.estimates(C, keep)
    v = CA.fy2028(fc, b_, p_)
    ck("SF19 redials collapsed to one call per number in ten minutes: same call", same_call(v, gold),
       "%d calls dropped; %.1f s: %s" % ((~keep & C.is911).sum(), p_, fmt(v)))
    ck("SF20 the two layouts' estimates agree (SF11, SF12 legacy and i3)", True)
    nov = no_dst(fc, busy, pat)
    ck("SF21 the 6 November 2027 night at four hours: same call", same_call(nov, gold), fmt(nov))
    ck("SF22 falls short on unrounded figures: every month at least 0.9 from 90", margin >= 0.9, "%.3f" % margin)
    hr = rounded_hours(fc, busy, pat)
    ck("SF23 hourly figures rounded first: same call", same_call(hr, gold), fmt(hr))
    cut0 = K.CUT_WIRELESS.astimezone(K.UTC).timestamp()
    cut1 = K.CUT_WIRELINE.astimezone(K.UTC).timestamp()
    both = (C.t >= cut0) & (C.t < cut1)
    leg = set(zip(np.round(C.t[both & (C.layout == "legacy")]).astype(int), C.cbn[both & (C.layout == "legacy")]))
    i3 = set(zip(np.round(C.t[both & (C.layout == "i3")]).astype(int), C.cbn[both & (C.layout == "i3")]))
    ck("SF24 the cutover days: calls in both exports, none in both", len(leg) > 100 and len(i3) > 100 and not (leg & i3),
       "%d legacy, %d i3, %d in both" % (len(leg), len(i3), len(leg & i3)))

    # ------------------------------------------------------------------------------------------------ one sigma
    se_p = pat / math.sqrt(nab)
    se_b = float(np.std(C.ready[ans] - C.ans[ans]) / math.sqrt(ans.sum()))
    for db, dp in ((se_b, 0), (-se_b, 0), (0, se_p), (0, -se_p), (se_b, -se_p), (-se_b, se_p)):
        v = CA.fy2028(fc, busy + db, pat + dp)
        ck("one sigma busy %+.2f s, patience %+.2f s: same call" % (db, dp), same_call(v, gold), fmt(v))
    lp = CA.estimates(C, late)[1]
    sl = lp / math.sqrt(CA.estimates(C, late)[3])
    for dp in (sl, -sl):
        v = CA.fy2028(fc, busy, lp + dp)
        ck("one sigma on the late shift's own patience (%.1f %+.1f s): same call" % (lp, dp), same_call(v, gold), fmt(v))

    # ------------------------------------------------------------------------------------------------ margins
    # what it takes to move July off 88 per cent, and each month nearest the standard across 90
    J = (2027, 7)
    p_lo = brentq(lambda p: CA.fy2028(fc, busy, p)[J] - 0.885, 60.0, pat, xtol=0.01)
    p_hi = brentq(lambda p: CA.fy2028(fc, busy, p)[J] - 0.875, pat, 900.0, xtol=0.01)
    b_lo = brentq(lambda b: CA.fy2028(fc, b, pat)[J] - 0.885, 200.0, busy, xtol=0.01)
    b_hi = brentq(lambda b: CA.fy2028(fc, b, pat)[J] - 0.875, busy, 260.0, xtol=0.01)
    ck("margin July rounds to 88 for a patience and a busy time far beyond one sigma",
       p_lo < pat - 10 * se_p and p_hi > pat + 10 * se_p and b_lo < busy - 5 * se_b and b_hi > busy + 5 * se_b,
       "patience %.1f to %.1f s, busy time %.1f to %.1f s" % (p_lo, p_hi, b_lo, b_hi))
    scaled = lambda s: {k: (v[0] * s, v[1]) for k, v in fc.items()}
    for ym, below in (((2027, 8), True), ((2028, 6), True), ((2027, 9), False), ((2028, 5), False)):
        if below:
            p90 = brentq(lambda p: CA.fy2028(fc, busy, p)[ym] - 0.90, 20.0, pat, xtol=0.01)
            b90 = brentq(lambda b: CA.fy2028(fc, b, pat)[ym] - 0.90, 150.0, busy, xtol=0.01)
            s90 = brentq(lambda s: CA.fy2028(scaled(s), busy, pat)[ym] - 0.90, 0.8, 1.0, xtol=1e-5)
        else:
            p90 = brentq(lambda p: CA.fy2028(fc, busy, p)[ym] - 0.90, pat, 20000.0, xtol=0.01)
            b90 = brentq(lambda b: CA.fy2028(fc, b, pat)[ym] - 0.90, busy, 300.0, xtol=0.01)
            s90 = brentq(lambda s: CA.fy2028(scaled(s), busy, pat)[ym] - 0.90, 1.0, 1.2, xtol=1e-5)
        ck("margin %s %d crosses 90 only with its arrivals 3 per cent or more off, the patience 50 s or the busy time "
           "8 s" % (K.MON3[ym[1]], ym[0]), abs(s90 - 1) >= 0.03 and abs(p90 - pat) >= 50 and abs(b90 - busy) >= 8,
           "arrivals x %.4f, patience %.1f s, busy time %.1f s" % (s90, p90, b90))

    # ------------------------------------------------------------------------------------------------ ladder
    ladder = {"R0 Erlang C": easy, "R1a fiscal 2026 observed carried forward": carried, "R1b own forecast": own,
              "R2 the hang-ups' own waits": CA.fy2028(fc, busy, wab), "R3 golden": gold}
    for k_, v in ladder.items():
        print("      ladder %-44s %-40s July %.2f" % (k_, CA.label_set(CA.short_months(v)), 100 * v[(2027, 7)]))
    ck("ladder rung 0 files May to September", CA.short_months(ladder["R0 Erlang C"]) ==
       [(2027, 7), (2027, 8), (2027, 9), (2028, 5), (2028, 6)])
    ck("ladder rungs 1a, 1b and 2 file no month or July alone",
       all(CA.short_months(ladder[k]) in ([], [(2027, 7)]) for k in ("R1a fiscal 2026 observed carried forward",
                                                                        "R1b own forecast", "R2 the hang-ups' own waits")))
    ck("ladder the decisive step reverses rung 2's direction",
       ladder["R2 the hang-ups' own waits"][(2027, 7)] > gold[(2027, 7)] > easy[(2027, 7)])
    grid = {"own forecast with Erlang C": CA.fy2028(fc, busy, pat, model="C", use_halvorsen=False),
            "own forecast with the hang-ups' own waits": CA.fy2028(fc, busy, wab, use_halvorsen=False),
            "the board's forecast, Erlang C with five call-takers": CA.fy2028(fc, busy, pat, model="C", c=5)}
    for k_, v in grid.items():
        print("      grid   %-44s %-40s July %.2f" % (k_, CA.label_set(CA.short_months(v)), 100 * v[(2027, 7)]))
        ck("grid %s files another set, every month at least 0.9 from 90" % k_,
           CA.short_months(v) != want and min(abs(100 * x - 90) for x in v.values()) >= 0.9,
           CA.label_set(CA.short_months(v)))
    worst2 = min(100 * (ladder["R2 the hang-ups' own waits"][ym] - gold[ym]) for ym in FY28)
    ck("ladder rung 2's figures all above the golden's by at least 0.9", worst2 >= 0.9, "%.2f" % worst2)
    worst0 = min(100 * (gold[ym] - easy[ym]) for ym in FY28)
    ck("ladder rung 0's figures all below the golden's by at least 1.0", worst0 >= 1.0, "%.2f" % worst0)
    # the calibration rival: Erlang C with the busy time scaled to reproduce fiscal 2026
    ros = CA.read_roster(target, R.F_ROSTER)
    t0 = K.HIST_START.astimezone(K.UTC).timestamp()
    nh = int(round((K.HIST_END.astimezone(K.UTC).timestamp() - t0) / 3600))
    obs26 = CA.backtest(C, ros, t0, nh, busy, pat, lambda h: h[4] == 2026)["obs"]
    f = lambda bb: CA.backtest(C, ros, t0, nh, bb, pat, lambda h: h[4] == 2026)["C"] - obs26
    bcal = brentq(f, busy * 0.7, busy)
    ccal = CA.fy2028(fc, bcal, pat, model="C")
    hit = sum(r0(ccal[ym]) == r0(gold[ym]) for ym in FY28)
    print("      ladder R1c Erlang C, busy time %.1f s to fit fiscal 2026   %-40s July %.2f; %d of 12 figures on the golden's"
          % (bcal, CA.label_set(CA.short_months(ccal)), 100 * ccal[(2027, 7)], hit))
    ck("ladder the calibrated Erlang C misses the golden's July, August and June figures",
       all(r0(ccal[ym]) != r0(gold[ym]) for ym in want), " ".join("%d" % r0(ccal[ym]) for ym in want))
    G["ccal"] = (bcal, ccal, hit)
    # the queue with hang-ups, its patience calibrated so it reproduces an observed period's compliance
    m25 = np.array([K.to_local(x).year == 2025 and K.to_local(x).month <= 6 for x in C.t])
    b25 = CA.estimates(C, m25)[0]
    for lbl, selc, bb in (("fiscal 2026", lambda h: h[4] == 2026, busy),
                          ("January to June 2025", lambda h: h[0] == 2025 and h[1] <= 6, b25)):
        o = CA.backtest(C, ros, t0, nh, bb, pat, selc)["obs"]
        pc = brentq(lambda p: CA.backtest(C, ros, t0, nh, bb, p, selc)["A"] - o, 40.0, 3000.0, xtol=0.5)
        v = CA.fy2028(fc, busy, pc)
        ck("the patience calibrated to %s's observed compliance (%.1f s): same call" % (lbl, pc), same_call(v, gold), fmt(v))
    sel26 = lambda h: h[4] == 2026
    oab = CA.backtest(C, ros, t0, nh, busy, pat, sel26)["ab_obs"]
    pa = brentq(lambda p: CA.backtest(C, ros, t0, nh, busy, p, sel26)["ab_A"] - oab, 40.0, 3000.0, xtol=0.5)
    v = CA.fy2028(fc, busy, pa)
    ck("the patience calibrated to fiscal 2026's observed hang-up share (%.1f s): same call" % pa, same_call(v, gold), fmt(v))

    # ------------------------------------------------------------------------------------------------ back-test
    bt = G["backtest"]
    ck("back-test out of sample: Erlang A with censored patience within 0.4 of fiscal 2026", abs(bt["A"] - bt["obs"]) < 0.004,
       "obs %.2f A %.2f" % (100 * bt["obs"], 100 * bt["A"]))
    ck("back-test Erlang C under fiscal 2026 by more than 1.0", bt["obs"] - bt["C"] > 0.010, "C %.2f" % (100 * bt["C"]))
    ck("back-test the hang-ups' own waits over fiscal 2026 by more than 0.8", bt["Ab"] - bt["obs"] > 0.008,
       "Ab %.2f" % (100 * bt["Ab"]))
    bm = G["backtest_months"]
    ck("back-test month by month: Erlang C below the observed in 12 of 12", sum(v["C"] < v["obs"] for v in bm.values()) == 12)
    ck("back-test month by month: the hang-ups' own waits above the observed in 12 of 12",
       sum(v["Ab"] > v["obs"] for v in bm.values()) == 12)
    ck("back-test hang-ups: Erlang A within 0.15 points, the hang-ups' own waits half again or more",
       abs(bt["ab_A"] - bt["ab_obs"]) < 0.0015 and bt["ab_Ab"] / bt["ab_obs"] > 1.4,
       "obs %.3f A %.3f Ab %.3f" % (100 * bt["ab_obs"], 100 * bt["ab_A"], 100 * bt["ab_Ab"]))

    # ------------------------------------------------------------------------------------------------ R2 mess neutral
    ck("R2 the legacy layout dropped from the estimates: same call (SF11, SF12 i3 layout)", True)
    ck("R2 test calls counted: same call (SF18)", True)
    ck("R2 redials collapsed: same call (SF19)", True)
    ck("R2 transfers-in left out: same call (SF11, SF12)", True)
    ck("R2 the floor roster and the FY2027 sheet carry nothing the golden reads", True)

    # ------------------------------------------------------------------------------------------------ asks
    ask_checks(ck, target, G, W)

    # ------------------------------------------------------------------------------------------------ separation and distractors
    tmp = tempfile.mkdtemp(dir=TASK, suffix=".tmp")
    try:
        for f in MAIN_FILES:
            shutil.copy(os.path.join(target, f), tmp)
        C3 = CA.read_calls(tmp, R.F_LEGACY, R.F_I3)
        b3, p3 = CA.estimates(C3)[:2]
        g3 = CA.fy2028(CA.read_forecast(tmp, R.F_FORECAST), b3, p3)
        ck("separation: the call from the main files alone is the golden", same_call(g3, gold))
        shutil.rmtree(tmp)
        os.makedirs(tmp)
        for f in [R.F_LEGACY, R.F_I3] + ASK_FILES:
            shutil.copy(os.path.join(target, f), tmp)
        C4 = CA.read_calls(tmp, R.F_LEGACY, R.F_I3)
        a4 = CA.ask_a(C4, CA.read_che(tmp, R.F_CHE), CA.read_boundary(tmp, R.F_BOUNDARY), CA.read_directory(tmp, R.F_DIRECTORY))
        b4 = CA.ask_b(C4, CA.read_callbacks(tmp, R.F_CALLBACK))[0]
        ck("separation: the asks without the roster, the forecast and the documents are the asks", a4 == G["ask_a"] and b4 == G["ask_b"])
        ck("distractors: the call and the asks read neither distractor", True, ", ".join(meta["distractor_files"]))
    finally:
        shutil.rmtree(tmp)

    # ------------------------------------------------------------------------------------------------ realism sweep
    realism(ck, target, files, C)
    ck.done()
    return ck


# ---------------------------------------------------------------------------------------------------- helpers
def km_patience(C):
    """Kaplan-Meier on every 911 call's wait (a hang-up is the event, an answer censors), and the exponential that fits
    its cumulative hazard over the first three minutes."""
    m = C.is911
    w = C.wait[m]
    ev = C.ab[m]
    order = np.argsort(w, kind="mergesort")
    w, ev = w[order], ev[order]
    n = len(w)
    at_risk = n - np.arange(n)
    times = w[ev]
    risk = at_risk[ev]
    H = np.cumsum(1.0 / risk)
    sel = times <= 180.0
    t_, H_ = times[sel], H[sel]
    th = float(np.sum(t_ * H_) / np.sum(t_ * t_))
    return 1.0 / th


def hazard_patience(C):
    m = C.is911
    w, ev = C.wait[m], C.ab[m]
    edges = np.arange(0, 1200, 30.0)
    tot_ev = tot_exp = 0.0
    for a in edges:
        expo = np.clip(w - a, 0, 30.0).sum()
        e = np.sum(ev & (w >= a) & (w < a + 30.0))
        tot_ev += e
        tot_exp += expo
    return tot_exp / tot_ev


def mean_of_hours(fc, busy, pat):
    mu, th = 3600.0 / busy, 3600.0 / pat
    out = {}
    for y, m in FY28:
        num = den = 0.0
        for nd, cells in M.night_cells(y, m):
            for dow, h in cells:
                lam = fc[(y, m, dow, h)][0]
                st, a5 = E.erlang_a(lam, mu, th, 4)[:2]
                num += lam * st / (1 - a5)
                den += lam
        out[(y, m)] = num / den
    return out


def rounded_hours(fc, busy, pat):
    mu, th = 3600.0 / busy, 3600.0 / pat
    out = {}
    for y, m in FY28:
        num = den = 0.0
        for nd, cells in M.night_cells(y, m):
            for dow, h in cells:
                lam = fc[(y, m, dow, h)][0]
                st, a5 = E.erlang_a(lam, mu, th, 4)[:2]
                num += lam * K.round_half_up(st / (1 - a5), 2)
                den += lam
        out[(y, m)] = num / den
    return out


def no_dst(fc, busy, pat):
    mu, th = 3600.0 / busy, 3600.0 / pat
    out = {}
    for y, m in FY28:
        num = den = 0.0
        for nd, cells in M.night_cells(y, m):
            seen = []
            for dow, h in cells:
                if (dow, h) in seen:
                    continue
                seen.append((dow, h))
                lam = fc[(y, m, dow, h)][0]
                st, a5 = E.erlang_a(lam, mu, th, 4)[:2]
                num += lam * st
                den += lam * (1 - a5)
        out[(y, m)] = num / den
    return out


def with_tests(C):
    """Every call counted as a 911 call, the test calls with the responder's few seconds as their busy time."""
    D = CA.Calls()
    for k, v in vars(C).items():
        setattr(D, k, v)
    D.is911 = np.ones(len(C.t), dtype=bool)
    D.ready = np.where(C.test & np.isnan(C.ready), C.ans + 10.0, C.ready)
    return D


def first_of_redials(C):
    """Keep the first call from a number in any ten minutes."""
    keep = np.ones(len(C.t), dtype=bool)
    last = {}
    for i in np.argsort(C.t, kind="mergesort"):
        k = C.cbn[i]
        if k in last and C.t[i] - last[k] < 600.0:
            keep[i] = False
        last[k] = C.t[i]
    return keep


def transient(fc, busy, pat, warm=False, steps=40):
    """Each fiscal 2028 night as one continuous queue: the state distribution carried hour to hour through the
    night's forecast rates (four call-takers), from empty at 22:00 or from the 21:00 hour's stationary state with the
    evening block's five; each arrival's chance of an answer within 15 seconds (or a hang-up within 5) read off the
    state it meets, integrated over the hour."""
    from scipy.linalg import expm
    mu, th = 3600.0 / busy, 3600.0 / pat
    c = 4
    N = c + E.KMAX
    St, ABx = E._tagged(c, mu, th, 15.0 / 3600, 5.0 / 3600)[:2]
    s15 = np.concatenate([np.ones(c), St])
    a5 = np.concatenate([np.zeros(c), ABx])

    def gen(lam, cc):
        Q = np.zeros((N, N))
        for n in range(N):
            if n + 1 < N:
                Q[n, n + 1] = lam
            if n > 0:
                Q[n, n - 1] = min(n, cc) * mu + max(n - cc, 0) * th
            Q[n, n] = -Q[n].sum()
        return Q
    cache = {}
    out = {}
    for y, m in FY28:
        num = den = 0.0
        for nd in K.late_nights(y, m):
            hrs = K.night_hours(nd)
            if warm:
                lam21 = fc[(y, m, nd.weekday(), 21)][0]
                p5 = E.stationary(lam21, mu, th, 5)
                p = np.zeros(N)
                n_ = min(N, len(p5))
                p[:n_] = p5[:n_]
                p /= p.sum()
            else:
                p = np.zeros(N)
                p[0] = 1.0
            for h in hrs:
                lam = fc[(y, m, h.weekday(), h.hour)][0]
                key = round(lam, 3)
                if key not in cache:
                    cache[key] = expm(gen(lam, c) * (1.0 / steps))
                P = cache[key]
                for k in range(steps):
                    q = p @ P
                    num += lam * 0.5 * (p @ s15 + q @ s15) / steps
                    den += lam * (1.0 - 0.5 * (p @ a5 + q @ a5)) / steps
                    p = q
        out[(y, m)] = num / den
    return out


def ask_checks(ck, target, G, W):
    C = G["C"]
    A = G["ask_a"]
    # truth from the world: true location in the township, presented in fiscal 2026, transfers to Wexley
    tru = {(2026, q): [0, 0] for q in (1, 2, 3, 4)}
    lo, hi = R.FY26
    for i in np.nonzero(np.isin(W.area, ["main", "detached"]))[0]:
        if not (lo <= W.t[i] < hi) or R.in_legacy(W, i) or W.kind[i] != "wireless":
            continue
        q = K.fiscal_quarter(K.to_local(W.t[i]).date())
        tru[q][0] += 1
        tru[q][1] += int(W.xout[i] == "wexley")
    tru = {k: tuple(v) for k, v in tru.items()}
    ck("Ask A golden equals the world's own Halvorsen calls in every quarter", A == tru, "%s against %s" % (A, tru))
    che, polys, dr = G["che"], G["polys"], G["directory"]
    stops = {"S1 the cracker (handset fix, the first part's outer ring, URIs naming Wexley)":
             CA.ask_a(C, che, polys, dr, holes=False, all_parts=False, xfer="name"),
             "S2 the routing location": CA.ask_a(C, che, polys, dr, fix="first"),
             "S3 full geometry, URIs naming Wexley": CA.ask_a(C, che, polys, dr, xfer="name"),
             "S4 quarters by UTC date": CA.ask_a(C, che, polys, dr, quarter="utc")}
    need = {"S1": 8, "S2": 8, "S3": 4, "S4": 4}
    for k_, v in stops.items():
        off = sum(v[q][j] != A[q][j] for q in A for j in (0, 1))
        ck("Ask A stop %s misses %d or more of 8" % (k_, need[k_[:2]]), off >= need[k_[:2]], "%d off: %s" % (off, v))
    # devices
    hole = {(2026, q): 0 for q in (1, 2, 3, 4)}
    det = {(2026, q): 0 for q in (1, 2, 3, 4)}
    alt = {(2026, q): [0, 0] for q in (1, 2, 3, 4)}
    for i in np.nonzero(W.area != "")[0]:
        if not (lo <= W.t[i] < hi) or W.kind[i] != "wireless":
            continue
        q = K.fiscal_quarter(K.to_local(W.t[i]).date())
        hole[q] += W.area[i] == "tamsen"
        det[q] += W.area[i] == "detached"
        if W.xout[i] == "wexley" and W.area[i] in ("main", "detached"):
            alt[q][0] += 1
            alt[q][1] += bool(W.xout_alt[i])
    ck("Ask A device A1: city calls inside the hole and detached-part calls in every quarter",
       all(150 <= hole[q] <= 600 for q in hole) and all(60 <= det[q] <= 200 for q in det), "hole %s detached %s" % (hole, det))
    ck("Ask A device A3: alternate transfers 8 to 15 per cent in every quarter",
       all(0.08 <= alt[q][1] / alt[q][0] <= 0.15 for q in alt), str({q: round(alt[q][1] / alt[q][0], 3) for q in alt}))
    first_cell = all(recs[0][1] == "cell" for recs in che.values())
    ck("Ask A device A2: every call's first record is its routing location", first_cell)
    ok_side, min_edge = True, 1e9
    for cid, recs in che.items():
        hs = [r for r in recs if r[1] != "cell"]
        sides = {CA.in_polys(r[3], r[2], polys) for r in hs}
        ok_side &= len(sides) == 1 and len(hs) >= 1
        for r in hs:
            x, y = GEO.to_xy(r[2], r[3])
            min_edge = min(min_edge, GEO.edge_dist_km(x, y))
    ck("Ask A C1: every call has a handset fix and all its fixes lie on one side, 40 m or more from every edge",
       ok_side and min_edge >= 0.040, "nearest fix %.0f m" % (1000 * min_edge))
    ck("Ask A scope: the extract's box holds the whole township",
       all(GEO.BOX[0] < x < GEO.BOX[2] and GEO.BOX[1] < y < GEO.BOX[3] for x, y in GEO.MAIN + GEO.DETACHED))
    # ask B
    Bm = G["ask_b"]
    tb = {}
    tdn = {}
    for (line, idx), tk in W.cb_member.items():
        if line != "911":
            continue
        task = W.cb_tasks[tk]
        hang = W.hang_t[idx]
        loc = K.to_local(hang)
        key = (loc.year, loc.month)
        tdn[key] = tdn.get(key, 0) + 1
        tb[key] = tb.get(key, 0) + int(task["first_dial"] is not None and 0 <= task["first_dial"] - hang <= 120.0)
    tru_b = {k: tb[k] / tdn[k] for k in tdn}
    ck("Ask B golden equals the world's own dial-backs in every month",
       all(abs(tru_b[k] - Bm[k]) < 1e-12 for k in Bm) and set(tru_b) == set(Bm), str({k: round(100 * v, 2) for k, v in tru_b.items()}))
    tasks = G["tasks"]
    bstops = {"S1 tasks joined on the opening call, the unjoined counted as not dialled back": CA.ask_b(C, tasks, match="ref")[0],
              "S2 tasks joined on the opening call, the unjoined dropped": CA.ask_b(C, tasks, match="ref", unmatched="drop")[0],
              "S3 tasks joined on the opening call, two minutes from the task's stamp":
              CA.ask_b(C, tasks, match="ref", anchor="created")[0],
              "S4 the task log alone, tasks as the unit": CA.ask_b(C, tasks, match="tasks")[0]}
    for k_, v in bstops.items():
        off = sum(K.round_half_up(100 * v[k], 1) != K.round_half_up(100 * Bm[k], 1) for k in Bm)
        ck("Ask B stop %s misses 6 of 6" % k_, off == 6, str({k: round(100 * x, 2) for k, x in v.items()}))
    for k_, v in {"S5 merges resolved, the misdials left out": CA.ask_b(C, tasks, misdials=False)[0],
                  "S6 merges resolved, two minutes from the stamp": CA.ask_b(C, tasks, anchor="created")[0]}.items():
        off = sum(K.round_half_up(100 * v[k], 1) != K.round_half_up(100 * Bm[k], 1) for k in Bm)
        ck("Ask B stop %s misses 4 or more of 6" % k_, off >= 4, "%d off: %s" % (off, {k: round(100 * x, 2) for k, x in v.items()}))
    for tol in (25.0, 45.0, 90.0, 300.0):
        ck("Ask B matching window %.0f s: same figures" % tol, CA.ask_b(C, tasks, tol=tol)[0] == Bm)
    edge = min(abs(100 * Bm[k] * 10 - math.floor(100 * Bm[k] * 10) - 0.5) for k in Bm)
    ck("Ask B no month on a one-decimal rounding edge", edge > 0.02, "%.3f" % edge)
    ck("realism no ask share a whole number and no ask count a multiple of 100",
       all(abs(100 * Bm[k] - round(100 * Bm[k])) > 0.05 for k in Bm) and all(v % 100 for q in A for v in A[q]),
       "%s %s" % ({k: round(100 * v, 2) for k, v in Bm.items()}, A))
    rep = {}
    for task in W.cb_tasks:
        if task["line"] != "911":
            continue
        for (line, idx, th) in task["members"][1:]:
            loc = K.to_local(th)
            rep[(loc.year, loc.month)] = rep.get((loc.year, loc.month), 0) + 1
    tot_rep, tot_den = sum(rep.values()), sum(G["ask_b_den"].values())
    ck("Ask B device B1: repeat abandons joined to open tasks in every month, 2 per cent or more overall",
       all(rep.get(k, 0) >= 1 for k in Bm) and tot_rep / tot_den >= 0.02,
       "%s, %.1f%% overall" % ({k: rep.get(k, 0) for k in Bm}, 100.0 * tot_rep / tot_den))
    lo2, hi2 = W.cb_window
    straddle = [i for i in np.nonzero(W.ab)[0] if lo2 <= W.hang_t[i] < hi2
                and K.to_local(W.t[i]).month != K.to_local(W.hang_t[i]).month]
    ck("Ask B C1: no abandoned call presented in one month and hung up in the next", not straddle, "%d" % len(straddle))
    near = 0
    for task in W.cb_tasks:
        if task["first_dial"] is None:
            continue
        for (line, idx, th) in task["members"]:
            if abs(task["first_dial"] - th - 120.0) < 1.5:
                near += 1
    ck("Ask B C1: no first dial within 1.5 seconds of any member's two-minute mark", near == 0, "%d" % near)
    # hazards (Layer 1): what each moves
    r1 = lambda d: {k: K.round_half_up(100 * v, 1) for k, v in d.items()}
    gb = r1(Bm)
    fixed = []
    for tk in tasks:
        t2 = dict(tk)
        for key in ("created", "first"):
            if not math.isnan(t2[key]) and K.to_local(t2[key]).utcoffset().total_seconds() == -5 * 3600:
                t2[key] = t2[key] + 3600.0
        fixed.append(t2)
    hb1 = r1(CA.ask_b(C, fixed)[0])
    ck("hazard HB1 the callback log read on a fixed offset loses the matches from 8 March",
       hb1[(2026, 1)] == gb[(2026, 1)] and hb1[(2026, 3)] < 20 and all(hb1[(2026, m)] < 5 for m in (4, 5, 6)), str(hb1))
    hb2 = r1(CA.ask_b(C, [dict(t, line="911") for t in tasks], match="tasks")[0])
    ck("hazard HB2 a task-side share with the administrative line's tasks moves every month",
       all(abs(hb2[k] - gb[k]) >= 2 for k in gb), str(hb2))
    by_num = {}
    for tk in tasks:
        if tk["line"] == "911":
            by_num.setdefault(tk["num"], []).append(tk)
    lo3 = dt.datetime(2026, 1, 1, tzinfo=K.TZ).timestamp()
    hi3 = dt.datetime(2026, 7, 1, tzinfo=K.TZ).timestamp()
    selb = sorted(np.nonzero(C.is911 & C.ab & (C.hang >= lo3) & (C.hang < hi3))[0], key=lambda i: C.hang[i])

    def share(rows):
        num, den = {}, {}
        for i in rows:
            loc = K.to_local(C.hang[i])
            key = (loc.year, loc.month)
            firsts = [tk["first"] for tk in by_num.get(C.cbn[i], []) if not math.isnan(tk["first"])
                      and tk["first"] >= C.hang[i] and tk["created"] <= C.hang[i] + 30.0]
            den[key] = den.get(key, 0) + 1
            num[key] = num.get(key, 0) + int(bool(firsts) and min(firsts) - C.hang[i] <= 120.0)
        return r1({k: num[k] / den[k] for k in den})
    ck("hazard Ask B's own construction reproduces the golden", share(selb) == gb)
    seen, keep = set(), []
    for i in selb:
        loc = K.to_local(C.hang[i])
        if (loc.year, loc.month, C.cbn[i]) not in seen:
            seen.add((loc.year, loc.month, C.cbn[i]))
            keep.append(i)
    hc1b = share(keep)
    ck("hazard HC1 one abandon per number a month moves every month of Ask B", all(hc1b[k] != gb[k] for k in gb),
       "%s, %d repeats dropped" % (hc1b, len(selb) - len(keep)))
    hc3 = share([i for i in selb if not C.xin[i]])
    ck("hazard HC3 the transferred-in abandons left out moves 4 or more months of Ask B",
       sum(hc3[k] != gb[k] for k in gb) >= 4, "%s, %d transferred in" % (hc3, int(np.sum(C.xin[selb]))))
    lo4 = dt.datetime(2025, 7, 1, tzinfo=K.TZ).timestamp()
    hi4 = dt.datetime(2026, 7, 1, tzinfo=K.TZ).timestamp()
    nums, cnt = {}, {}
    for i in np.nonzero(C.is911 & (C.kind == "wireless") & (C.layout == "i3"))[0]:
        hs = [r for r in che.get(C.cid[i], []) if r[1] != "cell"]
        if not hs or not (lo4 <= C.t[i] < hi4) or not CA.in_polys(hs[-1][3], hs[-1][2], polys):
            continue
        q = K.fiscal_quarter(K.to_local(C.t[i]).date())
        nums.setdefault(q, set()).add(C.cbn[i])
        cnt[q] = cnt.get(q, 0) + 1
    ck("hazard HC1 one call per number a quarter moves every quarter of Ask A",
       all(len(nums[q]) != A[q][0] for q in A) and all(cnt[q] == A[q][0] for q in A),
       str({q: (len(nums[q]), A[q][0]) for q in sorted(A)}))
    ck("hazard HC2 no test call is a wireless call", not np.any(C.test & (C.kind == "wireless")))


def realism(ck, target, files, C):
    # monthly 911 counts distinct, no round totals
    months = {}
    for x in C.t[C.is911]:
        d = K.to_local(x)
        months[(d.year, d.month)] = months.get((d.year, d.month), 0) + 1
    vals = list(months.values())
    ck("realism monthly 911 counts all distinct", len(set(vals)) == len(vals), "%d months" % len(vals))
    ck("realism no monthly count a multiple of 100", not any(v % 100 == 0 for v in vals))
    texts = [f for f in files if f.endswith((".md", ".csv", ".geojson"))]
    tells = []
    for f in texts:
        t = open(os.path.join(target, f), encoding="utf-8").read()
        if "\u2014" in t or "\u2013" in t:
            tells.append(f + " dash")
        if re.search(r"\bfictional\b|\bfictitious\b|\bconstructed for\b|\bthis exercise\b|\bsynthetic\b", t, re.I):
            tells.append(f + " fiction word")
    ck("realism no dash and no fiction word in the pack's text files", not tells, ", ".join(tells))
    pdfs = [f for f in files if f.endswith(".pdf")]
    bad = [f for f in pdfs if b"ReportLab" in open(os.path.join(target, f), "rb").read()]
    ck("realism PDFs carry no writer banner", not bad, ", ".join(bad))
    with zipfile.ZipFile(os.path.join(target, R.F_FORECAST)) as z:
        app = z.read("docProps/app.xml").decode()
    ck("realism the workbook carries Excel's application stamp", "<Application>Microsoft Excel</Application>" in app)
    last = max(C.t)
    ck("realism no call after 30 September 2026", K.to_local(last).date() <= dt.date(2026, 9, 30), str(K.to_local(last)))
    people = set(K.PEOPLE.values())
    readme = open(os.path.join(target, DOC.F_README), encoding="utf-8").read()
    named = set(re.findall(r"\b([A-Z][a-z]+ [A-Z][a-z]+)\b", readme)) & {p for p in people}
    ck("realism every person named in the pack is one of the drawn personas", named <= people, ", ".join(sorted(named)))
