# determinism-check report, task455, 2026-10-15

## Verdict
DETERMINISTIC (main call and every 2026 figure reproduce and are forced; no SOLUTION_WRONG). The 2025 supplementary figures reproduce but rest on two conventions the prompt does not pin (forks F1, F2).
**Disposition:** FIX_NOW
**Stumping type:** mechanism: other (entity resolution of continuing businesses, then rate ranking), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
From the shipped files the top three 2026 birth rates under guideline 3.3 and 3.4 are Eskwell 11.3, Dunrath 9.8, Quarrin 9.5. The runner-up is Caldmere at 7.8, 1.7 below Quarrin (1.667 unrounded). The call turns on removing the 128 new accounts that continue a business: 56 have a filed predecessor, 72 more show the same workers moving from a dead account. The wage-link boundary is clean (no new account between 0.40 and 0.80 shared workers, 128 above 0.80), so any threshold from 0.4 to 0.8 gives the same set. Register county and QCEW county agree for all 702 2026 births and for Q4 2025, so there is no county fork on the main call. No competing answer survives on the main call. Two 2025 conventions are open (below), so one prompt clause is needed.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Accounts first employing in 2026 (qcew month1..3_emplvl, register liability_date) | 702 | 702 | yes |
| Accounts with filed predecessor (register predecessor_account) | 56 | 56 | yes |
| Further continuations shown by the workforce (ui_wage_records worker_key, account_no, qtr; qcew) | 72 | 72 | yes |
| 2026 births by county, Eskwell/Dunrath/Quarrin/Caldmere/Tolbeck/Brennock/Fennamore | 86, 121, 82, 55, 44, 113, 73 | same | yes |
| Set aside by county, same order | 12, 14, 8, 29, 27, 23, 15 | same | yes |
| Q4 2025 establishments with employment | 759, 1236, 863, 702, 612, 1618, 1104 (6,894) | same | yes |
| 2026 rates | 11.3, 9.8, 9.5, 7.8, 7.2, 7.0, 6.6 | 11.33, 9.79, 9.50, 7.83, 7.19, 6.98, 6.61 | yes |
| Gap Caldmere to Quarrin | 1.7 | 1.667 | yes |
| 2025 births (first employment 2025 and 2025 liability date, register county) | 118, 52, 104, 77, 63, 47, 81 (542) | same | yes, under F1 and F2 conventions |
| Q4 2024 denominators by register county | 7.3, 7.4, 8.5, 10.4, 7.1, 7.7, 7.3 (rates; 6,895 total) | same | yes, under F2 convention |
| 2025 deaths | 115, 56, 91, 57, 98, 48, 84 (549); rates 7.1, 8.0, 7.4, 7.7, 11.0, 7.8, 7.6 | same | yes, under literal reading |

## Competing answers that survived
Main call: none.
- Filed predecessors only (the easy route): Eskwell 12.0, Caldmere 11.1, Tolbeck 10.8, Dunrath 10.2, Quarrin 9.8, giving Eskwell, Caldmere, Tolbeck. Closed by the dictionary (an unfiled takeover leaves no predecessor) and the guideline's birth definition, which is not limited to filed transfers.
- No set-aside (raw new accounts): Eskwell 12.9, Caldmere 12.0, Tolbeck 11.6. Closed by the guideline.
- Name, address or FEIN matching: not defensible (no shared FEIN or legal name; trade names recover 18 of 72; 22 births share an address with an older account but are different businesses).
- Rounding: rates ranked unrounded per guideline 4.2; the gap rounds to 1.7 either way.

Supplementary answers (2025), open:
- F1, definition of a 2025 birth. The prompt defines only a 2025 death. The golden uses a 2025 liability date (first payroll), excluding 109 accounts that first show employment in the extract's 2025 months but have old liability dates (reactivated or seasonal). Counting every first employment in 2025 gives 651 births, not 542 (Eskwell 13.6 against 10.4, Dunrath 9.9 against 8.5). The dictionary supports the golden; the prompt does not name it.
- F2, county basis for the Q4 2024 denominator and deaths. Register county (golden): denominators 1621, 703, 1225, 738, 1106, 889, 613. QCEW ZIP-based county through Q2 2025: 1655, 687, 1208, 753, 1090, 873, 629. Birth rates differ by up to 0.2 (Eskwell 10.2, Caldmere 7.6, Brennock 7.1). Deaths by QCEW county: 112, 58, 93, 55, 86, 100, 45 against golden 115, 56, 91, 57, 84, 98, 48. Guideline 3.2 and the dictionary favour the register, but a solver on the QCEW file alone gets different one-decimal figures.
- F3 (minor). Deaths include 38 accounts born and died in 2025 (not in the Q4 2024 base), and 57 source accounts of 2025 new accounts are excluded; both are the literal reading of the prompt. No fix needed.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 10 | yes |
| Formats | 3 or more | csv, pdf, xlsx, txt | yes |
| Large file | 25,000 rows or more | wage records 608,789; QCEW 65,564 | yes |
| Distractors in metadata.json, none labelled by file name | 2 or more | 3 (population estimates, SOS filings, grant disbursements) | yes |
| Distractors unused yet weighable, ruled out by a shipped fact | yes | judge: SOS file needed by no step; none carried the task | yes (the SOS file's lure was not tested by the thread beyond non-use) |
| Deliverables | 1 to 3, all in golden | 2 (pdf, xlsx), both in golden/ | yes |
| Asks multi-dimensional with unit and rounding | yes | counts as whole numbers, rates per 100 to one decimal; per-county, per-year cuts | yes |
| Prompt shape and 25 or more criteria | identifiable, 25+ | shape 01 (ranked list under a cap); rubric count not checked here, generated at build | not verified |
| Reads as real work product, not LLM generated | yes | judge found no authoring leakage; golden realism not re-read here | yes, with that limit |
| Prompt | one paragraph, under 1,000 characters, no persona | one paragraph, 987 characters | yes |

## Gate G reconciliation
Judge: mechanism other (entity resolution of continuing businesses, then rate ranking), stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. The design note's stump sentence names the same pair: the filed-predecessor and address-match routes end on Caldmere, Eskwell, Tolbeck (or Dunrath, Eskwell, Tolbeck) and the workforce-continuity count ends on Dunrath, Eskwell, Quarrin. The numbers agree (11.1/10.8 against 7.8/7.2; Quarrin 9.5). The thread named no declared distractor as the surface read carrying the task. Gate G: no shipped artifact ranks the counties wrong; no mismatch. Caveat the judge raised: the register is incomplete rather than wrong, so a reviewer may read the 72 workforce-only cases as a planted incompleteness. The dictionary's own statement that unfiled takeovers leave no predecessor is the licence, and the guideline's birth definition covers it.

Gate H three-rules line: domain: pass, layers: pass, decisive_step: analytical (borderline against planted/data_semantics). Swap test passes: birth rate, base period and successor linkage are specific to establishment demography. Layer 1 is the ZIP versus geocoded county change, NAICS vintages and two account-numbering schemes. Matches the design note's `## Three rules` (Layer 2 field_method; not semantics; not rule application).

## Stump power (Gate F)
Good. The easy path counts only the 56 filed predecessors, which puts Caldmere (11.1) and Tolbeck (10.8) in the top three and Dunrath and Quarrin out. Only linking worker flows between accounts removes the further 72. The dictionary's note on unfiled takeovers is a hint a strong model could find, but many will stop at the register. Route to live testing if the planted-incompleteness reading worries the author.

## Findings, ranked
1. F1 and F2: the 2025 births, denominators and deaths rest on two conventions the prompt does not state (liability-date birth definition; register county). Affects asks only, up to 0.2 on rates and up to 109 accounts on births.
2. Borderline Gate H read (incomplete register as planted incompleteness); no fix, a live-test call.
3. F3: literal reading, no action.
4. Rubric criteria count and golden realism not re-verified in this pass.

## Hygiene
PASS with notes. 10 files; wage file 608,789 rows, QCEW 65,564. Layer 1 noise present (ZIP versus geocoded county change in Q3 2025, address format change, NAICS 2017 versus 2022, 14 accounts that never report employment). File dates read May 2027, consistent with the 14 May 2027 extract date. No authoring leakage in the dictionary or guideline. Nothing exclusion-level.

## Next action for the author
Run /fix-determinism task455 with one prompt clause that files the WHAT for 2025: 2025 births are counted on the same definition as 2026 (first payroll, by liability date) and counties are the register's. Do not file how continuity is detected. The main call, stump, 2026 figures and solution blocks stay frozen; rebuild the goldens only if the clause changes a figure (it should not).
