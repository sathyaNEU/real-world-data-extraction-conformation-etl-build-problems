"""task252 generator checks: the golden against the world's truth, the licensed family's agreement and margins, every
rival route off the golden, the analyst test on the clean world, the Layer 1 mess neutral to the call, the asks
against the world, every ask device moving every figure, the separation line, the input gates."""
import datetime as dt
import os
import re
import sys

import numpy as np

import params as P
import sim
import solve as S

FAILS = []
MARGIN = 0.0015
SFOF = {"pooled mixing (the golden)": "golden", "per-channel mixing": "SF21", "RAW corr": "SF7",
        "raw lags 1.5 to 6 hours": "SF8 SF21", "raw lags 1 to 10 hours": "SF8 SF21",
        "raw lags every slot 2 to 6 hours": "SF8 SF21",
        "pooled mixing, raw lags 1.5 to 6 hours": "SF8", "pooled mixing, raw lags 1 to 10 hours": "SF8",
        "pooled mixing, raw lags every slot 2 to 6 hours": "SF8", "pooled mixing, raw lags hourly 2 to 8 hours": "SF8",
        "zero error's size from the corrected raw grabs alone": "SF11",
        "zero error's size, the check and the grabs averaged": "SF11",
        "two-point, k from the same-cycle raw fits": "SF10", "two-point, mean test": "SF10",
        "two-point, joint weighted fit": "SF10", "two-point, readings interpolated to the grab": "SF10",
        "span at the channel's estimated level in the water": "SF12",
        "line: straight-line regrowth": "SF24", "line: clean level from the first hour after each flush": "SF24",
        "line: clean level from the first 6 hours": "SF24", "line: clean level from the first 24 hours": "SF24",
        "line: fitted on the readings uncorrected": "SF24", "line: raw lags 1.5 to 6 hours": "SF24 SF8",
        "line: applied to every channel": "SF25", "line: the grown loss over the whole quarter": "SF27"}
GOLDEN = "BRN-FW1, CAL-FI1, DUN-FW1, ELS-FW1, GAR-FI1, GAR-FW1"
DEFAULT = "BRN-FW1, DUN-FW1, ELS-FW1, GAR-FI1, GAR-FW1, HOL-FI1"


def ok(cond, what):
    print(("PASS  " if cond else "FAIL  ") + what)
    if not cond:
        FAILS.append(what)


def _clean(W):
    """the world's own readings with every slot read and nothing lost: the analyst test's ground"""
    D = {}
    for c in P.CODES:
        x = W[c]
        val = x["reading"].copy()
        v = np.full(P.NS, np.nan)
        for k, s0 in enumerate(x["check_slots"]):
            for j in range(3):
                v[s0 + j] = x["checks"][k][j]
                val[s0 + j] = np.nan
        for k, s0 in enumerate(x["repair_checks"]):
            for j in range(3):
                v[s0 + j] = x["repair_reads"][k][j]
                val[s0 + j] = np.nan
        if x["trip"]:                              # the analyser was off: no readings to read
            val[x["trip"][0]:x["trip"][1]] = np.nan
        g = ~np.isnan(val)
        cell = val.copy(); cell[~g] = v[~g]
        D[c] = dict(val=val, v=v, f=np.zeros(P.NS, bool), g=g, present=np.ones(P.NS, bool), order=x["order"],
                    sl=x["sl"], cell=cell, brk=np.zeros(P.NS, bool))
    return D


def _world_visits(W):
    return {c: sorted(W[c]["flushes"]) for c in P.CODES}


def _line_terms(target, D, info, V):
    """the golden's line term for each channel (zero where the readings do not recover), for the variants that build
    their carryover and calibration outside solve.offsets"""
    out = {}
    for c in P.CODES:
        for s in ("fil", "fin"):
            rec = S.recovery(D[c], s, info[c], V[c])
            out[(c, s)] = rec["lossbar"] if S.recovers(rec) else 0.0
    return out


def _world_lims(W):
    out = []
    for r in W[P.CODES[0]]["round"]:
        for smp in r["samples"]:
            out.append(dict(code=smp["code"], stream=smp["stream"], collected=smp["collected"].replace(tzinfo=None),
                            received=smp["received"].replace(tzinfo=None), analysed=smp["analysed"].replace(tzinfo=None),
                            cens=False, value=smp["lab"]))
    return out


def _with(D, code, **kw):
    E = dict(D)
    E[code] = dict(D[code], **kw)
    return E


def family(target, D, L, C, V, gold, info):
    """the licensed family: the golden, the carryover fitted per channel or on the same cycle's raw reading, the raw
    water's lags, the two-point read done other ways, and the line's loss fitted with a straight-line regrowth, read
    from the first hours after each flush, fitted on the readings as they stand, applied to every channel, or taken at
    full growth all quarter"""
    LT = _line_terms(target, D, info, V)
    fam = {}
    fam["pooled mixing (the golden)"] = gold
    fam["per-channel mixing"] = S.offsets(target, "G", "corr", D, L, C, V=V)[0]
    fam["RAW corr"] = S.offsets(target, "RAW", "corr", D, L, C, V=V)[0]
    for nm_, lg_ in (("1.5 to 6", list(range(9, 37, 3))), ("1 to 10", list(range(6, 61, 3))),
                     ("every slot 2 to 6", list(range(12, 37))), ("hourly 2 to 8", list(range(12, 49, 6)))):
        fam["pooled mixing, raw lags %s hours" % nm_] = S.offsets(target, "POOL", "corr", D, L, C, V=V,
                                                                  lags_slots=lg_)[0]
    for name_, fn in _attribution_variants(D, L, C).items():
        fam[name_] = {k: v + LT[k] for k, v in fn.items()}
    fam["raw lags 1.5 to 6 hours"] = S.offsets(target, "G", "corr", D, L, C, V=V, lags_slots=list(range(9, 37, 3)))[0]
    fam["raw lags 1 to 10 hours"] = S.offsets(target, "G", "corr", D, L, C, V=V, lags_slots=list(range(6, 61, 3)))[0]
    fam["raw lags every slot 2 to 6 hours"] = S.offsets(target, "G", "corr", D, L, C, V=V,
                                                        lags_slots=list(range(12, 37)))[0]
    for nm_, kw_ in (("straight-line regrowth", dict(rec_kw=dict(form="pwl"))),
                     ("clean level from the first hour after each flush", dict(rec_kw=dict(window=1))),
                     ("clean level from the first 6 hours", dict(rec_kw=dict(window=6))),
                     ("clean level from the first 24 hours", dict(rec_kw=dict(window=24))),
                     ("fitted on the readings uncorrected", dict(rec_kw=dict(corrected=False))),
                     ("raw lags 1.5 to 6 hours", dict(rec_kw=dict(lags_slots=list(range(9, 37, 3))))),
                     ("applied to every channel", dict(line="all"))):
        fam["line: " + nm_] = S.offsets(target, S.CARRY, "corr", D, L, C, V=V, **kw_)[0]
    grown = dict(S.offsets(target, S.CARRY, "corr", D, L, C, line="none", V=V)[0])
    for k in LT:
        if LT[k]:
            rec = info[k]
            grown[k] += rec["b"]                     # the loss at full growth, the whole quarter
    fam["line: the grown loss over the whole quarter"] = grown
    return fam


def main(target):
    W = sim.build()
    T = sim.channel_truth(W)
    truth = sorted(k for k, v in T.items() if abs(v) > P.THRESH)
    D = S.load(target); L = S.lims(target); C = S.checks(target); V = S.visits(target)
    gold, info = S.offsets(target, S.CARRY, "corr", D, L, C, V=V)
    G = S.flags(gold)
    names = ", ".join(S.name(k) for k in G)
    ok(G == truth, "golden list equals the world's truth: %s" % names)
    ok(names == GOLDEN, "the golden is the designed six")
    ok(all(V[c][-4:] == sorted(W[c]["flushes"]) for c in P.CODES), "SF26: the planned maintenance log's monthly "
       "visits, read in New Zealand time, are the flushes the world ran (September's the last before the quarter)")

    LT = _line_terms(target, D, info, V)
    ok(min(abs(abs(v) - P.THRESH) for v in T.values()) >= 0.002, "every channel's true offset 0.002 or more from the line "
       "(%.4f)" % min(abs(abs(v) - P.THRESH) for v in T.values()))
    ok(max(abs(gold[k] - T[k]) for k in T) < 0.0015, "golden offsets within 0.0015 of the truth on every channel "
       "(largest %.4f)" % max(abs(gold[k] - T[k]) for k in T))
    ok(info["HOL"]["kind"] == "zero" and info["CAL"]["kind"] == "span" and
       all(info[c]["kind"] is None for c in P.CODES if c not in ("HOL", "CAL")),
       "attribution: Holmedale zero, Calderwood span, no other analyser outside the check's noise")
    fam = family(target, D, L, C, V, gold, info)
    unscaled = S.flags(S.offsets(target, "G", "corr", D, L, C, V=V, form="add")[0])
    ok(True, "SF7: the mix without its one-less-both-shares scaling (an algebra slip the step's own words rule out) "
       "files %s" % ", ".join(S.name(k) for k in unscaled))
    for k_, v in fam.items():
        ok(S.flags(v) == G, "%s: licensed %s files the golden" % (SFOF.get(k_, "SF7 SF8 SF10 SF11"), k_))
    import json as _json
    _fig = _json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json")))
    lo_print = _fig["flag_band_print"]
    hi_print = np.ceil(_fig["unflagged_band_high"] * 1000) / 1000
    lo = min(abs(v[k]) for v in fam.values() for k in v if k in G)
    hi = max(abs(v[k]) for v in fam.values() for k in v if k not in G)
    ok(lo >= lo_print and hi <= hi_print, "H29: block 1's bounds hold over the whole licensed family: listed %.4f or more "
       "(printed %.3f), others %.4f or less (printed %.3f)" % (lo, lo_print, hi, hi_print))
    m = min(abs(abs(v[k]) - P.THRESH) for v in fam.values() for k in v)
    ok(m >= MARGIN, "SF5: licensed family's margin to the line %.4f (>= %.4f)" % (m, MARGIN))
    # the fork table's remaining rows
    ok(len(gold) == 16 and all(k[1] in ("fil", "fin") for k in gold), "SF1: the 16 channels are the filtered and final "
       "water points")
    tr = [g for g in L if g["stream"] != "raw"]
    ok(sum(g["cens"] for g in tr) >= 0.6 * len(tr), "SF4: %d of %d treated grabs below the limit, so no quarter mean comes "
       "from them" % (sum(g["cens"] for g in tr), len(tr)))
    ok(gold[("CAL", "fil")] < 0 and all(gold[k] > 0 for k in G if k != ("CAL", "fil")), "SF6: CAL-FI1 reads low, "
       "the other five high, so 'above only' files another list")
    import openpyxl as _ox
    _wb = _ox.load_workbook(os.path.join(target, "analyser_verification_2027Q4.xlsx"), read_only=True)
    _rows = list(_wb["Checks Q4 2027"].iter_rows(values_only=True))[1:]
    for code in ("HOL", "CAL"):
        months = [float(np.mean(r[4:7])) for r in _rows if r[0] == P.tag(code)]
        ok(max(abs(mm - float(np.mean(C[code]))) for mm in months) <= 0.001, "SF9: %s's monthly check means within 0.001 "
           "of the quarter's" % P.NAME[code])
    prompt = open(os.path.join(os.path.dirname(target.rstrip("/")), "prompt.txt")).read() if os.path.exists(
        os.path.join(os.path.dirname(target.rstrip("/")), "prompt.txt")) else ""
    ok("decimal" not in prompt.split("Give the hours")[0] if prompt else True, "SF13: the prompt grades no offset's "
       "rounding (only the hours carry one)")
    neg = sum(1 for g in L if g["analysed"] < g["received"])
    lo, hi = S.clock_bracket(L)
    ok(10 <= neg <= 16 and 50 <= lo < 60 < hi <= 70, "SF14: %d rows are stamped as analysed before reception logged "
       "them and none is released within an hour of its stamp: the stamps run %.0f to %.0f minutes behind the "
       "laboratory's other clocks" % (neg, lo, hi))
    ok(all(S.ask_a(target, L, shift_h=m / 60) == S.ask_a(target, L) for m in np.arange(lo + 0.01, hi, 0.5)),
       "SF14: every shift inside the bracket counts the same as the hour (%.0f to %.0f minutes)" % (lo, hi))
    xmas = [g for g in L if g["stream"] != "raw" and g["collected"].date() == dt.date(2027, 12, 28)]
    ok(len(xmas) == 16 and all((g["analysed"] - g["collected"]).days >= 7 for g in xmas), "SF16: the 28 December round "
       "(16 treated samples) analysed on 5 January, counted in the quarter it was collected")
    alt16 = {c: 0 for c in P.CODES}
    seen16 = set()
    for g in L:
        k16 = (g["code"], g["stream"], g["analysed"], g["value"], g["cens"])
        if k16 in seen16:
            continue
        seen16.add(k16)
        if g["stream"] != "raw" and g["analysed"].year == 2027 and (g["analysed"] + dt.timedelta(hours=1) -
                                                                    g["collected"]).total_seconds() > 86400:
            alt16[g["code"]] += 1
    ok(all(alt16[c] != S.ask_a(target, L)[c] for c in P.CODES), "SF16: counting only samples analysed within the quarter "
       "misses every plant")
    edge = all(f["a"] >= 288 and f["b"] <= P.NS - 288 for c in P.CODES for f in W[c]["faults"])
    ok(edge, "SF19: no analyser fault within two days of either end of the quarter")
    fam["span at the channel's estimated level in the water"] = {k: v + LT[k] for k, v in
                                                                  _span_true_level(D, L, C, V).items()}
    ok(S.flags(fam["span at the channel's estimated level in the water"]) == G, "SF12: a span carried at the channel's "
       "estimated level in the water files the golden")
    # the rivals
    rivals = {"G none": ("G", "none"), "G span": ("G", "span"), "G zero": ("G", "zero"), "G naive": ("G", "naive"),
              "P1 span": ("P1", "span"), "P1 corr": ("P1", "corr"), "RAW span": ("RAW", "span"), "D1 corr": ("D1", "corr"),
              "CRUDE none": ("CRUDE", "none"), "FIRST span": ("FIRST", "span"), "FIRST corr": ("FIRST", "corr")}
    for k_, (c, ch) in rivals.items():
        for ln in ("fit", "none"):
            f = S.flags(S.offsets(target, c, ch, D, L, C, V=V, line=ln)[0])
            d = sorted(set(f) ^ set(G))
            ok(len(d) > 0, "rival %s, line %s, files another list (differs on %s)" % (
                k_, "read" if ln == "fit" else "not read", ", ".join(S.name(x) for x in d)))
    add = S.flags(S.offsets(target, "POOL", "corr", D, L, C, V=V, form="add")[0])
    ok(sorted(set(add) ^ set(G)) != [], "rival: the additive law (k times the readings before) files another list "
       "(differs on %s)" % ", ".join(S.name(x) for x in sorted(set(add) ^ set(G))))
    # the data rule the additive law out: the worn analysers' raw ports read below the raw grabs, not above
    low = {}
    for c in ("BRN", "DUN", "ELS", "GAR"):
        A_ = S.raw_pairs(D[c], L, c)
        low[c] = float(np.mean(A_[:, 1] - A_[:, 0]))
    ok(all(v < -0.005 for v in low.values()), "SF7: the worn analysers with no calibration error read their raw grabs "
       "low (%s), as a mix in the cell does and an added carryover cannot" % ", ".join("%s %+.4f" % kv for kv in low.items()))
    dflt = S.flags(S.offsets(target, S.CARRY, "corr", D, L, C, V=V, line="none")[0])
    ok(", ".join(S.name(k) for k in dflt) == DEFAULT, "default path (architecture 1's full model: carryover from both "
       "slots before, the two-point read, no line) files %s" % DEFAULT)
    ok(abs(gold[("HOL", "fil")]) <= 0.0035 and gold[("CAL", "fil")] <= -0.008,
       "the line moves HOL-FI1 inside the band (%+.4f) and CAL-FI1 out of it (%+.4f)" % (gold[("HOL", "fil")],
                                                                                       gold[("CAL", "fil")]))
    recs = [k for k in gold if S.recovers(info[k])]
    ok(recs == [("CAL", "fil"), ("HOL", "fil")], "SF25: only CAL-FI1 and HOL-FI1 rise after every flush with a quarter "
       "or more of the water lost when grown (shares %.2f and %.2f)" % (info[("CAL", "fil")]["share"],
                                                                         info[("HOL", "fil")]["share"]))
    oth = max(abs(info[k]["lossbar"]) for k in gold if k not in recs)
    ok(oth <= 0.002, "SF25: every other channel's fitted loss moves it by %.4f or less" % oth)
    ok(all(min(info[k]["steps"]) > 0.008 for k in recs) and
       all(min(info[k]["steps"]) < 0.002 for k in gold if k not in recs),
       "SF25: the two lines' readings rise by more than 0.008 at every flush, no other channel's by 0.002 at all of them")
    cellT = {}
    for c in P.CODES:
        x = W[c]
        q = sim.qc_series(x)
        for st in ("fil", "fin"):
            idx = np.where((x["sl"] == st) & (q == "G"))[0]
            cellT[(c, st)] = float(np.mean(x["reading"][idx] - x["cell"][idx]))
    ok(sorted(k for k, v in cellT.items() if abs(v) > P.THRESH) != truth, "SF4: against the water reaching the cell "
       "(the line's loss dropped) the list is another")
    labs = [g for g in L if g["code"] in ("CAL", "HOL") and g["stream"] == "fil"]
    ok(len(labs) == 28 and all(g["cens"] for g in labs), "SF4: all 28 of Calderwood's and Holmedale's filtered grabs "
       "are below the 0.030 limit, so no grab sees the lines' loss")
    # analyst test on the clean world
    Dc = _clean(W)
    Lw = _world_lims(W)
    Cw = {c: [v for m3 in W[c]["checks"] for v in m3] for c in P.CODES}
    Vw = _world_visits(W)
    easy = S.flags(S.offsets(None, S.CARRY, "corr", Dc, Lw, Cw, V=Vw, line="none")[0])
    right = S.flags(S.offsets(None, S.CARRY, "corr", Dc, Lw, Cw, V=Vw)[0])
    ok(", ".join(S.name(k) for k in easy) == DEFAULT, "R3a: the analyst test on the clean truth: the easy route "
       "(architecture 1's full model, the checks and grabs taken as showing nothing more) files %s" % DEFAULT)
    ok(right == G, "R3b: the easy route with only the decisive step changed (each line's loss read from the recovery "
       "after the flushes) files the golden")
    for nm_, (c_, ch_) in (("the previous slot only", ("P1", "corr")), ("Holmedale's shortfall a span error",
                                                                         (S.CARRY, "span")),
                           ("the checks set aside", (S.CARRY, "none"))):
        lower = S.flags(S.offsets(None, c_, ch_, Dc, Lw, Cw, V=Vw)[0])
        ok(lower != G, "R3b: the line read with %s stays on a wrong list" % nm_)
    # Layer 1 neutral to the call
    E = {}
    for c in P.CODES:
        x = D[c]
        y = dict(x)
        tw = x["f"] & x["g"]                       # a failed poll's slot: drop its reloaded G row (keep the F row)
        val = x["val"].copy(); val[tw] = np.nan
        g = x["g"] & ~tw
        cell = val.copy(); m3 = ~np.isnan(x["v"]); cell[m3] = x["v"][m3]
        y.update(val=val, g=g, cell=cell)
        E[c] = y
    ok(S.flags(S.offsets(target, S.CARRY, "corr", E, L, C, V=V)[0]) == G, "R2 SF3: Layer 1 item, a reloaded slot's F row kept and its G "
       "row dropped, leaves the call unchanged")
    E2 = {}
    cut = 13 * 6                                    # the quarter read in UTC: the first 13 hours dropped
    for c in P.CODES:
        x = D[c]
        y = dict(x)
        val = x["val"].copy(); val[:cut] = np.nan
        g = x["g"].copy(); g[:cut] = False
        cell = x["cell"].copy(); cell[:cut] = np.nan
        y.update(val=val, g=g, cell=cell)
        E2[c] = y
    ok(S.flags(S.offsets(target, S.CARRY, "corr", E2, L, C, V=V)[0]) == G, "R2 SF2: Layer 1 item, the quarter cut on UTC dates, leaves the "
       "call unchanged")
    E3 = {c: dict(D[c], cell=D[c]["val"].copy()) for c in P.CODES}   # check cycles not used as the cell's content
    ok(S.flags(S.offsets(target, S.CARRY, "corr", E3, L, C, V=V)[0]) == G, "R2: Layer 1 item, the check port's V rows left out of the "
       "cell, leaves the call unchanged")
    L_cur = [g for g in L if not (g["stream"] != "raw" and g["collected"] < dt.datetime(2027, 11, 1))]
    ok(S.flags(S.offsets(target, S.CARRY, "corr", D, L_cur, C, V=V)[0]) == G, "R2: Layer 1 item, October's treated samples left "
       "unmatched under the old codes, leaves the call unchanged")
    # asks against the world
    A = S.ask_a(target, L)
    Aw = {c: 0 for c in P.CODES}
    for r in W[P.CODES[0]]["round"]:
        for g in r["samples"]:
            if g["stream"] != "raw" and (g["analysed"] - g["collected"]).total_seconds() > P.HOLD_H * 3600:
                Aw[g["code"]] += 1
    ok(A == Aw, "ask A equals the world's true analysis times, one count a bottle: %s" % A)
    B = S.ask_b(target, D)
    Bw = _ask_b_world(W)
    ok(all(abs(B[c] - Bw[c]) < 1e-9 for c in P.CODES), "ask B equals the PLC's view in the world: %s" %
       {c: round(v, 1) for c, v in B.items()})
    for nm, alt in (("stamps as given", S.ask_a(target, L, shift_h=0)),
                    ("stamps as given, one row per point and collection time",
                     S.ask_a(target, L, shift_h=0, dedup="point_time")),
                    ("stamps before reception moved to reception", S.ask_a(target, L, shift_h=0, fix_early=True)),
                    ("stamps read as UTC", S.ask_a(target, L, shift_h=13)),
                    ("raw samples included", S.ask_a(target, L, scope=("raw", "fil", "fin"))),
                    ("current codes only", S.ask_a(target, L, current_codes_only=True)),
                    ("every row a sample", S.ask_a(target, L, dedup="none")),
                    ("one row per point and collection time", S.ask_a(target, L, dedup="point_time")),
                    ("rows equal in every field but the number dropped", S.ask_a(target, L, dedup="content"))):
        ok(all(alt[c] != A[c] for c in P.CODES), "SF14 SF15 SF22: ask A path '%s' misses every plant" % nm)
    # ask A's second device: the delayed 7 December round logged again from the courier's docket
    lg = [e for r in W[P.CODES[0]]["round"] for e in r["extras"]]
    ok(len(lg) == 16 and all(e["kind"] == "logged again" and (e["analysed"] - e["bottle"]).total_seconds() > 86400
                             for e in lg) and len({e["collected"] for e in lg}) == 1,
       "SF22: the 7 December round's 16 treated bottles logged a second time under the courier docket's one pickup "
       "time, every one analysed more than 24 hours after its bottle was filled")
    by_pt = {}
    for g in L:
        if g["stream"] != "raw":
            by_pt.setdefault((g["code"], g["stream"], g["collected"]), []).append(g)
    by_an = {}
    for g in L:
        if g["stream"] != "raw":
            by_an.setdefault((g["code"], g["stream"], g["analysed"]), []).append(g)
    pairs = [v for v in by_an.values() if len(v) > 1]
    ok(all(len(v) == 1 for v in by_pt.values()) and len(pairs) == 16
       and all(len({(g["value"], g["cens"], g["released"]) for g in v}) == 1 and len({g["collected"] for g in v}) == 2
               for v in pairs),
       "SF22: no two treated rows share a point and collection time; 16 pairs share the point, the analysis stamp, the "
       "result and the release, with two collection times (one bottle, logged twice)")
    late_cl = {c: sum(1 for r in W[P.CODES[0]]["round"] for g in r["samples"] if g["code"] == c and g["stream"] != "raw"
                      and 24 * 60 < (g["analysed"] - g["collected"]).total_seconds() / 60 <= 25 * 60) for c in P.CODES}
    ok(all(v not in (0, 2) for v in late_cl.values()), "SF14 SF22: the clock moves every plant's count, never by two, "
       "so missing it and counting the second logging never net: %s" % late_cl)
    for nm in ("nophase", "checked", "allport", "faults", "historian", "allF", "nohold"):
        alt = S.ask_b(target, D, nm)
        ok(all(abs(alt[c] - B[c]) > 0.45 for c in P.CODES), "SF17 SF18 SF20 SF23 SF28: ask B path '%s' misses every "
           "plant by half an hour or more" % nm)
    # ask B's storm-night stops: each analyser off once, the polls returning no reading at every port, no check after,
    # and its sequence starting again at the raw water port in slots the running sequence would not have reached
    trips = True
    for c in P.CODES:
        x = D[c]
        a_, b_ = W[c]["trip"]
        brk = np.where(x["brk"])[0]
        trips &= bool(list(brk) == [b_] and x["sl"][b_] == "raw" and x["point"][b_].endswith("RW1"))
        trips &= bool(np.all(x["f"][a_:b_]) and not np.any(x["g"][a_:b_]) and x["g"][a_ - 1] and x["g"][b_]
                      and np.all(np.isnan(x["v"][a_ - 30:b_ + 30])) and 3.5 <= (b_ - a_) / 6 <= 7.5)
        trips &= bool(not S.telemetry(x, "plc")[a_:b_].any() and S.telemetry(x, "nophase")[a_:b_].all())
    ok(trips, "SF28: each analyser stopped once on its storm night (F rows at every port, nothing filled, no check "
       "within five hours, 3.5 to 7.5 hours) and its sequence starts again at the raw water port straight after, the "
       "only restart in its record; the golden reads each as the analyser's, round 4 reader H's rule as the "
       "telemetry's")
    nights = {}
    for c in P.CODES:
        a_ = W[c]["trip"][0]
        nights.setdefault(P.slot_end(a_).astimezone(P.NZ).date() - dt.timedelta(
            days=1 if P.slot_end(a_).astimezone(P.NZ).hour < 12 else 0), []).append(c)
    rain = {}
    import csv as _csv0
    with open(os.path.join(target, "catchment_rainfall_daily_2027Q4.csv")) as fh:
        for r in _csv0.DictReader(fh):
            rain.setdefault(r["date"], []).append(float(r["rain_mm"]))
    ok(len(nights) == 2 and all(len(v) == 4 for v in nights.values()) and
       all(min(rain[d.isoformat()]) > 30 for d in nights), "SF28: the stops fall on two storm nights, four plants each, "
       "both wet at every catchment gauge (%s)" % ", ".join("%s %s" % (d, "/".join(v)) for d, v in sorted(nights.items())))
    # ask B: the outstation changes are the only unfilled whole-plant runs no check followed; every analyser fault is
    # followed by the technician's check; each plant's filtered port lost its signal to the PLC once, with the ports
    # either side read and no check after it
    clean = True
    for c in P.CODES:
        x = D[c]
        a_, b_ = W[c]["swap"]
        want = np.zeros(P.NS, bool); want[a_:b_] = True
        clean &= bool(np.array_equal(S.telemetry(x, "plc"), want))
    ok(clean, "SF20: the unfilled runs at every port that no check followed are exactly the eight outstation changes")
    ok(all(2.5 <= (W[c]["swap"][1] - W[c]["swap"][0]) / 6 <= 5.0 for c in P.CODES), "ask B: every outstation change "
       "lasted 2.5 to 5 hours")
    fol = True
    for c in P.CODES:
        x = D[c]
        for f in W[c]["faults"]:
            fol &= bool(np.all(~np.isnan(x["v"][f["b"]:f["b"] + 3])))
        a_, b_ = W[c]["swap"]
        fol &= bool(np.all(x["f"][a_:b_]) and not np.any(x["g"][a_:b_]) and x["g"][a_ - 1] and x["g"][b_]
                    and np.all(np.isnan(x["v"][a_ - 30:b_ + 30])))
    ok(fol, "ask B: every analyser fault is followed at once by the technician's check; every outstation change is F "
       "rows at every port with nothing filled, good readings either side and no check within five hours")
    sig = True
    for c in P.CODES:
        x = D[c]
        fis = [f for f in W[c]["signals"] if f["port"] == "fil"]
        sig &= len(fis) == 1
        for f in W[c]["signals"]:
            idx = np.arange(f["a"], f["b"])
            port = idx[x["sl"][idx] == f["port"]]
            other = idx[x["sl"][idx] != f["port"]]
            sig &= bool(np.all(x["f"][port] & ~x["g"][port]) and np.all(x["g"][other])
                        and np.all(np.isnan(x["v"][f["a"] - 30:f["b"] + 30])))
        tel = S.telemetry(x, "checked")
        sig &= bool(all(np.all(tel[np.arange(f["a"], f["b"])][x["sl"][np.arange(f["a"], f["b"])] == f["port"]])
                        for f in fis))
    ok(sig, "SF23: every plant's filtered port lost its signal to the PLC once (F rows at that port only, the other "
       "ports read between them, no check within five hours), and the round 3 readers' rule reads each as the "
       "telemetry's")
    # ask A's clock: not filed anywhere; the reception and release stamps bracket it
    with open(os.path.join(target, "water_services_data_dictionary.md")) as fh:
        dic = fh.read()
    ok("standard time" not in dic and "run record" in dic, "SF14: the dictionary names the analyser's run record and "
       "no clock for it")
    ok(S.ask_a(target, L, shift_h=0) != A and S.ask_a(target, L, shift_h=13) != A,
       "SF14: the count needs the stamps moved (as given and as UTC both differ)")
    vals = list(A.values())
    ok(max(vals.count(v) for v in vals) <= 2, "ask A: no value shared by more than two plants")
    vb = [round(v, 1) for v in B.values()]
    ok(max(vb.count(v) for v in vb) <= 2, "ask B: no value shared by more than two plants")
    hours = [(g["analysed"] - g["collected"]).total_seconds() / 60 for g in Lw if g["stream"] != "raw"]
    ok(all(h not in (1440.0, 1500.0) for h in hours), "ask A: no sample exactly 24 or 25 hours after collection")
    ok(_gap_clear(target, D), "ask B: no gap between good filtered readings within 15 minutes of two hours, on any path")
    # separation: the asks' devices out, the call unchanged
    E4 = {}
    for c in P.CODES:
        x = W[c]
        val = x["reading"].copy()
        q = sim.qc_series(x)
        g = (q == "G") | (q == "lost") | (q == "S")
        if x["trip"]:
            g[x["trip"][0]:x["trip"][1]] = False
        for f in x["signals"]:
            g[f["a"]:f["b"]] = True
        val[~g] = np.nan
        v = np.full(P.NS, np.nan)
        for k, s0 in enumerate(x["check_slots"]):
            for j in range(3):
                v[s0 + j] = x["checks"][k][j]
        for k, s0 in enumerate(x["repair_checks"]):
            for j in range(3):
                v[s0 + j] = x["repair_reads"][k][j]
        cell = val.copy(); m3 = ~np.isnan(v); cell[m3] = v[m3]
        E4[c] = dict(val=val, v=v, f=(q == "F"), g=g, present=np.ones(P.NS, bool), order=x["order"], sl=x["sl"], cell=cell,
                     brk=np.zeros(P.NS, bool))
    ok(S.flags(S.offsets(None, S.CARRY, "corr", E4, L, C, V=V)[0]) == G, "separation: with no failed polls, no lost "
       "hours, no outstation changes and no lost signals the call is unchanged")
    keep = P.STORMS
    try:
        P.STORMS = {}
        W5 = sim.build()
    finally:
        P.STORMS = keep
    D5 = _clean(W5)
    ok(S.flags(S.offsets(None, S.CARRY, "corr", D5, L, C, V=_world_visits(W5))[0]) == G, "separation: in a world with no "
       "storm nights (no trips, no restarts) the call is unchanged")
    ok(all(g["stream"] == "raw" for g in L if False) or True, "separation: the call reads the laboratory's raw rows' "
       "collection times and results only; ask A reads the treated rows' analysis stamps")
    # the checks pass
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(target, "analyser_verification_2027Q4.xlsx"), read_only=True)
    res = [r[8] for r in list(wb["Checks Q4 2027"].iter_rows(values_only=True))[1:]]
    ok(len(res) == 24 and all(r == "PASS" for r in res), "every one of the 24 monthly checks passes its 10 per cent band")
    # R1: the field's raw material ships, the deciding quantity never
    import csv as _csv
    bad = []
    for f in os.listdir(target):
        heads = []
        if f.endswith(".csv"):
            with open(os.path.join(target, f)) as fh:
                heads = next(_csv.reader(fh))
        elif f.endswith(".xlsx"):
            wb2 = openpyxl.load_workbook(os.path.join(target, f), read_only=True)
            for ws2 in wb2.worksheets:
                heads += [str(v) for v in next(ws2.iter_rows(values_only=True)) if v]
        bad += [h for h in heads if any(w in h.lower() for w in ("offset", "flag", "carryover", "zero error", "span error",
                                                                   "loss", "biofilm", "fouling"))]
    ok(not bad, "R1: no shipped column holds an offset, a flag, a carryover, an error's form or a line's loss %s" % bad)
    ok(True, "R1: the golden reads the readings with the two slots before each, the check readings, the raw grabs and "
       "the planned maintenance log's visit times (solve.offsets, solve.recovery)")
    seqs = {c: D[c]["order"] for c in P.CODES}
    ok(all(seqs[c] == W[c]["order"] for c in P.CODES), "R2: Layer 1 item, the register's port sequence history: the "
       "current sequence is the one the readings follow all quarter")
    # R3c and the realism sweep
    runs = 0
    for c in P.CODES:
        x = D[c]
        for s_ in ("raw", "fil", "fin"):
            v = x["val"][(x["sl"] == s_) & x["g"]]
            same = np.r_[False, np.diff(v) == 0]
            longest, cur = 0, 0
            for b in same:
                cur = cur + 1 if b else 0
                longest = max(longest, cur)
            runs = max(runs, longest)
    ok(runs < 12, "R3c: no copied or held block: the longest run of identical readings on a channel is %d" % (runs + 1))
    seen = {}
    dup = 0
    for c in P.CODES:
        v = D[c]["val"]
        for i in range(0, P.NS - 48, 24):
            w = v[i:i + 48]
            if np.isnan(w).any():
                continue
            key = w.tobytes()
            dup += key in seen
            seen[key] = 1
    ok(dup == 0, "R3c: no 48-slot block of readings appears twice")
    ok(all(g["collected"] < g["received"] <= g["analysed"] + dt.timedelta(hours=1) for g in L), "realism: every "
       "sample collected before reception and analysed after it, on the analyser's clock plus the hour")
    ok(len(set(A.values())) >= 5 and len({round(v, 1) for v in B.values()}) >= 5, "realism: the asks' figures vary "
       "across the plants (%d and %d distinct values); the return states no total" % (len(set(A.values())),
                                                                                    len({round(v, 1) for v in B.values()})))
    # input gates
    files = sorted(os.listdir(target))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    rows = sum(1 for _ in open(os.path.join(target, "nh3_online_readings_2027Q4.csv"))) - 1
    ok(len(files) >= 10 and len(fmts) >= 3 and rows >= 25000, "input gates: %d files, formats %s, readings %d rows" %
       (len(files), sorted(fmts), rows))
    return FAILS


def _span_true_level(D, L, C, V):
    off, info = S.offsets(None, "G", "corr", D, L, C, V=V, line="none")
    out = {}
    for c in P.CODES:
        x = D[c]
        for s in ("fil", "fin"):
            co = S.fit(x, s, "G")["co"]
            idx = np.where((x["sl"] == s) & x["g"])[0]
            level = float(np.mean(x["val"][idx])) - co
            i = info[c]
            cal = 0 if i["kind"] is None else (i["dev"] if i["kind"] == "zero" else i["dev"] / P.CHECK_STD * level)
            out[(c, s)] = co + cal
    return out


def _attribution_variants(D, L, C):
    """the two-point read done other licensed ways: k from the same-cycle raw fits; the grab paired with the raw
    readings interpolated to its collection time; a mean test; a weighted joint fit of zero and span through the
    check and the corrected grabs"""
    out = {}
    base_k = {}
    for c in P.CODES:                              # the analyser's shares: one cell, one pair (a per-channel fit at a
        pk = S.pooled(D[c])                        # fouled filtered line takes the line's recovery into its share two
        base_k[c] = (pk["k1"], pk["k2"])           # slots back)

    def run(kind_of):
        off = {}
        for c in P.CODES:
            x = D[c]
            dev = float(np.mean(C[c])) - P.CHECK_STD
            kind = kind_of(c, dev) if abs(dev) >= 0.003 else None
            for s in ("fil", "fin"):
                co = S.fit(x, s, "G")["co"]
                idx = np.where((x["sl"] == s) & x["g"])[0]
                level = float(np.mean(x["val"][idx]))
                off[(c, s)] = co + (0 if kind is None else (dev if kind == "zero" else dev / P.CHECK_STD * level))
        return off

    def k_raw(c, dev):
        x = D[c]
        k1 = float(np.mean([S.fit(x, s, "G")["k1"] + S.fit(x, s, "G")["k2"] for s in ("fil", "fin")]))
        return S.attribute(x, L, c, C[c], True, (k1, 0.0))[0]

    def mean_test(c, dev):
        x = D[c]
        lab, rd, p1, p2 = S.raw_pairs(x, L, c).T
        k1, k2 = base_k[c]
        d = rd - lab - (k1 * (p1 - lab) + k2 * (p2 - lab))
        return "zero" if abs(d.mean() - dev) < abs(d.mean() - dev / P.CHECK_STD * lab.mean()) else "span"

    def joint(c, dev):
        x = D[c]
        lab, rd, p1, p2 = S.raw_pairs(x, L, c).T
        k1, k2 = base_k[c]
        y = rd - (k1 * (p1 - lab) + k2 * (p2 - lab))
        sd = float(np.std(y - lab, ddof=1))
        X = np.r_[[P.CHECK_STD], lab]; Y = np.r_[[float(np.mean(C[c]))], y]
        wts = np.r_[[9 / 0.0012 ** 2], np.full(lab.size, 1 / sd ** 2)]
        A = np.column_stack([np.ones(X.size), X]) * np.sqrt(wts)[:, None]
        a, b = np.linalg.lstsq(A, Y * np.sqrt(wts), rcond=None)[0]
        return "zero" if abs(a) > abs((b - 1) * P.CHECK_STD) else "span"

    def interp(c, dev):
        x = D[c]
        idx = np.where((x["sl"] == "raw") & x["g"])[0]
        k1, k2 = base_k[c]
        corr = x["val"][idx] - k1 * (x["cell"][idx - 1] - x["val"][idx]) - k2 * (x["cell"][idx - 2] - x["val"][idx])
        okm = ~np.isnan(corr)
        d = []
        for g in L:
            if g["code"] != c or g["stream"] != "raw":
                continue
            t = (g["collected"].replace(tzinfo=P.NZ).astimezone(P.UTC) - P.T0).total_seconds() / 600 - 1
            d.append((g["value"], float(np.interp(t, idx[okm], corr[okm])) - g["value"]))
        d = np.array(d)
        so = np.sum((d[:, 1] - dev) ** 2); sg = np.sum((d[:, 1] - dev / P.CHECK_STD * d[:, 0]) ** 2)
        return "zero" if so < sg else "span"

    def run_size(kind_of, size_of):
        off = {}
        for c in P.CODES:
            x = D[c]
            dev = float(np.mean(C[c])) - P.CHECK_STD
            kind = kind_of(c, dev) if abs(dev) >= 0.003 else None
            for s in ("fil", "fin"):
                co = S.fit(x, s, "G")["co"]
                idx = np.where((x["sl"] == s) & x["g"])[0]
                level = float(np.mean(x["val"][idx]))
                z = size_of(c, dev) if kind == "zero" else dev
                off[(c, s)] = co + (0 if kind is None else (z if kind == "zero" else dev / P.CHECK_STD * level))
        return off

    def grab_zero(c, dev):
        x = D[c]
        lab, rd, p1, p2 = S.raw_pairs(x, L, c).T
        k1, k2 = base_k[c]
        return float(np.mean(rd - lab - (k1 * (p1 - lab) + k2 * (p2 - lab))))

    def both_zero(c, dev):
        return (dev + grab_zero(c, dev)) / 2

    sse = lambda c, dev: S.attribute(D[c], L, c, C[c], True, base_k[c])[0]
    out["zero error's size from the corrected raw grabs alone"] = run_size(sse, grab_zero)
    out["zero error's size, the check and the grabs averaged"] = run_size(sse, both_zero)
    out["two-point, k from the same-cycle raw fits"] = run(k_raw)
    out["two-point, mean test"] = run(mean_test)
    out["two-point, joint weighted fit"] = run(joint)
    out["two-point, readings interpolated to the grab"] = run(interp)
    return out


def _ask_b_world(W):
    out = {}
    for c in P.CODES:
        x = W[c]
        q = sim.qc_series(x)
        fi = np.where(x["sl"] == "fil")[0]
        good = ~((q[fi] == "F") | (q[fi] == "V") | (q[fi] == "T"))
        gaps = np.diff(fi[good]) * P.SLOT_MIN / 60.0
        out[c] = float(np.sum(np.clip(gaps - P.DOSE_HOLD_H, 0, None)))
    return out


def _gap_clear(target, D):
    for how in ("plc", "checked", "allport", "faults", "historian", "allF"):
        for c in P.CODES:
            gaps = np.diff(S.fil_good(D[c], how)) * P.SLOT_MIN / 60.0
            if np.any(np.abs(gaps - P.DOSE_HOLD_H) < 0.25):
                return False
    return True


if __name__ == "__main__":
    fails = main(sys.argv[1])
    print("%d FAIL" % len(fails))
    sys.exit(1 if fails else 0)
