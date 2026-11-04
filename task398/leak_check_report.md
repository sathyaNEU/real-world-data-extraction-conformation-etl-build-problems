# leak check, task398

**Verdict: REVIEW.** 26 files read, 5 golden figures and 6 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: source, intake, tributary, receptor, decisive, tessel, fennick, sampled, window, attribution, record, sentence, temperature, harmless, closed, shipped, carries, nothing, sub-watersheds, objective, forward, pattern, correct, second, decomposition

## 1 file names (REVIEW 1)
- **REVIEW** `lake/merrin_dam_precip_daily_2026.txt`: a text file in the pack: confirm it is the organisation's own record (a thread, a log, a letter) and does not describe the data

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `program/source_water_protection_plan_rev2.pdf`: carries 8 of 8 distinctive words of the committed call: 'Place the 2027 atrazine cost-share program in the Fennick Creek sub-watershed.'

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `program/source_water_protection_plan_rev2.pdf`: 10 of 25 stump-paragraph terms appear (source, intake, tributary, tessel, fennick, sampled); read whether the document names the move

## 6 ranking artifacts (REVIEW 2)
- **REVIEW** `program/haldane_extension_atrazine_use_survey_2026.xlsx`: names 5 of 6 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `program/source_water_protection_plan_rev2.pdf`: names 5 of 6 answer-set candidates beside numbers; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `lake/buoy_service_log_2026.csv`: 1 ISO dates after 2026-11-03, e.g. 2026-11-09

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Isolated reader, 2026-11-04 (general-purpose, sonnet, medium), architecture 1, on a fresh copy of prompt.txt and target/ (target.zip sha256 8fd1530d94abcbe381de4c1d10a313396a43c405f3176d226ae43e0c81bc937c). Sweep 3's and sweep 4's lines on the plan were kept out of the brief and ruled in the main thread. Verdict: no leak; the decisive step is read as an analytical choice (the plan 5.1 counterfactual, its method unfiled); the realism tells below go to the generator.

# Leak read, task398 (no solving)

1. Decisive step stated? Closest is the filed placement rule, source_water_protection_plan_rev2.pdf 5.1: "A day counts for a sub-watershed when the raw water would have stayed at or below the trigger that day without that sub-watershed's atrazine." It defines the counterfactual (remove one sub-watershed's atrazine) but not how to compute it. SOP-WQ-07 2.3 fixes the day's raw-water result. Nothing announces a pitfall or the intended method.
2. Ranking/scoring of candidates on the question: none. The Haldane survey and the plan's Table 2 give acreage, rates and areas only.
3. File that exists only to help the analyst: none clearly. The nearest are the plan and the SOP (governing documents, written as org documents), and the DC-04/LB-05 ratings workbook (plausible hydrometric record).
4. Figure or name that reads as the answer: none. Table 2 and the survey give no per-watershed day counts or causal shares.
5. Literal-fixing sentences:
   - Plan 5.1: "the one whose atrazine was behind the most days of the last completed season on which the plant's raw water was above the carbon-feed trigger. A day counts for a sub-watershed when the raw water would have stayed at or below the trigger that day without that sub-watershed's atrazine." Fixes: population = days in the season on which raw water was above the trigger; unit = day; comparison = counterfactual with that one sub-watershed's atrazine removed; an exceedance day can count for more than one sub-watershed.
   - Plan 5.2: "The season runs from 15 April to 31 October ... A day's raw-water result is the one SOP-WQ-07 sets." SOP 2.3: GC/MS confirmation where run on that day's sample, otherwise the ELISA screen. SOP 3.1: trigger is "above 3.0 ug/L".
   - Plan 3.2: "Where both laboratories analysed a bottle, the State Hygienic Laboratory's result is used. A result reported as not detected counts as zero in load calculations."
   Method for the counterfactual (load routing, travel time, dilution) is not filed.
6. What decides it: an analytical choice, the counterfactual attribution of exceedance days to each sub-watershed (plan 5.1), not a field reading or a planted item. The file-reading and rule steps (SOP 2.3 day result, SHL over ELISA, ND as zero, interpolating samples against flows) are supporting. I see no decoy; the survey xlsx is a plausible distractor (use, not load).

## Flagged items
a. harmless, because it reads as an NWS COOP-style station record (header "MERRIN DAM IA COOP ID 13-5528 ELEV 870 FT OBS AT 0700 LST", date and PRCP columns only), not a description of data or task.
b. harmless, because it gives acres, atrazine-treated acres, rates and respondents per sub-watershed, an extension survey. It does not rank on the raw-water-day question or speak to exceedances, though treated acres times rate gives a use ranking that a naive solver could take as a proxy (a distractor, not a leak).
c. harmless, because Table 2 lists area, station and site code only, and nothing points to one sub-watershed as the answer. The rule in 5.1 is generic.
d. harmless, because "Flag" is a normal LIMS result column (beside LIMS ID, RL, Analyst, Kit lot); all 249 rows are empty, which is plausible for a flag column but slightly vestigial.
e. harmless, because the entry (2026-10-31 "Recovery planned 2026-11-09") is a future-dated plan in a service log, a normal log entry; the data end 31 Oct. Mild: "Mixing to bottom expected within the week" (2026-10-06) is a field note on lake turnover, not about atrazine.

## Realism
Mostly none. Minor tells:
- Both PDFs (plan, SOP) share the same PDFlib 9.3.1 producer, empty Author, identical letterhead, the same "Prepared Brandi Dougherty / Carl Newman" block, and tiny files (3.6 KB and 6.2 KB, text only). They are consistent with one department's document system. The sign-off tables have no signatures, only names and dates. The record-drawing PDF (Ball & Frye) uses the same PDFlib producer (version 1.3) despite being a 2011 engineer's drawing, so the different organisation shares the generator's toolchain.
- The Brennick xlsx files (ELISA, field log, LIMS, operating report) name staff authors consistently (Dougherty, Newman, Dixon), matching the document sign-offs; fine.
- Flag column in the ELISA workbook is entirely blank; the DOSE setpoint file has only 11 rows.
- Staff initials BD/BC in the ELISA file dominate (BD 181 of 249) and field log has "ISCO ... carousel" notes; field-log remarks are plausible and varied.
