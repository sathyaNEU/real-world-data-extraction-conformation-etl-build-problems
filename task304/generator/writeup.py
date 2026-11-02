"""task304 architecture 5: submission.md, every figure emitted from figures.json."""

SNAME = ["Fatal", "Serious", "Slight"]
GROUPS = ["Pedestrian", "Pedal cyclist", "Motorcyclist", "Car occupant"]
QLAB = {"Q1": "Q1 (January to March)", "Q2": "Q2 (April to June)", "Q3": "Q3 (July to September)"}


def write(path, F):
    best, ru = F["call"], F["runner_up"]
    L = []
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** Urban & Regional Science (municipal service demand and resource allocation: a junction safety "
             "scheme placed on a county road network).")
    L.append("**Analytical objective:** Opportunity Sizing & Decision Support.")
    L.append("")
    L.append("## 1. Final Recommendation")
    L.append("")
    L.append("**Ardleshire should bid for the roundabout at %s.** It would prevent %.1f injury collisions a year, against "
             "%.1f at %s. Not %s, which had the most collisions in 2021 to 2025 but carries little traffic, so most of its "
             "count is the chance that listed it. Not %s, whose traffic predicts the most collisions of any listed junction "
             "but whose own record runs well below that." % (best, F["call_benefit"], F["runner_up_benefit"], ru,
                                                   F["observed_route"], F["model_route"]))
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    L.append("1. %s's expected injury collisions a year as it stands, at its 2026 traffic: **%.1f**." % (best, F["call_expected"]))
    L.append("2. %s's benefit (crossroads factor %.2f): **%.1f** injury collisions prevented a year." % (best, F["cmf"][best], F["call_benefit"]))
    L.append("3. %s, the runner-up: **%.1f** a year." % (ru, F["runner_up_benefit"]))
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    L.append("1. Took the listed junctions from network_screening_2026.pdf (give-way or stop-controlled junctions with %d or "
             "more injury collisions in 2021 to 2025) and their layout, control and traffic by year from "
             "junction_inventory_2026.xlsx." % F["screen_minimum"])
    L.append("2. Counted injury collisions by junction node and year for 2021 to 2025 in collision_records_2016_2025.csv, for "
             "every give-way or stop-controlled T, staggered and crossroads junction in the inventory (%s junctions, zero "
             "years included)." % "{:,}".format(F["reference_junctions"]))
    L.append("3. Fitted a negative binomial safety performance function to those junction-years (log of major and minor road "
             "traffic, layout and year terms): overdispersion %.2f." % F["overdispersion"])
    L.append("4. Combined each listed junction's own 2021 to 2025 count with its predicted count by empirical Bayes (weight "
             "1 / (1 + overdispersion x predicted five-year count) on the prediction) and carried the result to the "
             "junction's 2026 traffic at the window's average year level: %s %.1f a year." % (best, F["call_expected"]))
    L.append("5. Multiplied by one less the crash modification factor for each layout in Table 2 of "
             "junction_safety_fund_guidance_2027.pdf: %s %.1f prevented a year, %s %.1f." % (best, F["call_benefit"], ru,
                                                                                           F["runner_up_benefit"]))
    L.append("6. For Annex A, read the old system's 2026 collisions and casualties to May and the new system's JSON export from "
             "June, kept each collision the migration re-sent once (the new record on the same date and road within %d "
             "minutes and %d metres of an old one replaces it), applied the deaths within %d days in "
             "fatal_casualty_notifications_2026.xlsx matched on date, road, time and casualty, and left out the trunk "
             "sections in road_network_register_2026.csv, placed by their end nodes' eastings in the inventory." % (
                 F["match_minutes"], F["match_metres"], F["death_days"]))
    L.append("7. Took a collision's severity from its most severely injured casualty and each casualty's road user from "
             "casualty_type (old system) or class and the vehicle they were in (new system), by quarter of the collision date.")
    L.append("8. Placed the roundabout at the junction with the largest benefit: %s." % best)
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append("### junction_bid_2027.docx")
    L.append("")
    L.append("1. The junction: %s." % best)
    L.append("2. Injury collisions a roundabout would prevent each year, every listed junction:")
    for n in sorted(F["junctions"], key=lambda x: -F["benefit"][x]):
        L.append("   - %s: %.1f" % (n, F["benefit"][n]))
    L.append("3. Bar chart of those benefits by junction in Figure 1, %s's bar marked as the junction chosen." % best)
    L.append("")
    L.append("### bid_annex_2026.xlsx")
    L.append("")
    L.append("1. Injury collisions on the county's roads in 2026 by quarter and severity (A1):")
    for q in ("Q1", "Q2", "Q3"):
        a = F["ask_a"][q]
        L.append("   - %s: fatal %d; serious %d; slight %d" % (QLAB[q], a["Fatal"], a["Serious"], a["Slight"]))
    L.append("2. Their casualties in 2026 by quarter and road user (A2):")
    for q in ("Q1", "Q2", "Q3"):
        b = F["ask_b"][q]
        L.append("   - %s: pedestrians %d; pedal cyclists %d; motorcyclists %d; car occupants %d" % (
            QLAB[q], b["Pedestrian"], b["Pedal cyclist"], b["Motorcyclist"], b["Car occupant"]))
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
