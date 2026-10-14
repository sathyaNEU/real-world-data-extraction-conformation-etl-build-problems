# determinism-check report, task459, 2026-10-14

Three isolated judge threads (round 1, 2, 3) each saw a fresh unzip of the bundle and the extracted blocks. Round 3, on the final pack, is the verdict of record.

## Verdict
DETERMINISTIC (round 3)
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Rounds:
| Round | Verdict | Disposition | Scope |
|---|---|---|---|
| 1 | NOT_DETERMINISTIC (underspecified_objective) | SEND_BACK | Workbook asks 3, 4, 5 only; main call, 10 rates and 990 MW forced |
| 2 | DETERMINISTIC | FIX_NOW | Only xlsx document properties named a person (creator, lastModifiedBy); no solver-visible change |
| 3 | DETERMINISTIC | APPROVE | Final pack; no repair; optional dictionary sentence only |

## Why
RP-7 5.2 defines the rate as CO2 per MWh of net generation "it delivers under the commitment". RFO 3.1 to 3.3 make the commitment the plant's entire output at Contract Capacity in every hour. Read literally, that is each plant's CO2 per net MWh at Contract Capacity. Windows of 1, 2, 3 and 5 per cent, 2025 alone, and curves fitted from 80 or 90 per cent of capacity leave all ten plants on the same side of 925 (closest: Tamarack 949 on a fitted curve, Ashby Gulch 907). The price-order fill with pass-over (RFO 5.2) gives Juniper Draw, Kessling Creek and Ashby Gulch, 990 MW. The one live competing reading, the pooled 2024-25 average, gives Tamarack Landing plus Moraine Point, 905 MW. The shipped text rules it out, and it is the intended easy route. Round 1's forks (output window, Pacific year, plant-out definition, clock hours vs unit-hours, indicator field) were closed by filed wording in the repaired pack and re-judged; round 3 found no surviving fork on a graded figure.

## Recomputation ledger
| Figure | Claimed | Judge recomputed (round 3) | Reproduced |
|---|---|---|---|
| Rates lb/MWh: Tamarack, Juniper, Sorrel, Coldbrook, Moraine | 971, 890, 892, 982, 876 | 971.4, 889.5, 891.7, 981.8, 875.6 | yes |
| Rates: Ochre, Lindgren, Ashby, Kessling, Brenmoor | 791, 876, 885, 884, 1,064 | 791.4, 876.3, 885.0, 883.6, 1,064.3 | yes |
| Compliant total | 2,375 MW | 2,375 | yes |
| Fill running totals | 500, 1,030 (pass), 745, 1,020 (pass), 990, 1,255, 1,305 | same | yes |
| Slate | Juniper Draw, Kessling Creek, Ashby Gulch, 990 MW | same | yes |
| Easy route (2025/pooled average) | 905 MW | Tamarack 904 + Moraine 862 = 905 MW | yes |
| Ask A hours/counts (Tamarack to Brenmoor) | 23/2, 15/2, 22/3, 17/1, 85/7, 193/5, 46/2, 16/3, 84/5, 56/4 | 22.85/2, 14.8/2, 22.18/3, 16.7/1, 84.65/7, 193.17/5, 45.72/2, 15.8/3, 84.12/5, 56.05/4 | yes |
| Ask B clock hours | 73, 93, 81, 124, 22, 23, 53, 33, 15, 37 | same | yes |
| Hours at Contract Capacity | 294 to 1,020 | 294 to 1,020 | yes |
| Join | 175,440 meter hours | 175,440 matched, 0 misses | yes |

Sources: camd_hourly_emissions (CO2 short tons x 2000, stacks summed per facility and hour, +8 h to UTC), rfo2026_offer_meter_data, rfo2026_offers_received.xlsx, eia860 (name and county for blank codes), rfo2026_offer_gads_events_2025.csv, camd_monitoring_plans.

## Competing answers that survived
- Pooled/annual average reading (905 MW): closed by RP-7 5.2 "under the commitment" with RFO 3.1 to 3.3. This is the intended wrong route, not an open fork.
- Residual, low risk, supplementary only: "latest entered record stands" for GADS outage starts is not written in the dictionary (recoverable from entered_utc plus CAMD and meter running hours; alternatives move Moraine to 303 h, Ochre 297 h, Kessling 234 h). Round 2 and 3 judged it not required.
- Round 1 minor risks (blank EIA code read as incomplete offer, giving 775 MW; low capacity factors read as outside the standard) were not carried as forks by rounds 2 and 3.
- Round 3 caution: a harsh reader could class the main call as data_semantics because it hangs on "under the commitment"; the judge held analytical.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 12 | yes |
| Formats | 3 or more | 4 (csv 6, xlsx 3, pdf 2, txt 1) | yes |
| Large file | 25,000 rows or more | 245,616 (CAMD), 175,440 (meter) | yes |
| Distractors named in metadata.json | 2 or more, none labelled in a file name | eia923 generation workbook; 2027 planned-outage csv; neither name labels it a distractor | yes |
| Distractor relevance | unused, weighs, ruled out by a shipped fact | EIA-923 is barred by RP-7 5.3 ("only the plant's own records"); planned outages are for 2027, outside the rate; neither answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (pdf, xlsx), both in golden | yes |
| Asks | multi-dimensional, unit and rounding stated | 10 plants x rate, forced hours, outage count, substitute clock hours; whole lb, whole hours, MW stated in prompt | yes |
| Prompt shape and rubric | identifiable shape, 25 or more criteria | shape 01 (ranked list under a cap); 54 criteria per design note | yes |
| Prompt | one paragraph, under 1,000 chars | 758 chars | yes |
| Not LLM generated, goldens realistic | no tells | rounds 2 and 3: operator-style exports, no authoring language; xlsx author scrubbed after round 2 | yes (golden files not opened by the thread; golden-realism is a separate gate) |

## Gate G reconciliation
Thread (round 3): mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: Gate G method_or_model_selection, Layer 2 estimation_fit (emission rate at the committed operating level), stump_strategy population_selection, gap time and population. Card: gate_g method_or_model_selection, decisive_rule_filed false, official_decoy false. The thread's mechanism matches the declared one. The declared distractors (EIA-923, planned outages) were not named as the surface read carrying the task; the easy route is the pooled average of the main CAMD and meter data, not a distractor. Round 3 notes a borderline single_conceptual_flip reading and rejects it because the answer needs a load-conditioned estimate checked across windows and curves. No mismatch.

Gate H line: domain: pass, layers: pass, decisive_step: analytical. This agrees with the design note's Three rules (domain emissions-inventory, Layer 1 DST/UTC offsets, CT-1 to 1A renumbering, blank EIA codes, superseded GADS entries; Layer 2 rate at Contract Capacity; the strong analyst who executes every rule takes 905 MW).

## Stump power (Gate F)
Strong. The pooled or 2025 average clears Tamarack Landing (902 to 904) and fails Sorrel Butte, Kessling Creek and Ashby Gulch (979 to 996), filing 905 MW from different plants; the peak-hours route gives 775 MW. Rates at Contract Capacity need a load-conditioned estimate from the hourly CEMS-to-meter join. Asks A and B add independent failure points (UTC offsets, latest-entry GADS logic, plant-level outages, per-stack indicator counted in clock hours). The card's three-rule fields are consistent.

## Findings, ranked
1. None blocking (round 3).
2. Low: the "latest entry stands" rule for outage starts is not written in the dictionary (supplementary only; optional sentence, no figure moves).
3. Low: the main call rests on one clause, "under the commitment"; a harsh reader could classify it as semantics.
4. Closed in round 2: xlsx document properties named a person; scrubbed to the department.
5. Closed after round 1: workbook-ask forks, by filed wording and dictionary definitions. The design note records that round 1's proposed pins were declined where they file the method (the 2 per cent band).

## Next action for the author
Proceed to ship. The pack is final; any optional dictionary sentence would need a rebuild and the rerun it implies, so skip it unless you want that extra margin.
