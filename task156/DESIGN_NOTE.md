# task156: a district council's pump station, whether a subdivision can connect in 2027 within the station's consented overflows (architecture 2)

Private, never ships. Architecture 1 (Millrind's 2027 paid moderation pool, a developer Q&A network's volunteer
reviewers carried on survival by tenure) shipped 2026-10-17, was returned by the portal on 2026-10-27 with both
responses on the call, and was reshipped the same day as loop 3 with its world, prompt and asks kept. The batch 1
triage of 2026-10-31 re-roots the slot in a new world: nothing of architecture 1 is carried (world, decision,
quantity, prompt shell, deliverables, asks and mechanism are all new), and its identity sits in the card's
`lineage` with its fate.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task156.json`, architecture v2, registered 2026-10-31T18:27:04Z; architecture 1 (v1 loop 3, and v1 loops 1 and 2 before it) in `lineage`, its shell in `lineage_shells` |
| Domain / task type | `physical-environmental-sciences`, task type `hydrology-flood-frequency` (serves Forecasting): the deciding quantity is how often a pump station's capacity is exceeded under a long rainfall record, an exceedance frequency worked the way urban hydrology works it, by continuous simulation of a calibrated rainfall-derived infiltration and inflow model |
| Objective | Forecasting & Predictive Modeling: the station's average wet-weather overflows a year once the subdivision connects in 2027, a window not yet open, estimated the way the discharge consent states it (the network as it will be, run through the 2006 to 2025 record) |
| Shape | `other`: the call with the consent figure with and without the subdivision, the fitted infiltration components, a chart of the replay year by year against the limit, and row-set asks on records the call never reads (arithmetic in `## Shape` at stage 2) |
| Decision | `go_hold_or_stop`, answer unit `named_option`: connect in 2027, or hold the connection until the storage upgrade |
| Mechanism | population then time: the meter's 2024 to 2026 storms and dry days are not the population of days the consent's replay runs (Gap 2), and the decision is forward (Gap 1); generators G14 (conditioned yield: the infiltration a dry day and a storm drive is conditioned on the length of sewer below the water table, which the replay's wet years carry past anything the meter saw), G16 (the conditioned model chosen over one response per millimetre on storms it was not fitted on), G13; Gate G `forecasting`; strategy `forecast_method_backtest` (a rate stationary only in a constructed exposure, kilometres of sewer below the water table) |
| Layer 2 family / pattern | `forecast_uncertainty` (model choice on out-of-sample error); `own:submerged-length-conditioned-infiltration-chosen-out-of-sample` |
| Furniture | forum `council_or_assembly` (the elected district council resolves on the officers' report whether the subdivision connects in 2027), forcing event `vote_or_meeting` (the council's December 2026 meeting, which takes the developer's connection request), organisation family `local_government`, role family `operations_director` (the three waters operations manager), context artifact `monitoring_export` (the station's SCADA export the operations manager works from), calibration `realised_outcome_roster` (the station's overflow log, which the golden model reproduces and one response per millimetre does not), opening `question-first`, question form `whether` |
| Spine | `pump_station_inflow_2024-2026.csv`, the station's SCADA inflow every 15 minutes for three years (about 105,000 rows, UTC), beside the council's rain gauge, the regional bore's daily groundwater level from 2006, the asset register's pipes with invert levels and the 2006 to 2025 hourly rainfall record; constructed for this build, no real dataset |
| Deliverables | `subdivision_connection_assessment_2027.xlsx` (the assessment), `council_report_subdivision_connection_2027.docx` (the officers' report to council), `replay_overflows_2006-2025.png` (the replay year by year against the limit) |
| People | drawn with `guard.py names --geo "New Zealand" --seed 156`: Aaliyah Beattie, Benjamin Gilbert, Anaru Boyce (roles fixed at stage 3; Sean McDowall passed over, his first name already on task105); the requester is in no file and not in the prompt |

**Guard answers (registered card, `guard.py check` WARN, no BLOCK, after rebasing on main).**
- Redrawn after the rebase: task191 and task250 were registered on main after this worktree's base, and with them in
  the window `committee_or_panel`, `purchase_order_or_contract` and `filed_standard` BLOCKed. The replacements are the
  honester labels: a subdivision's connection held back for capacity is a growth decision an elected council resolves
  on an officers' report at a scheduled meeting, not a staff panel's, and the file the operations manager works from is
  the station's SCADA export; the consent stays in the pack as the governing document.
- `repeat.question_form` against task250: the decision is a gate (connect in 2027 or hold to the upgrade), and a gate
  asks whether (`guide-to-prompt`); "whether" holds 10 per cent of prompts on file, under its 30 per cent quota, and
  the second-sentence opener ("the") and the deliverable set (docx, png and xlsx) differ from task250's.
- `test.same_driver_older` (population, G14, forecasting) is differentiated on the card against task134, task146,
  task165 and task173 v1, one line each naming how the driver differs. The redrawn labels are the honest ones: the
  first probe carried `validated_decoy` true and Gap 1 first, which BLOCKed on `two_layer.validated_decoy` and on a
  signature spent in five builds; the meter's own record refutes one response per millimetre for anyone who checks it
  against the high-water-table storms and the overflow log, so `validated_decoy` is false, and the decisive gap is
  that the meter's days are not the replay's population, which puts population first.

**Abstraction test.** Stripped of nouns: how often a fixed capacity is exceeded once a steady load is added, when the
standing load and each event's response scale with how much of a fixed network lies below a fluctuating level read
from a separate record, so a response and a standing load read off a short record whose level mostly stayed low
understate a long record whose level often rose past most of the network. Nearest by mechanism:
- task178 (lineage, hydrology) fits one stage-discharge relation whose form changes above a level few gaugings reach;
  here no relation changes form: infiltration is linear in the submerged length, and the nonlinearity sits in how that
  length grows with the water level, read from the register's inverts, which no flow record shows.
- task138 (hydrology) replays past weather seasons through a root-zone balance started from each field's store; the
  replay is shared furniture (continuous simulation over a record is the field's method), the decisive move is not:
  there the share of each input reaching the store, here the exposure that conditions the response.
- task165 conditions an upgrade's gain on each site's untreated share, read from each site's own record; here the
  conditioning state is in no record of the storms or days: it is built from a level series against fixed elevations.
- task173 v1 re-mixes a bench of first-contact takers; here nothing is re-mixed, the exposure is continuous and
  physical.
- task134 and task146 condition on an option's payoff and on refusal timing within a period; neither builds an exposure.
None shares the latent structure, the default path and the correction.

**Data-native sentence.** The infiltration reaching the station through cracked joints and laterals runs only where a
pipe lies below the water table, so it scales with the kilometres of sewer whose inverts sit under that day's
groundwater level; on the river terrace that level follows the river's high flows from the upper catchment more than
local rain, the 2024 to 2026 meter ran through low-river years when the water table stood below most of the terrace's
sewers, and the consent's 2006 to 2025 record holds winters with it above most of them, so a response per millimetre
and a base flow read off the meter understate the replay's wet years.

**Sources read, one line each.**
- `guard.py recent`, `coverage`, `mechanisms --objective forecasting` (every forecasting driver on file, lineage
  included) and `slots` on the setting nouns (sewer, infiltration, water table, invert, pump station, overflow,
  groundwater; unit hydrograph, rainfall, replay, continuous simulation, consent, storage) and on the mechanism words:
  no slot note or card carries a sewer, infiltration or groundwater mechanism; the replay furniture is task138's and
  task178's, read above.
- The neighbouring re-roots' `pipeline.json` (task118, task130, task181, task191, task250, task268, task306, task470,
  task482): none touches physical-environmental-sciences hydrology this batch.
- `layer2-rigor-patterns.md`: no patterns filed for Physical & Environmental Sciences, so the pattern is the build's
  own.
- task174's paused notes: the forward condition must act through a quantity the change does not name and no unit in
  the record has reached, the data must reveal it, and the textbook validation passes only because the hold-out shares
  the training regime; here the meter's high-water-table weeks are the separating storms.

## Tried and rejected

- A mix shift by author tenure (new accounts' posts carry most review items, and AI took the newcomers): rejected at the
  draw, because the account-age column makes the segmentation a reflex the opponent runs on every visible attribute.
- Spam and flags scaling with page views rather than questions: rejected at the draw, because a per-queue trend of the
  flags already follows views, so the reflex lands, and the swap test reads it as generic demand forecasting.
- A volunteer pool with two retention types (veterans and casual reviewers) as a rung: dropped at the prototype, because
  the defensible retention estimators (tenure bands, pooled recent churn, a heterogeneity fit) split the per-site
  figures by up to 0.8 FTE; every site's pool now leaves at one steady rate since the pipeline dried up.
- Item and flag rates per question stepping up in 2023: dropped at the prototype, because a pooled ratio (over the
  step) and a reviewer trend over 2024 carry errors of opposite sign that cancel near the golden; both rates hold steady.
- Sizing the pool on the busiest 2027 month (shape 02): dropped at the prototype, because each late-2027 month's network
  hours carry about 300 hours of one-sigma spread, too wide for a monthly grid at any natural rounding.
- A volunteer pace with a wide spread across reviewers (KAPPA_SIG 0.60): the 2021 to 2023 and 2024 to 2026 saturated
  paces differed by 3.6 per cent, which moved Data & ML across its bin between eras; reviewers' own paces now spread at
  0.15.
- A Poisson trickle of new reviewers after the pipeline dried up: carried or dropped, it moved two sites by 0.4 FTE; the
  trickle is now a floor share (0.004) of the old inflow, and no construction moves a site.
- Pre-platform reviewers' grant dates drawn freely: they piled up at January 2013; tenure is now bounded by each site's
  launch on the register.
- Cover targets calibrated against random-walk inflows and exits: the calibration moved the wrong way; exits and inflow
  are now constructed (zero-sum swings within each quarter), and the January to September 2026 cover targets of
  Databases and Embedded & Hardware were set at 1.137 and 0.76 to centre their needs in their bins.
- Question moves drawn by source site: they ran the wrong way and reached 90,000 rows; moves are drawn into each
  destination at 0.55 of the first shares (49,530 rows).
- October to December 2026 on the chart with no question driver: a trend of each site's questions would be an open
  fork; the plan workbook carries the planning team's outlook sheet for those months, used only for the chart.
- WFM shifts of 7.5 paid hours: half the quarter totals ended on a half hour, a rounding fork at the nearest hour;
  shifts are now 8 paid hours, short days, overtime and corrections in whole hours.
- First actions on flags with an unbounded lognormal tail: some ran past the moderator tool's export run, dating rows
  after the as-of; a flag left past 90 hours is now escalated and taken within the next week of hours (no Ask A figure
  moves), and a review still open at the export keeps its first action as the handled time.
- The network first named Quernstone: a UK accounting firm carries that exact name (Companies House 04197485); the
  network is now Millrind (no company, network or software of that name found).
- Ask C's stop "each move applied in the month it moved": it files the golden's nine (no move straddles the window's
  edges enough to cross a rounding step), so it is recorded as a convergence, not a stop; Ask A's over-correction stop
  (reviewed flags dropped) misses 14 of 27, not 27.
- target.zip cut with a `target/` folder inside: the archive now carries the files at its root (house fix H4).
- Round 1, Ask C's device left silent (no file said how the old statistics job counted a moved question): the judge
  licensed three readings one decimal apart at every site (FIX_NOW). The warehouse notes now file the old job's counting
  and the comparison basis in the data team's voice; both other readings are asserted out. The device is no longer
  silent, so the cracker and the mirror both land Ask C (cracker sheet `hit`).
- Round 1, slide 2's series undefined (hours worked or need hours, flags in or out, which close standard, how October
  to December 2026 is counted): the operations notes now define paid review hours once, the prompt asks each year's
  actual hours totalled, and the three actual totals are graded and asserted (36,419, 36,233 and 29,626 hours); being
  construction figures, both top responses land them (cracker sheet `hit`). With Ask C, the pair ceiling moves from
  31.0 to about 41.0, over the 40 build target and under the 50 bar; precut fails its pair-ceiling and cracker rows on
  this alone, reported to the coordinator.
- Round 1, the roster missed the reviewers whose access lapsed in January or February 2024 without a platform review
  (its dictionary scope said every reviewer with access since 1 January 2024): a lapse rate read by lapse date then
  counted zero lapses in those months (1.92 per cent, 33). The 689 rows are now in the roster (first review blank), the
  dictionary's scope and lapse rule carry a worked example, and the lapse-date reading files the same nine.
- Round 1, the items no volunteer ever picks up drawn at one share for every item type: routed shares were identical
  across types in slack months, which read synthetic. Each type now has its own (close votes 0.91, low quality 0.72,
  edits 0.40, first posts 0.35 per cent); no graded figure moved. In saturated months the shares stay close across types
  because the 72-hour hand-off takes the oldest items first whatever their type; a per-type volunteer preference would
  change the routed mix that prices the frozen call, so it was not added.
- Round 1, the 24-hour share's denominator and the envelope's sign: the flag service standard now defines flag
  response as a share with the post-deleted closures out of both counts, the prompt names the measure (24-hour flag
  response), and the prompt asks how far above or below the envelope the request sits.
- Round 1, the question plan's 2026 actuals sheet stamped as pulled 8 October inside a workbook issued 18 September:
  the sheet now carries January to August 2026 as pulled on 14 September (no figure reads it).
- Round 2, Ask C held only less careful solvers once round 1 filed the old job's counting (the cracker landed it, precut
  failed): the 2022 sheet now carries the tag-sync undercount of May to August 2022 as first reported, with the
  statistics job's March 2023 restatement below its notes (sites down, months across); the careful-but-literal path
  misses all nine (nearest 0.27 points) and the golden's nine figures are unchanged.
- Round 2, the chart's three actual yearly totals (round 1): construction figures both top responses land; out of the
  prompt and the deliverable answers. The chart is graded on its content, its series filed in the operations notes and
  its months on the workbook's Monthly hours sheet. The pair ceiling is back to 31.4.
- Loop 3 (2026-10-27), the portal landed the call: both responses filed 35 FTE (the then golden) by building capacity
  against the inbox at the saturated pace and carrying each pool at its own lapse rate; the capacity framing was every
  strong solver's default, so it is now the default path and the decisive step moved to how the pool is carried.
- Two retention types with the pipeline drying in late 2024 or summer 2025: a trend of the network's lapse rate,
  extrapolated, landed the golden by coincidence (the closed pool's decline was already plain in the record); review
  access now closes on 1 September 2026, so the record shows only an open pool's flat rate.
- Grants following the question level squared (older pools at the sites AI hit hardest): the separations shrank and the
  trended-rate routes still tracked the golden; grants now follow the question level.
- Grants drying in January 2026 with the last twelve months' grants carried on: the two errors cancelled on the golden;
  with invitation-only access filed, no window of past grants is a reading of 2027.
- Invitations at 2 per cent of the old flow: carrying or dropping them moved a site by 0.44 FTE in all; invitations
  are now a handful a year and none fell in September.
- Covers calibrated by re-drawing the whole pool at each step: a site's need jumped by up to a whole FTE between
  iterations; each reviewer now draws from their own stream and each month's grants from a fixed quantile, so a cover
  change only adds or removes reviewers at the margin.
- The data dictionary, the file list, the operations notes and the warehouse notes (markdown): a file that describes the
  data is a leak (`dataset-generation` section 3); the conventions the asks and the chart need now sit in the operations
  handbook and the question count standard, and every export names its own columns.
- Annual netting at Databases and Infrastructure & DevOps 0.07 and 0.12 FTE from their bin edges, and the world's
  realised 2027 one bin lower at Data & ML (the 72-hour queue carries a short month's backlog into the next month's
  spare capacity): the three sites were re-centred slightly above their integers, and a day-by-day simulation of the
  hand-off on the forecast pool is asserted to file the same nine.
- Architecture 1 as a whole (2026-10-31, the batch 1 triage): the moderation pool's world, prompt and asks had been
  solved once on the portal and loop 3 kept them, so the slot is re-rooted in a new world with a new mechanism; the
  pool's leaving rate falling as fast leavers go first is spent for this slot.
- Re-root draw screens (2026-10-31), each rejected before any data was cut: a mixed-population flood frequency (spent
  in task273 and task130's notes); an event-driven trial's event count (task171 and task174 hold it); a dialysis
  cohort's eGFR slopes (a patient-level slope is the obvious route and the method forks); a vineyard's frost nights
  under inversions (dead in task170's notes); a health system's access change and a climate-extremes count (both
  measured dead in task174 and task170's notes); this slot's own frailty and tenure hazard (architecture 1).
- The first card probe for this draw carried `validated_decoy` true and Gap 1 first: BLOCKed on
  `two_layer.validated_decoy` (a closed record built to bless the wrong method) and on a structural signature spent in
  five builds. The design is drawn so the meter's own high-water-table storms and the overflow log refute one response
  per millimetre for anyone who checks them, and population (the meter's days are not the replay's) is the decisive gap.
- A June 2025 high river with storms in it (the spell centred in August): the meter logged three overflows in it that one
  response per millimetre misses, so the overflow log refuted the stop rung at the count level, a search signal; the spell
  now falls in a dry month of 2025 and the meter's logged overflows are dry-ground storms every rung reproduces.
- The spell's peak held below the replay's wettest days (12.6 km of sewer below the water table against 20): 812 replay
  days sat above anything the meter saw, so the deciding configuration was out of sample and the infiltration had to be
  extrapolated; the spell now reaches the replay's wettest days (one replay day above the meter's maximum).
- Pumps below the wet-winter base (92 to 100 L/s): the station spilled in dry weather on groundwater alone and the
  consent's 24-hour rule merged wet weeks into single long overflows, so more inflow could file fewer overflows and the
  count was not monotone in the flow; the pumps now sit above the wettest dry-weather peak and every overflow needs rain.
- Assumed unit hydrograph shapes and a crown or centreline reference for the submerged length: the replay spread 2.1 to
  5.0 a year, but only because those variants fit the meter two to three times worse; among fits within a few per cent of
  the best the figures agree inside the whole-number bin, so the figures are graded to whole overflows a year.
