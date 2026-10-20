"""submission.md from generator/figures.json: tags, the final recommendation, the critical components, the steps and the
deliverable answers. Every number written comes from figures.json."""
import json

import pack as P


def _n(v):
    return "{:,}".format(int(v))


def _p(v):
    return "%.1f" % abs(v)


def write(fig_path, out_path):
    fig = json.load(open(fig_path, encoding="utf-8"))
    ch = fig["call"]["change_pct"]
    br = fig["bridge"]
    du = fig["dual"]
    ro = fig["routes"]
    sh = fig["shootings"]
    out = []
    out.append("## Tags\n")
    out.append("**Domain:** Survey Research & Official Statistics (official time-series production: a city's "
               "police-recorded aggravated assault series restated across the department's move from summary "
               "(Return A) to incident-based (NIBRS) reporting, from the three months in which every victim carries "
               "both classifications, and conformed with the NIBRS extract, the Domestic Violence Unit's case log, "
               "the shooting log and the Medical Examiner's list into the scorecard's crime chapter).  ")
    out.append("**Analytical objective:** Data Extraction & Conformation (ETL).\n")
    out.append("## 1. Final Recommendation\n")
    out.append("**On the NIBRS basis Ellsmere's aggravated assaults %s %d per cent from 2024 to 2025: %s victims in "
               "2025 against about %s in 2024 restated.**" % ("rose" if ch > 0 else "fell", abs(ch),
                                                             _n(fig["nibrs_2025"]), _n(fig["restated_2024"])))
    out.append("The rise in the published figures is mostly the change in counting: 2024 as NIBRS would have counted it "
               "is about %s, well above the total Return A published, because NIBRS counts the assault victims the "
               "hierarchy rule hid, counts as aggravated the simple assaults with a weapon or force or serious "
               "injury, most of them domestic, and counts as simple the hands-and-feet assaults Return A scored "
               "aggravated for minor injuries. Restated at the October to December 2024 rate for each Return A line, "
               "2024 would be about %s and 2025 a fall of %d per cent from it, because that rate carries October to "
               "December's share of domestic victims among other assaults (%s per cent, against %s per cent in "
               "January to September) into the rest of the year.\n" % (
                   _n(fig["restated_2024"]), _n(ro["per_line_2024_hundred"]), ro["per_line_fall_pct"],
                   _p(fig["printed"]["dv_share_q4_pct"]), _p(fig["printed"]["dv_share_jan_sep_pct"])))
    out.append("## 2. Critical Components\n")
    out.append("1. 2024 as published from Return A (lines 4a to 4d, actual offenses): **%s**; 2025 counted from the "
               "department's extract: **%s**." % (_n(fig["published_2024"]), _n(fig["nibrs_2025"])))
    out.append("2. October to December 2024, the share of each Return A line's victims NIBRS counted aggravated: "
               "other assaults (4e) **%s per cent** for domestic victims and **%s per cent** for the rest; hands and "
               "feet (4d) **%s per cent**; firearm, knife and other weapon (4a to 4c) **%s per cent**." % (
                   _p(fig["printed"]["rate_4E_dv_pct"]), "%.2f" % fig["printed"]["rate_4E_non_pct"],
                   _p(fig["printed"]["rate_4D_pct"]), _p(fig["printed"]["rate_4A_pct"])))
    out.append("3. Domestic victims' share of other assaults (4e): **%s per cent** in October to December 2024, "
               "**%s per cent** in January to September (%s of %s)." % (
                   _p(fig["printed"]["dv_share_q4_pct"]), _p(fig["printed"]["dv_share_jan_sep_pct"]),
                   _n(du["dv_4e_jan_sep"]),
                   _n(du["e4_jan_sep"])))
    out.append("4. From the published 2024 total to the restated one, to the unit: %s, plus **%s** victims the "
               "hierarchy rule left unscored, plus **%s** victims of other assaults NIBRS counts aggravated, less "
               "**%s** victims of aggravated assault NIBRS counts simple: **%s**, about **%s** to the nearest "
               "hundred.\n" % (_n(fig["published_2024"]), _n(br["hidden"]), _n(br["gained"]), _n(br["lost"]),
                               _n(fig["restated_2024_units"]), _n(fig["restated_2024"])))
    out.append("## 3. Step-by-Step Solution\n")
    out.append("1. Counted the 13A rows of %s by the month reported in Ellsmere local time (report_datetime_utc "
               "is UTC): %s in 2025, and October to December 2024 the same way." % (
                   P.FILES["extract"], _n(fig["nibrs_2025"])))
    out.append("2. Took each month's actual offenses (column 4) from return_a_2024.xlsx; lines 4a to 4d sum to %s "
               "for 2024." % _n(fig["published_2024"]))
    out.append("3. In October to December 2024 (ucr_summary_class filled) took for lines 4a to 4d the share of each "
               "line's victims coded 13A, for robbery and homicide the 13A victims marked NS per Return A robbery "
               "incident and per homicide victim, and for line 4e the share coded 13A separately for victims whose "
               "relationship_1 is a family or intimate partner code and for the rest.")
    out.append("4. For each month of January to September 2024 counted the domestic victims of line 4e from %s "
               "(ucr_line 4E, report_date in the month, case_status not UNFOUNDED) and took the rest of line 4e as the "
               "month's other victims." % P.FILES["dvu"])
    out.append("5. Restated January to September at those rates, line by line and month by month, and added October to "
               "December as counted: %s, about %s to the nearest hundred; to 2025, %s%d per cent." % (
                   _n(fig["restated_2024_units"]), _n(fig["restated_2024"]), "+" if ch > 0 else "-", abs(ch)))
    out.append("6. Shootings: kept the rows of %s struck in an ASSAULT with outcome WOUNDED; left out every block the "
               "log marks N in any row (the North Ellsmere Township blocks, which it marks Y before October 2024), and "
               "dropped the people the Medical Examiner's list shows died of the wound (same date of injury, block, "
               "age and sex, place in Ellsmere); counted each person once (report number, time, age and sex) by the "
               "quarter shot, and a shooting as the people struck at one block and minute." % P.FILES["gvr"])
    out.append("7. Wrote ellsmere_aggravated_assault.xlsx.\n")
    out.append("## 4. Deliverable Answers\n")
    out.append("### ellsmere_aggravated_assault.xlsx\n")
    out.append("1. 2024 restated on the NIBRS basis, to the nearest hundred: %s; 2025: %s; change: %s%d per cent." % (
        _n(fig["restated_2024"]), _n(fig["nibrs_2025"]), "+" if ch > 0 else "-", abs(ch)))
    q = sh["victims"]
    s = sh["shootings"]
    out.append("2. Non-fatal shooting victims and the shootings they were hurt in, by quarter: " + "; ".join(
        "%s %s victims in %s shootings" % (k.replace("Q", " Q"), _n(q[k]), _n(s[k])) for k in sorted(q)) + ".")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
