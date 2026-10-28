"""task270 submission.md, drafted from figures.json: every number in it is a value the build computed."""
from __future__ import annotations

import os

import common as K


def _list(names):
    names = list(names)
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]


def write(task_dir, F):
    areas = sorted(K.AREA_NAMES)
    by_e = sorted(F["call"], key=lambda a: (F["e85"][a], a))
    e = F["e85"]
    L = []
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** Sociology & Demography (fertility, mortality and life table estimation).")
    L.append("**Analytical objective:** Descriptive & Distribution Analysis.")
    L.append("")
    L.append("## 1. Final Recommendation")
    L.append("")
    L.append("**The 2028 to 2030 late-life frailty program should go to %s, the four areas whose life expectancy at 85 "
             "under their 2024 to 2026 death rates is below seven years.**" % _list(by_e))
    L.append("Their figures run from %.1f years (%s) to %.1f (%s), and the nearest area above the line is %s at %.1f. "
             "Not Spraymouth: splitting its 85-and-over population by its 2021 census ages puts it below the line, but "
             "its late-eighties cohorts of 2021 are now in their nineties and rebuilt by age it reads %.1f. Not on the "
             "census split either for Saltwick Shoals and Dunesford, which it puts above seven years because the coast's "
             "cohorts that turned 85 after census night are left out of their 85-and-over groups."
             % (e[by_e[0]], by_e[0], e[by_e[-1]], by_e[-1], F["nearest_above"], F["nearest_above_e85"],
                e["Spraymouth"]))
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    L.append("1. Saltwick Shoals' life expectancy at 85 is **%.1f years** and Dunesford's **%.1f years**"
             % (e["Saltwick Shoals"], e["Dunesford"]))
    L.append("2. Spraymouth's life expectancy at 85 is **%.1f years**" % e["Spraymouth"])
    L.append("3. Windermoor's is **%.1f years** and Coldwater Plains' **%.1f years**" % (e["Windermoor"],
                                                                                     e["Coldwater Plains"]))
    L.append("4. The nearest area above the line, %s, is at **%.1f years**" % (F["nearest_above"],
                                                                            F["nearest_above_e85"]))
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    L.append("1. Took every death of a usual resident that occurred in 2024, 2025 or 2026 from %s and %s, each "
             "resident's area from the usual residence's 2021 SA2 by %s, ages in completed years from 85 to 94 and 95 "
             "and over (guidelines 3.3): %s deaths at 85 and over across the twelve areas."
             % (K.F_DEATHS, K.F_INTERSTATE, K.F_CORR, "{:,}".format(F["deaths_85plus_total"])))
    L.append("2. Rebuilt each area's population at each age at 30 June 2024, 2025 and 2026 from %s (SA2s summed to "
             "areas): each census age followed forward as its birth window, the 41 of 365 days born 1 July to 10 "
             "August a year younger at 30 June, less that window's deaths since census night, each year's 85-and-over "
             "total brought to the estimate in %s." % (K.F_CENSUS, K.F_ERP))
    L.append("3. Built each area's life table by single year to 94 with 95 and over closed on its own rate and half a "
             "year lived in the year of death (guidelines 3.2): life expectancy at 85 runs from %.1f years (%s) to %.1f "
             "(%s)." % (F["lowest_e85"], F["lowest"], F["highest_e85"], F["highest"]))
    L.append("4. Named the areas below seven years on the unrounded figures (guidelines 3.1 and 3.4): %s."
             % _list(by_e))
    L.append("5. Counted the after-hours visits in %s, which has one row per clinician attending: on each case, a "
             "clinician who arrives while the visit's clinicians are still there is the same visit and a later return "
             "is another, for residents aged 85 and over at the attendance by residence SA2 and arrival date in 2026."
             % K.F_AH)
    L.append("6. Counted different residents across the service's 1 July 2026 system change by taking a carried-over "
             "client's January to June key from the new system's external_id, so each resident counts once.")
    L.append("7. Recommended the program for %s." % _list(by_e))
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append("### %s" % K.G_BOOK)
    L.append("")
    L.append("1. Life expectancy at 85 in years and whether the area qualifies:")
    for a in areas:
        L.append("   - %s: %.1f, %s" % (a, e[a], "qualifies" if F["qualifies"][a] == "Yes" else "does not qualify"))
    L.append("2. Times in 2026 the after-hours service visited the area's residents aged 85 and over:")
    for a in areas:
        L.append("   - %s: %s" % (a, "{:,}".format(F["visits"][a])))
    L.append("3. Different residents aged 85 and over those visits reached:")
    for a in areas:
        L.append("   - %s: %s" % (a, "{:,}".format(F["residents"][a])))
    L.append("")
    L.append("### %s" % K.G_CHART)
    L.append("")
    L.append("1. One bar for each of the twelve areas against a dashed line at 7.0 years, with %s marked as qualifying."
             % _list(by_e))
    L.append("")
    with open(os.path.join(task_dir, "submission.md"), "w") as fh:
        fh.write("\n".join(L))
