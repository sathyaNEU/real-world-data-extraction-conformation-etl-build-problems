# Determinism check, task173 (architecture 4)

Three isolated judge threads (general-purpose, sonnet, medium) on fresh copies of prompt.txt, target/ and the submission's graded blocks, 2026-11-02. Rounds 1 and 2 drove the repairs recorded in DESIGN_NOTE.md ## Stage 4 rulings; round 3 is the verdict of record.

## Round 3

# Verdict, task173 (r3)

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. No repair needed, no model rerun.

**Why:** The activity-line document fixes the estimand (central expectation, FY 2027/28, both hospitals, any residence, the NEL-GS-07 code set) and requires consistency with the elective capacity plan. The capacity plan's section 3 shows the cholecystectomy list falling from about 1,000 to 160-330. The snapshots and PAS then give a flat emergency hazard for listed patients (about 0.0205-0.0214 per patient-month in every year and in every wait-duration band) and a stable non-listed age/sex base. Every reasonable variant lands in 403-416 and rounds to 400. The easy route (age/sex rates on all spells) gives 611 and files 600.

**Evidence (recomputed from target/):**
- NEL-GS-07 spells: 3,280 emergency first-episode gallstone spells after code normalisation (K80.2 D, K802X, etc.), the Fennick PAS to EPR map, and sex codes 1/2 vs text.
- Listed rate: 1,138 listed spells / 54,006 patient-months (Apr 2022 to Oct 2026) = 0.02107, which matches 0.0211.
- Plan exposure: 330+200+170+180+170+180+180+180+190+160+170+160 = 2,270, which matches. 0.02107 x 2,270 = 47.8, which matches.
- Non-listed base with the golden's convention (FY24 and FY25 full, FY26 Apr-Oct annualised, 2022-based mid-2027 population, out-of-area spells included, Marlstead + Coldvale as base) = 359.8, which matches "about 360". Total 407.6-407.7, which rounds to 400.
- All-spell base = 611.3 (golden 611.4), which matches.
- Forks tested on the main call (none moves the rounded answer):
  - Apr-Oct annualised for all three years: base 367.9, total 415.7, files 400.
  - Population year at FY end: 355.5-363.6.
  - FY25/26 only or FY23-26 window: total about 410-418.
  - Prior-month-only link: same 1,325 spells, rate 0.0211.
  - Excluding out-of-area spells: about 398.
  - Listed hazard by wait band (0-1, 1-2, 2-3, 3-6, 6-9, 9-12, 12-18, 18-24, 24+ months): flat, 0.018-0.025 with no gradient, so shrinking the list to a fifth is a proportional cut.
  - The only variant that moves the answer is linking to the same-month-end list only, which gives 478 (500). That link is wrong on the files: an emergency admission removes the patient from the list by month end, so only 941 vs 1,325 spells link.
  - Distance from the rounding boundaries (375 and 425) is 17 or more in every sound variant.
- Supplementary answers: all 16 values reproduced exactly.
  - Hernia counts (T202, T204, T241; Fennick rows dropped where the same patient and operation has a Marlstead pathway added later; both sides of a double repair kept):
    - 368/161, 389/137, 418/105, 430/79.
    - Raw, un-deduplicated Fennick would be 192/160/132/90, so the policy section 6 move rule and the "one count for each operation" rule force the dedup.
  - 52+ weeks (364 days or more, measured from the ERS referral_received where a UBRN exists; the snapshot rtt_clock_start runs 0-129 days later and is wrong for 21,043 rows):
    - 739/461, 757/427, 792/389, 791/375.
    - A pathway added on the day its predecessor's TCI date fell (a cancelled admission, policy section 4; 49% of such admissions show no procedure in PAS) inherits the predecessor's clock.
    - A moved patient's Marlstead pathway inherits the Fennick pathway's clock, so a chain of relisting then move is followed.
    - Without relisting inheritance: 706/457, 716/421, 752/384, 751/371. With snapshot clocks only: 706/372 and so on.
  - Literal reading is unique: RTT-GS-03 ("referral that began the patient's wait") plus policy sections 4 and 6 license exactly the golden. One Marlstead value (2026-03-31 = 791 vs 790 without the move-chain) needs the full chain; this is derivable, not open.
- The file layout of the CSV baseline output is not given in the prompt. This is a minor format looseness, not a numeric fork.
- Verified absent: no shipped file contains the recommendation's modelling language, but the action is just a number. The linkage and rate method are left open, as intended.

**Files/Hygiene:** PASS.
- 11 files: parquet (1), csv (6), pdf (3), xlsx (2). Four formats.
- Largest file: pas_inpatient_episodes_2021_2026.csv, 54,764 rows.
- Realistic mess: dotted and suffixed ICD codes, mixed sex coding, mixed admission-method vocabularies (PAS numeric vs EPR text), Fennick PAS to EPR renumbering at 2023-04-17 (FPW to PW), missing UBRNs, ERS vs snapshot clock mismatches.
- Distractors: ecds_abdominal_pain_attendances (not used by the solution), theatre_case_log (not used).
- Dates are coherent: activity-line doc 7 Oct 2026, capacity plan 22 Oct 2026, data to 31 Oct 2026.
- No README or authoring text in the bundle.
- No exclusion-level finding.

**Stump power (Gate F):** Moderate to good. The trap that does the work is applying standard age/sex rates to all admissions (611 files 600), or a proportional-to-list scalar applied to everything, rather than separating listed patients (needs a PAS to snapshot link via the Fennick map and prior-month-end timing) and driving them by the planned list. The capacity plan and the activity-line consistency sentence signal that capacity matters, so some strong runs will adjust. Many will do so with a heuristic that lands near 400-450 or on 500, and the exposure model's 400 is separated from those by the data. The supplementary layer (clock reconstruction, relisting inheritance, move dedup) is hard and multi-step.

**Stumping type (Gate G):** `mechanism: forecasting` (with decomposition_attribution), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The reported figures (history, plan list) are fine, and the forecast turns on an exposure-based projection that the trailing age/sex rate does not pin. On clean data it would still stump.

**Three rules (Gate H):** `domain: pass`, `layers: pass`, `decisive_step: analytical`. Domain: NHS activity planning (age/sex-rate demand projection against a capacity-plan-driven waiting list); the swap test fails to preserve meaning, since hospital/list/exposure-per-patient-month is field-native. Layer 1: PAS to EPR migration, code and sex coding mess, UBRN vs snapshot clock, Fennick numbering. Layer 2: the demand model with a listed-patient exposure component. The easy route (age/sex rates on all spells, or a plain trend) yields 611 and files 600.

**Fix:** none.

## Round 2

# Determinism verdict, task173 (round 2)

**Verdict:** NOT_DETERMINISTIC (narrow). The main call and 15 of the 16 baseline figures are forced. One graded figure forks by one unit: Marlstead General, waits of 52 weeks or more, 2026-03-31, golden 790 against a literal-chain reading of 791. Taxonomy: underspecified_objective (a clock rule left open for transferred pathways).

**Disposition:** FIX_NOW. Pin the one chain in the generator, either by giving transfer pathway PW5028653 (patient M1729018, T241) its UBRN or by filing that a transferred pathway keeps its patient's original referral clock, and re-state 790 or 791 to match. The main call, the stump and the other 15 figures stay frozen. No model rerun is needed for the main call.

## Why
The 2027/28 NEL-GS-07 figure of 400 is forced from the files. Listed cholecystectomy patients are admitted at about 0.021 a patient-month, the capacity plan leaves 2,270 patient-months, and the other spells run flat at about 350 to 365 a year. Every reasonable variant lands in 380 to 416, which rounds to 400. The fork is in ask 2 of the baseline. Row PW5028653 at Marlstead (patient M1729018, T241, added 2026-02-21) has no UBRN, and its raw clock is 2025-04-02, which is the reset date of a re-listing. That re-listing (PW5024162, Fennick) inherits the 2023-06-28 ERS clock through the cancelled-admission link. The golden gives the Marlstead transfer row the reset clock (363 days at 2026-03-31, so not counted). The filed definition, "the date the Trust received the referral that began the patient's wait for the operation", points to the same 2023-06-28 referral (traced via PW5016524, UBRN 511524651763), so the row counts and the figure is 791. No filed rule says which reading applies to a transfer row that follows a re-listing.

## Evidence (recomputed from target/)
- **Spells.** Normalising codes, 3,280 first-episode emergency gallstone spells (K80, K81, K83.0, K85.1) fall in the files.
- **Listed link.** A spell is a listed patient's when a cholecystectomy pathway added before the admission is on the month-end list of the admission month or the month before. This gives 253, 246, 247 and 232 listed spells a year for 2022/23 to 2025/26.
- **Rate.** 1,138 listed spells over 54,006 patient-months (April 2022 to October 2026) is 0.02107, so the golden's 0.0211 reproduces. The plan sum is 330+200+170+180+170+180+180+180+190+160+170+160 = 2,270, which reproduces. 2,270 x 0.0211 = 47.8.
- **Other spells.** Age/sex rates for 2024/25 to 2026/27, applied to the 2027 projection, give 359.9 (about 360). The central expectation is 407.7, which reproduces.
- **Naive route.** All admissions at the same rates give 611.4, which reproduces.
- **Sensitivity.** All of these round to 400.

| Variation | Non-listed base | Listed term | Total |
|---|---|---|---|
| Base-year window (2022 to 2026 versions) | 357.8 to 364.7 | 47.8 | 405 to 413 |
| Out-of-area spells excluded | 341 to 348 | 47.8 | 389 to 396 |
| Estimates against projections for the population | 359.8 to 359.9 | 47.8 | about 408 |
| Rate window from April 2021, 2024 or 2025 | | 0.0206 to 0.0223 (46.8 to 50.7) | |
| Rate for patients waiting under 3 months | | 0.0172 (39) | about 399 |

- **Hygiene of the link.** The map covers every F-number, with no unmapped numbers.
- **Baseline figures.** All 16 golden values reproduced exactly. Method: ERS referral date where a UBRN is present; a blank-UBRN pathway opened on the day of a cancelled elective admission (PAS row with no procedure) inherits the predecessor's clock; count of 364 days or more; Fennick rows dropped at a snapshot when Marlstead holds the same patient and operation; same-site pairs kept.
  - **52 weeks or more.** Marlstead 739, 757, 792, 790. Fennick 461, 427, 389, 375.
  - **Hernia repairs.** Marlstead 368, 389, 418, 430. Fennick 161, 137, 105, 79.
- **Forks tested that hold.**
  - **Stale transfer rows.** Dropping by "Marlstead row exists" or by "Marlstead added later" gives the same counts (31, 23, 27, 11 rows). Cases where Fennick has one row and Marlstead two do not change the result.
  - **Same-site pairs.** The 65 same-site, same-UBRN T202 pairs are bilateral repairs and are kept. Policy section 6 and the "one count for each operation" line support both rules.
  - **Treated-but-listed rows.** The 8 such rows are bilateral second repairs, not stale rows.
- **Open fork.** The one-unit fork above is the only one that changes a figure. Other re-listing then transfer chains (M3040340, M4027229, M4772708) are 52 weeks or more at every quarter end under either reading.
- **Solution text gap.** Step 6 of the submission does not say the transfer-row drop also applies to the 52-week count, although the golden figures use it. Add the sentence.

## Files/Hygiene
PASS. There are 11 files in 4 formats: 5 CSV, 1 parquet, 3 PDF and 2 xlsx. The PAS extract carries realistic mess: mixed sex coding, mixed method codes, dirty ICD strings, and a Fennick PAS to EPR number change. The ECDS file, the theatre log and the mid-year estimates are the unused distractors. There is no authoring disclosure. The October 2026 snapshots postdate the 22 October plan approval only slightly, which is coherent with a setting at 31 October. No exclusion-level finding.

## Stump power
Gate F: moderate to good. A strong solver who runs age/sex rates on all admissions files 600 (611.4). The capacity plan's list fall, and the need to link spells to the list through the Fennick number map, are the analytical step. The listed share is only about 40 percent and the structure is visible, so some strong runs will find it. This is not a semantics trap.

## Stumping type
`mechanism: forecasting`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. Gate G passes: no reported number is overturned. The difficulty is a demand-driver decomposition into list-driven and background admissions, projected on a planned structural change.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Layer 1 is the Fennick renumbering, mixed codes and the preliminary snapshot layouts. Layer 2 is separating the list-driven admissions and projecting them on the planned list. The easy route (age/sex extrapolation of all admissions) gives 611.4, rounding to 600. The baseline asks are rule application and data semantics, which is allowed because they are not the main call.

## Fix
Input_files (generator, one row) or solution. Pin the transfer-row clock for PW5028653 and restate Marlstead 2026-03-31 52 weeks or more as 790 or 791 to match. Add the missing sentence on the transfer-row drop in the 52-week count to the solution steps.

## Round 1

# Verdict, task173 (determinism judge, round 1)

- **Verdict:** NOT_DETERMINISTIC. The main call (NEL-GS-07 = 400) is forced. Supplementary asks 2 and 3 (the RTT baseline CSV, 16 figures) rest on an unstated population rule.
- **Disposition:** SEND_BACK. The fix is a pin in the files or prompt on how a patient listed at both hospitals is counted. That changes what solvers see, so a rerun is needed.
- **Why:** Gate C/E, underspecified_objective. The golden removes Fennick rows when Marlstead later listed the same patient and operation (same UBRN) and gives re-listed pathways their predecessor's clock. No shipped sentence states either rule.
  - RTT-GS-02 says only "patients waiting at the hospital, one count for each operation".
  - The capacity plan says "patients stay on the list of the hospital that added them", which points at keeping both rows, or at keeping Fennick's.
  - Policy section 6 ("booked by the receiving hospital") is the only support for keeping Marlstead's row.
  - Three readings are defensible and give different answers (see Evidence).

## Evidence (recomputed from target/)

**Main call (NEL-GS-07)**
- Spells rebuilt from PAS: first episode, emergency methods (21/22/28 and "Emergency - ..."), primary diagnosis in K80, K81, K83.0 or K85.1 after stripping dots. This gives 3,280 spells over 2021-04 to 2026-10, about 600 a year and flat.
- Patients on the cholecystectomy list, linked after the Fennick number mapping and the 1/2 versus Male/Female sex recode:
  - Listed spells from 2022-04 to 2026-10: 1,138 over 54,006 patient-months, a rate of 0.02107 per patient-month. **Reproduced.**
  - 2,270 patient-months in the capacity plan, section 3 table (Apr 2027 to Mar 2028 summed). **Reproduced.**
  - 2,270 × 0.02107 = 47.8. **Reproduced.**
- The listed-patient rate is stable by year (0.019 to 0.023) and by time on the list (0.017 to 0.025), so a constant rate is a sound basis. This is the genuine driver.
- Non-listed 359.9: **not reproduced exactly.**
  - My age/sex-rate rebuilds on the 2022-based mid-2027 population give 343 to 370, depending on how out-of-area spells are handled (93 spells), whether Apr-Oct is annualised by 12/7 or a seasonal ratio of about 1.66, and which population years are used.
  - Non-listed spells run flat at 334 to 357 a year, so every defensible variant plus 47.8 lands at 390 to 418. All round to 400. The 425 boundary is not reached by any correct variant.
  - Only a double-count of out-of-area spells (about 383, total 432) crosses 425, and that is an error, not a reading.
- Competing answers:
  - 611.4, or 600 rounded, from age/sex rates on all admissions. This is the intended wrong route.
  - A regression of monthly counts on list size. This is unstable because the observed list stays between 800 and 1,000 and the plan implies about 190.
  - Neither survives as a licensed answer.
- Gate B: every decisive fact is in a shipped file. The plan definitions are in the activity-lines PDF, the list in the capacity-plan PDF table and the snapshot parquet, rates in the PAS file, and population in the projections xlsx.

**RTT baseline (CSV)**
- Rebuilding with ERS referral date where a UBRN is present, predecessor clock inheritance (same patient and operation, new pathway added on the predecessor's TCI date; 236 pairs found), 364-day threshold, Fennick FENH number mapping, and dropping Fennick rows that Marlstead listed later (31, 27, 30 and 13 rows at the four quarter ends) reproduces **all 16 golden figures**. Examples: 739/461 and 368/161 at 2025-06-30, 790/375 and 430/79 at 2026-03-31.
- Bilateral inguinal pairs (same patient, operation and UBRN, different operation dates) are kept as two operations at both hospitals, which is consistent with "one count for each operation".
- Forks (52 weeks or more, Marlstead / Fennick; hernia, Marlstead / Fennick; 2025-06-30 shown first, 2026-03-31 last):

| Reading | 52wk Jun-25 | 52wk Mar-26 | Hernia Jun-25 | Hernia Mar-26 |
|---|---|---|---|---|
| Golden: drop the Fennick duplicate | 739 / 461 | 790 / 375 | 368 / 161 | 430 / 79 |
| Drop the Marlstead duplicate | 708 / 492 | 780 / 386 | 337 / 192 | 419 / 90 |
| Count both rows | 739 / 492 | 790 / 386 | 368 / 192 | 430 / 90 |

- Clock-source forks:
  - Raw rtt_clock_start gives 706/372 at 2025-06-30. Fennick clocks were reset at the EPR move, and 144 Marlstead hernia pathways have clock starts 60 to 130 days after the ERS referral. The ERS date is pinned by "from referral" and RTT-GS-03, so this fork is closed.
  - ERS only, without predecessor inheritance, gives 706/457. Re-listed pathways have no UBRN. Inheritance is supported only by "the referral that began the pathway" and "national referral to treatment rules" (external). It is inferable but not stated.
- The Fennick figures are each affected by the which-hospital fork. The Marlstead figures are affected by the drop-Marlstead reading. So the 16 baseline figures are not uniquely forced.

## Files/Hygiene: PASS (not exclusion-level)
- 11 files; formats are parquet, csv (6), pdf (3), xlsx (2).
- Largest file is PAS at 54,764 rows. Distractors present: ECDS attendances, theatre case log, access policy, mid-year estimates.
- Messy but realistic: mixed sex coding, mixed dx formats (K40.9, K409, K40.90), mixed admission-method vocabularies, a Fennick PAS-to-EPR number map, and UBRNs missing on re-listed pathways.
- PDF and xlsx metadata are clean in-fiction. Dates are coherent: snapshots end 2026-10-31, the plan was approved 2026-10-22, and the activity-lines PDF is dated 2026-10-07. No authoring leakage found.

## Stump power
- The trap is likely to work. The easy route is age/sex rates on all emergency gallstone admissions, which gives 611 (600) and ignores the capacity-plan cut of the list to about a fifth.
- Getting to 400 needs patient-level linkage of PAS spells to the monthly lists, a per-patient-month rate and the planned patient-months. A strong model that skips the linkage files 600, and one that regresses on list size is unstable.
- Everything the solver is told is correct, so the stump is analytical.

## Stumping type
`mechanism: forecasting`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.
A driver-based forecast where the history is read correctly and the demographic trend does not pin the plan year. Gate G passes.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`.
- Domain: health-service activity planning with age/sex rates on population projections and a capacity-driven driver. Swap test: it would not read the same with another field's nouns.
- Layer 1: the mapped Fennick numbers, mixed codings, ERS versus PTL clocks, and the preliminary-to-EPR system change.
- Layer 2: separating the listed from the non-listed population and applying the planned list.
- Easy route: demographic rates on all admissions, giving 611 (600).

## Fix
Where: prompt and/or input_files. Two changes:
1. Add one sentence to the activity-lines PDF (RTT-GS-02) or the prompt saying a patient on both hospitals' lists for the same operation is counted once, at the receiving (later-listing) hospital. This closes the 16 baseline figures.
2. Confirm that a pathway re-listed on the day of its predecessor's cancellation keeps the original referral (RTT clock). This is the inheritance rule behind 33 Marlstead rows.

No change to the main call, the ladder or the goldens beyond a documented rule. Optionally, record the exact out-of-area handling behind 359.9 in the solution block, since it does not reproduce to the decimal. The rounded 400 is unaffected.
