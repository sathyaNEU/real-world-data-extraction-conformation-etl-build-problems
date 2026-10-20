# determinism-check report, task249, 2026-10-20

## Verdict
DETERMINISTIC on the main call (no SOLUTION_WRONG); two supplementary-ask forks open.
**Disposition:** FIX_NOW
**Stumping type:** mechanism: statistical_rigor (calibration-sample selection bias / hysteresis), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Gate G: no shipped artifact ranks the candidates wrongly except the published report, whose loads are the procedure's own output (the stump's identity, not a distractor); declared distractors are precipitation_daily and reservoir_levels_daily, neither load-bearing. Classified clean.
Gate H: domain pass, layers pass, decisive_step analytical.

## Why
One isolated sonnet thread (brief: /tmp/determinism-check-task249-4821/judge_brief.md; verdict: /tmp/determinism-check-task249-4821/verdict.md) refitted SMP-03 s6 on all 1,031 samples and reproduced all 14 published loads to 0.1 per cent. A rising-water term puts SKB, JVB, FND and ESK over by 25 to 100+ per cent at any rise threshold from 0 to 3 per cent an hour; the other ten are within 7 per cent. Discharge, season or trip type do not give the same four. The easy route (refit, all stand) is robustly wrong. The two audit asks reproduce all 28 figures, but each leans on an input the files leave unstated.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| 14 published loads (refit) | within 0.1% | ratios 0.9998 to 1.0001 | yes |
| Over by >15%: SKB, JVB, FND, ESK | 4 over, 10 within | same, robust to threshold 0/1.5/3 | yes |
| Hours without usable reading (14) | SKB 702 ... LLU 673 | all 14 match | yes, only with G/O/K inference (fork 1) |
| QC-failed 2027 samples (14) | 12 failed batches | all 14 match | yes, only with statement lot concentration 54.0 (fork 2) |

## Competing answers that survived
1. Flags G, O, K appear in the parquet (8,823, 735, 60 rows) but data_dictionary.md and SMP-03 s5 define only blank, F, M, C; the 14 April 2026 migration is in no shipped file. Literal F/M-only reading gives different hours at all 14 stations (SKB 472, KVF 255, MKE 297 against 702, 459, 647); K as unusable shifts SKB to 704. The golden needs inference from the maintenance log (O rows match logged sonde-out windows 735 of 735; G spans end at cleaning visits). Closing rule: none filed. (Note: DESIGN_NOTE SF20/SF21 assert the log as referee; the judge reads this as inference, not text.)
2. lab_batch_export_2027.csv carries control_nominal_mg_l = 50.0 on every KS-27-06 line; the quality statement says 54.0. On the export's 50.0, failed batches are 16 not 12 and counts differ (SKB 6, MKE 9, HSD 16, SLU 13). The golden uses the statement; the files do not rank the two sources.
3. Chart magnitudes of the "estimate" depend on the rise-threshold convention (JVB 0.49 to 1.02 over). Only the four marked stations are forced; if magnitudes are graded this is unpinned.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 13 | yes |
| Formats | 3+ | 6 (parquet, csv, xlsx, pdf, eml, md) | yes |
| Large file | 25,000+ rows | 1,462,321 (parquet) | yes |
| Distractors in metadata.json, none named in a file name | 2+ | precipitation_daily, reservoir_levels_daily; not labelled in names | yes |
| Distractors unused yet weighable | yes | unused by the refit; weighable as storm/level context; neither answers a graded quantity | yes |
| Deliverables | 1 to 3 | 2 (xlsx, png), both in golden/ | yes |
| Asks multi-dimensional with unit and rounding | yes | 14-station audits, whole hours / whole samples stated | yes |
| Prompt shape and rubric 25+ | identifiable, 25+ | shape 10 (designation over 14 stations plus two audit figures plus chart); 14 verdicts + 28 figures + chart supply well over 25 criteria (rubric itself not generated yet, not checked) | yes (by construction) |
| Not LLM-generated, golden realistic | yes | judge: mild tell in uniform maintenance-log phrasing (about 8 remark strings), not exclusion-level; golden realism not re-judged here | yes, with note |
| No em dashes in prompt/submission | yes | none found | yes |

## Gate G reconciliation
Thread: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: stump_class analytical, analyst_test (refit with discharge/season reproduces loads and files none; the rising-water term alone files the four), domain_test (sediment-load rating curve conditioned on hydrograph limb). The card's mechanism, stumping_family, surface_read_dependency and sole_data_defect fields are empty, so there is nothing to mismatch on those; the substance matches the thread: same easy route, same decisive step, same four stations. Declared distractors were not named by the thread as carrying the task. Gate H line agrees with the design note's Three rules (domain test, swap, task type). No mismatch found; the one gap is that the card should record the four Gate G fields.

## Stump power (Gate F)
Good on the main call: the strong analyst's refit reproduces every published load to 0.1 per cent and so files "all stand"; the rising-water sampling bias must be found from residuals by hydrograph phase and is signposted nowhere. The judge expects real misses on the call and partial credit on the asks. Caveat for the main thread: the decisive step is a refit with an omitted-variable term, a textbook route a strong solver can take, and the judge records only that it is borderline between catching a wrong number and a refit; both stage 4 leak readers landed the call (supplied as context by the coordinator, not weighed in this verdict), so the measured stump will come from the scored readers and portal. The asks' devices (legacy flags, lot concentration) are inference-dependent and are fork findings, not stump credit.

## Findings, ranked
1. Fork 1 (legacy flag letters G, O, K and the 14 April 2026 migration unfiled; ask 2 moves at all 14 stations on the literal reading).
2. Fork 2 (export control_nominal_mg_l 50.0 against the statement's 54.0 for KS-27-06; ask 3 moves to 16 failed batches on the literal reading).
3. Chart magnitudes depend on an unfiled rise-threshold convention (only the marking is forced).
4. Card Gate G fields empty. 5. Uniform maintenance-log remark phrasing, minor.

## Next action for the author
Document, without touching the parquet or samples or filing the call's method: in data_dictionary.md (or SMP-03 s5) state that G, O, K are the pre-14-April-2026 logger codes for F, M, C, and that the batch export's control_nominal_mg_l is a template carry-over, not the certified lot concentration after 1 July 2027 (the quality statement governs); state in the golden that chart magnitudes are not graded or file the marking-only reading. Then re-judge once via /fix-determinism-style single pass.
