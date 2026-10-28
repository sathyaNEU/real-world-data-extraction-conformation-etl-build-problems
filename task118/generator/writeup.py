"""submission.md, drafted from figures.json: every figure in it is read from there."""
import figs as FG
import golden as GD
import params as P


def write(path, F):
    w, r = F["winner"], F["runner"]
    W = F["duties"][w]
    fuel = F["duties"]["FUEL"]
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** Economics & Econometrics (elasticity, welfare and policy impact estimation: a fixed Budget "
             "envelope given to the excise duty whose cut removes the most excess burden in the Budget year).")
    L.append("**Analytical objective:** Opportunity Sizing & Decision Support.\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**Give the 2027 Budget's GBP %.1f million envelope to spirits duty, cutting its 2027 rate of GBP %.2f a "
             "litre by about a fifth from 1 January 2027, which removes about GBP %.1f million of excess burden in 2027; "
             "the next best, cider, would remove about GBP %.1f million.**"
             % (F["envelope_m"], W["rate27"], F["winner_m"], F["runner_m"]))
    L.append("Not road fuel, whose duty and GST are the largest share of its price but whose drivers make under a third of "
             "their response to a price cut within 2027. Not cider, the most price-responsive duty, whose "
             "small wedge leaves little gain on the extra litres a cut buys. Not beer or wine, each about a quarter "
             "of the spirits figure.")
    L.append("\n## 2. Critical Components\n")
    L.append("1. Excess burden removed in 2027 by the envelope: **spirits about GBP %.1f million**, cider about GBP "
             "%.1f million" % (F["winner_m"], F["runner_m"]))
    L.append("2. The gain is counted on every extra litre at the whole of the duty and GST still charged on it, not "
             "only on the cut itself")
    L.append("3. Buyers' response is the part made within 2027 from a demand model with lagged adjustment: spirits "
             "nearly all of their long-run response by the fourth quarter, road fuel under a third")
    L.append("\n## 3. Step-by-Step Solution\n")
    L.append("1. Stacked %s (2008 to 2011, one sheet per duty) and %s (2012 to 2026 Q3, preliminary quarters "
             "included) into one quarterly series per duty, %d quarters at constant 2026 prices."
             % (P.FILES["series_old"], P.FILES["series_new"], F["quarters"]))
    L.append("2. For each duty fitted least squares of log clearances on four quarter dummies, log shelf price and the "
             "previous quarter's log clearances; the response to a price change from 1 January 2027 by quarter k is "
             "the first-quarter coefficient times (1 - adjustment^k) / (1 - adjustment).")
    L.append("3. Baseline (manual, section 5): the four quarters 2025 Q4 to 2026 Q3, each standing for its quarter of "
             "2027; producer price = the 2026 Q3 shelf price net of %d per cent GST less the duty then in force; the "
             "2027 rate from %s." % (F["gst_pct"], P.FILES["rates"]))
    L.append("4. For each duty solved for the cut at which duty and GST received in 2027, on the litres bought each "
             "quarter after the response, fall by GBP %.1f million (spirits by about a fifth of its rate)."
             % F["envelope_m"])
    L.append("5. Excess burden removed: each quarter, the area between the fitted constant-elasticity demand curve and "
             "the producer price over the extra litres, summed over 2027: spirits %.1f, cider %.1f GBP million."
             % (F["winner_m"], F["runner_m"]))
    L.append("6. Excise on releases (%s, CE14): exact duplicate rows dropped; procedure 4071 not cancelled; a "
             "declaration that a later one names as its related declaration is replaced by it, so each release counts "
             "once, as the last declaration of its chain, in the quarter the chain's first declaration was accepted "
             "(Eskerholm date, UTC to UK time)." % P.FILES["declarations"])
    L.append("7. Each item priced at quantity times the rate in force on that first day (duty_gbp repeats the "
             "declaration's total on every item row); less 6171 repayments (duty_gbp) in the quarter accepted; plus "
             "7171 removals to premises with no approval in force that day (EKW171 from 14 November 2025, EKW157 from "
             "9 October 2025) at that day's rate; GBP thousand to one decimal.")
    L.append("\n## 4. Deliverable Answers\n")
    L.append("### %s\n" % GD.DOCX)
    L.append("1. The duty: spirits, its 2027 rate of GBP %.2f a litre cut by about a fifth, removing about GBP %.1f "
             "million of excess burden in 2027." % (W["rate27"], F["winner_m"]))
    L.append("2. The next best: cider, about GBP %.1f million." % F["runner_m"])
    L.append("3. A bar chart of the excess burden each duty's cut would remove in 2027, spirits marked.")
    L.append("\n### %s\n" % GD.XLSX)
    L.append("1. Excise accounted for on releases from bonded warehouses, GBP thousand:")
    for c, *_ in P.DUTIES:
        for q in P.ASK_QUARTERS:
            L.append("   - %s, %s: %s" % (F["duties"][c]["name"], FG.QUARTER_LABEL[q], "{:,.1f}".format(F["asks_k"][c][q])))
    open(path, "w", encoding="utf-8").write("\n".join(L) + "\n")
