# RC26 — The account of Ferrier Square's lost weekday exits the Board adopts, when an entrance closure and a real station decline began on the same day

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Policy & Education · public transport capital planning |
| Mirrors | Storefront drops on two-sided marketplaces (Uber Eats and DoorDash restaurants, Amazon sellers, Google Maps local listings) where a temporary access outage and a lasting quality slip start in the same week, and the platform's record of past outages is the only measure of the part that comes back |
| Decision shape | A structure the body adopts: the cause account of the station's lost weekday exits, scored on which causes will still be missing at next autumn's census |
| Committed call | The five-part account the Station Review Board files for Ferrier Square, with the weekday exits of each cause to the nearest hundred and the persistent station-conditions component it carries into next year's target |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · O6 in-corpus natural experiments (the works log's past closures size the transient cause), with S1 (the Review counts journeys, the gates count exits) |
| Gate G mechanism | decomposition_attribution, with confirm_surface_read support |
| Measured traps engaged | #25 assumes an effect the log could measure · #2 counts file rows instead of the real unit · #11 beats the headline trap, misses the quiet one |
| Calibration form | Prior-period close-out: last year's Station Review close-out of seven stations, each adopted account set against this autumn's census |
| Driving force | The north entrance closed for escalator replacement on the same September day the station's conditions slipped, so every series in the pack returns only their sum. The only measure of what a closed entrance costs is the works log's nine past closures. They agree, at 0.270 of the closed entrance's journeys, only when each is taken as a destination effect in the OD model and divided by that entrance's share from the gate-array file and by its closed share of the census quarter. |

## 1. Situation

The metro authority runs one origin–destination census each autumn. Between the last two censuses, weekday exits at Ferrier Square, a
downtown station, fell from 45,000 to 36,000, while network journeys fell 5%. The Ferrier Square Business Improvement District (BID) wants a
station-improvement programme in next year's capital plan. Each year the Station Review Board adopts one account per flagged station.
The account sets the station's target for the next census, and the capital committee reads it. Ferrier Square's north entrance has been
closed since 1 September for escalator replacement and reopens in June. Ferrier Square is also the gate-line interchange with the regional
Lowmoor line.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct: the census matrices, the gate-array counts, the interchange taps, the works log and the
  close-out. No stakeholder's reading of their own figures is overturned. The BID is right that the station has slipped, and the account
  measures how much. The difficulty is sizing a transient cause that started the same day.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the BID letter and every voice. The Review's standard account, an OD decomposition on journeys, still books the
  whole destination effect to the station. A solver who notices the closure still books that same effect to the works.
* **Instrument repair.** No file is suspect. The gate arrays, card taps, census matrices, works log and close-outs are complete and current,
  and an exit count records exits correctly; a journey is built from taps, and no row claims to record one. Repair them anyway at every
  depth, down to an instrument that records every journey's origin and destination by day. Rung 0 still returns 6,900, rung 1 5,200, rung 2
  4,300 and rung 3 0, because both causes began on 1 September and every series steps once, by their sum. Only the past closures split them,
  so the decisive construction is still needed.
* **Lens swap.** The naive account describes this autumn's destination effect. The answer splits it by the part still missing at next
  autumn's census, sized from closures at other stations in other years: a different moment, measured on different populations.

## 3. The driving force

A strong solver links interchange taps so it counts journeys rather than gate exits, fits the Review's origin–destination model, and finds a
destination effect of −11.4%. The Review has always read that effect as station performance. Then the solver finds the closure in the works
log and reads the whole effect as works. The step appeared in the same census as the closure, and the station manager says the numbers will
come back when the doors reopen. Both readings name one cause, and both are wrong. The station's conditions slipped on the same day, and no
series can split the two. Only the works log's nine past closures can size a closed entrance. Measured naively, as raw changes in station
exits, they look useless: −1.8% to −13.9%, with no pattern. They become a constant only when each is taken as a destination effect, divided
by the closed entrance's share of journeys (from the gate-array file) and by the closed fraction of the census quarter (from the closure
dates). The constant is 0.270, from 0.269 to 0.271. That puts the works at 3,000 exits and leaves 1,300 exits of real station decline.

## 4. The ladder

| Rung | Construction | Lands on (persistent station component, of 9,000 lost exits) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Station exits against the network change, the excess booked to the station | Station 6,900 (+431%) | The dashboard comparison, and the BID's own case | The Review counts journeys, and 6,000 of last autumn's exits re-entered the Lowmoor gates within minutes on the same card |
| 1 | Hygiene of the unit: interchange exits linked out, journeys against the network | Station 5,200, interchange 2,000 (+300%) | Exits that were never journeys ending here are removed, and every count reconciles | The OD census shows Ferrier's riders come from corridors whose own travel fell more |
| 2 | The Review's OD decomposition on journeys, with the destination effect as station performance | Station 4,300, catchment 900 (+231%) | The Review's standing account. Its construction reproduces all seven close-outs exactly | The works log: the north entrance was closed for the whole census quarter |
| 3 | The step arrived with the closure, so the whole destination effect is works and returns in June | Station 0, works 4,300 (−100%) | An event-study reading, satisfying and transient, and the station manager's view | The nine past closures, measured the same way, cost 0.270 of a closed entrance's journeys, which is 3,000 exits here, not 4,300 |
| 4 | **Decisive:** works sized from the past closures (destination effect ÷ entrance share ÷ closed share of quarter), remainder booked to station conditions | **Works 3,000 (transient), station 1,300 (persistent)** | — | — |

* **Figure shape.** Every correction walks the station component down, from 6,900 to 0. The decisive move reverses that walk and leaves
  1,300. The full account is interchange 2,000, network 1,800, catchment 900, works 3,000 and station 1,300, totalling 9,000.
* **Partial correction priced (L3).** Rung 3 sits 1,300 exits from the answer, and every partial use of the past closures lands further
  away. Transferring their mean effect without dividing by entrance share books 2,800 to the station. Skipping the exposure scaling also
  books 2,800. Sizing the works from the three neighbours' gain books 3,100, because 60% of the lost riders went to buses. Taking their raw
  mean books 3,400. Assuming half the entrance is lost books a 1,500-exit gain.
* **Grid.** Unit (exits or journeys) × origin control (none or OD) × works sizing (none, whole step, past closures) = 12 cells. Every
  non-answer cell sits at least 900 exits (69%) from the answer. The nearest applies the past closures correctly but skips the Review's own
  origin control, so the catchment's 900 exits land on the station. The next nearest is the decisive method run on exits, at 2,500.
* **Which guard binds.** This is a figure inside a structure, with no ranking to change, so the separation floor binds, not the 1.20×
  rung margin.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** No document sizes an entrance closure or says a destination effect can hold one. The works log is a maintenance
   record with dates, entrances and contract numbers.
2. **Corpus blind for a computable reason.** *In every closed-out station both censuses ran with every entrance open, because the escalator
   programme was suspended for the whole of last fiscal year while its contract was re-tendered.* The close-out certifies rung 2 seven of
   seven times and cannot show how a closure splits a destination effect.
3. **No arithmetic symptom.** Journeys, exits, OD totals, gate arrays and interchange links reconcile on every rung. Diverted riders spread
   over three neighbours and buses, and no neighbour's destination effect moves outside its own year-to-year range.
4. **Not a row predicate.** The constant is, for each past closure, a model-derived destination effect divided by a joined entrance share
   and by a calendar exposure. It is then applied to a fifth station's share.
5. **The enumeration is arithmetic.** Nothing in the pack says how many exits the works cost. The figure is computed.
6. **No cutover date.** The census runs once a year, and both causes began between two censuses on the same day. No series steps at a date
   that isolates either cause.
7. **Survives deletion.** With every voice removed, the natural pipeline still stops at rung 2 or 3.

## 6. The calibration corpus

* **Form.** Last year's Station Review close-out: seven stations, each with its adopted account (network, catchment, interchange where it
  applies, destination) in weekday exits, set against this autumn's census.
* **What it certifies.** The journey unit and the Review's model. Rung 2's construction (interchange-linked journeys, the Review's weighted
  OD fit, log-proportional apportionment) reproduces all seven accounts to the exit. OD on exits reproduces five of seven, missing the two
  interchange stations by 600 and 1,100 exits. Sequential apportionment misses all seven, by 30 to 90 exits.
* **What it is blind to.** Entrance closures (property 2).
* **Twin pair (in the works log's closure record).** Closures W-14 and W-22 are identical on every works-log column: downtown two-entrance
  stations, escalator replacement, one full autumn quarter each. Their stations' destination effects were −4.9% and −9.7%, 1.99× apart. The
  closed entrances carried 18% and 36% of journeys. Only the share-normalised constant reproduces both, so no transferred effect survives.
* **Every rule exercised.** W-31 covered 6 of the census quarter's 13 weeks, and only exposure scaling reproduces its −2.5%.
* **Resemblance points at the decoy.** Ferrier Square most resembles closed-out Tanner's Yard: downtown, a gate-line interchange, an
  outer-corridor catchment. Its account booked a 3,900-exit destination effect to station performance, and its programme recovered 3,500
  of those exits by this census.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The Review manual: "The Review counts journeys, and a journey ends where the passenger leaves the network." The manual also
  fixes the census quarter, the weekday calendar and the OD model's weights and small-pair floor. The works programme files the north
  entrance's reopening date.
* **Empirical pins.** The closure constant comes from the nine past closures. The apportionment rule comes from the close-out. The
  interchange window comes from the tap record's empty band (below).
* **Voices.** BID chair: "Anyone who walks through Ferrier Square can see the station has gone downhill." Station manager: "A closed entrance
  always looks worse than it is; the numbers come back when the doors reopen." Planning lead: "Ferrier's riders live on the outer corridors,
  and the outer corridors stopped commuting."
* **Licensed wrong basis.** The Review manual records that the capital committee reads a station's destination effect as its station
  performance, as every Review has done, and will present Ferrier Square's account on that basis.

## 8. Determinism by construction

* **Interchange window.** Every linked exit is followed by a Lowmoor entry on the same card within 2 to 9 minutes, and none between 10 and 90
  minutes, so any window from 10 to 90 minutes links the same 6,000 and 4,000.
* **The constant.** The nine closures give 0.269 to 0.271, and every component of the account rounds to the same hundred anywhere in that
  range.
* **Exposure.** Closures start and end on week boundaries, and exposure is closed census weekdays over census weekdays.
* **Apportionment.** Log-proportional, pinned by the close-out. Component order cannot matter.
* **Maturity.** Both censuses are complete. The reopening falls in June, before next autumn's census, so the works component is wholly
  transient by the scoring date.
* **Small pairs.** Every origin feeding Ferrier Square clears the small-pair floor, so including or excluding small pairs leaves its account
  unchanged.

## 9. Prompt sketch and deliverables

> The Board adopts one account of why Ferrier Square's weekday exits fell by a fifth this autumn. That account becomes the station's target
> for next autumn's census and decides whether the BID's station programme goes into the capital plan. The BID is sure the station itself
> has gone downhill. Give me the account you would have the Board adopt: each cause, the weekday exits it accounts for to the nearest
> hundred, and which causes will still be missing at next autumn's census, written so I can read it into the minutes. Send
> `ferrier_account.xlsx`, a bridge chart `ferrier_bridge.png`, and a one-page `board_paper.pdf`.

* `ferrier_account.xlsx` — the account, the peak-share sheet (ask A), the fare sheet (ask B) and the close-out back-test (ask C).
* `ferrier_bridge.png` — a waterfall from 45,000 to 36,000 weekday exits with one bar per cause. Transient bars are hatched, the June
  reopening is annotated on the works bar, next autumn's target is drawn as a labelled reference line, and the title states the finding.
* `board_paper.pdf` — the account in words and what it means for the programme.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 12 downtown stations, the share of weekday exits between 07:00 and 10:00 local
  time in last autumn's census and in this one. *Device:* tap times are in UTC, as the tap dictionary states, and both census quarters cross
  the end of daylight saving. Reading UTC as local time moves 5 to 9 points of peak share at the commuter stations. The main call aggregates
  on the service-date column and never reads the hour.
* **Ask B (device-carried).** For each of the 12 downtown stations, this autumn's average weekday fare revenue for pay-as-you-go and for
  period products. *Device:* taps after a card reaches the daily cap post at full fare, and the cap refund posts as one end-of-day
  adjustment row per card, as the fare dictionary documents. Summing taps without the adjustments overstates pay-as-you-go revenue by 11–18%
  at the stations where most riders hit the cap. The main call uses no fares.
* **Ask C (validity).** For each of the seven closed-out stations, the Review's adopted network, catchment and destination components
  beside the ones your construction returns.
* **Decoupling.** Setting the closure constant to zero or to the full share changes no figure in asks A or B. Ask C runs only on stations
  that had every entrance open.

## 11. Rubric arithmetic

12 stations × 2 censuses (ask A) + 12 stations × 2 products (ask B) + 7 stations × 3 components (ask C) + the account's five causes, the
persistence of each and next autumn's target + 5 named chart parts + 3 files ≈ 85 criteria.

## 12. World-building constraints

* Last autumn: 45,000 weekday exits at Ferrier Square = 39,000 journeys + 6,000 Lowmoor interchanges. This autumn: 36,000 = 32,000 + 4,000.
  Network journeys fell 5.0%, and Ferrier's origin-weighted catchment factor is 0.975.
* The north entrance carried 30% of journeys, and the station-conditions factor is 0.964. Both began on 1 September.
* The nine past closures have mean entrance share 0.15 and mean quarter exposure 0.50. Each reproduces 0.270 ± 0.001, while their raw
  exit changes run from −1.8% to −13.9%.
* Per-rung station components are 6,900 / 5,200 / 4,300 / 0 / 1,300, and works components are 0 / 0 / 0 / 4,300 / 3,000.
* W-14 and W-22 are identical on every works-log column. Their shares are 0.18 and 0.36, and their effects −4.9% and −9.7%.
* The close-out holds seven stations, two of them gate-line interchanges, all with every entrance open in both censuses.
* Diverted riders split 40% to three neighbours and 60% to buses. UTC times and fare caps never touch service-date totals or the works log.
