# task117: the Civic Center decks' contracted service demand, realising analytical_tasks note FC01 (analytical_tasks/01_forecasting/FC01_garage-service-demand-vehicle-limited-draw.md)

Stage 1 (draw), drawn 2026-10-08. This is the build's one design note; the design stage extends it.

## Draw

```
DRAW  (independent draws, checked with .claude/skills/fingerprint/guard.py)
  Card filed with guard.py register before the ladder was written? yes, registered 2026-10-09 after checkpoint A (go)   Verdict: WARN
  Shape: 02 forecast across many periods   Gate G mechanism: forecasting (method_or_model_selection supporting)
  Gap: time (decisive), population   Pattern: E (decisive), A (frame)
  Domain: supply-chain-logistics   Subdomain (enumerated): sourcing-procurement   Objective: forecasting
  Pairing repeated from last build? No. task116 is product-analytics x opportunity-sizing-decision, and none of task114 to task116 is supply-chain-logistics x forecasting
  Stakeholder role: the city's energy manager, who buys utility service for city facilities and signs the service agreement (procurement_lead)
  Context-artifact type: operations_log, the facilities electricians' monthly sub-meter log for the two deck charging panels (kWh, and the maximum-demand register read and reset each month)
  Calibration form: settled_transaction_ledger, 36 months of settled sessions at the eight garages, each with its 15-minute interval readings
  Decision type: quantity_figure, the contracted demand in kW to the nearest 5 kW
  Decisive mechanism: G14 conditioned yield. Each forward session draws the smaller of 11.5 kW and its own car's onboard charger limit, reached through session, permit, registered model and the state vehicle list. G16 (session replay over ratio scaling) and G7 (the tariff's on-peak billing window) carry the lower rungs
  Repeats from prior builds: none inside the ban window. The (time, E) signature repeats task37, task44 and task97, all older, with a differentiation line for each on the card

  Niche: a city's contracted demand for the new dedicated utility service that will feed two permit-only garage decks once their 6.6 kW Level 2 pedestals are replaced by 11.5 kW units, committed for the first contract year under a twelve-month demand ratchet
  Forum: council_or_assembly (the city council approves the service agreement)   Forcing event: cutover_or_migration (the decks switch over to the new dedicated service when the old pedestals come out)   Organisation family: local_government
  Scoring unit: per active unit per period (a fixed monthly charge per contracted kW)
  World: United States, Washington; USD; the fictional city of Larch Harbor. Provisional invented names: Civic Center North Deck, Civic Center South Deck, Library Garage, North Sound Power & Light (the utility), Curbline Charging (the network operator)
  People, drawn with guard.py names --geo "United States, Washington" --seed 117: Shelley Tanner (city energy manager, the requester), Ricardo Moore (facilities engineer), Anthony Cantrell (lead electrician, keeps the sub-meter log), Paul Henderson (the utility's new-service planner), Timothy Pierce (permit office supervisor), Adam Warner (parking services manager)
  Spine (planned): session_intervals_2024-2026.parquet, about 1,500,000 rows, one 15-minute energy reading on one settled charging session, grain session x 15-minute interval, synthetic
  Deliverables (planned): civic_service_demand.xlsx (the demand build and the monthly forecast), deck_load_day.png (the busiest billed day at quarter-hour grain), contract_demand_note.pdf (commits to the figure)
  Opening move (provisional): calendar-first
  Criteria arithmetic (shape 02): 12 contract months x 2 figures (billed demand in kW, on-peak energy in kWh) = 24, plus the contracted kW, the month that sets it, the deck split at the binding interval (2), the gap to the utility's nameplate sizing, 5 named chart parts and 3 files, about 37 before any device-carried ask
```

As-of date: 2027-01-25

Similarity claim: no prior build is this puzzle, because none commits a forward capacity figure whose peak turns on a per-unit draw cap that bound in no closed period and is an attribute of a different entity three joins away; task114, the nearest sibling, shares the replay-under-a-new-configuration frame but turns on demand that newly appears, not on which limit binds.

## Stump sentence

A competent solver rebuilds the tariff's on-peak billing maximum from the interval readings, replays every closed session on the new pedestals at 11.5 kW until its delivered energy (a model that reproduces all 36 closed on-peak maxima to the kWh), scales by the filed 1.12 growth factor and files 115 kW (116 unrounded); the step that lands it there is never asking whether each car can take 11.5 kW, which only the join from session to permit to registered model to the state list's onboard charger rating answers, putting 78 per cent of the decks' cars at 7.2 to 7.7 kW and stretching their sessions past noon into the billed window, for a contracted demand of 150 kW.

## Decisive rung

Measured trap #13, validates on one population, applies to another (`.claude/skills/stumping/references/traps/_measured.md`): established, decided 3 of the 64 measured client tasks, 2 of them under 0.50 (Capital Grant Drawdown Forecasting 0.34, CDFI Award Compliance 0.39, the operator-weighted non-conformance claim 0.62). Here the session model (a session draws the pedestal rating until its energy is delivered, then nothing) fits every closed session it can be checked on, all 36 closed on-peak maxima at the decks to the kWh, and a solver applies it to forward sessions that differ on one axis: which limit binds. The difference is evidenced in the pack and stated nowhere: the Library pedestal (11.5 kW, used only by enforcement vans whose chargers stop at 11.0 kW) and the state list's charger ratings behind the permit registry.

The corpus law it rests on is L1 of `proven-in-production.md`, and its sentence can be written: in every closed session at the decks the car's onboard limit did not bind, because every closed pedestal was rated 6.6 kW and every registered vehicle accepts at least 7.2 kW. Below it, per the note: #7 uses the ready-made measure (rung 0) and #14 coarsens the segment (rung 1).

Part 6.1 checks against `proven-in-production.md`. Nothing in this draw is on the What-is-dead list: the committed figure is not the output of a filed formula (only the 1.12 growth factor is filed), the decisive rule is a per-car limit behind a join rather than one scannable parameter, the corpus is built blind rather than to refute the naive read, the graded quantity is what the city commits next rather than what the utility will invoice, and no status word gates anything. The discriminators are buildable in this world: L1's sentence above; S8's conditioning property sits on the state list three joins from the session, on no column the ledger carries; O1's twin pair is the North and South decks, identical on every ledger-visible column and about 2x apart once replayed per car (99.6 against 50.8 kW in the note); O3's free training instance is the Library pedestal; L3's priced partial is the fleet-average limit, which lands at 110 kW, further off than the rung it corrects.

## Nearest exemplars

1. Capital Grant Drawdown Forecasting (Nonprofit & Grant-making), measured mean 0.34 over 4 runs. Nearest on the decisive trap: the stage schedule reproduces every paid certificate and every closed year to the pound because a schedule is re-aligned once an award starts drawing, so the 127 awards not yet drawing, forecast from it, exhaust the balance a year early. The same architecture as here: a basis certified on every closed case it can be checked on, applied to forward cases that differ on one hidden axis.
2. Outbound Warehouse Volume Planning (Supply Chain & Logistics), measured mean 0.44 over 4 runs. Nearest on decision shape and domain: one forward volume committed to a counterparty booking that cannot be changed once filed, sized as a service level rather than a central estimate; the model picked the right profile and sized the allowance on the wrong window or in the wrong form.

## Guard

Verdict against the corpus: WARN, exit 0, on the scratch card. Heart text similarity is 0.05 at most (task59 v2), and no persona warns (Danielle and Gerald, the two drawn first names that warned, were not used).

The note's draw as it stands was BLOCK on eight findings, each cleared by redrawing the axis named: ban.pattern A (task114), with test.same_puzzle and test.same_driver on (time, A), a signature spent in nine earlier builds with task107 inside the window, by recording the decisive pattern as E with A as the frame; ban.artifact monitoring_export (task116) by replacing the network operator's peak report with the electricians' sub-meter log; ban.forum customer_or_counterparty and ban.forcing_event purchase_order_or_contract (task114) by taking the agreement to the city council and forcing it with the switchover onto the new service. The (time, E) signature then repeated three older builds and is differentiated on the card: task37 (an absolute split recovered from a closed roll that cuts a count), task44 (a moderator measured over a prior window that flips gainers) and task97 (a place-history count carried through an account conversion), none of which is a per-unit rate cap that never bound under the old equipment and raises a coincident peak.

WARN answers:

- repeat.gate_g (forecasting, against task115): forecasting is the honest label for a forward peak under a pedestal regime the closed window never reached, and task115 reaches its forecast through a different decisive pattern (D, two grains of a store panel), so the label repeats and the driver does not.
- overuse.gate_g (5 of the last 12): forecasting is the most wanted objective's own mechanism and the honest one here; method_or_model_selection stays the supporting label, and promoting it would be a key chosen to dodge the count.

## Changes from the source note

1. Decisive pattern recorded as E (conditioned yield), with A as the frame. The note names S4 with L1, which this corpus encodes as A; A is banned against task114 and (time, A) is the most spent signature on file. The decisive rung reads honestly as conditioned yield: the rated draw and the Library pedestal's measured 11.0 kW are each correct and apply to no deck car, the North and South twins split on fleet mix, and the fleet-average partial lands further away than the rung it corrects. Design consequence: the Library pedestal is both the free training instance and the measured rate that does not transport, so the design stage adds a replay at its 11.0 kW as a grid cell and asserts its distance from the answer.
2. Context artifact: the network operator's monthly peak-kW report (monitoring_export, banned against task116) is replaced by the facilities electricians' monthly sub-meter log for the two deck charging panels (operations_log). Rung 0 keeps its construction (the highest all-hours monthly peak x 1.12 x 11.5/6.6, 373 kW in the note) and its kill fact (the tariff's on-peak billing clause). The account manager's voice that endorsed the peak report goes with it, and the design stage recasts the social layer as beliefs rather than an endorsed quantity.
3. Forum and forcing event: the utility receiving the contracted demand by 1 March (customer_or_counterparty, purchase_order_or_contract, both banned against task114) becomes the city council approving the service agreement, forced by the switchover of the decks onto the new dedicated service when the old pedestals come out. The 1 March filing date, the ratchet and the fixed charge per contracted kW stay as world facts.
4. Requester made explicit: the note says only that the division signs; the draw makes the requester the city's energy manager (procurement_lead), which carries Supply Chain & Logistics, sourcing-procurement, honestly (purchased service capacity committed to a single supplier under a ratchet).
5. Shape chosen: the note names none and reaches its 59 criteria mostly through garage-level asks A and B over all eight garages. The draw takes shape 02, so the criteria come from the contract year's monthly billed demand on the new service, which are components of the committed figure. Asks A to C are re-cut at the design stage: A and B cover garages the call does not touch (an H18 risk), and ask C names the four rung constructions with their hit counts in the prompt, which hands the ladder over.
6. World filled where the note is silent: geography (United States, Washington), the fiction's as-of date (2027-01-25, after the December 2026 settlement and before the 1 March filing), provisional invented names and six personas drawn with guard.py names.

## Stage 2: design (2026-10-09)

Every figure below is a target the generator builds forward and asserts. The targets were checked for feasibility on a scratch prototype of the session physics (three seeds, every cell reproduced); the prototype is not the generator and does not ship.

### What the design stage settled

1. **The source note's figures cannot all be true at once, so the ladder is re-derived.** A session replayed at any draw of 7.2 kW or more is charging only inside the span it charged at 6.6 kW, so in any quarter-hour a deck's replayed load is at most its closed load times the ratio of the draws. The note's North figure (99.6 kW replayed per car, against a closed on-peak maximum near 62.5 kW) breaks that bound for a deck of 7.2 kW cars. On random session draws the prototype also put the 11.5 kW replay and the per-car replay within a few per cent of each other and the fleet-average replay within 2 to 14 per cent of the answer. The design therefore builds the binding days by construction (one constructed peak day per month, one rung-2 day) and lets the seed decide texture only. The ladder becomes 410 / 310 / 115 / 110 / 150 kW filed (the note had 373 / 244 / 116 / 150.4). The stump sentence's 115 kW (116 unrounded), its 78 per cent and its 150 kW all survive unchanged.
2. **The answer moves from 150.4 to 149.07 kW unrounded.** The ratchet argues for rounding a contract up, and 150.4 would file 150 to the nearest 5 kW and 155 rounded up. At 149.07 both readings file 150 (convergence). The contracted figure is unchanged.
3. **The deck split is 99.0 against 50.1 kW** (the note's 99.6 against 50.8), reached with the permits the world has. South holds three 7.7 kW cars, so its share of the binding quarter-hour is three cars at 7.2 and three at 7.7.
4. **The averaged replays are separated by a band, not by luck.** Every long session on a month's constructed peak day ends after 12:32 at its own slow draw and before 11:58 at 9.75 kW. Inside that band the per-deck average (North 7.242, South 9.692 kW) loses South's slow cars and lands 35 per cent low, the fleet average (8.081 kW) keeps everyone charging and lands at least 26 per cent high, and the per-car replay sits between them.
5. **The binding quarter-hour is flat against the quarter-hour before it and above the one after it.** Reading the interval stamps as starts or as ends returns the same 149.07 kW (C1), and the binding quarter-hour is unique.
6. **Rung 2's maximum is set on a different day in a different month** (Wednesday 10 June 2026, nine late-morning sessions), so a solver at rung 2 names June 2027, not February 2028, as the month that sets the figure.
7. **The Library pedestal now pins the composition in both directions.** The enforcement vans, listed at 11.0 kW onboard, draw 11.0 kW on it; the fleet's one pickup, listed at 19.2 kW onboard, draws the full 11.5 kW on the same pedestal on a handful of days. Without the pickup, "11.5 kW units deliver 11.0 kW in service" fits every closed record and the 11.0 kW replay is a defensible reading (a Gate C fork). With it, the smaller of rating and onboard rating is the only rule in the swept family that reproduces every closed session.
8. **The asks are re-cut, as the draw's change 5 required.** The eight-garage availability and billing asks are retired as second decisions (H18), and the construction-by-construction ask is retired because it hands the ladder over. The ask layer is two device-carried audits inside the decision (the forecasting method's 2025 record and the 2026 basis against the panel meters), plus the monthly forecast the shape supplies. On-peak energy is dropped as a second monthly figure: it is coupled to the main construction and would put more cracker-banked weight on the rubric.
9. **The calibration corpus is built blind, not argumentative** (the concern the draw sections raised). On the decks the rated replay and the per-car replay return identical figures on all 72 deck-months, so the corpus reproduces the naive path's session model and never refutes it (L1). The only place the corpus scores the composition is the Library pedestal, a population the decision does not touch (O3).
10. **H18 read settled.** Every ask below names how its answer enters the call (component, qualifier or audit trail); none is a figure for another decision, window or owner.
11. **Kept as drawn:** the pairing, shape 02, the three deliverables and their names, the forum, the forcing event, the six personas, the calendar-first opening move.

### Gate G

- **Litmus.** No. Every figure in the pack is correct and stays correct: the settled sessions and their quarter-hour readings, the panel meters, the pedestal ratings, the rate schedule, the permit registry and the vehicle reference list. No stakeholder's claim about their own figures is overturned, and the task does not exist to correct a reading of a correct number. The committed figure is a forward quantity for equipment that is not yet installed, and the difficulty is that what a session draws on it is set by a property that no closed record at the decks ever exercised.
- **Primary mechanism:** `forecasting`, with `method_or_model_selection` supporting.
- **Flags:** `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`.
- **Deletion test.** Delete the panel log (rung 0's ready-made measure), the facilities engineer's belief, the utility's nameplate sizing and both distractors. The ledger still certifies "a session draws the pedestal rating until its energy is delivered" on all 72 deck-months, the 11.5 kW replay is still the natural sophisticated build, and it still files 115 kW.
- **Clean-data test, three depths, asserted in the generator per suspect file.** Fill: nothing on the main path is incomplete (the 2026 deck sessions, permits, vehicle checks and reference rows are complete). Semantics: every field means what the field notes say. Instrument: give every closed deck session a perfect meter and record every car's onboard rating on the session; no closed figure changes, because 6.6 kW is what the old pedestals offered and every deck car accepted it. On perfect records rungs 0 to 3 still return 410, 310, 115 and 110 kW, and only the session, permit, plate, vehicle and reference-list join reaches 150. Off-path suspect files (the 2024 gateway export, the restated 2025 versions, the re-delivered batches, the reissued identifiers) are repaired one at a time with the answer and rung 2 asserted unchanged.
- **Lens swap.** The naive read (rung 2) and the answer replay the same sessions under two physical models of a regime that has not happened. Rung 2's model is certified on the closed regime (6.6 kW pedestals, 2026) and the answer's departs from it only where the forward regime binds (11.5 kW pedestals, April 2027 to March 2028). Different regime and moment: not a lens swap.
- **Pre-draw identity.** Contracted demand = 1.12 × the maximum over billing quarter-hours of the sum, over concurrently charging sessions, of min(11.5 kW, the car's onboard rating). Its inputs ship, but the composition min(rating, onboard rating) is neither filed nor visibly forced on the decision's population: at the decks it never binds, and it is forced only at a pedestal the decision does not touch.
- **Corpus direction.** Under the naive path the corpus reproduces: rung 2's session model regenerates every closed deck reading to 0.001 kWh. It never refutes the naive read.
- **No shipped artifact ranks or sizes the decision wrongly as its own claim.** The panel log reports past panel maxima at all hours and is labelled in-file for panel loading; the utility's guide states its planners' method as a matter of record (the licensed wrong basis); the two distractors answer other questions.

### Entity, unit of value and decision

- **Entity and unit.** The City of Larch Harbor buys a dedicated service from North Sound Power & Light for the two Civic Center decks. It pays a fixed monthly charge on every contracted kilowatt for the contract year, plus energy, and a month whose billing demand exceeds the contract resets the contract to that month's demand for twelve months. It is scored on contracted kW (per active unit per period).
- **Two quantities that both read as size.** The decks' all-hours panel maximum (the electricians' maximum-demand registers, 105.6 kW a panel, every pedestal drawing 6.6 kW at once on a full morning) against the rate schedule's billing-hours maximum (158.4 kW closed, 12:00 on 17 February 2026). On the new equipment, the pedestal rating (11.5 kW a unit) against each car's onboard rating (7.2, 7.7 or 11.0 kW). They size the contract differently because the panel peak sits in the morning outside billing hours, and because the rating describes the pedestal while the draw is set by whichever of pedestal and car is smaller.
- **Decision.** One figure: the contracted demand for the first contract year of the new service (April 2027 to March 2028), in kW to the nearest 5 kW, filed with the utility by 1 March 2027 after the city council approves the service agreement on Tuesday 16 February 2027. Decision shape: one figure filed at a date, reached through a ladder of corrections with disciplined signs.
- **Forward facing.** The committed quantity is the maximum billing demand of a contract year that opens on 1 April 2027; nothing in it is retrospective.

### The answer

**150 kW** (149.072 kW unrounded): 1.12 × 133.1 kW, the per-car replay's coincident billing-hours maximum in the quarter-hour starting 12:00 on Tuesday 17 February 2026, the basis month of contract month **February 2028**. At that quarter-hour North carries 88.4 kW unscaled (eight county pool cars at 7.2 kW and four private cars at 7.7 kW) and South 44.7 kW (three cars at 7.2 and three at 7.7): **99.0 against 50.1 kW** after growth, 1.98 to 1.

- **Rank on the natural pipeline.** The answer is the fifth of five rungs; the natural pipeline (rung 0) files 410 kW, 177 per cent above it.
- **Margin.** The answer is a figure graded in 5 kW bins with no ranking to change, so the separation floor binds rather than the 1.20x rung-margin floor. Nearest wrong single-error cell: 10.7 per cent (the per-car replay with the growth factor left off, 133.1 kW, filing 135). Nearest wrong rung: 22.2 per cent (rung 2, filing 115).
- **Bins.** 149.072 sits 1.57 kW above the 147.5 edge and 0.93 kW below 150.0 (the round-up edge); at whole kW it is 149, 0.43 kW from 149.5. The flip condition: rounding up files 155 only if the binding quarter-hour gains 0.83 kW unscaled (one more car charging through two of its minutes), and rounding to the nearest 5 kW only if it gains 3.06 kW; the band forbids both and the generator asserts it.

### The ladder

Five rungs. Every figure is computed by the generator from the shipped records; filed values are to the nearest 5 kW.

| Rung | Construction | Lands on | Gap it opens | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The electricians' panel log read as ready-made: the highest month's two maximum-demand registers summed (211.2 kW, both panels at their 105.6 kW ceiling) × 1.12 × 11.5/6.6 | 412.16 kW, files 410, +176.5% | time (the billing window, G7) | The rate schedule's billing-demand clause counts only quarter-hours from 12:00 to 20:00 on weekdays outside its listed holidays |
| 1 | The billing-hours maximum rebuilt from the quarter-hour readings (158.4 kW at 12:00 on 17 February 2026) × 1.12 × 11.5/6.6 | 309.1 kW, files 310, +107% | rule (method: replay against scaling, G16) | The readings themselves: every session draws its full rate only until its delivered energy is reached and then nothing, so a faster unit shortens sessions instead of multiplying load |
| 2 | Each 2026 deck session replayed at the 11.5 kW rating from its plug-in until its delivered energy; coincident billing-hours maximum × 1.12 | 115.92 kW, files 115, −22.2%, set 10 June 2026 (contract month June 2027) | rule (the draw a session takes) | The network's only 11.5 kW pedestal, at Library Garage, has drawn 11.0 kW in every enforcement-van session since it went in, so the rating is not what a session on these units draws |
| 3 | The same replay at the Library pedestal's in-service draw, 11.0 kW | 110.88 kW, files 110, −25.6%, same June day | population (whose acceptance) | On that same pedestal the fleet's one pickup, listed at 19.2 kW onboard, drew the full 11.5 kW, and the vans' listed onboard rating is 11.0 kW: 11.0 is the vans' acceptance, not the pedestal's output |
| 4 | **Decisive:** each session replayed at the smaller of 11.5 kW and its own car's onboard rating, reached by session → permit → plate → checked make, model and year → the reference list's onboard AC rating; coincident billing-hours maximum × 1.12 | **149.07 kW, files 150** | time (a regime the closed window never reached) and population (each car) | none |

**Why each rung is a place to stop.**

- **Rung 0.** It is the city's own metered peak at the two panels the new service replaces, grown by the filed factor and scaled for the faster units. An energy manager with a deadline files it. (Measured trap #7, the ready-made measure.)
- **Rung 1.** It is the billing determinant at the grain the rate schedule names, rebuilt from meter-grade quarter-hour readings rather than read off a register, then grown and scaled. It looks like the careful version of rung 0.
- **Rung 2.** It is a session-level model the ledger reproduces exactly in every closed deck month (72 of 72 deck-months, every reading to 0.001 kWh), applied to the equipment the procurement specification names, and it agrees with the facilities engineer's expectation that the billing window empties. (Measured trap #13: validated on one population, applied to another.)
- **Rung 3.** It replaces a nameplate with a measured draw from the city's own 11.5 kW unit, which is what a careful engineer does with a nameplate the record contradicts.
- **Rung 4** is the answer.

"A solver who does everything right up to rung 2 commits to 115 kW and names June 2027 as the month that sets it."

- **Every rung a different figure:** 410, 310, 115, 110, 150. ✓
- **The rung that carries the stump:** rung 4 is the step the competent solver never takes; the stump lands at rung 2 (or rung 3 for a solver who opens the Library pedestal and stops at its median draw).
- **The seven survival properties for rung 4.** 1 Written nowhere: no document says what limits a session's draw; the procurement specification states the units' rating only, and the reference list ships because the permit office prices permits by body class. 2 No sweepable corpus nominates it on the decision's population: on the decks the rated and per-car rules tie on all 72 deck-months. The Library pedestal does score the composition (the O3 trade, made on purpose): it is one pedestal in a network of eight garages and its sessions are under 1 per cent of the ledger. 3 No arithmetic symptom: quarter-hour readings sum to session energy, sessions to the panel meters (net of the panels' lighting load), under every rung. 4 Not a row predicate: the figure is a maximum over billing quarter-hours of a sum over concurrently charging sessions, each re-timed by its own car's rating through a three-hop join. 5 The enumeration is arithmetic: which sessions are still charging at 12:00 on the new units is computed by re-timing; no column says so. 6 No cutover date: the pedestal swap is in the future and no closed series steps. 7 Survives deletion (above).
- **Worth of each rung on the graded quantity:** 0→1 −25.0%, 1→2 −62.5%, 2→3 −4.3%, 3→4 +34.4%.
- **Sign:** every correction walks the figure down, from 410 to 110; only the decisive rung turns it back up.

### Position table (asserted row by row)

| Rung | Unrounded (kW) | Filed | Against the answer | Month that sets it | North / South at its binding quarter-hour, scaled (kW) |
|---|---|---|---|---|---|
| 0 | 412.16 | 410 | +176.5% | any full-morning month (the registers sit at their ceiling in several) | 206.1 / 206.1 (each register 105.6, scaled) |
| 1 | 309.12 | 310 | +107% | February 2028 | 154.6 / 154.6 |
| 2 | 115.92 | 115 | −22.2% | June 2027 | 64.4 / 51.5 |
| 3 | 110.88 | 110 | −25.6% | June 2027 | 61.6 / 49.3 |
| 4 | 149.07 | **150** | 0 | **February 2028** | **99.0 / 50.1** |

No rung sits within 22 per cent of the answer. The twin pair separates only at rung 4: the decks are equal under rungs 0 and 1 and 1.25 to 1 under rungs 2 and 3, against 1.98 to 1 under the answer.

### Separation, the guard that binds

The answer is a figure graded in 5 kW bins, so the rung-margin floor (1.20x on a ranking) has nothing to act on and the separation floor binds: no cell reachable by one defensible reading lands within 10 per cent. The decisive rung is worth ×1.286 over rung 2 and ×1.344 over rung 3. The deck split is the one place a ranking exists, and there the per-car edge (North 1.98x South) sits against at most 1.25x under every rival construction.

### The correction grid

Window (all hours, billing hours) × draw construction (eight) = 16 cells, plus single-error cells off the answer, the licensed basis, partial applications and the nearest two-error cells. Every cell is computed and asserted by name.

| Cell | Unrounded | Filed | Against 149.07 | Violates |
|---|---|---|---|---|
| billing hours, draw 6.6 (no equipment change) | 177.41 | 175 | +19.0% | the procurement specification (the 6.6 kW units are removed) |
| billing hours, rating ratio | 309.12 | 310 | +107% | rung 1's kill |
| billing hours, fleet-average ratio (8.081/6.6) | 217.2 | 215 | +45.7% | the session model and the per-session car |
| billing hours, replay at 11.5 | 115.92 | 115 | −22.2% | rung 2's kill |
| billing hours, replay at 11.0 | 110.88 | 110 | −25.6% | rung 3's kill |
| billing hours, replay at the fleet average 8.081 | 188 or more (asserted ≥ +20%) | 190 | +26% or more | the per-session car (an average hides the slow cars that run past noon and keeps the fast ones charging) |
| billing hours, replay at each deck's average (7.242 / 9.692) | 97.3 | 95 | −34.7% | the per-session car |
| billing hours, replay per car | 149.07 | 150 | answer | |
| all hours, any of the eight draws | 236.5 (draw 6.6) to 412.2 (rating ratio) | | +58% or more (asserted ≥ +40%) | the billing-demand clause |
| per car, growth factor left off | 133.10 | 135 | −10.7% | the planning standard's factor |
| per car, decks' own maxima summed | 149.07 | 150 | converges | (both decks peak in the binding quarter-hour) |
| per car, stamps read as interval ends | 149.07 | 150 | converges | (11:45 equals 12:00 on the binding day) |
| per car, all 36 months instead of the latest twelve | 149.07 | 150 | converges | (2024 and 2025 per-car peaks are lower) |
| per car, rounded up instead of to the nearest 5 kW | 149.07 | 150 | converges | |
| per car, vehicles as renewed in January 2027 | 149.07 | 150 | converges | (no deck permit changed vehicle) |
| utility planners' sizing, 32 × 11.5 × 0.6 to the next 5 kW above | 220.8 | 225 | +48% | the service agreement (the customer states its own forecast maximum) |
| partial: per car on North, rating on South | about 99.0 | 100 | −34% | the per-session car on half the population |
| partial: per car on South, rating on North | about 105.7 | 105 | −29% | the same |
| partial: ratings only for the county pool cars | about 91.8 | 90 | −38% | the same |
| two errors: draw 6.6 and growth left off | 158.40 | 160 | +6.3% | two violations pointing opposite ways (L4) |
| two errors: fleet-average replay and growth left off | 168 or more | 170 | +12.7% or more | two violations |

The answer is not the extreme of the grid; it is bracketed, the shape L5 accepts. The natural stops and the averaged-per-deck replay sit 22 to 35 per cent below, and the early stops, the unchanged draw and the fleet-average replay sit 19 to 177 per cent above. Every single-error cell is at least 10.7 per cent away; the only nearer cell needs two filed-rule violations in opposite directions.

### The calibration corpus

- **Form.** A settled-transaction ledger: every settled session at the eight garages from January 2024 to December 2026, each with its quarter-hour energy readings (the spine, about 1.5 million reading rows), plus the session header and the network's field notes.
- **Cases.** 72 deck-months (36 months × 2 decks), each with every reading and its monthly billing-hours maximum; and the Library pedestal's sessions since January 2024.
- **What it certifies.** The session model: a session draws a constant rate from plug-in until its delivered energy is reached, then nothing, and plug-out never cuts a session short (every closed plug-out falls at least two hours after delivery would complete at 7.2 kW). Replayed at 6.6 kW the model regenerates every closed deck reading to 0.001 kWh and so all 72 deck-month maxima exactly. It refutes rung 1: no closed session's load scales with anything but its own draw.
- **What it is blind to, and why (the L1 sentence).** *In every closed session at the decks the car's onboard rating did not bind, because every deck pedestal was rated 6.6 kW and every deck permit vehicle is listed at 7.2 kW or more.* The rated rule and the per-car rule return identical readings on every one of the 72 deck-months; asserted twice, structurally (minimum listed rating over 2026 deck vehicles ≥ 7.2) and case by case (zero differing readings).
- **The free training instance (O3).** The Library pedestal, rated 11.5 kW, installed January 2024. About 700 enforcement-van sessions draw 11.0 kW (the vans' listed onboard rating); at least ten sessions by the fleet's pickup draw 11.5 kW (listed 19.2 kW). The pattern is visible there and harmless, because the Library service is far below its contract.
- **The swept family for the draw on a pedestal (C2), five rules over every closed session at all eight garages.** Smaller of rating and onboard rating: reproduces every session. Rating: misses every van session (about 98 per cent of Library sessions). Onboard rating: misses every deck session. Proportional derate fitted to the vans (0.957 × rating): misses every deck session (6.31 against 6.6 kW). Fixed 11.0 kW on 11.5 kW units: misses every pickup session. Energy is conserved under every rule, so no total can see the difference; the check is session by session, and the counts are asserted, not a floor of one.
- **The twin pair (O1).** North and South decks: 16 pedestals each, matched 2026 session counts, arrival, dwell and energy distributions, and the same closed billing-hours load at the binding quarter-hour (79.2 kW each at 12:00 on 17 February 2026; each deck's own 2026 closed maximum within 1 kW of the other's). Replayed per car: 99.0 against 50.1 kW, 1.98 to 1, reproduced from the raw records by the per-car rule and by no rival (1.00 to 1 under rungs 0 and 1, 1.25 to 1 under rungs 2 and 3).
- **Every rule the golden composes, and the case that breaks if it is flipped.** The session model: every closed reading. The composition: the Library vans (flip to rating), the pickup (flip to a fixed derate), the decks (flip to onboard rating). The billing window: the rate schedule (filed). The coincident sum: the one-meter clause (filed), and the binding day where both decks peak together. The growth step: the filed factor. The basis months: the planning standard (filed). The car behind each session: the permit and vehicle checks, unchanged through 2026 and the January 2027 renewal.
- **Resemblance points at the decoy.** The 2027 permit base matches 2026's within 2 per cent on every count (permits per deck, holder mix, vehicles), and 2026 is the year the rated replay reproduces exactly.
- **Ordinal agreement is defeated** by the twin pair: two decks no ledger column separates, 1.98 to 1 apart under the answer, have no defensible ordinal reading under any rival.

### Pins and counter-pins

**Filed pins**, each stated once, in one file, as a rule and never argued:

| Pin | File (provisional name) | Authority |
|---|---|---|
| Billing demand is the highest average kW in any quarter-hour beginning 12:00 to 19:45, Monday to Friday, outside the listed holidays (with observed dates); contract demand in 5 kW steps; a fixed monthly charge per contracted kW; the twelve-month ratchet; billing month = calendar month for interval-metered service | the utility's new-service rate schedule (PDF) | 2, rate schedule |
| A forecast for a new or altered service starts from the latest twelve closed months at the equipment the service will supply, month by month, and applies the county's EV registration growth factor to each month's demand and energy; a factor applies to forecasts made after its adoption date; factor history table (2027 planning year: 1.12) | the city's facilities load forecasting standard (PDF) | 1, governing standard |
| The service supplies the two decks' 32 pedestals and nothing else, through one meter; energization on or about 1 April 2027; the first contract year is the twelve billing months from April 2027; the customer states the maximum billing demand it expects in that year | the draft service agreement (DOCX), with the replacement units as an exhibit (32 single-port units, 48 A at 240 V, 11.5 kW) | 2, contract |
| Both decks are permit-only; one vehicle per permit, checked against registration at issue and renewal | the permit rules, as the permit registry's header | 1 to 2 |
| quarter-hour stamps mark the interval's start, in local civil time with offset; demand = 4 × quarter-hour kWh; an authorization code identifies one settled charge and survives re-delivery | the network's export field notes (TXT) | 4, field semantics |
| The utility's planners size an EV service on connected nameplate × a diversity factor (0.6 for 21 to 40 units), state it to the next 5 kW above, and present it at the service review | the utility's new-service planning guide (PDF) | 2, the utility's own method: the licensed wrong basis |

**Empirical pins.** The session model (every closed reading); the composition (the Library pedestal against the decks); each car's onboard rating (session → permit → plate → checked vehicle → reference list).

**Counter-pins.** None at or above the planning standard. The utility's guide states the utility's method for its own planning, and the service agreement makes the contracted figure the customer's forecast maximum, so the guide is outranked for this filing and is graded as the figure the planners will raise. The panel log is labelled in-file as the panels' maximum-demand registers, all hours, read and reset monthly for loading checks. The facilities engineer's expectation is a belief in the social layer. The replacement-unit exhibit states the units' rating only. Anti-signpost rule for every document: no shipped sentence says what limits a session's draw, and none names the vehicle as a factor in charging power.

### Fork grid: the 22-axis closure table (determinism-check A.5)

| # | Axis | Reading chosen | Closed by |
|---|---|---|---|
| 1 | Population | The 2026 settled sessions at the 32 deck pedestals, including the few fleet-card top-ups there | Filed (service agreement scope, permit rules) + C1 (weekend, holiday and night sessions cannot enter a billing quarter-hour; no fleet-card session at the decks touches a month's peak day) |
| 2 | Unit of account | The combined service's coincident quarter-hour demand | Filed (one meter; quarter-hour demand) + C1 (each deck's own per-car maximum falls in the binding quarter-hour, so summing the decks' maxima returns 149.07) |
| 3 | Attribution window | Each contract month from the same calendar month of 2026 | Filed (planning standard) + C1 (no session on any month's peak day spans midnight) |
| 4 | As-of dating | The car checked for the session's permit | C1 (no 2026 deck permit changed vehicle in 2026 or at the January 2027 renewal; session-date and current readings return the same car) |
| 5 | Version basis | One version per 2026 deck session | C1 on the main path (restated versions exist only in May to July 2025, off path) |
| 6 | Divisor and denominator | None in the call (a maximum) | C1 (no ratio enters the figure; the 78 per cent share is reported, never used) |
| 7 | Weighting | Each session at its own draw | C2 (the composition is per session) + C4 (fleet average +26%, deck averages −35%) |
| 8 | Window length | The latest twelve closed months | Filed (planning standard) + C1 (the 36-month per-car maximum is 2026's) |
| 9 | Boundary inclusivity | Quarter-hours beginning 12:00 to 19:45 | Filed (rate schedule) + C1 (11:45 equals 12:00 on every month's peak day; no deck load after 19:00) |
| 10 | Rounding path | Full precision to the end; 5 kW at the call; whole kW per month | C1 (full quarter-hours are exact at 0.001 kWh; growth is linear; nearest and round-up both file 150; every monthly figure at least 0.2 kW from a half-kW edge, asserted) |
| 11 | Tie-break | The binding quarter-hour and month | C1 (12:00 strictly above 12:15 on 17 February; February 149.07 against January 131.82, 13.1% clear) |
| 12 | Maturity | Every 2026 month complete | C1 (every 2026 session settled by 10 January 2027; the extract is dated 18 January 2027) |
| 13 | Order of operations | Growth after the maximum; coincident sum before it | C1 (linear scaling; one quarter-hour) |
| 14 | Row order | Any | C1 (sums and maxima) |
| 15 | Duplicate resolution | None needed on the main path | C1 (no 2026 deck record is a re-delivery; genuine same-day repeats in 2026 never touch a peak day, so a blanket dedup cannot move the call) |
| 16 | Identity normalisation | Plate and make-model-year as written | C1 (every 2026 deck plate matches its check row character for character; every checked vehicle resolves to exactly one reference row) |
| 17 | Netting against gross | None | C1 (no reversing records at the decks in 2026) |
| 18 | Dimensional units | kW = 4 × quarter-hour kWh | Filed (field notes, rate schedule) + C4 (the quarter-hour kWh read as kW files 37 kW, a quarter of the answer, violating the billing-demand definition) |
| 19 | Code and status semantics | Account type, permit status | C1 (every 2026 deck session's permit is active on its date; account types never change a draw) |
| 20 | Integerisation | The 5 kW step | C1 (nearest and round-up agree) |
| 21 | Scope of a stated clause | Growth applies to each month's demand and energy; the ratchet to billing demand above contract | Filed (planning standard, rate schedule); the forecast maximum sits under the contract, so the ratchet never fires in the forecast |
| 22 | Forward window contents | Twelve billing months from April 2027, each from its 2026 month | Filed (service agreement, planning standard) + C1 (the 2027 permit base and vehicles match 2026's; no deck pedestal added or removed) |
| + | The draw on the new units (the decisive axis) | min(11.5 kW, onboard rating) per session | C2 (unique survivor of the five-rule family above) + C4 (every rival construction at least 10.7% away) |
| + | Clock | Local civil time with offset; the binding day in standard time | Filed (field notes) + C1 (no peak day falls on a DST change) |

### Deliverables and the criteria arithmetic

Shape 02, forecast across many periods: the twelve contract months are the repeated unit and the contract is their maximum.

1. **`contract_demand_note.pdf`**, one page, commits. The contracted demand (150 kW); the contract month that sets it (February 2028); every contract month's forecast billing demand in whole kW (April 2027 115, May 106, June 98, July 90, August 91, September 108, October 116, November 124, December 130, January 2028 132, February 2028 149, March 2028 123); the kW each deck carries in the quarter-hour that sets it (North 99, South 50); the figure the utility's planners will put up (225 kW) and the gap to ours (75 kW). 1 + 1 + 12 + 2 + 2 = **18 criteria**.
2. **`deck_load_day.png`**, rendered by the script. The day behind the figure (17 February 2026, the basis of February 2028) by quarter-hour; what the decks drew that day and the forecast load on the new units as two series; the contracted figure as a line carrying its value (150 kW); the quarter-hour that sets it marked (12:00, 149 kW); a title a councillor can quote. **6 criteria.** The billing-window shading was cut from the ask because naming the billing hours hands over rung 0's kill; the golden may still shade the window as presentation.
3. **`civic_service_demand.xlsx`**, written by the script. The method's 2025 record (each month's forecast of the decks' billing demand from 2024 in whole kW, and how far over or under the actual it came as a percentage of the actual to one decimal, signed: 24) and the 2026 basis against the panel meters (for each deck panel and each of its twelve 2026 readings, the metered kWh the sessions charged through that panel leave unaccounted for: 24). **48 criteria.**
4. Three files named as asked: **3 criteria.**

**Total about 75 against the floor of 25**, before the rubric generator samples. Script-generated: the chart and the workbook, and the note's table. Unit and rounding: the contract to the nearest 5 kW and the misses to one decimal stated in their own sentences; every other figure is in kW or kWh by a single convention sentence (H12). Distinct findings: the forward maximum and its month (a forecast), the deck split (a decomposition at one quarter-hour), the method's record (validity), the basis against the meters (a cross-file reconciliation). Named-parts visual ✓; breakdown at an explicit grain (panel × reading) ✓; robustness check (the 2025 record) ✓. Over-determination sweep: no ask states the per-car draw, a car's rating, a deck's fleet mix or the binding day's composition, and the deck split cannot be inverted into per-car ratings (two totals, eighteen cars).

### The ask ledger (supplemental-stumping)

**The main call's declared row population.** Session-header rows plugged in during 2026 at the 32 identifiers the pedestal register's 2026 rows place at the two decks, and their reading rows; the permit rows those sessions carry, their vehicle-check rows and the reference rows those vehicles resolve to; the rate schedule's billing-window clause and 2026 holiday list; the planning standard's basis clause and its 2027 factor row; the service agreement's scope, meter, contract-year and exhibit clauses. **Zero device rows and zero hazard rows inside it** (counts below, asserted).

**Pool A, the construction layer, coupled and device-free because its rows are the main call's rows.**

| Ask | Answer and use | Enters the call as | Stops | Files |
|---|---|---|---|---|
| A1 the twelve contract months' forecast, the month that sets the figure, the deck split | 12 monthly figures as listed above; February 2028; 99 / 50. Council reads the year behind the number | its components | rung 2: eleven months between 13 and 26 kW and June 116; draw 6.6: February 177; rung 1: February 310; answer | sessions, readings, pedestal register, permits, vehicle checks, reference list, rate schedule, planning standard, service agreement, field notes (10) |
| A2 the chart's values | the day, the 150 kW line, the 149 kW quarter-hour marked | its presentation | as A1 | as A1 |

The cracker banks pool A. The design keeps it to the twelve monthly figures, the split and three chart values, and puts the monthly forecast in the committing note as the figure's basis, so the generated rubric is steered to score it with the recommendation.

**Pool B, device-carried and decoupled.**

**B1. The 2026 basis against the panel meters.** For each deck's panel meter and each of its twelve 2026 readings, the metered kWh that the sessions charged through that panel leave unaccounted for (whole kWh; 24 figures).
- *Use:* the energy manager checks that the sessions the forecast is built from account for what the meters saw before signing; a basis that leaked sessions would understate every month. *Enters the call as* the audit trail of its input.
- *Construction layer:* the session energy delivered through each panel between two readings, cut at the reading instants from the quarter-hour readings (2026 deck rows, read only, clean).
- *Primary device, D8 meter clock (silent):* both deck sub-meters keep standard time all year, stated once in the meter nameplate record, and the electricians log the meter's own displayed time. From the 31 March read to the 30 October read every logged time is an hour behind civil time, so reading spans cut in civil time shift by the energy delivered in the offset hour at each end. Every time parses and every total ties; it moves readings 3 to 11 on both panels (18 figures), each by at least 2 kWh (asserted).
- *Hazards:* H1 (the re-delivered December 2025 batch, reading 1 on both panels); H4 (the back-fed unit, North readings 6 and 7); H5 (the double read, South reading 12).
- *Over-cleaning half:* genuine same-day repeat sessions in 2026 (unplug and replug, distinct authorization codes, never on a peak day); a dedup on permit, pedestal and day drops them and lands each affected reading low.
- *Ladder stops per reading:* calendar months for reading spans; civil-time spans (clock missed); panel by deck name (back-feed missed); re-deliveries kept; repeats over-deduped; golden. Every stop at least 2 kWh from the golden, every subset of mishandlings outside ±1 kWh.
- *Separation line:* the meter log, the nameplate record, the work orders and the register's circuit-assignment rows are outside the main call's population; the re-delivery is dated 2025; the double read is a log row. Zero device rows in the population.
- *File path (causal):* panel meter log (XLSX), meter nameplate record, session header, quarter-hour readings, pedestal register (circuit assignments with effective dates), electrical work orders, export field notes: **7 files, one short of the floor**, recorded as a debt for stage 3 to close causally or re-cut, never by padding. *Columns (13):* read time, kWh register, meter, clock mode, pedestal, plug-in, plug-out, delivered kWh, authorization code, reading start, reading kWh, circuit panel, effective from and to.
- *Free figures:* reading 2 on both panels and North reading 12 (3 of 24). The panels also carry deck lighting, so the unaccounted energy is not computable from any document (no oracle).

**B3. How the forecasting standard did in 2025.** For each month of 2025, the standard's forecast of the decks' billing demand made from 2024 (whole kW) and how far over or under the actual it came, as a signed percentage of the actual to one decimal (24 figures). The prompt says "billing demand", never "billing hours", so the ask does not name the window.
- *Use:* council will ask how far to trust the method behind the number; this is its record on the same decks. *Enters the call as* its qualifier (the method's validity check).
- *Construction layer:* the 2024 and 2025 coincident billing-hours maxima at the decks under the old units (the same window and coincidence logic as the call, no draw question), and the growth step.
- *Primary device, D7 reissued identifiers (silent):* at the April 2025 platform move the network renumbered every pedestal, and six retired deck identifiers were later reissued to new units at two other garages. Sessions before the move carry the old identifiers; the pedestal register keeps each identifier's assignments with effective dates. The raw identifier join sends some 2024 and early-2025 deck sessions to other garages, and the current-identifier filter drops them: both silent paths land on wrong 2024 bases (all twelve forecasts) and wrong January to March 2025 actuals, so all 24 figures move.
- *Hazards:* H2 (the factor vintage, all 24 figures); H3 (the restated versions, May to July); H1 (the re-delivered batches, October and December); H6 (gateway B, January to April).
- *Two-signed:* the golden misses lie within ±3.0 per cent, at least four each way; under every subset of mishandlings the naive misses stay two-signed with a mean inside ±1.5 per cent, so no path reads a bias in the growth step into the 2027 call (asserted).
- *Ladder stops:* raw identifier join; current-identifier filter; factor 1.09; latest version kept; re-deliveries kept; gateway B left out; golden.
- *Separation line:* every device row is dated before 2026 or sits in the factor history's 2025 rows; no 2026 identifier is reissued, and every 2026 deck session resolves to one register row under the raw and the effective-dated join alike. Zero device rows in the population.
- *File path (causal):* session header, quarter-hour readings, pedestal register (identifier history), version acceptance log, gateway B legacy export, forecasting standard (factor history), rate schedule (window and 2024 to 2025 holidays), export field notes: **8 files**. *Columns (15):* pedestal, plug-in, plug-out, delivered kWh, version, authorization code, reading start, reading kWh, register identifier, garage, effective from and to, acceptance status, factor, adoption date, holiday dates.

**Hazard table.**

| Hazard | Family | Asks it moves | Move per figure (asserted) |
|---|---|---|---|
| H1 re-delivered batches, October and December 2025: re-sent records under new session identifiers keep their authorization codes; genuine repeats carry their own | D1 | B1 reading 1 (both panels); B3 October and December | ≥ 5 kWh; ≥ 1.5 kW |
| H2 factor vintage: 1.08 adopted September 2024, revised to 1.09 in April 2025 for forecasts made after it | D2 | B3, all 24 | ≥ 1 kW at whole kW and ≥ 0.1 point |
| H3 restated sessions at four South units, May to July 2025: version 2 accepted, version 3 rejected in the acceptance log | D2 | B3 May to July | ≥ 1.5 kW |
| H4 one North unit back-fed from the Library panel, 1 June to 12 July 2026 (register circuit row plus a work order) | D7 | B1 North readings 6 and 7 | ≥ 100 kWh |
| H5 the South panel read twice on 31 December 2026, the later reading standing by the log's own rule | D2 | B1 South reading 12 | ≥ 20 kWh |
| H6 four North units' January to April 2024 sessions in the gateway B legacy export only | D4 | B3 January to April | ≥ 1.5 kW |

Primaries do not repeat a family (B1 D8, B3 D7). **The one referee:** the panel log's monthly energy for 2024 and 2025, byte-clean, which shows a deck session set falling short of its meter without handing over any billing-hours level (the lighting load blurs it to a few per cent). The generator asserts the re-deliveries, restatements and back-feed never touch a panel's all-hours maximum quarter-hour, so the maximum-demand registers referee nothing.

**Pair arithmetic (supplemental-stumping Part 0).** Planning weights 38 / 7 / 55; `L` is the share of pool-B weight a top response still earns.

- *Leakage estimate.* B1: a strong response that executes every visible hazard but misses the meter clock keeps 6 of 24; one that misses everything keeps 3. B3: a response that misses the reissued identifiers keeps none, whatever else it gets right, because the primary moves every figure. A strong response therefore leaks about 0.125 of pool B, and both top responses are expected near that.
- *Scenario (i), the monthly forecast scored with the recommendation* (the steer above): r is the planners' 225 kW, about 2 points. Asks are B1, B3 and the three chart values. Cracker 38 + 7 + 3.2 + 51.8 L; mirror 2.1 + 7 + 51.8 L. At L = 0.2 the pair averages **39.0**; at L = 0.125, 35.1.
- *Scenario (ii), the monthly forecast scored as asks:* pool A takes 15 of 63 ask criteria (13.1 points), r rises to about 6.3. At L = 0.2 the pair averages **44.1**; at L = 0.125, 40.9. That clears the bar of 50 and misses the target of 40.
- *No response on the call:* each top response scores about r + 7 + 41.9 L, so the pair averages near **22**.
- *What the pass condition rests on:* at most one response on the call (the ladder), pool-B leakage at or under 0.2 per top response, and the committing note carrying the monthly forecast as the figure's basis. If a round shows scenario (ii) above 40, the repair is more pool-B weight in this layer (B3's actual peaks as a third column, 12 more figures under H1, H3 and the primary), never a change to the ladder.
- *Reachability:* c, the share of ask weight reachable from a landed call, is the chart's three values in scenario (i) (about 6 per cent) and pool A in scenario (ii) (about 24 per cent).
- *Decoupling, asserted:* recompute every pool-B answer with the per-car rule replaced by the rated rule; every B1 and B3 figure is unchanged.

### Assertion plan (53, generator and independent verifier)

Main call and ladder:
1. The answer: 149.072 kW unrounded (±0.001), 150 to the nearest 5 kW and 150 rounded up; 1.572 kW above the 147.5 edge and 0.928 below 150.0.
2. Binding quarter-hour 12:00 on 17 February 2026; the 11:45 quarter-hour equals it; the 12:15 quarter-hour is lower.
3. North 88.4 and South 44.7 kW unscaled at the binding quarter-hour; North over South between 1.9 and 2.1.
4. Each deck's own per-car maximum falls in the binding quarter-hour.
5. The twelve monthly per-car figures equal their targets (131.824, 149.072, 123.200, 115.136, 105.952, 97.888, 89.824, 90.944, 108.192, 116.256, 123.760, 130.144 for January to December 2026), each at least 0.2 kW from a half-kW edge and all distinct at whole kW.
6. The runner-up month (January) at most 0.90 × the binding month.
7. Rung 0 = 412.16 kW: both panels' maximum-demand registers reach 105.6 kW (16 × 6.6) in the highest month, and no register ever exceeds it.
8. Rung 1 = 309.12 kW (closed billing-hours maximum 158.4 kW, 24 cars at 6.6).
9. Rung 2 = 115.92 kW, set on 10 June 2026 (nine sessions at 11.5).
10. Rung 3 = 110.88 kW, same day.
11. Each rung's month that sets it: rungs 1 and 4 February, rungs 2 and 3 June (rung 0's registers sit at their ceiling in several months, so its month is not asserted).
12. Draw 6.6 kW, billing hours: 177.41 kW.
13. Fleet-average ratio: 217.2 kW.
14. Fleet-average replay at least 20 per cent above the answer.
15. Deck-average replay 97.3 kW, at least 15 per cent below.
16. Growth left off: 133.10 kW.
17. Every single-error grid cell at least 10 per cent from the answer, by name; the convergent cells equal it exactly.
18. Every partial-application cell (per car on one deck, ratings only for the pool cars) at least 15 per cent away.
19. The two-error cells: nearest 6.3 per cent, both violations named, opposite in sign.
20. The 36-month per-car maximum equals 2026's.
21. Per car on the January 2027 renewal vehicles = 149.072.
22. The utility planners' figure 225 kW (220.8 to the next 5 kW above); gap 75 kW.

Corpus, composition and twins:
23. Rated and per-car rules identical on all 72 deck-months, reading by reading (zero differences).
24. Every 2026 deck vehicle listed at 7.2 kW or more (structural blindness).
25. The five-rule family over every closed session: the composition reproduces all; rating misses every van session; onboard misses every deck session; proportional derate misses every deck session; fixed 11.0 misses every pickup session; family size 5, miss counts printed.
26. Library pedestal: every van session at 11.0 kW, every pickup session at 11.5 kW, at least ten pickup sessions.
27. Twins: 2026 per-deck session counts within 2 per cent, arrival, dwell and energy distributions matched (two-sample KS statistic under 0.05), each deck's own 2026 closed maximum within 1 kW, closed loads equal on the binding day, per-car ratio at least 1.8.
28. Fleet shares: 57 of 73 deck vehicles at 7.2 or 7.7 kW (78.1 per cent); 44 of 48 North permits held by the county motor pool (91.7 per cent); 16 of 25 South vehicles at 11.0 kW (64.0 per cent).
29. Every closed plug-out at least two hours after delivery would complete at 7.2 kW.
30. Every session's readings sum to its delivered energy (0.001 kWh).
31. No session on any month's peak day spans midnight; no deck load after 19:00 on any peak day.
32. Every 2026 deck session's permit active on its date; one vehicle per permit through 2026 and the January 2027 renewal.
33. Every 2026 deck plate matches its check row character for character; every checked vehicle resolves to exactly one reference row.
34. Every 2026 session settled by 10 January 2027; extract dated 18 January 2027.
35. No tariff holiday carries deck load above 20 per cent of its month's peak (the holiday reading converges).
36. Every 2026 deck identifier resolves to one register row under the raw and the effective-dated join.

Separation, Gate G and the ask layer:
37. Zero device and zero hazard rows inside the main call's population, one count per device.
38. Clean-data test per suspect file (gateway B merged, identifiers resolved, accepted versions kept, re-deliveries removed, meter clock corrected, double read resolved): answer and rung 2 unchanged; answer ≠ rung 2.
39. Lens-swap: rung 2 and the answer differ only through the draw on the forward units (the closed replay is identical under both rules).
40. B1 golden for all 24 figures; each device moves its readings by its stated minimum; the meter clock moves every one of readings 3 to 11.
41. B1 every subset of mishandlings outside ±1 kWh of the golden on every device-carrying reading.
42. B1 lazy path lands on its first stop on every reading; the hygiene battery on the wrong path comes back clean (unique session identifiers, no unmatched joins).
43. B3 golden for all 24 figures; misses within ±3.0 per cent, at least four each way.
44. B3 naive misses two-signed with a mean inside ±1.5 per cent under every subset of mishandlings.
45. B3 the raw identifier join, the current-identifier filter and the 1.09 factor each move every figure (at whole kW or 0.1 point).
46. Decoupling: every B1 and B3 figure unchanged with the per-car rule replaced by the rated rule.
47. The re-deliveries, restatements and back-feed never touch a panel's all-hours maximum quarter-hour.
48. Pair simulation from the generated rubric once it exists: cracker and mirror sheets, the pair at or under 40 in scenario (i) and under 45 in scenario (ii).

Pack:
49. Input gates: at least 10 files, at least 3 formats, the reading spine at least 25,000 rows, at least two distractors named in `metadata.json`.
50. Anti-signpost grep over every shipped document: no sentence about what limits a session's draw or about the vehicle setting charging power (the reference list's column header excepted).
51. No headline figure on a round boundary; no share an exact round figure in a shipped document.
52. Two consecutive builds byte-identical.
53. H20: the prompt still carries "service agreement", "contracted demand", "North Sound Power & Light" and "I buy power", the nouns that make the sourcing-procurement decision visible, and none of "billing hours", "onboard" or "accept".

### Realism debts

1. **Large top-ups on the constructed peak days** (long sessions of about 25 to 45 kWh): forced because the band needs sessions still charging after 12:32 at 7.2 kW and finished before 11:58 at 9.75 kW. Mitigation: the peak days are winter and post-holiday days (17 February is the Tuesday after Presidents' Day; county pool cars return from field runs), background sessions stay at 10 to 20 kWh, and the generator asserts no visible gap in closed-record end times.
2. **92 per cent of North's permits held by one agency's pool cars.** A county motor pool leasing a block of permits; stated in the registry's holder column and nowhere else.
3. **Every month's peak day shares the band's structure.** Texture varies arrival times, counts and car mix month by month.
4. **Twins identical in distribution by construction.** Both decks are permit-only in one complex and draw from one workforce.
5. **The pickup's sessions on the Library pedestal** (at least ten over three years) are the only evidence that pedestal delivers its rating; they read as an occasional borrower.
6. **Sub-meters on standard time all year** are common where DST was disabled at install; stated once in the nameplate record.
7. **The vehicle reference list and the fictional county (H22).** Either a real public vehicle-spec source shipped exactly as published, with any constructed rows in their own declared file, or a city reference table declared as constructed. Real models are used only where their published onboard rating matches the class (7.2, 7.7, 11.0, 19.2 kW); otherwise the dataset stage re-tunes and re-asserts every cell. Invented names (city, county, garages, utility, network) go through the H21 check.
8. **Deck lighting on the charging panels** is what keeps the unaccounted energy from being computable; it is ordinary for a deck panel and is stated in the panel schedule only.

### Stopping rule (written before any round)

- **At ceiling:** two consecutive in-house rounds or portal results in which a response files 150 kW through the per-car join, by different routes. The scenario is then a computation; re-root the ask at stage 1 and move this architecture into the card's lineage.
- **One more repair:** a response files 150 by a route that skips the per-car join (a partial cell landing in the bin, a guess), or the pair clears 40 with at most one response on the call (a pool-B repair, one device per repair), or a response defends rung 3 from a reading of the Library pedestal that the pack does not refute (a determinism repair, never a difficulty one).
- **Working as built:** responses that stop at rung 2 or rung 3, including ones that open the Library pedestal and take its median draw.

### Pack plan (stage 3 builds against it; names provisional, in the organisations' own idiom)

| Role | File | Format | Used by |
|---|---|---|---|
| Spine | quarter-hour readings, eight garages, 2024 to 2026 (`session_intervals_2024-2026.parquet`) | Parquet | call, B1, B3 |
| Operating extract | settled session header (identifier, authorization code, version, pedestal, account, permit or fleet card, plug-in, plug-out, delivered kWh, settled at) | CSV | call, B1, B3 |
| Operating extract | the parking office's acceptance log for restated settlement versions | CSV | B3 |
| Operating extract | gateway B legacy export, January to April 2024 | CSV | B3 |
| Dimension | pedestal register: identifier history with effective dates, garage, rating, idle draw; circuit assignments as their own effective-dated rows | CSV | call, B1, B3 |
| Context artifact | the electricians' monthly deck panel log: read time (meter clock), kWh register, maximum-demand register, reset | XLSX | rung 0, B1, referee |
| Dimension | deck sub-meter nameplate record (meter, panel, CT ratio, clock mode) | CSV | B1 |
| Operating extract | facilities electrical work orders, 2026 | CSV | B1 |
| Dimension | parking permit registry (permit, deck, holder, holder type, plate, issued, renewed, status) | CSV | call |
| Dimension | permit vehicle checks (plate, VIN, make, model, model year, checked on) | CSV | call |
| Dimension | vehicle reference list (make, model, model years, body class, onboard AC rating) | CSV | call |
| Dimension | city fleet roster (unit, fleet card, department, make, model, year) | CSV | the Library composition |
| Governing document | the utility's new-service rate schedule | PDF | call, B3 |
| Governing document | the city's facilities load forecasting standard, with its factor history | PDF | call, B3 |
| Governing document | draft service agreement, with the replacement units as an exhibit | DOCX | call |
| Licensed wrong basis | the utility's new-service planning guide | PDF | the planners' figure |
| Dictionary and provenance | the network's export field notes and the parking office's data-sources note | TXT | all |
| Social layer | the council briefing thread (the facilities engineer's expectation, the utility planner's remark, as beliefs) | EML or DOCX | none (pressure only) |
| Distractor | Civic Center building electricity statements, 2024 to 2026 (whole building) | CSV | none |
| Distractor | the network's charger status events, all eight garages, 2026 | CSV | none |

About 19 files in six formats; the dataset stage may merge the two notes or fold the social layer into the agreement's cover email to sit nearer the median.

## Tried and rejected

- Stage 2, the source note's figures as one set (twins within 1 kW closed, 99.6 against 50.8 kW per car, rung 2 at 116, answer 150.4): infeasible, because a session replayed at 7.2 kW or more charges only inside its 6.6 kW span, so a deck's replayed load in a quarter-hour is at most its closed load times the draw ratio; North's 99.6 breaks that bound.
- Stage 2, twins drawn at random from one session distribution: the 11.5 kW and per-car replays converged (late arrivals charge into the window under every draw) and the fleet-average replay landed 2 to 14 per cent from the answer; replaced by one constructed peak day a month inside a band (after 12:32 at the car's draw, before 11:58 at 9.75 kW).
- Stage 2, the answer at 150.4 kW: under a ratchet a solver can round up, and 150.4 files 155 that way against 150 to the nearest 5 kW; moved to 149.07, where both readings file 150.
- Stage 2, a Library pedestal used only by 11.0 kW vans: "11.5 kW units deliver 11.0 in service" then fits every closed record, which makes the 11.0 kW replay a defensible reading (a Gate C fork); a pickup drawing the full 11.5 kW on the same pedestal was added.
- Stage 2, the source note's asks A and B (availability and billing at all eight garages) and C (the figure under each construction with its hit count): A and B answer decisions the call does not make (H18), and C hands the ladder over; all three retired.
- Stage 2, on-peak energy as the second figure per contract month: coupled to the main construction, so it adds weight the cracker banks and the mirror loses; dropped in favour of device-carried audits.
- Stage 2, a panel residual made only of the pedestals' idle draw: computable from the register alone, which hands over the residual and, by subtraction from the meter, the session energy (an oracle); deck lighting on the panels replaces it.
- Stage 2, the 2024 legacy export on standard time as the back-test's device: it shifts every daylight-time month the same way, so the naive back-test reads as a one-signed bias a solver could carry into the 2027 growth step; replaced by reissued pedestal identifiers.
- Stage 2, a sixth rung on the county's EV registration mix (trap #14, the coarsened segment): it needs a registration file only that rung uses and is a weaker stop than the permit registry a solver opens anyway; not built as a rung.
- Stage 2, the fleet-average replay as a rung: its kill fact is the same per-session join that reaches the answer, so it is a priced partial (L3) in the grid, not a rung.
