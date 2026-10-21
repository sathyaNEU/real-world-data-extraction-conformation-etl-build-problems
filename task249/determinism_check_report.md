# determinism-check report, task249, 2026-10-21

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (one optional pin recorded under Findings)
**Stumping type:** mechanism: decomposition_attribution (counterfactual exposure gain with a time-freed, censoring term), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Gate G: pass, no shipped artifact ranks the forms on the decision question; difficulty survives deleting every wrong number.
Gate H: domain: pass, layers: pass, decisive_step: analytical (the counterfactual estimand: recognised-item excess plus correct answers on items reached only in the time freed).

## Why
One isolated thread (sonnet, medium, Bash only, scratch /tmp/determinism-check-task249-r1/) recomputed every load-bearing figure from the fresh unzip of target.zip (sha256 prefix ff5b5f5b). The flag set (A, B, C, D, G, H) and all twenty sitting counts reproduce. Flagged forms sit at 1.68 to 2.33, the rest at 0.58 or below, so the 1.0 line has wide margin. Regulations 3.4, 7.1, 7.2 and 7.3 file population, unit, threshold and review rule; the method is left open and the data separates the candidates.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Resit sittings 2027 | 6,717 | 6,717 (6,289 without the number chain) | yes |
| Raw scores from bank keys + renumbering | all sittings | 35,275 of 35,275 match | yes |
| Exposure gain A to J | 1.7, 1.7, 2.3, 1.7, 0.6, 0.2, 1.7, 1.8, 0.4, 0.5 | 1.69, 1.74, 2.33, 1.79, 0.58, 0.17, 1.68, 1.87, 0.46, 0.53 | yes |
| Excess on recognised items A, C, G, H, B, D | 1.4, 1.8, 1.2, 1.1, 0.5, 0.5 | 1.44, 1.77, 1.17, 1.15, 0.49, 0.45 | yes (rounding) |
| Time-freed component B, D, I | 1.2, 1.3, 0.3 | 1.25, 1.34, 0.32 | yes |
| Pace on recognised items | about 70 per cent | log-time ratio 0.61 same item, 0.83 same model vs 1.06 unexposed | yes |
| Ask 2 failures A to J | 14, 9, 8, 11, 10, 21, 20, 14, 11, 24 | identical (119 WS_FAIL to 119 sittings, plus 23 Kochi) | yes |
| Ask 3 no-link sittings A to J | 32, 31, 33, 39, 33, 42, 38, 40, 59, 53 | identical | yes |

## Competing answers that survived
- Same-item exposure only, no item-model siblings: flags A, B, D, G (gains A 1.51, B 1.26, C 0.22, D 1.66, G 1.44, H 0.44), differing from the golden on C and H. The prompt and 7.1 say "shown"; regulation 3.4 and the bank's item_model column carry the sibling link, and the data shows the sibling pace effect (0.83 vs 1.06). Under the literal 7.2 counterfactual (correct answers that would not have been had no earlier sitting shown any item) a sibling gain is part of the estimand, so the same-item-only route is a narrower method, not a different estimand. The design note's fork table has no row for siblings (SF2 covers only "an item the candidate reached"). Residual risk: low to moderate.
- Excess on recognised items only (no time-freed term): flags A, C, G, H. This is the intended wrong easy route, analytical, closed by 7.2's counterfactual wording.
- Ask 2 counted by the log's booking_ref instead of the running sitting: C 12, E 7, F 16, G 12, I 9, J 15 against 8, 10, 21, 20, 11, 24. Data semantics on a supplementary ask only, free of the main-call rule.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 17 (the judge counted 18; the folder holds 17) | yes |
| Formats | 3 or more | 5 (10 csv, 3 xlsx, 2 pdf, 1 eml, 1 md) | yes |
| Large file | 25,000 rows or more | 60,443 (event log), 25,337 (r3 export) | yes |
| Distractors in metadata.json, none labelled in a file name | 2 or more | 4 named (practice orders, centre capacity, panel decision log, panel minutes); names are neutral | yes |
| Distractors unused, relevant, ruled out by a shipped fact | yes | unused by the solution; judge found none reproducing a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pdf), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | per-form counts over ten forms, whole numbers stated in prompt | yes |
| Prompt shape and rubric of 25 or more criteria | yes | shape 10 in metadata; design note estimates about 36 criteria (rubric is generated later, not verified here) | yes (estimated) |
| Reads as real, not LLM generated | yes | judge found no authoring disclosure; data_notes.md explanatory but not decisive | yes |

## Gate G reconciliation
Thread: mechanism decomposition_attribution, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: stump_class analytical, stump sentence is the recognised-item excess (A, C, G, H) versus the golden adding the time-freed items (B, D). These agree. The declared distractors are not named as the surface read carrying the task. Gate H line matches the note's Three rules (domain: psychometric exposure/speededness; Layer 1: two export releases, number chains, renumbering, UTC vs local, missing NET_BACK; decisive step: the counterfactual time-freed term, analytical). No mismatch.

## Stump power (Gate F)
The judge expects a strong stump rate: a solver stopping at the excess on recognised items files A, C, G, H and misses B and D, and a second hurdle is counting same-model items. Caution for the main thread: the decisive step is the field's speededness reasoning extended to a shared time limit, and the design note records that both call-only probes (sonnet and opus) landed the golden at the same-item-plus-sibling rung, so the library-method discount (stumping 1.3) applies; weigh this against the scored readers' result.

## Findings, ranked
1. Sibling-exposure convention is not filed in the prompt and has no fork-table row. It moves C and H on the main call under a narrower reading. Optional pin: state in the prompt or add an SF row (and a checks.py assertion) that items written from the same item model count as shown; this files the WHAT, not the method.
2. Ask 2 depends on the sitting-attribution reading of WS_FAIL (booking_ref vs running sitting); closed by SESSION_RESUME and incident reports, and documented as SF13.
3. data_notes.md is mildly explanatory; no step handed over.

## Next action for the author
Keep the build as is for shipping; if a rebuild is acceptable, add the sibling-counts-as-shown row to the fork table with its assertion, otherwise proceed with the scored readers' result.
