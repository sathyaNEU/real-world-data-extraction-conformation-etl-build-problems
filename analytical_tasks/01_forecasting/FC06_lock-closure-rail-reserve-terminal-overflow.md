# FC06 — How much grain to reserve rail for during next year's four lock closures, when storage fills terminal by terminal

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Supply Chain & Logistics · inland waterway freight |
| Mirrors | Committing overflow capacity when buffers are per site but the plan pools them (Amazon fulfilment-centre overflow when one site is full while the region has space, per-zone cloud capacity during a regional outage, retail distribution-centre overflow during a port closure) |
| Decision shape | One figure committed at a date: the tonnage the state freight office reserves rail for, filed by 1 December |
| Committed call | Grain tonnage to divert to rail during the four scheduled closures in the 1-in-10 year, to the nearest 1,000 tons |
| Gap · Pattern | Gap 3 (objective) over Gap 2 (population) · S5, a ceiling that does not commute (per-terminal storage), with two flawless grains below it (shipments at the lock, receipts at the terminals) |
| Gate G mechanism | binding_constraint, with forecasting support |
| Measured traps engaged | #10 notes a binding limit as a risk · #2 counts file rows instead of the real unit · #4 never tests its reading against the control |
| Calibration form | Revision log: the barge-booking system's revisions (deferrals and cancellations) for every stoppage in ten years |
| Driving force | During a closure a terminal's receipts can only go into its own licensed bins, so diversion is a sum over terminals of what each cannot hold. Pooling headroom across a pool's terminals hides the overflow wherever the space and the trucks are in different places. Terminal receipts are reported nowhere; they come from each terminal's stock change plus its barge loadings. In all 31 unplanned stoppages of the last ten years no terminal filled, so pooled and per-terminal readings both returned zero. |

## 1. Situation

A Corps district has fixed next year's four two-week maintenance closures (Locks 1–4, weeks 14, 22, 31 and 33). Grain trucked to the
fourteen river terminals above a closed lock cannot leave by barge, and what a terminal cannot store goes by rail. The state freight office
reserves rail by 1 December against the district's figure, and its reservation note sets that figure at the 1-in-10 year: the second-highest
total across ten replay years of receipts. The state's weekly receipts report is published by river pool.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: lock tonnage, the pool receipts report, terminal stock reports, the licence register and the booking
  revision log. No one's claim about their own numbers is overturned. The difficulty is the grain at which a correctly measured overflow
  binds.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the railroad's basis. Pool receipts against pool headroom is still the natural build, and it
  still files a figure a third low.
* **Instrument repair.** Publish receipts by terminal, perfectly. The pooled balance is still the obvious computation, and it is still
  wrong by the same tonnage, because the error is where the ceiling binds, not what was measured.
* **Lens swap.** The naive read and the answer are different populations: a pool's grain against each terminal's grain, and each closure
  is a moment the closed record never contained (a two-week closure with full receipts).

## 3. The driving force

A strong solver replaces lock tonnage with receipts, since diversion is about grain arriving, not grain leaving. It cleans the licence
register, computes headroom at each closure's start and runs ten replay years. It pools headroom within a pool because the receipts
report is published by pool, and pooled headroom is ample. But headroom is not fungible. Grain trucked to a terminal can only be held in
that terminal's licensed bins, and in pools 2 and 4 most of the empty space sits at terminals that take little of the harvest. A
terminal's weekly receipts are its stock change plus its barge loadings: the stock reports carry one half, and the other half is in LPMS
under the barge's origin dock. Diversion is the sum over terminals of each one's receipts minus its headroom, floored at zero, and that
is 51% above the pooled figure.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Two-week lock tonnage at each closed lock minus the summed register headroom above it, floored at zero, second-highest replay year | 31,000 t, −72% | The river's own count of what a closure stops, against the storage on file | The register keeps surrendered licences with their surrender date, and two terminals that changed operator are listed twice |
| 1 | Hygiene: surrendered licences removed, same construction | 44,000 t, −61% | Clean capacity, and every terminal now ties to its inspection certificate | The reservation note covers grain received above a closed lock, and lock tonnage is barge departures, smoothed by the storage it leaves |
| 2 | **E07 (two flawless grains):** pool receipts over each closure against pooled headroom, second-highest replay year | 74,000 t, −34% | The right flow at the grain it is published, and the revision log's deferrals reproduce it in every stoppage | The licence register: each terminal's capacity is its own, and in pools 2 and 4 headroom and receipts sit at different terminals |
| 3 | **Decisive:** terminal receipts rebuilt from stock change plus origin-dock barge loadings, each terminal's overflow floored at zero, summed, second-highest year | **112,000 t** | — | — |

* **Figure shape.** Every correction walks the figure up (−72%, −61%, −34%), and the per-terminal sum is the grid's maximum cell, since a
  sum of floors can never be below the floor of the sum. Every partial reading under-reserves.
* **Partial correction priced (L3).** Splitting pool receipts to terminals by licensed capacity, instead of rebuilding them, lands at
  81,000 t (−28%), because capacity share is exactly the allocation that hides the mismatch. Rebuilding per terminal from barge loadings
  alone (lock tonnage by origin dock) lands at 69,000 t (−38%), further away than rung 2.
* **Grid.** Licences (raw, clean) × flow (lock tonnage, pool receipts, terminal receipts) × pooling (pool, terminal) gives 10 feasible
  cells. The answer is the maximum. The nearest wrong cell is capacity-share splitting at −28%, and every cell that pools is at least
  34% low.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The reservation note says grain "that cannot be held" above the lock. No document says storage binds terminal by
   terminal or says how to get a terminal's receipts.
2. **Corpus blind for a computable reason.** *In every one of the 31 unplanned stoppages in ten years no terminal filled, because none
   lasted beyond four days and the tightest terminal held six days of receipts.* Pooled and per-terminal diversion were both zero in all
   31.
3. **No arithmetic symptom.** Terminal receipts sum to the pool report, stocks to the pool stock return, and diversions to whatever total
   each reading produces. Tonnage conserves under every rung.
4. **Not a row predicate.** Terminal receipts are an identity across two files (stock change plus origin-dock loadings), then a floor per
   terminal per replay year, then a sum, then an order statistic across years.
5. **The enumeration is arithmetic.** Which terminals overflow, by how much and in which replay year is computed. No column names them.
6. **No cutover date.** The closures are scheduled and future, and no series steps.
7. **Survives deletion.** No wrong number exists to delete. Without the voices, rung 2 is where a careful build stops.

## 6. The calibration corpus

* **Form.** The booking revision log: every barge booking at the fourteen terminals that a stoppage touched in ten years, with each
  deferral or cancellation and its new date.
* **What it certifies.** Receipts as the inflow: in every stoppage each terminal's stock rose by exactly its receipts and its deferred
  bookings equal its stock rise, so rungs 1–2 are confirmed. Lock tonnage misses every stoppage's deferral volume.
* **Free training instance (O3).** Nine years ago a 10-day planned closure at Lock 1 overflowed one terminal by 3,400 tons while pool 1 as
  a whole kept 9,000 tons of space, and the log shows cancellations at that terminal only. It is small, old and harmless, and it is the
  one case that exercises the per-terminal floor.
* **Twin pair.** Pools 2 and 3 are identical on every pool-level column: three terminals each, the same 1-in-10 two-week receipts, the
  same pooled headroom and the same lock tonnage. In a closure their terminals overflow 24,000 and 12,000 tons (2.0×), because in pool 2
  one terminal holds 70% of the headroom and takes 20% of the receipts. Pooled balances give the twins one figure.
* **Resemblance points at the decoy.** Next year's closure windows resemble the closed stoppages on every pool-level measure, and pooled
  balances fit those stoppages perfectly.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The maintenance schedule: closures in weeks 14, 22, 31 and 33, two weeks each. The reservation note: rail is reserved
  for grain received above a closed lock that cannot be held there, in the 1-in-10 year, which is the second-highest of ten replay years'
  totals. The licence register: a licence's capacity is the licensed bin capacity of one terminal.
* **Empirical pins.** Terminal receipts, from stock reports and origin-dock loadings. Headroom at each closure's start, from the stock
  reports. The per-terminal floor, from the Lock 1 closure in the revision log.
* **Voices.** The district's planning chief: "Lock tonnage is the river's own count, and it's what we have always sized closures on." The
  grain association's logistics lead: "Our members' bins are never the problem. Barges are."
* **Licensed wrong basis.** The reservation note records that the railroad prices reservations on the district's lock-tonnage exposure
  and will present its sizing on that basis at the rate meeting.

## 8. Determinism by construction

* **Replay.** Each replay year places the fixed closure weeks on that year's ISO calendar; no closure week straddles a year boundary.
* **Order statistic.** The reservation note fixes the second-highest of ten totals, so no percentile convention is exercised.
* **Stock timing.** Stock reports are weekly, as of Saturday; LPMS loadings are timed by departure, and the world is built so weekly
  identities close exactly.
* **Ownership.** No two terminals share an operator within a pool, so no company-level pooling reading is available.
* **Maturity.** Every stoppage in the log is closed and its last booking settled. The extract falls after the season's last loading.

## 9. Prompt sketch and deliverables

> The state freight office books rail by 1 December against whatever figure I give them for next year's lock closures, to the nearest
> thousand tons. Our planning chief would like to keep sizing on lock tonnage, as we always have. I need the tonnage, the build behind it in
> `rail_reserve_build.xlsx`, a chart `closure_overflow.png`, and a short `reservation_letter.pdf` I can send with the figure.

* `rail_reserve_build.xlsx` — the reservation build by closure, terminal and replay year, the tow-delay sheet (ask A) and the stoppage
  sheet (ask B).
* `closure_overflow.png` — one panel per closure: each terminal's 1-in-10 receipts against its headroom as paired bars, overflow shaded,
  the pooled headroom as a reference line, and the twin pools annotated.
* `reservation_letter.pdf` — the committed tonnage, its split by closure, and the bases the railroad and the district will raise.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each lock, last year's median and 90th-percentile tow delay from arrival to start of
  lockage, and the number of tows. *Device:* a 1,200-foot tow at a 600-foot chamber locks through in two cuts, recorded as two lockage
  rows sharing a tow ID. Delay is measured once per tow from the first cut's arrival, as the LPMS guide says. Per-row figures double the
  count and understate the delay at Locks 2 and 4. Tonnage sums are unaffected.
* **Ask B (device-carried).** For each lock, last year's availability and the number of unscheduled stoppages longer than 24 hours.
  *Device:* an extended stoppage is re-issued under the same notice number with a higher revision, and the latest revision supersedes.
  Counting revisions as stoppages overstates three locks and understates their availability.
* **Ask C (validity).** The reservation under each of the four rung constructions, and each construction's figure for the nine-year-old
  Lock 1 closure (3,400 tons actually cancelled).
* **Decoupling.** Replacing the per-terminal floor with pooled headroom changes no figure in asks A or B.

## 11. Rubric arithmetic

4 locks × 3 (ask A) + 4 locks × 2 (ask B) + 4 constructions × 2 (ask C) + the committed tonnage, its four closure splits and the replay
year that sets it + 5 named chart parts + 3 files ≈ 42 criteria.

## 12. World-building constraints

* Fourteen terminals in four pools, one operator each. Pools 2 and 4 hold most headroom at terminals with small receipts; pools 1 and 3
  are balanced.
* Rung figures 31,000 / 44,000 / 74,000 / 112,000 t; partial cells 81,000 and 69,000 t. No non-answer cell is within 28% of the answer.
* Two operator changes leave surrendered licences listed. Weekly stock identities close exactly with origin-dock loadings.
* All 31 unplanned stoppages lasted four days or less, and no terminal filled. The Lock 1 closure overflowed one terminal by 3,400 tons.
* Split-cut tows and re-issued notices never touch receipts, stocks or licences.
