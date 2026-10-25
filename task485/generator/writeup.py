"""submission.md from generator/figures.json: the five blocks, every figure taken from the generator's own output."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven"}


def joined(xs):
    xs = list(xs)
    return ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else xs[0]


def sv(x):
    return "%+.1f" % x


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    fail, meet = f["call"]["fail"], f["call"]["meet"]
    order = f["constants"]["order"]
    fail = [w for w in order if w in fail]
    v, dv = f["forecast"]["variance"], f["default"]["variance"]
    dfail = f["default"]["fail"]
    late = [w for w in dfail if w not in fail]
    young = [w for w in fail if w not in dfail]
    b = f["buildup"]
    shares = ", ".join("%.2f" % b[str(k)] for k in range(1, 7))
    out = ["## Tags", "",
           "**Domain:** Survey Research & Official Statistics, census, register and administrative data quality (a boundary "
           "commission's 2032 electorate forecast for a district's 23 wards, conformed from six electoral registers in two "
           "election management system layouts, the old system's notices of alteration, the address gazetteer, the "
           "council's completions monitoring and housing trajectory, and its polling district and ward schedules).",
           "**Analytical objective:** Data Extraction & Conformation (ETL).", "",
           "## 1. Final Recommendation", "",
           "**The draft recommendations should address %s: on the forecast for the register to be published on 1 December "
           "2032 these %s wards lie more than 10 per cent from the district's average of %s electors per councillor, and "
           "the other %d are within it.**" % (joined(fail), WORDS[len(fail)], f["forecast"]["average_whole"], len(meet)),
           "%s sit at %s per cent and %s at %s. Not %s, which the 2025 register plus the dwellings to come at the settled "
           "stock's electors per dwelling puts at %s: their sites complete from 2030, and a dwelling's electors join the "
           "register over the canvasses after it comes into use, so in 2032 they hold well under the settled level (%s). "
           "Not with %s within, at %s on that route: their estates completed from 2024 are still joining the register." % (
               joined(young + [w for w in fail if w not in young and v[w] > 0]),
               joined(sv(v[w]) for w in young + [w for w in fail if w not in young and v[w] > 0]),
               joined(w for w in fail if v[w] < 0), joined(sv(v[w]) for w in fail if v[w] < 0),
               joined(late), joined(sv(dv[w]) for w in late), joined(sv(v[w]) for w in late),
               joined(young), joined(sv(dv[w]) for w in young)), "",
           "## 2. Critical Components", "",
           "1. Local government electors on the register published 1 December 2025: **%s**." % f["components"]["electors_2025"],
           "2. Dwellings the housing trajectory expects from 1 October 2026 to 31 March 2032: **%s**." %
           f["components"]["trajectory_dwellings"], "",
           "## 3. Step-by-Step Solution", "",
           "1. Conformed the registers of 1 December 2022 to 2025 in ems_property_electorate_2022-2025.csv to "
           "llpg_extract_2026-10-12.csv through each property's UPRN (approved records in use, RD02 to RD04 houses, RD06 "
           "flats, the gazetteer's ward): %s local government electors on the 2025 register." % f["components"]["electors_2025"],
           "2. Counted each dwelling's canvasses by each register from its gazetteer in-use date, a property being first "
           "canvassed in the year it is in use on 31 August and applications determined by 31 October reaching the 1 "
           "December register (lorrimere_annual_canvass_report_2025.pdf).",
           "3. Took the settled level from the 2025 register at the dwellings at their seventh canvass or later (houses %.2f, "
           "flats %.2f electors per dwelling) and, from the 2022 to 2025 registers at the dwellings in "
           "housing_completions_monitoring_2014-2026.xlsx, the share of it a dwelling holds: %.2f on rolling registration "
           "alone, then %s at its first to sixth canvass." % (f["settled"]["house"], f["settled"]["flat"], b["0"], shares),
           "4. Carried each dwelling at its seventh canvass or later on the 2025 register at its 2025 count and every other "
           "dwelling, in use since or due in housing_trajectory_2026-09-30.xlsx (%s from October 2026 to March 2032, and "
           "2032/33's April to October, each year's completions spread evenly at the site's remaining mix), at its type's "
           "settled level times its share at its canvasses on 1 December 2032." % f["components"]["trajectory_dwellings"],
           "5. Divided each ward's forecast by its councillors (wards_councillors_2014_order.csv) against the district's %s "
           "electors over %d councillors, %s each: %s wards lie more than 10 per cent from it." % (
               f["forecast"]["total"], f["constants"]["council_size"], f["forecast"]["average_whole"], WORDS[len(fail)]),
           "6. For the 2021 register, read ELECTRA_PROPERTY_ELECTORATE_REV_2021.txt as the register Electra held when it "
           "was switched off on 4 March 2022 (dwellings first in use after 31 October 2021 hold electors in it, each an "
           "addition in the 2022 notices) and backed each local government entry of the notices of 4 January, 1 February "
           "and 1 March 2022 in ELECTRA_NOTICES_OF_ALTERATION_2021-01_2022-03.txt out of each property's TOTAL less its "
           "attainers and overseas electors (an addition taken off, a deletion put back, F entries and attainers left), "
           "by the ward of its 2014 district through polling_district_review_2023_schedule.csv: %s electors." %
           f["ask_a_total"],
           "7. The draft recommendations address the %s wards outside 10 per cent." % WORDS[len(fail)],
           "", "## 4. Deliverable Answers", "",
           "### ward_electorate_forecast_2032.xlsx", "",
           "1. Finding for each ward on the 2032 forecast:"]
    order = f["constants"]["order"]
    for w in order:
        out.append("   - %s: %s" % (w, f["call"]["findings"][w].lower().replace("outside: ", "outside, ")))
    out.append("2. Local government electors on the register published 1 December 2021, whole electors:")
    for w in order:
        out.append("   - %s: %s" % (w, "{:,}".format(f["ask_a"][w])))
    out += ["", "### ward_variance_2032.png", "",
            "1. Horizontal bar chart of each ward's 2032 variance from the district average against the 10 per cent lines: "
            "the %s wards outside (%s) marked beyond the lines and the other %d within them." % (
                WORDS[len(fail)], joined(fail), len(meet))]
    with open(os.path.join(TASK, "submission.md"), "w") as fh:
        fh.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
