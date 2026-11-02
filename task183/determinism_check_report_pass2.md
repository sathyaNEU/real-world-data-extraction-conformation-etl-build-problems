# determinism-check report, task183 (run a4, architecture 4, target.zip md5 a490e8dc18519a06212e46470e7ddb04), 2026-11-02

## Verdict
DETERMINISTIC, plus SOLUTION_WRONG on one wording point (SOLUTION_STEPS Step 4).
**Disposition:** FIX_NOW
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Executed literally, the pack forces Crystal Auto Spa (BC-10896) and Polished Nail Studio (BC-10731) as the only customers over EUR 40,000 beyond their own trading. BCR-3 4.1 says "its own trading", and the till customers calibrate the lodgement-to-trade-window logic. All 12 monthly An Post rows and all 12 monthly till rows reproduce to the cent. Two fixes are needed, neither touching the analytic surface:
1. Step 4 defines the figure as "cash lodged less fitted slope x the year's card trade", which gives 99,846 / 49,898 (up to 1,711 for the rest). The quoted 99,899 / 49,952 / 1,346 are intercept x number of lodgements. Both round to the same referrals.
2. The fee half-cent convention is unfiled. Many lodgements are round euro amounts whose handling fee is an exact half cent (1,700 gives 1.105). Half-up per lodgement reproduces all 12 golden fees; float or half-even rounding moves every month by 0.01 to 0.06.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Crystal intercept x 103 (CC1, Step 4) | 970 / 99,899 | 969.89 / 99,898.70 | Yes (intercept x n; not as Step 4 words it) |
| Polished intercept x 103 (CC2, Step 4) | 485 / 49,952 | 484.97 / 49,951.64 | Yes (same wording defect) |
| Highest other customer (CC3) | 1,346 | The Pizza Yard 1,345.72 | Yes |
| Till customers, cash less till cash sales | all negative | all 12 negative (-8,542 to -909) | Yes |
| Ask 1 cash, 12 months | Oct 1,507,545.73 ... Sep 1,516,109.13 | identical | Yes |
| Ask 1 fee, 12 months | Oct 1,876.85 ... Sep 1,890.65 | identical under half-up per lodgement; differs under float or half-even | Yes, conditional on an unfiled rounding rule |
| Ask 2 cash sales and paid-outs, 12 months | per submission | identical, all 24 values | Yes |
| Referral bins | 100,000 / 50,000 | mid-band (97.5k to 102.5k, 47.5k to 52.5k) | Yes |

## Competing answers that survived
- Fee rounding at exact half cents (ask 1, minor): half-up versus float or half-even gives different cents in every month. Closing rule: none shipped. Fix: add "a half cent rounds up" to Schedule 2 clause 1.2 or to the ask.
- Peer cash-to-card benchmark refers Abbey Tea Rooms (BC-10444) and Old Town Barber Shop (BC-10643) and misses Crystal and Polished. The thread judged it not defensible: BCR-3 and the prompt say "own trading", the two customers' lodgements track their own window card trade (R2 0.997 and 0.993, near-zero intercept), and till-verified customers show cash above card is possible.
- Soft exposure (Gate C/E, not a send-back): BCR-3 4.2 defines own trading only for till customers, so the intercept-structure reading for card customers is inferred rather than filed. The design note files the estimand and leaves the method open on purpose.
- Chart value for the 49 non-referred customers is method-dependent (up to about 1.7k apart). Only referral status and the 5k referral cash are determinate; the chart is not a uniquely graded figure.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 12 | Yes |
| Formats | 3 or more | CSV, XLSX, PDF | Yes |
| Large file | 25,000 or more rows | 66,735 rows (business_account_transactions) | Yes |
| Distractors | 2 or more, named in metadata.json, no file name labels one | 3 named (retail_sales_index, branch_cash_orders, an_post_office_list); names are neutral | Yes |
| Distractors unused yet weighable; none answers a graded quantity | required | Each is unused by the solution and relevant to the sector, the cash cycle or the channel. None reproduces a graded figure (judge). | Yes |
| Deliverables | 1 to 3, all in the golden | 2 (docx, xlsx), both in golden/ | Yes |
| Asks multi-dimensional with unit and rounding | required | 12-month by 2 or more measures tables, plus a chart. Rounding is in the prompt's last sentence (cent; nearest 5,000 euro). | Yes |
| Prompt shape and 25 or more criteria | required | shape 01 (metadata). Criteria count is not checked here: the rubric is generated and is not in the folder. 5 referral/chart elements plus 48 monthly cells suggest well over 25. | Yes (inferred) |
| Reads as real work product, not LLM generated | required | Thread found no authoring disclosure; golden not inspected by me beyond the files being present. | Yes (judge) |
| License-clean sources recorded | required | CC0 constructed, source and date recorded for all 12 | Yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note (stump sentence and Three rules): the decisive step is an `estimation_fit` decomposition against own card trade lodgement by lodgement, and the easy route is the peer ratio, which refers the cafe and the barber. Match. The thread names the same easy route, so there is no mismatch. The cafe and barber are the note's own surface-read lure (ordinary customers, not a planted memo or rule); they are not the metadata distractors, which are the three unused files. The thread does not name a declared distractor as the surface read carrying the task. The note's own "no decoy" line and the thread's "natural decoys, not planted" agree.

Gate G line: mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no.
Gate H line: domain: pass, layers: pass, decisive_step: analytical.

## Stump power (Gate F)
Moderate to good, per the thread. The aggregate cash/card ratio names the wrong pair, and only a lodgement-level fit with an intercept finds Crystal and Polished. The thread says a strong model that profiles lodgement amounts could catch the constant sum, so it expects partial failure. The thread did not class the decisive step analytical merely because the method is standard: it found the golden by fitting, with the data separating the candidates. My note for the main thread to weigh against the design note's ladder: lodgement-window regression with intercept is a textbook route that a strong solver can land, so the asks (old-platform field semantics, half-up fees, Z-report day reconstruction) carry much of the difficulty.

## Findings, ranked
1. Step 4 wording: "cash lodged less fitted slope x year's card trade" does not reproduce the quoted figures; it should read intercept x number of lodgements, with Steps 4 and 8 in agreement. (SOLUTION_WRONG, wording only.)
2. Fee half-cent convention unfiled in Schedule 2 clause 1.2 or the ask (minor Gate C fork on ask 1 fee cents).
3. Own trading for card customers is not filed in BCR-3 (soft Gate C/E; the note keeps the method open by design, forced by the till calibration).
4. Chart figure for non-referred customers is not pinned.

## Next action for the author
Fix Step 4 in submission.md to "intercept x number of lodgements", and file "a half cent rounds up" in Schedule 2 clause 1.2 (generator, then rebuild twice byte-identical); the pack change means the one allowed re-judge applies.
