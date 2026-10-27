"""submission.md from figures.json: tags, the recommendation, its components, the steps and the deliverable answers."""
import params as P

NAMES = {P.SHORT[b]: b for b in P.ORDER}


def c(x):
    return "{:,}".format(int(x))


def gbp(x):
    return "£{:,}".format(int(x))


def about(v):
    return "fewer than 5" if v < 5 else "about %d" % (int(round(v / 10.0)) * 10)


def write(path, fig):
    cl, ea, ex, A, B, F = fig["call"], fig["easy"], fig["ext"], fig["askA"], fig["askB"], P.FILES
    rb, tb = fig["basis"]["rise_bands_pct"], fig["basis"]["term_bands_months"]
    av = cl["avoided"]
    t = []
    t.append("## Tags\n")
    t.append("**Domain:** Banking, credit and financial risk (collections and recovery).")
    t.append("**Analytical objective:** Opportunity sizing and decision support.\n")
    t.append("## 1. Final Recommendation\n")
    t.append("**Place the Financial Support Team on the First-time buyer 2019-21 book in 2027: it avoids %s "
             "possessions there, against %s in High LTV 2022-24, the next best.**" % (about(av["FTB"]), about(av["HLTV"])))
    t.append("The first-time buyer book's 2021 borrowers who took a longer term at their 2026 rate switch are almost "
             "all up to date now, but the 2024 term increases fell behind %s after their first eight months, so the "
             "book's 2027 arrears cases outnumber every other book's. Not High LTV 2022-24, which leads on current arrears and on a forecast that reads the extended "
             "accounts' small payment rise as low risk. Not Shared ownership or Buy to let, at %s each.\n"
             % ("only" if ex["behind_8m"] == 0 else "mostly", about(max(av["SO"], av["BTL"]))))
    t.append("## 2. Critical Components\n")
    t.append("1. **%s** of the **%s** first-time buyer accounts on the book at 30 September 2026 had their remaining "
             "term raised at their 2026 rate switch, a median **%d** years, holding their payment rise to a median "
             "**%d per cent** against **%d per cent** for the switchers on the book who kept their term."
             % (c(ex["ftb_raised_2026"]), c(ex["ftb_on_book"]), ex["years_added_median"], ex["pay_rise_extended"],
                ex["pay_rise_kept"]))
    early = "**none** was" if ex["behind_8m"] == 0 else "**%d** were" % ex["behind_8m"]
    t.append("2. Of the **%s** accounts whose term was raised in 2024, %s two payments or more in arrears at one of "
             "the eight month ends after the month of the increase and **%d** at a month end after it up to 30 "
             "September 2026."
             % (c(ex["raised_2024"]), early, ex["behind_by_asof"]))
    t.append("3. Possessions avoided in 2027 (nearest ten): First-time buyer 2019-21 **%s**; High LTV 2022-24, Shared "
             "ownership and Buy to let **fewer than 5** each, at the planning rates of **%.1f**, **%.1f**, **%.1f** and "
             "**%.1f per cent** and the plan's **%d per cent** cut."
             % (about(av["FTB"]).replace("about ", ""), cl["rate_pct"]["FTB"], cl["rate_pct"]["HLTV"],
                cl["rate_pct"]["SO"], cl["rate_pct"]["BTL"], fig["basis"]["effect_pct"]))
    t.append("")
    t.append("## 3. Step-by-Step Solution\n")
    t.append("1. Rebuilt payments in arrears at each month end from %s (the arrears balance over the contractual "
             "payment, rounded down, %s section 2), with the re-sent month rows dropped." % (F["history"], F["policy"]))
    t.append("2. Marked each rate switch (a new product_code, read with the dashes taken out) and each month the "
             "remaining_term_months rose: %s first-time buyer accounts on the book had their term raised at the 2026 "
             "switch, and %d of the %s raised in 2024 had been two payments behind at a month end after the month of "
             "the increase up to September 2026, %s at one of the eight month ends after it."
             % (c(ex["ftb_raised_2026"]), ex["behind_by_asof"], c(ex["raised_2024"]),
                "none of them" if ex["behind_8m"] == 0 else "%d of them" % ex["behind_8m"]))
    t.append("3. Fitted the monthly chance of each move between nought, one and two or more payments behind on the "
             "January 2024 to August 2026 history, by book, the payment rise at the last switch (under %d, %d to %d, "
             "%d to %d, %d per cent or more) and the months since a term increase (none, under %d, %d to %d, %d or "
             "more), leaving out the month an account closes, each cell smoothed towards its book's rate with a weight "
             "of %d account-months." % (rb[0], rb[0], rb[1], rb[1], rb[2], rb[2], tb[0], tb[0], tb[1], tb[2],
                                        fig["basis"]["smoothing_weight"]))
    t.append("4. Carried every account on %s with recovery_stage None from its September 2026 arrears through 2027, "
             "month by month, with no allowance for accounts that close, counting each account's first entry from January to "
             "December 2027 once and taking it out of the chain there (%s section 2).",)
    t[-1] = t[-1] % (F["book"], F["plan"])
    t.append("5. Took %d per cent of each book's expected 2027 entries times its planning rate (%s section 3): "
             "First-time buyer 2019-21 %s possessions avoided, High LTV 2022-24 %s, Shared ownership and Buy to let "
             "%s each; the same chain without the term-increase state puts High LTV 2022-24 first."
             % (fig["basis"]["effect_pct"], F["plan"], about(av["FTB"]), about(av["HLTV"]),
                about(max(av["SO"], av["BTL"]))))
    t.append("6. From %s (one line per claim and action, the second defendant's lines dropped) counted the possession "
             "orders made or varied at hearings dated 1 October 2025 to 30 September 2026, an order line repeating "
             "the claim's previous order with no hearing between being the same order sent again, and took each "
             "claim as open at 30 September 2026 unless withdrawn, discharged, evicted or, since Ridley Varga's reports "
             "end at the warrant, recorded in %s as taken into possession after it was issued."
             % (F["litigation"], F["possessions"]))
    t.append("7. Took the latest statement of each sale reference in %s completed from 1 October 2025 to 30 September "
             "2026, matched receivers' sales to the account through %s, counted one possession sold per account and "
             "completion date (the Society issues a statement for each loan part), took the debt as the sum of the "
             "account's rows in %s (one per loan part) and each account's book from %s (the register's rows before "
             "April 2026 carry its earlier first-time buyer book), and set each loss to the debt less the sale price "
             "net of selling costs, nil where the sale covers it (policy section 8)."
             % (F["sales"], F["receivers"], F["possessions"], F["history"]))
    t.append("8. Recommended the First-time buyer 2019-21 book, %s possessions avoided against %s in High LTV 2022-24."
             % (about(av["FTB"]), about(av["HLTV"])))
    t.append("")
    t.append("## 4. Deliverable Answers\n")
    t.append("### support_team_2027_placement_paper.pdf\n")
    t.append("1. The book to work in 2027: First-time buyer 2019-21, %s possessions avoided." % about(av["FTB"]))
    t.append("2. The next best book: High LTV 2022-24, %s possessions avoided." % about(av["HLTV"]))
    t.append("3. Chart of possessions avoided in 2027 by book (section 3 of the paper), with and without the term "
             "increases carried, the First-time buyer 2019-21 book the largest with them.")
    t.append("\n### support_team_2027_workbook.xlsx\n")
    t.append("1. Possession orders made or varied at hearings from October 2025 to September 2026, of those suspended "
             "on terms, and possession claims open at 30 September 2026:")
    for k in ("FTB", "HLTV", "SO"):
        t.append("   - %s: %d, %d, %d" % (NAMES[k], A[k]["orders"], A[k]["suspended"], A[k]["open"]))
    t.append("2. Possessions sold with completion from October 2025 to September 2026 (sold, sold at a loss, average "
             "loss per possession sold):")
    for k in ("FTB", "HLTV", "SO"):
        t.append("   - %s: %d, %d, %s" % (NAMES[k], B[k]["sold"], B[k]["at_loss"], gbp(B[k]["avg_loss"])))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(t) + "\n")
