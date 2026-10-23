"""submission.md, drafted from generator/figures.json so every figure it states is one the generator computed.

    python3 task273/generator/writeup.py"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
NAME = {"Taxi": "Taxicabs", "Ride-hail": "Ride-hail", "Limousine": "Limousines", "Airport shuttle": "Airport shuttles",
        "Paratransit": "Paratransit", "Parcel delivery": "Parcel delivery", "App delivery": "App-based delivery"}
ORDER = ["Taxi", "Ride-hail", "Limousine", "Airport shuttle", "Paratransit", "Parcel delivery", "App delivery"]
WORD = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven"}


def joined(xs):
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def low(x):
    return x.lower()


def names(xs):
    return joined([NAME[x].lower() for x in xs])


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    cov = [NAME[u] for u in f["call"]["covered"]]
    notc = [NAME[u] for u in f["call"]["not_covered"]]
    u = f["uses"]
    above_name, above = f["nearest"]["above"]
    below_names, below = f["nearest"]["under"]
    hi = max(f["call"]["covered"], key=lambda x: u[x]["ratio"])
    s = f["sample"]
    a = f["asks"]
    out = ["## Tags", "",
           "**Domain:** General Statistics & Data Science (missing data, censoring and measurement error).",
           "**Analytical objective:** Descriptive & Distribution Analysis.", "",
           "## 1. Final Recommendation", "",
           "**The programme should cover %s of the seven uses: %s.**" % (WORD[len(cov)], names(f["call"]["covered"])),
           "Their drivers caused crashes at %.1f to %.1f times private drivers' rate per mile, %s nearest the line at "
           "%.1f, while %s all stay under %.1f. Not airport shuttles and paratransit, which the struck vehicles' share of the "
           "whole five years puts over the line: their miles run on freeways and in daylight, where crashes per mile "
           "are rare, so too few of them are struck for the miles they drive. Not a count of vehicles registered or "
           "permitted, which covers six uses because a commercial vehicle drives several times a private car's miles. "
           "Not road class or hour alone, each of which leaves ride-hail or both delivery uses under the line."
           % (above, u[hi]["ratio"], low(NAME[above_name]), above, names(below_names), below),
           "",
           "## 2. Critical Components", "",
           "1. Crashes caused between moving vehicles, 2021 to 2025: %s; private drivers **%s**."
           % ("; ".join("%s **%s**" % (low(NAME[x]), format(u[x]["crashes_caused"], ",")) for x in ORDER),
              format(f["private"]["crashes_caused"], ",")),
           "2. The Department's miles for the five years: **%s** million on the region's roads, in **%d** road class, "
           "day type and hour strata." % (format(int(f["region_miles_millions"]), ","), s["strata"]),
           "3. Each use's miles come from the **%s** vehicles that at-fault drivers struck in crashes with one driver "
           "at fault, each stratum's miles shared in proportion to them." % format(s["struck_vehicles"], ","),
           "4. %s, the nearest use above the line, at **%.1f** times private drivers' rate; %s all under "
           "**%.1f**." % (NAME[above_name], above, names(below_names), below),
           "",
           "## 3. Step-by-Step Solution", "",
           "1. From crash_extract_2021_2025_crashes.csv and crash_extract_2021_2025_units.csv, kept the crashes with "
           "two or more vehicles in transport (the coverage rule's crashes): %s crashes." % format(s["crashes_between_moving"], ","),
           "2. Took each crash's at-fault drivers from the 2023 form's AT_FAULT_UNIT and the 2016 form's contributing "
           "circumstance, gave each 2016 vehicle for hire or delivery the use of the operator named on the report "
           "(commission_operator_register_2026.xlsx), and left out drivers who fled unidentified, as the rule says: private "
           "drivers caused %s crashes." % format(f["private"]["crashes_caused"], ","),
           "3. Placed each crash in its road class (2016 crashes by legacy route and milepost through "
           "lrs_road_inventory_2025.xlsx), day type and Pacific hour (State Patrol times converted from UTC): %d strata."
           % s["strata"],
           "4. Gave each stratum the Department's miles: its road class's 2021 to 2025 VMT "
           "(travel_monitoring_report_2025.pdf, Table 1) times the class's share of its count stations' 2025 traffic in "
           "that day type and hour (ccs_hourly_volumes_2025.csv): %s million miles in all."
           % format(int(f["region_miles_millions"]), ","),
           "5. Shared each stratum's miles among the uses in proportion to the vehicles struck there by the one "
           "at-fault driver of a crash: %s vehicles struck." % format(s["struck_vehicles"], ","),
           "6. Divided each use's crashes caused by its miles and set the rate against private drivers': %s at "
           "%.1f, %.1f, %.1f and %.1f times; %s under %.1f."
           % (names(["Taxi", "Ride-hail", "Parcel delivery", "App delivery"]), u["Taxi"]["ratio"],
              u["Ride-hail"]["ratio"], u["Parcel delivery"]["ratio"], u["App delivery"]["ratio"], names(below_names),
              below),
           "7. For the asks, read crash_extract_2021_2025_persons_injury_crashes.csv one person once (a person listed "
           "again in the same seat of the same unit taken at the later record), with deaths from "
           "road_fatality_register_2021_2025.csv, over every crash of any kind a use's driver caused, and costed each "
           "crash once at its most severe final injury (dot_crash_unit_costs_2025.pdf): ride-hail %s people and USD "
           "%s million." % (format(a["ksi"]["Ride-hail"], ","), format(a["cost_millions"]["Ride-hail"], ",.1f")),
           "8. Recommended covering %s." % names(f["call"]["covered"]),
           "",
           "## 4. Deliverable Answers", "",
           "### fleet_safety_programme_2027.xlsx", "",
           "1. The coverage test, every use:"]
    for x in ORDER:
        out.append("   - %s: %s" % (NAME[x], "covered" if u[x]["covered"] else "not covered"))
    out.append("2. People killed or seriously injured in all the crashes each use's drivers caused, 2021 to 2025 (whole "
               "people):")
    for x in ORDER:
        out.append("   - %s: %s" % (NAME[x], format(a["ksi"][x], ",")))
    out.append("3. Cost of those crashes at the Department's crash unit costs (millions of dollars, one decimal):")
    for x in ORDER:
        out.append("   - %s: %s" % (NAME[x], format(a["cost_millions"][x], ",.1f")))
    out += ["", "### fleet_safety_programme_2027.pptx", "",
            "1. One chart of each use's rate per mile of causing crashes against private drivers' rate with the line "
            "at 1.5, the %s covered uses above it and highlighted (slide 2)." % WORD[len(cov)]]
    txt = "\n".join(out) + "\n"
    assert "—" not in txt
    with open(os.path.join(TASK, "submission.md"), "w", encoding="utf-8") as fh:
        fh.write(txt)
    return txt


if __name__ == "__main__":
    print(main())
