# task171 design note

**Status: PAUSED, architecture 3 spent at Gate F on ce04ed65 (stage 4, 2026-10-23); the number stays open and the next cell is screened under `## Rebuild (2026-10-23)`.**
The cell is economics-econometrics / discrete-choice-limited-dependent-variable-modeling; the draw is an electric
cooperative's optional overnight rate. The earlier screens are kept below as history under `## Earlier screens`.

## Draw

- **Cell.** Client domain Economics & Econometrics, task type `discrete-choice-limited-dependent-variable-modeling`
  (serves Forecasting). Objective Forecasting: the call is how many of the cooperative's standard-rate members will
  have moved to the optional overnight rate by the end of each quarter of 2027, and the annual revenue those members
  give up, a window not yet open, pinned by the record of the optional evening-peak rate offered from March 2024.
- **World.** Sablewood Electric Cooperative, a fictional member-owned rural distribution cooperative in a fictional
  two-county service territory in the United States (its people, systems and records are fictional; the field's
  method is real). Residential members on the standard rate R-1 were offered the optional evening-peak rate R-TOU
  (4 to 9 p.m. peak) from 1 March 2024; R-TOU closes to new members on 31 December 2026 and the optional overnight
  rate R-ON (11 p.m. to 6 a.m. off-peak) opens to R-1 members on 1 January 2027, marketed the way R-TOU was. The
  manager of rates and pricing files the 2027 enrolment and revenue forecast with the board's rates committee for the
  2027 budget. Records to billing month October 2026: the AMI load-research export (meter by billing month by
  load-research period), member and account records with rate history, the CRM's rate-change requests, meter
  exchanges, the rate schedules, billing summaries.
- **Card.** `domain` economics-econometrics, `subdomain` discrete-choice-limited-dependent-variable-modeling,
  `objective` forecasting, `shape` 02, `decision_type` quantity_figure, `answer_unit` count, `gap` [time, population],
  `pattern` [E], `generators` [G14, G3, G13], `gate_g` forecasting, `calibration_form` existing_book_actuals,
  `stump_strategy` forecast_method_backtest, `context_artifact` planning_thread, `role_family` product_manager, `forum`
  committee_or_panel, `forcing_event` launch_or_rollout, `org_family` cooperative_or_member_body; `stump_class`
  analytical; `layer2_family` estimand_identification; `layer2_pattern`
  own:optional-rate-take-up-priced-on-each-members-own-pre-offer-saving. People from `guard.py names --geo "United
  States" --seed 171`: Wendy Morris, Bryan Castro.
- **Axes, and why each value is the honest one.** The last three live cards (task273, task169, task478) hold
  regulator_or_inspector, council_or_assembly and board_of_directors, vote_or_meeting, budget_or_appropriation and
  purchase_order_or_contract, and government_agency, research_or_statistics_office and local_government. A
  cooperative's rates are set by its own board on its rates committee's recommendation (committee_or_panel), the
  forecast is forced by the overnight rate opening on 1 January 2027 (launch_or_rollout), and the organisation is a
  member body (cooperative_or_member_body). The decisive gap is time (the evidence is the evening rate's first year
  on the use members had before it was offered; the bet is the overnight rate's first year on 2026 use), which is
  also what cleared test.same_driver against task177 (population first).
- **Redrawn under the registration lock.** task175 filed composition_mix and finance_controller minutes before
  this card. The strategy is now forecast_method_backtest, and it is the honester key: `strategies.md` F6 is a pooled
  yield carried onto a moved base failing forward because the rate is stationary only in a constructed exposure,
  which is this draw exactly (the evening rate's take-up is stationary across rate designs only as a response to
  each member's own dollar saving on the use it chose on, rebuilt from the meter log, and the pooled take-up carried
  onto the overnight rate fails). The role is product_manager: the manager of rate products owns the optional rates
  the way a product manager owns a product line.
- **Guard.** `guard.py check` WARN only: repeat.gate_g and overuse.gate_g (the objective is Forecasting and the
  forecast itself carries the call, so `forecasting` is the honest mechanism); repeat.decision and
  repeat.question_form against task175 (the call is a count of members and a dollar figure, so quantity_figure and
  how-many are what the decision is). The older same-puzzle and same-driver
  signatures (task117, task137, task155, task166, task37, task44, task97, task481) carry one differentiation line
  each on the card. `slots` on the mechanism's words and on the setting's (tariff, optional rate, take-up, enrol,
  time-of-use, meter) found no earlier screen of an optional rate's take-up.
- **Strategy.** forecast_method_backtest: the members who take an optional rate are the members it pays, so a pooled
  take-up carried from the evening rate onto the overnight rate fails forward; the invariant is the take-up response
  to each member's own dollar saving, constructed from the meter log on the use each member chose on.
- **Data-native sentence.** In Sablewood's record a member took the evening rate by what that rate would have saved
  it on its own use in the year before the offer, and once on the rate it moved use out of 4 to 9 p.m., so the meter
  data after March 2024 show the evening rate's members cheaper on it than the saving they chose on; only the twelve
  billing months to February 2024 show the saving the choice was made against, and the overnight rate pays a
  different set of members (overnight-heavy, not evening-light) than the evening rate's takers.
- **Sources read, and how this differs.**
  - `layer2-rigor-patterns.md` discrete-choice 1 (willingness to pay as a coefficient ratio), 2 (IIA and nesting for a
    close new alternative), 3 (scale across samples): none is the decisive step; R-ON is not offered beside R-TOU, so
    no substitution pattern decides, and the saving enters in dollars on one sample.
  - task155 (this cell, shipped): a casual's acceptance of a call-in priced on its position against the casual's own
    rostered shift. Here the choice is an optional rate priced on the member's own bill saving, and the decisive read
    is which year of use the earlier rate's response is measured on.
  - task137 (composition at a repricing, two classes rebuilt from entry cohorts), task177 (an effect conditioned on
    days to each unit's own decision), task165 (a gain conditioned on own baseline): each conditions a measured rate
    on a property rebuilt from history; here the property is a bill saving priced from metered use, and the
    history's later use is contaminated by the earlier rate itself.
- **Screens run as code** (scratch `b171n/proto/tou3.py`, `tou4.py`; 40,000 members, three seeds per setting): the
  golden family (logit, logit with household covariates, probit, 25 saving bins, logit with consumption, a monthly
  discrete-time hazard) agrees within 0 to 3 per cent on the year-end count and within -2 to +6 per cent on the
  shortfall, with seed sigma about 1 per cent; the rivals measured against the golden logit (count / shortfall):
  the evening rate's first-year take-up at the average member's change +14 to +18 / -103 to -105; its cumulative
  take-up +41 to +45 / -104 to -106; its takers' overnight change carried +14 to +18 / +32 to +69; savers only +14 to
  +18 / +11 to +46; the take-up response read on 2026 use -56 to -58 / -26 to -34; read on the average of pre-offer
  and 2026 use -35 to -39 / -4 to +3; consumption and evening share as covariates -5 to +3 / -26 to -30; the saving in
  per cent of the bill +3 / -10 to -12 (rejected by the likelihood); the cumulative take-up on the right saving +23 to
  +27 / +3 to +10. Every rival misses at least one of the two figures by 10 per cent or more.

- **Stage 3 record.** `checks.py` 76 of 76, `verify.py` 0 problems, two byte-identical builds, `figures_check.py` 41 of
  41, `precut.py` exit 0, `voice-check.py` PASS, `leak.py` REVIEW with four lines, each answered: the committee paper
  carries the call's nouns because it is the request, without a figure; the schedules use "evening", "member",
  "optional" and "record" as a tariff does; the service accounts and the billing summary name the districts beside
  counts and rank nothing. `guard.py surface`: no persona pair; fifteen promoted pairs on axis collisions only (the
  neighbouring numbers' gap and decision type, task167's pattern E and one shared column set), for the author's
  adjudicated read if wanted. `guard.py heart` WARN only. Pair ceiling 29.6 by `generator/cracker.py`.

## Default path

The strong analyst's route, every field read and every filed rule applied (the field's textbook for an optional
rate's take-up: a binary choice on the member's own bill saving, fitted on the earlier rate and applied to the new one):

1. Reads the committee paper (RC-26-19) for the population (R-1 services on the books at October 31, 2026 billed
   for all twelve test-year months: 21,490), the outcome (R-ON in effect by December 31, 2027) and the revenue basis
   (R-1 bill less R-ON bill on the 2027 schedules at test-year use, counted in full).
2. Reads the rate schedules for the R-1, R-TOU and R-ON prices and the load-research periods, and the CIS rate
   assignments for R-TOU's first year: 2,017 of the 25,559 R-1 services open on March 1, 2024 had R-TOU in effect by
   the February 2025 read.
3. Prices every service's bill on R-1 and on R-TOU from the load-research extract, on its latest twelve billing months
   (November 2025 to October 2026), and fits the first-year take-up on that saving (logit, or a monthly hazard).
4. Prices every population service's R-1 and R-ON bills on the same twelve months and runs the overnight-rate savings
   through the fitted take-up.
5. Sums the probabilities and the probability-weighted savings.

**Ends on:** 1,000 services and $100,000 (991 services and $109,934 unrounded; the hazard form 1,092 and $85,306,
1,000 and $75,000).
**Golden:** 2,250 services and $200,000 (2,213.3 and $195,499 unrounded), with the evening rate's saving read on
each service's use in the twelve billing months before the offer (March 2023 to February 2024).

## Stump sentence

A competent solver fits the evening-peak rate's first-year take-up on each service's saving under it, read on the
latest twelve billing months, runs the overnight-rate savings through it and files 1,000 services and $100,000;
the step that lands it there is reading the saving on use the evening rate's takers had already changed by taking
it (their 4 p.m. to 9 p.m. share fell from 0.244 to 0.208 after joining while everyone else's held at 0.280), when
they chose on the use of the year before the offer, so the response comes out flat and the takers look like members
the rate barely paid.

## Three rules

- Task type: discrete-choice-limited-dependent-variable-modeling (Economics & Econometrics; serves Forecasting & Predictive Modeling).
- Domain test: the deciding quantity is each eligible service's probability of taking an optional rate within its first year, a binary choice whose price term is the service's own bill saving on the use it could see, estimated as a discrete-time logit hazard on the 2024 evening rate's first year and aggregated over the 2026 population; the revenue figure is the covariance of that probability with the saving.
- Swap: "which services will take an optional overnight rate, and what will it cost" read with hospital beds or school places for kWh has no member pricing its own alternative on its own bill and no record of who took the earlier option, so the choice model has nothing to price and the call stops making sense.
- Layer 1: the meter data management system's load-research extract splits a read period across two meter rows at an exchange (the 2025 firmware programme, failed meters) and marks some reads estimated; a move-in starts a new service account at the same meter; the CIS export writes service dates as MM/DD/YYYY; the TOU enrolment module writes the R-TOU rate rows, re-issues them at the January 2026 price change and is not end-dated by the account-closure batch; the MDM re-collects an estimated month for a current R-TOU meter and keeps both rows; the CRM stamps times in UTC, keeps duplicate web submissions as closed cases, and keys a web request to the member's first service; the billing MIS reports by issuing office, Pike Ridge's bills issued from Brisco Bend since July 2025. None is placed to be caught, and none moves the call (checks.py R2 and SEP).
- Layer 2: estimand_identification, own pattern: the take-up response that carries from one optional rate to another is the response to the saving on the use the member chose on, and the earlier rate's takers changed that use by taking it.
- Decisive step: read the evening rate's take-up against each service's saving on the twelve billing months before the March 2024 offer, not on later use the rate itself changed, and carry that response to the overnight rate's savings on test-year use.
- Not semantics: every field, period, price, rate row and date read correctly still leaves the analyst choosing which year of use prices the evening rate's saving, and the latest year, which the extract holds for every service and which the forecast's own revenue uses, files 1,000 and $100,000.
- Not rule application: no filed rule says which use a take-up response is read on or that members respond to their own saving; executing the paper's population, outcome and revenue sentences and the tariff's prices leaves the take-up model open, whose standing family (monthly hazard, 12-month logit and probit, 20 and 40 saving bins, with consumption or district, closed services counted as declining) spreads 4.8 per cent on services and 2.7 per cent on dollars and lands one printed cell, while the enumerated family including the latest-use and all-years readings spreads 991 to 2,298 services; the ruling-out is the record's own shift (takers' evening share 0.244 to 0.208, others 0.281 to 0.280), visible only by comparing a service's years.
- Analyst test: a strong analyst who prices every bill correctly and fits take-up on each service's own saving, read on the latest twelve billing months, files 1,000 services and $100,000 against the golden's 2,250 and $200,000.
- Estimand: the committee paper RC-26-19 files the population (R-1 services on the books at October 31, 2026 billed for all twelve billing months November 2025 to October 2026, none closing), the outcome (R-ON in effect on December 31, 2027), the revenue (R-1 bill less R-ON bill on the 2027 schedules at test-year use, counted in full), and the prompt files the rounding.
- No decoy: nothing is planted; no memo, draft, briefing or stakeholder figure carries a wrong count or shortfall; the shift in the takers' use is what an evening time-of-use rate does and is never stated.
- No certified replay: no published or certified figure is reproduced to recover a method; the evening rate's first-year take-up is read from the CIS rows and the extract, and no shipped file prints a take-up or a saving.
- Lesson: an earlier option's takers are its outcome as well as its evidence; a response measured after they took it is a response to the option's own effect, and the record shows the before only in the year before the offer. No build on file reads a choice response on pre-treatment covariates beside a post-treatment record of the same units.

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 the evening rate's first-year take-up at the average member's change (1,750, $50,000) | no | no | yes | no | no | yes | readable |
| 1 the takers' own overnight change carried, or savers only (1,750, $175,000 or $75,000) | no | no | yes | no | no | yes | readable |
| 2 take-up on consumption and evening share (1,750, $75,000); on all years' use (1,500, $175,000) | no | no | yes | no | no | no | readable |
| 3 take-up on own saving read on the latest twelve months (1,000, $100,000) | no | no | yes | no | no | no | readable |
| 4 (decisive) the saving read on the year before the offer (2,250, $200,000) | no: no sentence names a year of use for the response or says members' use changed | no: the extract carries every month alike, no flag on the takers | no: the reflex is the latest year, which the forecast's own revenue uses | no: no control ties only under the pre-offer year | no: the battery finds nothing, the rows are clean | no: a fitted response, not a ratio | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | R-1 services at October 31, 2026 | active, R-1 in effect, billed all twelve test-year months | active and not on R-TOU | same call (21,490 both) | asserted equal |
| SF2 | moved by December 31, 2027 | R-ON in effect at a read on or before December 31 | a request received by then | not observable | the paper: "R-ON is in effect for it on that date" |
| SF3 | none closing | the population as it stands | a closure hazard applied | about 4 per cent fewer | the paper: "no service is counted as closing or opening" |
| SF4 | revenue they give up | the full twelve test-year months, whatever month of 2027 | months on R-ON in 2027 only | a lower bin | the paper: "counted in full whatever month of 2027 the service moves" |
| SF5 | test-year use | billing months November 2025 to October 2026 | calendar 2026 | incomplete at the as-of | the paper names the billing months |
| SF6 | the cohort's part-year services | kept on their months | left out of the fit | same call (asserted) | records converge; annualising them is rejected by the likelihood (SF6b) |
| SF7 | customer charges | equal on R-1 and R-ON in 2027 | a fixed term | none | the schedules |
| SF8 | services against members | service accounts | membership numbers | same call (asserted) | the prompt counts services |
| SF9 | expected against likely count | the expected number | the median of draws | same call (asserted) | records converge |
| SF10 | rounding | nearest 250 services, nearest $25,000 | finer | n/a | the prompt |

## Ladder

| Rung | Route | Services | Revenue | Printed | Dies to |
|---|---|---|---|---|---|
| 0 | first-year rate times the population, average change | 1,729 | $39,577 | 1,750, $50,000 | the takers' saving (enrollees saved, the average member does not) |
| 0b | cumulative R-TOU share to October 2026 | 1,995 | $45,668 | 2,000, $50,000 | the first-year window and the takers' saving |
| 1 | takers' profile carried | 1,729 | $170,211 | 1,750, $175,000 | the overnight rate pays different members |
| 1b | savers only at the first-year rate | 1,729 | $79,945 | 1,750, $75,000 | take-up rises with the saving |
| 2 | consumption and evening share as covariates | 1,636 | $81,742 | 1,750, $75,000 | the covariates do not price the overnight rate |
| 2b | saving in per cent of the bill | 1,997 | $134,778 | 2,000, $125,000 | dollars fit by 40 log-likelihood units and more |
| 2c | saving on all years' use | 1,411 | $163,500 | 1,500, $175,000 | half the years are after the change |
| 3 | saving on the latest twelve months (logit; hazard 1,092 and $85,306) | 991 | $109,934 | 1,000, $100,000 | the takers changed that use |
| 4 | saving on the year before the offer (golden) | 2,213.3 | $195,499 | 2,250, $200,000 | |

Margins: the golden family (eight forms) sits in one printed cell on both figures, 68 services and $6,155 from the
nearest edge at its tightest member; every rival misses both printed figures, the nearest by one 250 cell (per cent,
cumulative) and two $25,000 cells. Worth: rung 3 to the golden moves services 2.2x and revenue 1.8x.

## Closure table

| Axis | Name | Reading | Closure |
|---|---|---|---|
| 1 | Population | R-1 services at Oct 31 2026, billed all twelve test-year months, none closing | filed in RC-26-19; SF1 asserted |
| 2 | Unit of account | service account | the prompt says services; SF8 same call |
| 3 | Attribution window | R-ON in effect by Dec 31 2027 | filed; reads in 2027 |
| 4 | As-of dating | rate in effect at Oct 31 2026; extract to billing month Oct 2026 | filed; C1 |
| 5 | Version basis | 2027 schedules for the forecast, 2024 for the evening rate's offer | the schedules' effective dates |
| 6 | Denominator | expected services among the population | filed population |
| 7 | Weighting | each service once | C1 |
| 8 | Window length | twelve billing months each side | filed for the test year; the offer year by the schedules |
| 9 | Boundary inclusivity | in effect on Dec 31 2027 inclusive | filed |
| 10 | Rounding path | sum unrounded, round once | the prompt |
| 11 | Tie-break | none needed | C1 |
| 12 | Maturity and censoring | closures before a read leave the risk set | the record's service ends; family converges |
| 13 | Order of operations | price bills, then take-up, then sum | C1 |
| 14 | Row order | none matters | C1 |
| 15 | Duplicate resolution | re-collected reads only on current R-TOU meters, outside the call's rows | SEP asserted |
| 16 | Identity normalisation | service account throughout | dictionary |
| 17 | Netting against gross | savings net per service, negative savers kept | filed revenue sentence |
| 18 | Dimensional units | kWh and dollars per kWh | the schedules and dictionary |
| 19 | Code and status semantics | R-1, R-TOU codes; Active and Final | dictionary |
| 20 | Integerisation | the expected count is not integerised before rounding | C1 |
| 21 | Clause scope | the paper's sentences govern the call; the tables' sentences the tables | the paper's headings |
| 22 | Forward window contents | R-ON marketed the way R-TOU was | filed in RC-26-19 |

## Literal reader

Executed word for word, the paper's population, outcome and revenue sentences and the schedules' prices fix every
input of the golden's quantity, and every literal reading of them (SF1 to SF10) lands the same call or is ruled out
by a quoted sentence; the easy answer comes from the easy method (the latest year's saving) on the same literal
estimand, never from another reading.

## Oracles

None tie only under the golden. The billing summary by office is a residential total of every schedule, matched by
both the golden and the default path alike; the CRM ties the evening rate's completed enrolments to the rate rows
under every reading; no shipped figure prints a take-up, a saving or a forecast.

## Ask sheet

**Main call's declared row population:** the extract's rows for the 25,559 cohort services in billing months March
2023 to February 2024 and for the 21,490 population services in November 2025 to October 2026; the CIS R-1 rows in
effect on March 1, 2024 and October 31, 2026 and the cohort's first R-TOU starts; service starts and ends. Device and
hazard rows in it: 0 (`checks.py` SEP: no re-collected read in the cohort's year before the offer or on a population
service; no open R-TOU row of a closed service in the population; every re-issued R-TOU row starts after the June 2025
upgrade, after the cohort's first year; first-year joins read the same from rows or spells; the call never reads the
CRM).

**Ask A. For the services on R-TOU at October 31, 2026, by district: how many had been on it without a break since
November 1, 2025 or earlier, and the kWh all of them used 4 p.m. to 9 p.m. and 11 p.m. to 6 a.m. in the test year**
(15 figures, whole numbers). H18 home: the book R-TOU carries into 2027 as it closes to new service, the committee's
second budget line beside R-ON. Path: the CIS rate rows and service accounts, the extract, the dictionary (four files,
nine columns).
- A1 (re-written rows; silent primary): since the June 2025 upgrade the TOU module re-writes a member's R-TOU row at
  any account maintenance, so 1,052 rows end one day before a same-code row begins; the spell is the run of
  contiguous rows, and the row in effect at October 31 starts at the last re-write. Every tenure cell moves (Arden
  Flats 247 to 174, Brisco Bend 396 to 269, Kessel Mill 547 to 364, Pike Ridge 149 to 102, Tamsey 358 to 245).
- A2 (re-collected reads; seen, reflex repair wrong): 697 estimated months of current R-TOU meters were re-collected
  and the MDM keeps both rows, the estimate loaded first; the battery's keep-first drop keeps the estimate. Every kWh
  cell moves (by 46 to 642 kWh).
- A3 (open rows on closed services; shared hazard): the TOU module's rows are not end-dated by the closure batch,
  424 closed services still show R-TOU open; a face-value read adds 56,769 to 155,548 kWh per district.
- Stops (asserted): in-effect row's start (all 5 tenure cells); keep-first on duplicated meter-months (all 10 kWh
  cells); open rows taken at face value (every cell).

**Ask B. The R-TOU enrolment requests received March 1 to May 31, 2024, local time, by district, and how many came
through the web form, a duplicate submission counted once, each in the district of the service it put on R-TOU**
(10 figures). H18 home: R-ON is marketed the way R-TOU was, so the launch's request load by district and channel is
the member services plan beside the forecast. Path: the CRM workbook, the CIS rate rows, the service accounts (three
files, eight columns).
- B1 (a web request keyed to the member's first service; silent primary): for a member holding a house in town and a
  farm dwelling, the web form keys the case to the member's first service while the CIS change goes onto the
  dwelling; the case's service never gets an R-TOU row and the member's other service gets one at the next read.
  Every cell moves (Sedge Flats 159 and 93 to 175 and 107, Brisco Bend 277 and 152 to 284 and 159, Kessel Mill 364 and
  224 to 354 and 215, Pike Ridge 71 and 37 to 70 and 36, Tamsey 267 and 148 to 255 and 137).
- Hazards: UTC stamps (22 cases change month in local time), duplicate web submissions closed as duplicates.
- Stops (asserted): the named service (all 10); UTC months and every case (the mirror, 9 of 10 miss).

**Hazard table.**

| Hazard | Root cause | Moves | Per-ask delta |
|---|---|---|---|
| H1 re-written TOU rows | account maintenance through the TOU module since June 2025 | A | tenure cells, -47 to -183 |
| H2 re-collected reads | the MDM's TOU re-collection keeps the estimate | A | kWh cells, 46 to 642 |
| H3 open TOU rows on closed services | the closure batch skips the module's rows | A | every cell of a face-value read |
| H4 first-service keying | the web form keys to the member | B | every cell, 1 to 16 |
| H5 UTC stamps, duplicate submissions | the CRM | B | the face-value read |

**Referee.** A1: the contiguous same-code rows and the tariff's once-in-twelve-months term; A2: two rows of one meter
and read period; B1: the R-TOU row on the member's other service at the read after the case. Each is countable from
shipped rows.

**Cracker sheet** (`generator/cracker.py` on the cut pack: the call landed, services open at October 31 filtered,
every filed rule executed, the battery's keep-first repair, the in-effect row's start, the named service)

| Ask row | Figures | Cracker's path | Device that holds | Verdict |
|---|---|---|---|---|
| Ask A, tenure and kWh by district | 15 | in-effect row's start; keep-first on duplicated meter-months | A1, A2 | miss |
| Ask B, requests and web requests by district | 10 | local months, duplicates dropped, the named service | B1 | miss |

Measured by: `generator/cracker.py` (Part 0's weights: the call and its components 38, the instructions 7, the asks
55 over the 25 ask figures; a response off the call keeps 5).

Mirror leakage: 4.0 per cent of ask weight (the mirror keeps 1 of 25: Pike Ridge's web count).

Pair ceiling: 29.6 measured on the cut pack (the cracker 45.0, the mirror 14.2). The honest risk: A1 falls to a reader
who builds spells from contiguous rows and A2 to one who keeps the actual read, so a reader taking both lifts the
cracker by 22 points; B1 is the silent one.

## Earlier screens (architectures 1 and 2, kept as history)

**The 2026-10-19 status: PAUSED at stage 1, no card registered, nothing cut.** The receiving-desk architecture was
re-rooted on the coordinator's call, and the re-draw screened the actuarial mortality-longevity cell on code
(three designs, prototypes a1 to a7 and b1) and the human-reliability cell on code (h1, h2). A second screen
took the coordinator's two candidates on code (screenA: event prediction in an outcomes trial, then fatigue
under a longer-shift roster), and neither held on measurement. A third and final screen (screenC) took the
coordinator's read-across candidates on code, F (a first annual renewal in a second market, measured in full
in an earlier market) and G (a new meter batch's failures, read from an older batch of the same design), with
the four stumping 1.2 screens of eda6c8c run first, and neither held. A fourth screen, the author's redraw in a
new world, took the political-science-public-policy cell (election-polling-forecasting) on code under the
round's bans (scratch r171/proto: seats_sim.py, tactical_sim.py), with stumping 1.3's library test applied, and
nothing held; a fifth took the scaling-laws cell the same way, and nothing held there either. No architecture
is live. This note holds the screen record only; it carries none of the `precut.py` sections, because no
design exists.

**The election cell, in one sentence.** The quantities with enough rows to price at the bar (seats from
constituency results, turnout from registers, ballots from tracking files) have textbook routes a back-test
settles, and the judgments beyond them are composition-type (who is in the electorate, which ballots remain,
which seats declared first, out this round), or carry levers under 20 per cent because the last result already
embeds the structure, or rest on an election-level behaviour estimated from a handful of past elections;
poll-based shares and margins fail on arithmetic before any of that.

**The scaling-laws cell, in one sentence.** A fifth screen took general-statistics-data-science (scaling-laws, the
subdomain never drawn) on code (scratch r171/proto: cbs_sim.py, dir_sim.py), with the client's three cards as the
default path: every judgment beyond the cards puts runs on a common exposure (batch-efficient tokens, the value of a
repeated token, a completed-schedule equivalent), so where some runs attain the plan's condition the effect is a filter
and a divide on them, and where none does its dependence is extrapolated by forms the runs cannot tell apart, while the
graded figures that can carry a 30 per cent lever (token and compute budgets) carry inversion noise of 10 to 50 per cent.

**The structural sentence, and the first thing to read.** A near-term mortality quantity of a population the
record observes every year is reproduced by carrying the last period's amount-weighted rate onto the current
roll, because next year's population is this year's population one year older; every analytical correction
the field owns (the amounts gradient, credibility, improvement, banding, a covariate model) corrects a
quantity the persistence route already measures in the right units, so the decisive step has to act on a
period the record never contained (the client's "a known schedule change makes the next period genuinely
differ"), and in mortality the scheduled changes are premium steps, which live on thin life-insurance deaths,
and benefit changes, which only move weights the persistence route can re-weight. The second screen met the
same wall from the other side: where the coming window differs from the record only in cells the record has
not yet filled (durations the late, lower-risk entrants have not reached; hours on duty most of a workforce
has never worked), either the field's standard forms disagree in those cells by more than any rival misses
by, or a straight line carried through the filled cells lands, so a draw here needs a coming-window
difference that the record measures in full somewhere else in itself. The third screen built exactly that and
found the read-across is the common-exposure subset screen's completion branch: no unit of the target has
reached the exposure, so the step aligns its units with a population that has, at a common point (the same
month of the term, the same age), and that alignment is itself a filter and a divide on the attaining
population, while every partial alignment (an earlier common point, a ratio of a related rate, a band at the
wrong point, a haircut) lands inside the bin the full alignment's own family needs, because the family spreads
as the target moves away from the attaining population, so the gap that moves the rivals out widens the bin
with them.

## Tried and rejected

- **Architecture 1, a regional grocery network's receiving desks (supply chain, never registered).** The 90th-percentile tractor count a DC closure needs was meant to turn on queueing at the receiving desks, but a flat 20 to 30 minute dwell uplift reproduces the queue's effect on that statistic within a tractor, and in the overload regime the stump needs the standard congestion constructions disagree (the M/D/1 desk is undefined there, the fluid queue runs 3 tractors under the discrete-event replay, the empirical wait curve 9 under, the hourly M/D/1 23 over or 3 under), so neither strength nor determinism held (prototypes p1 to p27, p27 the coordinator's four-construction and flat-uplift test).
- **Levers rejected inside architecture 1.** Drive-time calibration (another scalar correction a flat uplift absorbs); reverse congestion at a slow Northgate desk (about one response in three lands it); roster-capped demand rebuilt from release times (task168's driver, and the release times would have to be named in the estimand); dispatch re-timing (it works only with a filed or withheld dispatch rule).
- **A miners' pension trust's 2027 pension release, where larger pensions die sooner (actuarial mortality-longevity, prototypes a2 to a7).** A flat dollar rate per year of credited service makes the pension track years underground, so the amount-weighted experience ratio runs 11.6 to 13.0 per cent above the head-count ratio and every textbook factor (amounts lighter than lives) points the wrong way; on a cohort-built fund (miners only, 2023 to 2026 experience) the head-count route misses by 10.4 to 11.5 per cent, the head-count ratio times 0.95 by 14.9 to 15.9, times 0.90 by 19.4 to 20.3, the table at face value by 26.7 to 28.7, and the head-count route fails the 2026 hold-out by 3.3 to 5.6 standard deviations. It died because the release is observed every year: last year's release rate on the December roll lands 3.1 to 5.8 per cent from the golden even in a closed, ageing fund (the four-year crude rate 6.5), inside any bin that holds the twelve golden-family estimators (range 1.2 per cent) and one sigma (1.0 per cent), so the plainest rule of thumb lands, and a solver who weights by amounts lands too (the step is a coin flip).
- **The same trust's liability for the miners' pensions.** No persistence route exists, but on the same fund at 6 per cent the head-count multiplier moves the present value only 4.1 per cent against the generator's member-level model while a single amount-weighted multiplier lands 1.0 per cent under it (the service GLM 0.2 under, the table at face value 13.0 over), so no bin separates the rival while holding the estimators, and the decisive step reduces to the weighting a literate solver takes by reflex.
- **A term insurer's ten-year level-premium step (series A through its step in 2022 to 2024, series B stepping in 2027, healthy lives leaving at the step; prototype b1).** It died on determinism: series A's 27,332 persisters carry 117 deaths in their first post-step year and series B's forecast year 32, so face-weighted rates by jump band carry 10 to 20 per cent sampling error, and the band-matched golden route moved minus 13 and plus 33 per cent against the simulated claims across two seeds. A step at an anniversary is also task107's driver.
- **Screeners' threat-image detection under a summer roster with 30-minute X-ray stints and a large new-hire cohort (human-reliability-assessment, prototypes h1 and h2).** Persistence, tenure-only and minutes-only routes sit 1.5 to 4.3 points above a golden family that spreads 0.34 to 0.38 points within a seed, but the learning curve's form alone (exponential against logarithmic in experience) moves the figure 0.34 to 0.38 points, so whole-percent grading has no quarter-bin margin; both moves are visible attributes (stint length on the roster, tenure from the hire date), which is the reflex death task202 recorded for time on task and task182 for experience composition. The stronger variant, vigilance restored only by a break and not by a rotation, repeats task132's reset clock.
- **Paper screens, not coded.** A pandemic-contaminated window (the fund's level against contemporaneous population mortality): excluding 2020 and 2021 is the field's reflex and lands within 2 per cent, and the as-of would sit in early 2023, where a solver's own knowledge of 2023 mortality is an outside fork. Experience-rated employer groups chosen for the worst ratio: credibility toward the manual rate is the field's reflex and lands. Election polling: every vote-share family (house effects, likely-voter turnout, undecided allocation) spreads wider than the margin any rival misses by. Population pharmacokinetics: the decisive structures (renal covariate, accumulation to steady state, Michaelis-Menten elimination, unbound fraction) are filed formulas (rule application) or tail counts whose method families spread.
- **Event prediction in a blinded event-driven outcomes trial whose protocol amendment opened enrolment to lower-risk patients (biomedical-clinical-research, survival-time-to-event-analysis, the forecasting task type, since clinical-trial-design-analysis serves only experiment-causal; prototypes in screenA).** The count of first adjudicated primary events over the next 3 to 12 months, forecast from blinded pooled data, was to turn on the hazard by time since randomisation within entry cohort, because a hazard pooled over every entrant lends the late, lower-risk entrants the early entrants' hazard at the durations they are about to reach. It died on measurement in every layout tried. On a frailty-and-mixture truth (12,000 patients, Weibull shape 0.6, gamma frailty 0.5, the post-amendment cohort at about 0.6 of the earlier risk, 9 and 12 months ahead) the standard cohort-aware forms spread from 13 to 25 per cent under to 4 to 10 per cent over their median (log-normal 11 to 13 under, Cox 5 to 11 under, the stratified piecewise model 13 to 25 under, the Weibull 3 to 7 over), sigma 9 to 16 events on medians of 185 to 263, while the pooled Weibull sits only 15 to 18 per cent over the median and the pooled log-logistic 13 to 15. On a clean proportional-hazards Weibull truth (6,500 to 11,000 patients, cohort hazard ratio 0.4 to 0.5, 12 months ahead) the family spread 58 to 157 events on medians of 289 to 572 with a patient-bootstrap sigma of 16 to 22, so a bin holding it needs 197 to 396 events, against a nearest rival (the pooled log-logistic, or the last three months' events per patient-month) 25 to 85 off. On the most favourable layouts (a small early cohort with a long low-risk enrolment, or a late amendment, 3 to 12 months ahead) the three core forms alone (Weibull, Cox with its baseline carried on, piecewise exponential, each with the cohort term) spread 20 to 45 events on about 230 at nine months, sigma 3 to 15, bins needed 45 to 204, nearest rival 9 to 62 off, and even with no family spread the pooled log-logistic sits under four sigma of the golden in two of three seeds. The dial: the cohort effect bites only at durations the late entrants have not reached, so the golden itself carries a hazard into unobserved cells (proportional hazards borrowed from the early cohort, or the late cohort's own shape extrapolated), and that carry is what spreads the family; shortening the horizon to stay inside observed durations hands the call to the last months' events per patient-month, 12 to 30 per cent over at 9 to 12 months and 9 to 12 events off on about 100 at 3 months. The amendment notice the pack would carry also makes the decisive rung readable, and the duration piece without the cohort is task134 v2 round 1's driver (guard 0.18, the nearest).
- **Dispensing errors in a hospital pharmacy moving from 8-hour to 12-hour shifts, with hours 9 to 12 worked only on overtime extensions taken by staff whose own error rate is low (human-factors-ergonomics; the forecast would sit in human-reliability-assessment, since workload-fatigue-shift-analysis serves only root-cause; prototype simB).** On 70 staff over two years (about 32,000 shifts, 7,500 to 8,000 errors, volunteers selected two standard deviations on the logit of the person effect) the right family (person fixed effects with hourly or grouped duty-hour categories, a two-slope spline, with or without time of day) agrees within 1.0 per cent and a within-person shift bootstrap puts sigma at 2.2 to 2.3 per cent, so a bin holding it needs about 11 per cent of the forecast (440 to 470 errors); the pooled duty-hour model misses by 15 to 19 per cent and the flat rate per item by 13 to 15, but the gradient over hours 1 to 8 carried in a straight line to hour 12 lands 0.4 to 9.2 per cent from the golden (0.8 to 9.3 pooled), and the published 27.5 per cent excess for 12-hour shifts 8 to 11 per cent over, both inside the bin. The decisive step itself (the gradient read within each person rather than across people, applied to a forward plan that lengthens every shift) is task149's driver by the abstraction test (guard 0.15, the nearest), in the human-reliability cell where this slot's screener design already died.
- **A first annual renewal in a second market, read across from a first market whose annual cohorts have renewed in full (product-analytics, retention-cohort-lifetime-value-modeling; prototypes simF, runF, sweepF and screensF in screenC).** Market B's annual terms, six to eleven months run at the as-of, renew inside the window; market A's 29,900 complete first terms carry the only renewals on file; the golden reads each open B term from the state it has reached (auto-renew status, engagement) through A's renewals at the same month of the term. The eda6c8c screens, as code: dispersion and truncation do not apply (a level, no suppressing threshold); variance-only passes (the step moves the point estimate, lever over noise 9 to 45); the common-exposure subset screen fires, because no B term attains month 12 (0 of about 10,600), so the escape is completion from an attaining population that differs from B (B's engagement 0.34 to 0.50 sd lower at the same month), and the golden is itself a filter and a divide on A (banded same-month rates within 1.4 to 2.1 per cent of the logistic) while the attaining population's plain filter and divide (A's raw rate) misses by 16 to 28 per cent. Separation fails as well: across 36 runs (market gaps of 0.25 to 0.8 sd of habit, three persistence settings, three seeds) the family (two logistics, banded rates, a forest, a tree, engagement only, every month observed, a second-order chain) spreads 1.0 to 6.0 per cent with sigma 0.74 to 1.27, so the bin needs 5.3 to 16.1 per cent, and 6 to 11 routes land inside it in every run: A's renewal by month-1 engagement band in all 36 (0.25 to 0.92 bins), the end-of-term engagement band scored on present engagement (0.18 to 1.02), trial-day bands (0.40 to 1.17), the memoryless chain (0.46 to 1.10), the engagement-ratio and monthly-plan-ratio adjustments at the smaller gaps, a 10 to 30 per cent haircut and a textbook 30 to 35 per cent renewal rate at every gap. The bin widens with the gap because the family spreads as B moves away from A (a single dial), and the A-trained family itself runs up to 6 per cent above the truth on B's prior shift. guard.py slots found no earlier screen of the mechanism.
- **A new smart-meter batch's failures in its third year, read from an older batch of the same design observed to age ten (energy-systems-utilities, asset-condition-maintenance; prototypes simG, simG2 and sweepG in screenC; task164's peak-coincidence driver untouched).** 600,000 new meters at ages 2.0 to 2.5 and 900,000 old ones at 8 to 10, about 9,800 new-batch failures, a bathtub hazard (early-life decay, a constant, a wear-out onset); the golden is the old batch's age-specific rate at the window's ages scaled by the new batch's level against the old at the ages both have reached. The common-exposure subset screen fires: no new meter attains ages 2.5 to 3.5, the attaining old batch's own filter and divide misses by -23 to -27 per cent, and the golden is two filters and a divide (the new-to-old ratio over ages 1 to 2.5 times the old forward rate lands -0.2 to +3.2 per cent from it), the batch comparison at common ages any reliability analyst makes first. Under a proportional-hazards truth (five seeds) the family spreads 1.2 to 8.6 per cent with sigma 2.6 per cent, so the bin needs 13 to 27 per cent, and the accelerated-time form (+18 to +22), the new batch's cumulative rate carried (-13 to -17) and its last six months' rate (-15 to -23) sit inside it in most seeds, the new batch's 2026 rate (-20 to -26) and the old batch raw at about one bin. And the form that carries the batch difference into the ages the new batch has not reached decides the figure: under an accelerated-time truth, or a difference in the early-life mode only, the proportional-hazards family runs 16 to 27 per cent off the truth, told apart only by a likelihood ratio on the early ages (+17 to +63 units under the proportional truth, -29 to -55 under the accelerated one), which is the structural sentence's first horn again. A Weibull fitted to the old batch, the field's first form, runs +67 to +74 per cent.
- **Election polling, the swing scale (the redraw's lead; political-science-public-policy, election-polling-forecasting; seats_sim.py).** A seat projection under a filed national scenario (600 seats, six past elections, a third party C rising 15 to 20 per cent, the governing party falling 36 to 33) was to turn on the scale of the change across seats, uniform swing being the default. It died on stumping 1.3's library test, measured: under a logit truth the back-test of uniform, proportional and logit swing on the five past pairs picked logit in 4 of 4 seeds and landed within 0 to 5 seats of the truth's 64 to 72 C seats, proportional swing alone within 0 to 3, while uniform swing missed by 17 to 22 seats; under a uniform truth the back-test picked uniform in 3 of 3. The scale is a debate between textbook routes that a careful reader back-tests both sides of.
- **Election polling, a realignment that keeps moving (seats_sim.py, truth realign).** Each seat's lean drifting along a factor recovered from the history of seat-level changes (step 0.10 to 0.50 logits per election, transient noise 0.10 to 0.18) was meant to be the judgment beyond the swing scale. It died on lever: the logit swing the back-test picks lands within 0 to 6 seats of the truth's 83 to 101 C seats at every setting, because the last result already carries five steps of the realignment and one more adds under 6 per cent; the per-seat trend, factor, pooled AR and last-plus-mean-change routes all land inside the same few seats.
- **Election polling, tactical switching when a seat's configuration changes (tactical_sim.py).** The third party's voters moving to the close challenger where the governing party leads (rate 0.25 to 0.60, window 12 to 20 points), so seats entering that configuration gain beyond the swing. Truth 58 to 79 C seats; uniform swing 32 to 48 per cent under, but the logit swing the back-test picks only 5 to 13 seats (9 to 17 per cent) under, a swing stratified by the last result's winner and runner-up no closer, and the true model's own hard count up to 8 seats from its expected count, so the estimand's hard-or-expected choice forks by as much as the lever and the tactical form (window, decay, who switches) is a free specification.
- **Election polling, paper screens across the cell.** Poll-based vote shares and margins fail on arithmetic (a share cannot move 30 per cent; a margin's sampling sigma is about a point on 10,000 to 100,000 respondents). Turnout after a surge election: the comparable-election reflex lands, and with surge registrants it is composition, out this round. Election-day turnout from the remaining pool after early voting: the timing-against-turnout split rests on an assumption the data cannot force. The late count completed stream by stream: a few hundredths of a point on the margin, and task181's driver. Mail-ballot returns by time since each ballot was mailed: the mailing delay is a stated break, the realigned curve is the subset route, and the driver is task134 v2's and this slot's own screenA death. Expected seats of a party near a threshold: card 1's simulation lands. Phantom swing as a hold: a margin's sigma. Notional results on new boundaries from ward local results: a single-purpose file and the textbook allocation. The local-election swing pattern carried into a general election: a fitted regression on the obvious covariate. Ballot cure deadlines (task172), a holiday in the count's development (task162-like, small), a ranking cap in ranked-choice counts (task168-like), signature-sample duplicates and betting longshot bias (the swap test fails), seat quantile calibration (a variance lever on a few cycles).
- **Scaling laws, the critical batch (general-statistics-data-science, scaling-laws; cbs_sim.py).** A planned 1.5B run forced to an 8M-token batch by a new pod, graded on the tokens to first reach a target validation loss, the judgment beyond the three cards being that tokens stop being the exposure once the batch passes the critical batch, which grows as the loss falls (the steps-against-tokens tradeoff, the critical batch read from the batch sweeps). Truth 383B tokens; the golden (critical batch a power law in the loss) -4 to +4 per cent; the cards' pooled fit +27 to +43, the standard-batch grid -19 to -45, a batch covariate +36 to +41, one pooled critical batch +13 to +17. It died on determinism: the critical batch as a power law in the reducible loss fits the sweeps as well (residual sd 0.046 to 0.070 against 0.039 to 0.066) and lands +73 to +99 per cent (+99 to +230 in a fixed-recipe variant with the plan near its own critical batch, where the cards miss by -42 to -53), and as a power law in data size it runs wild; with the target inside the sweeps' losses the batch factor at the target is a filter and a divide on the largest sweep. The single dial is the target's distance below the sweeps.
- **Scaling laws, card 3's holdout direction against an overtrained plan (dir_sim.py).** A 1B model trained to about 250 tokens per parameter, the judgment being that the form is validated along the plan's tokens-per-parameter axis rather than on the largest compute. It died twice: where the forms differ enough to matter (a coupled truth against the additive form, RMSE 3.6 against 39 to 62 thousandths of a nat) every holdout and the in-sample fit pick the right form, so the card lands; and a token budget near the size's own loss limit swings -22 to +96 per cent across seeds under the true form itself.
- **Scaling laws, paper screens.** Repeated data (the value of an epoch at the plan's count is measured by small multi-epoch runs, a filter and a divide, unless its dependence on model size is extrapolated, which spreads); learning-rate drift with scale (the same dilemma); downstream accuracy read through the loss (the external models nearest the predicted loss are the forecast); continued pretraining from a cooled checkpoint (matched continuation pairs measure the penalty); interval calibration by back-test distance (a handful of origins); best-of-attempts selection at the largest scale (a lever of a few thousandths of a nat); compute accounting from configs, rolled-back tokens and eval-set drift (rule application or Layer 1).
- **Rebuild 2026-10-23, the discrete-choice cell, paper screens before any harness.** The client's three cards (willingness to pay as a ratio, IIA against nesting, scale across samples) are the default path, and each judgment drawn beyond them died on paper: congestion feedback when a toll moves trips onto a crossing that slows with its own volume (task253's and task228's fixed point); a randomised savings-plan invitation whose comparison arm is reached through co-workers (task131 architecture 1's household interference read where a group drew one arm); diversion after a product is withdrawn read from each buyer's browse log (the set a buyer would consider once the product is gone is not the viewed set less the product, and with stockout episodes the diversion is a filter and a divide); logit curvature at each unit's own propensity (task165's own-baseline gain); attenuation from skimmed travel times corrected on a GPS sub-study (skims are zone averages, so the error is Berkson and barely attenuates, and the sub-study sees only the chosen mode's time); a nesting dimension no category names (a likelihood back-test picks it, the election cell's death); choice-based sampling (calibrating constants to counts is the reflex); crop rotation after a price spike (the lagged crop is the obvious covariate); travel-time reliability (mean delay proxies its spread across routes and hours); a customer switching away from a plan whose provider fails (task169's two routes, one closed).
- **Rebuild 2026-10-23, departure-time choice under a 2027 peak surcharge (scratch `b171n/proto/dt1.py`).** A bridge's commuters choosing 15-minute slots under a scheduling-model truth (preferred arrival times, early and late penalties, a lateness step), with an early-bird discount and planned roadworks in the record to calibrate on. Over 18 settings the peak window lost 24 to 46 per cent of its share; a multinomial logit with slot constants and its toll and time coefficients calibrated on the early bird and the roadworks overstated the drop by -1 to +40 per cent (median about +20), and the early bird's slot shifts scaled to the surcharge understated it by 28 to 72. It died three ways: the textbook route sits 15 to 25 per cent of the drop off in most settings, under the 30 per cent lever the held builds carried, and straddles zero in one; the golden is a structural scheduling model over a latent preferred-arrival distribution, so its outsider family is a set of specifications (preferred time from habit or fitted, linear or stepped lateness) rather than one construction; and a peak surcharge names peak spreading, so the adjacent-slot step is the question's own reflex.

- **Rebuild 2026-10-23, measured inside architecture 3 before the pack was frozen.** (1) A take-up truth with one decision and a fixed launch-response curve put the textbook discrete-time hazard 10 to 15 per cent under the 12-month logit on the shortfall, so the truth is the monthly logit hazard the field writes, and the 12-month logit, probit and saving bins sit within 4.8 per cent of it on services. (2) With the overnight rate's customer charge above R-1's, the overnight savings sat left of the evening rate's and every form extrapolated in the lower tail; equal customer charges and the overnight rate's top savers kept inside the evening rate's range removed it. (3) A forecast population with part-year services forked on annualising their saving (2,298 services and $206,671 against 2,216 and $201,673); the paper now files the population as the services billed in all twelve test-year months, and annualising the cohort's part-year savings is rejected by 235 log-likelihood units. (4) Ask B by district and month left 3 to 7 of 15 cells unmoved by the first-service keying, so it is graded by district, with the two-service members' homes in town and their farm dwellings out of town. (5) A re-issue of every R-TOU row at one date put every tenure cell at zero under the in-effect row's start, a loud failure; the re-writes now follow account maintenance after the June 2025 upgrade (42 per cent of spells). (6) Districts named Coldwater and Velma were renamed (Brisco Bend, Tamsey) for real places with utilities, and Arden Flats (Sedge Flats) for reading as a person's name.
- **Architecture 3 (optional-rate take-up, Sablewood Electric Cooperative) spent at Gate F on ce04ed65, 2026-10-23.** Scored reader B filed 2,250 services and $200,000 and all 20 ask figures. Its path: "Cohort = R-1 services at launch, billed 12 months pre-launch, open through 2025-02-28; outcome = on R-TOU 12 months after launch. Logistic on annual dollar saving (R-1 minus R-TOU, 2024 rates, pre-launch use) fits best"; for the asks, "consecutive R-TOU rows (1-day gap) merged into spells ... after dropping the EST row of each EST/ACT duplicate" and "CRM times UTC converted to local ... 'Closed - duplicate' rows dropped". A careful reader calibrating take-up on a launch cohort reads the cohort's pre-launch covariates by default, because that is the textbook way to set up a launch cohort, so the decisive step was the default; and every ask device (spell gaps, estimate and actual duplicates, UTC, duplicate-closed rows) was visible hygiene the battery executes.

## Retired

task171 retired on 2026-10-19 under the author's rule for this round (a number that dies in its second new cell retires);
no card was ever registered. The seed's receiving-desk architecture died at the draw, and the redraw round's two cells
died on code: political-science-public-policy / election-polling-forecasting (e27c16f: the swing scale is settled by a
back-test a careful reader runs, and the realignment and tactical layers sit under the bar or fork on hard against
expected seats) and general-statistics-data-science / scaling-laws (96b18ed: every judgment beyond the three client
cards is a common exposure the sweeps either measure, so a filter and a divide lands it, or cannot pin, so the family
spreads past any rival). The lesson: in a field whose standard is a back-tested model choice, the back-test is the
textbook route and it lands.

## Rebuild (2026-10-23)

Reopened under the author's rule that no number stays retired; rebuilt from scratch in economics-econometrics / discrete-choice-limited-dependent-variable-modeling as architecture 3 (`## Draw`), the receiving-desk seed and both redraw cells left spent.
