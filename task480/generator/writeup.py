"""Write submission.md from generator/figures.json: every figure in it is one the generator computed."""
import json

import world as W

ORDER = [m[1] for m in sorted(W.MUNIS, key=lambda m: (m[2] != "city", m[2] != "village", m[1]))]


def c(v):
    return "{:,}".format(int(v))


def write(figs, out):
    f = json.load(open(figs))
    cr, mf = "Town of Cedar Run", "Town of Maple Ford"
    lo, hi = f["family_min_r10"], f["family_max_r10"]
    place = f["rungs"]["place"]
    tier = f["call"]
    no = [n for n in ORDER if n not in tier]
    L = []
    L.append("# task480 submission\n")
    L.append("## Tags\n")
    L.append("**Domain:** Survey Research & Official Statistics, census, register and administrative data quality (a state "
             "data center's 1 July 2026 municipal population estimates by the housing unit method, which set the "
             "municipalities in the road aid formula's urban tier for 2027).")
    L.append("**Analytical objective:** Data Extraction & Conformation (ETL) (the assessor's roll, the certificates of "
             "occupancy and demolition permits, the 2020 census block groups, the census history and the boundary "
             "register, the group quarters survey and the State Registrar's resident birth and death files conformed into "
             "each municipality's residents on 1 July 2026, births and deaths).\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**Three municipalities reach 10,000 residents on 1 July 2026 and move into the urban tier for the 2027 aid "
             "year: the City of Juniper, the City of Dunmore and the Town of Cedar Run.**\n")
    est = f["estimate"]
    L.append("Each dwelling standing on 1 July 2026 carries the persons the 2020 block groups show for dwellings of its "
             "type and age, and the group quarters add the 2026 survey's residents: on the eight-band profile the Town of "
             "Cedar Run holds %s residents and the Town of Maple Ford %s, and every other age profile (bands of three to "
             "ten years, with or without an age profile of its own for each type of dwelling, or a fitted curve) puts "
             "Cedar Run over the line and Maple Ford under it. Not Maple Ford in place of Cedar Run, which each "
             "municipality's 2020 persons per dwelling gives (Maple Ford %s, Cedar Run %s): a dwelling holds fewer people "
             "as it ages, so the 2020 average overstates Maple Ford's subdivisions of 1997 to 2015 and understates Cedar "
             "Run's homes built since 2019."
             % (c(est[cr]), c(est[mf]), c(place[mf]), c(place[cr])))
    L.append("")
    L.append("## 2. Critical Components\n")
    L.append("1. On the eight-band age profile of step 2 the Town of Cedar Run's 1 July 2026 estimate is **%s** residents, "
             "over 10,000, and the Town of Maple Ford's **%s**, under it; every other age profile puts the two on the "
             "same sides of the line." % (c(est[cr]), c(est[mf])))
    L.append("2. Applied to the dwellings standing at the 2010 and 2000 censuses, by the municipalities they stood in then, "
             "the age profile reproduces each municipality's household population more closely than its 2020 persons per "
             "dwelling does, and far more closely than persons per dwelling by year built; the 2020 persons per dwelling "
             "holds Maple Ford at **%s** and Cedar Run at **%s** for July 2026." % (c(place[mf]), c(place[cr])))
    L.append("")
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Built the dwelling stock from %s (living units by parcel: a two-family house or an apartment building one "
             "parcel, a townhouse unit its own), the certificates of occupancy in %s (each building once, at its first "
             "certificate, temporary or final; the dwellings certified in 2026 on lots the roll holds as vacant land "
             "added) and the completed permits in %s (expired permits left standing), each dwelling dated by its first "
             "certificate where it has one and otherwise at mid-year of its year built (the assessor's placeholder 0 "
             "taken as 1900), and typed in four by the roll's land use (1010 single-family; 1020 two-family and 1030 "
             "condominium unit, attached; 1050 apartments; 1080 manufactured homes; a certificate's use the same way)."
             % (W.FILES["roll"], W.FILES["cos"], W.FILES["demo"]))
    L.append("2. Placed each dwelling standing on 1 April 2020 in its 2020 block group (the first twelve digits of "
             "CENSUS_BLOCK_2020) and regressed each block group's household population (P15_001N in %s), by ordinary "
             "least squares without an intercept, on its dwellings of each of the four types and its dwellings by age "
             "in bands (0 to 5, 5 to 10, 10 to 15, 15 to 20, 20 to 30, 30 to 40, 40 to 60, 60 years and over, the last "
             "the base), giving persons per dwelling by type and age." % W.FILES["bg2020"])
    L.append("3. Checked the profile out of sample: on the dwellings standing at each earlier census, by the municipality "
             "they stood in then (%s: the annexations by tax key, the Towns and the Village of Ivydale together), it "
             "reproduces the household population in %s (step 2 of the critical components); the 2020 persons per "
             "dwelling and persons per dwelling by year built do not." % (W.FILES["boundary"], W.FILES["history"]))
    L.append("4. Applied the profile to every dwelling standing on 1 July 2026 at its age that day, by the municipality on "
             "the 2026 roll, and added the residents %s records for each municipality's facilities." % W.FILES["gq"])
    L.append("5. Compared each estimate with 10,000 unrounded (Municipal Road Aid Act, s. 84.21 (6)): Juniper, Dunmore and "
             "Cedar Run reach it, every other municipality falls short.")
    L.append("6. Births: kept the records in %s with a date of birth from 1 July 2025 to 30 June 2026 (each infant one "
             "record) and placed each in the municipality (MCD) of the address point in %s with the same house number, "
             "street and suffix as the residence; RES_CITY is the post office's city (the address points' POSTAL_CITY), "
             "not the municipality." % (W.FILES["births"], W.FILES["points"]))
    L.append("7. Deaths: the same for %s by date of death, a group quarters resident at the facility's address; "
             "RES_MCD_CODE follows the written city on deaths before 1 January 2026 and the address after."
             % W.FILES["deaths"])
    L.append("8. Recommendation: the City of Juniper, the City of Dunmore and the Town of Cedar Run are in the urban tier "
             "for 2027.")
    L.append("")
    L.append("## 4. Deliverable Answers\n")
    L.append("### tamarack_municipal_estimates_2026.xlsx\n")
    L.append("1. Whether each municipality is in the urban tier for the 2027 aid year:")
    L.append("   - In: %s" % ", ".join(n for n in ORDER if n in tier))
    L.append("   - Out: %s" % ", ".join(no))
    L.append("2. Each municipality's resident births from 1 July 2025 to 30 June 2026, as whole counts, in the workbook's "
             "order:")
    for n in ORDER:
        L.append("   - %s: %s" % (n, c(f["births"][n])))
    L.append("3. Each municipality's resident deaths from 1 July 2025 to 30 June 2026, as whole counts, in the workbook's "
             "order:")
    for n in ORDER:
        L.append("   - %s: %s" % (n, c(f["deaths"][n])))
    L.append("")
    L.append("### urban_tier_estimates_2026.svg\n")
    L.append("4. Bar chart of each municipality's estimated residents on 1 July 2026 against the 10,000 line.")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
