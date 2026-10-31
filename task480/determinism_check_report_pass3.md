# determinism-check report, task480 (architecture 3, pass 3), 2026-10-31

## Verdict
DETERMINISTIC
**Disposition:** FIX_NOW
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Post-thread state: the current submission.md and prompt.txt already differ from the text the thread saw. Dark bars are gone from ask 4, the critical-component back-cast errors are stated as an ordering, and the prompt now says "whole counts" (no "events"). The three FIX_NOW items below are therefore recorded as applied by the main thread, not re-judged by me. The ledger and findings describe what the thread judged.

The isolated thread (verdict at /tmp/determinism-check-task480-pass3/verdict.md) found the call forced by an out-of-sample back-cast the shipped census history supports. Every age-aware dwelling-stock estimate puts Cedar Run in (10,628 to 10,770) and Maple Ford (9,451 to 9,582) and Fallon (9,293) out. The two shortcuts (2020 persons per dwelling: Maple Ford 10,451 in, Cedar Run 9,735 out; type-only: Cedar Run 9,738, Maple Ford 8,735) file different tier sets and both fail the back-cast. Births (978) and deaths (1,070) reproduce exactly for all 14 municipalities. The one defect is wording: ask 4 says "in dark bars", which the prompt never asks for. Residual risk: no shipped sentence names the method, so determinism rests on the solver running the back-test (Gate C).

Note on the pack: task480/target was rebuilt after the thread's copy (realism fixes only: no state column on the vital files, distinct facility addresses, renamed group homes, varied street names). Eight files differ byte-wise from the thread's copy (births, deaths, address points, roll, certificates, demolitions, block groups, group quarters, county estimates); the coordinator states every figure in generator/figures.json is unchanged. The thread's recomputation was therefore not run on the shipped pack, and I did not re-run it (no second thread).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| 2020 dwelling stock | 45,334 (census housing units) | 45,334, block-group match within 3 | yes |
| Cedar Run, 1 July 2026 | 10,690 to 10,790 | 10,628 to 10,770 (point 10,675) | partly: the call and the bulk of the range, not the exact bounds |
| Maple Ford, 1 July 2026 | 9,590 to 9,620 | 9,451 to 9,582 (point 9,451) | partly: below the claimed range, under 10,000 either way |
| Tier set | Juniper, Dunmore, Cedar Run | same | yes |
| Births, 14 municipalities | golden (total 978) | all 14 equal | yes |
| Deaths, 14 municipalities | golden (total 1,070) | all 14 equal; 97 pre-2026 RES_MCD_CODE disagreements | yes |
| Back-test errors (1.7 and 2.0%; 4.5 and 6.5%; 7.4 and 13.5%) | CC2 | profile 2.3 to 3.7%; 2020 ratio 3.8% and 6.4% | direction only; exact figures not reproduced by the thread's approximate rebuild |

## Competing answers that survived
| Fork | Answer A | Answer B | Shipped rule closing it |
|---|---|---|---|
| Per-dwelling yield | age-aware profile: Juniper, Dunmore, Cedar Run | 2020 ratio: Juniper, Dunmore, Maple Ford; type-only: Juniper, Dunmore | none filed; closed only by the back-cast on the shipped 2000 and 2010 censuses |
| Twins | one record per infant | one event per delivery | the prompt says "events"; CHILD_SEX per record favours per infant (a wording risk) |

Forks tested that move nothing: 2026 certificates ignored, year built 0 (113 parcels), group quarters at 1 April, deaths by written city (settled by program statement s. 3 and the address points).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files, formats, large file | 10+, 3+, 25,000+ rows | 14 files; csv, xlsx, pdf; address points 50,055 rows | yes |
| Distractors | 2+ in metadata.json, none labelled by file name | dot_certified_local_road_miles_2026.xlsx, census_bureau_county_estimates_v2025.csv; neither named as a distractor | yes |
| Distractors unused, relevant, ruled out by a shipped fact | | Road miles is a different formula's input; the county file is county totals only (Tamarack 100,413) so it answers no graded quantity. Both are weak weights, not wrong-answer baits (Gate G neutral). | yes, thin |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, svg), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | | tier for 14, births for 14, deaths for 14, chart; "whole counts" stated | yes |
| Prompt shape, 25+ criteria | | shape 10; roughly 14 x 3 cells plus chart and call exceed 25 | yes |
| Reads as LLM generated / golden realism | | thread found no tell; not independently audited by me | yes (unaudited) |
| Ask 4 matches the prompt (as judged; current files since corrected) | | prompt asks for a chart of estimates against the 10,000 line; ask 4 adds "three urban tier municipalities in dark bars". The golden SVG has 3 bars in #1f6f5c, so it is not literally "dark". | NO |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no; Gate H: domain pass, layers pass, decisive_step analytical.
Card (task480.json): stump_class analytical; analyst_test (the 2020 ratio names the wrong municipalities because persons per dwelling falls with dwelling age); domain_test (housing unit method with a household yield modelled on dwelling age). Design note: stump sentence and Three rules agree. Match. The declared distractors are not named as the surface read, so they are not too load-bearing.
Discrepancies for the main thread:
1. The design note's Default path and Ladder give the golden family as Cedar Run 10,348 to 10,813 and Maple Ford 9,013 to 9,623, while submission.md claims 10,690 to 10,790 and 9,590 to 9,620. The submission ranges are narrower and the thread's Maple Ford range (9,451 to 9,582) sits partly below them. Align the claimed ranges with figures.json.
2. Ladder rung 3 (year built, no age shift) files Dunmore, Juniper, Cedar Run and Maple Ford. Only the back-cast separates it from the golden, and critical component 2's exact errors were not reproduced by the thread.
3. The design note's Literal reader and a 2026-10-31 note already log this FIX_NOW (the dark bars wording); confirm it is closed in the rebuilt pack.

## Stump power (Gate F)
High on paper. The natural route (2020 persons per dwelling by municipality, or a type-only fit) misses Cedar Run and files Maple Ford in, and the census history invites that reading. The age-aware route is a recognised estimator, but the thread found it nothing the data forces without the solver building the back-cast. This is a method-selection stump with no filed criterion; the main thread should weigh it against the ladder. The deaths ask also bites (97 wrong if RES_MCD_CODE is used).

## Findings, ranked
1. FIX_NOW: ask 4 "in dark bars" is not asked by the prompt, and the golden bars are green. Drop it, or make the prompt ask for the urban tier bars to be distinguished.
2. Claimed ranges in submission.md versus the design note and the thread (Cedar Run, Maple Ford) and critical component 2's exact errors: the thread could not reproduce them to the decimal. Check against figures.json.
3. Method is not filed; determinism depends on the back-test (Gate C residual).
4. Twins and "events" wording on births.
5. Pack rebuilt after the thread's copy; figures asserted unchanged only.
6. The county-estimates distractor is thin.

## Next action for the author
Edit ask 4 in submission.md (and the golden description) so it states only what the prompt asks, or add the distinguishing instruction to the prompt, then reconcile the submission ranges with figures.json, and re-judge once only if the prompt changes.
