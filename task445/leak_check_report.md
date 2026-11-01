# leak check, task445

**Verdict: REVIEW.** 11 files read, 32 golden figures and 6 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: decisive, section, september, register, marking, december, golden, demand, essays, choice, option, family, sentence, back-test, registered, comparison, choosers, device, change, type-pooled, architecture, export, centres, nothing, different

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `aeb_code_of_practice_2026.pdf`: carries 10 of 14 distinctive words of the committed call: "Scale Question 6 of the 2026 History Paper 2: raise every candidate's mark on it by 2 marks before the best two essays a"

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `aeb_code_of_practice_2026.pdf`: 8 of 25 stump-paragraph terms appear (section, register, marking, demand, choice, option); read whether the document names the move
- **REVIEW** `history_awarding_minute_2026.pdf`: 3 of 25 stump-paragraph terms appear (section, essays, option); read whether the document names the move

## 6 ranking artifacts (INFO 1)
- **INFO** `aeb_centres_register.csv`: names 3 of 6 answer-set candidates; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Architecture 3, read 1 on target.zip 51f94b0e (isolated Sonnet reader, a fresh copy of prompt.txt and target/ only).

1. Decisive step: none states it; the nearest are the code of practice's sections 4.2 and 4.3 and the awarding
   minute's item 3 (Research and Standards will report on the optional questions under sections 4.1 to 4.3), which
   say a report is due and not whether any question is raised.
2. Ranking file: none; only the 2025 question statistics carry per-question figures, last year's raw data with no
   scaling or recommendation.
3. Helping file: none; the email names the files as an ordinary work note, and the code of practice is a governing
   document.
4. Answer figure or name: none; the minute's boundaries and last year's question mean are context.
5. Population sentences: code 4.2 (an optional question is more demanding when the paper's candidates would have
   earned fewer marks on it than on the others taken together, measured in marks) and 4.3 (the raise by that
   difference, rounded, capped, only at 1.5 or more); read literally they fix the estimand over every candidate of
   the paper, those who did not answer the question included, and give no method.
6. What decides: an analytical choice, estimating what the whole cohort would have earned on each question when only
   the candidates who chose it have marks; the filed rules 3.2, 4.3 and 5.1 apply afterwards, and nothing is planted.

Sweep lines: codes 4.2 and 4.3 state the rule and say nothing about whether any question is scaled, harmless; no
sentence names a comparison group, a section or an ability proxy, or how candidates choose, harmless; the awarding
minute sets the boundaries and the paper's structure and defers to the report, harmless.

Realism: the registers, the entries workbook, the essay-marks log with its events, markers and scan batches and the
review log read as a board's own records, the documents terse and bureaucratic; the candidate numbers and entry rows
are sequential, as entry registers are.

Read 2 on target.zip a676a08f, after two personas were renamed for the people guard (Christopher Turner to Philip
Montes, Melissa Chen to Pamela Sullivan; the email, the workbooks' authors and the card; no figure moved); isolated,
a fresh copy.

1. Decisive step: none states it; code 4.3 is the rule only, and no file says whether Question 6 is scaled.
2. Ranking file: none; the 2025 question statistics are last year's context.
3. Helping file: none; the email lists the folder in passing, the PDFs are governing documents, the centres and
   markers files are lookups.
4. Answer figure or name: none.
5. Population sentences: code 4.2 as in read 1 (every candidate of the paper, those who did not answer included,
   measured in marks), with 3.2 and 4.3 fixing the order (raise, then credit the best answers, then the boundaries).
6. What decides: an analytical choice, estimating what the whole cohort would have earned on a question part of it
   chose; the event log, senior re-marks, re-entries and absentees are Layer 1, nothing planted.

Sweep lines as in read 1, each harmless. Realism: PDF and workbook metadata, the email's Darwin offset, natural mark
distributions, varied scan batches; the essay-marks log's event ids stepping by 1 to 3 is mildly regular.

### Architecture 1's reader (history)


One isolated reader (Sonnet, medium) on fresh copies of `prompt.txt` and `target/` under `/sbx/leak-task445-l3/`, after the judge's pass 3 repair changed the prompt's bridge sentence, 2026-10-12.

## Answers

### 1. Decisive analytical step
No single sentence names it. The nearest is OM-4 section 2 (ownership_methodology_OM-4.pdf): "Where a flag file is issued before the period's filing deadline, the holdings in reports not yet filed are estimated and the flag is set on the estimate. The estimate is made on the basis that, applied to the previous period with only the reports filed by the same number of days after its end as the reports in hand, comes closest to that period's ownership on all the reports since filed for it, on every security in the flag file; closeness is the largest difference, in percentage points, across those securities." It states the back-test selection criterion, so it points at the step (estimate the unfiled reports, back-tested on the prior period), but it does not say which candidate bases exist or which wins. Context that helps: the prompt's "Their flag file goes out on Wednesday 8 February" against data_sources.md ("filings accepted 3 Jan to 3 Feb 2023") and FORM13F_readme.htm (45 days after quarter end). Also OM-4 sec 2 on who counts: "every manager that filed a holdings report or combination report for the previous period and has not filed a 13F notice for this one".

### 2. File ranking or scoring the twelve names
none. No file gives December ownership or a crowded status per name. short_interest_20221230.csv is exchange short interest only (not ownership). The only threshold is OM-4 sec 7 ("above 80.0 per cent"). The 13flist and fsds extract are lookups, not rankings.

### 3. File that exists only to help the analyst
data_sources.md (maintained by Brian Guerra) is a guide to the folder, a mild helper; it also states "The SEC data sets are organised by the quarter a filing was submitted in, not the period it reports" and "nothing in them has been corrected", which tells the solver the Q4 data-set folder holds September-period reports. manager_register.csv has a `status` column and the note "`family` groups affiliates for research notes, not for ownership" (a helper-ish pointer against combining families). Everything else (SEC readme, 13F list, FSDS, OM-4, layout, watchlist, short interest) is plausibly desk/SEC/vendor material. Nothing I would call a file made only to help.

### 4. Figure or name reading as the answer
none. The only figure that reads as a decision number is the 80.0 per cent threshold in OM-4 sec 7, which is a filed rule and is context. No ownership percentage or flag appears anywhere.

### 5. Literal fixing sentences

OM-4 sec 2: "Institutional ownership of an issuer for a report period is the number of its shares held at the period end by the managers that report holdings for the period, divided by the issuer's shares outstanding."
 Literal: numerator = shares held at 31 Dec 2022 by the reporting managers; denominator = shares outstanding (sec 5).

OM-4 sec 2: "The managers that report holdings for a period are every manager that has filed a Form 13F holdings report or combination report for the period, and every manager that filed a holdings report or combination report for the previous period and has not filed a 13F notice for this one. A manager that files a 13F notice reports no holdings of its own; its holdings sit in another manager's report."
 Literal: population = (a) managers with a 13F-HR (holdings or combination) for 31 Dec 2022 in hand, plus (b) managers with a September holdings/combination report and no December notice, whether or not their December report has arrived. Group (b) not yet filed have no December lines, so they are the "not yet filed" set. Notice filers are excluded from both. It does not say how to treat managers present in September who filed neither a December report nor a notice other than as group (b); register `status` is not referenced.

OM-4 sec 2: "Each report is taken as amended." Literal: use the amended content; the readme distinguishes RESTATEMENT (replaces the whole report) from NEW HOLDINGS (adds entries). Literal reading is to apply each type accordingly; wording does not say what to do with multiple amendments beyond "as amended" (latest presumably).

OM-4 sec 2 (estimate): "the holdings in reports not yet filed are estimated and the flag is set on the estimate. The estimate is made on the basis that, applied to the previous period with only the reports filed by the same number of days after its end as the reports in hand, comes closest to that period's ownership on all the reports since filed for it, on every security in the flag file; closeness is the largest difference, in percentage points, across those securities."
 Literal: the estimation basis is chosen by back-test on September: restrict September reports to those filed by the same number of days after 30 Sep as the December reports in hand are after 31 Dec (daily build to 3 Feb = 34 days; the filing date of the last report in hand is arguably the cutoff), apply each candidate basis, compare with September ownership on all reports eventually filed (including amendments), and score each by the maximum absolute gap in percentage points across the twelve securities; the minimum wins. Left open: the candidate bases are not listed (e.g. carry forward each missing manager's September holding, scale the in-hand total by the September filed-by-then ratio, carry forward only some managers, etc.); the exact day-count cutoff; whether "reports in hand" counts amendments; ties. The estimate for missing managers is the only estimated part; what "estimate" means for managers' shares is open beyond the selection criterion.

OM-4 sec 3: "Information-table lines reported in shares (SH). Put and call lines are exposure, not ownership, and are left out." and "A manager's holding of a security is the sum of its lines for that security, whatever the investment discretion or other-manager entries on them." Literal: SH lines only, PUTCALL blank, sum all lines for a manager and security (SOLE/DFND/OTR all added, no de-duplication against OTHERMANAGER).

OM-4 sec 4: "a CUSIP is read as nine characters, upper case, with leading zeros restored. A line whose CUSIP fails its check digit is matched on issuer name and title of class where exactly one covered security fits." Literal: normalise CUSIPs (pad, uppercase), match to watchlist; check-digit failures matched by name plus class only if exactly one covered security fits (the 13flist is the covered universe). Note NOPR's watchlist CUSIP "359Y60106" is itself not a clean 9-digit-style CUSIP; whether it fails check digit is left to the analyst.

OM-4 sec 5: "The issuer's cover-page count (dei:EntityCommonStockSharesOutstanding) with the latest as-of date on or before the report period end." Literal: denominator = per issuer, the fsds num.txt value for that tag with greatest ddate <= 20221231 (no limitation on accepted date; the extract runs to 3 Feb 2023).

OM-4 sec 6: "Holders are named at the level of the filing manager (one CIK); affiliates that file their own reports are not combined." Literal: no family consolidation. Value basis whole dollars (irrelevant for share counts).

OM-4 sec 7: crowded = ownership "above 80.0 per cent" (strictly >80.0; at the stated one-decimal rounding, whether to test before or after rounding is not stated).

Layout v4: columns report_period, cusip, ticker, inst_own_pct, crowded (Y/N), prior_inst_own_pct, one row per security in watchlist sequence. Prompt: "each name's December institutional ownership and flag beside its September ownership on every report filed for that quarter" , September ownership is prior_inst_own_pct, computed by sec 2 on all September reports (as amended), sec 3-5 rules (denominator as-of on or before 30 Sep).

Waterfall (prompt): "a waterfall for the twelve names combined from a straight sum of every information-table line in reports for the quarter ended 30 September that carries one of their CUSIPs as written to our September institutional shares, with one bar each, in this order, for put and call lines, the other lines in reports replaced by a later amendment and lines we match back to their CUSIPs, every bar labelled in shares."
 Literal bars, in order: (1) put and call lines; (2) other lines in reports replaced by a later amendment (i.e. non-put/call lines sitting in reports superseded by an amendment); (3) lines matched back to their CUSIPs (lines whose CUSIP as written does not match but match under sec 4). Start = the straight sum (all lines carrying a watchlist CUSIP as written, in all reports for 30 Sep, from both the Q3 and Q4 data-set folders); end = September institutional shares per OM-4. Signs: bars 1 and 2 are removals (negative), bar 3 is an addition (positive). The start and end totals are implied by "waterfall ... from ... to" but not explicitly counted among "one bar each". Left open: whether new-holdings amendments count as "replaced"; whether PRN lines or lines of non-covered managers (notice filers) need their own bar (the wording lists three only, so such lines would be unbridged or fold into one of them); the order of operations for overlap (a put line in a replaced report belongs to bar 1 by the stated order).

### Realism tells
- data_sources.md "Pull for the December 2022 quarter files" and its explanation sentence reads slightly instructional but plausible for an internal data-engineering index.
- All twelve issuers, tickers and managers are fictional (e.g. "Ulverston Foods Holdings", "Harrowgate Materials") while sitting in files presented as real SEC downloads; the 13F list contains clearly synthetic issuer names (names truncated at 30 chars correctly).
- Watchlist NOPR CUSIP "359Y60106" has a letter in an unusual position, reads as placed to be found (check-digit failure / matching device).
- 13F data-set Q4 folder SUBMISSION accession prefixes (0001085146-22-...) are reused across many managers and the q4 file contains 30-Sep period reports amid dates, fine; but ADDITIONALINFORMATION and addresses (ZIP codes random like 29762 for Minneapolis MN, 16051 for Scottsdale AZ) look generated.
- Q3 vs Q4 data-set INFOTABLE share counts for the same manager and issuer are small and fabricated-looking (e.g. Whitby holding 299,913 shares; VALUE column in thousands inconsistent with share counts like 16126 for 299913 sh).
- manager_register.csv is tidy, hand-maintained by design; "family" column empty for many rows, fine.
- Short interest file contains tickers matching watchlist; plausible but unused (a distractor).
- File mtime all identical (4 Feb 2023), consistent with a single pull.

### REVIEW lines
- All 11 golden-figure hits in client_watchlist_crowding_2022Q4.xlsx (the nine-character watchlist CUSIPs): harmless: these are the filed watchlist CUSIPs themselves, input identifiers not answers.
- All golden-figure hits in edgar13f_daily_20230103_20230203/INFOTABLE.tsv (11 lines): harmless: ordinary holdings lines carrying the watchlist CUSIPs, raw data.
- All golden-figure hits in form13f_2022q3/INFOTABLE.tsv (11 lines): harmless: raw data lines carrying watchlist CUSIPs.
- All golden-figure hits in form13f_2022q4/INFOTABLE.tsv (11 lines): harmless: raw data lines carrying watchlist CUSIPs.
- ownership_methodology_OM-4.pdf, golden figure 80.0: harmless: the filed crowded threshold is a stated rule the prompt's flag depends on, not an answer figure.
- FORM13F_readme.htm, 3 of 25 stump terms (manager, managers, period): harmless: generic SEC vocabulary; the readme documents field definitions and does not name the move (estimating unfiled managers).
- client_flag_file_layout.md, 4 of 25 terms: harmless: layout spec; says nothing about the estimate or managers' filing status.
- data_sources.md, 6 of 25 terms: harmless-to-mild: it states data-set quarters are by submission date and that the manager register's `family` is not for ownership; it hints the Q4 folder holds September-period reports and warns against family combining, but does not name the estimation step.
- ownership_methodology_OM-4.pdf, 6 of 25 terms: leak (mild): OM-4 sec 2 does contain the method for the decisive step (population including prior-period filers who have not filed, and the back-test criterion for the estimate). It is a filed rule, not a naming of the answer, but it is the sentence that tells the solver the move exists; this is the document that carries it by design.
