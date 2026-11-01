"""Emits submission.md from figures.json, so no figure in the write-up is typed."""
import json
import os

import common as C


def write(figs, path):
    f = figs
    L = []
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** Physical & Environmental Sciences (emissions inventory).")
    L.append("**Analytical objective:** Data Extraction & Conformation (ETL).")
    L.append("")
    L.append("## 1. Final Recommendation")
    L.append("")
    L.append("**At its 2026 release the works would not keep under the %d kg annual mercury load that applies from 2028: "
             "it released %d kg (kiln 1 %d kg, kiln 2 %d kg), %d kg over, so it needs carbon injection.** Not the 2026 "
             "stack tests carried over the kiln hours (about %d kg), which every test measured with the raw mill running "
             "and so leave out what the kilns released in direct operation."
             % (f["limit_kg"], f["hg_works_kg"], f["hg_K1_kg"], f["hg_K2_kg"], f["over_by_kg"], f["tests_route_works_kg"]))
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    L.append("1. Kiln 1 released **%d kg** of mercury to air in 2026: its raw materials and fuels less what left in clinker and in the filter dust it bled to silo S7." % f["hg_K1_kg"])
    L.append("2. Kiln 2 released **%d kg**: its raw materials and fuels less what left in clinker." % f["hg_K2_kg"])
    L.append("3. The works released **%d kg**, **%d kg** over the %d kg load." % (f["hg_works_kg"], f["over_by_kg"], f["limit_kg"]))
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    L.append("1. Read condition %s of IEL-1186-03_conditions_consolidated_2026.pdf (the load counts every hour each kiln fires, in compound and in direct operation) and stack_tests_Hg_2024-2026.pdf (every run with the raw mill in operation), so the tested rate covers compound operation only." % f["licence_condition_load"])
    L.append("2. Took each kiln's year of mercury in: every month's raw material tonnes (dry) and fuel tonnes (as fired) in production_ledger_2026.xlsx times that month's composite in QC_lab_composites_2026.xlsx on the same basis (sand and slag: the quarter's composite).")
    L.append("3. Subtracted the mercury that left in clinker (the ledger's clinker times its monthly composite) and, for kiln 1, in the ledger's filter dust to silo S7 times the month's filter dust composite: kiln 1 %d kg, kiln 2 %d kg, works %d kg against %d kg." % (f["hg_K1_kg"], f["hg_K2_kg"], f["hg_works_kg"], f["limit_kg"]))
    L.append("4. Rebuilt each kiln's state through 2026 from DCS_event_journal_2026.txt, starting from the state at the start of the log: on feed from each KILN FEED ON until its next FEED OFF or MAIN BURNER TRIP (the burner trip stops the feed with it), and the raw mill stopped from each STOP or TRIP until its next START, with times read as Irish local time and the repeated hour of 25 October placed after the logged clock change.")
    L.append("5. Summed by local quarter (condition %s): hours on feed, kiln 1 %s, %s, %s and %s, kiln 2 %s, %s, %s and %s; hours in direct operation (on feed with the raw mill stopped), kiln 1 %d, %d, %d and %d, kiln 2 %d, %d, %d and %d."
             % tuple([f["licence_condition_hours"]] + [f["feed_h_K1_Q%d" % q] for q in range(1, 5)] + [f["feed_h_K2_Q%d" % q] for q in range(1, 5)]
                     + [f["direct_h_K1_Q%d" % q] for q in range(1, 5)] + [f["direct_h_K2_Q%d" % q] for q in range(1, 5)]))
    L.append("6. Took NOx from PI_historian_K1K2_2026_30min.csv, each half-hour's concentration at %d%% oxygen restated to the measured oxygen and times the dry flow, and the half-hours the historian lacks in May from CEMS_logger_A1-1_A1-2_May2026.csv, whose concentrations are already at the measured oxygen: kiln 1 %d t, kiln 2 %d t." % (f["o2_reference_pct"], f["nox_t_K1"], f["nox_t_K2"]))
    L.append("7. The works is %d kg over the load at its 2026 release, so carbon injection goes into the 2027 capital round." % f["over_by_kg"])
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append("### kiln_mercury_memo_2026.pdf")
    L.append("")
    L.append("1. At its 2026 release the works would not keep under the %d kg load; it needs carbon injection." % f["limit_kg"])
    L.append("2. Over the load by %d kg (%d kg against %d kg)." % (f["over_by_kg"], f["hg_works_kg"], f["limit_kg"]))
    L.append("3. Mercury released to air in 2026: kiln 1 %d kg, kiln 2 %d kg." % (f["hg_K1_kg"], f["hg_K2_kg"]))
    L.append("4. Bar chart of each kiln's hours in direct operation by month of 2026, on the memo's first page.")
    L.append("")
    L.append("### kiln_emissions_2026.xlsx")
    L.append("")
    L.append("1. Mercury released to air in 2026: kiln 1 %d kg, kiln 2 %d kg." % (f["hg_K1_kg"], f["hg_K2_kg"]))
    L.append("2. Hours on feed, 2026:")
    L.append("   - Kiln 1: Q1 %s, Q2 %s, Q3 %s, Q4 %s" % tuple(f["feed_h_K1_Q%d" % q] for q in range(1, 5)))
    L.append("   - Kiln 2: Q1 %s, Q2 %s, Q3 %s, Q4 %s" % tuple(f["feed_h_K2_Q%d" % q] for q in range(1, 5)))
    L.append("3. Hours in direct operation, 2026:")
    L.append("   - Kiln 1: Q1 %d, Q2 %d, Q3 %d, Q4 %d" % tuple(f["direct_h_K1_Q%d" % q] for q in range(1, 5)))
    L.append("   - Kiln 2: Q1 %d, Q2 %d, Q3 %d, Q4 %d" % tuple(f["direct_h_K2_Q%d" % q] for q in range(1, 5)))
    L.append("4. NOx to air in 2026: kiln 1 %d t, kiln 2 %d t." % (f["nox_t_K1"], f["nox_t_K2"]))
    L.append("")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))
