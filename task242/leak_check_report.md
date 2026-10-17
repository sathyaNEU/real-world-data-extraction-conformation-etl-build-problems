# leak check, task242

**Verdict: REVIEW.** 19 files read, 56 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: sensitivity, january, dropped, window, epidemic, collection, timing, single, quantity, fieldwork, laboratory, method, indicator, register, survey, season, infections, decisive, quality, specimen, marker, rogan-gladen, pooled, monitoring, surveillance

## 3 answer figures in the pack (REVIEW 13)
- **REVIEW** `dengue_bulletin_dec2027.pdf`: golden figure 12.7 appears: ...t 422 60 14.2 II Thenkarai 23 Oct to 2 Nov 465 59 12.7 III Puthanpalli 28 Oct to 7 Nov 406 50 12.3 IV Me...
- **REVIEW** `dengue_bulletin_dec2027.pdf`: golden figure 13.2 appears: ...c 417 31 7.4 XII Aranmanai 29 Oct to 8 Nov 409 54 13.2 City 13 Oct to 7 Dec 4,952 440 8.9 Table 1. Dengu...
- **REVIEW** `dengue_bulletin_dec2027.pdf`: golden figure 10.2 appears: ...8 Nov 378 35 9.3 VI Kizhakkoor 2 to 12 Nov 423 43 10.2 VII Velliyanur 8 to 18 Nov 432 19 4.4 VIII Chinna...
- **REVIEW** `dengue_bulletin_dec2027.pdf`: golden figure 12.3 appears: ...65 59 12.7 III Puthanpalli 28 Oct to 7 Nov 406 50 12.3 IV Melmangalam 22 Nov to 2 Dec 407 23 5.7 V Vadak...
- **REVIEW** `dengue_bulletin_dec2027.pdf`: golden figure 14.2 appears: ...ion share, 2027 (%) I Kadalur 13 to 23 Oct 422 60 14.2 II Thenkarai 23 Oct to 2 Nov 465 59 12.7 III Puth...
- **REVIEW** `dengue_bulletin_dec2027.pdf`: golden figure 5.7 appears: ...406 50 12.3 IV Melmangalam 22 Nov to 2 Dec 407 23 5.7 V Vadakkupatti 18 to 28 Nov 378 35 9.3 VI Kizhakk...
- **REVIEW** `dengue_bulletin_dec2027.pdf`: golden figure 7.4 appears: ...Nov 372 19 5.1 XI Sengalur 27 Nov to 7 Dec 417 31 7.4 XII Aranmanai 29 Oct to 8 Nov 409 54 13.2 City 13...
- **REVIEW** `dengue_bulletin_dec2027.pdf`: golden figure 5.1 appears: ...Nov 418 28 6.7 X Kottaivayal 12 to 22 Nov 372 19 5.1 XI Sengalur 27 Nov to 7 Dec 417 31 7.4 XII Aranma...
- **REVIEW** `dengue_bulletin_dec2027.pdf`: golden figure 4.4 appears: ...Nov 423 43 10.2 VII Velliyanur 8 to 18 Nov 432 19 4.4 VIII Chinnakulam 27 Nov to 7 Dec 403 19 4.7 IX Pe...
- **REVIEW** `dengue_bulletin_dec2027.pdf`: golden figure 6.7 appears: ...Dec 403 19 4.7 IX Periyamalai 10 to 20 Nov 418 28 6.7 X Kottaivayal 12 to 22 Nov 372 19 5.1 XI Sengalur...
- **REVIEW** `dengue_bulletin_dec2027.pdf`: golden figure 9.3 appears: ...Dec 407 23 5.7 V Vadakkupatti 18 to 28 Nov 378 35 9.3 VI Kizhakkoor 2 to 12 Nov 423 43 10.2 VII Velliya...
- **REVIEW** `dengue_bulletin_dec2027.pdf`: golden figure 4.7 appears: ...32 19 4.4 VIII Chinnakulam 27 Nov to 7 Dec 403 19 4.7 IX Periyamalai 10 to 20 Nov 418 28 6.7 X Kottaiva...
- **REVIEW** `vector_surveillance_sop_extract.pdf`: golden figure 100 appears: ...Houses with at least one positive container, per 100 houses inspected Container index (CI) Positive co...

## 4 design-note vocabulary (REVIEW 5)
- **REVIEW** `DATA_DICTIONARY.md`: 5 of 25 stump-paragraph terms appear (january, laboratory, register, survey, specimen); read whether the document names the move
- **REVIEW** `README.md`: 8 of 25 stump-paragraph terms appear (january, laboratory, indicator, register, survey, quality); read whether the document names the move
- **REVIEW** `dengue_bulletin_dec2027.pdf`: 5 of 25 stump-paragraph terms appear (fieldwork, indicator, survey, season, specimen); read whether the document names the move
- **REVIEW** `serosurvey_2027_protocol.docx`: 7 of 25 stump-paragraph terms appear (fieldwork, laboratory, register, survey, season, quality); read whether the document names the move
- **REVIEW** `sop_epi_07_quality_flags.pdf`: 6 of 25 stump-paragraph terms appear (quantity, laboratory, indicator, register, quality, surveillance); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

# Reader 2 (after the cover note was trimmed and the PDFs given subject lines)

## Solver's-eye read

### 1. Sentence telling the decisive step
None. The SOP-EPI-07 flag row (sop_epi_07_quality_flags.pdf) says only: "the quantity the register says the value stands for, estimated from the same data with allowance for the test's misclassification as the testing laboratory has measured it, is more than one and a half times the published value or less than two thirds of it". The register (epi_cell_indicator_register.xlsx, SERO-D1) says the value stands for "the share of the zone's residents aged one year and over infected with dengue virus between 1 January 2027 and the collection of their survey specimen". Neither says how to allow for misclassification. I had to work out myself: the panel (ngmc_igm_lot_verification_panel.csv) shows sensitivity falling with days since onset (about 83% within 30 days, 77% at 31-60, 40% at 61-90, 12% at 91-120, 0 beyond), specificity of about 97-99% (4 reactive of 300 controls), so a single sensitivity is wrong: IgM detects only recent infection while the register's quantity covers infection since 1 January, with time-varying detection depending on each zone's fieldwork date and the season curve (line list). Then a corrected estimate per zone and the 1.5x / 2/3 test.

### 2. File that already ranks or scores zones on the flag
None. The bulletin PDF gives only published shares. No file holds an estimated share or a flag.

### 3. File existing only to help the analyst
flag_review_request.eml and README.md read as pack scaffolding (the README lists files with purposes; "Files gathered ... for the quality flag review"). The cover note eml is plausible organisationally. The rain gauge and fogging log (and probably the specimen register) look like distractors but are plausible real records. DATA_DICTIONARY.md is analyst help but ordinary.

### 4. Figure or name reading as the answer
None found. The bulletin's published shares are context. The cover note and the filenames do not name the pitfall. The only slight pointer is the panel's onset_date and collected_on columns, plus the cover note's "onset and collection dates are as the clinic recorded them", which hints at time since onset but does not announce it.

### 5. Sentences that fix computation or population
- Prompt: "the infection share you estimate that value stands for": the estimand is what the register says the value stands for.
- Register SERO-D1: "infected with dengue virus between 1 January 2027 and the collection of their survey specimen": cumulative infection since 1 Jan to each person's collection date, not current IgM positivity. Implies modelling detection over time since infection (panel decay) against the 2027 infection timing, per zone/collection date.
- SOP M row: flag if estimate > 1.5 x published or < 2/3 x published (literal ratio thresholds, on the published value).
- SOP S row / register: shares among residents aged 1+; bulletin: "residents tested" is the denominator.
- Protocol 5: "an index of 1.10 or more is reactive and 0.90 to 1.10 is tested again"; cover note: "the repeat is the final result" (use result_final).
- Protocol 6: "household response rate is the share of sampled households, other than those the field team found vacant or not a dwelling, in which at least one member gave a blood specimen": denominator 2,178 less outcome 4 and 5 households (final outcome), numerator households with at least one specimen (igm_results household_id).
- SOP-VC-02 6: "each house inspected in the month counts once, with what was found at its round inspection. A locked call and a follow-up visit are not round inspections." BI = positive containers per 100 houses inspected; implies deduplicating premise_id (1,888 repeats), dropping LOCKED and follow-up rows (SR DONE likely), then mapping ward_no to zone via ncmc_ward_master_2027.csv (former_ward_nos exists, so old ward numbers may appear on forms).
- Kobo data dictionary: visit_number entered by interviewer, 57 duplicate household/visit pairs, two form versions: duplicate submissions to resolve.

### 6. What decides the main answer
(a) an analytical choice. The decisive step is estimating the true infection share from IgM results given waning, time-varying sensitivity and the infection timing (the register's cumulative definition), rather than applying one fixed sensitivity/specificity or counting reactives. No sentence states the correction method; the panel and register data give the structure. A careful analyst who cleaned data and read every rule could still file a wrong flag set with a flat Se/Sp correction. The supporting figures (BI, response rate) are data-cleaning/rule application, but they are the asks, not the call.

## Realism
- Mostly credible: Indian municipal naming, SOP and register wording, email headers and offsets, kobo ids look real. Bulletin Table 1 is coherent and sums (440/4,952 = 8.9).
- Minor: DATA_DICTIONARY.md and README.md read tidily "made for the task" (README.md lists every file and role). Cover note says "All plates passed the kit's run validity criteria" (mildly pointed). Dates in file listing are Jan 2028 while the CHO email is 10 Jan 2028 and the prompt says December bulletin; consistent.
- Bulletin Figure 1 y-axis ticks every 200 from 0 to 3600 in pdftotext is fine. Panel patient_refs repeat (FUC/26/0001 twice), plausible serial sampling.
- Nothing flagrantly LLM-sounding; the zone naming "Zone IV" / "VELLIYANUR" case variants in the line list read as realistic mess.

## Rulings (reader 2)

- Question 1 none; question 2 none; question 4 none (the panel's onset and collection dates are the data the field records, needed for any reading of the panel); question 6 an analytical choice. Harmless.
- Question 3: the request email is the City Health Officer's own message (the context artifact), and the README and the dictionary are the folder's ordinary handover files, as in every pack. Harmless.
- Question 5: every quoted sentence executes to the golden. Harmless.
- Realism: "All plates passed the kit's run validity criteria" is the line a laboratory writes on any run report. Harmless.
