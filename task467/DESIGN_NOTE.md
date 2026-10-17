# task467 design note: Velmont's 2027 taxi pickup fee

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first: seven architectures
were weighed for this seed and dropped before the card was registered.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task467.json` (architecture v1), registered 2026-10-17. Guard check WARN
  only. Answered: Gate G decomposition_attribution repeats task266, whose split is a program's completions among
  competing endings in an event history; here the split is one series' fall between a temporary rank and a permanent
  rail line that began the same day, read against a comparison series within the line's station zones, and the batch
  varies elsewhere (gap time, a dial, shape 04, a causal-design strategy, a board of directors, a Canadian airport
  authority). Redrawn at the check before registering: gap population with pattern E and Gate G
  decomposition_attribution blocked as a spent signature (task107, task129, task36, task44), so the decisive gap is
  time (the base year carries an arrangement the budget year reverses) with population second; Amy and Michael (first
  names in older builds) replaced from the same draw; deliverables docx and csv (csv and pdf repeated task466).
- **Seed:** ET24 (an airport ground transportation team budgets next year's revenue from the per-trip fee on taxi
  pickups, from monthly trip-record drops; a fee column that changed case and a fee that changed price). Kept: the
  world (an airport authority's per-trip taxi pickup fee, the regulator's monthly trip drops), the decision (next
  year's fee revenue, here the cost-recovery fee it sets) and the quantity (next year's fee-liable pickups). Dropped:
  the seed's mechanism rows (the column's case, the fee's step), which are data semantics; both survive only as Layer 1,
  each asserted neutral for the call.
- **Pairing:** Survey Research & Official Statistics / seasonal-adjustment-official-time-series-production / ETL, own
  pattern "a temporary break and a permanent one that began the same day, separated against a comparison series within
  the components the permanent one acts on". The authority's official monthly series of airport taxi pickups and
  drop-offs is conformed from the Vehicle-for-Hire Office's monthly Parquet drops (schema and timestamp changes, void
  rows, late records, a republished drop) and its 2023 archive, then restated to the loading arrangement the budget
  year will have; the restatement is the time-series producer's intervention adjustment, and SROS is a methods domain,
  so the swap is of the method: replacing the component-wise intervention estimate with the series' own break or the
  aggregate comparison moves the fee.
- **Shape:** 04, one dial: the 2027 pickup fee in 25-cent steps; every setting from $5.50 to $7.25 gets its 2027
  revenue on the restated base and its surplus or shortfall against the program budget, with the call, the restated
  base, the rank's effect and the flip; the conformed monthly series and the asks add the rest.
- **Strategy:** causal_design, the comparison the design implies. The temporary rank (4 November 2024 to 31 December
  2026) and the Airport Line (opened 4 November 2024) began the same day. The rank touches only pickups; the line takes
  riders in both directions, but only on trips to and from the zones its stations serve, and the airport's taxi
  drop-offs come from those zones far more often than its pickups go to them (business travellers ride from downtown
  offices and hotels to the airport and home to the suburbs when they return). So the pickups' own fall carries the
  line, the aggregate drop-off comparison carries the zones' different shares and shows almost no rank effect, and only
  comparisons within the station zones and within the rest, which agree, recover the rank's effect (a Simpson's paradox
  across strata in the aggregate comparison). Gap time (the evidence year holds an arrangement the decision year
  reverses) with population second; generators G6 (the comparison series' mix), G14 (the pooled comparison does not
  apply), G13 (the budget year's arrangement differs from the base year's); pattern E (an absolute split, the confounder
  controlled by construction, no column naming it); Gate G decomposition_attribution.
- **World:** Canada, an unnamed province. Velmont International Airport (about four million passengers a year) is run
  by the Velmont Airport Authority, a not-for-profit corporation with a calendar fiscal year. Licensed taxis pay the
  Authority a fee for each trip they begin at the airport; the Authority bills each taxi brokerage monthly from the
  City of Velmont's Vehicle-for-Hire Office trip records, and its Ground Transportation Fees By-law sets each year's
  fee at the lowest multiple of 25 cents at which the year's budgeted fee-liable pickups recover the Ground
  Transportation Program's budget. Finance Policy FP-07 budgets fee-liable pickups as the most recent complete year's,
  restated for any change in taxi loading arrangements (the location and operation of the taxi rank and holding lot)
  between that year and the budget year, with no traffic growth. On 4 November 2024 the forecourt reconstruction
  around the new Airport Line station began, the day Velmont Transit opened the line (Airport, Commerce Park,
  University, Midtown and Central stations), and taxis moved to a temporary rank on the parkade's Level 2 road; the
  forecourt rank reopens on 1 January 2027. The Vehicle-for-Hire Office publishes each month's taxi trip records as
  Parquet about five weeks after the month ends; the Authority pulls the trips that begin or end in zone 1 (the
  airport) and has kept every pull since January 2024; 2023 survives only as the Office's daily origin-destination
  archive.
- **Forcing fact:** the Authority's board approves the 2027 budget and the 2027 fee schedule in December 2026; the
  budget package goes to the Finance and Audit Committee first. The call faces forward: the fee charged on every 2027
  pickup. As-of: 16 October 2026, the date of the finance manager's memo, after the August 2026 drop (published
  2 October) and before September's.
- **Forum and forcing event:** board_of_directors (the Authority's board), budget_or_appropriation (the 2027 budget
  that carries the fee). Organisation utility_or_infrastructure; role finance_controller. Personas from `guard.py names
  --geo Canada --seed 467`: Olivia White (the Authority's manager of ground transportation finance, who brings the fee to
  the board), Joseph Heath (the Authority's director of ground transportation, who signed the temporary rank notice)
  and Johnny Houston (the Vehicle-for-Hire Office's open data coordinator, who signs the drops' change notes).
- **Data-native sentence:** the Airport Line took taxi riders in both directions but only on trips to and from the
  zones its stations serve, and the airport's taxi drop-offs come from those zones far more often than its pickups go
  to them, so all drop-offs fell almost as far as all pickups when the line opened the day the rank moved, although
  only the pickups moved rank; within the station zones and within the rest, the pickups fell the same share more than
  the drop-offs, and that share is the rank's.
- **The WHAT screen.** The estimand's five parts are filed. Population: the fee-liable pickups of 2025 (every trip a
  licensed taxi began at the airport, voided trips out; the by-law and FP-07). Outcome: those pickups restated to the
  forecourt rank, the loading arrangement 2027 will have (FP-07, which defines a taxi loading arrangement as the rank's
  and holding lot's location and operation, so the line is not one). Window: calendar 2025, the most recent complete
  year. Unit: trips; the fee in dollars, rounded up to the next 25 cents. Comparison: the program budget for 2027. The
  decisive step settles none of them: it is how the filed counterfactual (2025 with the forecourt rank) is estimated,
  and the data's structure (the line's footprint and the two directions' different zone shares) rules out the series'
  own break and the aggregate comparison.
- **Sources, one line each:**
  - `stumping/references/client/layer2-rigor-patterns.md`, seasonal-adjustment-official-time-series-production 1 (model
    level shifts in regARIMA before seasonal filtering, the event's date and type given): here both events' dates and
    types are given, and the step is splitting one dated fall between a temporary and a permanent change with a
    comparison series, which the listed pattern does not cover.
  - `stumping/references/client/two-layer-task-design.md`, estimand and identification (the right counterfactual,
    Simpson's paradox across strata): the client's own family; here the paradox sits in a comparison series whose
    strata mix differs from the treated series'.
  - `stumping/references/strategies.md` F8 and F1 (never a dated cause found by an event study): the dates here are
    filed and the fall is visible; an event study finds the combined fall, the reflex control finds a wrong split, and
    the step is the comparison's design within the line's footprint.
  - `dataset-generation/references/layer1-messiness.md`: monthly drops with schema drift, local time against UTC, void
    rows, late records, a republished drop, a fee that steps each 1 January; none on the decisive step, each asserted
    neutral.

## Default path

1. Read the Ground Transportation Fees By-law: the 2027 fee is the 2027 Ground Transportation Program budget divided by
   the 2027 budgeted fee-liable pickups, rounded up to the next 25 cents.
2. Read FP-07: the budgeted pickups are 2025's fee-liable pickups restated for any change in taxi loading arrangements
   between 2025 and 2027, with no traffic growth.
3. Union the monthly drops (the fee column's case normalised), convert the timestamps from UTC to local time from the
   drop where the meters switched, drop each void row with its original, place late records by their pickup time, and
   count 2025's trips beginning in zone 1: about 149,000 fee-liable pickups.
4. Read the rank notice: the temporary rank opened on 4 November 2024 and the forecourt rank reopens on 1 January 2027,
   so 2025 is restated to the forecourt rank.
5. Measure the rank's effect as the fall in pickups when it opened, the twelve months from November 2024 against the
   twelve months before (the 2023 archive supplying November and December 2023): about 21 per cent, so 2025 restates
   to about 189,000 pickups.
6. The program budget over the restated pickups is about $5.69 a trip; round up to $5.75.

Ends on: $5.75 a pickup

Golden: $6.50 a pickup

## Stump sentence

The default path restates Velmont's 2025 fee-liable pickups by their whole fall when the temporary rank opened on
4 November 2024 and sets the 2027 fee at $5.75, but the Airport Line opened that day and took taxi riders in both
directions to and from its station zones, so the fall carries the line, which stays in 2027; the analyst who controls
for the line with all the airport's drop-offs finds the rank cost only about 4 per cent and sets $7.00, because the
drop-offs come mostly from the station zones; within the station zones and within the rest the rank cost about 11.5 per
cent in each, and the fee is $6.50.

## Three rules

Task type: seasonal-adjustment-official-time-series-production: the Authority's official monthly series of airport taxi pickups and drop-offs, conformed from the Vehicle-for-Hire Office's monthly Parquet drops and its 2023 archive and restated to the loading arrangement the budget year will have across a temporary rank that began the day the Airport Line opened, a task type serving Data Extraction & Conformation (ETL).

Domain test: the deciding quantity is the temporary rank's effect on the monthly pickup series, the intervention a time-series producer removes to restate the series to the budget year's arrangement; with a permanent change beginning the same day, the series' own break carries both, and the comparison series (drop-offs) carries the permanent change's components in a different mix, so the effect is read component by component, and replacing that with the series' own break or the aggregate comparison (the generic intervention estimates) moves the fee from $6.50 to $5.75 or $7.00.

Swap: "a hospital's monthly admissions restated for an admissions desk moved the day a walk-in clinic opened, against its discharges" keeps the shape, because in a methods field the setting is always another field's; the swap is of the method, and the restatement fails the moment the component-wise intervention estimate is replaced by the series' break or the aggregate comparison, while the fee rule, the rank, the line's station zones and the two directions' zone shares are the airport's own.

Layer 1: the Vehicle-for-Hire Office's monthly Parquet drops (the fee column renamed in case from the July 2025 drop; meter timestamps in local time until the June 2025 firmware change and in UTC after it; voided trips as a negative-amount row beside the original; store-and-forward trips arriving in the next month's drop; a republished March 2026 drop beside the original), 2023 kept only as the Office's daily origin-destination archive, the fee stepping each 1 January while meters are reprogrammed over the first weeks, and the Authority's monthly billing statements by brokerage, which bill late trips as prior-period adjustments; each asserted neutral for the call (checks.py R2).

Layer 2: estimand identification, the right counterfactual: a temporary intervention that began with a permanent one is measured against the comparison series within the components the permanent one acts on, because the aggregate comparison mixes components the two series carry in different shares (a Simpson's paradox across strata).

Decisive step: measuring the temporary rank's effect as the pickups' change against the drop-offs' change within the taxi zones the Airport Line serves and within the zones it does not (about 11.5 per cent in each), which restates 2025's pickups to about 168,500 and sets $6.50; the pickups' own fall (about 21 per cent) sets $5.75 and the aggregate drop-off comparison (about 4 per cent) sets $7.00.

Not semantics: every field, code, unit and definition read correctly (the zones, the switch to UTC, the void rows, the fee column's case, the late records, a taxi loading arrangement as the rank's and holding lot's location and operation) still leaves the easy route reading the rank's effect off the pickups' fall or off all pickups against all drop-offs, because no field says that the line acts only on its station zones or that the two directions carry those zones in different shares; the step is the comparison's design, not a reading.

Not rule application: the by-law fixes the fee from the budget and the budgeted pickups and FP-07 fixes the base year, what is restated and that no growth is assumed; no rule or procedure says how the rank's effect is measured, and executing every filed rule with the pickups' own fall files $5.75, or with the aggregate comparison $7.00, so the step no rule performs is the comparison within the line's footprint.

Analyst test: a strong analyst who conforms every drop and counts 2025's fee-liable pickups correctly restates them by their fall when the rank moved and sets $5.75 (the default path's Ends on), and one who also controls for the Airport Line with all of the airport's drop-offs finds about 4 per cent and sets $7.00; the within-zone comparison sets $6.50.

Estimand: the Ground Transportation Fees By-law (the year's fee is the program budget over the year's budgeted fee-liable pickups, rounded up to the next 25 cents; a fee-liable pickup is a trip a licensed taxi begins at the airport, a voided trip not being a trip) and Finance Policy FP-07 (budgeted fee-liable pickups are the most recent complete year's, restated for any change in taxi loading arrangements between that year and the budget year, with no traffic growth; a taxi loading arrangement is the location and operation of the taxi rank and holding lot).

No decoy: nothing is planted to be caught; the drops are the Office's records as published, the rank notice and the transit bulletin describe their subjects, no memo, draft or briefing argues a method or a figure, no document computes a restatement or a fee, and the passenger statistics and the 2023 ground access survey are what the Authority keeps.

No certified replay: no published or certified figure reproduces only under one method; the billing statements are the Authority's own monthly bills, which every reading reproduces, and nothing is recovered by matching a filed number.

Lesson: a temporary change and a permanent one that begin the same day are separated against a comparison series only within the components the permanent one acts on, because the comparison series can carry those components in a very different mix and hide the temporary change almost entirely in the aggregate; no build on file restates a series across coincident breaks or reads an intervention against a comparison series whose component mix differs.

## Tried and rejected

- 2026-10-17, at the draw: a moving-holiday stump (Eid al-Fitr, Lunar New Year or Easter falling in a new month of
  the budget year): each fiscal year holds one occurrence, so the annual total moves under 1.5 per cent; only a monthly
  decision would carry it, and the seed's decision is a year's revenue.
- 2026-10-17, at the draw: a prudent budget at the annual total's 10th percentile with autocorrelated monthly errors:
  every reasonable model gives a different interval, so the figure is not determinate, and simulating paths from the
  fitted model, a strong solver's default, lands.
- 2026-10-17, at the draw: a fee elasticity read from the previous fee change and applied to a coming fee step: the
  functional form (constant elasticity or linear) moves the answer for a step of another size, a fork, and the naive
  route's two errors (the trend booked as the effect, then no trend after it) cancel.
- 2026-10-17, at the draw: a filed back-test choosing the forecasting method: the filed criterion makes the selection
  rule application, and the opponent back-tests by reflex.
- 2026-10-17, at the draw: a level shift at the end of the series (a recent fee change) under a univariate forecast:
  adaptive models absorb it within a few months, so the default lands.
- 2026-10-17, at the draw: the temporary rank alone, with the drop-offs as its comparison series: the drop-offs are the
  reflex control and land on the golden; the line opening the same day, acting only on its station zones, which the two
  directions carry in different shares, is what makes the reflex control wrong.
- 2026-10-17, at the draw: the airport's own passenger forecast as the driver, biased high: catching a stakeholder
  figure that is wrong so the task can overturn it is a plant.
