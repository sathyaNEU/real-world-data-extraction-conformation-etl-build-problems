"""task306 submission.md, written from figures.json (every figure emitted, none typed)."""
import analysis as A
import golden as GD

ORDER = GD.ORDER


def write(path, fig):
    c = fig["candidates"]
    win, run = c[fig["call"]], c[fig["runner_up"]]
    third = [k for k in ORDER if k not in (fig["call"], fig["runner_up"])][0]
    lines = ["## Tags", "",
             "**Domain:** Quantitative Finance (portfolio construction and risk: a systematic equity desk placing new "
             "capital with one of its backtested strategies, each sized by the alpha it keeps at that capital).",
             "**Analytical objective:** Opportunity Sizing & Decision Support.", ""]
    lines += ["## 1. Final Recommendation", "",
              "**Give the GBP 400 million to %s, which keeps GBP %d million of alpha a year at that size, GBP %d "
              "million more than %s, the runner-up.** Each strategy's gross alpha is netted of the shortfall its "
              "twelve months of rebalances would pay at GBP 400 million, priced on the desk's own orders at each "
              "trade's share of the stock's daily traded value. Not %s: its GBP %d million of gross alpha is the "
              "largest, but at GBP 400 million its month-end trades take a large share of each small cap's day, "
              "and it keeps GBP %d million."
              % (win["name"], win["net_gbp_m"], fig["gap_gbp_m"], run["name"], c[third]["name"],
                 c[third]["gross_gbp_m"], c[third]["net_gbp_m"]), ""]
    lines += ["## 2. Critical Components", "",
              "1. The desk's 2025 and 2026 orders cost more the larger their share of the stock's 20-session daily "
              "traded value: shortfall rises with the square root of participation, times the stock's daily "
              "volatility.",
              "2. At GBP 400 million the rebalances of December 2025 to November 2026 trade GBP %d million (%s), "
              "GBP %d million (%s) and GBP %d million (%s)."
              % (c["SCM"]["traded_gbp_m"], c["SCM"]["name"], c["MCV"]["traded_gbp_m"], c["MCV"]["name"],
                 c["LCQ"]["traded_gbp_m"], c["LCQ"]["name"]),
              "3. Alpha kept a year at GBP 400 million: %s." % "; ".join(
                  "%s **GBP %d million** of %d gross" % (c[k]["name"], c[k]["net_gbp_m"], c[k]["gross_gbp_m"])
                  for k in ORDER), ""]
    lines += ["## 3. Step-by-Step Solution", "",
              "1. Conformed the desk's orders: kept each execution id once from oms_fills_2025-2026.csv, read pounds "
              "fills as pence times 100, merged each BACKUP-RECOVERY order into the terminated original it "
              "continues (same account, stock, side and London date, the original's unfilled quantity), and "
              "measured each order's shortfall from its arrival mid, cost positive (TCA standard sections 1 and 2).",
              "2. Gave each order its participation, value at arrival over the 20-session average of close times "
              "volume in lse_daily_market_data_2025-2026.parquet, and the 60-session daily volatility, skipping "
              "each consolidation day in wealdmoor_security_master_2026-11-30.csv (TCA standard section 3).",
              "3. Fitted, band by band, shortfall on daily volatility times the square root of participation by "
              "least squares over the band's orders (IC-07 section 2: the desk's executions in the candidate's "
              "index band).",
              "4. Took each candidate's rebalances from 1 December 2025 to 30 November 2026 in "
              "backtest_rebalance_trades_2025-2026.csv, joined ISIN to SEDOL, scaled each traded weight to GBP 400 "
              "million and priced it on the fitted curve at its participation on the rebalance date (IC-07 "
              "section 2).",
              "5. Took each strategy's annualised gross alpha 2015 to 2026 from "
              "research_backtests_2027_candidates.xlsx times GBP 400 million and subtracted the cost.",
              "6. Recommended %s, GBP %d million ahead of %s." % (win["name"], fig["gap_gbp_m"], run["name"]),
              "7. For the workbook, gave each live strategy its orders through the dated trading account register "
              "(WM-DYN-01 is UK Dynamic to 30 June 2026 and the Severnvale transition from 17 August; WM-DYN-02 "
              "UK Dynamic from 1 July), then the value-weighted shortfall by quarter of 2026 and the value traded, "
              "filled quantity at the average fill price, by half year.", ""]
    lines += ["## 4. Deliverable Answers", "", "### %s" % GD.DECK, "",
              "1. Recommendation: give the GBP 400 million to %s." % win["name"],
              "2. Runner-up: %s." % run["name"],
              "3. Difference between them: GBP %d million a year." % fig["gap_gbp_m"],
              "4. Alpha each strategy keeps a year at GBP 400 million, whole GBP million:"]
    for k in ORDER:
        lines.append("   - %s: %d" % (c[k]["name"], c[k]["net_gbp_m"]))
    lines.append("5. Gross alpha a year at GBP 400 million, whole GBP million:")
    for k in ORDER:
        lines.append("   - %s: %d" % (c[k]["name"], c[k]["gross_gbp_m"]))
    lines.append("6. Chart on slide 1: each strategy's gross alpha beside the alpha it keeps, both in GBP million, "
                 "%s's kept alpha the tallest." % win["name"])
    lines += ["", "### %s" % GD.BOOK, "",
              "1. Implementation shortfall by quarter of 2026, basis points to one decimal:"]
    for n in A.LIVE_NAMES:
        lines.append("   - %s: %s" % (n, ", ".join("Q%d %.1f" % (q, fig["ask_shortfall_bps"]["%s Q%d" % (n, q)])
                                                    for q in (1, 2, 3, 4))))
    lines.append("2. Value traded by half of 2026, whole GBP million:")
    for n in A.LIVE_NAMES:
        lines.append("   - %s: %s" % (n, ", ".join("H%d %d" % (h, fig["ask_traded_gbp_m"]["%s H%d" % (n, h)])
                                                    for h in (1, 2))))
    lines.append("")
    open(path, "w").write("\n".join(lines))
