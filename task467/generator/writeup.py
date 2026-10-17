"""submission.md, drafted from generator/figures.json: every figure the write-up states comes from there."""
import json

import world as W


def write(fig_path, out_path):
    f = json.load(open(fig_path, encoding="utf-8"))
    c, k, rv, sp = f["call"], f["components"], f["rivals"], f["strata_pct"]
    names = W.BROKERAGES
    lines = [
        "## Tags",
        "",
        "**Domain:** Survey Research & Official Statistics (seasonal adjustment and official time-series production: "
        "the airport's monthly taxi trip series restated across a temporary intervention).",
        "**Analytical objective:** Data Extraction & Conformation (ETL).",
        "",
        "## 1. Final Recommendation",
        "",
        "**Set the 2027 taxi pickup fee at $%s.**" % c["fee_2027"],
        "2025's %s fee-liable pickups, restated to the forecourt rank, are %s, and $%s is the lowest 25-cent step at "
        "which they recover the $%s the 2027 budget assigns to the fee (a surplus of about $%s; $6.25 falls about $%s "
        "short). Not $%s, which takes the pickups' whole %s per cent fall as the rank's although the Airport Line, "
        "opened the same day, took part of it for good; not $%s, which sets all pickups against all drop-offs and finds "
        "only %s per cent, because the drop-offs come mostly from the line's station zones." % (
            k["recorded_2025"], k["restated_2025"], c["fee_2027"], k["amount_2027"], f["surplus_at_fee"],
            f["shortfall_one_step_below"], rv["own_fall"]["fee"], rv["own_fall"]["share_pct"], rv["all_dropoffs"]["fee"],
            rv["all_dropoffs"]["share_pct"]),
        "",
        "## 2. Critical Components",
        "",
        "1. 2025's fee-liable pickups as recorded: **%s**." % k["recorded_2025"],
        "2. The share of 2025's restated pickups the temporary rank cost: **%s per cent**, pickups against drop-offs within "
        "the Airport Line's station zones and within the other zones." % k["share_cost_pct"],
        "3. 2025 restated to the forecourt rank: **%s** budgeted pickups." % k["restated_2025"],
        "",
        "## 3. Step-by-Step Solution",
        "",
        "1. Counted 2025's trips beginning in zone 1 in %s, the final annual file FP-07 4.4 names (voided trips are not "
        "in it): %s fee-liable pickups." % (W.FILES["trips2025"], k["recorded_2025"]),
        "2. Built daily pickups and drop-offs by zone from %s, %s (each voided trip and its reversal taken out) and the "
        "2025 file." % (W.FILES["archive"], W.FILES["trips2024"]),
        "3. Grouped the city zones into the four named for the Airport Line's stations in %s (Downtown Central, "
        "Midtown, University and Commerce Park in %s), the only zones whose drop-offs fell from the twelve months "
        "before 4 November 2024 to 2025 (each by about a third), and the rest." % (W.FILES["bulletin"], W.FILES["zones"]),
        "4. In each group, the ratio of pickups to drop-offs was %s per cent lower in 2025 than in the twelve months "
        "before the move in the station zones and %s per cent lower in the other zones." % (sp["station_zones"],
                                                                                            sp["other_zones"]),
        "5. Restated 2025 under FP-07 4.3 as each group's 2025 drop-offs at the group's ratio of pickups to drop-offs in "
        "the twelve months before the move, summed: %s pickups, of which the rank cost %s per cent." % (
            k["restated_2025"], k["share_cost_pct"]),
        "6. Applied By-law GT-3 s.4 to the $%s on line %s of %s: $%s is the lowest step that recovers it (a surplus of "
        "about $%s; $6.25 about $%s short)." % (k["amount_2027"], f["stated"]["budget_line"], W.FILES["budget"],
                                                c["fee_2027"], f["surplus_at_fee"], f["shortfall_one_step_below"]),
        "7. For the ledger, billed each pickup once, to the brokerage its taxi belonged to when the trip began, at "
        "Schedule A's fee for the trip's year (By-law GT-3 s.3): 2025 from the annual file with the licence's brokerage "
        "on the trip date in %s (the file's brokerage_id is the licence's brokerage when the file was built), 2026 from "
        "the eight monthly files in Velmont local time, each voided trip and its reversal out and each re-sent copy "
        "(same licence, minute, zones and amounts as an earlier record) out." % W.FILES["affiliations"],
        "8. Recommended the 2027 fee of $%s a pickup." % c["fee_2027"],
        "",
        "## 4. Deliverable Answers",
        "",
        "### %s" % W.GOLDEN["memo"],
        "",
        "1. The 2027 fee: $%s a pickup." % c["fee_2027"],
        "2. 2025's fee-liable pickups: %s as recorded, %s as restated." % (k["recorded_2025"], k["restated_2025"]),
        "3. The share of 2025's restated pickups the temporary rank cost: %s per cent." % k["share_cost_pct"],
        "4. Against the $%s the 2027 budget assigns to the fee: surplus at $%s, $%s; shortfall at $6.25, $%s." % (
            k["amount_2027"], c["fee_2027"], f["surplus_at_fee"], f["shortfall_one_step_below"]),
        "5. Line chart of monthly fee-liable pickups and airport drop-offs, November 2023 to August 2026, in the memo's "
        "Monthly trips section, the temporary rank's months shaded.",
        "",
        "### %s" % W.GOLDEN["ledger"],
        "",
        "1. One row per brokerage per month, January 2025 to August 2026, %d rows: fee-liable pickups (whole trips) and "
        "fees owed (dollars and cents):" % int(f["ledger_rows"]),
    ]
    for r in f["ledger"]:
        lines.append("   - %s, %s: %s pickups, $%s" % (r["month"], names[r["brokerage_id"]], r["pickups"], r["owed"]))
    lines.append("")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
