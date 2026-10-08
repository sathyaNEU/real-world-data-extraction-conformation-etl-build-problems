# OS24 — What flexibility to bid into the winter peak tender, when last winter's kW per charging session carried each hub's building load and the hubs have doubled their bays

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · electricity flexibility markets |
| Mirrors | Bidding capacity from a per-unit performance ratio measured when each site's fixed contribution was spread over fewer units (demand-response aggregators such as Octopus, Kraken and Voltus bidding kW per enrolled device, Google and Microsoft quoting per-server power savings that include a hall's fixed cooling, Amazon per-parcel rates that carry a station's fixed costs) |
| Decision shape | One figure committed at a date: the availability bid in the distribution operator's winter tender, due 1 October |
| Committed call | The kW of import reduction guaranteed on winter weekdays from 16:00 to 19:00, rounded down to 10 kW |
| Gap · Pattern | Gap 1 (time) over Gap 2 (population) · S6, a correct share carried onto a different book (kW per session, which includes every hub's fixed building shed, carried onto hubs with twice the bays), with a suppressed district count bounded from a published percentage (#24) below it |
| Gate G mechanism | decomposition_attribution, with forecasting |
| Measured traps engaged | #7 uses the ready-made measure · #24 treats an unpublished figure as unknown · #13 validates on one population, applies to another |
| Calibration form | Retry or revision log: the hub controller's log of last winter's 24 trial events, every revision and retry of each hub's import target with the hub meter's half-hourly import |
| Driving force | Last winter's trial credited the operator with 6.5 kW per deferrable session: each hub cut 52 kW with its 8 bays full. But 20 kW of every cut was the hub's building load, canopy heaters and the café, which the controller sheds whatever the bays hold; sessions shed 4.0 kW each. The hubs now have 16 bays, so the ratio carried onto the denser book counts the building load again for every extra session. The split exists only by joining the hubs to the equipment register, and every trial event ran at 8 sessions a hub, so the ratio fits them all. |

## 1. Situation

A charge-point operator runs 40 hubs in the distribution network operator's winter tender zone, 24 of them in district K. By 1 October
it must bid the kW of import reduction it guarantees on weekdays from 16:00 to 19:00, rounded down to 10 kW, with a penalty for every kW
it fails to deliver. Last winter it ran 24 trial events, and the operator's trial report credits it with 6.5 kW per deferrable session.
This summer every hub was extended from 8 to 16 bays. The pack holds the controller's revision log, the session records, the hubs'
equipment register, and the government's tables of licensed plug-in cars by district. The commercial director wants the bid set from the
new bays.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the trial report's 6.5 kW, the revision log, the meters, the equipment register and the vehicle
  tables. The ratio really is what each session averaged last winter. No stakeholder read is overturned. The difficulty is that the ratio
  belongs to hubs with 8 sessions, and part of it does not grow with sessions.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the director's view. The trial's ratio, the forecast rule and the bounded district count still give a clean
  3,068 kW that fits every trial event.
* **Instrument repair.** The suspect file is the vehicle count table, which suppresses district K's count. Publish it (966 cars): rung 0
  still bids every bay at 4,480 kW, rung 1 collapses onto rung 2 at 3,068 kW, and the building load still has to be split out of the
  ratio. The revision log, the meters and the register are complete, and the log's hub targets are correct for what they record.
* **Lens swap.** The naive read scales a per-session ratio. The answer rebuilds each hub's cut from a fixed part and a per-session part,
  a different quantity on a different book.

## 3. The driving force

A strong solver drops the bays-times-charger bid, because the trial shows what a hub actually cuts. It takes the trial's 6.5 kW per
deferrable session and the operator's forecast rule: next winter's sessions at a hub are last winter's 8 times its district's growth in
plug-in cars, in whole sessions, up to its bays. District K's count is suppressed, so it bounds it from the published share of licensed
cars (2.1% of 46,000) rather than filling it at the county's growth, and K's hubs get 9 sessions while the rest fill their 16 bays. That
gives 3,068 kW, and the ratio fits all 24 events. But each hub's 52 kW was 20 kW of building load, which the controller sheds in every
event, plus 4.0 kW from each of 8 sessions. Doubling the bays doubles the sessions, not the building load. Rebuilt hub by hub, the zone can
cut 2,688 kW.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Every forward bay at the 7 kW charger rating | 4,480 kW (+67%) | The commercial team's capacity view, on the new bays | The trial report: hubs with 8 full bays cut 52 kW, 6.5 kW per deferrable session, not 7 kW a bay |
| 1 | The trial's 6.5 kW × forward sessions, K's suppressed count filled at the county's growth (13 sessions at K's hubs) | 3,692 kW (+37%) | The operator's own measured ratio on its own forecast rule | The percentage table: K's plug-in cars are 2.1% of 46,000 licensed, 943 to 989, growth 1.18 to 1.24 |
| 2 | The same with K's count bounded from the percentage table (9 sessions at K's hubs) | 3,068 kW (+14%) | Every input published or measured, and the ratio fits all 24 trial events | The equipment register: every hub sheds a 20 kW building load in events, whatever its sessions |
| 3 | **Decisive:** each hub's forward cut as its 20 kW building shed plus 4.0 kW per forward session | **2,680 kW (2,688 kW rounded down)** | — | — |

* **Figure shape.** Every correction walks the figure down and the answer is the minimum cell; the decisive move removes 12% of the rung-2
  figure.
* **Partial correction priced (L3).** A solver who splits the building load out but fills K at the county's growth lands at 3,072 kW (+14%).
  One who splits it out but keeps last winter's 8 sessions everywhere bids 2,080 kW (−23%), under-using the new bays. One who scales the
  building load with the bays as well lands at 3,488 kW (+30%).
* **Grid.** K's count (filled, bounded) × hub cut (per-session ratio, building plus sessions) gives 4 cells: 3,692, 3,072, 3,068 and the
  answer. The nearest wrong cell is 3,068 kW (+14%), and it carries the ratio forward unsplit.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The trial report states kW per deferrable session; the equipment register lists each hub's sheddable building
   load. No document says the ratio contains the building load, or that it will not grow with bays.
2. **Corpus blind for a computable reason.** *In every logged event every hub held 8 deferrable sessions at the peak, because its 8 bays
   were full, so the cut per session was 6.5 kW in every event and hub and the building share never varied.* The ratio reproduces all
   24 events at all 46 trial hubs.
3. **No arithmetic symptom.** Hub cuts reconcile to the meters, 6.5 kW per session sits under the 7 kW charger rating, and the ratio times
   sessions gives every event's total.
4. **Not a row predicate.** The answer needs each hub joined to the register for its building load, the per-session shed derived from the
   remainder, and each hub's forward cut rebuilt from its forward sessions.
5. **The enumeration is arithmetic.** No column splits a hub's cut into building and sessions; the log records hub targets only.
6. **No cutover date.** The trial ran at constant density, and the forward book is a forecast, not a step in any series the trial used.
7. **Survives deletion.** Removing the director's view leaves the trial ratio certifying rung 2.

## 6. The calibration corpus

* **Form.** The revision log: 24 trial events at 46 hubs (the zone's 40 and six outside it), every revision and retry of each hub's
  import target, and the hub meter's half-hourly import.
* **What it certifies.** Each hub cut 52 kW in every event with 8 deferrable sessions, the 6.5 kW ratio, 24 of 24 events within 1%; a
  constant 7 kW per bay misses every one.
* **What it is blind to.** The split between building and sessions (above).
* **Twin pair.** Trial hubs H07 and H19, outside the zone, are identical on every log column: 8 sessions and 52 kW in every event. H07
  sheds a 28 kW building load and its sessions 3 kW each; H19 sheds 4 kW and its sessions 6 kW each. Eight more sessions add 24 kW at H07
  and 48 kW at H19, 2.0× apart. Only the equipment register separates them.
* **Resemblance points at the decoy.** The extended hubs most resemble the trial's best performers, which delivered their ratio in every
  event.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The tender terms: availability bid in kW of import reduction, weekdays 16:00–19:00, December to February, rounded down
  to 10 kW, with a penalty for every kW not delivered. The operator's forecast rule: next winter's deferrable sessions at a hub are last
  winter's 8 times its district's growth in licensed plug-in cars, in whole sessions, up to its bays. The equipment register: each zone
  hub's sheddable building load, 20 kW. The bay plan: 16 bays at every hub.
* **Empirical pins.** The ratio and the per-session shed, from the revision log and the register. District growth, from the vehicle
  tables.
* **Voices.** The commercial director: "We've doubled the bays. Bid the bays." The trial lead: "Our ratio held in every event. It's the
  best number we have."
* **Licensed wrong basis.** The tender terms record that the operator's prequalification is checked against its trial ratio times its
  forecast sessions, and the DNO will present that check.

## 8. Determinism by construction

* **Density.** Every hub held exactly 8 deferrable sessions in every trial event, and the building shed ran in every event.
* **Shed.** Every zone hub sheds 20 kW of building load and 4.0 kW per session (each session drops from 7.0 to 3.0 kW).
* **Bound.** K's count of 943 to 989 against last year's 800 gives growth of 1.18 to 1.24, and 9 whole sessions anywhere in it; the rest
  of the zone grows 2.0 and fills its 16 bays.
* **Window.** Every trial event ran in the 16:00–19:00 window on a weekday, the tender's own window.
* **Rounding.** 24 × 56 + 16 × 84 = 2,688 kW, which rounds down to 2,680.

## 9. Prompt sketch and deliverables

> Our winter peak tender bid goes to the network operator on 1 October and I need the kW we can guarantee on weekdays from 16:00 to
> 19:00, rounded down to 10 kW, because every kW we miss is penalised. Our commercial director wants it set from the new bays. Give me
> the bid as a sentence for the submission, with `flex_bid.xlsx`, a chart `hub_cut_split.png`, and a short `bid_memo.docx`.

* `flex_bid.xlsx` — each hub's forward sessions and cut on the four bases, the building and session split, K's bound, the fault sheet
  (ask A) and the payment sheet (ask B).
* `hub_cut_split.png` — a script-rendered stacked bar chart: for K's hubs and the rest, last winter's and next winter's cut split into
  building load and sessions, the per-session ratio's forecast drawn as an outline over each forward bar, and the bid labelled.
* `bid_memo.docx` — the committed bid and the bridge from the bays-times-charger figure.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the six largest hubs, last winter's share of sessions ending in a charger fault and
  the median minutes to the next successful session on that charger. *Device:* a session retried after a fault is logged as a new session
  carrying `retry_of`, and the operations guide counts the original attempt once. Counting retries as sessions understates the fault share
  at the three hubs with most retries.
* **Ask B (device-carried).** For each of the six, the share of sessions paid by app, by card and on fleet accounts. *Device:* a fleet
  session appears in the session file and again as a fleet invoice line carrying its session ID, and the payments guide counts it once.
  Counting both inflates the fleet share at four hubs.
* **Ask C (validity).** The bid under each of the four rung bases, K's bound, and trial events reproduced (of 24) by the per-bay rating,
  the per-session ratio and the building-plus-sessions split.
* **Decoupling.** Carrying the ratio forward unsplit changes no figure in asks A or B. Session faults and payment records touch neither the
  revision log, the register nor the vehicle tables.

## 11. Rubric arithmetic

6 hubs × 2 (ask A) + 6 hubs × 3 payment shares (ask B) + 4 bases, the bound and 3 reproduction counts (ask C) + the committed bid, K's and
the rest's forward cuts per hub, the building load and the per-session shed + 5 named chart parts + 3 files ≈ 51 criteria.

## 12. World-building constraints

* 40 zone hubs (24 in K), 16 bays each; last winter 8 bays and 8 deferrable sessions a hub, cut 52 kW = 20 kW building + 8 × 4.0 kW.
* K: 800 plug-in cars last year, count now suppressed, 2.1% of 46,000 licensed (943–989); county growth 1.7; rest of the zone 2.0.
* Rung figures 4,480 / 3,692 / 3,068 / 2,688 kW; partial readings 3,072 and 2,080 kW.
* H07 and H19 match on every revision-log column.
* Session faults and payment records never touch the log, the register or the vehicle tables.
