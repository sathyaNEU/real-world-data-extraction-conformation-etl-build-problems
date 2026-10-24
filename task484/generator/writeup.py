"""submission.md from generator/figures.json: the five blocks, every figure taken from the generator's own output."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
SCC = [("2104008310", "Freestanding woodstoves, not EPA certified"),
       ("2104008320", "Freestanding woodstoves, EPA certified, non-catalytic"),
       ("2104008330", "Freestanding woodstoves, EPA certified, catalytic"), ("2104008400", "Pellet stoves"),
       ("2104008100", "Fireplaces"), ("2104008610", "Outdoor hydronic heaters")]


def c(n):
    return format(n, ",")


def num(x):
    return ("%.1f" % x).rstrip("0").rstrip(".") if isinstance(x, float) else str(x)


def joined(xs):
    return ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else xs[0]


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    Z = f["zones"]
    zones = f["order"]
    over = f["call"]["over"]
    under = [z for z in zones if z not in over]
    k, s = f["constants"], f["steps"]
    eb, wb = Z["East Bench"], Z["West Bench"]
    out = ["## Tags", "",
           "**Domain:** Physical & Environmental Sciences, emissions inventory (a county air quality program's "
           "2025-26 residential wood combustion inventory for a PM2.5 maintenance area's five burn zones, conformed "
           "from its device registry, its 2024-25 household survey, three propane distributors' delivery exports in "
           "three layouts, the airport station's temperatures, the state tool and Census block-group files).",
           "**Analytical objective:** Data Extraction & Conformation (ETL).", "",
           "## 1. Final Recommendation", "",
           "**%s exceeded their 2025-26 allotments and share the 2026-27 changeout fund, USD %s each; %s did not.**" % (
               joined(over), c(f["call"]["share"]), joined(under)),
           "In every zone the propane homes with a heating appliance took %d to %d per cent less propane in 2025-26 "
           "while those without one took what they took in 2024-25, and the wood burned in its place puts the East Bench "
           "at %d tons against %s and the West Bench at %d against %s. Not %s alone: carrying the 2024-25 survey's wood "
           "per appliance into 2025-26 leaves the benches at %d and %d tons, under their allotments." % (
               s["drop_lo"], s["drop_hi"], eb["pm"], num(eb["allot"]), wb["pm"], num(wb["allot"]), over[0],
               eb["default_pm"], wb["default_pm"]), "",
           "## 2. Critical Components", "",
           "1. 2025-26 PM2.5 from residential wood combustion: %s." % "; ".join(
               "%s **%d tons** (allotment %s)" % (z, Z[z]["pm"], num(Z[z]["allot"])) for z in zones),
           "2. PM2.5 from the wood burned in place of propane: %s." % "; ".join(
               "%s **%d tons**" % (z, Z[z]["extra_pm"]) for z in zones), "",
           "## 3. Step-by-Step Solution", "",
           "1. Counted the registry's devices in use in 2025-26 (installed before 1 October 2025, not removed) by burn "
           "zone and device code, %s appliances, and took each zone's wood per appliance by class from the 2024-25 "
           "survey responses as its methods note estimates it (face cords at a third of a cord, pickup loads at half, "
           "%d-pound bags)." % (c(s["appliances"]), k["bag_lb"]),
           "2. Matched every residential propane account in the Wapiti, Coldwater and cooperative files to its parcel "
           "(the geocode, or the cooperative's service address against burn_zone_parcels_2025.csv) and to the registry, "
           "splitting each zone's propane homes into those with a heating appliance in use in 2024-25 and 2025-26 and "
           "those without one (the state tool gives a fireplace no heating efficiency).",
           "3. Summed each account's deliveries in each heating season (1 October to 30 April): the two groups moved "
           "alike from 2023-24 to 2024-25 (season ratios within %.2f of each other in every zone), and in 2025-26 the "
           "homes without a heating appliance took %.3f to %.3f times their 2024-25 gallons while the homes with one "
           "took %d to %d per cent less." % (s["pre_gap"], s["comp_lo"], s["comp_hi"], s["drop_lo"], s["drop_hi"]),
           "4. Took each home's 2024-25 gallons at its zone's ratio less its 2025-26 gallons as the propane its appliance "
           "replaced and burned that heat (%s Btu a gallon at %d per cent furnace efficiency, "
           "heating_fuel_equivalents.csv) at the appliance's seasonal efficiency, %s million Btu a cord and %s a ton "
           "of pellets: PM2.5 of %s." % (c(k["btu_gal"]), k["afue_pct"], num(k["cord_mmbtu"]), num(k["pellet_mmbtu"]),
                                        joined(["%d tons in %s" % (Z[z]["extra_pm"], z) for z in zones])),
           "5. Added that wood to the survey's wood per appliance times the appliances, at the 2023 factors: %s tons "
           "against Table 4-2's %s." % (joined([str(Z[z]["pm"]) for z in zones]),
                                        joined([num(Z[z]["allot"]) for z in zones])),
           "6. Summed each zone's commercial and institutional accounts' 2025-26 season deliveries by delivery date, "
           "reading Coldwater's from the ticket reference (its statement accounts' transactions post on the first of "
           "the following month), with NOx at %s lb/MMBtu." % ("%.3f" % k["nox"]),
           "7. Outside the maintenance area, took each 2020 block group's 2019-2023 ACS wood-heated households at its "
           "share of housing units outside the area, the assessor's 2010 block groups carried to 2020 through the "
           "relationship file (%s main-heat households), then the tool's %s secondary households for each, its shares "
           "and its use." % (c(k["main_out"]), num(k["secondary"])),
           "8. Split the USD %s fund equally among the %d zones over their allotments: USD %s each to %s." % (
               c(f["call"]["fund"]), len(over), c(f["call"]["share"]), joined(over)), "",
           "## 4. Deliverable Answers", "",
           "### rwc_inventory_2025_26.xlsx", "",
           "1. The 2025-26 inventory by burn zone and SCC on sheet RWC inventory, each zone's total carried to the "
           "determinations.",
           "2. Commercial and institutional propane delivered in the 2025-26 season (sheet Commercial propane):"]
    for z in zones:
        a = f["ask_a"][z]
        out.append("   - %s: %s gallons, %.2f tons of NOx" % (z, c(a["gal"]), a["nox"]))
    out.append("3. Halvard County outside the maintenance area on the state tool (sheet Outside the area):")
    for scc, name in SCC:
        b = f["ask_b"][scc]
        out.append("   - %s: %s appliances, %.1f tons of PM2.5" % (name, c(b["app"]), b["pm"]))
    out += ["", "### zone_determinations_2026_27.csv", "", "1. One row per burn zone:"]
    for z in zones:
        x = Z[z]
        out.append("   - %s: %d tons of PM2.5, %s, USD %s" % (z, x["pm"], "exceeded" if x["exceeded"] else "did not exceed",
                                                            c(x["share"])))
    with open(os.path.join(TASK, "submission.md"), "w") as fh:
        fh.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
