# determinism-check report, task236, 2027-09-14 (run 2026-10-17)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: decomposition (ETL plus ascertainment adjustment), stumping_family: analytical_method (estimand and independent-denominator adjustment), surface_read_dependency: no, sole_data_defect: no

## Why
One isolated judge thread (sonnet, medium, scratch path only) recomputed every committed answer from the fresh unzip: the flag set (Far North, Metropolitan South, Metropolitan West, South Coast), the eight season-to-date counts and the eight week 36 rates. CDB-FLU-03 sections 2 to 4 pin the case definition, report week, region assignment, the 09:00 local (23:00 UTC) cut-off, the rate denominator and the flag test (share of infections notified, four weeks from the change over four before, more than a quarter either way). Flagged ratios are 1.87, 0.45, 1.53, 1.53 against 0.99 to 1.01, so the call is far from the threshold.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Cases built / in eight regions | 46,380 / 44,872 | 46,554 built, 174 other-state excluded, 46,380; 44,872 | yes |
| Before / after cases, 8 regions | 434/2,226; 763/2,267; 286/895; 583/1,368; 2,459/6,943; 2,603/2,638; 1,210/6,763; 655/2,487 | identical | yes |
| Share-notified ratio FN NC TB CW MN MS MW SC | 1.87 1.01 1.00 1.00 0.99 0.45 1.53 1.53 | 1.866 1.010 1.001 1.002 0.992 0.447 1.527 1.527 | yes |
| Season to date wk 14-36 | 3,560 4,113 1,505 2,491 12,037 6,133 11,230 3,646 | identical | yes |
| Week 36 rate per 100k | 53.7 39.1 54.6 50.6 36.7 24.9 68.4 104.0 | identical (wk 36 cases 157 203 117 191 423 255 659 426) | yes |

## Competing answers that survived
None that change a graded figure or the flag set.
- Cut-off read as 09:00 UTC gives different week 36 counts (FN 164, not 157). The dictionary states AEST and UTC and section 2 says 09:00 Monday, so the local reading is the literal one. Layer 1, pinned.
- Pooled activity, or mean of weekly ratios: same flag set.
- Notified time from the earliest result versus the first specimen's earliest result: identical counts.
- No preliminary-then-negative reversals, so preliminary handling does not fork.
- Weakest point (low risk): activity from ILI alone or positivity alone is not a measure of infections and flips NC, TB, CW, MN to flagged (ILI-only 1.31, 1.70, 1.77, 1.61). Section 4's word "infections" rules these out, but the estimation method is not filed word for word. This is the intended open method; the data separates the candidates.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 13 | yes |
| Formats | 3 or more | csv, pdf, xlsx, md | yes |
| Large file | 25,000 rows or more | gateway csv 229,848 rows | yes |
| Distractors | 2 or more named in metadata.json, no file name labels one | vaccine doses by region, laboratory turnaround by week; names are neutral | yes |
| Distractor role | unused by solution, relevant enough to weigh, ruled out by a shipped fact | neither counts cases or infections; doses peak in May, turnaround flat (design note); not answering a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 16 figures over two asks; rate to one decimal in the prompt, counts whole | yes |
| Prompt shape and rubric | identifiable shape, 25 or more criteria | shape 07 (grid of cells); metadata records 30 criteria | yes |
| Reads as real, not LLM generated | | judge found nothing; goldens not inspected visually by me | yes (judge) |

Provenance and license are recorded in metadata.json (CC0-1.0, seeded generator).

## Gate G reconciliation
Thread: mechanism decomposition, stumping_family analytical_method, surface_read_dependency no, sole_data_defect no. Card: stump_class analytical; the declared easy path is positivity (files 5 of 8 wrong: NC, TB, CW, MN flagged, FN missed). The judge named raw before/after counts as the easy route (also 5 wrong: those four flagged, MS missed). Different easy route, same stump: the independent sentinel infection index. Neither declared distractor is the surface read carrying the task, so no finding. Card fields mechanism and stumping_family are None; no mismatch to compare against. No shipped artifact ranks the regions and gets it wrong; Gate G holds.

## Gate H line
domain: pass, layers: pass, decisive_step: analytical. Matches the design note's Three rules (domain test, Layer 1 mess, Layer 2 field_method, not semantics, not rule application, no decoy).

## Stump power (Gate F)
Strong. Raw counts, positivity, unchanged-region controls and per-consultation or per-swab-positivity measures each file 4 or 5 regions wrong. Building the index from two sentinel files with missing returns and untested swabs is where a strong model plausibly fails.

## Findings, ranked
1. Low: the infection index (ILI per 100k times swab positivity) rests on the word "infections" in section 4 and the sentinel protocol rather than a filed formula. Judge considers the alternatives not defensible; no action required, and filing the formula would turn the decisive step into rule application.
2. Note: the judge's named easy route (raw counts) differs from the card's (positivity). Both are covered by the analyst test.

## Next action for the author
None required; proceed to stage 5 ship once the leak reader finishes.
