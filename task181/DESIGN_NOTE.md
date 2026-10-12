# task181 design note

Architecture 4. Seed AD04 (Anomaly Detection & Diagnostics, a pump's zone-D vibration split by operating point) is
idea material only: its insight is task180 v2's (a monitored signal carried in from ordinary operation), and its world
has no client task type that serves this objective. Three architectures are spent (`## Tried and rejected`); the
author's builds are never retired, so the objective and the number are kept and the draw is new.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task181.json`, architecture v4, registered 2026-10-12 after `guard.py
  check` (WARN only: `three_rules.strategy_risk` and `repeat.gate_g`, both answered below; the older same-puzzle and
  same-driver matches, task229 v1, task98 v3 and task60 v8, differentiated on the card).
- **Pairing:** Human Factors & Ergonomics, task type safety-incident-error-analysis, objective Anomaly Detection &
  Diagnostics (a pairing never built). The anomaly is a sector whose losses of separation will run over the safety
  plan's tolerance in summer 2027; the diagnosis is what generates a sector's losses. Shape 01 (each sector's forecast
  against the tolerance line, in or out). Decision `designation_set` (the sectors over the tolerance, possibly none),
  question form `whether`.
- **World:** Aldmark (a fictional northern European state), its national air navigation service provider Aldmark Air
  Navigation and the Holmvik Area Control Centre, eight elementary en-route sectors (Tarvik High, Tarvik Low, Mosby
  High, Mosby Low, Grendal, Linmark, Karrow, Lysvik) over a hub (Holmvik) and two regional airports (Brekka, Skarnes).
  Brekka gets a low-cost carrier's new base for the summer 2027 schedule.
- **As of:** extracts pulled 12 October 2026 (actuals 1 January 2025 to 30 September 2026); the summer 2027 traffic
  sample issued 9 October 2026; the unit safety review board approves the summer 2027 sector plan on 4 November 2026.
  `leak.py --asof 2026-10-12`.
- **Mechanism:** gap population (what one unit of exposure is: a pair of aircraft, one crossing the other's level),
  then time (the forward window holds traffic the closed window never had); pattern D (two flawless grains, the
  flight-hour grain of the extract and the crossing grain of the losses, no key bridging them); generators G2 (decisive)
  and G13. Gate G `forecasting`. Strategy `grain_or_unit`.
- **Furniture:** forum `committee_or_panel` (the unit safety review board), forcing event `season_or_peak` (summer 2027),
  organisation family `utility_or_infrastructure`, role family `capacity_planner`, context artifact `close_out_summary`
  (the summer 2026 safety performance close-out), opening `question-first`. Personas drawn with `guard.py names --geo
  Denmark --seed 181` (Dorte Koch, Erik Sørensen, Paw Frandsen); the prompt carries none of them.
- **WARNs answered.** `three_rules.strategy_risk` (grain_or_unit): nothing here turns on reading a field; every field is
  read the same on both paths, and the analyst test below names the easy route that still fails once every field and
  rule is read correctly. `repeat.gate_g` (forecasting against task501 v3): forecasting is the honest label, because
  the call is a bet on summer 2027 losses that no closed figure states; task501's mechanism (a buffer read off horizon
  totals instead of a cumulative path) shares nothing with this one.
- **Data-native sentence:** separation in this centre is lost almost only where one aircraft climbs or descends
  through the level of another in the same sector (level traffic on the airways is spaced in trail by the flow
  measures), so a sector's losses follow the vertical crossings its traffic creates, and the summer 2027 schedules send
  the new Brekka base's departures climbing through Tarvik High's busy eastbound cruise levels while adding few flight
  hours.
- **Sources read, one line each:**
  - `stumping/references/client/two-layer-task-design.md`: the three rules and the two layers; the mess goes on the ask
    paths and the stump into the forecast's exposure.
  - `layer2-rigor-patterns.md` has no human-factors patterns; the five families in the client's standard place this
    under the field's own method (`field_method`): the field's exposure for a separation loss is the interaction, not
    the hour flown.
  - `stumping/references/strategies.md` Parts 1, 4 and 6: the dead shapes avoided are the default construction as
    golden, a quantity named by a sentence or a column, a reflex (pool, square the traffic, stratify by phase, trend),
    a dated cause stepping a series, and a linear mechanism in a rate-times-exposure world.
  - `stumping/references/client/measured-drivers.md`: the held group's lesson taken is the compound construction a
    solver does not build (here an exposure made by pairing rows of one extract in time and level); none of their
    withheld-method pins is used.
  - Architecture 3's rejected draws (squared load, overlapping panels, competing exits, funnel limits, fabricated
    interviews as inliers, warranty curves, the seed's zone-D split): none is reused.

## Default path

The pipeline a competent analyst builds from the prompt's words and the files' grain:

1. Read the safety plan's tolerance: a sector's ATM-related losses of separation in the summer season (1 June to
   31 August) may not exceed 12.0 per 100,000 flight hours.
2. Load the occurrence export, keep the losses of separation with an ATM contribution, collapse the controller report,
   the conflict-alert log line and the pilot report of one occurrence to one, and attribute each to its elementary
   sector through the night configurations.
3. Sum each sector's summer flight hours from the flight data extract (entry to exit of every traversal), compute each
   sector's summer 2026 rate per 100,000 flight hours, and confirm it against the summer 2026 close-out.
4. Sum each sector's flight hours in the summer 2027 traffic sample against the same sample week of 2026, scale each
   sector's summer 2026 losses by that growth (the rate held at 2026's), and compare each forecast rate with 12.0.
5. No sector reaches 12.0 (Mosby High highest at about 11); file that summer 2027 stays inside the tolerance.

Ends on: no sector over the tolerance
Golden: Tarvik High

## Stump sentence

A competent solver keeps each sector's summer 2026 losses of separation per 100,000 flight hours, scales each sector's
losses with its 2027 flight hours from the traffic sample and files no sector over the tolerance (Mosby High highest at
about 11 against 12.0), and the step that lands it there is forecasting losses from flight hours when separation is lost
where one aircraft climbs or descends through another's level: the new Brekka departures add about 2 per cent to Tarvik
High's flight hours and roughly double the vertical crossings of its eastbound airway, which takes Tarvik High to about
14.5 losses per 100,000 flight hours while every other sector stays under 12.0.

## Three rules

- **Litmus:** no reported number is wrong and nothing overturns one. The flight data, the occurrence export, the
  close-out and the traffic sample are all correct; the difficulty is building a summer 2027 count no file states.
- Domain test: what decides the call is air traffic control's human-factors safety analysis of controller workload: a
  loss of separation is a controller error in a vertical interaction (an aircraft cleared through the level of
  another), so a sector's expected losses follow the vertical crossings in its traffic, a complexity measure the field
  keeps beside flight hours; with another field's nouns there are no flight levels to cross and no climb through a
  cruising flow, so the task does not survive the swap.
- Analyst test: a strong analyst who deduplicates the occurrence records, keeps the ATM-related losses, attributes each
  to its elementary sector under the night configurations and computes summer flight hours exactly still forecasts
  summer 2027 by scaling each sector's losses with its flight hours, with the square of its traffic or with its
  climbing and descending flight hours, and files that no sector exceeds 12.0, because only counting the vertical
  crossings in each sector shows the new Brekka departures taking Tarvik High over the tolerance.
- Layer 1: realistic mess from the centre's own systems, on the ask paths: the flight data extract at flight x
  elementary sector grain with levels in hundreds of feet and times in UTC, the night sector configurations in a
  separate opening log, an occurrence export with the controller report, the conflict-alert log line and any pilot
  report of one occurrence on separate lines under one occurrence number, callsigns that change between the flight
  plan and the radio, the season defined in local time against UTC stamps across the summer-time changes, and a
  traffic sample built by the forecast team in its own layout and key.
- Layer 2: a sector's forward losses are not its flight hours times its past rate, nor a function of its traffic count
  or of the time its traffic spends climbing: separation is lost between two aircraft where one changes level through
  the other's, so the forecast has to carry the vertical crossings each sector's traffic creates, and the record proves
  it (losses per crossing hold steady across sectors and months while losses per flight hour vary several-fold).
- **Stump class:** analytical. Rule 3 is cleared: no planted defect or decoy decides it, no field reading flips it (every
  field is read the same on both paths) and no stated rule produces it (the tolerance is filed; nothing in the pack
  says how to forecast the losses).

## Tried and rejected

- Architecture 1 (a credit union's counterfeit wave traced to two skimmed terminals behind a dominant common point):
  spent at in-house round 1, where a solver explained the co-visited sites away as subsets of the dominant source's
  victims and re-screened the residual; any further rung falls to the same subset check or opens a fork.
- Architecture 2 (a public health unit's pertussis line list, the fortnight completed by laboratory route): stumped
  in-house only while the estimand was open; the portal's determinism QC called it a fork, and once the eventual count
  was filed literally a per-laboratory completion landed it (96.8), and any filed criterion choosing the delay history
  names the step.
- Architecture 3 (a housing association's estates, near-repeat burglary runs against each estate's background):
  spent at design; a filed back-test on about ten break-ins per estate-quarter cannot select the background projection
  on honest data (the usual winter wins the back-test in most seeds), and nothing short of a planted smoothing closes it.
- An airspace-change safety case on losses of separation per flight hour against interactions, read retrospectively
  (which sector's 2026 losses most exceed its traffic): the industry keeps losses per 100,000 flight hours as its
  standard rate, so "beyond what its traffic explains" is a fork between that rate and the interaction rate; the
  forward count with the tolerance filed literally removes the fork.
- Forklift and pedestrian near misses scaled by the product of zone occupancies: the product of two counts is a
  mass-action reflex for a quantitative solver, so the decisive rung is readable.
- Rail signals passed at danger per approach at red: a stop-aspect exposure is the first thought once an aspect log
  ships (a solver reasons that only a red signal can be passed at danger).
- Hospital ward acquisitions of a resistant organism per colonised patient-day: colonisation pressure is infection
  prevention's own reflex, and under mass action it equals the colonised-day rate the reflex computes.
- A survey's regional estimate moved by a gradual shift to web interviewing, separated by its randomised-mode
  subsample: the randomised arm is a schema cue a solver uses at once.
- Excess deaths in a heatwave net of mortality displacement: once the window is filed literally the net excess is a
  reading, and the field is architecture 2's.
- Ambulance mileage, impossible days, upcoding against audit-log time, check kiting on uncollected funds: each turns on
  a filed rule or a field read correctly (rule application or data semantics).
- A workload ceiling crossed in saturated hours (errors by occupancy band applied to a 2027 staffing plan) and a queue's
  ageing into a 52-week breach: both are state-based forward projections, the family task183 and task132 already hold.
