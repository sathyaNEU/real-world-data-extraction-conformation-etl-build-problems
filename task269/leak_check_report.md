# leak check, task269

**Verdict: REVIEW.** 16 files read, 8 golden figures and 5 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: blueprint, domain, decision, examiner, policy, reader, candidates, record, variance, method, decomposition, candidate, decisive, examining, review, pooled, carries, stringency, architecture, coefficient, selection, design, examination, single, checks

## 3 answer figures in the pack (REVIEW 5)
- **REVIEW** `assessment_policy_v7.pdf`: golden figure 0.80 appears: ...st rank candidates with a reliability of at least 0.80: the share of the variance among candidates' tot...
- **REVIEW** `assessment_policy_v7.pdf`: carries 3 of 3 distinctive words of the committed call: 'Set the 2027 final OSCE at 13 stations.'
- **REVIEW** `board_of_examiners_minutes_2026-05-14.pdf`: carries 3 of 3 distinctive words of the committed call: 'Set the 2027 final OSCE at 13 stations.'
- **REVIEW** `final_osce_2027_delivery_plan.docx`: carries 3 of 3 distinctive words of the committed call: 'Set the 2027 final OSCE at 13 stations.'
- **REVIEW** `osce2027_blueprint_working_pack_index.txt`: carries 3 of 3 distinctive words of the committed call: 'Set the 2027 final OSCE at 13 stations.'

## 4 design-note vocabulary (REVIEW 7)
- **REVIEW** `assessment_policy_v7.pdf`: 11 of 25 stump-paragraph terms appear (blueprint, domain, decision, examiner, policy, candidates); read whether the document names the move
- **REVIEW** `board_of_examiners_minutes_2026-05-14.pdf`: 6 of 25 stump-paragraph terms appear (blueprint, examiner, policy, candidates, candidate, examination); read whether the document names the move
- **REVIEW** `casebank_migration_report_2025-11.pdf`: 5 of 25 stump-paragraph terms appear (blueprint, domain, record, review, examination); read whether the document names the move
- **REVIEW** `final_osce_2027_delivery_plan.docx`: 8 of 25 stump-paragraph terms appear (blueprint, domain, examiner, policy, candidates, candidate); read whether the document names the move
- **REVIEW** `osce2026_candidate_feedback_summary.pdf`: 3 of 25 stump-paragraph terms appear (candidates, candidate, examination); read whether the document names the move
- **REVIEW** `osce2027_blueprint_working_pack_index.txt`: 5 of 25 stump-paragraph terms appear (blueprint, examiner, policy, candidate, examination); read whether the document names the move
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: "Put that number in osce2027_station_plan.xlsx with the reliability of the total mark at every number of stations from 12 to 18, and with it, for each of the case bank's four domains, how many of its cases can be set in M"

## 6 ranking artifacts (REVIEW 1, INFO 1)
- **REVIEW** `examiner_availability_2027_responses.csv`: names 5 of 5 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `final_osce_2027_delivery_plan.docx`: names 5 of 5 answer-set candidates; confirm it does not rank them on the decision question

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Architecture 2. Each round: two isolated Sonnet readers at medium, each on its own fresh copy of `prompt.txt` and `target/`, each solving in full and handing back its figures, scored with `score_reader.py` before its answers were read.

Round 1 (2026-10-19). Both readers missed the call, each filing 16 stations by the pooled decision study (stations and examiners random from one bank, the stringency counted as error). Reader 1 kept 12 of 23 ask figures (Ask B, the training record joined on the staff number or else the name; exit 1); reader 2 kept 4 (Ask A, re-created records linked by domain, specialty and review date; exit 0). Both asks were re-sited and the allocation date filed (design note, Build record).

Round 2 (2026-10-19, the repaired pack). Both readers missed the call (16 each) and every ask figure: 0 of 23, exit 0, for each.

Answers, both rounds, all four readers alike:
1. The decisive step: no sentence states it; each quoted policy 4.3 ("the stations being drawn from the case bank each year and the examiners from the faculty's examiner register") and the plan's "Each station will have one examiner in each circuit" as the nearest. Verdict: the filed estimand; nothing names the domains as a fixed facet or the candidate-by-domain variance as true score.
2. A ranking file: none. Verdict: harmless.
3. A file only for the analyst: the pack index named by three readers as a convenience list. Verdict: harmless; an examinations office assembles such an index for a working pack.
4. A figure reading as the answer: none; the 0.80 standard and the eighteen rooms read as limits. Verdict: harmless.
5. The literal computation: policy 4.3 read as stations and examiners random, the plan's single examiner. Verdict: policy 4.2 fixes the domains drawn every year, so the literal reading with the blueprint is the golden (13); one round 1 reader named that study as an alternative and set it aside on 4.3's wording, which is the analytical step, not a fork (the judge reproduced 13 and found every variant tested files 13).
6. What decided: an analytical choice for all four (the examiner a random facet under single examining). Verdict: rule 3 holds; the step none of them took is the fixed blueprint.
7. Contradictions: the register's last refresher against the training record's outcomes, two staff-number schemes, the old bank's text dates. Verdict: the pack's designed mess, each how its system keeps records.
8. Realism: round 1 named evenly spaced CV codes, consecutive old codes for the re-created records, review dates shared to the day and personal addresses all name and digits; round 2 the empty comment box. Verdict: each fixed in the generator with no graded figure moving.

REVIEW lines (leak.py), judged by reader 1 of round 1 after it committed its figures: every line harmless (0.80 is the standard; the call's words are the documents' own subject; no document names a method; the prompt's second sentence says what to deliver, not how; neither the form nor the plan ranks a number of stations).
