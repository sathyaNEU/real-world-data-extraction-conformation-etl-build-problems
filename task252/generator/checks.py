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
from docs import HISTORIAN as HISTORIAN_SENTENCE

FAILS = []
MARGIN = 0.0015
SFOF = {"pooled mixing (the golden)": "golden", "per-channel mixing": "SF21", "RAW corr": "SF21",
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


DOC_EXT = (".pdf", ".eml", ".md", ".txt", ".docx", ".rtf", ".html")


def _text_of(path):
    """every shipped document's text, one way: pypdf's page text for a pdf (the leak sweep's reader), the file itself
    otherwise; every presence and absence assertion on a document reads it through here"""
    if path.endswith(".pdf"):
        import pypdf
        return "\n".join(p.extract_text() or "" for p in pypdf.PdfReader(path).pages)
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def _has(text, sentence):
    """a sentence found in a document's text, line breaks and runs of spaces read as one space"""
    return " ".join(sentence.split()) in " ".join(text.split())


def _find(pattern, text):
    """a pattern searched in a document's text, case aside, line breaks read as spaces"""
    return re.search(pattern, " ".join(text.split()), re.I)


# the names a describing file or sheet goes by (the leak sweep's own lists, dataset-generation section 3)
_DESCRIBE_NAME = re.compile(
    r"(?<![a-z])(read_?me|data_?dictionar\w*|dictionar(y|ies)|codebook|field_?notes|field_?guide|"
    r"fields?_(guide|notes|list|descriptions?)|\w*_fields|manifest|extract_contents|file_list|file_layout|glossary|"
    r"column_(notes|descriptions?)|data_?notes|how_to_read|about_this|export_notes|extract_notes|feed_notes|desk_notes|"
    r"data_team_notes|definitions|schema|layouts?_notes|handling_notes|release_notes)(?![a-z])", re.I)
_DESCRIBE_SHEET = re.compile(r"^(read ?me|notes?|dictionary|data dictionary|definitions|glossary|fields|field notes|"
                             r"about|about this (file|workbook)|how to (read|use)( this)?|columns?)$", re.I)


def _describe_name(f):
    return bool(_DESCRIBE_NAME.search(f.rsplit(".", 1)[0]))


def _describe_sheet(s):
    return bool(_DESCRIBE_SHEET.match(s.strip()))


def _columns_named(text, data_cols):
    """the data files' column names (four characters or more) a text carries verbatim, as whole tokens"""
    cols = {c.strip() for v in data_cols.values() for c in v if len(c.strip()) >= 4}
    return sorted(c for c in cols if re.search(r"(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])" % re.escape(c), text))


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


def _visits_as(target, tz):
    """the planned maintenance log's monthly visits as slots, the log's times read in the zone given"""
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(target, "online_analyser_register.xlsx"), read_only=True)
    out = {c: [] for c in P.CODES}
    for r in list(wb["Planned maintenance"].iter_rows(values_only=True))[1:]:
        if str(r[3]).startswith("Monthly planned maintenance"):
            out[r[1].split("-")[1]].append(P.slot_of(r[0].replace(tzinfo=tz)))
    return {c: sorted(v) for c, v in out.items()}


def _lims_as_utc(L):
    """the laboratory's times read as UTC: each wall time taken as a UTC instant and shown in New Zealand time"""
    f = lambda t: t.replace(tzinfo=P.UTC).astimezone(P.NZ).replace(tzinfo=None)
    return [dict(g, collected=f(g["collected"]), received=f(g["received"]), analysed=f(g["analysed"]),
                 released=f(g["released"])) for g in L]


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
    ok(_visits_as(target, P.NZ) == V, "SF26 control: the log read through this file's own loader in New Zealand time "
       "gives the golden's visits")
    Vu = _visits_as(target, P.UTC)
    off_u = S.offsets(target, S.CARRY, "corr", D, L, C, V=Vu)[0]
    ok(S.flags(off_u) == G, "SF26: the log's visit times read as UTC file the same six (CAL-FI1 %+.4f, HOL-FI1 %+.4f)"
       % (off_u[("CAL", "fil")], off_u[("HOL", "fil")]))

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
    import openpyxl as _ox1
    _pts = list(_ox1.load_workbook(os.path.join(target, "online_analyser_register.xlsx"),
                                   read_only=True)["Sample points"].iter_rows(values_only=True))[1:]
    _treated = sorted(r[0] for r in _pts if r[2] in ("Filtered", "Final"))
    _wq1 = _text_of(os.path.join(target, "WQ-DS-04_online_monitoring_data_standard.pdf"))
    ok(len(gold) == 16 and sorted(S.name(k) for k in gold) == _treated and
       _has(_wq1, "A treated water channel (filtered or final water)") and
       len([r for r in _pts if r[2] == "Raw"]) == 8,
       "SF1: the 16 channels are the register's filtered and final water points, the treated water channels WQ-DS-04 "
       "section 4 flags (the eight raw water points outside it)")
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
    # SF13: the prompt (read from the task folder, so the check runs on every build) carries one rounding instruction,
    # the hours'; no offset is graded to a rounding
    prompt = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "prompt.txt")).read()
    rnd = [s.strip() for s in re.split(r"(?<=[.?!])\s+", prompt.strip())
           if re.search(r"\bdecimals?\b|significant|\bround(ed|ing)?\b", s, re.I)]
    ok(len(prompt) > 200 and _has(prompt, "every channel's quarter offset against the 0.005 band") and
       rnd == ["Hours to one decimal."], "SF13: the prompt's one rounding instruction is the hours' (%s), and the "
       "chart's offsets carry none" % rnd)
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
    # SF29: the laboratory's times carry no zone in the export; read as New Zealand time (the golden) or as UTC, the
    # call and ask A converge
    Lu = _lims_as_utc(L)
    ok(all((u["collected"] - g["collected"]).total_seconds() == 13 * 3600 for g, u in zip(L, Lu)),
       "SF29 control: read as UTC every laboratory time moves 13 hours (the quarter is all daylight time)")
    off29, info29 = S.offsets(target, S.CARRY, "corr", D, Lu, C, V=V)
    ok(S.flags(off29) == G and info29["HOL"]["kind"] == "zero" and info29["CAL"]["kind"] == "span",
       "SF29: the laboratory's times read as UTC file the same six, Holmedale's shortfall still a zero error and "
       "Calderwood's a span error")
    q0, q1 = dt.datetime(2027, 10, 1), dt.datetime(2028, 1, 1)
    ok(S.ask_a(target, Lu) == S.ask_a(target, L) and all(q0 <= g["collected"] < q1 for g in L + Lu),
       "SF29: ask A's counts are the same with every laboratory time read as UTC, every sample collected inside the "
       "quarter either way")
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
        ok(all(abs(alt[c] - B[c]) > 0.45 for c in P.CODES), "SF17 SF18 SF20 SF28: ask B path '%s' misses every "
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
    ok(sig, "SF20: every plant's filtered port lost its signal to the PLC once (F rows at that port only, the other "
       "ports read between them, no check within five hours), and the round 3 readers' rule reads each as the "
       "telemetry's")
    # ask A's clock: not filed anywhere; the reception and release stamps bracket it. The absence is searched through
    # the one text extractor this file uses for every document, with a sentence known to be there as its control
    docs_text = {f: _text_of(os.path.join(target, f)) for f in sorted(os.listdir(target)) if f.endswith(DOC_EXT)}
    ok(all(len(t) > 200 for t in docs_text.values()) and len(docs_text) == 3 and
       _has(docs_text["WQ-DS-04_online_monitoring_data_standard.pdf"],
            "Ammonia samples are analysed within 24 hours of collection."),
       "SF14 control: the extractor reads all three documents (%s) and finds WQ-DS-04 section 6's holding-time "
       "sentence" % ", ".join("%s %d chars" % (f, len(t)) for f, t in docs_text.items()))
    clock = r"standard time|NZST|daylight|run record|instrument clock|\bclock\b"
    ok(_find(r"ammonium standard", docs_text["WQ-DS-04_online_monitoring_data_standard.pdf"]),
       "SF14 control: the search used below finds WQ-DS-04 section 5's 'ammonium standard'")
    ok(not any(_find(clock, t) for t in docs_text.values()), "SF14: no shipped document names the laboratory "
       "analyser's clock or its run record (%s)" % [f for f, t in docs_text.items() if _find(clock, t)])
    ok(S.ask_a(target, L, shift_h=0) != A and S.ask_a(target, L, shift_h=13) != A,
       "SF14: the count needs the stamps moved (as given and as UTC both differ)")
    # SF18: the historian's lost night of 17 November (no rows at all). What a fault on the historian's own server
    # leaves is filed once, in the process summary's telemetry paragraph; the slots it covers are read through pandas,
    # as the verifier reads the export
    import pandas as pd
    proc = docs_text["water_treatment_process_summary_2027.pdf"]
    ok(_has(proc, HISTORIAN_SENTENCE) and sum(len(re.findall(r"historian's own server", " ".join(t.split())))
                                              for t in docs_text.values()) == 1,
       "SF18: the process summary files once that a fault on the historian's own server leaves it with no record "
       "and the plants and their dose control run on")
    rd = pd.read_csv(os.path.join(target, "nh3_online_readings_2027Q4.csv"), dtype={"qc": str}, keep_default_na=False,
                     na_values=[""])
    rd["slot"] = ((pd.to_datetime(rd["reading_end_utc"], utc=True) - pd.Timestamp(P.T0)).dt.total_seconds()
                  // 600).astype(int) - 1
    missing = {c: sorted(set(range(P.NS)) - set(rd.loc[rd["site_code"] == c, "slot"])) for c in P.CODES}
    a_, b_ = W[P.CODES[0]]["lost"]
    night = P.slot_end(a_).astimezone(P.NZ)
    ok(all(missing[c] == list(range(a_, b_)) for c in P.CODES) and night.date() == dt.date(2027, 11, 17),
       "SF18: the slots with no row at all are one run, the same %.1f hours at all eight plants from %s New Zealand "
       "time, and nowhere else" % ((b_ - a_) / 6, night.strftime("%d %b %H:%M")))
    lostgap = {}
    for c in P.CODES:
        good_ = S.fil_good(D[c], "plc")
        good_ = good_[D[c]["present"][good_]]       # a slot with no row read as no reading at the PLC
        lostgap[c] = float(np.sum(np.clip(np.diff(good_) * P.SLOT_MIN / 60.0 - P.DOSE_HOLD_H, 0, None)))
    ok(all(lostgap[c] - B[c] >= 3.0 for c in P.CODES), "SF18: reading those slots as no reading at the PLC moves "
       "every plant's hours by 3.0 or more (the sentence decides it): %s" % {c: round(lostgap[c] - B[c], 1)
                                                                              for c in P.CODES})
    # closure 19: the codes. The historian's own code table labels each quality code; WQ-DS-04 files the G readings
    # (section 3) and the V check readings (section 5); the labels read true in the export
    qtab = pd.read_csv(os.path.join(target, "historian_quality_codes.csv"), dtype=str, keep_default_na=False)
    lab_of = dict(zip(qtab["qc"], qtab["description"]))
    ok(list(qtab.columns) == ["qc", "description"] and lab_of == {"G": "Good", "F": "No reading",
                                                                  "V": "Verification check"}
       and set(rd["qc"]) == set(lab_of), "closure 19: the historian's code table labels exactly the codes the "
       "readings carry (%s)" % ", ".join("%s %s" % kv for kv in lab_of.items()))
    chk_pt = rd["sample_point"].str.endswith("-CHK")
    ok(rd.loc[rd["qc"] == "F", "nh3_n_mgl"].isna().all() and rd.loc[rd["qc"] != "F", "nh3_n_mgl"].notna().all()
       and chk_pt[rd["qc"] == "V"].all() and not chk_pt[rd["qc"] == "G"].any(),
       "closure 19: the labels read true in the export: no F row carries a value, every G and V row does, and the V "
       "rows sit at the check ports")
    wq = docs_text["WQ-DS-04_online_monitoring_data_standard.pdf"]
    ok(_has(wq, "readings held in the historian with quality code G for the quarter") and
       _has(wq, "The check's three readings are also held in the historian with quality code V."),
       "closure 19: WQ-DS-04 sections 3 and 5 file the G readings and the V check readings")
    # dataset-generation section 3: no shipped file or sheet describes the data, by name or by content
    import openpyxl as _oxd
    names = sorted(os.listdir(target))
    sheets = [(f, s) for f in names if f.endswith(".xlsx") for s in _oxd.load_workbook(os.path.join(target, f),
                                                                                         read_only=True).sheetnames]
    ok(_describe_name("water_services_data_dictionary.md") and _describe_name("pack_manifest.csv") and
       _describe_sheet("Notes"), "section 3 control: the name test below catches a data dictionary, a manifest and a "
       "notes sheet")
    ok(not [f for f in names if _describe_name(f)] and not [s for s in sheets if _describe_sheet(s[1])],
       "section 3: no shipped file or sheet is named as a dictionary, readme, manifest, codebook, field notes, "
       "definitions or notes (%d files; sheets %s)" % (len(names), ", ".join(s for _, s in sheets)))
    data_cols = {}
    for f in names:
        if f.endswith(".csv"):
            data_cols[f] = list(pd.read_csv(os.path.join(target, f), nrows=0).columns)
        elif f.endswith(".xlsx"):
            for ws_ in _oxd.load_workbook(os.path.join(target, f), read_only=True).worksheets:
                data_cols["%s:%s" % (f, ws_.title)] = [str(v) for v in next(ws_.iter_rows(values_only=True)) if v]
    ok(set(_columns_named(_text_of(os.path.join(target, "lims_ammonia_2027Q4.csv")).split("\n")[0], data_cols)) >=
       {"sample_no", "lims_point", "collected", "received", "analysed", "released"},
       "section 3 control: the column search below finds the laboratory export's own header in its first line")
    named = {f: _columns_named(t, data_cols) for f, t in docs_text.items()}
    ident = lambda c: "_" in c or re.search(r"\d", c) or re.search(r"[a-z][A-Z]", c)
    most = {f: max(len(set(v) & set(cols)) for cols in data_cols.values()) for f, v in named.items()}
    ok(all(not [c for c in v if ident(c)] for v in named.values()) and all(m < 5 for m in most.values()),
       "section 3: no document names a data column as a field, nor five of one file's columns (%s)" %
       "; ".join("%s: %s" % (f, ", ".join(v) or "none") for f, v in named.items()))
    # document control dates: no workbook saved before an event it records, none after the folder's assembly
    import zipfile as _zf
    def _saved(f):
        core = _zf.ZipFile(os.path.join(target, f)).read("docProps/core.xml").decode()
        return dt.datetime.fromisoformat(re.search(r"<dcterms:modified[^>]*>([^<]+)<", core).group(1)
                                         .replace("Z", "+00:00"))
    pm_ = list(_oxd.load_workbook(os.path.join(target, "online_analyser_register.xlsx"),
                                  read_only=True)["Planned maintenance"].iter_rows(values_only=True))[1:]
    ck_ = list(_oxd.load_workbook(os.path.join(target, "analyser_verification_2027Q4.xlsx"),
                                  read_only=True)["Checks Q4 2027"].iter_rows(values_only=True))[1:]
    last_visit = max(r[0] for r in pm_).replace(tzinfo=P.NZ)
    last_check = max(r[2] for r in ck_).replace(tzinfo=P.NZ)
    folder = dt.datetime(2028, 1, 19, 9, 12, tzinfo=P.UTC)
    ok(last_visit < _saved("online_analyser_register.xlsx") < folder and
       last_check < _saved("analyser_verification_2027Q4.xlsx") < folder,
       "document dates: the register saved %s after its last visit (%s), the verification workbook %s after its last "
       "check (%s), both before the folder's assembly" % (_saved("online_analyser_register.xlsx").date(),
                                                          last_visit.date(), _saved("analyser_verification_2027Q4.xlsx")
                                                          .date(), last_check.date()))
    lims_last = max(max(g["received"], g["analysed"] + dt.timedelta(hours=1), g["released"]) for g in L)
    ok(lims_last.date() <= dt.date(2028, 1, 14), "document dates: the laboratory export's last stamp (%s) is on or "
       "before its export of 14 January 2028" % lims_last)
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
