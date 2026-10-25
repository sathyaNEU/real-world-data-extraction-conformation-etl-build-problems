# determinism-check report, task166, 2026-10-25

## Verdict
DETERMINISTIC (no SOLUTION_WRONG; one cosmetic solution-text mismatch, see Findings)
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The judge thread (one pass, sonnet, medium, scratch folder only) found the main call forced. The candidate payoff models separate decisively in sample and in a back-test (fit through Oct 2025, test Nov 2025 to Nov 2026), and the whole-stack model wins both. Its regional margin is large (Muskegon and the North about 38 to 39 against the Lakeshore about 24, Grand Rapids about 18, Kalamazoo and Battle Creek about 13 million), so the rounding to 40 and the second place hold. All 32 quote and paid-in-full counts reproduce exactly. The method is left open by the prompt and Policy 7.4.3, and only one family survives validation.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Loans on books 30 Nov 2026 (trial balance, ACTIVE) | 8,813 / USD 436.9M | 8,813 / 436.907M | yes |
| Muskegon and the North principal on books | USD 132.5M | 132.54M | yes |
| Payoffs in full Jan 2019 to Nov 2026 | 5,264 | 3,357 legacy + 1,907 core = 5,264 | yes |
| Loan-months | 362,831 | 368,405 | no, not load-bearing |
| Deviance, stack / first only / own rate | 48,888 / 49,476 / 52,395 | 48,948 / 49,538 / 52,690 | same order, small drift |
| Back-test deviance, stack / first only / own rate | n/a | 9,643 / 9,825 / 10,806 (902, 995, 1,675 predicted vs 943 actual) | stack wins |
| 2027 by region, stack model | 39.2 / 23.9 / 18.5 / 13.5 | 38.2 / 23.6 / 18.0 / 13.4 | ranks and rounding agree |
| 32 count cells (quoted, paid in full) | as filed | all 32 match | yes |

## Competing answers that survived
None. The fork is the payoff model: own note rate gives Grand Rapids (about 60), first-mortgage rate alone gives the Lakeshore, the whole-debt stack gives Muskegon and the North (about 40). Both rivals lose the validation by a wide margin, in sample (590 and 3,740 deviance) and out of sample (180 and 1,160). No fork on the asks: Eastern against UTC moves 0 of 3,172 statements across a quarter. The MTG-with-home-equity classification is bimodal once the first mortgage is amortized to the statement date.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 | yes |
| Formats | 3 or more | csv, xlsx, pdf, txt (4) | yes |
| Large file | 25,000 rows or more | core_he_trial_balance 197,078 rows | yes |
| Distractors | 2 or more in metadata, none labelled by file name | heloc_lines_2026-11.csv, county_house_price_index_2019q1_2026q3.csv; names are neutral | yes |
| Distractor behaviour | unused by solution, relevant, ruled out by a shipped fact | HELOC lines (excluded by Policy 7.4.3 scope) and HPI are available to weigh; neither answers a graded quantity | yes |
| Deliverables | 1 to 3 | 2 (xlsx, png), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 32 counts by center and quarter plus principal to nearest USD 10M, whole-number counts stated | yes |
| Prompt shape / rubric | identifiable, 25 or more criteria | pick-one forecast with a 16-cell table (32 counts) and a chart, so 25 or more is reachable | yes (rubric not yet generated) |
| Not LLM-generated, golden realism | clean | no disclosure or authoring language found by the judge; the thread did not flag the files | yes |

## Gate G reconciliation
Judge: method_or_model_selection, analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: gate_g method_or_model_selection, stump_class analytical, no decoy, no official decoy, decisive_rule_filed false. Match. The judge names no distractor as the surface read carrying the task; the declared distractors (HELOC lines, house price index) carry nothing. No reported number is misleading; the three rival readings come from the analyst's own model choice.

## Gate H reconciliation
Judge: domain pass, layers pass, decisive_step analytical. Card and note's Three rules: field_method layer 2 (a closed-end second's prepayment modeled on the whole stack's blended refinancing incentive), layer 1 the core conversion, codes and senior-lien reporting quirks, No decoy, Not semantics, Not rule application all filled. Match. Policy 7.4.3 files only the estimand (population, outcome, window, region, unit), never the behaviour, which is the WHAT and not the HOW.

## Stump power (Gate F)
The judge reads it as strong: the textbook own-note-rate curve gives Grand Rapids at about 60 and the first-mortgage lock-in gives the Lakeshore, both wrong for the call; the stack is reached only by recovering first-mortgage rates by the amortization identity and running the likelihood comparison. Caveat for the main thread: the stack is also the answer a strong solver reaches by testing the lien-rate candidates on the record (a standard prepayment-modeling route, stumping 1.3), and the judge itself reached the golden by running the candidate set and the validation, no judgment the data did not settle. Weigh this with the scored readers: the portal round 1 on the previous v1 design had both responses landing the call. The 32 counts are an independent multi-step linking layer (legacy xref, March hand sheet by address, MTG statements that also paid the home equity loan) that adds ask-side difficulty.

## Findings, ranked
1. Optional solution-text fix (no rerun): step 2 states 362,831 loan-months, the judge recomputes 368,405 on a closing-month-kept construction. Restate it or drop it. The in-solution deviances and regional figures also drift slightly from the judge's (48,888 vs 48,948; 39.2 vs 38.2 million for Muskegon and the North), which is implementation variance with identical ranks and rounding; the main thread may add a "to within about 1 million" note if the rubric grades the 39.2.
2. Stump power rests on model selection by validation, a recognisable textbook route; confirm with the scored readers before treating as settled. Not a determinism defect.
3. Small caution, not a fork: classifying MTG statements by the mortgage's 30 Nov 2026 balance instead of its balance at statement date misreads statements 2510642 and 2512510 (Grand Rapids Q2 64, Lakeshore Q4 77); the note date, rate, term and original amount in first_mortgage_servicing decide it.
4. Hygiene PASS: 16 files, four formats, dates coherent (pull 3 Dec 2026, policy 21 Oct 2026), no exclusion-level finding.

## Next action for the author
Edit the "362,831 loan-months" figure in submission.md step 2 (and anywhere it is repeated) to the recomputed value or remove it, then proceed to ship; no regeneration of inputs and no rerun.
