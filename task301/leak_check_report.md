# leak check, task301

**Verdict: REVIEW.** 13 files read, 25 golden figures and 3 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: measure, claimed, record, register, launch, status, patient, decisive, claims, call-only, extract, coverage, history, golden, smoker, cohort, recorded, sub-region, recordings, decision, survey, sentence, widening, reader, probes

## 4 design-note vocabulary (REVIEW 5)
- **REVIEW** `appraisal_guidance_child_poverty_2027.docx`: 4 of 25 stump-paragraph terms appear (measure, claimed, record, survey); read whether the document names the move
- **REVIEW** `complemento_familiar_coverage_2025.pdf`: 3 of 25 stump-paragraph terms appear (claimed, coverage, survey); read whether the document names the move
- **REVIEW** `complemento_familiar_rules_2026.pdf`: 3 of 25 stump-paragraph terms appear (claims, history, decision); read whether the document names the move
- **REVIEW** `ecvv2026_main_results.pdf`: 3 of 25 stump-paragraph terms appear (measure, register, survey); read whether the document names the move
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: 'The note, cabinet_note_child_poverty_2027.pdf, should make that recommendation in no more than two pages with a chart comparing the measures, and appraisal_annex_2027.xlsx should give the families the Complemento Familia'

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read (Leak reader, architecture 3 round 1 (2026-11-02, isolated, Sonnet at medium effort, on target.zip ae2a4182))

1. Decisive step: none; the guidance's 3.7 income test and the proposals' delivery lines (no 2025 return, not reached; families apply under the Complemento's decision and payment rules) are context, naming no winner or step.
2. Nothing ranks the measures on children lifted (the proposals' cost column is full-take-up cost).
3. Nothing exists only to help the analyst (territorial codes is a plain lookup; incidents, municipal estimates and the 2025 survey read as distractors or context).
4. Nothing reads as the answer (the 71.8 per cent coverage and the poverty rates are context).
5. Guidance 2.1 and 3.5 read literally: weighted children below the line without the measure and at or above it once the measure's payments received during 2027 are added; the estimand, not how take-up or timing is estimated.
6. An analytical choice: applying the measures' payments as paid in 2027, claim timing and take-up for measures that need a claim; no file states a take-up rate or a claim-timing profile; nothing planted.
Sweep flags: the guidance, coverage report, rules statute and main results are harmless (estimand and definitions; a past coverage rate; rule text for the ask; "it does not appraise policy measures"); the proposals do not rank on children lifted; the prompt does not hint at take-up or timing.
Realism: none generated (the reader's odd digit spacing is the files' Spanish decimal comma under semicolon separators, checked by the main session).

## Solver's-eye read (Leak reader, architecture 3 round 2 (2026-11-02, isolated, Sonnet at medium effort, on target.zip 3ab80e13))

1. Decisive step: none stated; the nearest are guidance 3.9 (under a claimed measure a newly entitled family receives payments only once it has claimed and its claim has been decided, then from the month the payment rules set) and rules 6.1 (paid from the month after the claim is decided); neither names a claim pace or method.
2. Nothing ranks the measures (the proposals' cost column is full-take-up cost).
3. Lookups and context only (territorial codes; the main results' response-rate definition; distractors).
4. Nothing reads as the answer (the 64.4 per cent is end-2025 coverage of existing entitlement).
5. Guidance 3.3, 3.5, 3.7 and 3.9 read literally: a child counts when 2027 equivalised income is below the line without the measure and at or above it with the payments actually received in 2027.
6. An analytical choice: how many newly entitled families claim, and when, under the claimed measures, from the register's evidence; nothing planted.
Sweep flags: clause 3.9 says only whose payments count and from when; the proposals, coverage and rules files rank nothing and give no claim speed; the fieldwork reissue column reads as the system's own field (reissue_of beside issue).
Realism: none generated; minor: the visits distribution is slightly odd.
