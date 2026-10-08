# AD43 — How many operator hours a week the new incident rule frees, when a fifth of the incidents it must catch are located only by landmark

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Supply Chain & Logistics · freeway traffic operations |
| Mirrors | Measuring a detector's recall against ground truth whose records are keyed two ways before cutting the staff the old alarm needed (incident detection in Google Maps and Waze evaluated against police logs located by landmark, network-outage detection evaluated against tickets located by site name rather than device ID) |
| Decision shape | One figure committed at a date: operator alert-duty hours freed per week next year, written into the roster plan |
| Committed call | The weekly operator hours taken off alert duty, to the nearest hour, in the roster plan filed on 15 November |
| Gap · Pattern | Gap 4 (rule recovered by exact reproduction) over Gap 2 (population of incidents) · an implicit join (landmark-only incidents resolved through the interchange table), with a latent attribution marker (lane closures identified by the sign log) below it |
| Gate G mechanism | method_or_model_selection, with binding_constraint support |
| Measured traps engaged | #18 joins only on the visible key · #17 guesses an attribution the data can settle · #3 stops at a close but inexact match |
| Calibration form | Published control set with a reproduction clause: the transport department's published lane-closure detection figures for the corridor's eight segments in 2023 and 2024, which the staffing policy requires any evaluation basis to reproduce exactly |
| Driving force | The new rule may replace operators only in a configuration that catches 85% of lane-closure incidents, and which incidents count is fixed by the department's published figures. A fifth of incidents carry no postmile, only a landmark code, and look unlocated; a third carry no lane field, though every lane closure gets a sign message within ten minutes. Only resolving landmarks through the interchange table and reading lane closures off the sign log reproduces all 16 published cells. On that basis the quiet configurations fail the gate, because landmark incidents sit at interchanges where congestion recurs and the profile rule is slow, so the centre must adopt the noisiest configuration and the freed hours fall to 51. |

## 1. Situation

A traffic management centre pages operators whenever a station on its 31-mile corridor drops below 35 mph: 18,000 pages a year, one
operator-hour per four pages. A profile-based rule (speed against the station's own time-of-week profile, confirmed at neighbouring
stations, held for several five-minute bins) comes in four configurations, from the quietest (mainline confirmation, four bins: 3,600 alerts)
to the noisiest (connector stations included, two bins: 7,300). The staffing policy lets the centre adopt the quietest configuration that
catches at least 85% of lane-closure incidents within 15 minutes, on an evaluation basis that reproduces the department's published detection
figures. The centre holds a year of station data, the police incident log, its sign-message log, the landmark and interchange tables and the
published figures. The operations chief is sure the quietest version will do.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: station speeds, alerts, the incident log as the police recorded it (postmile or landmark, lane field
  or blank), the sign log and the published figures. Nobody's numbers are overturned; the difficulty is which incidents the gate counts,
  which depends on links the incident log's main key does not carry.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the chief's view and the legacy alert file. A replay on postmile-located incidents with lane closures read from the
  sign log still adopts a quiet configuration and frees 60 hours.
* **Instrument repair.** Make the incident log perfect as a record: officers at an interchange record a landmark because that is where they
  are, and the record is right. The link to the mainline runs through the interchange table either way.
* **Lens swap.** The naive population is postmile-located incidents with a lane field; the answer's adds landmark-located and sign-identified
  lane closures, mostly at interchanges, a different population that moves the adopted configuration.

## 3. The driving force

A strong solver replays each configuration with profiles built only from prior same weekdays, drops samples below 50% observed as the memo
requires, matches alerts to incidents within a mile and 15 minutes, and notices that a third of incidents carry no lane field. It reads lane
closures off the sign log, where every closure gets a message within ten minutes, and adopts the mainline three-bin configuration (60 hours
freed at 87% recall). Every step is correct, and every incident it evaluates carries a postmile. The police record 22% of incidents only by
landmark ("eastbound at the Harbor interchange"), and the log's dictionary says the location is a postmile where recorded and otherwise a
landmark code. Those incidents look unlocated, and dropping them still leaves an evaluation that reconciles. Resolving each landmark through
the interchange table to its mainline postmile adds incidents at merges, where recurrent congestion keeps speeds near profile and the rule
confirms late. With them, only the connector two-bin configuration clears 85%, and the 16 published cells reproduce only on this basis.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Lane field as recorded, postmile-located incidents, all samples kept: the quietest configuration passes (89%) | 69 hours, +35% | A clean replay of the memo's rule against the police log | The memo's data-quality clause: samples under 50% observed are dropped, and without them the quietest configuration catches 84% |
| 1 | Hygiene applied: the four-bin mainline configuration fails, three-bin mainline passes (86%) | 66 hours, +29% | The rule as written on clean data | The sign log: every lane closure gets a message within ten minutes, and a third of closures have a blank lane field |
| 2 | Lane closures from the sign log: three-bin mainline fails (83%), three-bin connector passes (87%) | 60 hours, +18% | Every closure counted, and the evaluation reconciles to the log | The published figures: this basis gives 104 and 111 closures against the department's 131 and 140 |
| 3 | **Decisive:** landmark-only incidents resolved through the interchange table to mainline postmiles: only connector two-bin passes (86%) | **51 hours** | — | — |

* **Figure shape.** The answer is the minimum cell of the grid; every rung and partial reading frees more hours than the corridor can safely
  give up, and each is wrong in the same direction.
* **Partial correction priced (L3).** A solver who resolves landmarks by the nearest cross-street postmile on the street centreline file
  (instead of the interchange table) puts a third of them on the wrong side of the interchange or the wrong carriageway, gets 85.2% for the
  three-bin connector configuration and frees 60 hours: rung 2's figure, 18% above the answer and no nearer it.
* **Grid.** Hygiene (off or on) × lane attribution (field or sign log) × location (postmile only or landmarks resolved) = 8 cells: 69, 66,
  66, 66, 60, 60, 60 and 51. The nearest wrong cell is 60, 18% above the answer, and needs two of the three constructions.
* **Configuration table.** On the reproducing basis recall runs 78%, 80%, 83% and 86% from quietest to noisiest, so the gate selects
  exactly one configuration, 7,300 alerts against the legacy 18,000: (18,000 − 7,300) ÷ 4 ÷ 52 = 51.4.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The incident dictionary says a location is a postmile or a landmark code; nothing says landmark incidents belong in
   any evaluation or how the department counted them.
2. **The corpus pins a construction, not a menu (Pattern B).** Sign-log lane closures with landmarks resolved reproduce all 16 published
   cells (eight segments, two years) exactly. The sign log alone reproduces 6, the lane field alone 2, and every rival undercounts, so each
   misses both annual totals by at least 20%. Landmark resolution is a two-hop join (landmark to interchange to mainline postmile), not a
   parameter.
3. **No arithmetic symptom.** Every postmile-located incident matches a segment, every alert matches a station, and dropping landmark-only
   incidents leaves a closed, reconciling evaluation.
4. **Not a row predicate.** Each landmark incident needs the landmark table, the interchange table and a direction rule to reach a mainline
   postmile, then the time-and-distance match to alerts.
5. **The enumeration is arithmetic.** Which incidents enter the gate is computed; no column flags them.
6. **No cutover date.** Landmark recording is standing police practice at interchanges; nothing steps.
7. **Survives deletion.** Remove the chief's view and the legacy file: the postmile replay with sign-log closures is still the natural build.

## 6. The calibration corpus

* **Form.** The department's published lane-closure figures for the corridor: closures and closures detected within 15 minutes by the
  legacy rule, for eight segments in 2023 and 2024, with the staffing policy's clause that an evaluation basis must reproduce every cell.
* **What it pins.** Both constructions together (above). The sign-log marker is absolute: every incident with a recorded closure has a
  message, and no incident recorded as non-blocking has one.
* **Twin pair.** Segments 3 and 6 have identical police incident counts, postmile-located counts, lane-field counts and alert volumes. The
  department published 9 closures for segment 3 and 18 for segment 6, 2.0× apart, because nine of segment 6's closures were recorded at the
  Harbor interchange by landmark only.
* **Resemblance points at the decoy.** The corridor's 2025 incident profile matches 2023's on every visible column, so a lookup carries
  2023's published detection rate forward.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The staffing policy: the quietest configuration that catches 85% of lane-closure incidents within 15 minutes may be
  adopted, on an evaluation basis that reproduces the published figures; one operator-hour per four alerts. The memo's data-quality clause.
  The incident dictionary's location definition. One sentence each.
* **Empirical pins.** Lane closures from the sign log, landmark resolution from the tables, both through reproduction.
* **Voices.** The operations chief: "The quietest version will do; our corridor is not complicated." The roster manager: "Every page we drop
  is an operator back on the floor."
* **Licensed wrong basis.** The policy records that the operators' union evaluates rules on postmile-located incidents with the lane field as
  recorded and will present that evaluation at the roster consultation.

## 8. Determinism by construction

* **Landmark direction.** Each landmark code names a carriageway, and the interchange table gives one mainline postmile per carriageway, so
  no direction convention is chosen.
* **Match window.** No incident has an alert between 14 and 16 minutes after it, so 15-minute matching is not a fork.
* **Profiles.** Built from the prior eight same weekdays with holidays skipped, as the memo states; six- and ten-week profiles adopt the same
  configuration.
* **Rounding.** 51.4 hours rounds to 51 under any convention.

## 9. Prompt sketch and deliverables

> Next year's roster has to say how many operator hours a week come off alert duty if the new incident rule goes in, and it can only go in
> if it keeps catching the lane closures. The operations chief is sure the quietest version will do. Give me the number of hours, to the
> nearest hour, for the roster, and send `rule_replay.xlsx`, a chart `recall_by_configuration.png`, and a one-page `roster_note.pdf`.

* `rule_replay.xlsx` — the replay by configuration on each evaluation basis with its published-cell reproduction count (ask C), the patrol
  sheet (ask A) and the traffic-count sheet (ask B).
* `recall_by_configuration.png` — recall of the four configurations on each evaluation basis as grouped bars, the 85% gate as a labelled
  line, alert volume on a second axis, and the adopted configuration and freed hours in the title.
* `roster_note.pdf` — the committed figure and why each quieter configuration is not available.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the eight segments, service-patrol assists last year and their median duration.
  *Device:* an assist spanning midnight is split into one row per calendar day sharing an assist ID, as the patrol guide says; counting rows
  inflates assists and halves durations on two segments. The roster figure never uses patrol records.
* **Ask B (device-carried).** For each segment, annual average daily traffic and truck share from the count stations. *Device:* each station
  reports its two directions as separate rows and the count guide defines segment traffic as their sum; reading one direction halves three
  segments.
* **Ask C (validity).** For each of the four evaluation bases: published cells reproduced, the adopted configuration and the freed hours.
* **Decoupling.** Clearing landmark resolution and sign-log attribution changes no figure in asks A or B.

## 11. Rubric arithmetic

8 segments × 2 (ask A) + 8 × 2 (ask B) + 4 bases × 3 (ask C) + the committed hours, the adopted configuration, its recall and the recall of the
configuration ruled out + 5 named chart parts + 3 files ≈ 56 criteria.

## 12. World-building constraints

* Configurations: 3,600 / 4,200 / 5,600 / 7,300 alerts; legacy 18,000. Rung figures 69 / 66 / 60 / 51 hours.
* 22% of incidents carry only a landmark; 31% of closures have a blank lane field; every closure has a sign message within ten minutes.
* Published closures 131 (2023) and 140 (2024); the reproducing basis matches all 16 segment cells.
* Segments 3 and 6 are identical on every incident-log and alert column.
* Patrol logs and count stations never touch station speeds, alerts, the incident log or the sign log.
