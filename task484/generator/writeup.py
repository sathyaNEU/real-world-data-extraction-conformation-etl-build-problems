"""submission.md, drafted from generator/figures.json: every figure the write-up states comes from there."""
import json

import world as W

TAGS = ("**Domain:** Survey Research & Official Statistics (census, register and administrative data: housing unit "
        "method population estimates for cities near a revenue-sharing line, conformed from census, permit, ACS, "
        "group quarters and utility account records).\n"
        "**Analytical objective:** Data Extraction & Conformation (ETL).")
WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
         10: "ten", 11: "eleven", 12: "twelve"}


def fmt(n):
    return "{:,}".format(int(n))


def _join(xs):
    return ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else xs[0]


def write(fig_path, out_path):
    f = json.load(open(fig_path, encoding="utf-8"))
    F = W.FILES
    up, sec, a = f["call"], f["sections"], f["asks"]
    L = ["## Tags", "", TAGS, "",
         "## 1. Final Recommendation", "",
         "**Put %s of the %s cities in the 2027 upper tier: %s.**" % (WORDS[f["n_call"]], WORDS[f["n_cities"]],
                                                                      _join(up)),
         "Each has %s residents or more on 1 April 2026 by the housing unit method once the apartment buildings "
         "opened since the 2020 census are counted at the occupancy a building of the same age had reached in the "
         "utility's account record, not at the city's ACS occupancy rate: new buildings fill over a year or more, so "
         "the overall rate counts households not yet there, and on it the tier would be %s." % (
             f["line"], _join(f["textbook_route"])),
         "",
         "## 2. Critical Components", "",
         "1. Cities at %s residents or more on 1 April 2026: **%d** of %d." % (f["line"], f["n_call"], f["n_cities"]),
         "",
         "## 3. Step-by-Step Solution", "",
         "1. Took the twelve cities, their 2020 housing units and average household size from %s (rule %s)." % (
             F["census"], sec["cities"]),
         "2. From the three permit exports (%s, %s, %s), the buildings with a certificate of occupancy (FinalDate, "
         "C of O Date, co_issued_on) from 2020-04-01 to 2026-03-31, by city, classed single-family or multifamily by "
         "%s (an R3 by its units); less the units in %s finaled in that time (rule %s)." % (
             F["metro"], F["county"], F["civic"], F["codes"], F["demo"], sec["population"]),
         "3. From %s, the premises whose first bill month is after January 2021 (buildings opened in the record): for "
         "each number of months since the first bill, active_residential_accounts over residential_meters summed "
         "over the premises (months with five premises or more; beyond them the mean of the last seven)." % F["utility"],
         "4. Occupied units on 1 April 2026: the 2020 units less demolitions plus the single-family completions at the "
         "city's occupancy in %s (occupied over total housing units); each multifamily building at the step 3 share "
         "for its months from its certificate of occupancy month to April 2026." % F["acs"],
         "5. Population: occupied units times the 2020 average household size, plus the residents in %s; every city at "
         "%s or more is in the upper tier (rule %s): %s." % (F["gq"], f["line"], sec["tier"], _join(up)),
         "6. For the housing authorized (rule %s): the permits issued in 2025 in the three exports, less any whose "
         "parcel and project an earlier permit already carried (an expired permit issued again), units summed by "
         "city as single-family or multifamily by %s." % (sec["permits"], F["codes"]),
         "",
         "## 4. Deliverable Answers", "",
         "### %s" % W.GOLDEN["workbook"], "",
         "1. The upper-tier cities: %s (%s of %s)." % (_join(up), WORDS[f["n_call"]], WORDS[f["n_cities"]]),
         "2. Housing units authorized by permits first issued in 2025, single-family and multifamily:"]
    for c in f["cities"]:
        L.append("   - %s: %s single-family; %s multifamily" % (c, fmt(a["single"][c]), fmt(a["multi"][c])))
    L += ["", "### %s" % W.GOLDEN["memo"], "",
          "1. The upper-tier cities: %s." % _join(up),
          "2. Bar chart of every city's population on 1 April 2026 against the %s line, the upper-tier cities' bars in "
          "orange." % f["line"]]
    open(out_path, "w", encoding="utf-8").write("\n".join(L) + "\n")
