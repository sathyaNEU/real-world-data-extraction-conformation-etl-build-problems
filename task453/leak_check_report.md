# leak check, task453

**Verdict: REVIEW.** 13 files read, 20 golden figures and 7 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: sample, rejected, effect, rotation, comparison, interview, section, golden, series, design, redesign, groups, decisive, points, interviews, previous, phase-in, reader, seasonal, averages, effects, references, payroll, method, office

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `lfs_redesigned_questionnaire_methodology_note.pdf`: 14 of 25 stump-paragraph terms appear (sample, rotation, interview, series, design, redesign); read whether the document names the move
- **REVIEW** `regional_employment_support_act_2021_extract.pdf`: 3 of 25 stump-paragraph terms appear (section, design, points); read whether the document names the move
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: "By how much should the Regional Employment Support Act's 6.0 per cent trigger move now that the Labour Force Survey has moved to its redesigned questionnaire, and which regions does the restated trigger designate for 202"
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: 'Put the restated trigger, the change in the published unemployment rate it rests on and the designated regions in trigger_restatement_determination_2027.pdf with a chart of the national unemployment rate as published and'

## 5 announcements (REVIEW 1)
- **REVIEW** `lfs_redesigned_questionnaire_methodology_note.pdf`: 6 Contacts Questions on this note: Labour Market Methods (Debra O'Brien).

## 6 ranking artifacts (REVIEW 2, INFO 2)
- **REVIEW** `lfs_release_2026-12_tables.xlsx`: names 6 of 7 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `lfs_response_rates_2025-2026.xlsx`: names 6 of 7 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `lfs_psu_region_lookup_2025.csv`: names 6 of 7 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `region_classification_concordance_2019_2025.csv`: names 6 of 7 answer-set candidates; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read

Three isolated reader passes (Sonnet, medium), each on fresh copies of `prompt.txt` and the pack. Passes 1 and 2 ran on earlier builds; their realism notes were fixed in the generator and are recorded in the design note's `## Leak check`. Every REVIEW line above was read harmless in all three passes: the methodology note and the Act name no estimator, the contacts line announces nothing, and the release and the response workbook publish the survey's rates without ranking the regions on the decision.

### Pass 3 (final pack)

**1. Method for the main figure (the change)?** No sentence prescribes an estimator. What is fixed is the estimand: Act s9(2) "the number of percentage points by which the national unemployment rate published from the changed survey, once the change is in full use, differs from the rate the survey before the change would have published for the same months, rounded to one decimal place." The methodology note (s3) says the previous questionnaire "leaves the field with the November 2025 interviews, and from December 2025 every rotation group answers the redesigned questionnaire", and that "a published rate is the ratio of two such averages". Together these imply a rotation-group (ICS vs CAI 2014) comparison on the overlap months, but nothing says how (which months, pooled or averaged, same-group comparison). Verdict: "none" on the HOW; the files only set the counterfactual and the full-use window.

**2. File ranking/scoring on the question?** None. Release Table 2 gives regional published rates, but not the 12-month averages, restated rates or a designation. Table 1 gives the national published rate only. Nothing ranks regions or candidate values of the change.

**3. Anything that reads as the answer?** No. The nearest candidates are the release's published national series, which shows a visible rise at Nov/Dec 2025 (5.1 Oct, 5.5 Nov, 5.8 Dec), and the seasonally adjusted column. These read as context (a naive reader may take the published jump as the change). The response-rate workbook's "All regions" column and Oct-Dec rates are context, not the dwelling count.

**4. Literal fixing sentences and ambiguity.**
- Fixing: s9(2) above; s8 "6.0 per cent, or the rate as restated"; s7(1) "at or above the trigger rate", twelve-month average = "mean of the region's unemployment rates for the twelve months of that year", rates "as published ... to one decimal place"; note s4 "Each month before July 2025 is restated by adding the change as the determination states it, in percentage points to one decimal place, to the rate as published, for every region alike"; "July to November 2025 ... carried as published ... from December 2025 the published rates are on the redesigned basis"; s10 regions read on the classification in use for the year (2026 -> 2025 classification, so Table 2 labels are already right; concordance renumbers 2019 -> 2025).
- Possible two-reading points: (a) s9(2) "once the change is in full use" vs "for the same months": which months the national gap is taken over is not fixed (ICS fully in use only from Dec 2025; overlap months July to Nov 2025 each have one to five ICS groups). The year to restate against (designation 2027 reads calendar 2026) is clear. (b) "once the change is in full use ... for the same months" could be read as comparing Dec 2025 onward against a CAI counterfactual that does not exist in the files after Nov 2025; the solver must construct the counterfactual from the CAI cells in the overlap. These are the analysis, not a fork in terms. (c) The chart "as published and on the redesigned basis" for Jul-Nov 2025: note says carried as published; clear. (d) Also: the designation reads 2026 rates, which are already on the redesigned basis, so the restated trigger is compared with unrestated 2026 means; stated literally in Act and note, no fork.
- Dwelling count: mostly closed (Q4 2026 = 2026-10..12; responding = outcome 11 or 12 per dictionary; region via PSU lookup 2025; "counting each dwelling once however many months it responded"). Open point: what identifies a dwelling. `dwelling_ref` is "Sample reference: primary sampling unit, rotation group and line", not a dwelling id. The methodology note s1 says dwellings are replaced after their sixth interview "in the same primary sampling units"; in the parquet interview_no drops 6->1 (group E from Oct to Nov, 14,241 refs; group F from Nov to Dec, 14,162 refs), so one ref covers two different dwellings. The dictionary does not say refs are reused, so a literal reader counting distinct dwelling_ref undercounts (it merges the old and new dwelling on 28,403 replaced refs); the right unit is ref plus replacement (ref + sample cycle). It is derivable from the note and interview_no, but the dictionary text is silent: moderate semantic ambiguity worth closing or deliberately leaving as an ask-level device. Also "responded" is any month in the quarter by the prompt wording ("however many months it responded"); not stated as "at least one month", but this is the natural reading.
- CSV rows: regions: 9 (2025 codes/names) x 36 months (Jan 2024 to Dec 2026) = 324 rows is natural; but the prompt does not say column layout (long vs wide, region code or name, month format) and the method for Jul-Nov 2025 ("carried as published") is only in the note. Region code system (2025) follows from Table 2 labels. Layout unspecified: low-risk but open.

**5. What decides the main answer?** An analytical choice: estimating the questionnaire effect from the overlap (comparing CAI and ICS rotation groups in the same months and regions, with weighting/ratio-of-averages and the national level) rather than reading the step in the published series (Nov 5.5 -> Dec 5.8), which also contains seasonality and a real rise. Then rule application for the restated series and designation. The estimator choice is the stump; the dwelling count is a semantic/identity device.

## Realism

- **Fieldwork file:** 254,964 rows = 84,988 refs x 3 months, exactly rectangular (every ref contacted every month incl. vacant; no missing contacts, no attrition rows). A real contact file would not carry an identical row count per month or a vacant dwelling recontacted in all months with a dead-end outcome sequence; 4,669 of 5,535 October vacants stay 31 in November (plausible persistence but a flat 6.5% vacant rate in every month and a very smooth outcome mix). Lines per PSU-group 9 to 15, ~12 as the note says; 5 PSUs per interviewer area (236 areas x 5 = 1,180) is suspiciously tidy. Mode and interview_no are coherent (F2F first interview only? mode TEL 72%; first-interview mode split looks plausible). Interviewer_area codes sequential IA-101.. fine. No dates-of-contact or interviewer id: thin but acceptable.
- **Response workbook:** regional order (Capital lowest, Highlands highest) and Dec/Jan dip match the note and the fieldwork exactly (recomputed Oct 74.5, Nov 74.1, Dec 71.5; regional values identical to the decimal). Perfect reproducibility to the fieldwork is itself unlike two real offices' tables. Note text "most in the Capital and Harbour" is reasonable. One sheet, tidy; no footnote on provisional status. Minor.
- **Population benchmarks:** every value is a multiple of 10 (270 of 270), pattern of 5 age bands x 2 sexes x 9 regions, smooth growth ~0.8% a year; 55+ as one band. Real benchmarks usually rounded to 100 or unrounded. Slightly artificial but not alarming. The 2025 file uses age bands "15-24" etc. Region column loses leading zeros when parsed (stored as 01 text) fine.
- **Release tables:** formats fine (month labels Jan-2022, one decimal, contents sheet, footnotes). Table 1 rate column shows integers like 6 and 5 because of float storage (not formatted), as does Table 2 (4, 6.1); display format may hide it. Table 3 sheet is one row shorter than Table 2 (footnote count only). "Earlier months have not been revised." fine. No standard errors or revisions flags, which a real release would carry; acceptable.
- **Dictionary and manifest:** manifest "extracted" dates 2027-01-25 (after the release); plausible. Manifest row counts exact. Dictionary uses two naming styles (CAI file uppercase codes; ICS lowercase text codes), which reads like two systems and is a plausible Layer 1 touch. Only wrinkle: dictionary says "dwelling_ref ... Sample reference" without noting reuse. The CAI file with LFSTAT rows vs ICS wide counts is believable. ICS weighted counts are integers, CAI WTD000 are thousands with 3 decimals; consistent with the dictionary.
- **PDFs:** the Act extract is credible (consolidation caveat "This consolidation is not an official version", sections, definitions). Methodology note wording is mostly plausible; two tells: "about twelve sample references each, nine to fifteen with the size of the blocks a group is listed from" is clumsy; named authors (Debra O'Brien, Gabrielle Esson) look like generated names but harmless. Page 2 is nearly empty (a section 5 split across pages plus contacts). Note dated June 2025 yet says "Published estimates for July to November 2025" in the present tense and describes the Dec 2025 state as fact: a note issued 16 June 2025 cannot report that CAI "leaves the field with the November 2025 interviews" as completed; it is a plan, worded as plan. Fine but borderline. The note (June 2025) also states the 2025 classification applies from Jan 2025 and promises regional series "from January 2024", fine.
- **CAI file:** 202201 to 202511 with 6 groups until Jun 2025 then 5,4,3,2,1 (consistent with the note); 1,620 rows per full month; early months show RESP totals roughly 140k a month; regional RESP varies 10,952 to 24,078 plausibly.
- LLM/template tells found: none strong; the smoothness of reproduced response rates and the multiples of 10 are the only ones.
