# task177 design note

**Status: architecture 3, drawn 2026-10-23 (rebuild from scratch).** The number was RETIRED on 2026-10-22 and
reopened the next day under the author's rule that no number stays retired. Two rebuild cells found nothing that
holds (quantitative-finance volatility, biomedical survival; `## Tried and rejected`, `## Rebuild (2026-10-23)`);
the third cell, banking-credit-financial-risk / credit-scoring-pd-modeling (Forecasting), carries architecture 3
below. Architectures 1 and 2 are kept as records further down.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task177.json`, architecture v3 (v1 and v2 in its lineage with their
  fates).
- **Pairing:** client domain Banking, Credit & Financial Risk, task type credit-scoring-pd-modeling, which serves
  Forecasting & Predictive Modeling. The committed figure is a forward count: how many of the 2,400 payroll-deduction
  loans the cooperative disburses on 1 February 2027 to members employed by private firms will be in default (90 days past due) by
  31 January 2028, a window not yet open.
- **World (fictional throughout):** Coopservir (Cooperativa Servidores de Valdemora), the savings and credit
  cooperative of the Republica de Valdemora's public servants (pesos, VMP), has lent payroll-deduction loans
  (libranzas) to its members since 2014, the instalment taken at source by the Tesoreria General's central payroll.
  In 2025 it opened membership to the staff of 38 private employers in six sectors (contact centres, retail chains,
  security services, logistics and courier, food processing, private clinics) under deduction agreements that
  require each employer to send its payroll register every pay period, so members' deduction margins can be checked.
  The cooperative's rules lend only after twelve months of member savings, so the first private-employer loans are
  disbursed together on 1 February 2027 from a file of 2,400 approved applications. The board books the 2027
  budget's provision for them from the first-year default forecast.
- **Shape:** `other` on the card (the total and its split over six employer sectors, plus the asks' cells).
  Criteria: the call's total (1), the six sector counts (6), the asks' cells (designed at stage 2, at least 15),
  the two files (2): 24 before the asks' qualifiers, over 25 with them.
- **Decision:** `quantity_figure`, answer unit count, question form how-many. Forum `board_of_directors` (the
  cooperative's board approves the budget and its provisions), forcing event `budget_or_appropriation` (the 2027
  budget's provision for the first private-employer loans), org family `cooperative_or_member_body`, role family
  `finance_controller` (the cooperative's finance manager books the provision).
- **Strategy and family:** `decomposition_attribution`; Layer 2 family `estimand_identification`, pattern
  `own:pd-read-per-payroll-exit`. The forward default count splits into the route through a borrower leaving the
  employer's payroll while the loan is open and the small on-payroll route; the textbook PD reads the public book's
  low default as borrower quality when it is the rarity of the leaving event.
- **Gap, pattern, generators:** gap population (the public-servant book is not the private-employer launch), then
  time; pattern C read as the launch loans' leaving share, an absolute share the analyst builds behind the join of
  loans to payroll payees, never a column; generators G14 (the pooled rate does not apply to this pool), G6, G3.
- **Data-native sentence:** a payroll-deduction loan is paid by the employer's payroll at source, so its borrower
  can fall behind almost only by leaving that payroll with the loan still open, and the record of public servants,
  who rarely leave (and whose temporary staff hold loans capped to end before their contracts), carries that event
  so seldom that a model of default on the borrowers' own attributes reads its rarity as their quality; the private
  employers' own payroll registers, at employee-period grain, show how often their staff leave.
- **Sources, one line each.** Client cards credit-scoring-underwriting 1 to 4 (through-the-door, prior correction,
  out-of-time, fairness at the cutoff): each is a textbook route the opponent takes, none is the stump; this build's
  default path is card 3's out-of-time PD model scored on a new population. Card 3 of credit-default-risk-modeling
  (structural PD) is not this ground. task446 (the one earlier card in this task type) prices a flag by the kind of
  member raising it; here no flag exists, the rate is read per exit event. task169 closes one of two routes to the
  outcome; here no route closes, the forward population sits at the high end of the one route the record rarely
  takes. task177 v2 conditioned a test's effect on the days to each unit's bill; here no test and no timing within a
  cycle. task179's banking paper deaths (a payroll client leaving, read off customers who lost a salary credit) are
  the attaining-subset form of losing a payer; here no subset of the record sits at the forward exposure (the
  public permanent staff leave at 1.8 to 5.4 per cent a year against 14 to 42 in the private registers) and the only
  high-leaving subset, the temporaries, rarely default.
- **Same-puzzle and same-driver tests:** gap population, pattern C, decision quantity_figure, Gate G forecasting:
  no build in the last twelve, lineage included; the older task45 and task75 carry differentiation lines on the
  card.
- **Abstraction test:** stripped of nouns, the nearest drivers (`guard.py check`: task268 0.08, task446 0.07,
  task130 0.06, task183 0.05, task192 0.05) are a survival share with a lost-to-linkage class, a flag converting by
  its raising member, a reported-in-window cover, a part that keeps failing, and lifetime events by cohort; none
  reads the outcome rate per occurrence of a triggering event whose frequency is measured on the forward units' own
  payment records.
- **WARNs answered:** `overuse.strategy` (decomposition_attribution in 3 of 12): the honest label for an outcome
  split between a leaving route and an on-payroll route; composition_mix was the alternative and would also be
  honest, and the card keeps the label a reviewer reads the decisive step under. `overuse.objective`,
  `overuse.gate_g`, `repeat.gate_g`, `repeat.decision`: Forecasting is this lane's objective and a forward count is
  its natural call.
- **Axes redrawn at the draw, and why the replacements are the honester labels.** First pass against the live window:
  calibration form `existing_book_actuals` to `settled_transaction_ledger` (BLOCK against task171), since the
  forecast's transport rests on the private employers' paid payroll registers, the ledger that calibrates the leaving
  rate; shape `07` to `other` (BLOCK against task175), since one total and a six-sector split is not a grid. Second
  pass under the registration lock, after task178 v3 (a bank's options desk) filed first and banned
  `financial_institution`, `launch_or_rollout` and `portfolio_manager`: the world itself was redrawn from a state
  savings bank to a public servants' savings and credit cooperative, which is the commonest payroll-deduction lender
  in the region this world borrows from and makes the deduction agreements and the employers' payroll registers the
  natural records; the forcing event is then the 2027 budget's provision for the first private-employer loans, the
  role the finance manager who books it, and the forum the board that approves the budget.

## Screen

Measured on code before any card (scratchpad `b177c/proto/p2.py`, `p2sweep.py`, output `sweep_p2.out`; seeds 1 to
20 fixed before outcomes). The world: 70,000 public loans over 96 months across 70 agencies (permanent staff
leaving at 1.4 to 5.4 per cent a year, a third of agencies with 20 to 60 per cent temporaries whose loans are
capped to end before the contract), 38 private employers leaving at 10 to 42 per cent a year (log-normal around
24), 6,200 launch loans in the prototype; on leaving with the loan open the loan reaches 90 days past due 3 to 5
months later with probability about 0.55 (rising mildly with the balance left over the salary), and an on-payroll
route of 0.2 per cent a month. Graded figure: the launch loans' share in default by month 12.

| Route | min | median | max (per cent, 20 seeds) |
|---|---|---|---|
| truth (expectation on the forward borrowers) | 8.53 | 9.31 | 10.64 |
| pooled public 12-month default | 1.45 | 1.56 | 1.68 |
| logistic PD on borrower attributes, scored on the launch | 1.34 | 1.60 | 2.11 |
| temporaries as the high-leaving analogue | 1.55 | 1.79 | 2.06 |
| public PD scaled by all-staff turnover (private over public) | 3.29 | 3.95 | 4.70 |
| public permanent PD scaled by permanent turnover | 10.24 | 11.18 | 12.57 |
| golden: P(leave by month 8) x conversion + on-payroll rate | 8.82 | 9.52 | 10.57 |
| golden: conversion by month of leaving | 8.87 | 9.58 | 10.64 |
| golden: eventual conversion x lag distribution | 8.89 | 9.54 | 10.79 |
| golden: conversion by balance band | 8.68 | 9.41 | 10.46 |
| agency-level regression of default on leaving, extrapolated | 7.69 | 9.15 | 10.46 |

- **Lever:** the golden is 5 to 6 times the default path; the nearest wrong rung (all-staff turnover scaling) sits
  at 0.42 of the golden. The decomposition family's own spread is at most 0.42 percentage points (median 0.24) on a
  figure near 9.5, so about 4 per cent of the figure against a lever of several hundred per cent.
- **Bins:** at the nearest 5 per cent the four decomposition forms share the truth's bin in 20 of 20 seeds, the
  agency regression in 20, the permanent-turnover scaling in 19; the logistic and the all-staff scaling miss it in
  20 of 20. The build grades counts (the total to the nearest 50 of 2,400 loans, the sector counts to the nearest
  10), placed mid-bin on the cut world.
- **Screens (stumping 1.2) as code and algebra.** Dispersion: not a spread. Variance-only: the step moves the point
  estimate. Common-exposure subset: no public subset sits at the private leaving rate; the only high-leaving subset
  (temporaries) is the misleading analogue above (1.6 to 2.1). Partial coverage: every launch loan carries its own
  employer's leaving hazard. One-number screen: the correcting input is per employer (38) and per loan (term,
  tenure), never a scalar. Proxy screen: no shipped file publishes a turnover or headcount-change column; the
  leaving rate exists only by following employees through the registers. Truncation direction: none. The cheapest
  one-group-by route to the call: leavers per employee-month by employer from the registers, times the share of public
  loans defaulting after their treasury deductions stop for good; it is the golden's own construction once the
  exposure is seen, and nothing in the pack names it.

## Default path

1. Read the prompt, the product sheet and the credit policy: 2,400 loans disbursed on 1 February 2027, default is 90
   days past due on the loan, the window ends on 31 January 2028.
2. Load the public loan book (both cores through the crosswalk) and the default register; flag each public loan
   disbursed 2017 to 2025 that entered default within twelve months of disbursement.
3. Fit a PD model on the borrower and loan attributes the book carries (age, net salary, tenure with the employer,
   contract type, instalment over salary, term, agency type), checked out of time on the 2025 disbursements.
4. Score the 2,400 launch applications on the same attributes (tenure from the employer's certificate, contract
   type indefinite, salary from the application) and sum the probabilities, overall and by sector.

Ends on: about 50 of the 2,400 loans in default by 31 January 2028 (1.6 to 2.1 per cent).
Golden: about 250 (about 10 per cent), the launch loans' chance of their borrower leaving the employer's payroll
while the loan is open, from each employer's own payroll registers, times the share of public loans that defaulted
after their deductions stopped for good, plus the on-payroll rate.

## Stump sentence

A PD model fitted on the public book's borrower attributes and scored on the launch file files about 50 of the 2,400
loans in default by 31 January 2028; the public book's defaults run almost wholly through borrowers leaving the
payroll with the loan open, which the private employers' own payroll registers show five to six times as often, so the
count is about 250.

## Three rules

Task type: credit-scoring-pd-modeling (Banking, Credit & Financial Risk), which serves Forecasting & Predictive Modeling in the taxonomy; the call is a forward first-year default count for a new segment.
Domain test: the deciding quantity is the launch loans' first-year probability of default, which payroll-deduction lending reads as the chance that the borrower leaves the paying employer's payroll while the loan is open times the share of such loans that then reach 90 days past due, the leaving rate taken from each employer's own payroll and the conversion from the public book.
Swap: "how many of the 2,400 payroll-deduction loans will be in default a year after disbursement" with hospitals and patients in place of employers and borrowers stops making sense: nothing collects a patient's obligation at source from a body the patient can leave, so there is no event through which the outcome runs.
Layer 1: the legacy core's loans (to June 2021) carried into the new core under new numbers with a crosswalk, amounts in thousands and contract type as a letter; the treasury's deduction returns listing only the loan-months not applied, under a two-code scheme with a 2023 layout change and re-sent months; the 38 private employers' payroll registers sent under the deduction agreements since 2025, fortnightly and monthly payers side by side, mid-year and December bonus registers, vacation and final-settlement lines, re-sent registers and an employee-key change at the cooperative's 2026 intake-portal upgrade; the launch file's tenure certificates; the default register's cures and re-entries; each produced by the system named and none placed to be caught.
Layer 2: estimand and identification: which exposure the default rate is read on; the record's rate is a property of how rarely its borrowers leave their employer with a loan open, and it carries to a new population only per leaving event, with the leaving rate measured on the new population's own payroll.
Decisive step: decompose the first-year PD of a payroll-deduction loan into the borrower's chance of leaving the employer's payroll while the loan is open and the default rate that follows such an exit, read the conversion from the public book's permanent-staff loans whose deductions stopped for good, and take each private employer's leaving rate from its own payroll registers.
Not semantics: every field, code and definition read correctly (the two cores joined, the treasury codes, the 90-day definition, the registers' pay concepts) still leaves the PD model on borrower attributes at about 50, because no field names the leaving event and none states that default runs through it; the treasury's code for a deduction not applied covers a borrower short of margin and one gone from the payroll alike.
Not rule application: no filed rule or procedure says how to forecast the launch's default, and executing every stated rule (the default definition, the window, the deduction cap, the eligibility rules) leaves the estimator open; the enumerated family a competent analyst reaches for spans 1.3 to 12.6 per cent over 20 seeds (logistic on attributes, pooled, temporaries as analogue, all-staff and permanent turnover scalings, the decomposition forms, the agency regression), the standing family the data leave defensible (the four decomposition forms, the agency regression, the permanent-turnover scaling) spans at most 0.42 percentage points within the decomposition and 7.7 to 12.6 across all of it, and nothing filed does the ruling-out: the logistic is refuted by the records themselves (most public defaults follow a run of deductions not applied that never resumes, and the private employers' staff leave at five to six times the public rate), which no clause states.
Analyst test: a strong analyst who joins the two cores, reads the treasury returns and the default register correctly, fits a PD model on the public book's borrower attributes (validated out of time) and scores the 2,400 launch applications files about 50 loans in default by 31 January 2028, where the answer is about 250.
Estimand: the number of the 2,400 Libranza Empresarial loans disbursed on 1 February 2027 that are 90 days or more past due at any month-end up to 31 January 2028, as an expected count, in total and by employer sector, filed in prompt.txt and the product sheet (population, outcome, window, unit) with no comparison.
No decoy: nothing in the pack is planted to be caught; no memo, draft, briefing or stakeholder figure states a launch forecast, a turnover figure or a PD for the private segment, and no public-book PD table ships.
No certified replay: the method is not recovered by reproducing certified or published figures; no shipped figure is reproduced only by the decomposition, and the conversion and leaving rates exist only by construction from the records.
Lesson: a rate learned on one population carries to another only per occurrence of the event that produces it, and when that event's frequency differs between the populations it has to be measured on the new one's own records; no build on file reads an outcome rate per exit from the body that collects the obligation (task169 closes a route, task446 prices a flag by its kind, task177 v2 times a test's effect within a billing cycle).

## Architecture 2 record (product-analytics / churn-propensity-uplift-modeling, retired 2026-10-22)

### Draw

| Item | Value |
|---|---|
| Cell | product-analytics / churn-propensity-uplift-modeling (the taxonomy tags it F and OS), objective Forecasting, the round's second and last cell for this number |
| World | Daily Lantern Media (fictional), publisher of the national title The Daily Lantern, United Kingdom, GBP; about 1.3 million monthly digital subscribers |
| Call | the share of the 26 January 2027 at-risk list of monthly digital subscribers still subscribed on 31 March 2027 because they were sent the half-price retention offer and would not have been without it, to the nearest 5 per cent |
| Forcing event | launch_or_rollout: the offer goes out on Tuesday 26 January 2027, and the executive team weighs its cost against the subscriptions it keeps before the send |
| Stakeholder | head of subscriber retention in the audience revenue team (role family product_manager); personas Bernard Peacock and Natalie Taylor, drawn with `guard.py names --geo "United Kingdom" --seed 177` |
| Card axes | shape single-figure; decision quantity_figure, answer rate_or_share, question what; gap population then time; pattern E; generators G14, G7, G6; Gate G forecasting; calibration pilot_log; strategy composition_mix; context artifact planning_thread; forum executive_team; org family media_or_publishing; Layer 2 estimand_identification, pattern product-analytics/churn-propensity-uplift-modeling/1 |
| Guard | `guard.py check` PASS on the draft, with NOTE lines for seven older builds that share the gap, pattern and decision type or Gate G (task167, task31, task44, task56, task57, task76, task124), each differentiated on the card; the forcing event was first drafted as budget_or_appropriation, which task486 holds in the window, and the honest forcing fact is the send date; the gap reads population first, as the corpus codes a composition step (task165, task163, task83), and time second |

**The mechanism.** Last January the retention team sent the offer (half price on the next two monthly bills, taken by
a click within 30 days) to a random half of its 31 January 2026 at-risk list of monthly subscribers and held back the
other half. Subscriptions then billed on each subscription's own day of the month, so the test's deliveries fell at
every point of the subscribers' billing cycles. A subscriber weighs whether to keep paying as the next bill comes up:
an offer that lands in the fortnight before the bill catches them deciding and keeps about three in four of those who
would have gone at that bill, while one that lands earlier is mostly forgotten by then. The test therefore averages a
strong effect on the subscribers whose bill fell within two weeks of the send and almost none on the rest, about 9
kept per 100. From the October 2026 bill run the new subscriptions platform bills every monthly plan on the 1st, so
this January's list, sent on 26 January, has every bill on 1 February, six days after the send, and is kept at the
rate the test measured on its subscribers billed within two weeks of the send, about 20 per 100.

**Data-native sentence.** Last year's bills fell on each subscription's own day and this year's all fall on the 1st,
so the test spread its deliveries evenly over the billing cycle while this year's offer lands six days before every
bill; the offer works through the bill decision, and only the days from delivery to bill, rebuilt from the invoice
ledger, tell the test's persuadable half from the rest.

**Sources.** The library card product-analytics/churn-propensity-uplift-modeling/1 (target persuadables on randomised
treatment and control) is the default path done right; the stump is the judgment it takes for granted, that the effect
belongs to the subscriber rather than to where the offer lands in the subscriber's billing cycle. Cards 3 and 4 of the
same task type (Qini, rank by effect) are the same route. Strategy F5 (composition): the conditioning property here is
new, a delivery's place in each unit's own decision cycle, rebuilt from the invoice ledger and the send date and never
a column.

### Screen

- Measured before the card, on prototypes in the session scratchpad (r177/c2/proto; rebuild from code): c2a to c2f are
  in-memory worlds; c2pack.py writes a file-only mini-pack; c2out.py is an outsider re-implementation that reads only
  those files and builds every quantity with its own conventions.
- Lever against the family, on the outsider over three mini-pack seeds (7, 8, 9; truth 20.1 to 20.3 per cent): every
  route without the bill-timing step lands 9.4 to 9.9 (pooled difference of the arms, the outcome read by request
  date, two-model logistic and gradient boosting, transformed outcome, strata by plan and device, openers against the
  holdout), the 10 bin; every route with it lands 18.0 to 21.0 (bins of the days to the next bill inside the
  fortnight, a single day at 6, local linear at day 6 with bandwidths 3, 5 and 8, logistic with treatment by day
  splines, two-model with the days as a feature), the 20 bin. The lever is about 10.5 points against an outsider
  spread of 3.0 points (1.5 without single-day bins).
- Scalings that could land by accident: the arms' difference over the open rate 31 to 33, over the acceptance rate 74
  to 80, accepters against the holdout 44; none in the 20 bin. In prototype e an open rate of 45 per cent, the
  fortnight's own share of the cycle, put the first of these at 18.3, so the email world keeps the open rate near 30
  per cent.
- Constructions that build the days wrongly: the next invoice actually seen (leavers have none and drop out) 5.7 to
  7.1; the start date's day read as the bill day (wrong where a recovered failed payment moved it, and at month ends)
  14.6 to 17.2; a window running past the fortnight (days 1 to 16, 1 to 21) 13.4 to 18.3. Each is closed by the
  record: the invoice ledger carries every billing period, and the arms' difference by day falls to zero after day 14.
- Screens as code: the subset screen, filters on plan, device, tenure and engagement, gives 9.4 and none reaches the
  golden; the subset billed on the 1st reaches it, because day 1 sits in the fortnight, which is the decisive step
  taken under its calendar name. Dispersion does not apply (a level). Variance-only passes (the point moves from 10 to
  20). Truncation direction does not apply. The one-number screen passes (the correcting input is per subscriber, each
  one's days to the next bill). The forcing-file screen passes (no file holds the days to the bill, an effect by bill
  timing or a test readout). The dial (stumping 1.1): the family that skips the step is unanimous at 10 and the family
  that takes it unanimous at 20, with nothing left to choose inside either.
- Pack sizes from the screen: last year's test 200,000 subscribers half and half (single-day bins spread 3 to 5 points
  at 150,000), this year's list about 40,000 to 60,000.

### Default path

1. Build last January's test: the arms from `retention_campaign_2026-01_assignment.csv` (offer against holdout, as
   randomised), each subscription still subscribed on 31 March 2026 from `subscription_events.csv` (access_ended is the
   last day of access; a restart by 31 March counts), the subscriber features from `subscriber_profile_2026-01-31.csv`.
2. Fit the field's uplift model on the test: two models (offer arm, holdout) on the subscriber features with gradient
   boosting, the transformed outcome as the check, Qini on held-out halves; or read the arms' difference, 9.65 per 100.
3. Score this year's list (`at_risk_list_2027-01-26.csv`, the same features) and average the predicted uplift: 9.1 to
   9.5 per 100 across the textbook learners, 9.5 to 9.7 stratified by plan, region, device or risk band.
4. Report the share of the list kept by the offer to the nearest 5 per cent.

Ends on: 10 per cent
Golden: 20 per cent

### Stump sentence

An uplift model on last January's half-and-half test (two-model or transformed outcome on the subscriber features)
scored on this year's list files about 10 per cent; the test's subscribers whose next bill fell within two weeks of the
send were kept at about twice the overall rate and almost none of the rest, and every bill on this year's list falls
six days after the send, so the share is about 20 per cent.

### Three rules

Task type: churn-propensity-uplift-modeling in product-analytics, which serves Forecasting & Predictive Modeling: an uplift model estimated on a randomised retention test and scored on the next list to forecast the share of it the offer keeps.
Domain test: the deciding quantity is the heterogeneity of a retention offer's uplift by where the delivery lands in each subscriber's billing cycle (the days from the send to the next bill), estimated from the randomised test and carried to a list whose deliveries all land at one point of that cycle, which is the product analyst's own transport of an uplift from the test population to the target list.
Swap: with a utility's energy-saving nudge for the offer (homes for subscribers, the meter read for the bill) nothing is decided at a cycle edge and a nudge's effect does not lapse two weeks before the read, so the transport collapses to the test's average; the task stands on the subscription bill as the moment a monthly subscriber decides whether to keep paying.
Layer 1: the legacy billing export in pence with day/month/year dates and each subscription on its own billing day, moved for one in ten by a recovered payment; the platform's export in UTC with lines as JSON and invoices at account grain; the crosswalk between them; bills on the 29th to the 31st falling on 28 February; restarts inside the window; the app's acceptances under the app's own key and code; the save desk's half price under the offer's billing code; each mishandled alone leaves the call at 20 (R2 and SF rows in checks.py).
Layer 2: estimand_identification, card 1 of the task type (target persuadables on randomised treatment and control): the test identifies the offer's effect, but the effect belongs to the delivery's place in the billing cycle, and this year's list sits at one place in it, so the uplift is the test's own at that place, which only the bill days rebuilt from the invoice ledger reveal.
Decisive step: rebuilding each test subscription's days from the send to its next bill from its January 2026 bill in the legacy ledger, finding the offer's effect confined to the fortnight before the bill (about 20 per 100 there, under 1 after), and carrying that rate to a list whose every bill falls six days after the send.
Not semantics: every field, code and date read right (the arms, access_ended, the restarts, the January bills, the 1st-of-month calendar) still leaves the test's pooled difference or a feature-based uplift model scored on the list, which files 10 per cent; no field, code or definition says the effect depends on the bill.
Not rule application: no filed rule says how the test is carried to this year; the billing note's calendar is a fact both routes read, and executing every filed sentence with the textbook uplift model or the arms' difference files 10 per cent.
Analyst test: a strong analyst who reads every file right, takes the randomised arms and the outcome on 31 March, fits a two-model uplift on the subscriber features (or reads the arms' difference) and scores this year's list files 10 per cent, where the share is 20 per cent.
Estimand: the prompt files the population (the 48,000 subscriptions on the 26 January 2027 list, every one of them sent the offer), the outcome (still subscribed on 31 March 2027), the comparison (sent the offer against not sent it), the window (to 31 March 2027) and the unit (the share of the list, to the nearest 5 per cent); the dictionary files what subscribed on a day means (access_ended is the last day of access) and the plan that last January's arms were a random half.
No decoy: nothing is planted to be caught; no memo, briefing or figure states a share kept, an uplift or an effect by timing; the validation summary (a distractor) reports the risk model's calibration, a different quantity, and ranks nothing; the reader survey (a distractor) carries stated intentions only.
No certified replay: no published or certified figure reproduces the method; the effect by the days to the bill is recovered from the test's own records and no shipped figure is a function of it.
Lesson: an offer's uplift belongs to where it lands in the customer's decision cycle as much as to who the customer is, so a test whose deliveries fell across the cycle under-forecasts a send that lands at the decision point for everyone; no build on file turns on a delivery's place in each unit's billing cycle.

### Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| Arms and outcome built from the assignment and the events | plan ("a random half"); dictionary (access_ended) | arm, access_ended, restarted | yes | none | the joins | no | readable |
| Uplift model on the subscriber features, scored on the list (the card route) | none | the same features in both lists | the field's textbook | none | no | no | readable |
| This year's next bill on 1 February | note 1.2 | the platform lines' service periods | yes | none | no | no | readable |
| (decisive) The offer's effect by the days from the send to each test subscription's next bill, carried to six days | none: no document says the effect depends on the bill | the bill day lives only in the legacy ledger's January lines; no column holds a lead to the bill | the subscriber's features are the reflex | none: no file holds an effect by bill timing or a readout of the test | no sweep reaches it | no: a constructed covariate, then a conditional effect | silent |

### Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the share | of the 48,000 subscriptions on the list | of those who would have gone (a save rate) | another quantity | the prompt ("share of the 48,000 subscriptions") |
| SF2 | still subscribed on 31 March | the paid period covers that day; access_ended is the last day of access | access_ended read as the first day without access | same call (19.69) | the dictionary; converges |
| SF3 | a restart by 31 March | subscribed | restarts ignored | same call (20.39) | the dictionary's restarted event; converges |
| SF4 | because they are sent the offer | the effect of sending it, every list member sent | the effect of taking it (accepters against the holdout) | 45 (42.79) | the prompt ("because they are sent") |
| SF5 | who is sent this year | every subscription on the list, nobody held back | a holdout kept | same population | the plan ("nobody is held back this year") |
| SF6 | last January's comparison | the offer arm against the holdout, as randomised | the arms read off the email log (bounces as not sent) | same call (19.38) | the plan; the assignment file; converges |
| SF7 | a test subscription's billing day | its January 2026 bill | its December 2025 bill; started_on's day | same call (19.88; 18.98) | the dictionary (billed monthly on its billing day); converges |
| SF8 | bills on the 29th to the 31st in February | 28 February, 28 days after the send | 1 March | same call (19.88) | converges (outside the fortnight either way) |
| SF9 | the lead counted from | the send day (31 January 2026, 26 January 2027) | the list's cut (25 January 2027, seven days) | same call | converges (every lead inside the fortnight) |
| SF10 | this year's next bill | 1 February 2027 for every subscription | none | same call | note 1.2; every list subscription's own January line ends 31 January |
| SF11 | the bills inside each horizon | two: February and March in both years | none | same call | the calendars (asserted for every billing day) |
| SF12 | rounding | the unrounded share, once, to the nearest 5 per cent, halves away | rounding the per-day rates first | same call | the prompt's closing sentence |
| SF13 | the offer | the same offer as last January | none | same call | the plan ("The same offer went to a random half") |
| SF14 | the outcome read | by access (live on 31 March) | by the cancellation request | same call (18.72) | the dictionary; converges |
| SF15 | the unit | the subscription, in both lists | the customer | same call (one subscription per customer number on each list) | the prompt; the assignment's subscription_ref |

### Ladder

| Rung | Route | Figure (nearest 5 per cent; unrounded) | Dies to |
|---|---|---|---|
| 0 | the arms' difference, or an uplift model on the subscriber features scored on the list (the default path) | 10 (9.09 to 9.89) | the test by days to the bill: about 20 inside the fortnight, under 1 after |
| 1 | the difference scaled by the open rate, by the acceptance rate, or accepters against the holdout | 35, 70, 45 (33.35, 71.33, 42.79) | the prompt's "sent" (SF4) |
| 1 | the lead built from the next bill seen in the ledger (leavers have none) | 5 (5.89) | the ledger, which carries every test subscription's January bill |
| 2 | a window running past the fortnight (days 1 to 21) | 15 (13.76) | the by-day table: the difference falls from 18 to 14 to 6 across days 13 to 15 and is 3.5 or less on every later day |
| 3 | (decisive) the lead rebuilt from the January bills, the fortnight's rate carried to a list billed six days after the send | 20 (19.88) | the answer |

Worth: rung 0 is unanimous, every learner and stratification without the lead between 9.09 and 9.89, and every route
with it between 18.94 and 20.81 (bins of the lead inside the fortnight from days 1 to 14 down to day 6 alone, local
linear at day 6 with bandwidths 3, 5 and 8, two-model logistic and gradient boosting with the lead, the transformed
outcome and the X-learner with it, a logistic of treatment by the lead with and without knots), so the lever is about
10 points against a family spread of 1.9 (the outsider at the screen: 9.4 to 9.9 against 18.0 to 21.0). One standard
error either way (0.35) stays in the cell, 2.38 inside its lower edge. The bill day read off started_on lands 18.98 and
a window to day 16 lands 17.78, both in the golden's cell. The forecast's truth in the world (each list member's
expected share kept at a six-day lead) is 20.93.

### Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | the 48,000 subscriptions on the 26 January 2027 list, every one sent the offer | the prompt; the plan; SF1, SF5 |
| 2 Unit of account | a subscription | the prompt; SF15 |
| 3 Attribution window | subscribed on 31 March 2027 (31 March 2026 in the test) | the prompt; the dictionary; SF2, SF3 |
| 4 As-of dating | the extracts pulled 25 January 2027; the list cut that day | the plan; the list's file name and dictionary |
| 5 Version basis | the same offer as last January | the plan; SF13 |
| 6 Denominator | the list's 48,000 subscriptions | the prompt; SF1 |
| 7 Weighting | subscriptions, not customers or revenue | the prompt's "share of the 48,000 subscriptions" |
| 8 Window length | the test's whole list, its arms as randomised | the assignment file; SF6 |
| 9 Boundary inclusivity | 31 March inclusive (live on the last day of access) | the dictionary; SF2 converges |
| 10 Rounding path | once, at the end, to the nearest 5 per cent | the prompt; SF12 |
| 11 Tie-break | none arises | not applicable to a single share |
| 12 Maturity and censoring | every test subscription observed to 31 March 2026 | the events run to 25 January 2027 |
| 13 Order of operations | the lead built before the arms are compared | C1: the bins and the models give the same cell |
| 14 Row order | file order irrelevant | C1 |
| 15 Duplicate resolution | one January bill per test subscription | asserted (SEPARATION) |
| 16 Identity normalisation | the legacy reference across the assignment, the CRM snapshot, the ledger and the events | the dictionary; one key throughout |
| 17 Netting against gross | none on the call | not applicable |
| 18 Dimensional units | days and shares | not applicable |
| 19 Code and status semantics | the arm codes, the event codes | the dictionary; never the stump |
| 20 Integerisation | none | not applicable |
| 21 Clause scope | the 1st-of-month calendar covers every monthly digital subscription from 1 November 2026 | note 1.2 |
| 22 Forward window contents | two bills inside the window, 1 February and 1 March 2027, the offer on both | the plan (the next two monthly bills); note 1.2; SF11 |

### Literal reader

The method is open and forced by the record: the arms' difference by the days from the send to each test
subscription's next bill is 18 to 22 per 100 on every day from 1 to 13, 14.3 on day 14, 6.4 on day 15 and 3.5 or
less on every day after it, so the record itself says where the test's effect lives, and every route that conditions on
the lead lands 18.94 to 20.81. Executed word for word, the prompt fixes the population, the outcome, the comparison,
the window and the rounding; the plan fixes that every list member is sent the offer and that last January's arms were
a random half; the dictionary fixes subscribed on a day (access_ended the last day of access); note 1.2 fixes this
year's calendar. Every reading the text leaves open (access_ended inclusive or not, restarts counted or not, the arms
from the assignment or the email log, the billing day from the January or the December bill or started_on, the 29th to
31st on 28 February or 1 March, the lead counted from the send or the cut, the outcome by access or by request) gives
20 per cent (SF2 to SF15 in checks.py), and the reading that does not (the effect of taking the offer) violates the
prompt's "because they are sent". The default path reads the same literal estimand with the easy method.

### Oracles

- `billing_move_note_2026.pdf`: the platform's calendar (1.2), an input every route uses alike; it says nothing about
  the offer.
- `retention_model_validation_2026-12.pdf` (distractor): the risk model's calibration by band; it ranks nothing and
  reports no effect of any offer.
- `reader_survey_2026_q4.csv` (distractor): stated intentions; no arm, no bill.
- None ranks the forecast, states an uplift or confirms a timing effect.

### Ask sheet

**Main call's declared row population:** last January's assignment, its CRM snapshot, its events to 31 March 2026 and
each test subscription's January 2026 SUB line in `legacy_billing_invoices.csv`; this year's list and note 1.2's
calendar (each list subscription's own January line confirms it). Device and hazard rows in it: 0 (SEPARATION in
checks.py: one January bill per test subscription and no discount on it, the events carry the test's list only, and
this year's next bill is 1 February under every reading). Every row the call reads is frozen at round 1's bytes (FROZEN
in checks.py: the assignment, the CRM snapshot and the list byte for byte, the access and restart events, the January
SUB lines, each list subscription's last billed day, and every test subscription's outcome, arm and lead). The note the
call reads carries ask B's two filed hazards (3.2, and 4.1 to 4.2) and neither ask's primary.

**Ask A. The discount last January's offer gave on bills raised in February and in March 2026, on each plan, and how
many subscriptions on each plan took it** (9 figures, pounds to the nearest hundred, whole subscriptions). Golden,
unchanged since round 1: February 31,100, 22,200, 12,600; March 28,200, 20,200, 11,800; takers 6,224, 3,174, 1,402.
- H18 home: what the offer gives away, set against what it keeps (the plan's own words).
- Basis: the asking sentence (each bill by the month it was raised, the plan in the CRM snapshot); the plan's terms
  (half price on the next two monthly bills, on the subscription's own plan price; "A subscriber takes it from the
  offer email or the in-app message", so taking it is accepting it). Accepting and being discounted give one count:
  every subscription that accepted was discounted on its bills, as a discount line, a credit or the app's rate
  (asserted; reader C's "353 accepted but never had the discount applied" were the rate bills it did not read).
- Primary A1 (D2 the record posted under another line type; silent on the discount-line routes): 853 acceptances the
  engine applied only after the subscription's first discounted bill had been raised. Billing posted the half price on
  each of their two bills as a credit (CRED) against the acceptance, under the offer's code and the acceptance's
  reference, with no discount line. Every quoted reader route filters the discount lines (reader B: "legacy DISC lines
  whose applied_ref is an offers-engine acceptance"; reader D: "DISC lines with OE26 refs (customer-service STAY50 CS-
  refs excluded) plus half-price -MA plan lines"). On reader D's route every discount cell is low by 954 to 2,505
  pounds and every takers count by 501, 240 and 112; on reader B's by 1,422 to 3,815 and 763, 374 and 169. Fair: each
  such credit carries the offer's code, the subscription's own acceptance reference and exactly half its January
  charge, on its February and March bills only, and a block 3 step names the handling. Silent: the dictionary lists
  CRED as a credit, the goodwill credits sit beside them as CRED lines too, and every discount line still ties to an
  acceptance.
- A2 (D3 the discount carried in the charge; round 1's primary, now a hazard, filed in the dictionary since round 2):
  453 app acceptances the engine never applied, billed at the app's half-price rate (DIG-MA, DGP-MA, FAM-MA) with no
  discount line.
- A3 (D7 the true key elsewhere; a hazard): 692 app acceptances keyed by an app user id the CRM snapshot no longer
  holds; joined through the CRM's keys (the cracker, reader C) every takers count is low.
- A4 (D5 a category crossed by label; a hazard): the save desk's own half price uses the offer's billing code STAY50 on
  3,208 February and March lines, each naming a customer services case.
- A5 (D1 the same records under two keys; a hazard): 185 app accepters also accepted from the email under their CRM
  number, an acceptance no bill applied.
- A6 (a hazard): the app's acceptances carry the app team's code LNT-APP-JAN26; read off STAY50 alone (the mirror),
  every cell is low.
- Stops (`cracker.py`, each a complete pipeline): the mirror 0 of 9; the cracker 0 of 9; reader A's discount-line
  route (round 1) 0 of 9; reader B as quoted 0 of 9; reader C's route 0 of 9; reader D as quoted 0 of 9; the
  discount lines, the credits against an acceptance and the rate bills 9 of 9.
- Span: the offers engine, the CRM snapshot, the ledger, the assignment, the dictionary (5 files).
- Realism: an engine that applies an acceptance after a bill has gone out posts a credit against that bill; an app
  team ships its own code and a fallback rate; an app's user id changes on a re-login; a save desk reuses a code.

**Ask B. What this year's list was billed for its plans in each month from October 2026 to January 2027, net of credit
notes and of the goodwill credits on its invoices alike, on each plan** (12 figures, pounds to the nearest hundred).
Golden, unchanged since round 1: October 135,700, 105,500, 72,700; November 257,900, 199,400, 136,100; December
259,100, 200,200, 136,500; January 259,100, 200,300, 136,600.
- H18 home: what the list brings in, the revenue the offer protects beside what it gives away.
- Basis: the asking sentence, which since round 1 pins credit notes and the in-invoice goodwill credits alike (the
  judge measured the credit-notes-only reading at 300 to 1,100 pounds a cell); note 3.2 (Billing Operations reports
  each bill in the month of the UK date it was raised); note 4.1 and 4.2 (the duplicate October bills, and since round
  2 "Each credit note lists the legacy invoices it reverses and reduces those bills"); the dictionary's lines schema
  (qty, unit_amount, amount) and the legacy pull's scope (the bills of the subscriptions on either list and their
  add-ons), both filed since round 2.
- Primary B1 (D6 one line for two subscriptions, its convention filed): the dictionary files each platform line's qty
  as the number of subscriptions it bills and its amount as qty times unit_amount. 921 list subscriptions share their
  account with a second subscription on the same plan (a partner's, a student's), 594 of them set up the same day; from
  the run in which their lines are identical, the platform bills both on one line of qty 2 filed under the list
  subscription, in every month. Summing the amounts on the list's own lines (reader B's route: "platform invoice lines
  for list subscription ids, plan items only, goodwill credit lines (LOYAL-CR) netted, month = UK date of issue"),
  every cell is high, by 884 to 4,905 pounds; with the credit notes netted at their totals every cell still misses (by
  2,351 or more), and with the legacy October bills added and each covered bill taken off, by 884 or more. Fair: every
  qty-2 line bills exactly twice the list subscription's own charge, and each household's other subscription is in the
  pack under its own id (its own line before the two lines merge, or the crosswalk on the same account) and on no list;
  a block 3 step names the handling. The device is the reader's: the convention is filed, and seeing that the second
  unit is the household's other subscription is the work.
- B2 (D6 and D7; round 1's primary, now a hazard): the platform invoices per account, its subscription_id the first
  line's. The invoices filed under the list miss the 1,647 list subscriptions paid from another subscriber's account
  and carry the other plans on list accounts. On that route (the cracker), every cell misses by 152 to 5,094.
- B3 (D8; a hazard): the 1 October run was raised at 00:05 UK time, 23:05 to 23:59 UTC on 30 September.
- B4 (D6; a hazard): an invoice's total holds the Puzzles add-on and any other plan on the account.
- B5 (D1 and D2; a hazard): the legacy system's 1 October bills for seven batches and the platform's account-level credit
  notes of 14 October covering them (add-ons and other plans in). Note 4.2 files that a credit note reduces the bills it
  covers, so netting a note at its total against its header subscription is ruled out; the covered bills missing from
  the pull belong to subscriptions on neither list (the pull's filed scope). The duplicates and their credits cancel
  exactly on the list's plans, so the one-unit handling with neither, or with both, gives the golden (asserted).
- B6 (a hazard): goodwill credits of two pounds as negative lines; left out, every cell misses.
- Stops (`cracker.py`): the mirror 0 of 12; the cracker 0 of 12; reader B as quoted 0 of 12 (readers C and D took
  none of ask B in round 2 and are measured on the same route); reader B with credit notes at their totals 0 of 12;
  reader B with the legacy bills and the covered bills 0 of 12; one unit of each list subscription's own lines 12 of
  12.
- Span: the platform export, the list, the ledger, the crosswalk, the note, the dictionary (6 files).
- Realism: billing platforms print identical charges of one account on one line with a count; one subscriber pays for
  another's plan; a migration's first run lands on the old system's last night; a run not switched off is credited per
  account.

**Hazard table:** the replaced app ids (ask A, every cell); the save desk's code (ask A, every discount cell); the app's
code (ask A, every discount cell); the double acceptances (ask A, takers); the account grain (ask B, every cell); the
platform's UTC (ask B, October); the account totals (ask B, every cell); the duplicate October bills and their credits
(ask B, October); the goodwill credits (ask B, every cell).

**Referee:** the engine's acceptances against the ledger's applied_ref (which acceptances no bill applied), and each
platform line's text count against the list (whose subscriptions a line bills). These are the only records of either.

Pair ceiling: 28.5. The cracker lands the call with every filed rule and the hygiene battery and keeps 0 of 21 ask
figures; the mirror stops at the test's whole-list difference and keeps 0 of 21. Both round 1 readers missed the call
(10 and 10), as did both round 2 readers; on all four readers' routes in cracker.py the asks keep 0 of 21.
Mirror leakage: 0.0 per cent of ask weight
Measured by: generator/cracker.py

| Ask | Cracker sheet (every filed rule, the hygiene battery, the obvious keys; reader B's quoted routes) | Hits | Verdict |
|---|---|---|---|
| Ask A, last January's offer discounts and takers, nine figures | the engine's acceptances through the CRM's keys, the desk left out, their February and March discounts | 0 of 9 | miss |
| Ask A, reader B's quoted route (and reader A's) | the discount lines that name an acceptance, the plan of the bill's SUB line, takers the subscriptions on them | 0 of 9 | miss |
| Ask B, this year's list billed for its plans, twelve figures | the invoices filed under the list, plan lines with goodwill, UK time, legacy bills and credit notes netted | 0 of 12 | miss |
| Ask B, reader B's quoted route and both credit-note variants | the list's lines by their own ids, plan items, goodwill netted, UK date; then credit notes at totals; then legacy and covered bills | 0 of 12 | miss |
| Ask A, reader C's route (round 2) | the engine's acceptances through the CRM's keys as takers, the discount lines naming an acceptance | 0 of 9 | miss |
| Ask A, reader D's quoted route (round 2) | the discount lines with OE26 refs, CS cases out, plus the -MA rate lines at list price less the charge | 0 of 9 | miss |

### Leak sweep

`leak.py --asof 2027-01-25` on the round 3 pack (target.zip c2789bda): REVIEW, no LEAK, the same four lines. Each answered:
- Design-note vocabulary, the prompt: the ask sentence carries "subscriptions" and "invoices" because those are the
  asks' own nouns (ask A's takers, ask B's goodwill credits on the list's invoices, pinned since round 1); it says
  nothing about where a delivery lands in a billing cycle.
- Answer figures, `retention_offer_plan_2027.docx`: the plan states the question the executive team needs answered
  (the share of the list still subscribed on 31 March 2027 because of the offer) in the call's own words, and no
  figure; no file states a share, an uplift or an effect by timing.
- Design-note vocabulary, `billing_move_note_2026.pdf`: three generic billing words (billing, subscription, invoice);
  the note is Billing Operations' own record of the move, which ask B needs, and it says nothing about the offer.
- Dates after the setting, `subscriptions_platform_invoices.csv`: January 2027's billing periods end on 31 January
  (period_end and each line's "to"); every document was raised on or before 25 January (H16 in checks.py).
- The first cut's LEAK (the assignment file named with `test_`) and its REVIEW (a column named `main_device`) were
  fixed in the generator: `retention_campaign_2026-01_assignment.csv`, `most_used_on`.

House fixes run at stage 3: H6 (note 1.2 now says a new subscription's first bill is raised on its start day, as the
platform does), H16 (restarts after the pull are not in the events), H5 (note 3.2 pins a bill to the month of its UK
date), H9, H16 and H25 wired into checks.py (the dictionary names every CSV; no export holds a record after the pull;
both PDFs read in pypdf strict, pdfminer and pdftotext with their key sentences), H1 audit clean on the pack and the
goldens, H4 the zip's 14 members equal the tree byte for byte. The PDF footers carry no company number. H21: no real
title is called the Daily Lantern; the nearest is The Lantern, Ohio State University's student daily, another country
and kind of paper. `guard.py surface`: exit 0, six pairs promoted at card level only (task167, task76, task31 and task56
share the gap, pattern and decision type and are differentiated on the card; task179, two numbers away, retired on
2026-10-21; task229, a hydrometry flagging build, on surface tokens alone); no shared table schema; personas Bernard
Peacock and Natalie Taylor only. `guard.py heart`: PASS through round 2; on 2026-10-22, after the pull to bbc366d5, BLOCK on ban.strategy (composition_mix) and ban.forum (executive_team) against task446 v3, registered at 05:35:41Z on 2026-10-21 in another session and on main only after this card's registration at 05:48:20Z. The mechanism's label is the honest one, so no axis is relabelled; the author rules, as for architecture 1's window BLOCK.

## Architecture 1 record (psychology-behavioral-science, spent at Gate F on 2026-10-21)

**Status: architecture 1 spent at Gate F on target.zip 3be16ba3 (2026-10-21), paused at stage 1; the second cell this
round is assigned by the main session.** The round 5 re-judge was DETERMINISTIC and APPROVE, and a scored reader's
outcome-weighted habit model landed the 25 bin (`## Tried and rejected`). The history of architecture 1 follows.
Rounds 1 to 3 (2c536aaa, 2c11b94b, 8ab100af) re-sited the asks twice and moved the forecast to the nearest 5 per cent; round 3's
readers kept 0 of 24 asks. Round 4 on a2c932a3: readers G and H missed the call (10 and 20) and kept 0 of 24 asks; the
re-judge DETERMINISTIC, FIX_NOW, its own implementation at 26.9 to 27.2, 0.3 to 0.6 under the cell's 27.5 edge. The
four judge passes had run 26.0, 25.7, 26.4 to 27.2 and 26.9 to 27.2 against the generator's 26.05. Diagnosed by an
outsider's re-implementation (`## Outsider diagnosis`): the drift is two choices, the phone's outcome rate taken over
every call with the transfers' voice outcomes in it (+0.49, a scenario fact, now filed as plan 3.3) and the transferred
calls' own choice left out of the likelihood (+0.62, open in the record); together they reproduce the judge's 27.1.
The forecast was re-centred in its cell with the acceptance count (2,041 of 2,400 to 2,003 of 2,400): the golden 25.21,
every open reading a point or more inside. The learner, its rates and the transfers' weighting stay unfiled; the call's
other data files and its session rows are the round 1 judged pack's byte for byte (the J block in checks.py). The seed FC48 world (drop-off recycling bins) died at stage 1 on measurement before any card was filed
(its record is kept below under `## Seed world` and in `## Tried and rejected`). The redraw was handed the cell
psychology-behavioral-science / decision-making-computational-behavioral-modeling and searched it by prototype on
2026-10-19: goals as reference points (A) and drift-diffusion speed-accuracy adaptation (E) died on measurement and on
the library test, a dozen more on paper, and the imposed-contact learning discount (F) held. Prototypes are in the
session scratchpad (r177/proto).


### Draw

| Item | The draw |
|---|---|
| Card | `cards/task177.json`, registered at the DRAWN commit (e886198) through the round's serial lock |
| Pairing | `psychology-behavioral-science` (client domain), task type `decision-making-computational-behavioral-modeling` (serves Forecasting), objective Forecasting |
| World | Prairie Works Manitoba (fictional), a provincial employment and income assistance service; jobseekers on a claim check in every 14 days and ask questions in between, by calling the claimant line or through its digital assistant, Ask Prairie Works (app, web, and a voice service the claimant queue's overflow transfers calls to) |
| Decision | the March and April 2027 usage tiers for Ask Prairie Works, due on the vendor's order form by 8 January 2027 (`purchase_order_or_contract`); the head of contact services signs it (`line_manager_or_team`); the forecast comes from Digital Channels (`policy_adviser`) |
| Call | the share of the contacts that jobseekers on the register on 3 January 2027 start themselves from 1 March to 25 April 2027 that they start in Ask Prairie Works, after release 4.0 has answered every claimant-line call from 4 January to 28 February: **25 per cent** (to the nearest 5 per cent; unrounded 25.21) |
| Shape | `02`, a forecast for the window after the assistant-first weeks; the criteria come from the call, its two components and the 24 monthly cells of the asks (employers' conversations and our own staff and test conversations in each month of 2026), with the two files |
| Decision type / unit | `quantity_figure` / `rate_or_share` |
| Mechanism | gap population then time; pattern none, decisive G16 (the learning model the record selects), G7 (the assistant-first window) and G17 (the profile interval) supporting; Gate G `method_or_model_selection`; strategy `forecast_method_backtest`; Layer 2 `forecast_uncertainty`, pattern `psychology-behavioral-science/decision-making-computational-behavioral-modeling/3` |
| Calibration / context artifact | none / other (the vendor's usage-tier order form; the rollout plan is the governing document that files the dates, the routing, the check-in and what a contact is) |
| Deliverables | `assistant_share_forecast_mar_apr_2027.xlsx`, `assistant_first_aftermath_note.docx` |
| People | Loretta Rodgers (head of contact services), Sabrina Ward (Digital Channels), drawn with `guard.py names --geo "Manitoba, Canada" --seed 177 --n 30` |

**Data-native sentence.** The claimant queue's overflow sends phone-minded jobseekers to the assistant only in a few
dozen Monday-morning episodes, so the record holds eleven thousand contacts a jobseeker did not choose but never a run
of them, and a learner fitted to the whole record, where they are one assistant experience in six, back-tests well
while weighing them like chosen ones.

**The library test.** The cell's cards are the textbook route: a reinforcement-learning model of each jobseeker's
contact-by-contact channel choices compared on held-out choices (card 1), its parameters recoverable (card 2),
simulated to check it reproduces the behaviour (card 3). Applied as the cards state it, with one learning rate, it
files 40 per cent. The judgment beyond the cards, which the data settle, is which experiences teach: a contact the
jobseeker was sent to by the overflow moves their later choices about a fifth as far as one they chose (the split
beats one rate by 1,419 log-likelihood units and "transfers teach nothing" by 93), and the assistant-first weeks are
made of such contacts. The judgment without the learning model (next-contact rates after transfers, a Markov chain
split by route) misses too; the two together give the golden.

**Measured on the pack** (`generator/checks.py`, 413,866 contacts, 11,154 transfers): the golden 25.21, printed 25 to
the nearest 5 per cent and 2.29 points inside its cell (22.5 to 27.5); one learning rate 38.53; transfers teaching
nothing 19.57; no learning 13.64; transfers learned at the chosen rate (clean truth) 39.60; a pooled last-four logistic
28.89; a pooled first-order Markov chain 29.99; a pull to the last channel met 27.29 (133 log-likelihood units worse,
a form of the split that prints the golden's cell); contacts at each jobseeker's own 2026 rate with the check-in
ignored 23.23. The golden's family: 24.93 to 25.28 (a second simulation seed, starting values estimated, fitted on the
planning population only, fitted to 31 October, no overflow from 1 March, questions at each jobseeker's own rate,
claims closing at the register's rate); one standard error of the transfer rate either way 24.79 and 25.62. On the
clean truth: one rate 38.43, the split 25.10, the world's own expected window 24.99. The record selects the learning
model: fitted to January to October, the split predicts November and December's 68,677 choices better than one rate by
382 log-likelihood units and better than every reduced form (a last-one, last-four or last-eight logistic, transfers
pooled or apart; a Markov chain, pooled or apart) by 1,419 to 3,763, while one rate still predicts their share at 14 per
cent against 14 observed.

**The world after the screen** (fixed before the pack was cut, each change recorded with its reason): outcomes are
recorded by each system (an adviser's wrap-up, queue abandonment, the voice session's end state) rather than derived
from repeat contacts, because repeats make the contact count depend on the outcome and the count model became a
forecast fork of about a point; contacts are the plan's fortnightly check-in plus questions at one rate, so the
window's contacts per jobseeker are known rather than forecast; the lean is common to every jobseeker and claims
close at one rate, so the planning population's own fit, the full fit and the closures converge; the world's draw
(d7 of eight, the one whose family spread was smallest at scale 1.5) and the acceptance count were fixed last, by
the re-centre rule: 2,041 of 2,400 centred the family in its whole per cent, and in round 4 2,003 of 2,400 put the
forecast at its 5-per-cent cell's centre with the outside reproductions a point or more inside.

**Guard (2026-10-19).** WARN only. `overuse.org_family`: a public employment service is honestly a government agency,
and no government-agency build on file turns on a learning model of its clients' choices. `repeat.gate_g` and
`overuse.gate_g` (method_or_model_selection): the decisive step is honestly the selection of a learning model the
record settles; task269's is a reliability decision study, another pairing, gap and generator. `test.same_puzzle_older`
and `test.same_driver_older` are answered by the card's differentiation lines (task70, task104, task134, task168,
task463, task501, and task480's v1 lineage, drawn after this card).

**Heart (2026-10-21).** BLOCK on `ban.forum`, `ban.forcing_event` and `ban.org_family` against task248 and task165, ruled
by the author: the three furniture bans passed at registration (19 October 2026, 07:01Z, against task268, task269 and
task468) and fire only because task269 and task468 re-rooted after it, which moved task248 and task165 into this card's
window; the window stays fixed at the draw, with no card edit and no force.

**Sources, one line each.** Cards 1 to 3 of the task type give the family and the default path's route, never the
stump (stumping 1.3). task501's driver pools two regimes and rebuilds a static matrix from the season's own days;
here that static rebuild is a wrong rung, and the imposed rate sits inside a jointly fitted learning model. task148
censors a latent patience; nothing is censored here. task137 is a contact-centre world on a repricing share; the
decision, organisation, country and driver differ.

### Default path

1. Rebuild each jobseeker's contacts: calls to the claimant line from `contact_legs_2026.csv` keyed by the case number
   on the call's first leg (legacy codes through `telephony_migration_codes.xlsx`), conversations in the app or on the
   web from `assistant_sessions_2026.jsonl` through the assistant accounts in `contact_details_crosswalk.csv`, each
   conversation's outcome its last session's end state, each overflow transfer's outcome its voice session's.
2. Fit the field's reinforcement-learning model of channel choice to every contact by maximum likelihood: one value
   per channel moved by one learning rate after every contact towards its outcome, a softmax with a lean and a pull to
   the last choice; fitted to January to October it predicts 14 per cent of November and December's own contacts in
   the assistant, against 14 per cent observed.
3. Take the jobseekers on the register on 3 January 2027 (`claims_register_2026.csv`) from their end-of-record state
   and simulate the plan's weeks: every call met by release 4.0 resolving 2,003 of 2,400 to 28 February, then the line
   back to advisers with the 2026 transfer share, check-ins every 14 days, other contacts at the 2026 rate.
4. Read the share of their own contacts started in the assistant from 1 March to 25 April.

Ends on: 40 per cent
Golden: 25 per cent

### Stump sentence

One learning rate fitted to every contact and simulated through the assistant-first weeks files 40 per cent; the
overflow transfers in the record, the only contacts a jobseeker did not choose, move their later choices about a fifth
as far as a conversation they opened, so eight weeks of release 4.0 answering their calls convert far fewer of them
and the share is 25 per cent.

### Three rules

Task type: decision-making-computational-behavioral-modeling in psychology-behavioral-science, which serves Forecasting & Predictive Modeling: a reinforcement-learning model of each jobseeker's contact-by-contact choices, fitted by likelihood, compared out of sample and simulated forward.
Domain test: the deciding quantity is how far a contact the jobseeker did not choose moves their later channel choice against one they chose, a learning rate for imposed experiences inside a fitted reinforcement-learning model, which is the free-against-forced choice distinction of the field's own learning studies.
Swap: with servers for jobseekers ("the share of requests a server pool sends to the new cache after eight weeks of forced routing") nothing learns from what it was sent to, the agency term has nothing to act on, and the forecast collapses to a routing sum.
Layer 1: the platform's leg export in UTC with the legacy platform's codes and merged IVR-and-queue leg before the 6 July cutover; the vendor's session export with no zone marker and conversations split into sessions; case numbers keyed in the IVR against assistant accounts through the case system's contact details, with changed and shared phone numbers; outcomes recorded three ways; the workforce team's overflow log beside the transfers; staff and test accounts in the export; claims opening and closing; each mishandled alone leaves the call at 25 (R2 in checks.py).
Layer 2: forecast_uncertainty, card 3 of the task type (the winning model must reproduce the behaviour): the learning model has to separate chosen from imposed experiences before it is simulated through a window made of imposed ones, and the record's 11,154 transfers settle the separate rate by likelihood.
Decisive step: estimating a separate learning rate for the contacts the jobseeker did not choose (the overflow transfers) inside the jointly fitted model, and carrying it to the assistant-first weeks' calls.
Not semantics: every field, code and definition read right (transfers identified, their outcomes linked, the plan's definitions applied) still leaves one learning rate fitted to every contact, which files 40 per cent; nothing in the pack says chosen and imposed contacts differ.
Not rule application: no filed rule or procedure says how an experience moves a choice; the plan files the dates, the routing, the check-in and what a contact is, and executing all of them with the textbook one-rate model files 40 per cent.
Analyst test: a strong analyst who rebuilds every contact, maps the codes, links the transfers' outcomes, fits a reinforcement-learning model with one learning rate by likelihood, checks it on held-out contacts and simulates the assistant-first weeks files an assistant share of 40 per cent for March and April, where the share is 25 per cent.
Estimand: the prompt files the population (jobseekers on the register on 3 January 2027), the outcome (the share of the contacts they start themselves that they start in Ask Prairie Works), the window (1 March to 25 April 2027) and the unit (the nearest 5 per cent); the rollout plan's 5.1 files the denominator (every contact a jobseeker starts) and what starting a contact is (a claimant-line call is a phone start whoever answers it), 5.2 that a conversation counts once, and 4.1 the check-in on its due date.
No decoy: nothing is planted to be caught; no memo, draft, briefing, vendor estimate or stakeholder figure states a share, no file computes a forecast, and the acceptance test reports release 4.0's own resolution, a filed input every route uses.
No certified replay: no published or certified figure reproduces the method; the learning rates are recovered from the jobseekers' own records by likelihood, and no shipped figure is a function of them.
Lesson: an experience a person did not choose teaches them less than one they chose, so a period that imposes an option converts fewer people than a learner fitted to a record of mostly chosen experiences predicts; no build on file turns on a learning rate for imposed experiences.

### Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| Contacts rebuilt across the two exports | plan 5.1, 5.2; dictionary | caller_entered, call_ref, conversation_id | yes | none | the joins | no | readable |
| One-rate learning model fitted and back-tested (card route) | none | none | the field's textbook | none | no | no | readable |
| The plan's weeks simulated with release 4.0's acceptance share | plan 1.3, 2.1 to 4.1; acceptance summary | none | yes | none | no | no | readable |
| (decisive) A separate learning rate for the contacts the jobseeker did not choose | none: the plan routes calls and never says what a transfer teaches | the transfer is a routing fact on the queue leg; nothing marks how much it teaches | one rate for every contact is the reflex | none: no file scores a model | no sweep reaches it | no: a jointly fitted rate, not a ratio of counts | silent |

### Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | contacts jobseekers start themselves | calls they make to the claimant line, conversations they open in the app or on the web | callbacks the service makes | same call (callbacks are not in the exports) | plan 5.1 |
| SF2 | starting a contact in Ask Prairie Works | opening a conversation in the app or on the web; an overflow transfer is a call | transfers counted as assistant starts | 30 (27.64) | plan 5.1 ("on the phone by calling the claimant line, whether an adviser or the assistant's voice service answers the call") |
| SF3 | a conversation over several sessions | one contact, its last session's outcome | each session a contact | same call (25.46, R2) | plan 5.2 |
| SF4 | jobseekers on our register on 3 January 2027 | claims open that day | every claim in the register | another population | the prompt's date |
| SF5 | jobseekers joining after 3 January | not in the population | included | another population | the prompt's date |
| SF6 | the window's edges | Manitoba dates, 1 March to 25 April | UTC dates | same call (25.22) | converges |
| SF7 | what the assistant-first weeks route | every call reaching Claimant Services; the app as before | the app's conversations counted as imposed | another call | plan 2.1, 2.3 |
| SF8 | release 4.0's resolution | the acceptance test, 2,003 of 2,400 | the test's intents reweighted to the 2026 mix | same call (25.21) | converges |
| SF9 | the phone's resolution in 2027 | the 2026 record over the calls the queue keeps | July to December only | same call (25.22) | plan 3.3; converges |
| SF10 | overflow after 1 March | the 2026 transfer share | none | same call (25.15) | plan 3.2 |
| SF11 | contacts in the window per jobseeker | check-ins every 14 days from the claim's opening, other questions at the 2026 rate | each jobseeker's own 2026 rate, check-ins ignored | same call (23.23) | plan 4.1 |
| SF12 | rounding | the unrounded share rounded once to the nearest 5 per cent, halves away | rounding the weeks first | same call | the prompt's rounding sentence |
| SF13 | the order of a jobseeker's contacts | start times on one clock (legs UTC, sessions Manitoba time) | both read as one clock unconverted | same call (25.20, R2) | converges |
| SF14 | a call keyed by its caller | the case number keyed on its first leg | the caller's number through the contact details | same call (25.23, R2) | converges |
| SF15 | release 4.0's resolution of the conversations jobseekers open | the acceptance test's rate, as for calls | the 2026 assistant's rate (0.501) kept for the app and the web | 15 (15.61) | plan 1.3 |
| SF16 | a transfer's outcome after 1 March | release 4.0 on the voice service at the acceptance rate | the 2026 voice service's rate (0.496) | same call (25.14) | plan 1.3; converges |
| SF17 | the share's denominator | every contact the jobseekers start, the calls the voice service answers included | transferred calls left out | same call (25.84) | plan 5.1 ("every contact jobseekers start themselves") |
| SF18 | a check-in's day | its due date | as late as 2026's check-ins (0 to 3 days) | same call (25.21: each phase is four whole cycles, so no check-in changes phase) | plan 4.1 ("on its due date") |
| SF19 | the other contacts' rate | the 2026 rate per jobseeker-day | the last eight weeks' rate | same call (25.08) | converges |
| SF20 | the values' start (b, the record settles it) | halfway, 0.5 | 0, or 1 | same call (27.09, 22.63) | the record, by 6,017 and 11,385 log-likelihood units |
| SF21 | the pull after an assistant-first call (b) | to the channel chosen, the phone | to the assistant it met | 30 (28.01) | the record: a pull to the channel met is 133 units worse |
| SF22 | a transferred call's own choice (c, open) | in the likelihood, a phone start (plan 5.1) | left out of the likelihood | same call (25.80, 1.70 inside the cell) | converges |
| SF23 | the 351 on the register with no 2026 contact (c, open) | the fitted model's starting values | the others' mean state | same call (24.13, 1.63 inside) | converges; leaving them out narrows the prompt's population |
| SF24 | the phone's outcome rate after 1 March (a, filed) | the 2026 rate over the calls the queue keeps (0.883) | over every call, the transfers' voice outcomes in (0.870) | same call (25.68; 26.28 with SF22's alternative) | plan 3.3 |

### Ladder

| Rung | Route | Figure (nearest 5 per cent; unrounded) | Dies to |
|---|---|---|---|
| 0 | one learning rate for every contact, back-tested and simulated (the default path) | 40 (38.53) | the split's 1,419 log-likelihood units; the transfers' own next-choice rates |
| 1 | no learning: the last eight weeks of 2026 carried | 15 (13.64) | the 2026 series itself (35 per cent in January falling to 14) and the plan's weeks |
| 1 | transfers teach nothing | 20 (19.57) | the record, by 93 log-likelihood units |
| 2 | a pooled last-four logistic, or a pooled first-order Markov chain, of the choice | 30, 30 (28.89, 29.99) | the held-out choices (November and December, fitted to October): 1,612 and 3,763 log-likelihood units behind the split |
| 3 | (decisive) a separate rate for transfers, fitted jointly | 25 (25.21) | the answer |

Worth: rung 0 sits three cells above the golden and every route without the decisive step at least one cell from it,
the nearest the pooled logistic at 28.89, 1.39 past the cell's edge. The golden's family spans 24.93 to 25.28 and one
standard error of the transfer rate 24.79 to 25.62; round 3's readings (J3 in checks.py) run 23.89 to 25.84 and round
4's outsider readings (`## Outsider diagnosis`) 22.63 to 28.01, every open one a point or more inside the cell. Forms of
the split the record rejects print the golden's cell or the next: a pull to the last channel met 27.29 (133 units), no
pull to the last choice (1,137 units), a transfer moving the phone's value at the transfer rate 23.89 (31.8 units). The
reflexes split both ways (no learning and teaching nothing below; one rate and the reduced forms above), so no single
correction walks the default path to the answer.

### Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | jobseekers with a claim open on 3 January 2027, nobody joining later | the prompt; SF4, SF5 |
| 2 Unit of account | a contact (a call, a conversation) | plan 5.1, 5.2; SF1 to SF3 |
| 3 Attribution window | a contact in the window by the day it starts, Manitoba time | the prompt; SF6 converges |
| 4 As-of dating | the record to 3 January 2027, the plan's dates after it | the exports' coverage (manifest), the plan |
| 5 Version basis | release 4.0 at its acceptance share on every channel; the phone as in 2026 over the calls the queue keeps | plan 1.2, 1.3, 3.3, the summary; SF8, SF9, SF16, SF24 converge, SF15 ruled out |
| 6 Denominator | every contact the population starts in the window, the calls the voice service answers included | plan 5.1; SF17 |
| 7 Weighting | contacts, not jobseekers | the prompt's "share of the contacts" |
| 8 Window length | the fit on the whole record | C3: fitted to 31 October or on the population only, same figure |
| 9 Boundary inclusivity | 1 March to 25 April inclusive; open on 3 January inclusive | the prompt; C1 |
| 10 Rounding path | once, at the end, to the nearest 5 per cent | the prompt; SF12 |
| 11 Tie-break | none arises | not applicable to a single share |
| 12 Maturity and censoring | claims closing in the window drop out | C3: closures at the register's rate, same figure |
| 13 Order of operations | the learning runs in each jobseeker's start-time order | SF13 converges |
| 14 Row order | file order irrelevant; contacts sorted by start | C1 |
| 15 Duplicate resolution | a conversation's sessions collapse to one | plan 5.2 |
| 16 Identity normalisation | case number keyed in the IVR; accounts through the contact details | dictionary; SF14 converges |
| 17 Netting against gross | none | not applicable |
| 18 Dimensional units | contacts and shares | not applicable |
| 19 Code and status semantics | legacy and new codes, end states | `telephony_migration_codes.xlsx`, dictionary; never the stump |
| 20 Integerisation | none | not applicable |
| 21 Clause scope | the plan's routing applies to the Claimant Services queue only | plan 2.1, 2.2 |
| 22 Forward window contents | the plan's weeks: release 4.0 on every call to 28 February, advisers from 1 March with the overflow, each check-in on its due date | plan 1.3, 2 to 4; the acceptance summary; SF18 |

### Literal reader

The method is open and forced by the record: the reinforcement-learning family beats every reduced form on held-out
choices by 1,419 log-likelihood units or more, and inside it the separate transfer rate beats one rate by 382 held
out (1,419 on the whole record) and "transfers teach nothing" by 93. Executed word for word, the prompt fixes the
population, window, outcome and rounding (the nearest 5 per cent), and the plan's 1.3, 2.1 to 4.1 and 5.1 to 5.2 fix
release 4.0's resolution on every channel, the routing, the phone's outcome over the calls the queue keeps (3.3), the
check-in and its day, the denominator and what starting a contact is; every reading the text leaves open (the window's
clock, the intents' weighting, the phone's period, the overflow from 1 March, a transfer's outcome after it, the other
contacts' rate, the fit's data, the starting values, the closures, the Monte Carlo seed, a transferred call's choice in
or out of the likelihood, the start of the jobseekers with no 2026 contact) gives 25 per cent on the pack (SF6 to SF24,
the family, J3 and outsider rows in checks.py), and the readings that do not (transfers as assistant starts, the 2026
assistant's rate kept for the conversations jobseekers open) each violate a quotable sentence of the plan, while the
model forms that leave the cell (a transfer moving the phone's value at the chosen rate, an assistant-first call pulling
toward the assistant) are rejected by the record by 685.5 and 132.8 log-likelihood units.

### Outsider diagnosis

Round 4's re-judge reproduced every input and fit and forecast 26.9 to 27.2 against the generator's 26.05. An
independent re-implementation of the same model class (scratch, outside the build; the generator's checks.py now
carries each reading) replicated 26.01, then changed one choice at a time. Sizes at the round 4 pack (26.05):

| Choice | The golden | The outsider's alternative | Moves the share | Class | Closure |
|---|---|---|---|---|---|
| the phone's outcome rate after 1 March | over the calls the queue keeps, 0.883 | over every call, the transfers' voice outcomes in, 0.870 | +0.49 | (a) a scenario fact | filed, plan 3.3 (SF24) |
| a transferred call's own choice | in the likelihood | left out of it | +0.62 | (c) open: the two likelihoods cover different choices | left open; after re-centring 1.70 inside the cell (SF22) |
| the 351 on the register with no 2026 contact | the fitted model's starting values | the others' mean state | -1.12 | (c) open | 1.63 inside (SF23) |
| the values' start | halfway, 0.5 | 0, or 1 | +1.76, -2.71 | (b) settled: 6,017 and 11,385 units worse | the record (SF20) |
| the pull after an assistant-first call | to the phone the jobseeker chose | to the assistant it met | +2.91 | (b) settled: a pull to the channel met is 133 units worse | the record (SF21) |
| the phone's value during the assistant-first weeks | unmoved, no adviser met | moved by each call's outcome | -0.27 | (b) settled with the transfer-moves-phone forms, 31.8 and 685.5 units worse | the record (J3) |

The first two together reproduce the judge's 27.1 (27.12 at 26.05; 26.28 at the re-centred 25.21). With 3.3 filed,
the acceptance count was re-centred from 2,041 to 2,003 of 2,400 so the open readings sit a point or more inside the
cell: the golden 25.21 (2.29 inside), SF22's alternative 25.80, SF23's 24.13, both together 24.72, and the judge's own
pair 26.28.

### Oracles

- `overflow_episodes_2026.csv`: marks exactly the calls the legs mark as transferred (asserted); it confirms which
  contacts were imposed, never how much they teach, and ties under every reading.
- `vendor_invoices_2026.xlsx`: each month's billed tier band and the supplier's GST/HST number; the bands are too
  coarse to reconcile any count, so they tie under every handling of the asks' devices, and the number is ask B's
  referee for the second organisation in the staff console.
- `release4_acceptance_summary.pdf`: release 4.0's resolution, an input every route uses alike.
- `export_manifest.csv`: each file's coverage; it ranks nothing.
- None ranks the forecast or confirms a learning model.

### Ask sheet

**Main call's declared row population:** the claimant line's calls keyed with a case number (their legs in
`contact_legs_2026.csv`), the voice sessions their transfers met, the app and web conversations under accounts linked
to a case in `contact_details_crosswalk.csv`, the register, the plan and the acceptance summary. Device and hazard rows
in it: 0 (asserted, SEPARATION: no employer account and no account ever typed staff links to a case; the employer
widget's rows and the staff console's are their own channels). The round 1 repair touched none of it: the files the
call reads and no ask touches, and the call's own session rows, are the judged pack's byte for byte (J in checks.py).

**Ask A. For each month of 2026, the conversations employers held with Ask Prairie Works** (12 figures, whole
conversations). Golden: 945, 1,040, 1,555, 1,686, 1,850, 1,852, 1,660, 1,399, 1,838, 1,794, 1,799, 1,203.
- H18 home: a component of the March and April chat tiers the order commits to; employers' conversations ride the
  same tier as jobseekers'.
- Basis: the asking sentence (a conversation once, in the month it started, Manitoba time); plan 5.2 and the
  dictionary's conversation_id (a conversation keeps its id across sessions).
- Primary A3 (D7 the true key elsewhere, one conversation under two ids; silent): the widget, built by the vendor's
  integration partner, cuts its day at midnight UTC, its daily export boundary. A session still open at 00:00:00 UTC
  is closed there, written as a timeout, and the exchange carries on at that same second as a new conversation from
  the same account, so 183 conversations of 2026 reach the export under two conversation ids. Counted by
  conversation_id with the clock converted and the business number's accounts left out (both round 2 readers' path),
  every month is high, by 7 to 25 (January +8, February +7, March +25, April +8, May +20, June +21, July +11, August
  +16, September +23, October +18, November +14, December +12). Fair: each pair is a widget session ending at exactly
  00:00:00 UTC, short of the 30 idle minutes a timeout means, and its account's next session starting at that second
  under a new id; no other two employer sessions meet at a second, and the one other widget session that starts on
  the second has no closed twin. Silent: the dictionary says a conversation keeps its id across sessions, and nothing
  in the pack marks the cut.
- A2 (D8 a per-source clock; found by both round 2 readers, so a hazard now): the widget writes UTC with no zone
  marker where every other channel writes Manitoba time; employers' wage-subsidy claims fall due on each month's last
  day and many are filed that evening, so read unconverted every month moves, by 4 to 33.
- A1 (D5 out-of-scope rows known only by structure; found by every reader, a hazard): Digital Channels tests the
  employer portal under five test employer accounts registered to Prairie Works Manitoba's own business number
  (812447093, on the order form); counted as employers every month is high by 39 to 76.
- Hazards: sessions (a conversation reopened after a timeout keeps its conversation_id; plan 5.2 and the dictionary
  pin it).
- Stops (each a complete pipeline, `cracker.py`): natural 0 of 12; the business number found 0 of 12; the business
  number and the clock (both round 2 readers) 0 of 12; the business number and the day cut, clock unconverted, 0 of
  12; all three 12 of 12.
- Span: the session export, the order form, the employer line's legs, the dictionary, the plan (5 files).
- Realism: departments test their own portals under their own registration; an integration partner's widget logging
  UTC beside a vendor's local-time export is how mixed integrations really ship; a widget that partitions its log by
  UTC day splits whatever is open at midnight; claims due on a month's last day are filed that evening.

**Ask B. For each month of 2026, the conversations our own staff and test accounts held** (12 figures, whole
conversations). Golden: 1,256, 1,148, 1,326, 1,171, 1,163, 1,217, 1,332, 1,161, 1,224, 1,208, 1,252, 1,244.
- H18 home: the other component of the chat tiers; the vendor bills internal use like any other, and not its own
  support desk's.
- Primary B2 (D5 out-of-scope rows known only by structure, D9 a name agreement that lies; silent): Riverlot's support
  desk works in the tenant's staff console under seven accounts of its own (its daily checks, the days around each
  release, the cases the service raises), typed staff like ours. Ours carry Prairie Works Manitoba's business number
  in org_ref; the desk's carry Riverlot's (724906318, the supplier's GST/HST number on every invoice in
  `vendor_invoices_2026.xlsx`), on 572 of the console's 13,623 sessions. Counted as our staff, every month is high by
  29 to 71. Fair: the console carries two business numbers, the order form's customer and the invoices' supplier.
  Silent: the type is staff on every one of them, the dictionary describes org_ref for employer accounts only, and
  nothing else in the pack names the desk.
- B1 (D2 a label stored before a silent switch; one round 1 reader found it through the accounts' later staff rows,
  so a hazard now): the training team's practice accounts and Digital Channels' test accounts on the app and the web
  were created through the claimant sign-up and typed claimant until the vendor's release 3.4 re-typed them staff on
  14 September 2026; counted by type, January to September are low by 39 to 124.
- A1 shared: the test employers' conversations are our own test use, low by 39 to 76 in every month without it.
- Hazards: the staff console (staff all year), sessions against conversations.
- Stops: natural 0 of 12; the business number found (round 1 reader A) 0 of 12; the business number and every account
  ever typed staff (round 1 reader B) 0 of 12; the business number and the vendor's desk 3 of 12 (October to
  December); all three 12 of 12.
- Span: the session export, the order form, the invoices, the crosswalk, the dictionary (5 files).
- Realism: a vendor's support staff work inside a customer's tenant under their own organisation's accounts; a
  platform records each staff user's organisation; a type-only migration leaves the re-typed accounts without one.

**Hazard table:** sessions (both asks, every month, pinned); the employer widget's day cut (ask A every month, 7 to
25); the employer widget's clock (ask A every month, 4 to 33); the own business number (both asks, every month, 39
to 76); the vendor's support desk (ask B every month, 29 to 71); the re-typed accounts (ask B, January to September,
39 to 124).

**Referee:** the order form's business number (whose accounts the test employers and our console are) and the
invoices' supplier GST/HST number (whose the desk's are), the only records of either.

Pair ceiling: 28.5 (the cracker lands the call with every filed rule and every handling the readers found over two
rounds, the widget's UTC, the business number and the accounts ever typed staff, and keeps 0 of 24 ask figures; the
mirror handles the asks the same way off the call and keeps 0 of 24; a cracker finding the widget's day cut as well,
or the vendor's desk, keeps 12 of 24, a ceiling of 42.3)
Mirror leakage: 0.0 per cent of ask weight
Measured by: generator/cracker.py

Both rows were measured by the round 3 readers on 8ab100af, 0 of 12 on each ask for each reader, and neither ask's
data or wording has moved since; the round 3 repair touched the prompt's rounding of the share and two plan sentences
the asks do not read.

| Ask | Cracker sheet (every filed rule, the widget's UTC converted, the business number, every account ever typed staff) | Hits | Verdict |
|---|---|---|---|
| Ask A, employers' conversations, twelve months | employer channel less the business number's accounts, by conversation id, Manitoba month | 0 of 12 | miss |
| Ask B, our own staff and test conversations, twelve months | console, accounts ever typed staff and the business number's employer accounts | 0 of 12 | miss |

### Leak sweep

`leak.py --asof 2027-01-04` on the round 5 pack: REVIEW, five lines, no LEAK (the rounds before returned the same kinds
of line, each term list taken from that day's draft of this note). Each, harmless:
- Sweep 3, January's employer count 945 appears in the rollout plan: it is the exchange of the claimant line's number
  (204-945-0100), not a count.
- Sweep 3, the rollout plan carries 7 of 10 words of the committed call: they are the plan's own nouns for the
  estimand it files (jobseekers, the register, contacts they start, March and April); the plan states no share, no
  count and no forecast for any window.
- Sweep 4, the rollout plan carries contact, acceptance, transfer, claimant, overflow and check-in: its routing,
  planning and reporting vocabulary (the acceptance test it plans on, the claimant line, the overflow transfer back on
  from 1 March, what a contact is, the check-in's day); it never says what a transfer does to a later choice.
- Sweep 4, the acceptance summary carries window, acceptance, claimant and check-in: its test window, its own title,
  the claimant line's test number and the fortnightly check-in intent; it reports release 4.0's resolution only.
- Sweep 4, the prompt's question carries two terms of the note: they name what is counted and the routing the question
  conditions on, which the prompt has to state; neither names the learning model or the transfers.

### Seed world (FC48), set aside on 2026-10-18

**The seed world, as it stood.** Wave 8, new, Forecasting, seed FC48:
thirty unstaffed recycling drop-off points opened in December and January with 15 bins of 1,100 litres each
(ten on the coast, twenty in town, five of them in the Larchmere enclave round the lake), a July standard
(a point gets enough bins that its forecast July average weekly fill is at most 80 per cent of its bins),
weekly emptying logs carrying each bin's fill and any side waste, and a bin order due at the manufacturer by
15 March. The world, the decision and the quantity were kept; the seed's own mechanisms (the standard's "of
like demand" read as a filed method, the dashboard's district indices deciding as a decoy, a holiday-home
flag read off the property register) were set aside. Two decisive steps were screened on code, both forms of
the brief's comparison-group idea, and neither held. No architecture is live. This note holds the screen
record only; it carries none of the `precut.py` sections, because no design exists. The prototypes stay in
the session scratchpad (b177/proto).

**The structural sentence, and the first thing to read.** The graded object is a small sum of ceilings: at
each point the bins to add are the July fill over 0.8, rounded up, less 15, floored at nil, so a point that
will need 20 to 30 bins in July carries 5 to 15 of them in the answer and every per cent of error in its
July forecast moves its share of the answer two to three per cent. Each new point's forecast rests on its
own 10 to 13 winter weeks (about 2.5 per cent at a weekly noise of 8 per cent) and on its peers'
July-to-winter ratio, which runs 2 to 6 per cent apart from peer to peer within one kind of catchment. So
the right family's own members disagree by a median of 2.4 to 3.2 bins at a holiday point, which rules out
grading any point's bins, and the total moves 2.7 to 3.9 per cent under a redraw of the weekly noise. A bin
wide enough to hold the family with one sigma and a quarter-bin margin is a fifth to a third of the answer,
and at that width a flat summer uplift near the golden's own implied factor lands, along with the partly right
readings (the size or nearest-point peers, the half-term alone, the holiday points pooled). Thirty points
are too few for the lever this decision has against that noise.

**The registration finding.** The comparison-group step is honestly `composition_mix` (a district rate that
does not fit a point whose kind no column names, the kind rebuilt from the point's own winter history:
strategies F5, and task124 labelled a kind read from records the same way). task165 registered
`composition_mix` at 14:10 and task173 carries it in the queue, so the step could not be registered beside
either; `forecast_method_backtest` would have passed the guard and was not used. The window after task165's
registration (task201, task247, task165) also banned every honest forcing event, organisation and role this
world offers: the forcing event `season_or_peak` (task201, task247) and `purchase_order_or_contract`
(task165), the organisation `utility_or_infrastructure` (task201; a waste contractor running the network,
SIC 2007 section E) and `local_government` (task165), and the role `field_unit_lead` (task201, task247) and
`operations_director` (task165).

**The taxonomy finding.** The deciding quantity, each catchment's July population present against its
winter population, sits honestly in sociology-demography `population-estimation-demographic-projection` (F):
a seasonal population read from a symptomatic series, the waste itself, against catchments of like mix. The
literal home, urban-regional-science `municipal-service-demand-resource-allocation` (F), is task165's pairing
in the window.

**The repeat screen.** `guard.py recent`, `mechanisms --objective forecasting` and `slots` ran before any
card. `slots` on both candidate drivers, and on peers, analogs, summer, holiday, half-term, seasonality,
second homes, lets, owners, occupancy, cold start, like demand, comparable sites, seasonal index district,
summer uplift and drop-off bins, found no slot that spent a peer-seasonality or holiday-response mechanism;
the hits were words in unrelated notes. The closest card by mechanism is task124 (a unit's kind read from
its group's surviving records), the same family by its label.


## Tried and rejected

- **Candidate 1: peers read from each point's winter response to Christmas and the February half-term,
  three kinds of catchment** (residents, coastal villages with some lets, holiday cottages; the Larchmere
  enclave holiday cottages inside the Town district, the coast's villages and cottages mixed along the
  shore; prototypes `world4.py`, `p6.py`, `screen177.py`, whose output `screen177.out` is byte-identical over
  two runs; seeds 1 to 3 fixed before outcomes). Killed at stage 1 on measurement: the right family will not
  hold whole bins at any point, and at the width the total needs, a flat uplift and the partly right readings
  land.
  - The world: 140 mature points with two years of weekly emptyings (the Coast district 26 villages with
    some lets, 16 cottage sites and 12 residential estates; the Town district 76 residential villages and
    estates, 6 forest-lodge sites and 4 villages with some lets) and 30 new points opened 7 to 21 December
    (on the coast 5 villages, 3 cottage sites and 2 estates; in town 15 residential points and the five at
    Larchmere), the cottage points at 70 to 80 per cent of their 15 bins in an ordinary January week, the
    coastal villages at 60 to 73 and the residential points at 57 to 63. Weekly fill is the point's
    catchment (residents on a resident calendar with the Christmas packaging peak, holiday occupants on a
    school-holiday occupancy calendar) times a weekly noise of 8 per cent, with a 4 per cent summer factor of
    the point's own.
  - The golden (each new point's mean over its own weeks times the mean July-to-same-weeks ratio of its 8
    nearest mature points on the two winter responses): 153, 146 and 156 bins to add (truth 146, 144, 144).
    The right family (4 to 12 nearest, median, log and raw features, a silhouette-chosen k-means, local and
    quadratic regressions, the Christmas response alone, the whole weekly profile, a two-calendar
    decomposition, the true kind's mean) runs 135 to 157, 124 to 148 and 144 to 160, so -12 to +3 per cent,
    -15 to +1 and -8 to +3 of the golden; the k-means and the quadratic fit are the low members. One sigma
    over 12 redraws of the weekly noise is 4.4, 4.9 and 4.3 bins (2.8 to 3.3 per cent).
  - Per point the family spreads a median of 3.1 bins needed (3.11, 3.06, 3.15) and up to 5.8 to 6.3 at the
    non-residential points, against a whole bin, so no point's bins can be graded.
  - The reflexes, as shares of the golden: the district's own ratio -56 to -62 per cent, the dashboard's
    monthly index -56 to -62, every mature point's ratio -67 to -71, the 1, 3, 5 or 8 nearest points -55 to
    -69, a fit on distance to the coast -58 to -65, the Coast district's ratio borrowed for every
    holiday-looking point -36 to -44, the last July at the nearest point -78 to -83, a flat 1.25 -31 to -37, a
    flat 1.5 +33 to +34, a flat 2.0 +173 to +182, peers of like size -24, -30 and -4. The behavioural readings
    sit inside the family: the holiday-looking points pooled -12, -8 and -3, the top-ratio peers -1, +3 and +9,
    the half-term alone -5, -10 and -3. The decisive split is one obvious split (holiday or not), so it
    reads off the new points' own winter weeks once anyone looks.
  - The flat factor's total climbs about 40 to 46 bins per 0.1 and crosses the golden at 1.37 to 1.38
    (T(1.35) 145, 132 and 145; T(1.40) 166, 153 and 163), so 1.35 and 1.40 sit within 7 to 14 bins of it.
  - The back-test (each mature point forecast from its own winter 2025-26 against its July 2026, every other
    point as the pool) rejects the rivals by a visible margin: RMS log error 0.056 to 0.066 for the nearest
    peers on the two responses against 0.21 to 0.23 for the district, 0.26 to 0.27 for all points and 0.21 to
    0.22 for the three nearest points, and on the points whose kind is unlike their district 0.047 to 0.071
    against 0.43 to 0.46. Separation was never the problem.
  - Determinism at the total: rounding to 10, 20 or 25 bins, the family leaves the golden's bin in every
    seed but one (seed 3 at 25), and there one sigma breaks the quarter-bin margin; rounding to 50 holds the
    family and the margin in seeds 1 and 3 (in seed 2 the k-means leaves the bin), and puts the flat 1.35
    and 1.40, the pooled holiday points, the top-ratio peers and the half-term alone inside the golden's bin
    in every seed (and the size peers in seed 3).
  - The eda6c8c screens, as code on the clean truth: dispersion does not apply (a level; the July ratio's
    coefficient of variation within a kind is 0.031 to 0.036 for the cottages and 0.028 to 0.029 for the
    villages); variance-only passes (the golden is 2.28, 2.61 and 2.36 times the district route); the
    common-exposure subset, every filter and divide on a visible attribute (district, all points, nearest
    points, distance to the coast, size, the Coast district for the holiday-looking), misses by 24 to 71 per
    cent except the size peers in seed 3 (-4); truncation direction does not apply (overflow is logged as
    side waste and counted).
- **Candidate 2: the same reading with lets told from second homes** (the Larchmere enclave holiday lets;
  owner-used second-home villages on the coast and inland, emptier in winter and so steeper into July, as
  the lure a holiday-peer reading takes; the coast's new points lets and estates; same prototypes and seeds,
  the same output file). Killed at stage 1 on measurement for the same reason; the bracket it builds does
  not survive the width the noise needs.
  - The world: 148 mature points (the Coast district 30 villages, 14 let sites, 8 second-home hamlets and 12
    estates; the Town district 70 villages and estates, 10 second-home villages and 4 lodge sites) and the
    same 30 new points, the 13 holiday points lets. Lets fill at the half-term nearly as much as at Christmas;
    second homes fill at Christmas and hardly at the half-term (a winter response of about 3.3 to 3.9 at
    Christmas and 1.3 at the half-term, against about 2.3 to 2.5 and 1.9 to 2.1 for lets), so only the two
    responses together tell them apart.
  - The golden 236, 233 and 238 bins (truth 238, 231, 223); the family -5 to +2, -6 to +2 and -2 to +2 per
    cent of it; one sigma 8.9, 6.2 and 9.3 bins (2.7 to 3.9 per cent); per point a median spread of 2.4, 3.2
    and 3.1 bins needed and up to 4.6 to 7.9.
  - The bracket held in shape: the holiday-looking points pooled +28 to +39 per cent and the top-ratio peers
    +32 to +42 over the golden, the district -44 and the Coast district's ratio borrowed for the lake -31 to
    -33 under it. The rest: every mature point -48 to -52, the nearest 3 points -36 to -49, the distance fit
    -43 to -48, a flat 1.25 -41 to -43, a flat 1.5 +4 to +8, a flat 2.0 +100 to +103, the nearest point -53,
    -15 and -1, the size peers +3, -15 and -33, the half-term alone -1 to +1 (the back-test rejects it at RMS
    0.24 to 0.28, yet it lands on these new points, because none of them is a village or a hamlet).
  - The flat factor crosses the golden at 1.46 to 1.47, so 1.5 sits 4 to 8 per cent over it, inside any bin
    the noise allows.
  - The back-test: 0.057 to 0.065 for the nearest peers on the two responses against 0.35 to 0.36 for the
    district and 0.13 to 0.15 for the pooled holiday points, and on the off-district kinds 0.060 to 0.068
    against 0.62 to 0.64.
  - Determinism at the total: no rounding of 10, 20, 25 or 50 bins holds the family with one sigma inside a
    quarter-bin margin in any seed; inside the golden's bin sit a flat 1.45 to 1.55 at every rounding in
    some seed, the half-term alone at 10, 20 and 50 in every seed, the size peers in seed 1 and the nearest
    point in seed 3.
  - The eda6c8c screens: dispersion does not apply (the within-kind coefficient of variation is 0.022 to 0.040
    for lets and 0.044 to 0.063 for second homes); variance-only passes (1.77 to 1.79 times the district
    route); the common-exposure subset misses by 15 to 53 per cent except the nearest point in seed 3 (-1) and
    the size peers in seed 1 (+3); truncation direction does not apply.
- **The per-point requirement, measured on both.** Whole bins at each point need every defensible member of
  the family within a quarter-bin of the golden at 20 to 30 bins needed, about 1 per cent of the July
  forecast, which would take a within-kind ratio spread near 1 per cent and a weekly noise near 3 per cent:
  lockstep series. At the realistic 2 to 6 per cent and 8 per cent the members spread 2.4 to 3.2 bins.
- **The prototypes before the screen** (`p1.py` to `p11.py`) moved the parameters the same way and found
  the same wall: with the holiday points at 35 to 50 per cent of their bins in winter the totals were 30 to
  100 bins and one sigma 7 to 21 per cent; a beach-car-park kind made the two-response family split 62 to
  165 on one seed because a village's and a beach's winter responses coincide; a lets enclave among
  second-home lures with a mixed coast let the district route land by cancellation (the coast's villages
  over, the lake under).
- **Paper screens, not coded.**
  - The new points' ramp as households find them: FC04's station-maturity driver, task133's seed.
  - Each mature peer's July completed past its capacity from the peers that never overflowed: task168's
    driver.
  - The two Julys normalised for weather: a lever of 8 to 12 per cent on July fill, inside the bin the noise
    needs.
  - The school summer holiday's start: it falls within the same few days of late July in England in 2025,
    2026 and 2027, so no lever.
  - Deposits diverted from nearby mature points: the winter split carries into July, so no lever.
  - Dwellings times a kind's yield per dwelling: determinate per point only if every point captures the same
    share of its catchment, which is lockstep; with capture varying, the point's own winter level beats it
    out of sample.
  - The total July weekly fill in place of bins to add: a flat uplift lands, because the sum runs over the
    residential points too.

- **Redraw screen, 2026-10-19, candidate A: goals as reference points.** An activity-rewards programme raises
  its daily step goal (7,500 to 10,000) and pays a weekly reward for three goal-days (prototype `a_goal.py`,
  seeds 1 to 3, 3,000 members, 26 weeks, 13 forecast weeks). Killed on the library test and the round's G14
  ban. Truth 15,409, 15,150 and 15,762 weekly rewards (sigma 0.33 to 0.35 per cent); the share of weeks with
  three days at the new goal (default) -36.2, -36.3, -35.4 per cent; the current reward rate carried +78, +82,
  +76; the pile at the old goal read over every day (the card-literate route) -12.5, -12.3, -11.3 (stretch 0.44
  to 0.45 against 0.63 to 0.65 on days the reward was still in play, 32 per cent of days dead); the pile read on
  live days -2.4, -1.4, -0.8. The live-day rule leaves the forecast itself unchanged and fixes only the estimate
  of the stretch, an absolute split no column names (pattern E, G14); the band's carriage between two goal
  levels moves about 9 per cent on paper; the pile itself is what a card-literate reader looks for.
- **Candidate E: drift-diffusion speed-accuracy adaptation.** A selection test tightens its per-item limit
  from 10 to 6 seconds, an older 6-second version on another item bank in the record (prototype `e_ddm.py`,
  seeds 1 to 3, 2,000 candidates by 40 items, the 6-second boundary 0.75 of the unhurried one). Killed: at a
  70 per cent cut the truth passes 94.8, 95.4 and 93.8 per cent and truncating the current response times at
  6 seconds lands within 1.3, 0.8 and 1.4 per cent (mean accuracy 0.817 against 0.822: the slow responses
  truncation drops are the low-drift ones, so the totals coincide); only at a cut near the top does truncation
  miss (+26 to +29 per cent at a 0.75 boundary, +105 to +112 at 0.60), and there the lever is the DDM transport
  itself, the field's textbook route, on a tail share carrying 5 per cent relative noise; the old version timed
  out 1.9 to 2.2 per cent, so the censoring a careful fit adds is a negligible lever that card 3 catches.
- **Killed on paper the same day.** Hot-stove learning after an improvement (the card's learning model already
  updates only the chosen option, so the card lands; a lag-1 outcome logit sits near the golden over one
  quarter). Pooling titration answers whose offers followed the respondent's own earlier answers (the field
  scores each respondent's indifference point, which is the golden). Reference-dependent income targeting
  across a gig day (labour economics by taxonomy, as task157 found; a reduced form on own earnings lands;
  under 20 per cent on hours). A screener's criterion moving with prevalence (needs a gold-standard subsample;
  in range a regression on prevalence lands, out of range a fork). Every rate-by-state design carried to a new
  state mix (reference prices, the disposition effect, forgetting by gap, returns after a deferral, projection
  bias, streak breaks: honestly G14 or composition_mix). Notification habituation (task83's driver, rejected in
  task122's note). Peak-end follow-up (recognisable; lever about 24 per cent). Goal-gradient loyalty cards
  (lever about 4 per cent). Compromise and decoy menus (famous; past introductions land). The magnitude effect
  (amount as a covariate lands). Partition dependence in fund menus (the default fund dilutes it;
  identification only across employers). The description-experience gap in fare enforcement (past changes
  land). Bold against timid play under a stake cap (the pile at break-even plus a session simulation is the
  card-literate route, and players' time budgets reopen task148's censored-patience driver). A delivery promise
  as the reference point of learning (under 10 per cent on totals, a product-analytics home). A learner-share
  recruitment forecast (the analysis file's selection is a WHAT; a fatigue bend is G13).
- **F's own dead settings** (`f_forced.py`, `f_forced3.py`). With 1.4 imposed contacts per customer (six weeks
  at a contact a month) no learning lands within 1.4 per cent. With overflow on 6 per cent of contacts,
  redirects are 30 per cent of assistant experiences and the pooled reduced forms (a last-four logistic and a
  first-order Markov chain) cross the truth for imposed-to-chosen ratios of 0.25 to 0.40 (seed 1: -3 and -3 per
  cent at 0.35, -7 and -7 at 0.40); the draw keeps overflow at 2 per cent of calls (redirects about a tenth of
  assistant experiences) and the ratio near a fifth, where every pooled route misses by 10 per cent or more.
- **Stage 2 and 3 settings that moved the call when read another way** (measured on the d1 and d7 packs before the
  world was fixed; prototypes in r177/proto, g2 to g10):
  - Resolution derived from a repeat contact on the same topic within seven days: the contact count then depends on
    the outcome, and contacts simulated at each claimant's 2026 rate against repeats that follow failures moved the
    share about a point. Outcomes are recorded by each system instead.
  - Contacts at a gamma-distributed rate per claimant: each claimant's observed rate put the share 6.7 per cent under
    the truth (new claimants with no contact drop out, and a lucky count weighs a more phone-leaning state). The
    plan's fortnightly check-in fixes the window's contacts.
  - A lean spread across claimants (sd 0.4) and two claim lengths: the population-only fit, the full fit, the
    closures and estimated starting values spread 24.9 to 27.9 per cent. A common lean and one claim length converge
    them.
  - Scale 1.0 (9,000 claims open at the launch, 7,240 transfers): one standard error of the transfer rate moved the
    share 0.53 points and a fit to 31 October 0.55. Scale 1.5 brings them to 0.44 and 0.08.
  - 12 per cent of chat conversations split into sessions: counting every session as a contact moved the share 1.9
    points. At 1 per cent it moves 0.25.
  - Queue abandonment at 4 per cent: dropping abandoned calls moved the share 0.36 points. At 2.5 per cent it moves
    0.33, inside the bin.
  - Eight draws at scale 1.5: the family's farthest member 0.25 to 0.43 points from the golden, the pooled logistic
    1.3 to 2.6 points above it; d7 taken (0.28 and 1.95), the acceptance count then set to 2,041 of 2,400 to centre the
    family in its whole per cent.
  - The vendor first named Conversa Systems Inc., a word from real conversational-assistant firms (house fix H21);
    renamed Riverlot Dialogue Inc. before any reader saw it.
  - The write-up printing the fitted rates (0.398 and 0.078) and the gains to the unit: the transfer rate's estimate is
    0.07850, on the third decimal's rounding edge, the defensible fits put it at 0.077 to 0.079 and the chosen rate at
    0.397 to 0.398, and the teaching-nothing gain is 92.52. The write-up carries what every defensible fit shares (the
    transfers' rate about a fifth of the chosen rate, ratios 0.193 to 0.200; the gain over one rate more than 1,300 on
    the whole record, 1,419 with fixed starting values and 1,383 with them estimated); the workbook keeps the golden's
    own fit at two decimals.
  - Ask B's primary on the re-typed accounts (round 1, target.zip 2c536aaa): one reader collected every account that
    ever appears as staff and counted it staff all year (12 of 12 own-use months), and after the 14 September re-type
    those accounts read as staff anyway, so the other reader kept October to December. Re-sited onto the vendor's
    support desk in the staff console, which moves every month and which neither reader's path reaches; the re-typed
    accounts stay as a hazard.
  - Ask A's clock on the employers' ordinary evenings only (round 1): no employer conversation crossed February's
    boundaries on balance (31 January and 28 February both Saturdays) nor July's (30 June and 31 July crossing in equal
    numbers), and both readers kept those two months with the clock unconverted. Employers' month-end filings now move
    every month; of twelve draws of their own stream (a to l) only k moves every month by 4 or more, and k was taken.
  - The plan silent on release 4.0's resolution outside calls (round 1): the judge read 2.1 as filing the acceptance
    rate for the claimant line only, and the 2026 assistant's rate (0.501) kept for the app and the web files 16. Plan
    1.3 now files the planning assumption for every channel, the voice service's transfers after 1 March included
    (25.98 at the 2026 voice rate, the same call).
  - Ask A's primary on the widget's clock (round 2, target.zip 2c11b94b): both readers converted it ("employer-portal
    timestamps are UTC") and kept 12 of 12 employer months; the month-end filings had made the widget's UTC hour
    profile plain, and at medium effort clock conversion is a reflex. Re-sited onto the widget's day cut, a grain
    judgment the converted path still gets wrong in every month (7 to 25); the clock stays as a hazard.
  - The assistant-first weeks' share as critical component 2 (18 per cent): the golden's family puts it at 18.22 to
    18.32 (18.27 to 18.28 over six seeds, 18.46 with no pull to the last choice, a rejected form), 0.18 to 0.28 of a
    point from the 18.5 edge, and judge pass 2 reproduced 18.8 under its own conventions (pass 1 18.2), so a
    reasonable reproduction prints 19. Dropped from block 2, from step 4 and from the workbook; component 2 is now the
    record's 11,154 transfers among 413,866 contacts, which both judges reproduced exactly.
  - The forecast at a whole per cent (rounds 1 to 3): the golden 26.05 sat 0.45 from its cell's edge, and round 3's
    judge, under conventions the text left open (a check-in's lag, the other contacts' rate, the denominator, a
    transfer moving the phone's value), reproduced 25.8 to 27.9, straddling 26 and 27 (passes 1 and 2 had 26.0 and
    25.7). The prompt now asks the share to the nearest 5 per cent, plan 5.1 files the denominator and the start
    channel, and plan 4.1 the check-in's day; the learner, its rates and the transfers' weighting stay the analyst's.
  - The golden at 26.05 in the 25 cell (round 4, a2c932a3): independent re-implementations ran 0.5 to 1.2 points above
    it every time (26.0, 25.7, 26.4 to 27.2, 26.9 to 27.2), the last 0.3 to 0.6 under the cell's edge. The drift is
    the phone's outcome rate taken over every call (+0.49, now plan 3.3) and the transferred calls' choice left out of
    the likelihood (+0.62, open); the acceptance count went to 2,003 of 2,400 so the open readings sit a point inside.
- **Architecture 1 spent at Gate F (round 5, target.zip 3be16ba3).** The re-judge was DETERMINISTIC and APPROVE, but
  reader I landed the call: "Channel choice is habit-driven (fitted latent habit model: decays 0.63 per contact,
  weights by previous contact outcome; resolved chat strongly raises next chat use, voice resolved raises it modestly,
  abandoned calls push to chat)." and "release 4.0 filed at 83.5 per cent (acceptance) ... Chat share of contacts 1
  Mar-25 Apr = 26.2 per cent, rounded to 25." The lesson: whole per cent failed determinism and nearest 5 admitted an
  outcome-weighted habit model, so the lever between the golden and its neighbours was no wider than the golden
  family's own spread, and a quantity's lever has to clear that spread by a wide margin, measured on an outsider's
  re-implementation at the screen, before any rounding is chosen.
- **Second cell, product-analytics / churn-propensity-uplift-modeling (2026-10-21), candidates that died on paper
  before any prototype.** Each line was written when the candidate was dropped.
- A retention offer that defers rather than saves, graded at a horizon past the test's readout: the decisive step
  settles the outcome's window, a part of the estimand, so filing it is a literal read and leaving it open is a fork;
  extrapolating past the test's follow-up forks the family on the decay's form.
- An offer moved to a channel with higher reach, the test's effect scaled by its exposure (the effect per opened
  offer): the scenario sentence that files the channel change sends every reader to the open rate, and the transport
  of the per-reached effect is an assumption the data do not settle.
- Acceptances of a save offer read as saves against the randomised holdout: the holdout comparison is the uplift
  reflex itself.
- Training labels shaped by an always-on save programme, forecast with the programme switched off: the scenario files
  the switch-off and points at the holdout, a reflex once read.
- Stated intent to cancel after a price rise, calibrated by the last rise's stated-to-actual ratio: a known reflex for
  any forecaster holding both files.
- Discount depth extrapolated past the tested range against a saturating response: the plot shows the plateau, a
  reflex.
- A staggered market rollout read with not-yet-treated comparisons against two-way fixed effects: the textbook
  estimator now, landed by any strong reader.
- Paid account sharing with borrowers converting: the famous real case primes the golden reading.
- Free trials withdrawn so that the no-trial group's meaning changes: the post-change cohort is a mixture whose
  weights and third type (would-be trial leavers) fork the family.
- A promotional cohort's price step-up inside the window: the step-up date is visible and the earlier cohort is the
  analog route blind readers took on task167.
- A second offer to subscribers treated before, read on a re-randomised group: task83's driver (an effect conditioned
  on each unit's own prior treatment history) in other nouns.
- The effect carried on a relative rather than an absolute scale to a list with a higher base risk: task165's gain on
  each unit's own baseline in other nouns, and the scale choice is a coin flip between reflexes.
- Contact harming dormant subscribers (sleeping dogs) concentrated in a new list: email engagement is a standard
  feature, so any two-model uplift with it lands.
- An offer rationed by a monthly redemption cap read as a natural experiment by day of month: the effect is identified
  only with a day-of-month adjustment and a horizon for deferral, two forks.
- A threshold-assigned offer read by regression discontinuity: the bandwidth and order family forks the local effect,
  and a regression with the score as a covariate lands near it.
- Predicted uplift of a model's own top segment shrunk by honest evaluation: the graded figure would depend on each
  reader's model.
- **Second cell, candidate C2 (held at the screen).** The offer's effect by the days from delivery to each
  subscriber's next bill, carried from an anniversary-billed test to a list billed on the 1st: measured on six
  in-memory worlds and a file-only mini-pack with an outsider re-implementation (`## Screen`). One accidental lander
  was found and moved before the card: with the email open rate at 45 per cent, the fortnight's share of the cycle,
  the arms' difference divided by the open rate reproduced the golden (18.3 against 18.0); at 30 per cent it gives 31
  to 33.
- **Architecture 2, ask B on the add-on alone (stage 3, 2026-10-21).** With the invoices one per subscription and the
  Puzzles add-on in the total the only device on November to January, a reader parsing the lines column keeps those
  nine cells (the add-on lines carry their own subscription id), and with the call landed the pair would sit near 52;
  the platform now invoices per account, so a list subscription can be billed on another subscriber's invoice and a
  list account's invoice can carry another plan, which the route through the invoices filed under the list misses in
  every cell.
- **Architecture 2, cells near their edges (stage 3).** The first cut put October Digital 1.40 from its hundred's
  edge and four ask A cells within 15; acceptances by offer-arm subscribers deciding at neither bill (they pay both
  bills either way) and the goodwill credits now re-centre every money cell 30 or more inside, and no row the call
  reads moves (the call 19.88 and the default 9.65 before and after).
- **Architecture 2, the count of subscriptions billed twice for October (stage 2).** Dropped as a figure: it is read
  straight off note 4.1's batches and the credit notes, a seen hazard rather than a device.
- **Architecture 2, round 1 asks (stage 4 on target.zip 4827dc5d).** Both readers counted ask A from the bills: the
  discount lines carry the subscription, so the replaced app ids never mattered (reader B: "legacy DISC lines whose
  applied_ref is an offers-engine acceptance ... Takers = distinct subscriptions with such a discount"). Reader B took
  ask B from the line-level ids: every line names its subscription, so the account grain never bit ("platform invoice
  lines for list subscription ids, plan items only, goodwill credit lines netted, month = UK date of issue"). Reader A
  kept 9 of 21, reader B 21 of 21. Re-sited on the readers' own routes: ask A onto the app acceptances the engine never
  applied, which the app billed at a half-price rate with no discount line, and ask B onto a household's two
  subscriptions billed on one line under the list subscription. Both are measured on the quoted routes in cracker.py.
  The judge's hygiene: the validation summary's list floor is now 0.20, the plan dates last January's send, the
  dictionary says the campaign tool names a list's export by its send day, and the prompt pins credit notes and the
  in-invoice goodwill credits alike (the credit-notes-only reading had moved each cell by 300 to 1,100 pounds).
- **Architecture 2, round 2 asks (stage 4 on target.zip cc5a56de).** Reader D found ask A's rate bills on the bill path
  ("DISC lines with OE26 refs ... plus half-price -MA plan lines (list price minus billed)") and kept all nine; reader C
  kept none. The re-judge found ask B NOT_DETERMINISTIC: no shipped file said what a line's "x 2" meant, and netting a
  credit note by its header against its covered bills was a second, inferred step. Re-sited: ask A onto the
  acceptances applied after the first discounted bill had been raised, booked as credits against the acceptance (every
  quoted route filters the discount lines), with the rate codes filed in the dictionary as a hazard. Ask B's
  convention is filed as Layer 1 (the lines' qty and unit_amount), the credit note's effect in note 4.2, and the legacy
  pull's scope in the dictionary. The device left is the reader's own: summing a line filed under the list
  subscription counts the household's other subscription too.
- **Architecture 2, round 3 asks (stage 4 on target.zip c2789bda), the final pass.** The re-judge was DETERMINISTIC and
  APPROVE (the call at 20, every ask figure reproducing) and reader E filed the call at 10 and kept 0 of 9 on ask A (the
  credits posted against the acceptance held), but it kept all twelve of ask B: "platform invoice lines filed under
  list subscription ids ... one unit per line (qty 2 lines bill a second, non-list subscription)". Filing qty as the
  number of subscriptions a line bills closed the round 2 judge's fork and handed over the device in the same sentence.
  The lesson: an ask device whose determinism needs a filed convention dies when the convention is filed; such a
  device has to be found by an internal inconsistency with no convention to read, or re-sited. Across architecture 2
  the call held in every blind read (readers A to E filed 10; reader F's result was lost in a container restart) and
  the asks never cleared two readers in one round (round 1: 9 and 21 of 21; round 2: 0 and 9; round 3: 12 of 21).
- **Rebuild cell, quantitative-finance / volatility-derivatives-pricing (2026-10-23), candidate G measured on code:
  dealer gamma left by an overwriting programme's short calls.** The world: a fictional index (and, second form, a thin
  single stock) whose largest holder writes one-month calls 2 per cent out of the money at each monthly expiry; the
  dealers who buy them hedge delta, which damps every intraday move by 1/(1 + kappa G), G the calls' dollar gamma
  computed by identity from the holdings and the exchange's settlement volatilities; the programme winds up, so Q1 2027
  carries none of it. Default: HAR, AR(1) or a window mean on the observed realised variance. Golden: kappa from the
  de-damped HAR fit (profile, or within each expiry month), the de-damped series forecast with no programme gamma, the
  overnight variance kept undamped. Prototypes `g1.py` to `g5.py` (scratchpad b177n/proto), output `screen177n.out`
  byte-identical with `screen177n_run2.out` over two runs; seeds 1 to 30 fixed before outcomes. Killed on measurement:
  - index form: the lever is 27 to 35 per cent only at kappa G of 0.47 to 0.66, dealer hedging absorbing a third to two
    fifths of every intraday move, which no index of realistic depth shows; the golden family's own spread (the base
    forecast by HAR in levels or logs, AR(1), one-, two- and five-year means; gamma from the settlement volatility, a
    flat volatility or the trailing realised one; kappa by profile or within-month) is 9.5 to 14.0 per cent at the
    median and 19.8 to 26.5 per cent at worst over 20 seeds; at a vol-of-vol of 0.12 it falls to 3.7 per cent but the
    series is too flat to pass as an equity index; no whole-point rounding holds the family, and the nearest 5 at about
    18 puts the golden half a point from its edge;
  - the attaining subset: HAR on the observed series scaled by the lowest-decile gamma days' mean variance over the
    last two years' lands at a median 1.06 to 1.10 times the golden (0.87 to 1.42), so a crude conditioning on gamma is
    as good as the golden family;
  - single-stock form (base vol 36, overnight share 15 to 30 per cent, kappa G 0.33 to 0.43): lever 18 to 24 per cent
    against a golden spread of 9.5 to 12.2 per cent; the golden family sits in one nearest-10 bin with the whole default
    family below it in only 8 to 14 of 30 seeds, a bin that wide admits a judgmental bump of a third for "the pinning
    stops", and the kappa G of 0.75 a 50 per cent lever needs leaves visible expiry pinning, a cue to the mechanism.
- **The cell's structural finding (2026-10-23).** A volatility-level forecast carries its own model spread (window,
  levels against logs, the speed of mean reversion, the input a correction needs), measured at 5.6 to 14 per cent at the
  median at realistic vol-of-vol, so only a lever near 50 per cent survives any rounding without admitting a judgmental
  bump; the mechanisms that move a volatility that far are identities a textbook executes once the change is read
  (unlevering after a recapitalisation, the cheapest-to-deliver duration after a notional coupon change, a merger's
  exchange ratio, an index rebuilt on new weights), and the one that is not textbook, dealer gamma, gives 20 to 35 per
  cent at plausible strength. The structural quantities that are tight (a hedge ratio from smile dynamics, an overnight
  share, a dampening coefficient) move the graded figure by 5 to 15 per cent.
- **Rebuild cell, paper deaths (2026-10-23), one line each.**
  - Leverage relevered (equity vol as asset vol times assets over equity after a debt-for-equity exchange or a mandatory
    conversion): lever 40 to 100 per cent, but unlevering is the textbook move once the exchange is read, and noticing a
    dated conversion in the debt register is a field reading.
  - Bond future after a notional coupon change (the cheapest-to-deliver flips from the shortest to the longest bond, the
    future's price vol scaling with its duration over the conversion factor): a filed contract mechanic whose effect is
    the textbook cheapest-to-deliver computation, a lever of about 50 per cent against a yield-vol forecast spread near
    10.
  - Power cap after a plant retirement or a flat new load (residual demand shifted hour by hour by identity, the payoff
    through the price and margin curve): the supply-stack model is the field's textbook and the obvious-covariate
    regression, the cap's value rests on a few hundred scarcity hours, and the outage hours are the attaining subset.
  - An index reweighted or a constituent removed (the index variance rebuilt from the constituents): named, so the
    rebuild is the obvious move; a merger inside a capitalisation-weighted index changes nothing.
  - A stale-price index moved to auction or mid-quote closes: task135's nonsynchronous driver, and a replay of the filed
    methodology.
  - A closing auction replacing last-trade closes (the bid-ask bounce removed): the auction's own noise is unobserved,
    so the method forks, and the lever is about 10 per cent on liquid names.
  - Trading hours extended or shortened, a lunch break removed, a night session added: the variance of hours never
    traded is unobserved.
  - The Samuelson effect for a contract near delivery: a scheduled date, and the textbook term structure of volatility.
  - Minimum-variance delta from smile dynamics (the hedge read from the history of fixed-strike volatility against the
    index): tight, but the adjustment is 5 to 15 per cent of the Black-Scholes delta for single options, and a book
    netted to enlarge it is built for the lever.
  - A forward-start put or cliquet under a stationary moneyness skew: the naive route (today's three-month 90 per cent
    volatility) is the sticky-moneyness golden, and with an inverted term structure the golden is forward variance plus
    today's skew, the sophisticated reader's natural route.
  - Reserve scarcity and the overnight rate (reserves drained by identity, the spread through the reserve demand curve):
    days at the forward reserve level are the attaining subset, and a level below the record's forks on extrapolation.
  - Securities lending after an index deletion (the index funds' lendable supply leaves by identity, the fee through the
    utilisation curve): the fee is not a volatility, and the utilisation curve is the field's textbook.
  - A consumer price basket reweighted for an inflation swap fixing (seasonal factors re-aggregated on the new
    weights): a filed mechanic replayed on the component history, and the inflation desk's textbook.
  - Mortgage prepayment on each loan's own refinancing incentive: task171's driver (each unit's own saving) in
    mortgage nouns.
  - CVA with wrong-way risk: the hazard's response to the risk driver is a fitted behaviour whose copula forks, on a
    simulated figure.
  - Weather (degree-day) contracts after a settlement station or daily-mean definition change: the new station's
    history is the attaining subset, and the definition change a replay of the filed rule.
  - Barrier notes monitored on auction closes (observation noise lowers the minimum of the closes): a lever of 10 to 15
    per cent on thin stocks and none on an index.

- **Rebuild cell, biomedical-clinical-research / survival-time-to-event-analysis (2026-10-23), candidate H1 measured
  on code: the hazard on the time since each member's last discharge, with a December admission surge putting a
  large share of a heart failure registry's members days from a discharge at the forecast date** (deaths in the first
  quarter among members alive on 1 January, registry entry at the index discharge, a gamma frailty, a post-discharge
  death multiplier decaying over 30 days, admissions seasonal and raised by an outbreak in the last six weeks of the
  year; `h1.py`, scratchpad b177s/proto, byte-identical over two runs). Killed on the lever. At realistic strength (an
  outbreak at 2.5 times the usual admission rate, a sixfold excess just after discharge; 30,748 members, truth 1,225
  deaths) the duration curve times the history's first-quarter share lands at +0.6 per cent, the mean first-quarter
  rate of 2018 to 2026 at +1.0, and the golden family (tsd bands fine or coarse, monthly, quarterly or January
  landmarks) spreads -3.8 to +4.9. At strengths no registry shows (fivefold outbreak, tenfold excess) the best
  reflex is still only -6.3 per cent (an admission in the last 90 days at -8.8, in the last 30 days at -1.0, inside
  the golden family of -2.3 to +4.4). The surge's new entrants carry the duration curve, the season ratio carries the
  rest, and the last-30-days indicator is the golden.
- **Candidate A1 measured on code: graft failure on the recipient's attained age (a peak through ages 17 to 24) times
  a duration curve, failures over three years among a paediatric programme's functioning grafts** (4,750 to 12,613
  grafts, `a1.py`, byte-identical over two runs). Killed with no lever at all: the duration-only route lands at +0.8
  to +9.5 per cent, stratifying by age at transplant at +0.8 to +10.0, a proportional age term at +0.7 to +8.9, against
  the attained-age golden at -2.7 to +6.1. Attained age is age at transplant plus duration, and a stationary
  programme's at-risk mix over the window is the history's, so every route absorbs the clock (task174's finding,
  measured once more).
- **Rebuild cell, paper deaths (2026-10-23), one line each.**
  - Starts moved to the discharge day (a new initiation practice puts a drug's new starters days from a discharge,
    where the history's started at stable visits; the new-user curve the default): the cohort already started is the
    time-axis attaining subset, its observed first 45 days carrying about four fifths of the excess at a 30-day decay,
    and a cohort wholly in the future needs the practice change stated, which names the step.
  - Selection on a marker taken in an acute state (an in-hospital eGFR flagging patients for a kidney programme, the
    hazard on the steady-state level): regression to the mean is absorbed whenever the record's model conditions on
    the same kind of measurement, and where it is a different kind the call flips on reading what the value is (rule
    3, semantics).
  - Postmenstrual age in a neonatal network (onset on gestation at birth plus age): the same identity as A1, and
    stratifying by gestation is the first reflex.
  - The healthy-volunteer effect wearing off in a biobank cohort: 10 to 17 per cent at most on attained-age bands.
  - A case-cohort biomarker sample read as a cohort: the sampling design is a filed protocol fact, so weighting is
    rule application, and leaving it unfiled is a planted omission.
  - Lead time from earlier diagnosis (screening, a rapid-access clinic): the new route's survival needs a
    natural-history model that forks, and the recorded diagnostic delay is the shipped proxy.
  - Stage migration after a staging technology change (Will Rogers): the overall curve ignoring stage is both the
    reflex and the golden.
  - A learning curve at new implanting centres: earlier centres' first cases are the attaining subset, the premise
    names the new centres, and the swap test reads the same with new call-centre agents.
  - Transplant hazard rationed by a flat donor supply while the list grows: a medium reader names the supply, and a
    limit does not measure itself.
  - Infection on a ward's colonisation pressure under an occupancy change: mass action against frequency dependence
    forks the scaling.
  - Timing modifiers carried from a trial (onset to treatment, time since menopause, time since injury, symptom onset
    to an antiviral, surgery to adjuvant start): each is the field's best-known modifier and the forward change names
    it.
  - A run-in's exclusions carried to routine starters: the run-in log names the excluded, and the carry also needs a
    covariate reweighting that forks.
  - Relapse against reinfection after cure, carried to a lower-transmission district: genotype correction is the
    field's standard, and without it the split by timing is a free-form mixture fit.
  - Imminent re-fracture clustering read as a Poisson rate: time to first event is directly in the record.
  - Clinicians having treated the patients who gain most, a forward rule treating all: needs an instrument, and the
    instrument forks.
  - A hazard ratio among survivors attenuated by frailty, carried to late switchers: needs a frailty law, which forks.
  - Deferred deaths through exits removed as too sick, under a forward delisting rule: task169's driver in clinical
    nouns.
  - An effect landing before a recurring clinical session (the long dialysis gap, a refill due date): architecture 2's
    own driver.
  - Distance to the centre as the omitted covariate: a backdrop, the swap test reads the same.
- **The cell's finding, measured twice more.** Over a clinical record of realistic size, any clock the hazard runs on
  is absorbed by the duration curve with a season term when the population is stationary (A1: every route inside the
  golden family), and after a synchronising event that moves the population off the history's mix the duration
  curve times the season share stays within 0.6 to 6.3 per cent of the golden, even at strengths beyond any registry
  (H1), because new entrants carry the duration curve and the season carries the calendar. A lever of 30 per cent needs a forward change, and in this cell each forward change
  either names its step, closes a competing route (task169) or is architecture 2's driver.
- **Third rebuild cell, banking-credit-financial-risk / credit-scoring-pd-modeling (2026-10-23), candidate R4 measured
  on code: internal-rating momentum after a sector shock.** A business book's grades read a latent credit quality
  with review lags; a 2026 shock pushes a fifth of the book into deteriorating states, and the textbook route is the
  per-grade (Markov) PD on the 31 December grades. Prototype `b177c/proto/r4.py` (12,000 obligors, 2014 to 2026,
  annual and triggered reviews, noise 0.15 to 0.25, steps capped at 1, 2 or 9 notches): the truth sits 18 to 24 per
  cent above the per-grade PD, but every grade-by-recency-of-downgrade route (6, 12, 18, 24 months, three bins)
  moves the forecast by 0.1 to 2.3 per cent, because the shock's deterioration is mostly not yet rated and the
  history's recent downgrades are mostly noise; the latest year's per-grade rates land within -5 to +9 per cent.
  Dead: the golden is not identified from the records, and the PIT reflex beats it.
- **Candidate S1 measured on code: rating staleness under a review backlog.** The grade is a reading at the last
  review and PD is convex in the latent quality, so a backlog leaves the book's grades stale. Prototype
  `b177c/proto/s1.py` (backlogs of 60 and 90 per cent of scheduled reviews from June 2026, triggered reviews at 20
  and 50 per cent): grade-by-review-age routes move the forecast -1 to -7 per cent (the wrong way, survivors of
  stale grades are the ones no trigger caught), the truth is 8 to 10 per cent over the per-grade PD, and the
  history's support beyond 12 months since review is 0.1 per cent of obligor-years. Dead.
- **Third cell, paper deaths (2026-10-23), one line each.** Trade-link contagion after a large customer fails (the
  payroll-client-leaving death in task179's note by abstraction, and sized from a single event); payroll-deduction
  default read off reason codes that name the separation (the decomposition is then read off a column); fresh
  against chronic arrears in a roll-rate forecast (featurisable: months delinquent in the last twelve is a standard
  behavioural characteristic); top-up chains as one exposure (identity); a first-payment deferral clock (obvious
  from the terms); due date against payday (task177 v2's own driver by abstraction); payment protection insurance,
  guarantor payments, sold-before-default and portability of payroll loans (each a route closure, task169's
  driver); a cladding or flood-map designation (a filed rule and a join); fixed-rate resets and promotional-rate
  expiry (task137 and task166 ground, a behavioural slope, and the expiry is a column); a credit amnesty deleting
  bureau records (identified only from a single past event); income verification (task192's audit-subsample
  driver); distance to branch in a mobile expansion (the forward population's defining feature names the
  covariate).

## Retired

Retired on 2026-10-22 under the author's rule for the final ask pass (if round 3 still fails, the number retires).
Two architectures were built to stage 4, after the seed's own world (FC48, drop-off recycling bins) died at stage 1 on
measurement before any card.

- **Architecture 1, psychology-behavioral-science / decision-making-computational-behavioral-modeling: the two-rate
  learner.** A provincial employment service's share of jobseekers' own contacts its upgraded assistant would take in
  March and April 2027, after eight assistant-first weeks. The decisive step was a separate learning rate for the
  contacts a jobseeker did not choose (the overflow transfers), fitted jointly and carried through weeks made of
  imposed contacts. Five rounds re-sited the asks twice and moved the forecast to the nearest 5 per cent. It was spent
  at Gate F on target.zip 3be16ba3: the round 5 re-judge was DETERMINISTIC and APPROVE, but scored reader I landed the
  25 bin with an outcome-weighted habit model that never separated the imposed contacts. Lesson: the lever between the
  golden and its neighbours was no wider than the golden family's own spread.
- **Architecture 2, product-analytics / churn-propensity-uplift-modeling: the churn uplift by the days to the next
  bill.** The share of Daily Lantern Media's 26 January 2027 at-risk list kept to 31 March 2027 by a half-price offer,
  forecast from last January's randomised test. The offer worked only when it landed in the fortnight before a
  subscriber's next bill, and every bill on this year's list falls six days after the send, so the answer is 20 per
  cent against the test's whole-list 10. The call held: every blind reader (A to E) filed 10, and the round 1 and
  round 3 judges were DETERMINISTIC (round 3 APPROVE, the call's 95 per cent half-width about 0.7 points). The asks
  never cleared two readers in one round across three rounds, and the author's final pass failed on ask B (reader E,
  12 of 21).

The lesson the number leaves: an ask device whose determinism needs a filed convention dies when the convention is
filed. Ask B's household line could only be made determinate by saying in the dictionary what a line's quantity counts,
and the same sentence told the reader how to handle it. A device must be found by an internal inconsistency that a
grader can verify without a convention, or the ask must be re-sited before the judge sees it.

The card stays filed with `architecture_spent` set; both architectures are in its lineage. Three ask devices held
against scored readers and are kept here as reusable records:

- **Device record, the vendor's support desk (architecture 1, ask B).** A vendor's support staff work inside the
  customer's tenant under accounts typed staff, like the customer's own. The customer's carry its business number in
  org_ref; the desk's carry the vendor's, which appears only as the supplier's tax number on the vendor's invoices.
  Counting staff by type puts the vendor's desk into the customer's own use in every month. Measured: the round 3 and
  round 4 readers kept 0 of 12 each.
- **Device record, the widget's day cut (architecture 1, ask A).** An integration partner's widget partitions its log
  by UTC day: a session still open at 00:00:00 UTC is closed there as a timeout and carries on at that second as a new
  conversation id from the same account, so a conversation reaches the export twice. Fair, because a timeout means 30
  idle minutes and no other two sessions meet at a second. Measured: the round 3 and round 4 readers kept 0 of 12 each.
- **Device record, the offer's half price posted as credits (architecture 2, ask A, round 3).** An engine that
  applied an acceptance only after the subscription's first discounted bill had been raised has billing post the half
  price on both bills as credit lines (CRED) carrying the offer's code and the acceptance's own reference, with no
  discount line. Every reader that counts the offer from the discount lines misses those subscriptions in every month,
  plan and takers count. Fair, because each credit is exactly half the subscription's own charge, against its own
  acceptance. Measured: reader E kept 0 of 9; on reader D's round 2 route every discount cell is low by 954 to 2,505
  pounds.

## Rebuild (2026-10-23)

Reopened under the author's rule that no number stays retired, for a from-scratch rebuild in quantitative-finance /
volatility-derivatives-pricing (Forecasting), worktree `b_177n`. No candidate held at stage 1: candidate G (dealer gamma
from an overwriting programme) measured dead on code in three forms and seventeen more directions dead on paper, all in
`## Tried and rejected` with the cell's structural finding. No card registered (the card's lineage already carries both
spent architectures), nothing cut; PAUSED at stage 1 for the coordinator to assign another cell.

Second rebuild cell the same day, biomedical-clinical-research / survival-time-to-event-analysis (Forecasting),
worktree `b_177n` on origin/main 682b11dd, with task171's and task174's deaths in this task type read first and the
field's corrections (Kaplan-Meier, Aalen-Johansen, delayed entry, landmarks, new-user curves) taken as the default path.
Two candidates measured on code (H1, the time since the last discharge after an admission surge; A1, attained age) and
nineteen on paper, all in `## Tried and rejected` with the cell's finding. No card registered, nothing cut; PAUSED at
stage 1 again for the coordinator to assign another cell.

Third rebuild cell the same day, banking-credit-financial-risk / credit-scoring-pd-modeling (Forecasting), worktree
`b_177n` on origin/main e7f776e4. Two candidates measured dead on code (R4 rating momentum, S1 rating staleness) and
fourteen directions on paper (`## Tried and rejected`); candidate P held at the screen and carries architecture 3
(`## Draw`, `## Screen`): the first-year default of payroll-deduction loans read per exit from the employer's payroll,
carried from a public-servant book to private employers whose own salary batches show their staff leaving five to
six times as often. The card's v2 identity is already in its lineage; v3 registered on the filing day.

## Resume

Architecture 3 drawn 2026-10-23 (stage 1 complete at registration); resume at stage 2 (design: readability screen,
fork table, ladder, closure, asks, prompt; gate precut.py) from `## Draw`, `## Screen` and `## Default path`.
