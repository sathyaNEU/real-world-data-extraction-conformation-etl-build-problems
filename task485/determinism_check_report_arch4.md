# determinism-check report, task485, round 2, 2026-10-26 (judged bundle target.zip md5 56904a09695fe59485b6540a8db76db3)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The methods note files the estimand (2025-26 arrivals reaching their first anniversary, open stays counted at their chance of reaching it) and a selection criterion (completion chosen by squared error on the 2024-25 arrivals open at 31 Aug 2025, estimated from 2023-24). Recomputed from the bundle, the history-aware completion wins (0.155 against 0.172 by sector and months, 0.190 by sector share). It files HOS, FIN and DIG over allowance. The call is unchanged under every history-aware variant the judge tried (30-day-block age, analogous-cut training set, any-prior-stay history, added sex, UK, age, arrival month or quarter). Thinnest margin: HOS 231.6 against 230. The sector-by-months completion files six sectors over (CON 225.9, HSC 447.1, RET 184.0 as well), so the criterion separates the golden from the easy route. No tie and no semantic fork on the main call.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| 2025-26 arrivals (extract, arrival_date, 2014 codes mapped via sector_classification_2026.json) | 4,281 | 4,281 | yes |
| Open at 31 Aug 2026 CON / HSC / RET | 523 / 825 / 511 | same | yes |
| Of which returns | 180 / 239 / 184 | same | yes |
| Backtest, 2,763 open 2024-25 arrivals: sector+history+months | 0.155 | 0.1553 | yes |
| Sector+months | 0.172 | 0.1722 | yes |
| Sector share | 0.190 | 0.1901 | yes |
| Return share 2025-26 CON/HSC/RET | 31/26/33 % | 31.5/26.3/33.1 | yes |
| Return share 2024-25 | 13/12/18 % | 13.1/12.5/18.5 | yes |
| Twelve-month reach 2024-25, returns | 1/3/0 % | 1.4/2.9/0.0 | yes |
| Twelve-month reach 2024-25, first arrivals | 40/51/34 % | 40.4/50.7/33.7 | yes |
| Provisional vs allowance | HOS 253.7/230, FIN 380.5/350, DIG 208.7/190, CON 181.0/210, HSC 380.2/420, RET 149.4/170, OTH 278.6/300, AGR 90.2/110 | same | yes |
| Back series (80 values: arrivals and final long-term, 8 sectors by 5 years) | submission block 4 | all 80 | yes |
| 2023-24 workbook (3,610 arrivals, 1,887 long-term) | n/a | reproduces from the extract | yes |

## Competing answers that survived
Asks 2 and 3 only, not the main call. The files never state that one stay can be registered at two parish offices. The golden removes only records identical on arrival date, sex, birth year, nationality and activity that also ended on the same date on the same notice date (1,341 rows). Alternatives in the judged bundle:
- also removing identical open pairs (94 rows): 48 of 80 cells differ (max 8)
- no de-duplication: 79 of 80 differ (max 35)
- demographics only: 70 of 80 differ

The judge held the golden reading better supported (clean pairs share no parish and sit 3 to 60 days apart; open pairs look like chance coincidences), but not closed by the data. The judge flagged this as optional hardening. See the closing section for what the author did.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 11 | yes |
| Formats | 3 or more | 4 (csv x4, pdf x3, xlsx x3, json) | yes |
| Large file | 25,000 or more rows | extract 25,332, archive 35,550, crosswalk 32,707 | yes |
| Distractors | 2 or more named in metadata.json, none labelled by file name | census_2021_population_by_parish.xlsx, port_passenger_movements_2024_2026.xlsx; neither is labelled in its name; judge found them unused | yes |
| Distractor relevance | unused by solution, weighable, ruled out by a shipped fact | the judge found both present and unused; neither answers a graded quantity | yes |
| Deliverables | 1 to 3, all in the golden | 2 (xlsx, png) | yes |
| Asks | multi-dimensional, unit and rounding stated | ask 1 is 8 verdicts; asks 2 and 3 are 40 values each in whole persons | yes |
| Prompt shape and rubric | identifiable, 25 or more criteria | every sector, year and series graded: about 88 values plus the call and the chart | yes |
| Reads as real work, not LLM generated | no authoring language | judge found none in the PDFs, dates consistent with the fiction | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and metadata: the stump is the out-of-sample choice of the completion conditioned on migration history (a field_method, Layer 2). The declared distractors are the census and port movements, which the thread did not name as the surface read, so they are not load-bearing. No shipped artifact ranks the sectors on the decision. The thread and the note agree; no mismatch.

## Gate H
domain: pass, layers: pass, decisive_step: analytical. This matches the note's `## Three rules`: Layer 1 is the two-system register, crosswalk, TRANSFER records, code switch, day-first dates and double registrations. Layer 2 is completing open stays by history chosen on the filed back-test. The decisive step is not a decoy, not semantics (the sector-by-months route still misses with every field read correctly) and not rule application (the note never names the grouping).

## Stump power (Gate F)
Good. The default sector-by-months completion files six cuts, not three. The right route needs the back-test to be run with the self-join on reg_no as a candidate. One caution for the main thread to weigh with the scored readers' result: the back-test is a filed selection criterion, so a strong solver who runs it and offers history as a candidate lands the golden. That is the library's textbook route, not a judgment the data withholds.

## Findings, ranked
1. Asks 2 and 3: a competing-defensible reading on the double-registration rule (above). Mitigated, not closed, in the judged bundle. Addressed afterwards, see the closing section.
2. Chart: the prompt names no colour or tick, so presentation criteria were not filed. Addressed afterwards.
3. None on the main call.

## Next action for the author
Re-run the leak reader and the free gates on the rebuilt bundle (md5 c11307e9d8a0592f19e47aa823a6c293) and ship it. The judge is not re-run, per the one-pass contract.

## Closing note: changes after the verdict (not re-judged)
After the verdict the author acted on both optional notes in one generator pass. The 89 groups of identical legacy records still open at the extract, which are genuine companions and never double registrations, now differ in birth year. So the over-removal reading the thread measured, and keying on the leaving date alone, now files the golden back series exactly, asserted in checks.py. Block 4's chart line no longer names a colour or a tick. No golden figure moved. The rebuilt bundle is target.zip md5 c11307e9d8a0592f19e47aa823a6c293; this verdict applies to the judged bundle 56904a09695fe59485b6540a8db76db3, and the rebuilt one was not re-judged. I confirmed only that the zip on disk now carries the new md5.
