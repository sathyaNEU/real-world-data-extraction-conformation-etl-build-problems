# task124: the summer firm-capacity block split across eight weather-zone books, realising analytical_tasks note FC02 (analytical_tasks/01_forecasting/FC02_summer-block-split-cold-store-coincidence.md)

Stage 1 (draw), drawn 2026-10-10. This is the build's one design note; the design stage extends it. The note is the idea and this build is its first realisation. The note's decisive move (the tariff-class replay) fails the pilot test, so it survives as rung 3 and a new decisive rung is drawn after it (`## Changes from the source note`, item 1).

## Draw

```
DRAW  (independent draws, checked with .claude/skills/fingerprint/guard.py)
  Card filed with guard.py register before the ladder was written? Card filed: registered 2026-10-10 by the coordinator, first of the wave in task-number order; the scratch card is checked   Verdict: PASS (one NOTE, differentiated)
  Shape: 05 allocation to a fixed total   Gate G mechanism: forecasting (method_or_model_selection supporting)
  Gap: population (decisive), time   Pattern: E (decisive)
  Domain: business-operations-analytics   Subdomain (enumerated): other (an energy retailer's summer supply planning)   Objective: forecasting
  Pairing repeated from last build? No. task122 is product-analytics x experiment-causal, and none of task119, task121 and task122 is business-operations-analytics x forecasting, a pairing never built
  Stakeholder role: head of supply portfolio at a Texas retail electricity provider, who takes the summer block split to the risk committee (portfolio_manager)
  Context-artifact type: close_out_summary, last summer's risk report with its replay table (each zone book's ten summers replayed at last year's book)
  Calibration form: existing_book_actuals, ten closed summers (2017 to 2026) of the book's settled hourly load by zone, and hourly interval reads for its interval-metered premises
  Decision type: allocation_to_total, 400 MW in 5 MW lots across eight weather-zone books   Decisive mechanism: G14 conditioned yield. The refrigerated class's draw in the system's peak hour is measured only on the book's fourteen cold stores and ice plants, and every one of them was held to its firm level through every closed system peak by the company's own load-shift programme; the 31 new centres cannot join it before a metered summer, so they draw the analogs' undispatched level. G6 (the tariff-class replay, the note's move), G16 (the per-kW replay pinned by the replay table) and G10 (the enrolment amendments) carry the lower rungs
  Repeats from prior builds: none inside the ban window. The (population, E, allocation_to_total) signature repeats task83, older than twelve, differentiated on the card

  Niche: a Texas retail electricity provider splitting its risk committee's capped summer firm-capacity block across its eight weather-zone books in 5 MW lots, the season a cold-storage developer's 31 new distribution centres arrive in North Central and the book's only refrigerated analogs have only ever been metered under its own summer load-shift dispatch
  Forum: committee_or_panel (the risk committee caps the block and adopts the split)   Forcing event: season_or_peak (the June to September options are placed before the summer opens)   Organisation family: utility_or_infrastructure
  Scoring unit: per active unit per period (the block's call options are priced per MW for each summer month)
  World: United States, Texas; USD; a retail electricity provider serving homes and businesses in all eight ERCOT weather zones. Provisional invented names: Sabine Crest Energy (the provider), Harlan Ridge Cold Storage Partners (the developer), Business Saver programme (the load-shift programme, named so it does not describe its mechanism)
  People, drawn with guard.py names --geo "United States, Texas" --seed 124: Tammy Ochoa (head of supply portfolio, the requester), Gregory Sheppard (head of trading, holds the one licensed belief: Coast is where the summer risk sits), Craig Stewart (load-planning lead), Susan Kelley (chair of the risk committee), Donald Lee (manager of the programme desk that keeps the dispatch log)
  Spine (planned): idr_hourly_reads_summers_2017_2026.parquet, about 1,400,000 rows, one hourly read of one interval-metered premise on a June to September weekday, grain premise x hour, synthetic, shaped on ERCOT's published hourly load by weather zone
  Deliverables (planned): summer_block_split.xlsx (the exposure build, the replay and the lots), summer_block_committee.pptx (the committed split, with the levelling chart)
  Opening move (provisional): constraint-first (the committee's 400 MW cap)
  Criteria arithmetic (shape 05): 8 zone books x 3 figures (allocated block in MW, uncovered 1-in-10 exposure in MW, 1-in-10 peak-hour book load in MW) = 24, plus the water level, North Central's new refrigerated centres' peak-hour draw, 5 named chart parts and 2 files, 33 before any device-carried ask
```

As-of date: 2027-04-12

The enrolment extract closes on 9 April 2027, the risk committee meets on Friday 16 April 2027, the block covers June to September 2027, the ten closed summers are 2017 to 2026, and Harlan Ridge's 31 centres energise in May 2027, so none has an interval read on file.

Similarity claim: no prior build is this puzzle, because none splits a capped block by forecast exposure where the newcomers are priced from the only analogs on file and every analog's measured value at the deciding hour was held down by the organisation's own dispatch, which the newcomers are barred from. task83, the one build sharing the gap, the pattern and the decision type, conditions a randomized treatment effect on each unit's earlier exposure to that same treatment; task118 (OS01), the nearest trap #13 build in the window, nets a unit's own self-treatment out of a sized gain; task117 (FC01), the other electricity build in the window, re-times follow-on charges under faster equipment.

## Stump sentence

A competent solver rebuilds the per-kW replay that ties last year's risk report to the megawatt, collapses the enrolment amendments, joins the distribution utility's tariff class and prices North Central's 31 new refrigerated distribution centres at the class's own peak-hour draw measured on the book's fourteen cold stores (0.60 of maximum demand), filing North Central at 195 MW of the 400 MW block; the step that lands it there is taking those fourteen as what a cold store draws in the system's peak hour, when every one of them was held to its firm level through every closed system peak by the company's own Business Saver load-shift programme, which no site can join before it has a metered summer, so the centres run at the analogs' undispatched 0.90 and North Central takes 230 MW. (Figures provisional from the draw-stage sketch; stage 2 re-solves them.)

## Decisive rung

Measured trap #13, validates on one population, applies to another (`.claude/skills/stumping/references/traps/_measured.md`): established, decided 3 of the 64 measured client tasks, 2 of them under 0.50. In house it carried both builds that held the call in the pilot: FC01 (task117, held against the plain solver at round 4 and against both lenses at round 5) and OS01 (task118, the call missed in every round). The recipe maps one to one: the field that fits every row it can be checked on is the refrigerated class's draw in the system's peak hour (0.60 of maximum demand reproduces every analog's metered peak draw in every closed summer); the forward rows differ on one axis (the 31 new centres cannot be dispatched before a metered summer); the evidence of the difference is left in the record (the programme desk's dispatch log in kW, the step to each analog's firm level at the window's opening on every dispatch day, and the analogs' non-dispatch weekdays at the same hour, where they draw 0.88 to 0.92).

Trap #11 (beats the headline trap, misses the quiet one; 4 of 64, 2 under 0.50) stands behind it: a solver who refutes the pooled factor with the tariff class has beaten the note's headline move and still files rung 3. The lower rungs carry #4 and #12 (the replay table kills rung 0 and certifies the per-kW replay at 40 of 40 zone-summers), #2 (the amendment rows, file rows against premises) and #6 (the pooled factor treats a mixed book one way).

Card vocabulary, decisive first: gap population, time; pattern E; generators G14, G6, G16, G10; Gate G forecasting, with method_or_model_selection supporting. The corpus is blind for a computable reason: in every closed summer every refrigerated premise in the book was a programme member dispatched through the system peak (the programme recruited every refrigerated site the provider served), refrigerated premises held under 1 per cent of every zone book's maximum demand, and no new centre is in last year's book, so every replay-table cell reproduces under 0.60 and 0.90 alike.

## Ladder sketch

Provisional figures from the draw-stage sketch, eight books in the order Coast, East, Far West, North, North Central, South Central, Southern, West, in MW (400 in 5 MW lots, each lot to the largest remaining uncovered exposure). Stage 2 re-solves every cell.

| Rung | Construction | Lands on (MW) | North Central against the answer | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|---|
| 0 | P90 of each zone book's settled load in the system's peak hour over the ten closed summers, less hedges, levelled | 120 · 65 · 5 · 0 · 85 · 75 · 45 · 5 | -63% | It applies the policy's 1-in-10 words to the book's own settled data, and last summer's cells match last year's report exactly | Last year's replay table: the earlier summers' cells, replayed at last year's book, which the settled loads of a smaller book cannot reproduce |
| 1 | Per-kW replay: each summer's settled coincidence factor applied to the coming enrolled book's maximum demand, pooled per zone | 105 · 30 · 0 · 0 · 200 · 50 · 15 · 0 | -13% | It reproduces every cell of the replay table to the MW | The enrolment dictionary and the distribution utility's switch confirmations: the North Central amendment rows restate premises already enrolled, and the amendment supersedes |
| 2 | The same replay on the deduplicated book | 110 · 35 · 0 · 0 · 180 · 55 · 20 · 0 | -22% | Clean counts that tie to the switch confirmations, a validated replay, every reconciliation passing | The distribution utility's premise file: the 31 new North Central premises are in the refrigerated tariff class, which the pooled factor never held |
| 3 | Class replay: each new premise at its class's own draw in the system's peak hour, the refrigerated class's measured on the book's fourteen cold stores and ice plants (0.60 of maximum demand) | 105 · 30 · 0 · 0 · 195 · 55 · 15 · 0 | -15% | The class factor reproduces every analog's metered peak draw in every closed summer, the replay table still ties, and the programme terms confirm the new centres are not members | The programme desk's dispatch log: every closed system peak fell on a dispatch day, and on every dispatch day each of the fourteen steps to its committed firm level at the window's opening, while on non-dispatch weekdays at the same hour they draw 0.88 to 0.92 |
| 4 | **Decisive:** the 31 un-enrolled centres at the analogs' undispatched draw (0.90), every other premise as at rung 3 | **100 · 20 · 0 · 0 · 230 · 45 · 5 · 0** | answer | | |

Priced partials (L3): 0.60 on every new North Central premise, refrigerated or not, files North Central at 205 (-11%); 0.90 on every new North Central premise files 260 (+13%); 0.90 on the file before deduplication files 255 (+11%). The answer is bracketed: every rung below it, the over-applied partials above it. Stage 2 has to move rung 1 and rung 3 apart (they sit 5 MW apart on North Central here), hold every North Central cell at least 10 per cent from the answer, keep the eight-book vectors pairwise distinct, and re-cut the note's twin pair (P-1184 is an analog, so at the peak it drew its dispatched level and the pair is only 1.3 times apart there).

## Why it survives the solver

Against pilot_lessons.md, the step is one the plain solver has no shipped route to. No sentence describes it: no document says the cold stores' peak draw reflects dispatch, and the programme terms say only what a member agrees to and that a site cannot enrol before a metered summer, which the solver reads and executes as "the new centres are not dispatched", a conclusion that confirms its rung-3 figure instead of overturning it. No schema-visible join hands it over: membership sits on no enrolment, premise or class column, and the dispatch is evidenced as a quantity (each analog's reads stepping to its firm level at the window's opening, and the desk's log in kW), so the class factor the solver computes from the analogs' own interval rows at each closed system peak is exactly right for the analogs and shows no symptom. No reproduction check refutes the stop rung: last year's replay table holds no new centre and refrigerated premises are under 1 per cent of every zone book, so the corpus reproduces under 0.60 and 0.90 alike, blind for a computable reason rather than argumentative. And the solver's starting method is what lands it there: replaying each premise at its own closed peak draw is right for every existing premise, the analogs included (they stay dispatched), and the only rows it cannot replay are the newcomers', which it prices from the analogs. Like FC01's hand-offs, the decisive fact is operational and recorded where the question "what does a cold store draw at the peak" gives no reason to look, and the natural method holds it fixed; like OS01's netting, the natural reading (a cold store draws what our cold stores drew) is defensible and nothing in the pack contradicts it. The accepted weak point: a solver who checks the analogs' peak-day profile for flatness, or reads the programme terms and asks whether the fourteen are members, finds it; that is the intended discovery path, and the dispatch log keeps it findable.

## Nearest exemplars

1. CDFI Award Compliance, "File the Rapid Response Program extension on $272,018 unexpended at June 30" (Nonprofit & Grant-making), measured mean 0.39 over 4 runs (0.44, 0.31, 0.44, 0.42). Nearest on the decisive trap: a posting lag measured on single-family draws, correct for them, was carried to commercial draws that post on a longer clock only the SF-425 cells reveal, and three of four runs applied the single-family lag throughout. The same architecture as here: a factor certified on the population it was measured on, applied to forward rows that differ on one axis.
2. Agricultural Research Grant Allocation, "Place eleven states on the FY2022 Capacity Watch, New Jersey taking the largest reserve share" (Nonprofit & Grant-making), measured mean 0.36 over 4 runs (0.44, 0.41, 0.39, 0.44). Nearest on decision shape: a fixed reserve shared across many units by each unit's shortfall below a line, built off a control register that a words-only rule defers to; the model built the index from a variant reading and never tested it against the 200 filed cells.

## Guard

`guard.py check` on the scratch card (`<scratchpad>/cards/task124.json`) against the 119 registered cards: PASS, exit 0, with one NOTE. `guard.py heart` on the same card: PASS, nearest 0.05 (task111 v2 stump). Nearest driver similarity 0.06 (task121 v2). `guard.py validate`: 119 cards, 0 invalid. Not registered here; the coordinator registers in task-number order.

BLOCK cleared: `test.same_puzzle_older` (population, E, allocation_to_total) against task83, by a differentiation line on the card: task83 sizes a randomized treatment effect and splits it by each unit's own earlier exposure to that same treatment; here no effect is sized, a separate programme's dispatch held the analogs' measured level down at the very hour the policy reads, the newcomers are barred from that programme, so the analogs' level is restored from their own non-dispatch records before it transports, and the cap is levelled by exposure rather than ranked by effect.

WARNs: none remain. The first persona set warned on `people.first` for Kenneth (task93) and Robert (task104); both were replaced by Donald Lee from the same seed-124 draw and the sixth persona was dropped. Anthony Martin was skipped because Anthony is on task117's card, inside the last twelve, though the people index did not flag it.

Window bans honoured (last three by draw order: task119, task121, task122): role family compliance_or_audit (task119) is why the requester is the head of supply portfolio rather than the note's head of risk; forcing event vote_or_meeting (task122) is why the summer forces the call and the committee is only the forum; the window's context artifacts (capacity_report, monitoring_export, register) and calibration forms (retry_or_revision_log, prior_period_close_out, pilot_log) are avoided; shapes 18 and 07 are the last two; the window's decisive mechanisms are C, G3 and G13.

## Changes from the source note

1. Decisive move redrawn. The note's class replay is a schema-visible join (ESI ID to the distribution utility's premise file and its tariff class), and a finest-grain replay of the premise interval data shows the class's own peak draw; the pilot solver makes both moves by default (the RC01 v2 two-hop join, the FC01 v1 finest-grain replay). It stays as rung 3, now measured as the analogs actually drew at closed peaks. The new decisive rung is the analogs' undispatched draw for newcomers who cannot be dispatched.
2. The class factor's value changes: in the note the fourteen cold stores drew 0.90 at every closed peak; here they drew about 0.60 there because they were dispatched, and 0.90 is their undispatched draw on non-dispatch weekdays at the same hour.
3. Domain moved from Economics to Business & Operations Analytics (subdomain other), because Economics' boundary puts markets trading out of scope and a retail provider placing call options across zone books is that class.
4. Four zone books become ERCOT's eight weather-zone books, because shape 05 off four buckets reaches about 20 criteria and eight reach 33 off the structure.
5. The requester becomes the head of supply portfolio (compliance_or_audit is banned against task119) and the summer forces the call (vote_or_meeting is banned against task122); the risk committee stays the forum.
6. Deliverables go from three (workbook, PNG, PDF) to two (the workbook and a committee deck carrying the levelling chart).
7. The note's ask B (demand-response enrolment and curtailment) is retired, because the programme now carries the decisive rung and an ask on its records would walk the solver onto the decisive evidence; ask C (each construction's hits on the replay table) is retired because it names the ladder. Stage 2 redraws the asks off the programme's records under supplemental-stumping.
8. The note's twin pair (P-1184 and P-2207) stays on the class rung and is re-cut at stage 2 (see the ladder sketch).
9. World filled where the note is silent: Texas, the as-of date, provisional invented names and five personas drawn with guard.py names.

## Stage 2: design (2026-10-10)

Every figure below is a target the generator builds forward and asserts. The targets were worked on a scratch paper model of the zone books (per-summer pooled factors, the 2027 enrolled book, the hedges and the lot rule, three seeds of the factor series); the model is not the generator and does not ship. Allocations are in MW in the book order Coast · East · Far West · North · North Central · South Central · Southern · West.

### What the design stage settled

1. **The ladder is re-solved and rung 1 and rung 3 are pulled apart.** North Central files 50 / 255 / 145 / 165 / 210 MW across rungs 0 to 4 (the draw sketch had 85 / 200 / 180 / 195 / 230). Rung 1 now sits above the answer and rung 3 below it, 90 MW apart, because the amendment rows restate 275 MW of commercial premises (all off the 31 centres) and the centres carry 186 MW of maximum demand, not 150.
2. **The answer is 120 · 30 · 0 · 0 · 210 · 25 · 15 · 0.** Five books take lots. North Central's 31 centres add 167.4 MW to its 1-in-10 peak-hour load (0.90 of 186.0 MW).
3. **Rung 3 is the strong-solver stop and sits at 130 · 40 · 0 · 0 · 165 · 35 · 30 · 0**, 21.4 per cent under the answer on North Central. Every North Central cell a defensible reading reaches is at least 14.3 per cent from 210 (the nearest is a partial at 240; rung 1 at 255 is +21.4 per cent).
4. **The programme is refrigerated-only.** Business Saver's members are exactly the book's fourteen cold stores and ice plants, so the only class factor dispatch depresses is the refrigerated one. A programme with general commercial members would bias the new general commercial premises' class factor too, and the answer would need a second, unforced adjustment (Tried and rejected).
5. **The dispatch evidence is a billing record, not a curtailment log.** The programme desk's file is the bill credits per member account per called window (credited kWh and USD), keyed on the customer account number; accounts reach ESI IDs only through the billing account file. A log of kW curtailed per event names the quantity a peak forecaster adds back (Tried and rejected).
6. **No shipped sentence states when events are called.** The programme sheet says what a member commits (a firm level in kW through a called window, credited per kWh below its baseline) and who may join (a site whose meter has a full June to September of interval reads, which new construction cannot have). That every closed system peak fell inside a called window is visible only by setting the credit dates beside the system peak dates.
7. **The graded component set is cut to what the decisive rung moves.** The draw's 8 × 3 component block (allocation, uncovered exposure, 1-in-10 load per book) is replaced by allocation and the uncovered exposure left once the lots are in, per book. Under rung 3 the 1-in-10 load and the exposure of seven books are identical to the answer's, which would hand the mirror response 14 free criteria; the post-block exposure of every receiving book moves with the water level instead (Tried and rejected).
8. **The asks are drawn and kept off the programme's records**, as the draw required: the option premium per book per month (the cost beside the exposure) and the average fixed price of each book's existing summer hedges. Neither touches the programme, the enrolment or the interval reads.
9. **The prompt does not mention the developer or the centres.** Naming them in the request points every solver at the one population whose draw decides the call (Tried and rejected).
10. **Kept as drawn:** the pairing, shape 05, the two deliverables and their names, the forum, the forcing event, the five personas, the constraint-first opening move, the as-of date and the calendar.

### Stump sentence (re-solved)

A competent solver rebuilds the per-kW replay that ties last year's risk report to the megawatt on all 80 cells, collapses the North Central amendment rows, joins the distribution utilities' premise file and prices Harlan Ridge's 31 new refrigerated distribution centres at the refrigerated class's own draw in the system's peak hour, measured on the book's fourteen cold stores and ice plants (0.60 of maximum demand), filing 130 · 40 · 0 · 0 · 165 · 35 · 30 · 0 with North Central at 165 MW; the step that lands it there is taking the fourteen as what a cold store draws in the system's peak hour, when each of them sat inside a Business Saver called window at every closed system peak, held to its committed firm level, and no site can join before it has a metered summer, so the centres draw the analogs' uncalled level (0.90) and the split is 120 · 30 · 0 · 0 · 210 · 25 · 15 · 0.

### Gate G

- **Litmus.** No. Every figure in the pack is correct and stays correct: the settled zone loads, the interval reads, the enrolment extract, the premise file, the hedge position report, last year's risk report and its replay table, the programme's bill credits. No stakeholder's claim about their own numbers is overturned and the task does not exist to correct a reading of a correct number. The committed split is a forward allocation for a summer that has not opened, and the difficulty is that the only measured draw for the newcomers' class was measured under a condition the newcomers will not be in.
- **Primary mechanism:** `forecasting`, with `method_or_model_selection` supporting.
- **Flags:** `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`.
- **Deletion test.** Delete the head of trading's belief, the lenders' zone-share basis, the weather file and the ERCOT zone forecast. The replay table still certifies the per-kW replay on 80 of 80 cells, the premise file still hands over the tariff class, the fourteen analogs still draw 0.60 at every closed system peak, and rung 3 still files 165 on North Central.
- **Clean-data test, three depths, asserted per suspect file.** Fill: the one incomplete-looking file on the main path is the enrolment extract with its amendment rows; repaired to one row per premise it is rung 2's input, and rungs 3 and 4 do not move (answer(repaired) = answer(shipped), rung 3(repaired) = rung 3(shipped)). Semantics: every field means what the dictionary says; the maximum-demand field is each premise's own maximum, a different attribute from its draw in the system peak hour. Instrument: give every premise a perfect meter for every closed summer; nothing changes, because the analogs really drew 0.60 at every closed peak and the 31 centres have never seen a summer, so no instrument can record their peak draw. The decisive step survives all three repairs.
- **Lens swap.** Rung 3 and the answer price different populations under different conditions: the fourteen members inside called windows against 31 sites that cannot be called in 2027. Not the same population at the same moment.
- **Pre-draw identity.** Exposure = P90 over ten summers of the sum over premises of (draw factor × maximum demand) at the summer's system peak hour, less hedges. Every input ships except the newcomers' draw factor, which is neither filed nor visibly forced: the only class measurement says 0.60 and the 0.90 needs the uncalled weekdays, the credit dates and the eligibility clause put together.
- **Corpus direction.** Under the naive path the corpus reproduces: rungs 1 to 4 each reproduce all 80 replay-table cells to the MW, because no centre is in last year's book and refrigerated premises are under 1 per cent of every book's maximum demand. It never refutes rung 3.
- **No shipped artifact ranks or splits the block wrongly as its own claim.** Last year's risk report splits last summer's block (a closed period, labelled as such); the lenders' basis is stated as a basis, with no split computed; the ERCOT zone forecast is a published series about the grid, not the book.

### Entity, unit of value and decision

- **Entity and unit.** Sabine Crest Energy, a Texas retail electricity provider, buys firm summer capacity as monthly call options in 5 MW lots and is scored per MW of option per summer month (per active unit per period). The risk committee caps the block; the policy places each lot on the book with the largest remaining uncovered 1-in-10 exposure.
- **Two quantities that both read as size.** A book's maximum demand (the sum of its premises' own maxima) against its load in the system's peak hour. And, for the refrigerated class, its measured draw at the closed system peaks (0.60 of maximum demand) against its draw in an uncalled afternoon (0.90). They size North Central differently because the centres are a large block of one class whose measured peak draw was set by a condition they do not share.
- **Decision.** The split of 400 MW across the eight weather-zone books for June to September 2027, adopted by the risk committee on Friday 16 April 2027 before the options are placed. Shape 05, allocation to a fixed total.
- **Forward facing.** Every committed figure is a megawatt placement for a summer that opens seven weeks after the meeting.

### The answer

**120 · 30 · 0 · 0 · 210 · 25 · 15 · 0 MW.** North Central's 1-in-10 peak-hour load is 705.1 MW (0.4809 × 1,118.1 MW of existing and new general premises, plus 0.90 × 186.0 MW of centres), its uncovered exposure 340.1 MW against 365 MW of hedges.

| Book | 1-in-10 load (MW) | Hedges (MW) | Exposure before the block | Lots (MW) | Uncovered after the block |
|---|---|---|---|---|---|
| Coast | 726.2 | 475 | 251.2 | 120 | 131.2 |
| East | 304.2 | 145 | 159.2 | 30 | 129.2 |
| Far West | 208.9 | 95 | 113.9 | 0 | 113.9 |
| North | 176.1 | 80 | 96.1 | 0 | 96.1 |
| North Central | 705.1 | 365 | 340.1 | 210 | 130.1 |
| South Central | 433.2 | 280 | 153.2 | 25 | 128.2 |
| Southern | 267.2 | 120 | 147.2 | 15 | 132.2 |
| West | 241.1 | 135 | 106.1 | 0 | 106.1 |

- **The level the next lot would have gone to:** 132.2 MW, Southern. Under rung 3 it is 121.2 MW (Coast).
- **Lot-by-lot and the continuous water level converge.** The continuous level is 130.18 MW (121.0 · 29.0 · 0 · 0 · 209.9 · 23.0 · 17.1 · 0); rounded to the nearest 5 MW and by largest remainder it returns the same split, so a solver that levels continuously files the answer too (C1).
- **Bins.** Every post-block exposure sits at least 0.29 MW from a half-MW edge (Coast 131.21, East 129.17, North Central 130.12, South Central 128.19, Southern 132.23, Far West 113.91, North 96.12, West 106.14). No lot decision is within 0.96 MW of a tie: the highest out-of-set value is Southern's 132.23 and the lowest in-set value South Central's 133.19.
- **Rank on the natural pipeline.** Rung 0 gives North Central 50 MW and the most lots to Coast (130), which is the head of trading's belief; North Central is fifth of the five receiving books there. The answer is the fifth of five rungs.

### The ladder

Five rungs. Every figure is computed by the generator from the shipped records and asserted by vector.

| Rung | Construction | Lands on | North Central against 210 | Gap it opens | Killed by (one shipped fact) |
|---|---|---|---|---|---|
| 0 | The policy's words on the book's own settled data: P90 (inclusive) of each book's settled load in each closed summer's system peak hour, less hedges, levelled in 5 MW lots | 130 · 85 · 0 · 0 · 50 · 60 · 75 · 0 | -76.2% | time (the book that will exist against the book that did) | Last year's replay table: its nine earlier-summer cells per book are each summer's conditions at last year's book, which the settled loads of a smaller book cannot reproduce (8 of 80 cells match, all of them 2026's) |
| 1 | Per-kW replay: each summer's settled coincidence factor (settled load at the system peak over that summer's enrolled maximum demand) applied to the coming enrolled book, pooled per book, every enrolment row counted | 110 · 20 · 0 · 0 · 255 · 10 · 5 · 0 | +21.4% | population (rows against premises) | The enrolment dictionary: an amendment row carries the original ESI ID and supersedes it; 2,300 North Central amendment rows restate 275 MW already enrolled, and the switch confirmations tie only to one row per premise |
| 2 | The same replay on one row per premise | 135 · 45 · 0 · 0 · 145 · 40 · 35 · 0 | -31.0% | population (classes inside the pooled factor) | The premise file: the 31 new North Central premises are in the refrigerated tariff class, 186.0 MW of maximum demand, a class that held under 1 per cent of every book in every closed summer and draws differently from the pool |
| 3 | Class replay: each premise at its own tariff class's draw in the system peak hour, the refrigerated class measured on the fourteen cold stores and ice plants at every closed system peak (0.60 of maximum demand, flat across summers) | 130 · 40 · 0 · 0 · 165 · 35 · 30 · 0 | -21.4% | population and time (a condition the newcomers will not share) | The programme's bill credits: every closed system peak falls inside a called window credited to all fourteen accounts, and on uncalled weekdays at the same hour the fourteen draw 0.895 to 0.905; the programme sheet admits no site without a metered summer, and the 2027 roster lists none of the 31 |
| 4 | **Decisive:** the 31 centres at the analogs' uncalled draw (0.90 of maximum demand), every other premise as at rung 3, the fourteen members kept at their called draw | **120 · 30 · 0 · 0 · 210 · 25 · 15 · 0** | answer | | |

**Why each rung is a place to stop.**

- **Rung 0.** It applies the policy's 1-in-10 words to the book's own settled data and last summer's cells match last year's report exactly. A planner with a deadline files it, and it agrees with the head of trading that Coast takes the most. (Measured trap #7, the ready-made measure.)
- **Rung 1.** It reproduces all 80 cells of the replay table to the MW, the certification the report itself carries. (Traps #4 and #12: the reading tested against the control, and stopping at the first control that passes.)
- **Rung 2.** Clean counts that tie to the switch confirmations, a validated replay, every reconciliation passing. (Trap #2, rows against the unit.)
- **Rung 3.** It replaces a pooled factor with the class's own measured draw, reproduces every analog's metered peak draw in every closed summer, still ties all 80 replay cells, and the twin pair separates only under it. It is what a careful forecaster does with a block of new premises of a class the pool never held. (Trap #6, a mixed segment treated one way, refuted; trap #11 behind it.)
- **Rung 4** is the answer. (Trap #13: validates on one population, applies to another.)

"A solver who does everything right up to rung 3 commits to 130 · 40 · 0 · 0 · 165 · 35 · 30 · 0." "A solver who cleans perfectly and stops at rung 2 commits to 135 · 45 · 0 · 0 · 145 · 40 · 35 · 0."

- **Every rung a different vector:** yes, pairwise distinct, and every rung gives North Central a different figure (50, 255, 145, 165, 210).
- **The rung that carries the stump:** rung 4. The stump lands at rung 3 for the strong solver and at rung 2 for the solver who never opens the premise file.
- **The seven survival properties for rung 4.** 1 Written nowhere: no document says the analogs' peak draw reflects called windows or that a cold store's peak draw depends on membership; the programme sheet states commitment and eligibility only, and nothing states when windows are called. 2 No sweepable corpus nominates it: the replay table cannot see the centres (none is in last year's book) and every construction from rung 1 up reproduces 80 of 80. 3 No arithmetic symptom: interval reads sum to the settled zone loads (net of the profiled premises), counts tie to the switch confirmations, the lots sum to 400 under every rung. 4 Not a row predicate: the uncalled draw is a statistic over the fourteen premises' reads on uncalled weekdays at the peak hour, reached through credit dates set against system peak dates and an account-to-premise hop; membership sits on no enrolment, premise or class column. 5 The enumeration is arithmetic: which hours were called is recovered by joining the credit dates and windows to the reads; no column flags a read as called. 6 No cutover date: the programme opened in 2015, before the corpus, and every refrigerated premise entered the book with interval history at its meter (eligible on arrival), so each was a member at every closed peak it was in the book for and no closed series steps at a joining date; the dated contrast is between called and uncalled days inside every summer, and the step it shows is in the analogs' own reads, not in any outcome series a solver aligns. 7 Survives deletion (Gate G above).
- **Worth of each rung on the graded quantity (North Central's lots):** 0→1 +410%, 1→2 -43.1%, 2→3 +13.8%, 3→4 +27.3%.
- **Sign:** the chain is bracketed rather than one-directional. Rung 1 overshoots on the duplicated book, the cleaning rung and the class rung sit below, and only the decisive rung lifts North Central to 210. The over-applied partials (0.90 on every new premise, 0.90 on the duplicated book) sit above the answer, the omissions below it.

### Position table (asserted row by row)

| Rung | Coast | East | Far West | North | North Central | South Central | Southern | West | Next-lot level (MW) | North Central rank among books |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 130 | 85 | 0 | 0 | 50 | 60 | 75 | 0 | 48.7 | 5th |
| 1 | 110 | 20 | 0 | 0 | 255 | 10 | 5 | 0 | 143.2 | 1st |
| 2 | 135 | 45 | 0 | 0 | 145 | 40 | 35 | 0 | 117.2 | 1st (1.07x Coast) |
| 3 | 130 | 40 | 0 | 0 | 165 | 35 | 30 | 0 | 121.2 | 1st (1.27x Coast) |
| 4 | **120** | **30** | **0** | **0** | **210** | **25** | **15** | **0** | **132.2** | 1st (1.75x Coast) |

The answer is an eight-figure vector graded figure by figure, so the separation floor binds rather than a ranking margin (stumping Part 3): every receiving book's lots move between rung 3 and rung 4 (Coast -10, East -10, North Central +45, South Central -10, Southern -15), and no single-error cell a defensible reading reaches puts North Central within 14.3 per cent of 210. The 1.20x rung-margin floor is recorded for the North Central rank only and has nothing to guard, because the call is the vector.

### Separation and dominance

- **The decisive rung is worth 55.8 MW of North Central exposure** (0.30 × 186.0), which the levelling turns into +45 MW of lots on North Central and -45 MW spread across the other four receiving books. That clears the 10 per cent floor on North Central by 2.1x.
- **Dominance.** The carried advantage at rung 3 is North Central already leading Coast by 1.27x; the decisive rung does not have to flip a leader, it has to move five books' lots, and it moves each by at least 10 MW (two lots).
- **Corridor on the uncalled draw (C3).** Any factor in [0.885, 0.916] returns the answer (North Central's in-set value clears the best out-of-set value by 2.89 MW below and 3.07 MW above). Every estimator of the uncalled draw a solver could defend (the mean, median or maximum of the fourteen's uncalled weekday reads at the system peak hour of each summer, pooled or summer by summer, by maximum-demand weighting or by site, and the programme baseline the credits are computed against) lands in [0.894, 0.906], asserted.

### The correction grid

Toggles: load basis (settled, per-kW replay) × counts (rows, premises) × the centres' factor (pooled, 0.60 class, 0.90 uncalled) = 12 cells, plus the partial applications, the members' treatment and the licensed basis. Every cell is computed and asserted by vector and by North Central's distance.

| Cell | North Central (MW) | Against 210 | Violates |
|---|---|---|---|
| settled loads, any counts, any factor | 50 | -76.2% | the replay table (8 of 80 cells) |
| replay, rows, pooled (rung 1) | 255 | +21.4% | the enrolment dictionary's supersession |
| replay, rows, 0.60 on the centres | 270 | +28.6% | supersession |
| replay, rows, 0.90 on the centres | 310 | +47.6% | supersession |
| replay, premises, pooled (rung 2) | 145 | -31.0% | the premise file's class |
| replay, premises, 0.60 (rung 3) | 165 | -21.4% | the credits, the uncalled reads and the eligibility clause |
| replay, premises, 0.90 (answer) | 210 | | |
| partial: 0.60 on every new North Central premise, centres and the 90 MW of new general premises alike | 175 | -16.7% | the premise file's class for the general premises |
| partial: 0.90 on every new North Central premise | 240 | +14.3% | the same |
| members at 0.90 too (the fourteen uncalled in 2027) | 210 | converges | (the fourteen hold under 1 per cent of every book; asserted that no lot moves) |
| the centres at 0.885 or 0.916 | 210 | converges | (corridor) |
| the centres at 0.88 | 205 | -2.4% | outside every defensible estimator of the uncalled draw (lowest 0.894) |
| the centres at 0.92 | 215 | +2.4% | outside every defensible estimator (highest 0.906) |
| P90 by nearest rank or the exclusive convention on the answer's construction | stage 3 computes; asserted at least 6% from the answer or converging | | the risk policy's inclusive interpolation |
| continuous water level, rounded to 5 MW or by largest remainder | 210 | converges | |
| hedges netted by month instead of the summer strip | 210 | converges | (every summer hedge is a June to September strip) |
| lenders' zone-share basis (licensed wrong basis) | stage 3 computes; asserted Coast-led, North Central under 150 | at least -28% | the risk policy's exposure definition (the lenders' basis is named as theirs) |

The two cells inside 6 per cent (0.88 and 0.92) are not readings: they sit outside the range every defensible estimator of the uncalled draw returns, and stage 3 asserts that no estimator in the swept family (12 of them) leaves [0.894, 0.906]. Every single-error cell a defensible reading reaches is at least 14.3 per cent from the answer on North Central and moves at least two other books.

### The calibration corpus

- **Form.** Existing-book actuals: ten closed summers (2017 to 2026) of settled hourly load by zone book at true-up, hourly interval reads for every interval-metered premise on June to September weekdays, the enrolled maximum demand by book at each summer's system peak date, and last year's risk report with its replay table (8 books × 10 summers = 80 cells, each summer's settled factor at last year's book, whole MW).
- **What it certifies.** The per-kW replay and its divisor: settled load at the system peak over that summer's enrolled maximum demand reproduces 80 of 80 cells to the MW. Rivals swept (6): settled loads unscaled (8 of 80, every miss in one direction because every book grew, -4 to -31 per cent on the earlier cells, -12.6 per cent on the 80-cell total), the divisor at year end (31 of 80), the divisor at 1 June (44 of 80), the summer's average enrolled maximum demand (52 of 80), the zone's own peak hour instead of the system's (9 of 80), and 15-minute settlement intervals summed to the hour against hour-ending reads (stage 3 measures; asserted under 60 of 80). Stage 3 asserts every count and the worst miss per rival.
- **What it is blind to, and why.** The centres' draw. No centre is in last year's book, and the refrigerated class held under 1 per cent of every book's maximum demand in every closed summer (fourteen sites, 21.6 MW in all), so rungs 1, 2, 3 and 4 return the same 80 cells. The blindness is structural: it is asserted twice, on the class share (every book-summer under 1 per cent) and by re-running the 80 cells under 0.60 and 0.90 for the members (identical to the MW).
- **The class factor is fittable.** The fourteen's reads at each closed system peak give 0.60 of maximum demand in every summer (site range 0.55 to 0.65, each site's committed firm level over its maximum demand), so rung 3's factor reproduces every analog's metered peak draw exactly. Their uncalled weekday reads at the same hour give 0.895 to 0.905 in every summer. Both halves ship as records, never as a summary.
- **Uncalled hot days exist.** Each summer carries at least four weekdays in its hottest decile with no called window, on which the fourteen draw 0.90 at the peak hour; so the afternoon drop is tied to the calls and not to the heat, and the self-managed pre-cooling reading ("cold stores coast through hot afternoons on their own") is refuted by the records rather than by a sentence.
- **Twin pair.** Two North Central premises identical on every enrolment column (2.40 MW maximum demand, the same plan code, deposit class, meter type and premise age band, the same distribution utility): one a cold store among the fourteen, one a dry-goods warehouse. At the 2026 system peak they drew 1.44 and 0.91 MW (1.58x). The pooled factor gives both 1.15 MW and the maximum-demand band gives both the same figure; only the premise-level and class replays reproduce the pair. On an uncalled weekday at the same hour the cold store drew 2.16 MW (0.90), the warehouse 0.94 MW.
- **Resemblance points at the decoy.** The centres resemble the book's large commercial premises on every enrolment column, which are the premises the pooled factor fits, and they resemble the fourteen on the premise file's class, which is what rung 3 transfers.

### Pins and counter-pins

| Pin | Where (authority) | What it fixes |
|---|---|---|
| The block is 400 MW for June to September 2027, bought as monthly call options in 5 MW lots | risk committee minute of 19 March 2027 (level 3) | the total and the lot |
| Uncovered exposure is the coming summer's book load in the system's peak hour at the 1-in-10 summer (the 90th percentile across the ten most recent closed summers, inclusive interpolation), less the summer hedges in the position report; each lot goes to the book with the largest remaining uncovered exposure, a tie to the book listed first | risk policy (level 1) | the basis, the window, the percentile convention, the lot rule, the hedge source |
| The coming book is the book enrolled at the extract, every premise in service from 1 June at its enrolled maximum demand | risk policy (level 1) | the population and the ramp question |
| An amendment row carries the original ESI ID and supersedes it | enrolment data dictionary (level 4) | duplicate resolution |
| The system peak hour of each summer is the transmission operator's settled peak, hour ending, Central Prevailing Time | the settled-load file's header note (level 5), consistent with the published peak list shipped beside it | the reference hour |
| A member holds its committed firm level through a called window and is credited per kWh below its baseline; a site joins once its meter has a full June to September of interval reads | Business Saver product sheet (level 2) | eligibility (the centres are new construction with no meter history) |
| Empirical: the replay divisor | the replay table, 80 of 80 | axis 6 |
| Empirical: the refrigerated class's called and uncalled draws | the fourteen's interval reads, with the credit dates | the decisive factor, corridor [0.885, 0.916] |
| Licensed wrong basis: the lenders review summer exposure on the zone-share basis (the book's energy share of each weather zone's published 1-in-10 peak) and will see it in the covenant pack | risk policy (level 1), as a matter of record | named as theirs, refuted by the exposure definition in the same policy |

**Counter-pins: none.** The product sheet does not say when windows are called and does not mention peak load; the risk policy says nothing about classes, programmes or the developer; last year's report describes its method as the per-kW replay at last year's book, which is true and pinned to a closed book. Stage 3 greps the pack for "dispatch", "curtail", "peak" and "4CP" near the programme's name and asserts no hit outside the product sheet's one definition sentence.

### Fork grid: the 22-axis closure table (determinism-check A.5)

| # | Axis | Reading chosen | Closure |
|---|---|---|---|
| 1 | Population | the enrolled book at the extract, the 31 centres in, every amendment superseding | pinned (policy, dictionary); C4 for the row-count cells (+21.4% and beyond) |
| 2 | Unit of account | one premise (ESI ID), not one enrolment row | pinned (dictionary grain); C4 |
| 3 | Attribution window | the ten closed summers 2017 to 2026, June to September | pinned (policy); C1: every closed system peak falls in July or August, so a June to September or a July to August window selects the same peaks |
| 4 | As-of dating | the book at the 9 April extract; every premise starts on or before 1 May 2027 | pinned (policy); C1: no enrolled premise starts between the extract and 1 June, so "at the extract" and "at 1 June" select the same premises |
| 5 | Version basis | settled loads at true-up only | C1: only true-up ships, and the 2026 summer passed true-up (180 days after 30 September) before the extract |
| 6 | Divisor | that summer's enrolled maximum demand at the system peak date | C2: the replay table, 80 of 80 against six rivals |
| 7 | Weighting | each premise at its class's factor (rung 3's weighting), the centres at the uncalled draw | C4 (pooled 145, class 165, answer 210) |
| 8 | Window length | ten summers | pinned (policy) |
| 9 | Boundary inclusivity | P90 inclusive linear interpolation | pinned (policy); C4 for the nearest-rank and exclusive conventions, stage 3 asserts at least 6 per cent off or converging |
| 10 | Rounding path | loads and exposures unrounded through the levelling; whole MW only for display | C1: every displayed figure at least 0.29 MW from a half-MW edge, so rounding before levelling selects the same lots (asserted) |
| 11 | Tie-break | the book listed first | C1: no lot decision within 0.96 MW of a tie, so the tie-break is never used (asserted) |
| 12 | Maturity and censoring | all ten summers are closed and trued up | C1 (axis 5) |
| 13 | Order of operations | P90 of load, then less hedges | C1: hedges are a constant per book, so P90 of (load less hedges) is identical |
| 14 | Row order | not order-dependent | C1: lot placement depends only on the exposures; asserted under three row orders |
| 15 | Duplicate resolution | the amendment supersedes | pinned (dictionary); C4 (+21.4%) |
| 16 | Identity normalisation | ESI IDs as 17-digit strings in both the enrolment and the premise file | C1: the generator writes one format in both; asserted every enrolled ESI ID matches exactly one premise row |
| 17 | Netting against gross | hedges are purchases only, netted per book | C1: no sell trades in the summer strips |
| 18 | Dimensional units | enrolment in kW, reads in kWh per hour, settled loads and hedges in MW | C1/C4: a thousandfold slip is off every chart and self-discloses |
| 19 | Code and status semantics | the refrigerated tariff class code, the enrolment record types (new, amendment, drop) | pinned (premise-file code list, dictionary); drops are already removed from the extract's active rows (asserted) |
| 20 | Integerisation | 5 MW lot by lot | pinned (policy); C1 with the continuous level rounded to 5 MW and by largest remainder |
| 21 | Scope of a stated clause | "summer hedges" are the June to September strips in the position report | C1: every summer hedge is a four-month strip, so a monthly reading selects the same MW |
| 22 | Forward window contents | the centres in service and uncalled; the fourteen members called at the 2027 peak as at every closed one | C3 corridor [0.885, 0.916] for the uncalled factor; C1 for the members (uncalled 0.90 for them too moves no lot); policy pin for in-service |

Two axes outside the 22 that this build carries (both closed): **the system peak hour** (the transmission operator's settled peak, hour ending, pinned in the settled-load file's header and identical in the shipped peak list, C1) and **the estimator of the uncalled draw** (C3, the corridor above, twelve estimators swept).

### Deliverables and the criteria arithmetic

Shape 05, allocation to a fixed total. Two files, both written by the golden script.

1. **`summer_block_committee.pptx`** (the committing file, read at the meeting): the split on its first slide, and one chart with its parts named in the prompt: a bar per book for its uncovered exposure before the block, ordered largest first, its lots shaded on the bar, a line at the largest uncovered exposure any book carries after the block (132.2 MW, Southern) labelled with its value, and a title that states the split.
2. **`summer_block_split.xlsx`** (the working): one row per book with its lots and the uncovered exposure left once they are in; the lot premium per book for June, July, August and September 2027; and each book's average fixed price on its existing summer hedges. The golden also carries each book's 1-in-10 load, hedges and exposure before the block, ungraded by the prompt.

Criteria arithmetic: 8 books × 2 (lots, uncovered after the block) = 16, plus the next-lot level, North Central's centres' contribution (carried by the golden, graded if the rubric picks it up), 5 named chart parts and 2 files = 25 before the asks; ask A adds 8 books × 4 months = 32 figures and ask B 8, so 65 named figures. Rubric planning weights 38 / 7 / 55.

- **Script-generated:** both files, by the golden script from the shipped bundle. **Unit and rounding:** a block convention ("megawatt figures in whole MW") plus explicit pins on the two price figures (USD per MW-month to the nearest dollar, USD/MWh to the cent); lots are multiples of 5 by the policy.
- **Distinct findings across the set:** the split (and its level), the price of a lot by book and month, the price already locked on each book's cover. **Named-parts visual:** yes. **Breakdown at an explicit grain:** book × month. **Robustness check:** the next-lot level is the split's flip margin (how much more exposure any book would need before it takes the 81st lot).
- **The ask set does not over-determine the decisive constant.** Neither ask touches a load figure. The graded component set (lots and post-block exposure) determines North Central's exposure only within the 5 MW lot it sits in, and the centres' factor only to ±0.03, which the corridor already allows; a solver cannot back out 0.90 from the deliverables without having built it.

### The ask ledger (supplemental-stumping)

**H18 read.** Both asks are components of the committee's case for the block: the premium is the cost of the split the committee adopts (it signs the premium with the block), and the hedge price is what each book's existing cover already costs, the other measure the committee's book table carries beside its exposure. Neither is a figure for another period, another population or another decision, and neither is keyed to the call by name.

**Main call's declared row population** (generator constant `MAIN_ROWS`): the settled-load file's system-peak-hour rows for 2017 to 2026; the published peak list; every active row of the enrolment extract; the premise file's rows for enrolled ESI IDs; the switch confirmations; the interval reads of the fourteen at every hour and of every other premise at the ten system peak hours; the bill credits; the billing account rows of the fourteen; the 2027 roster; the replay table; the position report's MW column. **Zero device rows and zero hazard rows inside it, asserted.** Every device below lives in a file outside it, and no device can move hedge MW (amendments in the blotter change price only, asserted on every amended trade).

**Ask A: what a megawatt of call option costs each book in each summer month** (USD per MW-month, nearest dollar; 8 × 4 = 32 figures).
- **Use.** The risk committee signs the premium budget with the split; the trading desk places each book's lots at these prices.
- **Path (8 files, 14 columns):** the broker quote file (quote id, revision, broker, counterparty code, load zone, delivery month, premium, sent time), the third broker's own quote sheet (its own load-zone spellings and month labels), the quote decisions log (quote id, revision, decision), the trading desk procedures (the three approved brokers and each one's quoting convention; each lot is bought at the lowest accepted quote for its book's load zone and month; a per-MWh premium is converted at the hours of the notional it is quoted on), the trading calendar (date, NERC holiday), the book map (book, load zone, effective from), the counterparty master (code, legal name, approved from, approved to), the data dictionary.
- **Primary device (D4, silent): an absent channel.** The third approved broker sends its quotes as its own sheet in its own namespace ("Houston LZ" style zone spellings, "Jul-27" month labels), not through the desk's quote file; its quote is the lowest in at least ten cells. The careless path prices from the quote file alone and nothing fails. Organ: the procedures' list of three approved brokers (documentary) and the sheet itself (structural).
- **Hazards crossed:** H1 (holidays), H2 (reissued counterparty code), H3 (book map vintage), H4 (notional shape).
- **Stops (stage 3 asserts each value and its distance; every distance at least 1 per cent on every cell it moves):** S1 natural (the quote file alone, every per-MWh premium at 5x16 hours, latest delivered revision, every code taken as currently approved, the 2026 map); S2 units right, holidays missed (July and September cells 4.8 per cent high on every 5x16 conversion); S3 over-corrected (every revised quote and every quote under a reissued code dropped, losing the lowest valid quote in at least six cells); S4 right rules on the 2026 book map (East priced in the North load zone); answer.
- **Lazy delta:** S1 wrong on at least 24 of 32 cells.

**Ask B: the average fixed price on each book's existing summer hedges** (USD/MWh to the cent; 8 figures).
- **Use.** The committee's book table carries what each book's cover already costs beside what its lots will cost; the head of trading answers for it.
- **Path (8 files, 12 columns):** the trade blotter (trade id, amendment number, portfolio, product code, MW, fixed price, trade date), the confirmation matching log (trade id, amendment number, status), the portfolio-to-book crosswalk, the product code list (5x16, 7x16), the trading calendar, the trading desk procedures (the summer average is weighted by each trade's on-peak MWh over June to September), the position report (MW referee, ties per book), the data dictionary.
- **Primary device (D2, silent): the version of record is the latest matched amendment, not the latest booked.** Price-only amendments: a second amendment on several trades was booked and never matched (disputed and withdrawn), so the latest amendment number is the wrong price on those trades. Organ: the procedures' version-of-record clause (documentary) and the matching log (structural). Over-cleaning stop: ignoring amendments altogether.
- **Hazards crossed:** H1 (holidays move the 5x16 weights), H4 (7x16 trades carry more MWh than 5x16 trades of the same MW, so a MW-weighted average is wrong by 5 to 40 cents per book).
- **Stops:** S1 MW-weighted on the latest booked amendment; S2 matched amendments, MW-weighted; S3 matched, MWh-weighted with holidays ignored; S4 over-corrected (original prices only); answer. Every stop at least USD 0.05/MWh from the answer on at least six of eight books.

**Hazard table**

| Hazard | Root cause | Moves | Per-ask delta (stage 3 asserts) |
|---|---|---|---|
| H1 NERC holidays (Monday 5 July 2027 observed, Monday 6 September 2027) | the calendar is the desk's, not the weekday count | A (July, September cells on 5x16 conversions), B (5x16 MWh weights) | A: +4.8% on affected cells; B: 1 to 6 cents |
| H2 a counterparty code reissued in 2026 to a newly approved firm after the previous holder exited | the counterparty master is effective-dated | A (the reissued code's quotes are valid; an older code's lapsed approval voids its quotes) | A: the lowest quote changes in at least two cells |
| H3 the 2027 book map moves East from the North load zone to Houston | a 1 January 2027 remapping of East Texas premises | A (East's four cells) | A: East priced at the wrong zone, at least 3% off |
| H4 notional shape: one broker quotes per MWh of 5x16 notional and another per MWh of 7x16 notional; summer hedges are booked as 5x16 or 7x16 strips | the desk trades both products, and the shape lives on the broker or the product code, never in the price column | A (every cell where the 7x16 broker is lowest), B (every book holding 7x16 strips) | A: about 30% on the 7x16 broker's cells; B: 5 to 40 cents |

H1 and H4 cross both asks; H2 and H3 sit on ask A, whose path alone carries the counterparty and the load zone. One referee: the position report, byte-clean, which ties blotter MW per book and leaks no price.

**Pair arithmetic.** At planning weights (38 / 7 / 55), with `r` read as the recommendation criteria a rung-3 response keeps (the three zero allocations and the three non-receiving books' post-block exposures, about 10 points): 55 × (Lc + Ls) ≤ 28 - 10 = 18, so Lc + Ls ≤ 0.33. Target leakage 0.16 each (every cell under at least two silent devices, the primaries on the silent list). Cracker sheet 38 + 7 + 8.8 = 53.8, mirror sheet 10 + 7 + 8.8 = 25.8, pair 39.8. If no top response lands the call (the measured outcome on the client's hardest trap #13 tasks), the pair is about 26. Stage 3 reruns the sum with the generated rubric's weights.

**Decoupling, asserted.** Replace the centres' factor (0.90 by 0.60, by the pooled factor) and recompute both asks: every figure unchanged. The cracker and mirror sheets differ only in the recommendation block.

### Assertion plan (generator and independent verifier, 48 planned)

- Rungs 0 to 4 by vector, pairwise distinct, each rung's North Central figure and its distance from 210 (5).
- The answer's eight lots, eight post-block exposures, next-lot level and the centres' contribution (18), each post-block exposure at least 0.25 MW from a half-MW edge, and no lot decision within 0.9 MW of a tie (2).
- Lot-by-lot equals the continuous level rounded to 5 MW and by largest remainder (1); three row orders give the same split (1).
- The replay table: 80 of 80 under rungs 1 to 4, each of the six rivals' match count and worst miss, the settled-load rival's aggregate gap (8).
- The corpus blindness twice: every book-summer's refrigerated share under 1 per cent, and the 80 cells identical with the members at 0.60 and at 0.90 (2).
- The fourteen: called draw 0.55 to 0.65 per site at every closed system peak; uncalled draw 0.895 to 0.905 per summer; at least four uncalled weekdays per summer in the hottest decile; every closed system peak inside a credited window for all fourteen; no credit for any non-refrigerated account (5).
- The corridor: answer unchanged at 0.885 and 0.916, changed at 0.88 and 0.92, every one of the twelve estimators in [0.894, 0.906] (3).
- The correction grid and partials by vector, each against its violated rule (1, a table assertion over 14 cells).
- The twin pair: identical on every enrolment column, 1.44 and 0.91 MW at the 2026 peak, the pooled factor giving one figure (1).
- The clean-data test on the enrolment extract (answer and rung 3 unchanged after repair, answer differs from rung 3) and the lens-swap separation (2).
- Separation: zero device and hazard rows in `MAIN_ROWS`; every blotter amendment price-only; both asks unchanged under the centres' factor at 0.60 and pooled (3).
- Each ask's stops and distances, the lazy deltas and the per-hazard deltas (4, table assertions).
- Input gates: files, formats, the spine's row count, two declared distractors named in `metadata.json`, and the leak greps (programme vocabulary, no input file named in any document beside its own provenance line) (5).

### Pack plan (stage 3 builds against it; names provisional, in the organisations' own idiom)

| Role | File (provisional) | Path |
|---|---|---|
| Spine | `ami_idr_hourly_2017_2026.parquet`, about 1.4 million rows, premise × hour on June to September weekdays | main (and the decisive evidence at uncalled hours) |
| Operating extract | `zone_settled_load_s17_s26.csv`, hourly by book at true-up | main |
| Published series | `ercot_summer_system_peaks.csv` | main |
| Operating extract | `enrollment_extract_20270409.csv` | main |
| Counterparty file | `tdsp_premise_attributes.csv` (the distribution utilities' premise file with tariff class) | main |
| Operating extract | `switch_confirms_spring_2027.csv` | main |
| Governing document | `summer_risk_policy_2027.docx` (pins, licensed wrong basis) | main |
| Governing document | `rc_minute_2027-03-19.pdf` | main |
| Context artifact and corpus | `summer_2026_risk_report.pdf` with its replay table | main |
| Operating extract | `hedge_positions_20270409.xlsx` (MW and MWh per book; the referee) | main, ask B |
| Operating extract | `bsaver_credits_2017_2026.csv` (account, window date and hours, credited kWh and USD) | main (decisive) |
| Dimension | `billing_accounts.csv` (account to ESI IDs) | main (decisive hop) |
| Product terms | `business_saver_terms.pdf` and `bsaver_roster_2027.xlsx` | main |
| Ask A | `option_quotes_s27.csv`, `pecos_quote_sheet_apr2027.xlsx` (the third broker), `quote_decisions.csv`, `desk_counterparties.csv`, `book_zone_map.csv` | ask A |
| Ask B | `trade_blotter_s27.csv`, `confirm_match_log.csv`, `portfolio_books.csv`, `product_codes.csv` | ask B |
| Shared | `desk_procedures.docx`, `trading_calendar_2027.csv` | asks A and B |
| Distractors (declared in `metadata.json`) | `zone_daily_temps_2017_2026.csv` (weather by zone; a weather-normalised forecast breaks the policy's replay definition) and `ercot_zone_peak_outlook_2027.xlsx` (the grid's published zone peaks, the input to the lenders' basis) | none |
| Dictionary and provenance | `field_notes.md`, `extract_log.md` | all |

About 27 files and five formats (parquet, csv, xlsx, docx, pdf, md). Stage 3 may fold the two product-terms files and the two md files if the span floor survives, and records any fold here. Sources: every series is synthetic, shaped on ERCOT's public hourly load by weather zone and its published 2017 to 2026 summer system peaks; licence and dates go in the provenance record.

### Realism debts

- **The fourteen draw 0.895 to 0.905 of maximum demand on every uncalled weekday afternoon, whatever the weather.** Real refrigeration load rises with heat. Forced because the corridor has to hold every defensible estimator of the uncalled draw inside [0.885, 0.916] (2.9 MW of North Central exposure each way). Mitigation: the band is a plausible flat-compressor regime for large freezer warehouses, and the hot-day evidence (uncalled hot weekdays at 0.90) is what kills the pre-cooling reading.
- **275 MW of North Central maximum demand restated by amendment rows** (about 18 per cent of the North Central book) is large. Forced so that rung 1 lands at least 20 per cent from the answer above it while rung 3 sits below. Mitigation: the amendments come from one broker's re-papering of large commercial accounts at contract renewal, dated in a two-week run in March 2027, which the extract log records.
- **A refrigerated-only programme.** Real load-shift products enrol other large commercial sites. Forced because a mixed programme would bias the new general premises' class factor too and open a second, unforced adjustment. Mitigation: the product is sold as a thermal-storage product for cold stores and ice plants, which is the honest market for it.

### Stopping rule (written before any round)

- **At ceiling:** the plain solver lands 120 · 30 · 0 · 0 · 210 · 25 · 15 · 0 by setting the credit dates beside the system peaks, or by checking the fourteen's uncalled draw, in three consecutive hardening loops.
- **One more repair licensed:** the solver lands the call by a route other than the designed one (for example a generic "add back demand response" step applied to the analogs), which says the route is a habit, not a discovery; the repair moves the evidence, never deletes it.
- **Ship:** the solver files any other vector, rung 3 or not.

### Prompt

`prompt.md`, 249 words, constraint-first ("We can only buy 400 MW of summer firm capacity."), two files, `voice-check.py 124` clean (24.9 words a sentence, context 40.2 per cent, one rounding tag beside the "whole MW" convention, no "because"). The call closes the context as one quotable sentence (the megawatts each of the eight named books gets, adding to exactly 400), and both later paragraphs open on "the split". One belief, the head of trading's, as one clause. Nothing names an input file, the developer, the programme, the replay, the percentile, the window of summers or the hedge source; the policy carries all of them.

## Harden loop 1: the peak-heat rung (2026-10-10)

The round-1 solver landed the call through the designed route (credit dates beside the peak list, then the uncalled draw from the programme terms' baseline). The repair keeps every rung the solver climbed and adds one after its step 5, so that step still completes and now returns a wrong split. This section supersedes the Stage 2 ladder, position table, dominance, corridor and stump sentence where they disagree; the Stage 2 text stays as the record of what round 1 measured.

### What changed in the world

- **A member's uncalled draw follows its zone's heat.** On ordinary afternoons a member runs at its base level (about 0.76 of maximum demand); once its zone reaches design-day heat it runs at full load (0.977 to 0.984 by site), linear between heat-index marks 0.68 and 0.78. Every closed system peak sits far above the full-load mark, so an uncalled cold store would have drawn its full-load level in every closed peak hour. Called windows are unchanged (each member at its firm level, 0.60 pooled).
- **The programme's baseline averages ordinary afternoons.** The terms' baseline (ten most recent uncalled business days) is mostly built on days below the full-load mark, so at the closed peak hours it reads 0.885, and the credits recompute from it exactly. The programme's own settlement records therefore certify the wrong value (corpus direction: the credits reproduce the naive baseline, never refute it).
- **The zone temperature file moves onto the main path** (it carries the heat the step needs) and runs 30 F per unit of the heat index with 0.7 F of vendor scatter. A new declared distractor takes its slot: `loadfcst_da_s26.csv`, Load Planning's day-ahead forecasts of the book for summer 2026 (relevant-looking, unused: the policy replays ten closed summers at the coming book).
- **Targets retuned** so the corridor holds every peak-heat estimator and full maximum demand: East 160.0, South Central 155.1, North Central 340.2 MW before the block (Coast, Southern, the others unchanged). The answer split is unchanged.

### Stump sentence (loop 1)

A competent solver rebuilds the per-kW replay that ties all 80 cells of last year's replay table, collapses the North Central amendment rows, joins the premise register, sets the Business Saver credit dates beside the system peaks, sees that the fourteen cold stores' 0.60 peak draw came from called windows, and rebuilds their uncalled level with the programme's own baseline (ten most recent uncalled business days, 0.885 at the closed peak hours, which reproduces every credit line), filing 125 / 30 / 0 / 0 / 195 / 30 / 20 / 0 with North Central at 195 MW; the step that lands it there is taking the baseline, an average of ordinary afternoons, as the draw in a system peak hour, when on every uncalled weekday as hot as a closed peak the fourteen drew 0.98 of maximum demand, so the centres draw 0.98 (182.3 MW) and the split is 120 / 30 / 0 / 0 / 210 / 25 / 15 / 0.

### The ladder (as built)

| Rung | Construction | Lands on (MW) | North Central against 210 | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | P90 of each book's settled peak-hour load, less hedges | 115 · 70 · 35 · 20 · 30 · 45 · 60 · 25 | -85.7% | the replay table (8 of 80 cells) |
| 1 | per-kW replay, every enrolment row | 115 · 20 · 0 · 0 · 235 · 20 · 10 · 0 | +11.9% | the dictionary: AMEND supersedes |
| 2 | the replay on one row per premise | 140 · 50 · 0 · 0 · 130 · 45 · 35 · 0 | -38.1% | the premise register: the centres are NAICS 493120 |
| 3 | class factor: the centres at the fourteen's closed-peak draw (0.599) | 135 · 45 · 0 · 0 · 150 · 40 · 30 · 0 | -28.6% | credits on every closed peak date, the eligibility clause |
| 4 | the centres at the programme baseline (0.885) | 125 · 30 · 0 · 0 · 195 · 30 · 20 · 0 | -7.1% | risk policy s.2 (load in the system peak hour) against the fourteen's reads on uncalled weekdays as hot as a closed peak (143 member-days on 25 dates, every one 0.965 to 0.995) |
| 5 | **Decisive:** the centres at the peak-heat draw (0.980) | **120 · 30 · 0 · 0 · 210 · 25 · 15 · 0** | answer | |

- **Why rung 4 is a place to stop.** It is the programme's own counterfactual of what a member would have drawn uncalled, it is in a signed product sheet, it reproduces every credit line to the kWh, and it is what round 1's solver built. Nothing in the pack says the baseline understates a hot afternoon.
- **Why rung 5 is the answer.** The policy's exposure is load in the system peak hour; a peak hour is a design-day afternoon, and the fourteen's own uncalled reads on afternoons that hot are at full load. The construction is a join (reads to accounts to zones to the temperature file) and a condition on heat that no sentence describes.
- **Worth on North Central's lots:** 3 to 4 +30%, 4 to 5 +7.7%. Rung 4 moves four books against the answer (Coast +5, South Central +5, Southern +5, North Central -15).
- **Position table (next-lot level, North Central rank):** R0 70.1 (Coast leads, North Central 6th) · R1 139.9 (1st) · R2 114.7 (2nd, 0.93x Coast) · R3 119.1 (1st, 1.11x) · R4 129.9 (1st, 1.56x) · R5 132.1 (1st, 1.75x). The call is the vector, so the separation floor binds, not a ranking margin; the floor is 10 per cent on North Central for rungs 0 to 3 and 6 per cent for rung 4, each asserted.
- **Dominance.** The decisive move is worth 0.095 x 186.0 = 17.7 MW of North Central exposure, which the levelling turns into +15 MW on North Central and -15 MW across Coast, South Central and Southern. Smaller than the Stage 2 move (rung 3 to rung 4 was 55.8 MW), because the physical gap between an ordinary and a design-day afternoon is a fifth of maximum demand, not a third; stated rather than hidden.

### Determinism of the new step

- **Corridor (C3), scanned at 0.0005:** any centre factor in [0.9645, 1.006] files the answer; 0.963 files North Central 205, 1.008 files 215. Full maximum demand (1.00) sits inside it, so a solver who carries the centres at their whole maximum demand converges.
- **Peak-heat estimators, all inside the corridor by at least 0.004:** zone as hot as its coolest closed peak (the golden, 0.9803), as hot as its median closed peak (0.9806), hottest-decile weekdays by book-wide settled load, uncalled (0.9789), hottest tenth of each site-summer by zone maximum (0.9688), each site-summer's highest uncalled draw (0.9834), each site's highest over ten summers (0.9853).
- **Ordinary-afternoon estimators (C4), every one filing North Central at 195 or less:** pooled, by summer, by site, median, 2026 only (0.762 to 0.819, North Central 180 to 185), the programme baseline at the closed peak hours (0.885, 195) and over every called day (0.856, 190).
- **Readings that condition on heat but stop short of peak-day heat (C4, recorded):** the hottest fifth of each site-summer (0.923, North Central 200) and a straight line on zone maximum read at the mean peak-day maximum (0.932, 205). Both are refuted by the fourteen's own reads on days as hot as the peaks, which sit at 0.97 to 0.99 with no exception; the line is a misspecified model of a draw that stops rising at full load. They are the two nearest wrong cells (-4.8 and -2.4 per cent) and the accepted weak point of this loop.
- **Fork grid (asserted cell by cell, 18 cells):** rows with any centre factor 235 to 310 (supersession); partials on every new North Central premise 165, 235, 255 (the premise register); members uncalled in 2027 too, P90 nearest rank and exclusive, the full class replay and the NAICS replay all converge.
- **Lens swap.** Rung 4 and the answer price the same 31 centres from the same fourteen members' uncalled reads, but at different conditions: rung 4 at the ordinary afternoons a settlement baseline averages, the answer at the design-day afternoons the policy's peak hour is. Not one population at one moment under two lenses; the clean-data and instrument repairs leave both standing (a perfect meter on every member still shows 0.885 on baseline days and 0.98 on peak-heat days).
- **Survival properties for rung 5.** 1 written nowhere (no document mentions heat, full load or a baseline's bias); 2 the swept corpora point at rung 4 (the credits reproduce the baseline, the replay table is blind to the centres); 3 no symptom (every credit, count and replay cell ties under rung 4); 4 not a row predicate (a condition on a joined temperature statistic per member-day); 5 the enumeration is arithmetic (which member-days count is set by each zone's closed-peak temperatures); 6 no cutover date; 7 survives deleting every wrong number.

### Stopping rule (loop 1)

- **Ship:** the round-2 solver files any vector other than 120 · 30 · 0 · 0 · 210 · 25 · 15 · 0.
- **Harden again (loop 2):** it lands the answer by conditioning the members' uncalled draw on heat; the next repair moves after that step, never by burying the temperature file.
- **Retire:** landed after loop 3.

## Build record

Stage 3a (evidence pack), 2026-10-10. Generator `generator/build_pack.py` (modules `common`, `world`, `loads`, `desk`, `analysis`, `checks`, `writers`, `documents`, `docs2`, `pipeline`), seed 1242027. Independent verifier `generator/verify_pack.py` reads only `target/` (and `metadata.json` for the distractor gate) on its own code path.

**Gate outcomes.** Generator: 91 assertions, all green. Verifier: 37 checks, 0 failed, every graded figure equal to the generator's to the last digit (post-block exposures, 1-in-10 loads, 32 premiums, 8 hedge prices). Two consecutive builds into the scratchpad: all 28 files, `metadata.json` and the build record byte-identical (sha256), mtimes identical; the task-folder build matches the scratch builds byte for byte. `scrub_producer_metadata.py` audit over `target/`: clean, no producer signature, no stamp outside 2024-01-01 to 2027-04-12.

**Input gates.** 28 files, 6 formats (parquet, csv, xlsx, docx, pdf, md). Spine `idr_hourly_reads_summers_2017_2026.parquet`, 1,881,080 rows (the IDR premises and the fourteen members, weekdays June to September, hours ending 11 to 20). Distractors in `metadata.json` and nowhere in `target/`: `zone_daily_temps_2017_2026.csv` and `ercot_zone_peak_outlook_2027.xlsx` (the declared wrong-basis distractor). No two CSVs share a row count; every in-file date on or before the 9 April 2027 extract (calendar and delivery periods excepted); every file's mtime an in-fiction write time; the extract log names every file but itself.

**The answer and the ladder, as built (MW, Coast · East · Far West · North · North Central · South Central · Southern · West).**

| Rung | Split | North Central against 210 |
|---|---|---|
| 0 settled loads, own book | 115 · 65 · 35 · 15 · 40 · 45 · 60 · 25 | -81.0% (5th of the receiving books; Coast leads) |
| 1 per-kW replay, every row | 110 · 20 · 0 · 0 · 255 · 10 · 5 · 0 | +21.4% |
| 2 replay, one row per premise | 135 · 45 · 0 · 0 · 145 · 40 · 35 · 0 | -31.0% |
| 3 class factor 0.599 on the centres (stump) | 130 · 40 · 0 · 0 · 165 · 35 · 30 · 0 | -21.4% |
| 4 uncalled draw 0.900 on the centres (answer) | **120 · 30 · 0 · 0 · 210 · 25 · 15 · 0** | |

- 1-in-10 loads (answer): 725.9 · 304.2 · 208.9 · 176.1 · 705.0 · 433.2 · 267.1 · 241.1 MW. Exposure before the block 250.9 · 159.2 · 113.9 · 96.1 · 340.0 · 153.2 · 147.1 · 106.1. Uncovered after the block 130.9 · 129.2 · 113.9 · 96.1 · 130.0 · 128.2 · 132.1 · 106.1; the next lot would go to Southern at 132.1 MW. The centres add 167.5 MW (0.90048 × 186.0).
- Thinnest margins: lowest value a lot was taken at 133.19 (South Central) against the highest left 132.09 (Southern), 1.10 MW; every post-block exposure at least 0.29 MW from a half-MW edge (Coast 130.907 is the nearest whole-MW call at 0.41). Continuous water level 130.07, which rounds (nearest 5, largest remainder) to the same split.
- Corridor on the centres' factor, scanned at 0.0001: [0.8848, 0.9175] files the answer; 0.88 files 205 on North Central and 0.92 files 215. All twelve estimators of the uncalled draw lie in [0.9003, 0.9008].
- Grid cells as built: rows with the class factor 270, rows with the uncalled draw 310, partial class factor on every new North Central premise 175 (-16.7%), partial uncalled draw on every new North Central premise 250 (+19.0%); converging: members uncalled in 2027 too, P90 nearest rank, P90 exclusive, a class replay with every class at its own summer factor, a NAICS-level replay of the IDR premises.
- Corpus: the per-kW replay reproduces 80 of 80 cells of the close-out's replay table (every cell at least 0.1 MW from a half-MW edge). Rivals: settled unscaled 8 of 80 (2026's cells only, worst miss 37.7%), divisor at year end 1 of 80, at 1 June 17 of 80, summer-average enrolled MD 47 of 80, the zone's own peak hour 58 of 80. Class factor 0.599 at the closed peaks (0.597 to 0.601 by summer), uncalled draw 0.900 (0.895 to 0.905 by summer); members at most 0.91 per cent of any book-summer; every closed peak day credited to every member account; 4 to 6 uncalled weekdays in each summer's hottest decile.
- Twin pair (North Central, 2,400 kW, identical on every enrolment column): the cold store drew 1,437.3 kW at the 2026 peak, the dry-goods warehouse 910.0 kW (1.58x); the pooled factor gives both 1.154 MW.
- Lenders' zone-share basis (declared distractor): 110 · 75 · 0 · 15 · 60 · 70 · 60 · 10, Coast-led, neither the answer nor rung 0.

**Asks as built.** Ask A (premium, USD per MW-month, 32 book-cells over 16 zone-month values, since books sharing a load zone share a price): Pecos holds the lowest valid quote in 10 of 16 zone-months; the natural path is wrong on 32 of 32 cells (nearest 21.3% off); holidays missed moves 14 (2.6% or more); the over-corrector moves 12 (2.5% or more); the 2026 map moves East's 4 (2.0%). Every winning quote at least 2% under the next valid one; every premium at least 6 cents from a half-dollar edge. Ask B (USD/MWh): 78.92 · 75.91 · 75.52 · 75.91 · 75.80 · 72.74 · 77.93 · 76.88; each of the four stops is $0.05 or more off on 8 of 8 books; blotter MW ties the position report and every amendment is price-only. Separation: no device file is on the main call's declared population (the position report is the byte-clean referee shared with ask B).

**Where the build departs from the stage 2 targets (recorded, no design change).**
1. Post-block exposures sit at 130.9 / 130.0 / 132.1 for Coast, North Central and Southern (targets 131.2 / 130.1 / 132.2): the two summers that set each book's 1-in-10 pin their replay-table cells to the target, so clearing those cells off half-MW edges moved three targets by up to 0.31 MW. The split, the stump vector and every rung's North Central distance are unchanged; the tie margin widened to 1.10 MW.
2. Rung 0 is 115 · 65 · 35 · 15 · 40 · 45 · 60 · 25 (target 130 · 85 · 0 · 0 · 50 · 60 · 75 · 0); still Coast-led with North Central fifth.
3. The amendment run is 2,713 rows restating 275.0 MW (target 2,300 rows); the new general North Central premises are 113.1 MW (target 90), so the partials sit at 175 and 250.
4. The replay-table blindness is asserted on what the closed books cannot hold (no AMEND row and no centre in any closed book, so rungs 1 to 4 return the same 80 cells); the members are inside every closed book, so a variant that sets them at 0.90 there is refuted by the table rather than blind to it.
5. The 15-minute settlement rival is not built: the settled file is hourly at true-up.
6. The book is commercial and industrial only (premises are small and large commercial sites), because a residential book would put the enrolment extract near 600,000 rows; the premise file is Sabine Crest's `premise_register_20270409.csv` (ERCOT load profile and the NAICS code from the service application), and the refrigerated class is NAICS 493120 and 312113.
7. The close-out report is dated 2 February 2027, after true-up for the 2026 peak, and carries Table 1 (enrolled maximum demand and settled load at the 2026 peak) and the replay table, with no 2026 block split.
8. Product codes fold into the procedures (the 5x16 and 7x16 definitions); 28 files rather than 27.

### Harden loop 1 rebuild (2026-10-10)

**Gate outcomes.** Generator: 101 assertions, all green (new: M02b and M04b on rung 4, M11 on rung 4's level, G00 corridor, C08 ordinary afternoons 0.785 to 0.819 by summer, C08b every member-day as hot as its zone's coolest closed peak at 0.965 to 0.995 over 143 member-days on 25 dates, C08c the golden's estimator is the generator's factor, D01 to D03 the three estimator families). Verifier: 39 checks, 0 failed, on its own code path (temperatures read from the shipped file, the baseline rebuilt from the reads). Two consecutive scratch builds byte-identical on all 29 files, `metadata.json` and the build record; the task-folder build matches them byte for byte. `scrub_producer_metadata.py` over `target/` (band 2024-01-01 to 2027-04-12) and `golden/`: clean. `leak.py`: REVIEW, the same twelve lines answered under `## Leak review`. `guard.py heart`: PASS. `guard.py surface`: the same three promoted pairs as stage 3b (task63 "North Central", task89 deliverable species, task83 the differentiated older same-puzzle note), none a rename or regeneration case.

**Input gates.** 29 files, 6 formats; spine 1,881,080 rows. Distractors: `loadfcst_da_s26.csv` (23,424 rows, new) and `ercot_zone_peak_outlook_2027.xlsx`; `zone_daily_temps_2017_2026.csv` is on the main path now and is registered in `field_notes.md` beside the new forecast file (H9). No two CSVs share a row count; the extract log names every file but itself.

**As built (MW, Coast · East · Far West · North · North Central · South Central · Southern · West).** Answer 120 · 30 · 0 · 0 · 210 · 25 · 15 · 0 (unchanged). 1-in-10 loads 725.9 · 304.9 · 208.9 · 176.1 · 705.1 · 435.1 · 267.1 · 241.1; exposure before the block 250.9 · 159.9 · 113.9 · 96.1 · 340.1 · 155.1 · 147.1 · 106.1; uncovered after 130.9 · 129.9 · 113.9 · 96.1 · 130.1 · 130.1 · 132.1 · 106.1; the next lot to Southern at 132.1. The centres add 182.3 MW (0.9803 x 186.0). Thinnest margins: lowest value a lot was taken at 134.87 (East) against the highest left 132.09 (Southern), 2.78 MW; East's post-block 129.87 is the nearest whole-MW call at 0.37 from an edge. Rungs and grid as in `## Harden loop 1`. Asks unchanged: every premium and hedge price identical to stage 3a (the decoupling holds by construction, neither ask reads a load figure).

**Write-up and goldens.** `golden.py` reran on the shipped bundle (verifier path, every check asserted first); the Replay sheet's notes and the basis slide now carry the peak-heat draw, the ordinary-afternoon level and the baseline. `submission.md` blocks 1 to 4 revised: the 0.98 factor and 182.3 MW, step 5 on the temperature file, East 160 and South Central 155 before the block, East 130 and South Central 130 after; every block-4 line matched against the Split sheet. Golden containers audited clean.

## Leak review

`leak.py task124 --asof 2027-04-12`: REVIEW, no LEAK. Each REVIEW line, answered:

- Sweep 3, `summer_2026_risk_report.pdf` carries 251: Southern's 2019 cell in the closed replay table (at the 2026 book), not Coast's 2027 exposure; a coincidence of magnitude, no 2027 figure is in the report.
- Sweep 3, `field_notes.md`, `summer_2026_risk_report.pdf` and `summer_risk_policy_2027.docx` carry most words of the committed call: the words are the eight book names, "summer", "block" and "MW", which every document of this organisation uses; none states a 2027 lot figure.
- Sweep 4, `extract_log.md` and `field_notes.md` (closed, premise, system, window, settled): the dictionary's own field descriptions; neither mentions the members' peak-hour draw, called windows at the system peak or eligibility, so neither names the move.
- Sweep 4, `summer_2026_risk_report.pdf` (replay, closed, system, settled, summers): the report states the per-kW replay at the 2026 book, which is rung 1's certification by design (the corpus), not the decisive step.
- Sweep 4, `summer_risk_policy_2027.docx` (closed, premise, system, settled, method, summers): the policy's pins (1-in-10 definition, the coming book, the peak hour); the policy says nothing about classes, the programme or the centres.
- Sweep 6, `summer_2026_risk_report.pdf` names books beside numbers: Table 1 and the replay table are the closed 2026 book's peak-hour loads, with no block split and no 2027 figure, so nothing ranks the books on the 2027 question.
- Sweep 9, `hedge_positions_20270409.xlsx` and `trade_blotter_s27.csv` dates after the as-of: delivery periods of booked strips (June to September 2027, Q4-27, Cal-28), forward by nature.
- Sweep 9, `trading_calendar_2027.csv` dates after the as-of: the desk's 2027 calendar, forward by design.
- Harden loop 1 re-run: the same twelve REVIEW lines and no LEAK. The new `field_notes.md` entries (the temperature file and the day-ahead forecasts) state field semantics only and say nothing about heat, full load or the baseline.
- Stage 3b re-run after loop 1 (`--asof 2027-04-12`): REVIEW, the same twelve lines (sweeps 3, 4, 6 and 9), each answered above; no LEAK.

## Stage 3b: write-up and ship checks (2026-10-10)

- **Goldens.** `generator/golden.py` reads only `target/` through the independent verifier's code path (`verify_pack.py`, all its main-call, corpus and ask checks asserted before anything is written) and writes `summer_block_committee.pptx` (three slides: the split with the levelling chart, the premium and hedge prices, the basis) and `summer_block_split.xlsx` (Split, Replay, Lots, Premium, Hedge price, Notes). Figures printed before and after `golden-realism` and `reduce-house-fixes` are identical; two runs are byte-identical; the container audit is clean (in-fiction author, 14 April 2027 stamp). Every block-4 line of `submission.md` was matched against the workbook by script.
- **Whole MW.** Load less hedges and exposure less lots agree in whole MW on every book. The Split sheet's total row carries hedges and lots only, because the rounded load and exposure columns sum to 1 MW less than their unrounded totals.
- **Surface screen** (`guard.py surface`): three promoted pairs, none a rename or regeneration case. task63 shares the string "North Central", ERCOT's real weather-zone name, which task63 carries inside its own invented "North Central certification district" (North Dakota, a different fiction). task89 shares only the pptx+xlsx deliverable species (no file name, schema, prompt wording or mechanism overlap, mechanism 0.03). task83 is the differentiated older same-puzzle note already on the card. The people note flags "Sabine Crest", which is the company.
- **Heart** (`guard.py heart`): **BLOCK**, from `ban.pattern` (E), `ban.artifact` (close_out_summary) and `ban.forum` (committee_or_panel), all against task129, with a WARN on the pptx+xlsx set against task129. The guard orders cards by draw date then task number, and task125 to task130 were all drawn on 2026-10-10, so the "last three" for task124 is now task128 to task130, builds drawn after it. Run against its draw-order predecessors only (a scratch copy of the cards without task125 to task130), the same card is PASS with one NOTE (task83, differentiated), nearest driver 0.06. The axes on the card are the build's true ones and were not recoded to clear the ban. Either the coordinator rules on the window order, or one of task124 and task129 redraws the colliding furniture; this stage does not touch task129's card. Coordinator ruling (2026-10-10): the window order was the guard's fault, not the draw's. `guard.py` now checks a filed card against its own draw-order predecessors (a build drawn later met this one in its own registration check), and `guard.py heart task124` is **PASS** with one NOTE (task83, differentiated).

### Stage 3b rebuild after harden loop 1 (2026-10-10)

- **Goldens.** `generator/golden.py` rerun on the loop-1 pack (verifier path, every check asserted first). The printed figures are unchanged: split 120 / 30 / 0 / 0 / 210 / 25 / 15 / 0, uncovered before 251 / 160 / 114 / 96 / 340 / 155 / 147 / 106, after 131 / 130 / 114 / 96 / 130 / 130 / 132 / 106, next lot Southern at 132, the centres 182.3 MW at 0.980 (baseline 0.885, called 0.599), every premium and hedge price as in stage 3a. Two runs are byte-identical; the workbook is byte-identical to the previous ship, and the deck moved by one sentence (below). Container audit clean on `golden/` and `target/`.
- **Write-up.** `submission.md` keeps its five blocks; every block-4 line matched against the Split, Premium and Hedge price sheets. Step 5 now states the heat condition exactly as the verifier applies it (days with no credit line whose `tmax_f` in the site's zone is at least that zone's lowest `tmax_f` on the ten closed peak days, summed kWh over summed maximum demand).
- **reduce-house-fixes.** H3 bound: critical component 5 and the basis slide said "no book is left above 132 MW", false as worded with Southern at 132.09; both now state the maximum ("the largest uncovered exposure left after the block is 132 MW (Southern)"). H8: every clause and file cited (risk policy s.2, s.3, s.5; terms s.1; `field_notes.md` for AMEND; Table 2) resolves. H11: one `submission.md` and one `prompt.md` in the tree.
- **Leak, surface, heart.** `leak.py` REVIEW (the same twelve lines, answered under `## Leak review`). `guard.py surface`: the same three promoted pairs (task63 "North Central", task89 deliverable species, task83 differentiated), no rename or regeneration case. Card brought to loop 1: the solved architecture moved into `lineage` (harden loop 0), the main driver, driver_concrete and stump rewritten for the peak-heat rung, and a differentiation line against the slot's own lineage, which `test.own_lineage` and `driver.text` otherwise block (0.39), because hardening deliberately keeps the family. `guard.py heart task124`: PASS, nearest other build 0.05. `guard.py validate`: 126 cards, 0 invalid.

## Tried and rejected

- Draw, the note's tariff-class replay as the decisive rung: a schema-visible join (ESI ID to the premise file's class) that a finest-grain replay of the interval data also hands over, both default moves for the pilot solver; demoted to rung 3.
- Draw, a demand-response re-dispatch rung (the new centres join the programme on lower bids and displace the members carrying a fixed seasonal target, moving the reduction between zones with the book total unchanged): the centres on next season's roster prompt the solver to model their curtailment, which needs the dispatch rule, which hands over the displacement, and the rule has to be stated or empirical in a file the solver then executes.
- Draw, a maximum-demand basis rung (a new premise's maximum demand on the enrolment is its service application estimate, not a metered maximum): reachable by validating the field against interval data for existing premises and joining the application register on the same key; kept only as a candidate ask device.
- Draw, a first-summer ramp rung (new refrigerated sites fill over their first year): the same driver as analytical_tasks note FC04 (station maturity ramp), which a sibling build in this wave may realise, and a cohort split by commissioning age is a group-by a strong forecaster runs on analogs.
- Draw, an endogenous peak-hour shift (the newcomers move the reference hour): the reference is the transmission operator's system peak, exogenous to a retail book, a flat refrigerated load cannot move a peak, and an hourly replay finds it wherever it does apply.
- Draw, a cogeneration outage at a private-use network site (net load jumps to gross while the unit is out): it needs a shipped forward outage record, a sentence the solver executes, and an outage file in a peak-load folder is read as relevant at once.
- Draw, the note's Economics tag: Economics' boundary excludes markets trading, and a retail provider placing call options across zone books is that class.
- Draw, four zone books: shape 05 off four buckets reaches about 20 criteria.
- Draw, "Afternoon Hold" as the programme's name: it describes the mechanism a solver has to find; replaced by a neutral product name.
- Draw, Kenneth Ross and Robert Cobb as personas: first names in one older build each (task93, task104); replaced by Donald Lee from the same draw.
- Design, grading each book's 1-in-10 load and pre-block exposure (the draw's 8 x 3 block): under rung 3 seven of the eight books' loads and exposures equal the answer's, so a rung-3 response keeps 14 component criteria free; replaced by the uncovered exposure left once the lots are in, which moves on every receiving book with the level.
- Design, naming the developer or its centres in the prompt: it points every solver at the one population whose draw decides the call and invites the "what does a new cold store draw" question the stump depends on nobody asking.
- Design, a Business Saver file of kW curtailed per member per event: it names the quantity a peak forecaster adds back; replaced by the billing system's credits (kWh and USD per account per window), keyed on the account number.
- Design, a product sheet that says events are called on forecast system-peak days: one sentence that hands over why the fourteen's peak draw is low; the timing is left to the credit dates against the peak list.
- Design, a programme with general commercial members as well: their called draws would bias the new general premises' class factor too, so the answer would need a second adjustment no record forces.
- Design, refrigerated sites joining the programme a summer after joining the book: the joining summer shows a cold store at 0.90 in the system peak hour, a symptom in the class factor that hands the rung over; eligibility now runs on the meter's history, so every refrigerated arrival was eligible on arrival.
- Design, the amendment rows restating 60 MW (the source note): rung 1 then sits 5 MW from rung 3 and inside 10 per cent of the answer; 275 MW puts rung 1 at +21.4 per cent.
- Design, ask A's primary device as two brokers quoting per MWh of different notional shapes: the same insight as ask B's 5x16 against 7x16 weighting, so one discovery would pay twice; demoted to hazard H4 across both asks and replaced by the third broker's absent channel.
- Design, hedge prices in USD per MW-month beside USD/MWh in the blotter: a magnitude 300 times apart is loud and gets fixed by reflex; replaced by price-only amendments with a matching log.
- Design, a counterparty novation or a re-delivered blotter batch as an ask B device: either moves hedge MW for a solver who builds hedges from the blotter, which puts a device on the main call's path.
- Build, clearing every replay-table cell off its half-MW edge by moving that summer's swing alone: the two summers that set the 1-in-10 are pinned by the exposure target, so the factor solve pulled them straight back and the loop oscillated; they are cleared by a small target shift checked against both pinned cells and the post-block bins.
- Build, a 2026 block split in the close-out report: its figures cannot recompute from a pack that starts at summer 2017 and it reads as a split artifact; replaced by Table 1 (enrolled maximum demand and settled load at the 2026 peak).
- Build, the close-out dated October 2026: true-up for the 2026 peak was not available until late January 2027, so the report would cite settlement it could not have had; dated 2 February 2027.
- Build, residential premises in the book: the enrolment extract would run near 600,000 rows; the book is commercial and industrial.
- Build, a credit line whose account total lands on a half kWh: rounding conventions split on it; the member's first window-hour read is entered 0.1 kWh higher so every total has no half to round.
- Solve, round 1 (plain), the five-rung ladder as built: the solver landed 120 / 30 / 0 / 0 / 210 / 25 / 15 / 0 at step 5 of its path, in its own words "The members were curtailed on every system peak day (bsaver_credits), so their peak-hour reads cannot be used directly; on those days they run at about 0.60 of maximum demand ... That gives a factor of about 0.900 of maximum demand in every summer"; it set the credit dates beside the system peaks and took the uncalled baseline from the programme terms, so rung 3 never held it; hardening loop 1 of 3 follows.
- Harden loop 1, the uncalled-draw rung as built (rung 4 reached through the credit dates and the programme baseline): the solver's own path sentence, "The members were curtailed on every system peak day (bsaver_credits), so their peak-hour reads cannot be used directly ... Each site's baseline follows the program terms: the 10 most recent business days without a call", shows two free routes onto it; the credit file's window dates line up with the published peak list on a one-key date join a solver runs by reflex once it opens a file named for the programme, and the product sheet's baseline clause is a shipped sentence that describes constructing exactly the uncalled draw, so the decisive factor was a reading, not a construction; the uncalled draw stays as rung 4 and is no longer the answer.
- Harden loop 1, a members' NAICS split as the new rung (ice plants idle in the afternoon, cold stores do not, so the fourteen's pooled uncalled draw is wrong for 493120 centres): the split sits on the premise register's NAICS column, a one-key group-by the solver runs on the population it already holds, so it is a row predicate, not a construction.
- Harden loop 1, rooftop solar on the new centres (net load at the peak hour below the analogs' draw): it needs a DG column on the premise register or the enrolment, which names the adjustment on the very rows the solver prices.
- Harden loop 1, a draw linear in heat with no full-load level: every heat-conditioned estimator (regression, hottest decile, days as hot as the peaks) lands on a different factor, so the answer forks on the estimator; the full-load level is what makes the peak-heat estimators converge.
- Harden loop 1, a heat ramp from 0.45 to 0.80 or a step at 0.70 to 0.74: the programme baseline at the closed peak hours (its ten uncalled days run hot just before a peak) lands at 0.90 to 0.92, North Central 200, under 5 per cent from the answer; the ramp sits at 0.68 to 0.78 of the heat index, where the baseline lands at 0.885 and North Central at 195.
- Harden loop 1, leaving the hottest non-peak weekdays uncalled every summer so that the peak-heat sample is large: the desk would miss the five hottest days of every summer while calling cooler ones, a pattern that reads as constructed; the forecast-miss rule stays as built (five of the hottest decile uncalled by the worst forecast scores).
- Harden loop 1, zone temperatures at 14 degrees F per unit of the heat index with 1.1 degrees of scatter: the hottest tenth of each site-summer's uncalled weekdays by zone maximum mixed ordinary days in and landed at 0.949, outside the corridor; the file now runs 30 degrees per unit with 0.7 of scatter, which is also the realistic summer range (about 82 to 108 F).
- Harden loop 1 architecture, solved by round 2 plain (landed, 96.6, asks 7/8): the solver skipped the heat-matched uncalled weekdays and the programme baseline altogether and read the members' uncalled hours on the peak days themselves. In its words: "on each peak day, the 493120 member sites' average load in the uncalled hours (hours ending 11-14 and 19-20) divided by maximum demand is about 0.981-0.982 every year." The shoulder hours of the called peak day sit at full load, so the 0.98 level is visible on the very days the solver already has open; loop 2 has to make same-day uncalled hours read a different level (or not exist at peak-day load) without forking the heat-matched estimator.
- Harden loop 2, an hourly ambient profile on the members' uncalled draw (morning hours cooler, so the peak days' shoulders read under full load): under the loop-1 heat ramp the full-load mark is a few degrees above an ordinary day's maximum, so on a design day it is crossed by late morning and every shoulder hour of a peak day still reads full load; a profile steep enough to drop the shoulders 10 per cent needs a 9 F fall between hours ending 14 and 15, which no Texas afternoon has.
- Harden loop 2, an extended called window on the system-peak days (hours ending 12 to 20, so the peak days carry no uncalled hour to read): a cold store cannot hold a firm level for nine hours, the credit file would need window hours it does not carry, and it removes the solver's step instead of making it return a wrong answer.
- Harden loop 2, uncalled full load kept at 0.90 with pre-cool at 0.96 to 0.99: the peak-day shoulders filed North Central at 220 (+4.8 per cent), inside the 6 per cent floor; the full-load level is 0.85 of maximum demand so the shoulder reading lands at 230 (+9.5 per cent).
