# task471 design note: the 2027 Well Water Assistance counties on the private-well nitrate survey

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task471.json`, architecture v3, registered 2026-10-20 after a pull, brought
  to the built world the same day (nitrate, the permit and parcel lists, three laboratories).
  - Lineage: architecture 1 (Kessick Valley's route pitch, spent at Gate F) and architecture 2 (the program reviews on
    the 2026 licensure test form, spent at Gate G).
  - Guard: WARN only.
    - government_agency is the organisation in 36 builds: the state health department runs the private well program.
    - ETL in 6 of the last 12: the lane's objective.
    - Gate G method_or_model_selection repeats task477 and runs in 9 of 12: how two separately sampled, overlapping
      lists combine into one estimate is an estimator chosen on honest data.
    - Deliverable formats png and xlsx repeat task250, and question form "which" repeats: the decision picks counties,
      and a workbook with a chart is what the program's analyst sends.
  - Differentiation lines against task264 v2 (members weighted by event count within one sample of events) and task131
    v1 (interference between sibling sub-units).
  - Personas from `guard.py names --geo us --seed 471`: Tina Hurley (program manager), Steven Nguyen (environmental
    epidemiologist), Carlos Phillips (assistance coordinator). Donald Lara (v1) and Wanda Reed (v2) are not reused.
- **Pairing:** General Statistics & Data Science / data-integration-record-linkage-entity-resolution / ETL.
  - The integration: the program links two incomplete, overlapping lists of private wells into one survey population,
    conforms three laboratories' results and combines two separately drawn testing samples into one county estimate.
  - The deciding quantity: each county's total of wells above the nitrate standard over the union of the lists, a
    dual-frame estimate, the task type's own statistical object (data integration of overlapping sources).
- **World:** an unnamed U.S. state's Department of Health, its Office of Environmental Public Health and the Private
  Well Program, sixteen counties in three assessor layouts, three contract laboratories (Halvorsen Analytical,
  Cedarline Environmental Laboratories, Kinsale Water Testing).
  - The two lists: the well construction permit database (active domestic wells drilled under permit since 1986) and
    the county assessors' 2025 rolls (residential parcels recorded as served by a private well). They overlap: a
    permitted well on a parcel the roll records as on a private well is on both.
  - The survey: each list sampled separately per county with its own target of completed first tests (about 8 per
    cent of the permit list, about 4 per cent of the parcel list), declines replaced from the same list, a household
    drawn from the parcel list after its test from the permit list counted toward both targets.
- **Decision:** which counties qualify for the 2027 Well Water Assistance allocation: an estimated 250 or more wells
  in the county's survey population above 10 mg/L nitrate as nitrogen (WWA-2027-01 section 3.1).
- **Shape:** 10, a scorecard: each of 16 counties against the 250-well line, with each county's wells on the lists and
  its retests. Criteria: the call and its count (2), 16 verdicts, 16 wells-on-the-lists counts, 32 retest figures, the
  chart's parts (about 4) and the two files: about 72.
- **Strategy:** population_selection (`own:dual-frame-weights-for-wells-on-both-lists`), Gate G
  method_or_model_selection, calibration form none, context artifact register.
- **Sources:** the client's survey-design cards (unequal inclusion under a stated design) teach that the weights come
  from the design, not the sample; this build differs in that the design has two overlapping frames, so the weight of
  a well depends on a list it was not drawn from, which only the linkage shows. task452 (design weights after
  reclassification) and task264 (weights by event count) spend single-frame weighting; none spends overlapping frames.
- **Data-native sentence:** the permit list and the parcel list were each sampled at their own rate, a well on both
  could have been drawn from either, and the parcel-only wells (older and shallower, mostly pre-1986) run higher in
  nitrate than permitted wells, so the tested wells are not a sample of the union: pooling them understates the
  parcel-only wells, and weighting each by the list it came from counts the shared wells twice.

## Default path

1. Build each county's permit list (active domestic permits drilled 1986 to August 31, 2025) and parcel list (parcels
   coded private well), link them by parcel number or address, and count the wells on either list (42,598).
2. Conform the three laboratories' first tests to nitrate as nitrogen (Kinsale's NO3 divided by 4.427, the later
   report of a reanalysed sample standing) and join them to the draw manifest's tested kits (3,996 wells, 313 above).
3. Take each county's share of tested wells above 10 mg/L and multiply it by the county's wells on the lists.
4. Keep the counties at 250 or more.

- **Ends on:** three counties (Alderwick, Glenmoor and Netherby)
- **Golden:** six counties (Alderwick, Brannock, Farrowdale, Glenmoor, Lindmark and Netherby)

## Stump sentence

Scaling each county's share of tested wells above the standard to its wells on the two lists files three counties
(Alderwick, Glenmoor and Netherby), because the parcel list was sampled at about half the permit list's rate (4.0
against 8.3 per cent) and its parcel-only wells run higher in nitrate, so the pooled share leaves out Brannock,
Farrowdale and Lindmark; the analyst who notices the two rates and weights each tested well by the rate of the list it
was drawn from files ten, counting the 3,002 tested wells on both lists about twice.

## Three rules

- **Task type:** data-integration-record-linkage-entity-resolution in General Statistics & Data Science, which serves
  Data Extraction & Conformation: two incomplete, overlapping lists linked into one population and two samples
  combined into one estimate.
- **Domain test:** each county's total of wells above the standard over the union of two overlapping frames, estimated
  the way the field estimates a total from a dual-frame survey (Hartley 1962; Kalton and Anderson 1986), each tested
  unit weighted by one over its probability of selection from either frame, which the linkage supplies.
- **Swap:** "which clinics qualify on an estimated 250 patients above the line" read with one sample still reads, but
  the swap of the method is what breaks: replacing the dual-frame estimate with a generic summary (the tested share
  times the population, or one frame's estimate) moves the six to three or ten, so the statistical object decides.
- **Layer 1:** the permit database's other wells and dates (non-domestic, replaced, abandoned, drilled after the frame
  date), three assessor layouts with four parcel-number formats and their own water codes, addresses written
  differently on permits and rolls, three laboratories' layouts with Kinsale in NO3 and reanalyses under status,
  report date or version, replacement draws in the manifest, all produced by the systems that hold them; nothing
  placed to be caught.
- **Layer 2:** estimation_fit: the inclusion probability of a well on two separately sampled, overlapping lists,
  1 - (1 - f permit)(1 - f parcel), against the pooled share or the drawn list's rate.
- **Decisive step:** weight each tested well by one over its chance of selection from either list, which needs each
  tested well's membership in the list it was not drawn from (the linkage) and both lists' sampling fractions.
- **Not semantics:** every field, code, unit and definition read correctly (the lists, the linkage, the TESTED_EARLIER
  rows, nitrate as nitrogen, the standard) still leaves the pooled share at three counties and the drawn list's rate at
  ten: nothing in the records means anything other than what it says.
- **Not rule application:** no filed rule or procedure says how the survey's estimate is computed; the design report
  describes the draws and WWA-2027-01 files the estimand (the whole survey population, tested or not), so executing
  every stated rule still leaves the estimator to choose, and the easy choices file three or ten.
- **Analyst test:** a strong analyst who links the lists, conforms the laboratories and reads every rule correctly, then
  scales each county's tested share above the standard to its wells on the lists, files three counties (Alderwick,
  Glenmoor and Netherby); asserted in `checks.py` on the generator's clean truth, where the same route also files the
  three and the decisive step alone gives the six.
- **Estimand:** WWA-2027-01 3.1 and 2.2 with the design report section 2: the number of private domestic wells in
  each county on the permit list or the parcel list as they stood on August 31, 2025 (the whole survey population,
  tested or not) above 10 mg/L nitrate as nitrogen at a first test, against 250, the unit a well.
- **No decoy:** no memo, draft, briefing, published share or stakeholder figure states a county estimate, a pooled
  share or a weighting; the design report gives the lists' sizes, the targets and the letters' outcomes, all true,
  and nothing in the pack argues for any estimator.
- **No certified replay:** no certified or published county figure exists to reproduce; the method is the field's
  standard dual-frame estimator, recovered from the design, not from replaying a figure.
- **Lesson:** a sample drawn from two overlapping lists is not a sample of their union: each unit's weight comes from
  every list it is on, so the linkage that builds the population also builds the weights; no build on file teaches
  overlapping frames (task452 and task264 weight within one frame).

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 (default path), the tested share above times the wells on the lists (Alderwick, Glenmoor, Netherby) | none: 3.1 files the estimand, not a pooled share | the manifest and the results: fires | the natural expansion of a sample share: fires | none | none | one ratio: fires | readable |
| R1, each tested well at the rate of the list it was drawn from, or the two lists' estimates added (ten counties) | Table 2's targets and list sizes give two rates: fires | the manifest's FRAME column: fires | reweighting to the design: fires | none | none | one division per list: fires | readable |
| S, one list alone (permit list: Alderwick, Glenmoor, Netherby; parcel list: five) | 2.2 files either list: rules it out | the FRAME column: fires | none | none | none | one division: fires | readable |
| G (decisive), each tested well over its chance of selection from either list (six) | no clause names a weight, a probability or an estimator; the design report says only how the draws ran | membership in the other list is in no column: it comes from linking the drawn record to the other list | the reweighting reflex stops at the drawn list's rate | none | none | none: a probability over two independent draws for the wells on both | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "above the standard" | more than 10 mg/L nitrate as nitrogen | 10 or more | same call (no result printed at 10.00 or 44.27 NO3) | same call; WWA-2027-01 2.1 "more than 10 mg/L nitrate as nitrogen" |
| SF2 | the survey population's date | the lists as they stood on August 31, 2025 | the extract as delivered (permits drilled to July 2026) | same call | same call; design report 2 "as they stood on August 31, 2025" |
| SF3 | a reanalysed sample | the later report | the earlier report | same call | same call; design report 4 "its later report replaces the earlier one" |
| SF4 | Kinsale's nitrate | NO3 divided by 4.427 | read as nitrogen | Dunmere, Kestrel Plains and Rushbrook join | design report 4 "10 mg/L nitrate as nitrogen is 44.27 mg/L nitrate as NO3" and Kinsale's UNITS column |
| SF5 | "250 or more" | the estimate at or above 250 | above 250 | same call (no estimate within a well of 250) | same call |
| SF6 | the linkage | parcel number, else site address to situs address | parcel number alone; address alone | address alone: same call; parcel number alone: Dunmere joins | design report 2, "when the permit's parcel number is the parcel's or, on a permit that carries no parcel number, when the permit's site address is the parcel's situs address" |
| SF7 | the estimate's population | the whole survey population, tested or not | the tested wells above, counted | no county qualifies | WWA-2027-01 3.1 "the wells the Survey did not test as well as those it did" |
| SF8 | a well tested earlier from the permit list | counts toward the parcel list's target as well | the permit list's only | same call | same call; design report 3 "counts toward the parcel list's target as well" |
| SF9 | a blank water code | not on the parcel list | on it | not a reading: the Codes sheet says not recorded | the parcel compilation's Codes sheet, "Blank: not recorded"; design report 2, "records as served by a private well" |
| SF10 | the estimate's rounding | the verdict on the unrounded estimate | rounded to whole wells first | same call (no estimate within half a well of 250) | same call |
| SF11 | a well's county | the county of its permit, parcel and draw | the county on a retest request | the call reads no request | same call (main call); the ask's own reading is in the Ask sheet |
| SF12 | Kinsale's conversion factor | the design report's 4.427 (44.27 mg/L as NO3) | the fact sheet's 4.4 (44 mg/L) | same call (no Kinsale result between 43.9 and 44.4 mg/L NO3) | same call; design report 4 gives 4.427 for the survey |

## Ladder

Built figures, read from the cut pack by `generator/checks.py` (estimated wells above 10 mg/L nitrate as nitrogen in
each county's survey population, against 250).

- **R0, the default path: the tested share above times the wells on the lists (Alderwick 367, Glenmoor 567, Netherby
  542).** Brannock 205, Farrowdale 187 and Lindmark 193 fall short. Dies to Table 2 and the manifest: the parcel list
  was sampled at 4.0 per cent against 8.3, and the tested parcel-drawn wells run higher in nitrate.
- **R1, each tested well at the rate of the list it was drawn from (ten: the six and Dunmere 355, Ivyridge 361, Kestrel
  Plains 315, Rushbrook 319); the two lists' estimates added gives the same ten.** Dies to the linkage: 3,002 of the
  3,996 tested wells are on both lists and could have been drawn from either, and the TESTED_EARLIER rows show it.
- **S, one list alone (permit list: Alderwick, Glenmoor, Netherby; parcel list: Brannock, Farrowdale, Glenmoor,
  Lindmark, Netherby).** Dies to WWA-2027-01 2.2: the population is either list. Alderwick's permit-only wells run high
  (its parcel list alone gives 79), so neither single list lands the six.
- **G, the decisive move: one over each tested well's chance of selection from either list (Alderwick 408, Brannock
  304, Farrowdale 311, Glenmoor 720, Lindmark 317, Netherby 588).** Hartley's estimator at every split of the wells on
  both lists (0, 0.25, 0.5, 0.75, 1), the sum-of-rates approximation and the estimate post-stratified by list
  membership name the same six (C1, asserted); the generator's truth (every well's nitrate) gives the same six.
- **Margins (cut pack):** every qualifier at 1.17 times the line or more on every design-based estimator (Brannock at
  293 lowest), every other county at 0.87 or less (Ivyridge at 218 highest); R0 drops three counties at 0.75 to 0.82 of
  the line, R1 adds four at 1.26 to 1.44.
- **Position, separation and dominance:** a designation, not a ranking: R0 names three, R1 ten, the single lists three
  and five, the golden six; no wrong route names the six (asserted), and the call's two directions of error come from
  different rungs (pooling drops three, the drawn list's rate adds four).
- **Grid:** the Layer 1 slips each land elsewhere: Kinsale read as nitrogen adds Dunmere, Kestrel Plains and
  Rushbrook; linkage by parcel number alone adds Dunmere; the earlier reports, the extract's later permits and the
  TESTED_EARLIER reading leave the six (SF rows).
- **Worth:** the call and the grid of 16 verdicts and 16 wells-on-the-lists counts; R0 keeps every count and 13 of 16
  verdicts, so the ask carries the pair (Ask sheet).

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | wells on either list on August 31, 2025, tested or not | filed: design report 2, WWA-2027-01 2.2 and 3.1; SF2, SF7 |
| 2 | Unit of account | the well (a well on both lists once) | filed: "wells"; the linkage rule makes a permit and a parcel one well |
| 3 | Attribution window | first tests closed April 30, 2026 | every first test in the manifest is inside it (C1) |
| 4 | As-of dating | the lists at August 31, 2025; results as reported | filed; SF2 same call |
| 5 | Version basis | the later report of a reanalysed sample | filed: design report 4; SF3 same call |
| 6 | Denominator | each list's sampling fraction, target over list size | Table 2 gives both; the manifest's counts equal the targets (asserted) |
| 7 | Weighting | one over the chance of selection from either list | forced by the design (C1 across Kalton-Anderson, Hartley at five splits, post-stratified) |
| 8 | Window length | not applicable: one survey, one first test per well | C1 |
| 9 | Boundary inclusivity | more than 10 mg/L; 250 or more | filed (2.1, 3.1); nothing on either edge (SF1, SF5) |
| 10 | Rounding path | the verdict on the unrounded estimate; counts whole | no estimate within half a well of 250 (SF10); counts are integers |
| 11 | Tie-break | not applicable: no county within 30 wells of the line | C1 |
| 12 | Maturity and censoring | every first test reported before the as-of date | C1: every tested kit has a final result |
| 13 | Order of operations | link, then weight, then sum | one order; asserted in checks |
| 14 | Row order | file order changes nothing | C1: results keyed by kit, latest report by date or version |
| 15 | Duplicate resolution | a reanalysis replaced by its later report; a well drawn twice tested once | filed (design report 3 and 4) |
| 16 | Identity normalisation | parcel numbers to nine digits; addresses to house number and street name | C1: address alone links the same wells (SF6); each county's (number, street) is unique |
| 17 | Netting against gross | not applicable | none |
| 18 | Dimensional units | nitrate as nitrogen; Kinsale's NO3 divided by 4.427 | filed (design report 4); SF4 |
| 19 | Code and status semantics | WELL_USE, WELL_STATUS, water codes, OUTCOME, RESULT_STATUS | dictionary: the design report and the Codes sheet; never the stump |
| 20 | Integerisation | counts are whole wells; the estimate is not rounded before the verdict | C1 |
| 21 | Clause scope | 3.1 for the county call, 4.2 for the retests | filed scope |
| 22 | Forward window contents | the 2027 allocation reads the survey's estimate; nothing forward to forecast | filed (3.1): the call is the standard's designation for 2027 on the survey closed in 2026 |

## Literal reader

Executed word for word, WWA-2027-01 3.1 asks for the survey's estimate of wells above the standard over the whole
survey population, which the design report defines as the two lists on August 31, 2025 and the linkage as one well;
nothing names an estimator, so every literal reader must choose one, and every design-based estimator that uses the
two lists' fractions and each tested well's membership (Kalton-Anderson, Hartley at any split, post-stratified) gives
the six (C1, asserted); the pooled share and the drawn list's rate are easy methods on the same literal estimand, not
other readings; every SF row is same call or ruled out by a quoted sentence.

## Oracles

None. No control, published figure, reconciliation column or corpus ranks the counties or states an estimate: Table
2 gives the lists, targets and letters (true under every method), Table 3 the letters' outcomes, and the fact sheet
and the laboratory roster carry no county figure.

## Ask sheet

- **Ask A, each county's wells first tested above the standard and retested by June 30, 2026, and how many of those
  retests were still above it: 32 figures.** H18 home: WWA-2027-01 4.1 and 4.2, the households a qualifying county's
  assistance reaches (above on a first test and on a retest collected by June 30), a measure every county carries
  that the call does not turn on. Path: the retest kit requests (CHANNEL, ORIGINAL_KIT, SHIP_TO_ADDRESS, SHIP_TO_CITY,
  COUNTY_CODE, RETEST_KIT), the draw manifest (KIT_ID, FRAME, FRAME_RECORD), the permit extract (PERMIT_NO,
  SITE_ADDRESS), the parcel compilation (situs addresses), the three laboratories' results (kit, collection date,
  nitrate, status, report date, version, units), the standard (4.2): eight files, fourteen columns.
  Primary device: D7 with D9, the true key elsewhere and a control true only in its scope. The kit vendor routes a
  portal request to a county by the ZIP code the household types, and in most counties one of the two smaller towns
  has a ZIP code whose post office sits over the line, so that town's portal requests carry the neighbour's
  COUNTY_CODE and their retests go to the neighbour's laboratory under the neighbour's code. Counted in the county on
  the request, which both the request and the laboratory row agree on, every county's two figures move (asserted, 32
  of 32); counted in the county the survey tested the well in, through the first kit the request names, they are the
  golden. No sweep sees it: every request has a county, every first kit resolves, nothing repeats, and the statewide
  totals are the same under both.
  Hazards: phone requests carry no first kit and link only by ship-to address in the request's county (dropping them
  moves every county); retests collected after June 30 (requested before it); requests from households outside the
  survey and retests of wells first tested at or below the standard; Kinsale's NO3; reanalysed retests.
  Stops (asserted, `checks.py` and `generator/ceiling.py`): the request's county misses all 32; portal requests only
  misses all 32; no window keeps 2; no first-test filter keeps 16 (it moves the counties with below-standard
  requests); the golden reproduces the generator's truth exactly.
- **The construction layer:** the six counties, the 16 verdicts, the 16 counts of wells on the lists and the chart; the
  cracker has them.
- **Main population zero-counts (asserted):** the call reads no request and no retest result; no retest kit is a
  first-test kit; the routing touches no first test.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| A, each county's retested wells and retests still above | every request matched to its well (first kit, or the phone request's address), the window and the first-test filter applied, counted in the county the request and the laboratory both give; every county's two figures fall outside their bins | miss |

- Pair ceiling: 38.9 on the cut pack (weights 38 / 7 / 55; the cracker keeps the main block and instructions, 45.0,
  and none of the 32 ask figures; the mirror, R0, keeps every county's wells on the lists and 13 of 16 verdicts, and
  none of the ask figures on its own path, 32.8).
- Mirror leakage: 0.0 per cent of ask weight.
- Measured by: generator/ceiling.py

## Tried and rejected

- 2026-10-18, at the draw: the seed's own moves, a round-trip itinerary fare read as a one-way fare and the New York
  airports left as three markets: data semantics and a market definition (the estimand's unit), so neither may decide;
  kept as Layer 1 and as ask devices.
- 2026-10-18, at the draw: a windshield census (cards put on every car parked in the lots at sweep times), whose cards
  over-represent long stays in proportion to their length: population_selection, banned against task245 at the draw,
  and the label is not moved to pass the guard; replaced by the entry-plaza handout, a different mechanism (replies
  censored by the collection close, which thins the long stays instead of inflating them).
- 2026-10-18, at the draw: the fare premium over a log-log fare-distance benchmark, decided by retransformation bias:
  generic econometrics, and a clinic's charges against a severity curve read the same (swap test fails).
- 2026-10-18, at the draw: the three markets with the highest premium in thin ticket-sample cells, decided by
  shrinkage (the winner's curse): the shrinkage method is not forced by anything filed, a coin flip for determinism.
- 2026-10-18, at the draw: leakage read from an agency ticket dataset whose capture depends on the sales channel,
  measured where the ticket sample sees everything: the same lesson as task448 and task470 (capture by unit measured
  on the overlap).
- 2026-10-18, at the draw: a departure-lounge survey with a fixed quota of interviews per flight (unequal inclusion):
  a ratio within each destination sidesteps it, and by house precedent (task452) a design-weight stump is
  population_selection, banned at the draw.
- 2026-10-18, at the draw: capacity-censored (spilled) demand on full flights to the hubs: the demand turned away is
  model-dependent and every demand model is a fork.
- 2026-10-18, at the draw: the share of one-way tickets that are residents' trips (a one-way ticket's origin is not
  its traveller's home): turns on reading what the ticket origin field means, data semantics.
- 2026-10-18, at the draw: business travel by market from the fare-class proxy corrected for its false positives
  (Rogan-Gladen): the lesson task456 teaches (an imperfect record's false positives subtracted, not only its misses).
- 2026-10-18, at the build: the party verbatim beside the coded party in the cards file, with a filed rule sending the
  analyst to the verbatim for parties of nine or more: the rule pointed every careful solver at the verbatim column,
  where the sums sit in plain view; the verbatims moved to their own file and the cap dropped.
- 2026-10-18, at the build: home ZIPs keyed with a plus-four on 16 per cent of cards: matched as keyed they moved every
  trips figure out of its hundred, so a Layer 1 item carried figure difficulty; cut to a realistic 0.3 per cent and
  asserted neutral, with the two-county ZIP made a small rural office and the repeated batch chosen so its second copy
  moves no figure out of its hundred.
- 2026-10-18, at the build: passengers on the default path's weights ranked Washington, Phoenix and Tampa, the golden's
  three, so ranking on passengers was a shortcut to the call; the winter markets' parties cut to couples and singles
  (1.65 to 1.75) and Myrtle Beach's summer family trips raised to 3,000, so passengers on any weighting carry Myrtle
  Beach.
- 2026-10-18, at the build: the first realisation (seed 471) put New York within 1.12 of the third market once the party
  draw moved onto each card; New York and Dallas set lower in the world and a seed search run over 60 worlds; seed 504.
- 2026-10-18, at stage 4: seed 504's world, where New York led Dallas for the first market left out by 2 per cent and
  a reweighting or a dropped batch could swap them (reader round 1); the handout coverage reworked plaza by plaza and
  day by day with lot choice independent of the stay, and a 120-world search run with the fourth against the fifth at
  1.07 or more; one world passed, seed 512.
- 2026-10-18, at stage 4: the passengers device cut one way (a sum written on the card coded as its first number):
  reader round 2 read Q4 in the verbatims against `party` and recoded every party, the sums added.
- 2026-10-18, at stage 4: the same device cut both ways (the parties written with who they cover coded right, so adding
  every number written counts them twice): reader round 3 recoded every party right. Both cuts are mirror devices: the
  verbatims are documented beside the coded column (methods report 4.2), so reconciling them is the cracker's reflex,
  and no reading of Q4 the frozen documents leave open is both determinate and missed by a careful parser.
- 2026-10-19, re-root tried on paper: the same parking survey with the third pick held unless its lead over the first
  market left out clears twice its design-based standard error (cards clustered by handout day, weighted by the return
  window). Measured on the v1 pack it cannot bind: 73,909 returned cards put Phoenix, Tampa and Washington each 3.5
  standard errors clear of New York on the weighted card-level variance and 2.3 to 3.4 clustered by day; binding it
  would need a tenfold smaller sample and same-day group travel, a planted structure, and the clustering unit itself
  is arguable when the waves are consecutive days. Dropped before any data was cut.
- 2026-10-20, re-root: architecture 1 (the parking card survey, replies censored by the collection close) spent at
  Gate F, every reader landing the call, with its ask device a mirror device; by the author's rule (no retirement)
  architecture 2 is a fresh world in the least-drawn ETL task type, its decisive step one the record does not display.
- 2026-10-20, at the draw: repeat candidates who saw the anchor items on an earlier attempt, left in the equating
  sample: an anchor-contamination screen beside task450's, and the sample definition has to be filed anyway (a
  convention), which files the step; kept only as the filed sample (first attempts), with no exposure in the data.
- 2026-10-20, at the draw: Tucker against Levine under a large cohort difference (the anchor's reliability): the two
  differ by less than their sampling error at the cut and nothing a pack can carry forces one, a fork.
- 2026-10-20, at the draw: 2025 responses re-scored as a labelled trend sample: the label names the drift check, so
  the organ announces the step; replaced by the contractor's validity papers, which its QC summary reports only as
  agreement rates.
- 2026-10-20, at the draw (prototype 1): an anchor of 15 multiple-choice items and two of the three written
  assignments, heavier in written work than the test: the golden's methods split (Tucker 56 against chained
  equipercentile 57) and missed the generating truth; the anchor made proportional (20 items and one assignment, 44
  per cent written by points, as the test is).
- 2026-10-20, at the draw: filing the program's equating method (Tucker) in the 2025 technical report to close the
  equipercentile spread: its literal execution on the anchor as scored is the default path's cut, an official decoy;
  the method stays unfiled and the world is tuned so that Tucker, Levine and chained linear (each at three synthetic
  weights) and chained equipercentile agree on one cut with margin.
- 2026-10-20, stage 3: WA2's validity papers scored by the 2025 leaders' consensus (an audit set): `heart` blocked
  ban.calibration and ban.artifact against task473 once task249 was marked spent; redrawn as June 2025 responses
  carrying the score both of their 2025 reads gave, the two scoring regimes' overlap on the same responses and the
  operational metric the 2025 anchor scores are on (validity sample drawn on its own stream so the shift sits mid-bin:
  0.98 anchor points, raw 49 with 0.38 and 0.37 of margin, every rung and set unchanged).
- 2026-10-20, stage 4: architecture 2 itself, the rater-severity shift on the anchor's written assignment measured on
  the validity papers and taken out before the link. The judge (v2r1) found it DETERMINISTIC on the main call, but its
  Gate G disposition was SEND_BACK (planted_defect_flip, surface_read_rejection, sole_data_defect yes): on consistent
  scoring the anchor as scored is right and the task collapses, so the stump is catching that the as-scored anchor
  misleads. Gate H passed only as analytical (borderline planted). Both scored readers missed the call on the drop-WA2
  rung and all 32 ask figures, but a measurement bias in recorded values is a defect to catch, not an analysis on
  honest numbers. Spent; architecture 3 is a fresh draw on honest data.
- 2026-10-20, at the architecture 3 draw: a joint replacement registry whose earlier hips were back-loaded on each
  hospital's joining only if still in place, read by delayed entry. task265 already spends exactly that insight, so it
  was dropped before registering.
- 2026-10-20, at the v3 build: the parcel list alone (and the parcel-drawn share scaled to the wells on the lists)
  named the golden six by coincidence, because the parcel-only wells carried nearly every exceedance; Alderwick placed
  as a county whose permit-only wells run high (its parcel list alone gives 79), so no single list lands the six.
- 2026-10-20, at the v3 build: each county's estimate as a graded figure: the design-based estimators that all name
  the six differ by up to 59 wells in one county (Dunmere 164 to 223), so no figure is determinate; the estimate is
  charted and the graded grid is each county's verdict and its wells on the lists.
- 2026-10-20, at the v3 build: the retest ask's routing on one border town per county could not move every county's
  figures (several counties had no border retests); each county's border town drawn from its two smaller towns, and the
  search also kept the portal-only path off every figure, so the mirror keeps none of the 32.
- 2026-10-20, at the v3 build: results printed at 10.00, or Kinsale results between 44.0 and 44.27 mg/L NO3, would
  split the standard's "more than 10" from "10 or more" and the design report's factor from the fact sheet's; every
  result within 0.1 of the standard moved clear of it on its own side (SF1, SF12).
