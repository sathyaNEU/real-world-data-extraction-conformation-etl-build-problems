# leak check, task130

**Verdict: REVIEW.** 13 files read, 19 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: rejected, record, decisive, register, repair, holders, returns, household, forward, domain, benefits, months, strong, computation, ledger, tenter, households, device, objective, method, chosen, vendor, analyst, client, sentence

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `care_management_services_agreement_schedule_c.pdf`: carries 21 of 24 distinctive words of the committed call: 'Certify a programme baseline of $4,083 per member per month for the 140 enrolled members ($1,453 medical, $2,630 pharmac'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `northcourt_implementation_plan_2027-28.pdf`: 3 of 25 stump-paragraph terms appear (record, register, client); read whether the document names the move
- **REVIEW** `warehouse_readme_2027-03.txt`: 3 of 25 stump-paragraph terms appear (record, benefits, analyst); read whether the document names the move

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `northcourt_stratification_2026_claims_final.xlsx`: 140 ISO dates after 2027-03-12, e.g. 2027-04-01

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt form (clean)

## Solver's-eye read (round 2)

The second reader's verdict on v3: no sentence names the decisive step. Primed to look for it, the reader found the regression path and reproduced the golden of the time; it sized five forks on the main call, four signposts that read as the author's hand, and a list of realism tells. Disposition of each, against the build now shipped (programme baseline $4,083: $1,453 medical, $2,630 pharmacy):

- **A1, pharmacy carried forward at the enrolled members' own 2026 level.** Closed in the data. The acuity score counts pharmacy at 0.4 of medical dollars and the world carries one-off pharmacy (hepatitis C cures, G-CSF and capecitabine with chemotherapy, fixed-length venetoclax and adjuvant oral oncology, CMV prophylaxis, teriparatide, biologic starts, stops and switches, weight-loss GLP-1s started and stopped). The enrolled members' pharmacy rises into 2026 in every tier, and carrying it forward lands 31.7 per cent above the golden programme pharmacy and 20.4 per cent above the total, on no tier cell (checks.py fork 1).
- **A2, calendar 2025 against the bid's programme year.** Closed by shipped facts. The bid list's cover gives the proposed programme year and its terms; Schedule C.1(e) and (f) give the final list's calendar-2026 basis and the Programme Year three months later. Calendar 2025 trended 27 months lands 9.1 per cent off and misses every tier cell (fork 2).
- **A3, full-year members only.** Closed by Schedule C.1(c), which counts a member enrolled for part of the period for those months; full-year only lands 5.0 per cent off and misses every tier cell (fork 3).
- **A4, a pooled level spread by tier relativities.** Closed by Schedule C.1(h), which determines a Baseline PMPM separately for each Risk Tier from the experience of members in that tier; the pooled readings land 0.8 per cent off and miss every tier cell. The largest single member is now at most 25 per cent of a bid tier's medical and 22 per cent of its pharmacy (fork 4).
- **A5, the Actual PMPM's three-month run-out.** Closed by Schedule C.1(h), which takes earlier experience on claims paid through the Data Cut-Off Date; the other basis lowers each tier's medical by $2.70 to $8.15 and leaves pharmacy unchanged (fork 5).
- **B1, Recital C certifying the untreated control.** Rewritten: the recitals are procurement history (RFP 2025-07 cancelled before an award under the board's freeze on new non-instructional contracts, RFP 2026-11, the business-associate terms, the board's approval). The "provided no services" sentence is gone.
- **B2, the readme's crosswalk note naming the RFP data book.** Generic now: Bramwell's number format on its cards, reports and data books.
- **B3, a static crosswalk whose only job is the RFP list.** The readme says why it goes out with every pull: the office still works Bramwell-numbered paper.
- **B4, identifiable numbers in a bidder copy.** The folder's copy is the District's identified copy, with data book record numbers and ages from Northcourt, and the Bramwell member number and birth date added by Risk Management and Benefits; the cover says bidders got the data book without them.
- **Realism.** Inpatient revenue lines follow the diagnosis and the operation; NICU stays run by gestational age; no allowed claim falls after coverage ends (reason 27 denials instead); PDFs keep the producers of the organisations' own tools (LibreOffice, Chromium) and workbooks make no application claim; eligibility carries COBRA, rehires and dependents dropped and added back; claims are logged on business days; care teams follow the plan's rule; some 2025 claims settle in 2027; the renewal letter signs on its first page; the agreement carries conformed signatures. Deferred to after the solver round: none.
- **Fresh read due.** The prompt changed (compressed under 1,000 characters) and documents under target/ changed, so the next reader round reads this build.

## Solver's-eye read (round 3, after repair 2)

One isolated reader on Sonnet, on a fresh copy of the prompt (933 characters) and the 13 shipped files.

1. Decisive step: none. The nearest pointers are context, not instruction: the final workbook's cover (model 4.2 run on one calendar year of claims, the 140 highest-scoring members), Schedule C C.1(h) (a baseline per Risk Tier from the experience of members in that tier, the source of the experience left open) and Recital B (RFP 2025-07 cancelled before award).
2. Ranks or states the asked figures: none. The only asked figure stated anywhere is an input, the final workbook's tier counts (35, 37, 38, 30).
3. Exists only to help: none outright. The nearest is the TPA crosswalk, which the readme gives an in-world reason for.
4. Reads as the answer: none. The renewal letter's whole-plan PMPMs ($515.43, $233.04, $748.48) are the wrong population.

REVIEW lines: all four harmless (Schedule C states no PMPM or baseline; the implementation plan's words are its page header and records requests; the readme's are its own subject and its author's title; the 140 dates after the as-of are the enrolment effective date, 1 April 2027).

Forks the reader raised on the main call, and their disposition:
- Experience base (the enrolled members' own trended year against the untreated RFP cohort's year after selection): this is the stump, not a fork; the determinism judge rules on it at stage 7.
- RCV8692544 (rank 18, Tier 1) is on the final list but left coverage on 31 October 2026, while the list's cover says members enrolled on 1 March 2027, so Tier 1 reads 35 or 34: a fork introduced by repair 2's eligibility churn. Fixed before the solver round.
- The comparator tier for the 19 RFP members who are also on the final list (13 in a different tier there): measured, and closed before the solver round if it moves a graded figure.

Realism tells, deferred to the repair after a round the solver misses (stage 6b): UK spellings and day-month dates across documents from four Minnesota organisations; PDF producers (Skia/HeadlessChrome with a Linux user agent, LibreOffice 24.2) and embedded Liberation and Carlito fonts; one openpyxl fingerprint across four workbooks from three organisations; Recital B narrating the cancelled RFP and its reason; the RFP workbook's "District copy" cover row; the readme over-justifying the crosswalk and repeating the renewal letter's note on Bramwell's 2024 history; the renewal letter saying the stop-loss premium was confirmed on 22 February when the policy schedule was signed on 18 December 2026.
