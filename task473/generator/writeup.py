"""submission.md, drafted from generator/figures.json: every figure the write-up states comes from there."""
import json

import world as W


def _join(xs):
    return ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else xs[0]


def write(fig_path, out_path):
    f = json.load(open(fig_path, encoding="utf-8"))
    rows = f["rows"]
    hi = f["high_rates"]
    lines = [
        "## Tags",
        "",
        "**Domain:** General Statistics & Data Science (data integration: a fatal crash census whose surviving "
        "drivers were tested completely at three agencies and only after an arrest at the scene everywhere else, "
        "integrated into one completed count of alcohol-impaired-driving deaths per county, with the toxicology "
        "laboratory's specimens, the crash records system's reports and the DOT's vehicle miles).",
        "**Analytical objective:** Data Extraction & Conformation (ETL).",
        "",
        "## 1. Final Recommendation",
        "",
        "**%s are high-range for the FY2028 County Impaired Driving Task Force grants.**" % _join(f["call"]),
        "Their 2023 to 2025 rates are %s per 100 million vehicle miles against the %s line; the nearest below %s %s "
        "at %s. Not %s, which one share of unarrested drivers at .08 or more (%s per cent where every driver is "
        "tested) gives, because officers miss most drivers between .08 and .149 and few at .15 or more, so a county "
        "whose impaired drivers sit near the limit hides more of them; not %s, which one catch rate for every BAC "
        "(%s per cent) gives." % (
            _join(["%s %s" % (c, v) for c, v in hi]), f["threshold"], "is" if len(f["below_top"]) == 1 else "are",
            _join(f["below_top"]), f["below_top_rate"],
            _join(f["rival_share"]), f["share_pct"], _join(f["rival_one"]), f["one_catch_pct"]),
        "",
        "## 2. Critical Components",
        "",
        "1. At the State Patrol and the Corwin and Ossian sheriffs, which test every surviving driver, officers "
        "arrested **%s%%** of surviving drivers from .08 to .149 and **%s%%** at .15 or more." % (
            f["catch_lo"], f["catch_hi"]),
        "2. Tanager's county and city agencies arrested %d drivers found from .08 to .149 and %d at .15 or more, so "
        "**%s** impaired surviving drivers there were never tested." % (
            f["tanager_found_lo"], f["tanager_found_hi"], f["tanager_missed"]),
        "3. Tanager's 2023 to 2025 rate is **%s**, above the %s line." % (f["tanager_rate"], f["threshold"]),
        "",
        "## 3. Step-by-Step Solution",
        "",
        "1. Read %s and %s (2011 form codes, results in thousandths) and %s and %s (2024 form), kept each death "
        "within %d days of a 2023 to 2025 crash by crash county, and took drivers as guidelines %s defines them "
        "(%s)." % (W.FILES["crash23"], W.FILES["person23"], W.FILES["crash2425"], W.FILES["person2425"],
                   f["window_days"], f["sections"]["drivers"], W.FILES["guidelines"]),
        "2. Identified the agencies that draw blood from every surviving driver (manual %s) through %s's agency "
        "numbers and former codes: the State Patrol posts and the Corwin and Ossian sheriffs." % (
            f["sections"]["testing"], W.FILES["agencies"]),
        "3. At those agencies, divided the arrested surviving drivers by all surviving drivers in each band, .08 to "
        ".149 and .15 or more: %s%% and %s%%." % (f["catch_lo"], f["catch_hi"]),
        "4. At every other agency, counted each arrested driver found at .08 or more as one over its band's catch "
        "rate (%s and %s), the excess being that county's untested impaired surviving drivers (%s in Tanager), "
        "and gave each of the county's untested surviving drivers the excess divided by their number." % (
            f["weight_lo"], f["weight_hi"], f["tanager_missed"]),
        "5. Gave each crash its deaths times the chance that at least one driver was at .08 or more (guidelines %s), "
        "summed by county, and divided by the 2023 to 2025 vehicle miles of %s, each year's DVMT times its days "
        "(%d in 2024), per 100 million: Tanager %s." % (f["sections"]["estimand"], W.FILES["vmt"], f["leap_days"],
                                                         f["tanager_rate"]),
        "6. From %s, kept the 2025 DUI arrests by local collection date, one per agency case number, placed each in "
        "its agency's county from %s and each State Patrol arrest (submitted under SPHQ000) in its post's county "
        "from the post in its case number, and took the first specimen's whole-blood ethanol (serum divided by "
        "%s, the amended report over the superseded): the arrests and the per cent at .15 or more below." % (
            W.FILES["lab"], W.FILES["agencies"], f["serum"]),
        "7. From %s and %s, took each report's latest accepted version, kept public-road crashes with an injury and "
        "a driver unit HAD BEEN DRINKING, counted a crash two agencies reported once (same date, road, time within "
        "minutes and drivers), and dropped those in the census: the injury crashes below." % (
            W.FILES["reports"], W.FILES["units"]),
        "8. Certified %s as high-range (guidelines %s: %s or more)." % (_join(f["call"]), f["sections"]["rate"],
                                                                           f["threshold"]),
        "",
        "## 4. Deliverable Answers",
        "",
        "### %s" % W.GOLDEN["csv"],
        "",
        "1. Each county's 2023 to 2025 alcohol-impaired-driving deaths (whole numbers) and rate per 100 million "
        "vehicle miles (two decimals):",
    ]
    for r in rows:
        lines.append("   - %s: %d deaths, %s" % (r["county"], r["deaths"], r["rate"]))
    lines.append("2. Each county's 2025 impaired-driving arrests with a blood specimen at the State Toxicology "
                 "Laboratory and the per cent of them at .15 or more (one decimal):")
    for r in rows:
        lines.append("   - %s: %s arrests, %s%%" % (r["county"], format(r["arrests"], ","), r["pct15"]))
    lines.append("3. Each county's 2025 injury crashes in which no one died within %d days and an officer reported a "
                 "driver had been drinking:" % f["window_days"])
    for r in rows:
        lines.append("   - %s: %d" % (r["county"], r["crashes"]))
    lines += [
        "",
        "### %s" % W.GOLDEN["letter"],
        "",
        "1. High-range for FY2028: %s." % _join(["%s (%s)" % (c, v) for c, v in hi]),
        "2. Bar chart of the 14 counties' 2023 to 2025 rates against the 0.60 line, the high-range counties in red, on "
        "page 1.",
        "",
    ]
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
