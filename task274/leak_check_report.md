# leak check, task274

**Verdict: REVIEW.** 27 files read, 15 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: effect, resolution, outcome, decisive, disposition, window, records, terminated, recorded, completion, review, lottery, termination, months, reflex, method, provider, golden, asserted, architecture, causal, sentence, checks, randomised, participant

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `board_resolution_2025_31.pdf`: carries 6 of 7 distinctive words of the committed call: "We should renew Nethercote's pretrial diversion agreement for 2027 at the pilot's scale."

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `board_resolution_2025_31.pdf`: 5 of 25 stump-paragraph terms appear (effect, resolution, disposition, records, lottery); read whether the document names the move
- **REVIEW** `nethercote_services_agreement_2025.pdf`: 5 of 25 stump-paragraph terms appear (resolution, records, termination, months, participant); read whether the document names the move

## 8 column names (REVIEW 1)
- **REVIEW** `penal_code_conversion_table_2026.csv`: Python-style nulls or booleans (nan/None/True/False) in the first rows

## 9 dates after the setting (REVIEW 8)
- **REVIEW** `nethercote_reports/NCJS_Larkmoor_Participants_2026-01.xlsx`: 479 ISO dates after 2026-09-10, e.g. 2026-09-30, 2026-10-31, 2026-11-30, 2026-12-31
- **REVIEW** `nethercote_reports/NCJS_Larkmoor_Participants_2026-02.xlsx`: 586 ISO dates after 2026-09-10, e.g. 2026-09-30, 2026-10-31, 2026-11-30, 2026-12-31, 2027-01-31
- **REVIEW** `nethercote_reports/NCJS_Larkmoor_Participants_2026-03.xlsx`: 695 ISO dates after 2026-09-10, e.g. 2026-09-30, 2026-10-31, 2026-11-30, 2026-12-31, 2027-01-31
- **REVIEW** `nethercote_reports/NCJS_Larkmoor_Participants_2026-04.xlsx`: 808 ISO dates after 2026-09-10, e.g. 2026-09-30, 2026-10-31, 2026-11-30, 2026-12-31, 2027-01-31
- **REVIEW** `nethercote_reports/NCJS_Larkmoor_Participants_2026-05.xlsx`: 926 ISO dates after 2026-09-10, e.g. 2026-09-30, 2026-10-31, 2026-11-30, 2026-12-31, 2027-01-31
- **REVIEW** `nethercote_reports/NCJS_Larkmoor_Participants_2026-06.xlsx`: 1027 ISO dates after 2026-09-10, e.g. 2026-09-30, 2026-10-31, 2026-11-30, 2026-12-31, 2027-01-31
- **REVIEW** `nethercote_reports/NCJS_Larkmoor_Participants_2026-07.xlsx`: 1065 ISO dates after 2026-09-10, e.g. 2026-09-30, 2026-10-31, 2026-11-30, 2026-12-31, 2027-01-31
- **REVIEW** `nethercote_reports/NCJS_Larkmoor_Participants_2026-08.xlsx`: 1032 ISO dates after 2026-09-10, e.g. 2026-09-30, 2026-10-31, 2026-11-30, 2026-12-31, 2027-01-31

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 11 prompt gate (clean)


## Solver's-eye read

1. Decisive step. No file or sentence names a trap, but target/board_resolution_2025_31.pdf Section 3 states the estimand almost as a procedure: "the share of the defendants on the lottery lists who are convicted in the referred case at its final disposition, for those not offered a place less that for those offered one, in percentage points. Every defendant on a list counts, whether or not a defendant offered a place took it up and whether or not the case has reached its final disposition by 31 August 2026." That sentence tells the solver to analyse by offer (not by uptake) and to keep unfinished cases in the denominator. It is the closest thing to an announced decisive step. The lottery sheets' banner ("Places offered: 152 of 304 listed (Board Resolution 2025-31, section 2)") and the DVO/DVX/DVA event codes support it but do not announce it. Note the resolution does not say how an open case is scored (not convicted, or otherwise). The prompt itself says nothing about method.

2. No file ranks or scores the three options. The nearest is Resolution Section 5, which maps a reduction in points to renew-full (25 or more), pilot scale (15 to under 25) or lapse (under 15). It is a decision rule with no computed result. district_court_annual_statistics_fy2025.pdf and county_jail_population_2025_2026.csv carry no candidate ranking.

3. Helper-type files: legacy_event_codes.csv (code dictionary for the legacy docket), penal_code_conversion_table_2026.csv (2025 to 2026 section crosswalk), pretrial_diversion_policy_pdu_2026_01.docx (eligible-class table, A to E, sections 423.01 etc.), board_resolution_2025_31.pdf and nethercote_services_agreement_2025.pdf (governing documents; the agreement also says how program term and CS hours are set). There is no readme, manifest or notes file. These read as normal organisational documents, not as author explanations. The conversion table is a pure key map.

4. Nothing reads as the answer. No reduction, shares, counts or per-site totals appear anywhere. The only answer-adjacent figures are the Section 5 thresholds (25 and 15 points), which are context for the call. The lottery sheets list "Offered Y/N" per defendant, which is raw data, not a result.

5. Filed sentences that fix the computation literally:
 - Resolution Section 3 (quoted in 1): fixes population (every defendant on a monthly lottery list, offered or not, including those who declined and those not yet disposed), outcome (conviction in the referred case at final disposition), window (courts' records as of 31 August 2026), comparison (not offered minus offered, in points; the prompt flips the sign to "lowers").
 - Resolution Section 2: lists are defendants arraigned in the preceding month and found eligible, half offered by random draw, June 2025 to May 2026.
 - Resolution Section 6: "fiscal year 2026 is the year that ends on 30 June 2026" (fixes the window for the filed-cases and CS/restitution asks).
 - PDU policy Section 3: "A case is eligible when every count charges an offense in one of the classes below" (fixes the eligible-class membership by every count, using 2026 section numbers; the prompt asks for lead charge).
 - Services agreement Sections 3 and 7: program term starts the first of the month after agreement filing; reports list each participant enrolled any day of the month with CS hours and restitution (bears on the per-site asks and on overlap across monthly reports).
 Open point: how a case with no final disposition by 31 August counts as to conviction is not filed (the text says only that it counts).

6. What decides the main answer: mostly an analytical choice (intention to treat by offer versus comparing takers with non-takers or finished cases only, and handling of open cases), but Resolution Section 3 states the intention-to-treat rule outright, so a solver who reads it and applies it follows a stated rule. It is a leak risk for rule 3 (rule application): the deciding estimand is written down. Deciding sentences: "Every defendant on a list counts, whether or not a defendant offered a place took it up and whether or not the case has reached its final disposition by 31 August 2026." Section 5 then converts the figure to a call by thresholds, also stated rule application. Separately, much of the work (joining legacy and CMS records through case-number formats, 2025 versus 2026 section numbering, UTC timestamps) is Layer 1 cleaning, not a planted trap. Nothing looks planted.

7. Realism:
 - Mostly convincing exports. NCJS/Nethercote workbooks have plausible metadata (creator, generated stamps with minute-level times that differ, Natalie Hansen / N. Hansen). The two report layouts (Client No/CS Hrs "H:MM" text/dd-Mon-yy versus Participant ID/ISO dates) look like a real system change. Court case refs appear in varied formats (BW25CM00244, 25CM187 WM, WM-25-CM-00260, 26-CM-05272-SH). The CMS has CLERK/E-FILED/MIGRATED entry sources and a case-number scheme that changes mid-2026.
 - Tells to consider: (a) all docket event timestamps seen start at "T05:00:00Z" for migrated events (uniform), which is plausible for a midnight-local migration but is uniform. (b) The draw workbooks' file creation stamp is the draw date at a round-ish time (2025-06-05 10:12) and all twelve footers are identical ("Draw conducted by M. Nielsen ... witnessed by A. Aguilar"); plausible for a template. (c) Offer counts are exactly half rounded down every month (152 of 304, 156 of 312, 147 of 294 and 139 of 279, 157 of 314), consistent with the resolution, and lists of 285 to 319 each month look quite flat. (d) Nethercote report metadata "Generated" and the workbook creation times differ by a few hours with created always at 09:30:00 exactly (all 8 NCJS and 7 monthly workbooks show created hh:mm = 09:30:00), which is a machine tell. (e) Participant IDs run in a near fixed step (P2600334, 335, 339, 342, 348, 349) with the Aug 2026 report starting at those IDs, a minor tell. (f) The Jan 2026 monthly report of Nethercote shows the same participants' CS hours as "0:00" and "4:00" while Jul 2025 shows "2:00", "4:00", "3:00" for the same clients (cumulative versus monthly reading), plausible but worth the author checking against the generator. (g) The legacy and CMS jail files are lightly synthetic-looking (random-walk values) but harmless.
 - No prose that reads as written for a task; no document is dated after the events it describes. The PDU policy is "Effective 1 January 2026" and its docx internal zip stamps are 2026-09-01, after the January effective date, acceptable as a file-save date.

8. Mechanical sweep flags:
 - board_resolution_2025_31.pdf: harmless as to the recommendation words (renew, lapse, "full scale", "pilot's scale" are the legal thresholds in Section 5, which are the options asked about in the prompt) with no computed result. But see 1 and 6: Section 3 states the intention-to-treat estimand explicitly, which the author should weigh as handing over the decisive step. Not a leak of the figures. Verdict: no figure leak; flagged only for the estimand sentence.
 - penal_code_conversion_table_2026.csv: harmless. The only match is the offense title "False reporting to a law enforcement agency" (row 429.07 to 418.05); "False" is part of the title and no cell is a boolean or null. A pandas read would not coerce it because it is within a longer string in a text column. A bare section code like "412.10" will read as a float and could lose trailing zeros (e.g. 412.10 becomes 412.1, 434.80 style), which is a Layer 1 parsing hazard, not a leak.
 - NCJS_Larkmoor_Participants_2026-*.xlsx: harmless. The later dates are Program End values (scheduled twelve-month term ends, 2026-09-30 through 2027-06-30) of participants still Active, not events after the setting; the Aug 2026 report was generated 2026-09-03, before 10 September 2026. No Discharge Date or event date falls after the report date. No hidden columns or sheets (single visible "Report" sheet; hidden columns none).

### Re-read after the determinism repair (resolution section 3 reworded)

1. No sentence or file names the decisive step. The nearest is Resolution 2025-31 Section 3: "A case that has not reached its final disposition by 31 August 2026 counts by how it will end, not as a case without a conviction." It files the estimand, with pending cases counted by their eventual outcome. It does not say how to project that outcome. Section 3 also says "Every defendant on a list counts, whether or not a defendant offered a place took it up." This is a population filing (everyone on the list, whoever took up the place), not a method. I read both as legitimate filings of the WHAT. A strict reader might say the first sentence signals that censoring exists. No file says "use survival or a hazard method", and nothing is labelled as a method note.

2. No file ranks or scores the three options (full scale, pilot scale, lapse). Resolution Section 5 gives the thresholds (25 points or more, 15 to under 25, under 15) but no reduction figure. The lottery workbook shows Y/N offers only. The FY2025 court statistics PDF and the jail-population CSV give context and no effect estimate.

3. Files that exist mainly to help the analyst:
   - legacy_event_codes.csv, a code dictionary for the legacy docket.
   - penal_code_conversion_table_2026.csv, a bridge between the 2025 and 2026 penal-code numbering.
   - pretrial_diversion_policy_pdu_2026_01.docx, whose class table defines the eligible offense classes.
   - nethercote_services_agreement_2025.pdf, which explains the program term, reporting layout, site assignment and fiscal year.
   - board_resolution_2025_31.pdf, which sets the estimand, the thresholds and the fiscal year (Section 6).
   Each reads as a plausible organisational document. None is a readme or manifest, and none explains how the data fit together beyond what a county would write. The conversion table is the most task-shaped. It is a plausible county or state publication, though not a leak.

4. No figure or name reads as the answer. The only decisive-looking numbers are the Section 5 thresholds (25 and 15 points), which are rules. The lottery headers ("Places offered: 152 of 304 listed") are a design fact, not a result. No share, reduction or total is shipped.

5. Filed sentences that fix the computation:
   - Section 3, "the share of the defendants on the lottery lists who are convicted in the referred case at its final disposition, for those not offered a place less that for those offered one, in percentage points." Read literally, this fixes the population as every listed defendant (intention-to-treat, regardless of take-up), the outcome as conviction in the referred case at final disposition, the window as the records to 31 August 2026, and the comparison as not-offered minus offered. It also sets the sign.
   - "A case that has not reached its final disposition by 31 August 2026 counts by how it will end." This fixes the treatment of unfinished cases as their eventual outcome, not as non-convictions.
   - Section 6, fiscal year 2026 runs from 1 July 2025 to 30 June 2026. This fixes the window for the case counts, hours and restitution asks.
   - Policy section 3, "A case is eligible when every count charges an offense in one of the classes below." This fixes eligibility at case level, with all counts in the listed classes.
   - Agreement clause 6, the 5% retention of restitution. It could affect "restitution they paid", which is ambiguous between gross payments and net remittance. I flag this as a possible fork outside the main call.
   - Policy section 2: the eligible defendant has no prior conviction, no other pending case and is not on probation or parole.
   What is not settled by any filed sentence: how a pending case "will end" is estimated, the projection method, and the treatment of cases whose outcome is mixed (diversion terminated, restored to calendar). The lottery-day denominator is fixed by the lists.

6. The main call is decided mainly by an analytical choice:
   - The call is a threshold comparison of the reduction with the Section 5 cut-offs (rule application).
   - The reduction depends on handling cases still pending at 31 August 2026. Diversion terms run twelve months and cases continue, so many are right-censored. Counting them as non-convictions biases the estimate, and the resolution requires counting them by how they will end. Projecting those endings from the data (docket events, diversion status, completion and termination rates) is the part no filed sentence settles. This is an analytical choice and carries the decision.
   - Parts a stated rule settles: ITT population, sign, outcome definition, thresholds, fiscal year, section renumbering (conversion table), eligible classes (policy table).
   - Semantics and cleaning (not decisive, Layer 1): legacy vs CMS case-number formats (BW25CM00113 vs 26-CM-05272-SH vs "LC-25-CM-00687"), legacy event codes vs CMS event types, MM/DD/YYYY dates vs ISO, UTC timestamps (05:00Z/06:00Z, a local-midnight conversion), CS hours as "h:mm" strings vs integers, the two Nethercote report layouts, and the renumbered statute (423.01 means Assault in 2025 and Retail theft in 2026; 418.02 means Theft in 2025 and Disorderly conduct in 2026).
   - Nothing looks planted. The statute-section swaps are the genuine renumbering hazard, in the conversion table. They matter for the eligible-class count ask, not for the main call.

7. Realism:
   - Mostly plausible: the participant-report layouts differ by period (a monthly "Client No / CS Hrs h:mm" format through January 2026, then "Participant ID" in the NCJS format). Generated timestamps vary (08:23, 09:33, 09:05, 08:31). Case references are mixed in format (LC-25-CM-00687, BW 25 CM 463), as a human data entry would produce. There are footer rows like "Enrolled during month: 227".
   - Possible machine tells:
     - Lottery lists have exactly half offered, rounded down, every month (152/304, 156/312, 147/294, 139/279...). This follows the resolution's rule, so it is consistent.
     - Restitution values are multiples of 23.75 (23.75, 47.5, 71.25, 95), i.e. 95% of 25-dollar steps. Hours and payments in the Nethercote files progress in neat arithmetic steps (2, 4, 5, 9, 11, 15).
     - CMS entries show only 05:00:00Z and 06:00:00Z for migrated rows (12,696 and 5,528), as expected from a daylight-saving offset on date-only legacy data.
     - Participant IDs P2600002, P2600004... run in a near-sequential step within each month's cohort. Plausible for a system-assigned ID.
     - Docket statuses and the "Unsuccessful - conditions not met at final review" reason strings recur verbatim at term end.
     - The NCJS files all say "Prepared by: Natalie Hansen, Data Coordinator" while the older ones say "N. Hansen", which is consistent.
   - The pack documents are dated before the events they describe: policy created 2025-12-15 and effective 1 January 2026; agreement 20 May 2025 before the 1 June 2025 start. No after-the-fact dating.
   - The metadata stamps (creator, created equals modified) are the expected export pattern and are not uniform.
   - No prose reads as written for a task. The prompt is fine. The only prose I'd flag is Resolution Section 3's "counts by how it will end, not as a case without a conviction", which is slightly pedagogical for a board resolution, though it reads as a plausible evaluation clause.

8. Sweep flags:
   - board_resolution_2025_31.pdf: harmless. The words that match a recommendation are the Section 5 renewal thresholds, which belong in a governing document. They state a rule, give no reduction figure and rank no option. This is a stated rule that the golden call applies, not a leak of the answer.
   - penal_code_conversion_table_2026.csv: harmless. I see no True/False/None/NaN or null-like cell in the file. The columns are section numbers and offense titles. If a section such as "412.10" or "434.08" tripped the sweep, those are strings. Nothing there is a boolean or null.
   - NCJS_Larkmoor_Participants_2026-*.xlsx: harmless. The dates after 10 September 2026 are scheduled Program End dates (for example 2026-09-30, 2026-10-31, 2026-11-30, 2027-01-31). These are twelve-month terms from start dates, which the agreement (clause 3) specifies. The reports themselves are generated on or before 2026-09-03, and no discharge or event date is after the setting.

### Rulings on the re-read (main thread)

- Question 1: nothing quoted names the decisive step. The nearest sentence is the WHAT the repair filed (open cases count by their final disposition), which the determinism spec requires because the estimand includes members not yet observed; it names no stage, rate or projection, and every wrong-tier route but the recorded shares stays live on it (the arms' cumulative incidence at the longest follow-up 31 points, the cases ended so far, the terminations so far, `checks.py` Gate F rows). Harmless.
- Question 3: the code list, the conversion table, the policy, the agreement and the resolution are documents the county, the court and the provider keep; none explains the pack (`leak.py` sweeps 1 and 12 clean). Harmless.
- Question 5: restitution paid against remitted is closed by fork row SF20 (the prompt asks what participants paid; agreement clause 6 has Nethercote receive the payments and retain five percent of each; every new amount is 95 per cent of a whole-dollar payment, asserted). A terminated case's outcome is the docket's own final disposition. Harmless.
- Question 6: an analytical choice decides the call (projecting how the open cases end), with the reader naming no file or sentence that settles it; agrees with the judge's Gate H line. Pass.
- Question 7: the section 3 clause reads as a board's evaluation clause; it stays as worded, since the re-judge reads this wording. Restitution in 23.75 steps is the provider's whole-dollar instalments net of its retention, the form device D3 takes in a real remittance column; running totals of whole hours and system discharge reasons are what a case system writes. No fix.
- Question 8: the three sweep flags are ruled as in the first pass.
