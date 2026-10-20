"""submission.md from generator/figures.json: tags, the final recommendation, the critical components, the steps and the
deliverable answers. Every number written comes from figures.json."""
import json

import world as W

NUM = {6: "Six", 7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten"}


def _n(v):
    return "{:,}".format(int(v))


def _names(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def write(fig_path, out_path):
    fig = json.load(open(fig_path, encoding="utf-8"))
    by = {x["name"]: x for x in fig["municipalities"]}
    call = fig["call"]["names"]
    default = fig["rungs"]["R2b born abroad x years at the address"]["names"]
    added = [n for n in default if n not in call]
    dropped = [n for n in call if n not in default]
    stay = fig["rungs"]["R2c current stay"]["names"]
    a = fig["audit"]
    b = a["by_career"]
    towns = fig["career_towns"]
    seasonal = [t for t in towns if t["type"] == "G"]
    older = [t for t in towns if t["type"] == "O"]
    uni = [t for t in towns if t["type"] == "U"][0]
    out = []
    out.append("## Tags\n")
    out.append("**Domain:** Survey Research & Official Statistics (census, register and administrative data quality: "
               "the population register's over-count of residents who left the country unreported, measured by the "
               "Register Coverage Audit 2026 and applied to each municipality's register count within the "
               "characteristics that carry it, the length of the current stay since the latest settlement from abroad "
               "and an earlier departure, both rebuilt from the register's event history).  ")
    out.append("**Analytical objective:** Data Extraction & Conformation (ETL).\n")
    out.append("## 1. Final Recommendation\n")
    out.append("**%s of the 24 municipalities in play qualify for the 2027 small-municipality supplement: %s.**" % (
        NUM[fig["call"]["count"]], _names(call)))
    out.append("Each has an adjusted resident population on 1 January 2026 below 5,000: its register count less the "
               "registered persons the audit estimates were not living there, taken within the length of each "
               "person's current stay since the latest settlement from abroad and whether the person had left the "
               "country before it. %s is the qualifying municipality nearest the line and %s the nearest left out. "
               "Not the %s municipalities the register's own fields give (country of birth by years at the current "
               "address), which add %s and drop %s, because a move within the country resets the address date while "
               "only the event history shows who has come and gone before; not the %s the current stay alone gives, "
               "which drops %s.\n" % (
                   fig["nearest"]["below"], fig["nearest"]["above"], NUM[len(default)].lower(), _names(added),
                   _names(dropped), NUM[len(stay)].lower(), _names([n for n in call if n not in stay])))
    out.append("## 2. Critical Components\n")
    rc, bp = a["result_codes"], a["by_career_pct"]
    out.append("1. Sampled persons the audit found not living in their registered municipality on 1 January 2026 "
               "(final results %s): **%s of %s** (%s per cent)." % (
                   _names([str(c) for c in rc["absent"]]), _n(a["absent"]), _n(a["sampled"]), "%.2f" % a["share_pct"]))
    out.append("2. Not living there, by migration career: never settled from abroad **%s of %s** (%.2f per cent); "
               "settled from abroad with no earlier departure **%s of %s** (%.1f per cent); settled from abroad after an "
               "earlier departure **%s of %s** (%.1f per cent)." % (
                   _n(b["never"][1]), _n(b["never"][0]), bp["never"], _n(b["stayed"][1]), _n(b["stayed"][0]),
                   bp["stayed"], _n(b["returned"][1]), _n(b["returned"][0]), bp["returned"]))
    out.append("3. Registered persons settled from abroad who had left the country before: %s; against %s." % (
        "; ".join("%s **%s of %s**" % (t["name"], _n(t["left"]), _n(t["settled"])) for t in seasonal),
        "; ".join("%s **%s of %s**" % (t["name"], _n(t["left"]), _n(t["settled"])) for t in older + [uni])))
    out.append("4. Registered persons in the first to fourth year of their current stay: %s **%s**, against %s.\n" % (
        uni["name"], _n(uni["stay_1_4"]), _names(["%s **%s**" % (t["name"], _n(t["stay_1_4"])) for t in older])))
    out.append("## 3. Step-by-Step Solution\n")
    steps = [
        "Read population_register_extract_20260101.txt (its trailer's %s persons in the 24 municipalities in play, "
        "Ravenmeer one municipality under Article 14(4)) and population_register_events_extract.csv, dropped each "
        "annulled event with its ANN, and gave each person the completed years from the latest IMM to 1 January 2026 "
        "and whether an EMI came before that IMM." % _n(fig["totals"]["registered"]),
        "Took each audited person's last record in register_coverage_audit_2026_visits.csv as the final result (%d is "
        "no contact; %d counts as living there) and built the same two features from "
        "register_coverage_audit_2026_histories.csv: %s of %s not living there." % (
            a["result_codes"]["no_contact"], a["result_codes"]["present_left"], _n(a["absent"]), _n(a["sampled"])),
        "Measured the audit's share not living there within cells of the current stay (never settled from abroad, "
        "under 1, 1 to 4, 5 to 9, 10 or more years) by whether the person had left the country before; within those "
        "cells country of birth, nationality, years at the address, age and sex add nothing.",
        "Gave each registered person the share of their cell, summed by municipality, took the sum from the register "
        "count, rounded to the whole person and compared with 5,000 (Article 14(1) to (3)): %s qualify." % (
            NUM[fig["call"]["count"]].lower()),
        "Departures abroad: deregistration_messages_2025.csv's EMI messages the hub accepted "
        "(hub_acknowledgements_2025.csv), with a 2025 departure date and sent in 2025 in the country's time (the "
        "night batch logged at 23:00 UTC or later on 31 December left on 1 January 2026), each person who left twice "
        "counted twice, less the departures the register annulled as entered in error (an EMI with an ANN in the "
        "person's history).",
        "Deaths: the OVL messages the hub accepted with a 2025 date of death and sent in 2025 in the country's time, "
        "less the deaths the register annulled and the former residents whose registration had ended before they died "
        "(non_resident_records_extract.csv, DEPARTURE_DATE before the date of death).",
        "Wrote adjusted_population_supplement_2027.csv in the layout of the ministry's delivery specification and the "
        "chart of the adjusted resident populations against the 5,000 line.",
    ]
    for i, s in enumerate(steps, 1):
        out.append("%d. %s" % (i, s))
    out.append("")
    out.append("## 4. Deliverable Answers\n")
    out.append("### adjusted_population_supplement_2027.csv\n")
    out.append("1. Whether each municipality qualifies, its departures abroad in 2025 and its deaths in 2025:")
    for x in fig["municipalities"]:
        out.append("   - %s (%s): %s, %s departures abroad, %s deaths" % (
            x["name"], x["gm"], "qualifies" if x["qualifies"] else "does not qualify", _n(x["departures"]),
            _n(x["deaths"])))
    out.append("")
    out.append("### adjusted_population_supplement_2027.png\n")
    out.append("1. Bar chart of the 24 municipalities' adjusted resident populations against the 5,000 line, the %s "
               "under it highlighted: %s." % (NUM[fig["call"]["count"]].lower(), _names(call)))
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out).rstrip() + "\n")


if __name__ == "__main__":
    import os
    import sys
    here = os.path.dirname(os.path.abspath(__file__))
    write(os.path.join(here, "figures.json"), os.path.join(os.path.dirname(here), "submission.md"))
    sys.exit(0)
