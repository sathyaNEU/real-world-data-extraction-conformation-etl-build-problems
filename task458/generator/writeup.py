"""submission.md, written from figures.json so every figure it states is one the generator computed."""
import json

DIVS = [("KD", "Kitchen and Dining"), ("SL", "Storage and Laundry"), ("LE", "Lighting and Electrical"),
        ("TH", "Tools and Hardware"), ("GO", "Garden and Outdoor")]
SUBN = [("AHL", "Ashlund Home Ltd"), ("AHI", "Ashlund Home Ireland Ltd"), ("AHB", "Ashlund Home B.V.")]


def c(n):
    return "{:,}".format(int(round(n)))


def m(v):
    return "%.1f million" % v


def mp(v):
    """The provision, to the nearest million."""
    return "%.0f million" % v


def ms(v):
    """The shortfall or headroom, to the nearest 0.25 million."""
    return ("%.2f" % v).rstrip("0").rstrip(".") + " million"


def write(fig_path, out_path):
    f = json.load(open(fig_path))
    r = f["rungs"]
    s = []
    s.append("## Tags\n")
    s.append("**Domain:** General Statistics & Data Science (data integration, record linkage and entity resolution).")
    s.append("**Analytical objective:** Data Extraction & Conformation (ETL).\n")
    s.append("## 1. Final Recommendation\n")
    s.append("**Ashlund Home Group needs Northgate's written waiver of the borrowing base covenant before the FY2026 "
             "accounts are delivered: after a stock provision of GBP %s the borrowing base is GBP %s against GBP %.2f "
             "million drawn at 31 December 2026, a shortfall of GBP %s.**" %
             (mp(f["provision_gbp_m"]), m(f["borrowing_base_gbp_m"]), f["drawn_gbp_m"], ms(f["shortfall_gbp_m"])))
    s.append("The GBP %s surplus (excess lines plus Valuehall's own stock) cannot all go through Valuehall in 2027: a "
             "stocked store sells about GBP %s at cost a trading day whatever it holds, so the stores' %s trading days "
             "take GBP %s and the other GBP %s goes to trade buyers at %.3f of cost. Not a GBP %s provision with GBP %s "
             "of headroom, which valuing the whole surplus at Valuehall's %.3f recovery gives; nor GBP %s, which "
             "extending Valuehall's yearly sales in line with what it was sent gives." %
             (m(f["surplus_pool_gbp_m"]), c(f["valuehall_per_trading_day_gbp"]), c(f["store_days_2027"]),
              m(f["through_valuehall_gbp_m"]), m(f["to_trade_buyers_gbp_m"]), f["trade_recovery"],
              m(r["none"]["provision_m"]), m(r["none"]["headroom_m"]), f["valuehall_recovery"],
              m(r["fit"]["provision_m"])))
    s.append("")
    s.append("## 2. Critical Components\n")
    s.append("1. Excess stock at cost (beyond twelve months' net shipments to customers): GBP **%s** (%s)." %
             (c(f["excess_total_gbp"]), "; ".join("%s **%s**" % (nm, c(f["excess_by_company_gbp"][k])) for k, nm in SUBN)))
    s.append("2. Surplus to dispose of in 2027, with Valuehall's year-end stock of GBP **%s**: GBP **%s**; through Valuehall "
             "GBP **%s**, to trade buyers GBP **%s**." % (c(f["stock_at_cost_gbp"]["VH"]), c(f["surplus_pool_gbp"]),
                                                          c(f["through_valuehall_gbp"]), c(f["to_trade_buyers_gbp"])))
    s.append("3. Provision GBP **%s**; inventories after provision GBP **%s** (stock at cost GBP %s); borrowing base GBP "
             "**%s**; shortfall against GBP %.2f million drawn GBP **%s**." %
             (mp(f["provision_gbp_m"]), m(f["inventories_after_provision_gbp_m"]), c(f["stock_at_cost_gbp"]["total"]),
              m(f["borrowing_base_gbp_m"]), f["drawn_gbp_m"], ms(f["shortfall_gbp_m"])))
    s.append("")
    s.append("## 3. Step-by-Step Solution\n")
    s.append("1. Took the measurement rules from FIN-07 (excess beyond twelve months' net shipments to customers, "
             "transfers to Valuehall and group companies excluded; disposal proceeds ex VAT in 2027 through Valuehall and "
             "trade buyers, Valuehall's own stock with the excess; euro at the year-end rate) and the borrowing base from "
             "the facility extract's definitions and financial covenant.")
    s.append("2. Conformed the three stock registers to eaches and sterling (AHI case lines at their pack quantity, AHB's "
             "articles through its group-code table, euro at %.4f) and added Valuehall's 31 December stock: GBP %s at "
             "cost." % (f["fx_close"], c(f["stock_at_cost_gbp"]["total"])))
    s.append("3. Netted each line's 2026 despatches and returns to customers (cancelled lines and transfers dropped, AHI "
             "return receipts and case lines in eaches) and took the stock beyond them: GBP %s of excess." %
             c(f["excess_total_gbp"]))
    s.append("4. Measured Valuehall from its store weeks: proceeds over cost of sales %.3f in every year; in full weeks "
             "with at least GBP %s to sell, sales at cost of GBP %s a trading day in every store, January sale "
             "included, flat in the stock held." % (f["valuehall_recovery"], c(f["stocked_threshold_gbp"]),
                                                    c(f["valuehall_per_trading_day_gbp"])))
    s.append("5. Checked that rate on 2023, the year the stores were sent GBP %s and sold GBP %s against GBP %s at the "
             "daily rate; the rest went to trade buyers the following February at the lots' usual %.3f of cost." %
             (c(f["backtest_2023"]["goods_in"]), c(f["backtest_2023"]["sold"]), c(f["backtest_2023"]["predicted"]),
              f["trade_recovery"]))
    s.append("6. Valued 2027: the store plan's %s trading days at the daily rate put GBP %s through Valuehall at %.3f "
             "and the remaining GBP %s through trade buyers at %.3f, a provision of GBP %s." %
             (c(f["store_days_2027"]), c(f["through_valuehall_gbp"]), f["valuehall_recovery"],
              c(f["to_trade_buyers_gbp"]), f["trade_recovery"], mp(f["provision_gbp_m"])))
    s.append("7. For the year before, netted every company's customer lines by division, reading the AHI archive's lines "
             "dated before its July unit change as cases (their invoiced value per unit is the case price) and putting "
             "each of AHL's July price credits, booked on its non-stock code, on the one line of its order whose "
             "overcharge it equals to the penny (the line's quantity times its excess over the customer's price before "
             "the April rise), euro at the year's average of %.4f." % f["fx_avg_2025"])
    s.append("8. Borrowing base %.1f per cent of GBP %s is GBP %s, GBP %s short of the drawn GBP %.2f million: seek "
             "the waiver." % (f["advance_pct"], m(f["inventories_after_provision_gbp_m"]), m(f["borrowing_base_gbp_m"]),
                              ms(f["shortfall_gbp_m"]), f["drawn_gbp_m"]))
    s.append("")
    s.append("## 4. Deliverable Answers\n")
    s.append("### Ashlund_FY2026_stock_provision.xlsx\n")
    s.append("1. Provision: GBP %s." % mp(f["provision_gbp_m"]))
    s.append("2. Inventories after provision: GBP %s." % m(f["inventories_after_provision_gbp_m"]))
    s.append("3. Borrowing base: GBP %s." % m(f["borrowing_base_gbp_m"]))
    s.append("4. Shortfall against the drawn balance: GBP %s." % ms(f["shortfall_gbp_m"]))
    s.append("5. Excess stock at cost by trading company (GBP):")
    for k, nm in SUBN:
        s.append("   - %s: %s" % (nm, c(f["excess_by_company_gbp"][k])))
    s.append("6. Net units shipped to customers in 2025, by division:")
    for k, nm in DIVS:
        s.append("   - %s: %s" % (nm, c(f["units_2025_by_division"][k])))
    s.append("7. Net value invoiced for those shipments by division (GBP):")
    for k, nm in DIVS:
        s.append("   - %s: %s" % (nm, c(f["sales_2025_gbp_by_division"][k])))
    s.append("")
    s.append("### FY2026_stock_provision_note.pdf\n")
    s.append("1. Answer: seek Northgate's waiver of the borrowing base covenant before the accounts are delivered.")
    s.append("2. Provision GBP %s; borrowing base GBP %s; drawn GBP %.2f million; shortfall GBP %s." %
             (mp(f["provision_gbp_m"]), m(f["borrowing_base_gbp_m"]), f["drawn_gbp_m"], ms(f["shortfall_gbp_m"])))
    open(out_path, "w").write("\n".join(s) + "\n")
