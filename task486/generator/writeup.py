"""submission.md, every figure read from generator/figures.json."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import world as W   # noqa: E402

QLAB = ["Oct to Dec 2025", "Jan to Mar 2026", "Apr to Jun 2026", "Jul to Sep 2026"]
REC = W.RECIPIENTS


def money(v):
    return "${:,}".format(v)


def n(v):
    return "{:,}".format(v)


def write(fig_path, out_path):
    f = json.load(open(fig_path))
    nm = W.RECIPIENT_NAME
    o = []
    o.append("## Tags\n")
    o.append("**Domain:** General Statistics & Data Science, data integration, record linkage and entity resolution (four "
             "Continuums of Care's HMIS exports, a domestic violence coalition's comparable database, a homeless "
             "clinic's encounters and a city outreach team's contacts, resolved through a state linkage unit's pairwise "
             "findings into the people the Halvering Valley region served in FY2026, the basis of its 2027 fund split).")
    o.append("**Analytical objective:** Data Extraction & Conformation (ETL).\n")
    o.append("## 1. Final Recommendation\n")
    o.append("**Under policy RF-2027 the 2027 Fund pays %s.**" % "; ".join(
        "%s %s on %s people served" % (nm[k], money(f["amount|" + k]), n(f["people|" + k])) for k in REC))
    o.append("The region served %s people in FY2026, each counted once across the seven sources. Not the %s people "
             "that merging every chain of the linkage unit's links gives, which pays Halvering %s, %s less: a record "
             "carrying only a year of birth links to every client of that name, year and sex, so %s merged groups hold "
             "two records of one source.\n" % (n(f["people|ALL"]), n(f["default_people|ALL"]),
                                                 money(f["default_amount|HAL"]), money(f["default_short|HAL"]),
                                                 n(f["conflict_groups"])))
    o.append("## 2. Critical Components\n")
    o.append("1. The region served **%s** people in FY2026, each counted once across the HMIS exports, the coalition's "
             "database, the clinic's encounters and the outreach app." % n(f["people|ALL"]))
    o.append("2. By recipient: %s.\n" % ", ".join("%s **%s**" % (nm[k], n(f["people|" + k])) for k in REC))
    o.append("## 3. Step-by-Step Solution\n")
    steps = [
        "Read the four Continuums' HMIS client, enrollment, exit and services files stacked as sent (Melbray's dates "
        "month/day/year), dvc_comparable_db_export.xlsx, wsh_hch_encounters_fy2025_fy2026.csv, "
        "hot_field_app_contacts.jsonl and sdlu_linkage_pairs_run_20261008.csv, each record by its source and its own "
        "key: %s records." % n(f["records"]),
        "Flagged each record's FY2026 service under section 3 of regional_fund_policy_RF-2027.docx (an enrollment "
        "entered by 30 September 2026 and not exited before 1 October 2025, a coalition stay with a night in the year, a "
        "clinic encounter in the year at Street, Homeless Shelter or Transitional status, an outreach contact in the "
        "year, on local dates): %s records." % n(f["records_fy2026"]),
        "Took the unit's %s LINK findings strongest first and joined two records' people unless that put two records "
        "of one source in one person, since partnership_extract_guide.txt has each source hold a person once: %s "
        "people with FY2026 service (merging every chain instead leaves %s groups with two records of one source and "
        "gives %s)." % (n(f["links"]), n(f["people|ALL"]), n(f["conflict_groups"]), n(f["default_people|ALL"])),
        "Placed each person under section 4 (the Continuum of the latest HMIS enrollment open in the year, else the "
        "coalition for a coalition stay in the year, else the Continuum of the latest contact or encounter): %s." %
        ", ".join("%s %s" % (W.COUNTY[k] if k in W.COUNTY else "the coalition", n(f["people|" + k])) for k in REC),
        "Split %s (the %s Fund less the Partnership's %d per cent, section 2) in proportion and rounded each amount to "
        "the dollar: %s together, the Partnership's share taking the extra dollar." % (
            money(f["pool"]), money(f["fund"]), f["admin_pct"], money(f["split"])),
        "For the shelter nights, counted each person's night once across their emergency shelter and safe haven stays "
        "in the register's project types, from entry to the night before exit (an open stay to 30 September 2026), with "
        "the winter respite's bed-night services from hmis_services_fy2025_fy2026.csv, so a night on a stay left open "
        "after the person entered another shelter counts once: the 16 cells below.",
        "For the rapid re-housing waits, took each head of household's FY2026 move-in date, followed that person back "
        "through any rapid re-housing project of the Continuum they left on the day the next one began, whatever their "
        "relationship to the head there, and averaged the days from that first entry to the move-in by Continuum and "
        "household type, the region over all its move-ins: the 10 averages below.",
        "The 2027 Fund is split as in the Final Recommendation.",
    ]
    for k, s in enumerate(steps):
        o.append("%d. %s" % (k + 1, s))
    o.append("")
    o.append("## 4. Deliverable Answers\n")
    o.append("### halvering_2027_fund_allocation.xlsx\n")
    o.append("1. People served in FY2026 and 2027 amounts, whole people and whole dollars:")
    for k in REC:
        o.append("   - %s: %s people, %s" % (nm[k], n(f["people|" + k]), money(f["amount|" + k])))
    o.append("   - Region: %s people" % n(f["people|ALL"]))
    o.append("2. Nights people spent in emergency shelters (night-by-night included) and safe havens, FY2026 by quarter, "
             "whole nights:")
    for c in W.COCS:
        o.append("   - %s: %s" % (nm[c], "; ".join("%s %s" % (QLAB[q], n(f["nights|%s|Q%d" % (c, q + 1)]))
                                                for q in range(4))))
    o.append("3. Average days from a household's entry into rapid re-housing to its move-in, FY2026 move-ins, one "
             "decimal:")
    for c in W.COCS + ["ALL"]:
        name = nm[c] if c != "ALL" else "Region, over all its move-ins"
        o.append("   - %s: households with children %.1f, adults without children %.1f" % (
            name, f["rrh|%s|children" % c], f["rrh|%s|adults" % c]))
    open(out_path, "w", encoding="utf-8").write("\n".join(o) + "\n")


if __name__ == "__main__":
    T = os.path.dirname(HERE)
    write(os.path.join(HERE, "figures.json"), os.path.join(T, "submission.md"))
