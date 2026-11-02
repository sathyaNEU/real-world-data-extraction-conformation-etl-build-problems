"""Emits submission.md from figures.json (every number in blocks 1 to 4 comes from the generator)."""
import pack


def fmt(n):
    return format(int(n), ",")


def emit(path, F):
    L = []
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** General Statistics & Data Science, regression and classification model diagnostics "
             "(a resource model's estimates against grade control at the selection cut-off).")
    L.append("**Analytical objective:** Forecasting & Predictive Modeling.")
    L.append("")
    L.append("## 1. Final Recommendation")
    L.append("")
    L.append("**Budget %s ounces of gold for the ore Kelvanna Lake mines in 2027 at the 0.90 g/t cut-off.** Grade "
             "control will keep about %.1f Mt of ore from the 2027 schedule, because its block grades spread more "
             "widely than the resource model's and a 0.90 g/t cut on them keeps more gold than the model's own curve "
             "shows. Not the plan's %s oz on the model's estimates, and not that figure times the reconciliation "
             "reports' %.2f, a factor measured on ore cut at 0.50 g/t."
             % (fmt(F["budget_oz"]), F["ore_mt_1dp"], fmt(F["plan_oz_100"]), F["f05_2dp"]))
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    L.append("1. The plan's Schedule at 0.90 g/t on the resource model holds **%.2f Mt and %s oz**."
             % (F["plan_mt_2dp"], fmt(F["plan_oz_100"])))
    L.append("2. Over January 2023 to October 2026, grade control's gold over the model's is **%.2f** with both sides "
             "cut at 0.50 g/t and **about %.1f** with both cut at 0.90 g/t." % (F["f05_2dp"], F["f09_1dp"]))
    L.append("3. The 2027 ore on grade control is **%.1f Mt**." % F["ore_mt_1dp"])
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    L.append("1. Moved every primary blast-hole assay in %s from UTM to the mine grid with %s, read below-detection "
             "results at half the limit and over-range results from AU_GRAV_GPT, and averaged each block's holes "
             "per the budget basis memo: %s blocks pair with %s." % (pack.F_LIMS, pack.F_GRID, fmt(F["n_pairs"]),
                                                                     pack.F_MODEL))
    L.append("2. Re-cut the paired record at 0.90 g/t on both sides: grade control holds about %.1f times the model's "
             "gold there, against %.2f at the reconciliation reports' 0.50 g/t." % (F["f09_1dp"], F["f05_2dp"]))
    L.append("3. Took each block on the Schedule sheet of %s through every grade-control-to-model ratio in the "
             "record and kept the gold where grade control reads 0.90 g/t or more: %.1f Mt of ore and %s oz, to the "
             "nearest 100,000 t and 10,000 oz." % (pack.F_PLAN, F["ore_mt_1dp"], fmt(F["budget_oz"])))
    L.append("4. Added each haul in %s, its time moved from UTC to local, at the nominal payload of the truck that "
             "carried that number on the haul's date (%s, Fleet and Disposals sheets), counted a truck's second "
             "record from the same source within ten minutes once, and started from the 2022 year-end balance in "
             "%s." % (pack.F_DISP, pack.F_FLEET, pack.F_INV))
    L.append("5. Rebuilt the ball mill's run state from both of its tags in %s (UTC to local) and counted every "
             "shutdown in %s as down, including the shutdowns the historian did not store." % (pack.F_DCS, pack.F_CMMS))
    L.append("6. Shared each lot's fine gold in %s among the bars on its lines by their gross weights in %s (a bar "
             "melted as two lots takes both) and summed by pour date." % (pack.F_REF, pack.F_BARS))
    L.append("7. Budget gold for 2027 is %s oz." % fmt(F["budget_oz"]))
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append("### kelvanna_2027_budget_gold.xlsx")
    L.append("")
    L.append("1. Gold in the ore mined in 2027: %s oz." % fmt(F["budget_oz"]))
    L.append("2. Ore behind it: %s t." % fmt(F["ore_t_100k"]))
    L.append("3. Low-grade stockpile, tonnes and contained gold:")
    for lab, t, oz in F["stock_rows"]:
        L.append("   - %s: %s t, %s oz" % (lab, fmt(t), fmt(oz)))
    L.append("4. Hours the ball mill ran, by quarter (local time):")
    for lab, v in F["hours_rows"]:
        L.append("   - %s: %s hours" % (lab, fmt(v)))
    L.append("5. Fine gold in the bars poured, by quarter (local time):")
    for lab, v in F["fine_rows"]:
        L.append("   - %s: %s oz" % (lab, fmt(v)))
    L.append("")
    L.append("### lg_stockpile_2023-2026.svg")
    L.append("")
    L.append("1. Bar chart of the low-grade stockpile's tonnes at the four dates, each bar labelled with its tonnes and "
             "contained gold.")
    L.append("")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
