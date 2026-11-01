# determinism-check report, task125 (architecture 4, pass 1), 2026-11-01

Judged pack: target.zip sha256 5e01ea0a053ced155d39dc70c859f771372e58bdcb7912f0c8f2728e12e4c1d7. One isolated thread (verdict at /tmp/determinism-check-task125-a4/verdict.md). The arch 2 and arch 3 reports are untouched.

## Verdict
NOT_DETERMINISTIC (the thread's label), confined to the supplementary ask on patrol_figures_2026.csv (officer-hours). The main recommendation, every hot_spot_patrols_2027.pptx answer and the eight priority 1 medians are forced and reproduced.
**Thread disposition:** SEND_BACK. **Reconciled disposition:** FIX_NOW (ask-layer repair in the generator, then one re-judge). Reason: see "Reconciliation of the disposition".
**Stumping type:** mechanism: forecasting (with method selection), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no.
**Gate G:** PASS. **Gate H:** domain: pass, layers: pass, decisive_step: analytical.

## Why
The 20 designated segments, the five come in, the five drop out, the cut between 185090 and 186587, the 410 of 822, 801 of 1345, 200 and 61 event nights and the 16 Mariners games all reproduce from the bundle under the literal reading. The failure is Gates A and C on the officer-hours ask only. Three CAD unit rows on 2026-03-08 (spring-forward day) have cleared_utc before dispatched_utc and a fourth row has dispatch before receipt; no shipped file says how to treat them. Read literally, Ward 6 Q1 is 1024.9 (1025, golden 1024); dropping or clipping gives 1026 for Ward 6 Q1 and 1278 for Ward 8 Q1 (golden 1277). Ward 2 Q1 reproduces as 455 against golden 453 under every convention the thread tried. 30 of 32 ward-quarters match.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Founded patrol crimes 2022-26 after conformance; candidate segments | 52 candidates | 29,568 crimes; 52 segments | yes |
| Gardens event nights / Lakeshore event nights | 200 / 61 | 200 / 61 | yes |
| Lakeshore five | 410 of 822 | 410 of 822 | yes |
| Gardens five | 801 of 1345 | 801 of 1345 | yes |
| Mariners 2027 Lakeshore games; last Gardens game | 16; 20 Dec 2026 | 16 (8 Jan to 20 Mar); 20 Dec 2026 | yes |
| Top 20 designated, rank 19 / 20 / 21 | list in submission; cut 185090 / 186587 | identical list; 57.25 / 57.13 / 34.08 | yes |
| Come in / drop out | 5 / 5 | same sets | yes |
| Priority 1 medians wards 1-8 | 5.7 6.3 5.7 7.0 6.9 7.4 7.1 7.9 | all eight match (Ward 2 6.325, Ward 8 7.925 unrounded) | yes |
| Officer-hours, 30 of 32 ward-quarters | golden | match | yes |
| Ward 2 Q1 hours | 453 | 455.2 (455); no convention gives 453 | NO |
| Ward 6 Q1 hours | 1024 | 1024.9 (1025) negatives kept; 1026.07 dropped or clipped | NO |
| Ward 8 Q1 hours | 1277 | 1278 if the 8 March rows are dropped or clipped; matches only if negative rows kept | convention-dependent |

## Competing answers that survived
1. Spring-forward rows (3 negative-interval unit rows E26-006286 F2, E26-006287 F2, E26-006288 D2 in wards 6, 6, 8, plus dispatch-before-receipt E26-006289): keep negative, drop, or clip give Ward 6 Q1 1025 / 1026 / 1026 and Ward 8 Q1 1277 / 1278 / 1278. No shipped rule closes it.
2. Ward 2 Q1: golden 453 against 455 literal, an unexplained generator-versus-pack disagreement (a solution_incorrect cell).
3. Rural-address district residual: 3,444 CAD rows (about 9 percent) carry segment ids 4xxxxx absent from the street file, on CONCESSION, SIDEROAD, COUNTY RD and ELMVALE LINE addresses, district values 1-8. Reading "ward" as the district column adds 50 to 120 hours per ward-quarter (Ward 2 Q1 558, Ward 8 Q1 1360). The literal text (ward from the street file) supports the golden, but no shipped file names Elmvale. Residual risk, not a fail by the thread.
4. Medians near rounding edges (Ward 2 6.325, Ward 8 7.925): stable under the stated method, rounding path is the only exposure.
5. Per-segment linear-trend variant swaps 116925 for 162095 (46.9 against 50.4 for last place). Counts are flat citywide and 162095's non-event counts are noisy, so a poor method and not a licensed reading. Residual note.
6. The 2027 calendar's "35 home games / 2026 calendar" assumption in solution step 4 is not in any file, but the designation is robust (same set for Lakeshore nights 20 to 60, Gardens 0 to 10, and the literal 2027 register of 2 Gardens and 32 Lakeshore nights). Keeping the Gardens nights at 41 flips it, the intended wrong route.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 11 | yes |
| Formats | 3 or more | 4 (csv, xlsx, pdf, eml) | yes |
| Large file | 25,000 rows or more | RMS 82,436 rows (CAD 37,874) | yes |
| Distractors in metadata.json | 2 or more, none labelled in a file name | ward_profiles_2021_census.csv, streetlight_service_requests_2026.csv; names are neutral | yes |
| Distractors unused yet weighable | unused by solution, a shipped fact rules out | unused in all steps (thread); neither answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden, no format family required | 2 (pptx, csv), both in the golden | yes |
| Asks multi-dimensional, unit and rounding stated | each ask | 8 wards x 4 quarters hours; 8 medians; designation set, come-in, drop-out, chart; units and rounding in the prompt sentence | yes |
| Prompt shape and 25+ criteria | identifiable shape (01); 25+ | shape 01 on the card; the graded cells (20 + 5 + 5 + 32 + 8 + chart + call) comfortably exceed 25; the generated rubric was not seen | yes (inferred) |
| Prompt form | one paragraph, under 1,000 characters, no count the data hold | 560 characters; "the cut" and "each candidate" without counts | yes |
| Reads as real work product | no LLM tell | one rough sentence in the Final Recommendation ("Not the ranking of 2026's or the five years' counts, which keeps...") is a grammar slip for the author to polish under golden-realism | note |

## Gate G reconciliation
Thread: mechanism forecasting (with method selection), stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no, Gate G pass. Design note and card: gate_g `method_or_model_selection`, stump_strategy `composition_mix`, layer2_family `estimation_fit`, stump_class `analytical`, `official_decoy: false`, `decisive_rule_filed: false`. These agree: a forecast split into steady rate and venue-night excess carried on the 2027 calendar, with no planted defect, and the ward profiles and streetlight requests (the declared distractors) are not the surface read carrying the task. The thread reproduced the note's intended wrong route (2026 or five-year counts, keeping the Gardens five, leaving out the Lakeshore five). No mismatch.

## Gate H reconciliation
Thread: domain pass, layers pass, decisive_step analytical (hot spot designation by expected crime, event-conditioned forecast; Layer 1 is RMS versions, legacy codes, dd/mm dates, UTC and DST; Layer 2 the forecast). Card analyst_test and domain_test, and the note's Three rules (No decoy, Not semantics, Not rule application), say the same, and the swap test is answered (a hospital ward has no generator on a published calendar). No mismatch. The thread did not class the step analytical merely because the golden is a standard method: it observed that only an analyst who estimates event-night excess per segment and re-exposes it to the 2027 calendar gets the right 20.

## Stump power (Gate F)
Good, per the thread. The reported 2026 and five-year counts are correct and give a wrong 2027 set (same wrong five in, five out). The signal, the venue exposure shift, is visible in the 2027 duty sheet at a glance, so a strong model may find it, and the 2027 sheet showing the Mariners' move is a surface cue the main thread should weigh against the design note's ladder (a landable call for a solver who reads the register's 2027 sheet). The asks are the second lever and are the weak part in this pass: the officer-hours cells that do not reproduce would be graded against goldens a literal solver cannot match.

## Findings, ranked
1. **Spring-forward CAD defect, 8 March 2026** (3 unit rows with clear before dispatch, wards 6, 6, 8; 1 row dispatch before receipt): no filed convention. Moves Ward 6 Q1 and Ward 8 Q1 by about 1 hour. Repair in the generator (fix the rows or clean DST handling) or file the treatment in PO-14.
2. **Ward 2 Q1 golden 453 against literal 455** with no convention found for 453: a golden or generator error to find and correct; the highest-priority recomputation item.
3. **Ward 6 Q1 (1024 against 1025 / 1026) and Ward 8 Q1 (1277 against 1278)** follow from finding 1 and close with it, but the golden must be regenerated from the repaired pack.
4. **Rural-address district residual** (3,444 rows, 4xxxxx segment ids): the literal text supports the golden; consider one filed sentence on ward assignment from the street file so no reading can use the district column.
5. **Medians at rounding edges** (6.325, 7.925): no change needed unless the main thread wants a margin.
6. **Linear-trend variant** (116925 against 162095): residual, a poor method, no action.
7. **Unfiled 2027 game-count assumption in solution step 4:** the designation is robust, wording only; the step can state the 2027 register's own nights or be dropped.
8. **Final Recommendation sentence slip:** polish under golden-realism.

## Reconciliation of the disposition
Per determinism-check section 6, a disposition is read against the gate table. The table sends back on Gate G and Gate H, the two that say the build is the wrong build. Both pass here, Gate F is good, and the main call and the pptx answers are forced and reproduced. The failed gates are A and C, confined to the officer-hours ask on patrol_figures_2026.csv, which is an ask-layer repair that spends no architecture and does not require re-rooting (the asks are legally free of the call's rules). The thread's SEND_BACK label is therefore read as **FIX_NOW**. Condition: the repair changes data solvers see (the CAD rows) and moves graded figures (the hours golden), so the pack's approval is void and one re-judge is required after the fix; the main call, the pptx answers and the medians need no change.

## Next action for the author
In the generator, find why the golden gives Ward 2 Q1 453 against the literal 455, repair or exclude the four 8 March CAD rows in the pack (or file the treatment in PO-14), regenerate the hours golden and submission.md from the repaired pack, rebuild twice byte-identically, then re-judge once.
