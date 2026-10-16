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
| SF16 | the mixing proportions | each pumping well's rated capacity over the sum | the entry-point flow shared by capacity; equal shares | same call | asserted: same wells under each |
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
| 4 | As-of dating | the inventory's statuses and capacities as of 1 September 2026, the plan's list as drafted 30 September 2026 | filed |
| 5 | Version basis | the latest report revision of each sample | filed (the guide); SF15 |
| 6 | Denominator | none: a level against a line, then dollars | n/a |
| 7 | Weighting | each sample once; the mixture by the pumping wells' flows | design (the data's structure); SF16 |
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
| 18 | Dimensional units | ng/L in the state's export (the 2023 national survey's micrograms per litre is a distractor); gallons a minute to MGD | filed; SF8 |
| 19 | Code and status semantics | sample types, revision numbers, facility statuses; for the asks, facility types, meters, connection types | the guide and the inventory notes; never the stump |
| 20 | Integerisation | dollars whole; people whole; water to a tenth of a million gallons | prompt |
| 21 | Clause scope | section 6 of the plan governs the call; the operating reports and the register govern the asks | filed |
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
well. For the asks, the meter register ties each shared meter's readings to its wells under every handling, and the
register's population counts each system's own customers only.

## Ask sheet

| Ask | Figures | H18 home | Use | Primary device | Hazards | Path (files, columns) | Stops (lazy delta) | Realism |
|---|---|---|---|---|---|---|---|---|
| A, for each county, how much water the listed systems' wells pumped in 2025, in million gallons to one decimal | 4 | each listed system's 2025 production, a measure every candidate carries that the call does not turn on | the board's view of the water the list's wells deliver | D6: where two wells discharge to one header and share a meter, the operator writes the meter's readings and gallons on both wells' lines (Lindvik Lake, Halvorsen, Skogen, Elvholm Falls, one in each county, and three systems off the list); the meter register lists both facilities on the one meter | H1 (D5): Ackerholt Creek's emergency interconnect, purchased water on its own line in September; H2: Fjelstad's Well 2 meter changed out in June (the readings restart, the gallons are right); H3: Kesselring's emergency well ran three days in July (it is a listed system's well that pumped) | the operating reports (pws_id, report_month, facility_id, meter_start, meter_end, volume_gal), the meter register (meter_id, facility_ids, removed), the inventory (facility_type, status), the plan's Table 6-1 (county); 4 files, 10 columns | every row: over by 136.3 to 322.6 million gallons a county; wells only, each row: the same; active wells only: Hedstrom 912.7 against 913.5 once the meter is right; readings in place of gallons: Granlund 1,135.2 against 1,342.9 | a common discharge meter written on each well's line is what a monthly operating report form produces |
| B, for each county, how many people get their water from the listed systems' wells | 4 | each listed system's reach, a measure every candidate carries that the call does not turn on | the board's view of the people the list's wells serve | D7 and D5: systems that buy all their water from a listed system, and systems that buy from those buyers (Tamsholt to Oakmere, Halvorsen Township to Haldorsen Estates, Hedstrom Rural to Stensrud and Gunderholm, Fjelstad Junction to Lundquist); the register counts each system's own customers, and the chain is only in the connections file | H4: an emergency tie (Solberg Lake to Elvholm Falls) and a purchase that ended on 30 June 2025 (Hagestad Corners from Ackerholt Creek); H5: buyers living in another county than their seller (Arneberg, Gunderholm, Oakmere) | the register (pws_id, county, population_served, primary_source), the wholesale connections (buyer_pws_id, seller_pws_id, connection_type, in_service_to), Table 6-1; 3 files, 8 columns | listed systems only: under by 586 to 3,871 a county; buyers one step out: under by 156 to 611 in every county; every tie followed with no regard to type or end date: Granlund over by 846, Sandholm by 1,271 | consecutive systems buying from a buyer, emergency ties and ended purchases are what a state's system register holds |
| C, the chart | its parts | the construction | the call's own exhibit | none | none | the golden's well levels | R0 to R3 | the analyst's own exhibit |

- **Main population zero-counts.** No ask device or hazard sits in the twenty systems' 2024 and 2025 PFOA and PFOS
  samples, their collection records, their active wells' inventory rows or section 6 of the plan: the call computed
  with the operating reports, meter register, register and connections deleted equals the golden (asserted).
- **Hazard table.** H1 moves Granlund in A; H2 moves Granlund for a path reading meter readings; H3 moves Hedstrom for a path
  keeping active wells only; H4 moves Granlund and Sandholm in B for a path following every tie; H5 moves Hedstrom, Sandholm and
  Engvall for a path placing buyers in their seller's county.
- **Referee.** The register's notes file the counting rule for B (a system's population counts its own customers) and
  the inventory's notes file the facility types for A; no file says which meters are shared on the reports or which
  buyers sell on.

| Ask figures | Cracker's path | Cracker's value | Verdict |
|---|---|---|---|
| A pumpage (4) | the operating reports' gallons for the listed systems' wells, facility types from the inventory, summed by county | over by 136.3 to 322.6 million gallons in every county (the shared meters counted on both wells) | miss |
| B people (4) | the listed systems' populations plus the systems buying from them (full purchase, in service), by the buyer's county | under by 156 to 611 in every county (the buyers of buyers) | miss |

Mirror leakage: 0 per cent of the ask weight: the mirror (R0) takes A and B the cracker's way and misses all 8; it
keeps only the chart's format parts where it draws the chart.
Pair ceiling: 31 (the cracker at about 50 with the call, its components and the chart; the mirror at about 12).

## Tried and rejected

- 2026-10-16, at the draw: censored PFAS results at two reporting limits as the decisive step (Kaplan-Meier or a censored likelihood against substitution): the censoring family is task255's in this lane; censored results stay Layer 1 and converge.
- 2026-10-16, at the draw: a concentration-flow relationship to volume-weight each source's level from a few grab samples (missing at random given pumping): the move (a covariate carrying a quantity to the unsampled population) is task256's; dropped.
- 2026-10-16, at the draw: the seed's blend-down (treating only enough sources for each entry point to meet 4.0 ng/L): it needs the fund's rule to say one thing and the answer another, the official-decoy architecture the 10/10 rules ban.
- 2026-10-16, at the draw: treatment sized on each well's maximum-day pumping against its average: the basis would have to be filed (rule application) or left open (a fork).
- 2026-10-16, at design: a 2025 to 2026 window with a 2027 board date (files dated after the build); the window moved to 2024 and 2025 and the board to 18 November 2026.
- 2026-10-16, at design: asks on the 2026 design grants' payments (a payee changed after a consolidation, a cancelled warrant): the cracker joins payments to draws by voucher and lands; replaced by the shared-meter pumpage and the buyers-of-buyers reach.
- 2026-10-16, at design: a Hazard Index ask on the listed entry points: every device on its rows was executed by a filed rule or caught by the battery; dropped.
