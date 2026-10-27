# task304: which mortgage book the 2027 financial support team works, and the possessions it avoids there

Wave 6, Opportunity Sizing & Decision Support, perssathya. Architecture 1, drawn 2026-10-26 off the seed: OS06's
whole-home retrofit world died six times at call-only probes and a water-meter world once more (Tried and rejected),
so the number was redrawn in banking. Prototype call-only probes on this world (an isolated sonnet and an isolated opus
thread at medium effort, prompt and pack only) both missed the call: sonnet filed High LTV 2022-24 at 25 avoided on a
payment-shock onset model, opus filed High LTV at 29 on a Poisson entry hazard with a book-specific payment-shock effect
by months since the shock; neither examined the remaining-term history.

## Draw

| Axis | Value |
|---|---|
| Domain / task type | banking-credit-financial-risk / collections-recovery (serves Opportunity Sizing) |
| Objective | Opportunity Sizing & Decision Support: the headline is the possessions the team avoids in the chosen book, sized from the pool (the book's borrowers who fall two payments behind in 2027) to the realisable (each taken on, possession chance cut by 15 per cent), and the largest figure picks the book |
| Decision / answer unit / question form | pick_one_of_n / count / which |
| Gap / pattern / generators | time, population / none / G3 (record versus operation), G6, G13 |
| Gate G / strategy | forecasting / composition_mix: the 2027 pool holds far more extended accounts than any period a hazard is fitted on |
| Layer 2 | field_method, own:forbearance-carried-as-a-state-in-the-arrears-entry-forecast |
| Forum / forcing event / org family | committee_or_panel (the Society's Credit Committee) / launch_or_rollout (the team starts in January 2027) / financial_institution |
| Stakeholder | Aimee Atkinson, Head of Collections and Recoveries (operations_director) |
| People (guard.py names --geo uk --seed 304) | Aimee Atkinson; Oliver O'Brien, Financial Support Team Manager (the pilot report); Elliot Hunt, Chief Risk Officer (the risk appetite statement) |
| World | Calderbrook Building Society, West Yorkshire and the Pennine towns, GBP; records at 30 September 2026, plan paper October 2026 |
| Deliverables | support_team_2027_placement_paper.pdf (the Committee paper), support_team_2027_workbook.xlsx |
| Guard | WARN only: repeat.gate_g and repeat.decision against task166, repeat.question_form against task270 and task166; test.same_driver_older differentiated against task169 v2 |

The WARNs, answered: the decisive quantity is a forward count, so forecasting is the honest Gate G; the Committee
chooses one of four books and sizes it, so the decision is a pick with a figure; the Committee's question is which.
The axes redrawn at the check: `context_artifact` register to monitoring_export (the monthly loan-level extract is the
honest label; register repeated task270), and the decisive generator from G6 to G3 with time as the decisive gap (the
record shows an up-to-date account because of the Society's own operation, and the re-entries fall after the window the
record measures), after (population, G6) and (population, G3) repeated older and in-batch signatures.

## Default path

The strong analyst's route, every field read correctly and every filed rule applied (final world, seed 2, the plan's
printed planning rates: First-time buyer 2019-21 4.5 per cent, High LTV 2022-24 7.4, Shared ownership 1.9, Buy to let
10.7):
1. Rebuild payments in arrears at each month end (arrears balance over the current contractual payment, rounded down,
   policy section 2) and mark each entry, a month the account reaches two or more from fewer than two.
2. Fit the monthly chance of each move between nought, one and two or more payments behind on the 2024 to 2026
   history, by book and by the payment rise at the account's last rate switch (the probes added loan age, months since
   the switch, or the rise since completion).
3. Carry every account on the book at 30 September 2026 that is not in litigation or with a receiver through 2027,
   counting each account once, at its first entry, with no allowance for accounts that close (plan section 2).
4. Take 15 per cent of each book's expected entries times its planning rate: High LTV 2022-24 4.5 possessions avoided,
   First-time buyer 2019-21 2.9, Shared ownership 0.6, Buy to let 1.2.
Ends on: High LTV 2022-24, fewer than 5 possessions avoided (4.5), the first-time buyer book at 2.9.
Golden: First-time buyer 2019-21, about 10 possessions avoided (9.0), with High LTV 2022-24 next at fewer than 5 (4.5),
once each account whose remaining term rose at its rate switch is carried on the chance the earlier such accounts show
by months since the increase.

## Stump sentence

A competent solver fits the chance of falling two payments behind on book, current arrears and the payment rise at the
last rate switch, carries every account on the book through 2027 at the plan's planning rates and files High LTV
2022-24 first (4.5 possessions avoided against the first-time buyer book's 2.9); the step that lands it there is reading
the up-to-date first-time buyers' small payment rise as low risk when their remaining term rose at the switch, the
Charter extension that kept a budget the new rate broke up to date for a few months.

The data-native sentence: in the payment history 7,129 of the 16,455 first-time buyer accounts on the book at 30
September 2026 had their remaining term raised, by a median of ten years, at the 2026 switch off their 2021 five-year
fix, so their payment rose by a median 10 per cent where the switchers who kept their term saw 26 per cent, and of the
347 accounts whose term rose in 2024, 4 were two payments or more behind at a month end within eight months of the
increase and 81 were by 30 September 2026.

## Three rules

Task type: banking-credit-financial-risk / collections-recovery, which serves Opportunity Sizing: a collections function sizing where a support team avoids the most possessions.
Domain test: the deciding quantity is each book's 2027 entries into two payments of arrears, the collections forecaster's arrears-entry hazard carried account by account with forbearance as a state: a term extension at the rate switch lowers the payment and keeps the account up to date while the budget the new rate broke stays broken, so the account carries its own hazard by months since the concession.
Swap: "which hospital ward should the discharge team work, and how many readmissions would it avoid" keeps a pick and an effect size, but the object that decides, an account whose remaining term rose at a rate switch so its payment barely moved while the borrower could not meet the new rate, and the concession's delayed fall into arrears eight to fifteen months later, has no ward equivalent; with the nouns swapped the rate switch, the Charter extension and the arrears-to-possession route stop making sense.
Layer 1: the Society's own systems produce every mess item: product codes that lost their dashes at the July 2022 platform change, month rows re-sent in a later extract, payments in arrears derived from an arrears balance in pounds against the current payment, a possession register dated day-first that keeps the book each row was written under, arrears capitalised by collections clearing without a payment, properties in possession still on the book until they sell, and redeemed accounts absent from the book snapshot; none decides the call (each asserted not to move it).
Layer 2: field_method, the arrears-entry forecast with forbearance as a state: the 2027 entries come from each account's hazard given its concession history and the months since the concession, not from its current arrears and the payment change it shows.
Decisive step: carrying each extended account forward on the delayed re-default chance the 2024 and 2025 extensions show by months since the extension, instead of on the chance its up-to-date status and small payment rise imply.
Not semantics: every field read correctly (remaining_term_months is the months left to run) still leaves the easy route on High LTV, because no field says an account is forborne: the extension is an event read from the path of the remaining term, and the forecast still has to estimate what that event does to the hazard and when, from the earlier extensions' own outcomes.
Not rule application: no filed rule forecasts entries; the plan paper files who is counted, the year, the book as it stands at 30 September 2026, the planning rate and the 15 per cent cut, and leaves the entry forecast to the analysis. Measured on the final pack (seed 2): the enumerated family (the stock already two behind, this year's pace, a book-level chain, the payment-rise chain, a rate-rise chain by months since the switch) files High LTV with the first-time-buyer book at 0.6 to 3.7; the standing family (twenty-two constructions that carry the extension as a state, across banding, smoothing, fit window, the switch's rise, the closing month and one curve for every extended account) files the first-time-buyer book at 8.0 to 11.9, every member in the 10 bin and High LTV under 5 in every member; the ruling-out is quiet, since no clause, flag or one-group-by comparison on any shipped column separates the extended accounts.
Analyst test: a strong analyst fits the monthly chance of an account falling two payments behind on book, current arrears and the payment rise at its last rate switch, carries every account on the book through 2027 at the plan's planning rates and files the High LTV 2022-24 book first at 4.5, while the 2021 first-time buyers who extended their terms at the 2026 switch fall behind eight to fifteen months later and make the first-time-buyer book the largest at about 10 (9.0).
Estimand: the plan paper (financial_support_team_2027_plan_paper.pdf, sections 2 and 3) files the population (each book's borrowers whose account first reaches two payments in arrears from fewer than two during 2027, the accounts on the book at 30 September 2026, excluding accounts in litigation or with a receiver, each taken on once), the outcome (possession within 18 months of that month, at the book's own printed planning rate), the window (calendar 2027), the unit (possessions avoided, expected) and the comparison (the team cuts the chance by 15 per cent, the pilot report's planning figure), each account on the book counted through 2027 with no allowance for accounts that close.
No decoy: nothing is planted to be caught: the extensions are the Charter process the arrears policy describes in one line among its support options, no memo, draft or stakeholder figure argues for a book, and no file ranks the books on the decision.
No certified replay: no published or certified figure in the pack reproduces the method; the pilot report gives the 15 per cent planning cut and its own counts, which the history, the litigation actions and the receiver appointments reproduce.
Lesson: a borrower's up-to-date status after a concession is the concession's work, not evidence of health, so the concession history is a state the forecast carries with its own clock; no build on file teaches forbearance as a forecast state (task128 sized an early-arrears contact queue, task446 converted watch-list flags by the component that raised them).

## Readability screen

| Rung | What it needs | Verdict |
|---|---|---|
| payments in arrears at each month end | policy section 2 (the arrears balance over the current payment, rounded down) | readable |
| who is taken on, counted once, in 2027 | plan section 2 | readable |
| the planning rate and the 15 per cent cut | plan section 3, the pilot report | readable |
| the rate switch and its payment rise | the product code in the history (dashes lost before July 2022) | readable |
| the term raised at the 2026 switch and the delayed fall into arrears it carries into 2027 (decisive) | no sentence; the path of remaining_term_months in the history and the earlier extensions' outcomes | silent |

## Ladder

| Rung | Construction | First-time buyer | High LTV | Shared ownership | Buy to let | Call |
|---|---|---|---|---|---|---|
| R0 | the accounts already two or more behind at 30 September 2026 as the caseload | 0.6 | 0.8 | 0.2 | 0.3 | High LTV |
| R1 | this year's pace (January to September 2026 entries, annualised) | 2.9 | 4.9 | 0.6 | 1.3 | High LTV |
| R2 | a book-level chain (book and arrears only) | 2.1 | 4.5 | 0.7 | 1.2 | High LTV |
| R3 | the default path: the chain by book and the payment rise at the last switch | 2.9 | 4.5 | 0.6 | 1.2 | High LTV |
| R4 | the rate rise at the switch by months since the switch | 3.7 | 4.6 | 0.7 | 1.3 | High LTV |
| R5 | the golden: the term increase as a state by months since it, beside the payment rise | 9.0 | 4.5 | 0.6 | 1.2 | First-time buyer |

R3 is the stump and R4 the closest repair that misses (it models the switch's timing, not the concession). Every rung
is asserted in checks.py. Possessions avoided are expected values; the prompt rounds them to the nearest ten, so the
golden files the first-time buyer book at 10 and every other book under 5.

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | in 2027 | calendar 2027, January to December | the team's first twelve months from 4 January | same call | plan section 2: during 2027 |
| SF2 | reaches two payments in arrears | the month-end position reaches two or more from fewer than two | a count of missed payments from the receipts | another count | plan section 2 and policy section 2: the arrears balance over the current payment, rounded down |
| SF3 | taken on | once per account, at its first entry in 2027 | every entry in the year | same call (asserted) | plan section 2: in the first month of the year it does so |
| SF4 | the book | the accounts on it at 30 September 2026, none opened later | the book as it will stand in 2027, new lending included | same call (asserted) | plan section 2: the accounts on it at 30 September 2026 |
| SF5 | left with the recoveries team | recovery_stage Litigation or Receiver appointed at 30 September 2026 left out | kept in | same call (asserted) | plan section 2 |
| SF6 | the planning rate | the plan's printed rate for each book | a rate recomputed from the history and the register | same rates (asserted) | plan section 3 table; the recomputation reproduces it |
| SF7 | the team's effect | 15 per cent of the expected borrowers taken on times the planning rate | the pilot's own ratio on four payments behind (0.66, about 35 per cent less often) | same call, another figure | plan section 3: 15 per cent of its expected 2027 borrowers taken on times its planning rate; the pilot report: a 15 per cent cut for planning |
| SF8 | possessions avoided | an expected number, from expected entries | a whole-number draw | same call | plan section 3 (expected) |
| SF9 | the next best book | the second-largest possessions avoided on the same measure | the second-largest pool | same book | plan section 3: the book with the most possessions avoided is the one to choose |
| SF10 | the team's capacity | no cap: about 1,900 cases against at most 1,338 expected in any book | a cap at the capacity | same call | plan section 2: no borrower who qualifies is turned away |
| SF11 | the rounding | each book's unrounded expected figure to the nearest ten | the pool rounded first | same figures | the prompt |
| SF12 | ask A, a claim open at 30 September 2026 | not withdrawn, its order not discharged, no eviction, the property not taken into possession (the register, which Ridley Varga's reports never reach) | recovery_stage Litigation in the book; the claim file alone | 24, 61, 2; 52, 79, 7 | policy section 5 (a claim stays open until it is withdrawn, the order is discharged or the property is taken into possession); the register |
| SF13 | ask A, an order made or varied at a hearing | an order line after a hearing; a line repeating the claim's previous order with no hearing between is the same order sent again | every order line an order | 38, 83, 10 orders | policy section 5: the court makes or varies an order at a hearing |
| SF14 | ask A, the unit | claims (one panel firm writes a line per defendant) | lines | another count | the asking sentence (claims); the file's defendant column, two lines on one claim and date differing only there |
| SF15 | ask A, owner-occupied books | First-time buyer 2019-21, High LTV 2022-24, Shared ownership | Buy to let included | none (no buy-to-let claim) | policy sections 5 and 6 |
| SF16 | ask B, sold from October 2025 to September 2026 | completion date in the window, on the latest statement | statement dates | same rows | the sales file's completion_date |
| SF17 | ask B, the loss | the debt at possession less the sale price net of fees, nil where the sale covers it | a surplus as a negative loss | another average | policy section 8 |
| SF18 | ask B, a corrected statement | replaces the earlier one | both counted | same figures (asserted) | the statement column: a corrected statement carries the next number on the same sale reference |
| SF19 | ask B, the book | the account's lending book among the plan's four, as the payment history carries it for every account | the register's label read as written (its earlier first-time buyer label is not one of the four) | another split | plan section 1 (the four books); the history's book on every account, closed ones included |
| SF20 | ask B, at a loss | a loss above nil | none | none | policy section 8 |
| SF21 | the book through 2027 | every account on the book at 30 September 2026 counted for the whole year, none netted off for closing first | each account netted for the chance it redeems before falling behind (8.0 on the golden's construction) | same call (asserted), the same bin | plan section 2: with no allowance for accounts that close during the year |
| SF22 | ask B, a possession sold | one property: one sale per account and completion date, its debt every register row of the account (one per loan part) | each completion statement a sale, the register's repeated account a re-sent row | 27/5/2,600, 30/18/22,000, 6/0/0 | the asking sentence (possessions sold); the register: the account's rows share one possession date (asserted) |

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | the accounts on the book at 30 September 2026, not in litigation or with a receiver; none not yet observed (the book is fixed at that date), each counted through 2027 with no allowance for accounts that close | filed (plan section 2) |
| 2 | Unit of account | a borrower taken on at the account's first 2027 entry; expected possessions avoided | filed (plan sections 2 and 3) |
| 3 | Attribution window | entries in calendar 2027; possession within 18 months of the entry, inside the planning rate | filed (plan sections 2 and 3) |
| 4 | As-of dating | the book and the history at 30 September 2026; the plan of 9 October 2026 | filed (file names, plan) |
| 5 | Version basis | the plan's printed planning rates; policy version 7 | filed |
| 6 | Denominator | the planning rate's own (printed); none on the call's counts | filed |
| 7 | Weighting | each account once | filed (plan section 2) |
| 8 | Window length | the fit window is method: from July 2023, January 2024 or January 2025 every construction files the same call in the same bin | C1 (asserted) |
| 9 | Boundary inclusivity | month-end positions; January to December | C1 (asserted) |
| 10 | Rounding path | unrounded expected figures, each to the nearest ten | filed (the prompt) |
| 11 | Tie-break | none: 9.0 against 4.5 | asserted |
| 12 | Maturity and censoring | the 2026 extensions' fall into arrears comes after the record ends; the construction that carries it is the stump | WHAT filed; the decisive step is analytical |
| 13 | Order of operations | expected entries, times the planning rate, times 15 per cent | filed (plan section 3) |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | month rows re-sent in the history dropped (asserted not to move the call); ask A one claim per claim number; ask B the latest statement | asserted |
| 16 | Identity normalisation | product codes compared with the dashes taken out; one account numbering in the history | asserted |
| 17 | Netting against gross | ask B net proceeds, nil loss on a surplus | filed (policy section 8) |
| 18 | Dimensional units | payments in arrears from pounds over the current payment; GBP | filed (policy section 2) |
| 19 | Code and status semantics | account_status, recovery_stage, the litigation actions as each export writes them; the policy defines arrears, the court route and the loss | filed; never the stump |
| 20 | Integerisation | none on the call; ask counts are whole claims and sales | filed |
| 21 | Clause scope | the 15 per cent cut for every borrower the team works with, in any book | filed (pilot report section 3, plan section 3) |
| 22 | Forward window contents | 2027's entries from the book at 30 September 2026, the extended accounts' fall into arrears inside it | C1 across the standing family (asserted, 8.0 to 11.9, every member in the 10 bin) |

## Literal reader

Executing the prompt and every filed sentence word for word (the plan's sections 1 to 3, the policy's sections 2 and
5 to 8, the pilot report, the field descriptions) leaves one open move on the call: how each account's chance of first
reaching two payments in arrears in each month of 2027 is forecast. The estimand is filed literally (who is taken on,
counted once, in calendar 2027, the book as it stands with no allowance for accounts that close, at the printed
planning rate, cut by 15 per cent), every construction that carries the extended accounts on the chance the earlier
extensions show by months since the increase files the first-time buyer book at about 10 (8.0 to 11.9 across the
standing family, asserted, smoothing weights from none to 100 account-months included), and the constructions that
carry them on their current arrears and small payment rise file High LTV first at 4.5: an easy method on the same
literal estimand, never another reading of it.

## Oracles

None on the call: no file forecasts or ranks 2027 entries, and the plan's printed rates are inputs both routes share.
The pilot report's counts reproduce from the history, the litigation actions and the receiver appointments (asserted in
checks.py, recomputed in verify.py). On the asks there is no control
total: the possession register settles which open claims have ended in possession (ask A) and the payment history
carries each account's book (ask B), and neither ties a published figure.

## Ask sheet

**Ask A: in each owner-occupied book, the possession orders the courts made or varied at hearings from October 2025 to
September 2026, how many of those were suspended on terms, and the possession claims open at 30 September 2026 (9
figures, whole orders and claims).** H18: each book's recoveries caseload, the borrowers the team does not take on
because they are already with the panel solicitors (plan section 2), a measure every candidate carries that the call
does not turn on; the call reads none of the litigation file (asserted). Use: the recoveries team's own plan beside the
support team's. Primary device, silent (D2, a re-sent record nothing labels): Pennant Moss's case system writes a
fresh order line whenever the court re-seals an order and sends it again, with the same terms and no hearing between,
so a quarter of its orders appear twice; only the run of actions on the claim shows the second line is the same order.
Interior: a suspended order varied on the same terms at a later hearing is a genuine variation and counts, so dropping
every repeated order over-repairs. Second device on the open claims (D4, absence evidenced in a file no habitual join
reaches): Ridley Varga's reports end at the warrant, so a claim whose property was taken into possession reads open in
the claim file; only the possession register closes it. Hazards: one line per defendant from one firm, hearings listed
and adjourned, transfers between hearing centres. Files: litigation_open_claims, possession_register, mortgage_book,
mortgage_payment_history, arrears policy. Stops (first-time buyer, high LTV, shared ownership, as
orders / suspended / open): every re-sealed line an order 38/30/17, 83/65/43, 10/10/2 (the careful path, which also
closes claims through the register); every line counted, defendants included 39/31/17, 93/72/43, 11/11/2; every
repeated order dropped 34/27/17, 69/54/43, 9/9/2; no look at the register (open) 52, 79, 7; the register checked only
for accounts still on the book (open) 18, 55, 2; the book's Litigation stage as the open claims 24, 61, 2; golden
34/27/17, 71/56/43, 9/9/2.

**Ask B: in each owner-occupied book, the possessions sold with completion from October 2025 to September 2026, how
many of them were sold at a loss, and the average loss per possession sold (9 figures; counts, and pounds to the
nearest hundred).** H18: what a possession costs in each book, a second measure every candidate carries beside the
possessions the team avoids; the call reads none of the sales, receiver or register files (the planning rates are
printed; asserted). Use: the loss budget that goes with the plan. Primary device, silent (D2): an account with a
further advance holds two loan parts, and the Society writes a register row and a completion statement for each, so
one property sold reads as two sales with two debts; only reading the account and the completion date together shows
one possession whose debt is both parts'. Interior: the register's rows before the April 2026 re-cut carry its earlier
first-time buyer book, so each account's book comes from the payment history. Hazards: receivers' sales under their own
reference (the receivers' file holds the account), corrected statements re-sent in full (the later one replaces), a
surplus paid to the borrower (nil loss, policy section 8). Files: possession_sales_completed, possession_register,
lpa_receiver_appointments, mortgage_payment_history, arrears policy. Stops (sold / at a loss /
average loss): each statement a sale, the register's last row as the debt 27/5/2,600, 30/18/22,000, 6/0/0 (the careful
path); each statement a sale, the parts' debts summed 27/9/4,100, 30/30/31,400, 6/4/4,400; one sale per account, the
register's last row 20/5/3,500, 24/18/27,500, 4/0/0; the register's old label read as the 2019-21 book 45/30/18,500,
3/3/22,800, 0/0/none; golden 20/7/4,500, 24/24/33,300, 4/2/3,300.

Main population zero-counts: the call reads the book, the history, the plan and the policy's measurement section, and
none of the litigation, sales, receiver or register files; the asks read those four and the history only for each
account's book (asserted, separation).

| Ask | Cracker (lands the call, runs the battery, executes every filed rule) | Verdict |
|---|---|---|
| A orders, suspended, open | 3 of 9 (the open claims in every book) | miss |
| B sold, at a loss, average loss | 0 of 9 | miss |

Pair ceiling: 37.7 ((54.2 + 21.2) / 2), the cracker keeping 3 of the 18 ask figures on the call and the mirror the same
on the default path's call.
Mirror leakage: 16.7 per cent of ask weight.
Measured by: generator/pair.py on the cut pack.

## Pre-ship check

- Free gates (stage 3, final build): generator checks 157 passed (the golden and its bins, R3a the easy routes filing
  High LTV, R0 and R1, the standing family of constructions, SF1 to SF22, the pilot table reproduced, the extension
  facts invariant to the re-sent rows, both asks' stops, separation, the distractors unread, the input gates); two
  builds byte-identical (target.zip 57a875af); the independent verifier 0 mismatches on the cut zip (54 seconds once its
  account filter used a hashed lookup); figures_check 35 of 35; precut 52/0/0 with voice-check PASS (pair ceiling 37.7,
  mirror leakage 16.7 per cent, pair.py on the cut pack).
- leak.py REVIEW, each line ruled harmless: sweep 3, the plan paper carries the call's words because it is the
  Committee's own paper on the choice (the team, the four books, 2027, possessions) and holds no answer figure and no
  ranking (sweep 6 clean); sweep 4, the arrears policy defines payments in arrears, the support options and the court
  route, its one Charter sentence says a borrower who is up to date may extend the term without a fresh affordability
  assessment and nothing on what follows an extension; the risk appetite statement carries the Board's limits only;
  the plan paper files the estimand and names no forecast and no extension; the pilot report gives its eligibility,
  outcomes and result and names no extension; sweep 9, the 54,897 future dates are product_end_date, each account's
  contractual product end (to August 2031), forward by nature (H16 allow-list).
- Leak reader (two reads, the second on the final pack, neither solving): no decisive-step sentence, no analyst-only
  file, no answer figure; question 6 analytical; every rule in leak_check_report.md. The first read's realism tells are
  fixed in the generator: PDFs saved at working-day times on the UK offset with the writer's /Trapped key blanked
  (equal-length rewrite), references numbered from their own stream (no fixed steps), sale prices written as whole
  pounds, the litigation export named for the claims it holds (open at any time from January 2023), and the plan paper
  given its budget line and the Committee's July review.
- Determinism judge pass 1 (zip 5194480e): DETERMINISTIC, APPROVE; Gate G forecasting, analytical non-defect; Gate H
  domain, layers, decisive step analytical. Its three minor notes are closed in the generator: the prompt now asks for
  the next best book's own figure ("how many would it avoid in the next best book?"), critical component 2 counts "at
  one of the eight month ends after the month of the increase", and the open claims rest on policy section 5's filed
  definition (the register closes a claim when the property is taken into possession). Pass 2 on the final zip
  (57a875af): DETERMINISTIC, APPROVE, every workbook figure, component and planning rate reproduced; First-time
  buyer 2019-21 first in every variant that carries the term-increase state (8.0 to 9.7 avoided), High LTV 2022-24
  second (3.2 to 4.9) and first only with the term state dropped.
- guard heart WARN: overuse.objective (4 of the last 12), repeat.gate_g against task137 and task166, repeat.decision
  and repeat.question_form against task166, all answered at the draw (a pick among four books is the plan's own
  question; the forecast is the domain's).
- guard surface: 3 pairs promoted at surface 0.10 (corpus percentile 99), each adjudicated clean, shares components by
  design. task169 (the card's same-driver signature: gap time, pattern none, Gate G forecasting) sends events a closed
  processing route pre-empted through the remaining route's conversion after a filed change; task304 has no closed route
  and no filed change, and its forward count is each concession's delayed re-entry by months since it. task165 shares
  the composition-mix strategy only: its gain is conditioned on how much of a unit the old service level already
  treated. task453 is an ETL dial setting on rotation-group bias, a different objective and driver.
- Containers: the producer audit reports no writer signature; H4 the zip's 13 members equal the declared list (the
  data dictionary removed under the no-describing-file rule); H11 one submission and one prompt; H16 every extract
  ends by 30 September 2026 apart from product_end_date; H24 no generator word under target/.

## Tried and rejected

- Balance-point class (2026-10-24, probe seed 3041): households keeping their homes cold (balance points 49 to 54 F)
  took last year's retrofit as warmth; golden 24.75 GWh carrying the close-out by balance-point class. Coin flip:
  sonnet missed at 27.8, opus landed at 25.0 by fitting a variable-base balance point per premise and reading the
  close-out's savings by balance-point band. A heating state that a standard billing-analysis parameter reveals is a
  reflex stratification.
- Fuel substitution (2026-10-24, seed 3043): cold-kept homes heated one room with electric space heaters, so their gas
  looked tight and rose after the shell retrofit; golden 16.2 GWh against gas-only routes of 26 to 36. Landed by both
  probes (16.4): degree-day fits on each premise's electric reads split the units on the electric heating slope and the
  close-out's 139 negative-savings projects taught the class effect. A per-unit state the close-out labels with its
  outcome is carried by the supervised transport reflex, whatever file the state hides in.
- Income-qualified price response, documented (2026-10-24, seed 3044): Order 24-117 turned a rate discount into a fixed
  credit, so the close-out's before-and-after windows carried a price response the 2027 units will not show; golden
  42.5 GWh. Landed by both probes (43.1 and 42.8) reading the order and a load research sample.
- The same price response with no signal (seed 3044): sonnet found the step in the rate class's own bills against the
  other class in three minutes and filed 44.6 against same-rate routes of 44.2 to 44.3. A dated cause whose effect steps
  a series is found by an event study, unprompted, on the weaker model.
- Waiting list partly treated by the first stage (2026-10-25, seed 3041, county re-home): the 2027 scheduled units had
  their assessment visits (smart thermostat and weatherstripping, recorded in the field-visit register) during the
  months the 2025 installations are measured over, so the textbook not-yet-treated comparison understates the saving;
  the default (waiting list as comparison, or own year before) filed 23 to 24 GWh against a golden of 28 on clean truth
  (truth 28.1). Landed by both probes: opus compared the 2025 homes against the 834 homes with no visit in the window
  and took the assessment saving off the 2026-assessed baselines (27.47); sonnet fitted a panel with effect terms for
  post-assessment, post-install and a calendar shift (28.75). A dated per-unit event recorded in the pack is modelled by
  reflex as a covariate, whether it falls on the treated units or on the comparison. The clean family also spread 26.8
  to 28.7 GWh (total against heating-only normalized use, ratio of totals against mean of logs), because the common
  shift hit heating only; it would have needed a shift on total use to close Gate C.
- The lesson across the six: on this world the probes fit a degree-day model per premise, add a term for every recorded
  dated event, screen any comparison for recorded programme contact, stratify on every state the bills reveal, and
  carry the close-out's outcomes through every visible feature. The lane's builds that held turned instead on what the
  record counts (a shared upstream loss logged by every sibling, a population the demand model's origins omit, units
  still to arrive, records gone stale between recordings), so the next candidate here starts from what the bills,
  schedule or close-out double-count, omit or misstate, not from a per-unit effect, an event or a comparison group.
- Plan-only screens, rounds 2 to 5 (2026-10-26): fourteen candidates briefed to an opus plan reader (files and fields
  only, no data); every one was planned as the decisive step except meters without a lot file and mortgage concessions.
  A brief whose files and fields point at a mechanism gets it planned; only a mechanism living in an ordinary field's
  values that the default path has no reason to examine, with a forward implication, survived.
- Water meters by production run (2026-10-26, seed 1, Lowland Rivers Water, 2027 renewal district): a run of SJ-20s
  the 2021-22 renewals lost to stopped registers was partly held back and fitted in Holme from 2024. Probe B (opus) fitted
  stop rates by age, scanned the serials, found the defective batch and landed Holme; probe A (sonnet) filed Ashby 1,470.
  A strong pattern in the outcome record (failures clustered by serial) is found by a serial scan.
- Fixed five-to-ten-year extensions (2026-10-26): the payment after the extension spread the extended accounts across
  the payment-rise bands, so the chain with and without that band disagreed by up to 20 per cent on the first-time
  buyer figure; extensions are now sized as the Charter sizes them, the fewest whole years (up to ten) that bring the
  payment back, and the family closed to 25.4 to 34.0.
- Collections capitalisations that also lengthened the term (2026-10-26): a second kind of term increase, from
  accounts already in arrears, mixed into the state the decisive step reads and widened the family; capitalisation now
  re-spreads the arrears over the term left.
- Half the first-time buyer book extending (2026-10-26, budgets at 1.02 of the 2021 payment): 50 per cent of the live
  book took a longer term, more than a building society would see; budgets at 1.08 with a stronger fall into arrears
  bring it to 40 per cent and keep the call (seeds 1 to 9 measured: seed 3's rate-rise route filed the first-time buyer
  book, seeds 2, 4 to 9 put the golden or a family member on a bin edge; seed 1 holds every member in the 30 bin).
- Ask B over all four books, and the average loss with a surplus read as a gain (2026-10-26): buy to let had no
  shortfall in the window and its receivers' cross-reference is seen at once, so its figures leaked; the loss is now the
  policy's (nil on a surplus) and the ask covers the owner-occupied books.
- A pilot of six months (2026-10-26): about 300 borrowers an arm gave claim ratios from 0.4 to 1.0 by seed, too noisy
  for a report that halves the chance; the pilot now runs through 2024 (claims at 0.46 of the usual rate).
- Closing month rows that kept the balance and two payments of arrears (2026-10-26, stage 3): the month an account
  redeemed showed the full balance with the arrears grown by a payment, so the chain read a redemption as a fall into
  arrears; the closing row now clears both, and the fit leaves the month an account closes out.
- Halving the chance of possession (2026-10-26, stage 3): the call held under every construction but the first-time buyer
  figure ran 28 to 36 against the 35 edge (one curve for every extended account, by month, at 36; the book-level chains
  at 29 to 34), so the graded figure forked; at the pilot's 30 per cent cut the same constructions run 16.3 to 22.8,
  inside the 20 bin. The pilot's primary outcome moved to four payments behind within a year (about 120 an arm against
  50 claims), whose ratio (0.68) carries the cut, and its table is now rebuilt from the records.
- Accounts netted for closing first (2026-10-26): with the halving the closure-adjusted chains fell to 18 to 27, across
  the 25 edge; the plan now files the book as it stands with no allowance for accounts that close (SF21), and the netted
  chains, measured, still land in the 20 bin at the 30 per cent cut.
- Empty cells read as nothing (2026-10-26): with no smoothing and a band for every month an empty cell divided nought
  by nought and its accounts dropped out of the sum; an empty cell now takes its book's rate.
- Recoveries stream offsets 37, 43, 47, 59 and 61 (2026-10-26): on the final world each left an average loss within 20
  pounds of its rounding edge; 41 and 53 held their edges but let the careful cracker keep 3 and 2 of the 18 ask
  figures; offset 67 holds every edge at 29 or more and the cracker keeps 1.
- A projection window of twelve steps from October 2026 (2026-10-26, stage 4 round 1): the judge ran the chain twelve
  steps from October 2026 and mismatched the golden; the plan's year is January to December 2027, so the chain now runs
  October to December 2026 untallied and counts each account's first entry from January to December 2027 only.
- A 30 per cent cut on the chance of possession (2026-10-26): the pilot measures a cut in four payments behind, not in
  possessions, and a plan taking the whole arrears cut for possessions overreaches; the plan now takes 15 per cent, under
  half the pilot's cut in arrears, and the figures fall to the 10 bin and under 5.
- The first stage 4 asks (2026-10-26): open claims from the book's Litigation stage and the register's old book label
  were cracked at stage 4; ask A now turns on orders the courts re-seal and send again (one order) against genuine
  same-terms variations after a hearing, ask B on the loan parts (two register rows and two statements, one possession).
- The world after the window fix (2026-10-27, seed 1): High LTV's planning rate fell to 4.5 per cent and its figure to
  2.9, under the rate-rise route's first-time buyer figure (3.5), so the easy routes split; owner-occupied High LTV
  accounts now go to the panel solicitors faster once five payments behind (0.75 a month against 0.45), seeds 1 to 8
  scanned: seeds 1, 3, 4, 5 and 7 put High LTV or a family member over 5 or the first-time buyer family across an edge,
  seed 8 left High LTV 0.15 from 5, seed 6 left Shared ownership a planning rate near nothing; seed 2 holds every member
  (first-time buyer 8.0 to 11.9, High LTV 4.4 to 4.7, the easy routes' first-time buyer figure at most 3.7).
- Recoveries stream offsets 67, 71, 73, 79, 89 and 97 on seed 2 (2026-10-27): each left an average loss within 20 pounds
  of its rounding edge or let a re-sealed order fail to move the Shared ownership orders; 83 holds every check.
- The pilot's "half the cut in arrears, a 15 per cent cut" (2026-10-27): on seed 2 the stated arrears cut is about 35 per
  cent, whose half is not 15; the sentence now reads a 15 per cent cut, under half the cut in arrears, asserted.
- A data dictionary in the pack (2026-10-27, stage 3): the rule that no shipped file describes the data came in after
  the draw (leak.py LEAK on data_dictionary.csv); the dictionary is gone, the policy and the plan keep everything the
  Society defines (arrears, the court route, the loss, the four books), each export's own columns carry the rest, and
  the rate card's sheet of pricing terms is named Terms.
- Determinism closed by the data, after the portal's determinism return (2026-10-27; rubric and stump held; one judge
  unsure, one failed, competing_defensible_answer: a held-out-validated chain with no term-increase state, first-time
  buyer 316 against 325 observed, files High LTV, and the 2024 extensions read as small and possibly selected): on the
  shipped pack the September 2025 holdout at the first-time buyer book's own level does not separate the families (the
  payment-rise chain 396 and the term-state chain 409 against 389 observed), the separation lives only on the extended
  accounts (16 and 41 against 54), and the graded figure already forks among chains that carry the months since the
  switch (rate rise 3.7, months since the switch alone 3.7, payment rise 7.4, the term state 9.0; to the nearest ten 0,
  0, 10, 10). Enlarging the book's own earlier extensions to 1,500 to 1,800 unselected accounts (budgets tight from July
  2020, prior arrears 0.14 to 0.17 against the 2026 cohort's 0.16; twelve seeds over two origination profiles) took the
  time-static chain to z 2.4 to 6.3 in that holdout, but the rate-rise chain by months since the switch fitted it about
  as well as the term-state chain and filed High LTV in five seeds and the first-time buyer book in seven, and the
  default itself flipped in two (3.8 against 3.6 and 3.5). The fork is the stump: the 2027 figure rests on the extended
  accounts' share jumping, which no book-level holdout of a history where that share was small can pin, and any replica
  large enough to show at book level hands the switch-timing chains the answer. Architecture 1 spent.
- The ladder never enumerated the chain by the payment rise and the months since the switch: with no term state it
  files the first-time buyer book at 7.4 on the shipped pack (High LTV 4.6), so the write-up's step 5 clause (the same
  chain without the term-increase state puts High LTV first) held for one chain and not the family; a re-root enumerates
  switch-timing chains as a family of their own. Every model also under-predicts High LTV in that holdout (445 observed
  against 397 or 398, the young book's seasoning ramp), a bias any High LTV-side design in this world inherits.
- Re-root constraint (2026-10-27): the decisive 2027 quantity must be pinned by dynamics that played out at the
  contender book's own level in the history, the easy route failing because it lacks a covariate the data carries with
  known timing, not because a subgroup was rare before the forecast year. The one such shape seen in this world is a
  refix priced at product_end_date off the rate card the plan already names, and the prototype probes built a
  payment-shock model by months since the shock first, so it is a reflex: the re-root moves domain under the same
  objective and number unless a decisive step passes this constraint on paper.
