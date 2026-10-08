# OS25 — Which of five newly legal states a sportsbook should open first, when part of a state's market lives across the state line

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · regulated gaming markets |
| Mirrors | Launch sequencing for geofenced or local services whose demand at a market's edge comes from neighbouring areas the service cannot yet reach at home (Uber and Lyft city launches drawing riders across metro lines, Amazon same-day delivery zones, DoorDash and Instacart catchments, cross-border shopping in retail site selection), where the comparable markets' history holds demand that a new market will or will not inherit |
| Decision shape | Which of N gets one scarce thing (the opening launch team), with the sizing kept as the graded figure |
| Committed call | The state launched first, and that state's year-2 statewide mobile gross gaming revenue in $M to one decimal |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · Pattern B (a reproduction clause over a published control set; the market is a population built across a state line through a county adjacency join and a dated status), with an implicit brand-to-host-licence join (#18) below it |
| Gate G mechanism | method_or_model_selection, with forecasting |
| Measured traps engaged | #3 stops at a close but inexact match · #8 papers over a failed reproduction · #18 joins only on the visible key |
| Calibration form | Published control set with a reproduction clause: the regulators' compendium of year-2 mobile GGR for 14 launches from 2019 to 2024, and the board's policy admitting a sizing model only if it reproduces all 14 to the published $0.1M |
| Driving force | A mobile bet is placed where the phone is, not where the bettor lives. A state's year-2 market therefore includes the adults in adjacent counties of neighbours that have no legal mobile wagering through that year. Built through the county adjacency file and each neighbour's first day against the year-2 window, that population is the only construction that reproduces all 14 published figures (status read at launch reproduces 12, in-state adults 8). Granby, fourth of five by adults, sits against the suburbs of a neighbour with no statute. |

## 1. Situation

A sportsbook operator holds market access in the five states that open to mobile wagering on 1 January 2027: Alston, Brough,
Everly, Granby and Varley. It can staff one launch at the start and will open the other four through the spring. The board's launch
policy sequences states by statewide mobile gross gaming revenue (GGR) in year 2. It admits a sizing model only if the model
reproduces the regulators' compendium of year-2 figures for the 14 states that opened from 2019 to 2024. The pack holds the
compendium with its per-licence annex and definitions note, each state's licence register and market-access register, county
population estimates, a county adjacency file and the regulators' launch calendar. The industry association's market-depth index is
filed. Every regulator's geolocation rule requires a wager to be placed from a device located inside the state.

## 2. Gate G: why this is legal

* **Litmus.** Every reported figure is correct: the 14 published year-2 figures, the annex, the licence and market-access registers, the
  county estimates, the adjacency file and the launch calendar. No stakeholder read is overturned. The difficulty is which adults make
  up a state's market in 2028, and that is a population no file stores.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the chief commercial officer's belief and every voice. The brand model still reproduces 8 of 14 at one rate,
  the launch-date construction still reproduces 12 and names Everly, and the clause still sends the solver hunting.
* **Instrument repair.** One file is suspect: the compendium annex, whose operator field records the host licence, not the brand that took
  the bets (a narrower meaning). Repair it at all three depths: fill in each line's brand, read the line as the brand, then replace the
  annex with a register of live brands and each brand's GGR. Rung 1 then collapses onto rung 2 (Everly, 1.25× clear), rung 0 still
  returns Brough, and Granby still needs the border construction. Every other file is complete and current. Replace even the compendium
  with year-2 GGR split by bettor residence, the instrument that records cross-border play directly. The flat rate still names Brough,
  the brand model sized on residents still names Everly, and Granby's 2028 market must still be built from Sorrell's border counties
  and each neighbour's status in 2028.
* **Lens swap.** In-state adults and the adults who can place a bet inside a state's line in 2028 are different populations. The answer
  adds 4.6 million adults who live in Sorrell.

## 3. The driving force

A strong solver drops the flat per-adult rate as soon as the clause tests it. It adds the market-depth index and, from the market-access
register, counts brands rather than licences. Eight of the 14 controls then agree on one rate to the cent: $64.0 per adult at eight
brands. In all six misses the published figure sits above the model, and two of them opened in 2023 and 2024, so no early-market premium
explains them. What the six share is a neighbour with no legal mobile wagering through their year 2. A mobile bet is placed where the
phone is, so adults in the counties across that line drive over it to bet. Build that population through the county adjacency file,
compare each neighbour's first day against the comparable's own year-2 window, and sum adults from the county estimates: half a bettor
per such adult reproduces all 14. Forward, Everly's populous neighbour Tolland opens in July 2027, inside the candidates' first year,
and adds nothing in 2028. Granby sits against the suburbs of Sorrell, which has no statute: 4.6 million adults whose nearest legal bet
in 2028 is across Granby's line.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The comparables' median year-2 GGR per in-state adult ($74.4) × each candidate's adults | Brough, $372.1M (1.39× Alston) | The industry's standard comparable, read at the same stage of maturity | The clause: one per-adult rate reproduces at most 2 of the 14 published figures, which run from $32 to $132 per adult |
| 1 | The market-depth index at each state's licence count, at the rate on which the controls agree | Alston, $257.6M (1.31× Brough) | Market depth is the textbook driver, the licence register is the regulator's own list, and 4 controls agree on one rate | The market-access register: brands take bets under a host's licence, so Alston's ten licences carry four live brands and Everly's four carry twelve |
| 2 | The index at live brands from the market-access register | Everly, $203.8M (1.25× Alston) | Eight of 14 controls agree on $64.0 to the cent, and the six misses read as local enthusiasm | The launch calendar: each of the six misses had a neighbour with no legal mobile wagering through its year 2 |
| 3 | **Decisive:** effective adults are in-state adults plus half the adults in adjacent counties of neighbours with no legal mobile wagering through the year-2 window (county adjacency file × launch calendar × county estimates), × the index at live brands | **Granby, $337.0M** (4th of 5 on rung 0; 1.65× Everly) | — | — |

* **Position table.** Granby ranks 4th on rung 0, 5th on rung 1 and 4th on rung 2, and leads only rung 3. It is never 2nd on a rung.
* **Discriminator dominance.** Everly carries a 1.30× advantage into rung 3 ($203.8M against $156.8M). Its border multiplier is 1.00,
  because Tolland is open by 2028, against Granby's 2.15. That is an edge of 2.15×, 1.38 times the required 1.2 × 1.30 = 1.56. The
  product, Granby over Everly at rung 3, is 1.65.
* **Partial correction priced (L3).** Every half-applied construction names a wrong state. Neighbour status read at each launch instead
  of across year 2 reproduces 12 of 14. Forward, it counts Tolland's 5.6 million border adults for Everly and names Everly by 1.26×.
  Status read today also counts the fellow candidates: Everly by 1.21×. Every adjacent county regardless of status: Everly by 1.35×.
  The right border population with licences in the index: Alston by 1.26×. The right border population without the index: Brough by
  1.21×. Whole neighbouring states instead of border counties, weight refitted on the controls (0.16 to 0.17): Varley, which also touches
  the far edge of the 16-million-adult holdout Quorn, by 1.32× to 1.35×.
* **Grid.** Brand count (none, licences, live brands) × border population (none, status today, status at launch, every adjacent county,
  whole neighbouring states, status across year 2) gives 18 cells. Only live brands × year-2 status names Granby. Every other cell names
  Brough, Alston, Everly or Varley. The nearest wrong cells are one toggle away: the year-2 border without the index (Brough by 1.21×)
  and status read today (Everly by 1.21×). Reaching Granby from either takes the other half of the construction.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The policy makes reproduction the gate, and the geolocation rule says where a bet must be placed. No document
   says a state's market includes adults who live across the line, which counties count, or which date sets a neighbour's status.
2. **Reproduction, not a menu.** The year-2 construction reproduces 14 of 14 to the published $0.1M. The best rival, status read at each
   comparable's launch, reproduces 12. Its model overshoots both misses (Kirkby, Upton), so it fails the 14-launch total by +3.4%. Status
   read today reproduces 10, and its model falls short on all four misses, the 2019–2020 launches (−11.0% on the total). In-state adults
   reproduce 8, every miss short (−13.4%). The reproducing rule is a construction. Its population comes from a county adjacency join, gated
   by comparing each neighbour's first day against a window computed from the comparable's own launch, and summed from the county estimates.
   The rate and the weight of one half can be fitted only once that population exists. No sweep over in-state models reaches it.
3. **No arithmetic symptom.** Annex lines sum to the compendium's figures, county adults sum to state totals, and every brand in the
   market-access registers maps to a licence in the annex.
4. **Not a row predicate.** Granby's market is a sum over another state's counties, gated by a date comparison against a window, not
   by any status column. No row in any file belongs to it.
5. **The enumeration is arithmetic.** No column names a market population. Sorrell's 4.6 million adults enter Granby's figure through
   adjacency alone.
6. **No cutover date.** Sorrell has never legislated. The compendium publishes one figure per launch, and no shipped series steps.
7. **Survives deletion.** Removing every voice leaves the clause and a 12-of-14 rival.

## 6. The calibration corpus

* **Form.** The regulators' compendium: year-2 mobile GGR for 14 launches from 2019 to 2024 (the controls), with the per-licence annex
  and the definitions note. The board's reproduction clause makes the compendium a gate.
* **What it pins.** The year-2 construction, 14 of 14. Status read at launch reproduces 12, status read today 10, in-state adults at live
  brands 8, and whole neighbouring states 8 (only the eight without border inflow). Licences with the year-2 border reproduce 6,
  licences alone 4, every adjacent county at most 3 at a weight of one half, and a flat rate at most 2.
* **Twin pair.** Penrose and Thursby are identical on every lookup-visible column: 1.10 million adults, three licences hosting six brands,
  a January 2023 launch, and 2.2 million adults in adjacent counties across the state line. Their published year-2 figures are $121.9M
  and $61.0M, 2.0× apart. Penrose's neighbour is Sorrell. Thursby's neighbours had opened before it launched. Only the status-at-year-2
  construction separates them.
* **Free training instance.** Sorrell borders two comparables, Penrose and Stanmore, where its adults show up harmlessly in the corpus,
  and Granby, where they decide.
* **Resemblance points at the decoy.** Everly matches Delamere 2019 on three brands per licence and on a populous neighbour without legal
  wagering today, and Delamere's $131.7 per adult is the highest year-2 figure on file. Tolland opens inside Everly's first year. On the
  status that matters Everly is Upton, whose neighbour opened during Upton's year 1 and added nothing to its year 2.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The launch policy: states are sequenced by statewide mobile GGR in months 13–24 from each state's first day of mobile
  wagering. The clause: a sizing model may be used only if it reproduces the compendium's year-2 figure for all 14 comparable launches
  to the published $0.1M. The association's market-depth index: per-adult GGR scales with the square root of live mobile brands, indexed
  to eight. Population: adults aged 21 and over, latest county estimates, held flat.
* **Empirical pins.** Border counties from the adjacency file. Each neighbour's status from its first day in the launch calendar against
  the window. Live brands from the market-access registers. The rate ($64.0) and the border weight (one half) from reproduction.
* **Voices.** The chief commercial officer: "Brough is the biggest prize; size wins." The head of trading: "Depth of competition builds a
  market; go where the brands are." The compliance lead: "Geolocation keeps out-of-state players out, so the neighbours don't matter."
* **Licensed wrong basis.** The policy records that investor relations' per-adult sizing (in-state adults at the median comparable
  rate) is shown beside any model as the reference case.

## 8. Determinism by construction

* **Status windows.** No neighbour's first day falls inside any comparable's year-2 window or inside 2028, and every launch falls on the
  first of a month. Status read across the window, at its start or at its end therefore gives the same set. Tolland's first day, 1 July
  2027, falls inside the candidates' year 1.
* **Holdouts.** Sorrell and Quorn have no enacted statute and no date in the launch calendar, whose note says it lists every enacted
  opening date.
* **Adjacency.** The file lists rook adjacency (a shared boundary segment). No county touches a state line at a point only, so rook and
  queen readings agree.
* **Brands.** Every agreement in the candidates' market-access registers is approved with go-live on 1 January 2027, and no comparable's
  brand count changes inside its year 2.
* **Exact controls.** The world is built so each published figure equals the construction at $64.0 per effective adult and a border
  weight of one half, to the published $0.1M. Any two controls with different border shares return that rate and weight, and every rival
  misses at least one control by $37M or more.
* **Maturity.** Every comparable's year 2 closed by the end of 2025, before the compendium's cut-off, and nothing in it is restated.

## 9. Prompt sketch and deliverables

> We hold market access in all five states that open to mobile wagering on 1 January, and we can only staff one launch at the start. Our
> chief commercial officer says Brough, the biggest of the five, is the obvious opener. Tell me which state we launch first and how much
> mobile gross gaming revenue that state's market will take in its second year, in $ millions to one decimal, as the figure I put to the
> board. Send `launch_sizing.xlsx`, a chart `backtest_and_candidates.png`, and a one-page `board_paper.pdf`.

* `launch_sizing.xlsx` — the five candidates on each construction with its back-test against the 14 published figures, the hold sheet
  (ask A) and the stake sheet (ask B).
* `backtest_and_candidates.png` — a script-rendered two-panel chart. The left panel plots published against modelled year-2 GGR for the 14
  comparables under the brand model and the reproducing model (two marker styles), with the 45-degree line and the six brand-model misses
  labelled. The right panel shows the five candidates' year-2 GGR as bars, in-state and border-county parts stacked, with the chosen state
  marked.
* `board_paper.pdf` — the committed state, its figure, and the back-test that admits the model.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 14 comparable launches, year-2 hold: GGR divided by cash handle. *Device:* five
  regulators report handle including free-bet stakes, and the definitions note gives each state's promotional-wager line. Dividing by
  reported handle understates hold in those five by 15% to 25%.
* **Ask B (device-carried).** For each comparable, the average stake per wager in year 2. *Device:* two regulators count each leg of a
  parlay as a wager, as their reporting definitions say, and publish legs per ticket in an annex. Dividing their handle by reported
  wagers understates the average stake in those two by roughly half.
* **Ask C (validity).** Each candidate's year-2 GGR under the flat rate, licence counts, live brands, launch-date border status and year-2
  border status, with the number of controls each construction reproduces.
* **Decoupling.** Rebuilding the market on in-state adults changes no figure in asks A or B. Handle, promotional-wager lines and wager
  counts touch neither the compendium's GGR nor the border counties.

## 11. Rubric arithmetic

14 comparables × 2 (asks A and B) + 5 candidates × 5 constructions (ask C) + 5 reproduction counts + the committed state and its figure
+ 5 named chart parts + 3 files ≈ 68 criteria.

## 12. World-building constraints

* Candidates (adults / licences / live brands): Alston 3.6M / 10 / 4; Brough 5.0M / 3 / 2; Everly 2.6M / 4 / 12; Granby 2.0M / 3 / 12;
  Varley 1.6M / 6 / 8.
* Border-county adults by neighbour: Granby has Sorrell 4.6M (holdout), Varley 0.3M (candidate) and Lowick 0.2M (open). Everly has
  Tolland 5.6M (opens 1 July 2027) and Rydal 1.5M (open). Alston has Brough 3.0M (candidate), Kelso 2.0M (open) and Tolland 0.2M.
  Brough has Alston 0.8M (candidate), Yarrow 3.0M (open) and Sorrell 0.4M. Varley has Granby 0.4M (candidate), Sorrell 0.5M, Quorn
  0.3M (holdout) and Lowick 0.6M (open). Sorrell has 9.0M adults and Quorn 16.0M.
* Year-2 GGR at $64.0 ($M): rung 1 Alston 257.6, Brough 196.0, Everly 117.7, Varley 88.7, Granby 78.4. Rung 2 Everly 203.8, Alston
  162.9, Brough 160.0, Granby 156.8, Varley 102.4. Answer Granby 337.0, Everly 203.8, Brough 166.4, Alston 162.9, Varley 128.0.
* Comparables: 6 launches with every neighbour open before launch; 2 with a neighbour opening in their year 1 (Kirkby 2021, Upton
  2022); 4 with a neighbour opening after their year 2 (Delamere and Brecon 2019, Elstow and Ingram 2020); 2 bordering Sorrell (Penrose
  2023, Stanmore 2024). Published year-2 figures total $4,065.5M.
* Comparable adults / licences / brands, then border-county adults by the neighbour's opening: Hadley 5.8M / 8 / 14, 3.0M open; Lisle 2.4M /
  5 / 5, 1.8M open; Thursby 1.1M / 3 / 6, 2.2M open; Morland 3.9M / 7 / 7, 2.5M open; Norbury 0.9M / 2 / 2, 0.7M open; Selby 6.6M / 9 / 16,
  4.1M open; Kirkby 3.2M / 6 / 6, 1.6M opening in its year 1 and 0.9M open; Upton 4.4M / 5 / 9, 2.8M in its year 1 and 0.6M open; Delamere
  7.0M / 6 / 18, 5.2M opening later and 1.0M open; Brecon 1.5M / 4 / 4, 1.9M later; Elstow 2.9M / 4 / 8, 2.0M later and 1.2M open; Ingram
  4.7M / 6 / 6, 3.3M later; Penrose 1.1M / 3 / 6, 2.2M Sorrell; Stanmore 3.5M / 7 / 11, 1.0M Sorrell and 1.5M open. Each published figure is
  $64.0 × (adults + half the year-2 border adults) × the index, to $0.1M. The later-opening neighbours of Delamere, Brecon, Elstow and
  Ingram hold 13.0M, 6.0M, 5.0M and 8.0M adults in all.
* Reproduction: a flat rate at most 2, licences 4, licences with the year-2 border 6, live brands 8, whole neighbouring states 8, status
  today 10, status at launch 12, the answer 14 of 14.
* Penrose and Thursby match on every lookup-visible column. Everly matches Delamere on brands per licence.
* Handle, promotional-wager lines, wager counts and legs-per-ticket annexes never touch the compendium's GGR, the counties or the
  calendar.
