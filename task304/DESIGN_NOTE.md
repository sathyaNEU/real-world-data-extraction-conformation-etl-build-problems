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
| Objective | Opportunity Sizing & Decision Support: the headline is the possessions the team avoids in the chosen book, sized from the pool (the book's borrowers who fall two payments behind in 2027) to the realisable (each taken on, possession chance halved), and the largest figure picks the book |
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

The strong analyst's route, every field read correctly and every filed rule applied (prototype world, seed 1, the
filed per-book possession rates):
1. Rebuild payments in arrears at each month end (arrears balance over the current contractual payment, rounded down)
   and mark each entry, a month the account reaches two or more from fewer than two.
2. Fit the monthly hazard of entry on book, loan age, arrears in the month before and the payment rise at the account's
   last rate switch (opus added months since the switch; sonnet added the rise since completion).
3. Carry every live account not in litigation or with a receiver from 30 September 2026 through 2027, repricing the
   fixes that end before then, and sum the 2027 entries per book.
4. Multiply each book's entries by its filed 18-month possession rate and halve: High LTV 2022-24 18.9 possessions
   avoided, First-time buyer 2019-21 10.6, Buy to let 3.5, Shared ownership 1.9.
Ends on: High LTV 2022-24, about 19 possessions avoided.
Golden: First-time buyer 2019-21, about 26 possessions avoided (High LTV 19.0 on the same route), once the 2021 buyers'
term extensions at their 2026 switch are carried at the hazard the earlier extensions show by months since extension.

## Stump sentence

A competent solver fits the hazard of falling two payments behind on book, the payment rise at the last switch, loan
age and current arrears, carries every live account through 2027 at the filed possession rates and files High LTV
2022-24 at about 19 possessions avoided; the step that lands it there is reading the up-to-date first-time buyers'
small payment rise as low risk when their remaining term rose at the switch, the Charter extension that hid a budget
the new rate broke.

The data-native sentence: in the payment history the 2021 first-time buyers' remaining term jumps by five to ten years
in the month their five-year fix ended in 2026 while their payment barely moves, and the accounts whose term jumped the
same way in 2023 to 2025 fell two payments behind at many times the book's rate from about eight months later.

## Three rules

Task type: banking-credit-financial-risk / collections-recovery, which serves Opportunity Sizing: a collections function sizing where a support team avoids the most possessions.
Domain test: the deciding quantity is each book's 2027 entries into two payments of arrears, the collections forecaster's arrears-entry hazard carried account by account with forbearance as a state: a term extension at the rate switch lowers the payment and keeps the account up to date while the budget the new rate broke stays broken, so the account carries its own hazard by months since the concession.
Swap: "which hospital ward should the discharge team work, and how many readmissions would it avoid" keeps a pick and a halving, but the object that decides, an account whose remaining term rose at a rate switch so its payment barely moved while the borrower could not meet the new rate, and the concession's delayed fall into arrears eight to fifteen months later, has no ward equivalent; with the nouns swapped the rate switch, the Charter extension and the arrears-to-possession route stop making sense.
Layer 1: the Society's own systems produce every mess item: product codes that lost their dashes at the July 2022 platform change, month rows re-sent in a later extract, payments in arrears derived from an arrears balance in pounds against the current payment, a possession register dated day-first with receiver sales recorded as possessions, arrears capitalised by collections clearing without a payment, and redeemed and possessed accounts absent from the book snapshot; none decides the call.
Layer 2: field_method, the arrears-entry forecast with forbearance as a state: the 2027 entries come from each account's hazard given its concession history and the months since the concession, not from its current arrears and the payment change it shows.
Decisive step: carrying each extended account forward on the delayed re-default hazard the 2023 to 2025 extensions show by months since the extension, instead of on the hazard its up-to-date status and small payment rise imply.
Not semantics: every field read correctly (remaining_term_months is the months left to run) still leaves the easy route on High LTV, because no field says an account is forborne: the extension is an event read from the path of the remaining term, and the forecast still has to estimate what that event does to the hazard and when, from the earlier extensions' own outcomes.
Not rule application: no filed rule forecasts entries; the plan paper files who is counted, the year, the 18-month window and each book's possession rate, and leaves the entry forecast to the analysis. Measured on the prototype pack (seed 1): the enumerated family (payment-shock chain, rate-shock by months since the switch, book by age by arrears, extension-aware chain) spreads the first-time-buyer book's possessions from 20.5 to 52.9 and files two different books; the standing family (the extension-aware constructions the extensions' own outcomes leave defensible) files the first-time-buyer book on every member; the ruling-out is quiet, since no clause, flag or one-group-by comparison on any shipped column separates the extended accounts.
Analyst test: a strong analyst fits the monthly hazard of an account falling two payments behind on book, the payment rise at its last rate switch, loan age and current arrears, carries every live account through 2027 at the filed 18-month possession rates and files the High LTV 2022-24 book, while the 2021 first-time buyers who extended their terms at the 2026 switch fall behind eight to fifteen months later and make the first-time-buyer book the largest.
Estimand: the plan paper (financial_support_team_2027_plan_paper.pdf, sections 2 and 3) files the population (the chosen book's borrowers whose account first reaches two payments in arrears from fewer than two during 2027, excluding accounts in litigation or with a receiver), the outcome (possession within 18 months of that month, at the book's own filed possession rate), the window (calendar 2027), the unit (possessions, expected) and the comparison (halved by the team, per the pilot).
No decoy: nothing is planted to be caught: the extensions are the Charter process the arrears policy describes in one line among its support options, no memo, draft or stakeholder figure argues for a book, and no file ranks the books on the decision.
No certified replay: no published or certified figure in the pack reproduces the method; the pilot report gives the halving and its own counts, which the register reproduces.
Lesson: a borrower's up-to-date status after a concession is the concession's work, not evidence of health, so the concession history is a state the forecast carries with its own clock; no build on file teaches forbearance as a forecast state (task128 sized an early-arrears contact queue, task446 converted watch-list flags by the component that raised them).

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
