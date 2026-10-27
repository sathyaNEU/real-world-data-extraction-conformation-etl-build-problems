# determinism-check report, task144, 2026-10-27 (re-judge after FIX_NOW, scratch run r2)

## Verdict
DETERMINISTIC (no SOLUTION_WRONG)
**Disposition:** APPROVE for the main call and the forecast asks. The click-through ask (Ask A) was judged on the previous pack (f0ae1a2f) and has not been re-judged on the shipped pack (eb36b41e), see Findings 1.
**Stumping type:** mechanism: forecasting + method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The call is forced by the shipped files. The back-test on 19 closed lottery spotlights separates the rate definitions: day-8 rate RMSE 324 stars, whole-life rate 1,129. kilnkit totals about 12.1k against about 10.0k for slidewell and tracewire. The lead held under every variant the thread ran: baseline mean, median or pooled ratio (3.16k to 3.18k), rate cutoffs from day 6 to day 10, numerator and denominator choices. The two wrong answers are refuted by the pack's own back-test. Slidewell at about 14k comes from the whole-life rate. Tracewire comes from adding the lottery's mean lift to each trajectory (10.7k against kilnkit 7.3k).

## Recomputation ledger
The main-call, chart and nomination rows were run on the previous pack. Those files are byte-identical in the shipped pack. Rows marked "stale" sit on files that differ in the shipped pack.
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| External stars by 27 Sep (kilnkit / slidewell / tracewire) | 1,523 / 4,175 / 4,534 | same; the other four also match the chart's 2/2/2/1k | yes |
| Newsletter stars per subscriber | 0.71% of 433,812, about 3,000 | 0.711%, 3,085 | yes |
| Mean followers of starrers | 85 / 10 | 84.9 / 10.08 | yes |
| Feed rate from day 8 | kilnkit 1.8% (356/19,548), slidewell 0.7% (whole life 2.0%) | 1.82%, 0.74%, 1.98% | yes |
| No-spotlight kilnkit by day 90 | 3,000 | 3,158 to 3,178 | yes |
| Totals if spotlighted | 12/10/10/8/8/7/6 thousand | 12.1/9.97/9.97/8.2/8.1/6.95/5.88; none within 0.25k of a rounding boundary | yes |
| Back-test RMSE | day-8 rate reproduces within a few hundred; whole-life misses by more than 1,000 | 324 against 1,129 | yes |
| Nominators outside the organisation | kilnkit 22/27, tracewire 43/47, shiftgres 28/31, ferrolog 30/37, hullcheck 23/26 | identical (needs URL normalisation, two renames, email-hash matching, the full merged_into chain) | yes |
| Click-through, April / May (Postwerk) | 5,825/391,299 and 6,075/399,160 | same on the earlier pack | stale |
| Click-through, June to September (Relaymark) | 6,233, 6,536, 6,190, 6,404 subscribers | same on the earlier pack | stale |

## Competing answers that survived
No fork changes the main call or any committed figure. Residual notes:
1. The click-through denominator, "delivered to", is not defined in the files. The golden sums the two Tuesday batches. A union with the Thursday resend is not derivable. This is a minor ask-level risk.
2. The gateway-fetch rule is unstated. In the earlier pack it was forced by bimodal data: 9-link bursts within about 2 seconds, and "each link once" rows. The counts were identical for windows of 1 to 3 seconds and thresholds of 3 to 5.

## Spec gates
Checked by me against the shipped bundle and metadata.json. I did not count rubric criteria; there is no rubric file in the task folder.
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 17 | yes |
| Formats | 3 or more | 5 (csv, json, parquet, pdf, xlsx) | yes |
| Large file | one of 25,000 or more rows | relaymark_link_clicks has 431,644 rows | yes |
| Distractors | 2 or more named in metadata.json, none labelled in a file name | repository_traffic, trending_daily; unused by the solution, relevant to weigh, neither ranks the candidates | yes |
| Deliverables | 1 to 3, all in the golden | 2 (xlsx, png), both present | yes |
| Asks | multi-dimensional, unit and rounding stated | 6 issues by 2 measures, 5 repositories by 2 measures; the prompt states the unit and rounding | yes |
| Prompt shape and 25 criteria | identifiable, rubric of 25 or more | shape is "other", and the criteria count was not verifiable here | not verified |
| Reads as a real work product | | judge saw nothing that reads as LLM generated | yes |

## Gate G reconciliation
The thread's mechanism is forecasting with method selection, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. The design note declares forecasting, strategy forecast_method_backtest, and the decisive step as the rate window against the cascade regime. These match. The thread did not name either declared distractor (trending, traffic) as the surface read. It used trending only as corroboration of the slidewell launch burst. No shipped artifact ranks the candidates.

Gate H line: domain pass, layers pass, decisive_step analytical. The deciding quantity is a validated cascade forecast, so the domain is not a backdrop. Layer 1 is the schema v5/v6 codes, UTC against local time, renames, URL variants, merged accounts and ESP export formats. The easy routes are the whole-life rate (slidewell) and the mean lift (tracewire).

## Stump power (Gate F)
Good. Both easy routes land on a wrong repository that the pack's back-test refutes. The weak spot is that a multiplicative regression of added stars per newsletter star on the day-8 rate reaches kilnkit (11.5k) without the full cascade model. That regression validates best (RMSE 288), so the cascade is not the only road to the right call. The same regression on the whole-life rate gives slidewell 12.1k (RMSE 706). The main thread should weigh this against the scored readers' result.

## Findings, ranked
1. **Ask A pack is newer than the judged pack.** The coordinator states that since f0ae1a2f the only change is ask-side data: more subscribers behind link-checking gateways, with each gateway fetch kept at least two minutes before its reader's own first click. My diff of the shipped target.zip (eb36b41e) against the judged unzip confirms four files differ: postwerk_campaigns, postwerk_link_report, relaymark_campaigns and relaymark_link_clicks. All other files are identical. The claimed click-through figures are unchanged. They have not been recomputed on the new files, and I did not spawn a second thread. Two things need checking:
   - The counts still reproduce.
   - The gateway rule still separates cleanly. With the fetch two or more minutes before the reader's click, a rule keyed to 'four or more links within two seconds' may now miss or mis-split some, and the step 7 wording in submission.md may no longer describe the data.
   Both are unverified.
2. Optional hardening with no effect on the call: say in the click-through ask that "delivered to" means the people the Tuesday batches reached.
3. The golden's rounding to the nearest thousand leaves no figure near a boundary. No action.

## Next action for the author
Re-run the generator's own check of the six click-through counts (and the step 7 gateway rule) against eb36b41e. If they hold, ship. If the gateway rule no longer separates, fix only the ask-side data or its filed definition, then re-invoke me for one narrow ask-A re-judge.
