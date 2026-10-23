"""submission.md, drafted from generator/figures.json so every figure it states is one the generator computed.

    python3 task274/generator/writeup.py"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
ORDER = ["Wexmoor", "Corvale", "Lassiter", "Ulverne", "Vellance", "Quennel", "Yarrowmere", "Inskeep"]


def n(x):
    return format(int(x), ",")


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    C, a = f["counties"], f["asks"]
    opens = f["call"]["counties"]
    rest = [c for c in ORDER if c not in opens]
    out = ["## Tags", "",
           "**Domain:** Survey Research & Official Statistics (nonresponse, calibration and measurement-error adjustment).",
           "**Analytical objective:** Descriptive & Distribution Analysis.", "",
           "## 1. Final Recommendation", "",
           "**Open the 2027 vitamin D programme first in %s, %s, %s and %s: in each, more than 30 per cent of adults had "
           "serum 25(OH)D below 20 ng/mL on the reference measurement procedure's scale in the 2025 wave.**"
           % tuple(opens),
           "Each 2025 result is put on the reference scale through the calibration it was measured under: the October "
           "accuracy check fixes the bias of IA1's calibration of %s, and the December bridging run carries it to every "
           "calibration of both analyzers." % f["check"]["calibration_start"][:10],
           "",
           "## 2. Critical Components", "",
           "1. Accuracy-based check, event 2025-B (IA1, reagent lot 43012, 15 October 2025): mean difference **%+.1f per "
           "cent** from the reference values, under the IA1 calibration of %s." % (f["check"]["mean_difference_pct"],
                                                                                  f["check"]["calibration_start"]),
           "2. Bridging run: **%s** stored duplicates paired with the same adults' primary results; the run reads "
           "about **%d per cent** above the reference scale." % (n(f["bridging"]["pairs"]), f["bridging"]["bias_whole"]),
           "3. The %s final primary results were measured under **%d** calibrations (%d on IA1, %d on IA2), each "
           "with its own shift against the bridging run." % (n(f["results"]), f["calibrations_used"]["total"],
                                                            f["calibrations_used"]["IA1"], f["calibrations_used"]["IA2"]),
           "4. Share of adults below 20 ng/mL on the reference scale, to the nearest whole per cent: " +
           ", ".join("%s %d" % (c, C[c]["share_whole"]) for c in ORDER) + ".",
           "5. Every county stands at least **%.1f points** from 30 per cent." % f["family_margin_points"],
           "",
           "## 3. Step-by-Step Solution", "",
           "1. Kept the final results (RESULT_STATUS F) in lis_vitd_results_2025.csv and joined each to its adult through "
           "the tracking export's labels (hyphen removed) and to county and WTMEC2025 through the examined persons file.",
           "2. Placed each result under the calibration accepted on its analyzer most recently before it was run "
           "(analyzer_event_log_2025.csv in UTC, converted to Mountain time; LIS codes to serial numbers through the "
           "instrument register).",
           "3. Paired each bridging result with the same adult's primary result and took, for each calibration, the "
           "mean of the log of the primary result over the bridging result.",
           "4. Took the check's mean difference as the bias of the IA1 calibration in force on 15 October, so the "
           "bridging run's bias is that bias less the calibration's mean log ratio.",
           "5. Divided each result by the bridging run's bias times its own calibration's ratio, weighted with "
           "WTMEC2025 and read each county's share below 20 ng/mL against 30 per cent.",
           "6. Ask A: per adult, summed each product's vitamin D per unit (label amount in IU, mcg times 40, divided by "
           "the serving size; GENERIC lines as typed) times units a day times days taken, over 30; a GENERIC line that "
           "repeats one of the adult's labelled lines in strength per unit, days and units a day is that bottle's line "
           "appended by product matching and counts once; weighted with WTINT2025 over interviewed adults.",
           "7. Ask B: where a dwelling was screened twice, kept the sample persons of its later screening only (the "
           "earlier screening's people were selected again); left out persons found ineligible; counted complete, "
           "partial and proxy interviews and persons examined at the MEC.",
           "",
           "## 4. Deliverable Answers", "",
           "### %s" % "vitamin_d_status_2025.xlsx", "",
           "1. Counties where the programme opens first: %s; not %s." % (", ".join(opens), ", ".join(rest)),
           "2. Interviewed adults whose supplements averaged at least 1,000 IU of vitamin D a day (per cent):"]
    for c in ORDER:
        out.append("   - %s: %.1f" % (c, a["supplements_1000"][c]))
    out.append("3. At least 2,000 IU a day (per cent):")
    for c in ORDER:
        out.append("   - %s: %.1f" % (c, a["supplements_2000"][c]))
    out.append("4. Interview response rate (per cent):")
    for c in ORDER:
        out.append("   - %s: %.1f" % (c, a["interview_rr"][c]))
    out.append("5. Examination response rate (per cent):")
    for c in ORDER:
        out.append("   - %s: %.1f" % (c, a["exam_rr"][c]))
    txt = "\n".join(out) + "\n"
    assert "—" not in txt
    with open(os.path.join(TASK, "submission.md"), "w", encoding="utf-8") as fh:
        fh.write(txt)
    return txt


if __name__ == "__main__":
    print(main())
