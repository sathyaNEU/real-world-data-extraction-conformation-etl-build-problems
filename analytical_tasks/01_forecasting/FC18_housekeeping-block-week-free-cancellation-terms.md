# FC18 — Which August week gets the agency's housekeeping block, when the festival week's bookings were sold with free cancellation

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Supply Chain & Logistics · hotel operations staffing |
| Mirrors | Forecasting from a book of commitments whose cancellation terms differ by subgroup when the validated rate was fitted on a steady mix (Airbnb and Booking.com flexible against non-refundable reservations, Amazon pre-orders with free cancellation, airline and cloud reserved capacity sold under different release terms) |
| Decision shape | Which of N gets one scarce thing: the staffing agency's single block of temporary housekeepers, for one of five August roster weeks |
| Committed call | The roster week that gets the block, with its forecast occupied room-nights above the in-house crew's 2,660, to the nearest 10 |
| Gap · Pattern | Gap 2 (population) over Gap 1 (time) · S8, a pooled cancellation rate that fits every closed August and applies to no week of this one, with a loud grain decoy and a quiet share-with contamination below it |
| Gate G mechanism | forecasting, with decomposition_attribution |
| Measured traps engaged | #13 validates on one population, applies to another · #11 beats the headline trap, misses the quiet one · #18 joins only on the visible key |
| Calibration form | Counterparty acknowledgement file: the online travel agency's acknowledgements of every booking it delivered over two years, each with its confirmation number, cancellation terms, every change and cancellation, and the stay's outcome |
| Driving force | The memo's cancellation share at each lead is pooled, and it reproduces every closed August week within 1% because the free-cancellation share of the 1 July book never left 14–16%. This spring the agency sold the festival packages with free cancellation, so 48% of the festival week's book can walk away free, against none of the trade-fair week's, sold on the agency's non-refundable fair rate. Free-cancellation bookings lose 45% of their book by arrival, the rest 3%. The terms sit only in the agency's acknowledgement file, reached through the channel confirmation number, because the hotel's system files every agency booking under one rate code. |

## 1. Situation

A 480-room city hotel's in-house housekeeping crew can clean 380 occupied rooms a night. For August the staffing agency will supply one
block of temporary housekeepers for one Monday-to-Sunday roster week (W1 28 July–3 August to W5 25–31 August). The housekeeping
standard sends the block to the week with the most forecast occupied room-nights above the crew's 2,660 a week. The roster is set on 1
July from the revenue-management memo's forecast: rooms on the books, less the cancellation share at that lead, plus net new-booking
pickup at that lead, both averaged over the same weekday's nights in the last two Augusts.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the property-management (PMS) export, the night audit, the agency's acknowledgement file and its
  monthly partner report, the group contracts and the memo's curves. No one's claim about their own numbers is overturned. The difficulty
  is that the pooled cancellation rate describes no week of this August's book.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the agency's pricing basis. The memo's forecast on night-by-night rooms still names W3, and
  the closed Augusts still confirm the curve within 1%.
* **Instrument repair.** Record every booking and cancellation perfectly. The pooled rate stays exact for the books that produced it,
  and this August's festival-week book is a different mix of terms, so no better record of past Augusts shows its losses.
* **Lens swap.** The naive read and the answer differ in population: a book whose terms were mixed as in every closed August, against
  weekly books whose terms run from none free to 48% free.

## 3. The driving force

A strong solver expands every stay into its nights, finds the share-with reservations the night audit exposes, and applies the memo's
curve. The curve is exact on its history: in every closed August week the hotel lost 9.3% of its 1 July book by arrival. That rate is a
mixture, and the mixture held still. Bookings the agency sold with free cancellation lose 45% of their book by arrival, and everything
else, non-refundable agency rates, corporate and group contracts, loses 3%. Until this spring free cancellation was only on the agency's
flexible rate and made up 14–16% of every August week's book. This spring's festival packages were sold with free cancellation, and
the trade fair's visitors booked the agency's non-refundable fair rate. The festival week (W3) will shed far more than the curve says
and the trade-fair week (W4) far less. The PMS files every agency booking under one channel rate code, so the terms come only from the
agency's acknowledgement file, joined on the channel confirmation number.

## 4. The ladder

| Rung | Construction | Names (forecast room-nights above 2,660) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The memo's forecast on the 1 July book tallied by arrival week, the PMS pace report's grain | W1 (640 against 500) | The filed method on the system's own report | The housekeeping standard counts rooms occupied each night, and the congress block that arrives on Sunday 3 August stays four more nights in W2 |
| 1 | The same with every stay expanded night by night | W2 (590 against 500) | The right grain, every reservation-night counted, and the PMS's own stay history reproduced | **E15 (the quiet second trap):** the night audit's occupied rooms in closed congress weeks fall short of reservation-nights by exactly the share-with reservations, two reservations in one room |
| 2 | Share-with reservations counted once, as rooms | W3 (500 against 409) | Rooms tie to the night audit, the grain is right, and the curve reproduces every closed August week within 1% | The agency's partner report: 39% of this August's agency room-nights were sold with free cancellation, against 30% in each closed August, and the acknowledgement file shows the two terms' losses at 45% and 3% |
| 3 | **Decisive:** the 1 July book's cancellations calibrated by terms, each agency booking's terms joined from the acknowledgement file on its confirmation number | **W4 (420 against 291)** | — | — |

* **Position table.** W4 is 4th on rung 0 (288), 4th on rung 1 and 4th on rung 2 (288), and leads only rung 3. Leaders beat runners-up
  by 1.28×, 1.18×, 1.22× and 1.44×.
* **Discriminator dominance.** W3 carries a 1.74× advantage into rung 3 (500 against 288). W4's edge on the decisive axis is 3.44×
  (W4 rises 1.46×, from 288 to 420, while W3 falls to 0.42× of itself, from 500 to 212), against the required 1.2 × 1.74 = 2.09, a
  headroom of 1.65.
* **Partial correction priced (L3).** Calibrating by terms but keeping share-with reservations names W2 (485 against 420, 1.16×).
  Applying the partner report's August-wide 39% to every week's agency book names W3 (418 against W2's 362, 1.15×). Calibrating by channel
  instead of terms (agency 15.6%, everything else 3%, from the closed Augusts) names W3 (468 against W2's 405, 1.16×). W4's book is mostly
  agency bookings, so every channel-level reading marks it down.
* **Grid.** Grain (arrival week, night) × reservations (as stored, share-with once) × cancellation (pooled, by channel, August-wide terms
  share, booking terms) gives 16 cells. W1, W2 or W3 leads every cell but the answer's, each by at least 1.15×; the nearest is the
  August-wide terms share, which needs the join to become the answer.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The memo files a cancellation share by lead. No document says cancellation depends on terms, that the PMS rate
   code hides them, or which weeks the spring packages filled; the acknowledgement file ships for commission reconciliation.
2. **Corpus blind for a computable reason.** *In every closed August week the free-cancellation share of the 1 July book was 14–16%,
   because until this spring the agency offered free cancellation only on its flexible rate.* The pooled curve reproduces all ten closed
   August weeks within 1%, and so does a terms-calibrated curve.
3. **No arithmetic symptom.** Rooms tie to the night audit after share-with, agency bookings tie one for one to acknowledgements, and every
   forecast sits below the hotel's 3,360 room-nights a week.
4. **Not a row predicate.** No booking is dropped. Each week's book is re-weighted by the loss rate of its own terms mix, built through a
   join from the PMS to the counterparty's file, and only then compared across weeks.
5. **The enumeration is arithmetic.** Each week's expected loss comes from its own terms mix at each lead. No column ranks the weeks.
6. **No cutover date.** The promotion is dated, but no closed outcome series steps; its bookings have not arrived yet.
7. **Survives deletion.** No wrong number exists to delete. Without the voices, rung 2 is where a careful build stops.

## 6. The calibration corpus

* **Form.** The agency's acknowledgement file for two years: 41,000 bookings, each with its channel confirmation number, terms (free
  cancellation or non-refundable), timestamps of every change and cancellation, and whether the guest stayed.
* **What it certifies.** The loss rates by terms, from the 1 July-equivalent book to arrival: 45% for free cancellation and 3% for
  non-refundable, within a point in every closed month. With the hotel's own contracts at 3%, they recombine to the memo's 9.3% at every
  closed August's 14–16% free share. A back-tester is confirmed at rung 2.
* **What it cannot show.** A closed August week with a skewed terms mix (above).
* **Twin pair.** Spring weeks W19 and W22 are identical on every PMS column: a 35-day book of 1,960 room-nights, half of it agency, the
  same lead and weekday profile. They lost 368 and 182 room-nights by arrival (2.0×), because W19's agency book was 75% free cancellation
  under a city-break promotion and W22's 30%. The pooled and channel rates give both 182; only terms reproduce both.
* **Resemblance points at the decoy.** This August's book matches last August's on every PMS column (size, agency share, lead profile),
  and last August the pooled curve missed no week by more than 1%.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The housekeeping standard: the agency block goes to the roster week with the most forecast occupied room-nights above
  2,660. The revenue-management memo: the 1 July book less the cancellation share at each lead, plus net pickup at each lead, both from the
  last two Augusts' same-weekday nights. The PMS export guide: a share-with reservation carries the number of the reservation whose room it
  shares.
* **Empirical pins.** Loss rates by terms, from the acknowledgement file. Each agency booking's terms, by confirmation number. The share-with
  rule, from the night audit.
* **Voices.** The front-office manager: "The congress week always breaks housekeeping." The revenue manager: "Our cancellation curve has
  held for years; a booking is a booking."
* **Licensed wrong basis.** The standard records that the staffing agency prices the block from the weekly arrivals in the PMS pace report
  and will quote its premium for the week that report shows busiest.

## 8. Determinism by construction

* **Leads.** Every August night is 27–61 days out at 1 July, and both terms' loss rates are flat across those leads within half a point,
  so lead-bucket conventions converge.
* **Pickup.** The promotion ended on 30 June, so bookings made after 1 July carry the closed Augusts' terms mix and net pickup needs no
  recalibration.
* **Contracts.** The congress block's release date has passed and its contract allows no further release; corporate and direct bookings
  carry their terms in the PMS, all non-refundable or guaranteed.
* **Share-with.** Every share-with reservation points at one occupied reservation, with no chains.
* **Weeks.** Roster weeks run Monday to Sunday as the standard says, so the congress's Sunday night counts in W1.
* **Maturity.** The 1 July book is the PMS state at midnight on 30 June, and both closed Augusts are fully checked out and audited.

## 9. Prompt sketch and deliverables

> I sign the agency's August contract on Friday, and it buys one block of temporary housekeepers for one roster week. Our front-office
> manager is certain the congress week will break us. Tell me which week gets the block and how many room-nights above our own crew's
> capacity you expect that week, to the nearest ten, and send `august_block_case.xlsx`, a chart `week_overflow.png`, and a one-page
> `block_decision.pdf`.

* `august_block_case.xlsx` — the forecast for all five weeks under each construction, the rate sheet (ask A) and the cleaning sheet
  (ask B).
* `week_overflow.png` — each week's forecast room-nights as bars split into non-refundable, free-cancellation and pickup, the crew's 2,660
  as a labelled line, the pooled forecast as a marker on each bar, and the chosen week highlighted.
* `block_decision.pdf` — the committed week and its overflow, the runner-up, and the pace-report basis the agency will quote.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each roster week of last August, the average daily rate and revenue per available room.
  *Device:* complimentary rooms count as occupied in the night audit but carry no room revenue, and the audit's rate excludes them, as its
  definitions page states. Dividing revenue by all occupied rooms understates the rate in the two weeks with conference comps.
* **Ask B (device-carried).** For each roster week of last August, housekeeping minutes per occupied room and the share of rooms cleaned
  twice. *Device:* a room failed at inspection posts a second clean event with a redo flag, and the standard counts one clean per occupied
  room-night. Counting events inflates minutes per room in three weeks and invents a re-clean share where the log shows a redo.
* **Ask C (validity).** Each week's forecast overflow under each of the four rung constructions, with each construction's fit to the ten
  closed August weeks and to the twin spring weeks.
* **Decoupling.** Replacing booking terms with the pooled curve changes no figure in asks A or B.

## 11. Rubric arithmetic

5 weeks × 2 (ask A) + 5 weeks × 2 (ask B) + 5 weeks × 4 constructions (ask C) + the committed week, its overflow, the runner-up and the
margin + 5 named chart parts + 3 files ≈ 52 criteria.

## 12. World-building constraints

* 1 July book in room-nights (free agency · non-refundable agency · direct and corporate · group): W1 0 · 200 · 1,400 · 210; W2 600 ·
  500 · 200 · 840; W3 1,000 · 300 · 800 · 0; W4 0 · 1,500 · 600 · 0; W5 400 · 600 · 1,100 · 0. Share-with reservations: 50 in W1, 200 in
  W2 (50 a night, Sunday to Thursday). Net pickup: 670 / 1,128 / 1,255 / 1,043 / 1,075.
* Loss rates: 45% free, 3% everything else, 9.3% pooled; by channel 15.6% agency and 3% the rest. August-wide free share of the agency book
  39% this year and 30% in each closed August.
* Overflow by rung: W1 640/0/0/0, W2 0/590/409/291, W3 500/500/500/212, W4 288/288/288/420, W5 320/320/320/284. Partial cells 485 (W2),
  418 and 468 (W3).
* Spring weeks W19 and W22 are identical on every PMS column. Every forecast stays below 3,360 room-nights a week.
* Comps and inspection redos never touch the book, the acknowledgement file or the night audit's occupied counts.
