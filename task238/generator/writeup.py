"""Emits task238/submission.md from generator/figures.json, so no figure is typed."""
import datetime as dt
import json
import os

import params as P

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
NAMES = {101: "Quinpool Road", 102: "Spryfield", 103: "Clayton Park", 104: "Bedford Place",
         105: "Dartmouth - Portland St", 106: "Cole Harbour", 107: "Lower Sackville", 201: "Truro (Prince St)",
         202: "New Glasgow", 203: "Antigonish", 204: "Kentville", 205: "Bridgewater", 206: "Yarmouth",
         207: "Amherst"}


WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"}


def pct(x):
    return "%.1f%%" % x


def dollars(x):
    return "$" + format(int(x), ",")


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    w = F["watch"]
    acc = F["accuracy"]
    near = F["nearest_off"]
    names = ", ".join("%s (%d)" % (NAMES[s], s) for s in w[:-1]) + " and %s (%d)" % (NAMES[w[-1]], w[-1])
    accs = ", ".join(pct(acc[str(s)]) for s in w[:-1]) + " and " + pct(acc[str(w[-1])])
    L = []
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** General Statistics & Data Science, missing data, censoring and measurement error "
             "(retail price integrity).")
    L.append("**Analytical objective:** Data Quality Monitoring & Alerting.")
    L.append("")
    L.append("## 1. Final Recommendation")
    L.append("")
    L.append("**Put %s on Price Watch for the first quarter of 2027.**" % names)
    extra = [s for s in F["checkshare_route"] if s not in w]
    assert extra and all(s in F["checkshare_route"] for s in w), "the check-share route must add stores to the set"
    extra_names = " and ".join("%s (%d)" % (NAMES[s], s) for s in extra)
    L.append("Their fourth-quarter price accuracy is %s against the 99.0%% line, and %s (%d) is the nearest store "
             "to stay off at %s. Not the weekly random price audits, which check labels at random moments and put "
             "every store at %s or more. Not the Thursday checks' share of labels still at the old price, which "
             "also puts %s on." % (accs, NAMES[near], near, pct(F["nearest_off_acc"]), pct(F["audit_route_floor"]),
                                  extra_names))
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    k = 1
    for s in w:
        L.append("%d. %s (%d) price accuracy for Q4 2026 is **%s**" % (k, NAMES[s], s, pct(acc[str(s)])))
        k += 1
    L.append("%d. %s (%d), the nearest store above the line, is at **%s**" % (k, NAMES[near], near,
                                                                             pct(F["nearest_off_acc"])))
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    fl = P.FILES
    steps = [
        "Totalled each store's item scans from 1 October to 31 December 2026 in %s." % fl["hourly"],
        "For each changeover Thursday took each store's completed PCB batch (print time read in local time, label "
        "count) from %s and the units its price-changed items scanned that Thursday from %s."
        % (fl["printer"], fl["movement"]),
        "Read the hanging pace from %s: the share of checked labels still at the old price falls from all of them "
        "at the print to none once the batch is up, at one pace for every store." % fl["checks"],
        "Spread each changeover's changed-item units over that Thursday's hours as the store's own hourly scans, "
        "and counted as off the label the units scanned before the batch printed and, while it was going up, the "
        "share of its labels not yet hung.",
        "Added stray labels at the share %s finds outside changeovers, and took price accuracy as one minus the "
        "off-label scans over the item scans (PI-2 s.3.1): %s below 99.0%%, %s (%d) nearest above at %s (s.4.1)."
        % (fl["audits"], names, NAMES[near], near, pct(F["nearest_off_acc"])),
        "Scanner Code payouts: SC overrides in %s (original less override price, UTC converted to local, in the "
        "quarter) plus Scanner Code refunds in %s, a desk refund dropped only when it repeats a register payout of "
        "the same amount on the same receipt line and kept when it pays the rest of the Code remedy (s.5.1)."
        % (fl["overrides"], fl["desk"]),
        "Flyer prices: every advertised UPC of %s (an assorted line's varieties matched by brand, product and size "
        "among the week's AD START items) against the register price in force each day in each zone, the REVISED "
        "sheet of %s until a correction in %s takes effect at opening on its date, per unit for multi-buys, with "
        "the price paid above the flyer times that day's units in that zone from %s."
        % (fl["adplan"], fl["pricefile"], fl["corrections"], fl["adsales"]),
        "Put the %s stores below 99.0%% on Price Watch." % WORDS[F["n_watch"]],
    ]
    for i, s in enumerate(steps, start=1):
        L.append("%d. %s" % (i, s))
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append("### price_watch_2027q1.xlsx")
    L.append("")
    L.append("1. Price Watch for Q1 2027, with each Price Watch store's Q4 2026 price accuracy:")
    for s in sorted(int(x) for x in acc):
        if s in w:
            L.append("   - %d %s: Price Watch, %s" % (s, NAMES[s], pct(acc[str(s)])))
        else:
            L.append("   - %d %s: stays off" % (s, NAMES[s]))
    L.append("2. Dollars paid out under the Scanner Price Accuracy Code in Q4 2026, to the nearest dollar:")
    for s in sorted(int(x) for x in F["payouts"]):
        L.append("   - %d %s: %s" % (s, NAMES[s], dollars(F["payouts"][str(s)])))
    L.append("3. Flyer weeks that started in the quarter: advertised UPCs that rang up at a price other than the "
             "flyer price, and dollars customers paid above the flyer price that week:")
    for d in sorted(F["flyer_count"]):
        dd = dt.date.fromisoformat(d)
        n_ = F["flyer_count"][d]
        what = "none" if n_ == 0 else ("1 UPC" if n_ == 1 else "%d UPCs" % n_)
        L.append("   - Week of %d %s %d: %s, %s" % (dd.day, dd.strftime("%B"), dd.year, what,
                                                   dollars(F["flyer_over"][d])))
    L.append("")
    L.append("### price_accuracy_q4_2026.svg")
    L.append("")
    L.append("1. Dot chart of every store's Q4 2026 price accuracy against the dashed 99.0%% Price Watch line, the "
             "%s Price Watch stores in orange with their accuracy labelled, the others in blue." % WORDS[F["n_watch"]])
    L.append("")
    open(os.path.join(TASK, "submission.md"), "w").write("\n".join(L))


if __name__ == "__main__":
    main()
