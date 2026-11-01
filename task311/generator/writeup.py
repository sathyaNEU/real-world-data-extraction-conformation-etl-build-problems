"""submission.md and figures.json, both from the figures the generator computed (nothing typed)."""
import world as W

ORDER = (1, 2, 3, 4, 5)


def figures_json(F):
    c, ru = F["call"], F["runner"]
    out = {
        "call": W.RNAME[c],
        "runner_up": W.RNAME[ru],
        "boost": W.BOOST,
        "flip_interviews": F["flip_interviews"],
        "flip_per_area": F["flip_per_area"],
        "call_add_per_area": F["regions"][c]["add"],
        "call_areas": F["regions"][c]["areas"],
        "call_deffw_2025": round(F["regions"][c]["deffw"], 1),
        "call_deffw_boost": round(F["regions"][c]["deffw_boost"], 1),
        "call_icc": round(F["regions"][c]["rho"], 3),
        "north_between_share_pct": int(round(100 * F["regions"][1]["between_share"])),
        "kish_pick": W.RNAME[max(F["regions"], key=lambda r: F["regions"][r]["routes"]["R3_icc"])],
        "count_pick": W.RNAME[max(F["regions"], key=lambda r: F["regions"][r]["routes"]["R1"])],
    }
    for r in ORDER:
        x = F["regions"][r]
        key = W.RNAME[r].lower().replace(" ", "_")
        out["share_pct_" + key] = x["share_pct"]
        out["share_" + key] = round(x["share"], 4)
        out["add_" + key] = x["add"]
        out["kish_share_pct_" + key] = int(round(100 * x["routes"]["R3_icc"]))
        out["icc_" + key] = round(x["rho"], 3)
        out["count_share_pct_" + key] = int(round(100 * x["routes"]["R1"]))
        a = F["ask"][r]
        out["ask_completes_" + key] = a["completes"]
        out["ask_est_" + key] = round(a["est"], 1)
        out["ask_se_" + key] = round(a["se"], 2)
    out["supplement_take"] = 5
    out["supplement_take_boost"] = 5 + F["regions"][c]["add"]
    return out


def _f1(v):
    return "%.1f" % v


def submission(F):
    c, ru = F["call"], F["runner"]
    X = F["regions"]
    xc, xr, xn = X[c], X[ru], X[1]
    lines = []
    lines.append("## Tags")
    lines.append("")
    lines.append("**Domain:** Survey Research & Official Statistics (sample design, allocation and weighting).")
    lines.append("**Analytical objective:** Opportunity Sizing & Decision Support.")
    lines.append("")
    lines.append("## 1. Final Recommendation")
    lines.append("")
    lines.append("**Place the Wexcombe Foundation's 1,200 interviews in the %s.** Spread as %d more completed "
                 "interviews in each of its %d sampled areas they remove %d%% of the standard error of its 2027 "
                 "estimate, against %d%% in %s, the runner-up, which would need %d more interviews per area (%s in "
                 "all) to do better. Not the "
                 "North, whose error is widest but %d%% between areas the boost cannot add, so it gains %d%%. Not "
                 "%s on a design-effect projection that holds the 2025 weighting effect, which gives the %s only "
                 "%d%%."
                 % (W.RNAME[c], xc["add"], xc["areas"], xc["share_pct"], xr["share_pct"], W.RNAME[ru],
                    F["flip_per_area"], "{:,}".format(F["flip_interviews"]), int(round(100 * xn["between_share"])), xn["share_pct"],
                    W.RNAME[ru], W.RNAME[c], int(round(100 * xc["routes"]["R3_icc"]))))
    lines.append("")
    lines.append("## 2. Critical Components")
    lines.append("")
    lines.append("1. Table 2 of the 2025 technical report gives the %s an intraclass correlation of **%.3f**: "
                 "its error sits within areas, where added interviews reach it." % (W.RNAME[c], xc["rho"]))
    lines.append("2. The boost adds **%d** completed interviews in every %s area, so the supplement areas' take "
                 "rises from **5** to **%d** and the weighting effect falls from **%.1f** to **%.1f**."
                 % (xc["add"], W.RNAME[c], 5 + xc["add"], xc["deffw"], xc["deffw_boost"]))
    lines.append("3. The North's between-area variance is **%d%%** of its 2025 sampling variance, which no "
                 "interview added inside its areas removes." % int(round(100 * xn["between_share"])))
    lines.append("4. Projected area by area, the boost removes **%d%%** of the %s's 2027 standard error and "
                 "**%d%%** of %s's." % (xc["share_pct"], W.RNAME[c], xr["share_pct"], W.RNAME[ru]))
    lines.append("")
    lines.append("## 3. Step-by-Step Solution")
    lines.append("")
    lines.append("1. Read wexcombe_boost_terms_2027.pdf sections 2 and 3: the boost of 1,200 completed interviews "
                 "goes equally into a region's 2025 sampled areas, and the region is the one whose 2027 standard "
                 "error (the kind technical report section 4 describes) loses the largest share, both errors reckoned "
                 "the same way for the 2027 design on the 2025 wave.")
    lines.append("2. Took the 2025 complete and proxy interviews with a usable prescription answer from "
                 "northmark_phms_case_export_2023-2025.csv (North, Southern Uplands, Metro) and "
                 "ostrander_phms2025_cases.json (Central Valley, Lakeshore), and weighted each by its area's design "
                 "weight times occupied dwellings over completed interviews from phms_area_weights_2023-2025.csv, "
                 "joined through moh_survey_area_concordance_2024.xlsx; this reproduces Table 2 of "
                 "phms_2025_technical_report.pdf.")
    lines.append("3. Took each region's intraclass correlation from Table 2 as the between-area part of a "
                 "household's variance and one minus it as the within-area part.")
    lines.append("4. Projected each region's 2027 variance as the sum over its areas of the squared weight share "
                 "times the between-area part plus the within-area part over the take, with and without 1,200 "
                 "divided equally among the areas, and took one minus the root of the ratio.")
    lines.append("5. Ranked the regions: %s first at %d%%, %s second at %d%%." % (W.RNAME[c], xc["share_pct"],
                                                                               W.RNAME[ru], xr["share_pct"]))
    lines.append("6. Raised %s's per-area boost one interview at a time until it removed a larger share than the %s's, "
                 "comparing unrounded shares: %d more per area, %s interviews." % (W.RNAME[ru], W.RNAME[c], F["flip_per_area"],
                                                       "{:,}".format(F["flip_interviews"])))
    lines.append("7. For 2024, placed each Northmark case in its area by the numbering in force on its assignment "
                 "date (pre-2024 numbers for cases assigned before 22 April 2024, when the first number the old "
                 "series never had appears, the new numbers from then), mapped to the current regions through the "
                 "concordance, and computed each region's completed interviews, weighted estimate and standard "
                 "error as in step 2.")
    lines.append("8. Recommended the %s." % W.RNAME[c])
    lines.append("")
    lines.append("## 4. Deliverable Answers")
    lines.append("")
    lines.append("### boost_region_2027.xlsx")
    lines.append("")
    lines.append("1. Share of each region's 2027 standard error the 1,200 interviews would remove there, whole per "
                 "cents:")
    for r in F["rank_order"]:
        lines.append("   - %s: %d%%" % (W.RNAME[r], X[r]["share_pct"]))
    lines.append("2. Region to fund: %s." % W.RNAME[c])
    lines.append("3. Runner-up: %s." % W.RNAME[ru])
    lines.append("4. Smallest boost that would remove a larger share of the runner-up's error: %d more interviews per area "
                 "(%s interviews in all)." % (F["flip_per_area"], "{:,}".format(F["flip_interviews"])))
    lines.append("5. 2024 on the current regions:")
    for r in ORDER:
        a = F["ask"][r]
        lines.append("   - %s: %s completed interviews, estimate %s%%, standard error %.2f points"
                     % (W.RNAME[r], "{:,}".format(a["completes"]), _f1(a["est"]), a["se"]))
    lines.append("")
    lines.append("### boost_memo_2027.pdf")
    lines.append("")
    lines.append("1. Recommends the %s, with the %d%% share, %s's %d%% and the %d more interviews per area (%s in all) "
                 "%s would need." % (W.RNAME[c], xc["share_pct"], W.RNAME[ru], xr["share_pct"], F["flip_per_area"],
                                     "{:,}".format(F["flip_interviews"]), W.RNAME[ru]))
    lines.append("2. Bar chart of the share of the 2027 standard error removed in each region, the %s's bar "
                 "highlighted, on page 1." % W.RNAME[c])
    lines.append("")
    return "\n".join(lines)
