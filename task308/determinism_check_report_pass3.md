# determinism-check report, task308 (pass 3), 2026-10-26

## Verdict
NOT_DETERMINISTIC (no SOLUTION_WRONG on the main call; the step 7 text does not describe how workbook ask 2 was computed)
**Disposition:** SEND_BACK (judge). The pass-2 FIX_NOW (mid-year denominator, prompt and step 6) is closed: ask 1 reproduces on all 12 figures. A new fork sits in workbook ask 2. The repair is a prompt/pack change, so the rebuilt pack must be re-judged.
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Main call is forced: Pennine +0.087 (0.1), Severn Vale -0.084, Coastal North -0.490, Fenland -0.781; critical components 4 / 3.75 / 0.73 / 2.93 reproduce. Workbook ask 2 (buildings sums insured, graded to 0.1m) is not forced: the golden's four totals reproduce only with two conventions, (a) a cancelled term is out unless a later month listed it that began after both the cancellation and the month carrying it, and (b) 17 terms listed once (16 in Oct, 1 in Nov 2025) and never again, with no cancellation row, are off risk. Rule (b) is in neither the prompt, any shipped file nor step 7; as written ("last row is not a cancellation effective by then") those 17 are kept, and every region moves by GBP 0.5 to 1.8m (Coastal North 0.5, Fenland 1.4, Pennine 1.8, Severn Vale 1.7). Taxonomy: competing_defensible_answer. Secondary: Fenland sits on a rounding line.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Pennine layer value | 0.1 | +0.087 | yes |
| Severn Vale | -0.1 | -0.084 | yes |
| Coastal North | -0.5 | -0.490 | yes |
| Fenland | -0.8 | -0.781 (panel from cat-peril claims only: -0.734, rounds -0.7) | yes, fragile |
| Pennine expected recoveries / reinstatement premium / premium | 3.75 / 0.73 / 2.93 | 3.750 / 0.732 / 2.93 | yes |
| Four Pennine freezes exhaust layer; claims per firm 22.6-25.1 to 44.1-49.6 | as filed | 22.6, 23.8, 24.2, 25.1 to 44.1, 47.7, 46.4, 49.6; 64 occurrences, hinge 16.5, 2.8% | yes |
| Ask A, 12 per-policy figures | as filed | all 12 exact (needs date-loss correction on 63 cases, year from unit date, 116 left-open, 68 unmatched added) | yes |
| Ask B, 4 sums insured | 68,319.8 / 79,813.6 / 118,294.5 / 75,396.7 | exact only with rules (a)+(b); step 7 as written is off by 0.5-1.8m | only under an unwritten rule |

## Competing answers that survived
- Ask B, 17 never-relisted terms: kept (written step 7) vs off risk (golden). Totals differ by 0.5-1.8m per region against a 0.1m grade. No shipped note says absence means off risk.
- Ask B, cancellation tests: any cancellation up to 31 Dec out gives -1.2 to +0.9m; reinstated if any later row exists +1.3 to +3.5m; "later month began after the effective date" alone +10.6 to +32.3m; cancellation ignored +18 to +52m.
- Fenland value: panel firms counted from windstorm, flood and freeze claims only gives -0.7 against -0.8 (its 2013-10 windstorm sits at 9.985m against the 10m retention). Pennine, Severn Vale and Coastal North do not change rounding. The design note's SF8 covers all claims versus panel jobs, not this panel population.
- Ask A conventions (judge: findable by an expert but unstated): year from platform date shifts Pennine 2023 by -2.5 pounds; ignoring the left-open rule moves figures up to 0.6 pounds. Step 6 now files them; the prompt does not.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 13 | yes |
| Formats | 3+ | csv, parquet, pdf, xlsx | yes |
| Large file | 25,000+ rows | home_claims parquet 483,625 rows; bordereaux 79,459 rows | yes |
| Distractors in metadata.json | 2+, none named by file name | group_catastrophe_programme_2026.pdf, flood_resilience_survey_2024.csv | yes |
| Distractors unused, relevant | yes | judge saw both as unused; ruled out by shipped facts not separately verified here | yes (judge) |
| Deliverables | 1 to 3, all in golden | 2 (pdf, xlsx), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | yes (GBP million 1dp; pounds and pence) | yes |
| Prompt shape, rubric 25+ | yes | shape identifiable; criteria count not checked in this pass | not verified |
| Reads as real, not LLM generated | yes | no authoring language; parquet carries pandas/pyarrow metadata to strip | minor |

## Gate G reconciliation
Judge: forecasting / analytical_non_defect / surface_read no / sole_data_defect no; the distractors are not the carrying surface read. Design note and card: field_method, post-event demand surge (cost per claim against claims per panel firm, each event re-priced at its 2027 scale), decisive rung silent. These agree. The easy route (index and book scaling only) files Severn Vale at -0.1; the judge confirmed it (-0.084). Gate H: domain pass, layers pass, decisive_step analytical, matching the note's Three rules. Judge's one worry, that no document names the mechanism, is the note's intended "silent" rung and the data separate the candidates strongly.

## Stump power (Gate F)
Good. A strong analyst who index-adjusts and scales to the 2027 book lands on Severn Vale; only the capacity-cost relationship flips to Pennine, robust to hinge 0 to 20, window variants and any 2027 panel up to about 50 firms. The ops report mentions the panel, so the hint is mild. Margin 0.17m over Severn Vale. The method is a field standard (demand surge), so the main thread should weigh it with the scored readers' result.

## Findings, ranked
1. Ask B population is open (rule (b) and the cancellation/reinstatement tests are unfiled; step 7 does not reproduce the golden). Fix in prompt or pack.
2. Fenland -0.781 versus the -0.75 line under a defensible panel population (cat-peril claims only), against the note's claim that every value is 0.031 or more from a bin edge. Pin the panel (a WHAT: which claims count a firm) or move Fenland off the retention boundary.
3. Ask A conventions (date correction, year, left-open) unstated in the prompt; step 6 files them.
4. Strip parquet pandas/pyarrow metadata.

## Next action for the author
Close ask B in the pack or prompt by filing the population (the WHAT, not a procedure): for example in-fiction bordereau notes saying a term not listed in a month is off risk and what a cancellation row means, or have the generator list every term to its end. Make the solution step 7 match the rule actually used. In the same pass pin the panel-firm population behind claims per firm or move Fenland off 9.985m, rebuild, and re-judge once.
