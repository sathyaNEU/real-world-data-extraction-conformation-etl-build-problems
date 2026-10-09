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

Restated at harden loop 2 (2026-10-09). The stage-1 stump (115 kW from the rated replay, 150 kW per car) died in round 1 and the harden-loop-1 stump (150 kW from each session's car on its own date) died in round 2; both records are in `## Tried and rejected`.

A competent solver rebuilds the tariff's billing maximum from the interval readings, replays every 2026 deck session record on the new units at the smaller of 11.5 kW and the onboard rating of the car its permit carries in the contract year (each permit's January 2027 renewal check), a model that reproduces every closed reading at 6.6 kW, grows by the filed 1.12 and files 155 kW (155.357 unrounded, 160 rounded up, set at 12:00 on Tuesday 8 December 2026); the step that lands it there is replaying each settlement record as a charge of its own: Curbline's daily settlement run, starting at 10:00 a.m., closes every session still charging and carries the charge on in a new record from that second at the same unit under the same permit or card, so record by record each charge's second record restarts at the run at the car's full new rate, and cars that finish before noon as one charge are back on the meter at noon; joined back into charges (3,033 zero-gap pairs at the decks in 2026, the only reading whose charge counts reproduce every permit-month of Parking Services' 2026 charging statements), the contracted demand is 130 kW (129.136), set in the same quarter-hour.

## Decisive rung

Restated at harden loop 2 (2026-10-09). Measured trap #2, counts file rows instead of the real unit (`.claude/skills/stumping/references/traps/_measured.md`): established, decided 11 of the 64 measured client tasks, 7 of them under 0.50; its recipe is a unit the domain defines that no file stores directly, records shipped at a finer grain so the unit has to be built by linking rows, and a published figure computed on the true unit so the grain can be tested. Here the unit is the charge (one car's continuous connection at one unit), the file row is the settlement record, and Curbline's daily settlement run splits every charge still running when it reaches the garage (10:00 to 10:07 a.m.) into two records that meet end to start at the same unit under the same permit or card. The published figure is Parking Services' 2026 charging statements, whose charge counts reproduce on all 875 permit-months only when the pairs are joined (records as charges miss 822). The closed record cannot see the grain: at 6.6 kW a pair and its charge give the same readings, the same energy and the same session model (S07).

Trap #4 (never tests its reading against the control) stands behind it: the statements are the control, filed as billing history in a file the call does not otherwise open. Below it, #5 (the population a filter suggests) is now the trap of the rung-4 stop: the car as of the session date rather than the contract year, which round 2 avoided by taking each permit's January 2027 renewal car. #13 (validates on one population, applies to another) stays as the frame, and #7 (the ready-made measure) carries rung 0, the rated replay and the Library vans' measured draw (rungs 2 and 3) and the per-car onboard limit that round 1 executed as a work order.

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

## Build record (stage 3, 2026-10-09)

Rebuild from the repo root with `python3 task117/generator/build_pack.py --out task117/target --meta task117/metadata.json` (seed 1172027 in `pipeline.py`) and verify with `python3 task117/generator/verify_pack.py task117/target --meta task117/metadata.json`. Generator modules: `common.py` (clock, tariff calendar, quarter-hour load arithmetic), `world.py` (garages, unit identifiers and their history, vehicles, permits, checks, fleet, reference list), `sessions.py` (background days, the twelve binding days, the rung-2 day, the 24 back-test days, the Library unit, the public garages), `ledger.py` (identifiers, versions, deliveries, re-deliveries, the gateway B split, readings), `meters.py` (roof lighting, panel energy, read times, the electricians' log), `analysis.py` and `checks.py` (goldens and assertions), `documents.py`, `writers.py`, `build_pack.py`. `verify_pack.py` shares no code with them.

### Gates

- **Generator green:** 180 named assertions (main call and ladder 34, corpus and twins 24, back-test 69, panel audit 23, separation and Gate G tests 8, register referee 3, pack gates 14, container scrub 5), all passing.
- **Independent verifier green:** 33 checks, 0 failures. It reads only `target/` (and `metadata.json` for the gates), parses the billing window, the holiday dates, the factor table, the accuracy clause, the diversity table and Exhibit A's 11.5 kW out of the documents, rebuilds every car through permit, check and reference rows, replays on its own quarter-hour code, and recomputes the answer, the split, the twelve months, rungs 0 to 3 and their kill facts, the rival cells, the five-rule family, the Library unit, the session model, the twins, every 2026 maximum-demand register, all 24 back-test figures and all 24 panel figures. The two distractors are outside its read list.
- **Byte-identical:** two consecutive scratch builds agree on all 23 outputs by sha256 (21 pack files, `metadata.json`, the build record), and the task-folder build matches them on its 22 (the pack and `metadata.json`); a third build after the last code edit matched again.
- **Input gates:** 21 files in six formats (csv, parquet, xlsx, pdf, docx, txt); the spine holds 1,568,086 rows; two distractors named in `metadata.json`; the word appears nowhere under `target/`.
- **metadata.json clean:** domain, subdomain, objective, as-of date, deliverables, the two distractors, source, licence and file list; no answer figure (asserted).
- **Containers:** the house scrub audit is clean on `target/` (no writer name, no timestamp outside 2023-01-01 to 2027-01-25); OOXML entries carry fixed in-fiction timestamps; the Parquet footer carries no pandas schema.
- **leak.py** (as-of 2027-01-25): REVIEW, six lines, all sweep 4. Each is ordinary vocabulary of an EV charging service overlapping the stump paragraph (charging, vehicle, rating, session, monthly, measured, decision, closed, utility); none names the move, and the generator's signpost grep (G06) is green. Sweeps 1 to 3 and 5 to 11 clean.
- **guard.py surface:** three pairs promoted on card axes only (task37, task97, task44: decisive gap time and pattern E with forecasting and a quantity figure), the collisions the Guard section above already answers; surface similarity 0.075 to 0.093, ordinary for the corpus; only drawn personas appear in the pack (Shelley Tanner, Ricardo Moore, Paul Henderson, A. Warner, T. Pierce, log initials AC and RM).

### The answer

**150 kW** (149.072 kW unrounded, 1.572 kW above the 147.5 edge; nearest 5 kW and rounded up agree). Binding quarter-hour 12:00 on Tuesday 17 February 2026, contract month February 2028; the 11:45 quarter-hour equals it and 12:15 is lower; each deck's own per-car maximum falls in it. North 88.4 and South 44.7 kW unscaled, **99.0 against 50.1 kW** after growth (99.008 and 50.064), 1.98 to 1.

### The ladder as built

| Rung | Construction | Unrounded | Filed | Against the answer | Where it is set |
|---|---|---|---|---|---|
| 0 | panel log, highest month's two registers (105.6 + 105.6) × 1.12 × 11.5/6.6 | 412.16 | 410 | +176.5% | both registers at 105.6 in several months |
| 1 | closed billing-hours maximum 158.4 × 1.12 × 11.5/6.6 | 309.12 | 310 | +107.4% | 12:00, 17 February 2026 |
| 2 | replay at 11.5 kW | 115.92 | 115 | -22.2% | 12:00, 10 June 2026, nine sessions |
| 3 | replay at the Library vans' 11.0 kW | 110.88 | 110 | -25.6% | same June quarter-hour |
| 4 | per car | 149.072 | **150** | answer | 12:00, 17 February 2026 |

Rung 2's twelve monthly figures: 12.88, 19.84, 24.69, 25.76, 12.88, 115.92, 25.76, 25.76, 25.76, 25.76, 12.88, 13.69 kW (one or two late arrivals a month, June the rung-2 day). Rung 3: the same months at 11.0 kW, June 110.88. The unchanged-draw monthly figures run 103.5 to 177.4 kW.

### The correction grid as built

Draw 6.6 kW 177.408 (175, +19.0%); fleet-average ratio 217.21 (215, +45.7%); replay at the fleet average 8.081 kW 212.793 (215, +42.7%); replay at each deck's average (7.242 / 9.692) 97.328 (95, -34.7%); per car with growth left off 133.10 (135, -10.7%); per car on North with rating on South 99.008 (-33.6%); per car on South with rating on North 100.912 (-32.3%); ratings only for the county pool cars 100.912 (-32.3%); the planners' sizing 225 (32 × 11.5 × 0.60 = 220.8, to the next 5 kW above; gap 75 kW); every all-hours cell 236.5 to 404.3 (at least +58.7%). Two-error cells: draw 6.6 with growth left off 158.40 (+6.3%, violations opposite in sign); fleet-average replay with growth left off 189.99 (+27.4%). Convergent readings, all 149.072: the decks' own maxima summed, all 36 months, vehicles as renewed in January 2027, stamps read as interval ends (every monthly figure unchanged), rounding up.

### Corpus, twins, separation

- Every deck vehicle 2024 to 2026 is listed at 7.2 kW or more; the closed replay under the rated and the per-car rule is identical reading by reading on all 72 deck-months.
- Five-rule family over 26,493 measurable sessions with an identified vehicle (127 too short to show a full quarter-hour): the smaller of rating and onboard rating misses 0; rating misses 713 (every van session on the Library unit); onboard rating misses 25,780 (every 6.6 kW session and the pickup); the 0.957 derate misses 25,780; a fixed 11.0 kW on 11.5 kW units misses 13 (every pickup session).
- Library unit: 713 van sessions at 11.0 kW and 13 pickup sessions at 11.5 kW.
- Twins: 3,607 North and 3,600 South sessions in 2026; KS statistic 0.020 on arrival, 0.010 on dwell, 0.013 on energy; each deck's closed billing maximum 79.2 kW, equal at the binding quarter-hour; 1.98 to 1 per car.
- Fleet shares 57 of 73 at 7.2 to 7.7 kW (78.1%), 44 of 48 North permits held by Larch County Fleet Services, 16 of 25 South vehicles at 11.0 kW; fleet average 8.081, deck averages 7.242 and 9.692.
- Every 2026 deck session finished delivery at least 28 minutes before plug-out, so no replay at 6.6 kW or faster is cut short.
- Zero device and zero hazard rows in the main population (re-delivered rows, restated versions, gateway B rows, reissued identifiers: 0 each). Clean-data test per suspect file (gateway B merged, re-deliveries kept, latest restated version kept, identifiers by latest assignment): the answer and rung 2 are unchanged in every repair and stay in different bins; identifiers by first assignment leave the answer unchanged. Lens swap: the closed replay is identical under both rules. Neither audit reads a vehicle.
- Register referee: re-deliveries and the back-feed never change a panel's maximum-demand register, keeping either non-accepted restated version never changes a South register, and every one of the 73 maximum-demand readings in the log (each meter's first read has no earlier reset) equals the sessions-only maximum (the roof lights are off in every maximum quarter-hour), so the context artifact reproduces to the last digit.

### Ask A1 and A2 (the contract year)

Whole kW: April 2027 115, May 106, June 98, July 90, August 91, September 108, October 116, November 124, December 130, January 2028 132, February 2028 149, March 2028 123; every unrounded figure at least 0.24 kW from a half-kW edge. Deck split 99 and 50. Planners 225, gap 75. Chart: 17 February 2026 by quarter-hour, the 150 kW line, the 12:00 quarter-hour at 149 kW.

### Ask B3 (the standard's 2025 record), as built

Filed path, pinned by FES-07 section 4: the forecast stated in whole kW against the recorded billing demand in whole kW.

| 2025 month | 2024 base | Forecast at 1.08 | Recorded 2025 | Miss |
|---|---|---|---|---|
| Jan | 105.380 | 113.810 → 114 | 115.200 → 115 | -0.9 |
| Feb | 112.164 | 121.137 → 121 | 119.192 → 119 | +1.7 |
| Mar | 99.884 | 107.875 → 108 | 110.124 → 110 | -1.8 |
| Apr | 95.472 | 103.110 → 103 | 101.916 → 102 | +1.0 |
| May | 89.104 | 96.232 → 96 | 96.864 → 97 | -1.0 |
| Jun | 81.544 | 88.068 → 88 | 85.852 → 86 | +2.3 |
| Jul | 76.112 | 82.201 → 82 | 83.888 → 84 | -2.4 |
| Aug | 83.168 | 89.821 → 90 | 88.780 → 89 | +1.1 |
| Sep | 93.716 | 101.213 → 101 | 103.812 → 104 | -2.9 |
| Oct | 102.856 | 111.084 → 111 | 109.904 → 110 | +0.9 |
| Nov | 105.484 | 113.923 → 114 | 113.180 → 113 | +0.9 |
| Dec | 101.140 | 109.231 → 109 | 110.128 → 110 | -0.9 |

Six over, six under; every forecast and recorded demand 0.06 to 0.24 kW off a whole kW; every miss 0.015 to 0.046 points inside its bin and never an exact one-decimal share. Devices: reissued identifiers (primary, D7) move all 24 figures; the 1.09 revision moves all 24; gateway B moves January to April; the restated versions move the May to July misses; the re-delivered batches move the October and December misses. Under all 47 subsets of mishandlings the misses stay two-signed and their mean stays between -1.44 and +1.10 points. The coincident maximum equals the sum of each deck's own in all 24 months.

### Ask B1 (the 2026 basis against the panel meters), as built

Whole kWh, readings 1 to 12. North (SM-2231, CP-N): 1069, 909, 910, 725, 594, 592, 599, 691, 791, 914, 1065, 1130. South (SM-2232, CP-S): 933, 800, 794, 633, 520, 517, 523, 606, 693, 799, 932, 990. Every golden is 0.06 to 0.24 kWh off a whole kWh. Read times (meter clock, standard time): 30 Jan 07:00, 27 Feb 08:30, 31 Mar 07:45, 30 Apr 07:00, 29 May 09:00, 30 Jun 08:30, 31 Jul 09:15, 31 Aug 07:00, 30 Sep 08:45, 30 Oct 07:00, 30 Nov 08:30, 31 Dec 09:45 (South also 07:30). Devices: the meter clock (primary, D8) moves readings 3 to 11 on both panels by 4.5 to 59.9 kWh and leaves 1, 2 and 12 alone; the re-delivered December 2025 rows move reading 1 by 40.5 (North) and 32.9 kWh (South); the unit on the temporary house-panel feed moves North 6 and 7 by 168.8 and 71.6 kWh; keeping the first 31 December South read (hundreds digit misread) moves South 12 by 99.1 kWh; over-deduping the same-day repeats and calendar-month spans move further readings. Every subset of mishandlings lands at least 2.5 kWh from the golden on every reading; whole-session attribution by plug-in lands at least 2.5 kWh away. North 12 carries no device.

### Span

Main call, 12 files (session header, readings, station register, permit registry, vehicle checks, reference list, fleet roster, rate schedule, standard, agreement, field notes, data-sources note). B3, 9 files (session header, readings, station register, restatement decisions, gateway B export, standard, rate schedule, field notes, data-sources note). B1, 7 causal files (panel log, nameplates, session header, readings, station register, circuit schedule, field notes) plus the work orders as the documentary second antidote to the back-feed: the stage-2 debt of one file is closed by moving circuit assignments into the facilities schedule, and the work orders are corroborating rather than strictly necessary, since the schedule alone dates the temporary feed.

### Pack manifest

| File | Format | Rows | Role |
|---|---|---|---|
| session_intervals_2024-2026.parquet | parquet | 1,568,086 | spine |
| settled_sessions_2024-2026.csv | csv | 98,623 | operating extract, calibration ledger |
| restatement_decisions_2025.csv | csv | 45 | operating extract (version of record) |
| gateway_b_sessions_jan-apr2024.csv | csv | 302 | operating extract (legacy gateway) |
| station_register.csv | csv | 164 | dimension (identifier history) |
| deck_panel_circuit_schedule.csv | csv | 51 | dimension (circuit assignments) |
| deck_panel_meter_log_2024-2026.xlsx | xlsx | 75 reads | context artifact (rung 0), B1 |
| deck_submeter_nameplates.csv | csv | 2 | dimension (meter clock) |
| facilities_work_orders_2026.csv | csv | 20 | operating extract |
| ev_permit_registry.csv | csv | 75 | dimension |
| permit_vehicle_checks.csv | csv | 425 | dimension |
| vehicle_reference_list.csv | csv | 22 | dimension |
| city_fleet_roster.csv | csv | 19 | dimension |
| nspl_schedule_26_ev_charging_service.pdf | pdf | 2 pages | governing (billing window, holidays, 5 kW steps, ratchet) |
| fes-07_load_forecasting_standard_rev4.pdf | pdf | 1 page | governing (base months, factor table, accuracy record) |
| civic_center_ev_service_agreement_draft.docx | docx | 2 pages | governing (scope, one meter, contract year, Exhibit A) |
| nspl_new_service_planning_guide_2026_sec7.pdf | pdf | 1 page | licensed wrong basis |
| curbline_export_field_notes.txt | txt | | dictionary |
| parking_services_data_sources.txt | txt | | provenance, permit rules, version of record |
| civic_center_campus_electric_statements_2024-2026.csv | csv | 35 | distractor |
| charger_status_events_2026.csv | csv | 1,212 | distractor |

### Changes from the stage 2 design, made at stage 3

1. The back-test's rounding path is pinned in the standard: FES-07 section 4 now files that forecast demand is stated in whole kW and that a forecast's error is the stated forecast less the recorded billing demand in whole kW, as a percentage of that demand. The misses are computed on that path, and every forecast and recorded demand sits off a whole kW.
2. Back-test device magnitudes are smaller than the stage-2 targets (0.66 to 2.2 kW at the 12:00 quarter-hour against "1.5 kW or more"), sized so the mean condition holds under every subset; each still moves every figure its ledger row names (asserted). The "current-identifier filter" is the same silent path as the raw join here (a lookup reduced to each identifier's latest assignment); filtering to assignments still open is loud (26 retired identifiers stop joining) and is not a stop.
3. Assertion 29 is restated: plug-out after delivery at 6.6 kW (minimum slack 28 minutes) replaces "two hours after delivery at 7.2 kW", which the lunch-time unplug-and-replug sessions and the late arrivals do not meet; the property it protects, that no replay is cut short by departure, is unchanged.
4. Assertion 48 (the pair simulation from the generated rubric) waits for the rubric; the stage-2 pair arithmetic stands until then.
5. The social-layer thread is not built: the prompt carries the facilities engineer's expectation and the planners' method is filed in their guide, so a thread would restate both. The pack has 21 files, two above the 19-file target.
6. Open item for the realism pass (H21): "North Sound" is a real regional name used by real Washington organisations; the utility's name is in the prompt, so any rename is an author decision.

## Write-up and ship checks (stage 3, 2026-10-09)

Goldens from `python3 task117/generator/golden.py` (reads only `target/` through `verify_pack.py`'s readers and quarter-hour code, so the goldens and the verifier cannot drift). It asserts every figure against the build record before writing anything (`verify_pack.EXPECTED`: the answer, the binding quarter-hour, the split, the twelve months, rung 2, the planners' 225, all 24 back-test and all 24 panel figures), then writes the three deliverables and prints the critical components. Two consecutive runs are byte-identical on all three files and print identical figures.

- **`contract_demand_note.pdf`**, one page, memo from the energy manager to Mayor and Council dated 25 January 2027: title states the call; 150 kW; February 2028 at 149 kW (149.1 unrounded, 150 nearest and rounded up); North 99, South 50; the planners' 225 kW and the 75 kW gap (worth $10,260 a year at Schedule 26's $11.40); the twelve contract months in a table; Ricardo Moore's expectation answered from the record (78 per cent of 2026 permit vehicles at 7.2 or 7.7 kW, computed in the script); a source line and a footnote quoting the billing-demand definition and the factor's adoption date.
- **`deck_load_day.png`**, rendered by the script (dataviz palette blue and orange, validated): 17 February 2026 by quarter-hour, the 6.6 kW day as drawn and the February 2028 forecast as step series, the 150 kW line labelled, the 12:00 quarter-hour marked at 149 kW with the deck split, the billing window shaded as presentation, a finding title and a source strip.
- **`civic_service_demand.xlsx`**, written by the script: `2025 back-test` (base, factor 1.08, forecast, recorded, over or under, error to 0.1 per cent), `2026 panel check` (meter, read, meter-clock time, civil-time span, metered, session and unaccounted kWh), `Contract year` (each month's binding quarter-hour, 2026 replay, factor, forecast) and `Notes`.
- **`submission.md`**: the five blocks; block 4 carries all 1 + 12 + 1 + 2 + 2 figures of the note, the five chart parts and all 48 workbook figures in the prompt's order. A scratch cross-check matched every block-4 figure to the PDF and the workbook cell by cell.
- **golden-realism pass** (figures frozen first, then re-run and unchanged): memo genre rather than the four-heading spine, lopsided sections with the method longest, precision by quantity (whole kW, 149.1, $11.40, 0.1 per cent), named sheets, frozen headers, set widths, number formats, print areas, a notes sheet; the chart legend moved off the forecast line; an invented agenda item number removed because the pack carries none.
- **reduce-house-fixes register**: H1 goldens and inputs audited clean (PDF and workbook producer "City of Larch Harbor", stamps 25 January 2027; PNG carries no Software chunk); H4 `golden/` holds exactly the three named files, every visual opened; H6 every rule the golden states back-tests on the record (the draw composition misses 0 of 26,493 sessions, the 6.6 kW replay regenerates every deck reading, both 2026 panel maxima 105.6 kW, the meter clock's March to October offset); H7 two runs byte-identical; H8 every citation resolves (FES-07 sections 2 and 4 and Table 1, Schedule 26 sections 3, 4 and 7, agreement section 4 and Exhibit A, guide 7.3, WO-26-0418, circuit 33); H11 one `submission.md`, one `prompt.md`; H20 the prompt carries all four institutional nouns and none of the banned three. `verify_pack.py` 0 failures after the passes.
- **guard.py surface**: the three pairs promoted at stage 3 cut (task37, task97, task44) are promoted on card mechanism axes only, already differentiated on the card; surface similarity 0.075 to 0.089; no byte, schema, name or prompt-wording overlap, so nothing to rename or regenerate. Personas in the pack: Shelley Tanner, Ricardo Moore, Paul Henderson.
- **guard.py heart**: PASS (nearest driver 0.08, task59 v2; nearest stump 0.04); card `driver_concrete` restated with the as-built figures, answer, spine rows, deliverables and opening move filled; `guard.py validate` 116 cards, 0 invalid.

## Leak review

leak.py, as-of 2027-01-25, run at the stage-3 rebuild after harden loop 2 (2026-10-09): REVIEW, 6 lines, no LEAK; sweeps 1, 2 and 5 to 11 clean. Re-run at the stage-3 ship checks re-pass (2026-10-09) on the byte-identical pack: the same 6 lines, each answered below unchanged.

- Sweep 3, agreement, 11.5: Exhibit A's unit rating is the filed equipment specification every rung from 2 up uses; it states no rule about what a session draws, which car a permit carries or how a charge is recorded.
- Sweep 3, agreement, 6.6: the rating of the units being removed, also in the station register; context for the switchover, not an answer figure.
- Sweep 3, agreement, 6 of 7 words of the call: the agreement is where the figure is filed (Schedule 1 is a blank), so it shares the call's nouns (contract demand, first contract year) and carries no figure.
- Sweep 4, Schedule 26 (monthly, charging, measured): the tariff's billing-demand definition, the pin that kills rung 0; filed, not the decisive step.
- Sweep 4, data-sources note (session, decision, monthly, rating, charging): a folder description that files the permit rule once and describes each file as a folder listing would, the two new ones included (the courtesy report as weekend and holiday charging that is free to permit holders, the statements as monthly bills per permit with a session fee per charge); it never says to join records, to add the courtesy sessions to anything, or which car a forecast uses.
- Sweep 4, prompt, panel-meter sentence (session, charging): the B1 ask in the requester's words; it names the quantity, not the courtesy channel, the read-time split or any device.

Hand sweep of the new rung's and devices' own vocabulary (settlement run, record, pair, join, chain, split, continue, carry on, courtesy, free to permit holders, statement, UTC) over every shipped document: the field notes file the run's time once, under settled_on, and give session_id to each session record; the auth_code line ("one code identifies one settled charge") is the stage-3 re-delivery rule, unchanged; the data-sources note carries the two folder lines above; UTC appears only in the field notes' plug_in and plug_out definitions, which describe the export's own offsets. No document says that the run closes a session still charging, that a charge continues in a new record, that the courtesy sessions belong in a panel reconciliation, or that the fleet card file is stamped in UTC.

## Harden loop 1: design (2026-10-09)

Round 1's plain solver landed 150 kW (proxy 88.1) by executing the stage-2 decisive rung as a work order at its path step 4, and executed every ask device as the ask's own files state it (`## Tried and rejected`, the two round-1 lines). The repair keeps every rung the solver climbed and adds one after it: the solver's step 4 still completes, still joins every session to one car, still applies the smaller of 11.5 kW and the onboard rating, and still returns 150 kW, which is now wrong.

### What changed

1. **Rung 5, the car each permit carries in the contract year.** At the January 2027 renewal (check rows dated 5 to 13 January 2027, before the as-of date) Larch County Fleet Services renewed 18 of its 24 permits held by 2020 Bolt EVs (7.2 kW) onto 2023 Bolt EVs (11.0 kW): same make and model, new plate and VIN. The vehicle reference list gains the 2022 to 2023 Bolt EV row at its published 11.0 kW. No other permit changes car at the renewal and none changed during 2026 (asserted R03, B20).
2. **The binding days are recomposed** so the two readings of the car put the peak in different months. With each session's own car the year peaks at 12:00 on Tuesday 17 February 2026 (ten renewed cars still charging at noon), 148.512 kW, filed 150. With the contract-year car it peaks at 12:00 on Tuesday 8 December 2026 (six county cars that were not renewed and the four Teslas on North), 129.136 kW, filed 130. Every other month's binding day mixes kept and renewed pool cars so the two readings differ at whole kW in eleven months of twelve.
3. **The permit registry loses its plate column.** It held each permit's current plate, which after the renewal hands the contract-year car to any plate join; the car now comes only from the dated check rows, where the solver chooses the date.
4. **Fresh primary devices on both pool-B asks** (below). The stage-3 devices stay as hazards.
5. **No prompt change and no new clause anywhere.** The governing register (each permit names one vehicle, checked at issue and at every January renewal) was already filed once, in the data-sources note, and FES-07 already prepares the forecast for the service the decks will be supplying. Nothing is pinned louder.

### Gate G, restated

- **Litmus.** No. Every figure in the pack is correct, the renewal check rows included, and nothing a stakeholder states about their own figures is overturned. The difficulty is that the cars that will charge in the contract year are not the cars that made the base year's sessions.
- **Primary mechanism:** `forecasting`, `method_or_model_selection` supporting. **Flags:** `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`.
- **Deletion test.** Delete the panel log, the planners' guide and both distractors: the closed record still certifies the per-car replay with each session's own car on every 2026 reading, and it still files 150.
- **Clean-data test.** The checks file is complete and correct, so there is nothing on the main path to repair. The off-path suspect files (gateway B, the fleet card file, restated versions, re-deliveries, reissued identifiers) are repaired one at a time and the answer, rung 4 and rung 2 stay put and in three different bins (E02).
- **Lens swap.** Rung 4 and the answer replay the same sessions under the same physics with two fleets at two moments, 2026 and the contract year. The closed replay is identical under both (E04); they differ only through the forward fleet. Not a lens swap.
- **Pre-draw identity.** Contracted demand = 1.12 x the maximum over billing quarter-hours of the sum over concurrently charging sessions of min(11.5 kW, the onboard rating of the car the session's permit carries in the contract year), each 2026 session re-timed from plug-in at that draw.

**Rung 5 against the seven survival properties.** 1 Written nowhere: no document says the forecast uses the renewed fleet; the renewal is data in rows the solver already joins. 2 No corpus nominates it: every 2026 session was made by its 2026 car, the session-date join reproduces every closed reading, and the renewal is dated after the last 2026 session (R05). 3 No arithmetic symptom: both joins resolve every session to exactly one car and one reference row. 4 Not a row predicate on anything the solver holds: it is a property of a different entity (the permit's car) at a date nothing names. 5 The solver's own step completes and returns the wrong answer. 6 No cutover in a closed series: the renewal steps nothing in 2026. 7 Survives deletion. **The accepted weak point:** a solver who takes each permit's latest check without thinking about dates lands on the contract-year car by accident. That reading is the right one for a forward forecast, round 1 took the session-date join, and the plate column that would have made the latest car the default join is gone.

### The ladder

| Rung | Construction | Unrounded (kW) | Filed | Against the answer | Set at |
|---|---|---|---|---|---|
| 0 | panel log, the highest month's two registers x 1.12 x 11.5/6.6 | 412.16 | 410 | +219.2% | registers at 105.6 in several months |
| 1 | closed billing maximum 158.4 x 1.12 x 11.5/6.6 | 309.12 | 310 | +139.4% | 12:00, 17 February 2026 |
| 2 | replay at 11.5 kW | 103.04 | 105 | -20.2% | 12:00, 10 June 2026 (eight late sessions) |
| 3 | replay at the Library vans' 11.0 kW | 98.56 | 100 | -23.7% | same quarter-hour |
| 4 | per car, each session's car on its own date | 148.512 | 150 | +15.0% | 12:00, 17 February 2026 |
| 5 | **per car, the car each permit carries in the contract year** | **129.136** | **130** | answer | 12:00, 8 December 2026 |

Kill facts: rung 0 the billing-demand clause (Schedule 26); rung 1 the readings themselves (a faster unit shortens a session); rung 2 the Library unit's van sessions at 11.0 kW; rung 3 the pickup at 11.5 kW on the same unit; rung 4 the January 2027 renewal rows under the filed permit rule (a replaced car holds no permit in the contract year).

Worth of each rung on the graded figure: 0 to 1 -25.0%, 1 to 2 -66.7%, 2 to 3 -4.3%, 3 to 4 +50.7%, 4 to 5 -13.0%. The answer is bracketed by rungs 3 and 4.

"A solver who does everything right up to rung 4 commits to 150 kW and names February 2028 as the month that sets it."

### Position table (asserted)

| Rung | Unrounded | Filed | Month that sets it | North / South at its binding quarter-hour, scaled (kW) |
|---|---|---|---|---|
| 0 | 412.16 | 410 | several | 206.1 / 206.1 |
| 1 | 309.12 | 310 | February 2028 | 180.3 / 128.8 |
| 2 | 103.04 | 105 | June 2027 | 51.5 / 51.5 |
| 3 | 98.56 | 100 | June 2027 | 49.3 / 49.3 |
| 4 | 148.512 | 150 | February 2028 | 115.1 / 33.4 |
| 5 | 129.136 | **130** | **December 2027** | **82.9 / 46.3** |

Contract months, whole kW: answer April 2027 90, May 85, June 79, July 72, August 75, September 87, October 94, November 103, December 129, January 2028 109, February 68, March 98; rung 4 the same months 114, 109, 103, 88, 99, 119, 126, 119, 129, 125, 149, 114. The twin decks carry equal closed load at the answer's binding quarter-hour (66.0 kW each) and split 1.79 to 1 per car; rung 4 splits its own quarter-hour 3.45 to 1.

### Separation and dominance

The answer is a figure in 5 kW bins with no ranking, so the separation floor binds. Nearest single-error cells: growth left off 115.3 kW (-10.7%, files 115), the deck-average replay on 2026 vehicles 113.549 kW (-12.1%, files 115), rung 4 148.512 kW (+15.0%, files 150). Nearest two-error cell: each session's own car with growth left off, 132.6 kW (+2.7%), which files 135 under both roundings and needs two violations of opposite sign (L4). Bins: 129.136 sits 1.636 kW above the 127.5 edge and 0.864 below 130; at whole kW it is 0.364 from 129.5. Flip conditions, unscaled at the binding quarter-hour: rounding up files 135 only on a gain of 0.771 kW; to the nearest 5 kW a gain of 3.004 kW or a loss of 1.461 kW moves the bin.

### The correction grid (as built, every cell asserted by name)

Single-error cells: draw 6.6 kW 177.408 (175, +37.4%); rating ratio 309.12 (310, +139.4%); fleet-average ratio on 2026 vehicles 217.212 (215, +68.2%) and on contract-year vehicles 242.399 (240, +87.7%); replay at 11.5 kW 103.04 (105, -20.2%) and at 11.0 kW 98.56 (100, -23.7%); replay at the fleet average on 2026 vehicles 213.188 (215, +65.1%), at each deck's average on 2026 vehicles 113.549 (115, -12.1%), at the fleet average on contract-year vehicles 80.800 (80, -37.4%), at each deck's average on contract-year vehicles 89.613 (90, -30.6%); each session's own car 148.512 (150, +15.0%); growth left off 115.300 (115, -10.7%); the planners' sizing 225 (+74.2%); per car on North with rating on South 95.760 (95, -25.8%); per car on South with rating on North and ratings only for the county pool cars 92.848 each (95, -28.1%); every all-hours cell 236.544 to 396.404 (at least +83.2%). Two-error cells: own-date cars with growth left off 132.600 (135, +2.7%, opposite signs); draw 6.6 with growth left off 158.400 (160, +22.7%); deck averages on 2026 vehicles with growth left off 101.383 (100, -21.5%); fleet average on 2026 vehicles with growth left off 190.347 (190, +47.4%); the rated replay scaled by the old units' ratio 59.136 (60, -54.2%). Convergent readings, all 129.136: the decks' own maxima summed (both peak in the binding quarter-hour), all 36 months, each permit's latest check (as of energization, 1 April 2027), vehicles as of the council vote, stamps read as interval ends (all twelve months), rounding up.

### Closure table, the axes that moved

| # | Axis | Reading chosen | Closed by |
|---|---|---|---|
| 4 | As-of dating (now the decisive axis) | The car each permit carries in the contract year: its January 2027 renewal check, the latest on or before the forecast date | The forward window (the forecast is for April 2027 to March 2028) + the filed permit rule (one vehicle per permit, checked at issue and at every January renewal, so a replaced car holds no permit) + C1 (every as-of date from the renewal through the council vote and energization returns the same cars; no later check is on file) + C4 (the session-date reading files 150, +15.0%) |
| 16 | Identity normalisation | Make, model, trim and model year as written on the check row | C1 (every check row resolves to exactly one reference row, B21); the registry carries no plate to join on |
| 22 | Forward window contents | The 73 active permits as renewed in January 2027: 18 cars changed, no pedestal added or removed | Filed (agreement scope) + R01 to R03 |
| + | The draw on the new units | min(11.5 kW, onboard rating) per session | C2 (unique survivor of the five-rule family: 0 misses over 24,192 measurable sessions; rating 419, onboard 23,773, the derate 23,773, a fixed 11.0 kW 13) + C4 |

Every other axis keeps its stage-2 line.

### The ask ledger, re-hardened

**Pool A (the contract year, the month, the split, the chart).** Device-free and carried by rung 5: a solver at rung 4 files eleven of twelve months wrong (December alone agrees), names February, and gets both split figures, the chart's day and its marked value wrong; a solver at rung 2 or 3 gets every month wrong.

**B3, the standard's 2025 record. Primary device (new): fleet-card charges outside the export.** Before the April 2025 platform move a fleet card charge was authorised and settled through the fleet card processor, not through Curbline settlement, so it is absent from the settlement export; every fleet card charge at a Curbline station from 2024 to 2026 ships in `fleet_card_ev_transactions_2024-2026.csv` (START, END, KWH, STATION and NETWORK_REF, the charge's network reference). One fleet-card top-up ends inside the 12:00 quarter-hour on every back-test day (0.70 kW). Left out, it moves all 24 figures (C07, asserted in the parameter search). Added wholesale on top of the export, it double counts April to December 2025 and moves seven misses (C08). Silent: the export reconciles to itself and the field notes list FLEET as an account type; the only symptom is that FLEET rows begin at the platform move, visible to a solver who tabulates account type by month or matches the fleet file to the export on NETWORK_REF. Off path: 43 such charges at the decks, all before 1 April 2025 (C13), none in the 2026 population (E01). Hazards kept: reissued identifiers (all 24 figures), the 1.09 vintage (all 24), gateway B (January to April), restated versions (May to July misses), re-deliveries (October and December misses). Under all 143 subsets of mishandlings the misses stay two-signed with a mean between -1.47 and +1.70 points.

**B1, the 2026 basis against the panel meters. Primary device (new): reads inside a quarter-hour.** Every read is logged to the minute, none falls on a quarter-hour, and each meter is read at its own minute (the decks are read separately). The session energy between two reads is the readings for every whole quarter-hour plus, in the quarter-hour a read falls inside, each session's constant 6.6 kW draw up to the read time, which the closed readings certify (V17a). Rival splits and their moves on every reading: the straddling quarter-hour all before the read (what filtering readings by start time does) 1.51 to 11.77 kWh; all after it 1.51 to 11.84; the read moved to the nearest quarter-hour 1.52 to 16.76; pro rata inside the quarter-hour 0.76 to 1.69, always onto a different whole kWh (D13). Silent: every split completes and every total ties. Hazards kept: the meter clock on standard time (readings 3 to 11, 19.4 to 77.2 kWh), the re-delivered December 2025 batch (reading 1, 45.3 and 38.3 kWh), the back-fed unit (North 6 and 7, 176.7 and 57.0 kWh), the double read (South 12, 99.2 kWh), repeats over-deduped, calendar spans. Every subset of mishandlings lands on a different whole kWh on every reading, at least 1.5 kWh away unless it carries the pro rata split (D09, 24 readings).

**Pair arithmetic.** Planning weights 38 / 7 / 55. If rung 5 holds the field off the call, as it is built to, each top response scores about r + 7 + 55 L and the pair stays under 40 while each keeps under about half the pool-B weight, so both fresh primaries have to fall before the asks alone lift the pair over the target. If one top response lands the call, the pair reaches 40 only when the two together keep under about 0.47 of the ask weight, which needs at least one of the two primaries to hold against both. What the pass condition rests on: the session-date join at rung 4 (the step round 1 took) keeping every response but one off the call, then the fleet-card device, which has no symptom inside the export, holding against both top responses.

### Stopping rule for the next round

At ceiling: two consecutive rounds in which a response files 130 kW through the contract-year car by different routes; re-root at stage 1 and move this architecture into the card's lineage. One more repair: a response files 130 by taking each permit's latest check with no regard to dates and says nothing about the renewal (a determinism note, not a difficulty repair), or the pair clears 40 with at most one response on the call (a pool-B repair, one device per repair). Working as built: responses that stop at rung 4 (150 kW) or below.

## Build record (harden loop 1, 2026-10-09)

Rebuild and verify exactly as the stage-3 record says (`build_pack.py` with seed 1172027, then `verify_pack.py`), then `golden.py` for the deliverables.

- **Generator green:** 306 named assertions (main call and ladder 40, the renewal 7, corpus and twins 23, back-test 168 of which 143 are subsets of mishandlings, panel audit 37 of which 24 are readings, separation and Gate G tests 9, register referee 3, container scrub 5, pack gates 14), all passing.
- **Independent verifier green:** 39 checks, 0 failures. It reads only `target/` and `metadata.json`; it rebuilds each permit's car from the check rows at both dates, recomputes the answer, rung 4 and the renewal from the checks alone, adds the fleet card charges the export does not carry by NETWORK_REF, and splits every read's quarter-hour on the sessions' own draw.
- **Byte-identical:** two consecutive scratch builds agree on all 24 outputs by sha256 (22 pack files, `metadata.json`, the build record); the task-folder build matches them on its 23. `golden.py` run twice: the three deliverables byte-identical and the printout identical.
- **Input gates:** 22 files in six formats (csv, parquet, xlsx, pdf, docx, txt); the spine holds 1,534,415 rows; two distractors named in `metadata.json` and unread by the verifier.
- **Containers:** the scrub audit is clean on `target/` and on `golden/`.
- **Pack changes:** `fleet_card_ev_transactions_2024-2026.csv` added (5,108 charges, 2,015 of them before 1 April 2025 and outside the export, 43 at the decks); `ev_permit_registry.csv` without its plate column (75 permits); `permit_vehicle_checks.csv` 425 rows with the January 2027 renewal; `vehicle_reference_list.csv` 23 rows; `settled_sessions_2024-2026.csv` 96,708 rows; `gateway_b_sessions_jan-apr2024.csv` 301 rows; the data-sources note registers the new file (every shipped file listed).
- **Asks as built.** A1: the contract months above; the split 82.88 and 46.256 kW (83 and 46); the planners' 225 kW and the gap of 95. B3, forecast and miss: January 112 (-0.9%), February 117 (+2.6%), March 107 (-1.8%), April 106 (+1.9%), May 88 (-1.1%), June 88 (+2.3%), July 82 (-1.2%), August 90 (+2.3%), September 106 (-0.9%), October 114 (+1.8%), November 113 (+0.9%), December 111 (-0.9%). B1, unaccounted kWh: North 1,069, 908, 910, 725, 594, 592, 599, 691, 791, 914, 1,065, 1,130; South 934, 798, 794, 633, 520, 517, 523, 606, 693, 799, 932, 990; every golden 0.06 to 0.24 kWh off a whole kWh.
- **Write-up:** `submission.md` rewritten through `submission-writeup` (five blocks; block 4 matched to the PDF and the workbook cell by cell by a scratch cross-check); `golden-realism` pass after the figures froze (the legend moved off the 130 kW line, the source strip rewrapped, the memo held to one page); `reduce-house-fixes` register run (H3: one memo sentence corrected to "most of December's peak is theirs", since one 11.0 kW car also charges through the binding quarter-hour; H1, H4, H8, H9, H11, H16 clean).
- **leak.py** (as-of 2027-01-25): REVIEW, 8 lines, no LEAK. Sweep 3: the agreement's Exhibit A rating (11.5 kW), the removed units' 6.6 kW and the call's nouns (contract demand, first contract year), as at stage 3. Sweep 4: ordinary vocabulary of the service in the field notes, FES-07, Schedule 26, the data-sources note and the prompt's panel-meter sentence. A hand sweep of the new rung's and devices' own vocabulary over every shipped document (renewal, contract year, replacement car, fleet card, platform move, quarter-hour, read time) finds the permit rule filed once in the data-sources note, the checks' provenance line and the field notes' FLEET account type, and no sentence that names a move.
- **guard.py:** card restated (answer, stump, driver, driver_concrete, generators with G6 added, spine rows, differentiation against task37, task44 and task97 rewritten for the renewal rung, notes); `validate` 116 cards, 0 invalid; `check` PASS (the same three older builds noted, differentiated); `heart` PASS (nearest driver 0.07, task64 v2; nearest stump 0.03); `surface` promotes task37, task97 and task44 on card axes only, surface similarity 0.075 to 0.089, the pairs the card already answers; personas in the pack: Shelley Tanner, Ricardo Moore, Paul Henderson.

## Write-up and ship checks (stage 3 rebuild after harden loop 1, 2026-10-09)

- **Pack:** a scratch rebuild (`build_pack.py`, seed 1172027, 306 assertions green, answer 129.136 kW) matches `target/` and `metadata.json` byte for byte on all 23 files; `verify_pack.py` 0 failures.
- **Goldens:** `golden.py` reads only `target/`, asserts every figure against `verify_pack.EXPECTED`, and now also back-tests the memo's typed wording on the record: all 18 renewed permits are North Deck permits held by Larch County Fleet Services, moving from 2020 to 2023 Bolt EVs; the session-date replay peaks in February; the 7.2 and 7.7 kW cars carry more than half of the binding quarter-hour; the 2027 permit cars are rated 7.2, 7.7 or 11.0 kW only; and 98.7% of the 11.0 kW cars' morning sessions on the new units finish by noon (3,360 of 3,404). Two runs are byte-identical, with identical printouts; the workbook and the chart are byte-identical to the harden-loop goldens, and only the memo's wording moved.
- **submission.md:** five blocks, block 4 checked cell by cell against the PDF and the workbook (1 + 12 + 1 + 2 + 2 note figures, 5 chart parts, 24 back-test pairs, 24 panel figures). Block 1's last rival clause no longer quotes 150 kW, a figure no later block carries, and states the renewal through block 2's own figures (18 permits, 11.0 kW).
- **golden-realism:** figures frozen first. Memo in genre (memo block, finding title, lopsided sections, table with a source line, billing-demand footnote, page footer); workbook with named sheets, frozen headers, set widths, per-column number formats, print areas and a notes sheet; chart with a finding title, units, the labelled 130 kW line, the 12:00 quarter-hour marked with the deck split, the billing window shaded, and a source strip. Containers audit clean on `target/` and `golden/` (band 2023-01-01 to 2027-01-25).
- **reduce-house-fixes:** H1 clean on both trees; H3 one memo sentence corrected ("for the 11 kW cars that is right" becomes "the 11 kW cars nearly always are", now computed and asserted); H4 `golden/` holds exactly the three named files, each opened; H7 byte-identical reruns; H8 every citation resolves (FES-07 sections 2 to 4 and Table 1, Schedule 26 sections 2, 3, 4 and 7, agreement section 4, Exhibit A and Schedule 1, guide section 7, WO-26-0418, circuit 33); H11 one `submission.md`, one `prompt.md`; H20 G09 green.
- **leak.py:** REVIEW, 8 lines, no LEAK (answered under `## Leak review`). **guard.py surface:** task37, task97 and task44 promoted on card mechanism axes only (surface 0.075 to 0.089), already differentiated on the card; no byte, schema, name or wording overlap. Personas in the pack: Shelley Tanner, Ricardo Moore, Paul Henderson. **guard.py heart:** PASS (nearest driver 0.07, task64 v2; nearest stump 0.04). Card answer, answer_source, spine rows (1,534,415), deliverables (in the prompt's order) and opening move updated; `validate` 119 cards, 0 invalid.

## Harden loop 2: design (2026-10-09)

Round 2's plain solver landed 130 kW (proxy 89.2) by running rung 5 as the last link of the chain it was already building, and handled both fresh pool-B primaries as their own files state them (`## Tried and rejected`, the harden loop 2 line). The repair keeps every rung and adds one after the solver's step: its step 4 ("Re-simulated each 2026 session at min(11.5 kW, OBC), using the vehicle on the permit at the January 2027 renewal") still completes, still joins every record to one car at the right date, and now returns 155 kW, which is wrong.

**Re-root weighed.** The note's own stopping rule licenses this repair (one round, not two, has filed 130 through the contract-year car), and the orchestrator assigned loop 2. The repair moves the decisive step off the car chain entirely, onto the unit the replay runs on, which is trap #2 of the measured catalogue (counts file rows instead of the real unit, 11 of 64, 7 under 0.50) with trap #4 behind it (never tests its reading against the control). If round 3 lands 130 through the charge merge, loop 3 is the last on this architecture and a re-root at stage 1 is the default.

### The new rung

**Rung 6, the charge, not the settlement record.** Curbline's settlement run is daily from 10:00 a.m. local time; it reaches each garage at its own instant between 10:00 and 10:07, one instant per garage per day (S02). A session still delivering energy at the run is closed there and its charge continues as a new session record under a new authorization code, at the same station and permit or card, starting the second the first record ends. On the binding days 97.5 per cent of the decks' long morning sessions are charging at the run (S08), so the export carries them as pairs: 15,292 pairs across the eight garages from 2024 to 2026, 3,033 of them at the decks in 2026. The closed record cannot tell a pair from one charge: at 6.6 kW the second record draws from its first second, so the readings, the energy and the session model are identical either way (S07). Replayed on the new units record by record, the second record restarts at the run at the car's full new rate, and cars that finish before noon as one charge are back on the meter at noon. Replayed charge by charge (each zero-gap chain at one station under one permit or card merged into one block from its first start, energy summed), the answer is unchanged at 129.136 kW.

- **What pins it (determinism).** Structural: every zero gap at a station is one charge's pair, and no two records at a station overlap (S01, S04); a genuine unplug and replug leaves at least 30 minutes (S05), and at one unit under one permit or card any two records either meet end to start or sit 42 minutes or more apart, the shortest 42.7 (V07i), so every join tolerance under 42 minutes selects the same pairs. Documentary: the field notes give session_id to each session record, define plug_in and plug_out as the session's start and end, and file the settlement run's time once, under settled_on. Corpus (C2): Parking Services' 2026 permit charging statements bill each permit per charge; the joined chains reproduce the charge count and the energy on all 875 permit-months, records as charges miss 822, and merging every same-day record of a permit at a station (the over-merge) misses 35, the months with a genuine replug (S06, V07f). The over-merge converges on the call (the answer, its quarter-hour and all twelve months unchanged, S09 and V07g), so the only reading the corpus has to refuse for the call is records as charges.
- **Why it is silent.** Unique keys, unique authorization codes, no orphan, no fan-out, readings sum to energy, and the session model validates on every record. The tell exists only as a relation between two rows (a record ending and the next starting at the run minute, same unit, same permit) and in a billing file nothing in the call asks for.
- **Seven survival properties.** 1 Written nowhere: no document says the run splits a charge or that the replay should join records. 2 The closed record does not nominate it: records and charges give the same readings at 6.6 kW; only the statements separate them. 3 No arithmetic symptom (above). 4 Not a single-row flag: the pair is visible only by ordering a unit's records in time. 5 The solver's own step completes and returns the wrong answer. 6 No cutover in a closed series: the run has split records every day since January 2024. 7 Survives deletion. **The accepted weak point:** a solver who checks that each record finished delivery before its plug-out finds that the records the run closed were still delivering at plug-out, with no idle minute, and that the next record at that unit starts the same second; that is the intended discovery path, and the statements confirm it.

### Gate G, restated

- **Litmus.** No. Every record in the export is correct at its documented grain, the statements are correct, and nothing a stakeholder states about their own figures is overturned. The difficulty is that the export's row is a settlement record and the forecast replays charges.
- **Primary mechanism:** `forecasting`, `method_or_model_selection` supporting. **Flags:** `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`.
- **Deletion test.** Delete the panel log, the planners' guide and both distractors: the closed record still certifies the record-by-record replay on every 2026 reading, and it still files 155.
- **Clean-data test.** The export is not a suspect file: it is complete, current and at its documented grain, and joining its records into charges is the analysis, not a repair, since the closed load is identical before and after the join (S07). The off-path suspect files (gateway B, the fleet card file, restated versions, re-deliveries, reissued identifiers) are repaired one at a time and the answer, rung 4 and rung 2 stay put and apart (E02).
- **Lens swap.** No. Records and charges are two grains of the same correct data and give the same load in every closed quarter-hour (S07); they differ only under the forward regime, where a faster unit lets a charge finish before the run. The answer and rung 5 differ only through the forward replay, as rung 4 and the answer do through the forward fleet (E04).
- **Pre-draw identity.** Contracted demand = 1.12 x the maximum over billing quarter-hours of the sum over concurrently charging charges (records joined end to start at one unit under one permit or card) of min(11.5 kW, the onboard rating of the car the charge's permit carries in the contract year), each 2026 charge re-timed from its first start at that draw.

### The ladder as built (the natural path runs on records)

| Rung | Construction | Unrounded (kW) | Filed (nearest; up) | Against the answer | Set at | Killed by |
|---|---|---|---|---|---|---|
| 0 | panel log, the highest month's two registers x 1.12 x 11.5/6.6 | 412.16 | 410; 410 | +219.2% | several months | Schedule 26 billing window |
| 1 | closed billing maximum 158.4 x 1.12 x 11.5/6.6 | 309.12 | 310; 310 | +139.4% | 12:00, 17 February 2026 | the readings (a faster unit shortens a session) |
| 2 | replay at 11.5 kW (records and charges agree, A40) | 103.04 | 105; 105 | -20.2% | 12:00, 10 June 2026 | the Library vans at 11.0 kW |
| 3 | replay at the Library vans' 11.0 kW (records and charges agree) | 98.56 | 100; 100 | -23.7% | same quarter-hour | the pickup at 11.5 kW on the same unit |
| 4 | per car, each record's car on its own date, record by record | 162.243 | 160; 165 | +25.6% | 12:00, 17 February 2026 | the January 2027 renewal rows under the filed permit rule |
| 5 | per car, the contract-year car, record by record | 155.357 | 155; 160 | +20.3% | 12:00, 8 December 2026 | the zero-gap pairs at the run, and the statements' charge counts |
| 6 | **per car, the contract-year car, charge by charge** | **129.136** | **130; 130** | answer | 12:00, 8 December 2026 | none |

Worth of each rung on the graded figure: 0 to 1 -25.0%, 1 to 2 -66.7%, 2 to 3 -4.3%, 3 to 4 +64.6%, 4 to 5 -4.2%, 5 to 6 -16.9%. The answer is bracketed by rung 3 below and rung 5 above, and every rung files a different figure (A22, A43).

"A solver who does everything right up to rung 5 commits to 155 kW and names December 2027 as the month that sets it."

### Position table (asserted)

| Rung | Unrounded | Filed | Month that sets it | North / South at its binding quarter-hour, scaled (kW) |
|---|---|---|---|---|
| 0 | 412.16 | 410 | several | 206.1 / 206.1 |
| 1 | 309.12 | 310 | February 2028 | 180.3 / 128.8 |
| 2 | 103.04 | 105 | June 2027 | 51.5 / 51.5 |
| 3 | 98.56 | 100 | June 2027 | 49.3 / 49.3 |
| 4 | 162.243 | 160 | February 2028 | 115.1 / 47.1 |
| 5 | 155.357 | 155 | December 2027 | 82.9 / 72.5 |
| 6 | 129.136 | **130** | **December 2027** | **82.9 / 46.3** |

Contract months, whole kW: the answer April 2027 90, May 85, June 79, July 72, August 75, September 87, October 94, November 103, December 129, January 2028 109, February 68, March 98; rung 5 the same months 120, 97, 98, 92, 110, 102, 126, 144, 155, 122, 99, 109 (every month differs, A42); rung 4 142, 118, 114, 101, 134, 130, 155, 154, 155, 138, 162, 125. North carries the same load on records as on charges at both quarter-hours, so the run's pairs that matter are South's (A44, V07h).

### Separation and dominance

The answer is a figure in 5 kW bins with no ranking, so the separation floor binds. Nearest single-error cells: growth left off 115.3 kW (-10.7%, files 115), the deck-average replay on 2026 vehicles 113.549 kW (-12.1%, files 115), each session's own car on charges 148.512 kW (+15.0%, files 150), settlement records with the contract-year car (rung 5) 155.357 kW (+20.3%, files 155). Nearest two-error cells, each two violations of opposite sign (A30, A31): own-date cars with growth left off 132.6 kW (+2.7%, files 135), settlement records with growth left off 138.712 kW (+7.4%, files 140); the same-sign pair, own-date cars on records, is rung 4 (+25.6%). Convergent readings, every one 129.136 kW with every month unchanged: the decks' own maxima summed, all 36 months, each permit's latest check (as of energization), vehicles as of the council vote, stamps read as interval ends, rounding up, and the over-merge. Bins unchanged: 129.136 sits 1.636 kW above the 127.5 edge and 0.864 below 130.

Dominance: each rung's kill fact is in a shipped file, and only the answer's construction survives all of them: the billing clause (Schedule 26) kills rung 0, the readings kill rung 1, the Library van sessions kill rung 2, the pickup kills rung 3, the renewal check rows under the filed permit rule kill rung 4, and the zero-gap pairs, the field notes' settlement run and the statements' charge counts kill rung 5.

### Closure table, the axes that moved

| # | Axis | Reading chosen | Closed by |
|---|---|---|---|
| 2 | Unit of account (now the decisive axis) | The charge: records that meet end to start at one unit under one permit or card, joined into one block from the first start, energy summed | Structural (S01, S04, S05, V07i: every join tolerance under 42 minutes selects the same pairs) + documentary (the field notes' settlement run) + C2 (the 2026 statements: chains 875 of 875 permit-months, records as charges miss 822, the over-merge 35) + C1 (the over-merge converges on the call, S09, V07g) + C4 (records as charges file 155, +20.3%) |
| 15 | Duplicate resolution | Re-deliveries once per authorization code; a pair is not a duplicate | C1 (each record of a pair carries its own code and its own times and energy, so neither the code rule nor an exact-duplicate test merges a pair, and the answer path joins pairs on time, not on codes) |
| 1 | Population | Adds: weekend and holiday courtesy charging is not in the export and never enters the call | C1 (no courtesy session charges in a billing quarter-hour, D16; zero courtesy rows in the main call's population, E01) |
| 4 | As-of dating | Unchanged from harden loop 1: the car each permit carries in the contract year | As in the harden loop 1 table |

Every other axis keeps its stage-2 or harden-loop-1 line.

### The ask ledger, re-hardened (as built)

**Pool A (the contract year, the month, the split, the chart).** Device-free and carried by rung 6. A solver at rung 5 files every contract month wrong (A42), South's 72 against 46, the gap of 70 against 95, and the chart's line and marked value; it keeps the month (December), the day, North's 83 and the planners' 225. A solver at rung 4 files every month wrong and names February.

**B1, the 2026 basis against the panel meters. Primary device (new, D4 absent channel): weekend and holiday courtesy charging.** Charging at the decks on Saturdays, Sundays and the Schedule 26 holidays is free to permit holders and Curbline does not settle it, so those sessions never reach the settlement export; all 720 of them (2024 to 2026) ship in `curbline_courtesy_sessions_civic_decks_2024-2026.csv` (station, permit, connected and disconnected in local time, energy). They charged through the panels, so leaving them out moves every 2026 reading by 56.7 to 185.2 kWh (D15). Off path: no courtesy session charges in any billing quarter-hour and none is in the export (D16); zero courtesy rows in the main call's population (E01). Silent: the export reconciles to itself and the residual still reads as lighting; the only symptom is that the decks, alone of the eight garages, have no weekend or holiday rows in the export (V07j). Hazards kept: reads inside a quarter-hour (demoted from primary: whole quarter-hours either way or to the nearest boundary move every reading by 1.5 kWh or more, pro rata by 0.76 or more, D13), the meter clock on standard time (readings 3 to 11, up to 79.5 kWh), the re-delivered December 2025 batch (reading 1, 20.8 and 20.5 kWh), the back-fed unit (North 6 and 7, 176.7 and 57.0 kWh), the double read (South 12, 99.2 kWh), repeats over-deduped, calendar spans. Every subset of mishandlings lands on a different whole kWh on every reading (D09, 24 readings); the nearest wrong value sits 0.76 kWh from its golden.

**B3, the standard's 2025 record. Primary device (new, D8 clock): the fleet card file stamps START and END in UTC.** The fleet card charges at the decks before the April 2025 platform move are not in the export and have to be added (the harden-loop-1 primary, now a hazard), at their local times. Read as local, every back-test top-up lands about eight hours late, outside the noon quarter-hour, and all 24 figures land exactly where leaving the charges out lands them (C16). Recoverable without a sentence: every fleet charge after 1 April 2025 is in both files, and START is the export's plug-in in UTC to the second on all of them (C2, V19b). Hazards kept: fleet charges left out (all 24 figures, C07), the whole file added (seven of the April to December misses, C08), reissued identifiers (all 24, C09), the 1.09 vintage (all 24, C10), gateway B (January to April, C11), restated versions (May to July, C14), re-deliveries (October and December, C15). Under all 239 subsets of mishandlings the misses stay two-signed with a mean between -1.99 and +1.70 points (C05, C06).

**Separation, asserted zero inside the main call's population (E01):** re-delivered rows, restated versions, gateway B rows, fleet-card charges outside the export, reissued identifiers, rows outside the decks, rows outside the export, courtesy sessions.

### Pair arithmetic, restated

Planning weights 38 / 7 / 55. A solver who stops at rung 5 files 155 (160 rounded up) and loses the call, every contract month, the South split, the gap and the chart's line and marked value; it keeps the month, the day, North's 83 and the planners' 225. If rung 6 holds the field off the call, each top response scores about r + 7 + 55 L and the pair stays under 40 while each keeps under about half the pool-B weight, so B1's courtesy channel and B3's clock, each moving every figure in its ask, have to fall together before the asks alone lift the pair over the target. If one top response lands the call, the pair reaches 40 only when the two together keep under about 0.47 of the ask weight, which needs at least one of the two fresh primaries to hold against both.

### Stopping rule for the next round

At ceiling: a response files 130 kW by joining the pairs in round 3; loop 3 is then the last on this architecture and a re-root at stage 1 is the default. One more repair (loop 3): the pair clears 40 with at most one response on the call (a pool-B repair, one device per repair), or a response reaches 130 without joining the pairs (a determinism finding, not a difficulty repair). Working as built: responses that stop at rung 5 (155 kW) or below.

## Build record (harden loop 2, 2026-10-09)

Rebuild and verify exactly as the stage-3 record says (`build_pack.py` with seed 1172027, then `verify_pack.py`), then `golden.py` for the deliverables.

- **Generator green:** 419 named assertions (main call and ladder 45, the renewal 7, the settlement run and the charges 9, corpus and twins 23, back-test 265 of which 239 are subsets of mishandlings, panel audit 39 of which 24 are readings, separation and Gate G tests 9, register referee 3, container scrub 5, pack gates 14), all passing.
- **Independent verifier green:** 48 checks, 0 failures. It reads only `target/` and `metadata.json`; it joins zero-gap chains per station and permit or card, recomputes the answer and both record-by-record rungs with their quarter-hours and splits, reproduces every permit-month of the statements from the chains (and shows records and the over-merge do not), shows the over-merge converges on the call, parses the fleet card file's START and END as UTC, and adds the courtesy sessions to the panel spans.
- **Byte-identical:** two consecutive scratch builds agree on all 26 outputs by sha256 (24 pack files, `metadata.json`, the build record); the task folder's `target/` and `metadata.json` match them on all 25. `golden.py` run twice: the three deliverables byte-identical, printouts identical, and the task folder's goldens match.
- **Input gates:** 24 files in six formats (csv, parquet, xlsx, pdf, docx, txt); the spine holds 1,538,706 rows; two distractors named in `metadata.json` and unread by the verifier.
- **Containers:** the scrub audit is clean on `target/` and on `golden/` (band 2023-01-01 to 2027-01-25).
- **Pack changes:** `settled_sessions_2024-2026.csv` 111,280 rows and `session_intervals_2024-2026.parquet` 1,538,706 rows, the run's pairs included; `curbline_courtesy_sessions_civic_decks_2024-2026.csv` added (720 sessions); `ev_permit_charging_statements_2026.csv` added (875 permit-months); `fleet_card_ev_transactions_2024-2026.csv` 5,372 rows with START and END in UTC; the field notes file the settlement run's time under settled_on; the data-sources note registers both new files (every shipped file listed).
- **Asks as built:** pool A, B3 and B1 exactly as the harden loop 1 record states them (the 12 contract months, 83 and 46, 225 and 95; the 12 back-test forecasts and misses; the 24 panel figures), every golden unchanged.

## Write-up and ship checks (stage 3 rebuild after harden loop 2, 2026-10-09)

- **Pack:** two scratch rebuilds (`build_pack.py`, 419 assertions green, answer 129.136 kW) match `target/` and `metadata.json` byte for byte on all 25 files; `verify_pack.py` 0 failures.
- **Goldens:** `golden.py` reads only `target/`, joins the pairs before the replay, asserts that records less charges equals the pairs, and asserts every figure against `verify_pack.EXPECTED`. The memo's method paragraph names the run and the 3,033 pairs joined and the memo stays one page; the workbook's back-test sheet notes the UTC stamps, its panel sheet the courtesy sessions, and its Notes sheet the settlement run and the courtesy report; the chart is byte-identical to the harden-loop-1 golden. Two runs byte-identical, printouts identical.
- **submission.md:** blocks 1 to 3 revised through `submission-writeup` (block 1 gains the records rival; component 1 the joined records; step 2 the join and the statements; step 6 the UTC stamps; step 7 the courtesy sessions); block 4 unchanged and checked against the PDF, the workbook and the build record by a scratch cross-check (0 failures).
- **golden-realism:** figures frozen first; memo in genre (memo block, finding title, lopsided sections, table with a source line, billing-demand footnote, page footer); workbook with named sheets, frozen headers, set widths, per-column number formats, print areas and a notes sheet; chart unchanged.
- **reduce-house-fixes:** H1 clean on both trees; H2 every new figure in this note comes from the build record or the verifier (the over-merge convergence, rung 4's record-by-record quarter-hour and split, the 42-minute floor between records under one permit, and the decks' empty weekends in the export were measured in scratch first and are now asserted, S09, A44, V07g, V07h, V07i, V07j); H3 two golden sentences corrected (the memo's "every car charging at 10 a.m." becomes "every car still charging at the run", since the run reaches each garage between 10:00 and 10:07; the Notes sheet's "the same unit and permit" becomes "the same unit, under the same permit or fleet card", since fleet card charges are split too); H4 `golden/` holds exactly the three named files; H7 byte-identical reruns; H8 every citation resolves (FES-07 sections 2 to 4 and Table 1, Schedule 26 sections 3, 4 and 7, agreement section 4, Exhibit A and Schedule 1, guide section 7, WO-26-0418, circuit 33, the field notes' settlement run, the courtesy report and the statements by file name); H9 the data-sources note lists all 23 other shipped files; H11 one `submission.md`, one `prompt.md`; H16 no date in any extract after the 18 January 2027 export (latest 13 January 2027); H20 G09 green.
- **leak.py:** REVIEW, 6 lines, no LEAK (answered under `## Leak review`).
- **guard.py:** card restated (stump, driver, driver_concrete, G3 first among the generators, spine rows 1,538,706, notes); `validate` 119 cards, 0 invalid; `check` PASS (task37, task44 and task97 noted, already differentiated); `heart` PASS (nearest stump 0.05, task107; nearest driver 0.06, task110); `surface` promotes task37, task97 and task44 on card mechanism axes only (surface 0.075 to 0.089), already differentiated; personas in the pack: Shelley Tanner, Ricardo Moore, Paul Henderson. Recorded as the decisive mechanism the new rung blocks: as pattern D, test.same_driver against task115 (time, D, forecasting); as a decisive G3, ban.pattern against task121. The card keeps E (the architecture's conditioned yield) as its pattern and lists G3 first among the generators, as harden loop 1 did with G6; the author decides whether the rung is a new decisive mechanism.

## Write-up and ship checks (stage 3 re-pass after harden loop 2, 2026-10-09)

- **Pack:** a scratch rebuild (`build_pack.py`, seed 1172027, 419 assertions green, answer 129.136 kW) matches all 24 files of `target/` and `metadata.json` by sha256; `verify_pack.py` 48 checks, 0 failures.
- **Goldens:** `golden.py` run twice into scratch, printouts identical and every figure as the harden loop 2 record states it (130 kW, 129.136 unrounded, December 2027, 83 and 46, 225 and 95, the 12 contract months, the 24 back-test figures, the 24 panel figures). The workbook and the memo are byte-identical to the shipped goldens; the chart moved in its source strip only (below), its series, line, marker, title and labels unchanged.
- **submission.md:** unchanged; its five blocks checked against the printout, the memo text, the workbook cells and the meter log's read dates (every block-4 figure matches).
- **golden-realism:** figures frozen first; every golden opened cold. One edit: the chart's source strip said "each session replayed from plug-in", which describes the record-by-record replay (rung 5) rather than the answer's; it now reads "2026 deck charges (records split at the settlement run rejoined); each charge replayed from its start", matching the memo and the workbook's Contract year note. Two reruns byte-identical, the figures unchanged.
- **reduce-house-fixes:** H1 the scrub audit clean on `target/` and `golden/`; H3 and H6 the chart strip above, the memo's $12,996 (95 kW x $11.40 x 12) and 32 x 11.5 x 0.60 = 220.8 rechecked against Schedule 26 section 2 and guide Table 7-2; H4 `golden/` holds exactly the three named files, each opened; H7 byte-identical reruns; H8 every citation resolves (Schedule 26 sections 2, 3, 4 and 7; FES-07 sections 2 to 4 and Table 1 with its three adoption dates; agreement section 4, Exhibit A and Schedule 1; guide section 7.3 and Table 7-2; WO-26-0418; circuit 33 on both panels); H11 one `submission.md`, one `prompt.md`.
- **leak.py:** REVIEW, 6 lines, no LEAK (answered under `## Leak review`). **guard.py surface:** task37, task97 and task44 promoted on card mechanism axes only (surface 0.075 to 0.089), already differentiated on the card; personas in the pack: Shelley Tanner, Ricardo Moore, Paul Henderson. **guard.py heart:** PASS (nearest stump 0.05, task107; nearest driver 0.06, task110). Card answer, answer_source, spine rows (1,538,706), deliverables and opening move confirmed current; `validate` 119 cards, 0 invalid.

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
- Stage 3, back-test forecasts and 2025 actuals tuned to within 0.01 kW of a whole kW so every rounding path filed the same miss: twelve forecasts landing on round values under the 1.08 factor (and off them under 1.09, the raw identifier join or gateway B left out) is a receipt that confirms the intended handling; replaced by filing the accuracy record in FES-07 (whole-kW forecast against whole-kW recorded demand) and placing every forecast and actual 0.06 to 0.24 kW off a whole kW.
- Stage 3, back-test partials in 6-second steps (0.044 kW) with both the forecast and the actual held near a whole kW: almost no month had a candidate; replaced by partials at 0.004 kW resolution, still exact at 0.001 kWh, chosen by a seeded search.
- Stage 3, back-test misses landing exactly on -1.0 and -2.0 per cent (a recorded demand of exactly 100 kW): an exact round share is a generation tell; misses within 0.004 of a one-decimal value are excluded.
- Stage 3, panel-audit read times searched with the whole-kWh bin test as a hard filter: each golden is the roof lighting in the span plus display truncation, so it barely moves with the read time and most months had no passing time; read times are now chosen on the meter-clock and mishandling tests alone and one evening's photocell switch-on inside each span is trimmed, repeatedly because the registers truncate to 0.1 kWh, until the golden lands 0.06 to 0.24 kWh off a whole kWh.
- Stage 3, panel goldens trimmed to 0.05 kWh from a whole kWh: 24 near-whole goldens is the same receipt as the near-whole forecasts; the trim targets 0.11 to 0.19 kWh off a whole kWh.
- Stage 3, the unit on the temporary house-panel feed left empty for the six weeks of the feed (the day builders skip a blocked unit): the back-feed then moves nothing; the unit takes afternoon arrivals only, so it never charges in a panel's morning maximum and still moves North readings 6 and 7.
- Stage 3, the April 2024 back-test day drawn after the legacy gateway's retirement on 22 April: its gateway partial sat in the settlement export and the gateway device moved January to March only; the April day is now drawn before the 18th.
- Stage 3, fleet sessions assigned to fleet cards at random: one vehicle could charge at two garages at once; every fleet card carries its own occupancy.
- Stage 3, the restatement referee asserted as "no restated session charges in the panel's maximum quarter-hour": too strict, since the versions of a session differ only in their last quarter-hour; replaced by asserting that keeping the latest or the first version changes no register.
- Stage 3, the 31 December misread as an upward digit transposition with a +90 kWh fallback: the register's digits rarely allowed the transposition and the fallback is not a misreading; replaced by the hundreds digit read as a digit it is often mistaken for.
- Stage 3, a load-management clause in the planning guide (a system that caps the units' total draw): a shipped sentence about a limit on draw, and a question the agreement never answers; replaced by a construction clause.
- Stage 3, a provenance sentence saying a restated version replaces the earlier one once Parking Services "accepts" it: the word is the stump's vocabulary and failed the signpost grep; reworded to the ACCEPTED and REJECTED codes the decisions file carries.
- Stage 3, the design's departure assertion (every closed plug-out at least two hours after delivery at 7.2 kW): the lunch-time unplug-and-replug sessions and the late arrivals end their visits sooner; the operative property, delivery finished before plug-out, is asserted instead.
- Stage 3, the briefing-thread social layer: the prompt already carries the facilities engineer's expectation and the planners' method is filed in their guide, so the thread would only restate both; not built.
- Stage 3, the house scrub script given "North Sound Power & Light" for an OOXML file: it writes the producer into docProps unescaped and the bare ampersand broke the DOCX; the build passes an XML-escaped producer for OOXML.
- Stage 3, a note sentence saying no forecast month comes within 1 kW of the contract: February 2028 sits 0.93 kW under 150, so the sentence was false of the record; replaced by the ratchet's own wording.
- Stage 3, the golden workbook saved through openpyxl without repacking core.xml: `dcterms:modified` carried the build clock, inside the audit band so the scrub passed it, and made two runs differ; the repack now pins created and modified to the note's date.
- Stage 3, an agenda item number in the note's footer: the pack carries no agenda, so the number was invented texture; removed.
- Stage 4, round 1 (plain solver, proxy 88.1, call landed at 150 kW, every ask figure matched): the five-rung ladder as built, with rung 4 (the per-car onboard limit) silent in the documents. The solver skipped rungs 0 to 3 outright, reading Schedule 26's billing window and replaying sessions from the start, then executed rung 4 as a work order at path step 4: "Vehicle limits: matched each permit session to the vehicle on its latest permit_vehicle_checks entry on or before the session date, and fleet cards to city_fleet_roster. Looked up onboard_charger_kw in vehicle_reference_list by make, model, trim and model year ... The new rate is min(11.5, onboard)." A shipped onboard_charger_kw column sitting one join from the sessions is not a silent rung, because a solver replaying a charger swap asks what the car accepts by default. Every ask device also fell (gateway B in the 2024 base, 1.08 in force at the forecast date, standard-time meter clock, the N-11 back-feed, the later 31 December read). Harden loop 1 of 3 on this architecture.
- Harden loop 1, diagnosis of round 1 (the min(11.5, onboard) replay as the decisive rung, and five ask devices each adjudicated by a filed rule on the ask's own path): the decisive property was itself a shipped column (onboard_charger_kw), which is the way Pattern E degrades into a two-column lookup, so the solver's "Looked up onboard_charger_kw in vehicle_reference_list by make, model, trim and model year ... The new rate is min(11.5, onboard)" was a work order, not a discovery; and every ask device's organ sat in a file the ask path already opens, so the battery executed each one as written ("mapped station_id to garage using station_register in-service dates, because six old Civic IDs were reused", "Converted meter times from fixed PST (DST disabled)", "moving N-11 to HP-N for 1 Jun to 12 Jul 2026 per the circuit schedule and WO-26-0418", "keeping the later read when a meter has two reads on one day"). Dead: any rung whose answer is the listed onboard kW, and any ask device whose rule is filed where the ask's own files state it.
- Harden loop 1, February's binding day held at the stage-3 rung-4 figure of 149.072 kW (five renewed cars, six South 7.2 kW cars, the only composition whose contract-year February sat mid-bin): South's February load then exceeded any December South the answer could carry, so summing each deck's own maximum stopped converging; February moved to ten renewed cars and two South 7.2 kW cars (148.512 kW, still filed 150) and December carries both decks' maxima.
- Harden loop 1, the twins' closed loads equal at the rung-4 binding quarter-hour and both decks' 2026 closed maxima within 1 kW (the stage-3 twin assertions): incompatible with a December answer day, a February rung-4 day and the deck-maxima convergence at once; equality is kept at the answer's binding quarter-hour only (66.0 kW each).
- Harden loop 1, February's early car drawn from the renewed pool under the 9.75 kW bound alone: at its contract-year 11.0 kW it finished at 11:46, inside the 11:45 quarter-hour, so the end-stamp reading moved February's contract month by 0.67 kW; the early kind now also finishes by 11:44 at 11.0 kW.
- Harden loop 1, one read minute shared by both deck meters with reads off the quarter-hour: the pro rata split moves a reading by under a kWh at most instants, and no single minute moved both panels' readings far enough; each meter now has its own read minute, searched panel by panel with backtracking.
- Harden loop 1, the fleet-card device sized at 0.70 kW with only the twelve forecasts required to move: January and March held their one-decimal misses because the forecast and the recorded demand both dropped a whole kW; the parameter search now requires the device to move all 24 figures.
- Harden loop 1, a growth-factor regex matching any 1.12 in a shipped CSV: the fleet card file's dollar amounts tripped the single-statement gate on a currency cell; the rule's regex excludes CSV cell context.
- Stage 3 rebuild after harden loop 1, the memo sentence "for the 11 kW cars that is right" (answering the facilities engineer): 44 of the 3,404 morning sessions by cars at 11.0 kW still charge past noon on the new units, so the universal claim was false of the record; reworded to "nearly always" and the share asserted in `golden.py`.
- Stage 4 after harden loop 1, round 2 plain solver (proxy 89.2, call landed at 130 kW, every graded figure matching the golden, the 6 of 12 token score an undercount of formatting): rung 5, the contract-year car, read as a work order at path step 4: "Re-simulated each 2026 session at min(11.5 kW, OBC), using the vehicle on the permit at the January 2027 renewal (18 County Bolt EVs went from 2020 at 7.2 kW to 2023 at 11.0 kW)", because the renewal rows sit in the checks file the solver already joins and FES-07's "equipment the service will supply" reads as the forward fleet; both fresh pool-B primaries fell too (step 6 added the fleet-card charges by NETWORK_REF, step 7 split reads on the "exact constant-rate profile, not 15-minute bins"), so loop 1 bought nothing on either layer.
- Harden loop 2, diagnosis of round 2 (rung 5, the car each permit carries in the contract year, as the decisive rung; fleet-card charges outside the export as B3's primary; reads inside a quarter-hour as B1's primary): the contract-year car sat in the checks file and on the permit join that rung 4 already walks, and a forward forecast's own default as-of is the forecast date, so the solver's "Re-simulated each 2026 session at min(11.5 kW, OBC), using the vehicle on the permit at the January 2027 renewal (18 County Bolt EVs went from 2020 at 7.2 kW to 2023 at 11.0 kW)" was the last link of the chain it was already building, not a question it had to think to ask, and it priced rung 4 itself in passing ("With 2026 vehicles it would be 150 kW"). Both primaries died the same way: the fleet file's NETWORK_REF is a key a reconciling solver tries against the export by reflex ("40 Civic fleet-card transactions whose NETWORK_REF is missing from the settlement export"), and a read inside a quarter-hour invites the exact split of a profile the solver had already validated at step 3 ("Session kWh between reads comes from the exact constant-rate profile, not 15-minute bins"). Dead: a decisive rung that is a dated attribute of an entity the chain already joins, and an ask device whose organ is a key or a profile the solver has already validated for another step. Harden loop 2 of 3 on this architecture.
- Harden loop 2, rung 5 (the contract-year car, record by record) targeted at about 151 kW so that it filed 150 like the rung round 1 and round 2 priced: as built the run's pairs put 72.5 kW on South at noon on 8 December and rung 5 lands 155.357 (155, 160 rounded up); kept, because it files apart from every other rung and sits 20.3 per cent above the answer, and A41 and A22 assert the as-built bins.
- Harden loop 2, courtesy sessions drawn from every weekend and holiday session at the decks, gateway B's included: the legacy gateway export already carries the January to April 2024 sessions, so those would sit in two files; the courtesy report leaves gateway B sessions out.
- Harden loop 2, the settlement run splitting every session whose delivery spans the run instant: a delivery ending within a second of the run left a second record of zero kWh at three decimals; a session is now split only when its delivery runs more than a second past the run, and the fragment energies are asserted in the generator (first records at least 0.066 kWh, second records at least 0.001).
- Harden loop 2, panel read times kept from harden loop 1 once the courtesy sessions joined the spans: attributing whole sessions by plug-in time then landed 0.093 kWh from one golden (D12); the read-time search now rejects any time at which that rival lands within 1.5 kWh of the golden or on the same whole kWh.
- Stage 3 rebuild after harden loop 2, the memo sentence "record by record every car charging at 10 a.m. would restart at full power": the run reaches each garage between 10:00 and 10:07, so a car that finishes in those minutes is not split; reworded to "every car still charging at the run", and the Notes sheet's "the same unit and permit" to "the same unit, under the same permit or fleet card", since fleet card charges are split too.
- Harden loop 2, recording the new rung as the card's decisive mechanism: as pattern D (two grains) it repeats task115's (time, D, forecasting) signature (test.same_driver BLOCK) and as a decisive G3 (record versus operation) it repeats task121 (ban.pattern BLOCK); the card keeps E as the architecture's pattern and lists G3 first among the generators, as harden loop 1 did with G6, and the overlap goes to the author.
- Stage 3 re-pass after harden loop 2, the chart's source strip "each session replayed from plug-in": with the run's pairs in the export a session record is not a charge, so the strip described rung 5's replay; reworded to the charge, the records split at the run rejoined, in `golden.py`.
- Stage 4 after harden loop 2, round 3 plain solver (proxy 90.4 with landed read by hand, since the token match missed "April" and "March" in a sentence filing the same 130 kW; call landed at 130 kW, December 2027, North 83 and South 46, and every ask figure in block 4 matched exactly, the 6 of 12 token score again a formatting undercount): rung 6, the settlement run's record pairs, executed as a work order at path step 3, before any replay: "Found that the 10:00 settlement run splits sessions: 8,741 pieces where plug_in equals the previous plug_out at the same position with the same card. Merged them into 20,497 physical sessions. ev_permit_charging_statements_2026 confirms this: charges equal merged sessions in 100% of permit-months, and kWh ties exactly." Then rung 5 at step 5 ("The charger rating comes from the permit's Jan 2027 renewal vehicle") and both rivals priced in passing at step 6 ("with 2026 vehicles the maximum would be 149 kW; with unmerged session pieces it would be 155 kW"). Zero-gap end-to-start records at the same unit under the same card are found by the hygiene sweep a solver runs on any session export before building a load model, and the charging statements hand it a reproduction check it runs for free, so the pairs were a cleaning step rather than a rung; and the asks held nothing through three rounds because every device sits on a file the ask path already opens with its rule written beside it. Third crack of this architecture with harden_loops at 2: one hardening loop remains under the three-loop rule before a re-root.
