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
         "Each carried %s tonnes or more of on-road NOx per mile from October 2025 to September 2026. Every link's "
         "two-weekday count is expanded to the year class by class with the classifying stations' factors, except "
         "the combination trucks on the three terminal access roads (%s), which are the terminals' own drays and "
         "follow the vessel calls: each count is carried to the year by its terminal's gate record, the terminal's "
         "average daily trucks over the year against its trucks on the count days. Expanded with the stations' "
         "factors, a road counted in a busy week or a quiet one keeps that week's level, and the designation would "
         "be %s." % (f["line"], _join(sorted(f["access"])), _join(f["textbook_route"])),
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
         "day's count times the class group's factor for that day's month and weekday; for the combination trucks on "
         "the links %s names as terminal access roads, the mean over the count days of the day's count times the "
         "terminal's average daily trucks_in over the 365 days in %s over its trucks_in that day." % (F["links"],
                                                                                                    F["gates"]),
         "5. NOx per mile: each class group's annual average daily volume times 365 days times its rate in %s, summed "
         "over the groups, in tonnes (rule %s); designated every link at %s or more (rule %s): %s." % (
             F["rates"], sec["nox"], f["line"], sec["line"], _join(des)),
         "6. For the fleet sizing (rule %s), from %s: on each quarter's last day, the registrations in force "
         "(registered_from on or before the day, registered_to blank or on or after it), one truck per vin at its "
         "latest registration; a blank engine_model_year read from the engine_family's model year in %s; counted, "
         "with those of model year 2009 or older, by quarter and, on 30 September 2026, by motor carrier." % (
             sec["fleet"], F["fleet"], F["certs"]),
         "",
         "## 4. Deliverable Answers", "",
         "### %s" % W.GOLDEN["workbook"], "",
         "1. The designated links: %s (%s of %s)." % (_join(des), WORDS[f["n_call"]], WORDS[f["n_links"]])]
    L.append("2. Drayage trucks registered on each quarter's last day, and those with engines of model year 2009 or "
             "older:")
    for q, d in zip(range(1, 5), ("31 December 2025", "31 March 2026", "30 June 2026", "30 September 2026")):
        L.append("   - %s: %s trucks; %s of model year 2009 or older" % (d, fmt(a["trucks"]["Q%d" % q]),
                                                                          fmt(a["old"]["Q%d" % q])))
    L.append("3. On 30 September 2026, by motor carrier:")
    for c in sorted(a["carrier_trucks"]):
        L.append("   - %s: %s trucks; %s of model year 2009 or older" % (c, fmt(a["carrier_trucks"][c]),
                                                                          fmt(a["carrier_old"][c])))
    L += ["", "### %s" % W.GOLDEN["memo"], "",
          "1. The designated links: %s." % _join(des),
          "2. Bar chart of every link's on-road NOx per mile, October 2025 to September 2026, against the %s tonne "
          "line, the designated links' bars in orange." % f["line"]]
    open(out_path, "w", encoding="utf-8").write("\n".join(L) + "\n")
