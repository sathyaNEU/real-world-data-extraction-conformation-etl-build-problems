# RC10 — How much heat rate the compressor wash will win back over next year's dispatch, filed before the five-day outage is approved

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Economics · power plant operations and fuel cost |
| Mirrors | Maintenance timing against an efficiency KPI (data-centre PUE before a chiller clean, GPU fleet throughput before a firmware refresh, airline fuel burn before an engine wash), where the maintenance log already holds natural experiments of the intervention |
| Decision shape | One figure committed at a date (a component): the wash-recoverable heat rate, filed at the outage review on the 14th |
| Committed call | The reduction in the plant's heat rate over next year's dispatch plan that an offline compressor wash delivers, in Btu/kWh to the nearest whole unit |
| Gap · Pattern | Gap 4 (rule) over Gap 1 (time) · E26 (change-log natural experiments: eight logged washes measured against the twin turbine), with E07 (two grains, the annual mean and the hour) at rung 1 |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #25 assumes an effect the log could measure · #7 uses the ready-made measure · #13 validates on one population, applies to another |
| Calibration form | Parallel-run overlap: for each of the eight logged washes, the four weeks in which the two gas turbines ran side by side under identical dispatch, one washed and one not |
| Driving force | Fouling builds with the air a compressor swallows, not with the hours it fires or the months since its last wash. Two-shifting and overnight minimum load have kept the fired hours high and cut the air throughput. The OEM's rule of thumb, the calendar and the residual of the heat-rate bridge all overstate what a wash recovers. Only the eight logged washes, each read against its twin turbine, show the air-mass law, and its recovery has to be carried across next year's load profile hour by hour. |

## 1. Situation

A two-on-one combined-cycle plant's heat rate rose 3.5% year on year, from 7,000 to 7,245 Btu/kWh. The plant engineer wants a five-day offline outage
next month to wash both compressors and borescope the hot gas path. The commercial team says the plant is simply being two-shifted (off at midday
when solar floods the market, back for the evening ramp) and parked at minimum load overnight. The commercial policy approves an outage of this length
only if the wash recovers at least 100 Btu/kWh over the plant's next twelve months of planned dispatch. The maintenance log records every past wash.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the hourly operating data, the heat-rate bridge, the OEM manual, the maintenance log and the twin-turbine
  records. The engineer is right that the compressors have fouled, and the commercial team is right about two-shifting. Nothing is overturned;
  the figure is the size of the component the engineer names.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the licensed basis. The bridge's residual and the OEM's fired-hours rule still put the recovery
  above the approval line.
* **Instrument repair.** None suspect: the hourly fuel, power, airflow and ambient records are complete and continuous, the maintenance log
  holds every wash, the twin's records cover every overlap, and the OEM manual states its own rule correctly. Perfect metering leaves rung 0 at
  196, rung 1 at 128 and rung 2 at 112; none returns 92. A perfect bridge still cannot split its residual between fouling and hot-gas-path wear,
  and what a wash will win back next year is measurable only from past washes against the twin, carried across next year's dispatch.
* **Lens swap.** The residual describes how the plant degraded over the last year; the answer is what one intervention will change over the
  next year's dispatch: a different quantity over a different window.

## 3. The driving force

A strong solver builds the bridge hour by hour, because the curve is convex and two-shifting has piled hours at minimum load, and gets a
residual of 128 Btu/kWh after starts, load profile and ambient. It does not stop at "residual equals fouling": a residual also holds hot-gas-path
wear that no wash recovers. It reaches for the OEM manual's rule (1.5% per 8,000 fired hours since the last wash) and gets 112. Both are assumed
effects, and the maintenance log can measure the real one. Eight offline washes over four years, alternating between the two turbines, were each
followed by weeks in which both units ran side by side at the same dispatch; the washed unit's gain over its twin is a clean read of the wash.
Those eight reads scatter against fired hours, starts or months, and fall on one line against the compressor air mass ingested since the previous
wash (8 of 8 within 4%). Air mass comes from summing each hour's airflow, which closes at low load, so two-shifting has fouled the compressors
far less per fired hour than the manual assumes. The law gives a recovery in heat rate at each load; carried across next year's dispatch plan
hour by hour, it is 92 Btu/kWh, below the approval line.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Heat-rate bridge with the reference curve evaluated at each year's mean load; the residual is what the wash recovers | 196 Btu/kWh (+113%) | The engineer's own logic, with starts and ambient taken out | The hourly records: the load distribution turned bimodal, and a convex curve evaluated at the mean misses most of the part-load penalty |
| 1 | The bridge evaluated hour by hour on each year's own load and temperature; the residual is what the wash recovers | 128 (+39%) | Jensen's inequality handled, the bridge closes exactly | The bridge cannot split the residual between fouling a wash removes and hot-gas-path wear it does not |
| 2 | The OEM manual's rule (1.5% per 8,000 fired hours since the last wash) carried hour by hour over next year's dispatch plan | 112 (+22%) | A documented recovery rule, applied to the right horizon | The parallel-run reads of the eight logged washes: fired hours explain them poorly (3 of 8 within 10%) |
| 3 | **Decisive:** recovery per unit of compressor air mass, fitted on the eight twin-differenced washes, applied to the air mass ingested since the last wash and carried over the dispatch plan hour by hour | **92 Btu/kWh** | — | — |

* **Figure shape.** Every correction walks the figure down (196, 128, 112, 92), and the answer is the minimum of every cell in the grid, so
  every partial application approves the outage.
* **Partial correction priced (L3).** A solver who fits the air-mass law on plain before-and-after reads of each wash, rather than against the
  twin, absorbs the spring warm-up that followed six of the eight washes and lands at 121 (+31.5%), further than rung 2. Carrying the right law
  across next year at the plan's mean load instead of hour by hour lands at 103 (+12%), still above the approval line.
* **Grid.** Recovery basis (bridge residual at mean or hourly, calendar months, starts, fired hours, air mass from before-and-after reads, air
  mass from twin reads) × carry-over (mean load, hourly) gives twelve cells from 92 to 196. The nearest wrong cell is the right law at mean load
  (+12.0%), and every cell above 100 approves the outage the answer refuses.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The OEM manual states the fired-hours rule; the maintenance log lists washes with dates and before-and-after heat
   rates. No document mentions air mass, twin reads or a recovery law.
2. **The corpus pins a construction, not a menu.** The air-mass law reproduces 8 of 8 twin-differenced recoveries within 4%; the best rival
   (starts) 4 of 8, fired hours 3, calendar months 1. Each rival overstates the recovery of every wash that followed a two-shifting interval, so
   none reconciles on the eight-wash total. Air mass is a sum over every hour since each wash of the airflow at that hour's load, built from the
   hourly records and the compressor map, with no parameter to scan.
3. **No arithmetic symptom.** The bridge closes to the cent under every rung; the log's before-and-after figures are correct as recorded.
4. **Not a row predicate.** Exposure is an integral over thousands of hours between two log dates, and each wash's effect is a difference
   between two units over matched weeks.
5. **The enumeration is arithmetic.** The recovery is a fitted slope times a constructed exposure, carried over a planned load profile.
6. **No cutover date.** Fouling accrues continuously; the dated events (the switch to two-shifting in March, the last wash in February of last
   year) step no series the answer depends on.
7. **Survives deletion.** With every voice removed, the OEM rule still approves the outage.

## 6. The calibration corpus

* **Form.** The parallel-run overlaps: for each of the eight logged offline washes, two weeks before and two weeks after in which both gas
  turbines ran at identical dispatch, with each unit's hourly corrected heat rate; the washed unit's change relative to its twin is the wash's
  read.
* **What it pins.** The recovery law (above), and the twin read over the before-and-after read, which the spring warm-up biases upward in six
  of eight washes.
* **Twin pair.** Washes W3 and W6 followed intervals identical in fired hours (5,200), calendar months (11) and starts (310), in the same
  season. They recovered 58 and 27 Btu/kWh (2.15×): W3's interval was baseload and W6's two-shifted. Only air mass reproduces both.
* **Resemblance points at the decoy.** The current interval matches W5 on fired hours and months since the last wash, and W5, a baseload
  interval, recovered the most of any wash.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The commercial policy: an outage of five days or more is approved only if the work recovers at least 100 Btu/kWh over the
  next twelve months of planned dispatch. The dispatch plan for those twelve months, hour by hour.
* **Empirical pins.** The recovery law and its twin-read basis, from the overlaps; recovery by load from the twin reads at each load band.
* **Voices.** The plant engineer: "Three and a half per cent is fouling; I've seen it on every unit I've run." The commercial manager: "We're
  two-shifting harder than ever; the curve does the rest."
* **Licensed wrong basis.** The policy records that the OEM's service team sizes wash benefits on its fired-hours rule and will present that
  figure at the review.

## 8. Determinism by construction

* **Air mass.** Hourly airflow comes from the compressor map at each hour's load and inlet temperature; the map is filed and single-valued.
* **Twin read.** Each overlap has 14 days either side with no start on either unit and identical dispatch; the read is the mean difference.
* **Carry-over.** Recovery by load band (five bands) applied to the plan's hours; the plan has no hour on a band edge.
* **Hot-gas-path wear.** Out of the figure by definition of the wash; no rung's figure depends on how the residual's remainder is labelled.
* **Rounding.** Whole Btu/kWh; the answer sits mid-bin and 8% below the approval line.

## 9. Prompt sketch and deliverables

> Engineering wants five days offline next month to wash both compressors, on the strength of a 3.5% heat-rate rise, and commercial says we're
> just two-shifting harder. I need the number of Btu/kWh the wash will take off our heat rate over next year's dispatch, to the nearest whole
> unit, as the line I file at the outage review on the 14th. Send `wash_case.xlsx` and a chart `wash_recovery_law.png`.

* `wash_case.xlsx` — the four constructions, the generation sheet (ask A), the starts sheet (ask B) and the wash reproduction (ask C).
* `wash_recovery_law.png` — the eight twin-read recoveries plotted against air mass and, in a second panel, against fired hours, each with its
  fitted line; the current interval marked on both; and the 100 Btu/kWh approval line with the committed figure labelled.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the last twelve months, gross generation, net export and auxiliary consumption. *Device:*
  auxiliary load while the plant is offline or starting is imported through a separate import meter, as the metering schedule documents;
  netting only the unit meters understates auxiliary consumption most in the two-shifting months.
* **Ask B (device-carried).** For each month, starts by type (hot, warm, cold). *Device:* the operations log files a start that trips before
  synchronising as an attempt with a failed-start flag and the OEM classifies starts by hours offline; counting attempts as starts and ignoring
  the offline hours misclassifies a quarter of the warm starts.
* **Ask C (validity).** For each of the eight washes, the twin-read recovery and the recovery each of the four laws predicts; and the figure
  under each of the four rung constructions.
* **Decoupling.** Clearing the air-mass law changes no figure in asks A or B; neither feeds the recovery or the carry-over.

## 11. Rubric arithmetic

12 months × 3 figures (ask A) + 12 months × 3 start types (ask B) + 8 washes × 5 figures + 4 constructions (ask C) + the committed figure,
its distance from the approval line and the air mass since the last wash + 5 named chart parts + 2 files ≈ 125 criteria.

## 12. World-building constraints

* Heat rate 7,000 to 7,245 Btu/kWh; bridge residual 196 at mean load, 128 hourly.
* Since the last wash: 7,400 fired hours, 14 months, air mass about 62% of what the same fired hours at baseload would ingest.
* Recovery predictions, hourly carry-over: air mass (twin) 92, starts 104.5, fired hours 112, air mass (before-and-after) 121, calendar 139;
  mean-load carry-over adds 12% to each.
* W3 and W6 identical on fired hours, months, starts and season; twin reads 58 and 27.
* Import-meter auxiliary load and failed-start attempts touch no hour used in the air-mass sum or the carry-over.
