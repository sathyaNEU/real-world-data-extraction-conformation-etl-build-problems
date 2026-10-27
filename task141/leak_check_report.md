# leak check, task141

**Verdict: REVIEW.** 14 files read, 24 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: record, end-of-term, extension, petition, maximum, capped, window, architecture, petitions, decisive, golden, question, forecasting, nothing, detention, already, extensions, booking, orders, counts, analytical, domain, forecast, center, standard

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `jail_operations_plan_instructions_2027.pdf`: golden figure 210 appears: ...22 Okelan County pod of 64 beds one unit for each 210 felony probation revocation admissions projected...
- **REVIEW** `jail_operations_plan_instructions_2027.pdf`: carries 12 of 13 distinctive words of the committed call: "Okelan County's 2027 Jail Operations Plan should staff 7 violator pods (448 beds) for felony probation revocation admiss"

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `apd_annual_report_2025.pdf`: 3 of 25 stump-paragraph terms appear (petition, petitions, counts); read whether the document names the move
- **REVIEW** `jail_operations_plan_instructions_2027.pdf`: 4 of 25 stump-paragraph terms appear (record, orders, counts, standard); read whether the document names the move

## 9 dates after the setting (REVIEW 2)
- **REVIEW** `circuit_court_term_orders_2016_2026.csv`: 2461 ISO dates after 2026-10-16, e.g. 2026-10-17, 2026-10-18, 2026-10-19, 2026-10-20, 2026-10-21
- **REVIEW** `cms2_supervision_cases_2023_2026.csv`: 10816 ISO dates after 2026-10-16, e.g. 2026-10-17, 2026-10-18, 2026-10-19, 2026-10-20, 2026-10-21

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read (architecture 4, stage 4, zip 4066ee80)

I read the prompt and the 14 files under target/. I computed nothing.

**1. Decisive step.** No sentence announces it. The documents file the estimand and the law:
- jail_operations_plan_instructions_2027.pdf 4.2: "The projection counts every admission the plan year will see, including admissions on terms whose supervision begins after the extract."
- jail_operations_plan_instructions_2027.pdf 4.1: "Project the plan year's felony probation revocation admissions under the law in force in the plan year, with the courts, the probation department and the sheriff acting as the county's records to the extract show them acting."
- sb26_118_felony_probation_term_act.pdf, Section 4: "expires on the earlier of its scheduled expiration and the day 24 months after supervision on it began; but no term expires under this section before 31 March 2027."

These say that a projection under the cap is needed and that future-starting terms count. They do not say how to project, which model to use, or what the revocation hazard depends on. Nothing names a method, a hazard, a back-test or a pitfall.

**2. Ranking, scoring or forecasting file.** None. No file projects admissions, pods or bed-days. apd_annual_report_2025.pdf has FY2025 totals (846 felony revocations, 7,602 felony probationers), which are context for one past year, not the quantity asked.

**3. Files that exist only to help the analyst.** None clearly. The code tables (circuit_court_codes.xlsx, jms_booking_codes.csv, apd_office_codes.csv) are ordinary agency lookups. person_id_crosswalk.csv is a plausible cross-system key file. detention_daily_headcount_2025_2026.csv (06:00 counts by unit, not the 00:00 bed-day basis) and the annual report read as distractors, not helpers.

**4. Figure or name reading as the answer.** None. The only decision-linked numbers are the Okelan standard (one 64-bed pod per 220 admissions, or part of 220, filed 3 March 2021) and the other counties' standards. They are context. The other four counties' rows are Annex noise. The annual report's FY2025 counts are historical.

**5. Filed sentences that fix the computation, by what they fix:**
- jail_operations_plan_instructions_2027.pdf 2.2 and the Annex row for Okelan: pods = one unit per 220 projected felony admissions, or part of 220. This fixes the unit (pod of 64 beds) and the conversion from projected admissions to pods.
- 3.1: an admission is counted once per person on the day the court orders the commitment, however many terms were revoked that day. This fixes the unit of count and the date.
- 3.2: a felony admission is one where a term revoked is a felony term. Warrant holds and holds for another state are not admissions. This fixes the population.
- 4.1 and 4.2: the plan year is 2027, under the law in force in 2027. It includes admissions on terms that begin supervision after the extract. This fixes the window and the population, including members not yet observed.
- 4.3: nearest 100, with the parts it is built from. This fixes rounding and asks for the build-up.
- 5.1 to 5.3: bed-days are persons in the jail at 00:00 county time serving a revocation commitment, in any building, dated to the day that begins at that midnight. A person held on both a felony and a misdemeanor term counts once, as felony. Warrant holds and holds for another state are excluded. This fixes the time point, the buildings, the felony/misdemeanor tie rule and the exclusions.
- 1.3: Central time.
- 6.1: probationers at the extract, per supervising office, in four time-on-supervision bands. This fixes the population and the bands.
- sb26_118_felony_probation_term_act.pdf Sections 2(2), 3, 4: supervision begins on release from any confinement condition. The 24-month cap applies to terms imposed on or after 1 Jan 2027. Terms in effect expire at the earlier of scheduled expiration and 24 months after supervision began, and not before 31 March 2027. Section 5 adds that no new extension order may exceed what sections 3 and 4 allow. Section 6 says pending proceedings continue after a term ends. Section 7 exempts misdemeanor terms. This fixes the cap rule, the supervision start date and the expiry date.
- apd_annual_report_2025.pdf notes: a probationer is counted once per open term. This is a counting convention, not a fixed method.

**6. What decides the main answer.** From the pack alone it looks like an analytical projection decided by structure, with rule application and data semantics around it. The deciding structure is how felony revocation admissions depend on time on supervision (hazard against supervision tenure), and how the 24-month cap and the 31 March 2027 floor cut that exposure. The pack gives the cap as a rule (SB 26-118 s.3 to 4) and 4.2 requires terms that begin after the extract. Nothing in the pack says how to estimate the hazard, whether it varies by tenure, or what window to use. The sentences that make a projection necessary are 4.1, 4.2 and Section 4. The elements the solver must get right are CMS1/CMS2 stitching, the crosswalk merges, supervision start versus release from confinement, and term orders for extensions and tolling. These are Layer 1 mess and do not decide the call. I see no planted memo, decoy or hidden rule. One caution: the stated rules (Section 4 expiry, the 220 and 64 standard) are fully specified, so if the projection reduces to applying them to a count, the call would be rule application. I cannot tell from the pack alone.

**Sweep lines**
- (a) jail_operations_plan_instructions_2027.pdf flagged by the answer-figure sweep: **harmless**. The only figures are the county pod sizes and per-pod thresholds (64 beds, 220, and the other counties' values), which are the filed standard and not the answer. No admissions, pod count or bed-day result appears.
- (b) Dates after 16 October 2026 in circuit_court_term_orders_2016_2026.csv and cms2_supervision_cases_2023_2026.csv: **harmless**. The latest order_date, filed_date, supervision_begin and closed_date are all 2026-09-30. The later dates are only scheduled expirations (expiration_before, expiration_after, expiration_date), which are forward-looking by nature (about 1,586 term-order rows and 10,574 CMS 2 rows). No event is dated after the extract.

**Realism tells**
- detention_probation_bookings_2019_2026.csv has booking numbers from 2018 (B18000001) with release dates on 01/01/2019. These are carry-over records, consistent with the "CONVERTED TO NEW JMS" release reason. It is plausible, and not a tell.
- The three CSV families use different date formats (MM/DD/YYYY, ISO, DD-MON-YYYY) and different column naming (upper-case CMS1, lower-case CMS2). This reads as real system differences.
- The pods in the Annex have round, neat ratios (160, 190, 220, 200, 150). A State Board table listing five counties is a little tidy but not implausible.
- apd_annual_report_2025.pdf and the SB 26-118 and instruction PDFs are very clean and short. The statute is notably brief, with a one-line Section 6 and a tidy "Passed the Senate 21 April 2026" footer. A real enrolled bill is longer. This is a mild generated feel.
- File mtimes cluster on 2 Oct, with the PDFs on other dates (Jul 8, May 14, Oct 2025). Minor.
- The detention headcount's housing_unit has "V PODS 1-5", "SENTENCED" and "GENERAL POPULATION" mixed. Plausible.
- I found no hidden sheets, tracked changes or toolchain signatures in the xlsx (all sheets visible).

### The main thread's rulings on the read

- Question 1: nothing quoted; the sentences it lists (instructions 4.1 and 4.2, the Act's section 4) file the estimand and the law, not a method.
- Question 5: every sentence quoted fixes population, window, unit or conversion, and each executes to the golden's definitions (3.1 the order day, 3.2 the felony admission, 4.2 the terms beginning supervision later, 5.2 and 5.3 the bed-day, 6.1 the supervising office and bands, the Act's sections 3 to 7).
- Question 6: analytical; its caution (a projection that only applies the stated rules would be rule application) is answered by the ladder: every rule executed on the pooled projection files 886, five pods.
- Sweep (a) harmless: the instructions carry the filed standard only. Sweep (b) harmless: the post-setting dates are scheduled expirations.
- Realism: the Annex's round standards are what a board files (harmless); the enrolled Act read short, so a legislative declaration in section 1 and a safety clause were added, with no section renumbered and no rule changed.

## Solver's-eye read (architecture 4, stage 4 round 2, zip 2b591366)

Nothing was computed. I read the prompt, both PDFs, the code xlsx (all 7 sheets visible, none hidden) and the head, tail and column lists of every CSV.

**1. Which sentence or file names the decisive step?**
No sentence names it. The nearest candidates are all statements of context or definition.
- SB 26-118 s.4 (sb26_118_felony_probation_term_act.pdf): "A felony probation term in effect on the effective date of this Act expires on the earlier of its scheduled expiration and the day 24 months after supervision on it began; but no term expires under this section before 31 March 2027." This is the rule that fixes how the cap bites, but it does not say how the projection should be built.
- The instructions (jail_operations_plan_instructions_2027.pdf) s.4.1: "Project the plan year's felony probation revocation admissions under the law in force in the plan year, with the courts, the probation department and the sheriff acting as the county's records to the extract show them acting." This says what to project. It does not say how to model the behaviour.
- s.4.2: "The projection counts every admission the plan year will see, including admissions on terms whose supervision begins after the extract." This is a scope sentence. It hints that future supervision starts count, but gives no method.
Nothing says how revocation timing is modelled, for example hazard by time on supervision, a compression into the first 24 months, or a before/after comparison of cohorts. A careful reader will see "24 months from supervision start, with a floor at 31 March 2027" and "terms that begin after the extract" as the relevant machinery. That is the domain setup, not a pointer to the answer.

**2. Which file already ranks, scores or forecasts the quantity?**
None. There is no projection, forecast or ranking of admissions, pods or bed-days anywhere. apd_annual_report_2025.pdf has FY2025 counts only (846 felony and 293 misdemeanor revoked terms, 7,602 felony probationers). These are history for a different window, and the report counts terms, not admissions.

**3. Which file exists only to help the analyst?**
- person_id_crosswalk.csv, jms_booking_codes.csv, apd_office_codes.csv and circuit_court_codes.xlsx are the usual reference and key tables. Each could plausibly exist in a county's records, and each is needed to join or decode the others. The crosswalk, with its CURRENT and MERGED status and merged_into/merged_on columns, is a join aid, but a county's systems do hold such a table.
- detention_daily_headcount_2025_2026.csv is a daily count by unit, "persons_at_0600", and is not a bed-day count at midnight. It is a relevant-but-different measure, a likely distractor, and it does not look analyst-made.
None of the files reads as analyst-only.

**4. Which figure or name reads as the answer?**
None. The county standard (one pod of 64 beds per 210 admissions, or part of 210, filed 3 March 2021) is an input to the pod count. It is not the answer. The annex lists four other counties with other standards, which is plausible context. Table 2 in the annual report gives FY2025 revoked terms, which are history and not the 2027 figure. No file carries a 2027 number.

**5. Filed sentences that fix how the main figure is computed or over which population**
- Instructions s.3.1: "An admission is a person's commitment to the county jail on the revocation of a probation term the county probation department supervises. It is counted once, on the day the court orders the commitment, however many of the person's terms the court revoked that day." This fixes the unit (person-day of commitment, not terms) and the date (the order date).
- s.3.2: "An admission is a felony probation revocation admission when a term revoked is a felony probation term. Holds on a violation warrant before the court decides, and holds for another state, are not admissions." This fixes the population (felony-term revocations only; PV-HOLD and PV-OOS excluded).
- s.4.1 and s.4.2, quoted above. These fix the window (calendar 2027), the legal regime (the law in force in 2027) and the inclusion of terms that start after the extract. The behaviour of the actors is left to be inferred from the records.
- s.4.3: "State the projection to the nearest 100 admissions, with the parts it is built from." This fixes the rounding and asks for a decomposition.
- Annex, Okelan row: "one unit for each 210 felony probation revocation admissions projected for the plan year, or part of 210", pod of 64 beds. This fixes the pod rule as a ceiling of projected admissions over 210. The prompt's "how many of those admissions should the plan carry" refers to the rounded projection.
- SB 26-118 s.2(2): "Supervision on a term begins on the day the probationer is placed under the department's supervision on that term, which for a term with a confinement condition is the day of release from the confinement." This fixes the clock start for the 24 months.
- SB 26-118 s.3, s.4, s.5 and s.6 fix the cap (24 months from supervision start for new terms; the earlier of scheduled expiration and 24 months for terms in force, with no expiry before 31 March 2027; no later extension past the cap; pending proceedings continue).
- s.5.2: "A violator bed-day is counted for each person in the jail at 00:00 county time serving a commitment the court has ordered on the revocation of a probation term, in any of the jail's buildings, and is dated to the day that begins at that midnight. A person serving a commitment on weekends is counted at each midnight spent in the jail." This fixes the unit, the instant, the buildings and the weekend treatment.
- s.5.3: felony versus misdemeanor, with a mixed-term person counted once, as felony. Warrant and other-state holds are excluded.
- s.1.3: "Dates and times in a plan, and county time in these instructions, are Central time." This fixes the time zone. The newer bookings are in UTC, so conversion is needed.
- s.6.1: felony probationers at the extract, by office, in four time-on-supervision bands (under 1 year, 1 to under 2, 2 to under 3, 3 or more).
- Code table note: "No order imposing or extending a term may set it longer." (the longest term by class). This is context on term lengths.

**6. What decides the main answer?**
As far as I can tell without solving, it is an analytical choice. The rules (the 24-month cap, the 31 March 2027 floor, the clock start, the admission definition, the 210 divisor) are all stated. The records (petitions, term orders, CMS cases, bookings) must be joined, and the admissions must be projected under a changed term length. That needs a view of when in a term revocations occur and how a shortened term shifts or removes them. The file set does not tell you the shape of that timing, so the solver has to choose and justify a way of estimating it. An easy route is a historical average or an annual trend, or just a count of cases whose expiry the cap pulls in. The prompt does not point to either route. Execution of the stated rules is needed but does not settle the call. I see no planted decoy on the main call. The annual report gives FY2025 term counts, which would mislead only a solver who used terms as admissions. The daily 06:00 headcount is a nearby measure, but the definitions in s.5.2 exclude it. Those are weighable context, and I do not read them as the decisive step.

**(a) The answer-figure sweep flagged jail_operations_plan_instructions_2027.pdf: harmless.** The only figures in it are the filed standards (210, 64, the other counties' divisors and pod sizes), dates and section numbers. These are inputs. The Okelan row is a divisor and not a result, and no projection, pod count or bed-day figure appears.

**(b) The dates sweep flagged circuit_court_term_orders_2016_2026.csv and cms2_supervision_cases_2023_2026.csv for dates after 16 October 2026: harmless.** Every event date is on or before 30 September 2026 (the latest order_date and supervision_begin are 2026-09-30, and no closed_date is later). The later dates are only scheduled expirations (the term order file's expiration_before and expiration_after, up to 2033-09-19; the CMS 2 expiration_date, up to 2033-09-19). These are forward-looking dates a real system holds for open terms, not events after the extract.

**Realism tells**
- Mixed date formats across the bookings file. The pre-conversion rows use "02/05/2018 13:09" local time with booking numbers like B18000001, and the later rows use ISO UTC with numbers like OK2026004122. This is a plausible system conversion (the release reason CONVERTED TO NEW JMS supports it). It is a real-looking Layer 1 mess and I do not count it as a tell.
- Mixed formats across CMS 1 (upper-case column names, MM/DD/YYYY, single-letter office codes) and CMS 2 (ISO dates, snake_case, office codes via apd_office_codes.csv). This is plausible for a migration.
- circuit_court_term_orders order dates start 2016-07-01, 2016-07-02, 2016-07-03 on consecutive days in the first rows. This looks like a sort by date and not like a tell.
- The file modification times of the CSVs (1 to 2 October) are close together and out of order against the content dates. This is minor and not visible in file content.
- The instructions PDF and the Act PDF carry only plain metadata (no creator or producer). This is clean.
- The annual report is dated October 2025 (file time) with figures to 31 August 2025, which is consistent.
- Nothing reads as planted, announced or "for a test". The most test-shaped item is the instructions PDF being an unusually tidy single-purpose document that restates every definition the task needs, but a state board's county instructions plausibly do that.

### The main thread's rulings on the second read

- Question 1: nothing quoted; section 4 of the Act and instructions 4.1 and 4.2 file the law and the estimand.
- Question 5: each sentence fixes population, window, unit, rounding or the standard; the weekend clause added to 5.2 fixes a count the definitions already implied.
- Question 6: analytical; no planted decoy on the main call.
- Sweeps (a) and (b) harmless, as in the first read. Realism: no tell; the instructions restate their definitions as a board's instructions do.

## Solver's-eye read (architecture 4, stage 4 round 3, zip 9d45538d)

I read prompt.txt and the 14 files under target/ (13 data and document files plus the code workbook, whose 7 sheets are all visible; none is hidden). I computed no figures.

**1. Decisive analytical step.** No sentence or file names it. The prompt asks for pods and admissions "once SB 26-118 caps felony supervision at 24 months". The instructions PDF says only "Project the plan year's felony probation revocation admissions under the law in force in the plan year, with the courts, the probation department and the sheriff acting as the county's records to the extract show them acting" (jail_operations_plan_instructions_2027.pdf 4.1) and "The projection counts every admission the plan year will see, including admissions on terms whose supervision begins after the extract" (4.2). These file the estimand (law in force, plan year, new terms included). They do not say how to model it. Nothing says how to estimate the revocation hazard by time on supervision, or how revocations behave when terms are cut off. SB 26-118 sections 3 and 4 are the law itself, written as a statute.

**2. Ranks, scores or forecasts the quantity.** None. The APD annual report gives FY2025 counts only. The headcount file is a plain daily count by housing unit. No file projects 2027.

**3. Exists only to help the analyst.** None found. Every file is plausible in the county's records: the court codes, the office codes, the JMS code table, the crosswalk, the officer assignments, and the State Board instructions with the Annex. The officer assignments file and the annual report are probably the distractors. The office codes file is a real lookup, since EFD (Eastfield) exists only there.

**4. A figure or name that reads as the answer.** None. The pod standard (one unit per 210 admissions, 64 beds) is a filed county standard, which is context. No figure in the pack is a 2027 admissions count or a pod count.

**5. Filed sentences that fix the figure.**
- Instructions 3.1: an admission is counted once, on the day the court orders the commitment, however many terms were revoked that day. This fixes the unit and the date of the count.
- Instructions 3.2: an admission is felony when a term revoked is a felony term. Warrant holds and holds for another state are not admissions. This fixes the population.
- Instructions 4.1 and 4.2: the law in force in the plan year; every admission in the plan year, including those on terms beginning after the extract. This fixes the population and the window.
- Instructions 4.3: nearest 100 admissions, with the parts shown.
- Instructions Annex, Okelan row: "pod of 64 beds; one unit for each 210 felony probation revocation admissions projected for the plan year, or part of 210". This fixes the rounding up of pods, and the comparison is pods against the projected admissions.
- Instructions 5.2 and 5.3: a bed-day is a person in the jail at 00:00 county time on a revocation commitment; weekend sentences are counted at each midnight spent in jail; a person on both felony and misdemeanor commitments counts once, as felony. This fixes the unit, the clock and the dedup rule for the bed-day asks.
- Instructions 6.1: felony probationers at the extract, by office and by four bands of time on supervision. This fixes the population and the bands for the grid ask.
- Instructions 1.3: Central time.
- SB 26-118 section 2(2): supervision begins on the day of release from confinement, for a term with a confinement condition. This fixes the clock start.
- SB 26-118 section 3: terms imposed on or after 1 January 2027 expire no later than 24 months after supervision begins. This fixes the cap for new terms.
- SB 26-118 section 4: the earlier of the scheduled expiration and the later of 24 months after supervision began and 31 March 2027. This fixes the new expiry of terms in force.
- SB 26-118 section 5: extension and tolling after 1 January 2027 cannot push the expiry past the section 3 and 4 date.
- SB 26-118 section 6: pending proceedings continue after a term ends.
- Court codes workbook: the offense-class maximum term table, and "No order imposing or extending a term may set it longer."

**6. What decides the main answer.** From what is filed, an analytical choice decides the main number. The solver must estimate how revocations arise over time on supervision, then apply the cutoff to the open terms and the new terms, and handle the path where revocation is the exit. The rules are filed, but the revocation hazard is not stated anywhere. A solver who simply drops the admissions that would fall after the cutoff, or who treats the history as the plan year, could file a wrong answer. The semantic points (the bed-day clock, the weekend sentences, the dedup, and joining the crosswalk) look like they feed the asks, not the main call. I saw no planted decoy deciding the main call and no sentence announcing the step. One residual risk: sections 4 and 6 together with instruction 4.2 are a rule-application ladder, and whether the main call survives as analysis rather than execution cannot be judged without solving.

**Mechanical sweep lines**
- (a) jail_operations_plan_instructions_2027.pdf: harmless. The 210 is the county's filed standard, which is context. The shared words about admissions to carry and pods to staff are the prompt and the instruction restating the same ask. The instruction gives the standard, not the projection. apd_annual_report_2025.pdf: harmless. 206 is the FY2025 count of felony early terminations (Table 3). 210 is the count of felony petitions dismissed (Table 2). Neither is a 2027 figure and neither is a pod count. They are coincidental matches to the standard.
- (b) Dates after 16 October 2026: harmless. circuit_court_term_orders_2016_2026.csv has no order_date after 30 September 2026. The flag comes from the expiration_before and expiration_after columns, which run to 2033. These are scheduled expiries of terms in force, forward-looking by nature, and every term's expiry is a future date. cms2_supervision_cases_2023_2026.csv has no supervision_begin or closed_date after 30 September 2026. The flag comes from expiration_date, which runs to 2033 for open terms. Both are normal scheduled expiry dates and no record from after the extract is present.

**Realism tells**
- apd_annual_report_2025.pdf: the PDF Author metadata is a person's name, which is fine, and the producer is blank. The creation date is 15 October 2025 for a report on counts as at 31 August 2025, which is plausible. Table 2 totals (1,617 felony, 686 misdemeanor) differ from the petitions filed (1,593, 690), and the Notes explain this. Not a tell.
- The report's tables and text are very tidy (all rows sum exactly). The fonts are Carlito (a LibreOffice default for Calibri) with an unembedded Helvetica, which hints at a LibreOffice export rather than a county Word export. Minor.
- The CSV file timestamps show 1 to 2 October (mtime), within a day of the extract, all produced at once. A county would not export 8 systems within hours, but this is a filesystem artefact and not content.
- Mixed date formats across systems (CMS 1 uses MM/DD/YYYY, the officer file uses DD-MON-YYYY, the others use ISO) are plausible Layer 1 mess and read as authentic.
- The bookings file starts 2018 despite its name "2019_2026" and holds 'CONVERTED TO NEW JMS' release rows. This is plausible conversion mess and reads as authentic.
- The code workbook and the SJSB instructions are clean and short, but nothing in them reads as written for a test. The fixed, tidy county standard table of five counties with neat round thresholds is a mild tell, but it is a plausible standards annex.

### The main thread's rulings on the third read

- Question 1: nothing quoted; the restated section 4 and instructions 4.1 and 4.2 file the law and the estimand, and nothing names a method, a rate split or a pitfall.
- Questions 2 to 4: no file ranks, scores or forecasts 2027; the 210 standard is the county's filed context.
- Question 5: each sentence fixes population, window, unit, rounding or the standard, as in the first two reads; the restated section 4 fixes each term's end under the Act and no longer reads as moving early 2027 expirations to 31 March.
- Question 6: analytical; the reader names no planted decoy on the main call. Its residual note (sections 4 and 6 with instruction 4.2 as a ladder of rules) is the filed estimand: executing those rules leaves the end-of-term rate a capped term files at open, which is the decisive step.
- Sweeps (a) and (b) harmless: 206 and 210 in the annual report are FY2025 early terminations and dismissals; the later dates are scheduled expirations. Realism: the tidy annual report fonts and the five-county standards annex are minor and stand as written.

## Solver's-eye read (architecture 4, stage 4 round 4, zip 2cea3299)

Files read: prompt.txt and all 14 files under target/ (3 PDFs, 1 xlsx with 7 visible sheets and no hidden ones, 10 CSVs). Nothing computed.

**1. Decisive analytical step.** No sentence names it. The prompt only asks how many pods to staff "once SB 26-118 caps felony supervision at 24 months". The nearest pointer is the instruction text "4.1 Project the plan year's felony probation revocation admissions under the law in force in the plan year, with the courts, the probation department and the sheriff acting as the county's records to the extract show them acting" (jail_operations_plan_instructions_2027.pdf). That says to project under the new law and to use observed behaviour, but not how. It names no method, model or back-test.

**2. Ranks, scores or forecasts the quantity.** None. The annual report (apd_annual_report_2025.pdf) gives FY2025 counts of revocations (847 felony) and stocks. These are history, not a forecast. The headcount file is a daily count by unit with no projection.

**3. Exists only to help the analyst.** None found. Each file reads as an organisational record: court code tables, the office code list, the officer assignments, the person-ID crosswalk, the JMS codes, the annual report, the State instructions and the Act. The crosswalk and codes are the ordinary mess that comes with merged IDs. detention_daily_headcount_2025_2026.csv (06:00 counts by housing unit) looks like an unused distractor, since the bed-day definition is at midnight.

**4. Figure or name that reads as the answer.** None. The only candidate is the Okelan standard in the Annex, "one unit for each 210 felony probation revocation admissions projected for the plan year, or part of 210". It is a conversion constant, not a result. The 847 in the annual report is FY2025 history and is not the 2027 figure.

**5. Filed sentences that fix the figure.**
- Instructions 3.1: "An admission is a person's commitment to the county jail on the revocation of a probation term... counted once, on the day the court orders the commitment, however many of the person's terms the court revoked that day." This fixes the unit (one per person per order day) and the date.
- 3.2: felony when a term revoked is felony. Warrant holds and out-of-state holds are excluded. This fixes the population.
- 4.2: "counts every admission the plan year will see, including admissions on terms whose supervision begins after the extract." This fixes the population as including terms not yet begun.
- 4.1: projection under the law in force in the plan year, with actors behaving as the records show. This fixes the legal basis and the behaviour.
- 2.2/4.3 with the Annex: one 64-bed pod per 210 projected admissions or part of 210. This fixes the conversion with a ceiling.
- 5.2: a bed-day is a person in jail at 00:00 county time serving a revocation commitment, in any building, with weekend sentences counted at each midnight spent in jail. 5.3: felony takes precedence, counted once. 1.3: Central time. These fix the bed-day unit and the time basis.
- 6.1: completed years from the day supervision began, in four bands, by office at the extract. This fixes the cross-tab.
- The Act, s.4: a term in effect "expires on the earlier of (a) its scheduled expiration and (b) the later of the day 24 months after supervision on it began and 31 March 2027". Section 2(2): supervision begins on release from confinement. Section 3 covers new terms. Section 5: no later order may extend past those limits. Together these fix the law the projection runs under.
- Prompt: the window is Oct 2025 to Sep 2026, records to 30 Sep 2026, and bed-days are in whole days.

**6. What decides the main answer.** From the pack, a mix of the analytical estimand and following the Act's rules. The pack never says how to turn the Act and the observed revocation timing into a 2027 admissions projection. That is left to the analyst (survival and hazard of revocation by time on supervision, applied to the stock and to new terms). The sentences that frame it are Instructions 4.1/4.2 and Act ss.3-5. The Act's rules are stated and mechanical. The bed-day and supervision-start definitions are stated and are not the stump. Nothing reads as planted: there is no decoy memo and no unstated rule.

**Verdicts on the mechanical sweep.**
- (a) jail_operations_plan_instructions_2027.pdf, pod standard of 210 and shared words: harmless. 210 is the filed conversion constant, not the admissions projection, and the "violator pods to staff" wording is just the prompt's question restated from the instructions' own section 2.2.
- (b) Dates after 16 October 2026 in circuit_court_term_orders_2016_2026.csv and cms2_supervision_cases_2023_2026.csv: harmless. All order_date, filed, supervision_begin and closed dates are at or before 30 Sep 2026. The later dates are only scheduled expiration fields (expiration_after up to 2026 and later, expiration_date up to 2033), which are legitimately forward-dated terms. No post-extract events are recorded.

**Realism tells.**
- Mild: the headcount file's housing unit "V PODS 1-5" is a short name that the prompt's "violator pods" echoes. It is plausible as a real unit name but slightly on the nose. It is a 06:00 count, so it cannot give the midnight bed-days.
- Mild: the annual report is a single page with three tidy tables, and its totals reconcile suspiciously cleanly.
- File mtimes cluster on a few days in October, but they are metadata only.
- Nothing else reads as generated. The state, county and bill names are fictional but consistently styled, and the CMS1 and CMS2 layouts differ the way real system migrations do.

### The main thread's rulings on the fourth read

- Question 1: nothing quoted; instructions 4.1 file the law and the behaviour to project under, not the method.
- Questions 2 to 4: no file ranks, scores or forecasts 2027; the 210 standard is the county's filed conversion.
- Question 5: each sentence fixes population, window, unit, the standard or the Act's ends, now with 4.3 asking the units the projection calls for and 6.1 the office at the extract in completed years.
- Question 6: analytical; the reader names no planted decoy, no unstated rule, and the method from the record to 2027 left to the analyst.
- Sweeps (a) and (b) harmless, as in the earlier reads. Realism: the jail's unit name "V PODS 1-5" is the Detention Center's own label for its violator housing, and the annual report's tables recompute from the shipped rows; both stand.
