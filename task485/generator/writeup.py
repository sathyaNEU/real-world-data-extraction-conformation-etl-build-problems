"""submission.md from generator/figures.json: the five blocks, every figure taken from the generator's own output."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven"}


def joined(xs):
    xs = list(xs)
    return ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else xs[0]


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    order = f["constants"]["order"]
    des, nod = f["call"]["designated"], f["call"]["not_designated"]
    R = f["regions"]
    dflt = f["default"]["designated"]
    added = [r for r in order if r in dflt and r not in des]
    missed = [r for r in order if r in des and r not in dflt]
    kg = lambda r: R[r]["kg_ha"]
    c = f["components"]
    out = ["## Tags", "",
           "**Domain:** Physical & Environmental Sciences, emissions inventory (a national agriculture department's "
           "regional inventory of ammonia from cattle manure for the 2025-26 programme year, conformed from the bovine "
           "register's animal and movement exports, its herd register, the June census by farm, the land parcel "
           "register's farmed area and the environmental protection office's Tier 2 factors).",
           "**Analytical objective:** Data Extraction & Conformation (ETL).", "",
           "## 1. Final Recommendation", "",
           "**The Minister should designate %s as Ammonia Action Regions for the 2027 spreading season: on the ammonia "
           "from cattle manure arising in each region over 2025-26 these %s regions are at or above 26 kilograms a "
           "hectare of farmed land, and the other %s are under it.**" % (joined(des), WORDS[len(des)], WORDS[len(nod)]),
           "%s stand at %s kilograms a hectare. Not %s, at %s: the cattle on their holdings on 1 June include lowland "
           "yearlings out on summer grazing and calves bought in that spring, whose housed months fall in other regions, "
           "so the census at the annual factor per head puts them over the line. Not without %s, at %s: their finishers "
           "house stores all winter and send them to slaughter before June, which the census misses." % (
               joined(des), joined(kg(r) for r in des), joined(added), joined(kg(r) for r in added),
               joined(missed), joined(kg(r) for r in missed)), "",
           "## 2. Critical Components", "",
           "1. Ammonia from cattle manure arising in the twelve regions, 1 November 2025 to 31 October 2026: **%s "
           "tonnes**." % c["tonnes_total"],
           "2. Farmed land of the twelve regions in the 2026 land parcel register, commonage at each herd's share: "
           "**%s hectares**." % c["land_total"], "",
           "## 3. Step-by-Step Solution", "",
           "1. Rebuilt each animal's days in nbr_animals_2025-26.csv and nbr_movements_2025-26.csv, from its date of birth "
           "or 1 November 2025 to the day before its exit date or 31 October 2026, in HERD_AT_START and then in each "
           "destination herd from its arrival date (nbr_export_notes.txt): %s animal-days." % c["animal_days"],
           "2. Put each herd number in the 2024 region of its district in nbr_herd_register_2026-11.xlsx, a reissued number "
           "at the record valid on the day (designation rules, section 4).",
           "3. Classed each day by epo_cattle_ammonia_factors_2025.pdf (section 2 and the annex's dairy breeds) and charged "
           "Table 3's housed rate on days inside the Table 4 housing season of the region the animal was in that day and "
           "its grass rate on the others: %s tonnes of ammonia." % c["tonnes_total"],
           "4. Divided each region's ammonia by its farmed land in lpr_farmed_area_2026.csv by the herds' regions, a "
           "commonage parcel at the herd's SHARE_PCT: %s hectares." % c["land_total"],
           "5. Tested each region against 26 kilograms a hectare on the unrounded figures (designation rules, section 5): "
           "%s regions at or above it." % WORDS[len(des)],
           "6. For the contractors, took cattle slurry jobs dated 13 January to 30 April 2026 on herds in the herd register "
           "from vale_agri_jobs_2026.csv (loads times the tanker's gallons), countrywide_invoice_lines_2026.xlsx (SS- "
           "services, thousands of gallons) and basin_agri_job_sheets_2026.xlsx (metered cubic metres), at 0.00454609 "
           "cubic metres a gallon, and counted each job once: a Countrywide line whose Reference is a Vale Agri Job No or a "
           "Basin Agri Job No bills that contractor's job, so it is left out and the job sheet's volume and spreader are "
           "kept; trailing shoe, trailing hose, dribble bar, umbilical dribble bar and shallow injection are low-emission "
           "(designation rules, section 6): %s cubic metres, %s per cent low-emission." % (
               f["ask_a_total"]["m3"], f["ask_a_total"]["less_pct"]),
           "7. The Minister designates the %s regions at or above the line." % WORDS[len(des)],
           "", "## 4. Deliverable Answers", "",
           "### ammonia_action_regions_2027.xlsx", "",
           "1. Ammonia from cattle manure arising in each region over 2025-26, tonnes, kilograms a hectare of farmed land, "
           "and whether designated:"]
    for r in order:
        out.append("   - %s: %s tonnes, %s kg a hectare, %s" % (r, R[r]["tonnes"], R[r]["kg_ha"],
                                                                 "designated" if R[r]["designated"] == "Yes" else "not designated"))
    out.append("2. Cattle slurry spread by contractors on each region's farms from 13 January to 30 April 2026, cubic "
               "metres to the nearest hundred, and the share spread by trailing shoe, trailing hose or injection, per cent:")
    for r in order:
        out.append("   - %s: %s cubic metres, %s per cent" % (r, f["ask_a"][r]["m3"], f["ask_a"][r]["less_pct"]))
    out += ["", "### cattle_ammonia_per_hectare_2025-26.png", "",
            "1. Horizontal bar chart of each region's kilograms of ammonia a hectare against the 26 kilogram line, the %s "
            "designated regions (%s) in orange beyond the line and the other %s in grey under it." % (
                WORDS[len(des)], joined(des), WORDS[len(nod)])]
    with open(os.path.join(TASK, "submission.md"), "w") as fh:
        fh.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
