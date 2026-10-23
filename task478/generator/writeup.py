"""submission.md, every figure read from generator/figures.json."""
import json
import os

import bundle as B

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
SHORT = {"Wexley Point Energy Center": "Wexley Point", "Ashgrove Refining": "Ashgrove", "Valmora Glass Works": "Valmora",
         "Sedge Hollow Landfill Gas": "Sedge Hollow", "Haskett Ridge Compressor Station": "Haskett Ridge",
         "St. Aldric Medical Center": "St. Aldric", "Lindqvist Paperboard": "Lindqvist",
         "Tamsett State University": "Tamsett State", "Briar Flats Water Reclamation": "Briar Flats",
         "Merriwell Foods": "Merriwell", "Harrow Peaking Station": "Harrow", "Orchard Basin Almond Growers": "Orchard Basin",
         "Penrose Tire Retreading": "Penrose", "Quarry Lane Data Center": "Quarry Lane"}


def join(xs, word="and"):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " %s " % word + xs[-1]


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    F = f["facilities"]
    c = f["components"]
    five = f["call"]["facilities"]
    rank = f["rank"]
    six = c["sixth"]
    dflt = f["default"]
    out_default = [n for n in dflt["facilities"] if n not in five]
    in_default = [n for n in five if n not in dflt["facilities"]]
    hmm = f["ask_b"]["hmm_facilities"]
    rep = f["ask_b"]["replaced"]
    by_rank = sorted(five, key=rank.index)
    out = []
    out.append("## Tags\n")
    out.append("**Domain:** Physical & Environmental Sciences, emissions inventory (an air district's 2026 NOx inventory "
               "of fourteen facilities' SCR-controlled combustion units, conformed from continuous monitor hours, two "
               "source test databases, monthly emission statements and the compliance log, each unmonitored unit's "
               "rate carried along the operating hours on its catalyst).")
    out.append("**Analytical objective:** Data Extraction & Conformation (ETL).\n")
    out.append("## 1. Final Recommendation\n")
    out.append("**Sign the 2027 NOx reduction agreements with %s.**" % join(five))
    hask = "Haskett Ridge Compressor Station"
    out.append("Their Rule 4306 units emitted %s tons of NOx in 2026, against %s's %d in sixth. Not %s, whose %d tons "
               "on its latest source tests rest on two engines tested on worn catalysts it replaced in December "
               "2025; along the hours on the new catalysts its units emitted %d. Not %s, which makes the five on the latest "
               "tests only because they read %s weeks after new catalysts went in.\n"
               % (join(["%d" % F[n]["nox_tons"] for n in five]), six["name"], six["tons"], hask, dflt["tons"][hask],
                  F[hask]["nox_tons"], six["name"], join(["%s's" % SHORT[n] for n in in_default]) + " engines"))
    out.append("## 2. Critical Components\n")
    out.append("1. %s's units emitted **%d** tons and %s's **%d**, the lowest two of the five, against %s's **%d** in "
               "sixth." % (by_rank[3], F[by_rank[3]]["nox_tons"], by_rank[4], F[by_rank[4]]["nox_tons"], six["name"],
                           six["tons"]))
    out.append("2. Haskett Ridge Compressor Station's units emitted **%d** tons.\n"
               % F["Haskett Ridge Compressor Station"]["nox_tons"])
    out.append("## 3. Step-by-Step Solution\n")
    steps = [
        "Took the %d Rule 4306 devices in tbapcd_permit_devices.csv, %d with a CEMS, and summed each monitored "
        "device's 2026 nox_mass_lb in tbapcd_cems_hourly_2026.csv, matched by facility_id and unit_id to the permit "
        "list's FAC_NO and CEMS_UNIT_ID (guidance section 2): %s tons." % (c["devices"], c["monitored_units"],
                                                                          "{:,}".format(c["cems_tons"])),
        "Put every source test of the other %d units on lb/MMBtu, the 2022 to 2026 database's own column and the 2018 "
        "to 2021 database's NOX_LB_HR over FUEL_FLOW_SCFH times FUEL_HHV (guidance section 5): %d tests."
        % (c["open_units"], c["tests"]),
        "Spread each unit's monthly heat input (guidance section 4) and operating hours in "
        "tbapcd_emission_statements_2017_2026.csv evenly over the month's days, and counted each day's operating "
        "hours on the catalyst in service since the unit's last SCR INSTALLED or CATALYST date in "
        "tbapcd_compliance_events_2017_2026.csv.",
        "Fitted the log of each test's lb/MMBtu on its unit's catalyst hours at the start of the test day, one level "
        "for each unit and one climb for all: %s in the log for every 10,000 hours, about %d per cent for every 1,000 "
        "hours." % (c["climb_log_per_10000h"], c["climb_pct_per_1000h"]),
        "Summed each unit's 2026 heat input day by day at the rate its level and the climb give at the day's mid-day "
        "catalyst hours, and each facility's units: %s, then %s." % (
            join(["%s %d" % (SHORT[n], F[n]["nox_tons"]) for n in rank[:5]]),
            join(["%s %d" % (SHORT[n], F[n]["nox_tons"]) for n in rank[5:7]])),
        "For the gas, matched each line of tvg_commercial_billing_extract_2027-02.csv to its facility by service "
        "address and took USAGE_CCF as therms where it equals the read difference times PRESSURE_MULT times BTU_FACTOR "
        "(the %d lines the utility's new billing system issued, read from %s on) and as CCF times BTU_FACTOR where it "
        "equals the read difference times PRESSURE_MULT (the earlier lines), then divided by 10 and spread each bill "
        "as plan section 4.2 says: %s MMBtu in all." % (f["ask_a"]["therm_lines"], f["ask_a"]["first_therm_month"],
                                                         "{:,}".format(c["gas_total_mmbtu"])),
        "For the engines, read the logs of %s, which sum to their engines' hour meter differences in "
        "tbapcd_engine_inspections_2025_2027.csv only as hours and minutes, that way (1.30 is an hour and a half), "
        "took each run of %s before its 2026 replacement date at the removed engine's rating and tier in the "
        "compliance log's EQUIPMENT entry, and applied guidance section 6: %s lb in all."
        % (join(SHORT[n] for n in hmm), join(rep), "{:,}".format(c["engine_total_lb"])),
        "Recommended the five highest: %s." % join(five),
    ]
    for i, s in enumerate(steps, 1):
        out.append("%d. %s" % (i, s))
    out.append("")
    out.append("## 4. Deliverable Answers\n")
    out.append("### tbapcd_cerp_facilities_2027.xlsx\n")
    out.append("1. The five facilities for the 2027 NOx reduction agreements: %s." % join(five))
    out.append("2. Each facility's 2026 NOx from its Rule 4306 units, whole tons:")
    for n in B.ORDER:
        out.append("   - %s: %d" % (n, F[n]["nox_tons"]))
    out.append("3. Natural gas Tamsett Valley Gas delivered to each facility in calendar 2026, whole MMBtu:")
    for n in B.ORDER:
        out.append("   - %s: %s" % (n, "{:,}".format(F[n]["gas_mmbtu"])))
    out.append("4. NOx each facility's emergency standby engines emitted in 2026, whole pounds:")
    for n in B.ORDER:
        out.append("   - %s: %s" % (n, "{:,}".format(F[n]["engine_nox_lb"])))
    out.append("\n### tbapcd_nox_inventory_2026.csv\n")
    out.append("5. Fourteen rows in Appendix A order, each with the facility number, the facility and its tons as in "
               "item 2.")
    out.append("\n### tbapcd_facility_nox_2026.svg\n")
    out.append("6. Horizontal bar chart of the fourteen facilities' 2026 NOx from their Rule 4306 units, highest first, "
               "each bar labelled with its whole tons, the five agreement facilities in blue and the others in grey.")
    open(os.path.join(TASK, "submission.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
