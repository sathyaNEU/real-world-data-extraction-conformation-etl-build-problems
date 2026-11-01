# determinism-check report, task455, 2026-11-01 (pass 3)

## Verdict
DETERMINISTIC
**Disposition:** FIX_NOW (one prompt or guideline pin for the 2025 births population; the main call and every 2026 figure stand)
**Stumping type:** mechanism: etl_conformance, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Executed literally, the guideline (2.1, 3.3, 3.4) and the prompt give Eskwell, Dunrath, Quarrin (11.3, 9.8, 9.5), with Caldmere first out at 7.8, 1.7 below Quarrin. The continuation shares computed from the old account's side have an empty band from 0.4 to 0.8, so any threshold in that band gives the same 128 (56 filed transfers plus 72 shown by the workforce). The death flow shares have an empty band from 0.5 to 0.8. The removal of the dictionary and manifest, the renamed register headers, the two added files and the dropped county count did not open a fork on the main call: the thread resolved county basis, transfer rule and base from the PDF guideline and the register headers alone.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| New 2026 accounts | 702 | 702 (qcew, all liability_date 2026) | yes |
| Filed transfers | 56 | 56 | yes |
| Workforce continuations | 72 (128 total) | 72 (128) | yes |
| 2026 births E/D/Q/C/T/B/F | 86/121/82/55/44/113/73 (574) | same | yes |
| Set-asides | 12/14/8/29/27/23/15 | same | yes |
| Q4 2025 base | 759/1236/863/702/612/1618/1104 (6894) | same | yes |
| Rates | 11.3/9.8/9.5/7.8/7.2/7.0/6.6, gap 1.7 | 11.33/9.79/9.50/7.83/7.19/6.98/6.61, gap 1.67 | yes |
| 2025 births | 542 (118/52/104/77/81/63/47) | same, only with the unfiled liability-date-in-2025 filter | conditional |
| 2025 deaths | 527 (110/54/88/53/80/96/46) | same | yes |

## Competing answers that survived
- 2025 births population (open fork). The prompt says "counted as 2026's are". The golden also drops 88 accounts whose liability_date predates 2025 and that re-employed in 2025 after no employment in 2024Q4. Literal first employment in 2025 gives 630 births, not 542 (e.g. Eskwell rate 13.0, not 10.4). It touches supplementary answer 3 and the 2025 chart, not the call. No shipped rule closes it.
- County source for 2024Q4 to 2025Q2: qcew county_code differs from register worksite_county_code for 149 accounts. The prompt's "where its worksite lies" closes it to the register field, but a solver using the qcew code gets different 2025 figures.
- Continuation direction (new-account side only) gives Eskwell, Caldmere, Dunrath. The thread judged it an unreasonable operationalization (it misses 36 takeovers and treats 4-person start-ups as continuing a 192-worker payroll), with a small residual risk because the guideline never states the direction. The design note itself calls this the stump, so it needs a closure line (see Findings).
- Register transfers only, no set-aside, and the union of both sides (136) all give wrong or same-three-county answers and are ruled out by guideline 3.3 or leave the call unchanged.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 10 | yes |
| Formats | 3 or more | 4 (csv, pdf, txt, xlsx) | yes |
| Large file | 25,000 rows or more | wage records 616,296; qcew 65,416 | yes |
| Distractors | 2 or more in metadata.json, none labelled in a file name | 4 (population, SOS filings, grant disbursements, LAUS); the NAICS crosswalk is reference, not a distractor | yes |
| Distractor behaviour | unused, relevant, ruled out by a shipped fact | thread found none used by the solution; SOS and population hold no answer to a graded quantity | yes (per thread) |
| Deliverables | 1 to 3, all in the golden | 2 (pdf, xlsx), both present in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | county cuts for 2026, 2025 births and deaths and rates; counts whole, rates to one decimal | yes |
| Prompt shape and 25 criteria | identifiable shape, 25 or more | shape 01 (ranked list under a cap), about 28 arithmetic items plus chart; rubric is generated, not counted here | yes (design count) |
| Not LLM generated, goldens real | | thread found no authoring leakage; mixed-case city strings and stale county codes read as realistic mess | yes |

## Gate G reconciliation
The thread's mechanism etl_conformance matches the card and note (identity_resolution, G3/G10, Gate G etl_conformance). Stumping family analytical_non_defect agrees with `stump_class: analytical`. surface_read_dependency no, sole_data_defect no, and no declared distractor was named as carrying the task: no distractor is too load-bearing. The note's default path (register transfers only, Caldmere, Eskwell, Tolbeck) is the same wrong answer the thread found for the easy route, and the note's stronger new-side path (Caldmere, Dunrath, Eskwell) matches the thread's new-side-only competitor. No mismatch.

Gate H (thread): domain: pass, layers: pass, decisive_step: analytical. Layer 1 is the stale county code, mixed-case cities, the late register extract and the NAICS vintage change. Layer 2 is business-demography continuity read from worker flows. The note's three-rules lines (No decoy, Not semantics, Not rule application) are consistent with this. The thread did not class the step analytical merely because the method is standard: it reached the golden only through the old-side workforce test.

## Stump power (Gate F)
Good on paper. The easy route (filed transfers, or all 702) lands Eskwell, Caldmere, Tolbeck. Finding the other 72 needs workforce flows read from the old account's side. New-side and any-overlap readings punish the decoys (large closed payrolls feeding small start-ups). The 2025 and death asks add many hard cells. At least one of the top responses plausibly stays on the register route. Not a measured result; the portal measures it.

## Findings, ranked
1. Unfiled 2025 births rule (liability date in 2025 only). Affects supplementary answer 3 and the 2025 chart, not the call. Pin it in the prompt or guideline as a WHAT (population), not a method.
2. The continuation direction is unfiled and the new-side-only reading is the note's own wrong path. The thread judges the old-side reading the only reasonable one, with a small residual risk. File the WHAT in the guideline (for example, a business continues when most of the old account's last-quarter workforce is on the new payroll), not the method, and keep rule 3 intact.
3. County source for 2024Q4 to 2025Q2: closed by "where its worksite lies", low risk.

## Next action for the author
Add one line stating that a 2025 birth is an account first employing in 2025 whose register liability date is also in 2025 (or that accounts with an earlier liability date are not births), regenerate, re-run the free gates and re-judge once. Do not touch the 2026 figures.
