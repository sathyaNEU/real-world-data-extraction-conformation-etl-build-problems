# determinism-check report, task478 (architecture 7, run v7r1), 2026-10-23

## Verdict
DETERMINISTIC (no SOLUTION_WRONG)
**Disposition:** FIX_NOW (solution-side only; no input file changes, no rebuild of the bundle)
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The judge thread (one pass, sonnet, medium, scratch path only) recomputed the main call from the bundle: Ashgrove 26, Lindqvist 12, Merriwell 9, Valmora 8, Sedge Hollow 8 tons, with Tamsett State 7 in sixth. It holds for heat-content elasticity 5.5 to 6.5, for the latest test corrected, and for an arithmetic or geometric mean. The elasticity (about 6 per cent per per cent of Westside heat content) is derivable from the shipped files: the monitored boiler PB1's hourly fit gives 6.14 (6.19 over 1.035) and the Westside tests' within-device slope gives 6.26. The call has no open fork. Two ask-only answers carry small residual forks that the write-up does not justify; they do not touch the call.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| CEMS 2026 sum, tbapcd_cems_hourly_2026.csv (34,065 rows) | 32 tons | 31.59 (Ashgrove 23.30, Lindqvist PB1 8.28) | yes |
| Source tests, 112 + 136 | 248 | 248, facility 705 mapped to 0912, Method 19 matches lb/MMBtu to 0.1 per cent | yes |
| Elasticity, PB1 on BTU_FACTOR | about 6 | 6.14 (6.19 over 1.035); test slope 6.26 | yes |
| Facility tons (Ashgrove, Lindqvist, Merriwell, Valmora, Sedge, Tamsett, Haskett) | 26, 12, 9, 8, 8, 7, 4 | 25.96, 12.09, 9.04, 8.12, 8.09, 6.95, 3.89 | yes |
| Remaining facility tons (St. Aldric, Penrose, Harrow, Orchard, Briar, Quarry, Wexley) | 2, 1, 1, 1, 1, 1, 0 | 2.02, 1.14, 1.06, 1.02, 0.94, 0.84, 0.14 | yes |
| Gas, ask 3, total and every facility | 22,371,085 MMBtu | exact match, all 14 | yes |
| Engines, ask 4 total | 10,005 lb | 10,005; per facility within 0.5 lb | yes, except Wexley fork below |

## Competing answers that survived
Both are ask-only; the main call is unaffected.
1. **Wexley Point engine NOx (ask 4).** Golden reads HH.MM from the 5 May first log entry and gets 474 lb. Reading the 5 and 12 May entries (0.30, 0.30) as decimal hours gives 469 lb. The first value that cannot be a multiple of 0.05 is 17 May. Support for 5 May is weak (four identical 0.30 weekly entries; hour-meter excess 0.071 per start against 0.079 the other way). The other six facilities cut over exactly at their first non-multiple-of-0.05 entry. The design note's fork table has no row for this.
2. **Gas boundary for corrected-CCF lines (ask 3).** A bill-date boundary in place of read-to moves Penrose by about 1,394 MMBtu and Orchard by about 28. The Sedge Hollow line closing on 1 July supports read-to (its ratio is flat at 1.006 to 1.011 across twelve months). Not in the fork table by that name; step 5 states "lines read before 1 July".
3. (Not a fork.) The guidance never states that NOx depends on gas heat content; the judge classes this as the intended stump, derivable from PB1 and the test history.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 | yes |
| Formats | 3 or more | CSV 9, XLSX 3, PDF 2 | yes |
| Large file | 25,000 rows or more | tbapcd_cems_hourly_2026.csv 34,065 (no2 hourly 26,280) | yes |
| Distractors | 2 or more named in metadata.json, none labelled by file name | tbapcd_lowry_creek_no2_hourly_2026.csv, tbapcd_lowry_creek_onroad_nox_2026.xlsx, each with a reason; judge also flags the Rule 4307 units | yes |
| Distractor behaviour | unused by solution, relevant enough to weigh, ruled out by a shipped fact | NO2 monitors and on-road NOx are not facility emissions (stated in the plan); neither yields a graded figure | yes |
| Deliverables | 1 to 3, all in golden, no family required | 3 (xlsx, csv, svg), all in task478/golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 14-facility tons, MMBtu, lb; whole tons, whole MMBtu, whole pounds in the prompt | yes |
| Prompt shape and rubric | identifiable, 25 or more criteria | one-paragraph prompt, 825 characters; three 14-row asks plus the 14-bar chart supply well over 25 | yes |
| Reads as real work product, not LLM generated | yes | no authoring or benchmark language found by the judge; no em dashes in prompt.txt or submission.md; dates coherent (extracts 8 to 16 Feb 2027, guidance 17 Feb, plan draft 11 Mar) | yes (golden realism is the golden-realism skill's gate, not re-run here) |

## Gate G reconciliation
Judge: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no.
Card: gate_g `method_or_model_selection`, stump_class `analytical`, decisive_rule_filed false, official_decoy false, validated_decoy false.
Design note stump sentence: latest-test default path versus tests carried by the monitored boiler's rise (about 6 per cent a per cent).
Match on every field. The declared distractors (NO2 monitors, on-road NOx) are not named by the judge as the surface read carrying the task, so they are not too load-bearing. Gate G line: **method_or_model_selection, analytical_non_defect, surface read no, sole data defect no. No shipped artifact ranks the candidates wrongly; the difficulty survives deleting every wrong number.**
Note for the author: the design note's fork table (SF1 to SF26) has no row for the Wexley cut-over or the bill-date versus read-to boundary. `precut.py` passed, but the two residual forks above are unlisted conventions.

## Gate H line
`domain: pass`, `layers: pass`, `decisive_step: analytical`.
Matches the card (`analyst_test`, `domain_test`) and the note's `## Three rules`. Layer 1 is the two source test databases, the renumbered facility, CCF against therms, combined billing, HH.MM logs. Layer 2 is how a burner's NOx rate responds to fuel heat content. The swap test fails with other nouns.

## Stump power (Gate F)
The easy route is each unit's latest filed test as its rate. That puts Tamsett State (tests read on rich May 2026 gas) in the five and Merriwell (tests read on lean August 2025 gas, a canning season on rich 2026 gas) out. Uncorrected alternatives: Tamsett 7.65 to 7.90, Merriwell 6.78 to 6.82, Sedge 7.4 to 9.5. Corrected margin: Merriwell 9.0 against Tamsett 6.95.
The decisive step is a covariate adjustment, estimating the rate's sensitivity to heat content from a monitored unit and back-casting. This is a field-specific estimation step, not a textbook route taken automatically. A capable analyst who checks the test months against the Westside heat-content series could notice the drift, and PB1's fit and the Westside test slope agree, so a solver who looks for the effect finds it. The judge calls the margin wide. The main thread weighs this with the scored readers' result. The judge's borderline note, that "the latest tests mislead" could read as a surface read, is rated an estimand and adjustment problem and not a catch-the-defect problem.

## Findings, ranked
1. Wexley Point engine NOx, tbapcd_cerp_facilities_2027.xlsx ask 4 and tbapcd_rule4702_engine_logs_2026.xlsx: 474 lb against 469 lb on the decimal-hours reading of the 5 and 12 May entries; the 5 May cut-over rests on weak evidence and the solution does not state it. Ask-only. Solution-side fix.
2. Gas boundary, tvg_commercial_billing_extract_2027-02.csv, ask 3: read-to against bill date moves Penrose about 1,394 MMBtu and Orchard about 28. Step 5 says "read before 1 July" without naming the read-to date. Ask-only.
3. Elasticity basis, Critical Component 1 ("about 6"): the write-up should say it comes from the PB1 hourly fit (6.14) and agrees with the Westside tests' within-device slope (6.26), because the guidance does not file the dependence. Main-call stump; no change to the data.
4. Optional, not required: file the estimand "NOx emitted on the gas actually fired in 2026" in the guidance. This is the WHAT, not the HOW, but it is solver-visible, would cost a rebuild and rerun, and would weaken the stump. The judge lists it as optional; not recommended unless the main thread wants it.
5. Hygiene: the judge could not run a cross-batch reference check because other packages are outside its readable path. The main thread's `guard.py heart` covers that.

## Next action for the author
Edit submission.md only: in the step list add (a) the Wexley Point 5 May cut-over with its basis (four identical 0.30 weekly entries, hour-meter excess per start), (b) the read-to date as the CCF boundary, and (c) the PB1 fit (6.14) and the Westside test slope (6.26) as the basis of the elasticity. Add the matching two rows to the design note's fork table with their closure, assert them in checks.py, and rerun `precut.py`. The bundle, goldens and target.zip stay frozen.
