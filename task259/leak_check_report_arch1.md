# leak check, task259

**Verdict: REVIEW.** 12 files read, 12 golden figures and 5 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: movement, employers, report, employer, matched, reports, market, policy, platform, growth, respondents, pooled, crosswalk, decisive, people, filing, respondent, window, carries, median, extract, benchmark, sentence, family, inside

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `tarnwick_compensation_policy_2026.pdf`: golden figure 1.1 appears: ...6; replaces version 2025.1. 1. Purpose and scope 1.1 This policy sets how Tarnwick Systems prices base...
- **REVIEW** `tarnwick_compensation_policy_2026.pdf`: carries 7 of 7 distinctive words of the committed call: 'File the Data Engineer III midpoint at $170,000 for the pay bands that take effect on 1 April 2027.'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `tallyband_methodology.md`: 9 of 25 stump-paragraph terms appear (employers, report, employer, reports, respondents, filing); read whether the document names the move
- **REVIEW** `tarnwick_compensation_policy_2026.pdf`: 10 of 25 stump-paragraph terms appear (employer, matched, market, policy, crosswalk, people); read whether the document names the move

## 6 ranking artifacts (REVIEW 1, INFO 2)
- **REVIEW** `ats_requisitions_2026-10-14.csv`: names 4 of 5 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `hris_job_history_2026-10-14.csv`: names 4 of 5 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `tarnwick_engineering_job_architecture.xlsx`: names 4 of 5 answer-set candidates; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `hris_job_history_2026-10-14.csv`: 34 ISO dates after 2026-10-14, e.g. 2026-10-16, 2026-10-19, 2026-10-28, 2026-11-02, 2026-11-05

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read

One isolated reader (loop 1 cut, 2026-10-13), fresh copies of prompt.txt and target/ only.

1. Decisive step: none announced. Nearest: policy 4.3, "The market is read as in effect on the benchmark date, 1 October 2026: the base pay a job and level commands on that date", with the methodology's 36-month window; neither says what to do about the spread of filing dates. Nothing names the employers' arrival on the platform or a reading within employers.
2. Ranking or scoring file: none.
3. Helper file: people_data_exports_readme.md and tallyband_methodology.md read as field glossaries; neither names a method.
4. Answer-like figure or name: none; tallyband_level read as context.
5. Literal sentences: policy 4.2 (the matched respondents, counted once) and 4.4 (the three points, to $1,000); the reader judged 4.3 vague on restating old reports and its literal executor left them as filed (rung R1, $164,000). Ruled: 4.3 states the pay a job and level command on 1 October 2026, which a report filed in 2023 does not show; the loop-0 judge (two passes) and this loop's determinism pass rule on it; no change.
6. What decides: an analytical choice (how 36 months of reports become the market on 1 October 2026); the matching rules (4.2, the crosswalk) read as rule execution on lower rungs.

Mechanical REVIEW lines:
- Policy, golden figure 1.1: harmless, the clause number 1.1.
- Policy, 7 of 7 call words: harmless, the prompt's job, level and effective date; no number.
- Methodology, 9 of 25 stump terms: harmless, ordinary survey vocabulary; describes the latest-report and previous_ structure neutrally.
- Policy, 10 of 25 stump terms: harmless, the market definition; names no move.
- ATS, four levels beside numbers: harmless, requisitions by job code and status, no ranking.
- HRIS, 34 dates after the export: harmless, changes entered ahead as the readme says.

Realism tells (reader): the exports dated two weeks after the benchmark; a 25-row OEWS extract for one occupation; uniform respondent ids; owners named in the policy and readme; a small job architecture workbook; a tidy numbered policy. Ruled harmless: each is an ordinary export or document of its kind and none touches the call; the OEWS file is a state filter of one occupation, declared a distractor.
