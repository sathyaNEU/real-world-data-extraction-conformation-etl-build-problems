"""task252 figures (every number the write-up and the goldens state, emitted from the pack) and submission.md."""
import json

import numpy as np

import checks as K
import params as P
import solve as S

ORDER = ["BRN-FW1", "CAL-FI1", "DUN-FW1", "ELS-FW1", "GAR-FI1", "GAR-FW1"]
LINE = [("CAL", "fil"), ("HOL", "fil")]


def _join(xs):
    return ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else xs[0]


def _share_words(v):
    """a share lost in plain words, as an analyst would round it in a note"""
    if v >= 0.9:
        return "nearly all"
    return "about %d per cent" % int(round(v * 20) * 5)


def figures(target):
    D = S.load(target); L = S.lims(target); C = S.checks(target); V = S.visits(target)
    off, info = S.offsets(target, S.CARRY, "corr", D, L, C, V=V)
    base = S.offsets(target, S.CARRY, "corr", D, L, C, line="none", V=V)[0]
    rs = list(K.family(target, D, L, C, V, off, info).values())
    fl = S.flags(off)
    names = [S.name(k) for k in fl]
    assert names == ORDER, names
    assert all(S.flags(r) == fl for r in rs)
    assert sorted(k for k in off if S.recovers(info[k])) == LINE
    others = [k for k in off if k not in fl]
    lo_flag = min(abs(r[k]) for r in rs for k in fl)
    hi_other = max(abs(r[k]) for r in rs for k in others)
    pk = {c: S.pooled(D[c]) for c in P.CODES}
    worn = ["BRN", "DUN", "ELS", "GAR", "HOL"]
    A = S.ask_a(target, L)
    B = S.ask_b(target, D)
    lo, hi = S.clock_bracket(L)
    hol_dev = info["HOL"]["dev"]; cal_dev = info["CAL"]["dev"]
    rest = [k for k in off if k not in LINE]
    fig = {
        "call": _join(ORDER),
        "threshold": P.THRESH,
        "check_standard": P.CHECK_STD,
        "n_flagged": len(fl),
        "flagged": names,
        "flag_band_low": round(lo_flag, 4),
        "flag_band_print": round(float(np.floor(lo_flag * 1000) / 1000 - 0.001), 3),
        "unflagged_band_high": round(hi_other, 4),
        "unflagged_band_print": round(float(np.ceil(hi_other * 1000) / 1000), 3),
        "hol_zero_error": round(hol_dev, 3),
        "cal_span_pct": round(abs(cal_dev) / P.CHECK_STD * 100),
        "carry_share_1": round(float(np.mean([pk[c]["k1"] for c in worn])) * 100),
        "carry_share_2": round(float(np.mean([pk[c]["k2"] for c in worn])) * 100),
        "carry_share_healthy": 1,
        "default_path": _join(["BRN-FW1", "DUN-FW1", "ELS-FW1", "GAR-FI1", "GAR-FW1", "HOL-FI1"]),
        "hol_fi1_before_line": round(base[("HOL", "fil")], 3),
        "cal_fi1_before_line": round(base[("CAL", "fil")], 3),
        "hol_fi1_offset": round(off[("HOL", "fil")], 3),
        "cal_fi1_offset": round(off[("CAL", "fil")], 3),
        "cal_fi1_bound": round(float(np.floor(min(abs(r[("CAL", "fil")]) for r in rs) * 1000) / 1000), 3),
        "line_share": {S.name(k): round(info[k]["share"], 2) for k in LINE},
        "line_share_words": {S.name(k): _share_words(info[k]["share"]) for k in LINE},
        "line_tau_days": round(float(np.mean([info[k]["tau"] for k in LINE])), 1),
        "line_step_low": {S.name(k): round(min(info[k]["steps"]), 3) for k in LINE},
        "line_step_high": {S.name(k): round(max(info[k]["steps"]), 3) for k in LINE},
        "line_loss_mean": {S.name(k): round(-info[k]["lossbar"], 3) for k in LINE},
        "other_loss_max": round(max(abs(info[k]["lossbar"]) for k in rest), 3),
        "worn": ["Brannock", "Dunmere", "Elstow", "Garrick", "Holmedale"],
        "clock_lo": int(round(lo)),
        "clock_hi": int(round(hi)),
        "ask_a": {P.NAME[c]: int(A[c]) for c in P.CODES},
        "ask_b": {P.NAME[c]: round(B[c], 1) for c in P.CODES},
        "offsets": {S.name(k): round(v, 4) for k, v in sorted(off.items())},
        "carry": {S.name(k): round(pk[k[0]]["co"][k[1]], 4) for k in sorted(off)},
        "line": {S.name(k): round(info[k]["lossbar"] if k in LINE else 0.0, 4) for k in sorted(off)},
        "analysers": {c: dict(k1=round(info[c]["k"][0], 3), k2=round(info[c]["k"][1], 3),
                              check_mean=round(float(np.mean(C[c])), 4), form=info[c]["kind"] or "none")
                      for c in P.CODES},
    }
    return fig


def write_figures(path, fig):
    with open(path, "w") as fh:
        json.dump(fig, fh, indent=1, ensure_ascii=False)
        fh.write("\n")


def submission(fig):
    a = fig["ask_a"]; b = fig["ask_b"]
    sw = fig["line_share_words"]; lm = fig["line_loss_mean"]
    lines = [
        "## Tags",
        "",
        "**Domain:** Physical and environmental sciences (sensor calibration and measurement).",
        "**Analytical objective:** Data quality monitoring and alerting.",
        "",
        "## 1. Final Recommendation",
        "",
        "**Flag %s in the fourth-quarter 2027 return: these six treated-water channels read more than 0.005 mg/L as "
        "N off the water at their sample points.**" % fig["call"],
        "Each listed channel is %.3f or more off and every other channel within %.3f of zero, once each analyser's "
        "carryover from the two ports before a reading, its calibration error at the channel's own level and the "
        "ammonia its sample line takes before the cell are all counted. Not HOL-FI1: its carryover from the raw "
        "sample is cancelled by its filtered line's loss. Not HOL-FW1: its carryover from the raw sample two ports "
        "back is cancelled by Holmedale's zero error. Not CAL-FW1: Calderwood's calibration error is a span error, "
        "small at treated levels."
        % (fig["flag_band_print"], fig["unflagged_band_print"]),
        "",
        "## 2. Critical Components",
        "",
        "1. Five analysers (%s) do not empty their measuring cell between ports: each reading is a mix of its own "
        "sample with small shares of the two samples before it, so the channel read straight after raw water reads "
        "high, and at Garrick and Holmedale, with raw water two to three times the others', so does the channel read "
        "two ports after it." % _join(fig["worn"]),
        "2. Holmedale's analyser reads **%.3f** low at every level, a zero error that cancels HOL-FW1's carryover; "
        "Calderwood's reads about **%d per cent** low, a span error." % (abs(fig["hol_zero_error"]),
                                                                           abs(fig["cal_span_pct"])),
        "3. Calderwood's and Holmedale's filtered sample lines take %s and %s of the filtered water's ammonia before "
        "the cell once the line has grown its film again: their readings rise at every monthly line flush and fall "
        "back over the following days, on average about **%.3f** and **%.3f** below the water over the quarter."
        % (sw["CAL-FI1"], sw["HOL-FI1"], lm["CAL-FI1"], lm["HOL-FI1"]),
        "4. With the line counted, CAL-FI1 reads **%.3f** or more below its water and HOL-FI1 sits within **%.3f** of "
        "zero." % (fig["cal_fi1_bound"], fig["unflagged_band_print"]),
        "",
        "## 3. Step-by-Step Solution",
        "",
        "1. Read WQ-DS-04 sections 3 and 4 (the offset over the channel's G readings in the historian against the water "
        "at its sample point, flagged beyond 0.005 either way) and the register's port sequences and planned "
        "maintenance log; kept each slot's G row, a filled-in slot's G row standing over its F row, and took each "
        "reading's port from its sample point.",
        "2. For each analyser, fitted the carryover as a mix in the cell: both treated ports' readings together on the "
        "readings of the two slots before them (check readings as the cell's content), one pair of shares for the "
        "analyser, each port with its own level and its own response to the raw readings 2 to 8 hours earlier; each "
        "channel's carryover offset is the shares of the differences between the two slots before it and its own "
        "reading, divided by one less both shares. %s carry about %d per cent of the slot before and %d per cent of "
        "the one before that, the other three under %d per cent."
        % (_join(fig["worn"]), fig["carry_share_1"], fig["carry_share_2"], fig["carry_share_healthy"]),
        "3. Took each analyser's check mean from analyser_verification_2027Q4.xlsx and set it beside the raw grabs in "
        "lims_ammonia_2027Q4.csv, each paired with the raw reading of its slot with the raw port's own carryover taken "
        "out: Holmedale's shortfall is the same at both levels (a zero error), Calderwood's in proportion (a span "
        "error), the other six within 0.002 of 0.100.",
        "4. Took each treated reading's carryover and calibration error out and fitted what was left on the days since "
        "the last monthly line flush in the planned maintenance log (New Zealand time): a level, the raw readings 2 to "
        "8 hours earlier, and a loss that grows back as one less an exponential in those days. Only Calderwood's and "
        "Holmedale's filtered channels rise at every flush (by %.3f to %.3f and %.3f to %.3f, the six hours after it "
        "against the two days before) and fall back over the following days (a regrowth time of %.1f days for both); "
        "no other channel moves at the flushes."
        % (fig["line_step_low"]["CAL-FI1"], fig["line_step_high"]["CAL-FI1"], fig["line_step_low"]["HOL-FI1"],
           fig["line_step_high"]["HOL-FI1"], fig["line_tau_days"]),
        "5. Added to each of those two channels its line's fitted loss averaged over its G readings (%.3f and %.3f "
        "below the water), summed each channel's carryover, calibration error at its own level and line loss, and "
        "flagged beyond 0.005: %s." % (lm["CAL-FI1"], lm["HOL-FI1"], fig["call"]),
        "6. For each plant's treated samples, moved the laboratory's analysis stamps forward an hour: some runs are "
        "stamped up to %d minutes before reception logged their bottles and no result is released within %d minutes of "
        "its stamp, so the stamps run behind the laboratory's other clocks and every shift in that range counts the "
        "same; mapped the October codes through the laboratory's notice; counted each bottle once, the 7 December "
        "round's treated bottles being logged a second time under the courier docket's pickup time with the same point, "
        "analysis stamp, result and release; and counted those analysed more than 24 hours after collection."
        % (fig["clock_lo"], fig["clock_hi"]),
        "7. For each plant's filtered water port, treated as available to the PLC every slot except the check cycles "
        "and the slots no reading reached it: a failed poll later filled from the outstation, the historian's lost "
        "hours of 17 November and each run of unfilled F rows at every port that no check followed and across which "
        "the analyser's port sequence ran on unbroken (the November outstation changes) were the historian's alone, "
        "while the runs after which the sequence starts again at the raw water port (each analyser's stop on the storm "
        "night of 26 to 27 October or 3 to 4 December, until the morning reset) and the filtered port's own unfilled F "
        "rows, the other ports read between them (once at each plant), never reached the PLC; summed each gap between "
        "good readings beyond the two-hour hold.",
        "",
        "## 4. Deliverable Answers",
        "",
        "### ammonia_channel_offsets_2027Q4.xlsx",
        "",
        "1. Flagged channels, six: %s." % fig["call"],
        "2. Filtered and final water samples analysed more than 24 hours after collection, by plant:",
    ]
    for c in P.CODES:
        lines.append("   - %s: %d" % (P.NAME[c], a[P.NAME[c]]))
    lines.append("3. Hours at the fixed chlorine dose because the filtered water ammonia reading was not available, by "
                 "plant:")
    for c in P.CODES:
        lines.append("   - %s: %.1f" % (P.NAME[c], b[P.NAME[c]]))
    lines += ["",
              "### ammonia_channel_offsets_2027Q4.png",
              "",
              "1. Every treated channel's quarter offset by plant against the 0.005 band, the six flagged channels "
              "marked.",
              ""]
    return "\n".join(lines)
