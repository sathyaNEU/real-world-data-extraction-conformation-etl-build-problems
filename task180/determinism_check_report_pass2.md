# determinism-check report, task180, pass 2, 2026-10-12

## Verdict
DETERMINISTIC (the pass-1 wording defect, SOLUTION_WRONG on the tolerance claim, was re-flagged in minor form and has since been repaired; see Findings)
**Disposition:** APPROVE after the two wording repairs the coordinator reports as applied post-thread (tolerance claim narrowed, step 8 grouping and last-origin rule stated). The thread itself returned FIX_NOW on solution wording only. No figure, prompt or input file changed. I did not re-run the thread; the applied wording is checked by reading `submission.md` only.
**Stumping type:** mechanism: forecasting (borderline planted_defect_flip), stumping_family: analytical_non_defect (borderline), surface_read_dependency: no (borderline), sole_data_defect: yes by the clean-data test (borderline)

## Why
Executed literally, the scheme and ordinance reproduce the bulletin's located counts exactly, and the 2027 networks are designed to locate every earthquake of ML 0.6 or more. Pfeilbrunn's reviewed catalogue is complete at ML 1.0 only from 23:30 to 05:00 (442 of 658 events), so the night rate scaled by 24/5.5 gives 28.0 per 100,000 m3 against 9.6 whole-day, putting Q1 (about 223) and Q4 (about 206) over 120 while every other plant stays at 85 or under. All other night-window, Gutenberg-Richter and earlier-year conventions the thread tried leave the same classification. No gate failure; the only open points were the docx tolerance wording and the unstated origin-grouping and last-origin rules.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Pfeilbrunn located ML 1.0+ within 5 km, Jan 2023 to Sep 2026 | 658, of which 442 at night | 658 / 442 (`seismic_catalogue_reviewed...csv`) | yes |
| Pfeilbrunn rate per 100,000 m3 | 28.0 night-scaled, 9.6 whole-day | 28.0 / 9.6 | yes |
| Other plants' rates | not asserted separately | MOS 11.27, WDR 6.73, OTM 6.35, LZR 10.9 from Aug 2025 | yes |
| Pfeilbrunn 2027 | 223 / 70 / 44 / 206 | same | yes |
| Moorstetten 2027 | 85 / 37 / 26 / 81 | same | yes |
| Lanzenried 2027 | 76 / 33 / 24 / 73 | same | yes |
| Ottenmoos 2027 | 47 / 22 / 14 / 46 | same | yes |
| Wendelsried 2027 | 45 / 21 / 15 / 45 | same | yes |
| Annex volumes (15 values) | e.g. PFB Q1 794,800 | PFB Q1 794,756 etc., all 15 | yes |
| Annex automatic counts (15) | MOS 117/50/42 ... OTM 64/22/22 | identical | yes |
| Annex hours under four stations (15) | MOS 95.0/44.4/57.1 ... OTM 81.4/28.5/78.0 | identical | yes |
| Default-path counts | PFB 62 and 77, MOS 92 | PFB 77/62/18/15 per bulletin, MOS 92 | yes |

## Competing answers that survived
No fork changes the main call or any annex figure.
- Origin grouping tolerance: any gap from 1 to 5 s gives the golden; 0.5 s gives OTM Q1 65, 10 s moves LZR and WDR Q1 by 1. Was unstated in the text the thread saw; step 8 now says within 3 seconds.
- "Last origin": by creation time gives the golden; by latest origin time gives LZR 102/39/28 and PFB 82/23/18. Was unstated; step 8 now says the origin the system created last (the scheme's "final automatic solution" supports it).
- Docx quarter counts under other rate conventions: Gutenberg-Richter extrapolation gives rate 23.1 (184 and 170 in Q1 and Q4) and night-window volume weighting about 8 per cent higher. The old "any other rate convention" claim failed for Gutenberg-Richter; the claim is now restricted to the quiet-hour conventions with "no convention moves a cell across 120". The classification holds under all of them.
- Unshifted 2026 report labels would give PFB Q1 2026 868,150, wrong; closed by the receipt-month evidence (received dates, repeated December 2025 row, telemetry) and by scheme 6.2.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 | yes |
| Formats | 3 or more | 7 (csv, md, xlsx, json, parquet, pdf, xml) | yes |
| Largest file | 25,000 rows or large DB | `injection_hourly...parquet` 197,130 rows; `origins...csv` 31,267 rows | yes |
| Distractors | 2 or more in `metadata.json`, not labelled in names | `federal_catalogue_2023-2026.csv`, `groundwater_levels_2025-01_2026-09.csv`; no name labels them | yes |
| Distractors relevant and ruled out | same world, unused, a shipped fact rules out | federal catalogue (same events, magnitude 2.0 and over only, so blind below the counting line), groundwater (same plants, not a graded quantity); neither answers the decision question | yes (judged by reading; the thread named neither as the surface read) |
| Deliverables | 1 to 3 | 2 (`amber_outlook_2027.docx`, `tls_annex_2026.xlsx`) | yes |
| Goldens present | all named | both in `golden/` | yes |
| Units and rounding | stated in each ask | cubic metres to nearest hundred, whole counts, hours to one decimal | yes |
| Asks multi-dimensional | yes | 20-cell grid plus 45 annex figures | yes |
| Prompt shape and 25-criteria floor | identifiable, 25 or more | shape 07 (grid of cells), 65 graded cells | yes (generated rubric not inspected) |
| Realism | no LLM tells | thread found 16 plausible operational artifacts, no disclosures; golden realism not re-read by me | yes (thread's read) |

## Gate G reconciliation
Thread: forecasting across a measurement-regime change (borderline planted_defect_flip), analytical_non_defect (borderline), surface_read_dependency no (borderline), sole_data_defect yes by the clean-data test. Design note and card: gate_g forecasting, stump_strategy other (detection completeness on a daily noise cycle), pattern none, decisive step analytical. Mechanism agrees. The one soft point is sole_data_defect: with a complete catalogue the Pfeilbrunn pitfall disappears, so a reviewer could read the decisive step as a data defect; the thread kept it as wanted because the forward-regime forecast and the Lanzenried network-change layer remain, and the correct estimand is a completeness-corrected rate. Distractors are not the surface read: the thread's surface read is the bulletin's trailing located counts, which the design note labels the default path's input, and the thread listed the declared distractors only as hygiene. No build-versus-outside mismatch beyond that borderline reading.

## Gate H reconciliation
Thread: domain pass, layers pass (layer 1: shifted 2026 label convention, MST-Th4a alias, exchange-day epochs, LZR station replacement, UTC against local quarters; layer 2: completeness-corrected forecast), decisive_step analytical. This matches the design note's domain test (catalogue completeness by hour and the Gutenberg-Richter rate), layer 1 list and analyst test. No mismatch.

## Stump power (Gate F)
Good per the thread. The bulletin's all-green counts (maximum 92) point to no plant over amber and year-on-year growth points to Lanzenried (about 183). Reaching the golden needs the hour-of-day completeness structure and the 2027 detection change; the ordinance's ML 0.6 design and the town-network remarks are only indirect pointers. A strong model that reads the clock and magnitude distribution fails less often, a risk the portal will measure.

## Findings, ranked
1. `submission.md` Deliverable Answers ask 3, tolerance claim: the pass-2 thread found "within 8 per cent under any other rate convention" false for Gutenberg-Richter extrapolation. Reported as already narrowed to the quiet-hour conventions with "no convention moves a cell across 120"; the current text matches (checked by reading). Residual: the Gutenberg-Richter route lies outside the narrowed claim, which is accurate.
2. `submission.md` step 8: origin grouping tolerance and last-origin rule were unstated. Reported as applied (within 3 seconds, origin the system created last); the current text matches. The bundle's own text does not state either, so they remain choices carried by the clean event separation (spread at most 0.7 s then 8 s or more) and the scheme's "final automatic solution"; the thread judged both non-load-bearing for the call and, for creation order, supported by the scheme.
3. Borderline stumping-family and sole_data_defect reading (Gate G above); no file change, route to the portal.
4. Minor, hygiene: the catalogue's `reviewed_utc` runs to 12 October while the bulletin cites the catalogue as at 8 October; counts still match. Not exclusion-level.

## Next action for the author
Re-read the two edited lines in `submission.md` once against the golden docx and xlsx, then ship `target.zip` as built.
