# determinism-check report, task471, 2026-10-18

## Verdict
DETERMINISTIC (SOLUTION_WRONG on wording only)
**Disposition:** FIX_NOW
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One judge thread (sonnet, medium, run r1) saw only a fresh unzip of target.zip (sha256 8851287dbed0691d) and the five
blocks. Read literally, the standard (2.2, 2.6, 4.1) counts every trip, so the survey is expanded to the lots' entries,
and the methods report (3.1, 3.2, Table 1) says a card comes back only when the car leaves and the boxes closed on the
night of day 30; long stays handed late in a wave cannot be among the returns, and weighting by the handed cards on
the days that left room for each stay gives the golden: Tampa, Phoenix and Washington. The card-share expansion gives
Washington, New York and Dallas. Every load-bearing figure reproduced. The one defect is in the write-up: step 2 said
the shortlist was cut by Chicago, Charlotte, Detroit and Orlando, but only Orlando is on Appendix A.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Transient entries, three long-stay lots, by quarter | 204,574 / 239,891 / 261,189 / 228,402 | the same, both layouts | yes |
| Cards after the repeated batch | 74,377 (70 rows of batch 3-07 dropped) | 74,377, matching Table 1 | yes |
| Handout log | 336 rows | 242,701 cards handed, matching Table 1; every card number in a range; handout day plus nights equals the box date on every card | yes |
| Service-area cards | 5,347 | 5,347 | yes |
| Candidates | 14 | the shortlist's 15 less Orlando (seasonal Sanford) | yes |
| Trips, 14 candidates | Tampa 6,600 ... Fort Lauderdale 1,300 | 6,588 ... 1,278, every one in its hundred | yes |
| Passengers, 14 candidates | Tampa 10,900 ... | 10,912 ..., every one in its hundred (Q4 as written) | yes |
| Gap, Washington less New York | 1,200 | 1,197 | yes |

## Competing answers that survived
None on the call. Expanding by lot, per-plaza weights, weights by day count and the box cutoff a day either way all
keep the three and the first market left out; the gap stays in its hundred except the cutoff a day late (1,240), which
the methods report's night of day 30 rules out. The coded `party` against Q4 as written changes the passengers ask
only; the judge reads Q4 as written as the traveller's answer to "including you" (standard 2.7, counted in full).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 | yes |
| Formats | 3 or more | csv, pdf, xlsx | yes |
| Large file | 25,000 rows or more | 74,447 (cards), 148,754 (verbatims) | yes |
| Distractors named, none labelled in a file name | 2 or more | metadata.json names the DB1B market file (declared wrong-basis), the T-100 segments and the 2025 ground access workbook; no file name labels one | yes |
| Distractors unused yet weighable | yes | the DB1B file ranks New York, Denver and Boston on Kessick Valley's own passengers, ruled out by standard 2.1; the T-100 and the access survey rank nothing | yes |
| Deliverables | 1 to 3, all in the golden | 2 (csv, docx) | yes |
| Asks | multi-dimensional, unit and rounding stated | 14 markets' trips and passengers, nearest hundred | yes |
| Prompt shape and rubric | shape identifiable; 25 or more criteria | shape 01; 28 figures, the call, the first left out, the gap and the chart | yes |
| Not LLM generated | yes | no authoring leakage, coherent dates | yes |

## Gate G reconciliation
Thread: statistical_rigor, analytical_non_defect, no surface read, no sole data defect. The card files Gate G as
method_or_model_selection (the estimator the fieldwork design forces); both name the same decisive step, a
censoring-aware expansion of the replies, and both rule out a surface read. The thread's wrong answer (Washington, New
York and Dallas from the card shares) is the default path's Ends on. The declared distractor carries nothing. No
finding.

Gate H: domain pass, layers pass, decisive_step analytical, matching the note's Three rules and the card's
stump_class analytical.

## Stump power (Gate F)
Moderate: the methods report states the box timing plainly and the handout log gives the exact counts, so a careful
model that asks when a card can come back finds the step; one that expands card shares does not. The judge puts any
further difficulty in the asks, not the call.

## Findings, ranked
1. FIX_NOW, solution: step 2 named Chicago, Charlotte and Detroit as cut from the shortlist; only Orlando is on it.
   Fixed in writeup.py and in the brief (golden.py), both now from figures.json's served_shortlisted.

## Next action for the author
Rebuild with the wording fix and re-judge once.
