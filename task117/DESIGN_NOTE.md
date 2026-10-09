# task117: the Civic Center decks' contracted service demand, realising analytical_tasks note FC01 (analytical_tasks/01_forecasting/FC01_garage-service-demand-vehicle-limited-draw.md)

Stage 1 (draw), drawn 2026-10-08. This is the build's one design note; the design stage extends it.

## Draw

```
DRAW  (independent draws, checked with .claude/skills/fingerprint/guard.py)
  Card filed with guard.py register before the ladder was written? pending batch registration   Verdict: WARN
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

## Tried and rejected
