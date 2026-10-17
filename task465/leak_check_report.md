# leak check, task465

**Verdict: REVIEW.** 15 files read, 42 golden figures and 6 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: surveys, survey, shares, traits, household, equipment, association, product, decisive, method, estimates, utility, county, independence, architecture, sample, measured, health, inside, default, fusion, conditional, matching, together, screens

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `hema_screening_pilot_report_2025.pdf`: golden figure 800 appears: ...Addresses and contact The billing system drew 10,800 active residential service addresses at random in...
- **REVIEW** `hema_screening_pilot_report_2025.pdf`: golden figure 600 appears: ...resses at random in each of the two divisions, 21,600 in all. Each address was mailed the screener on M...

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `callowmere_hema_plan_2027_draft.pdf`: 5 of 25 stump-paragraph terms appear (survey, household, equipment, utility, health); read whether the document names the move
- **REVIEW** `heas_2025_technical_notes.pdf`: 6 of 25 stump-paragraph terms appear (survey, household, estimates, utility, county, sample); read whether the document names the move
- **REVIEW** `hema_screening_pilot_report_2025.pdf`: 3 of 25 stump-paragraph terms appear (household, equipment, screens); read whether the document names the move

## 6 ranking artifacts (REVIEW 2, INFO 1)
- **REVIEW** `hema_screening_pilot_report_2025.pdf`: names 3 of 6 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `medical_baseline_enrolment_2026.csv`: names 5 of 6 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `callowmere_service_divisions.csv`: names 5 of 6 answer-set candidates; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read

### Round 1 (pack before the stage-4 fix pass)

1. Decisive step. The nearest filed text is the plan's section 5: "In each division and band the table's households equal the State Demographer's estimate for July 1, 2025; its share of households whose annual home energy costs exceed 6 per cent of income equals the weighted estimate of the State Energy Office's Household Energy Affordability Survey 2025; and its share of households in which someone relies on electrically powered medical equipment equals the weighted estimate of the State Department of Health's State Health Survey 2025." Together with section 4 ("one caseworker for every 400 eligible households in a service division, or part of that number") it tells the solver to build the table from the county x band estimates. It does not say how the two shares combine (product of two marginal shares vs a joint share), nor that the screening pilot is not the basis. No sentence announces a pitfall.

2. No file ranks or scores the divisions on caseworkers or eligible households. heat_vulnerability_index_county_2025.csv ranks counties on heat vulnerability and the enrolment/work-order files count baseline households, but none gives eligible households or caseworkers per division. The pilot report gives raw return counts for North Metro and South Metro only.

3. Nothing is purely analyst-help. data_dictionary.csv and file_register.csv are the closest (a folder-level dictionary and register with a "Dates are Central Time" line) but plausible in a real shared folder. callowmere_service_divisions.csv (called the "division register" in the plan) is a legitimate source. The pilot, HVI, applications, enrolment and work-order files are distractors, not helpers.

4. No figure or name reads as the answer. The only answer-shaped items are the pilot report's "3,478 complete" and the plan's budget ($78,400 per caseworker), which are context.

5. Literal sentences and result.
- "A household is eligible for HEMA when (a) its household income is under $50,000, (b) its annual home energy costs (electricity, natural gas and other home heating fuels) exceed 6 per cent of its household income, and (c) someone who lives in the home relies on electrically powered medical equipment at home."
- "one caseworker for every 400 eligible households in a service division, or part of that number. The service divisions are the nine divisions of the company's division register." (ceiling of eligible/400 per division)
- Section 5 (quoted in Q1): households per division-band = demographer estimate; burden share = weighted HEAS estimate (WT_FINAL, annual electricity = 12 x ELEC_AMT where ELEC_BASIS is M, plus GAS_AMT and OTHER_AMT, over HHINC); equipment share = weighted SHS estimate (HH_WT, excluding 7/9, INCCAT 1-3 = under $25k, 4-5 = $25k-49,999).
- Division register has 30 counties in 9 divisions; the 8 demographer counties not in it (021, 035, 043, 047, 063, 067, 071, 075) drop out.
My literal computation (eligible = households x burden share x equipment share, per county and band, summed to division): Central 930, High Plains 865, Lakeshore 663, North Metro 1,270, Northern 519, River Valley 954, South Metro 843, Southern Hills 723, Southwest 1,525; total about 8,290 households. Caseworkers (ceiling of /400): 3, 3, 2, 4, 2, 3, 3, 2, 4 = 26. This treats the two shares as independent (product), which the plan's annex wording implies but does not state; not checked for reading sensitivity near the 400 boundaries. Smallest cell samples: 13 HEAS and 22 SHS interviews in a county-band.

6. What decides it. Mostly following the stated procedure with correct reading of fields: the ELEC_BASIS M x12 annualisation, income-band mapping between HEAS (dollars) and SHS (INCCAT), excluding don't know/refused, using WT_FINAL not WT_BASE, mapping counties via the register. The sentence that decides it is plan section 5 ("its share of households whose annual home energy costs exceed 6 per cent ... equals the weighted estimate ..."). The one analytical-looking judgement is combining the two marginal shares (independence) since no file provides a joint; the pilot (metro only, mail/phone, duplicates by ADDRESS_KEY, income-ended screens) tempts a shortcut but the plan says what the table must equal, so the call is rule application and field semantics rather than something a careful solver could get wrong by method. Nothing looks planted except the pilot as an evident decoy and the pilot's duplicate address keys.

###### Realism tells
- file_register.csv: RECORDS for the three files tie out exactly to the PDF/CSV counts (9,043 pilot rows = report total; 3,850 work orders; 38,827 spells); fine, but the register adds a "(folder),(dates)" row that reads as written for the solver.
- data_dictionary.csv: covers only some files and explains answer-relevant details (ELEC_BASIS, STATUS meanings); dictionary dated 2026-11-16 after the plan (2026-11-12) and division register 2026-11-02, plausible.
- Plan PDF: section 5 reads like a specification of the computation ("equals the weighted estimate of...") rather than a utility filing; a real plan would not describe a table as a set of equalities. "Part of that number" staffing phrasing is natural.
- Technical notes: "Respondents who could not give a 12-month amount gave a typical monthly bill instead" flags the trap-like field in prose; very explicit.
- Demographer workbook: county totals for Glasswold 38,000, Pinewold 24,000, Marlowcombe 52,000, Thornwold 61,000, Umberholme 47,000, Wendlecombe 33,000, Willowcombe 44,000 are round thousands while others are arbitrary tens; income bands for those counties are exact fractions (e.g. Glasswold 8,360 = 22%, 10,260 = 27%, 9,500 = 25%, 9,880 = 26%), which reads synthetic. The 8 counties excluded from the register are exactly these round ones.
- Unrealistic county names (Alderwold, Brackmere, Quarrowby etc. all -wold/-holme/-thorpe/-combe/-mere endings) and county FIPS skipping odd numbers 001..075 in a tidy sequence; HVI has Quillholme at exactly 100.0 and Ivythorpe 0.0 (min-max scaled), and the 38 counties sum to a state of 1,334,980.
- Pilot report: counts are tidy (10,800 per division, 21,600 total; mail+phone returns) and the report states 84 partials "27/13/33/11"; a pilot with ~42% return from a random draw with first-person narration reads fine, but "3,478 complete" ties exactly to the file.
- HEAS: HHINC rounded to nearest $100 as stated; WT_BASE/WT_FINAL four-decimal floats; RESPID H25 + step-of-3 numbering (H2510003, H2510006...) and SHS SEQNO stepping by 7, ENROL_ID by 3, WORK_ORDER by 3: regular increments look generated.
- medical_baseline_enrolment: first rows all START_DATE 2007-12-16 (sorted by date with a floor date), account numbers ascending 61000001xx; spells since 2020 file title but starts back to 2007.
- Work orders: COMPLETED_UTC timestamps like 23:43Z with SCHEDULED same date (a Central evening visit would be next UTC day); the register's Central-time note points at it.

#### Rulings (main thread)

- Q1, plan section 5 quoted as the nearest sentence: it names no pitfall (the reader says so), but it read as a recipe
  ("equals the weighted estimate"). Fixed: the annex now states the Commission's consistency check (the table
  reproduces the official household estimate and the two surveys' estimates of each share), a WHAT, never a method.
- Q2 and Q4: nothing ranks the divisions; the pilot report's complete count and the plan's budget are context.
  Harmless.
- Q3, the dictionary row "(folder), (dates)": fixed, row removed; the booked date's own description carries the
  company's Central Time day.
- Q5, the literal result 26 by the product of the two shares: the reader's own computation is the default path (the
  analyst test), not a filed rule; the annex fixes only what the table must agree with, and the product is the
  independence assumption the pilot rejects inside both bands. Kept as the stump; the annex reworded (Q1).
- Q6, "rule application and field semantics": the reader executed every filed rule and read every field and still
  filed 26, so the step that decides the call is the analysis of how the two traits combine (the judge's Gate H:
  `decisive_step: analytical`). The pilot is the utility's own screener test and carries no planted figure.
- Realism tells fixed in the generator: record numbers in regular steps (now increasing with the gaps a system leaves);
  the enrolment's floor start date (pre-2020 starts now thin out smoothly to 2003); the heat vulnerability index
  min-max scaled to exactly 0 and 100 (now a standard score, mean 50, standard deviation 15); round-thousand county
  totals and exact-fraction bands for the counties outside the territory (the cells the staffing never reads now carry
  their own estimation error); the dictionary now covers the index's and the applications' county columns and the
  estimates sheet. Kept: county FIPS codes in odd steps (the federal coding), the pilot's 10,800 addresses a division
  (its sample design), the work orders' UTC stamps beside Central booked dates (Ask B's hazard H2), the monthly-bill
  sentence in the technical notes (the survey's own documentation of ELEC_BASIS, Layer 1, neutral on the call).

### Round 2 (after the fix pass and the pilot redraw)

1.
Plan section 5 (callowmere_hema_plan_2027_draft.pdf) states the method: "in each division and band the table reproduces the State Demographer's household estimate for July 1, 2025, the State Energy Office's Household Energy Affordability Survey 2025 estimate of the share of households whose annual home energy costs exceed 6 per cent of income, and the State Department of Health's State Health Survey 2025 estimate of the share of households in which someone relies on electrically powered medical equipment." Section 4 gives the divisor: "one caseworker for every 400 eligible households in a service division, or part of that number." Section 2 gives the three eligibility tests. No sentence says the decisive step outright. The cell-level combination (households x burden share x equipment share) is the plan's own filed method.

2.
None. No file ranks or scores the nine divisions on caseworkers or eligible households. The HVI file ranks counties on heat vulnerability, which is a different quantity. The pilot report gives screen returns for two divisions only.

3.
data_dictionary.csv and file_register.csv are the closest: they are tidy folder indexes, but a real shared folder can have them. Nothing else exists only for the analyst. heat_vulnerability_index_county_2025.csv and energy_assistance_applications_2025.csv look like decoys. They are not used for the answer, and a real folder could hold them.

4.
None reads as the answer. Plan figures ($78,400 per caseworker, $1,150 per battery, $236,000 outreach, 400 per caseworker) are context. The pilot report returns (9,033 screens, 3,315 complete) read as a ready-made rate source, but they cover two divisions only.

5.
Quoted: Plan s.2, "income is under $50,000 ... annual home energy costs (electricity, natural gas and other home heating fuels) exceed 6 per cent of its household income ... someone who lives in the home relies on electrically powered medical equipment". Plan s.4, "one caseworker for every 400 eligible households in a service division, or part of that number. The service divisions are the nine divisions of the company's division register." Plan s.5, the sentence in 1 (cell = division x band, product of the three sources). HEAS notes s.4, annual cost = 12 x ELEC_AMT when ELEC_BASIS is M, plus GAS_AMT plus OTHER_AMT. HEAS s.3 and the SHS notes say the weights are calibrated to the Demographer's county-by-band estimates. SHS notes exclude don't know and refused from percentages.

Literal computation, as I ran it: Demographer households summed over each division's register counties for the two bands. Pooled WT_FINAL share with annual cost over 6% of HHINC per division and band. Pooled HH_WT share answering Yes among Yes and No per division and band (INCCAT 1-3 and 4-5). Product per cell, summed over the two bands, then ceiling of eligible/400. The shares are pooled across counties in a division.

| Division | Eligible | Rounded to 100 | Caseworkers |
|---|---|---|---|
| Central | 910 | 900 | 3 |
| High Plains | 858 | 900 | 3 |
| Lakeshore | 669 | 700 | 2 |
| North Metro | 1,266 | 1,300 | 4 |
| Northern | 523 | 500 | 2 |
| River Valley | 923 | 900 | 3 |
| South Metro | 972 | 1,000 | 3 |
| Southern Hills | 572 | 600 | 2 |
| Southwest | 1,507 | 1,500 | 4 |
| Total | 8,200 | | 26 |

Caseworkers are the same whether the ceiling is taken on the exact or the rounded eligible count. Two points are not settled by the text. The pooling level of the shares (division versus county) is not filed. The cell product assumes independence of the two shares, and the plan fixes that by saying the table "reproduces" the three estimates.

6.
Mainly following a stated rule or procedure, with some data semantics. The plan's s.5 prescribes the cell product, s.4 prescribes the staffing ratio, and the HEAS notes prescribe the annual cost. The reading-the-data parts are ELEC_BASIS M x12, excluding don't-know and refused, the INCCAT-to-band mapping, and the division register's nine divisions with unserved counties dropped. The analytical element is weaker: the choice to apply shares by division and band rather than pooling, and the pilot (two divisions, mail and phone, duplicates, Ended-income) as a tempting alternative source. A solver who reads s.5 literally reaches the answer with little judgement. No planted defect is decisive. The pilot report and file act as a rival rate source, but the plan names the sources.

###### Realism tells

- data_dictionary.csv and file_register.csv: every file listed with a CURRENT_AS_OF date, and the dictionary is "for this folder" and dated 2026-11-16, after the stated end-October 2026 data date. The register lists the plan as dated 2026-11-12, though the prompt speaks in the past tense of end October 2026. The folder is tidy in a way a real shared folder rarely is.
- file_register.csv: record counts exactly match files (9000, 12000, 9033, 38848, 3917, 30). The division register says 30 rows, but the register has no row for the 8 other counties in the Demographer file.
- household_estimates xlsx: all figures rounded to ten and region rows sum exactly. This is plausible for a published release. The 38 counties appear against only 30 in the division register, with no note on why.
- heas_2025_household_puf.csv: round sample numbers (exactly 9,000 completes, 12,000 in the SHS), and HHINC rounded to $100 with a top-code at $248,000, an unusual number.
- hema_screening_pilot_2025.csv and report: 10,800 addresses per division exactly and 21,600 in all. Return counts reconcile to the file (9,033). The pilot tables are neat. The screens' ELEC_12M and OTHER_FUELS_12M differ in definition from HEAS, which is convenient as a trap.
- plan s.5 reads like a method statement for the analyst: it spells out that the table "reproduces" three named official estimates, which a real filing would not narrate.
- plan s.1 to s.7: the budget lines ($78,400, $1,150, $236,000) are not used by the main question, and the plan is full of tidy dates (Dec 1 filing, Apr 1 staffing).
- medical_baseline_enrolment_2026.csv: early start dates are 2003-01-15, 2003-01-16, 2003-01-16, a floor-like run in the first rows (the sort order is by start date, so this may be benign). Account numbers run 61xxxxxxxx, a regular prefix. Row count is 38,848, but the file register says "active since January 1, 2020" while the first rows start in 2003 with end dates in 2022 and 2024. The 2003 start dates sit oddly with a stated 2020 cut.
- battery_placement_work_orders_2026.csv: WO numbers step by 13 (410004, 410017, 410030), a regular sequence. Rows begin in 2025-12 while the file name says 2026. The data dictionary says "Central Time" in SCHEDULED and UTC in COMPLETED_UTC, which is tidy for a time-zone trap.
- hema_screening_pilot_2025.csv: the first rows are all 2025-03-10 and all Ended - income, a floor date. SCREEN_IDs run S25-100009, 100022, 100024 in sorted order.
- heat_vulnerability_index_county_2025.csv: 38 counties, so it covers more counties than the division register. Rank and score are given. Plausible, but the file is a clear unused distractor.
- energy_assistance_applications_2025.csv: 456 rows is 38 counties x 12 months, a complete rectangular panel with no gaps.

#### Rulings (main thread)

- Q1 and Q5: the annex ("the table reproduces" the household estimate and the two surveys' estimates of each share) is
  quoted as the filed method, yet the reader's own answer to Q5 says the text files neither the pooling level nor the
  independence of the two shares. The annex fixes what the table must agree with; the product and the fused table both
  agree with it, so the literal text leaves the joint open and the reader's 26 is the default path, the analyst test's
  named wrong answer. No main-call fork: the re-judge recomputed 38 from the pack and every both-shares fusion lands
  on it. The pooling level is now pinned as a WHAT (each division and band estimated as a whole, SF15).
- Q2, Q3, Q4: no ranking file, the dictionary and register a real folder holds, nothing reads as the answer. Harmless.
- Q6, "mainly following a stated rule, with some data semantics": ruled the stump at work, not rule application; the
  step the reader calls a rule is the independence assumption the reader also says the text does not file. The judge's
  Gate H (passes 2 and 3) reads the decisive step as analytical.
- Realism tells, each harmless: the registers dated after the extracts (the folder assembled for the plan in
  November); record counts that tie (a register that ties to its files); 38 counties in the state files against 30 in
  the register (the territory, Layer 1); the work orders' first three numbers 13 apart (3,917 orders with gaps of 1 to
  214); the first day of mail returns heading the pilot file; "active since January 1, 2020" (spells on the rate at
  any time since then, some begun earlier); the applications' full county-by-month panel (a state agency's zero-filled
  report); the budget lines (context).

### Round 3 (after the estimation-domain pin in the plan's annex)

1. No file or sentence names the decisive step. The plan (callowmere_hema_plan_2027_draft.pdf, section 5) says the staffing "rests on the number of eligible households in each service division and eligible income band ... each estimated for the division and band as a whole", and that the table reproduces the Demographer's household estimate, the HEAS share with costs over 6 per cent of income and the SHS share with medical equipment. It says nothing about how the two shares combine into a joint "eligible" count. The closest hint is that the pilot (hema_screening_pilot_2025.csv, North/South Metro only) holds both items on the same household, but nothing says to use it.

2. None. No file ranks or scores the nine divisions on caseworkers or eligible households. heat_vulnerability_index_county_2025.csv ranks counties on a heat index, which is not the quantity. The medical baseline file and the battery work orders give counts by division, but these are enrolment and activity counts, not eligibility.

3. data_dictionary.csv and file_register.csv exist only to help the analyst (a field-by-field gloss and a provenance list across three agencies). A real shared folder would rarely hold a single dictionary mixing State Energy Office, Health Department and company files. The plan's section 5 is also unusually explanatory about the Commission's check, but that is plausible in a filing.

4. Nothing reads as the answer. The plan's "one caseworker for every 400 eligible households ... or part of that number" is a rule, not a result. The pilot report's table (9,033 returns, 3,315 complete) is context.

5. Sentences that fix the computation:
- "one caseworker for every 400 eligible households in a service division, or part of that number" fixes caseworkers = ceiling(eligible households / 400) per division.
- "A household is eligible for HEMA when (a) its household income is under $50,000, (b) its annual home energy costs (electricity, natural gas and other home heating fuels) exceed 6 per cent of its household income, and (c) someone ... relies on electrically powered medical equipment" fixes the eligibility definition.
- Section 5 ("by service division and eligible income band (under $25,000; $25,000 to $49,999) in 2025 ... each estimated for the division and band as a whole ... reproduces the State Demographer's household estimate ..., the HEAS share ..., and the SHS share ...") fixes the cells (nine divisions by two bands), the three inputs and the pooling of each share at division-and-band level, not county by county.
- The technical notes fix the annual electricity cost (M x 12; energy cost = electricity + gas + other) and the SHS codebook fixes the don't-know and refused exclusion and the INCCAT 1-3 / 4-5 band mapping.
- The prompt fixes rounding eligible households to the nearest hundred.

My literal computation: households (Demographer, summed over each division's counties per the register) x weighted HEAS share with cost > 6% of income (WT_FINAL, pooled over the division's counties within the band) x weighted SHS share Yes among Yes/No (HH_WT, pooled). I multiplied the two shares as if independent. The result is per division: band <25k households, burden share, med share, eligible; then the 25-49k band; then the total.
- Central: 17,060 x .5467 x .0731 = 681; 22,130 x .2167 x .0477 = 229; total 910 (900 rounded), 3 caseworkers.
- High Plains: 706.6 + 151.4 = 858 (900), 3.
- Lakeshore: 511.6 + 157.5 = 669 (700), 2.
- North Metro: 835.6 + 430.5 = 1,266 (1,300), 4.
- Northern: 427.3 + 95.3 = 523 (500), 2.
- River Valley: 685.6 + 237.6 = 923 (900), 3.
- South Metro: 718.5 + 253.2 = 972 (1,000), 3.
- Southern Hills: 424.2 + 147.5 = 572 (600), 2.
- Southwest: 1,141.1 + 366.1 = 1,507 (1,500), 4.
- Total caseworkers 26 under the independence product (county-by-county summing gives the same 26 here).

What the text fixes: the caseload ratio and ceiling, the eligibility test, the cost definition and the M x 12 handling, the bands, the division-and-band pooling, the exclusion of DK/refused, and the nearest-hundred rounding. What it leaves to me: how the burden share and the medical-equipment share combine into a joint share. The two surveys are different households and no sentence says "multiply". The pilot shows the two attributes are positively associated: among complete screens, roughly 11 per cent of burdened households use equipment against about 4 per cent of unburdened households, which is a joint far above the product of the marginals. Whether to use independence, the pilot's association or another joint is not filed. It also leaves whether the nearest-hundred figure or the unrounded one feeds the ceiling (the same result in every division here). The prompt asks for 2025 eligible households plus battery and baseline side counts. These side counts need their own definitions (end of October 2026 active spells, a Central-time January-October window from UTC completions, account transfers), which are semantic steps.

6. The main answer is decided by an analytical choice: how to combine two separately estimated shares into the eligible joint count for a cell, since the filed constraint is only that the table reproduces each marginal. Using the pilot's joint structure (the only file with both attributes on one household) to calibrate the dependence is the analytical step. The easy route is multiplying the marginals under independence, which gives a plausible but lower count. The plan's section 5 sets this up and nothing in it announces it. The mess (M x 12, band mapping, county-to-division, don't-know exclusion) is cleaning and not decisive. Reading the units wrongly would shift totals, but a careful reader gets them right.

###### Realism tells

- data_dictionary.csv and file_register.csv: tidy complete dictionary and register across three organisations, written in the company's voice with every column glossed. RECORDS in file_register matches the row counts exactly (9000, 12000, 9033, 38848, 3917, 30), which is unusually clean for an external bundle.
- hema_screening_pilot_report_2025.pdf: the return table sums exactly to the totals (3,196 + 1,320 + 3,327 + 1,190 = 9,033) and 21,600 addresses are exactly 10,800 per division. The "what the pilot taught us" paragraph gives convenient hints (callers read Q3 as natural gas only, "latest complete screen"). The 151 duplicate address keys are documented in advance. The report text is aimed at the solver. The "mail" and "phone" mode split is regular.
- callowmere_hema_plan_2027_draft.pdf: one page, very compact, and section 5 explains in a single sentence exactly which three sources the table must reproduce. A real filing would not narrate the survey sources this carefully. Round budget figures ($78,400, $1,150, $236,000).
- household_estimates_county_income_2025.xlsx: every county figure is a multiple of ten and the region rows sum to the county rows with no discrepancy. Planning regions are balanced. Eight of the 38 counties are not in the division register (Glasswold, Marlowcombe, Ostercombe, Pinewold, Thornwold, Umberholme, Wendlecombe, Willowcombe); the register is dated 2026-11-02, a few days before the plan.
- heas_2025_household_puf.csv and technical notes: WT_FINAL calibrates exactly to the Demographer figures by county and band, which the notes state outright. HHINC is rounded to hundreds with a top-code. 9,000 completes exactly, no missing values in any column (the notes say income was imputed).
- shs_2025_household_file.csv: 12,000 records exactly. The codebook is thin (no sample design, no field dates, no mode). CNTYFIPS is numeric (45) against the three-digit text codes elsewhere, which is plausible between agencies.
- medical_baseline_enrolment_2026.csv: file_register says "spells active since January 1, 2020", yet START_DATE runs from 2003-01-15 and several ended spells (2022) are included. The END_DATE maximum equals the extract date 2026-11-03 exactly, and the START_DATE maximum is the same day. Spells begin on rounded early dates (2003-01-15, 16, 16) in an apparently sorted file; account and enrolment IDs are tidy sequences (MB1000010, MB1000035, 6100000133 ...).
- battery_placement_work_orders_2026.csv: first rows are Dec 2025 non-completions, and work order numbers step in regular increments (410004, 410017, 410030, step 13). The data dictionary says SCHEDULED is Central Time and COMPLETED_UTC is UTC, which hands over the timezone point.
- heat_vulnerability_index_county_2025.csv: a distractor that ranks counties 1 to 38 without ties, with Quillholme at 102.1 and a mean of 50 / sd 15 as stated. It carries 38 counties, but only 30 are served.
- energy_assistance_applications_2025.csv: 456 rows = 38 counties x 12 months, a complete regular grid, no gaps or revisions.
- Dates: all source dates (2025-07-15, 2025-11-20, 2026-01-21, 2026-03-18, 2026-05-12) are fixed on plausible days, with one cluster of 2026-11-02/03/12/16 for the company files, the last being the data dictionary.

#### Rulings (main thread)

- Q1: none quoted; the estimation-domain pin names the cell, not the combination. Clean.
- Q2, Q3, Q4: no ranking file and nothing reads as the answer; the dictionary and register are the folder's own
  indexes (a real shared folder holds them). Harmless.
- Q5: the quoted text fixes the eligibility, the cost definition, the bands, the division-and-band cell, the
  don't-know exclusion, the caseload standard and the rounding, and leaves the joint open; the reader's literal 26 is
  the default path, and the reader itself names the open step. No main-call fork.
- Q6: analytical (how to build the joint from two separately estimated shares). Agrees with the judge's Gate H.
- Realism tells: the work orders' first numbers 13 apart (a coincidence two readers met at the top of the file) fixed
  in the generator, the record numbers redrawn with nothing graded moving; the rest harmless: counts that tie to the
  register and the survey notes (a folder's own index), spells on the rate since 2020 that began earlier (the
  register's wording), spells starting and ending on the extract day (records keyed that morning), the demographer's
  published tens, a one-page plan citing its sources, a dictionary that defines its columns, the state files' 38
  counties against the territory's 30 (Layer 1).
