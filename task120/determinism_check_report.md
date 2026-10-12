# determinism-check report, task120, 2026-10-12

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: decomposition_attribution (judge), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The DEP letter defines maximum day demand (water used per Eastern calendar day, mains loss counted as used), firm capacity (latest pump test per well, less the largest) and the loss formulas. The facilities summary supplies gallons per foot for each tank. Executed word for word, these give 4,469,527 gal on 2026-08-20 (3,103.84 gpm) against firm capacity 2,920 gpm, so 183.84 gpm, which is 184 gpm whether rounded or rounded up. Every load-bearing and supplementary figure reproduced. Gates A to E pass for the main call. One residual on supplementary asks (loss series, share, group use) is noted below: the sub-meter question.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Max-use day | 2026-08-20 | 2026-08-20 (next 24 Aug, 3,757,396) | yes |
| Production that day | 3,716,646 | 3,716,646 (log) | yes |
| Tank storage change | -752,881 | -752,881 (historian, gal/ft) | yes |
| Water used | 4,469,527 | 4,469,527 | yes |
| gpm | 3,103.8 | 3,103.84 | yes |
| Firm capacity | 2,920 | 2,920 | yes |
| Addition | 184 | 183.84, so 184 | yes |
| Monthly loss Oct25 to Sep26 | 9,249,728 / 8,692,700 / 8,985,071 / 9,346,726 / 8,267,450 / 9,031,386 / 9,488,916 / 10,095,785 / 12,119,389 / 15,036,717 / 14,447,009 / 10,868,335 | all 12 identical | yes |
| Annual loss | 125,629,212 | 125,629,212 | yes |
| Annual used | 1,021,278,949 | 1,021,278,949 | yes |
| Share | 12.3% | 12.301% | yes |
| Residence halls | 280,319,280 | 280,319,280 | yes |
| Academic + research | 366,798,732 | 366,798,732 | yes |
| Athletics | 36,193,200 | 36,193,200 | yes |
| Central energy plant | 87,422,200 | 87,422,200 | yes |

## Competing answers that survived
- Main call: none survived. Production-as-use (Aug 21, 4,136,417, none), UTC days (117), fixed EST midnight (145), main-zone tanks only (30 rounded up, 29 rounded off), all closed by the letter's "water used", "midnight to midnight, Eastern time", "the system", and the facilities summary's hill-zone tanks.
- Supplementary asks (loss series, share, group use): summing every inventory meter, with no service-line reconciliation, gives loss 79,753,351 and 7.8 per cent, residence 291,430,218 and plant 112,140,170. No shipped sentence says that eight meters (M-1118, M-3251, M-1661, M-2895, M-3341, M-5361, M-1297, M-5980) sit downstream of a building's service meter. The letter says deliveries are "as their meters recorded it". It is recoverable from the 2024 service line inventory (one domestic line per building) plus the meter locations, and "delivered to the building" forces it physically. The design note declares this as the P1 device on the asks, which the spec allows (asks may turn on semantics). The judge flagged it as residual Gate C risk on the supplementary asks only. The main call does not depend on it.
- Building 47 joined to the current inventory moves 1,523,470 gal from academic and research to residence halls. The removed-buildings sheet resolves it (P2).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | 10 or more | 17 | yes |
| Formats | 3 or more | 5 (csv, xlsx, pdf, docx, txt) | yes |
| Large file | 25,000 rows or more | SCADA historian 237,168 rows | yes |
| Distractors | 2 or more in metadata.json, none labelled in names | 3 (weather station, irrigation programs, borough quality report). No file name says distractor | yes |
| Distractors relevant, unused, ruled out | same world, answers nothing | The weather station and irrigation controller are the same-world operations records and are used by no figure. The borough quality report is only loosely relevant (a different water system), the weakest of the three. None answers the decision question | yes, weakest on the borough report |
| Deliverables | 1 to 3 | 2 (xlsx, docx) | yes |
| Asks multi-dimensional | yes | 12 monthly figures, year, share, bars, 4 groups | yes |
| Deliverables present | all | The goldens were not part of this bundle check. Design note: both built, verify.py passes | not independently checked |
| Units and rounding | stated | Prompt closes with whole gallons, whole gpm and per cent to one decimal | yes |
| Prompt shape and 25 criteria | 25 or more | Shape `other`, 28 criteria planned (call 4, series 14, chart 4, groups 4, files 2) | yes |
| Realism | no LLM tells | Judge found the pack coherent, in-fiction voice, no authoring language. Cosmetic: the operators' log is dated 2026-10-12, later than the other records' 10-06 to 10-09 exports | yes |

## Gate G reconciliation
The judge classified the mechanism as decomposition_attribution and the family as analytical_non_defect. The design note and card say `gate_g: method_or_model_selection` and `stump_strategy: other` (a mass balance). The label differs, and the design note explicitly rejected decomposition_attribution ("no contested split"). Both describe the same construction: use = production less storage change, an estimand and method choice on honest data. On substance there is no mismatch. The card's `stump_class: analytical`, `analyst_test` (production-as-use files none; partial constructions file 30, 117 or none) and the judge's competing-answer table agree. The judge also found a fixed-EST-midnight cell (145) that the design note's grid omits, which the letter closes. The judge did not name a declared distractor as the surface read.
Reconciliation: consistent. It is only a taxonomy label difference.

## Gate H
domain: pass, layers: pass, decisive_step: analytical. This matches the card's `domain_test` (maximum-day demand, firm capacity and a loss audit are specific to water supply) and `analyst_test`.

## Stump power (Gate F)
Good. The tempting path is the largest production day (Aug 21, the refill day), which gives 2,872.5 gpm against 2,920 and "add nothing". Only the storage balance at Eastern midnights finds Aug 20 and 184. Near misses each give a different wrong answer: UTC days 117, fixed EST 145, main-zone only 29 or 30. The judge named no too-easy signal.

## Findings, ranked
1. Low, supplementary asks only: the sub-meter downstream relationship (8 meters) has no shipped statement. This is a declared device and legal as an ask hazard, so no change is required. If the author wants it closed, add a "downstream of" note to `meter_inventory_2026-10-08.xlsx`. That changes the bundle and the stump-bearing device, so it is optional.
2. Cosmetic: the operators' log is dated 2026-10-12, later than the 10-06 to 10-09 export dates of the other records. It touches no figure.
3. Hygiene, outside the bundle: `task120/DESIGN_NOTE.md` lines 258 to 263 (`## Tried and rejected`) still carry the v1 tax-tier lines, and the header paragraph at the top contains a stray heading inside the Stage 3 build paragraph. The bundle is unaffected.
4. Weakest declared distractor: the borough quality report is only loosely relevant to the decision.

## Next action for the author
Proceed to SHIP: no determinism change is required.
