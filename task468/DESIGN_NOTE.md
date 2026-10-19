# task468 design note: the specialty clinical pharmacists, by the spend the members on therapy will run

Status lives in `pipeline.json`; this note holds the design of architecture 2. Read `## Tried and rejected` first.
Architecture 1 (the Larkhaven transit nominations) is spent; its record is in the card's lineage and the lines below.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task468.json` (architecture v2), registered 2026-10-19 after a pull. Guard
  check PASS after redrawing the role family (capacity_planner and the filed-standard artifact repeat task248 and
  task249), the decisive generator (G13, horizon, ahead of G6 and G14, which task268 and older builds hold) and one
  differentiation line against task98 v6. Shape 01 is banned by the last two builds (task268), so the call is an
  allocation (shape 05).
- **Pairing:** Healthcare Delivery & Health Economics / payment-claims-health-plan-analytics / Data Extraction &
  Conformation (ETL). Two pharmacy benefit managers' specialty claim files (the outgoing PBM's to December 2025, the
  incoming PBM's from January 2026) are conformed into one record of fills by member, drug class and month, repriced at
  the incoming PBM's contract prices; the call is the program's staffing, which turns on what that record says the
  members now on therapy will cost over the program year.
- **Shape:** 05, an allocation to a fixed total: the plan's Specialty Clinical Pharmacy Program staffs 24 clinical
  pharmacists across eleven specialty classes for July 2026 to June 2027, each class's share of the 24 set by its share
  of the spend the program will manage (the members on therapy at 30 June 2026, their fills in the class over the
  program year at the 2026 contract prices), whole pharmacists by the largest remainder. Criteria: eleven classes'
  pharmacists, eleven classes' projected spend, the most-staffed class and the asks.
- **Strategy:** composition_mix (the members on therapy are a mix of durations on therapy, and the mix differs by class
  and from last year's), decisive generator G13 (the program year is a horizon the trailing record does not cover at
  today's durations), with G6 and G14.
- **World:** the United States, an unnamed state. Merrow Health Plan, a nonprofit regional plan (about 210,000
  members). Its pharmacy benefit moved from Orrin Rx (to 31 December 2025) to Tallis Pharmacy Services (from 1 January
  2026). The plan added weight-loss GLP-1 coverage in January 2026; a hepatitis C outreach drive ran from May 2025. The
  Specialty Clinical Pharmacy Program (adherence calls, side-effect management, refill coordination) has 24 clinical
  pharmacists for the program year from 1 July 2026; its charter staffs each class by its share of the spend the program
  manages. Personas from `guard.py names --geo "United States" --seed 468`: Erik Marks (Director of Pharmacy), John
  Henry (the plan's pharmacy data analyst), Caleb Fischer (Tallis's account manager).
- **Forcing fact:** the program year began on 1 July 2026 and the staffing goes to the plan's executive team on 4 August
  2026 with the claims through 30 June. The call faces forward: the spend is the twelve months from July 2026.
- **Forum and forcing event:** executive_team, budget_or_appropriation; org family other (a nonprofit health plan, an
  insurer); role operations_director.
- **Data-native sentence:** a specialty drug's monthly spend on a member depends on how long the member has been on it
  (loading doses in the first fills, a hepatitis C course that ends after eight or twelve weeks, the steep early
  discontinuation of oral oncology and the weight-loss drugs, the near-lifelong persistence of HIV and multiple sclerosis
  therapy), and the classes' members on therapy in June 2026 sit at very different durations: the weight-loss class
  filled with new starters after its January coverage change and the hepatitis C outreach with short courses, while
  oncology's current users are the minority who survived the early months; so the trailing year, the June run-rate and
  last year's cohort each mis-state exactly the classes whose current users are unusually new or unusually seasoned.
- **The WHAT screen.** Population: the members whose fill in a class covers 30 June 2026 (the charter names them);
  outcome: the plan's paid amount for their fills in that class from 1 July 2026 to 30 June 2027 at the 2026 contract
  prices; window: those twelve months; unit: dollars, then whole pharmacists; comparison: each class's share of the
  eleven classes' total, the 24 by the largest remainder. The decisive step settles none of them: it is how the
  members' unobserved next twelve months are estimated, from a record where every past member's months on therapy
  show the shape (HOW, forced by the data's structure: classes and durations separate the candidate methods).
- **Sources, one line each:**
  - `stumping/references/client/layer2-rigor-patterns.md`, payment-claims 1 and 4: completion and ratio-of-totals
    exposure; here the exposure is months on therapy and the projection is a development conditional on duration,
    which no build on file carries (task451 completes claims by lag, task458 counts conditions by look-back).
  - `stumping/references/strategies.md` F1 and F5: a clock process already in the data, estimated from every unit
    that went through it (134 v2, 107 v4), and a pool whose duration mix moved (the weight-loss surge).
  - `dataset-generation/references/layer1-messiness.md`: two PBM layouts, reversals and rebills, re-keyed member
    identifiers, NDC formats, contract repricing, transition fills; none on the decisive step.

## Default path

1. Conform `orrin_rx_specialty_claims_2022_2025.csv` and `tallis_specialty_claims_2026h1.csv`: net reversals, link
   members through the PBM crosswalk, map each NDC to its class through the drug reference, reprice each fill at the
   2026 contract price.
2. Take each class's members whose last fill's days' supply covers 30 June 2026.
3. Project each class's spend for July 2026 to June 2027 as its spend over July 2025 to June 2026 (or June 2026 x 12),
   or, more carefully, as the class's members on therapy at 30 June 2026 times the following-year spend per member of
   the class's members on therapy at 30 June 2025.
4. Allocate the 24 pharmacists by the shares, largest remainder.

Ends on: last year's cohort's following-year spend per member applied to this June's members: the weight-loss class
takes pharmacists from oncology and the persistent classes (figures in `## Ladder` once calibrated).
Golden: each class's development by months on therapy (continuation and paid amount at each month since first fill,
from every member who passed it) applied at each current member's own duration.

## Stump sentence

The default path projects each class's members on therapy at 30 June 2026 by the following-year spend per member of
last year's members on therapy and staffs the weight-loss class above oncology, because the weight-loss class's
current users are mostly 2026 starters who will mostly stop within months, while last year's were the survivors of a
smaller, older intake; the development by months on therapy at each member's own duration gives oncology and the
persistent classes the pharmacists.

## Three rules

Task type: payment-claims-health-plan-analytics: two PBMs' specialty claim files conformed into one repriced record of fills by member, class and month, from which each class's program-year spend for the members now on therapy is projected, a task type serving Data Extraction & Conformation (ETL).

Domain test: the deciding quantity is each specialty class's paid amount over the program year for the members on therapy today, and the field's estimator is a persistence-and-cost development by months on therapy (loading doses, fixed hepatitis C courses, early discontinuation), applied at each member's own duration; carrying the trailing year, the June run-rate or last year's cohort forward each moves pharmacists between classes.

Swap: "the hospital's wards staffed by the bed-days their current inpatients will use" keeps an arithmetic shape but loses why it moves: there is no loading dose, no fixed eight- or twelve-week course and no months-on-therapy discontinuation curve in a ward census, and the weight-loss coverage change that filled one class with new starters has no counterpart.

Layer 1: Orrin Rx's file with reversals as negative lines and rebills; Tallis's file with a claim status column, its own member numbers linked through the plan's crosswalk, 11-digit NDCs against Orrin's 10-digit; Orrin's paid amounts against Tallis's 2026 contract prices; transition-of-care fills in January 2026; 28-, 30-, 84- and 90-day supplies. Each is the PBMs' systems as they run, asserted neutral for the call.

Layer 2: forecast_uncertainty, a development of spend by months on therapy conditional on the duration each current member has reached, estimated from every member who has passed each month since first fill.

Decisive step: projecting each class's members on therapy by the class's own continuation and paid amount at each month since first fill, starting each member at the duration they have reached, instead of last year's cohort, the trailing year, the June run-rate or a curve applied from first fill.

Not semantics: every field read correctly (reversals, crosswalk, NDCs, contract prices, days' supply, the charter's population and window) still leaves the easy route projecting this June's members by last year's cohort, because no field says how long a member has been on therapy or that the weight-loss class's mix of durations moved; the durations have to be built from each member's first fill across both PBMs' files.

Not rule application: the charter fixes the population, the window, the prices and the allocation; no rule or procedure says how the members' next twelve months are projected, and executing every filed rule with last year's cohort staffs the weight-loss class above oncology, so the step no rule performs is the development by months on therapy.

Analyst test: a strong analyst who conforms both files and reads every charter rule projects this June's members on therapy by last year's on-therapy cohort's following-year spend per member and allocates the 24 pharmacists on those shares, giving the weight-loss class pharmacists that belong to oncology and the persistent classes (the default path's Ends on); the development by months on therapy gives the golden allocation.

Estimand: the Specialty Clinical Pharmacy Program charter (the members whose fill in a class covers 30 June 2026; the plan's paid amount for their fills in that class from 1 July 2026 to 30 June 2027 at the 2026 Tallis contract prices; each class's share of the eleven classes' total; 24 pharmacists by the largest remainder), in the charter PDF.

No decoy: nothing is planted; the claim files are the PBMs' extracts as delivered, the drug reference and price list are the PBM's, and no memo, draft or briefing argues a projection method or a staffing.

No certified replay: no published or certified figure reproduces under one projection only; the charter's prior-year staffing is the program's actual history, not a test of a method.

Lesson: a cohort's forward cost is its development at the durations its members have reached, and last year's cohort stands for this year's only when the mix of durations has not moved; the decisive skill is to rebuild each member's duration from the record and develop from there, which no build on file teaches in a claims record.

## Tried and rejected

- 2026-10-17, at the draw: Urban & Regional Science for a transit seed: none of its task types serves ETL, so the
  pairing cannot be filed.
- 2026-10-17, at the draw: a passenger's average wait from the timetable's gaps (half the mean gap against the
  length-biased mean): generic arithmetic of any periodic service, so the domain reads as a backdrop, and it is not the
  data-integration task type's method (it survives as Ask C's device, which the 10/10 rules leave free).
- 2026-10-17, at the draw: two operators' stops linked across feeds to build combined corridor frequency: the right
  link is read off direction and stop sequence, a field reading, and the guard's identity risk lands on it.
- 2026-10-17, at the draw: delivered frequency from the planned schedule less cancellations cancelled by whole runs:
  needs a dispatch log, and a complete log counts delivered departures exactly, bypassing any estimate.
- 2026-10-17, stage 2: the review as a simple random sample of the unmatched events, its raw route mix the decisive
  step: a single insight the review file signposts (133 v1 died on a development sample pointing at its decisive
  step); the review is now a bus-day sample with one event each, so using it is R2 and weighting it is the move.
- 2026-10-17, stage 2: the composition varying by time band (trunk routes late in the afternoon only, pull-in deadheads
  at night): pooled and band-level shares gave different calls on Route 17, a grain fork (H14); lateness now flat
  through the day and out-of-service movements spread over it, so every stratification agrees.
- 2026-10-17, stage 2: Riverside failing on a four-an-hour timetable: Good Friday's Saturday service pulled its
  timetable average under four too, so the timetable rung landed on the golden; Riverside now runs five an hour and
  its afternoon runs went a quarter short of operators.
- 2026-10-17, stage 2: each candidate's lowest hourly average graded to one decimal: the weighted variants spread up
  to 0.3 on Route 2, so the prompt asks for the verdicts and the workbook carries the figures as supporting detail.
- 2026-10-17, stage 3: on-time shares to one decimal of a per cent: two routes' shares sat within a hundredth of a
  rounding edge, so the shares are graded to the whole per cent (every share further from its edge than one departure
  moves it, asserted); Hillcrest's lateness and timetable jitter moved so its share and its wait sit clear of their edges.
- 2026-10-17, stage 2: a scheduled-departures table from both feeds as an ask: a GTFS-literate cracker executes the
  calendar, calendar_dates and frequencies correctly, so no device held; replaced by the waits (an analytical device).
- 2026-10-17, stage 4: Ask A, Quinnell's April to June record by stop and service-day month: both outside readers
  found the file-head repeats by bus, stop and second and assigned the service days, the judge read the repeats as a
  fork, and no silent device reaches the record without touching the review's frame; dropped (the repeats, the 31
  March copy and the after-midnight service stay as Layer 1 on the call's path, asserted neutral).
- 2026-10-17, stage 4: Ask C, the scheduled wait on 13 May: the prompt's definition made the waiting-time paradox a
  literal integral both readers computed, the frequency window's end read two ways, and no representation of the feed
  hides a departure from a careful reader; dropped (the frequency trips now exact times, each block ending between
  two trips).
- 2026-10-17, stage 4: the on-time device as Quinnell's DeviationSec taken at arrival: both readers timed the
  departures from the timestamps and read the field as noise, and guidance 4.2's "as the AVL system records it"
  invited it; DeviationSec is now the departure against ScheduledDeparture, and the device is Arbor's minute-held
  schedule against the feeds' half minute.
- 2026-10-17, stage 4: Route 6's on-time share at 47.46, 0.04 from its edge (a reader rounding to one decimal first
  filed 48): the half-minute bands, set per transfer point, put every share at least 0.19 from its edge.
- 2026-10-17, stage 4: the eleven candidates named only by route colour in routes.txt (the judge's Gate B and E
  finding): Planning's candidate list now ships with each route's designated stop.
- 2026-10-17, stage 4: the on-time device as Arbor's minute-held schedule against the feeds' half minute: judge pass 2
  read the two schedule sources as an open fork (FIX_NOW), the pin naming the published timetable in guidance 4.1 and
  4.2 closed it, and reader round 3 then timed all eleven shares against the feeds. A device whose basis a filed
  sentence must name dies with the pin, and every other column the ask reads (the departure, the trip tie, the window,
  the days) is the call's own population, so no device on this ask can stay off the call's rows.
- 2026-10-19, repair: the stop-hour grain fork (reader round 3): the review drew 250 bus-days a month, so the
  stop-by-clock-hour cells held one to seven reviewed events and the minimum of thirteen noisy hourly estimates sat
  biased low; at 400 bus-days a month, with the within-bus-day draw on its own stream, every weighted grain (stop, stop
  and hour, band, month, vendor, the within-bus-day weight, counting-day reviews) files the golden and every raw grain
  the R2 slate (checks.py R3b, verify.py's stop-hour estimator).
- 2026-10-19, repair: replacing the dead on-time ask, measures tried on paper and dropped: the average scheduled wait
  (computed exactly from the feeds by any GTFS-literate solver, and "a weekday of current service" splits on the class
  days); missed trips from a dispatch log (it would hand every solver each route's delivered departures, the call's own
  quantity); APC boardings at the designated stops (doors open only in service, which would identify the out-of-service
  passes the review estimates); the fleet roster's asset tags moved between buses (it would move the review's bus-day
  join on the call's path); evening and Saturday counts (Quinnell's repeats and the cutover overlap are seen, not
  silent). The shelter ask takes none of the call's rows.
- 2026-10-19, architecture 1 spent (the transit nominations): four isolated readers landed the call, so the review
  weighted by its design was read off the memo's sampling procedure by every careful solver (Gate F, score_reader exit
  1), and judge pass 3 found the shelter ask NOT_DETERMINISTIC (no file states the moved-stop rule, and stating it
  hands over the device). The author chose to re-root.
