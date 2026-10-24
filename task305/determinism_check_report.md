# determinism-check report, task305, 2026-10-24 (pack 1680766e, re-judge pass; replaces the first pass)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated sonnet thread (medium) on a fresh unzip of target.zip at /tmp/determinism-check-task305-44869/target/ recomputed every graded figure from the bundle and reproduced all of them. The call (S3 Wrentoft, GBP 0.8m) holds for every guest-spend construction the data supports (0.77 to 0.81 across variants; S3 beats S1 for any per-pitch rate above about 1,300). The per-pitch rate is separated from its rivals by a store-by-store back-test (store 107 predicted 598k against 600k observed; store 105 345k against 343k). The thread's full verdict is /tmp/determinism-check-task305-44869/verdict.md.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Grocery stores in share (rating list, 280 m2 or more) | 24 | 24 | yes |
| Residents alone, S1 / S3 additions (GBP m) | 0.5 / 0.1 | 0.493 / 0.142 (S3 fourth of six) | yes |
| Guest spend per pitch | GBP 2,440 | 2,439.5 (6 pitch-measured entries, 2,525 pitches) | yes |
| With guests, S3 sells / adds (GBP m) | 7.1 / 0.8 | 7.118 / 0.800 | yes |
| With guests, S1 / S2 / S6 (GBP m) | 0.5 / 0.3 / 0.2 | 0.504 / 0.304 / 0.232 | yes |
| Largest park pitches | 1,750 | 1,750 (Wrentoft Lakes Holiday Park, LQ15 4DZ) | yes |
| Cases a week, stores 101 to 110 | 7456 7085 6968 7290 5954 6734 5710 4658 3890 4429 | 7456.2 7084.9 6968.3 7289.8 5954.2 6733.9 5710.1 4657.8 3890.0 4429.2 | yes (24 turned-away DEL stops dropped, /25; no value within 0.2 of a rounding edge) |
| Paid hours a week, stores 101 to 110 | 1839 1612 1444 1459 1182 1313 1243 1010 852 816 | 1838.7 1612.0 1443.8 1458.8 1182.4 1313.2 1243.4 1009.6 851.9 815.7 | yes (clock-in terminal store, /25) |
| Bus departures S1 to S6 | 40 102 40 60 68 80 | 40 102 40 60 68 80 | yes (pickup_type not 1, clock-day logic, joint routes 4 and 41 once) |

## Competing answers that survived
No fork changes the call or a graded amount under a rigorous reading. Residual forks, all on the asks:
1. **Bus ask, "departures":** GTFS final-stop rows (pickup_type 1) still carry a departure_time. Counting them gives S1 46 and S3 46 instead of 40 and 40; S2, S4, S5, S6 are unchanged. The prompt does not say "that pick up passengers". The design note closes this in its fork table (SF20, pickup_type asserted at every final stop), but the closure is not in the shipped text. This is the one finding that touches the graded text.
2. **Cases ask:** every TMS stop is status COMPLETE, so the turned-away rule is recoverable only from dwell time and the next-day repeat (and goods-in for stores 101 to 106). The separation is clean (dwell under 4 + 0.02 x cases for 24 stops, next-best stop at 6 or more) and the reading is unique. Nothing is filed, which is acceptable on an ask.
3. **Hours ask:** the WFM `location` column (the colleague's home store) against the clock-in terminal. The WFM column gives 101 = 2,097, not 1,839. "Worked at" and the punch terminals license the terminal reading, and 2,616 shifts are clocked in at another store. Recoverable from the files.
4. **Amount-level variants of the main call (non-rigorous):** no winter-baseline subtraction gives 0.9 (S3 still wins). Applying the 88 per cent to guest card spend gives 0.7 (S3 still wins). The data argues against both: flat winter spend at stores 102, 109 and 110 shows the off-season level is background, and card spend is already in store.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 20 | yes |
| Formats | 3 or more | 6 (csv, txt, xlsx, pdf, md, zip) | yes |
| Large file | 25,000 rows or more | ta_punches 109,184 rows; wfm_paid_hours 54,593 | yes |
| Distractors | 2 or more named in metadata.json, none labelled in a file name | dft_aadf_count_points_lq_2025.csv, customer_survey_store_scores_2025.csv (goods_in_receipts is a third, partial-rollout undercount, not named) | yes |
| Distractor weighing | unused by the solution, relevant, ruled out by a shipped fact | the car-park counts and survey scores do not answer a graded quantity | yes |
| Deliverables | 1 to 3, each in the golden | 2 (xlsx, docx); both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 10 + 10 + 6 figures; each states unit and rounding | yes |
| Prompt shape | identifiable | "other", per metadata.json | yes |
| Rubric | 25 or more criteria | 2 call criteria, 3 components, 26 ask figures, about 31; the rubric itself is generated downstream and was not inspected | yes (by count) |
| Not LLM generated | clean | grep clean on authoring strings; xlsx and PDF metadata in fiction; all evidence dated before 9 Oct 2026 | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card and design note: stump_class analytical, strategy population_selection, gate_g `forecasting`, generator G12 (census silence read as nobody there), layer2 field_method.

- **Substance matches.** Both name the same decisive step: the park guests are an origin the census never counts, priced per pitch from the out-of-region card spend at the chain's park-side stores. Both name the same easy route (residents only, S1 at 0.5m). The thread classes the ranking artifacts as clean: the filed model and every shipped figure are accurate and none ranks the sites.
- **Label mismatch (finding).** The card says `forecasting`; the thread says `method_or_model_selection`. The design note records that it moved the label away from `method_or_model_selection` because that label repeated task482 (five of the last twelve builds). The mismatch is in the label, not the mechanism, but it is the kind of difference a reviewer could read as a re-labelling to dodge the repeat guard. The author should confirm which label is honest.
- **Distractor check.** The declared distractors (traffic counts, survey scores) are not the surface read carrying the task. The easy route is the filed model on census households. Pass.
- **Borderline the thread raised.** The filed rule says "households as Census 2021 counted them". The solution adds non-household origins, which extends the rule and does not override it, because the PDF sets the shares and not the list of origins. A reviewer who reads census-only origins as a stated rule being overridden would send it to live testing.

## Gate H
domain: pass, layers: pass, decisive_step: analytical. The domain is the retail geographer's Huff-style spend-share model with a contribution appraisal; the swap test fails to make it generic. Layer 1 is UTC against UK dates, incomplete rollout, home store against clock-in store, postcode spacing, the GTFS service day past midnight with joint routes in two feeds, and the VOA layout. Layer 2 is demand origins outside the census plus a leakage-corrected pitch rate. No decoy, not semantics (reading every field correctly still gives the residents answer), not rule application (no stated rule yields the guests). This matches the design note's `## Three rules`.

## Stump power (Gate F)
Real. The filed model reproduces the ten stores' sales within 0.4 per cent (75.9m against 76.2m), so the residents-only route looks validated and lands on S1 at 0.5. The pooled-over-all-pitches route also lands on S1 (0.495 for S1, 0.268 for S3); the nearest-park-pitches route lands on S3 at 0.5. Each easy route files a wrong site or a wrong amount. The decisive step is not stated anywhere, and the notes file names the card feed and pitch measures but not their link. The thread did not class the step analytical merely because it is a textbook method; it reached the golden only by noticing the seasonal out-of-region spend in the feed, so this is not the landable-method case.

## Findings, ranked
1. **Bus ask lacks "that pick up passengers"** (optional fix). S1 and S3 read 46 instead of 40 under the alternative reading. Two of six bus figures are affected; the call is not.
2. **Gate G label mismatch** between the card and design note (`forecasting`) and the thread (`method_or_model_selection`). The design note says it moved off `method_or_model_selection` to avoid repeating task482.
3. **Non-household origins versus "households as Census 2021 counted them"** is a possible live-testing flag, not a determinism defect.
4. **Cases and hours reading rules are unfiled** (turned-away loads, clock-in terminal). Both are recoverable from the files and acceptable on an ask. Optional: record the back-test (per-store predicted against observed guest spend) as the evidence in the submission.

## Next action for the author
Add "that pick up passengers" after "bus departures" in prompt.txt. This is optional: it changes no graded figure and the prompt has to stay under 1,000 characters (it is now 667). Then confirm which Gate G label (`forecasting` or `method_or_model_selection`) the card should carry. The verdict is APPROVE and no re-judge is owed.
