# determinism-check report, task464 (architecture 11), 2026-11-02

## Verdict
NOT_DETERMINISTIC (main call LD2 is forced and reproduces; supplementary asks 5 and 6, the fund and the storm table, are not forced by the shipped files)
**Disposition:** SEND_BACK
**Stumping type:** mechanism: etl_conformance (cross-system source attribution), stumping_family: analytical_non_defect (main call; judge's Gate H3 reads the decisive step as rule_application), surface_read_dependency: no for the main call, yes for the storm table, sole_data_defect: no

## Why
Fund terms and policy wording say a claim counts on Pennant's bordereau and belongs to the year of its date of loss. Read literally, the bordereau gives the storms 6, 37, 10, 33, 12 and 55 claims and a fund of GBP 368,307. The golden (16, 27, 18, 25, 29, 38 claims; fund GBP 344,143) re-dates 35 bordereau claims by a make-safe job in the repairs log. No shipped file states that rule, and nothing marks the "broker's sheets" the solution cites. Label: answer_contradicts_files (asks 5 and 6). Separately, the main call is forced but its decisive step is read by the judge as rule application (Gate H3 fails).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Window claims / cost (escape of water) | 391 / 2,037,000 | 391 / 2,037,426 | yes |
| Flat-supply vs riser cost | 1,833,000 | 360 claims 1,832,732 (31 riser claims 204,695) | yes |
| LD1 prevented | 356,000 / 62 | 356,467 / 62 | yes |
| LD2 prevented | 727,000 / 148 | 727,224 / 148 | yes |
| LD3 prevented | 471,000 / 97 | 471,080 / 97 | yes |
| LD4 prevented | 348,000 / 68 | 347,795 / 68 | yes |
| LD5 prevented | 411,000 / 77 | 411,407 / 77 | yes |
| Fit cost LD1..LD5 | 179 / 112 / 255 / 238 / 230k | 178,798 / 112,181 / 254,763 / 237,916 / 229,824 | yes (under the golden kit reading) |
| Fund | 344,000 | 344,143 (30% x 1,147,144) | only under the golden storm dating |
| Storm claims | 16/27/18/25/29/38 | bordereau dates: 6/37/10/33/12/55 | no under the literal reading |
| Storm cost | 34/70/72/69/72/97k | bordereau dates: 11/92/36/105/26/142k | no under the literal reading |

## Competing answers that survived
1. Storm dating (asks 5 and 6): bordereau recorded date gives 6/37/10/33/12/55 claims and a fund of GBP 368,307. The golden re-dates 35 consecutive refs (PCS-312887 to 312904 and 312896; 313857 to 313864; 315420 to 315436) by their make-safe job. No filed sentence closes it. The golden rule "storm under way when raised" fails literally for 23 of 153 make-safes (raised 0.1 to 3.6 hours after the last gust hour); strictly "under way" gives 13/21/15/22/23/36 with 23 claims unassigned. The golden counts hold only under "latest storm to have started", which is unstated.
2. Fitting cost: ignoring post-register heating jobs gives LD1 197,542, LD2 116,669, LD3 291,120. The rule is stated only as "when it is fitted". Omitting the extra sensor for 2-bathroom flats gives LD1 178,068 and LD4 235,842 (both change at the 1,000 rounding).
3. Sub-excess claims: 10 escape-of-water claims in the window (7 on LD2) have incurred below the GBP 500 excess, and the wording says such a loss "is not a claim". Excluding them gives 381 / 2,034,621 and LD2 141 / 725,578 (claim count 141, not 148). Ranking unchanged; low risk, but a literal reader can take it.
4. Runner-up by prevented cost is the natural reading; by prevented cost per pound fitted it would be LD1 (1.99). The prompt does not say.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 15 | yes |
| Formats | 3 or more | csv, pdf, xlsx | yes |
| Large file | 25,000 or more rows | repairs log 58,841 rows | yes |
| Distractors in metadata, none labelled in a file name | 2 or more | epc_register, rent_roll named in distractor_files; names carry no label | yes |
| Distractors unused yet weighable | required | judge: epc, rent roll and preliminary listing; none answers a graded quantity | yes |
| Deliverables | 1 to 3 | 2 (xlsx, pdf) | yes |
| Asks state unit and rounding | required | yes in prompt | yes |
| Rubric 25 or more criteria | 25+ | not generated here; pipeline records 36 ask criteria | not verified by me |
| Reads as real, not LLM | required | judge saw no authoring language | yes |

## Gate G reconciliation
Judge: mechanism etl_conformance, family analytical_non_defect, surface_read_dependency no for the call and yes for the storm table, sole_data_defect no. The judge's naive reading (credit the damaged flat) gives LD3 at 109 claims / 581,954, so the surface read is the wrong answer the design intends; it does not name the declared distractors (epc, rent roll) as carrying the task. No Gate G finding on the distractors. Note: the judge says the storm table rests on a planted wrong date (the bordereau date), which the design note describes as a device in the asks (A2 and A3); the asks are free of rule 3, but the unfiled re-dating makes them indeterminate, not merely hard.

## Gate H reconciliation
Judge: domain pass, layers pass, decisive_step rule_application (H3 fails). Design note and card: stump_class analytical, Layer 2 decomposition attribution, "Not rule application: no filed rule says how a claim is traced to its escape". Mismatch on the decisive step. The judge reads the fund terms as filing the estimand (escapes from the supply of a flat on the list, whichever flats the water damaged), so the join through the repairs log is the execution of a stated population, and a strong analyst who read the terms would not credit the damaged flat. This is the finding most likely to predict a send-back.

## Stump power (Gate F)
Moderate. The terms ("whichever flats the water damaged", "would have damaged no flat at all") nearly name the trap, so a strong model looks for the source flat and then needs the stack-and-date join, legacy address mapping, kit rules and storm re-dating. The model most likely to fail is on the asks through unfiled rules, which is the fork above rather than analysis.

## Findings, ranked
1. Storm-dating fork (asks 5 and 6): golden depends on an unfiled re-dating rule; literal reading gives different storm counts, costs and fund.
2. Gate H3: the main call's decisive step is rule application per the judge; disagrees with the note's Three rules.
3. Fitting-cost reading rests on "when it is fitted" for the heating-job supply change (and the sensor rule); at least two rounded figures move.
4. Sub-excess rows can change the graded claim counts (LD2 141 vs 148).
5. Runner-up basis (prevented cost vs per pound fitted) is not stated.
6. Minor: premium workbook Total rows are uncached formulas.

## Next action for the author
Re-root or rebuild: file in the fund terms or policy wording which record dates a storm claim and which storm a claim belongs to, or drop the storm and fund asks; resolve the sub-excess rows; file the supply-when-fitted convention; then redesign the main call so its decisive step is analysis (for example a back-test or validated projection of prevented cost) rather than a stated population executed through a join. The main-call figures above reproduce and stand as the clean-data reference.
