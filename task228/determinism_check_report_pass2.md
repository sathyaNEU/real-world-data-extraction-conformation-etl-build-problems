# determinism-check report, task228, 2026-11-02 (pass 2)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Judge thread: one pass, sonnet, medium, scratch /tmp/determinism-check-task228-1793586632/ (verdict.md there). target.zip md5 b9cd7086c68d951c3c5be40508cce7b3. Reship after the leak-gate repair (no data_dictionary.md or export_manifest.csv) and the ask rework (new ask 3 on collector_client_summary_2026-08.parquet).

## Why
The 82 experiments split 18 with a confirmed data incident and 64 without. Install-level tests give gap sessions 10 and 0, late 5 and 0, duplicate 3 and 0, treatment share 3 and 0, events per install 0 and 3 (with an incident and without). DH-3 s5 allows at most 1 of the 64, so events per install is out and gap sessions leads. The hold line recomputes to 0.28. For ask 3 the collector summary leaves one reading of the day boundary and one data-supported reading of the install, and the golden figures reproduce exactly.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Labelled experiments | 18 with incident, 64 without | 18 register titles map to registry titles after whitespace and case normalisation; 82 completed runs | yes |
| Install rows | stack of three summaries | 659,739 rows, no duplicate (experiment, install) rows | yes |
| Gap sessions held (with / without) | 10 / 0 | 10 / 0; no gap z-score between 2.0 and 3.2 | yes |
| Late sessions | 5 / 0 | 5 / 0 | yes |
| Duplicate sessions | 3 / 0 | 3 / 0 | yes |
| Treatment share | 3 / 0 | 3 / 0 | yes |
| Events per install | 0 / 3 | 0 / 3 (p = 2e-3, 1e-7, 5e-4) | yes |
| Hold line | 0.28 pp | 0.2795 per-arm mean, 0.2778 median, 0.2811 pooled, control only and treatment only; all round to 0.28 | yes |
| Ask 3, 28 values (14 days x iOS, Android) | 6 Aug 39,523; 32,798 ... 19 Aug 1,232; 731 | all 28 reproduce exactly | yes |

## Competing answers that survived
1. **Unit of the test (main call).** DH-3 s3 and s4 say "significant at 1 per cent" but do not say whether the variance is taken over installs or sessions. Session-level two-proportion z: gap holds 11 / 4, duplicate 4 / 4, late 6 / 0. The 4 without an incident exceeds the allowance of 1, so gap sessions is out and late sessions wins at 6, line about 0.22. Install-level (the unit s2 says the platform assigns to arms): gap sessions, 0.28. The data separates them: the session-level test rejects 4 of 64 null experiments at a nominal 1 per cent (miscalibrated), the install-level test rejects 0 of 64. The judge calls this an analytical choice (clustering), forced by the data but not literally filed. Residual risk, recorded; the judge advises against pinning it, since that would make the main call rule application.
2. **What an install is (ask 3).** Reading A (golden): an install is carried across client IDs. 28,927 client IDs first appear on 9.4.2; exactly 5,009 have a first_seq equal to an earlier client ID's last_seq plus 1 (unique, same platform, that ID's last row; 9.4.2 start 4.8 to 383 hours after its last batch). No file states that an update issues a new client ID or the continues-by-one rule; both are inferred from the data, and no other linking field exists. Reading B: one client ID is one install, so the 5,009 predecessors stay "still on 9.4.1" forever.

   | Reading | 6 Aug (iOS; Android) | 19 Aug (iOS; Android) |
   |---|---|---|
   | A, install carried across client IDs (golden) | 39,523; 32,798 | 1,232; 731 |
   | B, one client ID is one install | 39,648; 32,928 | 3,659; 1,922 |

   B differs on every day (7 Aug 36,451; 28,392). The judge rates B not literal-reader-safe, because DH-3 s2 defines an install as the unit keyed by an install ID, not a client ID, and the files never equate a client ID to an install. Ask 3 is rated forced. A solver who misses the +1 join is wrong by about 2.5x on 19 August; the join is discoverable and is an analytical step.
3. **Day boundary (ask 3): closed.** Population: 82,551 9.4.1 rows, one per client ID; the rows whose first batch falls on 3 to 6 August give 77,539 clients (41,717 iOS, 35,822 Android), and the "overlap the window" reading gives the same set. Collector batch hours run 0 to 21 UTC only, so the distribution of batch hours across the file has no batches from 22:00 to 24:00 UTC, which is where Copenhagen midnight (22:00 UTC in summer) falls. Copenhagen end of day, UTC end of day and a fixed UTC+1 offset give identical figures for all 28 values. "Still on it" is as of end of day D, with silent installs counted as still on; no downgrade or interleaving occurs (0 overlaps within a client).

Other alternatives tested (direction rules in s3, the design-share test, Welch against z for events per install) change no check's pass or fail on the allowance, and no tie occurs.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 13 | yes |
| Formats | 3 or more | csv, parquet, pdf, json, xlsx, md (6) | yes |
| Large file | 25,000 rows or more | install_summary_2026q1.csv 238,808 rows (659,739 across three) | yes |
| Distractors | 2 or more in metadata.json, none named in a file name | 4 named: collector_daily_2026.csv, app_releases_2026.csv, booking_queue_2027q1.csv, weekly_review_log_2026.csv | yes (see note) |
| Distractor soundness | unused by the solution, weighable, ruled out by a shipped fact | judge found them available and unused; none answers a graded quantity. app_releases_2026.csv now carries 11.2.1 and the SDK dates but ask 3 is solved from the collector summary | yes, not independently stress-tested |
| Deliverables | 1 to 3, all in the golden | 1 (auto_hold_check_scorecard_2027.xlsx), present in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | three asks in one sentence set each with unit and rounding ("Hold line in the check's own unit, to two decimals; counts as whole numbers"); ask 3 is 14 days x 2 platforms | yes |
| Prompt shape and 25 or more criteria | identifiable shape, rubric 25 or more | shape 10 recorded in metadata.json; rubric criteria count not checked here (rubric is generated downstream) | not verified |
| Reads as LLM generated | no | judge found no authoring language; golden realism not re-read by this pass | yes per judge |

Note: the judge reported no metadata.json in the bundle. That is correct; metadata.json is in the task folder and carries provenance for the 13 files (source, date, CC0-1.0 license), as the leak-gate repair intended.

## Gate G reconciliation
Thread: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note (DESIGN_NOTE.md, Gate G line, read after the thread returned): analytical_non_defect (statistical rigour), surface_read_dependency no, sole_data_defect no. Match. The declared distractors were not named as the surface read carrying the task.

Gate H line: `domain: pass`, `layers: pass`, `decisive_step: analytical`. Layer 1 is mess (title spellings, service 1 vs 2 column schemas, CSV vs Parquet, app-wide incidents); Layer 2 is false-hold calibration of a data-health check on clustered units. The easy route (sessions as independent draws) lands late sessions at about 0.22; the correct route lands gap sessions at 0.28. The design note carries a `## Three rules` section with No decoy, Not semantics and Not rule application lines.

## Stump power (Gate F)
Moderate to good. The decisive step is the unit of analysis: a strong analyst who runs the natural session-level two-proportion test sees gap sessions fail the allowance with 4 false holds and files late sessions at 0.22. Events per install is a second decoy that leads on holds only if the allowance is ignored. Ask 3 stumps anyone who treats the client ID as the install. The judge did not class the decisive step analytical merely because the method is standard; it reached the call by testing which unit the data calibrates. The main thread weighs this against the design note's ladder.

## Findings, ranked
1. Unit of the test not literally filed (analytical, data forces the install-level reading). Leave open; pinning it files the HOW and turns the main call into rule application.
2. Ask 3 install identity rests on an inferred client-ID join (continues-by-one), not stated in any file. Judge rates it forced and discoverable; a literal reader reading "install" as client ID gets reading B (19 Aug 3,659; 1,922). Closure is the DH-3 s2 install definition. Accepted risk of the ask, which is free of the main call's rules.
3. No hygiene issues; nothing exclusion-level.

## Next action for the author
None required. Proceed with the ship checks for the reship; do not file the HOW for the significance test.
