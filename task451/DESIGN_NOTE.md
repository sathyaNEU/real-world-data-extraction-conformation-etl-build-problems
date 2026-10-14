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
- **Prototype** (three seeds before the generator): every paid-date chain ladder overstated 2026 against the received-date development, the all-history ladder by about a tenth and the recent windows by less, while the received-date development over all history and over the latest twelve months agreed. The build's measured ladder is in `## Ladder`, asserted in `checks.py`.

## Default path

The pipeline the measured opponent builds unsteered, from the prompt's words and the files' grain:

1. Read the partner agreement: total cost of care is the Fund's paid amount for medical claims with a first date of service in 2026, for members attributed to the partner in the month of service, whenever paid, pharmacy excluded, each member's year truncated at $200,000, over attributed member months; the corridor is 2 per cent over each partner's target.
2. Collapse each claim to its final version in the extract (replacements and voids by their frequency codes) and keep the medical claims with a first date of service in 2026.
3. Build attributed member months from the eligibility file and the monthly roster, and truncate each member's 2026 amount at $200,000.
4. Complete 2026: a lag triangle of paid amounts by month of service and month of payment from January 2025, volume-weighted chain-ladder factors over all of it, each service month's factor applied to each partner's paid amount for that month.
5. Divide by member months, compare with each partner's target plus 2 per cent, and name the partners over it.

**Ends on:** nine partners owe: Bellmont, Harrow Point, Kettle Run and Stonecrest, and Ashby Lane, Calder, Juniper Hollow, Ridgeline and Tamarack, whose completed cost sits under the corridor and is lifted over it by the paid-date completion (102.9 to 107.5 per cent of target on the build).

**Golden:** four partners owe: Bellmont Clinic Network, Harrow Point Medical Group, Kettle Run Health Partners and Stonecrest Internal Medicine (103.2 to 113.7 per cent of target across the golden family). The 2026 claims are developed on their received dates, whose provider submission lags never changed (or on the payments made after the go-live month, which lands the same four), and the latest service months owe what the administrator now pays within a day of receipt.

## Stump sentence

The default path names nine partners because step 4 completes 2026 with chain-ladder factors averaged over the 2025 and 2026 paid-date triangle, which carry Keswold's old five-week adjudication into the October to December 2026 claims that Tallis pays the day after it receives them, overstating 2026 by 10.2 per cent and lifting Ashby Lane, Calder, Juniper Hollow, Ridgeline and Tamarack to 102.9 to 107.5 per cent of target; developed on the received dates, whose provider lags never changed, four partners owe.

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

**Not semantics:** every field read right (the frequency codes, both date bases, the hour bank, the roster, the truncation) still leaves the completion to be chosen. The default path reads every one of them correctly and completes with the paid-date chain ladder, the field's textbook method, and lands nine partners.

**Not rule application:** the agreement files the WHAT (claims with a first date of service in 2026 whenever paid, attributed member months, the truncation, the corridor) and says only that the Fund estimates the claims not yet paid. No rule names a triangle, a basis or a set of factors, so executing every filed rule still leaves the default path on nine partners.

**Analyst test:** a strong analyst who keeps each claim's final version, builds attributed member months from the eligibility and roster, truncates each member's year at $200,000 and completes 2026 with chain-ladder factors from the paid-date triangle over all of 2025 and 2026 names nine partners as owing, the four and Ashby Lane, Calder, Juniper Hollow, Ridgeline and Tamarack at 102.9 to 107.5 per cent of target (the default path's `Ends on:`). Developing on the received dates names four.

**Estimand:** the partner agreement, Schedule B (`accountable_care_partner_agreement_schedule_b.pdf`). Total cost of care for 2026 is the Fund's paid amount for covered medical services with a first date of service from 1 January to 31 December 2026, for members attributed to the partner in the month of service, whenever paid, excluding outpatient prescription drugs, each member's year above $200,000 excluded, divided by attributed member months. The Fund issues the reconciliation from claims paid through the last business day of January, estimating the claims incurred in 2026 and not yet paid. A partner owes if its total cost of care is more than 2.0 per cent over its target.

**No decoy:** nothing is planted to be caught. No memo, draft, consultant's table or prior reconciliation states a completion factor, a reserve or a partner's 2026 result, and the administrator's dictionary dates the platform change as an ordinary release note.

**No certified replay:** no shipped figure is reproduced to recover a method. The 2025 claims have run out, so any completion back-tests on them, and nothing certifies a factor.

**Lesson:** a claims lag triangle is a record of how the payer paid. When adjudication speeds up, development measured on paid dates overstates what the newest months still owe, and the claims are developed on the clock that did not change; no build on file teaches it (the nearest driver on file is task181 at 0.07).

## Readability screen

| Rung | 1 filed sentence | 2 schema | 3 reflex | 4 control bench | 5 battery | 6 linear | Verdict |
|---|---|---|---|---|---|---|---|
| Paid as extracted (no estimate for the claims still to come) | fires: Schedule B, B.1.4 ("whenever the claims are paid") and B.3.1 (the Fund estimates the claims not yet paid) | no | no | no | no | no | readable |
| The paid-date chain ladder over all development, or the latest twelve months (the default) | no | fires: paid_date on every row and the extract's own grain make the paid triangle the obvious table | fires: the textbook completion | no | no | no | readable |
| The paid-date ladder over the latest six or four months | no | as above | fires: a recent-window habit | no | no | no | readable |
| (decisive) The 2026 claims developed on the payment process now in force: on their received dates, whose provider lags never changed, or on the payments after the go-live month | no. No sentence names a lag, a triangle, a factor, a reserve or payment speed. The dictionary's release note dates the move to Tallis because the frequency codes changed with it, says claim numbers stayed the same and that claims unpaid at the move were adjudicated on Tallis; nothing about how long payment takes | no. received_date is an ordinary field on every claim; no column marks the platform, and claim numbers do not change format | no. The reflexes (the chain ladder over all history, a recent window, by claim type, a back-test on 2025, which the old process paid) all land wrong | no. No control, prior reconciliation, published factor or 2026 result ships | no. The battery (versions, voids, keys, joins, duplicates) comes back clean on the wrong path | no. The gap is a product of link ratios across 24 lags, by service month | silent |

The decisive quantity is named by no sentence and no column, every reflex lands wrong, no control sees it, and the battery is clean. It is the record's own structure: the receipt-to-payment time collapsed on 5 October 2026 (median 23 days to 1), and only an analyst who asks what process paid the history finds it.

## Semantic fork table

One row per term of the main ask and per convention its computation rests on. The calls are measured on the build by `checks.py`; each ruling sentence is asserted present in its document.

| Id | Term or convention | Golden reading | Alternative reading | Call under the alternative | Ruled out by |
|---|---|---|---|---|---|
| SF1 | our twelve accountable care partners | the twelve groups of Exhibit 1 | none | same call | Exhibit 1 |
| SF2 | owe a shared-loss payment | total cost of care per attributed member month more than 2.0 per cent over the target | at or over 2.0 per cent | same call: no partner within 0.0001 of the line | Schedule B, B.2.1 ("exceeds its Target PMPM in Exhibit 1 by more than 2.0 per cent") |
| SF3 | for 2026 | claims with a first date of service in 2026 | claims paid in 2026 | not computed: refused | B.1.4 ("with a first date of service in the Performance Year") |
| SF4 | claims paid through January | the payment run of 29 January 2027, the last business day | the extract's run date, 1 February | same rows: no payment run between them | B.3.1 ("paid through the last business day of January following the year") |
| SF5 | total cost of care | the Fund's paid amount | the allowed amount | refused | B.1.4 ("the Fund's paid amount for covered medical services") |
| SF6 | attributed member months | on the roster for the month and eligible on the latest version of the spans | the roster alone | same call (asserted, R2) | B.1.3 ("eligible for the Fund's medical benefits and appears on the Fund's attribution roster") |
| SF7 | the large-claim exclusion | each member's year above $200,000 | none, or per claim | refused | B.1.5 ("the amount above $200,000 is excluded") |
| SF8 | covered medical services | professional, outpatient and inpatient claims | pharmacy included | refused | B.1.4 ("Outpatient prescription drugs dispensed by retail, mail-order and specialty pharmacies are excluded") |
| SF9 | a claim's value | its latest version's paid amount | every version summed, or the first version | same call for both (asserted, R2) | the dictionary ("The claim's value is the paid_amount of its latest version.") |
| SF10 | the month a claim belongs to | the month of its first date of service | the month paid or received | refused | B.1.4 ("attributed to the Partner in the month of that first date of service") |
| SF11 | the comparison | unrounded | the ratio rounded first | same call: no partner within 0.05 points of 102 per cent | B.2.3 ("are made on unrounded figures") |
| SF12 | the claims not yet paid | included at their estimate (the ultimate cost of 2026 services) | paid through January only | refused (R1 names two partners) | B.1.4 ("whenever the claims are paid") and B.3.1 |
| SF13 | an inpatient stay spanning months | the month of admission (its first date of service) | the month of discharge | refused | B.1.4 and the dictionary ("last date of service on the claim (the discharge date for an inpatient stay)") |
| SF14 | a member attributed to two partners in a year | the exclusion shared by the member's amounts with each | all to the last partner | refused | B.1.5 ("shared in proportion to the Member's amounts with each") |

The stump is none of these readings: the default and the golden read every term the same way and differ only in how the claims still to come are estimated.

## Ladder

Measured on the build (world seed 4512, `## Build record`) by `checks.py` and recomputed by `verify.py`. "Book" is the twelve partners' completed 2026 cost against the golden (G1). The share of target is each partner's total cost of care per member month over its Exhibit 1 target; a partner owes above 102.

| Route | Construction | Book | Partners named | Killed by |
|---|---|---|---|---|
| R1 | paid as extracted, nothing for the claims to come | -3.1 | 2: Bellmont, Stonecrest | B.1.4 "whenever the claims are paid" |
| R0 (default) | paid-date chain ladder, volume-weighted, all development from January 2025 | +10.2 | 9: the four, and Ashby Lane, Calder, Juniper Hollow, Ridgeline, Tamarack | the history was paid by a process that no longer pays (receipt to payment, median 23 days before 5 October 2026, 1 after) |
| R0 variant | paid-date ladder, latest twelve months | +10.2 | the same nine | as R0 |
| R0 variant | paid-date ladder, latest six months | +7.7 | 5: the four and Ashby Lane | the window still carries the old process and the go-live month's backlog |
| R0 variant | paid-date ladder, latest four months (the go-live month included) | +6.5 | 5: the four and Ashby Lane | the go-live month's backlog clearance inflates its links |
| G1 (golden) | received-date chain ladder, all development | 0.0 | 4: Bellmont, Harrow Point, Kettle Run, Stonecrest | |
| G2 | received-date ladder, latest twelve months | +0.2 | the same four | |
| G3 | paid-date ladder, payments after the go-live month only | +2.9 | the same four | |
| G4 | received-date ladder by claim type | -0.1 | the same four | |
| G5 | paid-date ladder on each claim's latest version (its paid amount in the month that version was paid), payments after the go-live month | +4.5 | the same four | |

**Share of target on the build** (golden family G1 to G5, lowest to highest; the default R0):
- owe: Stonecrest 108.9 to 113.7 (R0 119.4), Bellmont 107.1 to 112.3 (120.2), Kettle Run 103.7 to 109.1 (115.9), Harrow Point 103.2 to 107.9 (112.6);
- the default adds: Ashby Lane 96.2 to 100.9 (107.5), Tamarack 93.9 to 98.0 (103.2), Ridgeline 94.5 to 98.5 (103.1), Calder 94.1 to 98.7 (103.0), Juniper Hollow 95.1 to 99.0 (102.9);
- owe on no route: Brookhollow 87.6 to 92.3 (98.3), Sycamore 86.3 to 91.1 (95.7), Wren Valley 84.7 to 88.5 (94.7).

**Margins.** Every golden route keeps every partner at least 1.09 per cent from the 102 line (closest: G5 1.09, G4 1.22, G1 1.55, G2 1.69, G3 2.75). Every other route's landing is at least 0.82 per cent from it (R0 0.84, the twelve-month 0.82, the six-month 0.82, the four-month 1.10, paid as extracted 1.21). The placement (build.py `place_targets`) puts each banded partner at the geometric middle of its band, measured on the shipped data; Ashby Lane's band runs from the highest golden route (G5) to the paid ladder from the go-live month (the four-month window), so either post-cutover paid construction keeps it 1.09 per cent or more from the line.

**The reflex sweep** (asserted in `checks.py`). Every paid-date habit lands wrong: all development without the go-live month's payments (nine), the latest twelve months without them (nine), the latest five months (five), the payments before go-live only (nine), simple averages of the link ratios (nine), by claim type (eight) and by claim type over the latest twelve months (seven). The ladder on each claim's latest version by its paid date does too: all development (nine), the latest six months (nine), and from the go-live month with its backlog (five). Every development on the process now in force lands the four: received-date simple averages, the received-date latest six months, and the paid-date ladder on the latest two payment months.

**Forcing evidence on the build.** Receipt to payment: median 23 days (mean 31.5) for claims received before 5 October 2026, 1 day (mean 3.4) after. Service to receipt: median 13 days in 2025, 14 after go-live. The received-date first link is 2.569 over all development against 2.594 before go-live; the paid-date first link is 7.515 before go-live against 2.816 after.

**The grid and the Layer 1 slips** (R2 in `checks.py`, each on the golden route): every version's paid amount summed, each claim's first version only, member months from the roster alone, member months on each span's first version: the same four each time. The truncation is a filed rule (B.1.5), recorded, not a slip.

**Why the four golden routes agree and the rest do not.** Providers submit on a clock the Fund's administrator does not control, so the received-date development is the same before and after go-live, and Tallis now pays within a day of receipt. The paid-date history is the old five-week process. A recent window still carries it, and the go-live month's backlog clearance inflates its links; only the payments after the go-live month escape both, and they land the same four.

## Closure table

| # | Axis | Reading chosen | Closure |
|---|---|---|---|
| 1 | Population | members attributed to each partner on the roster for the month, eligible in that month | filed (B.1.2, B.1.3); SF6 asserted |
| 2 | Unit of account | the attributed member month; the claim at its latest version | filed (B.1.3, B.1.6); the dictionary for the version |
| 3 | Attribution window | a claim belongs to the month of its first date of service | filed (B.1.4); SF10, SF13 |
| 4 | As-of dating | claims paid through the run of 29 January 2027 | filed (B.3.1); SF4 |
| 5 | Version basis | each claim's latest version; each eligibility span's latest version | filed (dictionary; the Fund's notes); C1 asserted (R2) |
| 6 | Divisor and denominator | attributed member months for the year | filed (B.1.6) |
| 7 | Weighting | volume-weighted link ratios over the received-date triangle | C3: simple averages, the latest twelve months and by claim type land the same four (G2, G4 asserted) |
| 8 | Measurement window length | the performance year 2026 | filed (B.1.1) |
| 9 | Boundary inclusivity | more than 2.0 per cent over | filed (B.2.1); SF2, C4: no partner within 0.0001 |
| 10 | Rounding path | unrounded comparison; dollars to the thousand and shares to one decimal at the end | filed (B.2.3; the prompt) |
| 11 | Tie-break | none | not applicable |
| 12 | Maturity and censoring | the claims not yet paid are estimated, developed on the process in force | the decisive step; the data force it (forcing evidence, asserted) |
| 13 | Order of operations | truncation on paid amounts by member, completion on the partner's paid amounts by month | C1 on the call: taking the $200,000 off each member's claims before completing names the same four on every golden route, and no owing partner carries a truncated member (asserted) |
| 14 | Row order | order-free | C1 |
| 15 | Duplicate resolution | one latest version per claim | filed (dictionary); keys unique (asserted) |
| 16 | Identity normalisation | member ids as the Fund issues them; the roster's partner codes | filed (the Fund's notes); C1 |
| 17 | Netting against gross | voids at zero, replacements at their full amounts | filed (dictionary) |
| 18 | Dimensional units | US dollars throughout | C1 |
| 19 | Code and status semantics | legacy O, A, V and Tallis 1, 7, 8 frequency codes; P, D, V statuses | filed (dictionary) |
| 20 | Integerisation | none | not applicable |
| 21 | Scope of a stated clause | B.2.1 applies to each partner on its own target | filed |
| 22 | Forward window contents | the call settles 2026, a closed performance year; the open part is the claims still to come, which the estimand includes | filed (B.1.4, B.3.1) |
| + | Completion method | the received-date development (or the payments after the go-live month) | the method, never filed; C3 across the golden family, the data separating it from every paid-date route (asserted) |
| + | Ask A: pharmacy | Corvane's net plan paid for 2026 fills by members on the partner's roster for the fill month | filed (B.4.1(a)); the patient's member found by cardholder, birth date and sex |
| + | Ask B: outside share | professional paid amount (through 29 January) billed by anyone but the partner's group NPI | filed (B.4.1(b), the prompt's "not then with the partner"); the claim's billing group says who the clinician was with |

## Literal reader

The prompt and Schedule B, executed word for word, fix the estimand: the members attributed to each partner in the month of each claim's first date of service and eligible then; the Fund's paid amount for medical claims with a first date of service in 2026, whenever paid, each member's year above $200,000 excluded; per attributed member month; owing when more than 2.0 per cent over the Exhibit 1 target, unrounded. Every literal reading of those terms selects the same claims and months (SF1 to SF14). The claims not yet paid at 29 January must be estimated (B.3.1); no filed sentence names the method. The data force it: the administrator's receipt-to-payment time fell from a median of 23 days to 1 on 5 October 2026 while the providers' submission time held, so development measured on paid dates describes a process that no longer pays, and the received-date development, which held, is the one that describes the claims still to come. The default's nine come from that method, not from a reading.

## Oracles

- **What ships no figure.** No file states a completion factor, a reserve, a lag, a prior reconciliation, a 2026 total cost of care or a partner's result. Nothing ranks the partners.
- **The quality scorecard** (distractor). Quality decides only shared savings (B.2.2), never a shared loss.
- **The stop-loss summary** (distractor). Its $175,000 specific deductible and 12/15 basis belong to the reinsurance contract. B.1.5's $200,000 is the agreement's exclusion.
- **The dictionary's release notes.** They date the move to Tallis by its frequency codes and record that claims unpaid at the move were adjudicated on Tallis, which explains October's payments; they say nothing about how long payment takes. Read alone, the backlog sentence invites dropping October's payments from the paid ladder, which still names nine (asserted).
- **The Fund's notes and Corvane's layout.** Each states its own numbering (enrollment order; date of birth). They meet only on the pharmacy ask's path, not on the call's.
- **The asks' referee: the claim's billing NPI.** It says which group billed each professional service and arbitrates the outside share without naming a level. It ties under every handling of the call.

## Ask sheet

**The main call's declared population:** the medical claims extract (claims with a first date of service in 2026, at their latest version), the eligibility spans and the 2026 roster. Zero ask device rows in it: the pharmacy file is outside the total cost of care (B.1.4), and the billing and rendering NPIs are read by no step of the call. Scrambling every claim's NPIs leaves the call (asserted).

**Ask A: the Fund's 2026 pharmacy spending for each partner's members** (12 figures, to the nearest thousand dollars; B.4.1(a): fills in the Members' Attributed Member Months with the partner, reversals included whenever processed, which rules out counting only the reversals processed in 2026, a reading that moves Ashby Lane).
- H18 home: B.4.1(a), the report's pharmacy line: a measure every partner carries that the call does not turn on (pharmacy is outside the total cost of care).
- Use: the trustees read each group's pharmacy spending beside its medical cost.
- Primary device, D7 (the true key elsewhere): Corvane numbers a family's dependants by date of birth (person code 03 up), and the Fund suffixes member ids in order of enrollment. In a family whose spouse or a stepchild enrolled after the children, the natural join (cardholder and person code to member id) puts each patient on another member, often another partner's.
- Hazards: B2 reversals carrying the reversed claim's positive amounts, and B3 rebills (the layout says so; repaired right). Fills in months the member's eligibility was later ended (B.4.1(a) counts the Members' Attributed Member Months, so the roster alone overstates every partner by $1,599 to $10,519). The cardholder-only join puts every fill on the participant, so the pediatric group shows nothing (visible).
- Path: corvane_pharmacy_claims_2026.csv (17 columns) to the eligibility spans (subscriber id, birth date, sex) to the roster (month, partner), with the layout PDF and the Fund's notes. Three files, five columns on the causal path.
- Stops: golden (cardholder, birth date and sex, in the member's attributed member months); the person-code join, $4,485 to $112,830 under on every partner (Sycamore $290,000 against $403,000); the roster without the eligibility condition, $1,599 to $10,519 over; the cardholder join.
- Realism: pharmacy benefit managers key members by cardholder and person code; plan sponsors number their members their own way.

**Ask B: the share of each partner's members' 2026 professional spending, paid through January, that went to clinicians not then with the partner** (12 figures, to one decimal; B.4.1(b): the Fund's paid amount before B.1.5, which rules out spreading the $200,000 exclusion over the claims, a reading that moves Calder and Ashby Lane across a rounding edge).
- H18 home: B.4.1(b), the report's outside-services line: a measure every partner carries that the call does not turn on.
- Use: the partners and the Fund's network team read where the members' professional care went.
- Primary device, D2 with D7: the clinician roster is the 1 January 2027 snapshot. It omits the specialist each group lost during 2026 and dates its joiners only by "with partner since". Read for the whole year, it counts the leaver's pre-departure services as outside, and so does the since-dated read. The claim's billing NPI (each group bills under the group NPI in Exhibit 1) says which group the clinician was with when the service was given.
- Hazard: a rendering clinician absent from the roster read as outside (correct for outside clinicians, wrong for leavers).
- Path: the claims extract (rendering_npi, billing_npi, claim_form, paid_amount), Exhibit 1's group NPIs, the clinician roster, the roster and spans. Four files.
- Stops: golden (billing group); the snapshot read, 0.46 to 2.35 points over on every partner; the since-dated read, 0.49 to 2.35 points over.
- Realism: a network file is a current snapshot, and says so (a clinician who leaves a group is removed when the partner gives notice); claims bill under the group the clinician practised with that day.

**Hazard table.** Reversals (Ask A only, repaired right). A leaver's services before departure (Ask B: 0.46 to 2.35 points). Versions and voids (shared, repaired right, no ask moved).

**Cracker sheet.** The cracker lands the call, runs the hygiene battery and executes every filed rule; for the asks it joins Corvane by cardholder and person code and reads the clinician roster with its since dates.

| Row (cracker) | Cracker's figure | Golden | Verdict |
|---|---|---|---|
| A Ridgeline | 533,000 | 550,000 | miss |
| A Brookhollow | 560,000 | 581,000 | miss |
| A Sycamore | 290,000 | 403,000 | miss |
| A Stonecrest | 549,000 | 553,000 | miss |
| A Kettle Run | 476,000 | 525,000 | miss |
| A Harrow Point | 552,000 | 577,000 | miss |
| A Wren Valley | 515,000 | 533,000 | miss |
| A Bellmont | 459,000 | 505,000 | miss |
| A Calder | 456,000 | 524,000 | miss |
| A Tamarack | 647,000 | 660,000 | miss |
| A Juniper Hollow | 564,000 | 579,000 | miss |
| A Ashby Lane | 528,000 | 543,000 | miss |
| B Ridgeline | 36.9 | 35.9 | miss |
| B Brookhollow | 42.6 | 42.1 | miss |
| B Sycamore | 32.6 | 31.6 | miss |
| B Stonecrest | 41.5 | 40.7 | miss |
| B Kettle Run | 33.9 | 32.1 | miss |
| B Harrow Point | 45.5 | 44.5 | miss |
| B Wren Valley | 33.4 | 31.4 | miss |
| B Bellmont | 39.2 | 38.4 | miss |
| B Calder | 30.9 | 30.3 | miss |
| B Tamarack | 42.6 | 41.6 | miss |
| B Juniper Hollow | 28.5 | 26.2 | miss |
| B Ashby Lane | 41.7 | 39.9 | miss |

**Mirror sheet.** The mirror stops at the default (nine partners) and takes the same joins: it misses all 24 ask rows and the chart's title, keeping only the chart's bars and its 102 line (2 of about 28 ask criteria).

Mirror leakage: 7 per cent of ask weight.

Pair ceiling: 34 (the cracker 38 + 7 + 55 x 0.14 = 52.7, keeping the chart's four parts; the mirror 5 + 7 + 55 x 0.07 = 15.9).

## Pre-ship check

- **Three rules.** Domain: health plan analytics' own completion of the open service months from a claims lag triangle, checked against the payment process now paying (swap test in the Three rules section). Two layers: the Layer 1 inventory (versions and voids under two code sets, two date bases, the hour bank's retroactive postings in a dated export, the monthly roster, the pharmacy benefit manager's own member keys, the clinician roster as a January snapshot), all of it what the administrator's, the Fund's and Corvane's systems write; and the development basis that separates the providers' unchanged submission lag from Keswold's collapsed adjudication time. Decisive step analytical: the analyst who conforms everything, applies every filed rule and completes with the paid-date chain ladder names nine partners (asserted on the shipped data); changing the development basis alone gives the golden's four (asserted), and every paid-date habit in the reflex sweep stays wrong.
- **Gates.** 11 files in 5 formats, the claims extract at 174,248 rows, two distractors (the stop-loss policy summary and the quality scorecard) the solution never reads; 168 checks; `verify.py` PASS from the bundle alone (the five golden completions, the received-date ranges, both asks); two builds byte-identical; `figures_check.py` exit 0 (59 figures); `precut.py` exit 0; `leak.py --asof 2027-02-03` REVIEW with no LEAK; `guard.py surface` clean (the personas on the card) and `heart` WARN (Gate G overuse, decision type and question form, answered in the Draw).

## Leak check

- `leak.py --asof 2027-02-03` (after the final build, both reader passes appended to the report): REVIEW, no LEAK. The REVIEW lines: the corridor (2.0 per cent) in Schedule B (the filed WHAT); the agreement's vocabulary beside the call's partner names (Exhibit 1 lists every partner with its target); four documents sharing the design's ordinary vocabulary (member, months, roster, version, received), none naming the step; the agreement, the clinician roster and the quality scorecard naming every partner beside numbers (targets, tenure, quality points), none ranking the partners on who owes. Dates after the setting: clean once the eligibility export was dated (H16).
- Reader, pass 1 (isolated, Sonnet, medium, fresh copies of the prompt and the pack): Q1 to Q4 none (B.3.1 is the nearest sentence and names no method); Q5 every filed sentence executes to the golden's population; Q6 an analytical choice (the reader itself would complete from the paid-date lag, the default path); Q7 nothing constructed. Every sweep line harmless.
- Reader, pass 2 (after the release note's backlog sentence, the roster's scope sentence and B.4.1's pins; same isolation, a question added on Ask B): Q1 to Q4 none (B.3.1 still the nearest sentence); Q5 every filed sentence executes to the golden's population, B.4.1(a) and (b) included; Q6 an analytical choice (completion from the claims' own lag pattern); Q8 the files support the billing NPI against Exhibit 1's group NPI, the roster being a snapshot with leavers removed. One realism tell, fixed in the generator: the pharmacy file's drug codes were nearly all distinct (72,415 over 75,896 fills); each code now sits at its product's price level and repeats as in a real file (678 codes), with no figure moved (figures.json byte-identical across the rebuild).

## Determinism judge

- Pass 1 (2026-10-13, isolated thread on the cut pack): DETERMINISTIC, APPROVE. Every owed figure reproduced (the four, the nine on the paid-date ladder, the two with no completion, both asks all twelve rows); Gate G method_or_model_selection, analytical_non_defect, no surface-read dependency, no sole data defect; Gate H domain pass, layers pass, decisive step analytical. Its notes, repaired in one generator pass: the range ends taken across a post-cutover paid ladder the write-up did not pin (ranges now over the received-date developments; the latest-version construction is G5 and the targets are placed against it); "14 after" (now "from 5 October 2026"); Ask B's roster reading (the roster now states that leavers are removed); Ask A's reversal timing (B.4.1(a) now "reversals included whenever processed"). Report: `determinism_check_report.md`. No re-judge: APPROVE, and the repairs moved neither the call nor an owed ask figure.

## Tried and rejected

- 2026-10-13, architecture 1 (Survey Research & Official Statistics, aid statistics: the members' money followed through two pooled funds, Kenya, Rwanda and Mali for the offices), spent at design before its pack shipped. The honest swap test fails: with a fund-of-funds' or a franchise marketing levy's nouns the task reads the same, crediting a pool's spending to its contributors by what the pool held when it paid, so the decisive step is generic fund accounting and the domain was the backdrop (10/10 rule 1). Its generator and pack were removed at the re-root and stay in git history (commit 78f1fe8).
- 2026-10-13, architecture 1's design record, kept as written:
  - 2026-10-13, draw: the draft's vote at the council (vote_or_meeting) and a ranked list under a cap (shape 01). Rejected: task255 holds the forcing event and task256 the shape in the window; the host-country agreements and leases force the decision (purchase_order_or_contract) and the answer is built as a bridge from the members' own records to the money spent (shape 03).
  - 2026-10-13, draw: attribution at a transition (G4) as the decisive generator. Rejected: task450 v2 holds the pattern in the window; the members' money is provided elsewhere, through the funds (G5).
  - 2026-10-13, design: the second fund layer (the global fund's money inside the Sahel fund) as the decisive step. Rejected: the transfer is a provider-receiver join the solver already holds the key to (screen test 2), and the estimand's "one or more pooled funds" files it, so a careful solver lands it; the prototype also moved the three only at fifth place. It stays on the default path, and the decisive step moved to the money each fund held when it paid (G6).
  - 2026-10-13, design: shape 03 (a bridge between totals). Rejected: a bridge from the members' payments to the money spent walks the solver through the funds' timing and hands over the decisive step; the answer is a register of 13 countries with three measures (shape other).
  - 2026-10-13, design: a payer-and-receiver reconciliation ask keyed on year-end receipt dates. Rejected: an ask about money crossing the year end points at the funds' timing; the asks carry identity and version devices instead.
  - 2026-10-13, design: a shared decisive pool for both funds (one share window for both). Rejected: a single window lets a lag heuristic land; the global fund pays out a year late and the Sahel fund the same year, so only the money each fund held when it paid lands both.
- 2026-10-13, asks: B.4.1 worded without saying which members' fills count or whether the outside share is taken before B.1.5. Rejected: 361 fills ($48,025 on the build) fall in months a roster member's eligibility was later ended, and spreading the $200,000 exclusion over the claims moves Calder and Ashby Lane across a rounding edge, so two readings filed different ask figures; B.4.1(a) now counts the Members' Attributed Member Months and B.4.1(b) the Fund's paid amount before B.1.5.
- 2026-10-13, stage 4: the owing partners' ranges stated across a post-cutover paid ladder whose triangle the write-up did not pin. Rejected: the judge built it on each claim's latest version by its paid date and ran 1.6 to 1.8 points higher, with Ashby Lane at 101.6; the ranges are now stated over the three received-date developments only, that construction joined the golden family as G5, and the targets are placed against it (Ashby Lane 100.9 on G5, 103.1 on the four-month window).
- 2026-10-13, second-layer attempt after shipping (paper): development by service category made decisive, a late-2026 inpatient surge at the partners with older members making pooled received-date factors understate their open months. Rejected on the arithmetic: the claims still to come are about 3 per cent of 2026 cost (claims paid as extracted sit 3.1 per cent under the golden), so even a 30 per cent error in one partner's completion moves its cost about 1 per cent against golden margins of 1.09 per cent and more; the surge would have to be large enough to read as planted before the pooled factors named another partner.
