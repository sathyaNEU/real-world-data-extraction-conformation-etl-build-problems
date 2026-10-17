# Verdict: task152 (Hadley Ranch Solar, 2027 forward volume at the one-year P90)

Scope: judged from the prompt and the 23 shipped files only. Every load-bearing value was recomputed with pandas from the bundle (scratch work under judge-task152/work/). The cross-batch reference check could not be run because other task folders are forbidden by the isolation rules. It is not claimed as clean.

- **Verdict:** DETERMINISTIC

- **Disposition:** APPROVE. No rerun is needed. Optional pins are listed under Fix and none is required.

- **Why:** Policy rev. 4 (sections 3.1, 4.1, 4.2, 4.4) files the estimand literally: net energy at the revenue meter, P50 less 1.2816 sample standard deviations over the 25 calendar years of the Clearfield record, rounded down to 1,000 MWh, built from the Oct 2025 to Sep 2026 base period. Read literally, the shipped files give 70,000 MWh. The only open item is the method for the plant's PR on the new modules. The data separates the candidates: the wash-reset record in the work orders isolates module wear (12%) from soiling and inverter losses, and Corvane's report gives the gain (13.6%) against an unexposed comparator. Every valid wear estimator I tried lands the same rounded volume. The asks (availability, over/under) reproduce exactly and their forks are closed by evidence in the files (see Evidence).

## Evidence (recomputed; all reproduced)

| Item | Golden | Recomputed | Source |
|---|---|---|---|
| Base-period PR (meter net / (H_POA x 40,320 kWp)) | 65.5% | 65.47% (60,154.3 MWh net, 2,278.9 kWh/m2) | hadley_scada_daily (PLANT-RM E_EXP, E_IMP, MET-01 H_POA), 365 days |
| Module wear since 2016, post-wash days, temperature-corrected | 12% | 12.16% (days 1 to 3, full-hours days; range 11.4 to 12.5% across window, median/mean, baseline-year and intercept variants) | WO CLN Completed dates, both SCADA files via crosswalk, KS-315P -0.42 %/degC |
| PR on new modules | 85% | 84.5% = 0.6547 / 0.88 x 1.136 on 37,324.8 kWp | Corvane FA-2026-114 (13.6%), scope docx |
| P50 / SD / P90 | 73,000 / 1,700 / 70,000 | 72,709 / 1,695 / 70,536 (local-year and UTC-year POA give the same rounded result) | Clearfield POA, policy 4.2 |
| Easy route A: base PR x 1.136, no wear | 62,000 | 62,072 | |
| Easy route B: restore whole DC-side decline | 73,000 | 73,543 | |
| Easy route C: 2016 PR x 1.136 | 76,000 | 76,812 | |
| Ask 4, 16 inverter availabilities | as listed | 16 of 16 match to 2 decimals (production hours = local hours with POA >= 50 W/m2; unavailable = zero-AC production hour; excluded = zero-AC hours inside the 4 unplanned district interruptions and the 2 owner-request stops) | inverter_hourly_ac_2025, met_station_hourly_2025, interruption PDF, WO OWN rows, O&M Schedule 4 |
| Ask 5, over/under 2016 to 2025 | +5,507 / +5,779 / +3,346 / +3,801 / -2,056 / +1,758 / +8,933 / +4,158 / +9,017 / +7,853 | all reproduce (district 0417 REC less DEL; legacy file shifted back one day because the total is stamped with the interval end; MDM latest version; sold volumes from confirmations with amendments and buy-backs: 69,000 / 68,000 / 68,000 / 65,600 / 66,000 / 56,500 / 52,900 / 54,000 / 52,200 / 54,000) | district legacy .txt, MDM csv, Westmark PDF |

### Literal-reading options where the text is silent, and what each gives

1. **Wear estimator.** Windows of 1 day, 1 to 2, 1 to 3, 2 to 3 or 1 to 5 days after a wash, a 2016-only or 2016 plus 2017 baseline, or a regression intercept give wear of 11.4 to 12.5%. P90 is 70,140 to 70,940, so the volume is 70,000 in every case. Fails: no temperature correction on a same-season comparison gives about 13.9% and 71,000. Treating the unexposed Table A as the plant's "new" state gives about 16% and 73,000. Both are analyst errors the datasheet and Corvane's wording rule out, not competing readings. The margin is thin on the upside: the P90 sits 464 MWh below 71,000.
2. **Wash date.** Completed is the wash day. The step in daily yield falls on the Completed date (checked for 2016, 2022 and 2025), so this is closed by the data.
3. **Soiling-phase refinement.** A purist could argue the new modules start clean on Dec 19, 2026, which would add about 1% and move P90 toward 71,000 or more. No filed text licenses this. Policy 4.4 fixes the base-period method, so the literal reading stays 70,000. I record it as a residual risk, not a fork.
4. **Net energy source (asks only).** SCADA PLANT-RM copies the district meter within about 1 MWh a year. That flips the nearest-MWh answer for 2016, 2020, 2022 and 2023, and the SCADA misses 596 MWh in 2018 (lost days Aug 14 to 16). Policy 3.1 and LGIA Exhibit C name the district's meter as the revenue meter, and the README says SCADA gives the registers "as the SCADA reads them", so the district series is the one. Closed, though a SCADA-only solver would miss several of the 10 values.
5. **Sold volumes (asks).** The blotter shows "quantities as traded" and omits the 2021 and 2024 amendments and nothing else. The confirmations carry the amended contract quantities (56,500 and 52,200). The prompt's "volume sold forward, net of any buy-backs" is best met by the amended quantity. Closed by the confirmations.
6. **Logger gaps in the hourly AC file (53, 42, 33 and 35 missing hours for blocks 1 to 4).** Counting the gap hours as delivering gives the golden. Dropping them from numerator and denominator shifts 14 of 16 values by 0.01 to 0.03. The evidence supports the golden: the register advances over every gap, the four inverters in a block gain nearly equally, and the event log has no fault inside any gap.
7. **F-217 AC GRID FAULT (143 zero-AC production hours not covered by a district interruption).** Excluding these would move every availability. The data separates them: the four district interruptions appear as simultaneous, unacknowledged F-217 on all 16 inverters, and the other 104 are single-unit, Tresco-acknowledged trips lasting hours. Schedule 4.2(a) needs an outage of the Utility's system, and none is recorded for these. Closed.
8. **S-020 REMOTE STOP.** Stops acknowledged by Tresco users count against the contractor. Only the two owner-request work orders (Feb 11 and Sep 29, 2025) are excluded. The WO text gives the clock times and the event log carries the stop on that single day. Hourly data confirm the unit was not down on the other days in the WO's created-to-completed span. Closed.

Gate A passes (all figures agree across the blocks, and provenance and attribution check out). Gate B passes: every decisive fact is in a shipped file (policy, Corvane, WO, O&M schedules, SCADA, district meter, confirmations). Gate C passes with the margin note in option 1. Gate D passes. Gate E passes: the prompt pins the committed call and every ask's unit and rounding.

## Files/Hygiene: PASS (minor notes)

- 23 files in 6 formats (csv, pdf, docx, xlsx, txt, md). Several files are large (about 127k, 139k and 219k rows).
- The files read as plausible operational artifacts: legacy fixed-width billing text, an MDM export with versioned re-loads, the original and replacement SCADA in different layouts, units and time zones, work orders in free text. No authoring or benchmark language, no stray solver-facing text.
- Mild notes, none exclusion-level:
  - The README is a long explanatory cover note, and the Corvane report carries a method footnote. Both read a little tidy.
  - The README says `ack_by` is a Tresco control-room user, but `swhitehead` appears only on the owner-request stops.
- Temporal coherence is fine: README Oct 6, 2026; Corvane issued Oct 2, 2026 (scope paper said "first week of October"); forwards marked Oct 5; district data to Dec 31, 2025.
- Licence and provenance records live in metadata.json, which I was not permitted to read.
- The cross-batch and public-data contamination checks were not run.

## Stump power

Moderate to high. The main call has three plausible easy routes that all file a different volume: 62,000 (ignores that Corvane's comparator is an unexposed module), 73,000 (restores the whole DC-side decline, including the soiling and inverter losses the replacement keeps) and 76,000 (first-year PR plus the gain). The Tresco repowering table (+9 to +18% for other plants) is a usable distractor. Getting 70,000 needs the wash-reset isolation of module wear plus temperature correction.

The asks add heavy extra load: 16 availabilities to two decimals and 10 over/under figures, with timezone, versioning, amendment and logger-gap handling. Too-easy signals are mild: the scope paper lists what stays, and Schedule 2 states the once-a-year wash. Neither supplies the 12% itself.

## Stumping type

`mechanism: decomposition_attribution (with method selection)`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`

The reported numbers are all correct: Corvane's 13.6%, the base-year PR and the district energy. The difficulty is attributing the historical decline to module wear, soiling and inverter losses, and applying a correct gain to the right base. On clean data it would still stump, so Gate G passes and banned_stumping_type does not apply.

## Three rules

`domain: pass`, `layers: pass`, `decisive_step: analytical`

- **H1 (swap test).** P50/P90 energy-yield assessment, performance ratio, degradation separation and a P90 hedge volume are core PV yield work. Swapping in another field's nouns breaks the task.
- **H2.** Layer 1 is the UTC-versus-local day boundaries, the kWh-versus-MWh SCADA migration with the B2-INV3 to INV3R crosswalk, the district legacy-versus-MDM versions, amended confirmations and the logger gaps. Layer 2 is separating module wear from soiling and inverter loss using the wash cycle, temperature correction, and applying the unexposed-comparator gain to the right base.
- **H3.** The deciding step is the decomposition and the choice of the right estimand for "what the replacement removes". A capable analyst who cleaned the data and read every document correctly would still easily file 62,000, 73,000 or 76,000, so H3 passes as analytical.

## Fix

- **Where:** none required (solution and files stand).
- **Optional pins, no rerun:**
  - State in the availability ask or the data notes that the district meter series is the source for the over/under.
  - If the author wants the 71,000 upside closed, a one-line note in policy 4.4 that no wash-phase adjustment is made would do it.
