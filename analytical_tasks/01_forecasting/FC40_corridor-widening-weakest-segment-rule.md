# FC40 — Which cycle corridor gets the one widening before next summer, when a corridor is only as passable as its narrowest segment and the headline counter sits on its widest

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Policy & Education · urban active-travel planning |
| Mirrors | Placing a capacity investment where a chain of sub-units binds at its weakest link (conveyor lines limited by their slowest station, network paths limited by their narrowest link, road-segment congestion against route-level counts in mapping and ride-hail products) |
| Decision shape | Which of N gets one scarce thing: next year's single corridor widening, to one of six corridors |
| Committed call | The corridor to widen, and its forecast number of crowded days next summer |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · a minimum over sub-units (every segment must pass for the corridor to pass), recovered from a gold-standard subsample, with the segment coarsened (measured #14) at rung 1 |
| Gate G mechanism | method_or_model_selection, with forecasting support |
| Measured traps engaged | #14 coarsens the segment it was asked about · #4 never tests its reading against the control · #3 stops at a close but inexact match |
| Calibration form | Gold-standard verification subsample: 140 corridor-days on which trained observers walked each corridor and recorded whether cyclists could still pass safely |
| Driving force | Observers call a corridor crowded on a day when, in that day's peak hour, any one of its segments carries more than 85% of the flow its width can take. Every rival law, on the corridor's total, its headline counter or its average, has a flat loss curve on the 140 observed days. Each corridor's headline counter sits on its widest, busiest stretch; Millrace Way's counter reads moderate, but a 2.4-metre segment by the old mill carries almost all of its flow and is over the line on 41 summer days. |

## 1. Situation

A city can widen one cycle corridor before next summer, and its active-travel policy sends the widening to the corridor forecast to be
crowded on the most summer days. Each of six corridors has a headline counter shown on the city's dashboard and two to five further counters
along its segments. The pack holds every counter's hourly counts for three summers, the path inventory of segment widths, the design guide's
capacity by width, the counters' maintenance log, and the observers' records. The forecasting convention replays the last three summers'
days scaled by each counter's year-on-year growth. The committee report is due in a fortnight.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: hourly counts, widths, capacities, the dashboard and the observers' records. No stakeholder's reading
  of their own numbers is overturned; the bridge counter really is the busiest in the city. The difficulty is what makes a corridor crowded,
  which no document states and the observers' records pin.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the dashboard and every voice. A corridor's busiest counter is still its natural measure, and any threshold on it
  still matches the observations about two times in three.
* **Instrument repair.** Clean-data test. One file is suspect: Canal Street's headline loop over-counted by 40% on 26 days before
  recalibration. Corrected, rung 0 still names Harbour Bridge and rung 1 names Station Approach (rung 2's leader), neither Millrace Way.
  Every other counter, the path inventory and the capacity table are complete, the observers' records hold every corridor-day they claim,
  and the weakest-segment rule is still needed, because next summer's crowded days are a replay of segment flows through it.
* **Lens swap.** The naive read and the answer count different populations: days on which the corridor's busiest point is busy, against days
  on which its weakest segment fails, which happen on different days and different corridors.

## 3. The driving force

A strong solver replays three summers through each corridor's headline counter, counts days above the dashboard's 7,000, then moves to the
peak hour the policy names and compares the peak-hour flow with the headline segment's capacity, cleaning out a counter fault on the way. Each
step is correct, and each names a busy downtown corridor. But a corridor is a chain of segments. The observers' records reproduce only when a
corridor-day is crowded because some segment, in that day's peak hour, carries more than 85% of what its width can take: one narrow stretch is
enough. The headline counters were put where flows are largest, which is where paths are widest. Millrace Way's headline counter, on its
four-metre riverside stretch, reads moderate; its 2.4-metre mill segment carries 94% of the same flow and crosses the line on 41 replayed
summer days a year, more than any downtown corridor's weakest segment.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Replayed days with the headline counter's daily total above the dashboard's 7,000 | A, Harbour Bridge (22 days; 1.47×) | The city's own crowding indicator, run through the agreed replay | The policy assesses flow in the peak hour (the busiest 60 minutes in 07:00–09:30 or 16:00–18:30), not over the day |
| 1 | Peak-hour flow at the headline counter above 85% of the headline segment's capacity | B, Canal Street (31 days; 1.29×) | The fine segment the policy names, at the design guide's capacity | The maintenance log: Canal Street's headline loop over-counted by 40% on 26 of last summer's days before recalibration |
| 2 | Hygiene: the faulty loop's days replaced by its recalibrated ratio to the neighbouring counter | C, Station Approach (24 days; 1.26×) | Clean, peak-hour, capacity-based, and every count reconciles | The observers' records: a headline-counter rule matches 104 of 140 observed corridor-days, and every miss is a day a narrower segment was over capacity |
| 3 | **Decisive:** a corridor-day is crowded if any segment's peak-hour flow exceeds 85% of that segment's capacity for its width | **E, Millrace Way** (41 days; 5th of 6 on rung 0) | — | — |

* **Position table.** Millrace Way ranks 5th on rung 0 (4 days), 4th on rung 1 (9) and 4th on rung 2 (9), and leads only rung 3, by 1.58×
  over Station Approach (26). Rung leaders beat their runners-up by 1.47×, 1.29×, 1.26× and 1.58×.
* **Discriminator dominance.** Station Approach carries a 2.67× advantage into rung 3 (24 days against 9). The weakest-segment rule
  multiplies Millrace Way's days 4.56× (9 to 41) and Station Approach's 1.08× (24 to 26), an edge of 4.21× against the 3.2× that 1.2 × 2.67
  requires. The product, (1/2.67) × 4.21 = 1.58×, is Millrace Way's margin.
* **Partial correction priced (L3).** Every half-applied rule names a wrong corridor. Checking every segment in the peak hour but
  against the headline segment's capacity, ignoring widths, names Station Approach (25 days against Canal Street's 19, 1.32×): the mill
  segment carries less flow than Millrace Way's wider headline stretch, so it never binds at that stretch's capacity and Millrace Way
  stays at 9. Checking every segment against its own width but on daily totals names Harbour Bridge (24 days against Canal Street's 16,
  1.50×; Millrace Way 12), because Millrace Way's flow is packed into its commuter peaks.
* **Grid.** Time grain (day, peak hour) × counters (headline, every segment) × capacity (one threshold, each segment's width) × hygiene
  (raw, recalibrated) = 16 cells. Only peak hour, every segment and each segment's width together name Millrace Way, at 41 days with or
  without the loop correction (Canal Street reads 32 raw, still 1.28× behind). Every other cell names Harbour Bridge, Canal Street or
  Station Approach; the nearest is Station Approach by 1.32×.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The policy calls a corridor crowded "when cyclists can no longer pass safely" and names the peak hour; the design
   guide gives capacity by width. Nothing says crowding is decided segment by segment or that one segment suffices.
2. **Reproduction (Pattern B).** The weakest-segment rule reproduces 140 of 140 observed corridor-days; the headline counter's peak hour 104;
   the corridor's average across counters 96; daily totals 88. Every rival has a flat loss curve: any daily threshold from 6,000 to 8,000
   matches 84–90, so no threshold rescues it. The rule is a construction, not a menu: a group over each corridor-day of segment flows, each
   joined to its own width's capacity, and a maximum taken across them.
3. **No arithmetic symptom.** Segment counts reconcile to cordon totals, widths to the inventory, and the dashboard reproduces exactly.
4. **Not a row predicate.** Whether a corridor-day is crowded depends on the worst of several segments' peak-hour flows against several
   widths, so it needs a group and a maximum before any count of days.
5. **The enumeration is arithmetic.** No column marks a segment as the bottleneck; which segment binds on which day is computed.
6. **No cutover date.** The mill segment has been 2.4 metres for decades; nothing steps.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** 140 corridor-days over three summers on which trained observers walked each corridor at peak hour and recorded whether cyclists
  could still pass safely anywhere along it, with the counter data for those days.
* **What it certifies.** The peak-hour definition and the guide's 85% comfort line: both reproduce the observations wherever the headline
  segment is also the narrowest.
* **What it pins.** The weakest-segment rule (above).
* **Twin pair.** Station Approach on 14 July and Millrace Way on 21 July of the second summer show identical headline counters: daily total,
  peak-hour flow and peak-hour share. Observers recorded Millrace Way crowded and Station Approach clear, and over the whole replay their
  crowded days run 41 against 26 (1.6×), because Millrace Way's flow passes through 2.4 metres and Station Approach's through 3.5. No rule
  on the headline counters reproduces both.
* **Resemblance points at the decoy.** By headline flows, Millrace Way most resembles the corridor-days the observers recorded clear.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The policy: the widening goes to the corridor forecast to be crowded on the most summer days next year; flows are assessed
  in the peak hour, the busiest 60 minutes in 07:00–09:30 or 16:00–18:30. The forecasting convention: replay the last three summers' days,
  each counter scaled by its year-on-year growth. The design guide's capacity table by path width, with its comfort line at 85%.
* **Empirical pins.** The weakest-segment rule, from the observations. The faulty loop's correction, from its recalibrated
  ratio to its neighbour.
* **Voices.** The cycling officer: "The bridge counter is the busiest in the city; it's obviously the corridor." The traffic engineer:
  "Peaks are what hurt; look at the peak hour, not the day." The ward councillor: "The station approach is where the complaints come from."
* **Licensed wrong basis.** The policy records that the regional transport authority ranks corridors on their headline counters' days above
  7,000 and will present its view on that basis.

## 8. Determinism by construction

* **Replay.** The convention fixes the three summers and each counter's growth factor; every rung uses the same replayed days.
* **Line distance.** No segment's replayed peak-hour flow sits within 3% of 85% of its capacity, so the line's exact placement does not
  move any day.
* **Peak hour.** The busiest 60 minutes are taken from fifteen-minute counts on a rolling start; hourly-aligned and rolling readings give
  the same crowded days because every peak sits wholly inside a clock hour on the observed corridors.
* **Missing data.** Every segment counter is complete for every replayed day except the documented loop fault, whose correction is pinned.
* **Rounding.** Crowded days are counts and need none.

## 9. Prompt sketch and deliverables

> We can widen one cycle corridor before next summer, and the committee wants it where crowding is worst. Our cycling officer is sure it's
> the bridge, since its counter is the busiest in the city. Name the corridor and the number of crowded summer days you forecast for it, in a
> sentence for the committee report, and send `widening_case.xlsx` with the build and the sheets below, a chart `corridor_bottlenecks.png`,
> and a one-page `widening_memo.pdf`.

* `widening_case.xlsx` — crowded days by corridor and segment under each construction, the collision sheet (ask A) and the bike-share sheet
  (ask B).
* `corridor_bottlenecks.png` — for each corridor, a strip of its segments in order, each coloured by replayed peak-hour flow as a share of
  its capacity, the headline counter marked, the binding segment outlined, and crowded days labelled at the end of each strip.
* `widening_memo.pdf` — the committed corridor and days, and why each of the other five is not it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the six corridors, last summer's collisions involving cyclists, by severity (slight,
  serious, fatal). *Device:* a collision at a junction where two corridors meet is assigned to both in the collision geography, with the
  junction flagged in the collision data guide; counting by corridor double-counts eleven junction collisions. Collisions enter no part of
  the crowding forecast.
* **Ask B (device-carried).** For each corridor and summer month, bike-share trips starting or ending within 200 metres of it. *Device:* the
  operator's staff move bikes between docks as logged trips under staff accounts, which the operator's data note excludes from ridership;
  counting them overstates trips near four corridors.
* **Ask C (validity).** Each corridor's crowded days under each of the four rung constructions, and how many of the 140 observed
  corridor-days each construction reproduces.
* **Decoupling.** Clearing the weakest-segment rule changes no figure in asks A or B.

## 11. Rubric arithmetic

6 corridors × 3 severities (ask A) + 6 × 3 months (ask B) + 6 corridors × 4 constructions (ask C) + the committed corridor, its crowded days
and its margin + 5 named chart parts + 3 files ≈ 71 criteria.

## 12. World-building constraints

* Crowded days by rung (Harbour Bridge, Canal Street, Station Approach, Riverside Loop, Millrace Way, Northfield): rung 0 22/15/11/8/4/2;
  rung 1 18/31/24/7/9/3; rung 2 18/19/24/7/9/3; rung 3 21/20/26/9/41/4 (Canal Street 32 without the loop correction).
* Partials (same order): every segment at the headline capacity 18/19/25/7/9/3; each width on daily totals 24/16/13/9/12/2.
* Millrace Way: headline counter on a 4.0-metre segment; the 2.4-metre mill segment carries 94% of its flow.
* Observations: 140 corridor-days; reproduction 140 / 104 / 96 / 88; daily thresholds 6,000–8,000 give 84–90.
* The twin corridor-days are identical on every headline-counter column.
* Collision geography and staff rebalancing touch no counter, width or replayed day.
