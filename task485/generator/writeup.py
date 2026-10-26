"""submission.md from generator/figures.json: the five blocks, every figure taken from the generator's own output."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import world as W  # noqa: E402

NAMES = dict(W.SECTORS)
LOW = {s: n[0].lower() + n[1:] for s, n in NAMES.items()}
YEARS = ["2018-19", "2019-20", "2020-21", "2021-22", "2022-23"]
FLIP = ("CON", "HSC", "RET")


def joined(xs):
    xs = list(xs)
    return ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else xs[0]


def t(x):
    return "{:,}".format(x)


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    over = [s for s in W.SECT if s in f["call"]]
    under = [s for s in W.SECT if s not in over]
    pc = lambda k: "%d" % f[k]                                   # noqa: E731
    out = ["## Tags", "",
           "**Domain:** Survey Research & Official Statistics, census, register and administrative data quality (an "
           "island statistics unit's provisional long-term immigration by employment sector for the year to 30 June "
           "2026, conformed from its Population Register's current extract and legacy archive, the crosswalk between "
           "their registration numbers and two sector classifications, against the Population Policy's sector "
           "allowances).",
           "**Analytical objective:** Data Extraction & Conformation (ETL).", "",
           "## 1. Final Recommendation", "",
           "**The Council should cut the 2027 work permit quotas of %s, the three sectors whose provisional long-term "
           "immigration for 2025-26 exceeds its allowance.**" % joined(LOW[s] for s in over),
           "%s stay under their allowances once each stay still open at the cut is completed on the 2024-25 arrivals of "
           "the same sector, migration history and months on the island: the completion that would have predicted the "
           "2024-25 arrivals best a year earlier (mean squared difference %.3f, against %.3f by sector and months alone). "
           "Not those three as well, which the sector-by-months completion gives: returning workers, whose previous stay "
           "ended within the year before they arrived, made %s per cent of their 2025-26 arrivals against %s per cent a "
           "year earlier, and in 2024-25 reached twelve months %s per cent of the time against %s per cent for first "
           "arrivals." % (
               joined(NAMES[s] if i == 0 else LOW[s] for i, s in enumerate(FLIP)), f["backtest.golden"],
               f["backtest.sector_months"], joined(pc("returning.%s.2025_26.share_pct" % s) for s in FLIP),
               joined(pc("returning.%s.2024_25.share_pct" % s) for s in FLIP),
               joined(pc("returning.%s.2024_25.long_pct" % s) for s in FLIP),
               joined(pc("first.%s.2024_25.long_pct" % s) for s in FLIP)), "",
           "## 2. Critical Components", "",
           "1. 2025-26 arrivals still on the island at the 31 August 2026 cut short of their first anniversary: %s, "
           "of which %s are returns (a previous stay under the same registration number ended in the %d days before "
           "the arrival)." % (joined("%s **%s**" % (LOW[s], t(f["sector.%s.open_at_cut" % s])) for s in FLIP),
                              joined("**%s**" % t(f["returning.%s.2025_26.open" % s]) for s in FLIP),
                              f["history_window_days"]),
           "2. Of the 2024-25 arrivals in those sectors, returning arrivals reached twelve months %s per cent of the "
           "time and first arrivals %s per cent." % (
               joined("**%s**" % pc("returning.%s.2024_25.long_pct" % s) for s in FLIP),
               joined("**%s**" % pc("first.%s.2024_25.long_pct" % s) for s in FLIP)),
           "3. The methods note's test, on the %s arrivals of 2024-25 still open at 31 August 2025: the completion by "
           "sector, history and months scores **%.3f**, by sector and months **%.3f**, the sector's share of all "
           "arrivals **%.3f**." % (t(f["backtest.scored"]), f["backtest.golden"], f["backtest.sector_months"],
                                  f["backtest.flat_sector"]), "",
           "## 3. Step-by-Step Solution", "",
           "1. Took the ARRIVAL records with an arrival date from 1 July 2025 to 30 June 2026 in "
           "population_register_extract_20260930.csv, each sector from its 2014 activity code or 2026 sector code in "
           "sector_classification_2026.json: %s arrivals." % t(f["arrivals.2025_26"]),
           "2. At the 31 August 2026 cut counted a stay as long-term when its first anniversary had passed with no "
           "leaving date before it, and as not when its leaving date fell before its anniversary (the methods note's "
           "definitions); the rest are open: %s." % joined("%s %s" % (LOW[s], t(f["sector.%s.open_at_cut" % s]))
                                                         for s in FLIP),
           "3. Gave each arrival its migration history from the other stays under the same reg_no: a return when one "
           "of them has a leaving date in the %d days before the arrival date." % f["history_window_days"],
           "4. Scored the candidate completions on the methods note's test, each estimated from the 2023-24 arrivals "
           "and given to the 2024-25 arrivals open at 31 August 2025 (leaving notices received by 30 September 2025): "
           "by sector, history and whole calendar months on the island %.3f, by sector and months %.3f." % (
               f["backtest.golden"], f["backtest.sector_months"]),
           "5. Counted each open 2025-26 stay at the share of the 2024-25 arrivals of its sector and history still on "
           "the island after its whole months at 31 August 2026 whose stays reached their first anniversary (returns %s "
           "per cent and first arrivals %s per cent overall in %s), and added the stays counted long-term." % (
               joined(pc("returning.%s.2024_25.long_pct" % s) for s in FLIP),
               joined(pc("first.%s.2024_25.long_pct" % s) for s in FLIP), joined(LOW[s] for s in FLIP)),
           "6. Compared each unrounded figure with its 2025-26 allowance in Table 1 of "
           "population_policy_2024_2028_sector_allowances.pdf: %s exceed." % joined(LOW[s] for s in over),
           "7. For the back series, read the archive's day-first dates, gave each TRANSFERRED record the leaving date and "
           "notice date of the TRANSFER record its legacy number's reg_no holds in registration_number_crosswalk_2023.csv, "
           "kept the archive's own arrival date and activity, counted once any records identical in arrival date, sex, "
           "birth year, nationality and activity whose stays ended on the same date on notices received the same day "
           "(one stay registered at two parish offices), and added the current extract's ARRIVAL records with arrival "
           "dates in each year: the figures below.",
           "8. The Council cuts the 2027 quotas of %s." % joined(LOW[s] for s in over), "",
           "## 4. Deliverable Answers", "",
           "### provisional_long_term_immigration_2025_26.xlsx", "",
           "1. Each sector's provisional long-term immigration for 2025-26 against its allowance:"]
    for s in W.SECT:
        out.append("   - %s: %s" % (NAMES[s], "exceeds" if f["sector.%s.over" % s] else "does not exceed"))
    out.append("2. Arrivals registered for work by sector, persons, for the years 2018-19 to 2022-23:")
    for s in W.SECT:
        out.append("   - %s: %s" % (NAMES[s], ", ".join("%s %s" % (y, t(f["back.arrivals.%s.%s" % (y, s)]))
                                                     for y in YEARS)))
    out.append("3. Final long-term immigration by sector, persons, for the years 2018-19 to 2022-23:")
    for s in W.SECT:
        out.append("   - %s: %s" % (NAMES[s], ", ".join("%s %s" % (y, t(f["back.long.%s.%s" % (y, s)])) for y in YEARS)))
    out += ["", "### long_term_immigration_by_sector_2025_26.png", "",
            "1. A bar chart of each sector's provisional long-term immigration for 2025-26 against its 2025-26 "
            "allowance, the three sectors over their allowances marked.", ""]
    open(os.path.join(TASK, "submission.md"), "w").write("\n".join(out))


if __name__ == "__main__":
    main()
