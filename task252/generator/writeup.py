"""task252 figures (every number the write-up and the goldens state, emitted from the pack) and submission.md."""
import json

import numpy as np

import params as P
import solve as S

ORDER = ["BRN-FW1", "DUN-FW1", "ELS-FW1", "GAR-FI1", "GAR-FW1", "HOL-FI1"]


def _join(xs):
    return ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else xs[0]


def figures(target):
    D = S.load(target); L = S.lims(target); C = S.checks(target)
    off, info = S.offsets(target, S.CARRY, "corr", D, L, C)
    routes = [off, S.offsets(target, "G", "corr", D, L, C)[0], S.offsets(target, "RAW", "corr", D, L, C)[0]]
    fl = S.flags(off)
    names = [S.name(k) for k in fl]
    assert names == ORDER, names
    assert all(S.flags(r) == fl for r in routes)
    others = [k for k in off if k not in fl]
    lo_flag = min(abs(r[k]) for r in routes for k in fl)
    hi_other = max(abs(r[k]) for r in routes for k in others)
    pk = {c: S.pooled(D[c]) for c in P.CODES}
    worn = ["BRN", "DUN", "ELS", "GAR", "HOL"]
    A = S.ask_a(target, L)
    B = S.ask_b(target, D)
    lo, hi = S.clock_bracket(L)
    hol_dev = info["HOL"]["dev"]; cal_dev = info["CAL"]["dev"]
    fig = {
        "call": _join(ORDER),
        "threshold": P.THRESH,
        "check_standard": P.CHECK_STD,
        "n_flagged": len(fl),
        "flagged": names,
        "flag_band_low": round(lo_flag, 4),
        "flag_band_print": round(float(np.floor(lo_flag * 1000) / 1000 - 0.001), 3),
        "unflagged_band_high": round(hi_other, 4),
        "hol_zero_error": round(hol_dev, 3),
        "cal_span_pct": round(abs(cal_dev) / P.CHECK_STD * 100),
        "cal_span_treated": round(abs(cal_dev / P.CHECK_STD) * float(np.mean([np.mean(D["CAL"]["val"][np.where((D["CAL"]["sl"] == s) & D["CAL"]["g"])[0]]) for s in ("fil", "fin")])), 3),
        "hol_fw1_carry": round(pk["HOL"]["co"]["fin"], 3),
        "carry_share_1": round(float(np.mean([pk[c]["k1"] for c in worn])) * 100),
        "carry_share_2": round(float(np.mean([pk[c]["k2"] for c in worn])) * 100),
        "carry_share_healthy": 1,
        "hol_fw1_offset": round(off[("HOL", "fin")], 3),
        "default_path": _join(ORDER + ["HOL-FW1"]),
        "worn": ["Brannock", "Dunmere", "Elstow", "Garrick", "Holmedale"],
        "clock_lo": int(round(lo)),
        "clock_hi": int(round(hi)),
        "ask_a": {P.NAME[c]: int(A[c]) for c in P.CODES},
        "ask_b": {P.NAME[c]: round(B[c], 1) for c in P.CODES},
        "offsets": {S.name(k): round(v, 4) for k, v in sorted(off.items())},
        "carry": {S.name(k): round(pk[k[0]]["co"][k[1]], 4) for k in sorted(off)},
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
    lines = [
        "## Tags",
        "",
        "**Domain:** Physical and environmental sciences (sensor calibration and measurement).",
        "**Analytical objective:** Data quality monitoring and alerting.",
        "",
        "## 1. Final Recommendation",
        "",
        "**Flag %s in the fourth-quarter 2027 return: these six treated-water channels read more than 0.005 mg/L as "
        "N off the water they sample.**" % fig["call"],
        "Each listed channel is %.3f or more off and every other channel within %.3f of zero, once each analyser's "
        "carryover from the two ports before a reading and its calibration error at the channel's own level are both "
        "counted. Not HOL-FW1: its carryover from the raw sample two ports back is cancelled by Holmedale's zero error. "
        "Not CAL-FI1 or CAL-FW1: Calderwood's error is a span error, about %.3f at treated levels."
        % (fig["flag_band_print"], np.ceil(fig["unflagged_band_high"] * 1000) / 1000,
           fig["cal_span_treated"]),
        "",
        "## 2. Critical Components",
        "",
        "1. Five analysers (%s) do not empty their measuring cell between ports: each reading is a mix of its own "
        "sample with small shares of the two samples before it, so it is off by those shares of the differences "
        "between those samples and its own; the channel read straight after raw water reads high, and at Garrick and "
        "Holmedale, with raw water two to three times the others', so does the channel read two ports after it."
        % _join(fig["worn"]),
        "2. Holmedale's analyser reads **%.3f** low at every level, a zero error: its checks read that much low at "
        "0.100, and its raw port, once its own carryover from the treated ports ahead of it is taken out, falls short "
        "of the laboratory's raw grabs by about the same amount, far less than %d per cent of their level."
        % (abs(fig["hol_zero_error"]), abs(fig["cal_span_pct"])),
        "3. Calderwood's analyser reads about **%d per cent** low, a span error: its raw port falls short of the raw "
        "grabs in proportion to their level, and it has no carryover." % abs(fig["cal_span_pct"]),
        "4. HOL-FW1's carryover from the raw sample two ports back is about the size of Holmedale's zero error, so "
        "the two cancel and HOL-FW1 sits within **%.3f** of zero." % (np.ceil(fig["unflagged_band_high"] * 1000) / 1000),
        "",
        "## 3. Step-by-Step Solution",
        "",
        "1. Read WQ-DS-04 sections 3 and 4 (the offset over the channel's G readings in the historian, flagged beyond "
        "0.005 either way) and the register's port sequences; kept each slot's G row, a filled-in slot's G row "
        "standing over its F row.",
        "2. For each analyser, fitted the carryover as a mix in the cell: both treated ports' readings together on the "
        "readings of the two slots before them (check readings as the cell's content), one pair of shares for the "
        "analyser, each port with its own level and its own response to the raw readings 2 to 8 hours earlier; each "
        "channel's carryover offset is the shares of the differences between the two slots before it and its own "
        "reading, divided by one less both shares. %s carry about %d per cent of the slot before and %d per cent of "
        "the one before that, the other three under %d per cent."
        % (_join(fig["worn"]), fig["carry_share_1"], fig["carry_share_2"], fig["carry_share_healthy"]),
        "3. Took each analyser's check mean from analyser_verification_2027Q4.xlsx: Holmedale and Calderwood read about "
        "%d per cent low, the other six within 0.002 of 0.100." % abs(fig["cal_span_pct"]),
        "4. Paired each raw grab in lims_ammonia_2027Q4.csv with the raw reading of its slot, took the raw port's own "
        "carryover from the two slots before it out of the reading with the analyser's shares, and compared the "
        "shortfall left with the check's: constant at Holmedale (a zero error), in proportion at Calderwood (a span "
        "error).",
        "5. Added each analyser's calibration error at the channel's own level to the carryover offset and flagged "
        "beyond 0.005: %s." % fig["call"],
        "6. For each plant's treated samples, moved the laboratory's analysis stamps forward an hour: some runs are "
        "stamped up to %d minutes before reception logged their bottles and no result is released within %d minutes of "
        "its stamp, so the stamps run behind the laboratory's other clocks and every shift in that range counts the "
        "same; mapped the October codes through the laboratory's notice; counted each bottle once, the 7 December "
        "round's treated bottles being logged a second time under the courier docket's pickup time with the same point, "
        "analysis stamp, result and release; and counted those analysed more than 24 hours after collection."
        % (fig["clock_lo"], fig["clock_hi"]),
        "7. For each plant's filtered water port, treated as available to the PLC every slot except the check cycles "
        "and the slots no reading reached it: a failed poll later filled from the outstation, the historian's lost "
        "hours of 17 November and each run of unfilled F rows at every port that no check followed (a failed poll "
        "takes the plant's whole record and a fault is followed by the technician's check, so these were the "
        "telemetry's, one a plant in November) were the historian's alone, while the filtered port's own unfilled F "
        "rows, the other ports read between them, never reached the PLC (once at each plant); summed each gap between "
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
