# RC45 — Which fix the board funds for next year's school buses, when last year's two largest causes are already fading

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Supply Chain & Logistics · contracted student transportation |
| Mirrors | Carrier remediation at marketplaces and delivery networks (Amazon's delivery service partners, courier fleets at Uber Eats and DoorDash, outsourced last-mile carriers at retailers), where the carrier with last quarter's worst late rate is still onboarding routes it has just taken over and a driver shortage is clearing, so last quarter's excess ranks the remediation budget wrongly for the next one |
| Decision shape | Which of N root causes gets the fix: the board funds one fix for next school year, five aimed at five causes of the incident rise |
| Committed call | Fund the corrective-action plan with Brightway Bus Company: its ageing fleet's breakdowns carry about 1,250 excess incidents into next year, 1.9× any other cause |
| Gap · Pattern | Gap 1 (time) at the decisive rung, Gap 4 (rule) at rung 2 · Pattern A (past exceedance against forward yield), with the moderator in how a route's first weeks with a new contractor treat its incidents, and the finer controls of measured #12 separating two decompositions at rung 2 |
| Gate G mechanism | forecasting, with decomposition_attribution |
| Measured traps engaged | #13 validates on one population, applies to another · #12 stops at the first control that passes · #17 guesses an attribution the data can settle |
| Calibration form | Counterparty acknowledgement file: the contractors' signed acknowledgements of 640 corrective-action notices over five school years, each accepting a figure of excess incidents, with the plan-year acknowledgement of the incidents the plan removed |
| Driving force | The contracts office's excess report is correct, and its footer says it describes the year just ended. Measured against same-zone, same-month peers, the construction that reproduces all 640 past acknowledgements, last year's excess belongs mostly to the driver shortage (2,200 incidents on runs a driver doubled back to cover) and to Atlas (1,800), which took over 60 routes from an exiting contractor between January and April. But the fix buys next year. Aligned on each route's own takeover date, Atlas's excess sits in the route's first ten weeks and then settles to 360 a year. Endorsements have outrun leavers since January, so doubled-back runs fall to 30% of this year's. Brightway's breakdowns come from a fleet that only gets older, and they carry 1,248 into next year. |

## 1. Situation

A city school district contracts its school buses to five contractors on 1,100 routes. Incidents, meaning runs that reach school more than
ten minutes late and breakdowns, rose 60% this school year, from 10,000 to 16,000. The board will fund one fix for next school year, each
aimed at one cause: a request to the city for bus lanes on twelve corridors (traffic), a snow contingency contract (weather), a
corrective-action plan with Atlas Student Transit, which took over 60 routes from Greywell Transit between January and April, a
corrective-action plan with Brightway Bus Company, whose fleet is the oldest, or a retention bonus for drivers at every contractor (the
driver shortage). The transportation office's tally of reason codes puts "Heavy traffic" first, and its director wants the bus lanes. The
contracts manager blames Atlas.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct: the GPS-reconciled incident counts, the reason codes as entered, the route-coverage log, the
  route roster's takeover dates, the excess report, the endorsement file and the acknowledgements. Heavy traffic really is the most entered
  reason, and Atlas really did run the worst excess of the spring. No one's reading of their own figures is overturned. The question is how
  much of each cause will still be there next year.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the reason tally, the director, the contracts manager and every voice. The excess report still puts Atlas first,
  the construction that reproduces the acknowledgements puts the driver shortage first, and nothing in either points at Brightway.
* **Instrument repair.** Suspect: the reason code records each incident's cause with a narrower meaning, the reason a contractor's
  dispatcher chose, on a form that opens on "Heavy traffic". Repair: an independent cause for every incident, what actually delayed the
  bus. Rung 0 then tallies the driver shortage first (2,200) and Brightway third (1,300). Rung 1 never reads codes and still names Atlas
  (2,400), and rung 2 names the driver bonus (2,200). None names Brightway. Incident counts come from the GPS feed and the tow log, and the
  route-coverage log, the takeover dates, the endorsement file and the acknowledgements are complete, so nothing else is suspect. A true
  cause says why last year's buses were late, not how much of each cause recurs next year, so the forward construction is still needed.
* **Lens swap.** The naive moment is the school year just ended. The answer's is next school year, in which Atlas's takeover routes are no
  longer in their first weeks and the driver gap has mostly closed, a different moment and a different population of runs.

## 3. The driving force

A strong solver does not trust the reason codes, because the dispatcher picks them and the form opens on "Heavy traffic". It separates
weather and common shocks from contractor excess. The standard decomposition, with a citywide snow model and the median contractor's
growth, closes exactly on the report card's annual totals and puts Atlas first. The acknowledgement file is sharper. The excess
contractors accepted in 640 past notices is reproduced only against same-zone, same-month peers, with snow from the zone gauges. On that
construction the common shock is the driver shortage: 2,200 excess incidents on runs that a driver doubled back to cover, in the zones and
months with vacancies. The driver bonus leads Atlas, and the file shows plans removing 0.96 of the excess contractors accepted, so last
year's excess reads as next year's. But the excess report's footer says its figures describe the year just ended, and the fix buys next
year. Aligned on each route's own takeover date, Atlas's excess sits in the route's first ten weeks, while its drivers learn the stops,
and then settles to a rate that gives 360 next year. Endorsements have outrun leavers since January, so vacancies, and with them
doubled-back runs, fall to 30% of this year's. Brightway's breakdowns come from a fleet that only gets older: 1,248 next year, 1.89× the
driver bonus.

## 4. The ladder

| Rung | Construction | Names (excess incidents credited to each fix) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The year's increase tallied by reason code, each code mapped to the fix aimed at it | Bus lanes (traffic 2,700, 4.50× snow's 600) | The transportation office's own tally, and "Heavy traffic" tops it in every month | The incident form's guide: the contractor's dispatcher picks the reason, and the form opens on "Heavy traffic" |
| 1 | Snow from a citywide model, common growth at the median contractor's rate, contractor excess beyond both | Atlas plan (2,400, 1.60× the common component's 1,500, read as traffic) | Common shocks separated from contractor excess, closing exactly on the report card's annual totals | The acknowledgement file: this construction reproduces 212 of the 640 accepted figures and misses 31 of the winter log's 45 snow-day cells |
| 2 | Excess against same-zone, same-month peers on own-driver runs, snow from the zone gauges, excess on doubled-back runs to the shortage | Driver bonus (2,200, 1.22× Atlas's 1,800) | All 640 accepted figures and all 45 snow-day cells reproduced, and the file shows plans removing 0.96 of accepted excess the next year | The excess report's footer: "These figures describe the school year just ended. They are not a forecast of the next." |
| 3 | **Decisive:** each cause carried into next school year: Atlas's routes aligned on their own takeover dates, the driver gap projected from endorsements and leavers, snow at a median winter, Brightway's fleet aged a year | **Brightway plan (1,248, 1.89× the driver bonus's 660)**, 4th on rung 0 | — | — |

* **Position table.** The Brightway plan ranks 4th on rung 0 (400) and 3rd on rungs 1 and 2 (1,300), and leads only rung 3. Rung margins are
  4.50, 1.60, 1.22 and 1.89.
* **Discriminator dominance.** The driver bonus carries a 900-incident lead over Brightway into rung 3 (2,200 against 1,300). Carrying each
  cause forward takes 1,540 from the bonus and 52 from Brightway, a 1,488 swing, 1.65× the carried lead. The floor is 1.2×, so the edge has
  1.38× headroom.
* **Partial correction priced (L3).** A solver who aligns Atlas's routes on their takeover dates but carries the driver gap forward names the
  driver bonus at 2,200, 1.76× Brightway. One who projects the driver gap but reads Atlas's excess as chronic names Atlas at 1,800, 1.44×
  Brightway. A back-tester who carries every cause at the file's 0.96 names the driver bonus at 2,112, 1.22× Atlas. No half names Brightway.
* **Grid.** Basis (reason tally, citywide rate, zone-month peers) × forward step (none, the file's 0.96, takeover alignment only, driver
  projection only, both) gives 15 cells. Only zone-month peers with both forward steps name Brightway. The tally names bus lanes in all five
  of its cells and the citywide rate names Atlas or bus lanes. The nearest wrong cell is the citywide rate with both forward steps, which
  names bus lanes at 1,500, 1.20× Brightway.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The fund rule names next school year. No document says Atlas's excess is confined to each route's first weeks or that
   the driver gap is closing, and none connects either to the choice of fix.
2. **Corpus blind for a computable reason.** *In every acknowledged notice the accepted excess held no route's first weeks with a new
   contractor and no doubled-back run, because the contract bars a notice on any route in its first 90 school days with a new contractor
   and every contractor's roster was full throughout those five years.* Plans removed between 0.91 and 1.00 of the accepted excess in 640
   of 640 cases, which certifies rung 2's carrying forward.
3. **No arithmetic symptom.** Incidents, runs, acknowledgements and snow-day cells reconcile on every rung, and the 6,000-incident rise is
   partitioned exactly on rungs 1 and 2.
4. **Not a row predicate.** The forward figure needs each takeover route's incidents ordered on its own takeover date, Atlas's settled rate
   from routes past their tenth week, and a projected roster from endorsements and leavers.
5. **The enumeration is arithmetic.** No field marks an incident as transitional or a vacancy as closing. The ten-week settling is read from
   aligned route histories, and the vacancies from the roster.
6. **No cutover date.** Atlas took over its 60 routes in four tranches between January and April, so the settling runs on 60 clocks, not one
   date, and the driver gap closes month by month.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The contractors' signed acknowledgements of 640 corrective-action notices over five school years. Each accepts a figure of
  excess incidents on the cited routes and period, and the plan-year acknowledgement a year later accepts the incidents the plan removed.
* **What it certifies.** Rung 2's construction: zone-month peers on own-driver runs reproduce all 640 accepted figures, and the citywide rate
  reproduces 212. It also certifies carrying accepted excess forward: plans removed 0.96 of it on average, and never less than 0.91.
* **What it is blind to.** Transitional and closing excess (property 2).
* **Twin pair.** Routes R-114 (Atlas, January tranche) and R-207 (Brightway) are identical on runs (178), incidents (30), zone, reason-code
  mix and excess against zone-month peers (+13 each). Forward, R-207 carries 12.5 and R-114 6.0 (2.1×), because R-114's excess sat in its
  first ten weeks with Atlas. Only the takeover alignment separates them.
* **Resemblance points at the decoy.** Atlas's takeover most resembles the file's 2019 notices to Hartland Bus Lines, which had taken over 40
  routes from a contractor that left the district, and whose plan removed 0.97 of the excess Hartland accepted.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The fund rule: "The board funds the one fix expected to avert the most incidents in the coming school year." The
  contract's notice clause: "No corrective-action notice may cite a route in its first 90 school days with a new contractor." The incident
  form's guide: "The contractor's dispatcher selects the reason for each incident." The excess report's footer, quoted on rung 2.
* **Empirical pins.** Zone-month peers come from the 640 reproductions. Snow comes from the zone gauges through the winter log's cells. The
  ten-week settling comes from aligned route histories, and the driver projection from twelve months of endorsements and leavers.
* **Voices.** Transportation director: "Every dispatcher in the city tells you it's traffic." Contracts manager: "Atlas bid too low to run
  those routes, and it shows." Drivers' union representative: "Nothing gets fixed while drivers run two routes a morning." Brightway's
  general manager: "We have run these routes for twenty years and cured every notice we were given."
* **Licensed wrong basis.** The fund rule records that the board reads contractor performance from the excess report's figures for the year
  just ended and will see the fix on that basis.

## 8. Determinism by construction

* **Credit.** Each fix is credited with the whole of its cause's excess next year, and no fix touches another's cause.
* **Takeover alignment.** Every takeover route has one takeover date in the roster, and no route changes contractor next year. Any settling
  window from 8 to 14 weeks gives Atlas between 330 and 390.
* **Driver projection.** Vacancies averaged 120 this year and project to an average of 36 next year. Any trend window from 6 to 12 months
  gives a persistence between 0.25 and 0.35, so the bonus stays between 550 and 770, under Brightway.
* **Fleet and snow.** The fleet register dates every bus, and four of Brightway's 70 buses reach the contract's 16-year limit and are
  replaced in August. Any persistence from 0.90 to 1.00 keeps Brightway at or above 1,170. Snow uses the median of ten winters, and any of
  the middle six gives under 400.
* **Runs.** Peer rates are incidents per run from the route-coverage log, where a midday run is its own run.
* **Maturity.** Every incident of the year was reconciled to the GPS feed within ten days, and the extract is 30 days after the last school
  day.

## 9. Prompt sketch and deliverables

> The board votes in June on one fix for next year's school buses, after incidents rose 60%. Our contracts manager is convinced Atlas bid
> too low to run its new routes. Tell me which fix we fund, in a sentence the board can vote on, with the incidents a year you credit to each
> of the five fixes, to the nearest 10. Send `bus_fix_case.xlsx`, a chart `incident_causes.png`, and a one-page `board_paper.pdf`.

* `bus_fix_case.xlsx` — the five fixes on every construction, the ride-time sheet (ask A), the invoicing sheet (ask B) and the
  acknowledgement back-test (ask C).
* `incident_causes.png` — a bridge from last year's incidents to this year's by cause, a panel of each cause's excess this year beside next
  year, an inset of the takeover routes' excess by week since their own takeover with the tenth week marked, and a title naming the funded
  fix.
* `board_paper.pdf` — the funded fix and why each other fix averts less.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each contractor and quarter, the share of special-education riders whose ride exceeded the limit
  in their transportation plan. *Device:* the GPS feed times a run from its first pickup, while each plan's limit runs from that student's
  own boarding, which the stop-level boarding scans record. Timing from the first pickup roughly doubles the exceedances on the long
  special-education runs. Ride times never enter incident counts.
* **Ask B (device-carried).** For each contractor, the route-days invoiced last year. *Device:* the rate schedule bills a midday kindergarten
  run as half a route-day, and the invoice file carries one line per run with a run-type code. Counting lines overstates Summit's and
  Ferncliff's route-days by about 12%. The main call never reads invoices.
* **Ask C (validity).** For each of the five past school years, the excess the contractors accepted beside the figure your construction
  gives for the cited routes and periods.
* **Decoupling.** Clearing the forward construction or the zone-month peers changes no figure in asks A or B. Ask C holds no takeover route
  in its first weeks and no doubled-back run, by property 2.

## 11. Rubric arithmetic

5 contractors × 4 quarters (ask A) + 5 contractors (ask B) + 5 years (ask C) + the funded fix, the five fixes' figures and the winning margin
+ 5 named chart parts + 3 files ≈ 45 criteria.

## 12. World-building constraints

* Incidents rise from 10,000 to 16,000 on 1,100 routes run by Atlas, Brightway, Summit, Ferncliff and Tidewater.
* The reason tally of the rise is traffic 2,700, snow 600, driver 500, mechanical 400 and route unfamiliar 300, with 1,500 entered as
  "Other", which maps to no fix.
* Rung 1 splits the 6,000 into Atlas 2,400, common 1,500, Brightway 1,300 and snow 800. Rung 2 splits it into shortage 2,200, Atlas 1,800,
  Brightway 1,300, snow 700 and traffic 0. Next year's figures are Brightway 1,248, shortage 660, Atlas 360, snow 250 and traffic 0.
* Atlas's 60 takeover routes come in four tranches of 15, in January, February, March and April. Each route's excess settles within ten
  weeks to 0.033 a run. Last winter's snowfall was 2.8× the ten-year median.
* The acknowledgement file holds 640 notices, none on a route in its first 90 school days with a new contractor and none in a year with a
  vacancy. Zone-month peers reproduce 640, the citywide rate 212. Plan-year removal averages 0.96.
* R-114 and R-207 are identical on every column the shallow rungs read, with forward figures of 6.0 and 12.5.
* Every grid cell other than the answer names a wrong fix, the nearest at 1.20×.
* Boarding scans and invoices never touch incidents, the route-coverage log or the acknowledgements.
