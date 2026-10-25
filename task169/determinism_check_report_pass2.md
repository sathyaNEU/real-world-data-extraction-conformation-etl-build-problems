# determinism-check report, task169, 2026-10-25 (pass 2, portal round 2 repair)

## Verdict
The main call DETERMINISTIC; asks 2 and 4 NOT_DETERMINISTIC as shipped, closed afterwards in the prompt's ask clauses
**Disposition:** labelled SEND_BACK by the thread, read against the gate table as an ask-layer repair: Gates C and E fail
on supplementary asks only, the main call is forced (every sound estimate 18.2 to 20.9, all 20) and Gates F, G and H pass,
so no architecture is spent. Applied: the units the thread named, in the ask clauses ("one per parolee per hearing date";
"with the person back from the writ or released"), the call sentence untouched; write-up step 3 names its arrest base.
No graded figure moved (freeze --mode determinism PASS), so no further pass.
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Pack: target.zip 73e3137b, unchanged. Thread: scratchpad determinism-check-task169-r3, order kept (blind_derivation.md on
disk before graded_blocks.md was opened).

## The thread's verdict, verbatim

- **Verdict:** NOT_DETERMINISTIC (main call and ask 3 are forced; asks 2 and 4 are not). Main-call figure and ask 3 reproduce exactly; ask 2 and ask 4 reproduce only under conventions the prompt and bundle never file. Also SOLUTION_WRONG (minor wording, see Evidence).
- **Disposition:** SEND_BACK. The repair is two clauses in prompt.txt (what counts as "a recommitment" and when a writ trip "ended"); this changes what solvers see, so prior runs need a rerun. The main call, the stump and the ask 3 figures stay frozen.
- **Why:** Main recommendation (20 per cent) is forced: every sound estimate lands in 18.2 to 20.9, all rounding to 20. But ask 2 (golden total 3,174) holds only if two cases decided for the same parolee on the same date are one recommitment; counting each REVOKE/REVOKED decision, as the prompt's "the recommitments the Board ordered" reads literally, gives 3,523. Ask 4 holds only if a writ trip with no WRI ends at the release (or the next movement); nothing shipped says so, and paired-only execution gives different figures in every cell. Gates C and E fail on asks 2 and 4; taxonomy label: underspecified_objective.
- **Order kept:** yes. blind_derivation.md was written to disk before graded_blocks.md was opened.

## Evidence (recomputed from the bundle)
Main call. Releases PAR/RPR/PAROLE/REPAROLE 1 Jan 2019 to 30 Sep 2024: 30,959. Any ADM in 730 d about 52 per cent (easy wrong route, 50). NEW COMMITMENT ADM only 8.7 per cent (routes to 10). Cause of the gap: every arrest the Board revoked on is nolle prossed in the AOC extract (11,965 of 11,968 in-window revoked-on arrests NP; 354 of about 15,000 others), so the record's court-commitment rate is the Board's, not a court's. Court DOC-sentence rate on arrests the Board did not revoke: 22.2 per cent; same 22.2 per cent on the 8,736 arrests after the maximum expiration date (Board cannot revoke; revoked share 0.2 per cent), same grade mix. Arrests per release 0.871; per community day (custody days from PV ADM to next release removed; exposure 82.5 per cent of 730) 1.056 per 730 d. Expected court commitments admitted inside the window: 0.2216 x 1.056 x 0.86 to 0.90 timing, then 1-exp: 18.2 (crude timing) / 18.7 / 19.1 (banded hazard) / 20.9 (no timing). Poisson dispersion 0.97. Cohort-mix standardisation to the 6,466 (RPR 18 per cent) moves it under 0.1 pp. Golden 20.4 inside the range; nearest rounding line (17.5) is 0.7 pp below the lowest variant. Wrong routes: 50 (all admissions), 10 (NC ADM, 8.7 raw / 10.7 exposure-adjusted), 15 (arrests not exposure-adjusted: 0.871 x 0.2216 x 0.88). The ladder is separated by the analysis, not by a reading.
Step-3 figures: golden 9,410 / 15,707 / 3,483 and 25,117 versus my 9,365 / 15,688 / 3,482 and 25,053 (release-linking difference of about 0.2 per cent); 374 NP of the others matches. Not load-bearing, but the blocks' counts do not reproduce to the digit.

Ask 2 (D1 / D2 / D3 / D4, arrest / conditions alone). Golden 1,277/261, 621/210, 368/172, 116/149 reproduced exactly (3,174) with: legacy REVOKE rows dated to 2 Jan 2026 plus new-system REVOKED (199 legacy-carried cases appear in both and are deduplicated), minus rescinded by 30 Jun 2026 (41), then one recommitment per (parolee, hearing date) (347 merged; 185 pairs share one term_days and one PAROLE VIOLATOR ADM) and arrest if any merged case cites an arrest number (60 mixed pairs). Fork A: per decision row = D1 1,362 arrest / 354 alone, D2 658/259, D3 385/211, D4 123/171 (3,523). Fork B: arrest if all cases cite (differs by up to 60 orders). Neither is filed in the prompt; the Act's definition ("the return of a parolee") supports one-per-return but is not the instruction a literal executor follows.

Ask 3. Golden reproduced exactly: Garrison 34,632/35,505; Ridgway 21,448/23,962; Linwood 17,928/19,236; Corliss 10,265/10,627. "Parolee-days" is the filed unit, so concurrent detainers on one person are merged (summed per detainer would be 36,677/38,019 etc.); the end of a legacy revoked detainer, blank in the legacy file, is the next PAROLE VIOLATOR ADM (the new system's hold_end equals the ADM date in 99+ per cent of revoked cases). That join is an inference from the new file, not a stated rule, but the new system's own hold_end ("date the person left the county jail") closes it; end at action_date would give D1 30,741/31,687.

Ask 4. Golden reproduced to the digit only with trips ended at the first of next WRI, release, or (4 trips) the next ADM/TRN: KTR 3,443/4,237; FNW 3,838/4,166; DNM 3,896/4,122; LKV 3,957/4,546; BRW 3,947/4,497. Paired WRO-WRI only: KTR 3,307/4,124; FNW 3,710/4,044; DNM 3,747/3,969; LKV 3,795/4,379; BRW 3,783/4,325. 2,123 of 30,397 WRO have no WRI (2,119 followed by a release in 1 to 6 days; 9 reach an ADM/TRN long after). Step 8 as written (next WRI, or release if first) leaves those 4 to 9 trips open to the end of the extract and so does not itself reproduce LKV and BRW; the golden also needs end at next ADM/TRN. No shipped file or the prompt states how a trip without a return ends.

## Files/Hygiene
PASS with notes. 15 files (csv x9, parquet, xlsx x3, pdf x3 plus manifest), 4 formats, one file over 100,000 rows. Export manifest and dictionary read as system documents; fictional jurisdiction (Pembroke) consistent; dates coherent (extracts 2026-10-02 to 10-14, no fact after setting). Distractors present (PRAT study, capacity report, caseload, death matches). Legacy and new case systems, M/D/Y versus ISO dates, hyphenated crosswalk keys, mixed code vocabularies before March 2022 are Layer 1 mess and behave plausibly. One note: the methodology PDF 4.2 states the estimand in so many words (new court commitment within 730 d), which is fine for determinism. No exclusion-level finding.

## Stump power
Good. A capable analyst who cleans and reads everything correctly files 10 (count NC admissions, 8.7 to 10.7 per cent) or 15 (arrests per release without removing custody days), or 50 (every admission, the PRAT study's 45 to 61 per cent); only recognising that Board-revoked arrests never reached a court and re-applying the courts' own conversion at risk-time-adjusted arrest rates gives 20. Three distinct wrong answers sit one step apart on the 5-point ladder.

## Stumping type
`mechanism: forecasting (counterfactual rate under a changed regime, estimated from out-of-regime history); stumping_family: analytical_non_defect; surface_read_dependency: no; sole_data_defect: no`. The record's numbers are correct; the work is choosing the estimand's conversion (arrest to court commitment, per community-day) rather than catching a wrong figure. The NP pattern is a realistic system consequence (prosecutors drop cases the Board resolves), not a planted defect, and it is checkable on post-expiration arrests where it vanishes. Passes Gate G. Clean-data test: still stumps.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Field's own analysis: projecting a recidivism/return rate for a population forecast under a policy change, with exposure-adjusted hazard and court-conversion rates validated on a population the Board could not revoke. Swap test fails to preserve the task (it cannot be read as another domain). Layer 1: legacy versus new Board system, PAROLE/PAR code change, sbi hyphenation, orphan writs. Layer 2: counterfactual return rate at risk-time. Easy route: count new-commitment admissions (10) or arrests per release (15). Asks 2 to 4 are rule-application or semantics, which is allowed because the main call is not.

## Fix
prompt (asks 2 and 4 only; main call frozen): file the WHAT as a clause: ask 2 "count a parolee's recommitment once per hearing date, a reported arrest if any of the cases decided that day cites one"; ask 4 "a trip with no return ends on the day of the person's release or next movement". No data change; regenerate goldens only if the author chooses different conventions. Regenerate solution step 8 to name the ADM/TRN ending and step 3 counts to the recomputed ones.

