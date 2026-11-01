# determinism-check report, task170, 2026-11-01

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting (learning curve on own start count, exposure), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Judged bundle: target.zip md5 60c3b11bc414ba0d953667a2e3b5540d. The zip on disk now has md5 37e73b761d873736032a23baeb38678c: the coordinator reports data-only realism edits since (per-recorder SoM references, varied allocation dates, timetable-driven trains planned in the punctuality distractor) with figures.json byte-identical. Those edits were not re-judged (one pass, one thread); the author should confirm with the free gates that every graded figure still reproduces.

## Why
The main call (about 1,250 errors; 276 drivers; 111,000 starts) reproduces from the files. The point estimate is about 1,280 inside the 1,125 to 1,375 bin and holds across bands of 5/10/25/100/200, log bands and SVC-only exposure (1,255 to 1,280). Method is open and the data separates the candidates: the Phase 1 to 3 hazard is stable by calendar month at fixed own-start-count and falls steeply with own start count, so the pooled first-year rate and the months-since-go-live curve give about 850 to 860 (750 bin), and errors-per-driver gives about 2,380. Answers 3 and 4 reproduce exactly.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| OBR starts excl. TST | 707,562 | 707,562 (712,452 rows, 24 TST IDs) | yes |
| TDE errors after withdrawn/linked | 4,418 | 4,418 (5,229 less 132 less 679) | yes |
| Phase 4 drivers | 276 | 276 (GLH 40, DRC 39, KVN 46, ADM 51, MSB 53, FBK 47) | yes |
| Starts, 12 months | 111,357.6 | 111,357.6 (92,798 activations / 10 x 12, latest issue, Worked) | yes |
| Forecast | 1,280.2 | 1,279.2 | yes (same bin) |
| Units accepted/not, six depots | 8/6, 8/5, 7/6, 6/4, 5/5, 4/6 | identical, nearest margin 7 days | yes |
| LTR and BRK by Phase 1 to 3 depot (16 cells) | per submission | all 16 identical | yes |

## Competing answers that survived
Supplementary asks only; the main call is unaffected.
1. Ask 4 depot attribution: register Depot column (golden) against 31 Oct roster depot with chained numbers; the latter moves 8 of 16 cells by 1 to 5 (e.g. CNC BRK 64 v 59). The register reading is natural; the prompt does not pin it.
2. Ask 3 unit membership: formation list (golden) against works records' Programme Unit plus renumbering chain (GLH 5, DRC 6, KVN 5, ADM 4, MSB 2, FBK 1 accepted). The workbook conventions favour the formation list (the acceptance note defines acceptance by the unit's two driving vehicles) but the competing reading is plausible. The submission step 6 states the rule; whether a shipped sentence closes it is for the author to confirm.
3. Ask 4 OBR-download folding: rule application on an ask, data-forced (1,698 pair within 15 minutes after the UTC fix), permitted.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 15 | yes |
| Formats | 3+ | 3 (CSV, XLSX, PDF) | yes |
| Large file | 25,000+ rows | 712k-row OBR log, 58k duty file | yes |
| Distractors | 2+ named in metadata, no file name labels one | punctuality_by_depot, depot_weather_daily; neither labelled | yes |
| Distractors unused, relevant, ruled out | yes | judge: neither used, carry no error outcome | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, svg), both present | yes |
| Asks multi-dimensional with unit and rounding | yes | per-depot and per-cell asks; rounding sentence in prompt | yes |
| Rubric 25+ criteria | 25+ | per-depot cells (12 + 16 + main + components) clear 25 by count; not generated here | yes (by count) |
| Not LLM-generated / goldens real | yes | judge found none exclusion-level; PDFs terse | yes |

## Gate G reconciliation
Thread: mechanism forecasting, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: gate_g forecasting, stump_class analytical, strategy time_semantics, official_decoy false. Design note stump: pooled first-year rate files 750 (821.6) against 1,250 (1,280.2); the judge reaches the same default (about 850 to 860, 750 bin) and the same golden. Match. The declared distractors (punctuality, weather) were not named by the thread as the surface read; not too load-bearing. Gate G: no shipped artifact ranks the decision wrongly; classed forecasting.
Gate H: domain: pass, layers: pass, decisive_step: analytical. Matches the note's Three rules (domain test HRA experience shaping factor; layer 1 BST/UTC, crosswalk, renumbering, re-issued duties; layer 2 estimation_fit on own start count). The judge did not class it analytical merely because the method is standard: it reached the golden only via the own-count hazard, which the pooled route misses.
Minor: the card's analyst_test still reads "about 400, against about 650", stale against the note's 750 against 1,250. Fix in the card.

## Stump power (Gate F)
Moderate to good. Easy routes (pooled rate, months-since-go-live) land on 750; per-driver scaling on 2,250 or 2,500. A strong model that fits error against a driver's cumulative starts lands on the call, so the stump is real but not guaranteed; the main thread weighs it against the ladder.

## Findings, ranked
1. Judged bundle md5 differs from the current zip (data-only edits, graded figures frozen); confirm by the free gates, not re-judged.
2. Ask 4 depot attribution is not pinned in the prompt (8 of 16 cells would move under the roster reading).
3. Ask 3 unit source (formation list v Programme Unit) conflicts for 30 vehicles; confirm a shipped sentence names the formation list.
4. Card analyst_test numbers stale.
5. Time basis (register local, recorder UTC) is inferable only; does not move the forecast, but ask 4 fails without it (inferred from data, a Layer 1 item).

## Next action for the author
Re-run figures_check.py and verify on the current zip (md5 37e73b76...) to confirm every graded figure is unchanged, then optionally add "counted at the depot the register records it against" to the ask 4 wording and refresh the card's analyst_test; no re-judge needed.
