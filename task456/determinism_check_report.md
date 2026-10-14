# determinism-check report, task456, 2026-10-14

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One judge thread (general-purpose, sonnet, medium) saw only a fresh unzip and the inlined blocks. The shipped files force one estimand (article 2.4 full day, article 4.1 one in three, 28 days to 18 January). Annex section 5 says no feed is a record of full days and that every hospital reports in the same way in every region. Under that, the common-rate, free-share two-class latent class model gives the golden shares. The simple readings give all eight regions or none. The main call and all six asks recompute. Thread verdict: /tmp/determinism-check-task456-191318/verdict.md.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Hospital-days | 2,100 | 2,100 | yes |
| Census full / no report | 216 / 82 | 216 / 82 | yes |
| Board Closed days | 1,085 | 1,085 | yes |
| Transfer center CAP declines | 176 | 176 (175 if the 55 carried legacy_case rows replace the old-system rows) | yes, with a note |
| LCA shares | 52.8, 17.9, 10.3, 52.1, 12.4, 67.9, 78.9, 11.2 | identical to 0.1, same optimum from 3 starts | yes |
| Rounded shares | 50, 20, 10, 50, 10, 70, 80, 10 | same | yes |
| Placements out of region | 387 (70, 40, 32, 45, 49, 65, 58, 28) | identical | yes |
| ED diversion hours | 698 | 698.0 | yes |
| ICU Closed hours 24 Nov to 21 Dec | 4,723 | 4,722.9 | yes |

## Competing answers that survived
- None on the main call. Any feed gives all eight regions. Two feeds agreeing gives none. Census alone gives none. Board alone gives all eight. Annex section 5 rules out each of these.
- Ask 5 soft spot: no file says "Advisory with reason EMS diversion" is diversion. Reading Divert only gives 349 hours (NE 44, E 80, SE 56, UC 15, MS 67, SC 25, W 23, MD 39) against the golden 698. The shipped definition is the "series break" reading. The thread rates it defensible data semantics in an ask, not the main call. A literal reader could split.
- Ask 4 minor: 175 against 176 on the CAP count if carried legacy_case rows replace old-system rows. The step text and the golden fix this. It affects only a critical component, not the shares.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 15 | yes |
| Formats | 3 or more | csv, jsonl, pdf, xlsx | yes |
| Large file | 25,000 rows or more | 114,465 rows (jsonl) | yes |
| Distractors | 2 or more, in metadata, not named in a file name | federal respiratory weekly, compact_activations_2024-25 (the first has no label in its name; the second is a historical record, not a labelled distractor name) | yes |
| Distractor role | unused by solution, relevant, ruled out by a shipped fact | the thread found neither carries the call (no hospital-day count, different grain) | yes |
| Deliverables | 1 to 3, all in golden | 2, both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | region by region, rounding in prompt | yes |
| Prompt shape and rubric | shape identifiable, 25 or more criteria | metadata names shape 10; the rubric is generated later and was not counted here | partly (rubric not verified) |
| Realism | no LLM tells, real work product | thread found no authoring or benchmark disclosure, fictional names; golden realism not independently inspected by me | yes (thread) |

## Gate G reconciliation
The thread named the mechanism as latent class estimation, family analytical_non_defect, surface_read_dependency no, and sole_data_defect no. The design note's stump sentence and the card (`stump_class: analytical`) agree: any-feed counting gives all eight regions and the latent class model gives four. The thread named neither declared distractor as the surface read carrying the task. Gate G passes: no shipped artifact ranks the regions wrongly. The card's mechanism and stumping_family fields are None, so only the stump_class, analyst_test and domain_test fields were comparable. They match. No mismatch.

Gate H (thread): domain: pass, layers: pass, decisive_step: analytical. Design note `## Three rules` and the card's `analyst_test` and `domain_test` give the same reading, from the other side.

## Stump power (Gate F)
Moderate to good. Only the error-corrected estimate lands on the four regions. Risk of being too easy because annex section 5 describes the feed errors fairly explicitly, so a strong model may reach for Dawid-Skene or Hui-Walter. The heavy ETL traps sit in the asks, not the call. The thread's lever is to soften the annex description of the feeds' behaviour, which would change the pack and need a rerun.

## Findings, ranked
1. Optional: ask 5 diversion convention (Advisory with EMS diversion) is not stated in any file. No figure moves if the prompt or dictionary pins it.
2. Stump power risk: the annex wording may make the latent class route too obvious.
3. Northeast's bootstrap 5th to 95th percentile (34 to 68) touches one in three at the lower tail. The point estimate is stable.
4. Rounded tens are exact only for the filed estimator.
5. 176 versus 175 CAP count depends on the legacy_case rule, which the steps state.

## Next action for the author
No fix is required. Optionally pin the diversion convention for ask 5 in the data dictionary or prompt, which is a what-not-how filing, then proceed to ship.
