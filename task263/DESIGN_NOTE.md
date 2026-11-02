# task263 design note

Architecture 1, drawn 2026-10-16 (wave 3, Descriptive lane, sathay3012). Seed DA13: the world (a state drinking water revolving fund's $36 million of PFAS treatment-design grants for 2027), the decision (how far the fund reaches down its priority list, and each grant) and the quantity (treatment capacity at the sources whose own water carries PFOA or PFOS above 4.0 ng/L) are kept; the seed's mechanism rows were not read, and the pitfall is re-found from the data. The program's initial monitoring ran quarterly through 2024 and 2025 (the grant's averaging years) and on into 2026; the draft 2027 intended use plan is dated 30 September 2026 and goes to the state's Drinking Water Infrastructure Board on 18 November 2026, so every file in the pack predates the build and the call (grants not yet made) faces forward.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task263.json`, registered 2026-10-16. Re-drawn before any data was cut, once the builds registered earlier that evening (task233, task463, task152) were pulled: the decision sits with the state's Water Infrastructure Finance Authority, the public lender that runs the drinking water revolving fund with the environmental department (`financial_institution`), whose board of directors (`board_of_directors`) allocates the 2027 PFAS set-aside (`budget_or_appropriation`), the requester being the Authority's revolving-fund manager, who runs the fund's portfolio of loans and grants (`portfolio_manager`; `programme_officer` repeats task189); the context artifact is the state's system register; the stump strategy is keyed `composition_mix` (each sample's level is set by the mix of wells pumping, which shifts from sample to sample, so a well's average over its samples is confounded by its partners), the closest key (`decomposition_attribution`, kept as the Gate G mechanism) and the next (`grain_or_unit`) repeating task152 and task233. `guard.py check`: WARN only, `repeat.gate_g` against task152 (a decomposition of a utility-scale plan's cost, not a mixture of sources; answered here) and `test.same_driver_older` differentiated against task187 (a curved, capped response read at matched input spread) and task48 (a population recovered by aggregating up to a pair grain); task263 disaggregates measured blends down to their sources by a mass balance.
2. Pairing: Physical & Environmental Sciences (client domain) / emissions-inventory (a contaminant source inventory, built top down from measurements of mixtures) / Descriptive & Distribution Analysis. Physical & Environmental Sciences has never been paired with Descriptive.
3. Niche: an unnamed Upper Midwest state's drinking water revolving fund sets aside $36 million of its 2027 emerging-contaminants money for PFAS treatment-design grants: $2.4 million per million gallons a day (MGD) of treatment capacity at each active well whose own water carries PFOA or PFOS above 4.0 ng/L, at the well's rated capacity, up to $6 million a system, in priority order until the next grant does not fit. The program's PFAS initial monitoring samples entry points, where the wells pumping at collection mix; no well was sampled on its own in 2024 or 2025.
4. Call and shape: which systems the $36 million funds, each grant in dollars, and how many systems it reaches (`ranked_slate_under_cap`, question form how many). Shape 01 (ranked list under a cap): twenty systems with scored detections, each funded or not with its grant, the count reached, the first system not reached and the unspent balance.
5. Gate G `decomposition_attribution`, strategy key `composition_mix` (item 1): each entry-point sample is a flow-weighted blend of the wells pumping at collection, and the wells' own levels are recovered by a mass balance across samples whose blends differ as operators rotate the wells), decisive generator G2 (grain: the sample is a blend, the decision's unit is the well), then G3.
6. Data-native sentence: the program samples PFAS where water enters the distribution system, so every result is the blend of the wells pumping at that moment, in proportion to their flows; operators lead with a different well each month and call the others on as demand rises (some wells only ever run beside a lead), so the blends differ from sample to sample, and only a mass balance across a system's samples separates a well over the line from the clean wells it runs beside.
7. Sources, one line each:
   - `analytical_tasks/03_descriptive_distribution/DA13`: world, decision and quantity; its pitfall is not used (the note was not read past its Situation).
   - The two-layer design reference's Layer 2 families: `field_method` (the field's own method done right), here the environmental mass balance of a mixture of sources with known proportions, the top-down step of a contaminant source inventory; Physical & Environmental Sciences carries no Layer 2 pattern in the client library, so the pattern is `own:mass-balance unmixing of blended samples`.
   - task255 (censored likelihood) and task262 (a de-attenuated slope) on file in this lane: neither inverts a mixture; censored results here are Layer 1 and converge (every substitution gives the same wells).
8. People, drawn with `guard.py names --geo "United States, Wisconsin" --seed 263`: Judy Carey (the Authority's revolving-fund manager), Lynn Whitaker (the department's PFAS compliance lead); Kyle Hahn drawn and not used (a first name on file). Invented names: the Authority, the department's program, the state's community systems and their wholesale buyers, their wells and entry points, the laboratories.

## Default path

1. Read the draft 2027 intended use plan: a listed system's grant is $2.4 million for each MGD of rated capacity at its
   active wells whose own water (the water the well itself pumps) averaged more than 4.0 ng/L of PFOA or of PFOS over
   2024 and 2025, at most $6 million; the $36 million funds Table 6-1 in order and stops at the first grant it cannot
   cover.
2. Take the twenty listed systems' PFOA and PFOS from the entry-point results export: routine and confirmation samples
   collected in 2024 and 2025, the latest report revision, field blanks and duplicates set aside, non-detects at half
   the reporting limit.
3. Join each sample to its collection record and parse the sources in service: the wells pumping when it was drawn.
4. Give each well the average PFOA and PFOS of the samples taken while it was pumping; a well with either average over
   4.0 ng/L is over the line.
5. For each system, sum the inventory's rated capacity of its active wells over the line, convert to MGD, multiply by
   $2.4 million and cap at $6 million.
6. Walk Table 6-1 until the balance no longer covers the next grant.

Ends on: 7 systems.
Golden: 16 systems.

On the built pack the default path funds Torvik through Kesselring and stops at Nesvold with $672,000 left; the
golden funds Torvik through Valdahl, stops at Nordvold and leaves $451,200.

## Stump sentence

The default path funds 7 systems and stops at Nesvold with $672,000 left because it gives each well the average of the
entry-point samples taken while it pumped, so a clean well that runs beside a well over the line takes on that well's
water and its system's grant swells; each sample is the flow-weighted blend of the wells pumping at collection, and
solving every entry point's samples as a mass balance of its wells' own water leaves only the wells whose own water is
over 4.0 ng/L, so the $36 million reaches 16 systems and stops at Nordvold with $451,200 left.

## Three rules

Task type: emissions-inventory (Physical & Environmental Sciences), a contaminant source inventory built top down from measured mixtures, which serves Descriptive & Distribution Analysis in the taxonomy.
Domain test: the quantity that decides the call is each well's own PFOA and PFOS, apportioned from entry-point samples that blend the wells pumping at collection in proportion to their flows; the environmental field recovers it by a mass balance of the mixtures (a source apportionment with known mixing proportions), the top-down step of a contaminant source inventory.
Swap: "which hospitals' wards each carry an infection rate over the line, from samples of the shared air handlers" keeps a threshold but loses the flow-weighted mixing of sources with recorded proportions that the mass balance inverts, so the call no longer reads the same.
Layer 1: a statewide export of every community system's samples (the state's database); non-detects reported at each laboratory's reporting limit and one contract laboratory on Method 537.1 with its own analyte list (the laboratories); field reagent blanks and field duplicates among the field samples, and reissued reports loaded beside the originals (the database's load rules); sources in service written in each sampler's own hand, now and then left blank (the collection form); ISO dates in the results and month-first dates on the collection records (two systems); 2026 samples past the grant's years (the export's pull date). Nothing is placed to be caught; each converges (asserted).
Layer 2: the decomposition and attribution family; each entry-point sample is a mixture of the wells pumping at collection, and the wells' own levels are recovered by solving the samples of each entry point together as a mass balance with the flows as mixing proportions, rather than by attributing a sample's level to the wells in it.
Decisive step: inverting the mixtures, every entry point's samples solved together for its wells' own water (by least squares or by chained subtraction from the samples where partners ran), instead of giving a well the average of the samples it ran in, the flow-share weighted average or its samples run alone.
Not semantics: every field read correctly (the entry point, the sources in service, the flows, the reporting limits, the sample types, the plan's own-water definition) still leaves the analyst averaging the samples each well ran in, which names the wrong wells and files 7 systems; the plan defines the well's own water and no field holds it.
Not rule application: the plan fixes the estimand (a well's own water averaged over 2024 and 2025), the rate, the cap and the order; no filed rule or procedure says how to get a well's own water from entry-point blends, so executing every stated rule still files the default path's answer.
Analyst test: a strong analyst who reads every field and rule correctly attributes each blend to the wells pumping in it, averages each well's samples, sizes the grants and walks the list to 7 systems (Ends on), when the mass balance of the blends files 16 systems.
Estimand: the draft 2027 intended use plan (section 6) files the population (the active wells of the twenty listed systems), the outcome (each well's own PFOA and PFOS, the water the well itself pumps), the window (averaged over 2024 and 2025), the unit (the well, then the system's grant on its wells' rated capacity) and the comparison (more than 4.0 ng/L of PFOA or of PFOS).
No decoy: nothing is planted; no memo, draft, published figure or staff note argues a well, a grant or a reach, the blends are what the program's sampling produces, and the never-alone wells are the operators' peak wells.
No certified replay: the method is not recovered by reproducing a published figure; no file publishes a well's own level, a share or a grant.
Lesson: a sample taken where sources mix measures the mixture, and a source's own level comes from solving the mixtures together with their proportions; attributing a mixture's level to every source in it, even weighted by share, is what the field's mass balance replaces, and no build on file inverts measured mixtures into their sources.

## Survivor anatomy

Actor: each listed well's own PFOA and PFOS has no column in any file; the results hold entry-point blends and the records the wells pumping, so the deciding property is a relation across each entry point's samples that nothing stores (R1, asserted).
Link: the signal is read through each entry point's samples solved together, the pumping wells' rated capacities as the mixing proportions; no key joins a sample to a well's own level and no shipped sentence says a sample is a sum of its sources (R3c, asserted).
Reflex: the field's reflex, crediting each well with the samples taken while it pumped (the average of the samples it ran in), is rung 0 and files 7 systems stopping at Nesvold, the Ends on line, not the golden 16.
Back-test: the easy route validates on the pack: every well R0 puts over the line stands at an entry point with a result over 4.0 (asserted), and no file publishes a well's own level that could refute it.
Second use: every file the decisive step reads has its own use in the pack (the state's compliance export, the samplers' forms, the facility inventory, the grant rules), and deleting the step leaves every one of them.
Shock: the wells the mass balance moves are ordinary clean wells pumping beside a contaminated lead; on no sort of the active wells by a shipped statistic (the mean, median, highest or lowest of the samples each ran in, or rated capacity) are the golden's 23 the top 23 (asserted).
Pins: the plan files the WHAT (a well's own water averaged over 2024 and 2025, the rate, the cap, the order) and no filed sentence names a mixture, a balance, a share, the rotation or the sampling clock the stump rides on.

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 (default) each well given the average of the samples taken while it pumped | the plan defines a well's own water and the collection record names the wells pumping at each sample | the sources in service sit on every collection record, one join from the results | yes: attribute each measurement to the units present | none: no published well level | the battery finds nothing | yes: one average per well | readable |
| R1 the same average weighted by each well's share of the flow | none names a share | rated capacities in the inventory, one join | yes: weight by contribution | none | none | yes | readable |
| R2 the samples a well ran alone, the average of its samples where it never did | none | the sources in service show the single-well samples | yes: use the clean measurements where they exist | none | none | yes | readable |
| R3 (decisive) each entry point's samples solved together for its wells' own water | none names a mixture, a balance or a share; the plan defines the estimand, the guide says where the samples are drawn | no column holds a well's level or a mixing proportion | no: the opponent treats a sample as a measurement of what was present, not an equation in its sources | no published figure to reproduce | the battery (keys, duplicates, revisions, non-detects, units, the parse) never asks what a sample is a sum of | no: a least-squares solve per entry point across 8 to 16 samples, or a chain of subtractions | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the systems on the list | the twenty in Table 6-1 of the plan | every system with an entry-point result over 4.0 | same call (the list is the plan's) | the plan funds Table 6-1 in order |
| SF2 | a well's own water | the water the well itself pumps | the water leaving its entry point (the samples as taken) | 6 systems (Kesselring) | the plan: a well's own water is the water the well itself pumps |
| SF3 | averaged over 2024 and 2025 | every routine and confirmation sample collected in 2024 and 2025 | 2026 samples added; routine samples only | same call | the plan names the years; asserted: same call |
| SF4 | more than 4.0 ng/L of PFOA or of PFOS | either analyte's own level over 4.0 | the sum of the two over 4.0 | same call | the plan: of PFOA or of PFOS; asserted: same call |
| SF5 | more than | strictly over 4.0 | 4.0 or more | same call | no well's own level within 1.0 ng/L of 4.0 (asserted) |
| SF6 | active wells | wells with status Active in the inventory | emergency wells included | same call | the inventory's status; the one emergency well never ran at a sample, so it has no own water to judge |
| SF7 | rated capacity | the inventory's rated_capacity_gpm | the entry-point flow at collection; the 2025 pumpage | ruled out | the plan: rated capacity is the capacity the inventory records for the well |
| SF8 | MGD | gallons a minute times 1,440 over 1,000,000 | none | same call | every rated capacity is a whole number of gallons a minute, so each grant is exact to the dollar |
| SF9 | the cap | $6 million a system | none | same call | the plan |
| SF10 | stops | funding ends at the first grant the balance does not cover | skip that system and fund later ones that fit | same call | the plan; asserted: no grant after Nordvold fits $451,200 |
| SF11 | the order | Table 6-1 | an order by result or population | ruled out | the plan funds in the order of Table 6-1 |
| SF12 | reach | the systems funded | the systems with a grant over zero | same call | every listed system has a well over the line |
| SF13 | left | $36 million less the grants made | none | same call | the plan |
| SF14 | non-detects | half the reporting limit | zero; the reporting limit | same call | asserted: same call and same wells at every substitution |
| SF15 | quality-control samples and reissued reports | blanks and duplicates set aside, the latest revision | duplicates kept; blanks kept as zero; both revisions kept | same call | the guide's sample types and revision rule; asserted: same call |
| SF16 | the mixing proportions | each pumping well's rated capacity over the sum | the entry-point flow shared by capacity; equal shares; each well's 2025 monthly pumped volume | same call; same call; 14 systems as the operating reports write the meters (12 on each well's own volume, the wellhouse lines net of the wells piped into them) | asserted: same wells under the first two; the monthly volumes are ruled out by the inventory's own pump column beside rated capacity (every well "Vertical turbine, constant speed" or "Submersible, constant speed", so a well pumps at its rated capacity whenever it runs; filed once, read through the verifier's xlsx reader) and by the entry-point flow on every listed record, within 7 per cent of the running wells' rated capacities (median gap 1.2 per cent, largest 6.0; the verifier's readers) |
| SF17 | sources not recorded | those samples left out | the wells inferred from the entry-point flow | same call | asserted: same call |

## Ladder

Values on the built pack (analysis.py; asserted in checks.py, recomputed in verify.py).

| Rung | Construction | Reach | First not reached, left | Killed by |
|---|---|---|---|---|
| R0 (default) | each well given the average of its samples | 7 | Nesvold, $672,000 | a sample's level is its mixture's, so a clean well's average carries its partner's water |
| R1 | the same average weighted by flow share | 8 | Elvholm Falls, $2,400,000 | weighting a mixture by share still credits each well with the whole mixture |
| R2 | the samples a well ran alone, its average where it never did | 11 | Skogen, $1,708,800 | a well that only ever runs beside a lead (the operators' peak wells) is never alone; its own water is still in its samples, beside known partners |
| R3 (decisive) | each entry point's samples solved together as a mass balance | 16 (golden) | Nordvold, $451,200 | the golden |

- **Cells beside the rungs.** Every well at an entry point with a result over 4.0 (the compliance view): 6, Kesselring,
  $4,694,400; the wells pumping at a result over 4.0: 6, Kesselring; the median of a well's samples: 8, Elvholm Falls;
  the wells in each entry point's highest sample: 13, Isaksen Ridge, $796,800; the samples run alone and nothing for
  a well never alone: 19, nobody left out, $4,032,000. The golden is bracketed (13 and 19 on either side).
- **Separation.** Each rung names a different count, first system not reached and balance left; no rung shares the
  golden's count, stop or balance.
- **Worth.** The decisive move adds 5 systems (11 to 16), more than the moves before it (7 to 8, 8 to 11); it changes
  Torvik's, Wikstrom's and Dalrud's grants and the stop. R0 gets 1 of the golden's 16 grants (Halvorsen's, capped), R1 3,
  R2 7.
- **Convergence.** The mass balance by least squares, by non-negative least squares, by chained subtraction, with
  non-detects at zero, half or the reporting limit, with the entry-point flow or rated capacities or equal shares as
  proportions, on routine samples alone, with duplicates or blanks kept, with 2026 added, or with the sum of PFOA and
  PFOS, flags the same 23 wells and files 16 systems; the nearest well's own level sits 1.61 ng/L from the line.
- **Clean truth.** On the true blends with no laboratory scatter the rungs file 7, 8, 11 and 16 (R3a, R3b).

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the active wells of the twenty systems in Table 6-1 | filed (the plan); SF1, SF6 |
| 2 | Unit of account | the well, then the system's grant on its wells' rated capacity | filed (the plan) |
| 3 | Attribution window | samples collected in 2024 and 2025 | filed (the plan); SF3 |
| 4 | As-of dating | the inventory's statuses and capacities as extracted 1 September 2026, the register's populations as the plan's note dates them (1 September 2026), the plan's list as drafted 30 September 2026 | filed (the plan) and by construction (one inventory and one register in the pack; extraction dates in metadata.json) |
| 5 | Version basis | the latest report revision of each sample | filed (the guide); SF15 |
| 6 | Denominator | none: a level against a line, then dollars | n/a |
| 7 | Weighting | each sample once; the mixture by the pumping wells' flows | design (the data's structure: the inventory's pump column, the records' entry-point flow); SF16 |
| 8 | Window length | two calendar years | filed |
| 9 | Boundary inclusivity | more than 4.0 ng/L; collected 1 January 2024 to 31 December 2025 | filed; SF5 |
| 10 | Rounding path | grants exact to the dollar from whole gallons a minute; no rounding of levels before the comparison | prompt; SF8 |
| 11 | Tie-break | none needed: no well within 1.0 ng/L of the line | asserted |
| 12 | Maturity and censoring | non-detects under the reporting limit; every substitution flags the same wells | C1; SF14 |
| 13 | Order of operations | each well's own level first, then the comparison, then the grant, then the walk | filed (the plan) |
| 14 | Row order | none matters | C1 |
| 15 | Duplicate resolution | field duplicates and blanks are quality control; a reissued report replaces the first | filed (the guide); SF15 |
| 16 | Identity normalisation | the state sample number joins results and collection records; the sampler's text parses to well numbers | by construction; SF17 |
| 17 | Netting against gross | none | n/a |
| 18 | Dimensional units | ng/L in the state's export (the 2023 national survey's micrograms per litre is a distractor); gallons a minute to MGD | the producing systems' own units columns (the export's ng/L, the survey's own Units column in micrograms per litre, asserted); SF8 |
| 19 | Code and status semantics | sample types, revision numbers, facility statuses; for the ask, facility types and meters | the guide (sample types, revisions), the plan (the active wells are those the inventory lists as active) and the systems' own labels (Active, Emergency, Inactive; Well, Interconnection; each meter's registered facility and location); never the stump |
| 20 | Integerisation | dollars whole; water to a tenth of a million gallons | prompt |
| 21 | Clause scope | section 6 of the plan governs the call; the operating reports and the meter register carry the ask, by Table 6-1's county and the quarter of the report month | filed (the prompt, the plan's Table 6-1) |
| 22 | Forward window contents | the 2027 grants rest on the 2024 and 2025 samples, the two complete years the department reviewed | filed (the plan) |

## Literal reader

Executed word for word, the plan defines the eligible wells by their own water, the water each well itself pumps
averaged over 2024 and 2025, and no file holds it; the only measurements are entry-point samples whose collection
records name the wells pumping and whose entry-point flow equals their capacities' sum, so the literal estimand is each
well's own level recovered from the samples, and every consistent recovery (any of the mass-balance variants in the
ladder's convergence line) flags the same wells; averaging the samples a well ran in is not its own water but its
mixtures', so the readings that differ (SF2, SF7, SF11) each violate a quoted sentence and the rest give the same call.

## Oracles

none for the call: no file publishes a well's own level, a mixing proportion, a grant or a reach; the national survey
(2023, distractor) holds older entry-point blends in micrograms per litre with no sources in service, so it confirms no
well. For the ask, no file publishes a county's, a system's or a well's 2025 water; the referee is the pumps (the
inventory's rated capacity and constant-speed pump column against each line's days in service), never a total the
answer inverts from.

## Ask sheet

| Ask | Figures | H18 home | Use | Primary device | Hazards | Path (files, columns) | Stops (lazy delta) | Realism |
|---|---|---|---|---|---|---|---|---|
| A, for each county, how much water the listed systems' wells pumped in each quarter of 2025, in million gallons to one decimal | 16 (four counties by four quarters) | each listed system's 2025 production through the year, a measure every candidate carries that the call does not turn on | the board's view of the water the list's wells deliver, the summer quarter the treatment has to carry | a wellhouse meter that also carries a second well's water, a cardinality judged across two systems by the pumps: at Torvik (Hedstrom), Halvorsen (Engvall), Lindvik Lake (Granlund) and Elvholm Falls (Sandholm) a second well is piped into the first well's wellhouse ahead of its discharge meter and keeps its own meter at its pump; the register links each meter to the one facility it is registered to, at the wellhouse discharge like every other well meter, and the operator writes each meter on its facility's line, so the second well's water is on both lines; no field, location or note says so, the two lines never match in readings or gallons, and only the pumps show it | H1: Ackerholt Creek's September emergency purchase on its interconnection's line (not a well); H2: Fjelstad's Well 2 meter changed out in June (the readings restart, the gallons are right); H3: Kesselring's emergency well ran three days in July (a listed system's well that pumped); H4: Skogen's two wells on one header meter the register lists on both, its readings written on both lines (each meter once) | the operating reports (pws_id, report_month, facility_id, meter_start, meter_end, volume_gal, days_in_service), the meter register (facility_ids, location, removed), the inventory (facility_type, status, entry_point, rated_capacity_gpm, pump), the plan's Table 6-1 (county); 4 files, 15 columns | every line: over by 14.9 to 78.4 million gallons a county-quarter; each meter once (the careful route): over by 14.9 to 77.8; the second well taken off only where a line is beyond its pump: over by 0.6 to 7.9; only the overloaded well's line at its entry point: under by 5.1 to 41.3; active wells only: Hedstrom July to September under by 0.8; readings for gallons: Granlund April to June under by 207.7 | a newer well piped into an older wellhouse to share its chlorination and discharge meter, a register carrying one facility per meter and an operator reporting each meter on its facility's line are what a monthly operating report and a facility inventory produce |
| C, the chart | its parts | the construction | the call's own exhibit | none | none | the golden's well levels | R0 to R3 | the analyst's own exhibit |

- **The device's forcing (checks.py, on the shipped rows).** In every month the second well leads, the wellhouse line
  carries more than its own constant-speed pump delivers at its rated capacity in its days in service, 1.4 to 6.0
  times, in at least one month of every quarter at each wellhouse and twice or more in at least two months; net of the
  second well's own line it stays within 0.88 of its pump in every month; every other listed well line stays at or
  under 0.89 of its pump; the pump physics read from the rows finds exactly these four wellhouse meters and, at each,
  exactly one well that brings it within its pump (every other well at the entry point leaves it 4.2 times or more
  beyond).
- **Over-cleaning half.** Each wellhouse entry point has a third, separately metered well (Torvik's Wells 3 and 4,
  Halvorsen's Well 3, Lindvik Lake's Well 3, Elvholm Falls' Well 1). Taking every other well at the entry point off the
  overloaded line, or keeping only that line, undercounts every county-quarter by 4.7 to 40.9 million gallons. The
  second well runs only in the months it leads (bar one sampler's visit at Lindvik Lake, half an hour), so taking it
  off only in the months its line is beyond the pump files the golden: the piping's evidence and its effect coincide.
- **Pin test.** The asking sentence pins the population (the listed systems' wells), the grain (Table 6-1's county by
  calendar quarter of 2025), the unit and rounding (million gallons to one decimal, in the closing sentence); the
  device sits in the one dimension the pins leave open, which lines carry a well's own water, and no filed sentence
  names a meter, a wellhouse, a header or a pump's limit.
- **Main population zero-counts.** No ask device or hazard sits in the twenty systems' 2024 and 2025 PFOA and PFOS
  samples, their collection records, their active wells' inventory rows or section 6 of the plan: every file the call
  reads is byte-identical to the shipped cut c38b7092 (asserted by md5), and the call computed with the operating
  reports and the meter register deleted equals the golden (asserted).
- **Hazard table.** H1 moves Granlund July to September by 2.6 for a path keeping the purchase; H2 moves Granlund April
  to June by 207.7 for a path reading the meter readings; H3 moves Hedstrom July to September by 0.8 for a path keeping
  active wells only; H4 moves Hedstrom by 35.2 to 50.1 in every quarter for a path counting the header meter on both
  lines.
- **Referee.** The pumps: the inventory's rated capacity and its pump column (every well on a constant-speed drive)
  against each line's days in service, never a total the answer inverts from; no file publishes a county's, a
  system's or a well's 2025 water.
- **Ask B is cut** (the people living in each county who get their water from the listed wells): its renumbered buyer
  was spent by the register's twin of the same name and county, and no people device in the register and the
  connections passes both tests (Tried and rejected); the two files ship as distractors, named in metadata.json.
- **One primary family.** A response that models every pump keeps the ask; the ceiling prints that case (pair 58.5 if
  the cracker alone does it, 86.0 if both responses do) and no second family on these rows passed both tests.

| Rival reading (a careful judge's) | County-quarter figures | Verdict |
|---|---|---|
| the second well's own line left out instead of taken off the wellhouse line | the golden in every county-quarter | same |
| the second well found from the rows as the one well at the entry point that brings the wellhouse line within its pump every month | the golden; one well fits at each wellhouse (asserted) | same |
| the second well taken off only in the months the wellhouse line is beyond its pump | the golden in every county-quarter | same: the second well runs only in the months it leads, and in each of them its host's line is beyond the pump (asserted) |
| every other well at the entry point taken off, or only the overloaded line kept | 4.7 to 40.9 low in every county-quarter | ruled out: the third well brings no wellhouse line within its pump (asserted), so it is not inside the meter |
| the lines as written, each register meter once a month | 14.0 to 76.7 high in every county-quarter | ruled out: four wellhouse lines carry more than their pumps can deliver |
| the wellhouse well's rated capacity understated | n/a | ruled out: the entry-point flow on every listed record matches the running wells' rated capacities within 7 per cent (SF16), and the excess comes only in the months the second well leads |
| active wells only | Hedstrom July to September 0.8 low | ruled out: the emergency well is a listed system's well and pumped three days |
| the meter readings in place of the gallons | Granlund April to June 207.7 low | ruled out: the readings restart at the June meter change the register records; volume_gal is the gallons |
| the interconnection's purchase in | Granlund July to September 2.6 high | ruled out: purchased water, the inventory's Interconnection, not a well |

| Ask figures | Cracker's path (the careful solver: lands the call, runs the battery, reads every field by its plain meaning, executes every filed rule) | Cracker's value | Verdict |
|---|---|---|---|
| A water by county and quarter (16) | the operating reports' gallons for the listed systems' wells (facility types from the inventory, the emergency well that ran in, the interconnection out), each register meter once a month (Skogen's header), the battery clean (no exact or near-exact duplicate off the header, no equal gallons, no roll-up, readings continuous, units gallons by magnitude, every listed well twelve lines), by Table 6-1's county and the report month's quarter | over by 14.9 to 77.8 million gallons in every county-quarter (the four second wells' water on both lines) | miss |

Mirror leakage: 0.0 per cent of the ask weight: the mirror (R0) takes the ask the cracker's way and misses all 16.
Pair ceiling: 31.0 on the cut pack (the cracker 50.0 with the call, its components and the chart; the mirror 12.0);
two careful responses on the call 50.0 each; 58.5 if the cracker alone models every pump.
Measured by: `generator/ceiling.py`, run on target.zip after every change (checks.py runs its scoring on the cut
folder and asserts it): the careful-solver cracker keeps 0 of 16 ask figures, the mirror the same, the full includer
(the golden's own route) reproduces figures.json.

## Build record

- **World.** The twenty listed systems keep the draw's wells, entry points and own levels (Halvorsen's two wells over
  the line lowered to 18.5 and 9.8 ng/L and its Well 3 widened to 750 gpm so the clean well's estimate stays clear of
  the line under every handling); 88 other well systems, two surface-water systems, 17 wholesale buyers and two
  systems with their own wells beside a tie to a listed system; every quarter's sample at every entry point is the
  flow-weighted blend of the wells the month's rotation and the day's demand put in service (world.py); the 2025
  operating reports come from the same rotation, each sampling day's wells running that day.
- **Names.** Every invented place and organisation was screened against US places (every ZIP-code place, every
  county, every city over 15,000): none within one edit of a distinctive real word, none containing one; the first
  draft's names that sat on real Midwest towns were retired (checks.py H21 keeps the near-miss register).
- **Pack.** 12 files: the statewide results export (36,414 rows), the field collection records (1,519), the source
  facility inventory, section 6 of the draft 2027 plan, the sampling guide, the 2025 operating reports (2,652), the
  meter register, the system register, the wholesale connections, the laboratory list; two distractors (the 2023
  national survey in micrograms per litre, the private well program's results).
- **Gates.** checks.py 96 assertions (golden against the truth, the three rules, the ladder and its cells, every SF
  row, convergence, both asks and their stops, separation, distractors, input gates, realism, H21); verify.py PASS on
  its own code path (pandas, pypdf, normal equations); two builds byte-identical; figures_check 61 of 61; precut 49
  of 49; voice-check PASS; leak.py REVIEW (no LEAK); producer metadata clean; guard heart WARN; guard surface
  promotes task187 and task48 on the card axes alone (surface 0.09 and 0.07, no shared names or text), the two
  builds the draw differentiated (the card's differentiation lines).
- **Stage 4.** Leak reader loop 1: no decisive-step sentence (it names the plan's own-water definition and the
  record's sources in service as what a solver would have to work from), no ranking file, nothing reading as the
  answer, Q6 analytical (unmixing each entry point's blends decides); its realism notes fixed in one pass (names of
  one style, six counties statewide, priority points falling one or two at a time, a percentage in the plan implying
  an unexplained base). Judge r1 DETERMINISTIC, APPROVE (Gate G method_or_model_selection, analytical_non_defect;
  Gate H domain pass, layers pass, decisive step analytical); every graded figure reproduced and the call held under
  every variant tried; its one finding, block 1's rival clause for the samples a well ran alone (no fallback named,
  the thread got 20), reworded to name the fallback (11, asserted); its optional prompt pins ("all wells in the
  inventory", "as of 1 September 2026") declined, the literal readings already giving the goldens. Found in the same
  pass by the main thread: weighting each 2025 blend by the wells' monthly pumped volumes files 11 systems, now ruled
  out by a filed pump fact in the inventory's notes (SF16, asserted). The fix pass leaves every listed system's
  results and records byte-identical to the judged pack and every graded figure unchanged. Leak reader loop 2 on
  the fixed pack: the same answers (no decisive-step sentence, no ranking, Q6 analytical); its texture notes fixed
  (varied field notes, six closed systems in the register, connection dates off the first of the month), the
  listed systems' rows again unchanged.
- **Wave 3 audit (2026-10-18).** cracker.py, run on the strict battery, followed the purchase chains (the plain
  reading of "get their water from") and landed Ask B in all four counties; Ask B is now held by four buyers, one in
  each county, still on the connections under the id the register holds as inactive beside the active system of
  the same name and county (the cracker under by 51 to 297 a county, asserted). Judge pass 2 DETERMINISTIC, APPROVE
  (every figure reproduced; soft readings: the renumbering resolved by name, the county people are counted in, the
  emergency well); its optional tightening taken into the prompt after the verdict ("people living in the county
  ... any of those wells"), no graded figure moved. Reader loop 3 clean (Q1 none, Q6 analytical, neither ask's
  device named). checks 102, verify PASS, two builds byte-identical, figures_check 61 of 61, precut 50 of 50; the
  call's files and every listed row unchanged.

- **Leak re-check (2026-11-01).** The department's notes and the inventory's Notes sheet no longer ship (Tried and
  rejected). Against the shipped pack: 9 files byte-identical; the inventory's Facilities sheet identical but for its
  own pump column beside rated capacity (the sanitary survey's pump type, every well on a constant-speed drive); the
  federal survey identical but for its own Units column; the plan identical but for its note under Table 6-1 (the
  counting rule); the goldens and figures.json byte-identical. Provenance (each file's system, extraction or issue date
  and rows) is in metadata.json. checks 120, verify PASS, two builds byte-identical, freeze determinism PASS,
  figures_check 61 of 61, precut 61 checks 0 FAIL, voice-check PASS, leak.py at --asof 2026-09-30 REVIEW with no LEAK
  (sweeps 1, 12 and 13 clean), guard surface exit 0. Each REVIEW line, ruled:
  - 3, the plan names Torvik beside decision words: Table 6-1 is the list itself (rank, PWS id, system, county,
    population, points), with no grant, well or reach (R3c asserted).
  - 3, the plan carries 13 of 18 words of the call: the plan's own words for its list and set-aside; it names no reach,
    stop or balance.
  - 4, the plan holds 7 of the sweep's design-note terms: domain words; 6.3 reads as shipped, and the note's counting
    rule names no mixture, balance, share or solve (R3c asserted).
  - 4, the guide holds 13 of them: the sampling guide's own words, unchanged, read by three reader loops with no
    sentence naming the move.
  - 6, the plan names all 15 answer-set candidates beside numbers: Table 6-1 orders by priority points only.
  - 6, the operating reports name all 15 beside numbers: an export at its own grain (facility month), no ranking.
  - 6, the results export names all 15 beside numbers: an export at its own grain (analyte, sample, revision), no
    ranking.
  - 6, the collection records name all 15 beside numbers: one record per bottle set, no ranking.
  - 6, the inventory names all 15 beside numbers: one row per facility, no ranking.
  - 11, the prompt's "the twenty systems": predates this repair (voice-check WARN, PASS); it sits in the call's
    sentence, frozen in a determinism-scope repair; for the main thread.
  - 11, the shell quota ("give", png+xlsx): predates this repair, a corpus quota WARN; for the main thread.

- **Ask rework (2026-11-02, rubric scope, the call frozen).** The honest-cracker audit's two spent devices are gone:
  the four listed shared header meters (identical lines on both wells) became four wellhouse meters that also carry a
  second well piped in ahead of them, each second well keeping its own meter (world.py NESTED, records.py meters and
  write_mor), and Skogen's header stays as an announced hazard; Ask A moved from county totals to county by quarter
  (16 figures); Ask B (people) is cut and the system register and the wholesale connections ship as distractors. Two
  small systems' 2025 demand was raised 0.2 per cent (DEMAND_ADJ, Dalrud and Ekholm) so every county-quarter sits at
  least 0.12 of a rounding step from an edge. Every file the call reads is byte-identical to the shipped cut c38b7092
  (asserted by md5); only the operating reports and the meter register moved, with the prompt's ask sentence and its
  closing rounding sentence. The call's SF16 rival (the 2025 monthly volumes as mixing proportions) now files 14
  systems as the reports write the meters (12 on each well's own volume), still ruled out by the pump column and the
  entry-point flows. ceiling.py replaces cracker.py: the careful solver's battery runs clean and keeps 0 of 16, the
  mirror 0, pair 31.0, the full includer exact. Found while writing the survivor anatomy, for the main thread and
  outside this repair's scope: crediting a well as over the line only when even its lowest sample is over (the lowest
  sample it ran in) files 16 systems and leaves $451,200, every one of the 16 grants the golden's, and stops at
  Glomstad rather than Nordvold (it misses Nordvold's and Ekholm's Well 2 and adds Halvorsen's Well 3); the ladder
  does not list it.

## Pre-ship check

- **Rule 1, the domain, on the built pack.** The call is decided by each listed well's own PFOA and PFOS, recovered
  from 302 entry-point samples at 24 entry points by solving each entry point's samples as a mass balance of the
  wells pumping at collection (the field's source apportionment with known mixing proportions). No shipped column
  holds a well's level, a mixing share, an eligibility or a grant (asserted, R1). With another field's nouns the
  flow-weighted mixing of sources with recorded proportions is gone and the call no longer reads the same.
- **Rule 2, two layers.** Layer 1 on the call's path is what the state's systems write: a statewide export, a
  contract laboratory on another method, non-detects at each laboratory's limit, blanks and duplicates among the
  field samples, reissued reports kept beside the first, the samplers' free text (three records left blank),
  month-first dates on the records, 2026 samples past the plan's years; each mishandled leaves the same 23 wells
  and the same walk (asserted, R2). Layer 2 is the inversion of the mixtures: on the generator's clean truth the
  average of the samples a well ran in files 7 systems and the mass balance alone files the golden 16 (R3a, R3b).
- **Rule 3, the decisive step.** No shipped sentence names a mixture, a balance, a share or a solve (asserted on
  every document); the plan defines a well's own water as the water the well itself pumps, and the guide says
  where entry-point samples are drawn and what the collection record holds. Executing every filed rule with the
  natural per-well measure (the average of the samples it ran in) files 7 systems; nothing planted, copied or
  withheld carries the answer (R3c).
- **Determinism.** Least squares, non-negative least squares and chained subtraction, rated or metered or equal
  shares, every non-detect substitution, routine samples alone, duplicates or blanks kept, both report revisions
  kept, 2026 added and blank records inferred from the entry-point flow all flag the same 23 wells (the nearest
  1.61 ng/L from the line) and the same walk; skipping Nordvold changes nothing (no later grant fits $451,200);
  every grant is exact to the dollar; every county-quarter water figure sits at least 0.12 of a rounding step from an
  edge; the careful solver's route misses all sixteen county-quarter figures by ten or more rounding steps, and the
  second well's own line left out gives the golden as taken off the wellhouse line (asserted; ceiling.py on the cut).

## Tried and rejected

- 2026-10-16, at the draw: censored PFAS results at two reporting limits as the decisive step (Kaplan-Meier or a censored likelihood against substitution): the censoring family is task255's in this lane; censored results stay Layer 1 and converge.
- 2026-10-16, at the draw: a concentration-flow relationship to volume-weight each source's level from a few grab samples (missing at random given pumping): the move (a covariate carrying a quantity to the unsampled population) is task256's; dropped.
- 2026-10-16, at the draw: the seed's blend-down (treating only enough sources for each entry point to meet 4.0 ng/L): it needs the fund's rule to say one thing and the answer another, the official-decoy architecture the 10/10 rules ban.
- 2026-10-16, at the draw: treatment sized on each well's maximum-day pumping against its average: the basis would have to be filed (rule application) or left open (a fork).
- 2026-10-16, at design: a 2025 to 2026 window with a 2027 board date (files dated after the build); the window moved to 2024 and 2025 and the board to 18 November 2026.
- 2026-10-16, at design: asks on the 2026 design grants' payments (a payee changed after a consolidation, a cancelled warrant): the cracker joins payments to draws by voucher and lands; replaced by the shared-meter pumpage and the buyers-of-buyers reach.
- 2026-10-16, at design: a Hazard Index ask on the listed entry points: every device on its rows was executed by a filed rule or caught by the battery; dropped.
- 2026-10-16, at build: the first names (Tillerton, Halloway, Ivanhoe Ridge, Paxton Creek, Kettering Bluff, Sedgwick, Fenwick, Ellery and others) sat on or one edit from real US places; all invented names re-drawn and screened.
- 2026-10-16, at build: field reagent blanks carrying the visit's sources in service let a careless mass balance pull Halvorsen's Well 3 over the line; blanks' records now carry no sources (the sampler's habit), and Halvorsen's levels were lowered so every handling keeps the same wells.
- 2026-10-16, at build: a fixed daily run-time cap repeated monthly volumes across systems; the cap now varies by day and small systems' wells are sized to their demand.
- 2026-10-17, at stage 4: rounding the unlisted systems' pump ratings to 5 gpm changed their blends and confirmation samples, which renumbered the statewide samples and moved the listed systems' blank records and revisions; reverted to 25 gpm so every listed row stays as judged.
- Ask B held by the purchase chain alone (wave 3 audit): following buyers of buyers is the plain reading of "get their water from", and measured in code the cracker's closure landed all four counties; the chain now runs through a buyer renumbered on a change of owner, the connections still on its retired id.

- 2026-11-01, in-house re-check under the new leak gate: the department's covering notes (`data_request_notes_2026-09-02.txt`, each file's columns, codes and row counts; LEAK, 12 of the results export's columns named) and the inventory's Notes sheet (glosses of rated_capacity_gpm, entry_point and status, and the pump fact) shipped through wave 3 and describe the data. Replaced by metadata.json for provenance, by the plan for the two facts the build needs (6.3's pump fact closing SF16, the note under Table 6-1's counting rule as Ask B's referee), by the survey's own Units column for closure 18, and by the guide and the systems' own columns and labels for the rest; the asks' devices stay unstated.
- 2026-11-01, this reship's first cut (target.zip 81d61969): the pump fact filed as the last sentence of the plan's 6.3 ("Well pumps in the state's community systems are constant-speed: a well pumps at its rated capacity whenever it runs.") sat beside the own-water definition, and the stage 4 leak reader read the two together as a hint at the step the call turns on (recovering each well's own water from the entry-point samples); the sentence left the plan (6.3 reads as shipped) and the fact moved to the inventory's own pump column beside rated capacity, every well's pump on a constant-speed drive.
- The ceiling recorded on the reship cut was a narrowed cracker's (2026-11-01, honest-cracker audit): the careful solver, every field read by its plain meaning, every filed rule executed and the hygiene battery run, keeps 8 of 8 against the recorded 0 of 8, SPENT on Asks A and B, pair 58.5 with the mirror held at 0 (83.5 with the mirror on the honest route); the reason in one line: Ask A the paired wells' identical meter lines and the register's common discharge header; Ask B the inactive buyer rows with an active row of the same name and county. The ask layer is owed a /fix-rubric pass before delivery; the leak repair stands.

- 2026-11-02, ask rework: Ask A's shared header meters (the same readings and gallons on both wells' lines, the
  register listing both facilities on the meter) were executed by the careful solver's near-duplicate and
  each-meter-once battery; replaced by wellhouse meters that also carry a second well's water, found only by the pumps
  (Skogen's header kept as a hazard).
- 2026-11-02, ask rework: Ask B's renumbered buyers (the old id inactive beside an active twin of the same name and
  county) were re-keyed by the careful solver's name and county join; cut, with every people device screened as code:
  a consecutive system on an emergency tie with no source (an anti-join of the register against the inventory finds
  it), a stale full purchase whose buyer's own well came on (one county only can carry it, the inventory being the
  call's and frozen, and a label check finds it), an emergency tie carrying a buyer's whole supply (2025 flows against
  the 1 September 2026 register, a fork), a reseller's population holding its buyers' (against the plan's filed
  counting rule, a fork), a buyer across two counties (an allocation, a fork), a buyer renumbered under a new name
  (one system under two keys, the batch's closed re-keyed family).
- 2026-11-02, ask rework, new ask-only records screened and dropped: sanitary-survey deficiencies (a system-wide
  finding on every facility row is read off its element's plain meaning), wholesale bills in hundred cubic feet beside
  thousand gallons (a contract-rate second explanation, and the unit family another build in this batch carries),
  SCADA run hours for months a meter was out (the reconstruction forks at the rounding, and the blank volumes are an
  anti-join), the 2023 federal survey's sample points placed by their PFAS profile (only 8 of 24 entry points move),
  a PFAS mass inventory (it reads the call's construction), the 2026 design grants' amendments (the latest-version
  rule executes them), PFAS monitoring violations (the results, a call file, yield them).
- 2026-11-02, judge pass 4 on the ask rework (2c87c47f): the main call forced, the water ask SEND_BACK on one rival: the pump evidence showed the second well inside its host's line only in the 21 months it leads, so netting only those months (1.0 to 6.5 million gallons off in every cell) was as defensible as the golden's every month. Closed in the operations, no call file touched: the four piped wells run only as their month's lead (valved out of the rotation otherwise; the samplers' one sighting at Lindvik Lake in January kept as a half-hour run), so the evidence and the effect coincide and both readings file the golden (asserted). Filing which meters carry another well's water was rejected: it names the device. ceiling.py on 7a18885f: the cracker 0 of 16, pair 31.0.
