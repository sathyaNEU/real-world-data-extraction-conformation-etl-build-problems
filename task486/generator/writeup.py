"""submission.md from generator/figures.json: the five blocks, every figure taken from the generator's own output."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
DISTRICTS = ["Rookgate", "Dorrstead", "Glenskarn", "Ingmouth", "Neshdale", "Skelrigg"]


def c(n):
    return format(n, ",")


def joined(xs):
    return ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else xs[0]


def signed(p):
    return "%+d per cent" % p if p else "0 per cent"


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    sch, comp, asks, lad = f["schedule"], f["components"], f["asks"], f["ladder"]
    q = f["call"]["qualifying"]
    st = f["stated"]
    area = lad["area"]
    out = ["## Tags", "",
           "**Domain:** Survey Research & Official Statistics, census, register and administrative data quality (an "
           "island statistics office's workplace retail employment for 31 designated town centres in March 2022 and "
           "March 2026, conformed from the tax authority's PAYE returns in two layouts, the 2017 and 2023 rating lists, "
           "six district councils' business rates accounts in six layouts and the companies register).",
           "**Analytical objective:** Data Extraction & Conformation (ETL).", "",
           "## 1. Final Recommendation", "",
           "**%d of Torvasay's 31 designated town centres meet the 2027 Town Centre Renewal Fund's test: %s.**" % (
               len(q), joined(q)),
           "Once each multi-site employer's PAYE staff are placed at its premises by floor area times the staff per square "
           "metre its premises' description holds among single-site employers, the smallest fall among them between March "
           "2022 and March 2026 is %.1f per cent and the largest among the other centres %.1f per cent. Not the %d centres "
           "a share by floor area names (adding %s%s): the chains' new retail park units and warehouses hold far fewer "
           "staff per square metre than their shops. Not the scheme postcodes, which put the chains' staff at their head "
           "offices and agents." % (
               st["smallest_qualifying_fall"], st["largest_other_fall"], area["n"], joined(area["added"]),
               (" and dropping " + joined(area["dropped"])) if area["dropped"] else ""), "",
           "## 2. Critical Components", "",
           "1. Retail employers in the PAYE returns: **%s** in March 2022 and **%s** in March 2026, of which **%d** in each "
           "March occupied more than one premises, employing **%s** and **%s**." % (
               c(comp["retail_employers_2022"]), c(comp["retail_employers_2026"]), comp["multi_site_employers_2022"],
               c(comp["multi_site_employees_2022"]), c(comp["multi_site_employees_2026"])),
           "2. Workplace retail employment in the 31 centres together: about **%s** in March 2022 and **%s** in March "
           "2026, to the nearest thousand." % (c(comp["centres_total_2022_thousands"] * 1000),
                                              c(comp["centres_total_2026_thousands"] * 1000)),
           "3. Centres whose workplace retail employment fell by 8 per cent or more: **%d**." % len(q), "",
           "## 3. Step-by-Step Solution", "",
           "1. Conformed paye_returns_m12_2021-22.csv (layout 3) and paye_returns_m12_2025-26.csv (layout 4) into one table "
           "of schemes, kept SIC 2007 division 47 and added up each company's schemes: %s retail employers in March 2022 "
           "and %s in March 2026." % (c(comp["retail_employers_2022"]), c(comp["retail_employers_2026"])),
           "2. Resolved each sheet of business_rates_accounts_2017-2026.xlsx to UARNs through the two rating list "
           "extracts and matched each account liable on 31 March to its employer by company number, else by registered or "
           "previous name in companies_register_extract_20260501.csv, else by initials and surname; a letting company held "
           "by a retail employer's parent holds that employer's premises.",
           "3. Took each premises' description and floor area from the list entry in force on that 31 March "
           "(rating_list_2017_extract_20220404.csv for 2022, rating_list_2023_extract_20260413.csv for 2026): %d retail "
           "employers occupied more than one premises in each March, employing %s and %s." % (
               comp["multi_site_employers_2022"], c(comp["multi_site_employees_2022"]), c(comp["multi_site_employees_2026"])),
           "4. Measured each description's staff per square metre as the single-site retail employers' total employees "
           "over their total floor area, March by March.",
           "5. Placed each multi-site employer's employees at its premises in proportion to floor area times its "
           "description's staff per square metre, and summed the employees at premises whose list postcode is in each "
           "centre's rows of town_centre_schedule_2026.csv, terminated codes included: about %s in March 2022 and %s in "
           "March 2026." % (c(comp["centres_total_2022_thousands"] * 1000), c(comp["centres_total_2026_thousands"] * 1000)),
           "6. Applied the prospectus's 3.3 to the unrounded figures: %d centres fell by 8 per cent or more." % len(q),
           "7. Counted, in each district's centres, the shop premises in force on each 31 March whose account that day was "
           "an owner's, one on empty property relief or in the name of a company the register classes %s (letting its own "
           "real estate) or %s (developing building projects), a premises with no account being in occupation as the "
           "accounts' contents note says, and dated each empty spell from the first of the consecutive owners' accounts "
           "on its UARN: %s empty at 31 March 2022 (%s of them for twelve months or more) and %s at 31 March 2026 (%s)." % (
               f["stated"]["owner_class_letting"], f["stated"]["owner_class_development"],
               c(sum(asks["ask_a"][d]["2022"] for d in DISTRICTS)), c(sum(asks["ask_b"][d]["2022"] for d in DISTRICTS)),
               c(sum(asks["ask_a"][d]["2026"] for d in DISTRICTS)), c(sum(asks["ask_b"][d]["2026"] for d in DISTRICTS))),
           "8. The 2027 fund's eligible centres are the %d that fell by 8 per cent or more: %s." % (len(q), joined(q)), "",
           "## 4. Deliverable Answers", "",
           "### town_centre_fund_2027_eligibility.xlsx", "",
           "1. Workplace retail employment by centre, nearest 50, and its change, whole per cent (sheet Eligibility "
           "schedule, in the schedule's order):"]
    for r in sch:
        out.append("   - %s %s: %s in March 2022, %s in March 2026, %s, %s" % (
            r["code"], r["centre"], c(r["employment_2022"]), c(r["employment_2026"]), signed(r["change_pct"]),
            "meets the test" if r["qualifies"] == "Yes" else "does not meet the test"))
    out.append("2. Shop premises in each district's designated centres empty at each 31 March, and of those the ones empty "
               "for twelve months or more (sheet Vacancy annex):")
    for d in DISTRICTS:
        out.append("   - %s: %d at 31 March 2022, %d of them for twelve months or more; %d at 31 March 2026, %d of them for "
                   "twelve months or more" % (d, asks["ask_a"][d]["2022"], asks["ask_b"][d]["2022"], asks["ask_a"][d]["2026"],
                                              asks["ask_b"][d]["2026"]))
    out += ["", "### town_centre_retail_employment_2022_2026.png", "",
            "1. Horizontal bar chart of every centre's change from March 2022 to March 2026, sorted, with the 8 per cent "
            "line labelled, the %d qualifying centres in blue and each bar labelled with its change; the title states that "
            "%d of the 31 centres lost 8 per cent or more." % (len(q), len(q)), ""]
    text = "\n".join(out)
    assert "\u2014" not in text and "\u2013" not in text
    open(os.path.join(TASK, "submission.md"), "w").write(text)


if __name__ == "__main__":
    main()
