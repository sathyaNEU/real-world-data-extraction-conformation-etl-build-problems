"""Write task463/submission.md from generator/figures.json."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W   # noqa: E402


def _and(names):
    return ", ".join(names[:-1]) + " and " + names[-1] if len(names) > 1 else names[0]


WORDS = {4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"}


def _p(x):
    return ("%.1f" % x).replace("-", "-")


def write(fig_path, out_path):
    F = json.load(open(fig_path))
    N = W.INAME
    mv, st = F["moved"], F["stay"]
    R, P, D = F["rate"], F["published"], F["diff"]
    ni, no = F["nearest_in"], F["nearest_out"]
    dm = F["default_moved"]
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** Survey Research & Official Statistics (official time-series production: a retail prices "
             "index's grocery and household items compiled from three supermarkets' transaction records and set against "
             "the published index over a parallel year).")
    L.append("**Analytical objective:** Data Extraction & Conformation (ETL).\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**Move %d of the sixteen items to transaction data from the January 2027 index: %s. Keep %s on the field "
             "collection.**" % (F["n_moved"], _and([N[i] for i in mv]), _and([N[i] for i in st])))
    L.append("The moving items' 12-month rates to September 2026 from the transaction data sit within %.1f points of their "
             "published rates; %s are %s points apart. Not the %s that linking the twelve month-on-month comparisons "
             "moves (%s): in the nine items whose goods keep, an offer month's stocked-up buying weights each price cut "
             "heavily and the next month's recovery lightly, and the linked index ends below every line's own change.\n" % (
                 max(abs(D[i]) for i in mv),
                 _and(["%s (%s against %s)" % (N[i], _p(R[i]), _p(P[i])) for i in st]),
                 _and([_p(abs(D[i])) for i in st]), WORDS[len(dm)], _and([N[i] for i in dm])))
    L.append("## 2. Critical Components\n")
    L.append("1. %s, the moving item nearest the line: **%s** per cent against a published **%s**, a difference of **%s** "
             "points." % (N[ni], _p(R[ni]), _p(P[ni]), _p(D[ni])))
    L.append("2. %s, the staying item nearest the line: **%s** per cent against a published **%s**, a difference of **%s** "
             "points." % (N[no], _p(R[no]), _p(P[no]), _p(D[no])))
    L.append("3. Items moving: **%d** of 16." % F["n_moved"])
    L.append("")
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Put the three feeds into product-months as the plan defines them: %s with each resent week at its latest "
             "extract, %s with each fiscal week dated through %s and its EANs padded to 13 digits, and %s's daily rows "
             "through its sku_gtin table with 5 per cent GST added to the net values; a line is a GTIN at one supermarket, "
             "a week belongs to the month in which it ends, and a line's monthly price is its sales value with GST over its "
             "units, returns netted." % (W.FILES["wrenfold"], W.FILES["gorsedale"], W.FILES["calendar"], W.FILES["calderby"]))
    L.append("2. Classified each line through %s and kept, for each item, the lines each supermarket sold in every month "
             "from September 2025 to September 2026: %s lines over the sixteen items." % (
                 W.FILES["classes"], format(F["csv_panel_lines"], ",")))
    keep = [it for it in W.ICODE if it not in dm and it not in st]
    dr = [F["linked_drift"][it] for it in keep]
    L.append("3. Compiled each item's monthly index over those lines as a Törnqvist comparison of the month with "
             "September 2025 (each line weighted by its spending share averaged over the two months compared) and took "
             "the 12-month rate as the index's change from September 2025 to September 2026; GEKS and CCDI over the "
             "thirteen months and a direct Fisher give the same sixteen rates to one decimal. Linking the twelve "
             "month-on-month comparisons was not used: in the %s items whose goods keep, the month after an offer runs "
             "well below normal sales, so the linked index ends %s to %s points below the direct comparison and below "
             "every line's own change, which no change in the item's prices can do." % (
                 WORDS[len(keep)], _p(min(dr)), _p(max(dr))))
    L.append("4. Set each rate against the item's published 12-month rate to September 2026 (%s, sheet 12-month rates) "
             "and moved the items whose rates, each to one decimal, are within 1.5 points." % W.FILES["published"])
    L.append("5. For each supermarket and month, dated the arrival of the last file in %s carrying the month's records "
             "(a weekly file's weeks in the month they end, Calderby's extracts by their days, resends and second "
             "extracts included), converted from UTC to Kellesay time, counted the days after the month's end, and "
             "averaged the thirteen months." % W.FILES["deliveries"])
    L.append("6. Placed each category in %s on its RPI item by its name in %s (Wrenfold's 2025 codes name other "
             "categories in the map), left out Gorsedale's trade rows, added 5 per cent GST to Calderby's net sales, and "
             "divided each item's sales by the households' spending in %s." % (
                 W.FILES["returns"], W.FILES["catmap"], W.FILES["spending"]))
    L.append("")
    L.append("## 4. Deliverable Answers\n")
    L.append("### %s\n" % W.GOLDEN["workbook"])
    L.append("1. Moving to transaction data in January 2027: %s; staying on the field collection: %s." % (
        _and([N[i] for i in mv]), _and([N[i] for i in st])))
    L.append("2. Each item's lines compared, 12-month rate to September 2026 from the transaction data (per cent), "
             "published 12-month rate (per cent), difference (points) and January 2027:")
    for it in W.ICODE:
        L.append("   - %s %s: %d, %s, %s, %s, %s" % (it, N[it], F["lines"][it], _p(R[it]), _p(P[it]), _p(D[it]),
                                                    "moves" if it in mv else "stays"))
    L.append("3. Each supermarket's average number of calendar days after a month's end until its records for the month "
             "were complete, September 2025 to September 2026:")
    for r in (W.RNAME[x] for x in W.RETAILERS):
        L.append("   - %s: %s" % (r, _p(F["delivery"][r])))
    L.append("4. Each item's 2025 coverage, the supermarkets' retail sales with GST as a share of households' spending, "
             "whole per cent:")
    for it in W.ICODE:
        L.append("   - %s %s: %d" % (it, N[it], F["coverage"][it]))
    L.append("")
    L.append("### %s\n" % W.GOLDEN["chart"])
    L.append("1. One panel per item: its transaction-data index and its published index by month, September 2025 = 100, "
             "each panel titled with whether the item moves and its two 12-month rates; the %d moving items' "
             "transaction-data lines in one colour and the three staying items' in another." % F["n_moved"])
    L.append("")
    L.append("### %s\n" % W.GOLDEN["products"])
    L.append("1. %s rows, one per supermarket line and month of the sixteen items over the parallel year (%s lines), "
             "each with the line's units, sales value with GST and unit price; %s of the lines are in the lines "
             "compared." % (format(F["csv_rows"], ","), format(F["csv_lines"], ","), format(F["csv_panel_lines"], ",")))
    with open(out_path, "w") as f:
        f.write("\n".join(L) + "\n")
