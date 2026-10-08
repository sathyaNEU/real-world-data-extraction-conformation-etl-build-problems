# RC41 — Which cause of the 30% fall in Panama liftings the network plan answers, when the missing cargo still sends its empty boxes home

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Supply Chain & Logistics · ocean container network planning |
| Mirrors | Telling a capacity constraint from lost demand at container lines and marketplaces (Maersk and MSC network planning in the Panama drought, Amazon inbound routing when a port congests, API traffic that drops under rate limits), where volume that leaves one channel keeps flowing through another the planner's records do not follow |
| Decision shape | Which of N root causes gets the fix: one response in next year's network, each of five aimed at one cause of the lost liftings |
| Committed call | Fund the West Coast carrier-haulage product: 240k of the year's 450k TEU of lost Panama liftings is East Coast cargo that moved to the West Coast and the shippers' own rail, 3.2 times the next cause |
| Gap · Pattern | Gap 2 (population) at the decisive rung, Gap 3 (objective) at rung 2 · S2 (the moved cargo is a residual between the line's East Coast discharges and its East Coast depot returns), with the mixed segment of measured #6 at rung 2 (the East Coast import index split by origin through the bill-of-lading port of lading) |
| Gate G mechanism | decomposition_attribution, with binding_constraint |
| Measured traps engaged | #7 uses the ready-made measure · #13 validates on one population, applies to another · #6 treats a mixed segment all one way |
| Calibration form | Change log: the canal authority's advisory change log over twelve years, eleven restriction episodes, each with the line's liftings, blank sailings, East Coast discharges and East Coast depot returns before and after |
| Driving force | Every number is correct: the liftings, blank sailings, delay cancellations, both import indices, the discharges and the depot returns. The capacity reading books the unexplained fall to the canal, and the vessel register moves most of it to draft. Measured on the trade itself, Asia-origin East Coast imports fell 16%, which the change log certifies as demand, and that explains the rest. But the index falls whenever East Coast cargo is unladen on the West Coast. Under merchant haulage the line's custody ends at the West Coast port, yet the empty boxes still come home to its East Coast depots. Returns of the line's own boxes exceeded its own East Coast discharges by 240k TEU, cargo that appears in neither the Panama liftings nor the East Coast discharges, and true demand fell 40k. |

## 1. Situation

Corvina Line runs five Asia–US East Coast services through the Panama Canal. In the drought year its own Panama liftings fell from 1.50M
to 1.05M TEU, a 30% fall. The network committee funds one response for next year's network, each aimed at one cause: cutting a service
(demand), joining the canal's long-term slot programme (slot caps), swapping in shallower-draft ships (draft limits), schedule buffers and
priority booking (delay cancellations), or a carrier-haulage product through the West Coast with rail to the East Coast (cargo moved to the
West Coast). The charter funds the response aimed at the cause behind the largest part of the lost liftings. Commercial wants to cut a
service, and operations blames the canal.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct: the line's liftings, the blank-sailing log, the delay cancellations, both import indices, the
  East Coast discharges, the depot returns and the change log. Commercial is right that East Coast imports from Asia fell, and operations is
  right that the canal capped sailings. No one's reading of their own figures is overturned. The difficulty is where the missing cargo went.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete commercial's view and every voice. The capacity reading still books 370k TEU to slot caps, and the trade index
  still books 240k to demand.
* **Instrument repair.** Suspect: the blank-sailing log gives every blank the reason "canal restriction", coarser than slot or draft. Repair:
  the true reason on every blank. Rung 0 still names slot caps (310 once the draft blanks leave it), rung 1 draft (213) and rung 2 demand
  (240); none names the West Coast shift. The bills of lading are not suspect: under merchant haulage their place of delivery and consignee
  are the West Coast port and the shipper's forwarder, correctly. The moved cargo is a residual between the East Coast discharges and the
  East Coast depot returns, which no row records, so the residual is still needed.
* **Lens swap.** The naive reading sets the canal's capacity against the Panama liftings. The answer finds a population of East Coast cargo
  that left the Panama services but not the line, seen only in its empty boxes.

## 3. The driving force

A strong solver reads the fall as censored demand. It bounds demand with the East Coast import index and books the rest to the canal, then
splits the canal's share by lock set through the vessel register, because the Neopanamax locks were draft-limited and only the Panamax
locks were slot-capped. Then it does what a trade economist would do and measures demand on the trade itself: East Coast imports laden in
Asia, split out of the customs records through each bill's port of lading. They fell 16%, which explains almost all of the remainder, and
the change log certifies that index as demand in every past episode. Commercial looks right. But that index counts cargo where it is
unladen, and East Coast cargo unladen in Los Angeles is not in it. Under merchant haulage the line's custody ends at the discharge port, and
the merchant returns the empty to a depot in the consignee's region. The line's own boxes came back to its East Coast depots 240k TEU more
than its own East Coast discharges, its carrier-haulage moves and its sea repositioning can explain. That cargo still exists and is still on
Corvina ships. The shippers moved it to the West Coast and their own rail.

## 4. The ladder

| Rung | Construction | Names (lost liftings, thousand TEU) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Censoring: demand bounded by the East Coast import index (−3%), delay cancellations counted, everything else the canal's slot caps | Slot caps (370 against demand 45) | The demand-or-capacity test the question asks for, with the binding days visible | The vessel register and the advisories: the Neopanamax locks were never slot-capped, only draft-limited, and most of the line's TEU sails on Neopanamax ships |
| 1 | The canal's share split by lock set through the vessel register | Draft limits (213 against slot caps 157) | Every blank and every capacity TEU sits on the lock it used | The customs records: East Coast imports laden in Asia fell 16%, not 3% |
| 2 | Demand measured on Asia-origin East Coast imports, split out through each bill's port of lading, the rest split by lock set | Demand (240 against slot caps 89) | The demand measure on the trade itself, which the change log certifies in every past episode | The East Coast depots: returns of the line's own boxes exceeded its own East Coast discharges by 240k TEU |
| 3 | **Decisive:** the moved cargo recovered as the residual of the East Coast depot identity in the line's own boxes (returns − own discharges − carrier-haulage moves − sea repositioning), demand the remainder | **West Coast shift (240 against slot caps 75)**, tied last on rung 0 | — | — |

* **Position table.** The West Coast shift is tied last at zero on rungs 0, 1 and 2 and leads only rung 3. Rung margins are 8.2, 1.35, 2.70
  and 3.20.
* **Discriminator dominance.** Demand carries a 240k lead over the West Coast shift into rung 3 (240 against 0). The residual moves 200k from
  demand and 40k from the canal's share to the shift, a 440k swing in their difference, 1.83× the carried lead. The floor is 1.2×, so the
  edge has 1.53× headroom.
* **Partial correction priced (L3).** A solver who builds the depot identity on every box discharged from the line's ships forgets that
  vessel-sharing partners' boxes go home to the partners' depots. The residual shrinks to 110k, and demand leads at 170k, 1.55× the shift.
  One who suspects the shift and sizes it from the line's West Coast merchant-haulage discharges above the West Coast import index finds 95k,
  and demand leads at 185k, 1.95× the shift. Neither half names the shift.
* **Grid.** Demand basis (total index, Asia-origin index, residual on every box, residual on own boxes) × lock-set split (off, on) gives 8
  cells. Every cell without the own-box residual names slot caps, draft or demand. With it, both lock-set settings name the shift, because the
  residual replaces the demand estimate. The nearest wrong cells are the every-box residual's, which name demand at 170k (1.26× and 1.55×).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The tariff and the vessel-sharing agreement describe where empties go. No document links East Coast depot returns to
   lost Panama liftings, or mentions West Coast rail.
2. **Corpus blind for a computable reason.** *In every past episode the line's own East Coast depot returns balanced its own East Coast
   discharges within 0.5%, because every past restriction lasted under ten weeks, shorter than the rail carriers' 90-day minimum intermodal
   term, so no shipper moved East Coast cargo to the West Coast.* The change log certifies the trade index as demand in all eleven episodes.
3. **No arithmetic symptom.** Liftings, blanks, cancellations, discharges and both indices reconcile on every rung, and the rising depot
   stock is a correct stock change.
4. **Not a row predicate.** The moved cargo is an aggregate residual of four flows at the East Coast depots, and no booking, bill or box
   carries it.
5. **The enumeration is arithmetic.** No field marks a TEU as moved. The figure is an identity across complete records.
6. **No cutover date.** Shippers' rail contracts started through the year as each tender closed, so the shift accrued and never stepped.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The canal authority's advisory change log over twelve years: eleven restriction episodes (draft cuts and slot cuts), each with
  the line's weekly liftings, blank sailings, East Coast discharges and East Coast depot returns before and after.
* **What it certifies.** Rung 2's construction. In every episode, the Asia-origin East Coast index applied to the line's base matched the
  demand loss confirmed by the recovery after the restriction ended, and the capacity loss split by lock set matched the episode's blanks.
* **What it is blind to.** Cargo moved to the West Coast (property 2).
* **Twin pair.** The Savannah and Charleston depot regions are identical on own discharges, devanning times, carrier-haulage inbound moves and
  their share of the lost liftings. Their depot residuals are 64k and 31k TEU (2.06×), because Savannah's consignees sit within a day's truck
  of the Atlanta rail ramp. Only the depot identity separates them.
* **Resemblance points at the decoy.** The drought year most resembles the 2019 episode in the change log, when the Asia-origin index and the
  line's liftings fell together and the loss proved to be demand.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The network charter: "The committee funds the one response aimed at the cause behind the largest part of the year's lost
  Panama liftings, counted in the line's own boxes." The tariff: "Under merchant haulage the line's custody ends at the discharge port, and
  the merchant returns the empty to a depot the line designates in the consignee's region." The vessel-sharing agreement: "Each partner's
  boxes are returned to that partner's own depots."
* **Empirical pins.** The trade index as demand and the lock-set split come from the change log. The residual's terms come from the
  discharge lists, the depot counts, the carrier-haulage log and the repositioning log.
* **Voices.** Commercial director: "Shippers have stopped buying; we are running too many strings." Operations director: "Every blank sailing
  was a slot the canal would not give us." Fleet manager: "It was the Neopanamax ships that took the hit." Equipment controller: "The East
  Coast depots are filling up because exports have gone soft."
* **Licensed wrong basis.** The charter records that the trade committee reads every lane on the Asia-origin East Coast import index and will
  see the network plan on that basis.

## 8. Determinism by construction

* **Units.** Liftings, discharges and returns are counted in the line's own boxes by owner code, at one TEU for a 20-foot box, two for a
  40-foot and 2.25 for a 45-foot.
* **Timing.** The year starts and ends with the same stock of import boxes out with consignees, within 0.2%, so annual flows balance without a
  lag model.
* **Other flows.** No Asia import box was street-turned or off-hired on the East Coast in the year, and every carrier-haulage and
  repositioning move into the East Coast depots is logged. The reference year's residual was 0.3k TEU.
* **Blanks and cancellations.** Every blank sailing used one lock set, and every delay cancellation followed a delay notice within 72 hours.
* **Bills.** On merchant-haulage bills the consignee is the shipper's forwarder at the discharge port, so no bill carries an inland
  destination.

## 9. Prompt sketch and deliverables

> Commercial wants to cut one of our five Panama services because our East Coast liftings through the canal fell 30% this year. I can fund
> one response in next year's network, aimed at one cause. Tell me which cause we answer, in a sentence for the network committee, with the
> lost liftings you put on each of the five causes in thousand TEU, to the nearest thousand. Send `lane_causes.xlsx`, a chart
> `lost_liftings.png`, and a one-page `network_call.pdf`.

* `lane_causes.xlsx` — the five causes on every construction, the reliability sheet (ask A), the reefer sheet (ask B) and the change-log
  back-test (ask C).
* `lost_liftings.png` — a waterfall from last year's liftings to this year's with one bar per cause, the moved cargo fed by an inset of the
  East Coast depot identity (returns against own discharges), the trade index's reading as a ghost bar, and a title naming the funded
  response.
* `network_call.pdf` — the named cause, why each other cause is smaller, and the response it funds.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the five services and each quarter, schedule reliability: the share of port calls within
  one day of schedule. *Device:* the reliability standard measures each call against the schedule in force when the vessel left its previous
  port, which the schedule-history table holds, not against the pro forma. Using the pro forma understates reliability by 8 to 15 points on
  the two services that were re-timed. Port-call timing never enters liftings, blanks or depot flows.
* **Ask B (device-carried).** For each of the four East Coast ports and each quarter, billable reefer connections. *Device:* the terminals'
  monitoring logs one row per plug-in, and a box re-plugged within two hours of a yard move is one connection under the terminals' reefer
  tariff. Counting rows overstates connections by about 30% at the two terminals that restack reefers nightly.
* **Ask C (validity).** For each of the eleven past episodes, the East Coast depot identity's residual in the line's own boxes.
* **Decoupling.** Clearing the residual or the origin split changes no figure in asks A or B. Ask C shows the residual at zero in every
  closed episode, by property 2.

## 11. Rubric arithmetic

5 services × 4 quarters (ask A) + 4 ports × 4 quarters (ask B) + 11 episodes (ask C) + the named cause, the five causes' lost liftings and the
winning margin + 5 named chart parts + 3 files ≈ 62 criteria.

## 12. World-building constraints

* Own Panama liftings fall from 1,500k to 1,050k TEU. The 450k splits into Panamax-lock blanks 75, Neopanamax blanks 45, left-behind TEU on
  draft-limited sailings 15, delay cancellations 35, true demand 40 and the West Coast shift 240.
* The total East Coast import index fell 3% and the Asia-origin index 16%. Of the capacity share left after either demand bound, 35% sits on
  Panamax-lock services.
* Own East Coast depot returns exceed own East Coast discharges, carrier-haulage inbound moves and sea repositioning by 240k TEU. Partners'
  boxes discharged from the line's ships total 130k TEU. West Coast merchant-haulage discharges rose 95k TEU above the West Coast index.
* Savannah and Charleston are identical on every discharge, devanning and inbound-move column, with residuals of 64k and 31k.
* In all eleven past episodes the depot residual is under 0.5% of returns, and no episode lasted ten weeks.
* Schedule histories and reefer rows never touch liftings, blanks, discharges or depot counts.
