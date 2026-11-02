"""Writes submission.md from figures.json: every figure in blocks 1 to 4 is one the generator computed.

    python3 task149/generator/writeup.py"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)

ZN = {"KW01": "Kilcarrow city centre", "KW02": "Kilcarrow Docklands", "KW03": "University Hospital campus",
      "KW04": "Kilcarrow University", "KW05": "Carrigboy business park", "KW06": "Port of Kilcarrow, Ringcurran",
      "KW07": "Ballymurragh retail park", "KW08": "Airport business park", "KW09": "Lisnagry and Ardnagree",
      "KW11": "Rest of County Kilcarrow"}
SN = [("ARD", "Ardnagree"), ("LSG", "Lisnagry"), ("KCN", "Kilcarrow Central"), ("KDK", "Kilcarrow Docklands"),
      ("KUH", "University Hospital (with UHK)"), ("CBY", "Carrigboy (with Carrigboy Halt)"),
      ("LINE", "Ardnagree line, all stations' entries added together")]


def fmt(n):
    return "{:,}".format(n)


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    z = sorted(F["zone_boardings"], key=lambda k: -F["zone_boardings"][k])
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** Urban & Regional Science (forecasting: a metropolitan transport authority's weekday commuter "
             "boardings at a new commuter-rail station, built from census place-of-work flows and a mobile network "
             "operator's resident stay panel).")
    L.append("**Analytical objective:** Forecasting & Predictive Modeling.\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**Rathgarvan will carry about %s commuter boardings on an average ordinary weekday in 2029 (to the nearest "
             "100), below the %s that justifies the full scheme, so build the reduced scheme.** A boarding is a journey "
             "to work made on the day, and the catchment's census commuters do not go in every weekday: the panel "
             "shows the Docklands commuters going in on fewer than half of ordinary weekdays and the hospital's and "
             "Carrigboy's on fewer than three in five. Counting each census commuter as a boarding every weekday gives "
             "about %s and the full scheme.\n"
             % (fmt(F["total_boardings"]), fmt(F["threshold"]), fmt(F["census_daily_route_rounded"])))
    L.append("## 2. Critical Components\n")
    L.append("1. Weekday commuter boardings in 2029: **%s** (to the nearest 100), about %s below the full-scheme "
             "threshold of %s." % (fmt(F["total_boardings"]), fmt(F["gap_to_threshold_rounded"]), fmt(F["threshold"])))
    L.append("2. Scope: **reduced scheme**.")
    L.append("3. Boardings by workplace zone (nearest 10): " + "; ".join(
        "%s %s" % (ZN[k], fmt(F["zone_boardings"][k])) for k in z) + ".\n")
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Census 2022 place-of-work tables, final release: commuters from the seven catchment small areas by "
             "workplace zone, held at 2022; home workers, no fixed place and outside the county left out.")
    L.append("2. Panel: stays converted from UTC to Irish time; %d ordinary weekdays from 6 September to 26 November "
             "2027 (October bank holiday and mid-term week out, from the calendar file)." % F["ordinary_weekdays"])
    L.append("3. Each device's usual workplace: the zone (cell lookup, largest area share) of most of its stays of four "
             "hours or more away from its home cell, where it has at least three; each identifier over its own first "
             "to last day.")
    L.append("4. Share of ordinary weekdays each zone's commuters travel there (commuting days over observed days, per "
             "zone): the zones span %d to %d per cent." % tuple(F["zone_weekday_share_range_pct"]))
    L.append("5. Boardings per zone = census commuters x station share (refresh Table 2) x that share; the zones "
             "summed, then rounded once to the nearest 100, give %s; against the threshold of %s, the reduced scheme."
             % (fmt(F["total_boardings"]), fmt(F["threshold"])))
    L.append("6. Arrival shares: on each commuting day, the first stay in any cell of the commuter's workplace zone "
             "(car park, gate or hub stays included), Irish time, from 07:30 up to and including 09:30, over the zone's "
             "commuting days on ordinary weekdays.")
    L.append("7. Station shares: ordinary-weekday entries, September to November, summed per station-day over the "
             "station's codes (UHK with KUH, CBH with CBY) and each gate asset on the days the asset register places "
             "it there; 2027 average over 2019 average; the line as every code summed by day.\n")
    L.append("## 4. Deliverable Answers\n")
    L.append("### rathgarvan_boardings_2029.xlsx\n")
    L.append("1. Weekday commuter boardings, 2029: %s (nearest 100)." % fmt(F["total_boardings"]))
    L.append("2. Boardings by workplace zone (nearest 10):")
    for k in sorted(F["zone_boardings"]):
        L.append("   - %s %s: %s" % (k, ZN[k], fmt(F["zone_boardings"][k])))
    L.append("3. Share of journeys to work on ordinary weekdays arriving in the zone from 07:30 up to and including "
             "09:30 (whole per cent):")
    for k in sorted(F["arrival_share"]):
        L.append("   - %s %s: %d per cent" % (k, ZN[k], F["arrival_share"][k]))
    L.append("4. Average ordinary-weekday entries, September to November 2027 as a share of the same months of 2019 "
             "(whole per cent):")
    for k, n in SN:
        L.append("   - %s: %d per cent" % (n, F["station_ratio"][k]))
    L.append("\n### rathgarvan_demand_note.docx\n")
    L.append("1. Call: about %s commuter boardings on an average ordinary weekday in 2029, below %s, reduced scheme."
             % (fmt(F["total_boardings"]), fmt(F["threshold"])))
    L.append("2. Chart: boardings by workplace zone, the values in item 2 above.")
    open(os.path.join(TASK, "submission.md"), "w").write("\n".join(L) + "\n")
    print("submission.md written")


if __name__ == "__main__":
    main()
