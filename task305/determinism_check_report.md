# determinism-check report, task305, 2026-10-24

This is pass 4 on target.zip sha256 414157955646a50b54e00231c1aa740c48a298a87ccff95f35368559cd60d1f3. Passes 2 and 3 approved packs 1680766e and ec38f0bd; this report replaces the round-2 report at the author's instruction (no separate pass file). The main call is unchanged since pass 3; asks B (paid hours) and C (bus departures) have new data and write-up steps.

## Verdict
DETERMINISTIC (no SOLUTION_WRONG)
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated sonnet thread (medium) on a fresh unzip at /tmp/determinism-check-task305-r4/target/ recomputed every graded figure in submission.md blocks 1 to 4 from the raw bundle and reproduced all of them. The residents-only model files S1 at GBP 0.5M (0.496); carrying the six pitch-measured holiday parks as origins at about GBP 2,443 a pitch gives S3 7.13M sales and a 0.80M addition. S3 beats S1 for any per-pitch spend above about GBP 1,350, and every guest definition tried lands between 2,300 and 2,900. Asks 3, 4 and 5 (all 10 stores, all 6 sites) reproduce exactly. Thread verdict: /tmp/determinism-check-task305-r4/verdict.md.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Grocery stores of 280 m2 or more | 24 | 24 (37 grocery entries, 13 under 280 m2) | yes |
| Residents alone, S1 / S3 add (GBP m) | 0.5 / 0.1, S3 second of six | 0.496 / 0.145, second (S2 0.089) | yes |
| GBP per pitch | 2,440 | 2,443.03 | yes (rounded to the nearest 10; S3 add 0.803 at 2,440, 0.804 at 2,443) |
| Wrentoft Lakes pitches | 1,750 | 1,750 (LQ15 4DZ) | yes |
| S3 sales with guests | 7.1M | 7.131 to 7.134M | yes |
| S3 add with guests | 0.8M | 0.803 to 0.804M (running costs 976,000) | yes |
| S1 add with guests | 0.5M | 0.508M | yes |
| S2 add; own-store take | 0.1M; over a third | 0.091M; 36.6% | yes |
| Cases a week, 101 to 110 | 7,456 / 7,085 / 6,968 / 7,290 / 5,954 / 6,734 / 5,710 / 4,658 / 3,890 / 4,429 | 7,456.2 / 7,084.9 / 6,968.3 / 7,289.8 / 5,954.2 / 6,733.9 / 5,710.1 / 4,657.8 / 3,890.0 / 4,429.2 | yes, all 10 (24 turned-away DEL stops excluded, /25) |
| Paid hours a week, 101 to 110 | 1,903 / 1,533 / 1,476 / 1,368 / 1,207 / 1,318 / 1,241 / 1,073 / 812 / 783 | 1,902.9 / 1,532.6 / 1,475.7 / 1,367.9 / 1,206.8 / 1,317.9 / 1,240.6 / 1,072.7 / 811.7 / 783.2 | yes, all 10 (53,860 pairs, 471 orphan IN, 272 orphan OUT; terminal store; one wfm line per shift start date) |
| Bus departures S1 to S6 | 44 / 110 / 44 / 64 / 72 / 84 | 44 / 110 / 44 / 64 / 72 / 84 | yes, all 6 (nearest stops within 250 m, next beyond 480 m, so the 400 m line is not a fork) |

## Competing answers that survived
No fork gives a competing answer of equal standing or changes the call. Four rest on a data-derived inference rather than a filed sentence (the submission's own write-up steps 5 to 7 now file the turned-away rule, the terminal-store rule and the block_id rule, but the shipped notes do not):
1. **Cases, turned-away loads.** Counting every COMPLETE DEL stop gives 7,482 / 7,154 / 6,995 / 7,368 / 6,003 / 6,785 / 5,773 / 4,705 / 3,932 / 4,475. The split is clean (24 stops with dwell far below 4 min + 0.02 per case, each followed next day by a one-stop trip with identical cases); the 12 short stops at stores 101 to 106 fall before go-live, so goods-in cannot confirm them.
2. **Hours, wfm `location` against the terminal store.** By location: 2,128 / 1,463 / 1,474 / 1,356 / 1,190 / 1,335 / 1,245 / 1,023 / 789 / 708. "Worked at each store" and the terminal register favour the golden; the notes do not define `location`. Ignoring shifts with an unpaired punch: 1,881 / 1,515 / 1,452 / 1,349 / 1,195 / 1,301 / 1,222 / 1,055 / 800 / 772. Dating by clock-in or clock-out makes no difference.
3. **Buses, identity of a departure.** Every trip counted: 81 / 220 / 80 / 100 / 144 / 156. Dedup by stop and time only: 40 / 102 / 28 / 60 / 68 / 80. No Thursday carry-over past 24:00: 41 / 102 / 41 / 61 / 66 / 78. The prompt's "by the clock" and GTFS block semantics support the golden.
4. **Main amount, guest definition.** S3 first under every reading; the rounded amount moves only to 0.9 (all-year out-of-region spend, or Mar-Oct with no baseline) or stays 0.8 (Apr-Oct only, no card-share divide: 0.77). The even-spread-per-pitch construction gives S3 0.27 and S1 first, which is the intended easy route, not a rival.

These four are asks-level or amount-rounding forks the author may close with a neutral sentence in the notes; none is blocking.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 20 in the zip (thread counted 21) | yes |
| Formats | 3 or more | csv, txt, xlsx, pdf, md, zip (two GTFS feeds) | yes |
| Large file | 25,000 rows or more | ta_punches 108,463 rows (wfm about 61k) | yes |
| Distractors | 2 or more named in metadata.json, none labelled by file name | dft_aadf_count_points_lq_2025.csv, customer_survey_store_scores_2025.csv; names carry no label; both unused by the solution (thread read them as usable, relevant to a site decision); goods_in_receipts is a further unused file | yes |
| Distractor rule-out | one that answers a graded quantity reproduces and a shipped fact rules it out | neither distractor answers a graded quantity; not exercised | yes (n/a) |
| Deliverables | 1 to 3, all in the golden, no format family | 2 (xlsx, docx), both in golden/ | yes |
| Asks | multi-dimensional; unit and rounding stated | prompt states pounds to 0.1 million and whole numbers for cases, hours, departures; asks of 10, 10 and 6 figures | yes |
| Prompt shape and rubric 25 or more | identifiable shape; 25 or more criteria | metadata shape "other"; about 29 separately gradable figures (2 + 10 + 10 + 6 + docx) plus critical components; the generated rubric itself was not inspected | yes (by count, rubric unverified) |
| Prompt | one paragraph, under 1,000 chars | 691 characters | yes |
| Reads as real | no LLM tells; goldens read as work products | thread: no authoring language in property_data_notes.md; I did not re-read goldens for realism (golden-realism owns that) | yes (thread) |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: gate_g method_or_model_selection, stump_class analytical, no decoy. Design note: strategy population_selection, Gate G method_or_model_selection, decisive generator G12 (holiday-park guests are an origin the census never counts). The card and note say the same as the thread; no mismatch. The declared distractors (AADF counts, customer survey) are not named by the thread as the surface read, and the surface read the thread names is the filed residents-only model, which the pack presents as the model and not as a ranking of sites. Gate G: no shipped artifact ranks the sites wrongly.

Gate H, thread: domain pass, layers pass, decisive_step analytical (retail spatial-interaction model, swap test fails; Layer 1 UTC vs local, BNG vs WGS84, VOA layout, double-listed nights, orphan punches, joint feeds; Layer 2 demand-origin completeness calibrated on card data). Design note's Three rules: decisive step is carrying the parks as origins at a card-measured spend per pitch, same as the thread; Not semantics and Not rule application lines match (filing the model as given yields S1 at 0.5M, the easy wrong answer). No mismatch.

## Stump power (Gate F)
Plausibly strong. A capable analyst who runs the filed model over the census lands on S1 at GBP 0.5M (0.496). Reaching S3 needs the unprompted recognition that guests are an origin the census cannot hold, a per-pitch spend calibrated from out-of-region card spend weighted by the share of each park's spend that reaches our stores (an even spread gives S3 0.27 and S1 first), and a rerun of the appraisal. The thread did not class the step analytical merely because the method is standard, so no discount of the kind in the contract applies; the main thread weighs this with the scored readers' result.

## Findings, ranked
1. Advisory: the cases ask's turned-away rule is recoverable only from dwell time and the next-day repeat; nothing in the notes files what a short dwell means. Clean separation, unique reading.
2. Advisory: the notes do not define the wfm `location` column; terminal store is licensed by "worked at" but not stated.
3. Advisory: bus "departure" identity (block_id dedup, Thursday carry-over past 24:00) is recoverable from GTFS semantics, not filed in the bundle.
4. Advisory: the guest-spend baseline (Mar to Oct excess over the Nov to Feb level) is inferential; rounded amount stays 0.8 under the licensed reading and S3 wins under every reading.
5. Cosmetic: GBP 2,440 is 2,443.03 unrounded; consistent as rounded to the nearest ten.

## Next action for the author
None required. Ship on this pass. Optionally, if hardening the asks, add one neutral sentence per item 1 to 3 to property_data_notes.md (what a refused load is, what `location` means, what counts as one departure) without moving any figure; the main call and its stump stay frozen.
