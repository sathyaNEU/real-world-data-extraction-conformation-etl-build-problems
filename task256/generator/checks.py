"""The generator's assertions on the built pack: the input gates, the call and every configuration's accommodation,
each rung's own pick, the three rules' analyst test run on the generator's clean truth, the semantic fork table
(SF1 to SF18), the convergences, the ask's figures and devices, rounding margins and the goldens' agreement with
figures.json."""
import csv
import datetime as dt
import json
import os
import re

import numpy as np
import openpyxl

import analysis as AN
import docs as D
import records as R
import world as W

CHECKS = []


def ok(cond, label):
    if not cond:
        raise AssertionError(label)
    CHECKS.append(label)


def pdf_text(path):
    from pypdf import PdfReader
    return re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(path).pages))


def edge(v):
    """Distance, in percentage points, from a share to the nearest edge of one-decimal rounding."""
    x = round(100 * v * 10, 9)
    return abs((x - np.floor(x)) - 0.5) / 10


def run(target, golden, st, meta_path):
    CHECKS.clear()
    fig = st["fig"]
    files = sorted(os.listdir(target))
    meta = json.load(open(meta_path))

    # ---- input gates
    ok(len(files) >= 10, "ten or more files (%d)" % len(files))
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "three or more formats")
    rows = {f: sum(1 for _ in open(os.path.join(target, f))) - 1 for f in files if f.endswith(".csv")}
    ok(max(rows.values()) >= 25000, "a file of 25,000 or more rows (%s %d)" % (max(rows, key=rows.get), max(rows.values())))
    ok(len(meta["distractor_files"]) >= 2 and all(f in files for f in meta["distractor_files"]), "two distractors shipped")
    for f in files:
        if f.endswith((".csv", ".md")):
            t = open(os.path.join(target, f), encoding="utf-8").read()
        elif f.endswith(".pdf"):
            t = pdf_text(os.path.join(target, f))
        else:
            continue
        ok("—" not in t and "–" not in t, "no em or en dash in %s" % f)
    ok(max(e["date"] for e in st["enc"]) <= W.AS_OF, "no encounter after 30 September 2026")
    ok(max(w["closed"] for w in st["wos"]) <= W.AS_OF, "no work order closed after 30 September 2026")

    # ---- the population and its records
    ops = AN.counted(st)
    ok(len(ops) == fig["operators"]["n"] == 2110, "2,110 bus operators counted")
    phys = {}
    for e in st["enc"]:
        if e["type"] == "PHYS":
            phys.setdefault(e["emp"], []).append(e)
    ok(all(o["emp"] in phys for o in ops), "every counted operator has a DOT physical on file")
    roster = list(openpyxl.load_workbook(os.path.join(target, R.ROSTER), read_only=True)["Roster"].iter_rows(
        min_row=6, values_only=True))
    ok(sum(1 for r in roster if r[1] == "BUS OPERATOR") == 2110, "the roster's Bus Operator rows are the 2,110")
    ok(len({r[0] for r in roster}) == len(roster), "one roster row per employee")
    # the two exports agree wherever they overlap (Fernhill's copy of Ostrander's first half of 2021)
    ost = {r["ENC #"]: r for r in csv.DictReader(open(os.path.join(target, R.OSTRANDER)))}
    fh = list(csv.DictReader(open(os.path.join(target, R.FERNHILL))))
    taken = [r for r in fh if r["legacy_ref"]]
    ok(len(taken) > 1000, "Fernhill holds Ostrander's encounters from 1 January 2021 (%d)" % len(taken))
    agree = all(ost[r["legacy_ref"]]["WEIGHT LB"] == r["wt_lb"] and
                (not r["ht_in_no_shoes"] or abs(float(r["ht_in_no_shoes"]) - _ft_in(ost[r["legacy_ref"]]["HEIGHT (NO SHOES)"])) < 1e-9) for r in taken)
    ok(agree, "every taken-over record carries Ostrander's height and weight")
    ok(not any("sex" in h.lower() for h in list(fh[0].keys()) + list(next(iter(ost.values())).keys())),
       "SF9: no sex field in either export; the roster's is the only one")

    # ---- the call and every configuration
    acc = fig["acc"]
    order = [c for c, _, _ in W.CONFIGS]
    ok(fig["call"]["config"] == "H" and acc["H"] >= W.LINE, "the call is Configuration H at 95 per cent or more")
    ok(all(acc[c] < W.LINE for c in order[:order.index("H")]), "every cheaper configuration falls short")
    ok(acc["H"] - W.LINE >= 0.012, "H clears the line by 1.2 points or more (%.4f)" % acc["H"])
    ok(W.LINE - max(acc[c] for c in order[:7]) >= 0.015, "the nearest cheaper configuration is 1.5 points or more short")
    ok(all(edge(acc[c]) >= 0.02 for c in order), "SF7: every share 0.02 points or more from a rounding edge (%s)"
       % ", ".join("%s %.3f" % (c, edge(acc[c])) for c in order))
    ok(all(abs(acc[c] - W.LINE) >= 0.005 for c in order), "SF7: no configuration within half a point of 95.0")
    picks = fig["rung_picks"]
    ok(picks == {"G": "H", "R4": "G", "Rmarg": "G", "R1": "B", "R2": "E", "R3": "C", "R0a": "A", "Rind": "B",
                 "R0b": "B"}, "each rung files its own configuration: %s" % picks)
    r4 = fig["rungs"]["R4"]
    ok(r4["G"] - W.LINE >= 0.012 and W.LINE - max(r4[c] for c in order[:6]) >= 0.015,
       "the survey carried to the operators uncorrected files G with its margins (%.4f)" % r4["G"])
    tr = st["trial"]
    ft = fig["trial"]
    ok(ft["n"] == 140 and all(ft["stature_mean"][sx] <= fig["build"][sx]["stature_mean"] - 50 for sx in ("M", "F")),
       "the operators measured are 140 volunteers, 50 mm or more shorter than the roster (%s)" % ft["stature_mean"])
    eo = ft["eye_height_offset_mm"]
    ok(min(eo.values()) >= 20, "the operators measured sit taller than the survey gives their stature and weight "
       "(eye height %s mm)" % eo)
    ok(max(abs(v) for v in ft["raw_eye_height_gap_mm"].values()) <= 8,
       "their raw mean eye heights sit within 8 mm of the survey's (%s mm): their build hides the gap"
       % ft["raw_eye_height_gap_mm"])
    rm = fig["rungs"]["Rmarg"]
    ok(rm["G"] - W.LINE >= 0.012 and W.LINE - max(rm[c] for c in order[:6]) >= 0.015,
       "the survey moved by the raw mean gap files G with its margins (%.4f)" % rm["G"])
    r1 = fig["rungs"]["R1"]
    ok(r1["B"] - W.LINE >= 0.005 and W.LINE - r1["A"] >= 0.01, "the default path's B clears its line by half a point")

    # ---- the three rules' analyst test on the generator's clean truth
    truth = _truth(st, ops)
    mix = {sx: sum(1 for o in truth if o["sex"] == sx) / len(truth) for sx in ("M", "F")}
    easy = AN.pick({c: AN.acc_survey(W.ENVELOPES[c], mix) for c in order})
    ok(easy == "B", "analyst test: the easy route on clean truth (the survey's workers at the sex mix) files B")
    carried = AN.pick({c: AN.acc_carried(truth, W.ENVELOPES[c]) for c in order})
    ok(carried == "G", "analyst test: the survey carried to the operators on clean truth, uncorrected, files G")
    true_off = {sx: np.array([W.TRUE_OFFSET.get(d, 0.0) for d in AN.FIT]) for sx in ("M", "F")}
    decisive = AN.pick({c: AN.acc_carried(truth, W.ENVELOPES[c], offset=true_off) for c in order})
    ok(decisive == "H", "analyst test: the decisive step alone on clean truth (the workforce's own offset) files H")

    # ---- the semantic fork table
    off = AN.trial_offsets(st["trial"])
    act = AN.counted(st, active_only=True)
    ok(AN.pick({c: AN.acc_carried(act, W.ENVELOPES[c], offset=off) for c in order}) == "H",
       "SF1: operators on active duty only, H")
    ok(picks["R0a"] == "A", "SF2: each dimension at 95 per cent on its own files A")
    shifted = {}
    for c, opts, _ in W.CONFIGS:
        env = W.ENVELOPES[c]
        shifted[c] = AN.acc_carried(ops, {k: (None if lo is None else lo + 0.5, None if hi is None else hi - 0.5)
                                          for k, (lo, hi) in env.items()}, offset=off)
    ok(AN.pick(shifted) == "H", "SF3: limits read half a millimetre inside, H")
    mean_ops = AN.counted(st, latest=False)
    ok(AN.pick({c: AN.acc_carried(mean_ops, W.ENVELOPES[c], offset=off) for c in order}) == "H", "SF4: the mean of "
       "each operator's physicals, H")
    std0 = pdf_text(os.path.join(target, D.STANDARD))
    ok("each operator as measured at the operator's latest DOT physical examination on or before that date" in std0,
       "SF4 and SF16: the standard takes each operator as measured at the latest DOT physical examination")
    fit_text = pdf_text(os.path.join(target, D.FIT_REPORT))
    ok("measured unclothed and unshod as that survey measures them" in fit_text, "SF5: the envelopes are in the survey's dimensions")
    prices = [p for _, _, p in W.CONFIGS]
    ok(prices == sorted(prices) and len(set(prices)) == len(prices), "SF6: one price per bus per configuration, distinct")
    for c, _, p in W.CONFIGS:
        ok("${:,}".format(p) in fit_text, "SF6: configuration %s's price in the fit report" % c)
    ok("2026-09-30" in R.ROSTER and R.ROSTER in os.listdir(target), "SF8: the roster is the 30 September 2026 export "
       "(its file date)")
    std = pdf_text(os.path.join(target, D.STANDARD))
    ok("on 30 September of the year before the order's model year, whatever their duty status" in std,
       "SF8: the standard dates the roster")
    sv = pdf_text(os.path.join(target, D.SURVEY))
    ok(sv.count("Percentiles are computed from the normal distribution with the mean and standard deviation shown") == 2,
       "SF10: the survey's percentiles are normal")
    ok(abs(W.IN_TO_MM - 25.4) < 1e-12 and abs(W.LB_TO_KG - 0.45359237) < 1e-12, "SF11: exact conversions")
    half = {c: _count_over_half(ops, W.ENVELOPES[c], off) for c in order}
    ok(AN.pick(half) not in ("H", None) and order.index(AN.pick(half)) < order.index("H"),
       "SF12: counting operators above one half files %s, cheaper than H" % AN.pick(half))
    ok(sv.count("Correlations between dimensions, working") == 2 and "both sexes" not in sv.lower(),
       "SF13: within-sex correlations only")
    mc = {c: _monte_carlo(ops, W.ENVELOPES[c], off) for c in order}
    ok(AN.pick(mc) == "H" and all(abs(mc[c] - acc[c]) < 0.001 for c in order),
       "SF14: Monte Carlo with 200,000 draws per sex agrees within 0.1 point")
    pl = {c: _pearson_lawley(ops, W.ENVELOPES[c], off) for c in order}
    ok(AN.pick(pl) == "H" and max(pl[c] for c in order[:7]) <= W.LINE - 0.005,
       "convergence: a bivariate normal fitted to the operators' statures and weights files H, every cheaper "
       "configuration half a point short (%s)" % ", ".join("%s %.2f" % (c, 100 * pl[c]) for c in order))
    light = [dict(o, w=o["w"] - 1.0) for o in ops]
    ok(AN.pick({c: AN.acc_carried(light, W.ENVELOPES[c], offset=off) for c in order}) == "H",
       "SF16: weights less a kilogram of clothing, H")
    # SF18: how the measured operators move the survey's eye height: by sex or pooled, the mean or the median
    # departure, given stature alone, a regression refitted to them, ratio scaling, or weighted to the roster;
    # every reading files H
    def _v(o):
        return {c: AN.acc_carried(ops, W.ENVELOPES[c], offset=o) for c in order}

    sf18 = [("pooled over both sexes", AN.trial_offsets(tr, how="pooled"), 0.01),
            ("the median departure", AN.trial_offsets(tr, how="median"), 0.01),
            ("given stature alone", AN.trial_offsets(tr, given=["S"]), 0.01),
            ("a regression on stature and weight refitted to them", AN.trial_refit(tr), 0.01),
            ("a regression on stature alone refitted to them", AN.trial_refit(tr, cols=1), 0.005),
            ("ratio scaling added to the survey", AN.trial_ratio(tr), 0.005),
            ("pure ratio scaling", AN.trial_ratio(tr, pure=True), 0.005),
            ("each operator measured weighted to the roster", _weighted_offsets(tr, ops), 0.01)]
    for tag, o2, m in sf18:
        v2 = _v(o2)
        ok(AN.pick(v2) == "H" and v2["H"] - W.LINE >= m and W.LINE - max(v2[c] for c in order[:7]) >= m,
           "SF18: the offsets %s file H, %.1f point clear on both sides (G %.2f, H %.2f)"
           % (tag, 100 * m, 100 * v2["G"], 100 * v2["H"]))
    sheet = list(csv.reader(open(os.path.join(target, R.TRIAL))))
    ok(sheet[0] == ["subject", "session_date", "sex", "stature_mm", "weight_kg", "eye_height_sitting_mm"]
       and all(r[0].startswith("FT-") for r in sheet[1:]) and len(sheet) == 141
       and "with their stature and weight on the day" in fit_text,
       "SF19: the sheet carries its own subject numbers, no employee number, stature and weight taken on the day")
    mr = AN.trial_marginal(tr, ops)
    v4 = _v(mr)
    ok(AN.pick(v4) == "G" and v4["G"] - W.LINE >= 0.012, "the raw mean eye heights against the roster's carried "
       "mean (%s mm) file G (%.2f)" % ({sx: round(float(mr[sx][AN.SEH]), 1) for sx in mr}, 100 * v4["G"]))
    ost_hdr = next(csv.reader(open(os.path.join(target, R.OSTRANDER))))
    fh_rows = list(csv.DictReader(open(os.path.join(target, R.FERNHILL))))
    ok("HEIGHT (NO SHOES)" in ost_hdr and "ht_in_no_shoes" in fh_rows[0],
       "SF15: both providers' exports record height without shoes")
    descs = {(r["visit_type"], r["visit_desc"]) for r in fh_rows}
    ok(("DOTPE", "DOT physical examination") in descs and ("DOTRC", "DOT recertification, short certificate") in descs,
       "SF17: Fernhill's export describes recertifications apart from DOT physical examinations")
    rc_blank = all(not r["HEIGHT (NO SHOES)"] and not r["WEIGHT LB"] for r in csv.DictReader(open(os.path.join(target, R.OSTRANDER)))
                   if r["SERVICE"] == "DOT PHYSICAL - RECERT")
    rc_blank &= all(not r["ht_in_no_shoes"] and not r["wt_lb"] for r in csv.DictReader(open(os.path.join(target, R.FERNHILL)))
                    if r["visit_type"] == "DOTRC")
    ok(rc_blank, "SF17: no recertification in either export carries a height or weight")
    last_dot = {}
    for e in st["enc"]:
        if e["type"] in ("PHYS", "RECERT"):
            k = last_dot.get(e["emp"])
            if k is None or e["date"] > k["date"] or (e["date"] == k["date"] and e["type"] == "PHYS"):
                last_dot[e["emp"]] = e
    rc_last = {o["emp"] for o in ops if last_dot[o["emp"]]["type"] == "RECERT"}
    no_rc = [o for o in ops if o["emp"] not in rc_last]
    acc_rc = {c: AN.acc_carried(no_rc, W.ENVELOPES[c], offset=off) for c in order}
    ok(rc_last and AN.pick(acc_rc) == "H" and all("%.1f" % (100 * acc_rc[c]) == "%.1f" % (100 * acc[c]) for c in order),
       "SF17: leaving out the %d operators whose latest DOT visit is a recertification moves no share at one decimal"
       % len(rc_last))
    recent = [o for o in ops if (W.AS_OF - _latest_date(st, o["emp"])).days <= 730]
    ok(AN.pick({c: AN.acc_carried(recent, W.ENVELOPES[c], offset=off) for c in order}) == "H",
       "convergence: operators whose latest physical is within two years only (%d), H" % len(recent))

    # ---- the survey report and the fit report carry what the model reads
    for sx in ("M", "F"):
        for i, (code, name, unit) in enumerate(W.DIMS):
            ok("%s (%s) %.1f %.1f" % (name, unit, W.MEANS[sx][i], W.SDS[sx][i]) in sv, "survey row %s %s" % (sx, code))
    for c in order:
        for d in W.FIT_DIMS:
            lo, hi = W.ENVELOPES[c][d]
            ok("%s to %s" % ("no limit" if lo is None else "{:,}".format(lo), "no limit" if hi is None else "{:,}".format(hi))
               in fit_text, "fit report limit %s %s" % (c, d))
    vocab = re.compile(r"\b(conditional\w*|regression|residual\w*|predict\w*|transport(?:ed|ing)?|carried to|"
                       r"probabilit\w*)\b", re.I)
    for f in (D.STANDARD, D.FIT_REPORT, D.SURVEY):
        ok(not vocab.search(pdf_text(os.path.join(target, f))), "no decisive-step word in %s" % f)
    ok(not vocab.search(pdf_text(os.path.join(target, D.FM_PROCEDURE))), "no decisive-step word in %s" % D.FM_PROCEDURE)
    describing = re.compile(r"dictionar|manifest|readme|read_me|field_?notes|field_?guide|codebook|schema|definition|"
                            r"extract_?notes|export_?notes|notes", re.I)
    ok(not [f for f in os.listdir(target) if describing.search(f)],
       "section 3: no file named as a dictionary, manifest, readme or notes ships")

    # ---- the ask: option maintenance and twelve-year costs
    m = fig["maint"]
    ex = fig["maint_exact"]
    for o in W.OPTION_ORDER:
        ok(abs(ex[o]["rate"] - round(ex[o]["rate"]) - 0.003) < 0.0015, "option %s's rate sits just above a dollar" % o)
        ok(st["bm"][o] % 12 not in (3, 9), "option %s's bus-years off a rounding edge" % o)
    ok(AN.twelve_year(AN.option_maintenance(st), rounded=True) ==
       {c: v for c, v in fig["twelve"].items()}, "twelve-year costs agree from rounded and unrounded rates")
    lazy = AN.option_maintenance(st, labour_per_line=True)
    ok(all(round(lazy[o]["rate"]) != m[o]["rate"] for o in W.OPTION_ORDER), "D6: labour on every line moves every rate")
    roster_only = AN.option_maintenance(st, roster_only=True)
    ok(all(roster_only[o]["bus_months"] < st["bm"][o] for o in ("P", "R")) and
       all(roster_only[o]["bus_months"] == st["bm"][o] for o in ("T", "D", "V")),
       "D5 and D7: today's roster alone loses pedal and riser bus-years only")
    todays = AN.option_maintenance(st, todays_options=True)
    ok(todays["P"]["bus_months"] > st["bm"]["P"] and all(todays[o]["bus_months"] == st["bm"][o] for o in "RTDV"),
       "D2: today's options read into every month inflate pedal bus-years only")
    cracker = AN.option_maintenance(st, labour_per_line=True, roster_only=True, todays_options=True)
    ok(all(round(cracker[o]["rate"]) != m[o]["rate"] for o in W.OPTION_ORDER), "cracker: every rate missed")
    ok(round(cracker["P"]["bus_years"], 1) != m["P"]["bus_years"] and
       round(cracker["R"]["bus_years"], 1) != m["R"]["bus_years"], "cracker: pedal and riser bus-years missed")
    firsts = [r["accepted"] for r in csv.DictReader(open(os.path.join(target, R.FLEET)))]
    for r in csv.DictReader(open(os.path.join(target, R.DISPOSALS))):
        firsts += [r["accepted"], r["disposed"]]
    firsts += [r["completed"] for r in csv.DictReader(open(os.path.join(target, R.RETROFITS)))]
    ok(firsts and not [d for d in firsts if d[8:10] == "01"],
       "the bus-month rule's first day: no acceptance, disposal or fitting in the fleet files falls on a 1st")

    def months_read(opt, keep_disposal_day=False, fit_next_month=False, accept_next_month=False):
        n = 0
        for b in st["buses"]:
            for d in W.month_starts(*W.ASK_YEARS):
                a_ok = b["accepted"] < d if accept_next_month else b["accepted"] <= d
                g_ok = b["disposed"] is None or (d <= b["disposed"] if keep_disposal_day else d < b["disposed"])
                on = list(b["built"]) + [o for o, w in b["retrofit"].items() if (w < d if fit_next_month else w <= d)]
                n += a_ok and g_ok and opt in on
        return n
    ok(all(months_read(o, *flags) == st["bm"][o] for o in W.OPTION_ORDER
           for flags in ((True, False, False), (False, True, False), (False, False, True), (True, True, True))),
       "the bus-month rule's first day: every reading of a disposal, fitting or acceptance day gives the same bus-months")
    reused = [w for w in st["wos"] if w["bus"]["disposed"] is not None and
              any(b["no"] == w["no"] and b["disposed"] is None for b in st["buses"])]
    ok(len(reused) > 100, "D7: disposed buses' work orders carry fleet numbers on today's roster (%d)" % len(reused))
    multi = [w for w in st["wos"] if len(w["lines"]) > 1 and W.COMPONENTS[w["comp"]][1]]
    ok(len(multi) > 200, "D6: option work orders with several lines (%d)" % len(multi))

    # ---- separation: the ask's files feed nothing the call reads
    import build as BD
    ok(not set(BD.ASK_FILES) & set(BD.CALL_FILES), "no file is on both the call's and the ask's path")

    # ---- the goldens agree with figures.json
    gw = openpyxl.load_workbook(os.path.join(golden, "workstation_configurations_2027.xlsx"))
    ws = gw["Configurations"]
    for r in ws.iter_rows(min_row=6, max_row=13, values_only=True):
        c = r[0]
        ok(abs(r[3] - fig["acc_pct"][c] / 100) < 1e-12 and r[2] == W.PRICES[c] and r[5] == fig["twelve"][c] and
           r[4] == ("Yes" if fig["meets"][c] else "No"), "golden row %s" % c)
    mt = gw["Option maintenance"]
    for r in mt.iter_rows(min_row=5, max_row=9, values_only=True):
        o = [k for k in W.OPTION_ORDER if W.OPTIONS[k] == r[0]][0]
        ok(r[2] == round(m[o]["cost"]) and r[3] == m[o]["bus_years"] and r[4] == m[o]["rate"], "golden option %s" % o)
    svg = open(os.path.join(golden, "operator_accommodation_2027.svg")).read()
    for c in order:
        ok("%.1f%%" % fig["acc_pct"][c] in svg, "chart label %s" % c)
    ok("95 per cent" in svg and "Recommended: H" in svg, "chart line and marker")
    print("checks: %d assertions passed" % len(CHECKS))
    return len(CHECKS)


def _ft_in(t):
    m = re.match(r"(\d+)' (\d+)\"", t)
    return int(m.group(1)) * 12 + int(m.group(2))


def _latest_date(st, emp):
    return max(e["date"] for e in st["enc"] if e["emp"] == emp and e["type"] == "PHYS")


def _truth(st, ops):
    """The counted operators at their true stature and weight on 30 September 2026, before any measurement."""
    by = {p["emp"]: p for p in st["people"]}
    return [dict(o, s=by[o["emp"]]["s"], w=by[o["emp"]]["w"]) for o in ops]


def _weighted_offsets(trial, ops):
    """The operators measured's departures from the survey's eye height, averaged with weights that move them to
    the counted operators' statures and weights."""
    out = {}
    for sx, (tr, w) in AN.trial_weights(trial, ops).items():
        dev = np.array([t["seh"] for t in tr]) - AN._seh_pred(sx, [[t["s"], t["w"]] for t in tr])
        out[sx] = np.where(np.arange(len(AN.FIT)) == AN.SEH, float(np.sum(w * dev) / np.sum(w)), 0.0)
    return out


def _count_over_half(ops, env, off=None):
    per = AN.acc_carried(ops, env, per_op=True, offset=off)
    return float(np.mean([p > 0.5 for p in per.values()]))


def _monte_carlo(ops, env, off, n=200000):
    """Each operator's conditional normal sampled with pseudo-random draws: 200,000 per sex, spread over the sex's
    operators."""
    rng = np.random.default_rng(91)
    lo, hi = AN.bounds(env)
    hit = 0.0
    for sx in ("M", "F"):
        rows = [o for o in ops if o["sex"] == sx]
        mfit, mgiv, beta, resid = AN.conditional(sx)
        means = mfit + (np.array([[o["s"], o["w"]] for o in rows]) - mgiv) @ beta.T + off[sx]
        k = max(1, n // len(rows))
        z = rng.standard_normal((len(rows), k, 5)) @ np.linalg.cholesky(resid).T + means[:, None, :]
        hit += np.all((z >= lo) & (z <= hi), axis=2).mean(axis=1).sum()
    return hit / len(ops)


def _pearson_lawley(ops, env, off):
    """The operators' statures and weights replaced by a bivariate normal fitted within sex, carried the same way."""
    lo, hi = AN.bounds(env)
    tot = 0.0
    for sx in ("M", "F"):
        rows = [o for o in ops if o["sex"] == sx]
        x = np.array([[o["s"], o["w"]] for o in rows])
        mfit, mgiv, beta, resid = AN.conditional(sx)
        mu_x, cov_x = x.mean(axis=0), np.cov(x.T)
        m = mfit + (mu_x - mgiv) @ beta.T + off[sx]
        c = resid + beta @ cov_x @ beta.T
        pts = AN.normal_points(17) @ np.linalg.cholesky(c).T + m
        tot += len(rows) * float(np.mean(np.all((pts >= lo) & (pts <= hi), axis=1)))
    return tot / len(ops)
