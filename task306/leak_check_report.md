# leak check, task306

**Verdict: LEAK.** 13 files read, 20 golden figures and 7 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: orders, momentum, participation, average, candidate, executions, trades, sentence, decisive, golden, warranty, market, rebalances, export, pounds, smaller, standard, population, candidates, carries, turnover, determinism, carried, register, storms

## 1 file names (REVIEW 1)
- **REVIEW** `research_backtests_2027_candidates.xlsx`: a sheet named 'Notes': confirm it is the organisation's own notes and does not describe the data's columns or files

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `ic_capital_allocation_policy_2026.pdf`: 5 of 25 stump-paragraph terms appear (candidate, executions, trades, rebalances, standard); read whether the document names the move
- **REVIEW** `tca_standard_rev4.pdf`: 6 of 25 stump-paragraph terms appear (orders, participation, average, pounds, standard, register); read whether the document names the move

## 6 ranking artifacts (REVIEW 1, INFO 1)
- **REVIEW** `research_backtests_2027_candidates.xlsx`: names 4 of 7 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `trading_account_register.csv`: names 3 of 7 answer-set candidates; confirm it does not rank them on the decision question

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (LEAK 4, REVIEW 2, INFO 1)
- **LEAK** `ic_capital_allocation_policy_2026.pdf`: Producer names 'Wealdmoor Investment Committee', not the application that wrote the PDF
- **LEAK** `ic_capital_allocation_policy_2026.pdf`: Creator names 'Wealdmoor Investment Committee', not the application that wrote the PDF
- **LEAK** `tca_standard_rev4.pdf`: Producer names 'Wealdmoor Dealing', not the application that wrote the PDF
- **LEAK** `tca_standard_rev4.pdf`: Creator names 'Wealdmoor Dealing', not the application that wrote the PDF
- **REVIEW** `broker_commission_schedule_2026.xlsx`: docProps/app.xml has no TitlesOfParts, which Excel always writes
- **REVIEW** `research_backtests_2027_candidates.xlsx`: docProps/app.xml has no TitlesOfParts, which Excel always writes
- **INFO** `-`: audit reported no writer signature (1 lines)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: question form 'which' at 36% of 196 prompts (cap 30%); reword at the role level, not the verb

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)


## Solver's-eye read

Architecture 4, read 1 on target.zip 2ac88df8 (isolated Sonnet reader, a fresh copy of prompt.txt and target/ only),
before the FIX_NOW repair.

1. Decisive step: no sentence announces it; the nearest is IC-07 section 2's estimand (a candidate's expected alpha at
   a size is its gross alpha less the expected cost a year of trading its rebalances at that size), which gives no
   method.
2. Ranking file: none; the research workbook carries gross alpha, tracking error and information ratio only, before
   cost.
3. Helping file: none; the TCA standard's term table is a standard's glossary and the security master's corporate
   action notes are data.
4. Answer figure or name: none; the gross alphas are context.
5. Population sentences: IC-07 section 2 files the rebalances of the twelve months to 30 November 2026, scaled to the
   capital and traded in full on the rebalance day, costed at the TCA standard's shortfall from the desk's own
   executions; their literal result is the golden's population.
6. What decides: an analytical choice, the cost of trading GBP 400 million estimated from the desk's much smaller
   executions, which needs a size-dependent cost model the pack does not prescribe; the re-created orders, the block
   allocations, pence against pounds and the account mapping are Layer 1.

Read 2 on target.zip 7f2aba02, after the repair changed IC-07 section 2, the TCA standard's section 3, the ESG list
and the data.

1. Decisive step: none; IC-07 section 2 states the comparison, not the step.
2. Ranking file: none (gross alpha only: momentum 5.05, mid-cap value 3.02, large-cap quality 1.84 per cent).
3. Helping file: none.
4. Answer figure or name: none.
5. Population sentences: IC-07 section 2 as in read 1, the cost source narrowed to the desk's executions in stocks of
   the candidate's index band; literal execution gives the golden's population.
6. What decides: an analytical choice, the participation-dependent cost within each band carried to GBP 400 million;
   an analyst who applies the desk's average shortfall files momentum, and no sentence announces the step.

Sweep lines: the research workbook's Notes sheet is Research's own methodology note, harmless; IC-07 and the TCA
standard name the estimand and define shortfall, participation and volatility without a cost-versus-size method,
harmless; the workbook ranks on gross alpha only, harmless. The TCA standard's consolidation-day and 60-session rules
read as the desk's own measurement convention in the standard's definitional voice (mild, not a leak).

Realism: the email's header and quoted-printable wrapping, the GBX and GBP units, the BACKUP-RECOVERY orders, the block
allocations and the re-used account code read as the organisation's own systems; the mild tells (one-per-row tenfold
consolidations, synthetic-sounding issuer names on the ESG list, tidy commission tiers) give nothing away.
