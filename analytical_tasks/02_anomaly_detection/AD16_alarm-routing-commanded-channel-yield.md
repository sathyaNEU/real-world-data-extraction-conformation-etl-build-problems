# AD16 — Which alarms the operations board routes to the paid engineering contractor, when every alarm on a commanded channel has turned out to be the command

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Product Analytics · spacecraft telemetry operations and observability |
| Mirrors | Routing alerts to a paid escalation tier when alert yield depends on whether the signal was commanded (deploy-triggered alerts in cloud SRE teams, change-induced alarms in AIOps at Google and AWS, fleet telemetry after over-the-air pushes at Apple) |
| Decision shape | A structure the body adopts: the alarm-routing rule (detector, channel classes, which classes escalate), judged by confirmed faults escalated within the contractor's hours |
| Committed call | The routing structure the operations board adopts on 4 November 2026, and the confirmed faults per quarter it should deliver |
| Gap · Pattern | Gap 2 (population) over Gap 3 (objective) · conditioned yield (E05): absolute on a constructed channel property, the ledger's mix inverted against the decision set, with a binding hours limit at the lower rung (E14) |
| Gate G mechanism | decomposition_attribution, with binding_constraint support |
| Measured traps engaged | #13 validates on one population, applies to another · #10 notes a binding limit as a risk · #5 takes the population a flag or filter suggests |
| Calibration form | Settled-transaction ledger: the engineering contractor's 1,240 settled tickets over four quarters, each with its disposition and billed hours |
| Driving force | A channel whose values the spacecraft sets by command steps whenever a command lands, and every detector reads the step as an anomaly. Across the settled ledger, 0 of 412 tickets on such channels found a fault and 486 of 828 on free-running channels did. The ledger's pooled 39% is correct and applies to no channel. Which channels are commanded is not a column: it is the share of a channel's value changes that follow a command to its subsystem within two minutes, built from the command log, and the decision set is mostly commanded where the ledger was mostly not. |

## 1. Situation

A satellite operator's flight team receives alarms from anomaly detectors on 82 telemetry channels. Alarms either escalate to an engineering
support contractor, who bills hours on each ticket, or go to an automated log. Next quarter's routing goes to the operations board on 4
November. The operations standard judges a routing by the confirmed faults it escalates, counts detection at event level, and says
escalations must fit within the contract's 1,200 billed hours a quarter. The pack carries the channels' telemetry, the three detectors'
alarms, the command log, the channel dictionary, the vendor's benchmark deck (labelled as point-adjusted results on a public benchmark),
the contract register and the contractor's settled ledger.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the telemetry, the alarms, every command, the dictionary, the deck's benchmark numbers and every
  settled ticket. The vendor's combined detector does score best on its benchmark. Nothing reported is overturned; the difficulty is that
  the yield of an escalated alarm depends on a property of its channel that no file names.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the vendor's deck and the board chair's view. The ledger still gives a pooled 39% and detector yields that favour
  D1, and every structure built on them over-forecasts.
* **Instrument repair.** Give every detector perfect precision on the benchmark; they would still alarm on commanded steps, because a step
  is a real change in the signal. A better detector does not know the step was ordered.
* **Lens swap.** The ledger's population is mostly free-running channels under the old routing; the decision set is all 82 channels, 62%
  commanded. The answer applies yields to a different population of alarms, split by a property, not the same alarms re-weighted.

## 3. The driving force

A strong solver discounts the deck's point-adjusted F1, scores detectors at event level as the standard says, sees that escalating
everything breaks the hours cap, and fills the cap with the alarms the ledger says pay best, by detector or by subsystem. Each step is
competent and each forecast is too high. The ledger was written under the old routing, which escalated only thermal and power channels,
mostly free-running. In it, D1's tickets confirmed 51% and D2's 36%, a cross-section that favours D1, because D2 fires on step changes and so
drew more commanded channels. Conditioned on the property, the detectors are equal: 0% on commanded channels, 58.7% on free-running ones,
whichever detector raised the alarm. The property is behavioural: a channel is commanded when nearly all its value changes follow a
command to its subsystem within two minutes, which needs the command log joined in time and aggregated per channel. Commanded channels
sit in every subsystem, so no subsystem routing captures them. Routing the combined detector's alarms on free-running channels and logging
the rest escalates 330 alarms a quarter, 495 hours, 194 confirmed faults.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The deck's best detector (combined, D3) on all channels, every alarm escalated, forecast at the ledger's pooled 39% | Escalate all D3: 368 confirmed forecast | The benchmark winner, the ledger's own yield, the cap noted as a risk | The contract register: 940 escalations bill 1,410 hours against a 1,200-hour cap the standard says must hold |
| 1 | D3 on all channels, trimmed to the cap by dropping the subsystem with the lowest ledger yield (payload) | Escalate D3 less payload: 330 forecast | The cap applied in the structure, the ledger's subsystem yields used | The operations standard counts detection at event level, and D3's lead exists only point-adjusted; at event level D1 is best and leads the ledger at 51% |
| 2 | D1 on all channels, forecast at D1's ledger yield | Escalate all D1: 286 forecast | Event-level best, the ledger's best detector, within the cap | The ledger joined to the command log: every ticket on a commanded channel closed with no fault (0 of 412), whichever detector raised it |
| 3 | **Decisive:** channels split by the share of value changes following a command within two minutes; D3 alarms on free-running channels escalate, commanded channels' alarms go to the log | **Escalate D3 on free-running channels: 194 confirmed, 495 hours** | — | — |

* **Figure shape.** Every rung over-forecasts because it applies a mixture's yield to commanded alarms; the answer's forecast is the minimum.
  Per-rung offsets are +89.7%, +70.1% and +47.4%.
* **Partial correction priced (L3).** A solver who conditions on the dictionary's "commandable" flag (a channel with a command mnemonic)
  instead of observed behaviour routes only 18 channels and delivers 157 (−19.1%), because 13 free-running channels carry a mnemonic that is
  never used. A solver who conditions correctly but keeps D1 delivers 123 (−36.6%).
* **Grid.** Detector (D1, D2, D3) × class (none, subsystem, dictionary flag, observed behaviour) gives twelve structures. Every unconditioned
  or subsystem-conditioned structure over-forecasts by at least 47% or breaches the cap; dictionary-flag structures under-deliver by at
  least 19%. Only D3 on observed free-running channels delivers 194 within the cap.
* **What true yields say.** At the conditioned yields, the rungs' structures actually deliver 194 (but breach the cap), 182, 123 and 194:
  only the decisive structure is both feasible and best.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The standard, the deck and the contract say nothing about commands. The dictionary's flag says which channels can
   be commanded, not which are.
2. **The corpus pins a construction, not a menu.** Conditioned on observed behaviour the ledger splits absolutely, 0 of 412 against 486 of
   828, in every quarter and for every detector; the pooled 39%, the detector yields and the subsystem yields each fail on at least two
   quarters by more than 15 points, all in the same direction. The property is a construction: a time join to the command log, a count per
   channel and a ratio, with no column holding it.
3. **No arithmetic symptom.** Tickets tie to alarms, hours to the contract, alarms to telemetry; the pooled yield is exactly right for the
   ledger.
4. **Not a row predicate.** Whether a channel is commanded is a share over all its value changes, so it is a group property built by joining
   two time series.
5. **The enumeration is arithmetic.** Commanded channels follow commands in at least 92% of changes and free-running ones in at most 6%, so
   every cut between them, and every window from one to five minutes, draws the same 51 commanded channels.
6. **No cutover date.** Command plans run continuously; no series steps.
7. **Survives deletion.** With every voice and the deck removed, the answer and the difficulty are unchanged.

## 6. The calibration corpus

* **Form.** The contractor's settled ledger: 1,240 tickets over four quarters under the old routing, each with its alarm, channel, detector,
  disposition and billed hours.
* **What it pins.** The absolute split above; mean billed hours of 1.5 a ticket in both classes; and the mix: 67% of the ledger's tickets
  sit on free-running channels against 35% of next quarter's alarms.
* **Twin pair.** Ledger quarters Q2 and Q4 are identical on tickets by subsystem and detector (310 each) and on hours billed. Q2 confirmed 211
  faults and Q4 104 (2.03×), because 51% of Q4's tickets came from commanded channels during a payload campaign; only the constructed
  property separates them.
* **Every rule exercised.** Thirteen free-running channels carry an unused command mnemonic, so the dictionary flag is tested; one channel
  changed from free-running to commanded at a mode change and is classed on the latest quarter's behaviour.
* **Resemblance points at the decoy.** By subsystem and detector mix, next quarter's alarms most resemble ledger Q2, the best quarter.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The operations standard: a routing is judged by the confirmed faults it escalates; detection is counted at event level,
  alarms within ten timesteps forming one event; escalations must fit within the contract's billed hours. The contract register: 1,200
  hours a quarter.
* **Empirical pins.** The behavioural split and the class yields, from the ledger joined to the command log.
* **Voices.** The board chair: "The vendor's benchmark is the industry reference; I'd use its winner." The flight director: "Thermal and
  power have always been where our real faults are."
* **Licensed wrong basis.** The standard records that the contractor plans its staffing on the ledger's pooled yield and will review the
  routing on that basis.

## 8. Determinism by construction

* **Split.** The empty band between 6% and 92% makes the cut and the window immaterial.
* **Volumes.** Each detector's alarm volume per channel is stable across the last four quarters, so next quarter's volumes carry forward
  without a trend convention.
* **Hours.** Tickets bill in half-hour blocks with a mean of 1.5 hours in both classes and every quarter.
* **Events.** The standard's ten-timestep grouping is filed; no two events on a channel fall within twenty timesteps.

## 9. Prompt sketch and deliverables

> Next quarter's alarm routing goes to the operations board on 4 November: which alarms escalate to the engineering contractor and which go
> to the automated log. The vendor's deck says its combined detector scores best. Tell me the routing we adopt and the confirmed faults a
> quarter it should deliver, in two sentences for the board, with `routing_structure.xlsx` holding the sheets below, the chart
> `yield_by_class.png`, and `board_minute.docx`.

* `routing_structure.xlsx` — the channel classification and the routing build, the dropout sheet (ask A), the pass-booking sheet (ask B)
  and the structure table (ask C).
* `yield_by_class.png` — ledger yield by detector, by subsystem and by observed class as three panels, the 0-of-412 and 486-of-828 split
  annotated, next quarter's alarm mix against the ledger's as paired bars, and the 1,200-hour cap marked on an hours axis.
* `board_minute.docx` — the adopted structure, its confirmed faults and hours, and why the deck's winner and the subsystem routing are not it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the five subsystems, telemetry dropout minutes in each month of the last quarter.
  *Device:* gaps during planned ground-station handovers are listed in the pass schedule as handover gaps and are not dropouts, per the
  ground segment guide. Counting every gap overstates dropouts in the two subsystems downlinked on the busiest passes. The routing build
  never reads dropouts.
* **Ask B (device-carried).** For each of the three ground stations, pass hours booked and used in each month of the last quarter.
  *Device:* a pass booked across midnight UTC is recorded on its booking date with its full length, per the booking system's notes.
  Splitting it by calendar day misplaces hours in every month-end.
* **Ask C (validity).** For each of the four rung structures, its confirmed faults at the conditioned yields, its billed hours, and whether
  it fits the cap.
* **Decoupling.** Clearing the channel classification changes no figure in asks A or B.

## 11. Rubric arithmetic

5 subsystems × 3 months (ask A) + 3 stations × 3 months (ask B) + 4 structures × 3 (ask C) + the structure's detector, classes and routing,
its confirmed faults and its hours + 5 named chart parts + 3 files ≈ 49 criteria.

## 12. World-building constraints

* Next quarter's alarms: D1 560 (210 free-running), D2 590 (190), D3 940 (330); 51 of 82 channels commanded.
* Yields: commanded 0 of 412 ledger tickets, free-running 486 of 828 (58.7%), equal across detectors; pooled 39.2%.
* Commanded channels follow commands in at least 92% of value changes, free-running ones in at most 6%.
* Rung forecasts: 368 / 330 / 286 / 194; hours 1,410 / 1,185 / 840 / 495 against a 1,200 cap.
* Ledger Q2 and Q4 are identical on tickets by subsystem and detector; 13 free-running channels carry unused mnemonics.
* Handover gaps and midnight-spanning passes never touch alarms, tickets or the command log.
