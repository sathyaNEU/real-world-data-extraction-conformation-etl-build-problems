# leak check, task403

**Verdict: REVIEW.** 14 files read, 28 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: calendar, runway, season, release, trialist, catalogue, change, charge, control, content, viewing, nothing, standard, register, subscription, root-cause, decision, family, channel, decisive, weekly, toronto, notice, golden, airing

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `conversion_standard_v3.pdf`: 6 of 25 stump-paragraph terms appear (change, charge, viewing, standard, subscription, toronto); read whether the document names the move
- **REVIEW** `price_notice_PP-2025-07.pdf`: 6 of 25 stump-paragraph terms appear (change, charge, standard, subscription, toronto, notice); read whether the document names the move

## 8 column names (REVIEW 1)
- **REVIEW** `trial_register.csv`: columns a generator names and an organisation does not: signup_device

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `release_calendar.xlsx`: 10 ISO dates after 2026-03-09, e.g. 2026-04-03, 2026-04-10, 2026-04-17, 2026-04-24, 2026-05-01

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 11 prompt gate (clean)


## Solver's-eye read

### Round 1 (stage 4, target.zip c80ea809, one isolated reader at medium effort), and the main thread's rulings

- Q1 none: the closest sentence is the programme sheet's valuation line, which names the valuation basis and that the
  causes account for the fall once, not how the fall is apportioned. Ruling: no decisive-step sentence.
- Q2 none: no file ranks or scores the programmes (the paid media sheet shows spend and platform-reported starts).
- Q3 the conversion standard and the two crosswalks, read as ordinary organisational documents. Ruling: harmless.
- Q4 none: the programme costs and the slate's "Yes, if Gravel & Gold locks by July" read as context.
- Q5 the standard's section 4 (paid: the first charge collected within the retry schedule that applied at the due
  date), section 6 (the winter's trials against the same months a year earlier) and section 2 (the seven-day trial,
  the Toronto-time month), and the sheet's valuation basis. Ruling: each executes to the golden's population, outcome
  and comparison.
- Q6 an analytical choice: how the winter's fall is apportioned among the four causes and the residual. Ruling: rule 3
  holds; the judge's Gate H reads the same (analytical).
- Generated patterns: none beyond a weekly release schedule and consistent identifier shapes, both read as plausible.
- REVIEW `signup_device`: harmless, an ordinary sign-up attribute naming no method or answer.
- REVIEW the calendar's dates after 2026-03-09: harmless, scheduled releases a content calendar holds.

The fix pass that followed changed one document the call reads (the programme sheet's Funding line), so round 2 reads
again on target.zip 08a813d0.

### Round 2 (stage 4, target.zip 08a813d0, one isolated reader at medium effort), and the main thread's rulings

- Q1 none: the closest sentences are the standard's sections 4 and 5 (a plan change does not end the trial; each
  episode counts once in a trial, in either language), which define data, and the programme sheet's sentence that the
  valuations account for the fall once, which says the decomposition reconciles, not how. Ruling: no decisive-step
  sentence.
- Q2 none: the programme sheet lists the four programmes with costs and no valuation or rank.
- Q3 none clearly: the standard and the programme sheet read as governing documents; the release log and the paid
  media sheet as context. The paid media sheet's note that platform-reported starts are not the register names no
  method. Ruling: harmless.
- Q4 none: prices, costs and the slate's "Yes, if Gravel & Gold locks by July" read as context.
- Q5 the programme sheet's valuation line fixes the population (trials started 1 November 2025 to 31 January 2026), the
  outcome (paid conversions lost to each programme's cause) and the comparison (the same months a year earlier), not the
  attribution; the standard's sections 2 to 6 fix trial, paid, episode played and winter. Ruling: each executes to the
  golden's population, outcome and comparison.
- Q6 an analytical choice: how the winter's fall is apportioned among the four causes and what none addresses. The
  release log's heartbeat entries read as ordinary organisational notes. Ruling: rule 3 holds; the judge's Gate H reads
  the same (analytical).
- Q7 the Funding line ("one programme from the subscriber growth budget, the one with the highest valuation; none this
  cycle only if no programme's cause cost the 2025-26 winter's trials paid conversions") settles that one programme is
  funded by its valuation, rules out choosing by cost, and names no method. It leaves the valuation itself open, which is
  the analysis. Ruling: the funding fork (SF19) is closed; the runner-up is the next valuation, the prompt's own term, and
  the "In place for 1 Nov 2026" column stays context.
- Generated patterns: weekly Friday 00:00 releases with 37 to 57 minute runtimes, UUID shapes and smooth paid media
  figures, each read as plausible. Ruling: harmless.
- REVIEW `signup_device`: harmless, an ordinary sign-up attribute.
- REVIEW the calendar's dates after 2026-03-09: harmless, the scheduled Gravel & Gold slate a content calendar holds.

Final cut: `leak.py --asof 2026-03-09` REVIEW with no LEAK (the same four lines, each answered above and in the design
note); both reads clean on the main call.
