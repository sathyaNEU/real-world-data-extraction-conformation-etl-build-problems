"""submission.md, drafted from generator/figures.json so every figure it states is one the generator computed.

    python3 task280/generator/writeup.py"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
ORDER = ["BW", "CM", "DF", "EH", "GH", "KB", "LM", "SC"]
WORD = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six"}


def joined(xs):
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    hb = f["hubs"]
    des = f["call"]["designated"]
    dp = f["default_path"]
    dps = f["default_path_set"]
    nm = lambda h: hb[h]["name"]
    near_under = f["call"]["nearest_under"]
    flipped = [h for h in des if h not in dps]
    cov = f["coverage"]
    out = ["## Tags", "",
           "**Domain:** General Statistics & Data Science (missing data, censoring and measurement error).",
           "**Analytical objective:** Descriptive & Distribution Analysis.", "",
           "## 1. Final Recommendation", "",
           "**Designate %s of Tollard's eight hubs for 2027 under Schedule 4: %s.**"
           % (WORD[len(des)], joined([nm(h) for h in des])),
           "Their panel households' connections delivered under 80 per cent of plan for %s per cent of the weekday "
           "evening peak; %s, the highest of the rest, for %d per cent. Not %s alone, which the share of the completed "
           "tests gives (%s): a unit runs no test in an hour while the household's own line stays busy, and the "
           "households are busiest on the nights their nodes carry the most traffic, so the tests that ran sat at "
           "lighter loads than the peak as a whole (%s). Weighting each evening hour or each night equally does not "
           "remove it; counting every test not run as a failure designates all eight hubs."
           % (joined(["%d" % hb[h]["share"] for h in des]), nm(near_under), hb[near_under]["share"],
              joined([nm(h) for h in dps]), "; ".join("%s %d per cent" % (nm(h), dp[h]) for h in ORDER if dp[h] >= 15),
              "; ".join("%s %.1f against %.1f per cent average node load" % (nm(h), 100 * cov[h]["load_tested"],
                                                                             100 * cov[h]["load_all"])
                        for h in flipped)),
           "",
           "## 2. Critical Components", "",
           "1. Share of the weekday evening peak below 80 per cent of plan: %s." % "; ".join(
               "%s **%d** per cent" % (nm(h), hb[h]["share"]) for h in ORDER),
           "2. Average node utilisation in the hub's tested weekday peak intervals against every weekday peak "
           "interval of its panel households: %s; lighter in every hub." % "; ".join(
               "%s **%.1f** against **%.1f** per cent" % (nm(h), 100 * cov[h]["load_tested"], 100 * cov[h]["load_all"])
               for h in flipped),
           "3. Each household's tests were read against its node's utilisation in the tested interval and carried to "
           "every weekday peak interval of the window from the node's filing (per plan, the load above which the "
           "connection fell under 80 per cent of plan), each of the **%s** panel households counted equally."
           % format(f["totals"]["households"], ","),
           "",
           "## 3. Step-by-Step Solution", "",
           "1. Took Schedule 4, 3.1 and 3.2, with its definitions (1.2 to 1.8): every weekday interval from 7 to 11 pm "
           "local time, 14 September to 13 November 2026, of every panel household served from the hub, each "
           "household counted equally; designated above 20 per cent.",
           "2. Kept the %s panel households (enrolled before 14 September and still in the panel at 13 November), gave "
           "each test to its household through panel_units.csv, and dropped tests received twice."
           % format(f["totals"]["households"], ","),
           "3. Put each test in its UTC interval from its own offset, and read its node on the day "
           "(tollard_address_node_table.csv), the node's utilisation in that interval and the plan in force "
           "(tollard_subscription_history.csv, tollard_plan_catalogue.csv).",
           "4. Compared the node loads of the tested intervals with every weekday peak interval: the tests ran at "
           "lighter loads in every hub.",
           "5. For each household and plan, found the node load above which its tests fell under 80 per cent of plan "
           "and counted its node's weekday peak intervals above it; averaged the households by hub.",
           "6. For credits, merged each node's overlapping unplanned tickets into one outage, kept outages of four "
           "hours or more that began in the window (local time), and charged a day for each started 24 hours to the "
           "node's subscribers at the end of the month before.",
           "7. For capacity added, summed each hub's register capacity in service on 13 November less 14 September, "
           "leaving out the second records of the split nodes (the same children a day later, with no subscribers).",
           "",
           "## 4. Deliverable Answers", "",
           "### hub_peak_congestion_2026.xlsx", "",
           "1. Share of the weekday evening peak below 80 per cent of plan (whole per cent) and designation:"]
    for h in ORDER:
        out.append("   - %s: %d per cent, %s" % (nm(h), hb[h]["share"],
                                                "designated" if hb[h]["designated"] else "not designated"))
    out.append("2. Outage credits owed for unplanned outages that began in the window (subscriber-days):")
    for h in ORDER:
        out.append("   - %s: %s" % (nm(h), format(hb[h]["outage_credit_subscriber_days"], ",")))
    out.append("3. Downstream capacity added during the window (Mbit/s):")
    for h in ORDER:
        out.append("   - %s: %s" % (nm(h), format(hb[h]["capacity_added_mbps"], ",")))
    out += ["", "### hub_peak_congestion_2026.png", "",
            "1. One bar chart of the eight hubs' shares of the peak below 80 per cent of plan against the 20 per cent "
            "line, the %s designated hubs (%s) highlighted." % (WORD[len(des)], joined([nm(h) for h in des]))]
    with open(os.path.join(TASK, "submission.md"), "w") as fh:
        fh.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
