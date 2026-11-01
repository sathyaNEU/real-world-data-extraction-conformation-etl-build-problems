# Determinism check, task123 (pass 2, the re-judge after the FIX_NOW)

Isolated judge thread on a fresh unzip of target.zip (22 files, the HHAP file carrying the enrolling account) and the graded blocks of submission.md; run 2026-10-12. The thread's verdict follows unchanged.

# Determinism verdict, NHAG 2026-27 county split

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. No repair is needed and no model rerun is required. Two optional wording pins (rounding order, the Northline completion evidence) are listed under Fix.

**Why:** The prompt asks for twelve awards in proportion to each county's January 2026 residential therms. The shipped Standard (Ed3) pins every convention: gas-day months (2.3), service periods (2.4), billed therms (2.5), the premise county (2.6), unrounded shares (3.3), and the indicator definitions in Appendix B with premise-county counting (4.2). Executed word for word, the Standard gives the committed awards. Day-proration of each bill is contradicted by the shipped data. The MDMS shows 2.4 times the daily use in the 19 to 31 January cold snap as in 1 to 18 January, and Kestrel Valley's own cycle bills fit that shape better than flat proration (cross-cycle CV 4.2 percent against 12.0 percent). Every committed answer reproduced.

## Evidence (recomputed from target/ only)

**Main call, therms and awards.**
- Method: effective Kestrel Valley (KVG) bills are BILL not cancelled plus RBIL. Northbank (NNG) bills are parsed from the fixed-width layout, with service period = day after PREV-READ-DT through CURR-READ-DT. Pine Harbor (PHE) bills are used as billed, with CALENDAR bills falling wholly in their month.
- Each cycle bill is spread over its gas days by the mean usage_ccf per reporting meter, then summed by the county of PREMISE in service_points.
- Coverage: 47,228 premises have 31 Jan days covered with no overlap. COM and MFR premises have no residential bills. All premises map to a county.
- Region total: 10,260,670 therms, which rounds to the 10,260,000 stated.
- County therms, rounded to the nearest 10,000: Ashwell 940, Brennock 1,310, Carrow 500, Dellmoor 1,180, Evanshade 680 (677,510), Farrish 930, Glenhollow 480, Halvern 1,010, Keswin 620, Lorrance 1,050, Merrion 720, Tillery 840 (all in thousands). All reproduce.
- Awards on unrounded shares, rounded to $5,000: Ashwell 1,710,000, Brennock 2,380,000, Carrow 910,000, Dellmoor 2,145,000, Evanshade 1,230,000, Farrish 1,685,000, Glenhollow 875,000, Halvern 1,840,000, Keswin 1,125,000, Lorrance 1,905,000, Merrion 1,310,000, Tillery 1,525,000. The sum is 18,640,000 and all reproduce.
- Critical components: 10,260,000, Brennock 1,310,000 and Tillery 840,000 all reproduce. The 2.4 times cold-snap ratio reproduces (2.423 overall, 2.42 in each of the three PHE counties).
- Shape variants, all with the same twelve awards: validated reads only, median instead of mean, per-meter-normalised, and summed instead of averaged.
- Alternatives that fail:
  - Flat day-proration (11.19 million therms regionally, against 10.26 million): Brennock 2,465,000, Dellmoor 2,055,000, Lorrance 1,850,000, Tillery 1,435,000 and others. It conflicts with the observed daily shape.
  - Shares from therms rounded first: five awards move by $5,000 (Evanshade, Farrish, Glenhollow, Halvern, Lorrance). Standard 3.3 closes this: allocations use unrounded values.
- PHE CALENDAR bills equal round(MDMS CCF x 1.034) (max difference 0.5). The E-read bills (KVG) do not touch January.

**Residential disconnections for nonpayment completed in January (all reproduce).**
- Kestrel Valley: 41 OFF/NP/COMP orders completed in January, plus 13 Northline jobs with no matching service order. The union is 54, each disconnection once by account and day.
  - Ashwell 13, Brennock 13, Carrow 8, Dellmoor 12, Evanshade 8. Tillery has none from Kestrel Valley.
  - Orders alone would give 10, 9, 7, 9, 6.
- Northbank: DNP with result C and crew COMPLETED_AT in January gives Farrish 9, Glenhollow 8, Halvern 14, Keswin 5. Scheduled ACT_DATE would give 12, 11, 18, 14, but Appendix B says "completed in the month" and the notes define COMPLETED_AT as the crew close.
- Pine Harbor: 19 Completed Collections Shutoff work orders plus 17 NP VALVE_CLOSE events, with no overlap. Lorrance 13, Merrion 11, Tillery 12. The Eastern-date conversion moves no event across a month boundary.

**Residential accounts on a low-income payment plan on 31 January (all reproduce).**
- Kestrel Valley WCP: effective on or before 31 January and END_DT blank or on or after it, counted at the premise county via the billing extract. Ashwell 217, Brennock 384, Carrow 141, Dellmoor 282, Evanshade 211, Tillery 24.
  - SERVICE_COUNTY on the enrollment disagrees with the premise county on 139 enrollments. Standard 4.2 and 2.6 close this in favour of the premise county.
- Northbank HHAP: 821 flagged premises, of which 798 still have the enrolling account on 31 January. Farrish 198, Glenhollow 154, Halvern 270, Keswin 176. Counting flagged premises regardless would give 208, 155, 277, 181 (23 premises changed account).
- Pine Harbor IBPP: 1,094 arrangements in force, of which 787 are on accounts linked to a meter on 31 January. Lorrance 344, Merrion 215, Tillery 228, so Tillery is 228 + 24 = 252. The other 307 are old accounts whose links ended in October 2025 at the AMI exchange, with the plan left ACTIVE. Counting them by their last premise would give 506, 298, 290 for Lorrance, Merrion and Tillery. 464 of the new 88xxxxxxxx accounts carry their own IBPP, so the old rows are stale duplicates.

**Residual forks.** Neither flips a main award.
1. Applying the PHE AMI daily shape to Kestrel Valley and Northbank premises is an inference, not a filed rule. Standard 2.3 requires gas used on the January gas days. The shipped data separate the candidates: the MDMS shape, and the KVG cycle-bill fit above. No competing method survives.
2. The 13 Kestrel Valley disconnections that appear only in the Northline job report assume that a "job worked" on site is a completed disconnection. The report has no status column. Several of the 13 are followed by a reconnection order or a zero-therm final bill, which supports the reading, but the report does not state completion. This affects supplementary indicators for Ashwell, Brennock, Carrow, Dellmoor and Evanshade (orders alone: 10, 9, 7, 9, 6). It is a small risk and is not forced by any shipped sentence.
3. In the NNG and PHE low-income counts, the exclusion of enrolments whose account no longer holds the premise is not stated in a sentence. The data make it the only coherent reading, as shown above.

## Files/Hygiene

**PASS.**
- 22 files in 8 formats: csv, txt (fixed width), xlsx, parquet, json, docx, pdf and eml. Row and record counts match export_manifest_2026-04-20.csv. The largest file is KVG_RES_BILLING_EXTRACT (139,768 rows).
- Distractors present and unused by the solution: KVG_GS_BILLING_EXTRACT, NNG_READ_SCHEDULE_2026-27, PHE_PAYMENT_ARRANGEMENTS BUDGET and DPA rows, GS and MFR premises.
- Realism: the files read as system exports. Kestrel Valley uses US dates, Northbank a COBOL fixed-width layout, and Pine Harbor ISO dates and JSON. The contractor report and email thread are plausible. I found no authoring-process leakage, no synthetic or benchmark disclosure, and no dates after the 20 April 2026 setting.
- Temporal coherence holds. The service-order pull of 3 February predates the Northline report of 9 February, which explains the 13 missing jobs.
- No public-data contamination: this is a fictional multi-utility region. I made no license or provenance check beyond reading the files.

## Stump power

Moderate to good. The default path is to prorate each bill flat over its days, or to use the bills read in January. Both produce confident wrong awards (Brennock 2,465,000 against 2,380,000, Tillery 1,435,000 against 1,525,000, six or more awards off by $50,000 or more). The prompt does not hint at weather-shaped calendarisation, and the Standard states only the target ("gas used on those gas days"). A strong model that cleans the data and reads every definition correctly can still land on the flat reading. The supplementary traps are the Northline union, the stale-account enrolments, premise county against enrolment county, and completion against scheduled date. Each is plausible for a strong model to miss, though not individually decisive for the main call.

## Stumping type

`mechanism: method_or_model_selection` (calendarisation of cycle bills to gas-day months), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.

No reported figure is wrong. The bills are correct, and the difficulty is in estimating gas-day use within them, so the task would still stump on clean data. The pass is on the FINE-numbers method-selection shape.

## Three rules

`domain: pass`, `layers: pass`, `decisive_step: analytical`.

- **Swap test.** The task passes: replacing the gas nouns with another field's nouns makes the intra-bill daily-load weighting meaningless. Calendar-month allocation of billed energy (unbilled/calendarisation) is utility-analytics work.
- **Layer 1.** Messy extracts: cancel and rebill, a COBOL fixed-width layout with register rollover, cycle against calendar billing at AMI exchange, UTC against Eastern, a contractor report and several account histories.
- **Layer 2.** Allocating billed use to gas days with the observed daily load shape.
- **Easy route.** A strong analyst who reads everything correctly prorates flat by days. That gives Brennock 2,465,000, Dellmoor 2,055,000 and Tillery 1,435,000, among others.

## Fix

**Where:** none required for determinism.

**Optional pins, no model rerun needed:**
- Add "from unrounded county values" to the prompt or note. The Standard already says it in 3.3, and rounding first moves five awards.
- Where the Northline-only disconnections are discussed, state that the report lists completed jobs, so that the union is licensed in the files.


## Disposition taken

APPROVE. Of the two optional pins, the contractor report's header now reads that it lists completed jobs; rounding from unrounded county values is already the standard's 3.3. Identifiers were reissued in creation order and two documents trimmed on the leak reader's realism notes; no figure moved (verify and checks green, two byte-identical builds).

After this pass, five counties' displayed names changed (Carrow to Sauvain, Dellmoor to Rennick, Evanshade to Ottercreek, Glenhollow to Wynnell, Lorrance to Pellow) on the leak reader's realism note; the simulation keeps its keys and every figure is unchanged.
