# Verdict, task140 (C-22 batch guarantee, 2027 Q1)

**Verdict:** DETERMINISTIC (with a flagged Gate C risk on the cell-store forecast method and a minor one on the chargeback change date).

**Disposition:** APPROVE for determinism; optional FIX_NOW prompt/CS-3 pin (see Fix). No model rerun needed unless the author chooses to pin the forecast basis in the shipped text.

**Why:** Every committed figure reproduces from the shipped files. The main call turns on the cell-store busiest-hour forecast. The fitted hourly relation (33.1 + 2.9404 per machine in service + 0.20804 per batch core, residual s.d. 13 cores) is very tight, the 5,220-machine step is in the hardware plan, and the batch guarantee is the solved level (CS-3 5.2). That gives 109,492 and so 109,000. The competing answers (122,000 from a line through quarterly peaks, 120,000 from batch at last quarter's 57,000, 106,000 from batch at 122,000) each ignore a fact in the files: the machine step or the batch coupling. The fitted answer is robust to every variation I tried. CS-3 4.1 and the memo never name the forecast method, so the golden rests on an analyst choosing the structural model. That is the one real Gate C exposure.

## Evidence (recomputed from the bundle)
| Item | Result | Source |
|---|---|---|
| Reservable cores 5,220 x 96 x 1.45 | 726,624, reproduced | hardware plan (Racks, By quarter), memo overcommit 1.45 |
| Machines 5,220 | reproduced (4,640 + 29 racks x 20 = 580) | plan rev 11 Dec; installed series peaks at 4,640 in Q4 |
| Firm approvals (min of request, floor(budget/7.42)) | 576,972 reproduced; search-api 126,415, pricing 76,819, reco-serve 52,088 held to budget, other eight at request | requests csv, budgets xlsx Jan 2027 (C-22 lines via tenant_directory CC), rate R117 |
| cell-ctl peak forecast | line through 2026 quarterly peaks 1,999.25; driver fit gives about 2,021-2,026; both round to 2,000 | usage_hourly |
| cell-store fit | b0 33.05, 2.94039/machine in service, 0.20804/batch core, s.d. 13.0 (17,081 hours, 336 exact-duplicate rows of 17 Mar removed). Installed instead of in_service gives s.d. 15.6, so the data prefers in_service | usage_hourly, cell_hourly |
| cell-store at G=109,000 | 38,058 (all-history fit); 2026Q3-only fit about 38,045; reserves 38,000 | |
| Guarantee | (726,624-576,972-1,999-33.1-2.9404x5220)/1.20804 = 109,492 -> 109,000. Boundary distance about 500 either way. With reservations rounded first (577,000 / 2,000 / 38,000): 109,624 -> 109,000 | |
| Preemption loss (core-hours, share) | demand 71,995 (0.49), fraud 48,525 (0.31), nlp 134,899 (0.77), pricing 80,513 (0.37), ranking 121,830 (0.40), reco 144,274 (0.59): all match golden | runs, checkpoints, resizes |
| Machine-hours lost, came back (asset tag mapped through inventory Cluster ids, exact-duplicate REMOVED rows on 19 Aug dropped, intervals split by UTC month) | Jul 748 / 851, Aug 731 / 909, Sep 662 / 883, matching golden 750/850, 730/910, 660/880 | machine_events, inventory |
| Chargeback (ledger 2026Q3 + 29 quota changes, effective at the 00:00 UTC after reconciler application; 7.65 to 7.70 on 1 Sep) | all eleven match golden to 100 EUR (search-api 2,653,000 ... settle-batch 488,500) | ledger, quota_changes, reconciler runs, rate card, policy |

## Forks and competing answers
1. **Cell-store forecast method (Gate C, the main risk).** CS-3 4.1 says "the use forecast for its busiest hour" and nothing about method.
   - Line through quarterly peaks: cell-store 25.5k, guarantee 122,000.
   - Driver fit with batch at last guarantee (56-57k): about 27.1k store, guarantee 120,000.
   - Driver fit with batch at the solved guarantee: 109,000, the golden.
   - Driver fit with batch at the 122,000 line answer: 106,000.
   - A historical back-test does NOT separate line from driver (both within about 500 cores for 2026Q1-Q3, because machine growth was smooth). The separation rests only on the 640-machine step in the plan and the hour-level fit (s.d. 13 vs 640 without batch). An expert who reads the plan and tests drivers lands on 109,000. A line-extrapolating analyst is not unreasonable on the text alone. Judged forced given the data, but only just. A one-line pin removes it.
2. **Chargeback effective date of a change (minor).** Policy 2.2 says "release or grant made during the quarter". "Holds ... at 00:00 UTC" with the data-dictionary definition of changes_applied points to reconciler application, which the golden uses. Using requested_utc shifts several tenants by 100-700 EUR (payments 697,400 vs 696,700; search-api 2,653,300 vs 2,653,000), so a few cells would differ at the stated rounding. I judge the golden the literal reading, but it is not airtight.
3. **Preemption loss basis.** The data dictionary (write_started = state time, training carries on) and the restore_checkpoint column pin loss as cores integrated from the restored checkpoint's write_started to preemption, with resizes. Counting from commit time gives a different result (ranking 117,400, 0.38%). Clipping to Jul-Sep is required by the prompt (unclipped changes nlp to 0.76 and reco to 0.58). Pinned.
4. Machine-hours: "came back into service" excludes 7 never-returned (retired) assets; duplicates identical, so no fork.

## Files/Hygiene: PASS
- 24 files; formats pdf, csv, xlsx, docx, json, txt (6). One file of 239,470 rows. Distractors plentiful (batch_training_demand note, cells summary, ops log, hardware inventory beyond the machine-id join).
- Realistic noise: re-sent day (17 Mar), collector outage 19 Aug, duplicate event rows, machine id changes, superseded plan revision, other cells' budget lines.
- README_capacity_review_files.txt is an in-fiction file index. It carries no authoring language, so I rate it fine (a minor point against the "no README" rule; the author may drop it).
- Temporal coherence good (exports pulled 14 Dec, review 15 Dec, report 6 Oct, figures consistent with plan).
- No exclusion-level finding. No canonical public-data contamination. The cell-store/batch coupling is nowhere documented in prose (no leak).

## Stump power
Plausible stump. Model default: line through quarterly peaks or a driver fit at the old guarantee. The 580-machine step is stated in memo and plan, so a careful solver can find it, but the batch coupling and the simultaneous solution require genuine modelling. Supplements (checkpoint-state loss with resizes, asset-tag re-pairing, reconciler-timing chargeback) add multi-step load. The risk is that strong models split on the unpinned method (Fork 1), which would be a Gate C/D finding rather than a clean stump if a model finds the machine step yet chooses a different peak-forecast construction.

## Stumping type
`mechanism: forecasting` (with method_or_model_selection), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. Reported peaks are correct; the difficulty is a forward projection that history alone does not pin (the plan's machine step plus the batch coupling). On clean data it still stumps. Passes Gate G.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Domain: capacity planning of a compute cell (peak-hour use forecast against hardware growth, preemption loss from checkpoints, fault/maintenance availability, chargeback). Layer 1: change-log style re-sends, collector outage, machine-id churn, superseded plan, reconciler lag. Layer 2: a driver-based forecast of the platform reservation solved jointly with the guarantee. Easy route: trend line through quarterly busiest hours (cell-store about 25.5k) which gives 122,000; the correct driver model gives 109,000.

## Fix
- None required for correctness. Recommended, optional and low cost (prompt or CS-3 text, input_files): pin the forecast basis, for instance CS-3 4.1 stating that a platform service's busiest-hour forecast is made from its relation to the cell's installed machines and the batch tier's cores, or a filed selection criterion (a back-test where the structural model wins). That closes Fork 1 without handing over the answer.
- Optional: state in policy 2.2 that a change counts from the first 00:00 UTC after the quota service applies it (closes Fork 2).

## Disposition

The verdict above is the isolated judge thread's verdict.md, verbatim (one pass at medium effort on a fresh unzip of target.zip, prompt.txt, the submission's graded blocks and the judge's system prompt).

APPROVE. No re-judge is owed: the verdict is DETERMINISTIC and no FIX_NOW was raised. Both risks are closed in the record in one generator pass, and no graded figure moved (`freeze.py check --mode determinism` PASS; both goldens and `figures.json` byte-identical to the judged pack).

- Fork 1, the cell-store forecast method: the optional pin is refused. Filing the forecast basis in CS-3 4.1 (or a back-test criterion) names the decisive step and makes it rule application, and the back-test the judge ran does not separate the line from the drivers, so a filed criterion would pick neither. CS-3 4.1 already files the estimand the judge read ("reserved for the quarter at the use forecast for its busiest hour of the quarter", with 5.2 running batch inside that quarter's guarantee), so no method word was added. The design note's fork table now carries the two competing readings as their own rows: SF29 (batch at the last quarter's guarantee, 120,000) and SF30 (the load read at another answer's guarantee, 106,000 at 122,000), each ruled out by that estimand, with the data facts asserted in checks.py (at cell-store's busiest hour of every quarter on file batch held at least 99.6 per cent of that quarter's own guarantee, within 200 cores of it and 983 to 3,031 from the quarter before's; 109,000 is the one whole thousand whose own storage load leaves it). SF13 records the back-test's non-separation (the line misses 2026 Q1 to Q4 by 26 to 489 cores, the fit on both drivers by 177 to 204) and the data fact that separates them: 2027 Q1 opens 640 machines above 2026 Q4 (no quarter on file stepped more than 60), worth 1,615 cores of cell-store above the line on its own, with a guarantee near double the history's, both carried by the hourly fit (residual s.d. 13.0 cores on both drivers, 638.5 on machines alone, 356.2 on batch alone).
- Fork 2, Ask C's change date: closed in the filed text. Chargeback policy 2.2 now ends "A release or grant counts from the first 00:00 UTC after the cell's quota service has applied it.", naming no file or join. checks.py asserts the sentence ships, that its literal execution on its own code path gives the golden for all eleven tenants (from the applying run's start or finish, the same midnight), and that the request-time reading misses 11 of 11 (payments 697,400 against 696,700), the request day's own 00:00 10 of 11 and the application day's own 00:00 10 of 11 (SF25). The September rate split is closed beside it (SF26: the opening rate, the September rate all quarter and the rate from its publication each miss all eleven).
- Fork 3 and the machine-hours note are confirmed in the record (SF20 to SF23, SF32 to SF37). The README note is kept as an in-fiction file index.
- Changed under target/, figure-neutral: README_capacity_review_files.txt, batch_training_demand_2027H1.pdf, c22_capacity_report_2026Q3.pdf, capacity_memo_2027Q1.docx, chargeback_policy_2026.pdf, data_dictionary.xlsx, tech_budgets_2026_Q1-2027_freeze.xlsx (the policy sentence above; the memo's platform line names no source; the leak reader's realism tells reworded). Every data file is byte-identical to the judged pack.
- Gates on the final rebuild: checks.py 2,358 assertions, verify.py, two byte-identical builds, figures_check.py, precut.py, voice-check.py, leak.py (REVIEW, no LEAK), guard.py surface, heart and validate.
