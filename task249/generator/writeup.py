"""figures.json and submission.md, both emitted from the golden computed on the shipped pack."""
import json
import os

import pandas as pd

import params as P
import records as R
import sim
import solve as S

ORDER = [P.CODE[k] for k in P.KEYS]
REFIT_WITHIN = 0.1        # per cent: the claim the refit is graded against (asserted in checks.py)
CORRIDOR = (0, 3)         # per cent an hour: every threshold in it files the golden (asserted in checks.py)
CHECK_NAMES = {"blank": "blank filter", "recovery": "control recovery", "agreement": "aliquot agreement"}


def figures(target, F):
    g = S.solve(target)
    call = g["call"]
    over = sorted(c for c, v in call.items() if v["verdict"] == "over")
    under = sorted(c for c, v in call.items() if v["verdict"] == "under")
    refit_gap = max(abs(v) for v in _refit_gaps(target).values())
    b = pd.read_csv(os.path.join(target, F["batches"]))
    bt = b.drop_duplicates("batch").set_index("batch")
    failed_rows = []
    for k in g["failed_batches"]:
        c1, c2, ref, blank = g["qc"][k]
        why = []
        if abs(blank) > 0.5:
            why.append("blank filter %+.2f mg" % blank)
        for i, c in ((1, c1), (2, c2)):
            if not 0.9 <= c / ref <= 1.1:
                why.append("control aliquot %d at %.0f per cent" % (i, 100 * c / ref))
        if abs(c1 - c2) / ((c1 + c2) / 2) > 0.10:
            why.append("aliquots %.0f per cent apart" % (100 * abs(c1 - c2) / ((c1 + c2) / 2)))
        failed_rows.append([k, bt.loc[k, "weighed"], "; ".join(why), int((b["batch"] == k).sum())])
    f = pd.read_csv(os.path.join(target, F["field"]), keep_default_na=False)
    n27 = {c: int(((f["station"] == c) & (f["sampled"].str[:4] == "2027")).sum()) for c in ORDER}
    return {
        "call": {"over": over, "under": under, "within": sorted(set(ORDER) - set(over) - set(under)),
                 "verdict": {c: call[c]["verdict"] for c in ORDER}, "tolerance_pct": P.REVIEW_TOLERANCE,
                 "n_reissue": len(over) + len(under), "n_stations": len(ORDER)},
        "components": {"refit_reproduces_published_within_pct": REFIT_WITHIN, "refit_gap_max_pct": round(refit_gap, 3),
                       "published_t": {c: call[c]["published_t"] for c in ORDER}},
        "steps": {"rising_threshold_pct_per_h": round(100 * sim.RISE, 1),
                  "rising_corridor_pct_per_h": list(CORRIDOR), "interval_seconds": int(round(sim.DT * 3600)),
                  "old_sonde_limit_fnu": int(P.OLD_LIMIT),
                  "lot_concentration_mg_l": {lot: conc for lot, conc, _, _ in R.LOTS}},
        "asks": {"hours_without_usable_reading": {c: int(round(g["ask_a"][c]["hours"])) for c in ORDER},
                 "samples_in_failed_batches": {c: g["ask_b"][c] for c in ORDER},
                 "failed_batches": g["failed_batches"]},
        "_golden": {"call": call, "ask_a": g["ask_a"], "failed_rows": failed_rows, "n27": n27},
    }


def _refit_gaps(target):
    import routes as RT
    tab = RT.all_routes(target)
    return {c: v["refit"] for c, v in tab.items()}


def golden_content(fig):
    G = fig["_golden"]
    reg = {P.CODE[k]: (P.NAME[k], P.KIND_LABEL[P.SPEC[k][0]]) for k in P.KEYS}
    a = {c: dict(v, hours_whole=int(round(v["hours"]))) for c, v in G["ask_a"].items()}
    return {"order": ORDER, "call": G["call"], "name": {c: reg[c][0] for c in ORDER},
            "regime": {c: reg[c][1] for c in ORDER}, "ask_a": a, "ask_b": fig["asks"]["samples_in_failed_batches"],
            "failed_rows": G["failed_rows"], "n27": G["n27"]}


def write_figures(path, fig):
    out = {k: v for k, v in fig.items() if not k.startswith("_")}
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
        fh.write("\n")


def submission(fig):
    c = fig["call"]
    names = {P.CODE[k]: P.NAME[k] for k in P.KEYS}
    words = {0: "no", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight",
             9: "nine", 10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen"}
    ordered = [x for x in ORDER if x in c["over"]]
    over = ", ".join(ordered[:-1]) + " and " + ordered[-1] if len(ordered) > 1 else ordered[0]
    A = fig["asks"]["hours_without_usable_reading"]
    B = fig["asks"]["samples_in_failed_batches"]
    lines = []
    lines.append("## Tags\n")
    lines.append("**Domain:** Physical & Environmental Sciences (sensor calibration and measurement: turbidity "
                 "surrogates for the suspended-sediment loads a consultancy publishes for a hydropower company).  ")
    lines.append("**Analytical objective:** Data Quality Monitoring & Alerting.\n")
    lines.append("## 1. Final Recommendation\n")
    lines.append("**Re-issue the published 2027 loads of %s stations, %s, all over by more than 15 per cent; the other "
                 "%s stand.** At those four the calibration samples were taken mostly on rising water, when a unit of "
                 "turbidity carries more sediment, and the published regression carries that into every hour of the year. "
                 "Not the published regression refitted, which reproduces every load; not discharge, season or the "
                 "trip type added to it, which leave the rising-water samples' excess in the year's other hours.\n"
                 % (words[c["n_reissue"]], over, words[c["n_stations"] - c["n_reissue"]]))
    lines.append("## 2. Critical Components\n")
    lines.append("1. The procedure's regression refitted on the same samples reproduces all 14 published loads to within "
                 "**%s per cent**." % fig["components"]["refit_reproduces_published_within_pct"])
    lines.append("2. With an indicator of rising water at each sample, the relation of concentration to turbidity is "
                 "higher on rising water at SKB, JVB, FND and ESK, and the trip type then adds nothing at any station.")
    lines.append("3. Over by more than 15 per cent: **%s**; under: none; within: the other **%s**.\n"
                 % (over, words[c["n_stations"] - c["n_reissue"]]))
    lines.append("## 3. Step-by-Step Solution\n")
    lines.append("1. Joined field_samples_2025-2027.csv to lims_ssc_results_2025-2027.xlsx on year and bottle number "
                 "(final results; both sheets) and paired each sample, at its UTC time, with the station's nearest "
                 "15-minute turbidity reading in sediment_stations_15min_2025-2027.parquet.")
    lines.append("2. Refitted SMP-03 section 6 (log10 concentration on log10 turbidity, Duan's smearing) and applied "
                 "it to 2027's intervals (section 7): every load in suspended_sediment_loads_2027.pdf to within %s per "
                 "cent." % fig["components"]["refit_reproduces_published_within_pct"])
    lines.append("3. Marked each sample and each 2027 interval as on rising water when the 15-minute discharge's rate of "
                 "rise, averaged over the hour, exceeded %s per cent an hour (any threshold from %d to %d per cent an "
                 "hour gives the same four), and added that indicator to each station's regression with Duan's "
                 "smearing." % (fig["steps"]["rising_threshold_pct_per_h"], *fig["steps"]["rising_corridor_pct_per_h"]))
    lines.append("4. Applied each station's relation to every 15-minute interval of 2027 with that interval's own "
                 "indicator, summed concentration times discharge times %d seconds, and compared the published load "
                 "with it (section 8, 15 per cent either way): %s over, none under." % (fig["steps"]["interval_seconds"], over))
    lines.append("5. Counted, per station, the 15-minute intervals of 2025 and 2026 with no row, flagged fouled or sonde "
                 "out (F and M, and G and O before the data team's migration of 14 April 2026, which the maintenance "
                 "log's cleaning visits match; K and C are checks and usable), or at %s FNU before the station's "
                 "TS-40W was installed (station register, maintenance log), re-sent rows once, and divided by four."
                 % "{:,}".format(fig["steps"]["old_sonde_limit_fnu"]))
    lines.append("6. Took each 2027 batch in lab_batch_export_2027.csv once, computed each control aliquot as net mass "
                 "over volume against its lot's concentration in SMA_quality_statement_2027.pdf (%s mg/L), applied "
                 "section 4's three checks, and counted each station's sample lines in the %d failed batches."
                 % (", ".join("%s %.1f" % kv for kv in fig["steps"]["lot_concentration_mg_l"].items()),
                    len(fig["asks"]["failed_batches"])))
    lines.append("7. Re-issue the 2027 loads of %s.\n" % over)
    lines.append("## 4. Deliverable Answers\n")
    lines.append("### sediment_load_review_2027.xlsx\n")
    lines.append("1. Verdict on each station's published 2027 load (15 per cent either way):")
    for code in ORDER:
        v = c["verdict"][code]
        lines.append("   - %s %s: %s" % (code, names[code], "over by more than 15 per cent, re-issue" if v == "over"
                                         else ("under by more than 15 per cent, re-issue" if v == "under" else "within 15 per cent, stands")))
    lines.append("2. Hours in 2025 and 2026 without a usable turbidity reading, whole hours:")
    for code in ORDER:
        lines.append("   - %s: %s" % (code, "{:,}".format(A[code])))
    lines.append("3. 2027 samples weighed in a batch that failed its quality control:")
    for code in ORDER:
        lines.append("   - %s: %d" % (code, B[code]))
    lines.append("\n### station_loads_2027.png\n")
    lines.append("1. Each of the 14 stations' published 2027 load against the review's estimate on a log scale, the four "
                 "outside the tolerance (SKB, JVB, FND, ESK) in bold.")
    return "\n".join(lines) + "\n"
