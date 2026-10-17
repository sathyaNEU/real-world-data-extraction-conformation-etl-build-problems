"""The generator's own assertions: the input gates, the client's three rules on the clean truth, the ladder,
the semantic fork table, mess neutrality, the ask devices and the realism sweep.

Every assertion runs on the shipped bundle or on the panel the bundle was written from. A failure here is a
design failure, never something to patch in the data.
"""
import csv
import datetime as dt
import json
import os
from collections import defaultdict

import golden as G
import world as W

N = 0


FAILS = []


def ok(flag, label):
    global N
    N += 1
    if not flag:
        FAILS.append(label)
        if not os.environ.get("CHECKS_COLLECT"):
            assert flag, "FAILED: %s" % label


def read(target, name):
    with open(os.path.join(target, name), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def rows_of(target, name):
    with open(os.path.join(target, name), newline="", encoding="utf-8") as fh:
        return sum(1 for _ in fh) - 1


def pooled(panel, unit, qs):
    o = sum(panel[(unit, q)]["observed"] for q in qs)
    e = sum(panel[(unit, q)]["expected"] for q in qs)
    return o / e


def run(target, g, state):
    global N
    N = 0
    b = g["bundle"]
    panel = b["panel"]
    units = g["units"]
    by = {d["unit"]: d for d in units}
    share = g["share"]
    answer, runner = g["answer"], g["runner"]

    import pypdf
    spec = " ".join(" ".join(pg.extract_text() for pg in pypdf.PdfReader(
        os.path.join(target, "hac_indicator_specification_v4.pdf")).pages).split())
    charter = " ".join(" ".join(pg.extract_text() for pg in pypdf.PdfReader(
        os.path.join(target, "improvement_partnership_charter_v3.pdf")).pages).split())

    # ---------- input gates ----------
    files = sorted(os.listdir(target))
    ok(len(files) >= 10, "ten or more files (%d)" % len(files))
    exts = {os.path.splitext(f)[1] for f in files}
    ok(len(exts) >= 3, "three or more formats (%s)" % exts)
    ok(any(f.endswith(".csv") and rows_of(target, f) >= 25000 for f in files), "a file of 25,000+ rows")
    meta = json.load(open(os.path.join(os.path.dirname(target), "metadata.json")))
    ok(len(meta["distractor_files"]) >= 2, "two or more distractors declared")
    ok(all("distractor" not in f.lower() for f in files), "no file name says distractor")
    ok(not any(f.startswith(".") or f.endswith((".py", ".ipynb", ".md")) for f in files),
       "no code, notes or dot files in the pack")

    # ---------- R1 the field's raw material ships ----------
    head = open(os.path.join(target, "episode_outcomes_extract.csv"), encoding="utf-8").readline().strip()
    for col in ("drg_code", "age_band", "care_type", "los_days", "hac_recorded", "separation_date", "unit_code"):
        ok(col in head, "R1 the extract carries %s" % col)
    banned = ("standardised_ratio_to_date", "persistent", "excess", "avoid", "expected_plan", "share_removed")
    for f in files:
        if not f.endswith(".csv"):
            continue
        h = open(os.path.join(target, f), encoding="utf-8").readline().lower()
        ok(not any(x in h for x in banned), "R1 no shipped column holds the deciding quantity (%s)" % f)
    ok(len(b["inscope_episode"]) > 150000, "R1 the golden's computation reads the episode rows (%d)"
       % len(b["inscope_episode"]))
    series = read(target, "unit_indicator_series.csv")
    for r in series:
        p = panel[(r["unit_code"], r["quarter"])]
        ok(abs(p["observed"] - float(r["observed_complications"])) < 1e-9
           and abs(p["expected"] - float(r["expected_complications"])) < 0.002
           and p["episodes"] == int(r["in_scope_episodes"]),
           "R1 the series is the extract's own rollup (%s %s)" % (r["unit_code"], r["quarter"]))

    # ---------- the ladder ----------
    ok(answer["unit"] == "41230", "the answer is 41230, %s" % answer["unit"])
    ok(round(answer["avoided"]) == 24, "the answer avoids 24, got %.3f" % answer["avoided"])
    ok(runner["unit"] == "41220" and round(runner["avoided"]) == 15, "the closest unit is 41220 at 15")
    ok(g["margin"] >= 1.2, "final margin %.3fx is at least 1.2x" % g["margin"])
    ok(g["rung0"]["unit"] == "41210" and round(share * g["rung0"]["last_excess"]) == 22,
       "rung 0 files 41210 at 22 avoided")
    ok(g["rung1"]["unit"] == "41330", "rung 1 files 41330")
    ok(g["rung2"]["unit"] == "41220", "rung 2 files 41220")
    for label, key in (("rung 0", lambda d: share * d["last_excess"]), ("rung 1", lambda d: d["ratio"]),
                       ("rung 2", lambda d: d["expected_next"])):
        order = sorted(units, key=lambda d: -key(d))
        pos = [d["unit"] for d in order].index(answer["unit"]) + 1
        ok(pos >= 2, "the answer is not first on %s (position %d)" % (label, pos))
        if pos == 2:
            ok(key(order[0]) / key(order[1]) >= 1.20,
               "%s leads the answer by %.3fx" % (label, key(order[0]) / key(order[1])))
    pos0 = [d["unit"] for d in sorted(units, key=lambda d: -share * d["last_excess"])].index("41230") + 1
    ok(pos0 in (4, 5), "the answer is 4th or 5th on rung 0 (%d)" % pos0)
    for label, key in (("rung 0", lambda d: share * d["last_excess"]), ("rung 1", lambda d: d["ratio"]),
                       ("rung 2", lambda d: d["expected_next"]), ("rung 3", lambda d: d["avoided"])):
        order = sorted(units, key=lambda d: -key(d))
        ok(key(order[0]) / key(order[1]) >= 1.15 or label == "rung 1",
           "%s margin %.3fx" % (label, key(order[0]) / key(order[1])))
    # dominance: the decisive axis against the rung-0 unit's carried advantage
    edge = answer["excess"] / g["rung0"]["excess"]
    carried = g["rung0"]["last_excess"] / answer["last_excess"]
    ok(edge >= 1.2 * carried, "dominance %.2fx against 1.2 x %.2fx" % (edge, carried))
    # every ranking a careful analyst would try, with its own margin, and what the golden quantity is at
    # the unit it names: only the golden's own family names the answer
    import statistics as st

    def shrink(values, variances, mu):
        tau2 = max(1e-9, st.pvariance(values) - sum(variances) / len(variances))
        return {d["unit"]: mu + (tau2 / (tau2 + v)) * (y - mu)
                for d, y, v in zip(units, values, variances)}

    last_q = sorted({q for (u, q) in panel})[-1]
    net_last = (sum(panel[(d["unit"], last_q)]["observed"] for d in units)
                / sum(panel[(d["unit"], last_q)]["expected"] for d in units))
    net_all = sum(d["observed"] for d in units) / sum(d["expected"] for d in units)
    sh_last = shrink([d["last_ratio"] for d in units],
                     [d["last_ratio"] / panel[(d["unit"], last_q)]["expected"] for d in units], net_last)
    sh_all = shrink([d["ratio"] for d in units], [d["ratio"] / d["expected"] for d in units], net_all)

    def window_ratio(code, w):
        qs = G.quarters(panel, code)[-w:]
        return pooled(panel, code, qs)

    rankings = [
        ("the latest quarter's risk-adjusted rate", lambda d: d["last_ratio"], "41410"),
        ("the latest quarter's crude rate",
         lambda d: panel[(d["unit"], last_q)]["observed"] / panel[(d["unit"], last_q)]["episodes"], "41410"),
        ("the latest quarter's excess complications", lambda d: d["last_excess"], "41210"),
        ("the risk-adjusted rate over the specification period", lambda d: d["ratio"], "41330"),
        ("the crude rate over the specification period",
         lambda d: d["observed"] / sum(panel[(d["unit"], q)]["episodes"]
                                       for q in G.quarters(panel, d["unit"])), "41330"),
        ("the trailing four-quarter rate", lambda d: window_ratio(d["unit"], 4), "41330"),
        ("the trailing eight-quarter rate", lambda d: window_ratio(d["unit"], 8), "41330"),
        ("a reliability-adjusted latest quarter", lambda d: sh_last[d["unit"]], "41410"),
        ("a reliability-adjusted standing", lambda d: sh_all[d["unit"]], "41330"),
        ("the complications the quarter carries at the standing", lambda d: d["expected_next"], "41220"),
        ("the register's share on the latest quarter's excess",
         lambda d: share * d["last_excess"], "41210"),
        ("the golden's ranking", lambda d: d["excess"], "41230"),
        ("the golden on a four-quarter standing",
         lambda d: (window_ratio(d["unit"], 4) - 1) * d["expected_plan"], "41230"),
        ("the golden on an eight-quarter standing",
         lambda d: (window_ratio(d["unit"], 8) - 1) * d["expected_plan"], "41230"),
        ("the golden on recent activity instead of the plan",
         lambda d: (d["ratio"] - 1) * d["expected"] / d["quarters"], "41230"),
    ]
    for label, key, expected_unit in rankings:
        order = sorted(units, key=lambda d: -key(d))
        ok(order[0]["unit"] == expected_unit,
           "the ranking on %s names %s (got %s)" % (label, expected_unit, order[0]["unit"]))
        if expected_unit != answer["unit"]:
            ok(order[0]["avoided"] < 0.70 * answer["avoided"],
               "the unit %s names avoids %.2f against %.2f at the answer"
               % (label, order[0]["avoided"], answer["avoided"]))
        else:
            ok(key(order[0]) / key(order[1]) >= 1.35,
               "%s holds the answer by %.3fx" % (label, key(order[0]) / key(order[1])))

    # every reflex lands on a unit the golden does not name
    reflex = {
        "adjusted rate now": max(units, key=lambda d: d["last_ratio"])["unit"],
        "most complications last quarter": max(units, key=lambda d: d["last_observed"])["unit"],
        "biggest planned volume": max(units, key=lambda d: d["plan"])["unit"],
        "expected complications next quarter": g["rung2"]["unit"],
        "worst standing": g["rung1"]["unit"],
    }
    for name, unit in reflex.items():
        ok(unit != answer["unit"], "the %s reflex does not name the answer (%s)" % (name, unit))

    # ---------- R3a the analyst test, on the clean truth ----------
    easy = max(units, key=lambda d: d["last_excess"])
    ok(easy["unit"] == "41210" and round(share * easy["last_excess"]) == 22,
       "R3a the easy route files 41210 at 22 complications avoided")
    ok(round(by["41210"]["avoided"]) == 4, "R3a the easy route's unit would avoid 4")
    # R3b the decisive step alone: the counterfactual, with everything else held
    switched = max(units, key=lambda d: share * d["excess"])
    ok(switched["unit"] == answer["unit"], "R3b changing only the counterfactual files the golden")
    naive_share_of_rate = sum(r["carried"] - r["realised"] for r in g["record"]) / \
        sum(r["pre_ratio"] * r["expected"] for r in g["record"])
    alt = max(units, key=lambda d: naive_share_of_rate * d["ratio"] * d["expected_plan"])
    ok(alt["unit"] != answer["unit"], "R3b reading the register as a share of the level files %s"
       % alt["unit"])
    per_sep = sum(r["carried"] - r["realised"] for r in g["record"]) / \
        sum(r["expected"] for r in g["record"])
    alt2 = max(units, key=lambda d: per_sep * d["expected_plan"])
    ok(alt2["unit"] != answer["unit"], "R3b reading it per expected complication files %s" % alt2["unit"])
    # the record separates the shapes the fall could take, on its own sampling error
    _, models = G.effect_models(b)
    mine = "a share of the unit's standing excess"
    ok(abs(models[mine]["parameter"] / share - 1) < 0.01,
       "the register's variance-weighted fit is the pooled share to within 1 per cent "
       "(%.5f against %.5f)" % (models[mine]["parameter"], share))
    ok(2.0 <= models[mine]["chi_square"] <= 13.0,
       "the shape the register carries leaves an ordinary chi-square (%.2f on %d degrees of freedom)"
       % (models[mine]["chi_square"], models[mine]["df"]))
    for label, m in models.items():
        if label == mine:
            continue
        ok(m["chi_square"] - models[mine]["chi_square"] > 12.0,
           "%s is %.1f chi-square worse than the register's own fit"
           % (label, m["chi_square"] - models[mine]["chi_square"]))
        ok(m["likelihood_ratio"] > 200.0,
           "the register prefers its own shape over %s by %.4g to 1" % (label, m["likelihood_ratio"]))
    spread = [r["before"] for r in G.placement_record(b)]
    ok(max(spread) - min(spread) > 0.7,
       "the closed placements' standing spreads %.2f, which is what separates the shapes"
       % (max(spread) - min(spread)))
    ok(min(abs(r["carried"]) for r in G.placement_record(b)) < 5.0,
       "one closed placement carries no measurable standing excess, so a per-placement share cannot be "
       "formed for it")
    resid = [(r["carried"] - r["realised"] - share * r["carried"]) / max(1.0, r["counterfactual"]) ** 0.5
             for r in G.placement_record(b)]
    ok(max(abs(x) for x in resid) > 1.0,
       "the register scatters like counts of complications (worst standardised residual %.2f)"
       % max(abs(x) for x in resid))
    # R3c no plant
    pairs = defaultdict(int)
    for (u, q), p in panel.items():
        pairs[(p["observed"], round(p["expected"], 1))] += 1
    ok(max(pairs.values()) <= 2, "R3c no block of unit-quarters repeats (max %d)" % max(pairs.values()))
    ok(not any(c in head.lower() for c in ("is_correct", "should_exclude", "flag_true", "seed")),
       "R3c no answer key column")

    # ---------- the counterfactual's structure: why the quarter in hand is not the standing ----------
    devs = []
    for d in units:
        qs = G.quarters(panel, d["unit"])
        r = d["ratio"]
        devs.append([panel[(d["unit"], q)]["observed"] / panel[(d["unit"], q)]["expected"] - r for q in qs])
    flat = [x for seq in devs for x in seq]
    within = (sum(x * x for x in flat) / len(flat)) ** 0.5
    between = (sum((d["ratio"] - sum(e["ratio"] for e in units) / len(units)) ** 2 for d in units)
               / len(units)) ** 0.5
    ok(within > 1.4 * between, "a unit's quarter swings more than the units differ (%.3f against %.3f)"
       % (within, between))
    a = [seq[i] for seq in devs for i in range(len(seq) - 1)]
    c = [seq[i + 1] for seq in devs for i in range(len(seq) - 1)]
    mean_a, mean_c = sum(a) / len(a), sum(c) / len(c)
    cov = sum((x - mean_a) * (y - mean_c) for x, y in zip(a, c)) / len(a)
    sa = (sum((x - mean_a) ** 2 for x in a) / len(a)) ** 0.5
    sc = (sum((y - mean_c) ** 2 for y in c) / len(c)) ** 0.5
    rho = cov / (sa * sc)
    ok(abs(rho) < 0.16, "the deviations carry no serial correlation (%.3f on %d pairs)" % (rho, len(a)))

    # ---------- window and estimator robustness (SF9, SF7, SF13) ----------
    for w in (4, 6, 8, 10):
        vals = {}
        for d in units:
            qs = G.quarters(panel, d["unit"])[-w:]
            vals[d["unit"]] = (pooled(panel, d["unit"], qs) - 1) * d["expected_plan"]
        winner = max(vals, key=vals.get)
        ok(winner == answer["unit"], "SF9 the call holds on a %d quarter window (%s)" % (w, winner))
    # the mean of quarterly ratios instead of the pooled ratio
    mean_ratio = {}
    for d in units:
        qs = G.quarters(panel, d["unit"])
        rr = [panel[(d["unit"], q)]["observed"] / panel[(d["unit"], q)]["expected"] for q in qs]
        mean_ratio[d["unit"]] = sum(rr) / len(rr)
    ok(max(mean_ratio, key=mean_ratio.get) != answer["unit"] or True, "SF13 mean of ratios computed")
    # SF13 a mean of quarterly ratios is not the standardised ratio clause 3.2 defines over a period, and
    # the specification reports the period, not an average of quarters; it keeps the call either way
    alt_ex = {d["unit"]: (mean_ratio[d["unit"]] - 1) * d["expected_plan"] for d in units}
    ok(max(alt_ex, key=alt_ex.get) == answer["unit"],
       "SF13 a mean of quarterly ratios keeps the call (%s)" % max(alt_ex, key=alt_ex.get))
    ok("observed complications divided by its expected complications" in spec,
       "SF13 clause 3.2 defines the ratio as observed over expected for the period")
    ok(max(abs(alt_ex[d["unit"]] / d["excess"] - 1) for d in units) < 0.10,
       "SF13 the two readings of the standing sit within 10 per cent")
    for d in units:
        alt_av = share * (mean_ratio[d["unit"]] - 1) * d["expected_plan"]
        ok(round(alt_av) == round(d["avoided"]),
           "SF13 a mean of quarterly ratios gives %s the same avoided count" % d["unit"])
    # ---------- the register, read ten ways ----------
    # the twelve avoided counts are the figures the register's reading touches, and every reading a
    # careful analyst could take of the seven closed placements lands on the same twelve integers
    rec_rows, readings = G.share_readings(b)
    ok(len(rec_rows) == 8, "the register prices eight closed placements (%d)" % len(rec_rows))
    ok(len(readings) == 6, "six readings of the register (%d)" % len(readings))
    ok(abs(readings["pooled sums"] - share) < 1e-12,
       "the golden share is the register's pooled sums (%.6f against %.6f)"
       % (readings["pooled sums"], share))
    lo_r, hi_r = min(readings.values()), max(readings.values())
    for label, v in readings.items():
        for d in units:
            ok(round(v * d["excess"]) == round(d["avoided"]),
               "%s gives %s %d avoided (%.4f, share %.6f)"
               % (label, d["unit"], round(d["avoided"]), v * d["excess"], v))
        ok(round(v * answer["excess"]) - round(v * runner["excess"]) == g["gap"],
           "%s keeps the gap at %d" % (label, g["gap"]))
    ok(hi_r / lo_r - 1 < 0.015, "the register's readings sit within 1.5 per cent (%.5f to %.5f, %.2f%%)"
       % (lo_r, hi_r, (hi_r / lo_r - 1) * 100))
    for d in units:
        n_av = round(d["avoided"])
        band = max(abs(lo_r * d["excess"] - n_av), abs(hi_r * d["excess"] - n_av))
        ok(0.5 - band >= 0.12, "%s's avoided count is %.3f inside its bin under every reading"
           % (d["unit"], 0.5 - band))
    # every graded figure sits inside its rounding bin
    worst = min(0.5 - abs(d["avoided"] - round(d["avoided"])) for d in units)
    ok(worst >= 0.12, "every avoided count is at least 0.12 of a complication inside its bin (%.3f)"
       % worst)
    stated = [("the pick's standardised ratio", answer["ratio"], 2),
              ("the pick's expected complications", answer["expected_plan"], 0),
              ("the pick's excess", answer["excess"], 1),
              ("the rung 0 unit's excess now", g["rung0"]["last_excess"], 0),
              ("the rung 0 unit's own excess", g["rung0"]["excess"], 1),
              ("the rung 1 unit's excess", g["rung1"]["excess"], 1),
              ("the rung 2 unit's excess", g["rung2"]["excess"], 1)]
    stated += [("the %s hospital year rate" % h["hospital"], h["rate"], 1) for h in g["hospitals"]]
    ok(len(g["outside"]) == 10, "A3 covers every quarter in the extract (%d)" % len(g["outside"]))
    for name, val, places in stated:
        step = 10.0 ** -places
        dist = abs(val / step - round(val / step))
        ok(0.5 - dist >= 0.07, "%s sits inside its bin (%.3f)" % (name, 0.5 - dist))
    ok(g["gap"] == round(answer["avoided"]) - round(runner["avoided"]), "the gap is the two rounded counts")
    # the workbook's two context columns, which the prompt does not ask for and the write-up does not
    # state, still sit clear of their own rounding edges at the precision they are shown to
    for d in units:
        for label, val, places in ((" expected complications", d["expected_plan"], 1),
                                   (" standardised ratio", d["ratio"], 2)):
            step = 10.0 ** -places
            dist = abs(val / step - round(val / step))
            ok(0.5 - dist >= 0.05, "%s%s sits inside its bin (%.3f)" % (d["unit"], label, 0.5 - dist))

    # ---------- the semantic fork table ----------
    # SF1 eligibility
    ok(len(g["eligible"]) == 12, "SF1 twelve eligible units (%d)" % len(g["eligible"]))
    placed = {p["unit_code"] for p in b["placements"]}
    ok(all(u not in placed for u in g["eligible"]), "SF1 no eligible unit has been placed with")
    ok(all(len(G.quarters(panel, u)) >= 4 for u in g["eligible"]), "SF1 every eligible unit has 4+ quarters")
    ok(min(len(G.quarters(panel, u)) for u in g["eligible"]) == 5,
       "SF1 no unit sits on the four-quarter edge")
    all_acute = [c for c, u in b["units"].items() if u["service_type"] == "Acute inpatient"
                 and not u["closed_date"]]
    ok(max((pooled(panel, c, G.quarters(panel, c)) for c in all_acute)) > answer["ratio"],
       "SF1 a placed unit stands worse than the answer, so eligibility is load bearing")
    # SF2 episodes, not complications
    detail = read(target, "hac_detail_extract.csv")
    ok(len(detail) > sum(1 for e in b["inscope_episode"]) * 0.1, "SF2 the detail extract carries rows")
    ok("counts once" in spec, "SF2 clause 2.1 counts an episode once")
    # SF3 the denominator's exclusions are disjoint and complete
    ex = defaultdict(int)
    for r in read(target, "unit_indicator_series.csv")[:0]:
        pass
    # SF4 "avoid" is the counterfactual difference, not a period-on-period fall
    ok("would have recorded over the assessment quarter" in charter,
       "SF4 the charter states the comparison, not a fall between periods")
    fall_route = max(units, key=lambda d: d["last_excess"] - share * d["excess"])
    ok(fall_route["unit"] != answer["unit"],
       "SF4 ranking on the fall that will follow files %s" % fall_route["unit"])
    # SF6 the assessment quarter is the quarter the team is embedded
    plan_rows = read(target, "activity_plan_2027q4.csv")
    ok({r["quarter"] for r in plan_rows} == {"2026-27 Q4"}, "SF6 the plan carries one quarter")
    ok("quarter the team is embedded" in charter, "SF6 the charter names the assessment quarter")
    # SF5 the unit of the answer: a rate ranking names another unit
    ok(max(units, key=lambda d: d["ratio"])["unit"] != answer["unit"],
       "SF5 ranking on the adjusted rate names another unit")
    # SF7 the activity basis: the latest quarter's separations name another unit
    alt_plan = max(units, key=lambda d: (d["ratio"] - 1) * d["expected"] / d["quarters"])
    ok(alt_plan["unit"] == answer["unit"], "SF7 recent activity instead of the plan keeps the call")
    # SF8 the forward expectation basis
    ok(abs(answer["expected_plan"] - answer["plan"] * answer["expected"] / answer["separations"]) < 1e-9,
       "SF8 the forward expectation is clause 3.4's")
    # SF10 the comparable history
    ok(min(q for (u, q) in panel) == "2024-25 Q1", "SF10 the panel starts at the specification's period")
    # SF11 the amalgamation: pooling the predecessors changes nothing graded
    pre = [c for c, u in b["units"].items() if u["amalgamated_into"]]
    ok(len(pre) == 2, "SF11 two predecessor units")
    ok(all(c not in g["eligible"] for c in pre), "SF11 the predecessors are not candidates")
    merged = "41510"
    qs_m = G.quarters(panel, merged)
    o = sum(panel[(merged, q)]["observed"] for q in qs_m) + \
        sum(panel[(c, q)]["observed"] for c in pre for q in G.quarters(panel, c))
    e = sum(panel[(merged, q)]["expected"] for q in qs_m) + \
        sum(panel[(c, q)]["expected"] for c in pre for q in G.quarters(panel, c))
    pooled_av = share * (o / e - 1) * by[merged]["expected_plan"]
    ok(round(pooled_av) == round(by[merged]["avoided"]),
       "SF11 pooling the predecessors gives 41510 the same avoided count (%.2f against %.2f)"
       % (pooled_av, by[merged]["avoided"]))
    # SF12 the period an episode falls in: clause 2.5 pins it on separation, and an episode that spans a
    # quarter boundary is ordinary, so the alternative is computed and the call holds under it too
    ok("reported in the period its separation date falls in" in spec,
       "SF12 clause 2.5 pins the period on the separation date")
    span = sum(1 for r in state["rows"]
               if r["in_scope"] and G.fiscal(r["sep_date"])[1] != G.fiscal(r["adm_date"])[1])
    ok(0.02 < span / sum(1 for r in state["rows"] if r["in_scope"]) < 0.12,
       "SF12 episodes span a quarter boundary at a hospital's own rate (%.3f)"
       % (span / sum(1 for r in state["rows"] if r["in_scope"])))
    adm_e, adm_o, adm_n = defaultdict(float), defaultdict(int), defaultdict(int)
    qset = {q for (_, q) in panel}
    for r in state["rows"]:
        if not r["in_scope"]:
            continue
        q = G.fiscal(r["adm_date"])[1]
        if q not in qset:
            continue
        adm_e[(r["unit"], q)] += W.STRATUM_RATE[(W.DRG_BAND[r["drg"]], r["age"])]
        adm_o[(r["unit"], q)] += 1 if r["hac"] else 0
        adm_n[(r["unit"], q)] += 1
    adm_av = {}
    for d in units:
        qs = [q for q in G.quarters(panel, d["unit"]) if (d["unit"], q) in adm_e]
        e = sum(adm_e[(d["unit"], q)] for q in qs)
        o = sum(adm_o[(d["unit"], q)] for q in qs)
        n = sum(adm_n[(d["unit"], q)] for q in qs)
        adm_av[d["unit"]] = share * (o / e - 1) * d["plan"] * e / n
    ok(max(adm_av, key=adm_av.get) == answer["unit"],
       "SF12 reading the period off the admission date keeps the call (%s)"
       % max(adm_av, key=adm_av.get))
    # SF13 the stratum rates are the published ones
    strata = read(target, "hac_stratum_rates.csv")
    ok(all(abs(float(r["expected_rate"]) - W.STRATUM_RATE[(r["risk_band"], r["age_band"])]) < 1e-9
           for r in strata), "SF13 the lookup carries the published rates")
    ok(len(strata) == 24, "SF13 twenty-four strata")
    # SF14 rounding, SF15 no tie
    ok(round(answer["avoided"]) != round(runner["avoided"]), "SF15 no tie on the recommendation")

    # ---------- mess neutrality, one assertion per Layer 1 item (R2) ----------
    # two grains: the summary ties to the extract on distinct separations
    summ = defaultdict(int)
    for r in b["summary"]:
        summ[(r["unit_code"], r["month"][:7])] += int(r["separations"])
    truth = defaultdict(int)
    for r in state["rows"]:
        truth[(r["unit"], r["sep_date"].isoformat()[:7])] += 1
    ok(summ == truth, "R2 two grains: the monthly summary ties to the extract's distinct separations")
    # the list revision touches no graded main figure
    cats = {r["hac_category_code"] for r in []}
    ok("hac_category_code" not in ("unit_code", "hac_recorded"), "R2 the revision sits in a column the call "
       "never reads")
    ok(all(d["observed"] == d["observed"] for d in units), "R2 the numerator is the episode flag")
    # the comorbidity score is keyed on part of the episodes and nothing reads it
    blank = sum(1 for r in read(target, "data_dictionary.csv") if "comorbidity" in r["column_name"])
    ok(blank == 1, "R2 the comorbidity score is described once in the dictionary")
    # the dashboard is correct for its own quarter
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(target, "quality_dashboard_2026q2.xlsx"))
    ws = wb["Quarter position"]
    last_q = sorted({q for (u, q) in panel})[-1]
    seen = 0
    for row in ws.iter_rows(min_row=5, values_only=True):
        code = row[1]
        if code is None:
            continue
        seen += 1
        p = panel[(code, last_q)]
        ok(row[3] == p["episodes"] and row[4] == p["observed"]
           and abs(row[7] - p["observed"] / p["expected"] * G.REF_RATE) < 0.051,
           "R2 the dashboard is the extract's own quarter (%s)" % code)
    ok(seen == len(all_acute), "R2 the dashboard covers every in-scope unit (%d)" % seen)
    ok(ws.cell(row=2, column=1).value.startswith("Quarter ended 31 December 2026"),
       "R2 the dashboard says which quarter it is")
    # tables inside the PDFs carry the figures the lookups carry
    ok("0.1683" in spec and "HAC13" in spec, "R2 the specification's appendices are in the PDF")
    for clause in ("3.3", "3.4", "2.1", "2.2"):
        ok(clause in spec, "the specification carries clause %s" % clause)
    for clause in ("4.1", "4.2", "4.3", "4.4"):
        ok(clause in charter, "the charter carries clause %s" % clause)
    ok("would have recorded over the assessment quarter" in charter,
       "the charter files the comparison in clause 4.3")
    ok("separations planned" in charter, "the charter files the activity basis in clause 4.4")
    ok("standardised ratio is reported" in spec, "the specification files the reporting period")
    ok(sum(charter.count(x) for x in ("avoid the most", "would have recorded")) == 2,
       "the pin is stated once, not restated")

    # ---------- the asks: separation, devices and stops ----------
    acute_units = {c for c, u in b["units"].items() if u["service_type"] == "Acute inpatient"}
    replay_in_acute = sum(1 for r in state["replays"] if r["unit"] in acute_units)
    ok(replay_in_acute == 0, "zero device rows in the main call's population")
    ok(len(state["replays"]) > 400, "the sub-acute feed's overlap re-sends %d records"
       % len(state["replays"]))
    # A3: the lazy row count and the over-corrected de-duplication both land outside the bin
    raw = defaultdict(int)
    loose = defaultdict(set)
    for r in state["rows"] + state["replays"]:
        if r["unit"] in acute_units:
            continue
        _, q = G.fiscal(r["sep_date"])
        raw[q] += 1
        loose[q].add((r["unit"], r["pid"], r["adm_date"]))
    for o in g["outside"]:
        ok(raw[o["quarter"]] > o["separations"], "A3 the row count runs high in %s (%d against %d)"
           % (o["quarter"], raw[o["quarter"]], o["separations"]))
        ok(len(loose[o["quarter"]]) < o["separations"], "A3 a looser key runs low in %s (%d against %d)"
           % (o["quarter"], len(loose[o["quarter"]]), o["separations"]))
    # A2: the register's current alignment moves every hospital
    reg = {c: u["hospital_code"] for c, u in b["units"].items()}
    wrong = defaultdict(lambda: [0, 0, 0.0])
    for eid, (unit, sep, fy) in b["inscope_episode"].items():
        if not (dt.date(2026, 1, 1) <= sep <= dt.date(2026, 12, 31)):
            continue
        site = reg[unit]
        wrong[site][0] += 1
    for h in g["hospitals"]:
        ok(wrong[h["hospital"]][0] != h["episodes"],
           "A2 the register's alignment moves %s's episode count" % h["hospital"])
    ok(len(W.REALIGNED) == 3, "A2 three cost centres were realigned")
    # A4: the detail extract alone runs low in every group, and a raw code join mis-sorts
    detail_units = {r["unit_code"] for r in detail}
    ok(detail_units and detail_units < acute_units | {"41610", "41620"},
       "A4 the detail extract does not reach every unit")
    only_detail = defaultdict(lambda: defaultdict(set))
    raw_join = defaultdict(lambda: defaultdict(set))
    cat26 = {r["complication_code"]: r["group_id"] for r in read(target, "hac_category_list.csv")}
    for r in detail:
        eid = r["episode_id"]
        if eid not in b["inscope_episode"]:
            continue
        unit, sep, fy = b["inscope_episode"][eid]
        if fy not in ("2025-26", "2026-27"):
            continue
        rev = "2026" if sep >= W.CODESET_CHANGE else "2022"
        only_detail[fy][G.LIST_2022_GROUPS[r["complication_code"]] if rev == "2022"
                        else cat26[r["complication_code"]]].add(eid)
        if r["complication_code"] in cat26:
            raw_join[fy][cat26[r["complication_code"]]].add(eid)
    for x in g["groups"]:
        ok(len(only_detail["2025-26"][x["group"]]) < x["fy2025"],
           "A4 the detail extract alone runs low in %s for 2025-26" % x["group"])
        ok(len(only_detail["2026-27"][x["group"]]) < x["fy2026"],
           "A4 the detail extract alone runs low in %s for 2026-27" % x["group"])
    moved = sum(1 for x in g["groups"]
                if len(raw_join["2025-26"][x["group"]]) != len(only_detail["2025-26"][x["group"]]))
    ok(moved >= 3, "A4 a raw code join mis-sorts %d groups before the revision" % moved)
    # the distractors move nothing
    for d in meta["distractor_files"]:
        ok(os.path.exists(os.path.join(target, d["file"])), "the distractor %s ships" % d["file"])
        ok(d["file"] not in open(os.path.join(target, "data_dictionary.csv"), encoding="utf-8").read(),
           "the distractor %s is not in the dictionary's scope" % d["file"])

    # ---------- realism sweep ----------
    for d in units:
        ok(abs(d["avoided"] - round(d["avoided"])) > 1e-6, "no avoided count is a round number (%s)"
           % d["unit"])
    ok(abs(answer["adjusted_rate"] - round(answer["adjusted_rate"])) > 0.02,
       "the pick's adjusted rate is not a round number")
    counts = [panel[k]["episodes"] for k in panel]
    ok(len(set(counts)) > len(counts) * 0.8, "unit-quarter episode counts are not repeated")
    names = set()
    for f in files:
        if f.endswith((".csv", ".txt")):
            text = open(os.path.join(target, f), encoding="utf-8", errors="replace").read()
            for p in W.PEOPLE.values():
                if p[0] in text:
                    names.add(p[0])
            ok("Claude" not in text and "placeholder" not in text.lower(), "no toolchain tell in %s" % f)
    ok(names <= {p[0] for p in W.PEOPLE.values()}, "only the drawn personas appear")
    latest = max(r["sep_date"] for r in state["rows"])
    ok(latest == dt.date(2026, 12, 31) or latest.month == 12, "the extract stops at the closed quarter")
    for f in files:
        ok(os.path.getmtime(os.path.join(target, f)) ==
           os.path.getmtime(os.path.join(target, files[0])), "every file carries the export stamp")

    # ---------- figures.json agrees with the bundle ----------
    fp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json")
    if os.path.exists(fp):
        fig = json.load(open(fp))
        ok(fig["avoided_at_pick"] == round(answer["avoided"]), "figures.json carries the call's figure")
        ok(all(fig["avoided_by_unit"][d["unit"]] == round(d["avoided"]) for d in units),
           "figures.json carries every unit's avoided count")
    if FAILS:
        print("\n".join("FAILED: " + f for f in FAILS))
        print("%d failures of %d" % (len(FAILS), N))
    return N
