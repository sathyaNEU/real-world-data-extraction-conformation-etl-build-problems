# leak check, task213

**Verdict: REVIEW.** 17 files read, 38 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: escrow, wallet, seller, golden, account, ledger, rating, platform, quarter, reader, sentence, sellers, purchase, nothing, honest, shared, shipped, small-ticket, decisive, ledgers, control, tablets, playbook, family, return

## 3 answer figures in the pack (REVIEW 4)
- **REVIEW** `escrow_orders_2026-07.csv`: golden figure 15,102 appears: ...32Z,2026-07-09T19:59:32Z,released,osuswap42,ansaha15,102.550000,GHS,1703.69,mobile_money,1.025500 CXSMV8A7...
- **REVIEW** `integrity_notices_2026.pdf`: carries 4 of 7 distinctive words of the committed call: 'The 1 December integrity notice should report that the Q3 2026 sweep expunges 5,900 ratings.'
- **REVIEW** `moderation_playbook_v4.2.pdf`: carries 6 of 7 distinctive words of the committed call: 'The 1 December integrity notice should report that the Q3 2026 sweep expunges 5,900 ratings.'
- **REVIEW** `transparency_report_2026q2.pdf`: carries 4 of 7 distinctive words of the committed call: 'The 1 December integrity notice should report that the Q3 2026 sweep expunges 5,900 ratings.'

## 4 design-note vocabulary (REVIEW 6)
- **REVIEW** `integrity_notices_2026.pdf`: 4 of 25 stump-paragraph terms appear (account, rating, quarter, playbook); read whether the document names the move
- **REVIEW** `merchant_programme_terms_mp2.pdf`: 3 of 25 stump-paragraph terms appear (wallet, account, rating); read whether the document names the move
- **REVIEW** `moderation_playbook_v4.2.pdf`: 8 of 25 stump-paragraph terms appear (escrow, seller, account, rating, quarter, control); read whether the document names the move
- **REVIEW** `support_desk_procedure_sd04.pdf`: 4 of 25 stump-paragraph terms appear (escrow, seller, account, return); read whether the document names the move
- **REVIEW** `transparency_report_2026q2.pdf`: 6 of 25 stump-paragraph terms appear (escrow, seller, account, rating, quarter, sellers); read whether the document names the move
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: 'Send it as q3_ratings_sweep.xlsx with one line per ring (its accounts suspended, the Q3 ratings they gave, those the holdback keeps for manual review and those expunged) and the notice figure, plus q3_sweep_chart.png sho'

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

### Round 1 (stage 4, target.zip c745b735, one isolated reader at medium effort), and the main thread's rulings

- **Q1 decisive step:** none. The playbook states the sweep's rules (1.2, 2.1 to 2.3, 3.1 to 3.4), not how rings show in
  the data; no file says which accounts form rings or how to link accounts to one controller.
- **Q2 ranking or sizing files:** none. The integrity notices (Q1 and Q2 totals) and the transparency report
  (prevalence by quarter) are other quarters' context, the declared wrong-basis distractors.
- **Q3 describing files:** the Outcome codes sheet in `support_cases_2026q3.xlsx`, a code legend a desk export
  carries. Ruled harmless.
- **Q4 figures that read as the answer:** none.
- **Q5 filed sentences:** playbook 1.2, 2.2, 3.1, 3.2, 3.3, 2.1 and 2.3, each read literally as the fork table reads it
  (SF1 to SF10). The reader's note on 3.3 (which received ratings are held, and whose expunged ratings count against the
  cap) is closed by SF4 and SF5, both asserted, and the judge reproduced the 597 held on the golden reading.
- **Q6 what decides:** an analytical choice, which accounts one person or group controls; agrees with the judge's
  Gate H. Playbook 2.3 (the agent-point tablets) is a filed lower rung, and R3a and R3b show the decisive step is the
  loop across the escrow and the wallet (the route with the tablets set aside still files 2,400).
- **Q7 realism:** schema drift, uneven monthly counts, banded fees and a non-stepping order key read as exported.
  The score clumps at -10, -5, 0 and 5 are the rating scale's ordinary use (most raters give 10, the rest cluster on
  round values); ring accounts rate 10 like three honest raters in four, so the scores carry no ring signal. Ruled
  harmless. The playbook's one-rule-per-step neatness noted and kept: it is the governing document the sweep runs on.
- **Q8 the asks:** the dispute window, "withdrawn", the decision's direction, the market, and the withdrawal and
  cashback bases were raised. The judge recomputed every ask figure on the golden reading and flagged only the
  withdrawn-case reading, closed before ship in the prompt (round 2).
- **Flagged files:** all seven harmless.

### Round 2 (after the prompt's disputes sentence changed; target.zip unchanged, c745b735; one isolated reader at medium effort)

- **Q1:** none; the changed sentence says nothing about the main answer. **Q6:** an analytical choice (which accounts
  one controller runs, from devices, wallet transfers, handles and the tablets); nothing planted, no single field or
  stated rule decides it.
- **Q8, the new parenthesis** ("orders with a case opened on them, withdrawn or decided, each counted once"): states
  only what is counted (the unit, the inclusion of withdrawn cases, the dedup) and gives no method; leaves no reading of
  "dispute" open.
- **Readings the reader still raised, each closed by the data and now asserted in `checks.py`:**
  - the Q3 window (opened or decided, WAT or UTC): every case opens and is decided more than an hour inside the
    quarter (day 3.8 to day 88.0), so every reading counts one set;
  - "decided for the buyer" on orders with two cases: on the order a case is about (SD-04 1.2), every order's cases
    point one way; the mixed combinations exist only under the cited `order_ref`, which is the ask's device;
  - the market: every disputed order's buyer and seller share a market, and every cashback buyer is in its group's
    market;
  - the withdrawn amount (ledger requests or custodian transfers): each transfer equals the requests behind it, so with
    the month fixed by the prompt (the transfer's UTC confirmation) both give one total;
  - "different buyers": accounts, the only buyer identity the records hold.
- **Q7 realism:** nothing reads as generated. **Flagged files:** all seven harmless.
