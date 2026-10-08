# ET39 — Instructional spending per student from IPEDS: campuses whose finances live inside another campus

| Field | Value |
|---|---|
| Domain | Higher-education policy / state funding formulas / institutional research |
| Objective family | Data Extraction & Conformation (ETL / Pipeline Build) |
| Task shape | 01 · Ranked list under a cap (five lowest-spending reporting units receive a grant) |
| Core technique | Building reporting families from parent/child flags so numerators and denominators share a scope; harmonizing accounting-standard forms (GASB vs FASB); correct FTE source |
| Trap family (honest data) | Parent expenses divided by parent-only FTE; children with blank finance treated as zero; GASB-only extraction drops FASB-reporting publics |
| Primary sources | NCES IPEDS complete data files (HD, finance F1A/F2, 12-month instructional activity EFIA, flags) |

## 1. The real-world project

A state higher-education commission awards an **instructional investment grant** to the five public four-year reporting
units with the lowest instructional expense per FTE student. The analyst joined IPEDS finance to enrollment by UNITID.
Two branch campuses showed $0 instruction spending and topped the list; their flagship parent showed spending per student
far above its peers.

## 2. The business decision (one deterministic recommendation)

**Which five reporting units receive the grant, and which unit is sixth?**

Rules (commission method):

* Universe: in-state public 4-year institutions (HD `SECTOR = 1`) active in the year.
* Reporting family: an institution whose finance data are reported by another (finance parent/child flag indicates a
  child; parent UNITID in the parent-ID flag) joins its parent's family. Families are the ranking units; a family's name is
  the parent's.
* Numerator: instruction expenses (current-year total) from the form the **parent** used: GASB (F1A) or FASB (F2) — the
  variable for each form is listed in the method.
* Denominator: 12-month FTE (EFIA: undergraduate + graduate + doctor's-professional practice FTE) summed over **all family
  members**, regardless of how enrollment was reported.
* Fiscal year 2022 finance with academic year 2021–22 EFIA.
* Rank ascending by expense per FTE; ties by larger FTE.

## 3. Why this gets overlooked in real projects

* IPEDS rows look like one institution each; parent/child relationships live in a separate flags file and vary by survey
  component (finance may be combined while enrollment is separate).
* A child with finance reported elsewhere has blank finance; a careless `fillna(0)` makes it the "lowest spender".
* Most publics use GASB, so pipelines read only F1A; a few public institutions report on FASB forms and disappear.
* Fall headcount or fall FTE is often used instead of 12-month instructional-activity FTE.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1 | `HD2022.csv` | CSV | ~6.3k | NCES IPEDS | U.S. Gov public domain | Directory, sector, state |
| 2 | `F2122_F1A.csv` | CSV | ~1.7k | NCES IPEDS | Public domain | GASB finance |
| 3 | `F2122_F2.csv` | CSV | ~1.9k | NCES IPEDS | Public domain | FASB finance |
| 4 | `EFIA2022.csv` | CSV | ~6k | NCES IPEDS | Public domain | 12-month FTE |
| 5 | `FLAGS2022.csv` | CSV | ~6.3k | NCES IPEDS | Public domain | Parent/child indicators by component |
| 6 | `EF2021A.csv` | CSV | ~100k | NCES IPEDS | Public domain | Fall enrollment (tempting alternative) |
| 7 | `hd2022_dictionary.xlsx`, `f2122_f1a_dictionary.xlsx`, `f2122_f2_dictionary.xlsx`, `flags2022_dictionary.xlsx` | XLSX | — | NCES IPEDS | Public domain | Variable definitions |
| 8 | `ipeds_parent_child_reporting_faq.pdf` | PDF | — | NCES | Public domain | Parent/child semantics |
| 9 | `commission_method.pdf` | PDF | — | Task author | — | Rules in §2 |
| 10 | `ipeds_data_feedback_report_sample.pdf` | PDF | — | NCES | Public domain | Peer comparison convention (context) |

## 5. Deterministic solution path

1. Filter the universe; read finance parent/child flags; build families.
2. Take instruction expense from each parent's F1A or F2 record per the method's variable list.
3. Sum EFIA FTE across family members.
4. Compute per-FTE; rank ascending; five + sixth.
5. Contrast: UNITID-level join with zeros; GASB-only; fall FTE.

## 6. The traps

**Trap A — children as zero.** Branch campuses fill the bottom five.

**Trap B — parent expenses over parent-only FTE.** Flagship looks rich; real low spenders shift.

**Trap C — GASB only.** FASB-reporting publics drop out of the universe.

**Trap D — fall FTE.** Changes per-student values for institutions with large summer/online enrollment.

## 7. Why the data is honest

IPEDS publishes exactly what institutions reported, with explicit flags for combined reporting. The method defines the
scope; nothing is planted.

## 8. Draft task prompt (prose)

> The instructional investment grant goes to the five public four-year reporting units with the lowest instruction
> spending per 12-month FTE student, under the commission method in the folder. Using the IPEDS files, build the reporting
> families, compute spending per FTE and tell me the five and the sixth. Provide `instruction_per_fte.csv` with each
> family's members, form used, instruction expenses, FTE, spending per FTE and rank, and `instruction_per_fte.png`, a ranked
> dot plot with the five highlighted and multi-campus families marked. Add a one-page `grant_memo.pdf` naming the five, the
> gap between fifth and sixth, and which units a UNITID-by-UNITID join would have selected.

## 9. Deliverables

* `instruction_per_fte.csv`, `instruction_per_fte.png`, `grant_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* 5 units + 6th + gap; per-FTE values for ~12 units; family membership for 2–3 multi-campus systems; naive-join alternative.

## 11. Golden-output checklist

* Families from finance flags; both forms; family FTE; EFIA; decision stated.

## 12. Build notes (scope tuning)

* Choose a state with at least one multi-campus system reporting finance at the parent, and a public institution on FASB
  forms; confirm Traps A–C each change the five.
* Copy exact flag and variable names from the 2022 dictionaries (IPEDS renames variables occasionally).
