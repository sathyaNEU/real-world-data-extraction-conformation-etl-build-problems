# DA39 — Which bus corridor gets the upgrade grant, when past upgrades only added riders where buses lost their time at junctions

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Policy & Education · regional transit funding |
| Mirrors | Choosing where to deploy a fix whose past gains split on a cause nothing labels (a latency fix that only helps where time is lost in the network rather than the client, a checkout redesign that only lifts sites where users stall at payment, warehouse automation that only helps where pickers wait on travel), when the earlier rollouts ran mostly where the fix works |
| Decision shape | Which of N gets one scarce thing: the regional bus-priority upgrade grant goes to one of six corridors |
| Committed call | The corridor funded, and the journeys a year the upgrade adds there, in millions to two decimals |
| Gap · Pattern | Gap 1 (time) over Gap 2 (population) · Pattern E (conditioned yield: an upgrade's gain splits on where buses lose time, a construction from AVL timepoints), with journeys built from boardings at rung 1 (S1) and suppressed survey cells recovered at rung 2 (measured #24) |
| Gate G mechanism | forecasting, with decomposition_attribution support |
| Measured traps engaged | #13 validates on one population, applies to another · #2 counts file rows instead of the real unit · #24 treats an unpublished figure as unknown |
| Calibration form | Change-log natural experiments: ten past bus-priority upgrades, each with section-by-section journeys for the year before and the year after and the AVL timepoints of both years |
| Driving force | Bus priority adds riders by giving back time lost in traffic at signalised junctions. The change log's ten upgrades show it section by section: sections whose buses lost their time at junctions gained 22% to 26% in journeys, and sections that lose it at stops gained 0% to 2%. Where a corridor loses its time is a construction from AVL timepoints against the junction and stop registers, not a column. Past upgrades were mostly junction-delayed arterials, so the pooled +17% applies to no section, and the busiest candidates lose their time at stops. |

## 1. Situation

A regional transit authority funds one bus-priority upgrade a year, lanes and signal priority along one corridor, and its grant policy
sends it to the corridor where the upgrade will add the most journeys. Six corridors are eligible. Automatic passenger counters record
boardings by route; the latest on-board survey publishes boardings per journey by route and by sector, suppressing route cells under 30
respondents; and the AVL system logs every bus's timepoints. The pack holds counter boardings, the survey tables with respondent counts,
the counter guide, the AVL timepoint file with the junction and stop registers, the service-hours file, the change log of past upgrades,
and the grant policy.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each boarding count, each published factor and respondent count, each timepoint and each logged
  upgrade. Nobody ranks the corridors on journeys added and nothing reported is overturned. The difficulty is which corridors an upgrade
  can help.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the committee's basis. Journeys with recovered factors, raised by the pooled past uplift,
  still fund Lakeline.
* **Instrument repair.** Suspect: the on-board survey, a sample with three cells suppressed, and the counters, which record an interlined
  boarding under both routes. Repaired, interlining removed and every corridor's journeys known exactly, rung 0 still funds Harbour and
  rungs 1 and 2 fund Lakeline. The AVL timepoints are complete, and the journeys an upgrade will add are a forward quantity no instrument
  records, so the answer stays Wexford and the delay conditioning is still needed.
* **Lens swap.** The naive ranking scales every corridor by one pooled uplift; the answer gives each section the uplift of the sections
  that lose time where it does, a different population of comparable upgrades for each corridor.

## 3. The driving force

A strong solver converts boardings to journeys, removes the counter guide's interlined double counts, recovers the survey's three hidden
factors from the respondent-weighted sector identity, and scales each corridor's journeys by the change log's pooled uplift, +17%.
Lakeline, the express, leads with 9.7 million journeys. But the change log's ten upgrades split cleanly by section. Sections whose buses
lost most of their delay at signalised junctions gained 22% to 26%; sections that lost it at stops gained 0% to 2%. No column says which
kind a section is: the AVL timepoints, joined to the junction and stop registers, apportion each trip's delay between them. Lakeline's
buses lose their time at three interchange stops where queues board, and Wexford's at eleven signalised junctions on an arterial.
Upgraded, Wexford gains 1.10 million journeys a year and Lakeline 0.10 million.

## 4. The ladder

| Rung | Construction | Funds | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Annual boardings × the change log's pooled uplift (+17%) | A, Harbour feeder (3.32M added, 1.18× Ridgeway) | The counters are the ridership record, scaled by measured upgrades | The survey: riders board 1.00 to 2.80 times per journey by corridor, and the counter guide double-counts interlined trips |
| 1 | Journeys: boardings net of interlining ÷ published factors, hidden factors at the system average (1.55), × the pooled uplift | B, Ridgeway (1.81M, 1.31× Harbour) | The right unit, every corridor filled in | The sector table: each hidden factor is fixed by its sector's total and visible routes |
| 2 | Hidden factors recovered from the respondent-weighted sector identity, × the pooled uplift | C, Lakeline express (1.65M, 1.20× Harbour) | Exact journeys on every corridor, scaled by every past upgrade | The change log: sections losing time at stops gained 0% to 2%, sections losing it at junctions 22% to 26% |
| 3 | **Decisive:** each corridor's journeys × the uplift of its sections' delay type, apportioned from AVL timepoints against the junction and stop registers | **E, Wexford (1.10M, 1.19× Mill Lane)** (4th of 6 on rung 0) | — | — |

* **Position table.** Wexford ranks 4th on rung 0 (1.87M), 3rd on rung 1 (1.21M) and 5th on rung 2 (0.78M), and leads only rung 3.
* **Discriminator dominance.** Lakeline carries 2.12× over Wexford into rung 3 (9.7 against 4.6 million journeys). Conditioning
  multiplies Wexford by 1.41 (24% for 17%) and Lakeline by 0.06 (1% for 17%), an edge of 24×, against the 1.2 × 2.12 = 2.54 needed (9.4×
  headroom). The product, 24 / 2.12 = 11.3, is Wexford's lead over Lakeline on rung 3; Mill Lane, also junction-delayed, is runner-up at
  0.92M.
* **Partial correction priced (L3).** A solver who conditions on the authority's corridor types instead of measured delay counts the
  Lakeline express with the junction-delayed corridors and funds it, 2.1× Wexford (2.33M). One who apportions delay from the timetable's
  running-time allowances rather than the AVL timepoints counts Canal Street as junction-delayed and funds it, 1.53× Wexford (1.68M). No
  half lands on Wexford.
* **Grid.** Base (boardings, journeys at the system average, journeys with recovered factors) × uplift (pooled, by corridor type, by
  timetable delay, by measured delay) = 12 cells. The three cells with measured delay all fund Wexford; the other nine fund Harbour,
  Ridgeway, Lakeline or Canal Street.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The policy funds the most journeys added. The change log records each upgrade's journeys before and after, and
   the AVL file records timepoints. No document says where a corridor loses its time or that bus priority helps only junction delay.
2. **Pattern E, absolute in the change log.** Every junction-delayed section of the ten upgrades gained 22% to 26% and every stop-delayed
   section 0% to 2%, with nothing between; the pooled +17% fits no section. The delay split is a construction: each trip's timepoints
   against the junction and stop registers, delay apportioned segment by segment and summed by section.
3. **No arithmetic symptom.** Boardings tie to counter totals once interlining is removed, the sector tables tie, and every upgrade's
   before and after journeys tie to the survey.
4. **Not a row predicate.** A section's delay type sums thousands of timepoint segments, each apportioned to a junction or a stop.
5. **The enumeration is arithmetic.** No column gives a section's delay split or an upgrade's uplift.
6. **No cutover date.** The logged upgrades span ten years with no trend in their effect, and the grant's effect is next year's.
7. **Survives deletion.** With every voice removed, recovered journeys under the pooled uplift still fund Lakeline.

## 6. The calibration corpus

* **Form.** The change log: ten bus-priority upgrades between 2014 and 2023, each with section-by-section journeys for the year before
  and the year after, and its AVL timepoints for both years.
* **What it certifies.** That upgrades add journeys, and that journeys, not boardings, carry the gain.
* **What it pins.** The split by delay type, absolute in every section of all ten upgrades.
* **Twin pair.** Upgrades U-2 and U-7 match on corridor type, journeys before (6.2M), length, frequency and stop count. Their journeys
  rose 24% and 12% (2.0×): every section U-2 upgraded lost its time at junctions, and half of U-7's lost it at stops.
* **Resemblance points at the decoy.** By journeys, frequency and corridor type, Lakeline resembles the arterials whose upgrades gained
  most.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The grant policy: the upgrade goes to the corridor where it will add the most journeys a year, judged on the change
  log's measured upgrades. The counter guide documents interlined trips. The survey methods note fixes the suppression rule and the sector
  weighting.
* **Empirical pins.** The unit, from the survey; the hidden factors, from the identity; the delay split, from the change log and the AVL
  timepoints.
* **Voices.** The planning director: "The busiest corridor will gain the most; that's where the riders are." The data manager: "Every
  upgrade we have done has paid off, and the past gains will carry over."
* **Licensed wrong basis.** The policy records that the board's finance committee scores corridors on boardings and will review the award
  on that basis.

## 8. Determinism by construction

* **Identity.** Every sector has exactly one suppressed route and every route's respondent count is published, so each hidden factor is
  exact to two decimals.
* **Interlining.** The counter guide lists every interlined trip pair, and removal by trip ID is unambiguous.
* **Delay split.** No section's junction share of delay lies between 30% and 70%, so every section is cleanly one type.
* **Rounding.** No two corridors fall within 0.1 million journeys added at rung 3.

## 9. Prompt sketch and deliverables

> The corridor grant is decided at the March board, and our planning director wants it on the busiest corridor. Tell me which corridor
> gets it and how many journeys a year the upgrade will add there, in millions to two decimals, as the line for the board paper. Send
> `corridor_upgrade.xlsx`, a chart `delay_split.png`, and a one-page `grant_note.pdf`.

* `corridor_upgrade.xlsx` — journeys and journeys added for all six corridors under each rung, the fare sheet (ask A), the productivity
  sheet (ask B) and the change-log table (ask C).
* `delay_split.png` — each corridor's delay per trip split into junction and stop time as stacked bars, the ten past upgrades' section
  gains plotted against their junction share, the pooled uplift drawn as a line, and the funded corridor marked.
* `grant_note.pdf` — the committed corridor, the journeys it adds, and why the busier corridors fall away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each corridor, the share of fare-paying boardings on concession fares. *Device:* transfers
  within 60 minutes post as zero-fare taps with their own fare type, as the fare file's note says; counting them as fare-paying boardings
  understates concessions in four corridors.
* **Ask B (device-carried).** For each corridor, weekday boardings per service hour last quarter. *Device:* the service-hours file includes
  deadhead running, flagged by trip type; counting it understates productivity on four corridors.
* **Ask C (validity).** Journeys added for each corridor under each of the four rungs, and each past upgrade's section gains against its
  junction share.
* **Decoupling.** Clearing the delay conditioning changes no figure in asks A or B.

## 11. Rubric arithmetic

6 corridors (ask A) + 6 corridors (ask B) + 6 × 4 rung figures and 10 upgrade gains (ask C) + the committed corridor, its journeys added
and its margin + 5 named chart parts + 3 files ≈ 57 criteria.

## 12. World-building constraints

* Boardings (M): Harbour 19.5, Ridgeway 16.5, Canal Street 13.6 (7.7 net of interlining), Wexford 11.0, Lakeline 9.7, Mill Lane 5.0.
* Factors: Harbour 2.40, Canal Street 1.10 and Mill Lane 1.30 published; Ridgeway 2.80, Wexford 2.40 and Lakeline 1.00 hidden; system
  average 1.55. Journeys with recovered factors (M): Lakeline 9.7, Harbour 8.1, Canal Street 7.0, Ridgeway 5.9, Wexford 4.6, Mill Lane 3.8.
* Uplift by delay type: Wexford and Mill Lane 24%; Harbour and Canal Street 2%; Lakeline and Ridgeway 1%; pooled 17%. Journeys added at
  rung 3 (M): Wexford 1.10, Mill Lane 0.92, Harbour 0.16, Canal Street 0.14, Lakeline 0.10, Ridgeway 0.06. Partial cells: Lakeline 2.33,
  Canal Street 1.68.
* Concession taps and deadhead hours never touch a boarding count, a survey factor or a timepoint.
