"""submission.md, every figure read from generator/figures.json."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def join(xs, word="and"):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " %s " % word + xs[-1]


def pos(n):
    return n + ("'" if n.endswith("s") else "'s")


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    P = f["plants"]
    c = f["components"]
    st = f["stated"]
    cov = f["call"]["plants"]
    d = f["default"]
    nb = c["nearest_below"]
    added = [n for n in cov if n not in d["plants"]]
    order = list(P)
    out = []
    out.append("## Tags\n")
    out.append("**Domain:** Physical & Environmental Sciences, emissions inventory (a state air agency's 2026 press "
               "VOC inventory of fourteen printing and converting plants, conformed from press logs, safety data "
               "sheets, capture determinations, oxidizer historians and performance tests, each oxidizer's outlet "
               "carried to each production day's inlet).")
    out.append("**Analytical objective:** Data Extraction & Conformation (ETL).\n")
    out.append("## 1. Final Recommendation\n")
    out.append("**Rule 18-4 covers %s from 1 July 2027.**" % join(cov))
    out.append("Their presses emitted %s tons of VOC in 2026, %s the lowest at %d, against %s %d (%d short). Not the "
               "oxidizers' tested efficiencies, which put %s at %s tons: every test ran at maximum production, and on "
               "the part-production days of 2026 the fixed-speed fans drew their full air, so the oxidizers' outlets "
               "held near their floor and destroyed less than the tests show.\n"
               % (join(["%d" % P[n]["press_voc_tons"] for n in cov]), c["lowest_covered"]["name"],
                  c["lowest_covered"]["tons"], nb["name"], nb["tons"], nb["short_tons"], join(added),
                  join(["%d" % d["tons"][n] for n in added])))
    out.append("## 2. Critical Components\n")
    out.append("1. Across the %d tests the outlet holds near **%.0f** ppmv as carbon below an inlet of about **%s** "
               "ppmv and passes **%.1f** per cent of the inlet above it." % (c["tests"], c["floor_ppmc"],
                                                                            "{:,}".format(c["knee_ppmc"]),
                                                                            c["pass_pct"]))
    for i, n in enumerate(added, 2):
        out.append("%d. %s 2026 press VOC is **%d** tons, against **%d** on its latest test's efficiency."
                   % (i, pos(n), P[n]["press_voc_tons"], d["tons"][n]))
    out.append("%d. %s, the nearest plant below the line, emitted **%d** tons, **%d** short.\n"
               % (len(added) + 2, nb["name"], nb["tons"], nb["short_tons"]))
    out.append("## 3. Step-by-Step Solution\n")
    steps = [
        "Converted every row of press_material_use_2026.csv (shift and job records alike, Thameside Laminating's "
        "facility 0117 rows to Kelvedon Laminates) to pounds of VOC through safety_data_sheet_master_2027-01.xlsx: "
        "per cent by weight times density, or pounds per gallon less water and exempt compounds times the share of "
        "the product that is neither, pound rows by density.",
        "Split each controlled plant's VOC by the capture efficiency on the Capture sheet of "
        "deq_printing_plants_register_2027-02.xlsx; the four plants without an oxidizer emit what they used.",
        "Put oxidizer_historian_hourly_2026.csv on Central time, took each production day's PROCESS hours and their "
        "mean airflow (fan speed times the register's rated airflow where the historian logs speed), and with the "
        "register's carbon content read each day's inlet as carbon from its captured VOC.",
        "Put the %d runs in oxidizer_performance_tests_2017_2026.pdf on one basis (Marlow's propane figures times %d) "
        "and took the outlet as the mean of the runs under %s ppmv, about %.0f, and above the knee the mean share the "
        "runs over %s ppmv pass, %.1f per cent." % (c["runs"], st["propane_to_carbon"],
                                                  "{:,}".format(st["dilute_below_ppmc"]), c["floor_ppmc"],
                                                  "{:,}".format(st["concentrated_above_ppmc"]), c["pass_pct"]),
        "Read each day's outlet from its inlet, times its air and hours, for what the oxidizer let through, added the "
        "uncaptured VOC and compared each plant's year with 25 tons: %s." % join(
            ["%s %d" % (n, P[n]["press_voc_tons"]) for n in sorted(order, key=lambda n: -P[n]["press_voc_tons"])[:7]]),
        "For cleaning, priced each stores_cleaning_issues_2026.csv issue away from the presses at the revision in "
        "force on its date (HW-CS-210 at %.2f lb a gallon before its 1 June 2026 reformulation, per the revision log), "
        "less cantrell_bend_manifests_2026.csv weights under each plant's Cleaning profile (KG rows times %.5f), plus "
        "each washer's added less removed solvent in wexcombe_service_tickets_2026.csv and in Ostrander's lines in "
        "solvent_vendor_payments_2026.csv." % (st["cs210_rev3_lb_gal"], st["kg_to_lb"]),
        "For the gallons, took Corvane and Haldane lines shipped in 2026 (returns netted), read Haldane items on "
        "documents dated before 1 April 2026 through the replaces_item column of haldane_catalog_2026-04.csv, turned "
        "pound items into gallons by density, and set them against stock_counts_2026.csv and the press logs' use.",
        "Listed the plants at 25 tons or more: %s." % join(cov),
    ]
    for i, s in enumerate(steps, 1):
        out.append("%d. %s" % (i, s))
    out.append("")
    out.append("## 4. Deliverable Answers\n")
    out.append("### deq_rule18-4_applicability_2027.xlsx\n")
    out.append("1. Plants Rule 18-4 covers from 1 July 2027: %s." % join(cov))
    out.append("2. Each plant's 2026 press VOC, whole tons, and whether the rule covers it:")
    for n in order:
        out.append("   - %s: %d, %s" % (n, P[n]["press_voc_tons"], "covered" if P[n]["covered"] else "not covered"))
    out.append("3. Nearest plant below the line: %s, %d tons short." % (nb["name"], nb["short_tons"]))
    out.append("4. Each plant's 2026 VOC from cleaning away from its presses, tons to one decimal:")
    for n in order:
        out.append("   - %s: %.1f" % (n, P[n]["cleaning_voc_tons"]))
    out.append("5. Gallons of inks, coatings and adhesives each plant received in 2026 that its stock counts and press "
               "logs leave unaccounted for, whole gallons:")
    for n in order:
        out.append("   - %s: %s" % (n, "{:,}".format(P[n]["unaccounted_gal"])))
    out.append("\n### deq_printing_press_voc_2026.csv\n")
    out.append("6. Fourteen rows, each with the facility number, the plant, its 2026 press VOC as in item 2 and Y or N "
               "for coverage.")
    out.append("\n### deq_printing_press_voc_2026.svg\n")
    out.append("7. Horizontal bar chart of the fourteen plants' 2026 press VOC, highest first, each bar labelled with "
               "its whole tons, a vertical line at 25 tons, the five covered plants in blue and the rest in grey.")
    open(os.path.join(TASK, "submission.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
