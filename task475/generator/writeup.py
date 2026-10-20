"""submission.md from generator/figures.json (written by golden.py from the pack): the five blocks, every figure
emitted, never typed."""
import json

ORDER = ["Tallis", "Hesketh", "Brenmoor", "Quarrow", "Varden", "Fennick", "Kerrow", "Stanwick", "Wexley", "Hollin",
         "Esker", "Ardley", "Silbury", "Ravell"]


def money(v):
    return "${:,}".format(v)


def write(fig_path, path):
    f = json.load(open(fig_path, encoding="utf-8"))
    c = f["components"]
    call = f["call"]
    top = f["components"]["largest_county"]
    cap = f["inputs"]["cap_dollars"]
    fam, sh, al = c["families"], c["shares_pct"], c["allocations"]
    a, b = f["a_dwellings"], f["b_spending"]
    av, rv = f["averages"], f["rivals"]
    out = []
    out.append("## Tags\n")
    out.append("**Domain:** Demographic & Social Science (income and poverty statistics from tax returns; Survey "
               "Research & Official Statistics, census, register and administrative data quality: the IRS ZIP code "
               "statistics conformed to the council's fourteen member counties, with each county's returns with "
               "qualifying children recovered from its credit returns and credit amount).")
    out.append("**Analytical objective:** Data Extraction & Conformation (ETL).\n")
    out.append("## 1. Final Recommendation\n")
    out.append("**The Corran Valley Council of Governments should split the $20,000,000 2027 weatherization fund in "
               "proportion to each member county's tax-year 2023 earned income credit returns with qualifying "
               "children, and no county reaches the 12 per cent cap.**")
    out.append("%s County has the largest share, %.2f per cent (%s), under the cap's %s. Not the statewide share of "
               "returns with children applied to every county's credit returns, which puts %s at %.2f per cent and "
               "caps it, because %s's credit returns in the lowest income class claim far less than that share "
               "implies: far more of its claimants are childless workers than the state's. Not every credit return, which puts it at "
               "%.2f per cent.\n" % (top, call["largest_share_pct"], money(call["largest_allocation"]),
                                    money(cap), top, rv["statewide_share_largest_pct"], top,
                                    rv["every_credit_return_largest_pct"]))
    out.append("## 2. Critical Components\n")
    out.append("1. %s County's tax-year 2023 credit returns with qualifying children: **%s**" % (
        top, "{:,.1f}".format(fam[top])))
    out.append("2. The fourteen counties' credit returns with qualifying children: **%s**" % "{:,.1f}".format(
        c["total_families"]))
    out.append("3. %s County's share: **%.2f per cent**, under the 12 per cent cap" % (top, sh[top]))
    out.append("4. %s County's allocation: **%s**\n" % (top, money(al[top])))
    out.append("## 3. Step-by-Step Solution\n")
    steps = [
        "Conformed irs_soi_zip_code_data_ty2023_extract.csv (the latest year the IRS has published, policy 3.1) to "
        "counties through the residential ratio of zip_county_relationship_2023q4.xlsx, the four P.O. Box ZIP codes "
        "by their total ratio, the 00000 and 99999 lines counted for no county (policy 4.1 and 4.2).",
        "From Table 2 of dor_individual_income_tax_statistics_ty2023.pdf took the statewide average credit of a "
        "childless return and of a return with qualifying children in the IRS's first income class (the "
        "Department's first three classes): $%s and $%s; in every higher class each credit return has a qualifying "
        "child."
        % ("{:,.2f}".format(av["childless"]), "{:,.2f}".format(av["with_children"])),
        "Split each ZIP code's first-class credit returns into returns with and without qualifying children so that "
        "the two averages reproduce its credit amount (A59660, thousands of dollars), added its credit returns in "
        "the higher classes, and summed by county: %s %s of %s." % (top, "{:,.1f}".format(fam[top]),
                                                         "{:,.1f}".format(c["total_families"])),
        "Shared the fund in proportion to the counts (policy 5.1): the largest share, %s's %.2f per cent, is under "
        "the 12 per cent cap (5.2), so nothing is redistributed; allocations rounded to the nearest hundred dollars "
        "(5.3), %s %s." % (top, sh[top], top, money(al[top])),
        "Ask A: took the units of the jobs in wx_job_export_2026-09-30.csv funded by DOE-WAP or STATE-WX whose first "
        "COMPLETED change in wx_job_status_history_2026-09-30.csv falls in 2025 (policy 6.1; the export's "
        "COMPLETED_DATE is the latest completion, after any callback), each placed by its dwelling's tract county "
        "(Tallis-Hesketh Community Action enters Tallis on its Hesketh jobs): %s."
        % "; ".join("%s %s" % (k, "{:,}".format(a[k])) for k in ORDER),
        "Ask B: summed the lines of cvcog_grants_ledger_2024-07_2026-09.csv posted in 2025 that carry a job number, "
        "at the amount posted (the close-out's convention), each read as the previous system's job number through "
        "the MOVED conversion notes in the status history (the agencies invoiced 2025 under their old numbers) and "
        "placed by the job's tract county: %s." % "; ".join("%s %s" % (k, "{:,}".format(b[k])) for k in ORDER),
        "Recommended the proportional split with no county capped, %s the largest at %s." % (top, money(al[top])),
    ]
    for k, s in enumerate(steps, 1):
        out.append("%d. %s" % (k, s))
    out.append("")
    out.append("## 4. Deliverable Answers\n")
    out.append("### corran_valley_2027_weatherization_allocation.xlsx\n")
    out.append("1. No county reaches the 12 per cent cap (%s)." % money(cap))
    out.append("2. Tax-year 2023 earned income credit returns with qualifying children, one decimal:")
    for k in ORDER:
        out.append("   - %s: %s" % (k, "{:,.1f}".format(fam[k])))
    out.append("3. Share of the fourteen counties' returns, per cent to two decimals:")
    for k in ORDER:
        out.append("   - %s: %.2f" % (k, sh[k]))
    out.append("4. 2027 allocation, nearest hundred dollars:")
    for k in ORDER:
        out.append("   - %s: %s" % (k, money(al[k])))
    out.append("5. Bar chart of the fourteen allocations against a dashed line at the 12 per cent cap (%s) on the "
               "Allocation sheet, %s highlighted." % (money(cap), top))
    out.append("6. Dwellings the program weatherized in program year 2025, whole dwellings:")
    for k in ORDER:
        out.append("   - %s: %s" % (k, "{:,}".format(a[k])))
    out.append("7. The program's spending on dwellings in program year 2025, whole dollars:")
    for k in ORDER:
        out.append("   - %s: %s" % (k, money(b[k])))
    out.append("")
    out.append("### corran_valley_ty2023_county_credit_families.csv\n")
    out.append("1. One row per member county with its tax-year 2023 earned income credit returns with qualifying "
               "children to one decimal, the figures in item 2 above, beside its credit returns of every kind.")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
