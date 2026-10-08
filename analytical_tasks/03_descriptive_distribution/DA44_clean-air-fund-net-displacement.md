# DA44 — Which six clean-air measures a city funds, when each traffic zone it closes pushes nitrogen dioxide onto its boundary

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Policy & Education · urban air-quality programmes |
| Mirrors | Allocating a capped set of interventions whose local effect pushes the problem next door (fraud rules that move attacks to unprotected flows, moderation that shifts abuse to adjacent surfaces, traffic and load management that reroutes demand), so only net effects across every unit decide |
| Decision shape | An allocation under a cap: six measures chosen from nine candidates (three zone restrictions, six bus-corridor retrofits) |
| Committed call | The six measures funded, and the number of monitoring stations they bring to certain compliance with the annual limit |
| Gap · Pattern | Gap 3 (objective) over Gap 2 (population) · the deciding comparison (measured #20): net change across all stations, not each measure's local effect, with the station segment kept fine at rung 1 (measured #14) |
| Gate G mechanism | decomposition_attribution, with binding_constraint |
| Measured traps engaged | #20 leaves the deciding comparison unstated · #14 coarsens the segment it was asked about · #16 lets small shortcuts flip a thin margin |
| Calibration form | Prior-period close-out: last year's clean-air fund close-out, with each delivered measure's measured annual change at every one of the 12 stations |
| Driving force | A zone restriction lowers the stations inside it by about 6 µg/m³ and raises the stations on its boundary roads by 2.4, as all three restrictions in last year's close-out show. Read one measure at a time, restrictions look strongest. Summed across stations, two of the three push boundary stations that sit just under the limit back over it, and the set that clears most stations funds one restriction and five retrofits. |

## 1. Situation

A city's clean-air fund can deliver six measures this year, and its rules score the allocation on the number of the 12 monitoring stations
whose annual mean nitrogen dioxide is certainly below 40 µg/m³, the upper end of the station's interval. Nine candidates are costed:
three traffic-zone restrictions and six bus-corridor retrofits. The pack holds a year of hourly concentrations by station, the city's
annual report with zone averages, the compliance memo with the interval method, the candidate measures with the stations each touches,
and last year's close-out.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each hourly reading, each zone average, each measured change in the close-out. Nobody ranks the
  measures and nothing reported is overturned. The difficulty is summing effects that point in opposite directions at different stations.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the transport lead's view and the councillors' basis. Robust station intervals with each measure's local
  effect still fund all three restrictions and clear five stations.
* **Instrument repair.** Measure every street perfectly: the boundary increase is a real effect of moving traffic, already measured. What
  the decision needs is the net across stations, which no better monitor reports.
* **Lens swap.** The naive allocation credits each measure with its own stations; the answer credits it with every station it changes,
  including those it makes worse. Different stations enter each measure's count.

## 3. The driving force

A strong solver computes each station's annual mean with an interval robust to autocorrelation, as the compliance memo requires, and
prices each candidate by the stations it brings below the line. Zone restrictions cut their own stations by about 6 µg/m³ against about 3
for a retrofit, so the solver funds all three and three retrofits. Last year's close-out shows what else a restriction does. Traffic
displaced from a closed zone runs along its boundary roads, and every boundary station rose by 2.0 to 2.8 in the year its neighbour
closed. Four stations sit on restriction boundaries at upper bounds between 38.6 and 39.4. Funding all three restrictions pushes three of
them over. The deciding comparison is each set's net change at every station, and it funds Z2 and five retrofits, which clear eight
stations against five.

## 4. The ladder

| Rung | Construction | Funds | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Station means with hourly standard errors, each measure's local effect | Z1, Z2, Z3, B1, B2, B4; claims 9, clears 4 | Every hour counted, every measure priced | The compliance memo: intervals rest on daily means and their autocorrelation |
| 1 | The annual report's zone averages, robust intervals at zone grain | Z1, Z3, B2, B4, B5, B6; clears 3 | The city's published geography | The limit applies to each station, and three zones mix compliant and failing stations |
| 2 | Robust station intervals, each measure's local effect | Z1, Z2, Z3, B1, B3, B5; clears 5 | Right grain, right interval, every measure costed | The close-out: every restriction raised its boundary stations by 2.0 to 2.8 |
| 3 | **Decisive:** robust station intervals, net change of each candidate set at every station | **Z2, B1, B2, B3, B5, B6; clears 8** | — | — |

* **Allocation shape.** No intermediate rung funds the answer's set, and the answer clears the most stations of the 84 possible sets; the
  runner-up set clears 7.
* **Partial correction priced (L3).** A solver who nets displacement but keeps hourly standard errors funds Z2, B1, B2, B3, B4 and B6 and
  clears 6. One who nets displacement on zone averages funds Z2, B1, B2, B4, B5 and B6 and clears 6. Neither lands on the answer's set.
* **Grid.** Interval (hourly or robust) × grain (zone or station) × effects (local or net) = 8 cells, each funding a different set; the
  nearest wrong cells clear 6 stations.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The candidate sheet lists each measure's stations and expected local reduction. The close-out reports changes by
   station without attributing them, and no document mentions displacement.
2. **Pattern B, an effect the close-out pins.** Netting a 2.4 rise on boundary stations reproduces all 36 station changes of last year's
   five measures within 0.3; local effects alone miss the 9 boundary changes by 2.0 or more, all upward. The comparison is a construction:
   each candidate set's effects summed over every station, then each station's interval re-read against the limit.
3. **No arithmetic symptom.** Daily means tie to hours, zone averages tie to stations, and each measure's local effect matches the
   candidate sheet.
4. **Not a row predicate.** Whether a station clears depends on the sum of effects from several measures, some of them positive.
5. **The enumeration is arithmetic.** No column gives a station's net change under a set.
6. **No cutover date.** The close-out year's hourly data is not shipped; only annual changes are, so there is no series to align.
7. **Survives deletion.** With every voice removed, local effects still fund all three restrictions.

## 6. The calibration corpus

* **Form.** Last year's close-out: five measures delivered (three restrictions in other districts, two retrofits), with every station's
  measured change in annual mean.
* **What it certifies.** Each measure type's local effect (restrictions −6.1 ± 0.4, retrofits −3.0 ± 0.3), which a back-tester confirms.
* **What it pins.** Boundary displacement: +2.0 to +2.8 at all nine boundary stations.
* **Twin pair.** Stations S-04 and S-09 match on class, zone, last year's mean (42.1), distance to the treated corridor and traffic flow.
  Their measured changes were −4.0 and −2.0 (2.0×): S-09 sits on a restriction boundary and gained 2.0 from displaced traffic.
* **Resemblance points at the decoy.** On every candidate-sheet column, Z1 and Z3 resemble last year's most effective restriction.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The fund rules: six measures, scored on stations whose upper interval bound is at or below 40 µg/m³. The compliance memo:
  intervals from daily means with an effective sample size from their lag-1 autocorrelation.
* **Empirical pins.** Local and boundary effects, from the close-out.
* **Voices.** The transport lead: "Zone restrictions are the strongest tool we have; fund all three." The monitoring officer: "The
  report's zone averages are what the public sees."
* **Licensed wrong basis.** The fund rules record that the environment committee's councillors rank measures by the reduction at their own
  stations and will review the allocation on that basis.

## 8. Determinism by construction

* **Intervals.** Every station has at least 350 valid days, and no upper bound after any candidate set lies within 0.2 µg/m³ of 40.
* **Effects.** Boundary stations are listed for each restriction; no station borders two restrictions.
* **Search.** The 84 possible sets give a unique best (8 stations) and a runner-up at 7.
* **Base.** Next year is scored on this year's means plus measured effects, as the fund rules say.

## 9. Prompt sketch and deliverables

> The fund's six measures are fixed at the committee on the 4th, and the transport lead wants all three zone restrictions in. Tell me
> which six we fund and how many stations they bring certainly under the limit, with each station's net change under the set we fund, as
> the committee's decision table. Send `measure_selection.xlsx`, a chart `station_net_change.png`, and a one-page `selection_note.pdf`.

* `measure_selection.xlsx` — every candidate set's station outcomes, the hours sheet (ask A), the source sheet (ask B) and the rung table
  (ask C).
* `station_net_change.png` — each station's upper bound before and after the funded set as paired dots, the 40 µg/m³ line, boundary
  stations marked with their displacement, and the stations each rival set would clear listed in the margin.
* `selection_note.pdf` — the committed set, the stations it clears, and why the restriction-heavy sets clear fewer.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each station, the hours above 200 µg/m³ last year. *Device:* readings flagged as provisional
  were later ratified with corrections, and the ratification file supersedes them; counting provisional hours overstates five stations.
* **Ask B (device-carried).** For each station, the share of its annual mean from road traffic in the source-apportionment model.
  *Device:* the model reports shares for the model year's network, and the network change log reassigns two closed roads; reading the
  stale road codes misattributes three stations.
* **Ask C (validity).** Stations cleared by each of the four rung allocations, and each station's net change under the funded set.
* **Decoupling.** Clearing the displacement netting changes no figure in asks A or B.

## 11. Rubric arithmetic

12 stations (ask A) + 12 stations (ask B) + 4 allocations and 12 net changes (ask C) + the six funded measures and the stations cleared +
5 named chart parts + 3 files ≈ 54 criteria.

## 12. World-building constraints

* Station upper bounds today run 37.8 to 46.2; four boundary stations sit between 38.6 and 39.4.
* Effects: restrictions −6.1 inside and +2.4 on boundaries; retrofits −3.0 on their corridor.
* Stations cleared: 4 / 3 / 5 / 8; partial cells 6 and 6; runner-up set 7. S-04 and S-09 match on every visible column.
* Provisional flags and road codes never touch a daily mean or an effect.
