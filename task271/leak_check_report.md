# leak check, task271

**Verdict: REVIEW.** 15 files read, 14 golden figures and 9 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: following, architecture, trades, reader, minute, record, second, family, hospital, readers, reflex, provider, earlier, selection, decisive, nothing, health, population, markout, screens, carried, analysis, recorded, scored, carries

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `order_execution_policy_2025.pdf`: golden figure 1.5 appears: ...nue whose adverse move for a client flow is above 1.5 basis points is kept off that flow's venue list....
- **REVIEW** `order_execution_policy_2025.pdf`: carries 13 of 17 distinctive words of the committed call: "The board should keep Delvenne lit, Ardenwick mid, Thursgate mid and Quintrell SI off the platform's venue list and send"
- **REVIEW** `router_configuration_2026.pdf`: carries 11 of 17 distinctive words of the committed call: "The board should keep Delvenne lit, Ardenwick mid, Thursgate mid and Quintrell SI off the platform's venue list and send"

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `order_execution_policy_2025.pdf`: 3 of 25 stump-paragraph terms appear (record, second, provider); read whether the document names the move

## 6 ranking artifacts (REVIEW 1, INFO 2)
- **REVIEW** `venue_volume_report_2025.pdf`: names 5 of 9 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `order_execution_policy_2025.pdf`: names 7 of 9 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `venue_register_2026.xlsx`: names 7 of 9 answer-set candidates; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `uk_trading_calendar_2025-12-01_to_2027-01-31.csv`: 72 ISO dates after 2026-11-20, e.g. 2026-11-21, 2026-11-22, 2026-11-23, 2026-11-24, 2026-11-25

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read

Round 3 (target.zip 7718f1c7, the shipped pack), one isolated reader at medium effort that read only a fresh copy of prompt.txt and target/; rounds 1 (93bbb64c) and 2 (d6135883) are summarised in the design note's build record.



1. Decisive step: none states it outright. Nearest: order_execution_policy_2025.pdf 4.3, "A venue's adverse move for a client flow is the average adverse move of the fills that flow's orders would receive there, in continuous trading." This names the population as a counterfactual (the platform's fills), not the desk's whole book, but does not say how to build it. The dealing plan's "Platform market orders are small against the market, and each is filled in one execution" is context that points the same way.

2. Ranking or scoring of the candidates on the prompt's question: none. venue_volume_report_2025.pdf ranks five venues by volume share and order share, not by adverse move (see R4).

3. Files that exist only to help the analyst: none stand out. venue_register_2026.xlsx (the THGD/THGM code change, note "Replaces THGD") is the nearest, but a real register carries that. corporate_actions_2026.json and the calendar are ordinary reference data.

4. A figure or name that reads as the answer: none. The only candidate figure is the 1.5 bp threshold in policy 4.3, which is the filed test line (the prompt cites it), not a result.

5. Filed sentence fixing the main figure's population: order_execution_policy_2025.pdf 4.3, "A venue's adverse move for a client flow is the average adverse move of the fills that flow's orders would receive there, in continuous trading. A venue whose adverse move for a client flow is above 1.5 basis points is kept off that flow's venue list." Literal execution: for each of the eight venues, average the 60-second mid-move (against the order, in bp of the fill mid) over the fills that orders like the platform's would get at that venue, continuous session only, and keep off any venue whose average exceeds the line. Supporting text: 4.4 (read from Hessenby executions, last twelve months or year to date, busts left out), dealing plan section 4 (each platform order whole to one venue, filled in one execution) and the plan's dealing points and netting. Nothing says how to weight or select the desk's fills to resemble platform orders; the two asks in the prompt (mean order size against ADV, per dealing point) hand over the platform's size profile.

6. What decides the main answer: an analytical choice (the population and comparison group: the platform's small, single-fill market orders against the desk's mixed fund and algorithm child fills, which differ by venue mix and size). Deciding text: policy 4.3 "the fills that flow's orders would receive there", plus dealing plan section 4. It is not a single field or code reading, not an executed procedure, and nothing is planted. Data semantics (THGD/THGM, busts, UTC, CONT vs auction) are Layer 1 mess around it. Partial hint to note: router_configuration_2026.pdf says small direct-market-access orders go only to five venues and DMA screens are not connected to the midpoint books; that points to which executions resemble platform orders, but only as routing context.

## Sweep items
R1. harmless: the figure is the 1.5 bp line (and 60 seconds) in 4.3, the filed test the prompt itself cites; it is a threshold, not a venue result.
R2. harmless: the policy shares vocabulary with the answer sentence because it is the governing test (adverse move, venue list, basis points, flow). It states the rule, not the outcome or the population construction.
R3. harmless, with a small caveat: the router configuration names venues, DMA size band and which venues the desk's screens reach, so it shares words with the answer sentence. It gives no adverse-move result. The caveat is that it separates DMA-reachable venues from algorithm-only ones, which is background for which fills resemble platform orders. That is a filed fact of the world, not an instruction on method.
R4. harmless: it ranks five venues by share of volume and orders and passive/aggressive split for 2025, not by adverse move or any 60-second move. Volume order cannot be read as a keep-off ranking. It is a legitimate distractor (stale year, wrong measure).
R5. harmless: the calendar runs to 2027-01-31 because the plan starts dealing on 4 January 2027 and the dealing-point mapping needs future business days. Dates are OPEN/CLOSED only; 2027-01-04 is OPEN (Monday), 2027-01-01 closed. They carry no results.

## Realism tells
- Dates and calendar check out: 2026 bank holidays (4 May, 25 May, 31 Aug, Good Friday 3 Apr, Easter Monday 6 Apr, Christmas Friday, substitute Boxing Day Mon 28 Dec), 24/31 Dec early closes, 4 Jan 2027 a Monday. Settlement of the first Gresmere note (30 Dec 2025 trade, 2 Jan 2026 settle) respects the 1 Jan closure.
- order_execution_policy_2025.pdf Annex A lists THGD, withdrawn 29 May 2026 (register and router say so); a stale annex in a 2025 policy is plausible, no contradiction.
- venue_volume_report_2025.pdf: top five plus 18.1% for the midpoint books sums to 100.0; "Published 28 April 2026" fits an annual venue report. Fine.
- gresmere contract notes: "consideration_gbp" is gross plus charges on buys and gross less commission on sells (not gross consideration), so the column name is misleading; plausible broker-note net amount and a Layer 1 trap, not a contradiction.
- Gresmere file name says settling to 2026-11-03 while the last trade date is 30/10/2026; consistent with T+2.
- Pemberwick workbook prices are in GBP, Hessenby in pence; times local vs UTC; month tabs: ordinary multi-source mess.
- wealth_dealing_plan_2027.pdf: board paper authored by the COO in October, board meeting 9 December; consistent with the prompt and policy 4.2 and 6. The paper says "the venue showing the best price for its full size", unusual for a document author to specify but plausible.
- securities_master: names like "BJM plc" and tickers such as "XNR" are slightly generic, nothing placeholder-like. 120 securities, sensible ADVs.
- Nothing hidden: workbooks have visible sheets only (venue register one sheet, Pemberwick ten month tabs).

Main thread on the sweep's stump-vocabulary line (record, second, provider in the policy): the evidence clause 4.4 and the 60-second horizon; harmless.
