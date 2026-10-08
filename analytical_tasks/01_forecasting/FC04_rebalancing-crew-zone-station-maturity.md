# FC04 — Which zone gets next season's extra overnight rebalancing crew, when its newest stations have not finished growing

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Supply Chain & Logistics · micromobility fleet rebalancing |
| Mirrors | Sizing operations to a network whose newest nodes have not matured (Lime and Uber micromobility rebalancing, Amazon delivery stations in their first months, quick-commerce dark stores, newly lit cell sites ramping toward steady traffic) |
| Decision shape | Which of N gets one scarce thing: one additional overnight rebalancing crew for one of six service zones |
| Committed call | The zone that receives the extra crew next season, named in the budget letter, with its forward nightly need |
| Gap · Pattern | Gap 1 (time) over Gap 2 (population) · Pattern A (the measured past against forward yield), carried by maturity: the forward need of stations still on their ramp |
| Gate G mechanism | forecasting, with decomposition_attribution |
| Measured traps engaged | #5 takes the population a flag or filter suggests · #13 validates on one population, applies to another · #25 assumes an effect the log could measure |
| Calibration form | Change-log natural experiments: nine earlier station-commissioning batches, each logged with dates and weekly trips against matched mature stations |
| Driving force | Riverside's eighteen newest stations opened five weeks before the season closed and ran at 25% of the level every earlier batch reached by week 17. Every closed season was fully mature, because all earlier batches opened in the off-season, so last season's need forecasts each next season exactly. The new stations' forward need comes from the registry's commissioning dates and the ramp the nine logged batches share. No trip column carries a station's age. |

## 1. Situation

A city bike-share operator runs overnight crews that move bikes from where they pile up back to where the morning commute starts. It can
fund one more crew next season and must tell the city's transport department which of its six zones gets it. The operations standard
sizes crews on the coming season's average nightly rebalancing for the stations in each zone, using the zone assignment in force on
opening day. This autumn a permit delay held back Riverside's expansion, and 18 stations were commissioned five weeks before the close.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the trip table, the rebalancing log, the crew shift log, the station registry and the change log.
  No one's claim about their own numbers is overturned. The difficulty is that a new station's first five weeks say little about its
  next season.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the transport department's basis. Net imbalance from trips still names Harbourside, and the
  closed seasons still confirm it.
* **Instrument repair.** No file is suspect: the rebalancing log is a complete record of moves done, by the crew that did them, and the
  trip table holds every trip, the new stations' five weeks included. Even a log of uncapped need by station zone returns Harbourside at
  rungs 0–2 (190 against 150), because the new stations' mature level lies five months ahead.
* **Lens swap.** The naive read and the answer differ in moment: eighteen stations in their fifth week of service against the same
  stations in a mature season.

## 3. The driving force

A strong solver moves from logged moves to the zone the standard defines, sees that capped crews log less than the need, and rebuilds the
need from net overnight imbalance in the trip table. That build reproduces every uncapped zone's logged moves exactly and names
Harbourside. It also reads eighteen Riverside stations as quiet. They are not quiet, they are young. Every earlier batch in the change log
ran at 25% of its eventual level for eight weeks and reached 100% by week 17, measured against matched mature stations. All of those
batches were commissioned in the off-season and matured before any season opened, so no closed season contains a young station. Riverside's
forward need is its mature stations plus the eighteen at full level. That comes from the registry's commissioning dates and the logged
ramp, and it is 2.5× what the trip table shows.

## 4. The ladder

| Rung | Construction | Names (nightly moves) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Last season's logged overnight moves, grouped by the log's crew-zone field | A, Downtown (152 against 118) | The operations record of overnight work, grouped the way crews are run | The station registry's effective-dated zones: the standard counts moves at the zone's stations, and Downtown's crew serves 38 moves a night in two neighbouring zones |
| 1 | **E33 (the population a field suggests):** moves re-attributed to the zone of the station served, on opening-day boundaries | B, University (142 against 114) | Every move now sits where the standard puts it, and the total still ties to 585 | The crew shift log: University, Harbourside and Riverside trucks ran at capacity on most nights, so logged moves are work done, not need |
| 2 | Net overnight imbalance per station from the trip table, summed by zone | C, Harbourside (190 against 150) | The need itself, uncapped; it equals logged moves exactly in every uncapped zone | The registry's commissioning dates and the change log's ramp: Riverside's eighteen newest stations are at 25% of maturity |
| 3 | **Decisive:** mature stations' imbalance plus each new station's imbalance raised to maturity by the logged ramp | **D, Riverside** (300 against 190) | — | — |

* **Position table.** Riverside is 5th on rung 0 (70), 5th on rung 1 (84) and 3rd on rung 2 (120), and leads only rung 3. Each rung's
  leader beats its runner-up by 1.29×, 1.25×, 1.27× and 1.58×.
* **Discriminator dominance.** Harbourside carries a 1.58× advantage into rung 3 (190 against 120). Riverside's maturity edge is 2.50×
  (300 against 120), 1.32 times the required 1.2 × 1.58 = 1.90, for a final margin of 1.58×.
* **Partial correction priced (L3).** The commissioning step is dated and visible, so an event study reads Riverside's post-step run-rate
  and annualises it: 159 moves, and Harbourside still leads by 1.19×. Raising the new stations by the ramp on their season-average share
  instead of their weekly rate gives 146, which leaves Harbourside ahead (1.27× over University) and Riverside third.
* **Grid.** Need basis (logged by crew zone, logged by station zone, imbalance) × new-station treatment (as observed, annualised run-rate,
  matured by the ramp) gives 9 cells. No logged move touches a new station, because routes are rebuilt monthly and the eighteen joined
  the November build, so the logged rows collapse to Downtown and University. The imbalance row names Harbourside, Harbourside and
  Riverside. The nearest wrong cell is the run-rate cell (Harbourside by 1.19×).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The change log records batches and their trips. No document says new stations ramp or that Riverside's are
   young, and the registry's commissioning date is one field among forty.
2. **Corpus blind for a computable reason.** *In every closed season each station had at least 17 weeks of service before opening day,
   because all nine earlier batches were commissioned in the off-season, between late October and early December.* Last season's imbalance, grown by the filed factor,
   reproduces each of the four closed seasons within 1%.
3. **No arithmetic symptom.** Moves re-attribute without loss (585 both ways), and imbalance ties to logged moves in every uncapped zone.
   Young stations trip no check.
4. **Not a row predicate.** Maturity is a station's age at the extract, joined from the registry, mapped through a ramp recovered from
   nine batches, and applied to its weekly imbalance before summing by zone.
5. **The enumeration is arithmetic.** Which stations are young and how far from maturity is computed. No column flags them.
6. **No cutover date carries the answer.** The commissioning step is dated, and it is the decoy: aligning to it lands on Harbourside. The
   decisive quantity is the part of the ramp no series has reached.
7. **Survives deletion.** No wrong number exists to delete. Without the voices, rung 2 is where a careful build stops.

## 6. The calibration corpus

* **Form.** The operations change log: nine station-commissioning batches over five years, each with its stations, commissioning dates
  and 26 weeks of trips against matched mature stations in the same zone.
* **What it certifies.** The ramp: 25% of the mature level in weeks 1–8, rising linearly to 100% at week 17, identical within one point
  across all nine batches. It also certifies the imbalance construction, because each batch's zone need rose by the batch's matured
  share.
* **What it cannot show.** A young station inside a season (above).
* **Twin pair.** Stations K-31 (batch 6, in week 11 at the batch's winter review) and E-09 (Eastgate, three years old) were identical on
  every trip-table column in the review week: 19 docks, the same trips and nightly imbalance, and the same residential class. The next
  season K-31 needed 2.0× E-09's moves, because in week 11 it stood at 50% of its ramp. Only age from the registry, read through the
  ramp, reproduces both.
* **Resemblance points at the decoy.** The eighteen new stations resemble Eastgate's low-demand residential stations on every column the
  trip table carries.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The operations standard: crews are sized on the coming season's average nightly rebalancing for the stations in each
  zone, using the zone assignment in force on opening day. The planning sheet: a growth factor of 1.05 for every zone.
* **Empirical pins.** The ramp, from the change log. The imbalance construction, from the uncapped zones' logged moves.
* **Voices.** The operations director: "Downtown always eats the most crew hours; that's where the bikes pile up." The data-science
  lead: "Riverside's new stations are quiet. We over-built there."
* **Licensed wrong basis.** The standard records that the transport department, which co-funds crews, allocates on logged moves by crew
  zone and will present that allocation at the budget meeting.

## 8. Determinism by construction

* **Night and boundaries.** A night is 22:00–05:00, trips are timed by undocking, and no station changes zone between the extract and
  opening day.
* **Ramp position.** Every new station is in weeks 1–5 at the extract, inside the 25% plateau, so no interpolation convention is
  exercised.
* **Imbalance.** Need is each station-night's positive net outflow, summed; this reproduces logged moves exactly in Downtown, Midtown and
  Eastgate, whose crews never hit capacity.
* **Growth.** The filed factor is uniform, so it cannot reorder zones.
* **Routes.** Crew routes are rebuilt monthly from stations with four full weeks of service, and the eighteen new stations joined the
  November build, after the late-October close, so no logged move touches them and
  the maturity question can only be asked of the trip table.
* **Maturity of the record.** The season's trips are complete at the extract; the open-trip queue was empty at close.

## 9. Prompt sketch and deliverables

> We can fund one more overnight crew next season, and on Thursday I have to tell the city which zone gets it. Our operations director
> is certain it belongs downtown. Name the zone in one sentence I can put in the budget letter, with the nightly need it is sized
> against, and send me `crew_zone_case.xlsx`, a chart `zone_need_ladder.png`, and a short `crew_allocation_memo.pdf`.

* `crew_zone_case.xlsx` — the need build for all six zones, the outage sheet (ask A) and the repair sheet (ask B).
* `zone_need_ladder.png` — the six zones' nightly need under the four constructions as grouped bars, Riverside's new-station share stacked
  and labelled, an inset of the nine batches' ramps, and the chosen zone marked.
* `crew_allocation_memo.pdf` — the committed zone, its need, the runner-up and why each other zone falls away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each zone, the share of last season's mornings with at least one station empty for more than
  60 minutes between 07:00 and 09:00, and the worst month. *Device:* dock telemetry posts communications loss as an offline status, which
  the telemetry dictionary excludes from emptiness. Reading offline as empty overstates outage mornings in two zones.
* **Ask B (device-carried).** For each zone, bikes out of service at each month-end and the mean days to repair. *Device:* a bike moved
  between workshops closes its ticket as a transfer and opens a new one, as the maintenance manual documents. Counting tickets as repairs
  double-counts transferred bikes and restarts their clocks, understating days to repair in three zones.
* **Ask C (validity).** Each zone's nightly need under each of the four rung constructions, and each construction's fit to the nine
  change-log batches.
* **Decoupling.** Removing the ramp adjustment changes no figure in asks A or B.

## 11. Rubric arithmetic

6 zones × 2 (ask A) + 6 zones × 2 (ask B) + 6 zones × 4 constructions (ask C) + the committed zone, its need, the runner-up and the
margin + 5 named chart parts + 3 files ≈ 60 criteria.

## 12. World-building constraints

* Rung needs: 152/118/108/92/70/45 (crew zone), 142/114/108/92/84/45 (station zone), 190/150/120/114/92/45 (imbalance), and Riverside 300
  at rung 3. Riverside's mature stations need 112 a night and the eighteen new ones 188 at maturity (25% plateau, five of 28 weeks).
* The new stations opened five weeks before close. All nine earlier batches opened between late October and early December and share the 25%-to-100% ramp.
* University, Harbourside and Riverside crews ran at truck capacity on most nights; the other three never did.
* K-31 and E-09 are identical on every trip-table column in the review week; K-31's next-season need is 2.0× E-09's.
* Telemetry offline intervals and workshop transfers never touch trips, moves or the registry.
