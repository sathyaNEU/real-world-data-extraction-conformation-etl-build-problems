# leak check, task501

**Verdict: REVIEW.** 14 files read, 42 golden figures and 4 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: asserted, golden, register, deadline, inside, balance, period, investment, decisive, window, unfunded, pacing, january, reserve, history, audited, readable, lender, replaced, pattern, closed, default, construction, notice, tranche

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `richtlinie_liquiditaet_privatmarkt_RL-PM-05.docx`: carries 4 of 4 distinctive words of the committed call: 'Elect a standby facility of CHF 225 million for 2027.'
- **REVIEW** `stiftungsrat_protokoll_auszug_2026-09-24.pdf`: carries 3 of 4 distinctive words of the committed call: 'Elect a standby facility of CHF 225 million for 2027.'
- **REVIEW** `term_sheet_lindenhof_standby_2027.pdf`: carries 3 of 4 distinctive words of the committed call: 'Elect a standby facility of CHF 225 million for 2027.'

## 4 design-note vocabulary (REVIEW 5)
- **REVIEW** `feldbeschrieb_privatmarkt_extrakt.md`: 7 of 25 stump-paragraph terms appear (register, balance, period, investment, january, audited); read whether the document names the move
- **REVIEW** `halbjahresbericht_privatmarkt_2025-H1.pdf`: 4 of 25 stump-paragraph terms appear (register, period, reserve, notice); read whether the document names the move
- **REVIEW** `mail_standby_fazilitaet_2027.txt`: 5 of 25 stump-paragraph terms appear (register, investment, january, audited, notice); read whether the document names the move
- **REVIEW** `richtlinie_liquiditaet_privatmarkt_RL-PM-05.docx`: 9 of 25 stump-paragraph terms appear (register, investment, unfunded, january, reserve, history); read whether the document names the move
- **REVIEW** `term_sheet_lindenhof_standby_2027.pdf`: 4 of 25 stump-paragraph terms appear (period, january, lender, notice); read whether the document names the move

## 6 ranking artifacts (REVIEW 2)
- **REVIEW** `fondsregister_2026-12-31.xlsx`: names 4 of 4 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `programmkonto_lindenhof_2025-2026.csv`: names 4 of 4 answer-set candidates beside numbers; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `fondsregister_2026-12-31.xlsx`: 68 ISO dates after 2027-01-06, e.g. 2027-01-26, 2027-02-16, 2027-03-23, 2027-05-08, 2027-05-13

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read

Reader (Sonnet, medium) on the stage 3 cut, prompt.txt and target/ only. Q1: none (RL-PM-05 4 fixes the election rule, not how the expected calls are built; the register's Hinweise sheet carries the standard rule that after the investment period capital is called only for follow-ons and expenses, a filed rule the analyst must use, not the method). Q2: none (the 2025 half-year report gives H1 2025 distributions by strategy, a different period, not by quarter). Q3: none (the field description and the extract protocol are ordinary extract documentation). Q4: none (the term sheet's amounts are the lender's menu; the NAV covenants are context). Q5: RL-PM-05 4 with 3, 5.1 and 2.4: the smallest offered amount X with 150 + X at least 1.1 times the 2027 expected calls; not computed by the reader. REVIEW lines: all harmless. Readings raised on the ask: the custodian's CHF credit at its dealing rate against the notice at the reference rate of the value date (the prompt names the reference rate); quarter by booking date or value date (the field notes now define Valuta); IN_KIND and withdrawn lines. On the call: the 25 per cent NAV covenant as a possible cap on the larger amount. Realism: mixed English and German terms in the custodian CSV (plausible for a Swiss custodian); neat counts.

Stage-4 repair (2026-10-12): the readings above are answered in the design note (`## Literal reader`, fork rows SF17 and SF18). The repair changed RL-PM-05 s.5.2 (the estimation period) and the minutes' item 6.1 and regenerated every data file, so this read was taken on the stage-3 cut and the reader re-reads at the re-judge.
