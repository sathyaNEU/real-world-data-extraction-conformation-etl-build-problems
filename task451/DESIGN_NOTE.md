# task451 design note

Architecture 2, re-rooted 2026-10-13 (wave 2, oviya1301). Architecture 1 (aid statistics: the members' money followed through two pooled funds) was spent at design when the honest swap test failed; its record is in the card's lineage and in `## Tried and rejected`.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task451.json`, architecture v2, registered 2026-10-13 with architecture 1 in `lineage`. `guard.py check` returns WARN only. Each WARN is answered here.
  - `repeat.gate_g` and `overuse.gate_g` (method_or_model_selection, 7 of the last 12): the honest label for a development basis pinned by the data. The mechanism (a payment process that changed inside a claims lag triangle) is on no other card.
  - `repeat.decision` (designation_set) and `repeat.question_form` (which), both against task450 v2: the agreement settles partner by partner, so the call names the partners that owe. Domain, gap and mechanism all differ from task450's test equating.
  - `test.same_driver_older` against task135 v2 is differentiated on the card. task135 measures co-movement between holdings priced at different times of day; this build completes a closed year's unpaid claims from a triangle whose payment process changed.
- **Pairing:** Healthcare Delivery & Health Economics / payment-claims-health-plan-analytics / Data Extraction & Conformation (ETL). Claims from the administrator's extract (versions, two date bases), an hour-bank eligibility file and a monthly attribution roster are conformed into the partner agreement's total cost of care, incurred in 2026 whenever paid, per attributed member month. Completing the latest service months from a claims lag triangle is the task type's own method; the client names it as the type's first rigor pattern.
- **Objective:** ETL. The conformed dataset is each partner's 2026 total cost of care on the agreement's basis, judged against the agreement's corridor.
  - Retrospective by design: the agreement settles a closed performance year, and the open part is the claims run-out, which the estimand includes.
  - Not retaggable as Forecasting: no future value is predicted. The quantity is a closed year's incurred cost, completed from the claims already received and paid.
- **Shape:** other, a register of the twelve partners against their targets. Criteria arithmetic (planned; the ask sheet fixes it at design):
  - the call: whether each partner owes, 12;
  - two per-partner asks on measures the call does not use: 2026 inpatient admissions and 2026 pharmacy cost, 24;
  - the two files: 2.
  - About 38 in all.
- **Strategy:** maturity_censoring. The open service months are not fully developed. The decisive move is which development describes the claims still to come, after the payer's adjudication sped up inside the history.
- **Mechanism:**
  - Gap: time (decisive: the development history was paid by a process that no longer pays), with population supporting (the attributed member months).
  - Generators: G7 decisive (the operating window of the adjudication process), G16 (the method the data select), G17 (the margin, asserted).
  - Gate G: method_or_model_selection. Layer 2: field_method, `own:development-on-the-payment-process-in-force`.
- **World:** the Laurelford Building Trades Health and Welfare Fund, a jointly trusteed multiemployer fund in western Pennsylvania covering about 10,500 lives.
  - Its claims are administered by Keswold Benefit Services and its pharmacy benefit by Corvane Pharmacy Benefits; the claims funding runs through Halberd National Bank.
  - Since 2025 it has had accountable care agreements with twelve partner groups. Each partner has a 2026 target cost per attributed member month, and a partner whose total cost of care is more than 2 per cent over its target pays the Fund a share of the excess.
  - Keswold moved the Fund's claims onto its Tallis platform on Monday 5 October 2026. Payment runs went from weekly (Thursdays, after network repricing and review) to every business day.
- **As-of:** claims paid through Friday 29 January 2027 (the agreement's settlement basis), the extract run on Monday 1 February 2027, and the trustees' meeting of 17 February 2027 approving the settlement notices.
- **Furniture:**
  - Forum trustees_or_governors (the Fund's board of trustees); forcing event purchase_order_or_contract (the agreement's annual reconciliation); organisation cooperative_or_member_body (a jointly trusteed multiemployer fund).
  - Role research_desk (the administrative office's health analytics lead; the prompt names no one); context artifact filed_standard (the partner agreement); calibration none.
- **People:** drawn with `guard.py names --geo "United States" --seed 451` and on the card: Ariel Hogan (Fund administrator), George Khan (Fund controller), Jason Pollard (Keswold's account executive), Linda Austin (chair of the trustees' health committee).
- **Data-native sentence:** every claim in this pack carries two clocks, the day the administrator received it and the day it paid it.
  - The providers' delay to the first never changed. The administrator's delay from the first to the second fell from about five weeks to a day when the Fund's claims moved to Tallis on 5 October 2026.
  - So a lag triangle of paid dates mixes two payers' speeds, and the last months of 2026 owe far less than the history says.
  - On a claims book whose adjudication speed never changed, the trap does not exist.
- **Sources, one line each:**
  - `layer2-rigor-patterns.md`, payment-claims-health-plan-analytics pattern 1 (complete recent claims with lag-triangle factors; shortcut: paid as extracted): taken one step further. Paid as extracted is a lower rung here, and the textbook completion is itself the trap, because its factors were measured under a payment process that no longer pays.
  - `two-layer-task-design.md`, field_method (development triangles): the field's method done right includes checking that the development measured is the development in force.
  - `strategies.md`, maturity and the process the window never saw: the claims outstanding at the cut are paid by a process the triangle's history never saw.
  - `layer1-messiness.md`, Healthcare 3 (claim headers and replacement bills collapsed to the final action claim) and 1 (identifiers that do not line up, here the pharmacy benefit manager's cardholder and person code): Layer 1, none of it on the decisive step.
- **Prototype** (scratch `t451v2/proto3.py`, `proto4.py`; seeds 7, 8 and 9; about 190,000 claims): every paid-date chain ladder overstates 2026 against the received-date development.
  - All history: +9.9 to +10.2 per cent. The latest twelve diagonals: +8.3 to +8.8. The latest six: +6.2 to +6.5. The latest four (the go-live month included): +5.1 to +5.8.
  - The diagonals after the go-live month (the backlog cleared): +2.7 to +3.2. Paid as extracted: -2.6 to -3.1.
  - The received-date development over all history and over the latest twelve months agree within 0.3.

## Default path

The pipeline the measured opponent builds unsteered, from the prompt's words and the files' grain:

1. Read the partner agreement: total cost of care is the Fund's paid amount for medical claims with a first date of service in 2026, for members attributed to the partner in the month of service, whenever paid, pharmacy excluded, each member's year truncated at $200,000, over attributed member months; the corridor is 2 per cent over each partner's target.
2. Collapse each claim to its final version in the extract (replacements and voids by their frequency codes) and keep the medical claims with a first date of service in 2026.
3. Build attributed member months from the eligibility file and the monthly roster, and truncate each member's 2026 amount at $200,000.
4. Complete 2026: a lag triangle of paid amounts by month of service and month of payment from January 2025, volume-weighted chain-ladder factors over all of it, each service month's factor applied to each partner's paid amount for that month.
5. Divide by member months, compare with each partner's target plus 2 per cent, and name the partners over it.

**Ends on:** seven partners owe (the four the golden names, and three whose completed cost sits between about 3 and 9 per cent under the corridor and is lifted over it by the completion; design placement, the generator names them).

**Golden:** four partners owe. The 2026 claims are developed on their received dates, whose provider submission lags never changed (or on the payments made after the go-live month's backlog cleared, which lands the same four), and the latest service months owe what the administrator now pays within a day of receipt.

## Stump sentence

The default path names seven partners because step 4 completes 2026 with chain-ladder factors averaged over the 2025 and 2026 paid-date triangle, which carry Keswold's old five-week adjudication into the October to December 2026 claims that Tallis pays the day after it receives them, overstating 2026 by about ten per cent; developed on the received dates, whose provider lags never changed, four partners owe.

## Three rules

**Task type:** payment claims health plan analytics (`payment-claims-health-plan-analytics`), serving the ETL objective: the administrator's claims, the hour-bank eligibility and the attribution roster conformed into the agreement's incurred total cost of care per attributed member month, the open months completed from the claims lag triangle.

**Domain test:** the deciding quantity is each partner's 2026 incurred medical cost per attributed member month. Health plan analytics estimates it by completing the latest service months from a claims lag triangle, and checks that the development measured is the development of the claims still unpaid; when adjudication speeds up, it develops the claims on their received dates.

**Swap:** "which accountable care partners owe a shared-loss payment for 2026, now that claims paid through January are in" becomes "which schools owe the district for overspending their 2026 budgets, now that January's ledger is in": there is no claim, no lag from service to receipt to payment, no adjudication platform and no triangle, so the completion that decides the call has nothing to act on.

**Layer 1:** what these systems produce, none of it on the decisive step.
- The administrator's extract carries every version of a claim: originals, replacements and voids, by their 837 frequency codes.
- Every claim has two date bases: service from and through, and received and paid.
- The Fund's eligibility is earned through an hour bank, with retroactive months when an employer's late contributions post.
- The attribution roster is a monthly snapshot by primary care provider of record.
- The pharmacy benefit manager's file is keyed by cardholder and person code, not by member id.
- The agreement truncates each member's year at $200,000.
- The bank's funding wires follow the payment-run calendar, weekly and then daily.

**Layer 2:** field_method (development triangles). Development measured on a payment process no longer in force misstates what the open months still owe. The expert completes on the process that never changed (the providers' submission, through the received dates), or on the payments made since the change settled.

**Decisive step:** completing the open 2026 service months with development that describes the claims still unpaid at the cut. These are claims Tallis pays the day after it receives them, so they are developed on their received dates, whose provider lags never changed, not with chain-ladder factors averaged over a paid-date history that Keswold's old five-week adjudication produced.

**Not semantics:** every field read right (the frequency codes, both date bases, the hour bank, the roster, the truncation) still leaves the completion to be chosen. The default path reads every one of them correctly and completes with the paid-date chain ladder, the field's textbook method, and lands seven partners.

**Not rule application:** the agreement files the WHAT (claims with a first date of service in 2026 whenever paid, attributed member months, the truncation, the corridor) and says only that the Fund estimates the claims not yet paid. No rule names a triangle, a basis or a set of factors, so executing every filed rule still leaves the default path on seven partners.

**Analyst test:** a strong analyst who keeps each claim's final version, builds attributed member months from the eligibility and roster, truncates each member's year at $200,000 and completes 2026 with chain-ladder factors from the paid-date triangle over all of 2025 and 2026 names seven partners as owing (the default path's `Ends on:`). Developing on the received dates names four.

**Estimand:** the partner agreement, Schedule B (`accountable_care_partner_agreement_schedule_b.pdf`). Total cost of care for 2026 is the Fund's paid amount for covered medical services with a first date of service from 1 January to 31 December 2026, for members attributed to the partner in the month of service, whenever paid, excluding outpatient prescription drugs, each member's year above $200,000 excluded, divided by attributed member months. The Fund issues the reconciliation from claims paid through the last business day of January, estimating the claims incurred in 2026 and not yet paid. A partner owes if its total cost of care is more than 2.0 per cent over its target.

**No decoy:** nothing is planted to be caught. No memo, draft, consultant's table or prior reconciliation states a completion factor, a reserve or a partner's 2026 result, and the administrator's dictionary dates the platform change as an ordinary release note.

**No certified replay:** no shipped figure is reproduced to recover a method. The 2025 claims have run out, so any completion back-tests on them, and nothing certifies a factor.

**Lesson:** a claims lag triangle is a record of how the payer paid. When adjudication speeds up, development measured on paid dates overstates what the newest months still owe, and the claims are developed on the clock that did not change; no build on file teaches it (the nearest driver on file is task181 at 0.07).

## Tried and rejected

- 2026-10-13, architecture 1 (Survey Research & Official Statistics, aid statistics: the members' money followed through two pooled funds, Kenya, Rwanda and Mali for the offices), spent at design before its pack shipped. The honest swap test fails: with a fund-of-funds' or a franchise marketing levy's nouns the task reads the same, crediting a pool's spending to its contributors by what the pool held when it paid, so the decisive step is generic fund accounting and the domain was the backdrop (10/10 rule 1). Its generator and pack were removed at the re-root and stay in git history (commit 78f1fe8).
- 2026-10-13, architecture 1's design record, kept as written:
  - 2026-10-13, draw: the draft's vote at the council (vote_or_meeting) and a ranked list under a cap (shape 01). Rejected: task255 holds the forcing event and task256 the shape in the window; the host-country agreements and leases force the decision (purchase_order_or_contract) and the answer is built as a bridge from the members' own records to the money spent (shape 03).
  - 2026-10-13, draw: attribution at a transition (G4) as the decisive generator. Rejected: task450 v2 holds the pattern in the window; the members' money is provided elsewhere, through the funds (G5).
  - 2026-10-13, design: the second fund layer (the global fund's money inside the Sahel fund) as the decisive step. Rejected: the transfer is a provider-receiver join the solver already holds the key to (screen test 2), and the estimand's "one or more pooled funds" files it, so a careful solver lands it; the prototype also moved the three only at fifth place. It stays on the default path, and the decisive step moved to the money each fund held when it paid (G6).
  - 2026-10-13, design: shape 03 (a bridge between totals). Rejected: a bridge from the members' payments to the money spent walks the solver through the funds' timing and hands over the decisive step; the answer is a register of 13 countries with three measures (shape other).
  - 2026-10-13, design: a payer-and-receiver reconciliation ask keyed on year-end receipt dates. Rejected: an ask about money crossing the year end points at the funds' timing; the asks carry identity and version devices instead.
  - 2026-10-13, design: a shared decisive pool for both funds (one share window for both). Rejected: a single window lets a lag heuristic land; the global fund pays out a year late and the Sahel fund the same year, so only the money each fund held when it paid lands both.
