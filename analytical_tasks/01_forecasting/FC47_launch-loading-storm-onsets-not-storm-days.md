# FC47 — How many satellites to load on each of 2027's six launches, when the storm loss the limit counts falls once per storm and the files count storm days

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Supply Chain & Logistics · satellite launch and constellation deployment |
| Mirrors | Loading scarce launch or delivery capacity against an event risk counted in the wrong unit (constellation deployment after the February 2022 storm losses, catastrophe cover priced per event rather than per day, cloud failover sized on incidents rather than incident-hours) |
| Decision shape | An allocation under a cap: up to 60 satellites on each of six booked launches, the rest held for 2028 |
| Committed call | Satellites to load on each of the February, April, June, August, October and December launches, and how many of the 360 wait for 2028 |
| Gap · Pattern | Gap 3 (objective) over Gap 1 (time) · S1 (the unit the loss is counted in, a storm, is not the unit the pack records), with the population a flag suggests (measured #5) at rung 2 |
| Gate G mechanism | forecasting, with method_or_model_selection |
| Measured traps engaged | #2 counts file rows instead of the real unit · #5 takes the population a flag or filter suggests · #7 uses the ready-made measure |
| Calibration form | Retry and revision log: the orbit-raising log for 40 past batches, every planned burn, every stand-down, hold and retry, the day each satellite crossed 350 km, and every loss |
| Driving force | A satellite below 350 km is lost at a storm's onset, before the stand-down that follows can protect it: the revision log shows 33–37% of the low satellites lost at every onset, whether the storm then ran one day or four. A storm is a run of storm days, a unit no file stores; the Kp files hold three-hour values and a daily storm-day table. In 2027, the declining phase of cycle 25, storms are long recurrent ones, 2.2–3.1 storm days each, so counting days counts every storm two or three times and halves every launch's load. |

## 1. Situation

A broadband satellite operator has 360 satellites ready for 2027 and six rideshare launches booked, each dispenser carrying at most 60.
Satellites are released at 210 km and raise themselves to their shell; until they pass 350 km a geomagnetic storm's drag can bring them
down. The mission assurance memo lets a launch carry only as many satellites as keep its expected storm loss at two or fewer; anything
that cannot fly in 2027 waits for 2028. The pack holds GFZ's three-hour Kp record since 1932 with its daily storm-day table, SILSO's
smoothed sunspot series, the fleet register, the orbit table, the orbit-raising revision log and the risk desk's climatology sheet. The
loading plan goes to the launch provider on 1 December.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the Kp values, the storm-day table, the sunspot series, the register, the orbit table and the log.
  No stakeholder's reading of their own numbers is overturned; storm days really are what the risk desk has always counted. The difficulty
  is the unit the loss falls in, which no file stores.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the mission assurance lead's view and every voice. The daily storm-day table is still the natural input, and
  any loss rate applied to it still halves the April and October loads.
* **Instrument repair.** Imagine a perfect space-weather record. Storms would be measured exactly, but 2027's storms have not happened;
  how many onsets each launch's exposure will meet is still a forecast built from storms grouped out of the record.
* **Lens swap.** The naive read and the answer count different populations: storm days, two to three to a storm in the declining phase,
  against storm onsets, one to a storm.

## 3. The driving force

A strong solver forecasts the storm days each launch's exposure will meet from the Kp history aligned by months since the cycle's smoothed
maximum, because 2027 sits in cycle 25's declining phase, where storms run 1.4 to 2.2 times the all-years rate. It takes the exposure from
the orbit table rather than the fleet register's raising flag, because a campaign paused by a stand-down or a conjunction hold was closed
on plan while its satellites were still low. It applies the log's 35% loss per storm to each storm day and loads 165 satellites. Every
step is correct. But the log never shows a loss on a storm's second or third day: every loss falls at an onset, when drag rises before the
stand-down protects the satellites, and 33–37% of the low satellites go whatever the storm's length. A storm is a run of storm days, and
in the declining phase the recurrent storms run 2.2 to 3.1 days. Counting onsets, four launches fill to 60, April carries 52 and October
49, and 19 satellites wait for 2028.

## 4. The ladder

| Rung | Construction | Lands on (Feb / Apr / Jun / Aug / Oct / Dec; deferred) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The risk desk's climatology: all-years storm days per window over the register's 9-day raising period, 35% lost per storm day | 47 each; 78 | The desk's own sheet and the loss rate the log records | SILSO's series: 2027 sits 28–38 months after cycle 25's smoothed maximum, and at that phase the Kp record holds 1.4–2.2 times the all-years storm days |
| 1 | Storm days from windows aligned by months since each cycle's maximum (cycles 17–24) | 38 / 23 / 52 / 42 / 21 / 44; 140 | Phase-aligned analogs, the standard space-weather forecast | The orbit table: satellites stayed below 350 km for 12 days on average, while the register's raising flag closes on the planned day 9 even for paused campaigns |
| 2 | Exposure from the orbit table, 12 days | 29 / 17 / 39 / 31 / 16 / 33; 195 | Right phase, right exposure, every count reconciled | The revision log: every loss fell at a storm's onset, 33–37% of the satellites then low, whether the storm ran one day or four |
| 3 | **Decisive:** storms built as runs of storm days from the three-hour Kp, onsets per 12-day window from the phase analogs, 35% lost per onset | **60 / 52 / 60 / 60 / 49 / 60; 19** | — | — |

* **Figure shape.** Rungs 0 to 2 walk the loads down (deferred 78, 140, 195) and the decisive rung reverses past rung 0: April and October
  carry 52 and 49, the other four fill to 60, and 19 wait.
* **Partial correction priced (L3).** A solver who sees that losses track storms but calibrates a per-day rate on the log's totals (35%
  divided by the log's 2.6 days a storm) loads April 45 and October 42 and defers 33 (April −13%, October −14%). One who counts onsets but
  keeps the climatology, or keeps the register's 9-day exposure, fills every launch to 60 and defers none (April +15%, October +22%).
* **Grid.** Alignment (all-years, phase) × exposure (9-day flag, 12-day orbit table) × unit (storm days, onsets) = 8 cells. The four
  storm-day cells defer 78 to 195; the three onset cells without both corrections fill every launch and defer none. Only the full
  construction loads April 52 and October 49; every other cell is at least 8 satellites (15%) away on one of them.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The memo caps expected storm loss; the log lists losses by date. No document says losses fall at onsets, defines a
   storm as a run of days, or says how long a run is.
2. **Reproduction (Pattern B).** Losses of 35% at each onset reproduce all 40 batches' losses to the satellite; 35% per storm day reproduces
   34, missing every batch met by a multi-day storm, all high; a per-day rate fitted to the log's total reproduces 31. The rule is a
   construction, not a menu: three-hour values become storm days, storm days become runs, and runs are joined to each satellite's days below
   350 km.
3. **No arithmetic symptom.** Storm days reconcile to the three-hour values, exposure to the orbit table, losses to the register; every
   rung's loads respect the dispenser cap.
4. **Not a row predicate.** A storm is a run across days; whether a day starts one depends on the day before, so onsets need an ordered
   pass over the record before any window is counted.
5. **The enumeration is arithmetic.** No column marks an onset; the daily table marks storm days only.
6. **No cutover date.** No outcome series steps; the declining phase lengthens storms gradually as recurrent streams take over.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The orbit-raising revision log for 40 batches since 2020: every planned and revised burn, every stand-down, conjunction hold and
  retry, each satellite's crossing of 350 km, and each loss with its date.
* **What it certifies.** The phase-aligned storm counts (the storm days the past batches met follow the analogs) and the 12-day exposure.
* **What it pins.** The loss unit and rate: every loss on an onset day, 33–37% of the satellites then below 350 km, none on a storm's later
  days.
* **Twin pair.** Batches 2023-07 and 2024-11 each carried 50 satellites, met three storm days inside their exposure and match on every
  register column. They lost 17 and 36 (2.1× apart), because 2023-07's three days were one storm and 2024-11's were three one-day storms.
  Storm-day counts predict them equal; only onsets reproduce both.
* **Resemblance points at the decoy.** By storm days per window, 2027's launch months most resemble the past batches that lost satellites,
  so the day-based limits look prudent.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The mission assurance memo: a launch carries no more satellites than keep its expected storm loss at two or fewer;
  exposure runs while a satellite is below 350 km; a storm day is a UT day with any three-hour Kp at or above 6−. The dispenser cap of 60.
  The launch dates.
* **Empirical pins.** The loss per onset and the storm structure, from the log and the Kp record. The 12-day exposure, from the orbit table.
  Onsets per window by phase, from cycles 17–24.
* **Voices.** The mission assurance lead: "Storm days are what kill satellites; count every one." The launch manager: "April has cost us
  before; April is cursed." The space-weather consultant: "Climatology is the honest baseline; phase-chasing is curve-fitting."
* **Licensed wrong basis.** The memo records that the launch insurer rates each launch on the storm days its exposure window is expected to
  contain and will price the policy on that basis.

## 8. Determinism by construction

* **Storm runs.** No two runs in the record are separated by exactly one or two quiet days, so any merge rule from zero to two quiet days
  builds the same storms.
* **Phase.** Cycle 25's smoothed maximum is October 2024 in the SILSO series; ±1 month and ±2 month analog bands give onset rates within 2%.
* **Exposure.** Onsets scale linearly with exposure across 9 to 19 days in the analogs, so a 12-day mean and the full exposure distribution
  give the same expected onsets within 1%.
* **Loss.** At these onset rates, 35% per onset and the compounded 1 − 0.65ⁿ agree within 1%.
* **Loads.** Each cap is the whole number below two divided by the expected loss per satellite; no unrounded cap sits within 0.1 of a whole
  number (April 52.7, October 49.5).

## 9. Prompt sketch and deliverables

> We have 360 satellites ready for 2027 and six rideshare launches booked, each able to carry 60. Our mission assurance lead says storm
> days are what kill satellites, so we should count every one. Tell me how many to load on each launch and how many wait for 2028, in one
> line I can send the launch provider, and send `launch_loading.xlsx` with the build and the sheets below, a chart
> `storm_onsets_by_month.svg`, and a one-page `loading_memo.docx`.

* `launch_loading.xlsx` — expected storm days and onsets per launch window, the loads, the passes sheet (ask A) and the capacity sheet
  (ask B).
* `storm_onsets_by_month.svg` — for each launch month, paired bars of expected storm days and storm onsets in the 12-day exposure, the
  two-satellite loss line converted to a load on a second axis, the 60-satellite cap drawn, and each launch's committed load labelled.
* `loading_memo.docx` — the committed loads and deferral, and why counting storm days halves them.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the three ground stations and each month of last quarter, the share of scheduled
  contact passes completed. *Device:* a pass rescheduled after an antenna fault keeps its pass ID with a new start in the pass-revision
  table, as the ground-segment guide documents; scoring against the original schedule marks rescheduled passes missed at two stations.
  Ground passes enter no part of the loading.
* **Ask B (device-carried).** For each of the four shells and each quarter of the last year, bandwidth sold. *Device:* capacity sold under
  a multi-shell contract is booked to the contract's primary shell in the sales ledger, with the split in the contract-allocation table, as
  the commercial data guide documents; reading the ledger alone puts all of it on one shell. Sales enter no part of the loading.
* **Ask C (validity).** The loads and deferral under each of the four rung constructions, and how many of the 40 past batches each loss
  rule reproduces.
* **Decoupling.** Clearing the storm runs changes no figure in asks A or B.

## 11. Rubric arithmetic

3 stations × 3 months (ask A) + 4 shells × 4 quarters (ask B) + 4 constructions × 2 (ask C) + the six committed loads and the deferral + 5
named chart parts + 3 files ≈ 48 criteria.

## 12. World-building constraints

* Expected storm days in a 12-day window at each launch's phase: Feb 0.196, Apr 0.325, Jun 0.146, Aug 0.180, Oct 0.352, Dec 0.170;
  onsets: 0.080, 0.1085, 0.068, 0.075, 0.1155, 0.074 (2.2–3.1 days a storm). All-years storm days 0.16 a window, 2.4 days a storm.
* Loss 35% of the low satellites per onset (33–37% in the log); exposure 12 days (70% of satellites cross on day 9, paused ones near day 19).
* Loads by rung: 47 each (78 deferred); 38/23/52/42/21/44 (140); 29/17/39/31/16/33 (195); 60/52/60/60/49/60 (19). Partials: per-day rate
  on the log's totals 60/45/60/60/42/60 (33); onsets without phase or without the 12-day exposure, 60 each (0).
* The twin batches are identical on every register column and in storm days met; lost 17 and 36.
* Pass revisions and contract allocations touch no Kp value, exposure day or loss in the loading.
