"""submission.md from figures.json: tags, the recommendation, its components, the steps and the deliverable answers."""
import build as B
import golden as GD
import solve as S


def c(x):
    return "{:,}".format(int(x))


QN = {"2025Q3": "July to September 2025", "2025Q4": "October to December 2025", "2026Q1": "January to March 2026",
      "2026Q2": "April to June 2026"}


def write(path, F):
    FL = B.FILES
    o = F["oos_line_days"]
    t = []
    t.append("## Tags\n")
    t.append("**Domain:** Economics and econometrics (structural demand: where a product's demand goes when it is "
             "unavailable).")
    t.append("**Analytical objective:** Opportunity sizing and decision support.\n")
    t.append("## 1. Final Recommendation\n")
    t.append("**Move infant formula onto automated store ordering first: it adds about NZD %s a year to the chain's "
             "formula sales.**" % c(F["call_add"]))
    t.append("Formula's out-of-stock line-days lose their sales outright, because its whole shelf empties when the "
             "supplier's weekly delivery is missed. Not bottled water, which has the most out-of-stock line-days (%s) "
             "and the most sales at its lines' own rates, because its shoppers take another water from the same shelf. "
             "Not dry pet food, because its shoppers buy the missing bag after the restock. Not gluten-free bakery, "
             "which is smaller on every count.\n" % c(o["Bottled water"]))
    t.append("## 2. Critical Components\n")
    t.append("1. Out-of-stock line-days in 2025-26: bottled water **%s**, infant formula "
             "**%s**, dry pet food **%s**, gluten-free bakery **%s**." % (c(o["Bottled water"]), c(o["Infant formula"]),
                                                                          c(o["Dry pet food"]),
                                                                          c(o["Gluten-free bakery"])))
    t.append("2. Every one of formula's **%s** out-of-stock line-days falls on the **%s** store-days all %d of its "
             "lines were out." % (c(o["Infant formula"]), c(F["win_whole_shelf_store_days"]), F["win_lines"]))
    t.append("3. Formula adds about **NZD %s** a year, the most of the four." % c(F["call_add"]))
    t.append("\n## 3. Step-by-Step Solution\n")
    t.append("1. Mapped each till code in %s to its article with %s (article numbers to 2 March 2025, GTINs from 3 "
             "March, two pack changes) and joined the sales to %s by store, article and day." % (FL["pos"], FL["codes"],
                                                                                           FL["stock"]))
    t.append("2. Marked each line-day that opened with on_hand_open at zero on a day the store traded (the two refit "
             "weeks have no sales and are left out): %s, %s, %s and %s out-of-stock line-days for water, formula, pet "
             "food and gluten-free bakery in 2025-26." % (
                 c(o["Bottled water"]), c(o["Infant formula"]), c(o["Dry pet food"]), c(o["Gluten-free bakery"])))
    t.append("3. Took a line's expected units on a day as its mean on the same weekday within four weeks either side, "
             "over days it was on the shelf, outside the fortnight after its own restock and with no other line of its "
             "category out (eight weeks either side where four hold fewer than two such days).")
    t.append("4. Took each category's loss as its out lines' expected units on their out days, less its lines' units "
             "above expectation on days another of its lines was out and in the fortnight after their own restock, at "
             "each line's shelf_price_fy2026 in %s, and halved it per %s: formula about NZD %s, the most of the four."
             % (FL["lines"], FL["plan"], c(F["call_add"])))
    t.append("5. In %s took on_hand as the opening stock up to 1 February 2026 and as the closing stock from 2 February "
             "(only from then does a line sell on a day it shows nothing on hand), so a day's opening after go-live is "
             "the previous day's close plus that morning's delivery; counted each trial store's line-days that opened "
             "with nothing in the 13 weeks either side." % FL["trial"])
    t.append("6. In %s counted the stops arriving after the store opened: at 6:30 up to 31 March 2026 and at 7:00 "
             "from 1 April, the half hours the first sales in %s start from (%s gives the current 7:00), totalled by "
             "island." % (FL["stops"], FL["trading"], FL["stores"]))
    t.append("7. Joined each delivery_ref in %s to its appointment in %s and took each appointment's pallets once (the "
             "receiving system books a truck's pallets onto every line under every dispatch advice it carried), totalled by "
             "category and month of receipt." % (FL["grn"], FL["dock"]))
    t.append("\n## 4. Deliverable Answers\n")
    t.append("### %s\n" % GD.DECK)
    t.append("1. Move infant formula onto automated store ordering first: about NZD %s a year." % c(F["call_add"]))
    t.append("2. Bar chart of the sales each of the four categories adds a year, infant formula highlighted and "
             "labelled about NZD %s." % c(F["call_add"]))
    t.append("\n### %s\n" % GD.XLSX)
    t.append("1. Breakfast cereal out-of-stock line-days after the system went live (2 February to 3 May 2026), and "
             "their per cent change from the 13 weeks before, by trial store:")
    for s in S.TRIAL_STORES:
        v = F["ask_trial"][str(s)]
        t.append("   - %s: %s line-days, %.1f per cent" % (F["store_names"][str(s)], c(v["after"]), v["change_pct"]))
    t.append("2. Distribution centre deliveries that reached a store after it opened, 1 July 2025 to 30 June 2026, by "
             "island:")
    for g, v in F["ask_late_stops"].items():
        t.append("   - %s Island: %s" % (g, c(v)))
    t.append("3. Pallets the distribution centre received from each category's suppliers, by month of receipt, July "
             "2025 to June 2026:")
    for k in S.DC_CATS:
        v = F["ask_pallets"][k]
        t.append("   - %s: %s" % (k, ", ".join(c(v[m]) for m in S.MONTHS)))
    open(path, "w").write("\n".join(t) + "\n")
