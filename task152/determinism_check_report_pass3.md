# determinism-check report, task152, pass 3, 2026-11-01

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Cut judged: 22 files, README removed, Exhibit C.3.1 now has the midnight-to-midnight Arizona-time sentence. The coordinator notes C.3.1 was narrowed after this cut (legacy billing system records a day's total at 0000 of the next date; the meter data system records it against the day itself). The judge's dating finding (legacy file date L = energy of day L-1; MDM read_date = same day; the overlap agrees at a one-day offset) is the reading that sentence states, and no figure moved. The narrowed text was not re-judged.

## Why
Every committed figure recomputes from the shipped files. Time zones, units, meter 0417, legacy dating, SCADA tag meanings (crosswalk) and the CLN work order Completed date are determinate without the README: each is closed by a shipped file or the data (the overlap offset, the hourly header UTC-7, the WO step at Completed date). The thread's literal readings that differ from the golden either do not reproduce or are defeated by shipped data.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Base PR Oct 2025 to Sep 2026 | 63.7% | 63.706% | yes |
| Wear (Dec 2025 post-wash vs 2016) | 14% | 13.8% | yes |
| Repowered PR | 85% | 84.8% | yes |
| P50 / sd | 73,000 / 1,900 | 73,089 or 73,279 / 1,923 or 1,928 | yes |
| Volume | 70,000 | 70,624 or 70,807, floored | yes |
| Availability, 16 inverters | as filed | exact to 2 dp | yes |
| Over/under 2016 to 2025 | as filed | all 10 match | yes |

## Competing answers that survived
- Wear against sealed Table A rather than the plant's own 2016 level: volume 71,000 (P50 74,000, sd 2,000). Closed by data: the plant's as-new level already sat 1 to 4% under Table A (DC cabling and mismatch the repowering keeps). Residual, not open.
- Availability, logger-gap hours removed from P: moves the second decimal by -0.01 to -0.02. P is defined by the met station, so the filed reading is the literal one. Small residual.
- Easy route (60,000), no temperature correction (67,000), WO Created date, k=0 to 2 (71,000), UTC years (sd 2,000): all distinct and each ruled out.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / large file | 10 / 3 / 25,000 rows | 22 / 5 / 219,144 rows | yes |
| Distractors | 2+ in metadata.json, none named in a file | tresco_repowering_program pdf, palo_verde_forwards csv | yes (names carry no label) |
| Distractors unused, weigh, ruled out | yes | forward curve and repowering percentages, ruled out by shipped data; neither answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pdf), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 16-inverter and 10-year tables, rounding in prompt | yes |
| Prompt shape / 25 criteria | identifiable, 25+ | single-figure shape; criteria counted in design note Ask sheet, count not re-derived | not re-verified |
| Reads as real work product | yes | thread found no tool banners or hidden content; minor cosmetic WO date and ack_by differences | yes |

## Gate G reconciliation
Thread: mechanism forecasting, analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: stump_class analytical, with analyst_test (60,000 easy route; 76,000, 73,000, 72,000 overshoots) and domain_test (separating wear from retained losses). Design note stump sentence and Three rules agree. No mismatch. Gate G: no shipped artifact ranks the candidates wrongly; the declared distractors are not the surface read.

Gate H: domain pass (PV yield P50/P90, wear vs soiling, swap test fails to read the same), layers pass, decisive_step analytical (wear separated from retained losses, then the out-of-year spread).

## Stump power (Gate F)
Strong on paper: the easy route lands 60,000, 10,000 MWh low, and the refinements land 71,000 to 76,000. Margin: the answers hold for PR 0.8410 to 0.8523 and the estimate is 0.8478, so the upper edge is 0.45% away. The wear estimators tried all give 0.861 to 0.8626. The main thread weighs this against the ladder.

## Findings, ranked
1. Thin upper margin on the volume (clean, not contested). No action.
2. Table A fork is the only live one that moves the answer; data closes it.
3. Logger-gap hours in availability: small residual.
4. Cosmetic: owner-stop WO dates and ack_by differ; no figure moves.
5. Narrowed C.3.1 sentence not covered by this judge pass.

## Next action for the author
Proceed to ship; no repair needed.
