# task469 design note: Kelderby's summer 2027 ground time review

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task469.json` (architecture v1), registered 2026-10-17 after a pull, so
  every card filed before it was in the check. Guard check WARN only, answered here: Gate G method_or_model_selection
  is in seven of the last twelve builds (it is the honest key: the decisive step is choosing an estimator that treats
  the hidden turn times as censored, against the observed ground times or the overruns alone). The structural tests'
  older matches are differentiated on the card: task101 (a threshold cut from a distribution the decision's own
  payments had entered), task126 (units a succession link joined) and task450 v1 (durations sampled in proportion to
  length by scheduled visits). Nearest driver task155 at 0.09.
- **Seed:** ET26 (an airport authority's performance team saw its hub's arrival on-time rate fall between two summers;
  the dashboard listed the regional operators apart from the brands they fly for, and the board asked the wrong airline
  for an explanation). Kept: the world (a hub, the brands and the regional operators flying for them, the authority's
  performance team) and the carrier relationship as the unit the authority holds to account; the quantity stays
  punctuality, read where the authority can act on it, the time a relationship's turns need at its stands. Made forward
  facing: the call is on the ground times the airlines filed for summer 2027. Dropped: the seed's move (mix against rate
  between the brand and its partners), which is composition_mix and banned against the last three, and the marketing
  against operating carrier reading, which is data semantics; it survives as a lower rung (pooling one operator's
  turns for two brands).
- **Pairing:** General Statistics & Data Science / data-integration-record-linkage-entity-resolution / ETL. The
  authority's evidence is a linked dataset: its operational database's stand events (on-block and off-block, keyed by
  registration, stand and ATC callsign), the filed schedules (commercial flight numbers in SSIM files), the operators'
  flight logs with their delay codes (two code versions) and the affiliate register, joined into turns. GSDS is a
  methods domain, so the swap is of the method: the deciding quantity is a tail probability of a duration that the
  schedule left-censors (estimation_fit, censoring and truncation), and replacing the censoring-aware estimate with the
  share of observed ground times, of overruns, or of the turns scheduled at the new ground time in 2026 moves the call.
- **Shape:** 14, cuts of a distribution per segment: for each carrier relationship and aircraft type at the E gates,
  the share of turns that need longer than the ground time it filed, the shortest ground time the authority would
  accept on its 20 per cent standard, and the verdict on the filing.
- **Strategy:** maturity_censoring (the censoring family: here the allowance, not the cut, hides the values), decisive
  generator G3 (the stand log's ground time against the turn's need), with G17 (the censoring-aware estimate) and G13
  (the 2026 allowance against the shorter 2027 one).
- **World:** Canada, an unnamed province. Kelderby International Airport is run by the Kelderby Airport Authority, a
  not-for-profit airport authority, and is a schedules-facilitated airport for its regional concourse (the E gates,
  ground-level stands with walk-out boarding). Norvale Air, the hub's dominant brand, sells Norvale Connect flights
  flown by Pellmont Aviation (E175 jets) and Sable Coast Air (Q400 turboprops) under capacity purchase agreements and
  turned by Norvale Ground Services; Tellura Airways sells Tellura Express flights flown by Pellmont (E175) and turned
  by a contracted handler; Grayling Air flies and turns its own ATR 72s. The authority's schedule facilitation
  guideline accepts a filed minimum ground time at the E gates when no more than 20 per cent of the relationship's
  turns of that aircraft type would need longer, judged on the turns of the most recent summer peak (15 June to 15
  September 2026); a turn needs the time from on-block until the aircraft is ready to push back. For summer 2027 the
  carriers filed shorter ground times for most relationships.
- **Forcing fact:** the authority's Schedule Facilitation Committee answers the summer 2027 initial submissions at its
  18 November 2026 meeting; the airside operations director's workbook goes to it. As-of: 30 October 2026. The call
  faces forward (the 2027 season's turns, not yet run); the evidence is the closed 2026 peak.
- **Forum and forcing event:** committee_or_panel (the Schedule Facilitation Committee), season_or_peak (the summer
  2027 schedule submissions). Organisation utility_or_infrastructure; role operations_director. Personas from
  `guard.py names --geo Canada --seed 469`: Joanne Gilbert (Director, Airside Operations, who brings the review to
  the committee), Gabriela Armstrong (analyst, Airside Performance, who keeps the stand log) and Arthur Bryant
  (Manager, Gate Planning); Danielle Welch replaced (her first name in task101).
- **Data-native sentence:** a turn at the E gates pushes back on time whenever it is ready by its scheduled departure,
  so the stand log shows how long a turn needed only when the turn held the departure up; under the 2026 schedules most
  turns had more time than the carriers now file for 2027, so the turns that would need longer than the new ground
  time mostly finished inside their old allowance and left on time, and only the turns whose inbound came in late
  enough to leave less than the new ground time show the share in full.
- **The WHAT screen.** Population: a relationship's turns of one aircraft type at the E gates (one aircraft's stand
  visit from on-block to off-block between an arrival and a departure of that relationship), the summer 2027 turns
  judged by the summer 2026 peak's (filed in the guideline). Outcome: the turn needs longer than the filed ground time,
  need being on-block to ready for pushback. Window: 15 June to 15 September 2026 as evidence, summer 2027 as the
  application. Unit: turns. Comparison: 20 per cent. The decisive step settles none of them: it is how the share is
  estimated from turns whose need the schedule hid whenever they finished inside their allowance.
- **Deliverables:** `kelderby_summer2027_ground_time_review.xlsx` (the call: each relationship's verdict on its filed
  ground time and the shortest it could file, each share needing longer, the asks, a chart of the shares against the
  standard).
- **Sources, one line each:**
  - `stumping/references/client/layer2-rigor-patterns.md`, data-integration-record-linkage-entity-resolution: the
    ETL task type the conformance sits in; the decisive analytic is the domain's treatment of censored durations
    (`two-layer-task-design.md`, estimation_fit, censoring and truncation), with no pattern on file for an allowance
    hiding the values, so the pattern is the build's own.
  - `dataset-generation/references/layer1-messiness.md`: a stand log in local time beside operators' logs in UTC, ATC
    callsigns against commercial flight numbers, SSIM fixed-width schedules, two delay-code versions, tows splitting a
    turn across stands, registrations with and without the hyphen, an aircraft moving between operators and flight
    number blocks changing hands mid-summer; none on the decisive step, each to be asserted neutral.
  - The lane's spent drivers (`guard.py mechanisms --objective etl`, 47 builds): none reads a duration hidden by an
    allowance; the nearest families are maturity (task451, task458, task462: values not yet observed at a cut) and
    length-biased sampling (task450 v1), both differentiated.

## Tried and rejected

- 2026-10-17, at the draw: the seed's own move, the hub's on-time fall split into mix against rate between the brand's
  mainline and its regional partners: composition_mix, banned against the last three (task194), and the client counts
  it as Simpson's paradox already taught.
- 2026-10-17, at the draw: marketing brand against operating carrier as the decisive step: a field reading (data
  semantics); kept only as a lower rung, one operator's turns for two brands pooled.
- 2026-10-17, at the draw: delay propagation through aircraft rotations (delay the hub generated against delay carried
  in): the decisive step defines the outcome (what delay a station generated), so the WHAT screen kills it; filed it is
  rule application, unfiled the call is not determinate.
- 2026-10-17, at the draw: linking the stand log's ATC callsigns to commercial flight numbers with nearest-schedule
  false links pulling late arrivals onto the next flight: the record-linkage pattern's other half, but task468, one
  build back, carried the matcher-error family, and catching the false links would be what decides (a plant by the
  litmus).
- 2026-10-17, at the draw: operators' reported arrival times against the authority's docking sensors, corrected by a
  sensor subsample's sensitivity and specificity: the reporting error reads as planted, and task230 and task456 already
  teach misclassification correction.
- 2026-10-17, at the draw: ramp-log times rounded to five minutes heaping on the 15-minute threshold: the decisive step
  would be reading the rounding convention (data semantics), on a margin under a point.
- 2026-10-17, at the draw: day-clustered uncertainty in the summers' on-time change (signal against noise): the
  analytic belongs to complex-survey-estimation-variance, which serves no ETL objective, and the call would retag as
  anomaly detection.
