"""Emit submission.md from figures.json (every figure is read, none typed)."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)

PERIODS = ["10 Feb to 9 Mar 2025", "10 Mar to 6 Apr 2025", "7 Apr to 4 May 2025"]
STATIONS = ["Westgate", "Centre Square", "Union Yards", "Millbrook", "Fairgrounds", "Cobb Street", "Ashford Road",
            "Ridgeview", "Prairie Gate"]
WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight"}


def dlist(ds):
    if len(ds) == 1:
        return "district %s" % ds[0]
    return "districts %s and %s" % (", ".join(ds[:-1]), ds[-1])


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    t = {x["label"]: x for x in f["teams"]}
    e, h, c = t["Eastline group"], t["Hollin station group"], t["Cobb Street station group"]
    s = [x for x in f["teams"] if x["label"].startswith("District")][0]
    L = []
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** Criminology and justice, crime incidence and hotspot analysis (offender series linkage).")
    L.append("**Analytical objective:** Anomaly detection and diagnostics.")
    L.append("")
    L.append("## 1. Final Recommendation")
    L.append("")
    L.append("**The summer plan should stand up %s series teams: the Eastline group's team on %s, the Hollin station "
             "group's on %s, the Cobb Street station group's on %s and the %s's on %s.**"
             % (WORDS[f["n_teams"]], dlist(e["districts"]), dlist(h["districts"]), dlist(c["districts"]),
                s["label"].replace("District", "district"), dlist(s["districts"])))
    L.append("The Eastline group's %d offences are one series because %d westbound trains each carried two or three of "
             "its snatches at different stations. Not %s teams, one per station cluster, which splits that group four "
             "ways by straight-line distance. Not %s teams, which folds the Cobb Street group into it although on %s "
             "evenings the two struck within three minutes of each other at stations no train joins in that time."
             % (e["n"], f["eastline_trips"], WORDS[f["rung0_teams"]], WORDS[f["rung2_teams"]],
                WORDS[f["simultaneous_evenings"]]))
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    L.append("1. The Eastline group is **%d** offences on the platforms at Ridgeview, Ashford Road, Millbrook and Union "
             "Yards, joined by **%d** westbound train trips that each carried two or three of them; its ground is "
             "**%s**." % (e["n"], f["eastline_trips"], dlist(e["districts"])))
    L.append("2. The Cobb Street station group is a separate group of **%d** offences on **%s**: none of its snatches "
             "sits on one of those trips, and on **%d** evenings it struck within three minutes of the Eastline group at "
             "Union Yards." % (c["n"], dlist(c["districts"]), f["simultaneous_evenings"]))
    L.append("3. The Hollin station group is **%d** offences on **%s** and the %s **%d** offences on **%s**."
             % (h["n"], dlist(h["districts"]), s["label"].replace("District", "district"), s["n"], dlist(s["districts"])))
    L.append("4. Patrol **%s** have no series in the review period." % dlist(f["no_series_districts"]).replace("districts", "districts"))
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    L.append("1. Took robbery and theft from the person with a phone taken (OPS-41 section 2) from "
             "rms_occurrence_extract_20260511.csv by occurred_from_local, 9 February to 3 May 2026, with the transit "
             "officer reports in tpo_occurrence_log_2025_2026.xlsx not already filed with the Service, and kept the "
             "%d with two or more suspects (an offender group, section 3)." % f["n_group_scope"])
    L.append("2. Linked those offences on method, overlapping suspect ages, %d km and %d days: %s local series, one each "
             "at Ridgeview, Ashford Road, Millbrook, Union Yards, Cobb Street and Hollin and one of street robberies in "
             "district 6." % (f["linkage_km"], f["linkage_days"], WORDS[f["rung0_teams"]]))
    L.append("3. Placed each platform offence on the train trips leaving its station within three minutes of "
             "occurred_from_local, from the gtfs/ feed with frequencies.txt expanded and calendar_dates.txt applied: "
             "%d trips each carry two or three offences at different stations and join the Ridgeview, Ashford Road, "
             "Millbrook and Union Yards series into one group of %d." % (f["eastline_trips"], e["n"]))
    L.append("4. Kept Cobb Street apart: no trip carries one of its offences with another, and %s of its offences fell "
             "within three minutes of an Eastline group offence at Union Yards." % WORDS[f["simultaneous_evenings"]])
    L.append("5. Took each group's ground from its offences' coordinates in patrol_districts_2026.geojson (OPS-41 "
             "section 4): %s teams." % WORDS[f["n_teams"]])
    L.append("6. 2025 comparison: put each 2025 RMS offence in its 2026 district by coordinates, read each transit "
             "officer station code as the station whose gate array carried that code on the day "
             "(fare_gate_daily_summary_2025.csv with carvale_transit_codes.xlsx), dropped reports referred to the "
             "Service that match an RMS file at the same station, and counted by Mountain-time date: %d offences."
             % f["ask_a_total"])
    L.append("7. Station figures: summed fare_gate_entries_hourly_2026.csv by gate array (codes were renumbered on 29 "
             "March) on Mountain-time dates, and counted every Eastline stop_times call with frequencies.txt trips "
             "expanded and calendar_dates.txt holiday services applied, in the twelve weeks.")
    L.append("8. Recommendation: the %s teams in block 1." % WORDS[f["n_teams"]])
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append("### series_assessment_2026.xlsx")
    L.append("")
    L.append("1. Series teams, %d, with ground and series offences in the review period:" % f["n_teams"])
    for x in f["teams"]:
        L.append("   - %s: %s, %d offences" % (x["label"], dlist(x["districts"]), x["n"]))
    L.append("2. Robbery and theft from the person with a phone taken, 2026 patrol districts, same twelve weeks of 2025:")
    for d, v in sorted(f["ask_a"].items(), key=lambda kv: int(kv[0][1:])):
        L.append("   - District %s: %d (%s), %d (%s), %d (%s)" % (d[1:], v[0], PERIODS[0], v[1], PERIODS[1], v[2], PERIODS[2]))
    L.append("3. Eastline stations, 9 February to 3 May 2026, fare-gate entries and scheduled Eastline train calls in "
             "both directions:")
    for st in STATIONS:
        L.append("   - %s: %s entries, %s train calls" % (st, format(f["ask_b"][st], ","), format(f["ask_c"][st], ",")))
    L.append("")
    L.append("### summer_series_deployment_memo.docx")
    L.append("")
    L.append("1. One-page memo to the deputy chief recommending the %s series teams and their ground as in item 1 above, "
             "with the reason the Eastline group is one group and the Cobb Street group another." % WORDS[f["n_teams"]])
    L.append("")
    open(os.path.join(TASK, "submission.md"), "w").write("\n".join(L))


if __name__ == "__main__":
    main()
