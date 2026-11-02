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
        "integrated into one completed count of alcohol-impaired-driving deaths per county, with the DOT's vehicle "
        "miles and the county courts' criminal traffic cases).",
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
        ".149 and .15 or more: %s%% and %s%%; holding out each State Patrol post in turn, these rates recover its "
        "unarrested drivers at .08 or more from its arrests with a root mean square miss of %s drivers, against %s "
        "for one unarrested share." % (f["catch_lo"], f["catch_hi"], f["bt_ipw"], f["bt_pool"]),
        "4. At every other agency, counted each arrested driver found at .08 or more as one over its band's catch "
        "rate (%s and %s), the excess being that county's untested impaired surviving drivers (%s in Tanager), "
        "and gave each of the county's untested surviving drivers the excess divided by their number." % (
            f["weight_lo"], f["weight_hi"], f["tanager_missed"]),
        "5. Gave each crash its deaths times the chance that at least one driver was at .08 or more (guidelines %s), "
        "summed by county, and divided by the 2023 to 2025 vehicle miles of %s, each year's DVMT times its days "
        "(%d in 2024), per 100 million: Tanager %s." % (f["sections"]["estimand"], W.FILES["vmt"], f["leap_days"],
                                                         f["tanager_rate"]),
        "6. From %s, kept each county court's impaired-driving cases (the three DUI charges) for offenses in 2025, "
        "counted as one prosecution a case dismissed on the day the same court opened another for the same offense "
        "date and arresting agency together with that later case (guidelines %s: one for each person charged and "
        "offense), and took each prosecution's last case: a guilty plea or verdict on an impaired-driving charge by "
        "28 February 2027 is a conviction, and an amended charge, a deferral, a dismissal, an acquittal or no "
        "disposition is not: the prosecutions and the per cent convicted below." % (
            W.FILES["court"], f["sections"]["baselines"]),
        "7. Certified %s as high-range (guidelines %s: %s or more)." % (_join(f["call"]), f["sections"]["rate"],
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
    lines.append("2. Each county's impaired-driving offenses of 2025 that its county court had prosecuted by 28 "
                 "February 2027 (one for each person charged and offense, whole numbers) and the per cent of them "
                 "that had ended in an impaired-driving conviction by then (one decimal):")
    for r in rows:
        lines.append("   - %s: %s offenses, %s%%" % (r["county"], format(r["prosecuted"], ","), r["pct_conv"]))
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
