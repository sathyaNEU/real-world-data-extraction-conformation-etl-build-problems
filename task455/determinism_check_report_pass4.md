# determinism-check report, task455, 2026-11-01 (pass 4, the one re-judge after FIX_NOW)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: other (successor-predecessor linkage of births from worker flow; the pass 3 thread called it etl_conformance), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Executed literally, guideline FC-G-2027-01 (2.1, 3.3, 3.4) and the prompt give Eskwell, Dunrath, Quarrin (11.3, 9.8, 9.5). Caldmere is first out at 7.8, 1.7 below Quarrin. The 72 workforce continuations separate cleanly from the old account's side: overlap is at least 0.83 for the 72 and at most 0.33 for the other 574 births, so any threshold from 0.34 to 0.83 gives the same 574. The pool window (same quarter, +1, +3) and a one-quarter gap cap all give 128. The new 3.3 sentence ("first it ever reported under its account, not the first in the year being measured") is in the shipped PDF. The thread treats it as licensing the exclusion of the 88 seasonal reopeners from 2025 births. It still notes that no file says liability_date means first payroll. The 2026 figures are unchanged.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| New 2026 accounts | 702 | 702 (qcew first month in 2026; all 2026 liability dates) | yes |
| Filed transfers | 56 | 56 (register predecessor field) | yes |
| Workforce continuations | 72 (128 total) | 72 (128) | yes |
| Births | 574 | 574 | yes |
| 2026 births E/D/Q/C/T/B/F | 86/121/82/55/44/113/73 | same | yes |
| Set-asides | 12/14/8/29/27/23/15 | same | yes |
| Q4 2025 base E/D/Q/C | 759/1,236/863/702 (6,894) | same | yes |
| Rates | 11.3/9.8/9.5/7.8/7.2/7.0/6.6 | same | yes |
| 2025 births | 542 over 6,895; 118/52/104/77/81/63/47 (rates 7.3/7.4/8.5/10.4/7.3/7.1/7.7) | same, with the liability-date-in-2025 filter | yes |
| 2025 deaths | 527; 110/54/88/53/80/96/46 (rates 6.8/7.7/7.2/7.2/7.2/10.8/7.5) | same, with the one-quarter successor test | yes |

## Competing answers that survived
1. Continuation direction (unfiled, deliberately). The golden measures from the old account's side. Competing readings:
   - New side only gives 602 births and Eskwell 11.5, Caldmere 10.1, Dunrath 9.9, with Quarrin out at 9.0.
   - Either side above 0.5 gives 566 births and the same three counties, with Quarrin at 8.9 and 77 births.
   - Filed transfers only gives 646 births and Eskwell 12.0, Caldmere 11.1, Tolbeck 10.8.

   The thread judges the old-side reading the only one the guideline's "is sold ... and goes on" licenses, since a new-side rule would call a 3-person start-up from a 192-worker plant a continuation. It records residual risk for a solver who ties linkage to the new payroll's share. This is the design's stump, not a closed fork, and I record it under stump power.
2. 2025 births population. A qcew-only first month gives 630, not 542. This touches supplementary answer 3 and the chart, not the call. The new 3.3 sentence licenses the golden's reading, but liability_date is undefined in the files. Residual and supplementary only.
3. 2025 deaths successor window. A two-quarter window gives 494, not 527. The one-quarter window separates cleanly (114 above 0.8, none between 0.35 and 0.8). Supplementary only.
4. County source for 2024Q4 to 2025Q2. qcew county_code differs from the register worksite_county_code for 145 accounts. "where its worksite lies" closes it to the register field, so it is closed.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 10 | yes |
| Formats | 3 or more | 4 (csv, pdf, txt, xlsx) | yes |
| Large file | 25,000 rows or more | wage records 616,296; qcew 65,416 | yes |
| Distractors | 2 or more in metadata.json, none labelled in a file name | 4 (population, SOS filings, grant disbursements, LAUS); no file name labels one | yes |
| Distractor behaviour | unused, relevant, ruled out by a shipped fact | thread found none used by the solution or answering a graded quantity (the NAICS crosswalk is reference) | yes (per thread) |
| Deliverables | 1 to 3, all in the golden | 2 (pdf, xlsx), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | county cuts for 2026 and 2025 births, deaths and rates; counts whole, rates to one decimal | yes |
| Prompt shape and 25 criteria | identifiable shape, 25 or more | shape 01 (ranked list under a cap), about 28 graded items plus the chart; the rubric is generated and I did not count it | yes (design count) |
| Not LLM generated, goldens real | | thread found no authoring leakage; the data reads as system extracts | yes (golden realism not re-read by me) |

## Gate G reconciliation
The thread's family analytical_non_defect agrees with the card's `stump_class: analytical`. Both give surface_read_dependency no and sole_data_defect no. The thread's mechanism label (other, linkage from worker flow) differs in wording only from the note's identity_resolution and etl_conformance, and describes the same step. No declared distractor was named as the surface read. The note's default path (register transfers, Caldmere/Eskwell/Tolbeck) and its stronger new-side path (Caldmere/Dunrath/Eskwell at about 10.1) match the thread's two competitors. No mismatch.

Gate H (thread): domain: pass, layers: pass, decisive_step: analytical. Layer 1 is imperfect keys across the register, qcew and wage files, county-code drift and seasonal reopeners. Layer 2 is deciding which new accounts are births by linking old and new payrolls. This agrees with the note's Three rules (No decoy, Not semantics, Not rule application). The thread noted that the decisive step could read as rule application if the overlap rule were stated. It is not stated, so the solver must choose it. The thread did not class the step analytical on the strength of a standard method, because the golden is reached only through the old-side test. The thread also called the layer "borderline with a hidden-continuation planting" and recommended a portal or live test. The note answers this, since the 72 continuations are the UI systems' own take-overs with no memo or marker.

## Stump power (Gate F)
Moderate to good, argued on paper only. The easy route is the filed transfer field alone (646 births, Caldmere/Eskwell/Tolbeck). The next route, reading flow from the new side, also misses (Caldmere/Dunrath/Eskwell). Only the old-account-side flow reaches the golden. A strong solver who finds the wage linkage may still choose the new side. That keeps the call-miss plausible for at least one of the top two. The portal measures the result.

## Findings, ranked
1. Continuation direction unfiled. Kept deliberately, because filing it would name the decisive step. The thread rates the old-side reading as the only licensed one, with residual divergence risk. No action, per the instruction.
2. liability_date is not defined as first payroll anywhere in the files. Supplementary only (2025 births, 542 against 630). The 3.3 sentence licenses the golden. Optional hardening is to state the WHAT in the prompt.
3. The two-quarter death-successor window gives 494 against 527. Supplementary only. Optional hardening is to state a one-quarter window as a WHAT.

## Next action for the author
Ship the cut as it stands. The pass 3 finding 1 is closed, and findings 2 and 3 above are optional.
