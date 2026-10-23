"""submission.md, every figure read from generator/figures.json."""
import json
import os

import bundle as B

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
SHORT = {"Wexley Point Energy Center": "Wexley Point", "Ashgrove Refining": "Ashgrove",
         "Valmora Renewable Fuels": "Valmora", "Sedge Hollow Creamery": "Sedge Hollow",
         "Haskett Ridge Poultry": "Haskett Ridge", "St. Aldric Medical Center": "St. Aldric",
         "Lindqvist Paperboard": "Lindqvist", "Tamsett State University": "Tamsett State",
         "Briar Flats Water Reclamation": "Briar Flats", "Merriwell Foods": "Merriwell",
         "Harrow Linen Services": "Harrow Linen", "Orchard Basin Almond Growers": "Orchard Basin",
         "Penrose Tire Retreading": "Penrose", "Quarry Lane Correctional Facility": "Quarry Lane"}
MONTH = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
         "December")


def join(xs, word="and"):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " %s " % word + xs[-1]


def pos(n):
    return n + ("'" if n.endswith("s") else "'s")


def day(s):
    y, m, d = s.split("-")
    return "%d %s" % (int(d), MONTH[int(m) - 1])


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    F = f["facilities"]
    c = f["components"]
    five = f["call"]["facilities"]
    rank = f["rank"]
    six = c["sixth"]
    dflt = f["default"]
    in_default = [n for n in dflt["facilities"] if n not in five]
    out_default = [n for n in five if n not in dflt["facilities"]]
    el = f["ask_b"]["elog"]
    rep = f["ask_b"]["replaced"]
    banked = f["ask_b"]["bank_facilities"]
    by_rank = sorted(five, key=rank.index)
    out = []
    out.append("## Tags\n")
    out.append("**Domain:** Physical & Environmental Sciences, emissions inventory (an air district's 2026 NOx inventory "
               "of fourteen facilities' boilers and process heaters, conformed from continuous monitor hours, two "
               "source test databases, monthly emission statements and the gas utility's heat content, each unmonitored "
               "low-NOx burner's tests carried to the heat content of each month's gas).")
    out.append("**Analytical objective:** Data Extraction & Conformation (ETL).\n")
    out.append("## 1. Final Recommendation\n")
    out.append("**Sign the 2027 NOx reduction agreements with %s.**" % join(five))
    tam, mer = in_default[0], out_default[0]
    out.append("Their Rule 4306 units emitted %s tons of NOx in 2026, against %s %d in sixth. Not %s, whose boilers' "
               "latest source tests were read in May 2026 on rich Westside gas and overstate a winter fired on lean; %s "
               "latest tests were read in August 2025 on lean gas and understate a canning season fired on 2026's rich "
               "summer gas.\n" % (join(["%d" % F[n]["nox_tons"] for n in five]), pos(six["name"]), six["tons"], tam,
                                   pos(mer)))
    out.append("## 2. Critical Components\n")
    out.append("1. A low-NOx burner's rate rises about **%d** per cent for each per cent rise in its gas's heat content, "
               "from the monitored Lindqvist power boiler's 2026 hours against the Westside heat content."
               % c["rise_pct_per_pct"])
    out.append("2. %s units emitted **%d** tons and %s **%d**, the lowest two of the five, against %s **%d** in "
               "sixth.\n" % (pos(by_rank[3]), F[by_rank[3]]["nox_tons"], pos(by_rank[4]), F[by_rank[4]]["nox_tons"],
                             pos(six["name"]), six["tons"]))
    out.append("## 3. Step-by-Step Solution\n")
    steps = [
        "Took the %d Rule 4306 devices in tbapcd_permit_devices.csv, %d with a CEMS, and summed each monitored "
        "device's 2026 nox_mass_lb in tbapcd_cems_hourly_2026.csv, matched by facility_id and unit_id to the permit "
        "list's FAC_NO and CEMS_UNIT_ID (guidance section 2): %s tons." % (c["devices"], c["monitored_units"],
                                                                          "{:,}".format(c["cems_tons"])),
        "Put the %d source tests of the other %d units on lb/MMBtu, the 2022 to 2026 database's own column and the "
        "2018 to 2021 database's NOX_PPMVD at 3 per cent oxygen through Method 19 (guidance section 5), and took each "
        "unit's 2026 monthly heat input from tbapcd_emission_statements_2018_2026.csv, MMSCF at the heat content in "
        "tvg_monthly_heat_content_2018_2027.csv for the facility's BTU area and month (guidance section 4)."
        % (c["tests"], c["open_units"]),
        "Fitted the log of the Lindqvist power boiler's measured 2026 hourly NOx rate (D-1701, nox_rate_modc 01) on its "
        "Westside BTU_FACTOR over 1.035 in the hour's month: about %d per cent a per cent of heat content, the rise the "
        "Westside burners' own tests show against their months' heat content." % c["rise_pct_per_pct"],
        "Carried each unmonitored burner's tests from their months' heat content to 1.035 by that rise, took the unit's "
        "level as the geometric mean of its carried tests, and summed each 2026 month's heat input at that level "
        "carried to the month's heat content, then each facility's units: %s, then %s." % (
            join(["%s %d" % (SHORT[n], F[n]["nox_tons"]) for n in rank[:5]]),
            join(["%s %d" % (SHORT[n], F[n]["nox_tons"]) for n in rank[5:7]])),
        "For the gas, matched each line of tvg_commercial_billing_extract_2027-02.csv to its facility by service "
        "address, took USAGE_THERMS on the lines read before 1 July 2026 as corrected CCF times BTU_FACTOR (read as "
        "therms they fall below the plan units' own fuel in the emission statements) and as therms from the July reads, "
        "took the usage of the combined-billing accounts %s once a period, not once a meter, then divided by 10 and "
        "spread each bill as plan section 4.2 says: %s MMBtu in all." % (
            join(f["ask_a"]["combined_accounts"]), "{:,}".format(c["gas_total_mmbtu"])),
        "For the engines, read the logs of %s as hours and minutes from their first e-logbook entries (%s; 0.30 is half "
        "an hour, as the hour meters in tbapcd_engine_inspections_2025_2027.csv bear out), took the emergency lines of "
        "the engines run in parallel at %s at the outage hours the compliance log's OUTAGE entries record, each run of "
        "%s before its 2026 replacement at the removed engine's rating and tier in the EQUIPMENT entry, and applied "
        "guidance section 6: %s lb in all." % (
            join(SHORT[n] for n in B.ORDER if n in el), join("%s %s" % (SHORT[n], day(el[n])) for n in B.ORDER
                                                             if n in el),
            join(SHORT[n] for n in banked), join(rep), "{:,}".format(c["engine_total_lb"])),
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
