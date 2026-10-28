# leak check, task177

**Verdict: REVIEW.** 16 files read, 33 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: meeting, silent, members, groups, default, family, carried, portfolio, policy, history, golden, meetings, carries, ledger, section, window, pattern, asserted, current, six-month, payroll, forward, instalment, states, carrying

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `pvm_jlg_operating_policy_v6.pdf`: carries 3 of 5 distinctive words of the committed call: "About 300 of the pool's 12,880 loans will be 90 or more days past due on 30 June 2027."
- **REVIEW** `tb_term_sheet_PVM-2026-12.pdf`: carries 5 of 5 distinctive words of the committed call: "About 300 of the pool's 12,880 loans will be 90 or more days past due on 30 June 2027."

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `pvm_field_update_cyclone_2026-11.pdf`: 3 of 25 stump-paragraph terms appear (meeting, portfolio, meetings); read whether the document names the move
- **REVIEW** `pvm_jlg_operating_policy_v6.pdf`: 8 of 25 stump-paragraph terms appear (meeting, members, groups, portfolio, policy, meetings); read whether the document names the move
- **REVIEW** `tb_term_sheet_PVM-2026-12.pdf`: 7 of 25 stump-paragraph terms appear (meeting, members, portfolio, meetings, section, current); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read

One isolated reader (general-purpose, medium) over fresh copies of `prompt.txt` and `target/` only, 2026-10-28, pack `b4bdda9106e04f1d`. It read the four PDFs in full and every data file's structure, headers and a sample of rows; it computed no answer.

1. **Decisive step told:** none. No file states a forecasting method or names the pitfall; the policy files only the days-past-due and PAR definitions; a grep of the PDFs for forecast, projected, expect, estimate, likely to and will be found nothing.
2. **Ranking or scoring file:** none. The portfolio report is a flat monthly branch table with no sort, flag column, hidden rows or comments.
3. **File only to help the analyst:** none. The bureau's member directory is bureau reference content the guardrail note's counting rule needs, not a note about the bundle.
4. **Figure or name reading as the answer:** `summary_active_mfi_lenders` and `summary_mfi_outstanding` in `cic_portfolio_review_PVM_20261231.csv` look like a ready-made breach count for the guardrail ask, but they count member codes (a converted lender's old and successor codes as two), so used as they stand they do not match the filed counting rule.
5. **Filed sentences fixing computation or population:** term sheet clause 3 (the population is the pool tape's 12,880 loans at the cut-off); policy section 6 (days past due from the oldest instalment not paid in full, loan by loan, on 30 June 2027); the field update's "We have not announced a moratorium" (the clock runs unmodified); CPN-MF-07 sections 2 and 3 (the breach test per borrower on the cut-off report, JLG and MFI-IND only, an institution's codes collapsed into one).
6. **What decides the main answer:** an analytical choice. Nothing filed states a forecasting rule; the analyst decides how much of the post-cyclone arrears rolls to 90 days, for example a uniform historical roll rate against one differentiated by exposure or cohort, estimated from the instalment history.

**REVIEW line, `pvm_jlg_operating_policy_v6.pdf` shares words with the main question:** harmless. The shared words are the filed definition in section 6, where the prompt's "90 or more days past due" comes from; it files the measurement, not the forecast or a method, and carries no figure tied to the pool or June 2027.

**Realism:** none. Meeting gaps of 13, 14 and 15 days from holiday shifts; claim settlement ratios 0.45 to 0.99 with three of 138 open; the platform boundary agrees with the 1 April 2025 migration; containers carry business authors and no toolchain signature.

**Main thread rulings.** Question 4 is harmless: the summary columns are the bureau's own report furniture and the designed wrong basis of the guardrail ask (`## Ask sheet`, the bureau summary stop, +11 to +25 per branch), they never touch the main call, and the counting rule that corrects them is filed (CPN-MF-07 section 3); the silent primary (the Nirmala pre-migration account numbers reported beside the new ones) is not named. Every question 5 sentence executes to the golden: the pool tape's 12,880 loans, the section 6 rule, no moratorium, and the guardrail test as the golden runs it.

### Re-read after the stage-4 repair (2026-10-28, pack `03afa0d90f6245ea`)

The prompt's rounding sentence was reworded and the bureau directory gained `parent_code`, so the reader ran again on fresh copies of `prompt.txt` and `target/` only, under the same brief.

1. **Decisive step told:** none. The bundle fixes the population and the window; no sentence names a roll-rate, vintage-curve or extrapolation method.
2. **Ranking or scoring file:** none. The portfolio report is branch-month history to 2026-12 only; the bureau's summary columns count a converted lender's two codes as two institutions (331 borrowers with both codes active), so they are a wrong count under CPN-MF-07, not a precomputed answer.
3. **File only to help the analyst:** none. The term sheet's clause 11 lists the data room's files, as one of eleven deal terms in a genuine term sheet.
4. **Figure or name reading as the answer:** none. The pool's 12,880 loans and INR 4104.15 lakh describe the population; no figure dated after the cut-off anywhere.
5. **Filed sentences fixing computation or population:** term sheet clause 3 (the pool tape's loans), clause 5 (product, current at the cut-off, seasoning, the fourteen branches, all of which the tape already satisfies), the prompt's window and threshold, and policy section 6's days-past-due rule. Each files the population, window or unit; none files a method.
6. **What decides the main answer:** an analytical choice, the method for projecting currently current loans six months forward (which history is a valid comparison, how to use the two platforms, how to weigh the cyclone); nothing in the bundle states a procedure.

**REVIEW line, the operating policy:** harmless; section 6 defines days past due and PAR 90 generically, the only mention of 90 in the document, with no number, method or ranking.

**Realism:** none. Non-round branch metrics, a plausible enrolment curve, meetings over six weekdays, postings over 23 months, in-world container metadata. The reader noted that SELF and GS always equal the demand and NIL is always zero over 333,018 rows, and read it as the policy's own full-or-nothing rule (section 4), not as a generated tell.

**Main thread ruling.** Every question 5 sentence executes to the golden's population, window and unit; nothing to fix.

### Re-read after the guardrail note's section 3 wording (2026-10-28, pack `90d1fbd324871a49`)

The judge's second pass moved one sentence of CPN-MF-07 section 3 (the parent clause), so the reader ran a third time on fresh copies, same brief.

1. **Decisive step told:** none; the policy's definitions fix what is measured, never how to forecast it.
2. **Ranking or scoring file:** none; the bureau's summary columns are raw per-inquiry totals, not filtered to JLG and MFI-IND or folded through the directory's parent and successor codes.
3. **File only to help the analyst:** none.
4. **Figure or name reading as the answer:** none; the portfolio report stops at December 2026 and the pool tape's `dpd_at_cutoff` is zero throughout.
5. **Filed sentences:** policy section 6 (days past due) and section 4 (OWN, GRP_SUPP, SELF and GS paid in full); term sheet clause 5 (the pool's 12,880 loans); CPN-MF-07 sections 2 and 3 for the branch figure, executed as the golden runs it: active JLG and MFI-IND lines at their latest report, codes merged through the directory's parent and successor codes, breach on four institutions or INR 2,00,000.
6. **What decides the main answer:** an analytical choice; no document states a roll-rate, vintage or regression procedure.

**REVIEW line, the operating policy:** harmless; the standard days-past-due and PAR 90 definition the question needs, no pool figure, forecast or ranking.

**Realism:** none.

**Main thread ruling.** Clean; every question 5 sentence executes to the golden.

### Re-read after the term sheet's clause 12 (2026-10-28, pack `3a18f553c3611317`)

The portal's determinism return added clause 12 to the term sheet (the forecast's basis: the pool as it stands at the cut-off, and members' repayment from 1 January 2027 as in the Assignor's experience before the cyclone), so the reader ran a fourth time on fresh copies of `prompt.txt` and `target/` only, same brief.

1. **Decisive step told:** none. Clause 12 "states the estimand and condition, not the method"; the policy's sections 3, 4 and 6 bear on how the history is read and are ordinary policy text.
2. **Ranking or scoring file:** none. The portfolio report holds branch PAR history, not the pool's loans; the tape's `dpd_at_cutoff` is a snapshot; the cyclone update forecasts nothing.
3. **File only to help the analyst:** none. The member directory is bureau reference content that CPN-MF-07 section 3 refers to; the migration map is a system artefact; the claims register and the postings are distractors.
4. **Figure or name reading as the answer:** none. The pool's 12,880 loans and INR 4104.15 lakh are context.
5. **Filed sentences fixing computation or population:** clause 12 (the population at the cut-off, the outcome and its date, the forward repayment condition), clause 5 (current loans at the cut-off), policy sections 4 and 6, and the prompt's rounding. They fix the estimand and leave the method open. The reader named its weak point here: different windows before the cyclone, or different methods, might move the count by more than 100, which it could not judge from the text and did not test.
6. **What decides the main answer:** an analytical choice, the repayment model built from the history before the cyclone and its unit of analysis; reading the platform identifiers and GRP_SUPP correctly is Layer 1 cleaning.

**REVIEW lines:** harmless. The term sheet carries the call's words as the bank's own pricing basis and names no method. The operating policy carries the standard days-past-due and PAR 90 definitions and section 4's payment codes, a field definition the ledger needs.

**Realism:** minor items only, none from this repair. "Supersedes version 6" on version 6.1, ordinary for a point release. Fifty-two instalments on every loan, the one JLG product clause 5 files. A next-due date it read as the 6th of each month, a misreading of the dd-mm-yyyy format: the tape carries ten dates in the first fortnight of January 2027. The field update's reassurance lines, the clean pool totals in clause 3, a 13-row directory, and the bureau's summary columns repeated on every account row.

**Main thread ruling.** Clean. The weak point in question 5 is settled by measurement. Read only from the month ends whose 181 days closed before landfall, the forecast is 277.4 (SF16, asserted). The group-level chain calibrated before the cyclone gives 277.8, against 547.2, 801.7 and 1,191.1 calibrated on December, on November and December, and after landfall (SF15, asserted). The isolated judge's specifications on both platforms' eras give 276 to 302, every one 300. A reader's account of a route is not a measurement (`determinism-check` section 1), so nothing here is a fix.
