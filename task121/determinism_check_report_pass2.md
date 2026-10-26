# determinism-check report, task121, 2026-10-26 (architecture 6, stage 4 round 1; the earlier determinism_check_report.md is architecture 5's)

## Verdict
DETERMINISTIC
**Disposition:** FIX_NOW (solution-side pins only, no rerun of the pack, prompt and main call unchanged)
**Stumping type:** mechanism: decomposition_attribution, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no
Judge input: fresh unzip of target.zip (md5 c9cf774f8c770a18fbf0b25a28c0c1ed) at /tmp/determinism-check-task121-054317/target/; verdict at /tmp/determinism-check-task121-054317/verdict.md.

## Why
The main call is forced by the shipped files. The QA program (qa_program_definitions_2025.pdf 1.1) defines a cause as the change without which the measure would have stayed where it was. Rest between shifts is bimodal, so any threshold from 9 to 15 h gives the same quick-return set. From March the quick-return shifts run at 31.1 per cent against 10.7 on rested shifts (10.2 before March), so the rise sits on the quick returns and not on release 13.3, the academy class or the call mix. All five committed answers reproduced.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Under-triage Sep-Feb | 10.5 | 1,310 / 12,620 = 10.45 | yes |
| Under-triage Mar-Aug | 14.8 | 1,471 / 9,966 = 14.76 | yes |
| Quick-return share of shifts pre / post | 1.5 / 15.8 | 66/4,543 = 1.45; 803/5,080 = 15.81 | yes (window-dependent) |
| Rate on quick returns, post | 31.1 | 618 / 1,989 = 31.07 | yes |
| Rested shifts post / pre | 10.7 / 10.2 | 853/7,977 = 10.69; 1,063/10,449 = 10.17 | yes |
| Veterans pre / post | 10.4 / 14.5 | 10.37 / 14.49 | yes |
| Earlier mix, Mar-Aug | 14.7 | 14.73 | yes |
| P90 processing time, 12 months | 121 to 130 | rank ceil(0.9n) on earliest unit-history assignment; all 12 match (CAD unit_assigned gives 142 to 156) | yes |
| Median time to first compression, 12 months | 112 ... 112 | coached primary reviews, recorder offset applied; all 12 match with ties half up | yes |
| 911 answered within 15 s, 12 months | 93.1 ... 93.2 | TG01/02/03/05, answered, not abandoned, local month; all 12 match | yes |

## Competing answers that survived
None decisive. Residual forks:
- Pooled versus mean of monthly rates (10.4/14.7 against 10.5/14.8): QA 2.2 defines the rate as a ratio of counts, so pooled is literal.
- Critical component 2 window: counting Aug 2025 shifts gives 1.4, counting stray Sep 2026 shifts gives 15.9. A supporting figure, not an ask. Pin the window.
- December 2025 median time to first compression is 104.5 s: half up gives 105 (golden), banker's rounding gives 104. The one asked figure that is not rounding-proof. Pin the rounding or accept 104.
- UTC month grouping changes one month of Ask C (Nov), but QA 1.2 pins local time.
Release 13.3 (rested shifts 10.2 to 10.7), academy class (17.2 to 16.9, no change) and the call mix do not survive.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 | yes |
| Formats | 3 or more | 4 (csv, xlsx, pdf, txt) | yes |
| Large file | 25,000 rows or more | CAD 67,532; unit history 71,326; CHE 131,247; ePCR 55,062 | yes |
| Distractors in metadata.json | 2 or more, not labelled by name | protocol_case_reviews, ems_unit_hours (plain names); judge found both unused by the solution | yes |
| Distractor relevance | weighs, ruled out by a shipped fact | not checked arithmetically by me; the judge found nothing answers a graded quantity from them | yes (judge-reported) |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png), both in submission | yes |
| Asks | multi-dimensional, unit and rounding stated | 3 monthly series x 12 months, rate/seconds units and rounding in prompt | yes |
| Prompt shape and rubric | 25 or more criteria | design note counts 47 | yes |
| Not LLM generated, goldens realistic | - | judge: system-extract realism; golden realism not separately read by me | yes (judge-reported) |
Minor hygiene: a few Sep 2026 roster rows and 2 Sep UTC CHE calls sit outside the index's stated end of 31 Aug 2026; no answer changes.

## Gate G reconciliation
Read from DESIGN_NOTE.md after the thread returned. The thread's mechanism (counterfactual attribution among coincident changes, comparison on rested shifts), family (analytical_non_defect), surface_read_dependency no and sole_data_defect no match the design: Layer 2 is `estimand_identification`, exposure varying inside the period, with the rest built from shifts worked. No shipped artifact ranks the candidates; the release note claims nothing about triage. The declared distractors (case reviews, unit hours) are not the surface read; the surface read is release 13.3, a named coincident change and not a declared distractor. No mismatch.
Gate H: thread says domain pass, layers pass, decisive_step analytical, with a residual note that discovering the rest-hours feature is borderline feature discovery. The design note's Three rules give the same decisive step (build each call-taker's rest, match calls to shifts, compare quick-return against rested before and from March) and the same domain test. Consistent.

## Stump power (Gate F)
Moderate to good per the judge. The easy route (release 13.3, 18.1 per cent against 10.5) is plausible and the roster-derived rest comparison separates it; the asks add independent traps (stale unit_assigned, recorder offset and calibration duplicates, TG07 and abandoned calls). The decisive step is a comparison no document invites, which is analysis and not a filed rule. Stump evidence rests on the scored readers.

## Findings, ranked
1. December 2025 median time to first compression is a 104.5 s tie; pin half-up 105 in the solution/rubric, accepting 104 or naming the rounding.
2. Critical component 2 needs its window stated (shifts starting 1 Sep 2025 to 28 Feb 2026 and 1 Mar to 31 Aug 2026).
3. Optional tidy-up: prune the Sep 2026 roster rows and 2 Sep UTC calls (only if a rebuild happens anyway).

## Next action for the author
Edit the submission and rubric text for findings 1 and 2 (solution side only; the prompt, target.zip and the main call stay frozen), then ship; no second judge pass is needed since nothing the solver sees changes.
