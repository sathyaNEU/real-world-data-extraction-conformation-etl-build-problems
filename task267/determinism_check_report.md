# Determinism check, task267, pass 1

Round 1 of stage 4 (2026-10-17), on the seed 285 pack with the shares asked to one decimal. The determinism-judge agent had no Agent tool, so the isolated judge thread ran from its brief; its verdict follows as written. The fixes (the write-up's step on copies four or five hours later, the sensitivities to the whole percent on seed 694, the memo grain left to the export's own inconsistency) are recorded in the design note's build record; pass 2 judges the rebuilt pack.

# Verdict, task267

**Verdict:** DETERMINISTIC (main call forced; two small residual forks on supplementary figures, listed below). Solution blocks reproduce in full.

**Disposition:** FIX_NOW. File two conventions that only fix what the correct figure IS (the A11 duplicate copy on 5 March, and the group-weighting estimand for the shares), no change to the analytic surface; no model rerun needed if done as a note/dictionary pin. APPROVE is defensible if the author accepts the residual forks.

**Why:** The call is forced by protocol 6.2/6.3 plus the shipped data: weighting complete OGTTs back to the 2026 groups (RULE vs not referred, 7,604 / 30,997 adults) puts A60 (50.9), A57 (79.1), R26A60 (77.1), SC5 (59.0) under 85% and leaves A57G120 (91.3 / 35.9) and A55 (92.6 / 48.7) qualifying, A57G120 with fewer referrals. The call survives every weighting variant tried (unweighted gives a different, wrong call: R26A60 at 93.5 and 24.5%).

**Evidence (recomputed from target/):**
| Figure | Reproduced | Source |
|---|---|---|
| 38,601 adults (97 re-sent encounter_ids dropped, first screening per program_id; 786 return visits matches close-out) | yes | screening_encounters_2026.csv |
| 11,168 complete OGTT, 1,158 undiagnosed; all 11,509 results match on 7 digits | yes | ogtt_results_2026.txt |
| Shares (undiagnosed / screened): A60 50.9/8.5, A57 79.1/28.1, R26A60 77.1/24.5, SC5 59.0/35.6, A57G120 91.3/35.9, A55 92.6/48.7 | yes (50.93, 79.07, 77.13, 59.00, 91.27, 92.61; 8.51, 28.10, 24.53, 35.63, 35.88, 48.73) | encounters + ogtt + candidate_referral_rules_2027.xlsx |
| Cartridges per analyzer A01..A12 (3602, 4068, 3661, 3134, 3879, 3547, 3036, 3243, 3040, 3511, 3560, 3432), total 41,713 | yes, only when BOTH the 4-hour copies (8,588 rows) and the 63 five-hour copies of 5 March (serial GQ2-41391, A11) are dropped, E-02/04/06/09 excluded, serial mapped to tag by date, season days 2 Mar to 20 Nov 2026 | gq200_run_log_2026.csv, analyzer_asset_register.xlsx, gq200_error_codes.pdf |
| Monthly net / adults-screened dollars Mar-Nov (15,207.50/14,630.00 ... 49,742.00/49,126.00), totals 435,088.50 / 428,274.00 | yes, by service_date month, each credit line at its applied-to invoice line's 38.50 | thessler_invoice_lines_2026.csv |

Forks found:
1. A11 cartridges: the shipped run log has no note that rows are held twice. Dropping only exact 4-hour copies (the solution's stated rule) gives A11 = 3,621 (total 41,774); the golden 3,560 also needs the 5-hour copies on 2026-03-05, which the solution step does not state. A solver can see the whole-day replication, but the step as written is not the golden.
2. Credit memo grain: on multi-line memos amount_usd repeats the memo total on each line (e.g. -77.00 on each of 2 lines applying to 38.50 lines). Literal summing gives net 434,780.50 for the season file, not 435,088.50 (the credit would exceed the line it applies to, so the golden reading is the only coherent one, but it is nowhere filed).
3. Weighting estimand for the shares: group weights over complete tests (golden) versus design weights (all drawn, no-shows counted non-diabetic) change last digits: A60 50.9 vs 51.0, R26A60 77.1 vs 77.3, SC5 59.0 vs 59.1. Event-stratified weights move A60 to 50.5 and A57G120 to 91.7. The qualifying set and the call never change; only the supplementary tenth-of-a-percent figures are method-sensitive. Protocol 6.2 ("counting every adult screened, whether or not they had the test") supports the golden reading.
4. Tests "of adults screened" = invoiced accessions present in ogtt_results (205 invoice lines have none); reasonable but implicit.

**Files/Hygiene:** PASS. 14 files, formats csv, xlsx, pdf, txt (4); run log 51,094 rows, encounters 39,484 rows, invoices 12,239 rows. Realistic mess (re-sent rows, dropped hyphens/leading zeros/lower case, M/D/Y dates, loaner serials, credit memos). Distractors present (event_calendar, participant_feedback, orlenby profile, close-out). No authoring disclosures, dates coherent (extracts 14-18 Jan 2027, close-out consistent with encounters). Nothing exclusion-level.

**Stump power:** Moderate. The easy route (rule-by-rule shares among adults who had the OGTT) gives R26A60 (93.5% / 24.5%) as the cheapest qualifier, wrong; the correct answer needs the 1-in-5 evaluation draw reweighting. Protocol 4.2 and 6.2 point close to the correction, so a strong model may clear it; the asks (dedup with unstated 4h/5h copies, serial-to-tag by date, credit grain) carry most of the difficulty.

**Stumping type:** `mechanism: statistical_rigor`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. Partial-verification (workup) bias correction on honest data decides the call; no reported figure is wrong.

**Three rules:** `domain: pass`, `layers: pass`, `decisive_step: analytical`. Screening-test evaluation under partial verification is what a diagnostic-screening field estimates; easy route = shares among completed OGTTs only, which picks R26A60 instead of A57G120. Layer 1: re-sent rows, mistyped IDs, loaner/replacement analyzers, credit memos.

**Fix:** none for the main call. Solution/prompt-note: state in the solution step that run-log copies recur at both 4 hours and 5 hours (5 March, A11), pin that credit lines count at the applied-to invoice line's amount, and file the group-weighting convention for the shares (population: all adults screened in 2026, each complete test standing for its 2026 group). Keep the shipped data unchanged.
