"""submission.md, drafted from generator/figures.json so every figure it states is one the generator computed."""
import json

import pack as P

F = P.FILES
WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten",
         11: "eleven", 12: "twelve"}


def _list(names):
    return ", ".join(names[:-1]) + " and " + names[-1] if len(names) > 1 else names[0]


def _n(v):
    return "{:,}".format(int(v))


def write(fig_path, out_path):
    fig = json.load(open(fig_path, encoding="utf-8"))
    rows = fig["counties"]
    q = sorted(fig["call"])
    rungs = fig["rungs"]
    pooled = sorted(rungs["pooled"])
    drawn = sorted(rungs["drawn list"])
    dropped = sorted(set(q) - set(pooled))
    added = sorted(set(drawn) - set(q))
    lines = []
    lines.append("## Tags\n")
    lines.append("**Domain:** General Statistics & Data Science (data integration and record linkage: a health "
                 "department links two overlapping lists of private wells, conforms three laboratories' results and "
                 "estimates each county's wells above the nitrate standard from a survey sampled from both lists).  ")
    lines.append("**Analytical objective:** Data Extraction & Conformation (ETL).\n")
    lines.append("## 1. Final Recommendation\n")
    lines.append("**%s of the sixteen counties qualify for the 2027 Well Water Assistance allocation: %s.**  " % (
        WORDS[len(q)].capitalize(), _list(q)))
    lines.append("Each has an estimated 250 or more wells in its survey population above 10 mg/L nitrate as nitrogen "
                 "once every tested well counts for the wells it stands for, one over its chance of selection from "
                 "either list. Not the %s that scaling each county's share of tested wells above the standard to its "
                 "wells gives (%s): the parcel list was sampled at %.1f per cent against the permit list's %.1f, and "
                 "its parcel-only wells run higher in nitrate (%.1f per cent of the tested ones above the standard "
                 "against %.1f per cent of the tested wells on the permit list), so the pooled share leaves out %s. "
                 "Nor the "
                 "%s that "
                 "weighting each tested well by the sampling rate of the list it was drawn from (that list's target "
                 "over its wells in Table 2) gives: a well on both "
                 "lists had two chances of selection, and counting it at one list's rate counts it about twice, "
                 "which puts %s over the line.\n" % (
                     WORDS[len(pooled)], _list(pooled), fig["parcel_rate"], fig["permit_rate"],
                     fig["parcel_only_share"], fig["others_share"], _list(dropped), WORDS[len(drawn)], _list(added)))
    lines.append("## 2. Critical Components\n")
    lines.append("1. Counties at or above 250: **%d** of 16." % fig["qualifying_count"])
    lines.append("2. Sampling rates across the sixteen counties: permit list **%.1f%%** (%s of %s wells), parcel list "
                 "**%.1f%%** (%s of %s)." % (fig["permit_rate"], _n(fig["nP_total"]), _n(fig["NP_total"]),
                                             fig["parcel_rate"], _n(fig["nQ_total"]), _n(fig["NQ_total"])))
    lines.append("3. Tested wells on both lists: **%s** of the **%s** tested; wells on the survey's lists: **%s**.\n" % (
        _n(fig["tested_both_total"]), _n(fig["tested_total"]), _n(fig["union_total"])))
    lines.append("## 3. Step-by-Step Solution\n")
    steps = [
        "Built the permit list from %s (WELL_USE DOMESTIC, WELL_STATUS ACTIVE, DATE_DRILLED from 1986-01-01 to "
        "2025-08-31) and the parcel list from %s (the water code each layout gives for a private well, Codes sheet); "
        "both match Table 2 of %s, %s and %s wells." % (F["permits"], F["parcels"], F["design"], _n(fig["NP_total"]),
                                                      _n(fig["NQ_total"])),
        "Linked each permit to its parcel by parcel number (digits only) or, on a permit with none, by house number "
        "and street name (directions, suffixes and punctuation set aside): a well is on both lists when its permit's "
        "parcel carries the private-well code, %s wells in the survey population." % _n(fig["union_total"]),
        "Read %s: TESTED and TESTED_EARLIER rows count toward each list's target, so the permit list is sampled at "
        "f = target over its wells and the parcel list likewise; each tested well's place on the other list comes "
        "from the linkage (%s of %s tested wells are on both)." % (F["manifest"], _n(fig["tested_both_total"]),
                                                                    _n(fig["tested_total"])),
        "Took each first-test kit's final nitrate as nitrogen from %s (RESULT_STATUS FINAL), %s (latest Report "
        "Date) and %s (highest VERSION, NO3 divided by 4.427): %s tested wells above 10 mg/L." % (
            F["hal"], F["ced"], F["kin"], _n(fig["tested_above_total"])),
        "Summed, over each county's tested wells above the standard, one over the well's chance of selection: f "
        "permit, f parcel, or 1 - (1 - f permit)(1 - f parcel) for a well on both lists; %s counties at or above 250 "
        "(%s lowest at %d, %s highest below at %d), and Hartley's estimator at every split of the wells on both "
        "lists and the estimate post-stratified by list membership give the same %s." % (
            WORDS[fig["qualifying_count"]], fig["lowest_qualifier"]["name"], fig["lowest_qualifier"]["estimate"],
            fig["highest_short"]["name"], fig["highest_short"]["estimate"], WORDS[fig["qualifying_count"]]),
        "Matched each request in %s to its well by ORIGINAL_KIT (portal) or by ship-to house number and street in the "
        "request's county (phone), and counted each well in the county the survey tested it in, not the county a "
        "border ZIP code routed the request to." % F["retests"],
        "Kept retests of wells first tested above 10 mg/L whose retest sample (the laboratories' collection date) "
        "was collected on or before June 30, 2026 (WWA-2027-01 4.2); households outside the survey and later retests "
        "left out; still above when the retest is above 10 mg/L: %d retested, %d still above." % (
            fig["retested_total"], fig["still_above_total"]),
        "Charted the sixteen estimates against the 250-well line, the qualifying counties highlighted.",
    ]
    for i, s in enumerate(steps, 1):
        lines.append("%d. %s" % (i, s))
    lines.append("\n## 4. Deliverable Answers\n")
    lines.append("### nitrate_assistance_counties_2027.xlsx\n")
    lines.append("1. Counties that qualify: **%d**: %s." % (len(q), _list(q)))
    lines.append("2. Each county: private domestic wells on the survey's lists; qualifies; wells first tested above "
                 "the standard and retested by June 30, 2026; of those, still above:")
    for r in sorted(rows, key=lambda r: r["name"]):
        lines.append("   - %s: %s; %s; %d; %d" % (r["name"], _n(r["union"]), "yes" if r["qualifies"] else "no",
                                                 r["retested"], r["still_above"]))
    lines.append("\n### nitrate_assistance_counties_2027.png\n")
    lines.append("3. Bar chart of the sixteen counties' estimated wells above the standard against the 250-well line, "
                 "the %s qualifying counties highlighted." % WORDS[len(q)])
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
