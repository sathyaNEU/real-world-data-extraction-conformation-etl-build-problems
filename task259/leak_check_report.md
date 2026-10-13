# leak check, task259

**Verdict: REVIEW.** 12 files read, 10 golden figures and 5 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: report, policy, market, matched, movement, growth, respondents, filing, reports, crosswalk, platform, people, median, benchmark, extract, employer, family, respondent, decisive, pinned, compensation, carries, carried, quantity, re-reporters

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `tarnwick_compensation_policy_2026.pdf`: carries 7 of 7 distinctive words of the committed call: 'File the Data Engineer III midpoint at $168,000 for the pay bands that take effect on 1 April 2027.'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `tallyband_methodology.md`: 8 of 25 stump-paragraph terms appear (report, respondents, filing, reports, extract, employer); read whether the document names the move
- **REVIEW** `tarnwick_compensation_policy_2026.pdf`: 11 of 25 stump-paragraph terms appear (policy, market, matched, crosswalk, people, median); read whether the document names the move

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

Two isolated reads (Sonnet, medium), each on a fresh copy of `prompt.txt` and `target/` only.

- **Q1, the decisive step:** none named. The nearest sentence is policy 4.3; after pass 1 it reads "The market is read
  as in effect on the benchmark date, 1 October 2026: the base pay a job and level commands on that date", which the
  second reader took to require every report's pay restated as at 1 October 2026 while leaving the method open (it
  reached first for the repeat filers' own growth, the default path).
- **Q2, ranking:** no file ranks the levels or states a midpoint; the OEWS table and the offers extract are other
  bases (the declared distractors).
- **Q3, helper files:** none; the readme's "changes already agreed are entered ahead" and the methodology's advice to
  use a subscriber's own mapping read as the systems' own notes.
- **Q4, answer figures:** none.
- **Q5, literal sentences:** policy 4.2 fixes the population (US, full time, survey match, crosswalk level, counted
  once), 4.3 the date, 4.4 the points and rounding; each executes to the golden's population and points. Pass 1 read
  4.3 ("as in effect") as leaving open whether to take the latest reports as filed: fixed in the generator (the WHAT
  pinned, no method named), confirmed closed by pass 2.
- **Q6, what decides:** an analytical choice, how to restate stale reports to the benchmark date; the filters around
  it are rule application on lower rungs; nothing planted.
- **Realism:** round counts, sibling employer names, a uniform crosswalk and a readme sentence narrating the posting
  grain (pass 1) were fixed in the generator; pass 2's remaining notes (word-plus-trade names in bulk, uniform mapping
  dates) were fixed with varied names and per-employer mapping dates. The zone change on one date and the 36-month
  window are the systems' own.
- **Ask forks:** the headcount's zone source (the HRIS's recorded zone against the dated zone table), leave and
  contingent workers, and the requisitions' posting grain and status dates: each is closed by the readme's column
  definitions and the dated table (the judge reproduced every cell on that reading).

REVIEW lines: the policy carrying the call's words (harmless: the estimand's authority, no figure); the methodology's
and the policy's ordinary vocabulary (harmless: neither names a carry, a movement or a growth rate); the ATS naming
the four levels (harmless: requisition rows, no ranking); the HRIS's 34 dates after the export (harmless: changes
entered ahead, as its readme says).
