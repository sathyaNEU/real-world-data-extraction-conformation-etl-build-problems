# task137 design note

Architecture 3, drawn and registered 2026-10-26 (wave 2 slot, Forecasting lane, sathya8571), the number's third and last
architecture. Architecture 1 (Kaimai Building Society's maturity campaign booked in agent-hours, banking) was landed on
the portal; architecture 2 (Calderbrook Care's 2027 adverse-drug-event admissions, the care world) lost every decisive
step it held to isolated probes before a pack shipped. Both identities are in the card's lineage and their dead ends in
the last section; nothing of either world is kept. This draw is Calderwick Police's forecast of the first-year
detentions at its new city-centre custody hub.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task137.json`, architecture v3, registered 2026-10-26T05:10:19Z on main
   437a0102, brought to the shipped pack at stage 3 (answer, analyst test, stump, layer 1, spine rows, people).
   `guard.py check` on the card: PASS, with NOTEs only (`test.same_puzzle_older` differentiated against task133 and
   task196, `test.same_driver_older` against task133 and task180, `driver.near` 0.25 against this slot's
   never-registered architecture 3 candidate 2).
2. Pairing: Urban & Regional Science (client domain) / `municipal-service-demand-resource-allocation` / Forecasting &
   Predictive Modeling. The deciding quantity is a public service's demand at a new site, the detentions a custody suite
   books in its first year, forecast from the service's demand model over the site's catchment and used to size the
   site's cells and staff.
3. Niche: Calderwick Police, a metropolitan county force in England (124 wards in five districts, four custody suites:
   Northgate and Eastmoor in Calderwick city, Southfields and Wendle Cross in the county). The Tanner Street custody hub
   opens on 1 April 2027 and takes the six city centre wards from Northgate and Eastmoor; the fit-out contract signed on
   9 December 2026 fixes its cells and detention officer posts from its planning figure for 2027-28, its remand cells
   from the four suites' remand holds and its medical rooms from their initial health assessments.
4. Call and shape: the hub's 2027-28 detentions to the nearest 250 (`quantity_figure`, how-many); shape `other`: the
   call with its two parts and the note's chart, plus two ask grids on the four existing suites' 2025-26 operations
   (remand holds, two figures a suite; initial health assessments, day and night a suite), counted in `## Ask sheet`.
   Criteria: the call, its two parts and BTP's crimes (4), the chart (5 years and the stacked 2027-28 bar), 16 ask
   figures, the two files: 28 or more.
5. Mechanism keys: gap population (the force's arrest records are not everyone its suites book); pattern none,
   generators G12 (the records' silence about BTP's arrests read as nobody there), G5 (the railway is policed by another
   force, whose custody the territorial force provides), G3 (the records count the force's arrests, the suite books every
   detainee from its wards); strategy `population_selection`; Gate G `forecasting`, not `method_or_model_selection`,
   because the graded object is a forward projection whose history is read correctly and the step is the new site's
   intake rather than a choice between fitted models (task305's judges read its origin set as model selection because
   its call was a site pick).
6. Layer 2: `field_method`, pattern `own:custody-demand-counts-every-arresting-agency-not-the-force-records-alone`.
7. Furniture: forum `executive_team` (the chief officer team signs the fit-out contract); forcing event
   `purchase_order_or_contract`; organisation family `local_government` (a territorial force under a locally elected
   commissioner; `government_agency` is spent against task121); role family `capacity_planner` (Custody Services
   Planning); context artifact `filed_model` (the custody demand model note); calibration `existing_book_actuals` (the
   four suites' arrest records against the model). `committee_or_panel` is spent against task121 as well.
8. Spine: the force's arrest records, April 2021 to September 2026 (127,845 rows), one row per arrest by a Calderwick
   officer. The forcing file is data.police.uk's street-level crime for the force area as the community safety
   partnership downloads it (158,906 rows), which carries British Transport Police's crime at the stations; the custody
   fact is note 2 of the custody service's suite allocation notes. The asks read the Criminal Justice Unit's remand files
   and the custody healthcare provider's contact export.
9. Deliverables: `tanner_street_planning_figure_2027-28.xlsx` and `hub_planning_note.docx`.
10. People, from `guard.py names --geo GB --seed 137`: Liam Clayton (programme manager) and Emma Roberts (Custody
    Services Planning), the two people the brief and the note need. Katherine, Rachel, Duncan, Rebecca, Richard, Joseph
    and Amelia repeat older builds' first names. None appears in the prompt.

**Spent mechanisms on the ground** (`guard.py mechanisms --objective forecasting --strategy population_selection`, seven
builds): task22 a declining segment masked by inflations of its own base; task132 a wear curve restarted by
replacements; task136 an intervention enrolling units about to take up anyway; task141 outcomes recorded only for the
units a decision-maker let through; task150 arrivals from outside at a steady count beside transfers from siblings;
task168 capped units completed from slow-season builds; task137 v2 short-stay occupants booked through another
organisation's system. None prices a second agency's caseload booked into the operator's own facility.

**Slot screens.** `guard.py slots` on the driver's words returns task117, task179, task134, task182, task190, task194,
task198 and task229, none an outside agency's intake; on the setting's words (custody, police, detention, station,
arrest) it returns task141 (a county detention centre's bed-days, defendants boarded out), task169 (arrests per day out
of custody under a revocation change), task473 (blood draws under a sheriff's agency number) and task273, none a
suite's intake from another force's arrests.

**Probes before the draw.** The candidate was probed before registration on a six-file pack (`t137_a3/probe7` in the
session scratchpad: the planning brief, the model note, the arrest records, the street-level extract, the allocation and
the LSOA lookup; generator `p7lib.py`, seed 7216), call plus the over-24-hour share, by two isolated Opus probes.
- p137i filed 4,500 (4,515.7). It ran model v2 ward by ward, reproduced the published validation exactly (5,904, 3,093,
  7,883 and 7,435), checked pooled growth, a flat level, the last twelve months and a seasonal Poisson, and wrote that the
  street crime file and the LSOA lookup were not needed: the file includes British Transport Police records, and BTP
  detainees are not in the force arrest file and are not counted. Ask 14.8.
- p137j filed 4,500 (4,516). It ran the same model and six alternatives and wrote that the street file has 1,740 of its
  2,022 BTP crimes in the hub wards around the station, that BTP detainees are not in the force's arrest register, and
  that if BTP books into Tanner Street the hub will see extra detentions not captured here; it left that as a caveat.
  Ask 14.8.
Both saw the outside body and dismissed it, the survivor pattern (task305's out-of-region cardholders, task306's
imports). The golden on that pack was 4,750 (4,779.0); two of two missed. Their realism notes are answered in the
shipped pack: the possible duplicate pair is now the ordinary co-arrest pattern (12.2 per cent of the six wards' arrests
are in incidents of two or more, each a person with their own record, R2c); 2,780 arrests are booked away from their
ward's suite (overflow at 0.6 per cent, plus Eastmoor's 19-day flood closure and Wendle Cross's 88-day cell refit,
realistic and kept); demand moves year to year (3,472, 3,734, 3,615, 3,680 and 3,732 in the six wards, the 2021-22
COVID tail, Kingsway down after its clubs closed, Mill Bank up with its canal-side bars, X1); the arrest records are
keyed by the force's arrest reference, numbered by year; `detention_hhmm` stops at charge, which ask A turns on.

**The Gate B fact.** p137j's own words, "if BTP books into Tanner Street", are the judge's question, so the fact that a
detainee is booked at the suite serving the ward of arrest, whatever force or agency arrested them, is filed as note 2
of the custody service's allocation notes, among six other operating notes (the allocation's start date, a full or
closed suite, terrorism detainees, section 136, children, the unchanged wards), never in the brief's estimand sentence
and never naming the railway force. Single use: the clause is in that note and nowhere else in the pack (asserted X8;
no shipped document names British Transport Police, which appears only as a value of the street-level file's `Reported
by`). Deletion: with note 2 removed nothing says where a railway arrest is booked (a force with no cells could use any
suite, or its own in another city), so the BTP part loses its place at Tanner Street and the golden is no longer forced:
the note is load-bearing once and stated once. Whether it turns the probes' caveat into a landing is the stage 4
reader's and the judge's Gate F question.

**Data-native sentence.** British Transport Police polices Calderwick and Kingsway stations, inside two of the six
wards, and with no cells of its own books the people its officers arrest there into the force suite serving the ward;
their arrests are BTP's, so the force's arrest records, on which the custody demand model is built and validated, hold
none of them, and their only trace in the pack is BTP's recorded crime at the stations in the partnership's
data.police.uk extract, 1.28 per cent of the force area's recorded crime and one crime in fourteen in the six wards.

## Three rules

Task type: municipal-service-demand-resource-allocation (Urban & Regional Science), which serves Forecasting in the taxonomy: a public service's demand at a new site from its demand model over the site's catchment, sized to set the site's cells and staff.
Domain test: The deciding quantity is the hub's first-year detentions worked the way custody planning works a suite's demand, every detainee the suite books counted by the agency that arrested them and carried forward from the catchment's record; the hub's catchment holds two railway stations policed by British Transport Police, which has no cells of its own and books its arrests into the territorial force's suite for the ward, so the demand is the force's own arrests by its model (3,754) plus BTP's arrests sized from BTP's recorded crime at the force's own arrests per crime by offence type (281), which moves the planning figure from 3,750 to 4,000.
Swap: "the hub books another police force's arrests at the stations in its wards" put into a hospital's admissions or a utility's megawatt-hours loses its mechanism: no second health service admits patients with no beds of its own and hands them to the nearest hospital by ward, no utility's load is metered by another company that books it into the first's substations, and neither converts another body's recorded incidents into its own intake at an incident type's arrest rate.
Layer 1: the arrest records' UTC clock against UK-time financial years (the custody system's export), arrests booked away from their ward's suite when a suite is full or closed (the Force Control Room's routing, with Eastmoor's flood and Wendle Cross's refit), co-arrests booked minutes apart (one custody record per person), data.police.uk's anonymised map points and LSOAs rather than wards with two reporting forces in one file (the partnership's download), a best-fit LSOA to ward lookup (ONS), arrest offence groups against data.police.uk's crime types with a warrant, recall or breach group that has no crime type (the custody system's offence list), a pull with half of 2026-27 in it; each is what these systems produce, none carries the call, and each is asserted neutral (R2a to R2g).
Layer 2: field_method: the demand model's population is every detainee booked into the suite, so the force's own arrests, modelled and validated on four suites, are completed by BTP's arrests at the hub's two stations, sized from BTP's recorded crime there at the force's own arrests per recorded crime by offence type.
Decisive step: carrying British Transport Police's arrests at Calderwick and Kingsway stations as the second population of the hub's demand, each crime BTP recorded there in 2025-26 at the force's own arrests per recorded crime of its type, rather than taking the force's arrest records as everyone the hub will book.
Not semantics: every field reads as what it is: the arrest records hold the force's officers' arrests, the street-level file names the force that recorded each crime, and the allocation notes say a detainee goes to the ward's suite whoever arrests them; no field, code or definition says that BTP's arrests are missing from the model, that BTP polices the hub's wards or how many it arrests, and the analyst who reads all of it correctly still counts the force's arrests, as both probes did knowing BTP's detainees are not in the force's records.
Not rule application: the model note files the WHAT (a suite's demand is the people arrested in the wards it serves) and the HOW for the force's own records (each ward's latest year carried at its capped three-year change), and no rule says which arrests the records omit or how to size them, so executing every filed rule over the arrest records files 3,750. Measured on the shipped pack: the enumerated own-arrest family (nine constructions: the model with and without its cap, Holt-Winters damped, the latest year, the three- and two-year means, a five-year trend, the last twelve months, the latest year at the force's change) spreads 3,675.7 to 3,833.0, every member printing 3,750; the standing family that carries BTP (twenty constructions: five own-arrest bases by four sizings, per-type rates with and without the warrant share, the force's overall rate and the six wards' overall rate) spreads 3,933.1 to 4,044.5, every member printing 4,000; what rules the frame out is no filed clause but the record, BTP's 1,702 crimes at the two stations in the street-level file read with note 2's routing by ward of arrest, and nothing names it.
Analyst test: A strong analyst who reads every file correctly runs the custody demand model over the six wards' arrest records, reproduces its back-test on the four open suites (0.966 to 1.016), cross-checks Holt-Winters, a trend, the latest year and the last twelve months and files 3,750, where the golden is 4,000; checks.py runs both on the generator's clean truth (R3a, R3b) and on the pack.
Estimand: the detentions the Tanner Street hub will book from 1 April 2027 to 31 March 2028 (the brief and the prompt), a suite's demand being the people arrested in the wards it serves (the model note, 2.1), each detainee booked at the suite serving the ward of arrest whichever force or agency arrests them (the allocation notes, note 2).
No decoy: nothing is planted: the arrest records are the force's own, the street-level file is data.police.uk's, the allocation is the custody service's; no memo, draft or figure argues for a count, no file states a figure for the hub (R3c), and no stakeholder figure is set up to be overturned.
No certified replay: no certified or published figure sits in the pack to be reproduced; the model's validation table is its own back-test on the arrest records, blind to BTP because both of its sides are those records, and the sizing of BTP's arrests is recovered from no figure.
Lesson: a custody suite's demand is every detainee booked into it, while a territorial force's arrest records hold only its own officers' arrests; where another force works inside the catchment with no cells of its own, as the railway police do at a city's stations, its arrests are demand the force's model never sees, and its own recorded crime read at the host force's arrests per crime is what prices it; no build on file prices a second agency's caseload booked into the operator's own facility.

## Default path

1. Read the brief and the allocation: the six city centre wards move to Tanner Street on 1 April 2027.
2. Count each of the six wards' arrests in the force's records by UK-time financial year, converting `arrested_utc`
   (3,732 in 2025-26).
3. Run the custody demand model as filed: each ward's 2025-26 arrests carried two years at its three-year average
   change, capped at 10 per cent a year, summed over the six wards (3,754.4).
4. Re-run the model's validation from 2024-25 and reproduce its table; cross-check Holt-Winters, the latest year, a trend
   and the last twelve months, all in the same printed cell.
5. Read the street-level file as context: BTP's rows are BTP's crimes and its detainees are not in the force's records,
   so they are left out.

Ends on: 3,750 (3,754.4)
Golden: 4,000 (4,035.9)

## Stump sentence

A competent analyst runs the force's validated custody demand model over the six wards' arrest records and files 3,750,
where the golden is 4,000; the step that lands it there is taking the force's arrest records as everyone the hub will
book, when British Transport Police officers policing Calderwick and Kingsway stations, inside the hub's wards, have no
cells of their own and book their detainees into the force suite serving the ward, 281 a year from the 1,702 crimes they
record there, which sit in data.police.uk's street-level file and in none of the force's records.

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 the custody demand model on the six wards' arrest records | yes (model note 2.1 to 2.4) | yes (ward, arrested_utc) | yes | yes (the model's own validation table reproduces) | no | yes | readable |
| 1 another forecast on the same records (Holt-Winters, trend, latest year, means, last twelve months) | no | yes | yes (add a method, back-test it) | yes (the same back-test) | no | yes | readable |
| 2 BTP as a share of the street-level file, scaled onto the model | no | yes (`Reported by`) | yes (a visible second reporter) | no | no | yes | readable |
| 3 (decisive) BTP's arrests at the hub's two stations as a second population, sized from BTP's crimes there at the force's own arrests per crime of each type | no (note 2 states only where any detainee is booked; no sentence names BTP, the stations or a missing population) | no (no column holds BTP's arrests; BTP is a value of `Reported by` in a file the model never reads) | no (the opponent's reflexes are validate, add methods, back-test; the back-test cannot see BTP because both of its sides are the force's records) | no | no | no (a second population placed by ward and priced by type, not a column of the frame) | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the detentions the hub will book | every person booked into Tanner Street from 1 April 2027 to 31 March 2028, whoever arrested them | only the arrests in the force's records | 3,750, the easy route on the same estimand rather than a second reading of it | the brief's sentence (the detentions the hub will book) with allocation note 2 (a detainee goes to the ward's suite whichever force or agency arrests them) |
| SF2 | 2027-28 | 1 April 2027 to 31 March 2028, the base year 2025-26 carried two years | the base carried one year (3,741.0) | same call (asserted SF2, SF5) | the brief's dates; same call |
| SF3 | the hub's wards | the six wards the allocation moves to Tanner Street | Northgate's and Eastmoor's whole catchments | another population | the allocation's `suite_from_1_april_2027` column |
| SF4 | an arrest's financial year | the UK date of arrest (model 2.2) | the UTC date in the records (3,755.2) | same call (asserted) | model 2.2; same call |
| SF5 | carried forward | two years from 2025-26 | one year | same call (asserted) | same call |
| SF6 | the cap | 10 per cent a year either way | no cap | same call: no hub ward reaches it (asserted L6) | same call |
| SF7 | rounding | the nearest 250 | nearest 100 or 50 | another print | the prompt and the brief |
| SF8 | BTP's year | the street-level file's April 2025 to March 2026 | another span | none in the file | the file's months (asserted) |
| SF9 | the stations in the hub | Calderwick station in Abbey Fields and Kingsway station in Kingsway, placed by the LSOA lookup | placed by map point or station name | same call | the lookup (asserted) |
| SF10 | arrests per recorded crime | the force's 2025-26 arrests per its own recorded crime of each type, with its warrant share | without warrants (267.4), the force's overall rate (257.4), the six wards' rate (290.0) | same call: 3,933.1 to 4,044.5 across five bases by four sizings (asserted) | same call |
| SF11 | BTP's crime that comes to the hub | the two stations in the six wards | every BTP crime in the force area at the overall rate (4,061.0) | same print | allocation note 2: the county stations' detainees go to their own wards' suites |
| SF12 | a detention | one person booked in, the records' one row per arrest | one incident, co-arrests collapsed (3,787.0) | 3,750 | the dictionary's "one row per arrest by a Calderwick Police officer" |
| SF13 | whose arrest rates | the force's whole area | the six wards' arrests per crime | same call (asserted) | same call |
| SF14 | warrant arrests in the model | counted, as the records hold them | left out and grossed back up | same call (asserted) | same call |

## Ladder

| Rung | Route | 2027-28 | Printed (nearest 250) | Distance from the golden's cell (3,875 to 4,125) | Dies to |
|---|---|---|---|---|---|
| 0 | the custody demand model on the six wards' records | 3,754.4 | 3,750 | 120.6 | BTP's arrests at the two stations, booked at the ward's suite (note 2), in no force record |
| 1 | the other own-record methods (nine in all) | 3,675.7 to 3,833.0 | 3,750 | 42.0 at the nearest | the same |
| 2 | the model scaled by BTP's share of the street-level file (1.28 per cent) | 3,802.3 | 3,750 | 72.7 | a share of the area's crime is not the arrests at the hub's two stations |
| 3 | golden family: five own-record bases by four BTP sizings | 3,933.1 to 4,044.5 | 4,000 | inside, 58.1 or more from each edge | |
| over-reach | every BTP crime in the force area at the overall rate | 4,061.0 | 4,000 | inside | the county stations' detainees go to Southfields and Wendle Cross |

Position and margins: the default and every own-record method sit in one cell with 42.0 to spare; the decisive step
moves the figure 281.4 (7.5 per cent of the default) against an honest-family spread of 111.4 on a cell of 250; the
golden sits 89.1 from its nearer edge; the world's own expected 2027-28 detentions (3,912.5, the clean truth) are in the
golden's cell (R3b').

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | everyone booked at Tanner Street in 2027-28 | filed: the brief, model 2.1, allocation note 2 |
| 2 Unit of account | detentions, one person booked in | the question names it; SF12 |
| 3 Attribution window | 1 April 2027 to 31 March 2028 | the brief and the prompt |
| 4 As-of dating | records pulled 6 October 2026; street-level crime to March 2026 | the brief's file notes |
| 5 Version basis | custody demand model version 2.0 | the model note |
| 6 Denominator | the force's recorded crime of each type for the arrest rates | C3: every sizing prints 4,000 (SF10) |
| 7 Weighting | by crime type | C3 (SF10, SF13) |
| 8 Window length | three-year change; one year of BTP crime | model 2.3; the file's year |
| 9 Boundary inclusivity | financial years from 1 April | model 2.2 |
| 10 Rounding path | once, the total to the nearest 250 | the prompt; the golden family in one cell (L2) |
| 11 Tie-break | none | no ranking |
| 12 Maturity and censoring | 2026-27 is half a year in the pull | C1: the model reads full years; the last twelve months print the same (R2e) |
| 13 Order of operations | model then sum; BTP sized then added | C1, additive |
| 14 Row order | none | C1 |
| 15 Duplicate resolution | co-arrests are people | SF12; look-alike co-arrests dropped print the same (R2c) |
| 16 Identity normalisation | LSOA to ward, best fit | the lookup; every row maps (R2f) |
| 17 Netting against gross | none | n/a |
| 18 Dimensional units | counts | n/a |
| 19 Code and status semantics | offence groups against crime types; warrants | dictionary; SF14 |
| 20 Integerisation | the rounding of an expected count | the prompt's rounding |
| 21 Clause scope | note 2 covers every arrest, the allocation's wards | the note's wording |
| 22 Forward window contents | the six wards' arrests and the two stations' BTP arrests in 2027-28 | the model's carry and BTP's 2025-26 crime held level (the golden family spans both choices) |

## Literal reader

Executed word for word, the prompt, the brief, the model note and the allocation notes fix the count (the detentions
Tanner Street books from 1 April 2027 to 31 March 2028, a suite's demand being the people arrested in its wards, each
detainee booked at the suite serving the ward of arrest whoever arrests them, to the nearest 250) and leave the estimate
of each part to the data; every reading of SF2 to SF14 either violates a quoted sentence or files the same call, and the
easy answer (3,750) comes from an easy method on the same literal estimand, the force's own records taken as everyone the
hub will book, not from another reading.

## Oracles

none: no control, published figure or reconciliation column in the pack confirms either the default or the golden. The
model note's validation table is the force's own back-test and reconciles under both answers, because both of its sides
are the force's arrest records; the street-level file carries crimes, not arrests; the distractors (the estates register,
the ward populations, the late-night licences, the bank holidays) carry no detentions.

## Ask sheet

Both asks sit on the four existing suites' 2025-26 operations, a population the call never reads (the call reads the six
wards' arrests by ward and BTP's street-level crime; the asks read the remand files, the healthcare export and the
arrest records' bookings and clocks). H18 home for both: the same fit-out contract the call sizes, its remand cells and
its medical rooms, each turned from the planning figure into rooms with the existing suites' rates.

- **Ask A, remand holds by suite for defendants charged in 2025-26 and kept in custody for court (8 figures: cell hours
  from charge to handover, to the nearest hour, and how many were held more than 24 hours from booking in).** Files:
  `cju_remand_files_2025-03_2026-04.csv` (urn, linked_arrest, custody_suite, charged, first_hearing, court,
  handed_to_escort), `calderwick_police_arrests_2021-04_2026-09.csv` (arrest_ref, custody_suite, arrested_utc,
  booked_in_utc, ward, offence_group, detention_hhmm, outcome), the brief's file notes. Primary (which records are one
  event, from an identity): a file carries the case's arrest reference, which for 104 of the 2025-26 files is the
  case's earlier arrest (a release under investigation or on bail in the same ward and offence group), so the detention
  that ended in the remand is the remanded arrest charged at the file's suite at the file's charge time, found by the
  identity booking plus clock equals charge; joined on the linked arrest, those holds start weeks early and every one
  counts as over 24 hours. Second primary (a paper row covering several ledger lines): 77 co-defendants charged in turn
  after the file's first-named defendant have no file of their own; they are the remanded arrests arrested in the same
  minute, ward and offence group, each on their own charge and booking times and the file's handover. Hazards: UK
  wall-clock remand times against UTC arrest times (the dictionary states both), the detention clock stopping at charge,
  the extract running March 2025 to April 2026, charge year against arrest year. Stops (each a complete pipeline, the
  golden 4,487, 2,811, 7,767, 5,595 hours and 183, 109, 296, 240 held): each file at its linked arrest (4,077, 2,512,
  7,422, 5,298; 179, 104, 289, 237), co-defendants attached at the file's charge time (4,498, 2,817, 7,775, 5,603; 197,
  117, 304, 249), the linked arrest's booking with co-defendants on their own clocks (cell hours right; 197, 117, 304,
  249), the detention clock for the 24 hours (22, 16, 30, 34), the remand times read as UTC (4,642, 2,907, 7,955,
  5,848), every file in the extract (5,427, 3,133, 8,546, 6,847). Realism: a CJU case file is keyed to its
  investigation's arrest and names its first defendant; nothing is planted, and every suite carries both kinds of
  record (asserted A10).
- **Ask B, initial health assessments by suite in 2025-26, begun from 07:00 to 19:00 and at night (8 figures).** Files:
  `custody_healthcare_contacts_2025-26.csv` (contact_ref, episode_ref, suite, clinician, contact_type, started, ended,
  outcome), the arrest records' bookings by suite, the allocation (each ward's suite), the brief's file notes. Primary
  (an inconsistency only a cross-file cut shows): the export's suite is the clinician's team, and two suites closed in
  2025-26 (Eastmoor after a flood, 14 August to 2 September 2025; Wendle Cross for its cell refit, 3 November 2025 to
  30 January 2026) while their teams worked at the suites their wards were booked into, so 889 assessments labelled with
  a closed suite took place at Northgate or Southfields; nothing in the export is odd, and only the arrest records' gap
  in bookings and the closed suite's wards booked at the host place them. Second device (which records are one event):
  an assessment running across the 07:00 or 19:00 handover is closed by the outgoing clinician and finished by the
  incoming one on a new line (291 lines), while a detainee back from the emergency department is assessed again (323
  second assessments): one line a contact over-counts, one assessment an episode under-counts. Stops (the golden 1,178
  and 1,470, 526 and 670, 1,571 and 2,078, 1,115 and 1,515): every line by its suite (1,159 and 1,484, 567 and 737,
  1,226 and 1,684, 1,498 and 2,059), handover lines joined with the suite as labelled (1,146 and 1,426, 558 and 714,
  1,217 and 1,619, 1,469 and 1,974), closures moved with the handover lines kept, one assessment an episode, one
  closure found (each keeps at most four of eight, B7). The closure window is the arrest records' own, from the last
  booking before the gap to the first after it; no assessment of a detainee booked before a closure falls after it and
  no closed suite's line falls between its last booking and its team's move (B3, B4), so reading the detainees already
  in the cells either way selects the same rows (C1).
- Separation: the call recomputes byte for byte with the remand and healthcare files deleted (S1); the asks' device rows
  are remand files and healthcare lines, none of them an arrest row, and the closures move bookings, never wards (S2,
  S3). The main population's zero-counts: no device row in the six wards' arrest counts or the street-level file.
- Reuse: neither primary repeats a device of the last three builds; the closure relabel and the case-keyed file are
  bespoke to custody (screened against 1.1e: no duplicate row, no comment, code or flag names the closures, the
  continuation or the case key).

| Ask | Figures | Cracker (lands the call; UK times converted, charges in 2025-26, files joined to their linked arrests, co-arrested remands without a file attached at the file's times; handover lines merged, suite as labelled) | Verdict |
|---|---|---|---|
| A cell hours, four suites | 4 | co-defendants carried at the file's charge time, not their own | miss |
| A held more than 24 hours, four suites | 4 | the linked arrest's booking for the files keyed to a case's first arrest | miss |
| B begun 07:00 to 19:00, four suites | 4 | the closed suites' teams counted at their own suites | miss |
| B begun at night, four suites | 4 | the same | miss |

Measured on the cut pack: the cracker keeps 0 of 16 ask figures and the mirror (off the call, each file at its linked
arrest, handover lines merged, suites as labelled) 0 of 16. A reader who rebuilds every remand defendant, re-keying the
case-keyed files by charge time and carrying co-defendants on their own clocks, keeps ask A's eight and none of ask B's;
on the call that reader scores 72.5 and off it 39.5, so the build rests on the closures holding ask B and on the call
holding, which the stage 4 reader and the judge measure.

Pair ceiling: 28.5 (cracker 45.0 with 0 of 16 ask figures, mirror 12.0 with 0 of 16, on weights 38, 7 and 55)

Mirror leakage: 0.0 per cent of ask weight

Measured by: generator/pair.py

## Layer 1 inventory

| Mess | System that writes it | File | Natural mishandling | Asserted |
|---|---|---|---|---|
| UTC arrest times against UK financial years | the custody system's export | arrests | financial years by the UTC date | R2a, SF4: 3,755.2, same call |
| bookings away from the ward's suite (overflow, Eastmoor's flood, Wendle Cross's refit) | the Force Control Room's routing | arrests | a suite's demand counted by booking suite | R2b, S3: same call |
| co-arrests booked minutes apart | one custody record per person | arrests | look-alike co-arrests dropped as duplicates | R2c: 229 dropped, same call |
| warrant, recall or breach arrests with no crime type | the custody system's offence list | arrests | warrants left out of BTP's sizing | R2d, SF14: same call |
| half of 2026-27 in the pull | the 6 October 2026 pull | arrests | the partial year read as a year | R2e: the model reads full years |
| two reporting forces, LSOAs not wards, anonymised map points | data.police.uk via the partnership | street-level, lookup | rows the lookup misses dropped | R2f: every row maps |
| remand files in UK time, keyed to the case, one file for co-defendants | the Criminal Justice Unit's system | remand files | ask A only | A1 to A10 |
| contacts by the clinician's team, split assessments, second assessments | the healthcare provider's system | healthcare export | ask B only | B1 to B7 |

## Stage 3 gates

Run 2026-10-26 on the final rebuild (target.zip md5 8b091e27, 12 members, 11,265,244 bytes).

- `precut.py task137`: 51 checks, 0 FAIL, 0 WARN (the prompt gate inside it: `voice-check.py` exit 0, 883 characters).
- `generator/checks.py`: 85 assertions, 0 failed (input gates G1 to G6, the three rules R1a to R3c', ladder L1 to L6,
  SF1 to SF14, separation S1 to S3, ask A A1 to A10, ask B B1 to B7, realism X1 to X11, each distractor's deletion D1,
  figures.json F1).
- `generator/verify.py` (csv, openpyxl, pypdf and python-docx, no generator state, no pandas): every figure reproduces,
  the model note's validation table included.
- Two rebuilds byte-identical to each other and to `target/`; the goldens rebuilt twice byte-identical to `golden/`;
  `build.py --zip` cut twice byte-identical.
- `figures_check.py task137`: 51 figures in blocks 1 to 4, 0 absent.
- `generator/pair.py`: cracker 0 of 16 ask figures, mirror 0 of 16, pair ceiling 28.5, mirror leakage 0.0.
- Realism sweep (X1 to X11) green; `golden-realism` pass done (finding titles, a Notes sheet, a source note, the chart
  labelled with its parts, the cell-hours total that would not foot left out); container audit
  (`scrub_producer_metadata.py`) clean on `target/` and `golden/`; the model note reads the same through pypdf lenient
  and strict, pdftotext and pdfminer (H25).
- House fixes: H1 clean; H2 every design-note figure asserted (X11) or printed by golden.py and pair.py; H9 the brief's
  file notes name every other shipped file (X10); H11 one submission.md and one prompt.txt, architecture 1's three
  determinism reports removed; H18 both asks enter the fit-out contract the call sizes; H20 the prompt names the
  catchment; H21 the city renamed from Harrowdown; H23 every ask reads with "none".
- `leak.py --asof 2026-10-26`: REVIEW, no LEAK. Each line is harmless: "the model" three times in the model note is the
  document's subject; the 109 it finds is inside the validation table's 8,109, not an ask figure; the brief carries the
  call's words because it is the request and states no figure; the stump-paragraph words in the brief and the model
  note (records, arrest, demand, population, booked, service, programme) are the field's own nouns, and neither
  document names the railway force, another agency or a missing population; the two December 2026 dates are GOV.UK's
  published bank holidays.
- `guard.py check task137`: PASS, NOTEs only. `guard.py heart task137`: PASS (nearest 0.05). `guard.py surface
  task137`: no BLOCK; four pairs promoted for adjudication, all history severity on card mechanism axes (task133,
  task180 and task196 differentiated on the card since the draw; task138, drawn 10-12 in the physical sciences with a
  store-balance driver, differentiated at stage 3); Abbey Fields read as a person is a ward.

## Tried and rejected

- The seed's architecture (FC08): the vendor's standard dialling rules withheld from the contract and recovered from its
  acknowledgements, with the callable-number count behind two number-level joins as the decisive unit. Rejected at the
  draw: a rule recovered from settled records is banned as the decisive step, and with the rules filed the callable
  count is rule application; the wash stays as depth on the default path.
- A first card in the seed's world as a bank (`financial_institution`, context artifact `operations_log`): blocked by
  the guard against task128, live beside this build (a Canadian bank's collections centres); the deposit-taker became a
  New Zealand building society and the context artifact the block-order thread.
- The coming list's special as the 2024 three-year special (5.65 per cent onto a 3.00 per cent card): the latest
  campaign's share by term and the share by locked rate within term landed 2 to 3 per cent under the golden, because the
  2026 campaigns' three-year deposits, opened at the 2023 peak, met the same drop. Moved to a 2023 four-year special,
  whose past four-year peers all locked in the 2021 and 2022 lows; every term-based rival now lands 19 to 28 per cent
  short.
- Hours to the nearest 100: with the list's drops on thin past support (0.25, 0.55, 1.50 points) the estimator corridor
  (bands of 0.2 to 0.5 at offsets, logistic, isotonic) spread 110 to 230 hours. The 2027 card was set so the list's
  drops sit on dense past drops (0.45, 1.35, 2.00, 2.30, 2.50), and the block moved to multiples of 250 (SOW 2.2,
  procedure 6.1).
- Hours to the nearest 500: the locked-rate and trend rivals landed all three months, and rounding each month to 500
  stopped the months adding to the block.
- Extract notes that said the certificates in the holdings view were moved to the core and what MIGRATED means: they
  narrated Ask B's overlap; the notes now describe the files' fields only.
- Forum `line_manager_or_team` (the head of deposits signing the block order alone): task136 moved its forum to the same
  key after this card was registered, and `ban.forum` blocked; the Deposits Committee now approves the block.
- Write-up figures rounded coarser than they read: the list's retention-offer share to the nearest 5 per cent (60,
  against 62.1) and its non-reaching dials to the nearest 500 (67,500, against 67,354.8); the judge read both as wrong.
  Now whole per cent and nearest 100 (62, 67,400), with freeze.py allowing the two keys
  (`components.retention_share_pct`, `steps.non_reaching_dials`); the Final Recommendation and Critical Components move
  only by that 60 to 62.
- The judge's wording for the Ask A clause (a deposit counts if any of its maturity proceeds were in a society term
  deposit, its principal the amount in term deposit then): "maturity proceeds" is the transfer extract's narrative and
  points at Ask A's device, and "the amount on term deposit then" reads as the new deposit's whole balance, new money
  included (the whole-principal stop). Filed as: counting a deposit if any of its principal was, and only the part that
  was.
- Round 1 shipped design: weak per the 10/10 audit (COMPLIANT_WEAK), because its decisive step, the share of
  conversations going to the retention offer conditioned on each deposit's drop from its locked rate to the card, was
  the strong model's reflex and the field's textbook model: a logistic of the retention outcome on term with a separate
  locked-rate slope per term booked about 5,496 hours, inside the golden's 5,500 bin, without reading any card; the
  share by locked rate sat one bin under; Ask B's migration batches file announced the overlap and an account-level
  dedup against it cracked the ask; Ask A's clause (a deposit counted if any of its principal was kept, and only that
  part) signalled the partial-move device; and the swap test passed only narrowly (insurance renewals priced off a rate
  card read almost the same). Round 2 keeps the world, the call and the asks' populations and moves the decisive step
  to the class of the money, a reason only deposit repricing behaviour has.
- A market-gap stump for round 2 (each deposit's locked rate against a published market rate for its term and opening
  month, the deposits far above the market leaving): the market table made the premium a visible column and the step
  one join (readability tests 2 and 6); the class is rebuilt from each list's own cohorts instead, with no table naming
  it.
- Other round-2 candidates for the decisive step, dropped at the draw: the term structure of the card alone (still the
  drop, read term by term, the reflex the audit measured); the best card across terms as the rate a deposit is compared
  with (a second reading of the rate it reinvests at, a fork and never a stump); money above the Depositor Compensation
  Scheme's per-depositor cover leaving at maturity (a filed limit executed on a visible principal column, rule
  application read off the schema).
- Round 2's first prototype kept round 1's January to March 2027 card (four years 3.15 per cent, so the special's drop
  was 2.50 points): past special money dominated the 2.50 band, so the share by drop alone booked near the golden, and
  the locked-rate-by-term logit carried the special's deposits at about 0.8. The 2027 card was turned up (four years
  4.00, a drop of 1.65), a band in which past conversations are 89 per cent member money.
- The card's gap reordered to population first: `guard.py check` blocked on `test.same_driver` (population, E,
  forecasting against task124's lineage) and `test.same_puzzle_older`; the gap stays time then population, the honest
  order for a premium that lapses at first maturity.
- January's share of the 2023 four-year special's sales at 0.242: January's hours sat near a rounding edge and the drop
  and term logistic landed January's bin (1,250); the sales by month are now 0.184, 0.408 and 0.408, January's golden
  1,206.9 and that rival's January 1,000.
- Ask B at six figures (each month's maturing principal on and off the list): with Ask B the most obvious device, the
  cracker's pair ceiling rose to 41; cut to four figures (the three months and the quarter's part not on the list),
  39.0.
- Ask A's device as a posting date (D8, maturity proceeds posted on the next business day): the hygiene battery's
  unmatched-join count found it at once; moved to the payments system's settlement account with the matured deposit
  named only in the narrative (D7).
- The write-up's past share for member money (15 per cent, 14.57 unrounded) and all past conversations' share in the
  special's band (35 per cent, 34.55): both within 0.07 of a rounding edge; dropped from figures.json, the write-up, the
  note and the workbook, the band given by class instead (88 and 28 per cent, 0.24 and 0.18 from an edge).
- The note's chart title "Seven in ten hours are conversations, most of them retention offers": under the round-2
  shares January's conversations go to the offer 45 per cent of the time and the retention offer's minutes are under
  half the talk in January and March; retitled to the measured two-thirds (0.665 to 0.693, asserted).
- Band shares as a Critical Component (88 against 28 per cent at drops of 1.50 to 1.75): a corridor member (special
  money pooled, a logistic within each class) never computes them; the component keeps the class's 87 per cent and the
  bands stay in the steps.
- Portal round 1 (2026-10-25): response 1 landed the call exactly, 5,250 agent-hours (1,250, 2,000 and 2,000 by maturity month), so reading each reached holder's retention-offer share by the class of the money (the 2023 four-year special's block at 5.65 per cent against its cohort's 5.15) is a reflex for the portal's model, as the drop was for the audit's; with both the drop and the class spent, the world's deposit behaviour layer has no decisive step left, and the one structural step it still holds (a reached holder's conversation settling the holder's later deposits on the list, so hours follow holders, not deposits) reads the same with a clinic's reminder calls, a backdrop by the swap test.
- Re-root to architecture 2 (2026-10-25): architecture 1 spent on portal round 1 (above); the slot moves to a new
  cell, healthcare-delivery-health-economics / utilization-access-demand-forecasting, with nothing of the seed's world kept.
- Architecture 2 draw, coastal high-water flood days in 2027 from the window's astronomical tide plus skew surge
  (climate-weather-extremes): dead on the slots screen, it is task178's architecture 1, spent at Gate F when a scored
  reader conditioned on the 2027 tide table; the prototype (`tide.py`) had shown 2027's tide-only exceedances 15 to 25
  per cent under 2026's at a semidiurnal port.
- Architecture 2 draw, candidates killed on the lane's dead lists before code: bike-share pairs and pupil yield by
  estate age (task170's ninth cell), event prediction and illness-death states (task171, task174), the disposition
  effect in listings and notification habituation (task177's rate-by-state screens), vacancy chains (too close to
  task166's live junior-on-senior driver), OR-list overruns and clinic slot cascades (task170's replay law).
- Architecture 2 draw, a liability book's back-loaded accident year (`res1.py`, two seeds): the accident-year chain
  ladder missed by -36 to -42 per cent but Bornhuetter-Ferguson and frequency-severity on earned exposure landed within
  5 to 14 per cent: the textbook fallback for an immature year is the golden, so dead.
- Architecture 2 draw, warranty claims on a months-in-service clock a new retail channel delays (`war1.py`, two seeds):
  the shipment-clock default missed by only -2 to -5 per cent; dead on lever.

- Interacting pairs as the decisive step (the registered card's, 2026-10-25, restarted thread): a strong enumerator's own
  pick, so on the enumerable chain. On the generator's world a logistic with the canonical pairs wins out of sample
  (log-likelihood -1,629.7 against -1,741.2 per medicine and -1,641.8 for every two-way pair, 2023 to mid-2025 fitted,
  the next nine months scored), and replayed on the regimens the reviews left it files 191 admissions against the
  golden's 343; the pairs stay as a rung any solver climbs, and the decisive step moves to the stopped medicines'
  restarts.
- The dead thread's restart world with the programme counting as each resident's annual review: the 2027 annual reviews
  then all fall in October to December 2027, and leaving them out filed 9 per cent high, a fork between two readings of
  the procedure; the programme is now additional to the annual review, which continues in its usual month, so an
  implicit stop hazard over every month and explicit 2027 reviews agree within 1 per cent (345.4 against 343.0).
- Start hazards scaled by frailty: the pooled restart clock then sat 3 to 6 per cent under the truth, so a frailty-
  stratified estimator would have crossed a bin; the start and restart hazards are frailty-free and the record's clock
  recovers the truth within 1 per cent.
- Pair partners stopped only where the pair is held, with small main effects for NSAIDs and benzodiazepines: the per-
  medicine model with a pooled start hazard landed within 1 per cent of the golden (two errors of opposite sign); the
  criteria now stop NSAIDs and benzodiazepines in every regular user, their own effects carry most of their harm, and
  that route sits at 329 (4 per cent under).

- The restart clock as the decisive step (the stopped medicines restarted on the record's clock from each earlier
  stop), probed 2026-10-26 on a six-file pack (golden 343.0, nearest 25 = 350; frozen 191 to 220, pooled Markov 295):
  two isolated Opus call-only probes landed it, p137a at 350 (355.4) and p137b at 350 (361.9), each with a monthly
  Poisson rate on the month's medicines and their combinations, frailty and care type, validated on October to December
  2026, every medicine switched month by month with recent stoppers restarting faster and about three in ten stopped at
  an annual review, a leaving hazard and a microsimulation, back-tested on the 2024 and 2025 year-start cohorts within 2
  to 5 per cent. Any transition the record shows as a rate gets measured; dead. Their realism catches carried forward:
  the programme stopped 93 per cent of the NSAIDs and benzodiazepines it reviewed against 31 per cent at annual reviews
  under criteria the schedule called the same; no annual reviews after 26 October 2026; 24 admissions overlapping the
  person's previous stay; discharge dates after the pull.
- The blanket-programme restart curve (the programme's stops restarting like Ferncliffe's 2025 blanket programme rather
  than like selective annual-review stops), prototyped 2026-10-26 before a probe: the pooled clock landed 9 to 17 per cent
  under it and the per-medicine model with the pooled clock within one bin (two errors of opposite sign); set aside
  unprobed for the coordinator's evidence from five probe deaths: every dead step put the decisive attribute on the frame's
  own units, where a thorough modeller joins it and measures it, and the survivors (task305, task306) carry a body the
  frame does not hold; re-registered on the step-down guests.

- The step-down guests as the decisive step (re-registered 2026-10-26, d1f3551d), probed on a six-file pack (probe3):
  Opus probe p137c took the step, filing 500 (502.4) as 407.4 for the long-term residents plus 95.0 for the step-down
  guests (37 drug-event readmissions over 23,576 occupied bed-days, 180 beds at 92.1 per cent occupancy), because Annex A
  split each home's beds into long-term and step-down. No honest rebuild hides them: the golden is determinate only if a
  file states the 2027 step-down beds (an annex, a bed plan, a purchase order or a registration variation), and the
  probe cross-matched every file by NHS number (it found the 81 guests who became long-term residents, none on the
  register); if the trusts' returns carry the guests, they are an unmatched block, and if they do not, the guests' rate
  has no determinate source (an analogue choice is a fork). Dead in this world.
- The households other councils placed in Hartmoor's hotels and hostels as the decisive step (architecture 3's first
  candidate, a borough council's 2027 Part 7 assessments; probe pack probe5, golden 1,400 against the frame's 1,200, never
  registered): Opus probe p137f landed it exactly, 1,400 (1,383) and both asks. The block bookings showed as 655 s208
  notices in Q4 2026 against about 20 a quarter, and normalised addresses linked 151 of the 324 earlier placed households
  to later cases (47 per cent, about 27 per cent within a year), a direct analogue in the same files, carried to the 2027
  window by a Kaplan-Meier curve. Every landing so far had an anomaly that invites a look plus an analogue a join can
  measure; the next candidate keeps the outside body steady and quiet, applies a validated model to a situation the
  record's units never had, ties the body to the quantity by an indirect domain link, and forces its size and rate from
  ordinary data with other uses.
- The serving personnel beside a new urgent treatment centre as the decisive step (architecture 3's second candidate,
  Harrowdown ICB's Wexley UTC, 2027 attendances; probe pack probe6, golden 12,500 against the model's 11,000, never
  registered): Opus probe p137h landed it, 12,500 (12,456.7) and the ask. It ran the model as filed (10,846), then
  calibrated the open centres' other attendances as 0.98 per cent of ICB attendances plus 0.99 times the model's demand
  for the census defence population, a fit that matched all three centres and explained Tolland's higher share by the
  RAF station; it knew the personnel are registered with Defence Medical Services, and it excluded the prison and the
  halls students correctly. Defence was the communal establishment table's largest category, and the open centres
  carried enough of it to calibrate the rate. The next candidate's outside body is small wherever the solver can
  measure it, absent from the open units, concentrated on the new one, and sized from data the model does not use.

- Re-root to architecture 3 (2026-10-26): architecture 2, the care world, is spent on probes (the pairs, the restarts and
  the step-down guests above), so the number moves to urban-regional-science / municipal-service-demand-resource-allocation
  with nothing of Calderbrook kept; architecture 3's first two candidates (above) died at the probe gate before
  registration, and the third, the Tanner Street custody hub (Harrowdown Police's on the probe pack, Calderwick Police's since stage 3), was missed by both probes (`## Draw`).

- Stage 3, ask B as each suite's initial health assessments in each quarter (16 figures): the closures reached only the
  quarters they fell in (six of sixteen cells), so a reader who joined the handover lines and kept the labelled suites
  kept ten; moved to day and night by suite (eight figures), every one of which a closure reaches (B6, B7).
- Stage 3, ask B framed as the custody healthcare tender: a second decision with its own owner (H18); its home is now
  the medical rooms of the same fit-out contract.
- Stage 3, Wendle Cross's refit as the only closure: it reaches two suites; Eastmoor's 19-day flood closure in August
  2025, with its team at Northgate, reaches the other two.
- Stage 3, an overflow booking into Wendle Cross during its refit: the nearest-suite overflow ignored the closure, so
  the arrest records' longest Wendle Cross gap fell inside the refit (22 December to 12 January); a closed suite takes
  no overflow.
- Stage 3, the refit's move at its planned 08:00: assessments of detainees booked before the move but seen after it
  read either way; the move is the minute after the last booking, and Eastmoor's planned closure was set at 14:20 so
  that no assessment of a detainee booked before either closure falls after it (B4, C1).
- Stage 3, co-defendants charged at the first-named defendant's time: the file's charge time served every defendant on
  it, so attaching them at the file's times was right; they are now charged in turn after the first-named defendant.
- Stage 3, every file keyed to its own detention: the co-defendant join was the only reconstruction and the reverse
  unmatched join finds it; 104 of the 2025-26 files now carry the case's earlier arrest, as a remand file does when the
  person was released and arrested again.
- Stage 3, a file matched to its detention by suite and charge time alone: two unrelated Southfields defendants were
  charged at 05:18 on 10 October 2025; the linked arrest is taken first and the charge-time match only where the linked
  arrest is an earlier release.
- Stage 3, the detention clock on UK wall-clock times: a hold across the October clock change came out an hour long;
  the clock is elapsed time in UTC and the remand times are its UK reading.
- Stage 3, remand stream 0 and 1: a cell-hours sum 0.02 hours from its rounding edge and a hold within two minutes of 24
  hours; stream 8 clears both (A4, A5).
- Stage 3, the probe pack's personas (Charlene Dale, Hugh Metcalfe): `guard.py names --geo GB --seed 137` does not give
  them; replaced with Liam Clayton and Emma Roberts from that draw.
- Stage 3, the BTP part as a graded figure to the nearest 10: the four sizings print 260, 270, 280 and 290; the part is
  stated with its method in the write-up and only the call is graded on its print.
- Stage 3, the city and force named Harrowdown (the probe pack's name): it contains Harrow, a real London borough
  with its own school, and is the name of a real Oxfordshire hill (H21); renamed Calderwick, with the estate's postcodes
  moved off the real HD and CV areas to unassigned ones (CK, CL). No figure moved.
- Stage 3, the prompt's question without the catchment: the estimand read only "the detentions the hub will book";
  it now names the six city centre wards the hub takes over, which is model 2.1's population and the domain's
  catchment (H20).
- Architecture 3 spent at stage 4 (2026-10-26, on d1d38e72): the determinism judge returned DETERMINISTIC on every
  committed figure with disposition SEND_BACK. Gate G read the call as a single conceptual flip (stumping family
  surface_read_rejection, surface_read_dependency yes, sole_data_defect yes) and Gate H its decisive step as
  data_semantics: the flip rests on the brief's coverage line ("one row per arrest by a Calderwick Police officer") and
  allocation note 2, and any BTP figure from 121 to 371 rounds to 4,000, so once the note is read nothing analytical can
  go wrong. Both scored readers landed 4,000: reader A (Sonnet) quoted note 2 as the decisive-step sentence (5 of 21 ask
  figures, 23.8 per cent, all five the chart's years; score_reader exit 1), and reader B (Opus, 3,754 plus about 265 BTP)
  wrote that what flips the answer between 3,750 and 4,000 is close to reading a stated rule and a field's definition.
  Neither took an ask figure: both re-keyed the files carrying a case's earlier arrest and missed the co-defendants, and
  both counted the closed suites' teams at their own suites. The probes missed only while the coverage fact was unfiled;
  filing it, which determinism needs, makes it semantics and lands it, so the same fact cannot be both Gate B's pin and
  silent. The judge's other findings, kept for the record and not fixed: pin 19:00 (nine first assessments start
  exactly then), pin the assessment unit and the "where it happened" wording, say defendants are counted from the arrest
  records, and the model PDF's header still reads HARROWDOWN POLICE (an upper-case leftover of the rename); reader B
  also flagged the HDL licence prefix and four arrests at the spring clock change booked before their arrest time (a
  local time in the skipped hour converted as GMT). By build-pipeline an architecture is spent on a SEND_BACK, and the
  retirement rule applies to this third spent architecture unless the author sets another cap; that decision is the
  author's, and no architecture 4 is drawn.
