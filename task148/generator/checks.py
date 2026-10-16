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
    busy, pat, wab, nab = G["busy"], G["patience"], G["wab"], G["n_abandoned_late"]
    pat_all, wab_all, nab_all = G["patience_all"], G["wab_all"], G["n_abandoned"]
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
       "%d calls, %d abandoned; the late shift %d calls, %d abandoned" % (G["n_911"], nab_all, G["n_911_late"], nab))

    # ------------------------------------------------------------------------------------------------ R3 on the clean truth
    tb = float(np.mean(W.busy[~W.ab]))
    wl = np.array([K.is_frisat_late(K.to_local(x)) for x in W.t])
    easy = CA.fy2028(fc, tb, pat, model="C")
    ck("R3a the easy route (Erlang C, measured busy time, the board's forecast, four call-takers) files May to September",
       CA.short_months(easy) == [(2027, 7), (2027, 8), (2027, 9), (2028, 5), (2028, 6)],
       CA.label_set(CA.short_months(easy)) + "; July %.2f" % (100 * easy[(2027, 7)]))
    tp = float(np.sum(W.wait[wl]) / W.ab[wl].sum())
    dec = CA.fy2028(fc, tb, tp)
    ck("R3b the decisive step alone (the queue with hang-ups at the late shift's own patience, over every wait) files "
       "the golden", same_call(dec, gold), "%.1f s: %s" % (tp, fmt(dec)))
    tpa = float(np.sum(W.wait) / W.ab.sum())
    tw = float(np.mean(W.wait[W.ab & wl]))
    twa = float(np.mean(W.wait[W.ab]))
    lower = {"R2 the late shift's hang-ups' own waits": CA.fy2028(fc, tb, tw),
             "R2 every hang-up's own wait": CA.fy2028(fc, tb, twa),
             "R2b one patience for every call, over every wait": CA.fy2028(fc, tb, tpa),
             "R1b the analyst's own forecast (no Halvorsen move)": CA.fy2028(fc, tb, tp, use_halvorsen=False),
             "R0 with five call-takers": CA.fy2028(fc, tb, tp, model="C", c=5)}
    for k_, v in lower.items():
        ck("R3b %s stays off the golden's months" % k_, CA.short_months(v) != want, CA.label_set(CA.short_months(v)))
    ck("R3b the golden's late-shift patience is the world's within its sampling error",
       abs(pat / K.PATIENCE_WEEKEND_NIGHT - 1) < 3.0 / math.sqrt(nab), "%.2f against %.1f (%d hang-ups)" % (
           pat, K.PATIENCE_WEEKEND_NIGHT, nab))
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
    ck("R3c no document says callers differ by hour, day or call mix",
       not any(re.search(r"hang up (sooner|faster|less)|less patient|more patient|call mix|give up", t) for t in texts.values()))

    # ------------------------------------------------------------------------------------------------ rule-3 sentence audit
    how = DOC.sop_sentences("measure") + DOC.sop_sentences("positions") + DOC.sop_sentences("staffing")
    ck("rule 3 the HOW sentences name no queue, wait distribution or patience",
       not any(re.search(r"queue model|erlang|patience|hold on|wait time distribution", s, re.I) for s in how), "%d sentences" % len(how))
    admitted = {"Erlang C": easy, "Erlang A on the hang-ups' waits": lower["R2 the late shift's hang-ups' own waits"],
                "Erlang A with one patience for every call": lower["R2b one patience for every call, over every wait"]}
    loc_fy = G["loc_fy"]
    late = C.late
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
        num = den = 0.0
        for nd in K.late_nights(y, m):
            for hh in K.night_hours(nd):
                lam = fc[(y, m, nd.weekday(), hh.hour)][0]
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
    oct25 = dt.datetime(2025, 10, 1, tzinfo=K.TZ).timestamp()
    bwin = {"fiscal 2026": loc_fy == 2026, "January to June 2025": loc_fy == 2025, "fiscal 2027 Q1": loc_fy == 2027,
            "the late shift's calls": late, "legacy layout": C.layout == "legacy", "i3 layout": C.layout == "i3",
            "transfers-in left out": ~C.xin}
    for nm_, msk in bwin.items():
        b_ = CA.estimates(C, msk)[0]
        v = CA.fy2028(fc, b_, pat)
        ck("SF11 busy time over %s: same call" % nm_, same_call(v, gold), "%.2f s: %s" % (b_, fmt(v)))
    pwin = {"fiscal 2026": late & (loc_fy == 2026), "the last twelve months": late & (C.t >= oct25),
            "the i3 layout": late & (C.layout == "i3"), "transfers-in left out": late & ~C.xin,
            "Friday and Saturday nights to 06:00": C.wknight}
    for nm_, msk in pwin.items():
        p_, w_, n_ = CA.estimates(C, msk)[1:]
        v = CA.fy2028(fc, busy, p_)
        ck("SF12 the late shift's patience over %s: same call" % nm_, same_call(v, gold), "%.1f s (%d hang-ups): %s" % (p_, n_, fmt(v)))
    km = km_patience(C, late)
    v = CA.fy2028(fc, busy, km)
    ck("SF13 Kaplan-Meier on the late shift's waits, an exponential fitted to it: same call", same_call(v, gold),
       "%.1f s: %s" % (km, fmt(v)))
    hz = hazard_patience(C, late)
    v = CA.fy2028(fc, busy, hz)
    ck("SF13 the late shift's hang-up rate over waiting time by 30-second band, pooled: same call", same_call(v, gold),
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
    b_ = CA.estimates(C2)[0]
    p_ = CA.estimates(C2, late)[1]
    v = CA.fy2028(fc, b_, p_)
    ck("SF18 test calls counted as 911 calls: same call", same_call(v, gold), "%.2f s, %.1f s: %s" % (b_, p_, fmt(v)))
    keep = first_of_redials(C)
    b_ = CA.estimates(C, keep)[0]
    p_ = CA.estimates(C, keep & late)[1]
    v = CA.fy2028(fc, b_, p_)
    ck("SF19 redials collapsed to one call per number in ten minutes: same call", same_call(v, gold),
       "%d calls dropped; %.1f s: %s" % ((~keep & C.is911).sum(), p_, fmt(v)))
    ck("SF20 the two layouts' estimates agree (SF11 busy time; SF12 the i3 layout)", True)
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
        ck("one sigma busy %+.2f s, the late shift's patience %+.2f s: same call" % (db, dp), same_call(v, gold), fmt(v))

    # ------------------------------------------------------------------------------------------------ margins
    J = (2027, 7)
    p_lo = brentq(lambda p: CA.fy2028(fc, busy, p)[J] - 0.885, 30.0, pat, xtol=0.01)
    p_hi = brentq(lambda p: CA.fy2028(fc, busy, p)[J] - 0.875, pat, 2000.0, xtol=0.01)
    b_lo = brentq(lambda b: CA.fy2028(fc, b, pat)[J] - 0.885, 180.0, busy, xtol=0.01)
    b_hi = brentq(lambda b: CA.fy2028(fc, b, pat)[J] - 0.875, busy, 280.0, xtol=0.01)
    ck("margin July rounds to 88 for a patience beyond one sigma and a busy time beyond five",
       p_lo < pat - se_p and p_hi > pat + se_p and b_lo < busy - 5 * se_b and b_hi > busy + 5 * se_b,
       "patience %.1f to %.1f s, busy time %.1f to %.1f s" % (p_lo, p_hi, b_lo, b_hi))
    G["july_band"] = (p_lo, p_hi, b_lo, b_hi)
    scaled = lambda s_: {k: (v_[0] * s_, v_[1]) for k, v_ in fc.items()}
    flips = {}
    for ym, below in (((2027, 8), True), ((2028, 6), True), ((2027, 9), False), ((2028, 5), False)):
        if below:
            p90 = brentq(lambda p: CA.fy2028(fc, busy, p)[ym] - 0.90, 10.0, pat, xtol=0.01)
            b90 = brentq(lambda b: CA.fy2028(fc, b, pat)[ym] - 0.90, 150.0, busy, xtol=0.01)
            s90 = brentq(lambda s_: CA.fy2028(scaled(s_), busy, pat)[ym] - 0.90, 0.8, 1.0, xtol=1e-5)
        else:
            p90 = brentq(lambda p: CA.fy2028(fc, busy, p)[ym] - 0.90, pat, 20000.0, xtol=0.01)
            b90 = brentq(lambda b: CA.fy2028(fc, b, pat)[ym] - 0.90, busy, 300.0, xtol=0.01)
            s90 = brentq(lambda s_: CA.fy2028(scaled(s_), busy, pat)[ym] - 0.90, 1.0, 1.2, xtol=1e-5)
        flips[ym] = (s90, p90, b90)
        ck("margin %s %d crosses 90 only with its arrivals 3 per cent or more off, the patience 25 s or the busy time "
           "8 s" % (K.MON3[ym[1]], ym[0]), abs(s90 - 1) >= 0.03 and abs(p90 - pat) >= 25 and abs(b90 - busy) >= 8,
           "arrivals x %.4f, patience %.1f s, busy time %.1f s" % (s90, p90, b90))
    G["flips"] = flips

    # ------------------------------------------------------------------------------------------------ ladder and the rivals
    def show(name, v, rung=""):
        s_ = CA.short_months(v)
        figs = sum(r0(v[ym]) == r0(gold[ym]) for ym in FY28)
        print("      %-6s %-62s %-44s July %.2f; %2d of 12 figures" % (rung, name, CA.label_set(s_), 100 * v[(2027, 7)], figs))
        return s_, figs
    ladder = {"R0 Erlang C": easy, "R1a fiscal 2026 observed carried forward": carried, "R1b own forecast": own,
              "R2 the late shift's hang-ups' own waits": CA.fy2028(fc, busy, wab),
              "R2 every hang-up's own wait": CA.fy2028(fc, busy, wab_all),
              "R2b one patience for every call": CA.fy2028(fc, busy, pat_all), "R3 golden": gold}
    for k_, v in ladder.items():
        show(k_, v, "ladder")
    ck("ladder rung 0 files May to September", CA.short_months(ladder["R0 Erlang C"]) ==
       [(2027, 7), (2027, 8), (2027, 9), (2028, 5), (2028, 6)])
    ck("ladder rungs 1a, 1b and the late shift's hang-ups' waits file no month short",
       all(CA.short_months(ladder[k]) == [] for k in ("R1a fiscal 2026 observed carried forward", "R1b own forecast",
                                                        "R2 the late shift's hang-ups' own waits")))
    ck("ladder every hang-up's own wait files July alone or none, every month 0.15 or more from 90",
       CA.short_months(ladder["R2 every hang-up's own wait"]) in ([], [(2027, 7)])
       and min(abs(100 * x - 90) for x in ladder["R2 every hang-up's own wait"].values()) >= 0.15,
       "%.1f s: %s" % (wab_all, CA.label_set(CA.short_months(ladder["R2 every hang-up's own wait"]))))
    ck("ladder one patience for every call files May to September, every month 0.5 or more from 90",
       CA.short_months(ladder["R2b one patience for every call"]) == [(2027, 7), (2027, 8), (2027, 9), (2028, 5), (2028, 6)]
       and min(abs(100 * x - 90) for x in ladder["R2b one patience for every call"].values()) >= 0.5,
       "%.1f s" % pat_all)
    ck("ladder the decisive step reverses the hang-ups' waits' direction",
       ladder["R2 the late shift's hang-ups' own waits"][(2027, 7)] > gold[(2027, 7)] > easy[(2027, 7)])
    worst0 = min(100 * (gold[ym] - easy[ym]) for ym in FY28)
    ck("ladder rung 0's figures all below the golden's by at least 1.0", worst0 >= 1.0, "%.2f" % worst0)
    pooled = {"the late block, every night": C.lateblock, "nights 22:00 to 06:00, every night": C.lateblock | ((C.lhour >= 2) & (C.lhour < 6)),
              "Friday and Saturday 18:00 to 02:00": late | ((C.lhour >= 18) & (C.lhour < 22) & np.isin(C.lwd, [4, 5]))}
    for nm_, msk in pooled.items():
        p_ = CA.estimates(C, msk)[1]
        v = CA.fy2028(fc, busy, p_)
        show("one patience over %s (%.1f s)" % (nm_, p_), v, "pool")
        ck("rival one patience over %s files another set, every month 0.3 or more from 90" % nm_,
           CA.short_months(v) != want and min(abs(100 * x - 90) for x in v.values()) >= 0.3, CA.label_set(CA.short_months(v)))
    grid = {"own forecast with Erlang C": CA.fy2028(fc, busy, pat, model="C", use_halvorsen=False),
            "own forecast with the late shift's hang-ups' own waits": CA.fy2028(fc, busy, wab, use_halvorsen=False),
            "own forecast with one patience for every call": CA.fy2028(fc, busy, pat_all, use_halvorsen=False),
            "the board's forecast, Erlang C with five call-takers": CA.fy2028(fc, busy, pat, model="C", c=5)}
    for k_, v in grid.items():
        show(k_, v, "grid")
        ck("grid %s files another set" % k_, CA.short_months(v) != want, CA.label_set(CA.short_months(v)))
    # the calibration routes: a correction of the standard queue, or one patience, fitted to the agency's own history
    ros = CA.read_roster(target, R.F_ROSTER)
    H = Hist(C, ros)
    cC = CA.fy2028(fc, busy, pat, model="C")
    wins = {"fiscal 2026, every hour": lambda h: h[4] == 2026, "the whole history, every hour": lambda h: True,
            "January to June 2025, every hour": lambda h: h[0] == 2025 and h[1] <= 6,
            "06:00 to 22:00": lambda h: 6 <= h[2] < 22, "the four-call-taker hours": lambda h: h[6] == 4,
            "the Sunday to Thursday late block (four)": lambda h: (h[2] >= 22 or h[2] < 2) and not h[5]}
    late_wins = {"the whole history": lambda h: True, "fiscal 2026": lambda h: h[4] == 2026,
                 "calendar 2025": lambda h: h[0] == 2025, "January to June 2025": lambda h: h[0] == 2025 and h[1] <= 6,
                 "June 2025 to September 2026": lambda h: (h[0], h[1]) >= (2025, 6),
                 "the last twelve months": lambda h: (h[0], h[1]) >= (2025, 10),
                 "January to September 2026": lambda h: h[0] == 2026,
                 "the June to September months": lambda h: h[1] in (6, 7, 8, 9)}
    for k_, s_ in late_wins.items():
        wins["the late shift at five, " + k_] = lambda h, s_=s_: h[5] and s_(h)
    # the late shift's own history at five call-takers holds 46 to 184 misses a window: a scalar correction of the
    # standard queue fitted there is noisy, and three of its sixteen cells land the set by sampling (design note)
    known = {("the late shift at five, fiscal 2026", "miss-rate"), ("the late shift at five, fiscal 2026", "busy"),
             ("the late shift at five, January to September 2026", "miss-rate")}
    landers = set()
    G["calibration"] = {}
    for nm_, sel in wins.items():
        Gw = H.groups(sel)
        o, ab_o = H.obs(Gw)
        pcw = H.predC(Gw, busy)
        f_ = (1 - o) / (1 - pcw)
        miss = {ym: 1 - f_ * (1 - cC[ym]) for ym in FY28}
        bcal = brentq(lambda b: H.predC(Gw, b) - o, 120.0, 320.0, xtol=0.05)
        busyfit = CA.fy2028(fc, bcal, pat, model="C")
        res = {"miss-rate factor %.3f" % f_: miss, "busy time %.1f s" % bcal: busyfit}
        try:
            p1 = brentq(lambda p: H.predA(Gw, busy, p)[0] - o, 15.0, 30000.0, xtol=0.5)
            res["one patience to its compliance, %.0f s" % p1] = CA.fy2028(fc, busy, p1)
        except ValueError:
            pass
        for lab, v in res.items():
            s_, figs = show("%s on %s" % (lab, nm_), v, "cal")
            G["calibration"][(nm_, lab)] = (s_, figs, v)
        if "late shift" not in nm_:
            for lab, v in res.items():
                ck("calibration %s on %s files another set" % (lab.split(" ")[0] + " " + lab.split(" ")[1], nm_),
                   CA.short_months(v) != want, "%s: %s" % (lab, CA.label_set(CA.short_months(v))))
        else:
            for lab in list(res)[:2]:
                if CA.short_months(res[lab]) == want:
                    landers.add((nm_, lab.split(" ")[0]))
                if (nm_, lab.split(" ")[0]) not in known:
                    ck("calibration %s on %s files another set" % (lab.split(" ")[0] + " " + lab.split(" ")[1], nm_),
                       CA.short_months(res[lab]) != want, "%s: %s" % (lab, CA.label_set(CA.short_months(res[lab]))))
    ck("calibration the late shift at five: the scalar corrections land in at most 3 of 16 windows (fiscal 2026 both, "
       "January to September 2026 the miss-rate factor)", landers <= known,
       "%d land: %s" % (len(landers), "; ".join("%s, %s" % x for x in sorted(landers))))
    G["calibration_landers"] = sorted(landers)
    for wt in ("calls", "groups"):
        lo_ = logistic_route(H, busy, fc, pat, weight=wt, slope=False)
        show("logit offset on Erlang C, every hour, weighted by %s" % wt, lo_, "cal")
        ck("calibration a logit offset on Erlang C over every hour (weighted by %s) files another set" % wt,
           CA.short_months(lo_) != want, CA.label_set(CA.short_months(lo_)))
        lg = logistic_route(H, busy, fc, pat, weight=wt, slope=True)
        s_, figs = show("logistic recalibration of Erlang C, every hour, weighted by %s" % wt, lg, "cal")
        G["calibration"][("every hour", "logistic, %s" % wt)] = (s_, figs, lg)
    em = empirical_route(H, fc)
    show("empirical curve of compliance on calls, the four-call-taker hours", em, "emp")
    ck("empirical compliance against hourly calls on the four-call-taker hours files another set",
       CA.short_months(em) != want, CA.label_set(CA.short_months(em)))

    # ------------------------------------------------------------------------------------------------ back-test
    bt = G["backtest"]
    ck("back-test the late shift's fiscal 2026 hang-ups: one patience for every call predicts under half of them",
       bt["late"]["ab_A1"] < 0.5 * bt["late"]["ab_obs"], "obs %.3f%%, one patience %.3f%%" % (100 * bt["late"]["ab_obs"], 100 * bt["late"]["ab_A1"]))
    ck("back-test the late shift's fiscal 2026 hang-ups: its own patience predicts them within a third",
       abs(bt["late"]["ab_A"] / bt["late"]["ab_obs"] - 1) < 0.34, "obs %.3f%%, own patience %.3f%%" % (100 * bt["late"]["ab_obs"], 100 * bt["late"]["ab_A"]))
    ck("back-test the whole floor: each segment's patience within 0.3 of fiscal 2026, Erlang C under it by more than 0.5",
       abs(bt["all"]["A"] - bt["all"]["obs"]) < 0.003 and bt["all"]["obs"] - bt["all"]["C"] > 0.005,
       "obs %.2f A %.2f C %.2f" % (100 * bt["all"]["obs"], 100 * bt["all"]["A"], 100 * bt["all"]["C"]))
    seg = G["segments"]
    labs = list(seg)
    ck("the late shift's patience is under half of every other segment's",
       all(seg[labs[0]][3] < 0.5 * seg[k][3] for k in labs[2:]), " ".join("%.0f" % seg[k][3] for k in labs))

    # ------------------------------------------------------------------------------------------------ R2 mess neutral
    ck("R2 the legacy layout dropped from the estimates: same call (SF11 busy time, SF12 i3 layout)", True)
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
        b3, p3 = CA.estimates(C3)[0], CA.estimates(C3, C3.late)[1]
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
def km_patience(C, mask=None):
    """Kaplan-Meier on the 911 calls' waits (a hang-up is the event, an answer censors), and the exponential that fits
    its cumulative hazard over the first three minutes."""
    m = C.is911 if mask is None else (C.is911 & mask)
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


def hazard_patience(C, mask=None):
    m = C.is911 if mask is None else (C.is911 & mask)
    w, ev = C.wait[m], C.ab[m]
    edges = np.arange(0, 1200, 30.0)
    tot_ev = tot_exp = 0.0
    for a in edges:
        expo = np.clip(w - a, 0, 30.0).sum()
        e = np.sum(ev & (w >= a) & (w < a + 30.0))
        tot_ev += e
        tot_exp += expo
    return tot_exp / tot_ev


class Hist:
    """The history by clock hour, grouped (year, month, hour, weekday, call-takers) with each group's mean count as
    its rate (the back-test's convention), for the calibration routes."""

    def __init__(self, C, ros):
        self.t0 = K.HIST_START.astimezone(K.UTC).timestamp()
        self.nh = int(round((K.HIST_END.astimezone(K.UTC).timestamp() - self.t0) / 3600))
        self.cnt, self.ok15, self.ab5, self.abn = CA.hourly(C, self.t0, self.nh)
        self.HT = CA.hour_table(ros, self.t0, self.nh)

    def groups(self, select):
        g = {}
        for k in range(self.nh):
            if select(self.HT[k]):
                y, mo, h, wd, fy, late, c = self.HT[k]
                g.setdefault((y, mo, h, wd, c), []).append(k)
        return {key: np.array(ks) for key, ks in g.items()}

    def obs(self, Gw):
        num = sum(self.ok15[ks].sum() for ks in Gw.values())
        den = sum(self.cnt[ks].sum() - self.ab5[ks].sum() for ks in Gw.values())
        ab = sum(self.abn[ks].sum() for ks in Gw.values())
        n = sum(self.cnt[ks].sum() for ks in Gw.values())
        return num / den, ab / n

    def predC(self, Gw, busy):
        mu = 3600.0 / busy
        num = n = 0.0
        for (y, mo, h, wd, c), ks in Gw.items():
            lam = self.cnt[ks].mean()
            num += len(ks) * lam * E.erlang_c(lam, mu, c)
            n += len(ks) * lam
        return num / n

    def predA(self, Gw, busy, pat):
        mu, th = 3600.0 / busy, 3600.0 / pat
        num = den = ab = n = 0.0
        for (y, mo, h, wd, c), ks in Gw.items():
            lam = self.cnt[ks].mean()
            w = len(ks) * lam
            st, a5, pab = E.erlang_a(lam, mu, th, c)[:3]
            num += w * st
            den += w * (1 - a5)
            ab += w * pab
            n += w
        return num / den, ab / n


def _logit(p):
    p = min(max(p, 0.5), 0.99995)
    return math.log(p / (1 - p))


def logistic_route(H, busy, fc, pat, weight="calls", slope=True):
    """Erlang C recalibrated on the history: logit(observed) on logit(Erlang C) over every hour group (weighted by
    calls or by group), with a free slope or an offset alone, applied hour by hour to the FY2028 forecast at four
    call-takers."""
    Gw = H.groups(lambda h: True)
    mu = 3600.0 / busy
    xs, ys, ws = [], [], []
    for (y, mo, h, wd, c), ks in Gw.items():
        den = H.cnt[ks].sum() - H.ab5[ks].sum()
        if den <= 0:
            continue
        o = H.ok15[ks].sum() / den
        lam = H.cnt[ks].mean()
        xs.append(_logit(E.erlang_c(lam, mu, c)))
        ys.append(_logit(o))
        ws.append(H.cnt[ks].sum() if weight == "calls" else 1.0)
    xs, ys, ws = np.array(xs), np.array(ys), np.array(ws)
    if slope:
        X = np.vstack([np.ones_like(xs), xs]).T
        Wm = np.diag(ws)
        a, b = np.linalg.solve(X.T @ Wm @ X, X.T @ Wm @ ys)
    else:
        a, b = float(np.sum(ws * (ys - xs)) / np.sum(ws)), 1.0
    out = {}
    for y, m in FY28:
        num = den = 0.0
        for nd, cells in M.night_cells(y, m):
            for dow, hh in cells:
                lam = fc[(y, m, dow, hh)][0]
                z = a + b * _logit(E.erlang_c(lam, mu, 4))
                num += lam / (1 + math.exp(-z))
                den += lam
        out[(y, m)] = num / den
    return out


def empirical_route(H, fc):
    """Observed compliance against the hour's realised calls on the four-call-taker hours, made non-increasing (pool
    adjacent violators), and each forecast hour's expected compliance under Poisson counts at its forecast rate."""
    from scipy.stats import poisson
    num, den = {}, {}
    for k in range(H.nh):
        if H.HT[k][6] != 4 or H.cnt[k] <= 0:
            continue
        n = int(H.cnt[k])
        num[n] = num.get(n, 0.0) + H.ok15[k]
        den[n] = den.get(n, 0.0) + H.cnt[k] - H.ab5[k]
    ns = sorted(den)
    vals = [[num[n] / den[n], den[n], [n]] for n in ns]
    i = 0
    while i < len(vals) - 1:
        if vals[i][0] < vals[i + 1][0]:
            v0, w0, n0 = vals[i]
            v1, w1, n1 = vals[i + 1]
            vals[i] = [(v0 * w0 + v1 * w1) / (w0 + w1), w0 + w1, n0 + n1]
            del vals[i + 1]
            i = max(i - 1, 0)
        else:
            i += 1
    curve = {}
    for v, w, members in vals:
        for n in members:
            curve[n] = v
    cx = np.array(sorted(curve), dtype=float)
    cy = np.array([curve[int(x)] for x in cx])
    out = {}
    for y, m in FY28:
        nm_ = dm_ = 0.0
        for nd, cells in M.night_cells(y, m):
            for dow, hh in cells:
                lam = fc[(y, m, dow, hh)][0]
                ks = np.arange(1, int(lam * 3 + 30))
                pk = poisson.pmf(ks, lam)
                cv = np.interp(ks.astype(float), cx, cy)
                nm_ += float(np.sum(pk * ks * cv))
                dm_ += float(np.sum(pk * ks))
        out[(y, m)] = nm_ / dm_
    return out


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
    stops = {"S1 the cracker (handset fix, the first part's outer ring, URIs naming Wexley, the call identifier)":
             CA.ask_a(C, che, polys, dr, holes=False, all_parts=False, xfer="name", key="callid"),
             "S2 the routing location": CA.ask_a(C, che, polys, dr, fix="first"),
             "S3 full geometry, URIs naming Wexley": CA.ask_a(C, che, polys, dr, xfer="name"),
             "S4 quarters by UTC date": CA.ask_a(C, che, polys, dr, quarter="utc"),
             "S5 every other step right, records joined on the call identifier alone":
             CA.ask_a(C, che, polys, dr, key="callid"),
             "S6 full geometry and the directory, URIs naming Wexley, the call identifier alone":
             CA.ask_a(C, che, polys, dr, xfer="name", key="callid")}
    need = {"S1": 8, "S2": 8, "S3": 4, "S4": 4, "S5": 8, "S6": 8}
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
    # device A4: calls answered from the backup centre have their location records filed under the incident identifier
    bk = {(2026, q): [0, 0] for q in (1, 2, 3, 4)}
    for i in np.nonzero(np.isin(W.area, ["main", "detached"]))[0]:
        if not (lo <= W.t[i] < hi) or R.in_legacy(W, i) or W.kind[i] != "wireless":
            continue
        q = K.fiscal_quarter(K.to_local(W.t[i]).date())
        if K.at_backup(W.t[i]):
            bk[q][0] += 1
            bk[q][1] += int(W.xout[i] == "wexley")
    shares = [bk[q][0] / A[q][0] for q in A]
    ck("Ask A device A4: Halvorsen calls whose records the backup centre filed under the incident identifier, in every "
       "quarter and unevenly (1 to 8 per cent of a quarter's calls, the largest share twice the smallest or more)",
       all(0.01 <= x <= 0.08 for x in shares) and max(shares) >= 2 * min(shares),
       "%s; shares %s" % ({q: tuple(v) for q, v in bk.items()}, " ".join("%.3f" % x for x in shares)))
    cids, iids = set(C.cid[C.layout == "i3"]), set(C.iid[C.layout == "i3"])
    by_c = sum(k in cids for k in che)
    by_i = sum(k in iids for k in che)
    ck("Ask A device A4 is fair: every location record's call_id is one i3 call's callId or incidentId, never both",
       by_c + by_i == len(che) and not (cids & iids), "%d keys: %d call identifiers, %d incident identifiers (%.1f%%)" % (
           len(che), by_c, by_i, 100.0 * by_i / len(che)))
    queues = set()
    with open(os.path.join(target, R.F_I3), encoding="utf-8") as fh:
        for line in fh:
            queues.add(json.loads(line)["queue"])
    ck("Ask A device A4 carries no marker: every i3 call names the same queue and carries both identifiers",
       len(queues) == 1 and all(x for x in C.iid[C.layout == "i3"]), ", ".join(sorted(queues)))
    first_cell = all(recs[0][1] == "cell" for recs in che.values())
    ck("Ask A pin's subject: every call's first record is its routing location", first_cell)
    readme = open(os.path.join(target, DOC.F_README), encoding="utf-8").read()
    ck("Ask A pin: the agency places a wireless call by the last handset location received (README); the routing record "
       "alternative is stop S2", "places a wireless call by the last handset location received for it" in readme)
    wex = [u for u, ag in dr.items() if ag == K.NEIGHBOUR]
    ck("Ask A pin: the ESInet directory files Wexley's alternate URI under Wexley County Emergency Communications; the "
       "primary-only alternative is stop S3", len(wex) == 2 and any("alt07" in u for u in wex), ", ".join(sorted(wex)))
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
    readme = open(os.path.join(target, DOC.F_README), encoding="utf-8").read()
    sop = " ".join(DOC.sop_sentences())
    off_ = lambda v: sum(K.round_half_up(100 * v[k], 1) != K.round_half_up(100 * Bm[k], 1) for k in Bm)
    show_ = lambda v: str({k[1]: round(100 * x, 2) for k, x in v.items()})
    # the pins, each with the alternative it closes
    ck("Ask B pin: every abandoned 911 call is called back, however briefly the caller held on (SOP 2.10 7.1)",
       "every abandoned 911 call is called back by the callback desk, however briefly the caller held on" in sop.lower())
    v = CA.ask_b(C, tasks, misdials=False)[0]
    ck("Ask B pin's alternative: abandons within 5 seconds left out moves 4 or more months", off_(v) >= 4, "%d off: %s" % (off_(v), show_(v)))
    ck("Ask B pin: a task closed as caller called in was never dialled (README)",
       "a task closed as `caller called in` was never dialled" in readme.lower())
    v = CA.ask_b(C, tasks, called_in="dialled")[0]
    ck("Ask B pin's alternative: caller-called-in tasks counted as dialled back moves 4 or more months", off_(v) >= 4,
       "%d off: %s" % (off_(v), show_(v)))
    ck("Ask B pin: one open task per callback number, a further abandon joins it (README)",
       "the desk works one open task per callback number" in readme.lower() and "joins that task and opens none of its own" in readme.lower())
    for k_, v in {"tasks keyed on their opening call, the unjoined counted as not dialled back": CA.ask_b(C, tasks, match="ref")[0],
                  "tasks keyed on their opening call, the unjoined dropped": CA.ask_b(C, tasks, match="ref", unmatched="drop")[0]}.items():
        ck("Ask B pin's alternative: %s moves 3 or more months" % k_, off_(v) >= 3, "%d off: %s" % (off_(v), show_(v)))
    # the silent devices
    v = CA.ask_b(C, tasks, lines911=True)[0]
    ck("Ask B device B4: the 911 tasks alone (the administrative line's open tasks dropped) misses 6 of 6", off_(v) == 6,
       "%d off: %s" % (off_(v), show_(v)))
    for k_, v in {"S3 opening-call keys, two minutes from the task's stamp": CA.ask_b(C, tasks, match="ref", anchor="created")[0],
                  "S4 the task log alone, tasks as the unit": CA.ask_b(C, tasks, match="tasks")[0],
                  "S6 two minutes from the task's stamp": CA.ask_b(C, tasks, anchor="created")[0]}.items():
        ck("Ask B device B2 %s misses 5 or more of 6" % k_, off_(v) >= 5, "%d off: %s" % (off_(v), show_(v)))
    xl = {}
    for task in W.cb_tasks:
        if task["line"] != "ADMIN" or task["first_dial"] is None:
            continue
        for (l_, idx, th) in task["members"]:
            if l_ == "911" and 0.0 <= task["first_dial"] - th <= 120.0:
                loc = K.to_local(th)
                xl[(loc.year, loc.month)] = xl.get((loc.year, loc.month), 0) + 1
    ck("Ask B device B4: 911 abandons dialled back by an administrative-line task in every month",
       all(xl.get(k, 0) >= 1 for k in Bm), str({k[1]: xl.get(k, 0) for k in Bm}))
    for tol in (25.0, 45.0, 90.0, 300.0):
        ck("Ask B matching window %.0f s: same figures" % tol, CA.ask_b(C, tasks, tol=tol)[0] == Bm)
    edge = min(abs(100 * Bm[k] * 10 - math.floor(100 * Bm[k] * 10) - 0.5) for k in Bm)
    ck("Ask B no month on a one-decimal rounding edge", edge > 0.02, "%.3f" % edge)
    ck("realism no ask share a whole number and no ask count a multiple of 100",
       all(abs(100 * Bm[k] - round(100 * Bm[k])) > 0.05 for k in Bm) and all(v % 100 for q in A for v in A[q]),
       "%s %s" % ({k: round(100 * v, 2) for k, v in Bm.items()}, A))
    rep = {}
    for task in W.cb_tasks:
        for (line, idx, th) in task["members"][1:]:
            if line != "911":
                continue
            loc = K.to_local(th)
            rep[(loc.year, loc.month)] = rep.get((loc.year, loc.month), 0) + 1
    tot_rep, tot_den = sum(rep.values()), sum(G["ask_b_den"].values())
    ck("Ask B 911 abandons joined to an open task (a 911 or an administrative-line one) in every month (the linkage pin bites)",
       all(rep.get(k, 0) >= 1 for k in Bm), "%s, %.1f%% overall" % ({k: rep.get(k, 0) for k in Bm}, 100.0 * tot_rep / tot_den))
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
        hs = [r for r in (che.get(C.cid[i]) or che.get(C.iid[i], [])) if r[1] != "cell"]
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
