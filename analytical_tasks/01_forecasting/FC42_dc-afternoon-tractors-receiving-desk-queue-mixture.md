# FC42 — How many tractors the dedicated fleet needs on duty at the afternoon peak while the Northgate DC is shut, when every truck's time at a distribution centre is set by one receiving desk's pace

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Supply Chain & Logistics · dedicated truckload fleet planning (grocery distribution) |
| Mirrors | Sizing a dedicated fleet whose cycle time is set by a shared receiving point (the dedicated carriers that run Walmart's and Kroger's supplier loads into regional distribution centres, container drayage into a congested cross-dock), where the receiving point's speed was only ever measured below its capacity |
| Decision shape | One figure committed at a date: the tractor roster for January to March |
| Committed call | Tractors on duty at the afternoon peak on weekdays next quarter, as a whole number |
| Gap · Pattern | Gap 4 (rule) over Gap 1 (time) · a mixture, not a constant (one receiving desk sets the dwell of every lane that delivers there), with a field validated on one population and applied to another (measured #13) at rung 1 |
| Gate G mechanism | forecasting, with method_or_model_selection |
| Measured traps engaged | #13 validates on one population, applies to another · #2 counts file rows instead of the real unit · #3 stops at a close but inexact match |
| Calibration form | Settled-transaction ledger: the retailer's settled freight bills for the last two years, each carrying the distribution centre's signed gate-in and release times |
| Driving force | A truck's time at a distribution centre is set by its receiving desk, not by its lane or its load. Riverside DC releases one trailer every 12 minutes, first come first served, so its dwell is a queue fed by every lane that delivers there. At last year's 4.2 afternoon arrivals an hour the queue always cleared, and Riverside looked like the network's fastest DC at 14 minutes; with Northgate shut for its retrofit, 7.0 an hour arrive against a pace of 5, and the queue grows all afternoon. The pace shows only as exact 12-minute spacing between release times on the settled freight bills. |

## 1. Situation

A dedicated truckload carrier runs a grocery retailer's inbound loads from nine truck yards into four distribution centres: Ashby,
Riverside, Northgate and Dunmore. Northgate closes for an automation retrofit from January to March, and the retailer's routing guide
sends each of its loads to the nearest open DC by the routing matrix. The service agreement sets the weekday roster at the
90th-percentile weekday of the most tractors busy at once in the afternoon's busiest hour, and the carrier's planning convention replays
last year's same quarter. The pack holds the dispatch system's load and tractor-status tables, the retailer's settled freight bills, the
routing matrix, the retailer's carrier scorecard of average dwell by DC and the routing guide. The roster is signed on 1 December.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: load and status times, the settled bills, the drive times and the scorecard, which really does
  rank Riverside fastest. No stakeholder's reading of their own numbers is overturned. The difficulty is what Riverside's desk does at a
  load it has never carried, which no record of the past shows directly.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the operations manager's view and every voice. Replaying last year with each DC's hourly mean dwell is still
  the natural build, it still reproduces every closed quarter within a tractor, and it still lands at 28.
* **Instrument repair.** Clean-data test. No file the ladder reads is incomplete, stale or narrower than it claims: the status table
  records every attachment (a tractor re-dispatched mid-trip stays attached to both loads, as the dispatch guide documents), the freight
  bills every gate-in and release, the routing matrix every drive time. The deepest repair available, a status table with one row per
  tractor and minute, makes rung 0 return 31 and rung 1 28 (rung 2's figure), neither 40, and the desk queue is still needed, because
  Riverside has never received seven trucks an hour.
* **Lens swap.** The naive read and the answer describe different moments of the same desk: Riverside below its pace, where dwell is a
  stable 14 minutes, against Riverside above it, where dwell grows with every arrival since midday.

## 3. The driving force

A strong solver replays last January to March from the tractor-status table, re-drives Northgate's loads to their new DCs by the routing
matrix, gives each diverted load the receiving DC's hourly mean dwell rather than its own, counts distinct tractors rather than
tractor-load pairs, and reads the busiest afternoon hour's 90th-percentile weekday: 28 tractors. It back-tests the method on the previous
year and lands within a tractor. Every step is correct. But a truck's dwell at Riverside is not a property of Riverside's average
afternoon: the receiving desk releases one trailer every 12 minutes in arrival order, so each truck waits for every truck ahead of it,
whichever yard sent it. Last year Riverside's afternoon arrivals averaged 4.2 an hour against a pace of 5, so queues formed only in bursts
and cleared within the hour. Next quarter the diverted loads bring 7.0 an hour from noon, the queue grows by two trucks an hour, and on
the 90th-percentile weekday eleven trucks are at Riverside at once by half past three. Built as a first-come queue at the 12-minute pace
the bills reveal, the afternoon needs 40 tractors.

## 4. The ladder

| Rung | Construction | Lands on (tractors) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Last year's quarter replayed as recorded, Northgate's loads re-driven by the routing matrix, each keeping its recorded dwell | 36 (−10%) | The planning convention applied to the letter, with the closure modelled | The retailer's scorecard: dwell belongs to the receiving DC, and Northgate's 38-minute mean is the network's slowest |
| 1 | Diverted loads take the receiving DC's hourly mean dwell | 33 (−17.5%) | Calibrated by receiving DC, the subgroup the forward rows differ on | The dispatch data guide: a tractor re-dispatched mid-trip stays attached to both loads, so counting open tractor-load pairs counts it twice |
| 2 | Hygiene: distinct tractors busy each minute | 28 (−30%) | Clean, DC-calibrated, and the back-test on the previous year lands within a tractor | The settled freight bills: at Riverside every release that follows a waiting truck comes exactly 12 minutes after the one before |
| 3 | **Decisive:** each DC's receiving desk built as a first-come queue at the pace its bills reveal (Riverside 12 minutes), fed by the replayed arrivals from every yard | **40** | — | — |

* **Figure shape.** Rungs 0 to 2 walk the roster down (−10%, −17.5%, −30%) and the decisive rung reverses past rung 0, so a solver who
  stops anywhere short leaves the afternoon short of tractors.
* **Partial correction priced (L3).** A solver who suspects congestion but scales Riverside's mean dwell by the load ratio (7.0 / 4.2)
  lands at 29 (−27.5%). One who sees the 5-an-hour pace but uses a steady-state queue, finds it undefined above the pace and caps each
  wait at the longest wait on the bills (52 minutes) lands at 33 (−17.5%).
* **Grid.** Diverted dwell (own recorded, receiving hourly mean, receiving desk as a queue) × count (tractor-load pairs, distinct
  tractors) = 6 cells: 36, 31; 33, 28; 45, 40. The nearest wrong cells are 36 (−10%) and the queue with tractor-load pairs at 45
  (+12.5%); reaching either takes dropping one whole correction.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The scorecard gives each DC's mean dwell; the retailer's receiving appointment guide sets a two-hour target. No
   document says a desk releases at a fixed pace, in arrival order, or that a mean belongs to a load.
2. **Reproduction (Pattern B).** A first-come queue at 12 minutes reproduces all 1,940 Riverside release times on the bills to the minute;
   an 11- or 13-minute pace misses all 212 queued releases; hourly means reproduce none of the queued releases and miss them by up to 40
   minutes. The rule is a construction, not a menu: a recursion over each DC's arrivals from every yard, joined from the status table's
   gate-in stamps to the bills' release times, and no sweep over constants reaches it.
3. **No arithmetic symptom.** Bills reconcile to loads, status stamps to dispatches, drive times to the matrix, and every rung's replay
   reproduces the previous year within a tractor.
4. **Not a row predicate.** A truck's wait depends on every truck that reached the same desk before it, so it needs an ordered recursion
   per DC, not a filter or a group mean.
5. **The enumeration is arithmetic.** No column marks a release as queued; queues are computed from arrival order and pace.
6. **No cutover date.** The retrofit lies in the future and steps nothing in the pack; Riverside's pace has been 12 minutes on every bill.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The retailer's settled freight bills for two years: every paid load, its receiving DC, and the DC-signed gate-in and release
  times the retailer requires before it settles a bill.
* **What it certifies.** Rungs 1 and 2: each DC's hourly mean dwell, the 10-minute drop-and-hook after every release, and a replay that
  reproduces each closed quarter's afternoon 90th percentile within a tractor.
* **What it is blind to, and what it pins.** *In every closed afternoon Riverside's arrivals averaged under five an hour, so its queue
  cleared within the hour and its hourly mean described every afternoon;* the pace itself, 12 minutes in arrival order, is pinned by the
  212 queued releases.
* **Twin pair.** Two weekday afternoons at Riverside last February each brought six trucks between 15:00 and 16:00, from the same yards
  with the same load types. They spent 147 and 297 truck-minutes at the DC (2.0× apart), because one afternoon's six arrived eleven minutes
  apart and the other's within five minutes. Hourly means predict them equal; only the 12-minute queue reproduces both.
* **Resemblance points at the decoy.** The scorecard ranks Riverside the network's fastest desk, and by drive time and load type the
  diverted loads most resemble Riverside's own.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The service agreement: the weekday roster covers the 90th-percentile weekday of the most tractors busy at once in the
  afternoon's busiest hour. The planning convention: replay last year's same quarter with the quarter's known changes. The routing guide:
  each load goes to the nearest open DC by the routing matrix.
* **Empirical pins.** Each DC's release pace and order, and the drop-and-hook time, from the settled bills.
* **Voices.** The operations manager: "Riverside turns trucks faster than any DC we serve; Northgate's loads will clear quicker there than
  they ever did at home." The fleet planner: "We've rostered on last year's busy tractors for six years and never been more than a
  tractor out." The finance director: "Volume is flat, so I don't see why the afternoon needs more."
* **Licensed wrong basis.** The service agreement records that the retailer audits the carrier's roster against last year's
  90th-percentile busy tractors and will check the roster on that basis.

## 8. Determinism by construction

* **Replay.** The convention fixes last year's January to March weekdays (63 afternoons), and the retailer's volume forecast is flat, so
  no scaling arises.
* **Routing.** No yard's loads sit within two minutes of a tie between two open DCs in the matrix, so every diverted load has one
  destination.
* **Pace and order.** Every queued release at every DC fits its integer pace in arrival order; drop-and-hook is 10 minutes on every bill.
* **Peak hour.** 15:00–16:00 is the busiest weekday hour in all six grid cells.
* **Percentile.** The ordered afternoon maxima are flat around the 90th percentile (the 55th to 59th of 63 are all 40), so inclusive and
  exclusive definitions agree.

## 9. Prompt sketch and deliverables

> Northgate DC shuts for its retrofit from January to March, and its loads will go elsewhere. Our operations manager expects Riverside to
> absorb them without trouble. Tell me how many tractors we need on duty at the afternoon peak next quarter, as a whole number, in one
> sentence for the roster, and send `roster_build.xlsx` with the build and the sheets below, a chart `riverside_afternoon.png`, and a
> one-page `roster_note.html`.

* `roster_build.xlsx` — the replay under each construction, the pickup sheet (ask A) and the fuel sheet (ask B).
* `riverside_afternoon.png` — trucks at Riverside minute by minute from 11:00 to 19:00 on the 90th-percentile weekday under hourly means
  and under the 12-minute queue, with arrivals as ticks along the axis, the 5-an-hour pace as a reference slope, and the peak hour shaded.
* `roster_note.html` — the committed figure, what Riverside's desk does above its pace, and why last year's busy tractors understate it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the nine yards and each month of last quarter, the share of supplier pickups made
  within their appointment window. *Device:* a pickup the supplier reschedules keeps its original appointment in the tender table, with
  the new window in the appointment-change table, as the transport-management guide documents; scoring against the tender table
  understates on-time pickups at six yards. Pickup timing enters no part of the roster build, which runs from dispatch to release.
* **Ask B (device-carried).** For each of the nine yards, last quarter's fuel per loaded mile. *Device:* fuel drawn at a shared yard pump
  posts to the yard's bulk account, with the tractor in the pump-allocation table, as the fuel guide documents; reading card transactions
  alone understates fuel at four yards. Fuel enters no part of the roster build.
* **Ask C (validity).** The afternoon requirement under each of the four rung constructions, and how many of the 212 queued Riverside
  releases each construction reproduces to the minute.
* **Decoupling.** Clearing the desk queue changes no figure in asks A or B.

## 11. Rubric arithmetic

9 yards × 3 months (ask A) + 9 yards (ask B) + 4 constructions × 2 (ask C) + the committed figure and Riverside's forecast afternoon
arrival rate + 5 named chart parts + 3 files ≈ 54 criteria.

## 12. World-building constraints

* Last year's weekday afternoons (12:00–18:00): Riverside 4.2 arrivals an hour, never more than six in an hour; Northgate 3.1, of which
  the routing matrix sends 2.8 to Riverside and 0.3 to Dunmore. Next quarter Riverside receives 7.0 an hour against a 5-an-hour pace.
* Mean gate-in to release: Northgate 38 minutes, Riverside 14; drop-and-hook 10 minutes after every release.
* Requirement by rung: 36 / 33 / 28 / 40. Grid: own dwell with distinct tractors 31; queue with tractor-load pairs 45. Partials: scaled
  mean 29, capped steady-state wait 33. Tractor-load pairs add five tractors at the 90th-percentile peak hour under every construction.
* Bills: 1,940 Riverside releases, 212 of them queued, each exactly 12 minutes after the previous one.
* The twin afternoons are identical in hourly arrivals, yards and load types; 147 and 297 truck-minutes at the DC.
* Rescheduled pickups and shared-pump fuel touch no busy interval, bill or arrival used in the forecast.
