"""Write task461/submission.md from generator/figures.json: every figure in it is emitted, never typed."""
import json

import world as W

LONG = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
        "December"]


def n0(v):
    return "{:,}".format(int(v))


def write(fig_path, out):
    F = json.load(open(fig_path))
    c, comp, k = F["call"], F["components"], F["constants"]
    L = ["## Tags\n",
         "**Domain:** Physical & Environmental Sciences (emissions inventory: an office tower's base building Scope 2 "
         "intensity and its Scope 1 lines for a sustainability-linked loan).",
         "**Analytical objective:** Data Extraction & Conformation (ETL).\n",
         "## 1. Final Recommendation\n",
         "**Report to %s that Pellow House's base building missed its 2026 target: %.1f kg CO2e per square metre "
         "against %.1f, %.1f kg over.**" % (W.BANK, c["kpi_kg_m2"], c["target_kg_m2"], c["margin_kg_m2"]),
         "The base building used %s MWh in 2026: the import less the nine tenancy supplies, with the three comms rooms "
         "metered inside their occupiers' supplies counted once. Not every tenancy meter in the register subtracted, "
         "which takes those rooms out twice and files %.1f, inside the target; not every meter named a comms, server or "
         "equipment room left out, which leaves the roof licensee's own supply in the base building and files %.1f.\n"
         % (n0(comp["base_building_mwh"]), F["rungs_kpi_kg_m2"]["all"], F["rungs_kpi_kg_m2"]["names"]),
         "## 2. Critical Components\n",
         "1. The base building used **%s MWh** of electricity in 2026 (import %s MWh less tenancy supplies %s MWh)."
         % (n0(comp["base_building_mwh"]), n0(comp["import_mwh"]), n0(comp["tenancy_supplies_mwh"])),
         "2. EM-102, EM-105 and EM-108 sit inside EM-101, EM-104 and EM-107: **%s MWh** that subtracting every listed "
         "meter takes out a second time." % n0(comp["nested_rooms_mwh"]),
         "3. Base building Scope 2 emissions are **%.1f t CO2e**, a KPI of **%.1f kg CO2e per m2**."
         % (comp["scope2_t"], c["kpi_kg_m2"]),
         "",
         "## 3. Step-by-Step Solution\n",
         "1. Summed %s by settlement date into calendar months on the building's clock: the import was %s MWh."
         % (W.FILES["hh"], n0(comp["import_mwh"])),
         "2. Read every tenancy meter in %s from %s at each month's local midnight (watt-hour registers divided by "
         "1,000, EM-110 to its removal and EM-118 after it)." % (W.FILES["register"], W.FILES["bms"]),
         "3. Compared the meters' half-hourly increments: EM-102, EM-105 and EM-108 never exceed EM-101, EM-104 and "
         "EM-107 and fell to zero exactly when those supplies were isolated in the June switchboard maintenance, so "
         "they sit inside them; EM-114 stayed live through every tenancy isolation and is a supply of its own.",
         "4. Took the nine supplies (EM-101, EM-103, EM-104, EM-106, EM-107, EM-109, EM-110 with EM-118, EM-112, EM-114) "
         "from the import month by month, as %s defines Base Building Electricity: %s MWh for the year." % (W.FILES["schedule"],
                                                                         n0(comp["base_building_mwh"])),
         "5. Applied parts 2 and 3 of the schedule: %s kg CO2e per kWh gives %.1f t, over %s square metres %.1f kg "
         "CO2e per m2, %.1f over the %.1f target." % (k["factor_kg_per_kwh"], comp["scope2_t"], n0(k["nla_m2"]),
                                                      c["kpi_kg_m2"], c["margin_kg_m2"], c["target_kg_m2"]),
         "6. Gas oil: converted each dip in %s through %s, placed each week's burn on that week's runs in %s to "
         "get the stock at each quarter's local midnight, and added %s: litres by quarter below, at %s kg CO2e per "
         "litre." % (W.FILES["dips"], W.FILES["calib"], W.FILES["runs"], W.FILES["dockets"], k["diesel_kg_per_l"]),
         "7. Refrigerant: each chiller's additions in %s less the kilograms %s recovered to cylinders on the same job: "
         "kilograms by chiller below, at a GWP of %s.\n" % (W.FILES["fgas"], W.FILES["recovery"], n0(k["gwp_r134a"])),
         "## 4. Deliverable Answers\n",
         "### %s\n" % W.GOLDEN["report"],
         "1. Base building electricity by month, MWh:"]
    for i, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]):
        L.append("   - %s: %s" % (LONG[i], n0(F["base_building_mwh_month"][m])))
    L += ["2. Base building electricity for 2026: %s MWh." % n0(comp["base_building_mwh"]),
          "3. Base building Scope 2 emissions: %.1f t CO2e." % comp["scope2_t"],
          "4. KPI: %.1f kg CO2e per m2 against the %.1f target: missed, by %.1f kg."
          % (c["kpi_kg_m2"], c["target_kg_m2"], c["margin_kg_m2"]),
          "5. Standby generator gas oil burned, litres and kg CO2e:"]
    for q in ("Q1", "Q2", "Q3", "Q4"):
        L.append("   - %s: %s litres, %s kg CO2e" % (q, n0(F["diesel_l"][q]), n0(F["diesel_kg_co2e"][q])))
    L.append("6. Refrigerant released, kg and kg CO2e:")
    for ch in sorted(F["refrigerant_kg"]):
        L.append("   - %s: %.1f kg, %s kg CO2e" % (ch, F["refrigerant_kg"][ch], n0(F["refrigerant_kg_co2e"][ch])))
    L += ["", "### %s\n" % W.GOLDEN["letter"],
          "1. Result stated against the target: %.1f kg CO2e per m2 against %.1f, missed by %.1f kg, with the base "
          "building's %s MWh and %.1f t CO2e." % (c["kpi_kg_m2"], c["target_kg_m2"], c["margin_kg_m2"],
                                                   n0(comp["base_building_mwh"]), comp["scope2_t"]),
          "2. Chart: the base building's electricity in each month of 2026 as bars, each labelled in MWh."]
    with open(out, "w") as f:
        f.write("\n".join(L) + "\n")
