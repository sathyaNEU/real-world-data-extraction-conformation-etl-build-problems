# AD43 — How many operator hours a week the new incident rule frees, when the department credits a detection only from inside the closure's queue

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Supply Chain & Logistics · freeway traffic operations |
| Mirrors | Measuring a detector's recall the way the authority that certifies it measures it before cutting the staff the old alarm needed (incident detection in Google Maps and Waze scored against transport agencies' published detection rates, network-outage detection scored against a regulator's published availability figures) |
| Decision shape | One figure committed at a date: operator alert-duty hours freed per week next year, written into the roster plan |
| Committed call | The weekly operator hours taken off alert duty, to the nearest hour, in the roster plan filed on 15 November |
| Gap · Pattern | Gap 4 (rule recovered by exact reproduction) over Gap 2 (population of incidents) · a reproduction-gated control set whose only reproducing construction credits a detection to an alert from a station inside the closure's queue, with a latent attribution marker (lane closures identified by the sign log) and landmark resolution below it |
| Gate G mechanism | method_or_model_selection, with binding_constraint support |
| Measured traps engaged | #3 stops at a close but inexact match · #17 guesses an attribution the data can settle · #4 never tests its reading against the control |
| Calibration form | Published control set with a reproduction clause: the transport department's published lane-closure figures for the corridor's eight segments in 2023 and 2024 (closures, and closures detected within 15 minutes by the legacy rule), which the staffing policy requires any evaluation basis to reproduce exactly |
| Driving force | The new rule may replace operators only in a configuration that catches 85% of lane closures within 15 minutes, on a basis that reproduces the department's published figures. Once every closure is counted, the closure counts reproduce, and the detected counts still do not: an alert within a mile of a closure is not a detection of it. The department credits an alert only when its station sits inside the closure's queue at that minute, the contiguous run of stations behind the closure on its own carriageway running below 70% of profile. Downstream merges and the opposite carriageway raise alerts near a closure for reasons of their own. On the queue basis the quiet configurations fail the gate, the centre must adopt the noisiest configuration, and the freed hours fall to 51. |

## 1. Situation

A traffic management centre pages operators whenever a station on its 31-mile corridor drops below 35 mph: 18,000 pages a year, one
operator-hour per four pages. A profile-based rule (speed against the station's own time-of-week profile, confirmed at neighbouring
stations, held for several five-minute bins) comes in four configurations, from the quietest (mainline confirmation, four bins: 3,600
alerts) to the noisiest (connector stations included, two bins: 7,300). The staffing policy lets the centre adopt the quietest configuration
that catches at least 85% of lane-closure incidents within 15 minutes, on an evaluation basis that reproduces every one of the department's
published detection figures. The centre holds a year of station data, the station inventory, the police incident log, its sign-message log,
the landmark and interchange tables and the published figures. The operations chief is sure the quietest version will do.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: station speeds, alerts, the incident log as the police recorded it, the sign log and the published
  figures. Nobody's numbers are overturned; the difficulty is which alerts count as detecting a closure, which no record states.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the chief's view and the legacy alert file. A replay on every closure, with any alert within a mile and 15
  minutes credited, still adopts the three-bin connector configuration and frees 60 hours.
* **Instrument repair.** Suspect file: the police incident log, whose lane field is blank for 31% of closures and whose location is only a
  landmark code for 22% of incidents. Repaired so every incident carries its postmile and lane, rung 0 on the full population adopts the
  three-bin mainline configuration (66 hours), rung 1 adds hygiene and adopts the three-bin connector (60 hours), rung 2 returns the same
  60, and the queue credit is still needed: a complete log reproduces the closure counts, never the detected counts.
* **Lens swap.** The naive detection is any alert near a closure in space and time; the answer's is an alert from inside the closure's
  queue, a different set of alert-closure pairs that moves the adopted configuration.

## 3. The driving force

A strong solver replays each configuration with profiles built only from prior same weekdays, drops samples below 50% observed as the memo
requires, reads lane closures off the sign log (every closure gets a message within ten minutes, a third have a blank lane field), resolves
landmark-only incidents through the interchange table, and checks the basis against the published figures: the closure counts now
reproduce in all 16 cells. It credits an alert within a mile and 15 minutes as a detection and adopts the three-bin connector configuration
at 87%. Every step is correct, and the detected counts miss in 11 of 16 cells, all of them high. Near merges and interchanges, recurring
congestion downstream and on the opposite carriageway raises alerts within a mile of a closure that have nothing to do with it. The
department's figures reproduce only when an alert is credited from a station inside the closure's queue: the contiguous run of stations
upstream on the closure's carriageway that sit below 70% of profile at the alert's minute. On that basis only the connector two-bin
configuration clears 85%.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Lane field as recorded, postmile-located incidents, all samples kept, any alert within a mile and 15 minutes credited: the quietest configuration passes (89%) | 69 hours, +35% | A clean replay of the memo's rule against the police log | The memo's data-quality clause: samples under 50% observed are dropped, and without them the quietest configuration catches 84% |
| 1 | Hygiene applied: the four-bin mainline configuration fails, three-bin mainline passes (86%) | 66 hours, +29% | The rule as written on clean data | The sign log: every lane closure gets a message within ten minutes, and a third of closures have a blank lane field |
| 2 | Every closure counted (lane closures from the sign log, landmark-only incidents resolved through the interchange table), the one-mile credit kept: three-bin mainline fails (83%), three-bin connector passes (87%) | 60 hours, +18% | The closure counts reproduce in all 16 published cells | The published detected counts: this basis credits 118 and 127 detections against the department's 104 and 112, high in 11 of 16 cells |
| 3 | **Decisive:** credit an alert only from a station inside the closure's queue at that minute (contiguous upstream stations on its carriageway below 70% of profile): only connector two-bin passes (86%) | **51 hours** | — | — |

* **Figure shape.** The answer is the minimum cell of the grid; every rung and partial reading frees more hours than the corridor can safely
  give up, and each is wrong in the same direction.
* **Partial correction priced (L3).** A solver who credits only upstream alerts on the closure's carriageway within a fixed window
  reproduces at most 11 of the 16 detected counts; at the best window (1.5 miles) the three-bin connector configuration passes at 85.2% and
  frees 60 hours: rung 2's figure, 18% above the answer and no nearer it.
* **Grid.** Hygiene (off or on) × population (as recorded or every closure) × credit (one-mile window, fixed upstream window, queue) = 12
  cells, running 69, 66, 66, 60, 66, 60, 60, 60, 60, 60, 60 and 51. The nearest wrong cell is 60, 18% above the answer, and only hygiene,
  every closure and the queue credit together reach 51.
* **Configuration table.** On the reproducing basis recall runs 78%, 80%, 83% and 86% from quietest to noisiest, so the gate selects exactly
  one configuration, 7,300 alerts against the legacy 18,000: (18,000 − 7,300) ÷ 4 ÷ 52 = 51.4.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The department's methodology note says a closure is detected when the legacy system "alerted for it within 15
   minutes"; no document says which alerts the department attributed to which closure or mentions a queue.
2. **The corpus pins a construction, not a menu (Pattern B).** The queue credit reproduces all 32 published numbers (16 closure counts, 16
   detected counts). The one-mile window reproduces the closure counts and 5 detected counts; a fixed upstream window of any length from 0.5
   to 3 miles reproduces at most 11. Every rival credits alerts the department did not, so each overshoots both annual detected totals. The
   queue is a construction behind a join (closure to station inventory to each station's speed against profile at the alert's minute), not
   a window to sweep.
3. **No arithmetic symptom.** Alerts and closures match cleanly under every window, and the one-mile basis reconciles to the closure counts
   exactly.
4. **Not a row predicate.** Each closure's queue needs the inventory's station order and carriageway, every station's speed against its
   profile minute by minute, and the contiguous slow run upstream at the alert's minute.
5. **The enumeration is arithmetic.** Which alerts the department credited is computed; no column marks an alert as a detection.
6. **No cutover date.** The department credited detections the same way in both published years; nothing steps.
7. **Survives deletion.** Remove the chief's view and the legacy alert file, and the one-mile replay on every closure is still the natural
   build.

## 6. The calibration corpus

* **Form.** The department's published lane-closure figures for the corridor: closures, and closures detected within 15 minutes by the
  legacy rule, for eight segments in 2023 and 2024, with the staffing policy's clause that an evaluation basis must reproduce every number.
* **What it pins.** The closure population, through the closure counts (rungs 1 and 2), and the queue credit, through the detected counts.
  The sign-log marker is absolute: every incident with a recorded closure has a message, and no incident recorded as non-blocking has one.
* **Twin pair.** Segments 3 and 6 had 18 closures each in 2024, identical alert volumes and 15 one-mile detections each. The department
  published 14 detections for segment 3 and 7 for segment 6, 2.0× apart, because segment 6 lies below the Harbor merge, where recurring
  downstream congestion raises alerts outside any closure's queue; only the queue construction separates them.
* **Resemblance points at the decoy.** The corridor's 2025 incident profile matches 2023's on every visible column, so a lookup carries
  2023's published detection rate forward.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The staffing policy: the quietest configuration that catches 85% of lane-closure incidents within 15 minutes may be
  adopted, on an evaluation basis that reproduces every published figure; one operator-hour per four alerts. The memo's data-quality
  clause. The station inventory as the record of station order and carriageway. One sentence each.
* **Empirical pins.** Lane closures from the sign log and the queue credit, both through reproduction.
* **Voices.** The operations chief: "The quietest version will do; our corridor is not complicated." The roster manager: "Every page we drop
  is an operator back on the floor."
* **Licensed wrong basis.** The policy records that the operators' union evaluates rules on postmile-located incidents with any alert
  within a mile credited and will present that evaluation at the roster consultation.

## 8. Determinism by construction

* **Queue threshold.** Around every closure, stations sit below 60% or above 80% of profile, so any threshold between them builds the same
  queue.
* **Match window.** No closure has an alert between 14 and 16 minutes after it, so 15-minute matching is not a fork.
* **Profiles.** Built from the prior eight same weekdays with holidays skipped, as the memo states; six- and ten-week profiles adopt the
  same configuration.
* **Rounding.** 51.4 hours rounds to 51 under any convention.

## 9. Prompt sketch and deliverables

> Next year's roster has to say how many operator hours a week come off alert duty if the new incident rule goes in, and it can only go in
> if it keeps catching the lane closures. The operations chief is sure the quietest version will do. Give me the number of hours, to the
> nearest hour, for the roster, and send `rule_replay.xlsx`, a chart `recall_by_configuration.png`, and a one-page `roster_note.pdf`.

* `rule_replay.xlsx` — the replay by configuration on each evaluation basis with its published-number reproduction count (ask C), the patrol
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
* **Ask C (validity).** For each of the four evaluation bases: published numbers reproduced, the adopted configuration and the freed hours.
* **Decoupling.** Clearing the queue credit, the sign-log attribution and landmark resolution changes no figure in asks A or B.

## 11. Rubric arithmetic

8 segments × 2 (ask A) + 8 × 2 (ask B) + 4 bases × 3 (ask C) + the committed hours, the adopted configuration, its recall and the recall of
the configuration ruled out + 5 named chart parts + 3 files ≈ 56 criteria.

## 12. World-building constraints

* Configurations: 3,600 / 4,200 / 5,600 / 7,300 alerts; legacy 18,000. Rung figures 69 / 66 / 60 / 51 hours.
* 22% of incidents carry only a landmark; 31% of closures have a blank lane field; every closure has a sign message within ten minutes.
* Published closures 131 (2023) and 140 (2024), detected 104 and 112; the one-mile window credits 118 and 127; the queue credit matches all
  32 published numbers.
* Segments 3 and 6 are identical on every incident, alert and one-mile-detection column.
* Patrol logs and count stations never touch station speeds, alerts, the incident log, the sign log or the station inventory.
