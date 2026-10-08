# DA20 — How a bus agency shares 60 headway-supervisor posts, when the frequent network ends where four routes' branches begin

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Supply Chain & Logistics · urban bus operations |
| Mirrors | Allocating field staff on a metric pooled over a whole line when the commitment covers only its high-frequency section (ride-hail and delivery ETA promises that apply inside dense zones, cloud latency objectives that cover only premium regions, fulfilment pick-rate targets set for fast-moving zones only) |
| Decision shape | An allocation: 60 weekday-peak supervisor posts shared across the eight routes of the 2027 frequent network in proportion to passenger-hours of excess wait on the frequent network |
| Committed call | Posts per route in whole numbers summing to 60, headed by route 14's |
| Gap · Pattern | Gap 3 (objective) over Gap 4 (rule) · E18, the segment the standard names (the frequent network's stop ranges) coarsened to whole routes, with E22 (excess wait, which only the mean and spread of headways together give) and the vendor's revised departures below it, and a revision log blind to branches (L1) |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #14 coarsens the segment it was asked about · #20 leaves the deciding comparison unstated · #12 stops at the first control that passes · #7 uses the ready-made measure |
| Calibration form | Retry or revision log: the programme's quarterly log, Q1 2023 to Q3 2026, each supervised route's provisional excess wait and its revised figure after the location vendor re-ran unmatched pings |
| Driving force | The standard shares posts by excess wait on the frequent network: the stop ranges where riders turn up without a timetable, listed on the network map. Every table the agency keeps is by route. Four of the eight routes run a frequent trunk into an infrequent branch, where 30-minute headways drift far from the timetable. Pooled by route, that branch delay looks like the bunching supervisors manage, and it hands those routes 11 more posts. On the frequent network alone, route 14, a crosstown trunk that is on time on average and bunched all day, rises to 13. Every quarter in the revision log comes from routes that are frequent end to end, so the log reproduces the pooled measure perfectly. |

## 1. Situation

A city bus agency's headway-management programme posts supervisors at timepoints in the weekday peaks to keep buses evenly spaced. For
2027 the frequent network has eight routes (3, 7, 9, 14, 22, 31, 40 and 52) and the programme has 60 posts. The programme standard shares
them in proportion to weekday-peak passenger-hours of excess wait on the frequent network. The pack holds the location vendor's
departures at timepoints (as first published and as revised), automatic passenger counts by stop, the timetable feed, the frequent-network
map with each route's frequent stop range, the revision log, the monthly service report and the standard. The split is published on 8
January 2027.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: departures, revisions, boardings, the timetable, the map and the log. The service report's
  route lateness is right about routes, and nobody's reading of their own numbers is overturned. The difficulty is which riders the
  standard counts.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the operations chief's view, the analyst's view and the riders' council's basis. Every table in the pack is
  still kept by route, and the revision log still reproduces the route measure exactly.
* **Instrument repair.** Perfect the location data and the branches still run 30-minute headways that drift. A branch's waiting is real
  delay, measured correctly. It is simply not the waiting the standard allocates on.
* **Lens swap.** The two reads count different riders: everyone boarding the eight routes in the peaks, against the 61% who board on
  the frequent network. Branch riders are outside the second population.

## 3. The driving force

A strong solver sees that the service report's lateness (mean headway against the timetable) is not excess wait. It computes the
expected wait of a rider arriving at random from the observed headways at each timepoint, subtracts half the scheduled headway and
weights by boardings, the comparison the standard names. It then finds that the vendor's revised departures differ from the first
release where unmatched pings split headways in the downtown canyon, switches to the revised file, and reproduces all 60 route-quarters in
the revision log. That is complete and back-tested. But the standard counts excess wait on the frequent network, and the map ends four
routes' frequent ranges where their branches begin. Beyond that point buses run every 30 minutes, riders time their arrival to the
timetable, and the long, irregular headways that dominate a pooled route figure are a dispatch problem, not a spacing problem. Restricted
to the map's stop ranges, the branch routes lose a third of their posts and route 14 gains four.

## 4. The ladder

| Rung | Construction | Lands on (route 14's posts) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Posts by route lateness (mean headway less scheduled, × boardings), first-release departures | 3 (−76.9%) | The service report's headline measure | The standard allocates on excess wait: the expected wait of a rider arriving at random, less half the scheduled headway |
| 1 | Excess wait by route (E22), first-release departures | 8 (−38.5%) | The standard's named measure, built from the mean and spread of headways together | The revision log: first-release departures reproduce none of its 60 revised route-quarters |
| 2 | Excess wait by route, revised departures | 9 (−30.8%) | Reproduces all 60 revised route-quarters exactly | The frequent-network map: routes 7, 22, 9 and 40 are frequent only to the junction where their branches begin |
| 3 | **Decisive:** excess wait on the map's stop ranges only, with boardings on those stops (E18) | **13** | — | — |

* **Figure shape.** Every correction raises route 14's share, and the answer is the maximum cell. The full table is 3: 5, 7: 6, 9: 7,
  14: 13, 22: 6, 31: 13, 40: 4, 52: 6. Rung 2 gives 3: 4, 7: 11, 9: 7, 14: 9, 22: 9, 31: 9, 40: 7, 52: 4, with the four branch routes
  holding 34 posts against 23.
* **Partial correction priced (L3).** A solver who restricts the headways to the frequent ranges but keeps whole-route boardings as the
  weights gives route 14 10 posts (−23.1%). One who restricts on first-release departures gives it 11 (−15.4%). One who drops the four
  branch routes outright gives it 22 (+69.2%).
* **Grid.** Departures (first release or revised) × measure (lateness or excess wait) × segment (route or frequent range) gives 8 cells.
  Route 14 receives 3, 5, 8, 9, 11 or 13 posts across them, and only revised excess wait on the frequent ranges gives 13. The nearest
  wrong cell is 11 (−15.4%).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The standard says "on the frequent network", the map lists stop ranges, and every table, report and log is kept
   by route under the heading "frequent routes". No document says that a route's branch is outside the measure, or why.
2. **Corpus blind to the segment.** The log certifies the measure and the revised departures exactly. *In every closed quarter the
   frequent range was the whole route, because the programme has supervised only routes 14, 31, 3 and 52, which are frequent end to
   end.* Run over the log, the route and frequent-range constructions return identical figures.
3. **No arithmetic symptom.** Departures reconcile to trips, boardings to the passenger-count totals, and every construction reproduces
   its own rows. A branch's long headways are real.
4. **Not a row predicate.** A timepoint's membership comes from its position in the route's stop sequence against the map's range, and
   the excess wait is a statistic of each timepoint's headway distribution weighted by the boardings it serves.
5. **The enumeration is arithmetic.** 39% of peak boardings and 29% of route-level excess wait fall outside the ranges, computed stop by
   stop.
6. **No cutover date.** The branches have run on 30-minute headways for years, and no series steps.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, every table is still by route.

## 6. The calibration corpus

* **Form.** The revision log: 60 route-quarters (routes 14, 31, 3 and 52, Q1 2023 to Q3 2026), each with the provisional excess wait
  published a week after the quarter and the revised figure published after the location vendor re-ran unmatched pings.
* **What it certifies.** The measure and the departures. The standard's excess wait on revised departures reproduces all 60 revised
  figures. First-release departures reproduce none of them and overstate the log's total by 18%, every quarter the same way. Lateness
  reproduces none.
* **What it is blind to.** Branches (above).
* **Twin pair.** Routes 22 and 31 are identical on every route-level column: peak boardings, lateness (170 passenger-hours), headway
  spread, and route excess wait (520 passenger-hours revised, 660 first-release). Route 31, a supervised route in the log, is frequent end
  to end. Half of route 22's excess wait sits on its branch. On the frequent ranges they carry 520 and 260 passenger-hours (2.0×), and
  13 posts against 6.
* **Resemblance points at the decoy.** On every route-level column, routes 7 and 22 resemble the supervised routes whose excess wait the
  programme cut furthest.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The standard: "Posts are shared in proportion to weekday-peak passenger-hours of excess wait on the frequent network.
  Excess wait at a timepoint is the expected wait of a rider arriving at random, from observed headways, less half the scheduled
  headway, weighted by the boardings at the stops it serves." The peaks are 07:00 to 09:00 and 16:00 to 18:30. Posts are whole and
  shared by largest remainder.
* **Empirical pins.** The measure and the revised departures, from the revision log.
* **Voices.** The operations chief: "The long routes are where riders suffer most." The programme analyst: "The revision log matches our
  method to the minute every quarter."
* **Licensed wrong basis.** The standard records that the riders' council reviews the split against the service report's route
  lateness table.

## 8. Determinism by construction

* **Ranges.** The map lists each route's frequent range by stop, and ranges derived from the timetable (scheduled peak headway of ten
  minutes or less) coincide stop for stop.
* **Revisions.** Each trip's latest revised departure is used. No revision changes a trip's stop sequence.
* **Peaks and days.** Weekdays of Q3 2026, both peaks, every scheduled trip.
* **Allocation.** Largest remainder on unrounded shares, with no tie at any rung.
* **Boardings.** Each stop's peak boardings attach to the timepoint that serves it, as the standard's weighting clause does.

## 9. Prompt sketch and deliverables

> The programme has 60 supervisor posts for 2027 across the eight routes of the frequent network, and I publish the split on 8 January.
> Our operations chief thinks the long routes are where riders suffer most. Give me the posts per route, whole numbers summing to 60, in
> a sentence I can publish, and send `posts_2027.xlsx` with the sheets below and a chart `excess_wait_by_route.png`.

* `posts_2027.xlsx` — each route's excess wait and posts under each rung's construction, the revision log reproduction (ask C), the
  duties sheet (ask A) and the shelters sheet (ask B).
* `excess_wait_by_route.png` — stacked bars of each route's peak excess wait split into frequent range and branch, the posts at rung 2
  and rung 3 as markers, routes 22 and 31 annotated, and the frequent-range boundary drawn on routes 7, 9, 22 and 40.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** Duties worked per operator by garage and month, January to June 2026, for six garages.
  *Device:* a split duty is two pieces of work under one duty number, as the scheduling guide documents. Counting pieces as duties
  overstates 27 of the 36 cells by 6% to 14%.
* **Ask B (device-carried).** Shelter outages (lighting or display) by district and month over the same period, for five districts.
  *Device:* an outage running past midnight continues as a new daily record carrying a continuation flag, as the facilities guide
  documents. Counting records as outages overstates 22 of the 30 cells.
* **Ask C (validity).** Each route's posts under each of the four rung constructions, the revision log's reproduction count for
  lateness, first-release and revised excess wait, and routes 22 and 31's excess wait on the frequent ranges.
* **Decoupling.** Duties and shelter records share no row with the departures, boardings or map. Clearing the frequent-range
  restriction changes no figure in asks A or B.

## 11. Rubric arithmetic

6 garages × 6 months (ask A) + 5 districts × 6 months (ask B) + 8 routes × 4 constructions, 3 reproduction counts and 2 twin figures
(ask C) + the 8 committed posts + 4 named chart parts + 2 files ≈ 117 criteria.

## 12. World-building constraints

* Peak passenger-hours of excess wait per weekday (frequent range / branch, revised): 14: 540/0, 7: 220/430, 22: 260/260, 31: 520/0, 9:
  300/100, 3: 200/0, 40: 160/220, 52: 240/0. First release: 14: 560/0, 7: 240/640, 22: 280/380, 31: 660/0, 9: 420/130, 3: 330/0, 40:
  170/300, 52: 250/0. Lateness (frequent / branch): 14: 70/0, 7: 90/150, 22: 80/90, 31: 170/0, 9: 170/40, 3: 210/0, 40: 60/80, 52:
  60/0.
* Route 14's posts by rung 3 / 8 / 9 / 13; other cells 5 and 11; partials 10 and 22.
* Revision log: 60 route-quarters on routes 14, 31, 3 and 52, reproduced 60/60 by revised excess wait.
* Routes 22 and 31 are identical on every route-level column.
* Duties and shelters touch no departure or boarding.
