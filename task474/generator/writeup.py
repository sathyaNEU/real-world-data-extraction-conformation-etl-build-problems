"""submission.md, drafted from generator/figures.json: every figure the write-up states comes from there."""
import json

import world as W

TAGS = ("**Domain:** Physical & Environmental Sciences (emissions inventory: an on-road NOx inventory by roadway link, "
        "each link's vehicle-miles by class expanded from short classification counts with continuous count station "
        "factors).\n"
        "**Analytical objective:** Data Extraction & Conformation (ETL).")
WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
         10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen"}


def fmt(n):
    return "{:,}".format(int(n))


def _join(xs):
    return ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else xs[0]


def write(fig_path, out_path):
    f = json.load(open(fig_path, encoding="utf-8"))
    F = W.FILES
    des, sec, a = f["call"], f["sections"], f["asks"]
    L = ["## Tags", "", TAGS, "",
         "## 1. Final Recommendation", "",
         "**Designate %s of the %s port roadway links for the 2027 Air Corridor Program: %s.**" % (
             WORDS[f["n_call"]], WORDS[f["n_links"]], _join(des)),
         "Each carried %s tonnes or more of on-road NOx per mile from October 2025 to September 2026 once each link's "
         "two-weekday count is expanded to the year class by class: trucks with the monthly and day-of-week factors "
         "the classifying stations measure for trucks, cars with those for cars. Trucks run well above their annual "
         "average on weekdays and are nearly flat by season, so expanding a weekday count with all-vehicle factors "
         "and splitting it by the counted truck share carries too many trucks into the year and designates %s." % (
             f["line"], _join(f["textbook_route"])),
         "",
         "## 2. Critical Components", "",
         "1. Links at or above %s tonnes of NOx per mile: **%d** of %d." % (f["line"], f["n_call"], f["n_links"]),
         "",
         "## 3. Step-by-Step Solution", "",
         "1. Took every link in %s (rule %s) and its two count days, both directions, from the programme and site the "
         "register names: %s (hourly), %s (15-minute sheets, one per site) and %s (hourly by lane), as passenger "
         "(1-3), single-unit (4-7) and combination (8-13) daily totals." % (F["links"], sec["links"], F["dot"],
                                                                            F["county"], F["consultant"]),
         "2. From %s, each classifying station in %s, both directions summed by date and class group, days with no "
         "record left out." % (F["stations"], F["register"]),
         "3. For each class group, each classifying station's factor for each month and day of week: its average "
         "daily volume over the year divided by its average volume on that month's days of that weekday; the "
         "group's factor the average over the four classifying stations.",
         "4. Each link's annual average daily volume for each class group: the mean over its two count days of the "
         "day's count times the class group's factor for that day's month and weekday.",
         "5. NOx per mile: each class group's annual average daily volume times 365 days times its rate in %s, summed "
         "over the groups, in tonnes (rule %s); designated every link at %s or more (rule %s): %s." % (
             F["rates"], sec["nox"], f["line"], sec["line"], _join(des)),
         "6. For the terminal operations review (rule %s), from %s: Berth 20's gate_in moved an hour later in the "
         "daylight-time months (its in-gate keeps standard time, its out-gate local time); at Pacific Gateway a "
         "transaction sharing its container_no and gate_in with a later transaction_id under another tag is the "
         "voided first keying and is dropped; at Berth 40 a leg out through the rail ramp gate (out_lane RG1) and "
         "the tag's next leg in through it (in_lane RG1) are one stay; then each tag's overlapping transactions at a "
         "terminal merged into one visit from its first gate_in to its last gate_out, and visits counted and turn "
         "minutes averaged by terminal and the quarter of the gate_in date." % (sec["gates"], F["gates"]),
         "",
         "## 4. Deliverable Answers", "",
         "### %s" % W.GOLDEN["workbook"], "",
         "1. Every link, designated or not:"]
    for k in f["links"]:
        L.append("   - %s: %s" % (k, "designated" if k in des else "not designated"))
    L.append("2. Every terminal and quarter: truck visits and average turn time (minutes, one decimal):")
    for t in sorted(f["terminals"]):
        for q in range(1, 5):
            k = "%s Q%d" % (t, q)
            L.append("   - %s, %s: %s visits; %.1f minutes" % (
                f["terminals"][t], f["quarters"][str(q)], fmt(a["visits"][k]), a["turn"][k]))
    L += ["", "### %s" % W.GOLDEN["memo"], "",
          "1. The designated links: %s." % _join(des),
          "2. Bar chart of every link's on-road NOx per mile, October 2025 to September 2026, against the %s tonne "
          "line, the designated links' bars in orange." % f["line"]]
    open(out_path, "w", encoding="utf-8").write("\n".join(L) + "\n")
