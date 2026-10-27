"""submission.md, drafted from figures.json.

    python3 task307/generator/writeup.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
ORDER = ["TIP-28-014", "TIP-28-021", "TIP-28-009", "TIP-28-030"]
STATIONS = {"S-0101": "Route 9, Ashkettle Bridge", "S-0102": "Center Street Bridge", "S-0103": "Southport Bridge",
            "S-0104": "Route 9 at Millbrook", "S-0105": "Route 9 south of Lakeview Road",
            "S-0106": "Millbrook Road at Quarry Lane", "S-0107": "Harbor Avenue at Dock Street",
            "S-0108": "Lakeview Parkway east of Harbor Avenue"}
CORR = {"R9": "Route 9, Lakeview Road to Ferry Street", "CS": "Center Street, Millbrook Road to downtown",
        "SP": "Southport Avenue, Millbrook Road to downtown", "HA": "Harbor Avenue, Southport Bridge to Lakeview Parkway"}
DIRWORD = {"EB": "eastbound", "WB": "westbound"}


def c(n):
    return "{:,}".format(int(n))


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    a, ru = F["award"], F["runner_up"]
    an, pm = F["annual_vh"], F["per_musd_vh"]
    L = []
    L += ["## Tags", "",
          "**Domain:** Urban and regional science (transportation network planning).",
          "**Analytical objective:** Opportunity sizing and decision support.", ""]
    L += ["## 1. Final Recommendation", "",
          "**Put the Center Street Bridge widening (%s) forward for the FY2028 TIP's congestion-relief slot: with the "
          "2028 peak-hour trips re-assigned to equilibrium on each build network it saves %s vehicle-hours a year, %s "
          "per million dollars.**" % (a, c(an[a]), c(pm[a])),
          "Not the Route 9 Millbrook auxiliary lane (%s, %s per million), which saves the most when its own links are "
          "re-timed at the no-build volumes, but once trips re-route its extra lane feeds the Route 9 bridge, which "
          "binds, while the Center Street lane draws trips off Route 9. Not the Southport signal and turn-lane package "
          "(%s, %s per million) or the Ferry Street exit ramp (%s, %s per million)."
          % (c(an[ru]), c(pm[ru]), c(an["TIP-28-030"]), c(pm["TIP-28-030"]), c(an["TIP-28-021"]), c(pm["TIP-28-021"])),
          ""]
    L += ["## 2. Critical Components", "",
          "1. The Center Street Bridge widening saves **%s** vehicle-hours a year" % c(an[a]),
          "2. The Route 9 Millbrook auxiliary lane saves **%s** vehicle-hours a year once trips re-route" % c(an[ru]),
          "3. The Center Street Bridge widening saves **%s** vehicle-hours a year per million dollars" % c(pm[a]), ""]
    L += ["## 3. Step-by-Step Solution", "",
          "1. Built the directed network from the two-way records in MAMPO_v42_subarea_links_2028NB.csv (capacity is "
          "each direction's lanes times Table 4.2's capacity per lane, times by Table 4.2's volume-delay functions) "
          "and coded each candidate's change from the Model coding sheet of FY2028_TIP_congestion_relief_candidates."
          "xlsx: the Center Street Bridge widening is the largest change in the region's peak-hour vehicle-hours.",
          "2. Assigned the AM and PM tables in MAMPO_v42_subarea_trips_2028.csv to user equilibrium (relative gap "
          "below 0.000001, documentation 6.1) on the no-build network and on each build network, and annualised each "
          "reduction per scoring guidance 2.2 (times 247 times 2.9): Center Street %s, Route 9 %s, Southport %s, Ferry "
          "Street %s vehicle-hours a year." % (c(an[a]), c(an[ru]), c(an["TIP-28-030"]), c(an["TIP-28-021"])),
          "3. Divided by each candidate's year-of-expenditure cost in the Candidates sheet: Center Street %s, "
          "Southport %s, Route 9 %s, Ferry Street %s vehicle-hours per million dollars."
          % (c(pm[a]), c(pm["TIP-28-030"]), c(pm[ru]), c(pm["TIP-28-021"])),
          "4. For the count stations (ATR_hourly_volumes_2025.csv, S-0103R continuing S-0103), an hour is a true count "
          "only when both directions answered with status OK, it is not the first answered poll after a missed one "
          "inside a running day (the station's counters carry the missed hours' vehicles into it), and the direction "
          "is outside a fault: from the first hour its share of the two-way traffic steps away from its usual share "
          "for that hour of the week through the day of the loop or detector card work order in the Maintenance 2025 "
          "sheet of ATR_station_inventory_2025.xlsx; valid days and the K-factor's hours follow manual 4.1 to 4.3, "
          "giving the AADT and K-factors in block 4.",
          "5. For the validation, converted VOL_PCE in MAMPO_v42_base2025_station_volumes.csv to vehicles with "
          "HV_PCT (documentation 6.3) and compared it with the mean count at hour ending 8 (AM) and 18 (PM) over the "
          "valid Tuesdays to Thursdays of March to May and September to October 2025 (documentation 6.4), giving the "
          "percentages in block 4.",
          "6. The slot goes to the largest annual benefit (scoring guidance 3.1): the Center Street Bridge widening.",
          ""]
    L += ["## 4. Deliverable Answers", "", "### mampo_tip2028_project_ranking.xlsx", "",
          "1. Annual benefit and benefit per million dollars, each candidate (vehicle-hours a year to the nearest "
          "1,000; vehicle-hours per USD 1 million to the nearest 100):"]
    for k in F["ranking"]:
        L.append("   - %s %s: %s; %s" % (k, F["names"][k], c(an[k]), c(pm[k])))
    L.append("2. The recommended project: %s, %s." % (a, F["names"][a]))
    L.append("3. 2025 AADT (whole vehicles) and K-factor (three decimals), each permanent station:")
    for s in sorted(F["aadt"]):
        L.append("   - %s %s: AADT %s; K %s" % (s, STATIONS[s], c(F["aadt"][s]), F["k_factor"][s]))
    L.append("4. 2025 base-year validation, model less count as a percentage of the count (one decimal):")
    for key, v in F["validation_pct"].items():
        s, d, per = key.split()
        L.append("   - %s %s %s %s peak hour: %s" % (s, STATIONS[s], DIRWORD[d], per, v))
    L += ["", "### mampo_tip2028_executive_brief.pptx", "",
          "1. Recommendation: put the Center Street Bridge widening forward, %s vehicle-hours a year, %s per million "
          "dollars." % (c(an[a]), c(pm[a])),
          "2. Bar chart of the four candidates' annual benefits on slide 1, Center Street highlighted."]
    L.append("")
    open(os.path.join(TASK, "submission.md"), "w").write("\n".join(L))


if __name__ == "__main__":
    main()
