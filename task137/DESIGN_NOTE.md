# task137 design note

Architecture 4, drawn and registered 2026-10-26 (wave 2 slot, Forecasting lane, sathya8571), under the author's ruling
that task137 is neither retired nor paused. Architecture 1 (Kaimai Building Society's maturity campaign booked in
agent-hours, banking) was landed on the portal; architecture 2 (Calderbrook Care's 2027 adverse-drug-event admissions)
lost every decisive step it held to isolated probes before a pack shipped; architecture 3 (Calderwick Police's Tanner
Street custody hub) was spent at stage 4 when the judge read its decisive step as data semantics. All three identities
are in the card's lineage and their dead ends in the last section; nothing of any of them is kept. This draw is
Hollinsfield and Brantmoor Hospitals NHS Foundation Trust's plan for the GP-referred blood-test visits its new
community phlebotomy hub at Kingsmead Health Village will see in 2027-28.

## Reopened

2026-10-26, after architecture 3 was spent at stage 4 (SEND_BACK) and the build was paused (30e89353): the author ruled
that task137 is neither retired nor paused and continues until it ships. Architecture 4 is authorised, in any world and
with any stump strategy; the author asked for heavier realistic data messiness and for techniques where several
defensible methods compete while the answer stays deterministic. Two architecture 4 candidates were probed in parallel:
thread A's staggered food waste rollout (probe8) was landed by Opus probe p137lb before registration (`## Tried and
rejected`), and explorer B's walk-in phlebotomy clinic (probeB1) was missed by both isolated Opus probes, p137ka and
p137kb, which filed 51,000 against that pack's golden of 54,000. The clinic is architecture 4, registered 2026-10-26;
the sections below describe it.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task137.json`, architecture v4, registered 2026-10-26T14:03:36Z with v1 to v3 and
   thread A's unregistered v4 candidate in its lineage and the author's ruling in its notes. `guard.py check`: WARN,
   answered: `repeat.decision` (quantity_figure after task487: the forecast's call is a level, which is the honest type)
   and `repeat.deliverables` (png and xlsx after task121's architecture 6: a plan workbook and the chart of the demand
   it rests on); NOTEs `test.same_puzzle_older` against task156 and `test.same_driver_older` against task111 v2 and
   task86 v2, each differentiated on the card, as are task168, task308 v1, task108, task147 and task18, the
   unconstrained-demand builds on file.
2. Pairing: Healthcare Delivery & Health Economics (client domain) / `utilization-access-demand-forecasting` /
   Forecasting & Predictive Modeling. The deciding quantity is a service's unconstrained demand at a new site: the
   GP-referred blood tests a community hub staffed never to run out of tickets will draw in its first year, forecast
   from the walk-in clinic's record with the capacity effects taken out.
3. Niche: Hollinsfield General Hospital's walk-in phlebotomy clinic (Outpatients block A, Monday to Friday 07:30 to
   15:30, seven posts, adults with a GP or hospital-clinic request). The senior phlebotomist sets the day's tickets at
   40 a substantive and 32 a bank phlebotomist on the floor; once they have gone, reception turns arrivals away with
   the offer of a booked slot at Brantmoor Community Hospital and logs them for the PALS return. It ran out on 58 of 253
   clinic days in 2025-26, mostly in the weeks a hospital clinic's recall programme crowded the queue. Twelve practices
   refer, seven of them running their own phlebotomy clinics under the local enhanced service. From 1 April 2027 the
   Kingsmead hub takes every patient with a GP request and never runs out; hospital-clinic patients stay at block A.
   The integrated care board's planning assumption (3.5 per cent a year) is applied to 2025-26.
4. Call and shape: the hub's 2027-28 GP-referred visits to the nearest 2,500 (`quantity_figure`, how-many); shape
   `other`: the call with its three components, the weekly chart of 2025-26 GP-referred demand (seen, turned away and
   kept in-house, 53 weeks), and two ask grids on the walk-in clinic's other work (hospital-clinic visits by specialty
   and quarter, 28 figures; working days lost to sickness and the sickness absence rate by quarter, 8 figures).
   Criteria: the call and its three components (4), the chart (3 or more), 36 ask figures, the two files: 25 or more.
5. Mechanism keys: gap time then population (the record was made under a clinic that ran out and the plan bets on one
   that never does, and the patients the run-outs sent elsewhere are in no record); pattern none, generators G5 (the
   practices' own phlebotomists bleed the deterred patients), G12 (a turned-away patient is logged, a deterred one
   leaves no record), G13 (the record's horizon held run-outs, the hub's holds none); strategy `other`, because the
   nearest key, `informative_censoring`, is task487's inside the three-build window and `causal_design` is banned
   against task121; Gate G `forecasting`: the graded object is a forward level whose history is read correctly.
6. Layer 2: `field_method`, pattern
   `own:walk-in-unconstrained-demand-adds-patients-deterred-by-recent-run-outs-not-only-those-turned-away`.
7. Furniture: forum `customer_or_counterparty` (the integrated care board agrees the trust's 2027-28 activity plan);
   forcing event `purchase_order_or_contract` (the activity plan in the 2027-28 contract); organisation family
   `hospital_or_health_provider`; role family `capacity_planner` (Clinical Support Services planning); context
   artifact `close_out_summary` (the clinic's 2025-26 annual report); calibration `none`.
8. Spine: the new kiosk's queue events, 18 November 2024 to 30 September 2026 (311,893 rows: check-in, call and
   completion events, the check-in carrying the request form's type, the issuing organisation's code and the request
   date read from its barcode); with the legacy ticket file (April 2023 to November 2024) the daily record runs 883
   clinic days. The deterrence is identified from the record's own variation in run-outs, which the hospital clinics'
   recall programmes mostly drive and which the reception log records day by day.
9. Deliverables: `hub_plan_2027-28.xlsx` and `gp_demand_2025-26.png`.
10. People, from `guard.py names --geo GB --seed 137`: Katherine Storey (the phlebotomy service manager, the annual
    report's author), Hugh Metcalfe (pathology operations lead), Charlene Dale (reception, the log's owner), Bethan
    Matthews (the board's head of planned care) and Joseph Wood (the hub's session planner). Patricia, Rachel, Richard,
    Rebecca and Duncan from the same draw repeat older builds' first names (`people.first`), so they are left out.
    None appears in the prompt.

**Spent mechanisms on the ground** (`guard.py mechanisms --objective forecasting --strategy causal_design`, six builds):
task88 an added booking displacing full-rate demand; task139 an intervention read per assigned unit; task144 seeded
adoptions through followers; task163 a cut drawing in marginal entrants; task178 a forward dispersion with an absorbing
agent removed; task173 work-induced failures spread thinly. The unconstrained-demand builds on file recover demand
truncated on the day or counted twice after it: task18's lost-volume replays, task108's resubmissions, task147's runs
through full nights, task168's detruncation of sold-out departures, task308 v1's supply rebuilt at its peaks. None
prices demand held down in later weeks by a service's own run-outs; here the day's truncation is logged in full and its
detruncation is a rung below the golden.

**Slot screens.** `guard.py slots` on the setting's words (phlebotomy, blood, walk-in, ticket, turned away) returns
task147, task168, task173, task280, task303 and task305, none a walk-in clinic; on the mechanism's (deterred,
unconstrained, latent, demand, refused, capacity, balk) task168, task147, task194, task116, task117 and task120, none a
deterrence carried from one week's run-outs into the next.

**Probes before the draw.** The candidate was probed before registration on a call-only pack (`t137_b/probeB1` in the
session scratchpad: the two queue systems, the reception log, the e-roster and the annual report; seed 16, a
deterrence of 0.30 on every arrival, golden 54,000 against 51,000 at the nearest 1,000), by two isolated Opus probes.
- p137ka filed 51,000 (50,857.0): it completed each run-out day from the arrival-time profile of the days that did not
  run out (a 2025-26 base of 47,475.55), checked seen plus turned away against it (50,821), and found that turned-away
  patients do not return the next day (a coefficient of 0.008).
- p137kb filed 51,000 (50,821): seen plus the log's turned away, checked against the profile gross-up (a ratio of
  1.03), a regression of uncapped-day visits on the previous one and two days' turned-away counts (0.01 and -0.01) and
  staffing, and read the flat years as capped demand.
Both priced the same-day censoring and the return of the turned away, and neither asked whether a week of run-outs
kept later patients away. Their notes are answered in the shipped pack: service times vary by phlebotomist, with
fasting and long draws and re-calls; the log's AM and PM boxes split at the 12:30 shift change, with an "inc PM" comment
on some mornings; the probe pack's 35 tickets a phlebotomist became the senior phlebotomist's 40 and 32; the call moved
to GP-referred visits, the hub's population.

**The domain anchor and the Gate B facts.** The deterrence is held by the practices that can bleed their own patients:
the annual report's "Most of the catchment's practices run their own phlebotomy clinics under the local enhanced
service" (a fact about the practices, in the service description) and the practice register's
`phlebotomy_les_2025-26` flag, with the request form's practice code from November 2024, make it measurable by
practice: practices with a clinic dip after run-out weeks and practices without do not, and that comparison is a member
of the golden family (44,528). No shipped sentence says that run-outs keep later patients away, that practices bleed
patients in-house because of them, or how many (asserted: no document carries "in-house" or "own clinic" in that
sense). The hub's population is filed in the prompt and section 6 of the annual report (every patient with a GP request,
never out of tickets, set from 2025-26), with Brantmoor's booked clinic carrying on as now.

**Data-native sentence.** The clinic runs out mostly when a hospital clinic's recall programme crowds its queue, for
weeks at a time, and seven of the twelve referring practices have phlebotomists of their own, so in the week after the
clinic has kept running out those practices bleed their patients in-house rather than send them to queue, and the
next week's GP-referred arrivals fall by about a fifth at a full week of run-outs (a coefficient of -0.210); the
patients kept are in no file, while reception's log, which counts only the patients turned away at the door, reads as
the clinic's whole unmet demand.

## Three rules

Task type: utilization-access-demand-forecasting (Healthcare Delivery & Health Economics), which serves Forecasting in the taxonomy: a service's unconstrained demand at a new site, forecast from its activity record with the capacity effects taken out, to set the site's activity plan.
Domain test: The deciding quantity is the hub's unconstrained GP-referred demand, which a healthcare demand planner estimates by taking capacity effects out of observed activity; at a walk-in phlebotomy clinic the capacity effect is not only the patients turned away on a run-out day but the patients whose practices, running their own phlebotomy clinics under the local enhanced service, keep them in-house in the week after the clinic has kept running out, measurable in the practice codes on the GP request forms, so the estimate is a count model of daily GP-referred arrivals on calendar terms and the previous week's run-out share, with the deterrence undone day by day and the result grown at the board's planning assumption.
Swap: "the hub will see the GP-referred patients whose practices bled them in-house after the walk-in clinic's run-out weeks" put into a school's pupils or a utility's megawatt-hours loses its mechanism: no referrer teaches a pupil for a week because the school was full the week before, and no network meters another's load because a substation ran short; the step needs a referral the referrer can fulfil itself, a GP blood test request that the practice's own phlebotomist or the hospital can draw, and the board's growth assumption for GP direct access phlebotomy.
Layer 1: two queue systems with a parallel-run fortnight held by both (the legacy file in local time with re-keyed times and test tickets, the new kiosk's events in UTC), reception's log in two layouts with month totals and dates typed as text (the PALS return), blank practice barcodes and a practice merger (the forms and the ODS codes), clinic codes reallocated on 1 April 2026 with only the current register shipped (the patient administration system's replacement), long-term sickness as one row a spell (the e-roster's HR feed), vacant lines and bank shifts, financial years, bank holidays, varied service times and re-calls; nothing is placed to be caught.
Layer 2: field_method: unconstrained demand at a capacity-limited walk-in service is its arrivals with every capacity effect taken out, and the run-outs' effect reaches the following week through the practices that can bleed patients themselves, so the demand is estimated by a count model of daily GP-referred arrivals on the previous week's run-out share with calendar terms, the deterrence undone day by day, rather than by adding the log's turned away or detruncating the run-out days.
Decisive step: undoing, in each 2025-26 clinic day's GP-referred arrivals, the fall that follows a week in which the clinic kept running out, read from a Poisson model of daily arrivals on weekday, month, trend, the day after a bank holiday and the share of the previous calendar week's clinic days that ran out, rather than taking seen plus turned away as the demand a hub that never runs out will see.
Not semantics: every field reads as what it is: the queue records count the patients seen, the log counts the patients turned away at the door, the register says which practices hold the phlebotomy enhanced service, and the annual report says the hub will not run out; no field, code or definition says that run-outs keep later patients away or that practices bleed them in-house, and an analyst who reads all of it correctly files 42,500, as both probes did after checking the log against the ticket-issue curve and checking that the turned away do not come back.
Not rule application: the prompt, the annual report and the board's letter file the WHAT (every patient with a GP request at a hub that never runs out, 2025-26 grown 3.5 per cent a year for two years with no working-day adjustment) and no rule says what 2025-26's demand was or how to measure it, so executing every filed rule files 42,500. Measured on the shipped pack: the enumerated family spreads 40,355 to 45,114 over three printed cells (seen alone and every arrival pooled 40,000; seen plus turned away, the run-out days completed from the ticket-issue curve and a fit on the days that did not run out 42,500; every deterrence specification 45,000); the standing family, the 27 deterrence specifications the record leaves defensible (five windows, negative binomial, an instrument, the practices with a clinic against those without, a programme-week dummy, six added covariates or windows, two fitting spans, the fitted mean at nil, two least-squares forms, weekly totals and six quiet-period fits), spreads 44,035 to 45,114, 0.43 of one printed unit and one call; and nothing loud does the ruling-out: no sentence, column or control refutes seen plus turned away, whose own checks agree with it (42,749 and 42,745), and only the fitted coefficient (-0.210, standard error 0.014) does once a solver puts the previous week's run-outs into the model.
Analyst test: A strong analyst who reads every file correctly joins the two queue systems with the parallel-run fortnight counted once, adds reception's GP-referred turned-away patients to the GP-referred patients seen (39,731 in 2025-26), confirms the log against each run-out day's ticket-issue curve and a fit on the days that did not run out (42,749 and 42,745 grown) and grows 3.5 per cent a year for two years, filing 42,500 (42,561), where the golden is 45,000 (44,685); checks.py runs both on the generator's clean truth (R3a 42,561, R3b 44,992) and on the pack.
Estimand: the GP-referred blood-test visits the Kingsmead hub will see from 1 April 2027 to 31 March 2028, every patient with a GP request, the hub never running out of tickets (the prompt; the annual report, section 6, with Brantmoor's booked clinic carrying on as now), planned from 2025-26's underlying demand grown 3.5 per cent a year for two years with no working-day adjustment (the prompt; the board's planning assumptions letter), to the nearest 2,500 visits.
No decoy: nothing is planted: the queue records, the log, the e-roster, the kiosk file and the registers are the clinic's own systems' exports, the annual report states the clinic's own year correctly and the board's letter its growth assumptions; no memo, draft or figure argues for a count, no file states a demand figure for the hub (the draft session plan carries chairs and slots, a distractor), and no stakeholder figure is set up to be overturned (R3c).
No certified replay: no certified or published figure is reproduced to recover a method; the annual report's activity table is the clinic's own count of patients seen and turned away, which the easy route and the golden both reproduce, and the deterrence is recovered from the record's own variation, not from any figure.
Lesson: a walk-in service's unconstrained demand is not its patients seen plus its patients refused: where referrers can provide the service themselves, the service's recent run-outs send later patients to them, so the record's arrivals, refusals included, are held down by the service's own record of running out, and a forward site that never runs out gets them back; no build on file prices demand deterred by a service's own recent run-outs, the unconstrained-demand builds (task18, task108, task147, task168, task308 v1) all recovering demand truncated on the day or counted twice after it.

## Default path

1. Read the prompt and the annual report: from 1 April 2027 the hub takes every patient with a GP request and never runs
   out; the plan is 2025-26 grown 3.5 per cent a year for two years.
2. Count each clinic day's GP-form visits from the legacy ticket file (Outcome Seen) to 17 November 2024 and the new
   system's CHECKED_IN events (UTC converted to UK time) from 18 November, the parallel-run fortnight once: 38,386 in
   2025-26, which matches the annual report.
3. Read both layouts of the reception log, month totals left out: 1,345 GP-form patients turned away on 58 run-out days
   in 2025-26, which matches the annual report.
4. Check the log: complete each run-out day from the ticket-issue curve of the days that did not run out (42,748.6 when
   grown) and fit GP-referred arrivals on the days that did not run out (42,744.7); both agree with it.
5. Check that the turned away do not come back later (they are offered a booked slot at Brantmoor), so adding them
   counts nobody twice.
6. Grow 39,731 at 3.5 per cent a year for two years: 42,560.8, filed at the nearest 2,500.

Ends on: 42,500 (42,561)
Golden: 45,000 (44,685)

## Stump sentence

A competent analyst adds reception's GP-referred turned-away patients to the GP-referred patients the walk-in clinic saw
in 2025-26 and grows the sum, filing 42,500, where the golden is 45,000; the step that lands it there is taking seen
plus turned away as the demand a clinic that never runs out will see, when practices running their own phlebotomy
clinics keep their patients in-house in the week after the clinic has kept running out, 1,983 GP-referred patients in
2025-26 who never reached the clinic and appear in no count, recovered only from how each day's GP-referred arrivals
fall with the share of the previous week's clinic days that ran out.

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| 0 GP-referred patients seen, grown | yes (the report's GP seen) | yes (Request, request_type) | yes | yes (the report's table) | no | yes | no | readable |
| 1 seen plus GP-referred turned away (the default) | yes (the report's turned-away column, a hub that never runs out) | yes (the log) | yes (add the refusals) | yes (the report's column) | no | yes (one sum) | no | readable |
| 2 the run-out days completed from the ticket-issue curve, or demand fitted on the days that did not run out | no | yes (issue times, the logged run-out days) | yes (detruncation, the revenue manager's move) | yes (agrees with the log) | no | no | no | readable |
| 2b every walk-in arrival modelled together with last week's run-outs | no | yes | yes (one demand model for the clinic) | no | no | no | no | readable |
| 3 (decisive) the previous week's run-out deterrence undone day by day | no (no sentence names run-outs keeping later patients away, the practices keeping patients in-house or how many; the report's line on the practices' own clinics describes the practices) | no (no column holds the deterrence or the patients kept; the run-out share is built from the log by week) | no (the reflexes are detruncation and the return check: the first agrees with the default, and the second reads positive on all visits, t 8.8 and 9.6, because the recall programmes run on) | no (no control ties under the golden) | no | no (a fitted coefficient on a constructed weekly share, undone day by day) | no (the log is the PALS return, the queue records the activity count, the register the practices' list sizes and contracts) | silent |

The decisive row's risk is the return check on GP-form visits alone: on this pack it reads negative (t -4.5 and -7.9
for the previous one and two days' GP turned away), where on probeB1 both probes read it at nought on all visits; a
reader who runs it on GP forms and asks why the days after a run-out are quieter can reach the step. That is the stage
4 reader's Gate F question.

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | GP-referred | the request form the patient chose at the kiosk (Request GP form, request_type GP) | a practice code on the form (426 forms without a barcode left out) | same call (44,429) | same call |
| SF2 | 2025-26 | 1 April 2025 to 31 March 2026 | calendar 2025 (44,222) | same call | the board's letter ("2025-26, the last complete year") and the report's financial year |
| SF3 | growing 3.5 per cent a year for two years | compounded, 1.035 squared | simple, 1.07 (44,633) | same call | same call |
| SF4 | no working-day adjustment | none | 2027-28's 256 clinic days against 2025-26's 253 (45,214) | same call | the prompt and the board's letter |
| SF5 | every patient with a GP request at a hub that never runs out | the turned away are demand | the patients seen alone (40,000) | 40,000 | the prompt ("staffed never to run out of tickets") and the report's section 6 |
| SF6 | the parallel-run fortnight | counted once (the two systems agree day by day) | counted twice (45,527) | same call | same call |
| SF7 | the hub's own run-out record | nil throughout 2027-28 | a share carried from the walk-in clinic | another estimand | the prompt ("staffed never to run out of tickets") |
| SF8 | visits | one ticket a visit | distinct patients | none: the records carry no patient key | the prompt's "visits" |
| SF9 | every patient with a GP request | the GP-referred demand of the trust's walk-in service, set from 2025-26 | every GP blood test in the catchment, the practices' own clinics included | no file counts the practices' work | the report's section 6 ("Its activity plan is to be set from 2025-26") |
| SF10 | Brantmoor's booked clinic | carries on as now, outside the hub | its booked patients moving to the hub | no file counts them | the report's section 6 ("the booked clinic at Brantmoor Community Hospital carries on as now") |

## Ladder

| Rung | Route | 2027-28 | Printed (nearest 2,500) | Distance from the golden's cell (43,750 to 46,250) | Dies to |
|---|---|---|---|---|---|
| 0 | GP-referred patients seen, grown | 41,120.0 | 40,000 | 2,630 | the hub never runs out, so the 1,345 turned away are demand |
| 2b | every walk-in arrival, GP and hospital, modelled with last week's run-outs | 40,354.7 | 40,000 | 3,395 | the hospital-form arrivals that rise in the recall programmes' weeks cancel the GP fall; the hub takes GP-referred patients only |
| 1 | seen plus GP-referred turned away (the default) | 42,560.8 | 42,500 | 1,189 | the patients the practices kept in-house after run-out weeks |
| 2 | the run-out days completed from the ticket-issue curve; a fit on the days that did not run out | 42,748.6; 42,744.7 | 42,500 | 1,001; 1,005 | the same: both complete the day, and the deterred patients never arrived |
| 3 | golden family: 27 deterrence specifications | 44,035.4 to 45,114.5 | 45,000 | inside, 285 or more from each edge | |

Position and margins: the default and both careful-frame methods sit in one cell with 1,001 to 1,189 to spare (check 2,
asserted); the decisive step moves the figure 2,124 (5.0 per cent of the default) against a standing-family spread of
1,079 on a cell of 2,500; the golden sits 935 inside its nearer edge; the record's fit picks the previous calendar
week's share over two weeks and rolling 5, 10 and 20 clinic days (AIC 7,568.0 against 7,608.2 to 7,668.6); on the
clean truth the default files 42,561 and the deterrence undone 44,992 (R3a, R3b), and the generator's latent 2025-26
demand grown files 45,074. Across seeds 26 to 37 the same construction holds check 2 at 11 of 12, seed 34 failing by
the programme-week dummy alone.

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | every patient with a GP request at the hub in 2027-28 | filed: the prompt, the report's section 6; SF9, SF10 |
| 2 Unit of account | visits, one ticket a visit | the prompt; SF8 |
| 3 Attribution window | 1 April 2027 to 31 March 2028, from 2025-26 | the prompt; SF2 |
| 4 As-of dating | records to 30 September 2026, the folder dated 2 October 2026 | the files' own spans |
| 5 Version basis | the board's 2026-27 to 2028-29 planning assumptions | the letter |
| 6 Denominator | none: a level | n/a |
| 7 Weighting | each clinic day's arrivals | C1: the 27 specifications print one call |
| 8 Window length | the deterrence window | C2: the record's fit picks the previous calendar week (AIC), and every other window prints the same call |
| 9 Boundary inclusivity | financial years from 1 April; the parallel-run fortnight | SF2; SF6 same call |
| 10 Rounding path | once, the plan to the nearest 2,500 | the prompt; the family in one cell |
| 11 Tie-break | none | no ranking |
| 12 Maturity and censoring | run-out days censored at the last ticket | the log completes them; the ticket-issue completion prints the default's cell (C1 for the careful frame) |
| 13 Order of operations | the deterrence undone, then grown | C1: multiplicative, either order |
| 14 Row order | none | C1 |
| 15 Duplicate resolution | the parallel-run fortnight, re-calls (one visit, several calls), test tickets | SF6; CHECKED_IN counts visits; R2 test tickets |
| 16 Identity normalisation | practice codes, the merger of K91027 into K91031 | SF1: the call reads the kiosk's GP choice |
| 17 Netting against gross | none | n/a |
| 18 Dimensional units | visits | n/a |
| 19 Code and status semantics | request types, the log's AM and PM boxes and month totals, Outcome values | the dictionary; R2 |
| 20 Integerisation | an expected count | the prompt's rounding |
| 21 Clause scope | "every patient with a GP request"; "underlying demand" | SF9, SF10; the report's section 6 |
| 22 Forward window contents | the hub never runs out, so no deterrence in 2027-28 | SF7: the base is grown at the board's assumption |

## Literal reader

Executed word for word, the prompt, the annual report and the board's letter fix the count (the GP-referred visits the
Kingsmead hub will see from 1 April 2027 to 31 March 2028, every patient with a GP request, never out of tickets, the
2025-26 base grown 3.5 per cent a year for two years with no working-day adjustment, to the nearest 2,500) and leave the
estimate of 2025-26's underlying demand to the data; every reading of SF1 to SF10 either violates a quoted sentence or
files the same call, and the easy answer (42,500) comes from an easy method on the same literal estimand, seen plus
turned away taken as the demand, not from another reading.

## Oracles

none: no control, published figure or reconciliation column in the pack confirms either the default or the golden. The
annual report's activity table (GP seen 38,386, GP turned away 1,345, 58 run-out days) reconciles under both answers,
because both reproduce it before the decisive step; the kiosk's ticket allocations tie the capped days' seen counts
under both; the distractors (the patient survey and the hub's draft session plan) carry no demand figure.

## Ask sheet

Both asks sit on the walk-in clinic's other work in 2025-26, rows the call never reads: the call reads GP-form arrivals
by day and the log's GP counts; ask A reads the hospital-form check-ins and the clinic register, ask B the e-roster's
substantive lines. H18 homes: ask A is the hospital-clinic demand that stays at block A when the GP-referred patients
move to the hub, by specialty and quarter for its session plan; ask B is the sickness allowance the hub's establishment
carries, from the clinic team's own 2025-26 record under the report's definition.

- **Ask A, hospital-clinic visits in 2025-26 by specialty and quarter (28 figures, whole visits).** Files:
  `phlebotomy_queue_events_2024-11-18_to_2026-09-30.csv` (CHECKED_IN rows: request_type HOSP, request_org, the clinic
  code, request_date), `outpatient_clinic_codes.csv` (clinic_code, specialty, clinic_days, code_in_use_from
  01/04/2026). Primary (a reconstruction from an identity in the data): the trust reallocated its seven outpatient
  clinic codes alphabetically by specialty when the patient administration system was replaced on 1 April 2026, and the
  register carries only the current codes; every 2025-26 request was issued under the old codes, the same seven strings
  attached to other specialties, so the join matches every row, leaves nothing unmatched and puts every count under the
  wrong name. The old codes are recovered from the weekdays each code's requests were issued on, which are its clinic's
  days, matched to the register's clinic_days (one specialty each, asserted). Hazards: requests issued from 1 April
  2026 carry the new codes; quarter by the visit's date, not the request's; the recall programmes' surges (Cardiology
  1,690 in Q1, Diabetes and endocrinology 3,367 in Q3, Rheumatology 2,269 in Q4), which the current-register join hands
  to Diabetes and endocrinology, Cardiology and Gastroenterology. Stop: the current register read as 2025-26's codes
  (0 of 28, asserted). Realism: a code reallocation at a PAS replacement is ordinary, the register describes the
  current system, and nothing in any file narrates the change.
- **Ask B, working days lost to sickness and the sickness absence rate by quarter of 2025-26 (8 figures, whole days and
  per cent to one decimal).** Files: `eroster_phlebotomy_2023-04_to_2026-09.csv` (Employee no, Assignment, Roster date,
  Hours, Absence, Vacant line), the clinic days (the queue records and `bank_holidays_england.json`), the report's
  section 4 definition. Primary (a paper row covering several ledger lines): the e-roster records a long-term sickness
  spell as one row on its first day carrying the spell's hours (270.00 from 29 May 2025, 337.50 from 17 November 2025),
  and the spell runs over the post's clinic days to its next roster line, crossing a quarter each time; the remedy is to
  spread the hours over those clinic days, bank holidays excluded, in numerator and denominator alike. Hazards: vacant
  lines and bank shifts outside the denominator, annual leave inside it, bank holidays not clinic days (spreading the
  November spell over weekdays moves two days from Q4 to Q3), 7.5 hours a day. Stops: the rows on their own dates (42,
  10, 53, 9 days; 9.6, 2.5, 11.5, 2.1 per cent; 0 of 8, asserted); sickness rows counted as days (7, 10, 9, 9; 0 of 4,
  asserted). Golden: 29, 23, 39, 23 days; 6.8, 5.6, 8.7, 5.2 per cent, each rate at least 0.02 inside its cell.
- Separation: the call recomputes unchanged with the hospital-form codes scrambled and reads no roster row (asserted);
  the asks' device rows are hospital-form check-ins and roster lines, none of them a GP-form arrival or a log count.
- Reuse: neither primary repeats a device of the last three builds; the code reallocation and the spell row are bespoke
  to a hospital's systems and screened against the hygiene battery (no duplicate, no unmatched join, no comment, flag or
  code names either).

| Ask | Figures | Cracker (lands the call; UK times, the parallel run once, the log's two layouts; hospital codes joined to the clinic register; roster rows on their own dates under the report's definition) | Verdict |
|---|---|---|---|
| A hospital-clinic visits, seven specialties by quarter | 28 | the current register's codes read as 2025-26's, every cell under the wrong specialty | miss |
| B days lost, four quarters | 4 | the long-term rows' hours taken on their first day | miss |
| B sickness rate, four quarters | 4 | the same | miss |

Measured on the cut pack by `pair.py`: the cracker keeps 0 of 36 ask figures and the mirror (off the call at 42,500,
the same ask routes) 0 of 36. The modelled risk is ask B: a 270-hour day is an impossible row the hygiene battery can
see, and a reader who spreads it over clinic days keeps all eight; with that on both sides the cracker scores 57.2, the
mirror 24.2 and the pair 40.7. The stage 4 reader measures both.

Pair ceiling: 28.5 (cracker 45.0 with 0 of 36 ask figures, mirror 12.0 with 0 of 36, on weights 38, 7 and 55)

Mirror leakage: 0.0 per cent of ask weight

Measured by: generator/pair.py

## Layer 1 inventory

| Mess | System that writes it | File | Natural mishandling | Asserted |
|---|---|---|---|---|
| a parallel-run fortnight in both queue systems | the cutover's double keying | legacy file, events | counted twice | SF6: 45,527, same call |
| legacy times re-keyed, test tickets | the old kiosk, the IT team's tests | legacy file | test tickets kept as visits | R2: no test ticket carries a GP form |
| events in UTC against UK clinic days | the new kiosk's export | events | dates read in UTC | R2: every check-in falls on the same UK date |
| the log's two layouts, month totals, dates typed as text | reception's PALS return | reception log | typed-in dates dropped, totals counted | R2: 2 rows, same call |
| blank practice barcodes, a practice merger | the request forms, the ODS register | events, practices | GP-referred read by practice code | SF1: 426 forms, same call |
| clinic codes reallocated on 1 April 2026 | the PAS replacement | events, clinic register | ask A only | ask A assertions |
| long-term sickness as one row a spell, vacant lines, bank shifts | the e-roster's HR feed | e-roster | ask B only | ask B assertions |
| financial years, bank holidays | the trust's calendar | all | calendar years, bank holidays as clinic days | SF2; ask B |

## Stage 3 gates

To be run in the worktree after the DRAWN commit; the results replace this line.

## Tried and rejected

- The seed's architecture (FC08): the vendor's standard dialling rules withheld from the contract and recovered from its
  acknowledgements, with the callable-number count behind two number-level joins as the decisive unit. Rejected at the
  draw: a rule recovered from settled records is banned as the decisive step, and with the rules filed the callable
  count is rule application; the wash stays as depth on the default path.
- A first card in the seed's world as a bank (`financial_institution`, context artifact `operations_log`): blocked by
  the guard against task128, live beside this build (a Canadian bank's collections centres); the deposit-taker became a
  New Zealand building society and the context artifact the block-order thread.
- The coming list's special as the 2024 three-year special (5.65 per cent onto a 3.00 per cent card): the latest
  campaign's share by term and the share by locked rate within term landed 2 to 3 per cent under the golden, because the
  2026 campaigns' three-year deposits, opened at the 2023 peak, met the same drop. Moved to a 2023 four-year special,
  whose past four-year peers all locked in the 2021 and 2022 lows; every term-based rival now lands 19 to 28 per cent
  short.
- Hours to the nearest 100: with the list's drops on thin past support (0.25, 0.55, 1.50 points) the estimator corridor
  (bands of 0.2 to 0.5 at offsets, logistic, isotonic) spread 110 to 230 hours. The 2027 card was set so the list's
  drops sit on dense past drops (0.45, 1.35, 2.00, 2.30, 2.50), and the block moved to multiples of 250 (SOW 2.2,
  procedure 6.1).
- Hours to the nearest 500: the locked-rate and trend rivals landed all three months, and rounding each month to 500
  stopped the months adding to the block.
- Extract notes that said the certificates in the holdings view were moved to the core and what MIGRATED means: they
  narrated Ask B's overlap; the notes now describe the files' fields only.
- Forum `line_manager_or_team` (the head of deposits signing the block order alone): task136 moved its forum to the same
  key after this card was registered, and `ban.forum` blocked; the Deposits Committee now approves the block.
- Write-up figures rounded coarser than they read: the list's retention-offer share to the nearest 5 per cent (60,
  against 62.1) and its non-reaching dials to the nearest 500 (67,500, against 67,354.8); the judge read both as wrong.
  Now whole per cent and nearest 100 (62, 67,400), with freeze.py allowing the two keys
  (`components.retention_share_pct`, `steps.non_reaching_dials`); the Final Recommendation and Critical Components move
  only by that 60 to 62.
- The judge's wording for the Ask A clause (a deposit counts if any of its maturity proceeds were in a society term
  deposit, its principal the amount in term deposit then): "maturity proceeds" is the transfer extract's narrative and
  points at Ask A's device, and "the amount on term deposit then" reads as the new deposit's whole balance, new money
  included (the whole-principal stop). Filed as: counting a deposit if any of its principal was, and only the part that
  was.
- Round 1 shipped design: weak per the 10/10 audit (COMPLIANT_WEAK), because its decisive step, the share of
  conversations going to the retention offer conditioned on each deposit's drop from its locked rate to the card, was
  the strong model's reflex and the field's textbook model: a logistic of the retention outcome on term with a separate
  locked-rate slope per term booked about 5,496 hours, inside the golden's 5,500 bin, without reading any card; the
  share by locked rate sat one bin under; Ask B's migration batches file announced the overlap and an account-level
  dedup against it cracked the ask; Ask A's clause (a deposit counted if any of its principal was kept, and only that
  part) signalled the partial-move device; and the swap test passed only narrowly (insurance renewals priced off a rate
  card read almost the same). Round 2 keeps the world, the call and the asks' populations and moves the decisive step
  to the class of the money, a reason only deposit repricing behaviour has.
- A market-gap stump for round 2 (each deposit's locked rate against a published market rate for its term and opening
  month, the deposits far above the market leaving): the market table made the premium a visible column and the step
  one join (readability tests 2 and 6); the class is rebuilt from each list's own cohorts instead, with no table naming
  it.
- Other round-2 candidates for the decisive step, dropped at the draw: the term structure of the card alone (still the
  drop, read term by term, the reflex the audit measured); the best card across terms as the rate a deposit is compared
  with (a second reading of the rate it reinvests at, a fork and never a stump); money above the Depositor Compensation
  Scheme's per-depositor cover leaving at maturity (a filed limit executed on a visible principal column, rule
  application read off the schema).
- Round 2's first prototype kept round 1's January to March 2027 card (four years 3.15 per cent, so the special's drop
  was 2.50 points): past special money dominated the 2.50 band, so the share by drop alone booked near the golden, and
  the locked-rate-by-term logit carried the special's deposits at about 0.8. The 2027 card was turned up (four years
  4.00, a drop of 1.65), a band in which past conversations are 89 per cent member money.
- The card's gap reordered to population first: `guard.py check` blocked on `test.same_driver` (population, E,
  forecasting against task124's lineage) and `test.same_puzzle_older`; the gap stays time then population, the honest
  order for a premium that lapses at first maturity.
- January's share of the 2023 four-year special's sales at 0.242: January's hours sat near a rounding edge and the drop
  and term logistic landed January's bin (1,250); the sales by month are now 0.184, 0.408 and 0.408, January's golden
  1,206.9 and that rival's January 1,000.
- Ask B at six figures (each month's maturing principal on and off the list): with Ask B the most obvious device, the
  cracker's pair ceiling rose to 41; cut to four figures (the three months and the quarter's part not on the list),
  39.0.
- Ask A's device as a posting date (D8, maturity proceeds posted on the next business day): the hygiene battery's
  unmatched-join count found it at once; moved to the payments system's settlement account with the matured deposit
  named only in the narrative (D7).
- The write-up's past share for member money (15 per cent, 14.57 unrounded) and all past conversations' share in the
  special's band (35 per cent, 34.55): both within 0.07 of a rounding edge; dropped from figures.json, the write-up, the
  note and the workbook, the band given by class instead (88 and 28 per cent, 0.24 and 0.18 from an edge).
- The note's chart title "Seven in ten hours are conversations, most of them retention offers": under the round-2
  shares January's conversations go to the offer 45 per cent of the time and the retention offer's minutes are under
  half the talk in January and March; retitled to the measured two-thirds (0.665 to 0.693, asserted).
- Band shares as a Critical Component (88 against 28 per cent at drops of 1.50 to 1.75): a corridor member (special
  money pooled, a logistic within each class) never computes them; the component keeps the class's 87 per cent and the
  bands stay in the steps.
- Portal round 1 (2026-10-25): response 1 landed the call exactly, 5,250 agent-hours (1,250, 2,000 and 2,000 by maturity month), so reading each reached holder's retention-offer share by the class of the money (the 2023 four-year special's block at 5.65 per cent against its cohort's 5.15) is a reflex for the portal's model, as the drop was for the audit's; with both the drop and the class spent, the world's deposit behaviour layer has no decisive step left, and the one structural step it still holds (a reached holder's conversation settling the holder's later deposits on the list, so hours follow holders, not deposits) reads the same with a clinic's reminder calls, a backdrop by the swap test.
- Re-root to architecture 2 (2026-10-25): architecture 1 spent on portal round 1 (above); the slot moves to a new
  cell, healthcare-delivery-health-economics / utilization-access-demand-forecasting, with nothing of the seed's world kept.
- Architecture 2 draw, coastal high-water flood days in 2027 from the window's astronomical tide plus skew surge
  (climate-weather-extremes): dead on the slots screen, it is task178's architecture 1, spent at Gate F when a scored
  reader conditioned on the 2027 tide table; the prototype (`tide.py`) had shown 2027's tide-only exceedances 15 to 25
  per cent under 2026's at a semidiurnal port.
- Architecture 2 draw, candidates killed on the lane's dead lists before code: bike-share pairs and pupil yield by
  estate age (task170's ninth cell), event prediction and illness-death states (task171, task174), the disposition
  effect in listings and notification habituation (task177's rate-by-state screens), vacancy chains (too close to
  task166's live junior-on-senior driver), OR-list overruns and clinic slot cascades (task170's replay law).
- Architecture 2 draw, a liability book's back-loaded accident year (`res1.py`, two seeds): the accident-year chain
  ladder missed by -36 to -42 per cent but Bornhuetter-Ferguson and frequency-severity on earned exposure landed within
  5 to 14 per cent: the textbook fallback for an immature year is the golden, so dead.
- Architecture 2 draw, warranty claims on a months-in-service clock a new retail channel delays (`war1.py`, two seeds):
  the shipment-clock default missed by only -2 to -5 per cent; dead on lever.

- Interacting pairs as the decisive step (the registered card's, 2026-10-25, restarted thread): a strong enumerator's own
  pick, so on the enumerable chain. On the generator's world a logistic with the canonical pairs wins out of sample
  (log-likelihood -1,629.7 against -1,741.2 per medicine and -1,641.8 for every two-way pair, 2023 to mid-2025 fitted,
  the next nine months scored), and replayed on the regimens the reviews left it files 191 admissions against the
  golden's 343; the pairs stay as a rung any solver climbs, and the decisive step moves to the stopped medicines'
  restarts.
- The dead thread's restart world with the programme counting as each resident's annual review: the 2027 annual reviews
  then all fall in October to December 2027, and leaving them out filed 9 per cent high, a fork between two readings of
  the procedure; the programme is now additional to the annual review, which continues in its usual month, so an
  implicit stop hazard over every month and explicit 2027 reviews agree within 1 per cent (345.4 against 343.0).
- Start hazards scaled by frailty: the pooled restart clock then sat 3 to 6 per cent under the truth, so a frailty-
  stratified estimator would have crossed a bin; the start and restart hazards are frailty-free and the record's clock
  recovers the truth within 1 per cent.
- Pair partners stopped only where the pair is held, with small main effects for NSAIDs and benzodiazepines: the per-
  medicine model with a pooled start hazard landed within 1 per cent of the golden (two errors of opposite sign); the
  criteria now stop NSAIDs and benzodiazepines in every regular user, their own effects carry most of their harm, and
  that route sits at 329 (4 per cent under).

- The restart clock as the decisive step (the stopped medicines restarted on the record's clock from each earlier
  stop), probed 2026-10-26 on a six-file pack (golden 343.0, nearest 25 = 350; frozen 191 to 220, pooled Markov 295):
  two isolated Opus call-only probes landed it, p137a at 350 (355.4) and p137b at 350 (361.9), each with a monthly
  Poisson rate on the month's medicines and their combinations, frailty and care type, validated on October to December
  2026, every medicine switched month by month with recent stoppers restarting faster and about three in ten stopped at
  an annual review, a leaving hazard and a microsimulation, back-tested on the 2024 and 2025 year-start cohorts within 2
  to 5 per cent. Any transition the record shows as a rate gets measured; dead. Their realism catches carried forward:
  the programme stopped 93 per cent of the NSAIDs and benzodiazepines it reviewed against 31 per cent at annual reviews
  under criteria the schedule called the same; no annual reviews after 26 October 2026; 24 admissions overlapping the
  person's previous stay; discharge dates after the pull.
- The blanket-programme restart curve (the programme's stops restarting like Ferncliffe's 2025 blanket programme rather
  than like selective annual-review stops), prototyped 2026-10-26 before a probe: the pooled clock landed 9 to 17 per cent
  under it and the per-medicine model with the pooled clock within one bin (two errors of opposite sign); set aside
  unprobed for the coordinator's evidence from five probe deaths: every dead step put the decisive attribute on the frame's
  own units, where a thorough modeller joins it and measures it, and the survivors (task305, task306) carry a body the
  frame does not hold; re-registered on the step-down guests.

- The step-down guests as the decisive step (re-registered 2026-10-26, d1f3551d), probed on a six-file pack (probe3):
  Opus probe p137c took the step, filing 500 (502.4) as 407.4 for the long-term residents plus 95.0 for the step-down
  guests (37 drug-event readmissions over 23,576 occupied bed-days, 180 beds at 92.1 per cent occupancy), because Annex A
  split each home's beds into long-term and step-down. No honest rebuild hides them: the golden is determinate only if a
  file states the 2027 step-down beds (an annex, a bed plan, a purchase order or a registration variation), and the
  probe cross-matched every file by NHS number (it found the 81 guests who became long-term residents, none on the
  register); if the trusts' returns carry the guests, they are an unmatched block, and if they do not, the guests' rate
  has no determinate source (an analogue choice is a fork). Dead in this world.
- The households other councils placed in Hartmoor's hotels and hostels as the decisive step (architecture 3's first
  candidate, a borough council's 2027 Part 7 assessments; probe pack probe5, golden 1,400 against the frame's 1,200, never
  registered): Opus probe p137f landed it exactly, 1,400 (1,383) and both asks. The block bookings showed as 655 s208
  notices in Q4 2026 against about 20 a quarter, and normalised addresses linked 151 of the 324 earlier placed households
  to later cases (47 per cent, about 27 per cent within a year), a direct analogue in the same files, carried to the 2027
  window by a Kaplan-Meier curve. Every landing so far had an anomaly that invites a look plus an analogue a join can
  measure; the next candidate keeps the outside body steady and quiet, applies a validated model to a situation the
  record's units never had, ties the body to the quantity by an indirect domain link, and forces its size and rate from
  ordinary data with other uses.
- The serving personnel beside a new urgent treatment centre as the decisive step (architecture 3's second candidate,
  Harrowdown ICB's Wexley UTC, 2027 attendances; probe pack probe6, golden 12,500 against the model's 11,000, never
  registered): Opus probe p137h landed it, 12,500 (12,456.7) and the ask. It ran the model as filed (10,846), then
  calibrated the open centres' other attendances as 0.98 per cent of ICB attendances plus 0.99 times the model's demand
  for the census defence population, a fit that matched all three centres and explained Tolland's higher share by the
  RAF station; it knew the personnel are registered with Defence Medical Services, and it excluded the prison and the
  halls students correctly. Defence was the communal establishment table's largest category, and the open centres
  carried enough of it to calibrate the rate. The next candidate's outside body is small wherever the solver can
  measure it, absent from the open units, concentrated on the new one, and sized from data the model does not use.

- Re-root to architecture 3 (2026-10-26): architecture 2, the care world, is spent on probes (the pairs, the restarts and
  the step-down guests above), so the number moves to urban-regional-science / municipal-service-demand-resource-allocation
  with nothing of Calderbrook kept; architecture 3's first two candidates (above) died at the probe gate before
  registration, and the third, the Tanner Street custody hub (Harrowdown Police's on the probe pack, Calderwick Police's since stage 3), was missed by both probes (`## Draw`).

- Stage 3, ask B as each suite's initial health assessments in each quarter (16 figures): the closures reached only the
  quarters they fell in (six of sixteen cells), so a reader who joined the handover lines and kept the labelled suites
  kept ten; moved to day and night by suite (eight figures), every one of which a closure reaches (B6, B7).
- Stage 3, ask B framed as the custody healthcare tender: a second decision with its own owner (H18); its home is now
  the medical rooms of the same fit-out contract.
- Stage 3, Wendle Cross's refit as the only closure: it reaches two suites; Eastmoor's 19-day flood closure in August
  2025, with its team at Northgate, reaches the other two.
- Stage 3, an overflow booking into Wendle Cross during its refit: the nearest-suite overflow ignored the closure, so
  the arrest records' longest Wendle Cross gap fell inside the refit (22 December to 12 January); a closed suite takes
  no overflow.
- Stage 3, the refit's move at its planned 08:00: assessments of detainees booked before the move but seen after it
  read either way; the move is the minute after the last booking, and Eastmoor's planned closure was set at 14:20 so
  that no assessment of a detainee booked before either closure falls after it (B4, C1).
- Stage 3, co-defendants charged at the first-named defendant's time: the file's charge time served every defendant on
  it, so attaching them at the file's times was right; they are now charged in turn after the first-named defendant.
- Stage 3, every file keyed to its own detention: the co-defendant join was the only reconstruction and the reverse
  unmatched join finds it; 104 of the 2025-26 files now carry the case's earlier arrest, as a remand file does when the
  person was released and arrested again.
- Stage 3, a file matched to its detention by suite and charge time alone: two unrelated Southfields defendants were
  charged at 05:18 on 10 October 2025; the linked arrest is taken first and the charge-time match only where the linked
  arrest is an earlier release.
- Stage 3, the detention clock on UK wall-clock times: a hold across the October clock change came out an hour long;
  the clock is elapsed time in UTC and the remand times are its UK reading.
- Stage 3, remand stream 0 and 1: a cell-hours sum 0.02 hours from its rounding edge and a hold within two minutes of 24
  hours; stream 8 clears both (A4, A5).
- Stage 3, the probe pack's personas (Charlene Dale, Hugh Metcalfe): `guard.py names --geo GB --seed 137` does not give
  them; replaced with Liam Clayton and Emma Roberts from that draw.
- Stage 3, the BTP part as a graded figure to the nearest 10: the four sizings print 260, 270, 280 and 290; the part is
  stated with its method in the write-up and only the call is graded on its print.
- Stage 3, the city and force named Harrowdown (the probe pack's name): it contains Harrow, a real London borough
  with its own school, and is the name of a real Oxfordshire hill (H21); renamed Calderwick, with the estate's postcodes
  moved off the real HD and CV areas to unassigned ones (CK, CL). No figure moved.
- Stage 3, the prompt's question without the catchment: the estimand read only "the detentions the hub will book";
  it now names the six city centre wards the hub takes over, which is model 2.1's population and the domain's
  catchment (H20).
- Architecture 3 spent at stage 4 (2026-10-26, on d1d38e72): the determinism judge returned DETERMINISTIC on every
  committed figure with disposition SEND_BACK. Gate G read the call as a single conceptual flip (stumping family
  surface_read_rejection, surface_read_dependency yes, sole_data_defect yes) and Gate H its decisive step as
  data_semantics: the flip rests on the brief's coverage line ("one row per arrest by a Calderwick Police officer") and
  allocation note 2, and any BTP figure from 121 to 371 rounds to 4,000, so once the note is read nothing analytical can
  go wrong. Both scored readers landed 4,000: reader A (Sonnet) quoted note 2 as the decisive-step sentence (5 of 21 ask
  figures, 23.8 per cent, all five the chart's years; score_reader exit 1), and reader B (Opus, 3,754 plus about 265 BTP)
  wrote that what flips the answer between 3,750 and 4,000 is close to reading a stated rule and a field's definition.
  Neither took an ask figure: both re-keyed the files carrying a case's earlier arrest and missed the co-defendants, and
  both counted the closed suites' teams at their own suites. The probes missed only while the coverage fact was unfiled;
  filing it, which determinism needs, makes it semantics and lands it, so the same fact cannot be both Gate B's pin and
  silent. The judge's other findings, kept for the record and not fixed: pin 19:00 (nine first assessments start
  exactly then), pin the assessment unit and the "where it happened" wording, say defendants are counted from the arrest
  records, and the model PDF's header still reads HARROWDOWN POLICE (an upper-case leftover of the rename); reader B
  also flagged the HDL licence prefix and four arrests at the spring clock change booked before their arrest time (a
  local time in the skipped hour converted as GMT). By build-pipeline an architecture is spent on a SEND_BACK, and the
  retirement rule applies to this third spent architecture unless the author sets another cap; that decision is the
  author's, and no architecture 4 is drawn.

- Re-root to architecture 4 (2026-10-26): architecture 3 spent at stage 4 (above) and the author's ruling the same day
  that task137 is neither retired nor paused; the number moves to healthcare-delivery-health-economics /
  utilization-access-demand-forecasting with nothing of Calderwick kept.
- Architecture 4 backup candidate (probe8, 2026-10-26, never registered): Kestermoor District Council's 2027-28 Annual Tonnage Nomination to the Thrumley ERF, kerbside residual after a staggered weekly food waste rollout (two caddy-only pilot waves, then three waves that also swapped in a 180-litre residual bin, the 48-round wave 4 six periods in, wave 5 live from 2027-28 period 1), golden 53,000 against 55,000 to 58,000 for the static and pooled TWFE routes; died on Opus probe p137lb, which landed 53,000 (53,174.5) by comparing each wave period by period with wave 5, the one not yet treated, splitting the two packages and running wave 4 along wave 3's path: the package column in the rollout schedule hands over the clean comparison by package, so a staggered rollout with a documented package split is a reflex for the probe model, not a stump.
- Architecture 4 draw, explorer B's families: demand censored by capacity and vintages, never the staggered rollout. The
  recapture form (a patient turned away comes back on a later day and is counted twice, so only the refusals that never
  return are demand the record missed) was dropped before code: a regression of later days' visits on the turned-away
  counts is the opponent's own return check, which both probes then ran unprompted on probeB1. The deterrence form
  (a week of run-outs keeps the next week's patients away) went to the probe pack.
- Architecture 4 probe pack probeB1 (seed 16, a deterrence of 0.30 on every arrival, golden 54,000 against the default
  51,000 at the nearest 1,000): both Opus probes missed (`## Draw`), but its own rolling five-day share attenuated to
  52,000 (52,046) and its clean-day fits printed 49,000 and 52,000, forks a full pack could not ship.
- Stage 2 prototypes v2 and v3 (the deterrence on every arrival, the run-outs from staffing shortfalls): whenever the
  run-outs were scattered the rolling-window members attenuated a cell under the previous-week share, and a vacancy
  overlapping a surge gave the vacancy a t of 3 or more. The run-outs now come mostly from the hospital clinics' recall
  programmes, which run for weeks; the vacancy sits in summer; the bank backfills the long-term sickness lines; so every
  window files one call and staffing has no effect of its own (t 0.29 for the vacancy, -0.20 for staff on the floor).
- The deterrence on every GP-referred patient: it is now held by the seven practices with their own phlebotomy clinics
  (arrivals times exp(-0.45 x the previous week's run-out share)), the five without one untouched, so the step is a
  referral pattern the request forms' practice codes show rather than a property of every patient.
- The plan to the nearest 1,000: the deterrence specifications spread 44,035 to 45,114 across two cells. At the nearest
  2,500 they sit in one (43,750 to 46,250), with the default (42,561) and both careful-frame methods one cell under.
- A practice barcode blank on 3.1 per cent of GP forms: a solver counting GP-referred visits by practice code would
  have moved the call; 0.6 per cent now (426 forms), the same call either way (SF1).
- The annual report's sentence on the hospital clinics' recall programmes (which months each specialty recalled its
  patients): it named the run-outs' driver and made the GP dips readable beside it; removed, the programmes show only
  in the hospital-form visits by clinic code, which ask A counts.
- Personas outside the seed-137 draw (Liam Clayton, carried from architecture 3) and from it with first names older
  builds use (Rachel Reynolds, Patricia Bryant; Richard, Rebecca and Duncan also warn): replaced with Charlene Dale,
  Bethan Matthews and Joseph Wood from `guard.py names --geo GB --seed 137`.
- Strategy `causal_design` on the card: `ban.strategy` against task121's architecture 6 inside the three-build window,
  and `informative_censoring`, the nearest key, is task487's; filed as `other`.
- Brantmoor Community Hospital's booked clinic left unstated: with the turned away offered a booked slot there, "the hub
  takes every patient with a GP request, walk-in and booked" left open whether Brantmoor's own booked patients move to
  the hub, which no file counts; the annual report now says the booked clinic at Brantmoor carries on as now (SF10).
- A family-spread assertion at 0.4 of the printed unit: the 27 specifications spread 0.43 (44,035 for the programme-week
  dummy to 45,114 for the quiet-period fit over ten clinic days), every one at least 285 inside the cell; the assertion
  is one printed cell and a spread under 0.45, with the figure stated rather than the family trimmed.
