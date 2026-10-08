# DA39 — Which bus corridor carries the most journeys and gets the upgrade grant, when the survey hid three corridors' transfer factors

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Policy & Education · regional transit funding |
| Mirrors | Ranking options on a figure a survey publishes with small cells suppressed (engagement in small app markets, seller metrics under privacy thresholds, ads reach buckets), where a published total and its visible parts fix the hidden cell |
| Decision shape | Which of N gets one scarce thing: the regional corridor-upgrade grant goes to one of six bus corridors |
| Committed call | The corridor funded, and the annual journeys it carries, in millions to one decimal |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · a suppressed cell recovered from a published total and its visible parts (measured #24), with journeys built from boardings (S1) at rung 1 |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution support |
| Measured traps engaged | #24 treats an unpublished figure as unknown · #2 counts file rows instead of the real unit · #4 never tests its reading against the control |
| Calibration form | Change-log natural experiments: seven past route restructures that removed a transfer, each with boardings and journeys before and after |
| Driving force | Journeys are boardings divided by each corridor's boardings per journey from the on-board survey, which suppresses cells under 30 respondents. Each suppressed corridor is the only hidden cell in its sector, and the sector's respondent-weighted factor and every respondent count are published. The hidden factor is therefore exact. The express corridor's riders board once (1.00), not at the system average (1.55), and the cross-town corridor that leads on imputation transfers heavily (2.80). |

## 1. Situation

A regional transit authority funds one corridor upgrade a year, and its grant policy sends it to the corridor whose riders make the most
journeys on it. Six bus corridors are eligible. Automatic passenger counters record boardings by route. The latest on-board survey
publishes boardings per journey by route and by sector, suppressing route cells with fewer than 30 respondents. The pack holds counter
boardings, the survey tables with respondent counts, the counter guide, the service change log, and the grant policy.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each boarding count, each published factor and respondent count, each logged restructure. Nobody
  ranks the corridors on journeys and nothing reported is overturned. The difficulty is a value the survey did not print.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the committee's basis. Boardings converted with published factors and the system average for
  the hidden cells still name Ridgeway.
* **Instrument repair.** A larger survey would publish the three cells, but the pack's published cells already fix them exactly. The
  difficulty is reading an identity, not repairing a measurement.
* **Lens swap.** The naive ranking divides three corridors' boardings by a system average; the answer divides them by their own factors.
  Different journeys on the express and cross-town corridors.

## 3. The driving force

A strong solver converts boardings to journeys, which the change log certifies: every restructure that removed a transfer cut boardings
by exactly the transfer boardings while journeys held flat. It removes the counter guide's interlining double counts. Three corridors'
factors are blank, so it fills them with the system average of 1.55 boardings per journey, and Ridgeway, a cross-town corridor, leads. But
the survey's sector table is respondent-weighted, and every route's respondent count is printed even where its factor is not. Each hidden
corridor is the only blank in its sector, so its factor is the sector total less the visible routes, divided by its own respondents.
Ridgeway transfers at 2.80 and the Lakeline express at 1.00. Lakeline carries 9.7 million journeys, 1.19× the next corridor.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Annual boardings | A, Harbour feeder (19.5M, 1.18× Ridgeway) | The counters are the authority's ridership record | The change log: removing a transfer cuts boardings while journeys hold flat |
| 1 | Journeys: boardings ÷ published factor, hidden factors at the system average (1.55) | D, Canal Street (12.4M, 1.16× Ridgeway) | The right unit, every corridor filled in | The counter guide: interlined trips record each boarding under both routes |
| 2 | Hygiene: interlining double counts removed | B, Ridgeway (10.6M, 1.31× Harbour) | Clean counts on the right unit, every gap filled | The sector table: each hidden factor is fixed by its sector's total and visible routes |
| 3 | **Decisive:** hidden factors recovered from the respondent-weighted sector identity | **E, Lakeline express (9.7M, 1.19× Harbour)** (5th of 6 on rung 0) | — | — |

* **Position table.** Lakeline ranks 5th on rungs 0, 1 and 2 (9.7M boardings, then 6.3M journeys at the system average), and leads only
  rung 3.
* **Discriminator dominance.** Ridgeway carries 1.70× over Lakeline into rung 3. Recovery multiplies Lakeline by 1.55 (1.55 / 1.00) and
  Ridgeway by 0.55 (1.55 / 2.80), an edge of 2.80×, against the 1.2 × 1.70 = 2.04 needed (1.37× headroom). The product, 2.80 / 1.70 =
  1.65, is Lakeline's lead over Ridgeway on rung 3.
* **Partial correction priced (L3).** A solver who recovers only Lakeline's factor leaves Ridgeway at 10.6M, 1.10× Lakeline. One who
  recovers all three but keeps the interlining double counts names Canal Street at 12.4M, 1.27× Lakeline. One who reads the sector identity
  as boardings-weighted recovers Lakeline at 1.34 and names Harbour at 8.1M, 1.12× Lakeline. No half lands on Lakeline.
* **Grid.** Boardings (raw or cleaned) plus journeys × hygiene (off or on) × hidden factors (excluded, system average, sector identity)
  gives 8 cells. Seven name Harbour, Canal Street or Ridgeway; only cleaned journeys with the identity name Lakeline.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The survey's methods note says suppressed cells "are not published". It describes the sector table as
   respondent-weighted in a footnote about weighting, not about recovery.
2. **Pattern B, an identity rather than an estimate.** The recovered factors return every published sector total to the printed two
   decimals; the system-average fill misses all three sectors by 0.18 to 0.41. The recovery is a construction: respondent counts, visible
   factors and the sector total combined per sector.
3. **No arithmetic symptom.** Every sector table ties, boardings tie to the counter totals after the interlining removal, and journeys
   never exceed boardings.
4. **Not a row predicate.** Each hidden value comes from a weighted identity across the other routes of its sector.
5. **The enumeration is arithmetic.** No column carries the hidden factors.
6. **No cutover date.** One survey wave and one counter year, with nothing stepping.
7. **Survives deletion.** With every voice removed, the system-average fill still names Ridgeway.

## 6. The calibration corpus

* **Form.** The service change log: seven restructures that removed a transfer between 2017 and 2023, each with counter boardings and
  survey journeys for the year before and the year after.
* **What it certifies.** Journeys as the unit: boardings fell by the removed transfer boardings in all seven, within 0.3%, while journeys
  changed by under 1%.
* **What it is blind to.** Suppressed cells: every restructured route had a published factor in its survey year.
* **Twin pair.** Restructures R-3 and R-6 match on corridor type, boardings before, service hours and routes merged. Boardings fell 18%
  and 9% (2.0×) because R-3 removed a transfer for twice as many journeys; journeys held flat in both, which only the journey unit
  reproduces.
* **Resemblance points at the decoy.** By boardings and service hours, Lakeline resembles the low-ridership corridors the log never
  restructured.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The grant policy: the upgrade goes to the corridor whose riders make the most journeys on it. The counter guide documents
  interlined trips. The survey methods note fixes the suppression rule and the sector weighting.
* **Empirical pins.** The unit, from the change log; the hidden factors, from the identity.
* **Voices.** The planning director: "Boardings are what we count and what the board knows." The data manager: "Where the survey left a
  blank, the system average is the honest fill."
* **Licensed wrong basis.** The grant policy records that the board's finance committee scores corridors on boardings and will review the
  award on that basis.

## 8. Determinism by construction

* **Identity.** Every sector has exactly one suppressed route, and every route's respondent count is published, so each hidden factor is
  exact to two decimals.
* **Interlining.** The counter guide lists every interlined trip pair, and removal by trip ID is unambiguous.
* **Journeys.** Journeys on a corridor are its boardings divided by its factor, as the change log reproduces.
* **Rounding.** No two corridors fall within 0.5 million journeys at rung 3.

## 9. Prompt sketch and deliverables

> The corridor grant is decided at the March board, and our planning director wants it to go where the boardings are. Tell me which
> corridor gets it and how many journeys a year its riders make, in millions to one decimal, as the line for the board paper. Send
> `corridor_journeys.xlsx`, a chart `corridor_ranking.png`, and a one-page `grant_note.pdf`.

* `corridor_journeys.xlsx` — the journeys build for all six corridors, the fare sheet (ask A), the punctuality sheet (ask B) and the
  rung table (ask C).
* `corridor_ranking.png` — the six corridors' journeys under each rung as grouped bars, the three recovered factors annotated beside the
  system average, and the funded corridor marked.
* `grant_note.pdf` — the committed corridor, its journeys, and why the others fall away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each corridor, the share of fare-paying boardings on concession fares. *Device:* transfers
  within 60 minutes post as zero-fare taps with their own fare type, as the fare file's note says; counting them as fare-paying boardings
  understates concessions in four corridors.
* **Ask B (device-carried).** For each corridor, weekday on-time performance last quarter. *Device:* the performance standard excludes
  each trip's origin timepoint, which the timepoint file flags; including it overstates punctuality on every corridor.
* **Ask C (validity).** Journeys for each corridor under each of the four rungs, and each hidden factor under the identity, the system
  average and the boardings-weighted reading.
* **Decoupling.** Clearing the identity changes no figure in asks A or B.

## 11. Rubric arithmetic

6 corridors (ask A) + 6 corridors (ask B) + 6 × 4 rung figures and 3 × 3 hidden factors (ask C) + the committed corridor, its journeys
and its margin + 5 named chart parts + 3 files ≈ 61 criteria.

## 12. World-building constraints

* Boardings (M): Harbour 19.5, Ridgeway 16.5, Canal Street 13.6 (7.7 net of interlining), Wexford 11.0, Lakeline 9.7, Mill Lane 5.0.
* Factors: Harbour 2.40, Canal Street 1.10 and Mill Lane 1.30 published; Ridgeway 2.80, Wexford 2.40 and Lakeline 1.00 hidden; system
  average 1.55.
* Rung 3 journeys (M): Lakeline 9.7, Harbour 8.1, Canal Street 7.0, Ridgeway 5.9, Wexford 4.6, Mill Lane 3.8.
* Concession taps and timepoints never touch a boarding count or a survey factor.
