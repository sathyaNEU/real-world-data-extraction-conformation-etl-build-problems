# leak check, task134

**Verdict: REVIEW.** 15 files read, 41 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: booking, puerto, person, booked, detainer, removal, address, window, deaths, follow-up, estimator, adopted, projection, points, districts, population, removals, bookings, replaced, probability, decisive, censoring, kaplan-meier, reading, rating

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `cjp_26-014_cover_note.txt`: 11 of 25 stump-paragraph terms appear (booking, person, booked, detainer, removal, address); read whether the document names the move
- **REVIEW** `commissioners_court_order_2023-118.pdf`: 5 of 25 stump-paragraph terms appear (booking, person, booked, population, bookings); read whether the document names the move
- **REVIEW** `ojg_rng-27-01_application_guidance_fy2027.pdf`: 8 of 25 stump-paragraph terms appear (booking, person, detainer, address, adopted, projection); read whether the document names the move

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

## 11 prompt form (clean)

## Solver's-eye read (round 1)

Reader verdict: no leak. It raised two determinism forks, five realism tells (four on the path to the requested numbers), eight lesser tells and four conventions to confirm, and the clone pre-flight (CLEAN) added two soft notes. All were fixed in the generator in repair r1 and the pack rebuilt: checks.py 6,291 assertions green, verify.py green, two scratch builds byte-identical to `target/`, `golden/` and `target.zip`. The golden is now 33 navigators (8, 8, 4, 6, 4, 3) for 7,441 projected returns, and R1 is still the decisive rung (37, Puerto 10).

### A. Determinism forks

- **A1, the window start.** Fixed. Order 2023-118 now carries one closing clause, "7. This order takes effect at 12:01 a.m. on 1 November 2023.", and ends "SIGNED AND ENTERED on 10 October 2023." over conformed signatures, so the October date reads as a signing; the state guidance states no date. The suggested tail "and governs every person booked on or after that time" was left out, because it would open a booked-date reading of a window guidance 4.4 defines on releases. The signing-date reading would add 630 releases, move Puerto -0.2, Norte -0.6 and Sur -0.4 points at 36 months, and change no navigator.
- **A2, returns after a removal.** Fixed. Guidance 4.2 now reads "A return is any later booking of the same person into the county jail on a new arrest or on a warrant, whatever happened between the release and that booking", with its exclusions for court commitments, transfers in and same-date bookings unchanged.

### B. Realism tells

- **B1 [PATH], every release placed in a precinct.** Fixed. 10.4 per cent of releases now carry an address code instead of a precinct (3.1 another Texas county, 1.2 another state, 3.3 another country, 2.9 no fixed address; legacy and JMS codes in the cover note): 25.4 per cent of transfers to ICE against 8.3 per cent of other releases, so most detainees keep local addresses. Guidance 4.5 puts an address outside the county in no district and no fixed address in the district the jail is in, which the adopted projection's note names (SD1 Puerto); both projections count releases by the same rule. Stump size kept: R1 asks for 37 against 33 (+4, floor 3) and 10 at Puerto against 8 (+2, floor 2).
- **B2 [PATH], removed people never come back.** Fixed in the simulation. 19 per cent of removals are followed by a return to the county and 9.1 per cent of people removed are booked again within three years of removal; 173 post-reform cohort releases ended in a logged removal and were booked again by the cut. A-Numbers are one per person; "reinstated order" sits only on log rows of people removed before (661 rows); ERO bonds come 1 to 8 days after the transfer and immigration-judge bonds 16 to 89 days (516 rows). The golden is now one minus Kaplan-Meier with the cut as the only censoring, equivalently the cumulative incidence with a Confirmed death as the only competing exit (the same figures to one decimal, exact and in 1,000 jittered fits). New rung R7, the cumulative incidence with removal and death as absorbing exits, asks for 32 (Puerto 51.6 per cent against 54.2, 7 navigators). The stump, ladder, closure table, checks.py and verify.py were rewritten to match.
- **B3 [PATH], merged duplicate SO numbers above the sequence.** Fixed. A duplicate legacy record takes the next SO number on the day it was opened, so the 384 MERGED DUP numbers sit inside the normal sequence (SO172933 to SO294316), each after the person's first number.
- **B4, ages.** Fixed. Releases are aged 17 to 76, 1.6 per cent of them 17, and nobody is booked after 76.
- **B5 [PATH], every commitment a weekend.** Fixed. Court commitments are now weekend series, straight sentences of 5 to 365 days, fines laid out and the rest of a weekend sentence after a failure to report: of 3,801 commitments released, 2,336 leave on a weekend release, 1,434 on time served and 31 to ICE. A failure to report picked up on a capias is a warrant booking, and a return.

### Lesser tells

- **Booking numbers.** Fixed. Numbers are issued when a booking is entered: voids leave 219 legacy and 200 JMS numbers unused, and 1,318 bookings were entered two or more hours after a later-booked one; the cover note explains both.
- **The detainer log.** Fixed. Month totals are live COUNT formulas (61 months, plus each fiscal year) with the values Excel caches; the log misses 63 transfers and enters 43 twice, every row still links to one release to ICE through the identifiers the cover note lists, and the note says Jail Records has not checked the log against the IC / 51 rows. No golden figure reads it.
- **Long holds.** Fixed. 211 releases come more than 365 days after their booking in the extract (pretrial holds on F1 to SJ new arrests, median 190 days, capped at 1,300).
- **23:59 stamps.** Fixed. The cap is gone; 12 releases are stamped 23:59.
- **Personal-bond times.** Fixed. From the reform, personal bonds come out after the 8 a.m. and 8 p.m. dockets: 92.6 per cent of post-reform personal-bond releases fall between 8 a.m. and noon or 8 p.m. and midnight.
- **Pretrial caseload.** Fixed. New cases are about 72 per cent of personal bonds plus 7 per cent of surety and cash bonds, opened 1 to 11 days after release, with closures, so they no longer equal personal-bond releases by district and month.
- **Workbooks.** Fixed. Every xlsx is written in Excel's own layout (shared strings, styles, formulas where a person types them with cached values, a calculation chain, the Office theme, properties naming Microsoft Excel and the fiction's authors and dates); the application workbook computes projected returns, navigators and the county totals by formula.
- **PDFs.** Fixed. The guidance (45 KB) and the order (47 KB) are word-processor documents exported by LibreOffice Writer with the Liberation fonts embedded as TrueType; the order carries a conformed signature block (County Judge, four commissioners, the Clerk's attestation, seal); the metadata names LibreOffice (7.6 on the 2023 order, 24.2 on the 2026 guidance) and creation instants inside the fiction.

### C. Clone pre-flight notes

- **Carrier phrase.** Fixed. The sentence now reads "Work from Julie Houston's extracts, the guidance and the adopted projection."; the rest of the prompt is unchanged word for word, and voice-check flags no carrier.
- **Dictionary name.** Fixed. `jail_extracts_readme.txt` is now `cjp_26-014_cover_note.txt`, Jail Records' cover note to the planning office's data request CJP-26-014, and every reference moved with it (generator, checks, submission step 1, metadata, design note).

### D. Conventions confirmed after the rebuild

- **Probable deaths.** Hold. The cover note's "County statistics use Confirmed matches only." excludes them, and the Kaplan-Meier form reads no death at all; with Probable matches the death-competing form would show Sur at 60.8.
- **Pending ICE dispositions (123 rows).** Hold. No ICE outcome, pending, bond or removal, ends or censors a release's follow-up, so they change nothing.
- **Ties.** Hold. Events are taken with same-day censorings at risk; the death-competing form, exact and in 1,000 jittered fits (the first build's 60 among them), rounds to the golden in every district and horizon. Censor-first ties, which no library uses by default, would move a figure by up to 0.069 points and are not claimed.
- **Chart month.** Hold. Month m is day round(m x 1,095 / 36), chart only.

## Solver's-eye read (round 2)

Read on the repair r1 cut, before the pre-round rework. Its findings are summarised here from the pre-round brief, with the disposition of each.

### A. Determinism forks

- **A1, the main call: "booked again" against the guidance's "return".** Fixed in the pre-round rework. The prompt said "booked back into the jail" and "booked again", while guidance 4.2 counts only new-arrest and warrant bookings as a return; counting court commitments and transfers in as well gives 7,961 returns and 35 navigators against the golden's 7,441 and 33. The prompt now carries only the guidance's own term ("projected returns", "return probabilities"), and checks.py asserts that the any-booking reading lands off the call on the navigator vector, the total and the returns.
- **A2, the 12- and 24-month estimator fork.** Deferred to the repair after a round the solver misses (`pipeline.json`, deferred).
- **A3, the monthly life table.** Deferred. It concerned the return-curves chart, which the prompt no longer asks for; kept on the deferred list as the brief directs.

### B. Realism tells

- **Concurrent bookings, the generic guidance, the daily population, the death linkage's tidiness, the timing rules.** Deferred to the repair after a round the solver misses; none of the pre-round changes touches them.

### C. The pre-round rework, for the next read

- No document under `target/` changed: the 14 files the pack shipped are byte-identical (sha256 asserted in checks.py). One data file was added, `pretrial_assessments_export_20261103.csv` (Pretrial Services' assessment export, 57,108 rows), which only the ask reads.
- The prompt was rewritten (941 characters, rule-first) and the ask moved off the call onto that export. The next read covers the prompt and that file.

## Solver's-eye read (round 3, targeted)

Read on the pre-round cut, covering the rewritten prompt and the one new file (`pretrial_assessments_export_20261103.csv`); no other document under `target/` changed.

### Questions 1 to 4

- **Q1, decisive step named:** none. The request's "return probabilities at 12, 24 and 36 months" names no method; guidance 4.4 says only that the probability is estimated from the county's own releases. That almost no release can show 1,095 days of follow-up is left to inference.
- **Q2, figures stated or ranked:** none. The adopted projection carries district release totals (inputs); the caseload and pilot files are context; the export carries no release, district or count field.
- **Q3, a file that exists only to help:** none. The export reads as an ordinary case-management export, and order 2023-118 item 1 is its reason to exist.
- **Q4, an answer-like figure or name:** none. "SD1 Puerto, the district the county jail is in" is a pinned convention.

### The main call

- **"Return": no divergence.** Guidance 4.2 decides it (a return falls on a date after the release; a court commitment or a transfer in is not one), which settles the 190 same-day warrant rebookings. The windows are 4.4's 365, 730 and 1,095 days. Identity is pinned by the cover note's crosswalk and MERGED DUP. The release set and the district rule are pinned (4.1, 4.4, 4.5, the order's effective time, the projection's no-fixed-address line).

### Ask-level forks (deferred to the post-round repair)

- **Which assessment.** Initial against latest-before-release differ on about 1,500 releases; only the request's "left the jail rated" speaks to it.
- **Assessments completed after release.** 10,437 rows; initials completed after release rise from about 1 per cent to over 10 per cent from March 2025, after a 28 February to 3 March gap. The reader weighed counting them against leaving 2,655 releases unrated and did not read the hosted clock.
- **Completed in the release minute.** 11 releases (10 in one district), at-or-before against strictly before.
- **Never assessed.** Court commitments, transfers in and pre-order bookings fall outside the three counts; whether to add a fourth column is open.
- **Blank booking numbers.** 1,167 rows; person number plus booking date resolves each one uniquely (612 releases).

### Realism tells (deferred)

- `assessment_id` is contiguous and strictly in completion order.
- Every join resolves with zero residue.

### Disposition

No leak-level finding and no fork on the main call, so nothing is fixed before the round. The five ask-level items and the two tells go on the `deferred` list for the post-round repair.
