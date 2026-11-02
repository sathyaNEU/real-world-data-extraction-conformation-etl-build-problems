# determinism-check report, task137, 2026-11-02 (architecture 5, target.zip md5 90f3dba97187bcf182764a196ae51bbb, run a5)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The judge thread (one pass, scratch /tmp/determinism-check-task137-a5/, verdict at verdict.md) reproduced every graded figure from the bundle. The year comes out at 337 to 355 raw under every light-aware exposure model it fitted, all inside the 325 to 375 rounding cell for 350. The record's rate by clock hour gives 283, which rounds to 300. The recoveries and repair-cost asks reproduce to the rounding unit. Three watch items are recorded below; none opens a competing answer for the year.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Truck claims to 30 Sep 2026 | 840 | 840 | yes |
| Dark share of km, record | 7.6% | 7.64% | yes |
| Dark share of km, 2027 schedule | 23.3% | 23.31% | yes |
| Dark/day multiplier | about 2.6 | 2.33 to 2.76 by spec (2.43 three bands, 2.73 own 04-07 band, 2.76 light only) | partly: inside the range, tied to no single spec |
| 04-07 dark km, claims vs expected | 48 vs 23.2 | 48; 23.2 | yes |
| 2027 claims by quarter | 346.9 (94.4/72.2/78.5/101.9) | 337.6 to 351.4; every parsimonious model rounds to 350 and 100/75/75/100 | yes |
| Clock-hour-only rate route | 300 (281.9) | 283.4, rounds to 300 | yes |
| Repair cost by depot, 2025 / H1 2026 | 235,100/148,800; 206,400/110,700; 219,100/92,500; 157,300/114,800 | 235,125/148,840; 206,394/110,726; 219,108/92,544; 157,327/114,755 | yes |
| Recoveries by collision quarter | 73,000; 60,000; 43,200; 64,500; 58,000; 81,100 | 72,994; 59,960; 43,179; 64,457; 58,001; 81,052 | yes |

## Competing answers that survived
No competing answer for the main call (300 vs 350 is closed by the dark/day gap visible in the record at the same clock time). Watch items, none of which flips a graded answer:
1. **Quarterly split under flexible models.** A pooled-hour variant (dark hours under 150k km pooled) gives 371 for the year but Q4 112.8, which rounds to 125 rather than 100, and Q1 103.7. In the strictest parsimonious fit Q1 is 90.6, which is 3.1 above the 87.5 edge. A saturated hour x light model gives 323 (300), but it assigns zero rate to dark hour 06 on 14k km and is not a reasonable estimator. The quarter margin is thin where model-form freedom is wide.
2. **Multiplier range.** "About 2.6" sits inside 2.3 to 2.8 and is reproduced by no single obvious band choice. It is a Critical Component, so a reviewer who refits may not match it.
3. **Two inferred ask rules**, forced by the data but stated in no shipped file:
   - Two identical ADAS lines on a camera-and-radar truck are one per sensor. Counting every identical pair once would move Carlisle 2025 to 216,700 and shift all eight depot figures by 1,300 to 2,400.
   - A receipt that matches only a duplicate-closed claim (blank insurer field) takes its payer from the original claim. Without this, 2025Q3 recoveries would be about 39,900 instead of 43,200 (Elsdon 2,816.59 and Fenwick 3,284.49).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 12 | yes |
| Formats | 3 or more | 4 (csv, xlsx, pdf, json) | yes |
| Large file | 25,000 rows or more | 116,424 and 119,448 rows | yes |
| Distractors | 2 or more in metadata, none named in a file name | store_delivery_windows_2027.xlsx, bank-holidays json; a file name does not label either as a distractor | yes |
| Distractors relevant but unused | unused by the solution, ruled out by a shipped fact | Both unused and neither answers a graded quantity. The judge saw no leverage in either. | yes |
| Deliverables | 1 to 3, all in the golden | 2 (xlsx, docx), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | recoveries by 6 quarters and repair cost by 4 depots x 2 periods, nearest £100 stated | yes |
| Prompt shape and 25 or more criteria | identifiable, 25+ | shape 02 in metadata; rubric is generated at the portal and I could not count criteria here (the design note's ask sheet argues the arithmetic) | not verified |
| Reads as real, not LLM generated | yes | The judge saw no authoring leakage. I did not read the goldens' prose. | yes (judge hygiene PASS) |

## Gate G reconciliation
Thread: mechanism `method_or_model_selection`, stumping_family `analytical_non_defect`, surface_read_dependency `no`, sole_data_defect `no`.
Design note and card (read after the verdict): strategy `composition_mix`, a decisive step of rating each kilometre on the light it is driven in beside the clock band, and `stump_class: analytical`. The thread's reading matches the declared design. The surface route is the clock-band or clock-hour rate (281.9 in the card, 283.4 recomputed), a correctly computed rate rather than a wrong shipped figure. The declared distractors (store windows, bank holidays) are not named as the surface read, so they are not too load-bearing. No finding.

## Gate H
`domain: pass`, `layers: pass`, `decisive_step: analytical`. The card's `analyst_test` and `domain_test` agree: a strong analyst who cleaned the data and read Appendix C would still file 300 by the clock-band rate. The thread did not class the step analytical merely because it is a standard method; it recomputed the clock-hour route and landed 300 itself.

## Stump power (Gate F)
Good per the thread. The easy route (rate by time of day, or the trailing 280 a year) gives 283 to 300 and reads as sound. Only separating light from clock hour, which the record confounds with season, reaches 350. The Appendix C table is shipped but nothing names the mechanism. The thread expects a meaningful share of strong runs to land 300. Light-aware fits all land 350, so a solver who finds the mechanism will land the call, and the ladder's ask layer must keep the pair under the bar.

## Findings, ranked
1. Thin quarter margins under flexible models (Q4 112.8 in one pooled variant rounds to 125; Q1 sits 3.1 above its edge in the strictest fit). Watch, not blocking.
2. The multiplier "about 2.6" is not tied to a single specification (2.3 to 2.8). Optional: restate it as a range, or tie it to the stated band choice.
3. Two ask rules (one ADAS line per sensor; payer taken from the original claim for duplicate-closed claims) are inferred from data patterns and filed in no shipped sentence. The golden reading is the only one the data supports, but a literal reader has no sentence to cite.
4. Rubric criteria count not verified here.

## Next action for the author
Optionally restate the multiplier in the solution blocks as a range, and add the one-per-sensor ADAS rule and the duplicate-claim insurer lookup to the solution steps. Neither changes a graded figure, so the build may proceed to ship.
