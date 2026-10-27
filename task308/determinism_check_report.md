# determinism-check report, task308, 2026-10-27

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (two optional wording tightenings, see Findings)
**Stumping type:** mechanism: method_or_model_selection (conditional common-mode capacity valuation, with etl_conformance for the member figures), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One judge thread (sonnet, medium) recomputed every load-bearing figure from a fresh unzip. Everything reproduces. The award is forced: Red Willow import is the only offer with a large positive net value once Ketchum Ridge is valued at the availability of the Northgate IT peakers in the shortfall hours. In all 337 shortfall hours the ten IT peakers are out together under cause 9130, so Ketchum removes 0 MWh (RA-3 s7, "in that hour, judged from the evidence the record holds"). Sensitivity variants not licensed by the filed rules (first-report revision, whole-hour outages) do not change the award.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Fleet EUE, MWh/yr | 9,500 | 9,506.7 | yes (to 100) |
| Ketchum Ridge removed | 0 | 0.0 | yes |
| Red Willow removed | 7,100 | 7,077.8 | yes |
| Sandhill Draw removed | 2,000 | 2,012.2 | yes |
| Coulee Flats removed | 400 | 432.7 | yes |
| Payments, USD M | 23.2 / 35.8 / 28.4 / 25.8 | 23.22 / 35.81 / 28.35 / 25.8 | yes (Sandhill 28.35 is a half-up tie) |
| Net values, USD M | -23 / 106 / 12 / -17 | -23.2 / 105.8 / 11.9 / -17.1 | yes |
| Member 2025 net energy (8) | golden | identical | yes |
| Member 12-CP averages (8) | golden | identical | yes |

## Competing answers that survived
- Ketchum at its 4.5% EFORd or fleet-average availability: removes about 6,740 to 6,890 MWh, net USD 112 to 115 million, files Ketchum. Ruled out by RA-3 s7 and the record (every IT peaker out in every shortfall hour). This is the declared easy route, not a surviving fork.
- Temperature-conditional estimator for Ketchum: about 770 MWh, net about -8. The award holds, but Ketchum's two graded figures (0 vs about 800 MWh; -23 vs -8) would differ. Residual fork on graded asks, not on the call.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 14 | yes |
| Formats | 3+ | 4 (pdf, xlsx, csv, parquet) | yes |
| Large file | 25,000+ rows | MDM export 351,120; weather 87,672; profiles 87,672 | yes |
| Distractors | 2+ named in metadata, none in a file name | northgate_hub_forward_curve_2027.xlsx, member_load_forecasts_2027.xlsx; names unlabelled | yes |
| Distractors unused yet weighable | yes | forward curve (energy settled at market), draft forecasts, vendor EFORd; judge found them relevant and unused | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, docx), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | prompt states all roundings and units | yes |
| Prompt shape, 25+ criteria | yes | 862 characters; 1 + 12 offer figures + award + 16 member figures plus call components exceeds 25 | yes |
| Not LLM-reading, goldens realistic | yes | judge: synthetic, templated service-order notes, nothing exclusion-level | yes (golden-realism owns the rest) |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Gate H: domain pass, layers pass, decisive_step analytical.
Design note and card: stump is correlated common-mode availability (analytical), no decoy, declared distractors are the forward curve and member forecasts. Match. The thread did not name a declared distractor as the surface read carrying the task; the surface read is the vendor EFORd, which the note calls a true annual figure, not a metadata distractor. No Gate G mismatch.

## Stump power (Gate F)
Moderate to good. The wrong route (EFORd or class average in every hour) files Ketchum at USD 112 to 115 million, a different award, not a rounding slip. Caveat for the main thread: the design note itself records that no filed sentence names fuel, cold or the class's hours, and that the availability-model family spans 0 to 7,100 MWh and files two awards. The judge accepts the record-based reading as literal under RA-3 s7. A strong analyst who reads s7's "in that hour, from the evidence" and looks at the outage co-timing lands the call; the decisive step is a judgment the data settles, so weigh it against the ladder, and against the ban on a decisive rule left unstated, rather than treating it as safely closed.

## Findings, ranked
1. (Optional, wording) Ketchum's 0 MWh and USD -23 million rest on "in that hour" read literally; a temperature-conditional estimator gives about 770 MWh and about -8. One clause saying the offer is counted at the availability of the Northgate IT peakers in that same hour would close it, but it would file the HOW; weigh against the 10/10 rule on filing method. Alternative: accept the fork as a lower-weight ask risk.
2. (Optional) Sandhill Draw payment 28.35 is an exact half-up tie; consider moving the payment off the boundary or stating the rounding convention.
3. (For main thread) The unstated-rule exposure in Stump power above.

## Next action for the author
No determinism repair needed. Decide on findings 1 and 2 (generator-side, no rerun of the judge required), then proceed to ship with the leak reader's verdict.
