"""submission.md from generator/figures.json: every figure the write-up states is emitted from the figures file."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K   # noqa: E402


def n(x):
    return "{:,}".format(x)


def write(task):
    f = json.load(open(os.path.join(HERE, "figures.json")))
    c, co, a, cx = f["call"], f["components"], f["asks"], f["context"]
    sh, pk, tp = co["loss_share_pct"], co["packs_in_scope"], cx["topup_share_pct"]
    nm = K.REGION_NAME
    order = cx["order"]
    pick, run = c["region"], c["runner_up"]
    by_share = "; ".join("%s %d%%" % (nm[g], sh[g]) for g in order)
    lines = [
        "## Tags",
        "",
        "> **Domain:** General Statistics & Data Science (missing data, censoring and measurement error).",
        "> **Analytical objective:** Descriptive & Distribution Analysis.",
        "",
        "## 1. Final Recommendation",
        "",
        "**Start the 2027 pack programme in %s.** Its HFC packs lost %d%% of their full charge in 2026, %d points "
        "more than %s's %d%%. Not the North East, whose packs were charged %d%% of their charge in 2026 but entered "
        "the year short of refrigerant they had lost in 2025, so they lost %d%%; not %s on the charges alone (%d%%), "
        "which leave out the refrigerant its packs had lost by the end of 2026 and not yet had replaced." % (
            nm[pick], sh[pick], c["gap_points"], nm[run], sh[run], tp["NE"], sh["NE"], nm[pick], tp[pick]),
        "",
        "## 2. Critical Components",
        "",
        "1. 2026 refrigerant lost as a share of the HFC packs' full charge: %s" % by_share,
        "2. HFC packs in service throughout 2026: %s" % "; ".join("%s %d" % (nm[g], pk[g]) for g in K.REGIONS),
        "3. Refrigerant charged less recovered in 2026, as a share of full charge: %s" % "; ".join(
            "%s %d%%" % (nm[g], tp[g]) for g in K.REGIONS),
        "",
        "## 3. Step-by-Step Solution",
        "",
        "1. Took the HFC packs in service throughout 2026 from the Packs sheet of fgas_register_2026.xlsx (Refrigerant "
        "Strategy 2.3), each to its region by its store in hallowmere_stores.csv: %d packs." % cx["packs_total"],
        "2. Summed each pack's 2026 refrigerant charged less recovered on its routine and breakdown jobs in "
        "kelbray_job_sheets_2024_2026.csv (the store number padded to three digits, trade names read as R448A and "
        "R449A).",
        "3. Measured each pack's own receiver response from its 2024 to 2026 job sheets: the median of (departure "
        "level less arrival level) over (kilograms charged less recovered) on its charges over 0.5 kg, and its full "
        "level as the median departure level.",
        "4. Read each pack's shortfall on 31 December 2025 and on 31 December 2026 from "
        "tarnley_receiver_levels_2024_2026.csv through tarnley_pack_tags.csv: full level less the day's mean level, "
        "over the response, and not below zero.",
        "5. Each pack's 2026 loss is its net charge plus its shortfall at the end of 2026 less its shortfall at the "
        "end of 2025; each region's losses added up over its full charges added up (Strategy section 3): %s." %
        by_share,
        "6. Full charge in tonnes of CO2 equivalent at the strategy's GWP table, each pack at the refrigerant on its "
        "latest job sheet, which for packs retrofitted by the gas supplier is the new blend while the register still "
        "lists R404A: %s; on R404A %s." % (
            "; ".join("%s %s" % (nm[g], n(a["charge_co2e_t"][g])) for g in K.REGIONS),
            "; ".join("%s %s" % (nm[g], n(a["r404a_co2e_t"][g])) for g in K.REGIONS)),
        "7. Cabinet and cold room charges: each 2026 job on an asset of the register's Cabinets and cold rooms sheet "
        "counted once at the weight its cylinder lost in kelbray_cylinder_log_2026.csv, since some handheld jobs "
        "carry the job's total on every asset line: %s kg." % "; ".join(
            "%s %.1f" % (nm[g], a["equipment_kg"][g]) for g in K.REGIONS),
        "8. The programme starts in %s, the region whose packs lost the largest share of their charge in 2026." %
        nm[pick],
        "",
        "## 4. Deliverable Answers",
        "",
        "### %s" % K.BOOK,
        "",
        "1. First region of the 2027 programme: %s" % nm[pick],
        "2. 2026 refrigerant loss as a share of full charge: %s" % "; ".join("%s %d%%" % (nm[g], sh[g])
                                                                              for g in K.REGIONS),
        "3. HFC packs' full charge in tonnes of CO2 equivalent: %s" % "; ".join(
            "%s %s" % (nm[g], n(a["charge_co2e_t"][g])) for g in K.REGIONS),
        "4. Of which on R404A, in tonnes of CO2 equivalent: %s" % "; ".join(
            "%s %s" % (nm[g], n(a["r404a_co2e_t"][g])) for g in K.REGIONS),
        "5. Refrigerant charged in 2026 into integral cabinets and cold rooms, kilograms: %s" % "; ".join(
            "%s %.1f" % (nm[g], a["equipment_kg"][g]) for g in K.REGIONS),
        "",
        "### %s" % K.CHART,
        "",
        "1. Horizontal bars of the four regions' 2026 loss shares, %s (%d%%) highlighted, %s" % (
            nm[pick], sh[pick], ", ".join("%s %d%%" % (nm[g], sh[g]) for g in order[1:])),
        "",
    ]
    with open(os.path.join(task, "submission.md"), "w") as fh:
        fh.write("\n".join(lines))


if __name__ == "__main__":
    write(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE))
