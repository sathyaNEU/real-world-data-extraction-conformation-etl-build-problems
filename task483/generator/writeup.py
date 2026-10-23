"""submission.md, every figure read from generator/figures.json."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
MA, CDL = "Medical Assisting", "Commercial Driver License, Class A"


def join(xs, word="and"):
    xs = [str(x) for x in xs]
    sep = "; " if any("," in x for x in xs) else ", "
    return xs[0] if len(xs) == 1 else sep.join(xs[:-1]) + "%s%s " % (sep.rstrip() if sep == "; " else "", " " + word) \
        + xs[-1]


def c(n):
    return "{:,}".format(n)


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    pr = f["programs"]
    cl = f["call"]
    k = f["components"]
    st = f["stated"]
    deg = [p for p in pr if pr[p]["test"] == "earnings"]
    sht = [p for p in pr if pr[p]["test"] == "placement"]
    fail_deg = [p for p in deg if pr[p]["tested"] and not pr[p]["passes"]]
    fail_sht = [p for p in sht if pr[p]["tested"] and not pr[p]["passes"]]
    ma, cdl = k["medical_assisting"], k["cdl"]
    o = []
    o.append("## Tags\n")
    o.append("**Domain:** Survey Research & Official Statistics, census, register and administrative data quality (a "
             "state outcomes release of campus-by-cohort earnings cells and a workforce board's employer-quarter wage "
             "records, conformed with a four-campus college's completion extracts, grant roster and program inventory "
             "into the board's workforce value designation file).")
    o.append("**Analytical objective:** Data Extraction & Conformation (ETL).\n")
    o.append("## 1. Final Recommendation\n")
    o.append("**Larkspur Basin Community College's workforce value designation lapses for the 2027-28 Career Training "
             "Grant year: %d per cent of the 2024-25 completers of its tested programs (%s of %s) are in passing "
             "programs, under the %d per cent the standard needs.**" % (cl["share_pct"], c(cl["in_passing"]),
                                                                       c(cl["tested"]), cl["line_pct"]))
    o.append("Medical Assisting's completers earn a median %d thousand dollars, under the 34.2 thousand benchmark, and "
             "%d per cent of the Commercial Driver License program's grant completers were working on day 180, under "
             "70. Not %d per cent: averaging each program's campus-by-cohort medians puts Medical Assisting at %d "
             "thousand, and counting any pay in the quarter holding day 180 puts the CDL program at %d per cent, "
             "though %d of its %d grant completers had left their first carrier weeks before day 180 or started at the "
             "next weeks after it, inside that quarter.\n"
             % (ma["pooled_thousands"], cdl["dated_pct"], k["default_share_pct"], ma["averaged_thousands"],
                cdl["quarter_pct"], cdl["quarter_working"] - cdl["working"], cdl["grant_completers"]))
    o.append("## 2. Critical Components\n")
    o.append("1. Medical Assisting's median earnings, its six campus-by-cohort cells pooled, are **%d** thousand "
             "dollars; its cells' medians averaged by completers give %d." % (ma["pooled_thousands"],
                                                                            ma["averaged_thousands"]))
    o.append("2. The CDL program's day-180 figure is **%d** per cent (%d of %d grant completers working); pay from any "
             "employer in the quarter gives %d." % (cdl["dated_pct"], cdl["working"], cdl["grant_completers"],
                                                    cdl["quarter_pct"]))
    o.append("3. Either correction alone keeps the designation: **%d** per cent with the pooled medians and quarter "
             "pay, **%d** with the averaged medians and the dated jobs." % (k["degree_half_alone_pct"],
                                                                            k["short_half_alone_pct"]))
    o.append("4. The programs that fail on earnings: %s. On placement: %s.\n" % (join(fail_deg), join(fail_sht)))
    o.append("## 3. Step-by-Step Solution\n")
    steps = [
        "Joined every program through larkspur_program_inventory_2025-26.xlsx (both student systems' program codes, "
        "the grant's program IDs, and the CIP codes Information Technology and Criminal Justice carried before fall "
        "2022) and took the three-years-after cells for award year 2020-21 from "
        "postsecondary_earnings_outcomes_2024_edition.xlsx and 2021-22 from "
        "postsecondary_earnings_outcomes_2025_edition.csv, the 2024 earnings times %.4f; Paralegal Studies' cells "
        "are suppressed, so it is not tested." % st["cpi_factor"],
        "Rebuilt each cell's earnings distribution by joining its five percentiles straight, pooled the cells by "
        "completers with earnings and solved for the point where the pooled share reaches half: each credit "
        "program's median.",
        "Took the grant completers from ctg_participant_roster_2023-2026.csv (exit reason Completed, sections ending "
        "1 July 2024 to 30 June 2025; Forklift and Material Handling has %d, under 20, and is not tested) and day "
        "%d as the section's last day plus %d days." % (pr["Forklift and Material Handling"]["grant_completers"],
                                                     st["day"], st["day"]),
        "In ctg_participant_wage_records_2022q3-2026q2.csv kept the latest report for each participant, employer and "
        "quarter, and counted a completer as working when a job paid in the quarter holding day 180 was paid in the "
        "quarters before and after too, or when its start (paid in the next quarter only) or its exit (paid in the "
        "one before only) dated from its pay in the quarter against its pay in its adjacent full quarter falls on "
        "the working side of day 180.",
        "Counted each program's 2024-25 completers in fennimore_ridgefield_completions_2024-25.xlsx and "
        "copper_flats_antelope_springs_completions_2024-25.csv, grant participants or not, and took the share of the "
        "tested programs' %s completers in passing programs: %s, %d per cent." % (c(cl["tested"]), c(cl["in_passing"]),
                                                                              cl["share_pct"]),
        "For the clock hours, took larkspur_ctg_attendance_2023-2026.csv, dropped the rows it repeats (one week of "
        "March 2025 appended again at its end), read each session's time as hours and minutes after the point (no "
        "entry runs past fifty-nine after it, and the full sessions of a program scheduled in half hours read point "
        "thirty, so a completer at every session totals the inventory's clock hours only that way), and summed the "
        "sessions dated 1 July 2024 to 30 June 2025 under the program of each session's section in the roster.",
        "For the loan principal, joined each credit program's 2024-25 completers by state student ID to "
        "larkspur_direct_loan_disbursements_2019-2026.csv, kept subsidized and unsubsidized loans, summed each "
        "disbursement before 1 July 2024 with returns netted and counted each loan from then once, since that aid "
        "system writes the loan's amount for the award year on each of its disbursements (two such rows run past the "
        "annual limits in larkspur_cost_of_attendance_2024-25.pdf); the median to the nearest 10 dollars.",
    ]
    for i, s in enumerate(steps, 1):
        o.append("%d. %s" % (i, s))
    o.append("")
    o.append("## 4. Deliverable Answers\n")
    o.append("### larkspur_workforce_value_2027-28.xlsx\n")
    o.append("1. The call: the designation lapses for 2027-28.")
    o.append("2. Each credit program's earnings figure, whole thousands of dollars:")
    for p in deg:
        x = pr[p]
        o.append("   - %s: %s" % (p, ("%d" % x["figure_thousands"]) if x["tested"] else "not tested (no published "
                                                                                       "cell)"))
    o.append("3. Each short-term program's placement figure, whole per cent:")
    for p in sht:
        x = pr[p]
        o.append("   - %s: %s" % (p, ("%d" % x["figure_pct"]) if x["tested"] else "not tested (%d grant completers)"
                                  % x["grant_completers"]))
    o.append("4. The programs that fail: %s." % join(fail_deg + fail_sht))
    o.append("5. The share of the 2024-25 completers of tested programs in passing programs: %d per cent (%s of %s)."
             % (cl["share_pct"], c(cl["in_passing"]), c(cl["tested"])))
    o.append("6. Each short-term program's clock hours its grant participants attended from July 2024 to June 2025, "
             "whole hours:")
    for p in sht:
        o.append("   - %s: %s" % (p, c(pr[p]["clock_hours_fy2025"])))
    o.append("7. Each credit program's median of all the Direct Subsidized and Unsubsidized Loan principal its 2024-25 "
             "completers who borrowed took out at the college, nearest 10 dollars:")
    for p in deg:
        o.append("   - %s: %s" % (p, c(pr[p]["loan_median_usd"])))
    o.append("\n### larkspur_program_tests_2027-28.svg\n")
    o.append("8. Two bar panels, one bar per tested program, each labelled with its figure: the %d credit programs' "
             "median earnings in thousands of dollars against a dashed line at 34.2, and the %d short-term programs' "
             "day-180 shares against a dashed line at 70 per cent; passing programs in blue, failing in orange; the "
             "title states the call and the %d per cent share."
             % (sum(1 for p in deg if pr[p]["tested"]), sum(1 for p in sht if pr[p]["tested"]), cl["share_pct"]))
    open(os.path.join(TASK, "submission.md"), "w", encoding="utf-8").write("\n".join(o) + "\n")


if __name__ == "__main__":
    main()
