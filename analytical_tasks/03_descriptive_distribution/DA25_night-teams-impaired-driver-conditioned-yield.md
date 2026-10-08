# DA25 — Which areas get a dedicated night enforcement team, when patrols only ever prevented the crashes impaired drivers cause

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Policy & Education · road-safety enforcement operations |
| Mirrors | Placing intervention capacity on the hours and places where the intervention works rather than where incidents peak (trust-and-safety and fraud-review shifts at Meta, Uber and Amazon, where a reviewer prevents only the abuse they can act on; ride-hail safety features targeted on the trips where they change outcomes) |
| Decision shape | A structure the body adopts: which of eight command areas get a dedicated night enforcement team in 2027, scored on whether the team, patrolling its best three consecutive night hours, would prevent at least 10 fatal or serious collisions a year |
| Committed call | The list of areas that get a night team |
| Gap · Pattern | Gap 3 (objective) over Gap 2 (population) · E05 (Pattern E), the patrol yield conditioned absolutely on whether an impaired driver was involved, a property reached only through the toxicology results, with E20 (collisions reaching an area's team through the segment register's patrolling unit, not the attending force's code) and the wrap-around window below it, pinned by the evaluation's gold-standard subsample |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #25 assumes an effect the log could measure · #13 validates on one population, applies to another · #18 joins only on the visible key · #7 uses the ready-made measure |
| Calibration form | Gold-standard verification subsample: the 2025 independent evaluation of 24 night operations drawn at random from the 60 in the operations log, each with the fatal and serious collisions it prevented, estimated against matched control nights |
| Driving force | A night team prevents collisions by catching and deterring impaired drivers, and nothing else it does moves the count. In all 24 evaluated operations, collisions involving a driver over the alcohol or drug limit fell by 45% to 49% in the patrol window, and every other collision by 0% to 1%. The log's pooled 18% is a true average and applies to no area. Impairment sits only in the toxicology results, joined through each vehicle's driver test, and no column of the collision file predicts it within the night. The areas with the most night collisions are freight corridors and rural trunk roads where few drivers are impaired; the town centres and the resort where most are have fewer collisions, in peaks that cross midnight. |

## 1. Situation

A regional roads-policing collaboration covering eight command areas will fund dedicated night enforcement teams in 2027. The board's
rule gives an area a team when the team, patrolling its best three consecutive hours between 20:00 and 06:00 every night, would prevent
at least 10 fatal or serious collisions a year, judged on the 2021–2025 collisions. The pack holds the collision file (time to the
minute, severity, attending force, road segment, conditions), the vehicle and driver tables, the toxicology results, the road-segment
register with each segment's patrolling unit, the collaboration agreement, the operations log of 60 past night operations with window
collisions before and during each, the 2025 evaluation, and the analyst's patrol-window workbook. The board meets on 3 March 2027.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: collision times and severities, the attending forces, the segment register, the toxicology
  results, the log's counts and the evaluation's estimates. The log's pooled 18% is a true average of what patrols achieved, and nobody's
  reading of their own numbers is overturned. The difficulty is which collisions a patrol can prevent.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the head of roads policing's view and the highways agency's licensed basis. The freight corridors still hold
  the most night collisions, and the log still offers one measured yield to scale them by.
* **Instrument repair.** Clean-data test. No file is suspect. Every fatal and serious collision carries its time to the minute, its
  attending force and its road segment; every driver in one has a toxicology result, breath at the scene or blood at hospital; the
  operations log and the evaluation are complete. The force code records which force attended, a correct field for a different
  attribute from the unit that patrols the segment. Nothing is left to fill, correct or replace: rung 0 adopts Ambleford and Carrowmoor,
  rung 1 adds Brackenridge, and rung 2 adopts Ambleford, Brackenridge, Carrowmoor, Denholm and Easterly. Even with the force code
  rewritten as the patrolling unit, rung 0 would adopt Ambleford, Carrowmoor and Easterly and rung 1 rung 2's five. The answer stays
  Brackenridge, Denholm, Fenmarsh and Gorsley, because conditioning each window's yield on impairment, through the toxicology join, is
  still needed.
* **Lens swap.** The two reads count different populations: every fatal and serious collision in a window, against the impaired-driver
  collisions a patrol can prevent. Ambleford's freight window holds 64 collisions a year and 4 of the second kind.

## 3. The driving force

A strong solver reads the board's rule, fixes the analyst's workbook so that windows may run across midnight, and assigns collisions on
the strategic road network to the unit the segment register names, as the collaboration agreement says. It then scales each area's
best window by the operations log's measured yield, 18% of window collisions, which is exactly the kind of evidence a board wants. That
adopts five areas, the freight corridors first. But the evaluation of 24 operations shows the yield was never 18% anywhere. Joined to
the toxicology results, every operation splits absolutely: collisions with an impaired driver fell by 45% to 49%, and all others by 0%
to 1%, on every road type, night and area. The past operations ran in town centres, where 38% of window collisions involve an impaired
driver, so their pooled yield looks generous. Ambleford's freight corridor has 64 collisions in its best window and 4 with an impaired
driver. Fenmarsh's resort has 40 in a window across midnight and 27. Re-scored, the teams go where impaired drivers are.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The analyst's workbook: best window within a calendar day, collisions by attending force, × the log's pooled 18% | Ambleford, Carrowmoor | The unit's own patrol-window workbook and its measured yield | The board's rule: a night window is any three consecutive hours between 20:00 and 06:00, across midnight |
| 1 | Best window from any start minute, across midnight | Ambleford, Brackenridge, Carrowmoor | The rule's window, searched in full | The collaboration agreement: strategic-network collisions belong to the unit the segment register names, whichever force attended |
| 2 | Collisions assigned through the segment register's patrolling unit (E20) | Ambleford, Brackenridge, Carrowmoor, Denholm, Easterly | The rule's population and window, scaled by the measured yield | The evaluation: the pooled yield reproduces 7 of 24 evaluated operations, and every one equals 47% of its impaired-driver collisions |
| 3 | **Decisive:** prevented collisions = 47% of impaired-driver collisions (toxicology join) and none of the rest, with each area's window chosen on that count (E05) | **Brackenridge, Denholm, Fenmarsh, Gorsley** | — | — |

* **Structure shape.** Each rung adopts a different list, and only rung 3 adds Fenmarsh and Gorsley and drops Ambleford and Carrowmoor.
  Prevented collisions a year at rung 2 and rung 3: Ambleford 11.5 and 6.1, Brackenridge 11.0 and 17.9, Carrowmoor 10.4 and 5.6, Denholm
  10.4 and 11.3, Easterly 11.2 and 5.6, Fenmarsh 7.9 and 12.7, Gorsley 6.5 and 11.3, Hallow Down 5.0 and 5.6.
* **Partial correction priced (L3).** Every half-applied construction adopts a wrong list. Conditioning the yield but keeping each area's
  busiest window drops Fenmarsh, whose busiest window is its 02:30 freight peak (Brackenridge, Denholm, Gorsley). Conditioning on
  attending-force assignment drops Denholm, whose trunk segments carry 5 of its impaired-driver collisions (Brackenridge, Fenmarsh,
  Gorsley). Conditioning within a calendar day adopts Denholm alone. Conditioning on Friday and Saturday nights, the visible stand-in for
  drink-driving, splits nothing in the evaluation and adopts rung 2's five.
* **Grid.** Window (calendar day or across midnight) × assignment (attending force or patrolling unit) × yield (pooled or conditioned)
  gives 8 cells and 8 different lists, from none at all to five areas. Only windows across midnight, the patrolling unit and the
  conditioned yield adopt the four.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The board's rule says "would prevent". The operations log reports each operation's collisions before and during.
   The evaluation reports what each operation prevented. No document says what kind of collision a patrol prevents, and the toxicology
   results are filed for prosecutions, not for evaluation.
2. **Reproduction, and why it is a construction.** The conditioned yield reproduces all 24 evaluated operations within 0.3 collisions.
   The pooled 18% reproduces 7, over-predicting every operation with few impaired drivers and under-predicting every one with many.
   Conditioning on night of the week, road class or light conditions reproduces at most 8. The reproducing quantity needs every window
   collision's drivers joined to their toxicology results. No collision column carries it, and no threshold or setting reaches it.
3. **No arithmetic symptom.** Every collision, driver and test reconciles, the log's before and during counts tie to the collision file,
   and the pooled yield is the exact ratio of the log's totals.
4. **Not a row predicate.** A collision's prevention weight comes from its drivers' test results through the vehicle and driver tables,
   and an area's count is the best window's sum of those weights, a search over start minutes.
5. **The enumeration is arithmetic.** 2,140 fatal and serious night collisions a year, 690 of them with an impaired driver, are sorted by
   the join and summed over sliding windows.
6. **No cutover date.** Operations ran in every year of the log, the drink-drive limits have not changed, and no series steps.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, the measured 18% is still the only yield the log prints.

## 6. The calibration corpus

* **Form.** The 2025 evaluation: 24 operations drawn at random from the 60 in the log, each with the fatal and serious collisions it
  prevented, estimated against matched control nights in comparable areas.
* **What it certifies and pins.** The conditioned yield (above). It also confirms the window arithmetic: each evaluated operation's
  window collisions, counted from its start minute and across midnight where the window ran, tie to the log.
* **Twin pair.** Operations 2023-14 and 2024-03 are identical on every column of the log and the collision file: town-centre windows of
  22:30 to 01:30, 17 fatal and serious collisions in the window the year before, the same road mix, nights and light conditions. The
  evaluation found they prevented 3.8 and 1.9 collisions (2.0×), because 8 of the first window's collisions involved an impaired driver
  and 4 of the second's. Every pooled construction predicts 3.1 for both.
* **Resemblance points at the decoy.** By collision volume and road mix, Ambleford's freight window most resembles the evaluation's two
  largest operations, which prevented the most because 60% of their window collisions involved an impaired driver.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The board's rule: "An area receives a night enforcement team when the team, patrolling its best three consecutive hours
  between 20:00 and 06:00 every night, would prevent at least 10 fatal or serious collisions a year, judged on the 2021–2025 collisions."
  The collaboration agreement: "Collisions on the strategic road network are the responsibility of the unit that the segment register
  names for the segment." The toxicology guide: a driver is impaired when any result exceeds a legal limit for alcohol or a specified drug.
* **Empirical pins.** The yield split and its rates, from the evaluation.
* **Voices.** The head of roads policing: "The freight corridors are where the night crashes cluster. That's where a team earns its
  keep." The road-safety partnership's analyst: "The operations log already measured what a patrol is worth."
* **Licensed wrong basis.** The board's rule records that the highways agency allocates its own traffic officers by collisions per
  kilometre of network and will compare the board's list with its own.

## 8. Determinism by construction

* **Yield.** Any rate from 45% to 49% on impaired-driver collisions, and from 0% to 1% on the rest, leaves every area at least 0.8
  collisions above or 3.3 below the line, and moves no area's best window.
* **Windows.** Every area's best window under each construction leads the next-best start by at least one collision a year, and no
  window's count depends on whether its end minute is open or closed.
* **Impairment.** Every driver in every fatal or serious collision has a toxicology result, and the guide's limits decide every one;
  a collision counts as impaired when any of its drivers is.
* **Assignment.** Each segment has one patrolling unit. Off the strategic network, the attending force is the patrolling unit.

## 9. Prompt sketch and deliverables

> Which of our eight areas should get a dedicated night enforcement team next year? The board meets on 3 March, and our head of roads
> policing reckons the freight corridors are where the night crashes cluster. Give me the list of areas, as the board would minute it,
> and send `night_teams.xlsx` with the sheets below and a chart `night_windows.png`.

* `night_teams.xlsx` — each area's best window and prevented collisions under each rung's construction (ask C), the camera sheet (ask A)
  and the response sheet (ask B).
* `night_windows.png` — for each area, a 24-hour clock of fatal and serious collisions with the impaired-driver collisions shaded, the
  chosen window marked, the prevented count against the 10-collision line, and the twin operations annotated.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** Speed-camera offences by area and quarter of 2026. *Device:* an offence notice reissued after a
  keeper nominates another driver keeps the original row with status "reissued" and adds a new row under the same incident number, as
  the camera-enforcement guide documents. Counting rows overstates 19 of the 32 cells.
* **Ask B (device-carried).** Median emergency response time to road traffic incidents by area and quarter of 2026. *Device:* an incident
  upgraded to emergency after dispatch carries the emergency clock from the upgrade, recorded as a second grading row, as the
  call-handling standard documents. Timing from the first grading overstates 14 of the 32 cells.
* **Ask C (validity).** Each area's best window and prevented collisions under the four rung constructions, the evaluation's
  reproduction counts for the pooled and conditioned yields, and the twin operations' evaluated and predicted prevented collisions.
* **Decoupling.** Camera and call-handling records share no row with the collision file, the toxicology results or the operations log.
  Clearing the impairment conditioning changes no figure in asks A or B.

## 11. Rubric arithmetic

8 areas × 4 quarters (ask A) + 8 areas × 4 quarters (ask B) + 8 areas × 4 constructions, 2 reproduction counts and 4 twin figures (ask C)
+ 8 area decisions + 4 named chart parts + 2 files ≈ 116 criteria.

## 12. World-building constraints

* Best windows and fatal or serious collisions a year (all, impaired; attending force / patrolling unit where they differ): Ambleford
  03:00–06:00 78/5, 64/4 and 23:00–02:00 41/14, 38/13; Brackenridge 21:00–24:00 44/20 and 23:00–02:00 61/38; Carrowmoor 01:00–04:00 58/9
  and 22:30–01:30 39/12; Denholm 22:00–01:00 52/19, 58/24 and 21:00–24:00 47/17, 52/22; Easterly 02:00–05:00 50/4, 62/5 and 22:00–01:00
  30/12, 31/12; Fenmarsh 23:30–02:30 40/27, 02:30–05:30 44/6 and 21:00–24:00 30/17; Gorsley 22:30–01:30 36/24 and 21:00–24:00 31/19;
  Hallow Down 22:00–01:00 28/12 and 21:00–24:00 25/10.
* Lists by rung: Ambleford, Carrowmoor / + Brackenridge / Ambleford, Brackenridge, Carrowmoor, Denholm, Easterly / Brackenridge, Denholm,
  Fenmarsh, Gorsley. Grid cells: Ambleford, Carrowmoor, Easterly (calendar day, patrolling unit, pooled); none (calendar day, attending
  force, conditioned); Brackenridge, Fenmarsh, Gorsley (across midnight, attending force, conditioned); Denholm (calendar day, patrolling
  unit, conditioned).
* Operations log: 60 operations, 38% of window collisions with an impaired driver, pooled yield 18%. Evaluation: 24 operations, the
  conditioned yield 24/24 within 0.3, pooled 7/24.
* Region-wide, 2,140 fatal and serious night collisions a year, 690 of them with an impaired driver. Impairment is uncorrelated with road
  class, night of the week and light conditions within the night hours.
* Operations 2023-14 and 2024-03 are identical on every log and collision column; 8 and 4 of their 17 window collisions involved an
  impaired driver.
* Camera and call-handling records touch no collision, driver or operation row.
