"""Renders submission.md from the solution, so every figure and every count word in the write-up comes
from the objects that produced it (house fix H3)."""
from decimal import Decimal

from params import GROUP_CLASSES_V2, SITES
from solution import rnd

D = Decimal
ORDER = ["CHA", "MAI", "CES", "RAY"]


def m(x):
    return "${:,}".format(rnd(x))


def render(path, sol):
    upg = sorted([r for r in sol["rows"] if r["a"]["kind"] == "upgrade" and r["nbv"] == 0], key=lambda r: int(r["asset"]))
    ids = [r["asset"] for r in upg]
    words = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight"}
    n_up = words.get(len(ids), str(len(ids)))
    id_list = ", ".join(ids[:-1]) + " and " + ids[-1]
    months = sorted({sol["eng"].host_end(r["a"]) for r in upg})
    mname = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    span = "between %s and %s %d" % (mname[months[0] % 12], mname[months[-1] % 12], months[-1] // 12) if len(months) > 1 else \
        "in %s %d" % (mname[months[0] % 12], months[0] // 12)
    h2 = m(sol["h2"])
    lines = []
    lines.append("# task110: Yacaaba Radiology fixed asset migration, January to June 2027 depreciation\n")
    lines.append("## Tags\n")
    lines.append("**Domain:** Accounting, Audit & Forensic Analytics, fixed assets and leases (internal audit's re-performance of a practice's fixed asset register migration to the group ledger).  ")
    lines.append("**Analytical objective:** Data Extraction & Conformation (ETL).\n")
    lines.append("## 1. Final Recommendation\n")
    lines.append("**The group ledger will post %s of depreciation on Yacaaba Radiology's assets from January to June 2027.**\n" % h2)
    lines.append("Each equipment upgrade runs over the remaining life of the imaging system its capital approval names, the only basis that "
                 "reproduces both Yacaaba's depreciation postings and the 2024 depreciation in note 9 of its FY2025 report, and %s upgrades on "
                 "systems that run out %s load at nil book value. Not the five-year life the rates tab gives options and accessories: it "
                 "replays every posting and balance but not the 2024 imaging depreciation. Not stopping each upgrade when its system's life ends "
                 "while keeping five-year rates: it misses the same 2024 figure.\n" % (n_up.lower(), span))
    lines.append("## 2. Critical Components\n")
    lines.append("1. The rebuilt schedules reproduce all **90** account-months of Yacaaba's depreciation postings from July 2025 to September 2026 to the cent, and both years of note 9 in the FY2025 report.")
    lines.append("2. **%s** equipment upgrades (assets %s) load at nil book value with no remaining months." % (n_up, id_list))
    lines.append("3. Yacaaba's ledger still posts **%s** of depreciation from October to December 2026." % m(sol["q4"]))
    lines.append("4. **%d** assets load, at a book value of **%s**.\n" % (sol["load_rows"], m(sol["load_nbv"])))
    lines.append("## 3. Step-by-Step Solution\n")
    lines.append("1. Cleaned `YCB_asset_register_2026-10-02.xlsx` to the ledger by dropping the Capitalised N items and the repeated invoice lines, after which cost ties to `YCB_trial_balance_30-09-2026.xlsx` account by account.")
    lines.append("2. Rebuilt every asset straight line from its month of purchase on the Rates tab, with computer equipment moved to four years prospectively from July 2025 (FY2025 note 1(e)), the Cessnock OPG's $38,000 impairment from June 2025 (note 9), and the Bremer Voluson continued on the depreciation brought forward in its February 2026 intercompany journal.")
    lines.append("3. Put each Equipment upgrades row on the remaining months of the imaging system its request in `YCB_capital_approvals_2018-2026.csv` names by system and site, the only upgrade basis that reproduces both the 90 account-months in `YCB_GL_detail_2025-07_to_2026-09.csv` and the 2024 depreciation in note 9 of `YCB_FY2025_financial_statements_extract.pdf`.")
    lines.append("4. Ran the schedules to 31 December 2026: %s of October to December depreciation." % m(sol["q4"]))
    lines.append("5. Applied FIN-PRO-022 to `verification_scans_YCB_2026.csv` and `RAY_count_sheet_07-10-2026.pdf` (5:00 pm Sydney time cut-off on 9 October, serial where the tag is blank, site of record where sighted): %d nil-book-value assets not sighted are written off and %d assets load at %s." % (len(sol["written_off"]), sol["load_rows"], m(sol["load_nbv"])))
    lines.append("6. Classed each asset with the approved v2 sheet of `group_asset_class_mapping.xlsx` on its account in the 9 October trial balance run, which moves the Charlestown reception joinery to leasehold improvements.")
    lines.append("7. Depreciated the load from January 2027 under section 6 of `fa_migration_standard.pdf`: %s for January to June 2027." % h2)
    lines.append("8. Recommendation: sign the load off; the group ledger will post %s of depreciation on Yacaaba's assets from January to June 2027.\n" % h2)
    lines.append("## 4. Deliverable Answers\n")
    lines.append("### fa_load_2027-01-01.csv\n")
    lines.append("1. %d rows, one per asset that loads, with asset number, description, site, group asset class, cost, accumulated depreciation at 31 December 2026, book value, remaining months and January to June 2027 charge, amounts in dollars and cents." % sol["load_rows"])
    cost = sum((r["cost"] for r in sol["rows"]), D(0))
    acc = sum((r["acc_dec"] for r in sol["rows"]), D(0))
    lines.append("2. Column totals: cost ${:,.2f}; accumulated depreciation at 31 December 2026 ${:,.2f}; book value ${:,.2f}; January to June 2027 charge ${:,.2f}.".format(cost, acc, sol["load_nbv"], sol["h2"]))
    lines.append("3. Assets %s (equipment upgrades) carry nil book value and 0 remaining months.\n" % id_list)
    lines.append("### cutover_signoff.docx\n")
    lines.append("1. January to June 2027 depreciation on Yacaaba's assets: %s, stated first." % h2)
    lines.append("2. By site as the assets load (book value at 30 September 2026, October to December 2026 depreciation, book value loaded, January to June 2027 charge):")
    for s_ in ORDER:
        v = sol["sites"][s_]
        lines.append("   - %s: %s, %s, %s, %s" % (SITES[s_], m(v["nbv_sep"]), m(v["q4"]), m(v["nbv_load"]), m(v["h2"])))
    lines.append("3. Assets coming across with nothing left to depreciate, count and original cost:")
    for s_ in ORDER:
        v = sol["sites"][s_]
        lines.append("   - %s: %d assets, %s" % (SITES[s_], v["nil_count"], m(v["nil_cost"])))
    lines.append("4. Book value loading by group asset class:")
    for c in GROUP_CLASSES_V2:
        lines.append("   - %s: %s" % (c, m(sol["classes"].get(c, D(0)))))
    lines.append("5. Bar chart of the January to June 2027 charge by site at the end of the note, one bar per site labelled in dollars, titled with the %s total." % h2)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
