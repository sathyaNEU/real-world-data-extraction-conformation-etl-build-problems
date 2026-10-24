"""submission.md from generator/figures.json: the five blocks, every figure taken from the generator's own output."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
ORDER = ["Brannock", "Ivelton", "Quarrow", "Saddeny", "Wethermoor", "Ellick"]
SCC = [("2104008310", "non-certified freestanding woodstoves"), ("2104008320", "certified non-catalytic woodstoves"),
       ("2104008330", "certified catalytic woodstoves"), ("2104008400", "pellet stoves"),
       ("2104008100", "fireplaces"), ("2104008610", "outdoor hydronic heaters")]
COUNTY = {"Brannock": "Selwick", "Ivelton": "Selwick", "Quarrow": "Corrin", "Saddeny": "Corrin", "Wethermoor": "Tamsey",
          "Ellick": "Tamsey"}


def t1(x):
    return "%.1f" % x


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    A = f["areas"]
    trig = [a for a in ORDER if A[a]["determination"] == "TRIGGERED"]
    clear = [a for a in ORDER if a not in trig]
    k = f["constants"]
    out = ["## Tags", "",
           "**Domain:** Physical & Environmental Sciences, emissions inventory (a regional clean air agency's periodic "
           "inventory of residential wood combustion for six PM2.5 maintenance areas, built from its device registry, "
           "its household survey, its stove changeout programme's applications, the maintenance plans' 2014 base year, "
           "the state tool, ACS block-group tables and the assessors' housing units).",
           "**Analytical objective:** Data Extraction & Conformation (ETL).", "",
           "## 1. Final Recommendation", "",
           "**%s and %s trigger their contingency measures for the 2026-27 heating season; %s do not.**" %
           (trig[0], trig[1], ", ".join(clear[:-1]) + " and " + clear[-1]),
           "Each area's 2014 base year is rebuilt for the appliances the plan counted then: the non-certified stoves and "
           "outdoor boilers changed out since 2015 burned at the survey's rate for their class and the heat status on "
           "their applications (the programme funded main-heat households first), the rest of the 2014 stock at the "
           "survey's rate for its class. Carrying the survey's class means back to the 2014 count reads the survivors "
           "as the 2014 stock and triggers all six areas.", "",
           "## 2. Critical Components", "",
           "1. Areas triggering their contingency measure: **%s** (%s per cent against %d) and **%s** (%s per cent "
           "against %d)." % (trig[0], t1(A[trig[0]]["reduction"]), A[trig[0]]["commitment"], trig[1],
                             t1(A[trig[1]]["reduction"]), A[trig[1]]["commitment"]),
           "2. Reductions from the recalculated 2014 base year against each commitment: " +
           "; ".join("%s %s per cent against %d" % (a, t1(A[a]["reduction"]), A[a]["commitment"]) for a in ORDER) + ".",
           "3. PM2.5 from residential wood combustion in tons, the 2014 base year then the 2025-26 season: " +
           "; ".join("%s %s and %s" % (a, t1(A[a]["pm14"]), t1(A[a]["pm26"])) for a in ORDER) + ".", "",
           "## 3. Step-by-Step Solution", "",
           "1. Counted the 2025-26 appliances: the registry's active devices, each area read on the 2020 boundary through "
           "the parcel crosswalk, each device type mapped to its SCC.",
           "2. Took wood burned per appliance from each area's survey respondents by class, face cords at a third of a "
           "cord, pickup loads at half, pellets in tons (bags of %d pounds), %s tons per cord, the 2023 PM2.5 factors." %
           (k["bag_lb"], k["tons_per_cord"]),
           "3. Rebuilt the 2014 base year on the plan's 2014 count: the completed changeouts (applications matched to an "
           "area by parcel or street address) at the survey's cords for their class and recorded heat status, the rest "
           "of each class at the class mean, the certified and pellet stoves at the survey's units installed by 2014.",
           "4. Took each area's reduction from the 2014 base year to 2025-26 and compared it with its commitment in Table "
           "4-1 of the contingency provisions; below the commitment triggers.",
           "5. Counted the registry's appliances in place in the 2014 season on the 2020 boundaries, a record closed on "
           "the day a record of the same kind and install year is registered at its address being the same appliance "
           "registered again; the items are appliances registered after the plan's extract and parcels that left an area "
           "in 2020.",
           "6. Built each county's remainder on the state tool: each 2020 block group's main-heat households from the "
           "2019-2023 release, times its housing units' share outside the areas (the assessors' 2010 block groups carried "
           "to 2020 through the relationship file), %s secondary households per main-heat household, the tool's shares "
           "and use." % k["tool_secondary"], "",
           "## 4. Deliverable Answers", "",
           "### contingency_determinations_2026_27.csv", ""]
    for i, a in enumerate(ORDER, 1):
        x = A[a]
        out.append("%d. %s: 2014 base year %s tons, 2025-26 %s tons, reduction %s per cent against %d, %s." %
                   (i, a, t1(x["pm14"]), t1(x["pm26"]), t1(x["reduction"]), x["commitment"], x["determination"]))
    out += ["", "### rwc_periodic_inventory_2025_26.xlsx", "",
            "1. The 2014 base year's PM2.5 by area and SCC, tons:"]
    for a in ORDER:
        out.append("   - %s: " % a + "; ".join("%s %s" % (n, t1(f["cells"]["%s.%s" % (a, s)]["pm14"])) for s, n in SCC))
    out.append("2. The registry's appliances in place in the 2014 season, by area and SCC (2020 boundaries, each "
               "appliance once):")
    for a in ORDER:
        out.append("   - %s: " % a + "; ".join("%s %d" % (n, f["ask_a"]["%s.%s" % (a, s)]["registry"]) for s, n in SCC))
    out.append("3. Each county's remainder outside the maintenance areas, 2025-26 PM2.5 by SCC, tons:")
    for c in ("Selwick", "Corrin", "Tamsey"):
        out.append("   - %s: " % c + "; ".join("%s %s" % (n, t1(f["ask_b"]["%s.%s" % (c, s)]["pm"])) for s, n in SCC))
    open(os.path.join(TASK, "submission.md"), "w").write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
