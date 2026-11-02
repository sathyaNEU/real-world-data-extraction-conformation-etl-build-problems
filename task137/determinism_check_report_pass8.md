# determinism-check report, task137, 2026-11-02 (pass8, run a5b)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Thread: one sonnet/medium judge on the pass-8 brief; scratch /tmp/determinism-check-task137-a5b/ (verdict.md there). target.zip md5 90f3dba97187bcf182764a196ae51bbb. The prompt is the current single paragraph (644 bytes).

## Why
The 350 call (150 April to September, 200 other six months) is forced by the shipped files. The 2027 schedule drives 23.3 per cent of its kilometres in the dark against 7.64 per cent in the record. Every model that prices light apart from clock time lands 336 to 352 in total, 149 to 152 April to September and 186 to 200 other. All round to 350/150/200 at the nearest 50. The clock-time-only or flat per-km rate lands 281 to 283, which rounds to 300. All supplementary figures reproduced.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Truck claims to 30 Sep 2026 | 840 | 840 (ravensby listing + register; 14 withdrawn, 21 duplicates out) | yes |
| Dark share of record km | 7.6% | 7.64% (both Gridtrak files, Appendix C) | yes |
| Dark share of 2027 km | 23.3% | 23.3% (route_schedule_2027.xlsx) | yes |
| Dark/light ratio | 2.6 | 2.32 to 2.76 by band choice | yes, band-dependent |
| 04:00-07:00 dark km claims | 48 obs, 37.6 / 23.2 expected | 48; 15.6 at light rate; 23.2 at pooled band rate | yes (37.6 not separately listed by the thread) |
| 2027 forecast | 346.9 / 150.7 / 196.3 | variants 337.6 to 351.8 total, Apr-Sep 150.1 to 151.7, other 187.5 to 200.1 | yes, rounds same |
| Clock-only model | about 282 | 283.4 (Apr-Sep 143) | yes |
| Ask 3, six quarters | 73,000 / 60,000 / 43,200 / 64,500 / 58,000 / 81,100 | 72,994 / 59,960 / 43,178 / 64,457 / 58,001 / 81,052 | yes |
| Ask 4, 12 depot-half-year costs | as filed | all 12 reproduce to nearest 100 | yes |
| Note docx asks | 350 split plus chart | not in the judge's bundle; determinate from figures above | not checked by thread |

## Competing answers that survived
None that changes a committed answer. Watch items recorded:
- **325 line vs Poisson sampling.** The lower rounding line is 325. Method range is 336 to 352 (clean), but the sampling interval on the ratio (1.8 to 3.0) gives 319 to 360. Thin but clean margin; every method using the data lands the same way. Fits that ignore the 04:00-07:00 dark km give 314 (300); the thread judges that an unreasonable reading (48 observed against 37.6 modelled).
- **Ledger-duplicate and ADAS-pair convention (ask 4).** Identical lines are one invoice posted twice, except two identical ADAS lines on a camera-and-radar truck. No file states it; derivable from the data and certified by ask 3's penny matches. A solver summing as posted gets Carlisle H1-25 115,300 against 91,700. Main supplementary risk.
- **Seven repair jobs on duplicate-closed notifications.** Golden counts the collision's cost (ask says "collisions"); a filter to Settled/Open claims drops it (Cramlington H1-25 96,800 against 102,100). Golden is the better reading.
- **Half-up penny match.** Q3 2025 receipt 1,621.43 (Ingleby) is half of 3,242.85 and matches only with half-up rounding of 1,621.425.
- Split fractions are unfiled and found by penny matching: unique and self-checking, but demanding.
- Optional fix if a rerun is ever accepted: a one-line prompt pin on collision cost and repeated identical lines. Not required, and it would invalidate prior runs.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / large file | 10+ / 3+ / 25,000+ rows | 12 / 4 (csv, xlsx, pdf, json) / 119,448 rows | yes |
| Distractors | 2+ named in metadata.json, no file name labels one | store_delivery_windows_2027.xlsx, bank-holidays-england-and-wales.json (file names not labelling) | yes |
| Distractor weight and non-use | unused, weighs, shipped fact rules out | bank holidays: Calendar 2027 sheet governs; store windows: first window is depart + 30 min on all 252 routes; neither answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (claims_fund_2027.xlsx, claims_note_2027.docx), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | recoveries by quarter (6), repair cost by depot x half-year (12); claims to nearest 50, money to nearest 100 pounds in the prompt | yes |
| Prompt shape, 25+ criteria | shape 02; 25+ | shape 02 in metadata.json; design note records the rubric at 27 | yes (from the note, not regenerated here) |
| Not LLM-read, goldens business-real | yes | thread saw no authoring or benchmark language; golden realism not re-read in this pass | yes (thread hygiene PASS) |

## Gate G reconciliation
Thread: mechanism forecasting; stumping_family analytical_non_defect; surface_read_dependency no; sole_data_defect no. Design note stump sentence: the easy route rates by clock band and files 300 (281.9); golden 350 (346.9); the step is reading risk off the light, not the clock. Thread's easy route is 283.4 to 300. This matches. The thread names neither declared distractor as the surface read, so the distractors are not too load-bearing. No mismatch.

Gate H (thread): domain pass, layers pass, decisive_step analytical. The design note's Three rules agree: the domain is claims frequency per kilometre of exposure; layer 1 is unit, clock, key and duplicate-posting mess; layer 2 is separating light from clock time. The decisive step is not the field's standard textbook method applied without judgment: the data must separate the clock band from light, and the same light term is used in the golden.

## Stump power (Gate F)
Moderate. Clock-hour or flat per-km models land 281 to 283, which files 300. The call needs the BST conversion, depot sunrise/sunset blocks and a light term. But a simple dark-vs-light Poisson rate with no bands gets 349, so a solver who merely thinks of darkness passes. The 04:00-07:00 check is an optional refinement. Much of the difficulty sits in the ask layer (penny matching in ask 3, ledger dedup with a sensor exception in ask 4). For the main thread to weigh against the ladder: a solver who adds a light term lands the call, so a ladder that keeps one of the top two off it rests on the BST/Appendix C work and the ask layer.

## Findings, ranked
1. No blocking finding.
2. Ask 4 dedup and ADAS exception is unfiled; derivable and cross-certified by ask 3.
3. Thin margin to 325 under sampling uncertainty, clean across methods.
4. Seven duplicate-closed notification jobs and the half-up penny are convention-dependent, golden is the better reading.
5. The note docx was not in the judge's bundle, so it was not checked by the thread.

## Next action for the author
Proceed to ship: record APPROVE with the leak reader's result. Make no change to the prompt or pack.
