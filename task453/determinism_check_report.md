# determinism-check report, task453, 2026-11-02 (architecture 3, stage 4)

## Verdict
DETERMINISTIC (conditional: the amalgam method is not filed; the data separate it, one residual fork on the names). No SOLUTION_WRONG.
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
From 29,294 permits with a 2026 cremation date, the register's commissioning dates and the three survey tables, the cohort-carried amalgam gives 44.8 per cent of mercury in abated cremations, below 55. Ashgrove and Tallis Creek are the two largest unabated crematoria by mercury; both counted as abated gives 58.9 per cent. All 20 levies and all 25 quarterly bypass counts reproduce. The weak point: no document says how the survey becomes the 2026 decedents' teeth. The yes/no answer holds under every reading; only the designated names move.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| 2026 cremations (permits; equals controller CREMATION cycles) | 29,294 | 29,294 | yes |
| Abated share of mercury | ~45% | 44.8% (53.9 kg total) | yes |
| Ashgrove / Tallis Creek mercury | two largest unabated | 3.93 / 3.67 kg | yes |
| Share with both counted | ~59% | 58.9% | yes |
| 20 levies (e.g. Wynford 34,357; Tallis Creek 73,324; Corbett Narrows 123,131) | listed | all to the dollar | yes |
| 25 quarterly bypass counts | listed | all exact (ET converted to UTC) | yes |

## Competing answers that survived
| Reading | Share | Designated |
|---|---|---|
| Golden: cohort carried along its own change | 44.8% | Ashgrove + Tallis Creek |
| 2016 table at age at death | 41.8% | Tallis Creek + Dunmore Falls |
| 2006 table at age at death | 43.7% | Tallis Creek + Dunmore Falls |
| 2016 cohort at age less 10, no change | 46.3% | Ashgrove + Corbett Narrows |
| 3-wave quadratic | 46.2% | Ashgrove + Corbett Narrows |

- Closing evidence: the amalgam peak moves about ten years a decade across the three waves, so no single wave at age at death fits. A back-test of "repeat last change" gives RMSE 0.56 (men) and 0.63 (women) against 0.98 and 0.80 for no change. The quadratic cannot be back-tested on three waves and is the weakest-supported rival, not excluded by a shipped sentence. Residual risk: low to moderate.
- Levy fork: 171 independent and about 190 Halbrook/Shoreline account credits carry no booking. Matching to the lines they reverse is unambiguous (0 of 171 ambiguous). The alternative, deducting at posting year, moves nearly every levy (Wynford 34,393 vs 34,357; Tallis Creek 73,359 vs 73,324; Corbett Narrows 123,190 vs 123,131; Larchmere 49,577 vs 49,567). Rule 2.2 "net of credits allowed against those fees" favours the golden; the matching is a hard device, not an open reading.
- Bypass fork: alarms uncleared 5 minutes or more open the bypass until PLANT RESET (inlet falls to about 39 C); shorter ones leave it hot (about 170 C). Counting short alarms gives Fenwick 25/30/22/27; reading ET as UTC gives 72 overlaps against 220. Both are ruled out by the labelled columns and the temperature trace.
- Gap: 353 decedents aged 30 to 37 have no 2006 band for age less 20. Every fallback tried gives 44.8 to 44.9 per cent and the same pair. Not decisive.

## Spec gates (checked on the unzipped bundle and metadata)
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats | 10+ / 3+ | 14 / 4 (csv, xlsx, pdf, parquet) | yes |
| Large file | 25,000+ rows | fee returns 74,600; plant log 305,339 | yes |
| Distractors in metadata.json, not named in a file name | 2+ | stack tests PDF, 2026 deaths workbook; neither labelled by name | yes |
| Distractor unused yet weighable | yes | stack tests: post-abatement concentrations; deaths: all dispositions. Neither reproduces a graded figure | yes |
| Deliverables | 1 to 3, all in golden | 2 (certificate PDF, levy xlsx), both in golden/ | yes |
| Asks multi-dimensional with unit and rounding | yes | 20 levies, 25 crematorium-quarter cells, dollars to nearest dollar | yes |
| Rubric 25+ criteria | 25+ | generated at grading; not countable here. 20 levies plus 25 bypass cells plus call components imply it | not verified, likely |
| Reads as real work product, not LLM generated | yes | not contradicted by the judge's hygiene read; golden realism not re-judged here | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Gate H: domain pass, layers pass, decisive_step analytical.
Card: stump_class analytical. The analyst_test and domain_test name the same easy route the thread found, the 2016 age profile at age at death (41.8 per cent, Tallis Creek + Dunmore Falls). Design note `## Three rules` has No decoy, Not semantics and Not rule application lines, and the note's own family (41.8, 43.7, 46.3, 44.0 to 45.0) matches the thread's table. No mismatch.
The declared distractors (stack tests, deaths workbook) were not named by the thread as the surface read. Neither is load-bearing.
The thread's one unfiled point (the estimand) is the design note's declared Layer 2 and is closed by data, not by a withheld rule.

## Stump power (Gate F)
Good, for an analytical reason. A strong analyst's easy route, the latest wave at age at death, files the wrong pair. The no-change cohort files a second wrong pair. The thread did not class the decisive step as the field's standard method reached with no judgment. Asks add two reconstructions no sentence states (credit-to-line matching; bypass spans from alarm, reset and temperature). The main thread weighs this against the design note's ladder.

## Findings, ranked
1. Method unfiled, data-separated (low to moderate): the 3-wave quadratic (46.2, Ashgrove + Corbett Narrows) is not excluded by a shipped sentence. Under the CLAUDE.md rule that the method stays open only where the data separate the candidates, the back-test does separate the rival cohort forms. Optional: file the estimand (the amalgam of those cremated, as of 2026), never the method.
2. Credit-matching device for asks is unstated; the alternative reading moves essentially every levy. Closed by rule 2.2 wording and unambiguous matches.
3. 353 decedents aged 30 to 37 lack a 2006 band; no effect on the result.
4. The side claim that counting cremations designates Corbett Narrows alone was not verified. It is rationale, not a graded figure.
5. Rubric criteria count is unverified.

## Next action for the author
None required to ship on the determinism gate. Optionally, decide whether to file the estimand clause in the prompt (a rerun would follow).
