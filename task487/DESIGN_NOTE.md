# task487 design note: an upstream oil producer's 2026 release-event methane for the province's release-event levy, each event found at a lease operator's visit split between the share the previous visit started and the share that arose between visits (architecture 1)

Status lives in `pipeline.json`; this note holds the design. Architecture 1, drawn 2026-10-26. The slot's seed (ET44,
an online wholesaler's loyalty tiers from a net-spend distribution) was read for its header and situation only: once its
decoy-era mechanism is set aside the world carries no quantity the field estimates (a tier cut of a spend distribution
is a sort, and the seed's steps are semantics), so the first draw is made in the emissions-inventory cell on what the
seed's quantity shares with this one, a total built from records whose own durations are not recorded. The candidates
screened before this draw are in `## Tried and rejected`.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task487.json` (architecture v1), registered 2026-10-26T13:07:47Z and
  checked again after filing: PASS, one NOTE (driver similarity 0.16 against task476 v2, differentiated on the card).
  The window the axis bans read at filing (task485 v4, task121 v5 and task308 v1, the live cards filed last; task270
  v5, task137 v2, task486 v3 and task269 v4 are spent and skipped) closes the pairing survey-research-official-
  statistics / etl and the subdomain census-register-administrative-data-quality, the strategies maturity_censoring,
  causal_design and binding_constraint, the shapes 18 and other, the forums minister_or_cabinet, committee_or_panel and
  board_of_directors, the forcing events vote_or_meeting, other and budget_or_appropriation, the organisations
  research_or_statistics_office, government_agency and financial_institution, the roles statistical_office_head,
  compliance_or_audit and portfolio_manager, the artifacts published_series, monitoring_export and filed_standard and
  the generators G9, G4 and G14. The draw's honest labels clear all of them: the operator files its 2026 release events
  with the provincial regulator (regulator_or_inspector, statutory_or_regulatory_filing), the requester is the area
  production superintendent who signs the filing (field_unit_lead), the stakeholder's own file is the lease operators'
  visit log (operations_log), and the organisation is an upstream oil producer (other: no vocabulary key fits and
  utility_or_infrastructure would be untrue).
- **Labels redrawn at the draw, and why the filed ones are the honester:** the first draft carried G3 decisive (record
  against operation: the previous visit did it) with Gate G method_or_model_selection, and BLOCKed on
  `test.same_puzzle_older` (task126, task138, task82) and `test.same_driver_older` (task126, task275, task450 v1, task468
  v4, task469); with G7 decisive and method_or_model_selection it BLOCKed on `test.same_driver` against task308's
  lineage inside the batch. What carries the stump is a split of correctly recorded events between two drivers (the
  previous visit, and the hours since), which is `decomposition_attribution`, and what fixes when the started share
  began is the visit log's departure times, an operations file pinning when the event could have begun (G7), with the
  record-against-operation reading (G3) second. The gap is population (Gap 2, the file is not the thing): the event
  log's windows stand in for active hours they are not.
- **Pairing:** Physical & Environmental Sciences / `emissions-inventory`, drawn for Data Extraction & Conformation
  (ETL). The deliverable is the conformed 2026 release-event inventory in the regulator's event schema, one row per
  event, built from two pumper apps (a mid-year migration), the operator's event log, the SCADA tank pressure alarm
  journal, daily production, the batteries' vapour analyses and the battery register.
- **The world and the decision.** A fictional western Canadian province levies upstream operators on the methane their
  release events vent (an open thief hatch, a combustor whose pilot is out, a relief valve lifting or stuck), assessed
  each year on the previous calendar year's events and banded into tiers by the operator's total tonnes, each tier
  carrying a fixed levy and an inspection obligation for the year. The operator runs 180 tank batteries on twelve lease
  operator (pumper) routes: most batteries are visited once a weekday, two routes also on Saturdays, high producers twice
  a weekday and low producers on Mondays, Wednesdays and Fridays, so the window between one visit's departure and the
  next arrival runs from a few hours to most of a week across holidays and relief days. Every visit gauges the tanks
  through the thief hatch and checks the combustor, and every event present at an arrival is found then and closed on
  site; at the 40 per cent of batteries with tank pressure telemetry a relief valve lift raises an alarm and is timed
  exactly. The filing states each event's start, closure and vented methane; the levy follows from the total.
- **Timing (the pack's present is mid-January 2027).** The 2026 records are complete; the filing is due 31 March 2027
  and the tier fixes the 2027 levy and the 2027 inspection obligation. The quantity is retrospective by construction (a
  closed year's events) and the call it fixes is forward: what the operator budgets and staffs in 2027.
- **Shape:** `03`, a bridge between two totals: from the methane the records date (the alarm-timed events and every
  visit-found event's hours after it was found) to the methane over each event's active hours, one reconciling item per
  route (twelve), with the two totals, the gap and the tier.
- **The default path holds the field's practice (stumping 1.1b).** An inventory that cannot date an event's start takes
  the midpoint of the window since the last time the equipment was known good, or the conservative last-known-good start;
  the alarm-timed relief events, whose starts sit uniformly across their inter-visit windows, confirm the midpoint to a
  careful analyst. The golden is the decomposition the data force: incidence of each kind against window length is a
  per-visit part plus a per-hour part, the per-visit part starting at the previous departure.
- **Prototype (scratchpad `t487/proto4.py`, four seeds):** truth 91 to 101 t; the midpoint 69 to 76 t (about 25 per cent
  low); the conservative window start 134 to 149 t; hatch events at the window start and the rest at the midpoint 105 to
  118 t; the per-kind decomposition 90 to 97 t, pooled over kinds 91 to 98 t, per route 91 to 97 t; likelihood ratios of
  the per-visit part 88 to 162 (hatch), 20 to 51 (pilot) and 0 to 1 (relief valve, which no visit starts).
- **Data-native sentence:** on the prototype the lease operators found about 1,500 hatch and pilot events in the year,
  and after a 64-hour weekend window only about 1.7 times as many as after a 22-hour weekday one, not the 2.9 times the
  hours would give, because a large share of them were started by the visit before; the relief valve events the alarms
  time exactly arose evenly in the hours between and so sit like a midpoint.
- **People** (drawn with `guard.py names --geo canada --seed 487`): Rhonda Wheeler (area production superintendent, the
  requester), Charlene Logan (regulatory analyst).

## Three rules

Task type: emissions-inventory (Physical & Environmental Sciences), tagged in the taxonomy for Data Extraction &
Conformation (ETL): the conformed event-level release inventory the regulator's schema requires, from two pumper apps,
the event log, the alarm journal, production and vapour analyses.
Domain test: The deciding quantity is the operator's 2026 vented methane from release events, each event's tank vapour
rate (flash and standing vapour from the battery's oil throughput and vapour analysis) over its active hours, where the
active hours of an event a lease operator finds at a visit are split between the share the previous visit starts and the
share that arises between visits, read from how often each kind of event is found against the window's length.
Swap: put a ward's fall rounds in for the pumper's visits and the gauging that opens a thief hatch, the flash vapour that
leaves through it, the knockout drain that drowns a combustor pilot and the relief valve the tank pressure alarm watches
stop making sense, and with them the vapour rate each hour is priced at.
Layer 1: two pumper apps across a 1 July migration (local time, then UTC); GPS geofence double check-ins; a battery
renamed after a purchase with its history under the old licence; event log free text naming each kind several ways;
production in cubic metres against analyses in mole per cent; alarm chatter re-raising one relief event within minutes.
Each is produced by the operator's ordinary systems and none is placed to be caught.
Layer 2: estimation_fit: an event's start inside an observation window that the inspecting visit itself opens, so the
window's placement carries information about the start and the even-spread (or uninformative interval-censored)
placement is misspecified; the share started by the visit is identified by incidence against window length.
Decisive step: splitting each kind's events found at visits into a per-visit part, started as the previous visit ended,
and a per-hour part arising evenly between visits, from how often each kind is found against the length of the window
since the previous departure, and running each found event's expected hours from that split.
Not semantics: every field reads as what it is (departures, arrivals, finds, closures, alarms); no code, note or column
marks an event's cause or start, every visit gauges and checks the combustor alike, and an analyst who conforms every
file exactly still files the lowest tier by spreading each start evenly through its window.
Not rule application: the directive files the WHAT (each event's methane from its start to its closure, at the expected
start where the records do not date it) and nothing about how a start is placed; the enumerated family (midpoint, the
alarm-validated midpoint, the conservative window start, hatch at the start and the rest at the midpoint) spreads across
all three tiers (69 to 149 t on the prototype), the standing family (the decomposition per kind, pooled, per route)
spreads 90 to 98 t inside one tier, and what rules the rest out is a fitted per-visit term (likelihood ratio 88 to 162
for hatches) that no table shows until incidence is set against window length.
Analyst test: A strong analyst conforms both apps, joins every find to the previous departure, prices each event at the
battery's vapour rate, starts it halfway back (the alarm-timed relief events sit evenly across their windows) and files
the lowest tier at about 72 t, where the golden is the middle tier at about 92 t.
Estimand: each 2026 release event's vented methane from its start to its closure, its start where the records do not
date it taken at its expected value given the operator's records, summed over the operator's events and banded by the
directive's tiers (`release_event_directive_2025.pdf`, "What the filing reports" and "Tiers").
No decoy: nothing is planted: the visit log, the event log, the alarm journal, production and analyses are the
operator's ordinary records; no memo, draft, prior filing or stakeholder figure argues for a tier or a placement, and the
alarm journal is shipped because the alarm-timed events' own hours are in the inventory.
No certified replay: no certified or published figure sits in the pack to be reproduced, and no method is recovered
from one.
Lesson: an inspection that can start the events it later finds leaves those events running for their whole windows, so
the found events' active time is longer than half their windows by a share that falls as the windows lengthen; the
share is read from how incidence grows with the window, and an exactly timed record of a kind the inspection cannot
start confirms the even spread it misprices. No build on file reads an inspection-started share from incidence against
window length (nearest driver 0.16, task476 v2, a seasonal start profile from a second record).

## Tried and rejected

- 2026-10-26, draw screen for this number, each dead on file, on the rules or on paper before a card was written: the
  seed's own world (loyalty tiers cut from a spend distribution: a sort over a conformed column, and every step the seed
  names is semantics); customer identity across a wholesaler's accounts and marketplace channels (identity resolution, a
  rule or a reading); seasonal annualisation of part-year spend (task123, task474); claims completion, bundles against a
  comparison group, contract-order reconciliation, risk-adjusted ratios of totals and high-cost regression to the mean
  (the payment-claims cell's patterns, banned in the window or rule application); NEAT method choice under a large group
  difference (task471's screen: a fork), anchor drift, position effects, plausible values and rater drift (task450,
  task482 v6 and v11, task471 v2); quasi-identifier coincidences between two hashed lists (task468's false links on
  common identifiers, and too small at a fine key); random-effects pooling of emission-factor studies (a meta-analysis
  outside the record-linkage task type, and the interval estimators fork); clustered stack-test runs behind a revision
  (task261's driver); temporal disaggregation for a recession trigger and turning points on a trend-cycle (the survey
  research pairing is banned against task485 in this window); catalyst ageing per cumulative hours, fouling per fuel
  burned, cold starts by soak time and flare efficiency by wind (a rate carried across an operating condition: task459,
  task478 v7, task480); tank losses from gauge readings taken just before each refill (task229's driver, checks see the
  state just before resetting it); a storage tank's overflow at its own fill time (one subtraction once the gauge sheet is
  joined); the same visit-started events placed at a slate of hours (stumping 1.1h's two horns: the graded quantity here
  is one total, not a slate).
