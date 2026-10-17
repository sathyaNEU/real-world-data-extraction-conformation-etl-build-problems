# determinism-check report, task466, 2026-10-17

## Verdict
DETERMINISTIC
**Disposition:** FIX_NOW (two metadata date edits; no graded figure moves)
**Stumping type:** mechanism: statistical_rigor (censored-data likelihood in a low-flow frequency fit), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The 50-year flow (1.55 cfs), the permit withdrawal (0.68 MGD) and the Stage 2 shortfall (0.23 MGD) are forced by the shipped text. WR-14 fixes the LP3 form, skew -0.30, maximum likelihood and the climatic year. The water-works reports quote the 1893 two-MGD stoppage rule, so each "No stoppage" year is a known observation above 3.09 cfs. The permit fixes the 0.50 cfs passby, and the plan fixes the 0.91 MGD demand and the smallest-block rule. The judge found no surviving competing answer.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Gauged years | 74 | 74 (min 1.487 cfs, 1965) | yes |
| Report years | 14 / 40 / 3 | 14 / 40 / 3 (1909, 1918, 1944 missing) | yes |
| 10/25/50/100-yr flow (cfs) | 2.54/1.89/1.55/1.29 | same | yes |
| Withdrawal (MGD) | 1.32/0.90/0.68/0.51 | same | yes |
| Shortfall (MGD) | none/0.01/0.23/0.40 | same | yes |
| Block | 0.3 MGD | 0.3 MGD | yes |
| Recurrence at which 0.3 stops covering | 65 yr (1.44 cfs) | 64.78 yr | yes |
| Eight Stage 2 periods (avg/high) | as filed | match to 2 decimals | yes |

## Competing answers that survived
None accepted. The judge tested these forks:
- Gauge-only fit: 1.87 cfs, block 0.1.
- 40 quiet years dropped: 1.31 cfs, block 0.4.
- 40 quiet years entered at exactly 3.09: 1.23 cfs, block 0.5.

Residual risk: WR-14 never uses the word "censored", and the CSV ask says "where the record gives one", so a literal solver may drop the quiet years. The 1893 agreement quoted in the transcription ties each silent year to a flow above 3.09 cfs. The judge treats dropping them as discarding stated information, not a defensible reading. I flag it for the author to confirm that WR-14's "earlier records at the site" wording is enough to close it.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 | yes |
| Formats | 3 or more | 4 (pdf, csv, txt, xlsx) | yes |
| Large file | 25,000 or more rows | 27,592 (daily values txt) | yes |
| Distractors | 2 or more in metadata, none named in a file name | regional regression PDF, precipitation CSV | yes |
| Distractor use | unused by the solution, weighed, ruled out by a shipped fact | the regression report says it is not used at gaged sites; the judge found neither used | yes |
| Deliverables | 1 to 3, all in the golden | 2, both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | yes | yes |
| Rubric of 25 or more criteria | 25 or more | not generated at this stage; shape 13 (scenarios and the flip point) | not verified |
| Reads as real, not LLM generated | clean | judge saw no leaks. Date incoherences below | fix |

## Gate G reconciliation
Judge: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no.
Design note: censored observation, analytical stump, method selection (G17, G12, G16). The declared distractors are the regression report and the precipitation file, and the judge did not name either as the surface read. No mismatch.
Gate G classification: pass (analytical, not surface-read rejection).
Gate H line: domain pass, layers pass, decisive_step analytical.
Design note, "Not rule application": it says no filed rule gives the censored treatment. This is the exact fork the judge flagged, and the 1893 agreement is the only closure. Keep it explicit in the fork table.

## Stump power (Gate F)
Good. Each easy route lands on a different wrong block: 0.1 (gauge only), 0.4 (quiet years dropped) and 0.5 (quiet years set to 3.09). The golden is 0.3. The judge rates a stump as moderately likely.

## Findings, ranked
1. data_dictionary.csv and folder_contents.csv carry an as_of of 2026-11-20, and metadata.json carries 2026-11-24. Both are after the 2026-10-15 retrieval snapshot and today's date, 2026-10-17.
2. The meter register gives HR-WF an in-service date of 2014-04-22, but the historian HR tag has values from 2012-01-01.
3. The WR-14 wording does not say "censored" (residual risk above). Not a defect.

## Next action for the author
Correct the as_of dates in data_dictionary.csv, folder_contents.csv and metadata.json, and the HR-WF in-service date, in the generator. Rebuild, rezip, and re-judge once only if the rebuild moves a graded figure. None should move.
