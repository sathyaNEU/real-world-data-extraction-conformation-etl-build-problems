"""task304 architecture 4: submission.md, every figure read from figures.json."""
import json
import sys


def fmt(n):
    return "{:,}".format(int(n))


def write(fig_path, out_path):
    F = json.load(open(fig_path, encoding="utf-8"))
    best, second = F["call_hub"], F["runner_up"]
    hubs = F["hubs"]
    L = []
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** Epidemiology & Public Health (health burden and impact modelling: an occupational noise control).")
    L.append("**Analytical objective:** Opportunity Sizing & Decision Support.")
    L.append("")
    L.append("## 1. Final Recommendation")
    L.append("")
    L.append("**Brolga should install the 2027 induct-line enclosure at %s.** It brings %d workers from at or above "
             "85 dB(A) to below it, against %d at %s. Not %s, which leads only when every worker is given their job "
             "title's place, because at %s the inductors and the rotation's loaders share the induct hours. Not %s, "
             "which has the most workers at or above the standard (%d) but brings only %d below, its line staying above "
             "it for anyone at induct most of the shift."
             % (best, F["below"][best], F["below"][second], second, F["default_hub"], best, "Eastern Creek",
                F["pool"]["Eastern Creek"], F["below"]["Eastern Creek"]))
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    L.append("1. %s: **%d** workers at or above 85 dB(A) in the reference weeks, **%d** of them brought below by the "
             "enclosure (induct area **%.1f** dB(A) after it)." % (best, F["pool"][best], F["below"][best],
                                                               F["levels"][best]["Lp"]))
    L.append("2. %s, the runner-up: **%d** brought below." % (second, F["below"][second]))
    L.append("3. Eastern Creek: **%d** at or above, **%d** brought below." % (F["pool"]["Eastern Creek"],
                                                                          F["below"]["Eastern Creek"]))
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    L.append("1. Took every employee with a WORKED shift in ta_shift_records_20260928_20261108.csv and every labour-hire "
             "operative in labour_hire_timesheets_oct_nov_2026.xlsx whose shift began 12 October to 8 November 2026 "
             "(Schedule 2, clause %s), with each worker's hub and shifts worked." % F["clauses_cited"]["population"])
    L.append("2. Converted wcs_operator_sessions_export_20261116.csv from UTC to each hub's local time, placed each session "
             "in the shift it began in, and joined its badge to a payroll or labour-hire number through "
             "badge_register_20261113.xlsx at the session's date (reissued badges by their issue and cancel dates, "
             "contractors left out).")
    L.append("3. Summed each worker's induct hours over the reference weeks, divided by their shifts worked, and computed "
             "their LAeq,8h per Schedule 2, clause %s, from the induct, floor and amenities levels in "
             "noise_survey_report_2026.pdf, before and with the induct level in induct_enclosure_design_report_rev2.pdf."
             % F["clauses_cited"]["exposure"])
    L.append("4. Counted by hub the workers at 85 dB(A) or more and those brought below it: %s %d brought below, %s %d."
             % (best, F["below"][best], second, F["below"][second]))
    L.append("5. Placed each EP-01 vend in ppe_vending_transactions_2026q3.json at the hub its machine stood at, from the "
             "sites of its visits in ppe_vending_service_visits_2026q3.csv (moving on its COMMISSION visit, not the asset "
             "list's current site), in that hub's local time, at one pair a vend before the machine's RANGE CHANGE visit "
             "and five pairs from it.")
    L.append("6. Replayed each client's tests in audiometry_results_2025_2026.csv from their first test per Schedule 3, "
             "each confirming retest becoming the reference (not the reference in audiometry_clients_20261106.xlsx), "
             "and placed each shift confirmed in 2026 at the worker's hub on the retest date from "
             "hr_site_transfers_2026.csv.")
    L.append("7. Placed the enclosure at the hub with the most workers brought below: %s." % best)
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append("### induct_enclosure_2027.pptx")
    L.append("")
    L.append("1. The hub: %s." % best)
    L.append("2. Workers at or above 85 dB(A) in the reference weeks, and brought below it by the enclosure, by hub:")
    for h in hubs:
        L.append("   - %s: %d at or above, %d brought below" % (h, F["pool"][h], F["below"][h]))
    L.append("3. Bar chart of the workers brought below by hub on slide 3, %s's bar marked." % best)
    L.append("")
    L.append("### hearing_program_2026.csv")
    L.append("")
    L.append("1. Earplug pairs issued at each hub in July, August and September 2026, local time:")
    for h in hubs:
        p = F["pairs"][h]
        L.append("   - %s: July %s; August %s; September %s" % (h, fmt(p["7"]), fmt(p["8"]), fmt(p["9"])))
    L.append("2. Workers whose 2026 hearing tests confirmed a standard threshold shift:")
    for h in hubs:
        L.append("   - %s: %d" % (h, F["sts"][h]))
    L.append("")
    open(out_path, "w", encoding="utf-8").write("\n".join(L))


if __name__ == "__main__":
    write(sys.argv[1], sys.argv[2])
