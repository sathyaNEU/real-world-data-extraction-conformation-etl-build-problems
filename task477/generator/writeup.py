"""submission.md, drafted from generator/figures.json: every figure the write-up states comes from there."""
import json

import world as W

TAGS = ("**Domain:** Survey Research & Official Statistics (seasonal adjustment and official time-series production: "
        "pay-date calendar effects in quarterly covered wages).\n"
        "**Analytical objective:** Data Extraction & Conformation (ETL).")


def fmt(n):
    return "{:,}".format(int(n))


def _join(xs):
    return ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else xs[0]


def write(fig_path, out_path):
    f = json.load(open(fig_path, encoding="utf-8"))
    F = W.FILES
    nm, gr, pg = f["names"], f["growth"], f["paid_growth"]
    sl, nxt = f["call"]["slate"], f["call"]["next_in_line"]
    out = [s for s in f["paid_slate"] if s not in sl]
    left = [s for s in sl if s not in f["paid_slate"]]
    k = f["constants"]
    L = ["## Tags", "", TAGS, "",
         "## 1. Final Recommendation", "",
         "**Name %s as the 2027 to 2029 sector-partnership slate; %s is next in line.**" % (
             _join(["%s (%s%%)" % (nm[s], gr[s]) for s in sl]), "%s (%s%%)" % (nm[nxt], gr[nxt])),
         "These are the four eligible industries with the fastest growth in pay per job from 2021 to 2025 for the "
         "work done in each year. Not %s, which wages as paid put on the slate (%s): 2025 carried an extra Thursday "
         "pay date (1 January 2026 paid on 31 December 2025) for the payrolls run on Thursdays, which these two "
         "industries largely are, so their 2025 wages hold more than a year's work." % (
             _join([nm[s] for s in out]), _join(["%s%%" % pg[s] for s in out])),
         "",
         "## 2. Critical Components", "",
         "1. Growth in pay per job, 2021 to 2025, for the work done: %s." % _join(
             ["%s **%s%%**" % (nm[s], gr[s]) for s in out + left]),
         "2. Eligible industries (2025 annual average jobs of %s or more): **%d**." % (fmt(f["min_jobs"]),
                                                                                      f["n_eligible"]),
         "",
         "## 3. Step-by-Step Solution", "",
         "1. Took Tallis County's (%s) private sector rows (own_code 5, agglvl_code 74) from %s, %s and %s, using the "
         "annual release for 2025 in place of the first-published quarters; %d sectors had 2025 annual average jobs "
         "(the mean of the twelve monthly levels) of %s or more (guidelines %s)." % (
             W.COUNTY_FIPS, F["qcew_a"], F["qcew_b"], F["qcew_c"], f["n_eligible"], fmt(f["min_jobs"]),
             f["sections"]["eligible"]),
         "2. Counted each quarter's pay dates on four every-other-week phases (Fridays from 1 and 8 January 2021, "
         "Thursdays from 7 and 14 January 2021; a weekly payroll pays on both phases of its weekday), a date falling "
         "on a weekend or federal holiday paid the business day before, since %s counts wages in the quarter paid." %
         F["layout"],
         "3. For each eligible industry, regressed the log of quarterly wages per job (total_qtrly_wages over the mean "
         "of the three monthly levels), %d to %d, on year and quarter effects and the four counts; each coefficient "
         "times %s (the biweekly pay dates in an average quarter) is that phase's share of the payroll." % (
             W.Y0, W.Y1, k["qd"]),
         "4. Divided each industry's %d and %d wages by 1 plus the sum over phases of share times (pay dates in the "
         "year times %d over %d, less 1), then by annual average jobs, and took 2025 over 2021 less 1 (guidelines "
         "%s): %s." % (f["base"], f["latest"], k["step"], k["days"], f["sections"]["measure"],
                       _join(["%s %s%%" % (nm[s], gr[s]) for s in f["order"]])),
         "5. Counted each 2025 exiter in %s once, at the last exit, treating two participant IDs with the same "
         "birth_date and home_zip and identical wage records in %s as one person; took wages above zero in the second "
         "quarter after that exit; mapped a row reported under a professional employer organization's account to the "
         "client business through ui_acct and rptg_unit against %s (peo_acct, client_seq); kept the business paying "
         "the most and its NAICS sector in %s (manual %s): %s exiters in eligible industries." % (
             F["exits"], F["wages"], F["peo"], F["employers"], f["sections"]["industry"],
             fmt(f["asks"]["exiters_total"])),
         "6. Took the checks in %s issued in 2025 and not voided, joined each to its lines in %s by check_no, valued "
         "each line at voucher_amount over of_installments (the last installment taking the cents left over, so a "
         "check's lines sum to its amount), and assigned it to the target industry %s gives the program named in the "
         "line's description, active or withdrawn, since a withdrawn program's ID is reissued (guidelines %s): $%s." % (
             F["register"], F["ita"], F["etpl"], f["sections"]["ita"], fmt(f["asks"]["ita_total"])),
         "7. Named the four eligible industries with the highest growth (guidelines %s) and the fifth as next in "
         "line: %s; next %s." % (f["sections"]["slate"], _join([nm[s] for s in sl]), nm[nxt]),
         "",
         "## 4. Deliverable Answers", "",
         "### %s" % W.GOLDEN["table"], "",
         "1. One row per eligible industry, in order of growth: growth in pay per job 2021 to 2025 (whole percent), "
         "on the slate, 2025 exiters employed in the second quarter after exit, 2025 ITA payments (nearest dollar):"]
    for s in f["order"]:
        L.append("   - %s (%s): %s%%; %s; %s exiters; $%s" % (nm[s], s, gr[s], "on the slate" if s in sl else
                                                                "not on the slate", fmt(f["asks"]["exiters"][s]),
                                                                fmt(f["asks"]["ita"][s])))
    L += ["", "### %s" % W.GOLDEN["memo"], "",
          "1. The slate for the board's vote: %s; next in line %s." % (_join([nm[s] for s in sl]), nm[nxt]),
          "2. Horizontal bar chart of every eligible industry's growth in pay per job, 2021 to 2025, each bar "
          "labelled with its whole percent, the slate's four bars darker.",
          "3. The application table by industry with the same growth, exiter and ITA figures as %s." %
          W.GOLDEN["table"]]
    open(out_path, "w", encoding="utf-8").write("\n".join(L) + "\n")
