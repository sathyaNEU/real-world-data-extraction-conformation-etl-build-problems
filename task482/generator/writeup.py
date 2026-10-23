"""submission.md, every figure read from generator/figures.json."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def join(xs, word="and"):
    xs = [str(x) for x in xs]
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " %s " % word + xs[-1]


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    st = f["stations"]
    c = f["components"]
    d = f["default"]
    nb = c["nearest"]
    pr = f["call"]["priority"]
    keys = [p.split()[0] for p in pr]
    dkeys = [p.split()[0] for p in d["priority"]]
    missed = [k for k in keys if k not in dkeys]
    o = []
    o.append("## Tags\n")
    o.append("**Domain:** General Statistics & Data Science, data integration, record linkage and entity resolution (a "
             "city bike-share programme's archive of its operator's station status feed, the operator's trips, fleet "
             "moves and rider fault reports, and its pay-station vendor's sales, work orders, register and alarm log, "
             "conformed into each station's Schedule C availability and pay-station figures for the fourth quarter "
             "of 2026).")
    o.append("**Analytical objective:** Data Extraction & Conformation (ETL).\n")
    o.append("## 1. Final Recommendation\n")
    words = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight"}
    o.append("**The City names %s priority stations for the first quarter of 2027 under Schedule C: %s, each under 90 "
             "per cent availability in October 2026 (%s per cent).**"
             % (words.get(f["call"]["count"], f["call"]["count"]), join(pr), join([st[k]["lowest"] for k in keys])))
    o.append("The station that cleared the line by the least is %s %s, %d per cent in %s, %.1f points above 90. Not %s "
             "alone: the status feed counts a docked bike as available until Northlane marks it out of service, and "
             "bikes that broke on rides and were docked unreported stayed listed while renters took the bikes around "
             "them, so read as the bikes in working order the feed puts %s at %s per cent in October.\n"
             % (nb["station"], nb["name"], nb["availability"], nb["month"], nb["margin_points"],
                join(d["priority"]), join(["%s %s" % (k, st[k]["name"]) for k in missed]),
                join([d["lowest"][k] for k in missed])))
    o.append("## 2. Critical Components\n")
    o.append("1. With each docked bike that broke on a ride counted out of working order from the end of that ride "
             "until a van took it to the depot, the lowest month of Q4 2026 puts %s."
             % join(["%s at **%d** per cent" % (k, st[k]["lowest"]) for k in keys]))
    o.append("2. The feed's available bikes taken as the bikes in working order put them at %s per cent and name %s "
             "alone." % (join([d["lowest"][k] for k in keys]), join(d["priority"])))
    o.append("3. The nearest station above the line is %s %s at **%d** per cent in %s, **%.1f** points clear.\n"
             % (nb["station"], nb["name"], nb["availability"], nb["month"], nb["margin_points"]))
    o.append("## 3. Step-by-Step Solution\n")
    steps = [
        "Mapped each feed station ID to its City station in wellhaven_bike_share_station_list.xlsx (W-17 Linden Avenue "
        "under 117 until its move on the evening of 8 November and 125 after) and read northlane_trips_2026q4.csv once "
        "per trip (its week of 16 November is repeated at the end), its times on Eastern time with a trip in the "
        "repeated hour of 1 November placed by its duration, and northlane_fleet_moves_2026q4.csv with the WHB- prefix "
        "dropped from its bike numbers.",
        "Rebuilt every bike's spells docked at a station from the trips (staff rides too, since they moved bikes) and "
        "the fleet moves: from a ride's end or a van's drop to the next ride's start or a van's pickup, a bike first "
        "recorded leaving a station counted as docked there from the start of the records.",
        "Counted a docked bike out of working order from the end of the ride that left it when renters took other bikes "
        "from its station while it stood there and a van then took it to the depot, where it stayed a day or more "
        "before it was back on the street, and every other docked bike in working order; a bike counted out this way "
        "that a full station's surplus or a storage run took decides no minute, since a bike a rider then took was "
        "docked beside it.",
        "For each station and each minute of service hours (6:00 to midnight Eastern) from October to December 2026, "
        "counted the minute available when a bike in working order was docked at its start (Schedule C, C.1), and "
        "divided each month's available minutes by its service minutes (C.2).",
        "Listed the stations under 90 per cent in a month (C.3): %s; the lowest month above the line is %s's %s, "
        "%d per cent." % (join(keys), nb["station"], nb["month"], nb["availability"]),
        "For pay-station sales, kept paystation_sales_2026q4.csv's sales not voided and sold in the fourth quarter on "
        "Eastern time, and placed each at the pay station its terminal was in when it was sold, from the terminal "
        "replacements in paystation_work_orders_2026q4.xlsx (the export's pay_station column is each terminal's "
        "present pay station in paystation_register_2027-01-08.xlsx).",
        "For the hours without card payments, ran each COMMS_LOST and READER_FAULT alarm in "
        "paystation_alarm_log_2026q4.csv (the register's codes that stop card payments) from its raise to its clear or "
        "to the pay station's next restart, after which a fault still present is raised again in the same second, "
        "merged overlapping alarms and summed the service hours of October to December.",
    ]
    for i, s in enumerate(steps, 1):
        o.append("%d. %s" % (i, s))
    o.append("")
    o.append("## 4. Deliverable Answers\n")
    o.append("### priority_stations_2027q1.xlsx\n")
    o.append("1. The priority stations for Q1 2027: %s." % join(pr))
    o.append("2. Each station's availability in its lowest month of Q4 2026, whole per cent, and whether it is a "
             "priority station:")
    for k in sorted(st):
        o.append("   - %s %s: %d, %s" % (k, st[k]["name"], st[k]["lowest"], "priority" if st[k]["priority"] else "not"))
    o.append("3. The station that cleared the line by the least: %s %s, %d per cent in %s, %.1f points above 90."
             % (nb["station"], nb["name"], nb["availability"], nb["month"], nb["margin_points"]))
    o.append("4. Each station's Q4 2026 pay-station card sales, dollars to the cent:")
    for k in sorted(st):
        o.append("   - %s %s: %s" % (k, st[k]["name"], "{:,.2f}".format(st[k]["sales_cad"])))
    o.append("5. Each station's Q4 2026 service hours its pay station could not take a card payment, whole hours:")
    for k in sorted(st):
        o.append("   - %s %s: %d" % (k, st[k]["name"], st[k]["hours_no_card"]))
    o.append("\n### station_availability_2026q4.html\n")
    o.append("6. A horizontal bar chart of the %d stations' availability in their lowest month of Q4 2026, lowest first, "
             "each bar labelled with its whole per cent and its month, a dashed line at 90 per cent, the %d priority "
             "stations in orange and the rest in grey, with each station's monthly figures in a table beneath."
             % (f["call"]["of"], f["call"]["count"]))
    open(os.path.join(TASK, "submission.md"), "w", encoding="utf-8").write("\n".join(o) + "\n")


if __name__ == "__main__":
    main()
