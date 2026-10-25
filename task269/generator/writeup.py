"""submission.md, drafted from generator/figures.json so every figure it states is one the generator computed.

    python3 task269/generator/writeup.py"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    c, ev, dp, A = f["call"], f["evidence"], f["default_path"], f["ask_a"]
    out = ["## Tags", "",
           "**Domain:** General Statistics & Data Science (missing data, censoring and measurement error).",
           "**Analytical objective:** Descriptive & Distribution Analysis.", "",
           "## 1. Final Recommendation", "",
           "**Accept the appraisal vendor's offer of the county-wide single-family reappraisal: the certified 2026 "
           "single-family "
           "roll fails the State Tax Commission's Rule 18-7 on both tests, a median assessment ratio of %.2f, below "
           "the rule's level band, and a coefficient of dispersion of %d, above its uniformity limit.**"
           % (c["level"], c["cod"]),
           "Not the 2025 arm's-length sales against their 2026 values as they stand (%.2f and %.1f, inside the rule): "
           "the parcels sold in 2025 rose a median %.1f per cent from the 2025 roll against %.1f per cent for the "
           "rest, so those sales measure the parcels revalued after their sale, not the roll."
           % (dp["level"], dp["cod"], ev["sold_change_pct"], ev["unsold_change_pct"]),
           "",
           "## 2. Critical Components", "",
           "1. Single-family parcels with a 2025 arm's-length sale rose a median **%.1f%%** from the 2025 roll to the "
           "2026 roll; the other single-family parcels on both rolls a median **%.1f%%**, most of them by their "
           "neighbourhood's common factor." % (ev["sold_change_pct"], ev["unsold_change_pct"]),
           "2. Those **%s** sold parcels are **%.1f%%** of the **%s** single-family parcels on the 2026 roll."
           % (format(ev["reviewed_parcels"], ","), ev["reviewed_share_pct"], format(ev["single_family_parcels"], ",")),
           "3. The study rests on **%s** sales once the **%d** whose permit work was finaled after the deed are set "
           "aside." % (format(ev["study_sales"], ","), ev["set_aside_sales"]),
           "",
           "## 3. Step-by-Step Solution", "",
           "1. Read str_rule_18-7_residential_ratio_studies.pdf: the level and the coefficient of dispersion are "
           "taken over every parcel of the class on the certified roll; market value comes from the 2025 Q deeds, "
           "each price times the index for January 2026 over the index for the deed's month "
           "(residential_price_index_tillford.csv); a sale is set aside where improvements or boundaries changed "
           "after the deed.",
           "2. Took the Q deeds in recorder_deeds_2025.csv whose parcel number, without its dashes and with a 0 "
           "added, is an R1 parcel in assessor_roll_2026_certified.csv, and set aside the %d whose work in "
           "building_permits_2025.csv was finaled after the deed: %s sales, whose 2026 values over their indexed "
           "prices give %.2f and %.1f." % (ev["set_aside_sales"], format(ev["study_sales"], ","), dp["level"],
                                          dp["cod"]),
           "3. Joined assessor_roll_2025_certified.xlsx to the 2026 roll on the same parcel numbers: the %s "
           "parcels with a 2025 Q deed rose a median %.1f%%, the parcels without one %.1f%%, most of them by "
           "their neighbourhood's (nbhd_code) common change." % (format(ev["reviewed_parcels"], ","),
                                                                ev["sold_change_pct"], ev["unsold_change_pct"]),
           "4. For each study sale took its 2025 value times its neighbourhood's median change among parcels without "
           "a 2025 Q deed, to the nearest %d, over its indexed price, standing for the %.1f%% of the class that did not "
           "sell; its 2026 value over its indexed price stands for the %.1f%% that did."
           % (f["rounding"]["value"], ev["unsold_share_pct"], ev["reviewed_share_pct"]),
           "5. Weighted the two sets of %s ratios by those shares (%s of %s parcels sold): the median is %.2f and "
           "the average absolute difference from it %d per cent, so the class fails both tests."
           % (format(ev["study_sales"], ","), format(ev["reviewed_parcels"], ","),
              format(ev["single_family_parcels"], ","), c["level"], c["cod"]),
           "6. Condominium class: the Q deeds of R2 parcels, a Wexley Commons deed signed (or permit issued) before "
           "its parcel_change_log_2025.csv entry took effect read at the new parcel identifier, a sale set aside where "
           "its unit was combined (COMBINE) or its permit work in building_permits_2025.csv finaled after the deed: "
           "%d sales, a median of %.2f, an aggregate ratio of %.3f, a COD of %.1f and a price-related differential of "
           "%.3f." % (A["sales"], A["level"], A["agg"], A["cod"], A["prd"]),
           "7. Board of Review: from board_of_review_hearings_2025.csv the hearings from %s on whose value_before "
           "equals the parcel's certified 2025 value (the earlier hearings are appeals of the 2024 roll), each parcel "
           "at its last hearing in its case (a case may list several parcels), REDUCED parcels summed by market area "
           "through the 2025 roll's neighbourhood and neighborhood_crosswalk.csv." % f["cert_2025"],
           "8. Recommended accepting the vendor's offer of the single-family reappraisal.",
           "",
           "## 4. Deliverable Answers", "",
           "### reappraisal_recommendation.docx", "",
           "1. Accept the vendor's offer of the county-wide single-family reappraisal: the roll fails Rule 18-7.",
           "2. Median assessment ratio of the 2026 single-family roll: %.2f" % c["level"],
           "3. Coefficient of dispersion of the 2026 single-family roll: %d" % c["cod"],
           "",
           "### ratio_study_2026_roll.xlsx", "",
           "1. Condominium class:",
           "   - Sales the study rests on: %d" % A["sales"],
           "   - Median assessment ratio: %.2f" % A["level"],
           "   - Aggregate assessment ratio: %.3f" % A["agg"],
           "   - Coefficient of dispersion: %.1f" % A["cod"],
           "   - Price-related differential: %.3f" % A["prd"],
           "2. Board of Review reductions of the 2025 roll, single-family and condominium parcels, by market area:"]
    for a in sorted(f["ask_b"], key=int):
        b = f["ask_b"][a]
        out.append("   - Market area %s (%s): %d parcels reduced, %s dollars taken off" %
                   (a, b["name"], b["parcels"], format(b["value_off"], ",")))
    out.append("")
    with open(os.path.join(TASK, "submission.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(out))


if __name__ == "__main__":
    main()
