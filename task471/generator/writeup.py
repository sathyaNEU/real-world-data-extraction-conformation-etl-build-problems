"""submission.md from generator/figures.json: tags, the final recommendation, the critical components, the steps and the
deliverable answers. Every number written comes from figures.json."""
import json

import world as W


def _n(v):
    return "{:,}".format(int(v))


def _names(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def _r2(v):
    return "%.2f" % v


def write(fig_path, out_path):
    fig = json.load(open(fig_path, encoding="utf-8"))
    call = fig["call"]["organisers"]
    dflt = fig["default"]["organisers"]
    changed = fig["default"]["changed"]
    nat = fig["national"]
    young = [fig["groups"][W.group_label(g)] for g in W.YOUNG_GROUPS]
    asks = fig["asks"]
    pct = fig["factors_pct"]
    out = []
    out.append("## Tags\n")
    out.append("**Domain:** Survey Research & Official Statistics (census, register and administrative data quality: each "
               "region's adults on census day estimated from the 2025 Census and its Post-Enumeration Survey by "
               "dual-system estimation within the survey's cells, the men aged 18 to 49 brought to the sex ratio that "
               "demographic analysis of births, deaths and long-term movements gives, and conformed with the roll at "
               "census day and the roll's transaction log into the Commission's enrolment-gap file).  ")
    out.append("**Analytical objective:** Data Extraction & Conformation (ETL).\n")
    out.append("## 1. Final Recommendation\n")
    out.append("**%s of the %d organisers.**" % (_names("%s %d" % (W.NAME[c], call[W.NAME[c]]) for c in W.CODES),
                                                 fig["call"]["total"]))
    out.append("Each region's share is its adults usually resident on census day less its electors with a residential "
               "address, the adults estimated by dual-system estimation within the survey's cells with the men aged 18 "
               "to 49 raised to the sex ratio demographic analysis gives, because the census and its survey miss the "
               "same young men and leave the men's estimates about %d per cent short of it while the women's agree. Not "
               "the dual-system estimates as they stand, which give %s; not the census counts, which leave out everyone "
               "the census missed and change %d regions.\n" % (
                   fig["young_men"]["short_pct"], _names("%s %d" % (n, dflt[n]) for n in changed),
                   fig["census_only"]["n_changed"]))
    out.append("## 2. Critical Components\n")
    out.append("1. Electors on the roll at the close of census day with a residential address: **%s**." % _n(
        nat["electors"]))
    out.append("2. Adults on census day by dual-system estimation within the survey's region, sex and age-group cells: "
               "**%s**." % _n(nat["dse_adults"]))
    out.append("3. Men per woman aged 18 to 24, 25 to 34 and 35 to 49: dual-system estimates **%s**; demographic analysis "
               "**%s**." % (_names(_r2(g["ratio_dse"]) for g in young), _names(_r2(g["ratio_da"]) for g in young)))
    out.append("4. Dual-system estimates of men aged 18 to 49 against demographic analysis: about **%d per cent** short, "
               "the women's agreeing with it." % fig["young_men"]["short_pct"])
    out.append("5. Adults on census day after the correction: about **%s million**.\n" % _r2(nat["golden_adults_million"]))
    out.append("## 3. Step-by-Step Solution\n")
    steps = [
        "Took the electors with a residential address (ADDRESS_TYPE R) in roll_at_close_of_census_day_2025.csv to "
        "regions through electorates_and_regions.csv (plan 2.2): %s." % _n(nat["electors"]),
        "In each estimation cell of pes_2025_methods_report.pdf (region by sex by age group) took the count in "
        "census_2025_usual_residents_by_region.xlsx less its imputed records, kept the share of the cell's records in "
        "pes_2025_census_records.csv with STATUS C and raised that by the cell's people in pes_2025_people.csv over "
        "those with MATCH M: dual-system estimates of %s adults." % _n(nat["dse_adults"]),
        "Rebuilt the population on census day by sex and single year of age, cohort by cohort, from "
        "live_births_by_sex_1925_2025.csv less deaths (deaths_by_year_of_birth_1925_1990.xlsx and "
        "deaths_by_year_of_birth_1991_2025.csv) and departures plus arrivals "
        "(long_term_movements_by_year_of_birth_1950_2025.csv), the period 2025-01-01/2025-03-03 included: men per "
        "woman of %s at 18 to 24, 25 to 34 and 35 to 49, against the dual-system estimates' %s, the women's estimates "
        "agreeing with it." % (_names(_r2(g["ratio_da"]) for g in young), _names(_r2(g["ratio_dse"]) for g in young)),
        "Multiplied every region's dual-system estimates of men in each of those age groups by demographic analysis's "
        "men per woman over the dual-system estimates' (about %s per cent more men), the women and the other ages as "
        "estimated: about %s million adults." % (_names(str(p) for p in pct), _r2(nat["golden_adults_million"])),
        "Subtracted each region's electors and shared the %d organisers on the differences by largest remainders "
        "(plan 3.1; no share falls under two): the organisers above." % fig["call"]["total"],
        "New electors: in roll_transactions_2025_2026.csv read PROCESSED in each platform's time basis "
        "(roll_extract_data_dictionary.xlsx) and the old platform's (R25-) electorate numbers as the 2020 review's, "
        "placed through NUMBER_BEFORE_2024_REVIEW in electorates_and_regions.csv (a reinstatement of an old-platform "
        "removal restores the same region only under those numbers); took a person as every PERSON_REF that REF_TXN ties "
        "together (an old-platform move is an enrolment at the new address and a removal of the old record pointing back "
        "at it, under two references); kept the accepted transactions from 5 March 2025 to 30 June 2026 in the country's "
        "time and counted each person once at the residential address of their first enrolment, leaving out anyone a "
        "removal in the window shows on the roll on census day (it takes off a record no enrolment in the window made): "
        "%s." % _n(asks["new_total"]),
        "Removed because they had died: the accepted DEL rows in the same window with reason 01 on the old platform "
        "(deceased, roll_platform_migration_notes.pdf) or 11 or 12 on the new (roll_extract_data_dictionary.xlsx), in "
        "the region of their electorate read the same way, less those a later accepted transaction reverses through "
        "REF_TXN (a reinstatement, or on the old platform an enrolment putting right a removal made in error): %s."
        % _n(asks["died_total"]),
        "Wrote enrolment_gap_allocation_2027.csv in the layout of enrolment_gap_file_specification.xlsx and "
        "enrolment_gap_allocation_2027.png, a bar chart of each region's organisers.",
    ]
    for i, s in enumerate(steps, 1):
        out.append("%d. %s" % (i, s))
    out.append("")
    out.append("## 4. Deliverable Answers\n")
    out.append("### enrolment_gap_allocation_2027.csv\n")
    out.append("1. Each region's organisers and, between census day and 30 June 2026, the people added to the roll there "
               "who had not been on it on census day and the electors removed from it there because they had died, "
               "whole numbers:")
    for r in fig["regions"]:
        out.append("   - %s (%s): %d organisers, %s added, %s removed because they had died" % (
            r["name"], r["code"], r["organisers"], _n(r["new_electors"]), _n(r["removed_died"])))
    out.append("")
    out.append("### enrolment_gap_allocation_2027.png\n")
    out.append("1. Bar chart of the 16 regions' organisers in region code order, each bar labelled with its count.")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out).rstrip() + "\n")


if __name__ == "__main__":
    import os
    import sys
    here = os.path.dirname(os.path.abspath(__file__))
    write(os.path.join(here, "figures.json"), os.path.join(os.path.dirname(here), "submission.md"))
    sys.exit(0)
