# determinism-check report, task470 (architecture 2), 2026-10-31

Judge thread: one pass, verdict at /tmp/determinism-check-task470-191731/verdict.md (brief judge_brief.md in the same folder). target.zip sha256 26076f7e43ec0c97b2c28988ecfa57066c891a809a12576809f748f028542a10. Replaces the architecture 1 report.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The regulation (Sections 3, 4, 6) fixes the population, the "nobody lived there on any day of 9 to 22 November" rule, the rounding and the 5.0 line. The meter data separates the candidates cleanly: the largest daily evening/morning rise over night use is under 0.3 kWh for 395-396 dwellings and over 1 kWh for all but one of the rest, so every threshold from 0.3 to 0.8 kWh and the window variants give the same 396 vacant dwellings and the same five qualifiers. Every main-call and ask figure reproduced.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Counted dwellings (matrikkel, Bolig, in use by 1 Nov 2026) | 8,020 | 8,020 (1640/520/980/860/430/740/380/1120/560/790) | yes |
| Vacant dwellings | 396 | 396 (66/38/63/33/28/34/31/36/30/37) | yes |
| Shares | 4.0/7.3/6.4/3.8/6.5/4.6/8.2/3.2/5.4/4.7 | same; qualifiers 5802, 5803, 5805, 5807, 5809 | yes |
| Persons registered 1 Nov | 13,599 and all 30 age cells | identical, register of 5 Jan rolled back over 856 later events | yes |
| Land-register holdings | 133/17/149/80/27/141/23/136/86/58 | identical, tinglyst rollback, company closure, name-only titles | yes |

## Competing answers that survived
None on the main call. Rejected: fortnight-average rise (7 qualifiers, ruled out by Section 4 "any day"), median day (Langgrav 5.1, same), register empties (all 10, Section 4), consumption floor (none, heated empties).
One residual low-risk fork on ask 4 only: dokumentdato instead of tinglyst_dato moves 14 deeds (132/16/148/74/25/140/22/135/85/50). The register wording ("held on the land register") favours tinglyst_dato.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / large file | 10 / 3 / 25,000 rows | 14 / 5 (csv, parquet, xlsx, pdf, eml) / 2,720,816 rows | yes |
| Distractors in metadata.json, none named in a file | 2+ | spotpriser_no1, nettselskap_avbrudd | yes (names carry no label; both unused, outage hours miss the night window, prices cannot answer the quantity) |
| Deliverables | 1 to 3, all in golden | 2 (docx, xlsx), both present | yes |
| Asks multi-dimensional, unit and rounding | yes | per-municipality cuts; shares to one decimal stated; counts are integers | yes |
| Prompt shape and 25+ criteria | shape identified | shape 01 (design note: well over 25 criteria; rubric is portal-generated, not verifiable here) | yes, by design note |
| Reads as real, not LLM generated | yes | judge saw no authoring language | yes |
| Stage 4 conditions in prompt | question first, under 1,000 chars | 919 chars | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: gate_g method_or_model_selection, stump_class analytical. Match. The declared distractors (spot prices, outage log) were not named as the surface read carrying the task. Gate H: domain pass, layers pass, decisive_step analytical, matching the card's analyst_test (consumption floor gives none, register gives all ten) and domain_test. The thread's extra route (fortnight-average rise, 7 qualifiers) is ruled out by the filed "any day" wording, so it is a rule reading, not a fork.

Open readings raised by the leak reader:
- Dwelling with no metering point, or points not valid across the fortnight: covered in part. Verdict: every counted dwelling has a household point (8,074 by bruksenhet_id, 99 by address, all unique), 63 points on later units dropped, meter changes summed, estimated-then-replaced deliveries resolved. I checked the shipped metering file myself: 90 points carry a gyldig_til (15 to 20 Nov) and 147 start after 9 Nov, which are the meter changes the verdict sums, and none is left unmeasured. The verdict does not state what a dwelling with a gap would score because none exists. No finding.
- Population register state on 1 Nov: covered. The verdict rolled the 5 Jan 2027 snapshot back over the events and reproduced all 30 cells; it notes a direct join without the rollback loses 105 persons. It did not give the as-is-snapshot totals per municipality, so the as-is alternative is shown wrong only in aggregate, and the regulation's 1 November date (filed in the prompt) closes it.
- Land register holding on 1 Nov: covered for the transfers rollback (tinglyst fork above). The share question: I checked the shipped grunnbok_hjemmel file, every row has andel 1/1 (5,119 rows), so a share-of-unit reading cannot differ from whole-unit. Closed.

## Stump power (Gate F)
Good per the thread: population register, a consumption floor and the fortnight-average rise each land a wrong main call; asks 3 and 4 add rollback and ownership-closure traps. Caution for the main thread: the field's standard smart-meter occupancy method (diurnal rise over night load) is a textbook route a strong solver could land, and the 0.5 kWh figure is filed in Critical Components, not the prompt, with the data (bimodal rise) settling any value from 0.3 to 0.8. Weigh against the ladder in the design note.

## Findings, ranked
1. Low: ask 4 dokumentdato versus tinglyst_dato (14 deeds), literal reading is tinglyst. No fix required.
2. Info: stump-power caution above.

## Next action for the author
None required; ship. Optionally add a fork-table row naming tinglyst_dato as the holding date for ask 4.
