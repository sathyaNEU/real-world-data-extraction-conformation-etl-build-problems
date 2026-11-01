# leak check, task189

**Verdict: REVIEW.** 12 files read, 2 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: method, sample, clause, asserted, authority, programme, average, standard, sentence, decisive, kilcrohane, sensitive, points, comparison, export, non-detects, laboratory, monitoring, estimator, qualifier, schedule, reflex, censored, reported, observation

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `kilgarron_quarterly_report_2025q3.pdf`: 3 of 25 stump-paragraph terms appear (sample, authority, laboratory); read whether the document names the move
- **REVIEW** `laboratory_method_schedule.pdf`: 7 of 25 stump-paragraph terms appear (method, sample, authority, export, laboratory, qualifier); read whether the document names the move
- **REVIEW** `surface_water_quality_regulations_2019.pdf`: 11 of 25 stump-paragraph terms appear (method, sample, authority, programme, average, standard); read whether the document names the move
- **REVIEW** `tirneevin_quarterly_report_2025q3.pdf`: 3 of 25 stump-paragraph terms appear (sample, authority, laboratory); read whether the document names the move

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


## Solver's-eye read, stage 4 of the rubric reship (2026-11-01)

One isolated reader (general-purpose, Sonnet, medium) held only `prompt.txt` and a fresh unzip of
`target.zip` (cbc5251ba0d7c644) and was asked the six leak questions, a realism check and whether the
pack tells the analyst how to count the ortho-phosphate samples. It solved nothing. Its answers and the
main thread's ruling on each:

- **Q1, the decisive step.** No sentence states it. The closest pointer it quotes is clause 7.2's third
  sentence ("the figure the results it holds support", no property of a fitted distribution), which it
  reads as pointing at the handling of below-limit results without naming a method. Ruling: as on the
  shipped version and frozen with the call; the design note's survivor anatomy records the sentence under
  Pins.
- **Q2, a ranking file.** None. **Q4, an answer-like figure.** None.
- **Q3, helper files.** The method schedule's scope notes, the batch log and the register's network note.
  Ruling: the method schedule and the register are records the authority keeps and the call reads (the
  register is the shipped commit's byte for byte); the schedule's nitrate note, which no ask uses since
  the nitrate ask was retired, is removed. The batch log is the laboratories' contractual record.
- **Q5 and Q6.** The literal execution it gives of clauses 4.1, 4.2, 4.4, 7.1 to 7.3, 7.5 and 7.6 is the
  golden's construction, with the below-limit estimate the open analytical choice. Ruling: no main-call
  fork; the decisive step is analytical.
- **Q7, realism.** (a) Sample numbers advancing in a fixed step in the Kilgarron report: fixed, the
  laboratories number nutrient bottles in the order they reach reception and each report lists its
  results by client point and collection date, so consecutive rows no longer step by one bottle's
  determinands (the commonest gap between neighbouring rows now occurs 5 times in 127 at Kilgarron). (b) Tirneevin's report
  printed an empty result column for its below-limit results: fixed, it prints the limit with its
  qualifier. (c) Withdrawn and re-issued results shown as approved in the reports: harmless, the reports
  are dated 20 January 2026 and list results as issued then. (d) Times on a five-minute grid and a
  uniform programme: harmless, field sheets record to five minutes and a programme is uniform by design.
- **Q8, the ortho-phosphate count.** No sentence tells the analyst how to count the samples or what to
  correct (the devices are silent). The readings it offers, ruled: the qualifier against a comparison of
  each value with its method's limit converges, no quantified result sits below its own limit (asserted
  in `checks.py`); samples held against samples required is settled by the request's words ("the
  compliance samples the year holds an approved result for"); results as approved at the year's end
  against as the export holds them moves one MCPA and three ortho-phosphate results approved after 31
  March 2026, and no cut-off at the year's end is filed anywhere, so the return reads the export as
  extracted, the call's own convention.

**Re-check after the judge's second pass (2026-11-01).** The judge's findings were fixed in data alone:
each compliance point's nutrient bottle now carries the collection date and time of the point's
pesticide sample that month, the two operational points that share a Tirneevin code are never sampled
on the compliance point's visit day, the reissued ortho-phosphate batches carry no withdrawn status, and
the reports list their rows by client point and date. No sentence under `target/` or in the prompt was
added or reworded (the method schedule's nitrate note was removed, a removal), so under the leak-check
rule `leak.py` alone re-ran on the final cut (target.zip f2c0b70568a20c9a): REVIEW on the same four
sweep-4 lines, each the domain's own nouns, and no LEAK.

