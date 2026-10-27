"""submission.md from generator/figures.json: the five blocks, every figure taken from the generator's own output."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import asks as AK  # noqa: E402
import common as K  # noqa: E402


def usd(x):
    return "USD %s" % format(int(round(x)), ",")


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    A = lambda q, k: f["askA.%s.%s" % (q, k)]
    B = lambda q, k: f["askB.%s.%s" % (q, k)]
    out = ["## Tags", "",
           "**Domain:** Actuarial Science & Insurance, pricing, ratemaking and credibility (the lifetime loss ratio of a "
           "vehicle service contract channel's next year of sales, costed per mile of exposure at the odometer, for its "
           "renewal election under the obligor's rate manual).",
           "**Analytical objective:** Forecasting & Predictive Modeling.", "",
           "## 1. Final Recommendation", "",
           "**Copperline should renew the Fareline channel on 1 January 2027 with the maximum high-use surcharge.**",
           "A 2027 Fareline contract is forecast to cost about %d per cent of its price in claims over its cover at "
           "current rates, over the rate manual's 70 per cent standard, and about %d per cent at the price with the 40 "
           "per cent surcharge, inside it. Repair claims accrue per mile and climb steeply with the odometer past "
           "70,000 miles; a Fareline driver buys cover on a car at about %s miles and drives about %s miles a year, so "
           "the 75,000 covered miles run out in about %d months at odometers the channel's own six months have not "
           "reached, and the cover is costed per mile at each odometer from the whole book, which has driven them." % (
               f["lr.current_price_pct_nearest_5"], f["lr.surcharged_price_pct_nearest_5"],
               format(f["fareline.odometer_at_sale_nearest_1000"], ","), format(f["fareline.annual_miles_nearest_1000"], ","),
               f["fareline.months_to_limit_nearest_1"]),
           "", "## 2. Critical Components", "",
           "1. Claims cost per 1,000 miles driven under cover, whole book 2019 to September 2026: about **USD %.1f** "
           "below 70,000 miles on the odometer and climbing past it (the workbook's cost per mile sheet, by 10,000-mile "
           "band)." % f["cpm_per_1000.under_70000_usd"],
           "2. A 2027 contract's claims cost over its cover, each 2026 Fareline contract run from its odometer at sale "
           "at its own annual mileage to the earlier of 75,000 miles and 60 months: about **%s** against an average "
           "price of about **%s**, a lifetime loss ratio of **%d per cent** at current rates and **%d per cent** with "
           "the surcharge (every banding of the odometer and every treatment of the last reading gives %.1f to %.1f "
           "per cent at current rates)." % (
               usd(f["lifetime.claims_cost_usd_nearest_100"]), usd(f["lifetime.average_price_usd_nearest_10"]),
               f["lr.current_price_pct_nearest_5"], f["lr.surcharged_price_pct_nearest_5"], f["standing.lr_min_pct"],
               f["standing.lr_max_pct"]),
           "3. The forecast rests on the **%s** 2026 Fareline contracts with a weekly feed reading after their sale "
           "date." % format(f["fareline.contracts_2026"], ","),
           "", "## 3. Step-by-Step Solution", "",
           "1. Joined %s, %s (contract numbers before 4 March 2024 to their new numbers), %s and %s (Fareline's weekly "
           "feed by VIN to its contract) on the contract." % (K.REGISTER, K.CROSSWALK, K.CLAIMS, K.READINGS),
           "2. Claims cost per claim: parts and labour lines net of the deductible line and of reversed lines, goodwill "
           "left out (rate manual 4), at the repair order's odometer.",
           "3. Miles under cover: each contract's odometer path from the sale through its readings in cover to its last "
           "reading, stopped at 75,000 miles from the odometer at sale, split by 10,000-mile odometer band.",
           "4. Cost per mile in each band: the band's claims cost over its miles under cover, whole book.",
           "5. Each 2026 Fareline contract's annual mileage from its weekly feed; its cover runs from its odometer at "
           "sale to the earlier of 75,000 miles and 60 months at that mileage, costed band by band; averaged over the "
           "contracts and divided by their average price, then by 1.4 for the surcharged price (rate manual 3 and 5).",
           "6. For the cancellations, took each contract's first request received (contract terms 5): a dealer's or "
           "owner's by contract number, a lienholder's payoff request as the contract on that VIN showing that "
           "lienholder (a VIN resold carries the next owner's contract too), and the refund by the terms' formula with "
           "the request's odometer or the latest reading on or before it; a contract showing a lienholder refunds to it.",
           "7. For the dealer premium, read the three bordereau layouts (Brazos in cents, the independents by VIN and "
           "day-first sale date), and took as not received each dealer-month payment the bank returned, matched in %s "
           "on the dealer's name in %s, the settlement month and the payment's total; a payment re-sent on a later "
           "bordereau is received." % (K.RETURNS, K.DEALERS),
           "", "## 4. Deliverable Answers", "",
           "### %s" % K.DECK, "",
           "1. Election for 1 January 2027: %s." % f["call.election"],
           "2. Lifetime loss ratio of 2027 Fareline sales: about %d per cent at current rates, about %d per cent with "
           "the 40 per cent surcharge." % (f["lr.current_price_pct_nearest_5"], f["lr.surcharged_price_pct_nearest_5"]),
           "3. Chart: claims cost per 1,000 miles by odometer band, flat at about USD %.1f to 70,000 miles and climbing "
           "past it, the bands a Fareline cover runs through marked." % f["cpm_per_1000.under_70000_usd"],
           "", "### %s" % K.BOOK, "",
           "1. Retail contracts cancelled and refunds owed: %s." % "; ".join(
               "%s %d contracts, %s, of which %s to lienholders" % (q, A(q, "contracts_cancelled"),
                                                                   usd(A(q, "refunds_usd")),
                                                                   usd(A(q, "refunds_to_lienholders_usd")))
               for q in AK.QA),
           "2. Retail contracts sold in 2025, premium received from dealers to 30 September 2026 and outstanding: %s." % (
               "; ".join("%s %s received, %s outstanding" % (q, usd(B(q, "premium_received_usd")),
                                                              usd(B(q, "premium_outstanding_usd"))) for q in AK.QB)),
           ""]
    s = "\n".join(out)
    assert "\u2014" not in s and "\u2013" not in s
    open(os.path.join(TASK, "submission.md"), "w").write(s)


if __name__ == "__main__":
    main()
