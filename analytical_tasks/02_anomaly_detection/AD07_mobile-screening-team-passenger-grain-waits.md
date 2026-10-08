# AD07 — Which airport gets the one mobile screening team for the summer, when the wait survey samples quiet hours densely and peak hours thinly

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Supply Chain & Logistics · aviation passenger screening operations |
| Mirrors | Placing scarce service capacity where customers actually wait, when the wait survey samples hours rather than customers (support-queue staffing at cloud providers, checkout staffing in big-box retail, delivery-station staffing at Amazon-scale networks where scan samples over-represent quiet hours) |
| Decision shape | Which of N gets one scarce thing: the agency's single mobile screening team for the summer peak |
| Committed call | The one airport the team works from 15 June to 31 August 2027 |
| Gap · Pattern | Gap 2 (population) · Pattern D (two grains, both flawless: sampled cards against passengers), with the deciding comparison (E22) at the rung below |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #2 counts file rows instead of the real unit · #20 leaves the deciding comparison unstated · #7 uses the ready-made measure |
| Calibration form | Existing-book actuals: the after-action book of last summer's 15 deployment-weeks, each with the passengers moved within the standard |
| Driving force | The wait survey hands a card to one passenger in five in quiet hours and one in twenty-five at the morning bank, by a protocol nobody wrote down. A card is not a passenger, and long waits live in the hours with the fewest cards, so every card-grain figure flattens the airport whose waits sit in a single early bank. Weighting each card by its checkpoint-hour's throughput over its cards, a reconciliation between two files, is the only reading the after-action book reproduces. |

## 1. Situation

A national screening agency has one mobile team for the summer peak and places it at one of eight airports that its throughput detector
flagged this spring. The deployment policy judges the team by the passengers it moves through screening within the 20-minute standard who
would otherwise have waited longer. The pack carries the detector's flags, last summer's hourly checkpoint throughput, last summer's wait
cards (each sampled passenger's entry and exit times), the lane register with this spring's new lanes, and the after-action book.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the detector's aligned growth, the throughput counts, each card's wait, the lane register and the
  after-action actuals. The detector is labelled as describing spring throughput, and the airport managers' card statistics are right
  about cards. Nothing reported is overturned; the difficulty is that cards and passengers are distributed differently across hours.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the detector export. The card file still yields a share over 20 minutes per airport, and every
  natural use of it, net of new lanes or not, still names C or B.
* **Instrument repair.** Hand a card to every passenger from now on; last summer has already happened, and the cards it produced are
  correct for what they sample. A perfect card count of last summer would still need weighting to hours, because the protocol set the
  sampling rate.
* **Lens swap.** The naive read is the population of sampled cards; the answer is the population of passengers, which puts most of its
  weight in the peak hours the cards thin out: a different population, not the same records under another lens.

## 3. The driving force

A strong solver sees that spring growth is not summer waiting, turns to the card survey, collapses duplicate scans, computes each airport's
share of passengers over 20 minutes, notices that one airport opened five lanes this spring and nets the passengers they absorb. Every
step is competent and it names C. But the survey's sampling rate was set by staffing at each checkpoint and hour band, one card in five
passengers in quiet hours and one in twenty-five at the morning bank, and the protocol is not in the pack. Long waits live in the bank
hours, where cards are thinnest. Airport E's waits sit almost wholly in its 05:00–08:00 low-cost bank, so its card share reads 11.5% while
its passenger share is nearly three times that. The bridge from cards to passengers is a reconciliation: each card carries its checkpoint-hour's
throughput divided by that checkpoint-hour's cards. Nothing invites it, and only it reproduces the after-action book.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The detector: spring throughput growth against the holiday-aligned baseline | A (+14.2%) | The agency's own anomaly screen, calendar-aligned, and growth is what breaks a checkpoint | The after-action book: last summer's realised moves bear no relation to spring growth at the six airports deployed |
| 1 | Hygiene and the survey: duplicate exit scans collapsed, share of last summer's cards over 20 minutes in the peak | B (17.8%) | The direct measure of waiting, cleaned, at the airport level the policy names | The lane register: B commissioned five lanes this spring, enough to absorb most of its excess |
| 2 | The deciding comparison: last summer's excess passengers (card share × throughput) net of the passengers this spring's new lanes absorb | C (61,000) | Demand against capacity, stated as one comparison, every input on file | The after-action book: card-grain excess reproduces 6 of 15 deployment-weeks within 5% |
| 3 | **Decisive:** each card weighted by its checkpoint-hour's throughput over that checkpoint-hour's cards, excess summed per checkpoint-hour, net of new lanes | **E (118,000)** (5th of 8 on rung 0) | — | — |

* **Position table.** E ranks 5th on rung 0 (+6.4%), 4th on rung 1 (11.5%) and 3rd on rung 2 (41,000), and leads only rung 3, 1.55× D
  (76,000) and 1.64× C (72,000). Intermediate leaders hold margins of 1.26×, 1.24× and 1.27×.
* **Discriminator dominance.** C carries a 1.49× advantage over E into rung 3 (61,000 against 41,000). Passenger weighting multiplies E's
  excess by 2.88 and C's by 1.18, an edge of 2.44 against the 1.2 × 1.49 = 1.79 required, 1.37× headroom.
* **Partial correction priced (L3).** A solver who converts cards to passengers at airport level, card share times total throughput, has a
  passenger figure that is still card-weighted and names C (61,000 against D's 48,000, 1.27×). A solver who weights by hour band
  airport-wide instead of by checkpoint-hour names D (88,000 against E's 74,000, 1.19×): D's long waits sit at its densely carded main
  checkpoint, which airport-wide band weights inflate, and E's at the thinly carded second of its two checkpoints, which they deflate.
  Neither half lands on E.
* **Grid.** Weighting (card, airport-level conversion, hour band, checkpoint-hour) × new lanes (ignored or netted) gives eight cells. Every
  cell that ignores the new lanes names B, whose gross excess is the largest under any weighting; the netted cells name C, C, D and E. The
  nearest wrong cell, hour-band weighting (D), needs the checkpoint dimension of the reconciliation dropped.
* **The deciding comparison (#20).** E's 118,000 passengers moved against C's 72,000 is the comparison the decision note has to state;
  neither the card shares nor the lane counts compute it alone.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The sampling protocol is not in the pack; the card file has no weight and no sampling field. The policy says
   passengers; nothing says cards are not passengers.
2. **The corpus pins a construction, not a menu.** Checkpoint-hour weighting reproduces all 15 deployment-weeks within 2%; card grain
   reproduces 6 and hour-band weighting 9, and every rival under-predicts the weeks whose waits sat in a bank, so each fails on the book's
   total too (card grain by 31%). The weight is a construction: it exists only after cards are grouped by checkpoint-hour and divided into
   that hour's throughput, and no column holds it.
3. **No arithmetic symptom.** Cards tie to the survey's daily returns, throughput ties to the national daily series, and every card falls
   in an hour with throughput.
4. **Not a row predicate.** It needs a group-by on checkpoint-hour in two files, a ratio between them, a weighted excess per hour, and a
   per-hour netting against new lane capacity.
5. **The enumeration is arithmetic.** Which passengers waited over 20 minutes is estimated per checkpoint-hour; no field carries it.
6. **No cutover date.** The protocol ran unchanged all summer; no series steps. The only dated item, the spring lane openings, sits in the
   rung below.
7. **Survives deletion.** With every voice and the detector removed, the answer and the difficulty are unchanged.

## 6. The calibration corpus

* **Form.** The after-action book: last summer's three mobile teams over 15 deployment-weeks at six of the eight airports, each week with
  the passengers moved within the standard as the agency's operations analysts recorded them.
* **What it pins.** Checkpoint-hour weighting reproduces 15 of 15 within 2%; card grain 6 of 15, under-predicting the book's total by 31%;
  hour-band weighting 9 of 15.
* **Twin pair.** Deployment-weeks D-07 and D-11 are identical on cards collected, card share over 20 minutes (14.0%), weekly throughput and
  lanes staffed. The book records 9,840 and 4,710 passengers moved (2.09×), because D-07's long waits sat in a thinly sampled bank and
  D-11's were spread through densely sampled hours.
* **Every rule exercised.** Two weeks include checkpoint-hours with a single card, so the weighting is tested at its extreme; one week
  straddles a new lane's commissioning, so the netting is tested.
* **Resemblance points at the decoy.** E's card profile most resembles the deployment-weeks with the smallest recorded moves.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The deployment policy: the team goes where it will move the most passengers through screening within the 20-minute
  standard who would otherwise have waited longer. The summer peak runs from 15 June to 31 August. Lanes in the lane register commissioned
  before the peak are in service for it, at the register's rated capacity.
* **Empirical pins.** The checkpoint-hour weighting, from the after-action book.
* **Voices.** The regional director: "Growth is what breaks a checkpoint; follow the detector." The general manager at B: "Our card survey
  has been the worst in the region two summers running."
* **Licensed wrong basis.** The policy records that the airports' joint operations council ranks airports on the card survey's share over 20
  minutes and will present that ranking at the planning session.

## 8. Determinism by construction

* **Weights.** Every checkpoint-hour with throughput holds at least one card, so no weight is undefined, and duplicate exit scans share a
  card serial, so the collapse is a key group-by.
* **Netting.** New lanes are netted per checkpoint-hour at the register's 150 passengers an hour; netting per day instead gives the same
  order at rungs 2 and 3.
* **Window and threshold.** The peak window is filed; 15- and 25-minute standards give the same leader at every rung.
* **Forward use.** The policy's book and last summer's waits are the basis; this spring's schedules are on file and change no airport's
  order, because no airport gains or loses a bank.

## 9. Prompt sketch and deliverables

> We have one mobile screening team for the summer peak, and it has to go to one airport. The regional director would follow the spring
> detector. Name the airport in one sentence for the deployment order, and send `summer_deployment.xlsx` with the sheets below, the chart
> `wait_weighting.png`, and a one-page `deployment_order.pdf`.

* `summer_deployment.xlsx` — the airport build, the interceptions sheet (ask A), the overtime sheet (ask B) and the book reproduction (ask C).
* `wait_weighting.png` — for each airport, passengers over 20 minutes by hour of day at card grain and at passenger grain as paired curves,
  the morning bank shaded, new-lane capacity as a dashed line, and the chosen airport highlighted.
* `deployment_order.pdf` — the committed airport and the deciding comparison against C.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each airport, last summer's prohibited-item interceptions per 10,000 passengers and the share
  found at PreCheck lanes. *Device:* the interception log writes one row per item, and a bag holding several items produces several rows
  under one bag-check ID, as the incident guide documents. Counting rows overstates interceptions at the three airports with the most
  multi-item bags. The card survey and the waits never touch the interception log.
* **Ask B (device-carried).** For each airport, officer overtime hours in June, July and August. *Device:* overtime on a shift that crosses
  midnight is booked to the shift's start date, per the timekeeping guide. Assigning hours by their clock time moves month-end night shifts
  into the wrong month at the five airports with overnight checkpoints.
* **Ask C (validity).** For each of the four rung constructions, the deployment-weeks it reproduces within 5% out of 15.
* **Decoupling.** Clearing the card weighting changes no figure in asks A or B.

## 11. Rubric arithmetic

8 airports × 2 (ask A) + 8 airports × 3 months (ask B) + 4 constructions (ask C) + the committed airport, its passengers moved and the
deciding comparison against C + 5 named chart parts + 3 files ≈ 55 criteria.

## 12. World-building constraints

* Rung leaders are A, B, C, E. E is 5th / 4th / 3rd / 1st; intermediate margins are at least 1.24×; E leads rung 3 by 1.55×.
* Rung 2: C 61,000, D 48,000, E 41,000. Rung 3: E 118,000, D 76,000, C 72,000. Airport-wide hour-band weights: D 88,000, E 74,000.
* Sampling: one card per five passengers in quiet hours, one per twenty-five in bank hours, varying by checkpoint; no protocol ships.
* E's waits over 20 minutes sit 81% in its 05:00–08:00 bank, at the second and thinner-carded of its two checkpoints; C's are spread
  across the day. B's five spring lanes absorb 70% of its excess.
* The book holds 15 deployment-weeks at six airports; D-07 and D-11 are identical on every card-level column.
* Interception rows and overtime bookings never touch the card file, the throughput file or the lane register.
