# determinism-check report, task166 (architecture 3), 2026-10-26

## Verdict
NOT_DETERMINISTIC (margin_or_boundary_fragility), confined to the "about 600" figure. The call (Southwest) and the runner-up (Texas & Gulf) are forced; all 24 hours, 18 counts and 6 values reproduce.
**Disposition:** FIX_NOW
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The judge's 18 reconstructions of the filed estimand (link rule x founder attribution x window) put the Southwest at 519 to 581, against the golden 608.9. None reaches the golden. The "nearest 100" line is 550, so about half the variants answer 500 and half 600. T&G is 375 to 462 in every variant and is second in all of them. The Southwest is first only through the founder link, by 100 or more in every variant. The naive founders-plus-trend double count gives about 760, so a band of roughly 500 to 650 keeps that wrong route outside.

Two unfiled conventions drive the spread:
1. **Founder link rule.** Mobile only gives 2,228 founders. Mobile plus name where the mobile is missing adds 409. Name matching for users who do have a mobile is mostly noise (median lag 13 months). The judge's median lag is 10 to 10.5 months against the golden 11, and the founding rate is 4.6 to 5.4 per hundred removals against the golden 5.6. The golden's rule (mobile, else name, latest removal) is described only in submission.md step 3. No shipped document files it.
2. **Founder's region.** The golden credits a founder to the leaver's region (90 per cent own-region). The memo says region is "the parent's billing state", which read literally is the founding company's own state. That lowers the Southwest by about 20 to 25. The golden's attribution therefore sits against the memo's literal region definition. SF5 in the design note covers the map but not this attribution. No shipped document closes it.

The usual-intake component also moves (138 to 225 against the golden 206.8) with the exclusion set and window.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| 2025 new paying customers | 1,744 | 1,744 (SW 303 / SE 288 / T&G 388 / MW 264 / NE 222 / PA 279) | yes |
| SW removals Apr-Sep 2026 | 6,487 | 6,488 | yes (off by 1) |
| 2025 monthly average | 267.2 | 267.1 | yes |
| Ratio | 4.05 | 4.05 | yes |
| Founders linked | 4,395 | 2,228 (mobile) to about 2,637 (plus name) | no, link rule unfiled |
| Median lag | 11 months | 10 to 10.5 | borderline |
| Founders per 100 removals | 5.6 | 4.6 to 5.4 | no |
| Own-region share | 90% | 89 to 92% | yes |
| SW founders 2027 | 402.1 | 325 to 406 | partly |
| SW usual intake | 206.8 | 138 to 225 | partly |
| SW 2027 total | 608.9 | 519 to 581 | no |
| T&G 2027 total | 479.3 | 375 to 462 | no (second either way) |
| 24 hours | as listed | all match | yes |
| 18 plan counts | as listed | all match | yes |
| 6 contract values | as listed | all match | yes |

## Competing answers that survived
1. **Main figure.** Mobile-only link with the founder's own billing state gives about 530 to 550, which answers "500". Mobile then name with leaver-region attribution gives about 580, which answers "600". The memo's region wording is the only shipped rule, and it favours the first. The pod placement and runner-up do not move.
2. **Asks 2 and 3, same-day amendments.** 140 of the 1,744 customers have an amendment effective on their first paid invoice date. "In force on" the date keeps the change (golden). Reading "terms before the change" would move plan counts and values. The judge rates this low probability, but it is unfiled in the prompt.

Closed forks: the removal definition (the Seats line), the reactivation test, the parent roll-up, voided invoices and the territory map.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 | yes |
| Formats | 3 or more | 4 (csv, xlsx, pdf, docx) | yes |
| Large file | 25,000 rows or more | 256,204 rows (product_user_directory) | yes |
| Distractors | 2 or more in metadata.json, none named by file | board deck and onboarding_csat_responses named; no file name labels one | yes |
| Distractor relevance | unused, weighable, ruled out by a shipped fact | board deck is old-map FY2020-23 history; CSAT, CRM Sales Region and the cases file's plan/ACV are also weighable. The cases file plan/ACV differ from start terms for 14% and 30% of rows. | yes |
| Deliverables | 1 to 3, all in the golden | 2 (docx, xlsx) | yes |
| Asks | multi-dimensional, unit and rounding stated | 24 + 18 + 6 figures, each with unit and rounding | yes |
| Prompt shape, rubric | identifiable, 25 or more criteria | other, 54 graded figures | yes |
| Reads as real work product | yes | judge saw no LLM or benchmark tells | yes |

No spec-gate failures. The one open item is the figure's determinism.

## Gate G reconciliation
The judge's tags are forecasting / analytical_non_defect / surface no / sole defect no. The design note and card say the same: stump_class analytical, a Layer 2 estimand-identification spillover, nothing planted. The declared distractors (board deck, CSAT) are not the surface read carrying the task. The easy route (own-history trend, season and spend) gives T&G at about 470 to 500, the judge's own figure. Match.

## Gate H reconciliation
Judge: domain pass, layers pass, decisive_step analytical. The design note's `## Three rules` agree (champion-led adoption with a lagged cohort link). The judge adds one caution: discovery rests on an unannounced join. No mismatch.

## Stump power (Gate F)
The judge rates it strong. The easy route misses the call. Opus reader B, running the per-region Poisson route, filed T&G at 500 with the Southwest second at 417. It hit 48 of 48 ask figures. Reader A is still running.

Caution for the main thread: if a solver finds the founder link but lands at 519 to 550, it answers the right region with "500". Whether that scores as a miss on the figure depends on the grading fix below.

## Findings, ranked
1. **Figure fragility.** "About 600 / 608.9 at the nearest 100" is not reproduced by any of the judge's 18 rigorous reconstructions (519 to 581). Fix: grade the figure as a band that holds them (500 to 650, with the 760 double count outside), or ask for the nearest 200. The inputs and analytical surface stay frozen.
2. **Founder region conflicts with the memo's literal region definition.** The golden uses the leaver's region and the memo says the parent's billing state. Either file the attribution (the WHAT: the founding company's region, or the leaver's) or grade a band that covers both. Do not file the HOW of the link.
3. **Link rule unfiled.** Restate critical components 2 and 3 as ranges the files support (median lag 10 to 11 months, founding rate 4.6 to 5.6 per hundred removals, usual intake about 140 to 225). The golden's 4,395 founders, 11 months and 5.6 depend on noisy name matches.
4. **Same-day amendments (asks 2 and 3).** Optionally add "terms in force on the first paid invoice date, changes effective that day included" to the prompt. It is a WHAT filing, not a HOW.
5. **Low:** the 6,487 versus 6,488 removal count is an off-by-one that should be grade-tolerant.

## Next action for the author
Re-grade the 2027 figure as a band (or at the nearest 200) and restate components 2 and 3 as ranges. Do not file the link method. Then decide with the scored readers whether the founder-region attribution needs a one-line WHAT filing in the memo. After that, run one re-judge under `/fix-determinism`.
