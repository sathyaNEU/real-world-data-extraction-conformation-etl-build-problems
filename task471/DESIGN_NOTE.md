# task471 design note: the 2027 enrolment campaign's organisers on the census-day adults not on the roll

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first.

## Draw

Architecture 5, drawn 2026-10-20 after architecture 4 (the register over-coverage audit) was spent at Gate F. Card
`.claude/skills/fingerprint/cards/task471.json` (v5), registered 2026-10-20T17:17:37Z; guard check WARN only.

- **Pairing.** Survey Research & Official Statistics / census-register-administrative-data-quality (client domain
  survey-research-official-statistics), objective Data Extraction & Conformation (ETL): the National Statistics Office
  conforms the 2025 Census, its Post-Enumeration Survey, the vital and border statistics and the Electoral Commission's
  roll at census day into the enrolment-gap file the Commission shares its 2027 campaign organisers on.
- **Shape 05, allocation to a fixed total.** 200 organisers shared among the 16 regions in proportion to each
  region's adults not on the roll (estimated adults usually resident on census day less electors on the roll that
  day), largest remainders, at least two each. Criteria: the call and each region's organisers (17), the chart's
  named parts, and two asks per region (32); the regions' adults not on the roll are not graded, because the golden's
  family spreads them over a few thousand while the organisers stay fixed.
- **Decision.** allocation_to_total, answer unit count, question form how-many; forum the Commission
  (committee_or_panel), forcing event the 2027 general election (vote_or_meeting), org family
  research_or_statistics_office, stakeholder the office's manager of population estimates (statistical_office_head).
- **Strategy.** population_selection, decisive generator G8 (reachability against magnitude): the people both counts
  reach are not the people there are; Gate G method_or_model_selection; Layer 2 family field_method, pattern
  own:dual-system-correlation-bias-corrected-by-demographic-analysis-sex-ratios.
- **Data-native sentence.** In a census the people a count misses are not missed at random: men aged 18 to 49 with no
  settled household are missed by the census and by its coverage survey alike, so the survey's recount, which the
  dual-system estimate treats as an independent second count, cannot see them, and only the population that births,
  deaths and border movements fix can; and because the gap the Commission allocates on is a small difference of two
  large counts, the men left out move the organisers between regions.
- **Sources.**
  - Client card census-register/1 (dual-system estimates within post-strata, after erroneous enumerations) is the
    textbook route and this build's default path; the decisive step is the judgment that route takes for granted (the
    census and the survey miss people independently) and the data settle (`stumping` 1.3; the Layer 2 library header).
  - `measured-drivers.md`, held group: the construction a solver never considers is outside its hypothesis space; a
    coverage survey's reader looks inside the survey, and the benchmark that settles the dependence sits in the vital
    and border statistics.
  - This lane's record: readers missed every call that turned on a structure of the process no document names
    (task472, task473, task475, task476, task477) and landed every call that turned on a textbook design correction a
    document made readable (this slot's v1, v3 and v4).
  - task448 and task473 (capture measured on an overlap; a catch rate by the trait's level): differentiation lines on the
    card. Here no capture rate is measured for the people both counts miss; their number comes from a sex ratio.
- **WARNs answered.** overuse.objective: the ETL lane is this author's lane. repeat.gate_g and overuse.gate_g against
  task474 v4: the honest key for a call pinned by the data's internal consistency; task474's driver (renewal churn in
  payment claims) shares nothing else. repeat.question_form against task474 v4: the call is a count per region.
- **Personas** (`guard.py names --geo "New Zealand" --seed 471`): Chelsea Buckley, Bryan Tapp.

## Default path

1. Read `enrolment_campaign_plan_2027.docx`: the 200 organisers go to the 16 regions in proportion to each region's
   adults not on the roll on census day (4 March 2025), by largest remainders, at least two each; adults are the people
   aged 18 or over usually resident in the region that day, whether or not the census counted them; the roll is the
   electors at the close of census day with a residential address in the region.
2. Read `census_2025_usual_residents_by_region.xlsx` (one sheet a region, single years of age by sex, the imputed
   records shown beside each count) and the post-enumeration survey's files, `pes_2025_people.csv` (the survey's
   people, matched to a census record or not) and `pes_2025_census_records.csv` (the census records in the sampled
   meshblocks, each correctly counted or in error), with the cells `pes_2025_methods_report.pdf` files: region by sex
   by age group (18 to 24, 25 to 34, 35 to 49, 50 to 64, 65 and over).
3. In each adult cell took the census records the survey could match against (the count less the imputed records),
   kept the share the survey found correctly counted and raised them by the survey's people over those the census also
   counted, the dual-system estimate; summed the cells by region: the adults on census day.
4. Took the residential electors in `roll_at_close_of_census_day_2025.csv` to regions through
   `electorates_and_regions.csv`, subtracted, and shared the 200 organisers by largest remainders with a floor of two:
   Ardenmere 26, Merriton 20, Westerby 26, Larchfield 28, Glenwhite 31, Hawksridge 4, Fairholme 11, Eastwold 12,
   Corran Valley 6, Drumlea 4, Orrinvale 4, Inchgarry 8, Strathmuir 6, Rowanlea 3, Kilraven 8, Nethermoor 3.

Ends on: Westerby 26, Larchfield 28 and Glenwhite 31 organisers, Ardenmere 26, Hawksridge 4, Corran Valley 6, Drumlea 4 and Nethermoor 3.

Golden: Westerby 25, Larchfield 26 and Glenwhite 29 organisers, Ardenmere 27, Hawksridge 5, Corran Valley 7, Drumlea 5 and Nethermoor 4, the other eight regions as the default path gives them.

## Stump sentence

The default path estimates each region's adults by the post-enumeration survey's dual-system estimates within its
cells, the textbook coverage estimator, and gives Westerby 26, Larchfield 28 and Glenwhite 31 organisers against
Ardenmere 26, Hawksridge 4, Corran Valley 6, Drumlea 4 and Nethermoor 3; the estimator takes for granted that the census
and the survey miss people independently, and the men aged 18 to 49 with no settled household are missed by both, so
the estimate leaves about 4 per cent of them out; because a region's adults not on the roll are a small difference of
two large counts, raising the men to the sex ratio that births, deaths and border movements fix (which the women's
estimates match) moves eight regions' organisers.

## Three rules

Task type: census register administrative data quality (a census's net coverage error measured by its post-enumeration survey and corrected for the dependence between the two counts, conformed with the roll into the Commission's enrolment-gap file), a task type serving Data Extraction & Conformation (ETL).

Domain test: the deciding quantity is each region's census-day adult population corrected for coverage, estimated the way census coverage measurement estimates it: dual-system estimates within post-strata, with the correlation bias the dual-system model assumes away measured against demographic analysis's sex ratios and restored to the adult men.

Swap: "how many of 200 nurses does each region get on its patients not registered with a doctor, from a register audit" keeps the subtraction and loses the structure: there is no independent recount whose capture can depend on the first count's, no birth cohort and no sex ratio fixed by births, deaths and migration to measure the shortfall against.

Layer 1: each item written by the system that holds it and none moving the call when mishandled (asserted, R2): the census outputs' workbook (a sheet a region under header blocks, a contents sheet and notes, ages 100 and over in one row; the row dropped leaves the call); the vital statistics' deaths in two layouts (1925 to 1944 wide by year of birth in a workbook, 1945 to 2025 long in a CSV; the workbook missed leaves the call under every age range and mode of the correction); the series' provisional period for the first weeks of 2025 (ignored, the call stands); eight electorates renamed at the 2024 boundary review and every electorate renumbered in alphabetical order (the roll at census day and the concordance carry the current numbers and names); and, on the asks' path only, the roll log's two platforms (the old one's running numbers, the country's time, its own reason codes, the 2020 review's electorate numbers as on the 2023 general election's roll, and a new record for every enrolment with the elector's older record removed overnight as a duplicate; the new one's hex keys, UTC, one record a person, reinstatements naming an old-platform removal by the key the migration gave it) and an extract that runs three months past the reporting period. The imputed records, the survey's match and enumeration codes and the overseas electors are the estimator's and the plan's own inputs, filed in the methods report and the plan, not mess.

Layer 2: the field's own method done right (field_method): the dual-system estimator's independence assumption fails for one group, and the bias it leaves is measured by demographic analysis's sex ratio, the method census coverage evaluation uses for correlation bias, then carried to every region's men of the age.

Decisive step: measuring the dual-system estimates' correlation bias against demographic analysis (each age group's men per woman from births, deaths and border movements by year of birth) and raising the men aged 18 to 49 in every region to the sex ratio it gives against the women's estimates, which agree with demographic analysis.

Not semantics: every field, code and definition read correctly (the imputed records, M and N, C, D, V, O and W, the cells, usual residence, the roll's residential addresses) still leaves the easy route on the dual-system estimates, whose eight wrong regions come from a dependence between two honest counts that no field, code or definition records.

Not rule application: the plan files the population, the day, the subtraction and the sharing rule; the methods report files the survey's design and its cells; no shipped sentence names a dual-system estimator, a dependence, demographic analysis or a sex ratio, so executing every stated rule leaves the solver at the textbook estimate and its wrong eight.

Analyst test: a strong analyst who reads every file and rule correctly and estimates each region's adults by dual-system estimation within the survey's cells (the textbook coverage estimator) files Westerby 26, Larchfield 28 and Glenwhite 31 organisers, Ardenmere 26, Hawksridge 4, Corran Valley 6, Drumlea 4 and Nethermoor 3, because the estimator's independence assumption leaves out the men both counts missed.

Estimand: the Commission's plan (enrolment_campaign_plan_2027.docx, sections 2 and 3): the people aged 18 or over usually resident in each region on census day, 4 March 2025, whether or not the census counted them, less the electors on the roll at the close of census day with a residential address in the region; 200 organisers in proportion, largest remainders, at least two each.

No decoy: nothing is planted to be caught: the census counts who it counts, the survey recounts its meshblocks independently, the vital and border series are complete registrations, the roll is the roll; no memo, draft, briefing or earlier allocation argues a method, and no published estimate ranks the regions on the gap (the 2018-base estimates at June 2024 are a declared wrong-basis distractor, another date and another base).

No certified replay: no published coverage estimate, earlier enrolment gap or certified figure ships to back a method out of; demographic analysis is rebuilt from registrations, not read off a filed table.

Lesson: a dual-system estimate is only as good as the independence of its two counts, and where the same people evade both, demographic analysis's sex ratio measures what neither count can see; no build on file corrects a capture-recapture estimate for correlation bias against an outside demographic benchmark.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0, the census counts as they stand (14 regions off) | the plan's "whether or not the census counted them" sends the solver past the counts: fires | the workbook's counts: fires | none | none | none | one subtraction: fires | readable |
| R1, one national coverage ratio per sex and age group (10 off) | none | the survey files summed nationally: fires | a single coverage factor is the first adjustment to hand: fires | none | none | one ratio a cell: fires | readable |
| R2, dual-system estimates within the survey's cells (8 off, the default path) | the methods report files the cells and the codes: fires | MATCH and STATUS: fires | the textbook coverage estimator: fires | none | none | three ratios a cell: fires | readable |
| R3 (decisive), the men aged 18 to 49 raised to demographic analysis's sex ratio | no clause names a dependence, demographic analysis or a sex ratio: silent | no column holds it; the flows are national series by year of birth: silent | the reflex stops at the survey's estimator: silent | no control ties under either: silent | every record valid, the battery finds nothing: silent | a cohort accounting over a century of registrations and a ratio against the women: silent | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | adults | aged 18 or over on census day, by the census's single years of age | 18 or over at the plan's date | another population | plan 2.1: "aged 18 or over on census day" |
| SF2 | usually resident, counted or not | the census's usual residents plus the people it missed, less its records in error | the census count | R0 | plan 2.1: "whether or not the census counted them" |
| SF3 | census day | 4 March 2025 | the survey's fieldwork | none | plan 2.1 and the workbook's title |
| SF4 | on the roll | electors at the close of census day with a residential address in the region | every elector including overseas ones | 12 regions off | plan 2.2: "Overseas electors are not counted in any region."; they carry address type O |
| SF5 | sharing | largest remainders on the unrounded shares, at least two each, the floor taken first | rounding each region's adults first | same call (asserted) | plan 3.1 |
| SF6 | region | the 16 regions; each electorate in one region | none | none | the concordance |
| SF7 | imputed records | the survey's census-record sample excludes them, so the ratio's base is the count less the imputed | the count with them | 11 regions off (12 corrected) | methods report 3.3: "except the records the census imputed" |
| SF8 | enumeration codes | C counted correctly; D, V, O and W in error | W counted | another share | methods report 3.3 table |
| SF9 | match codes | M matched to a census record, N not | none | none | methods report 3.2 |
| SF10 | cells | region by sex by the five adult age groups | cells pooled by region, by region and sex, or by region and age | 8 regions off as they stand; 7, 2 and 7 corrected | methods report 4: "estimation cells: region by sex by age group" |
| SF11 | the correction's carry-down | each age group's factor on every region's men alike | the extra men shared on each region's census misses | same call (asserted) | demographic analysis is national (no regional flows ship) |
| SF12 | demographic analysis's date | census day, the 2025 provisional weeks included | the end of 2024 | same call (asserted) | the notes: provisional period to 3 March 2025 |
| SF13 | the target | the men's estimate at demographic analysis's sex ratio against the women's | demographic analysis's male total | same call (asserted) | the women's estimates agree with demographic analysis within 0.2 per cent |
| SF14 | the ages corrected | 18 to 49, where the two disagree | 18 to 64, or every adult age, by ratio, by total or with both sexes raked | same call (asserted, also with the deaths workbook missed) | the 50 to 64 and 65 and over ratios agree within 0.2 per cent |
| SF15 | birth timing | the share born before 4 March in each year of birth (62 of 365) | none of them | same call (asserted) | the notes: births by calendar year |
| SF16 | the asks' window | after the close of census day to the end of 30 June 2026, the country's time, in an extract that runs to 30 September 2026 | the stamps as stored; the extract's whole span | another count | specification 2: "Dates and times are the country's time." and the reporting period; the dictionary's PROCESSED: "the old platform's in the country's time, the new platform's in UTC" with the offset and the daylight saving period |
| SF17 | new electors: who a person is, and whether they were on the roll | each elector number once, a record being a PERSON_REF; on the roll at the close of census day if a removal in the window takes off a record nothing in the window had put on it | one person a reference; references tied by REF_TXN; a first transaction that is a removal; any removal; a number issued before census day | another count each | specification 3: "not on the roll at the close of census day", "each person once"; the dictionary: PERSON_REF "The platform's reference for the person's record", ELECTOR_NO "The elector number"; the records: every old-platform enrolment under a number issued before census day names the removal it puts right or is followed overnight by the removal of the elector's other record |
| SF18 | removed because they had died | deaths under each platform's code, less removals a later accepted transaction anywhere in the extract reverses: a reinstatement of the same record or an enrolment naming the removal | 01 read one way throughout; only removals REF_TXN names; reversals inside the window only | another count | the dictionary (11, 12, REF_TXN), the migration notes (legacy 01), specification 4: "A removal later reversed was not a removal."; the records: each reinstatement of an old-platform removal carries the removed record's reference and elector number |
| SF19 | the region of a transaction | the electorate number on the old platform's transactions is the 2020 review's, as on roll_at_2023_general_election_by_electorate.csv; on the new platform's the concordance's | every number read as the concordance's | another count | the records: the reinstatements of old-platform removals restore the same region only under the 2023 roll's numbers, and the old platform's transactions by electorate number follow the 2023 roll, not the census-day roll (checks.py) |
| SF20 | added to the roll | an accepted enrolment or reinstatement that puts a person who was not on the roll at the close of census day on it, a removal made before census day and put right in the window included | enrolments only; enrolments that put a removal right left out | another count each | specification 3: "the people added to the roll in the reporting period who were not on the roll at the close of census day"; the dictionary: "REI the reinstatement of a removed elector"; the records: each such reinstatement names a removal the extract, which starts on census day, does not hold |

## Ladder

- **R0**, the census counts less the roll: 14 regions off the golden (Glenwhite 38 and Ardenmere 17 against 29 and 27).
- **R1**, one national dual-system ratio per sex and age group applied to each region: 10 regions off.
- **R2**, the default path, dual-system estimates within the survey's cells: 8 regions off (Westerby 26, Larchfield 28,
  Glenwhite 31, Ardenmere 26, Hawksridge 4, Corran Valley 6, Drumlea 4, Nethermoor 3).
- **R3**, the golden: the men aged 18 to 49 raised by 3.6, 4.0 and 4.8 per cent (18 to 24, 25 to 34, 35 to 49); each
  lower rung with the same correction stays off (the census counts 9 regions, the national ratio 11).
- **Margin:** the golden's largest-remainder cut clears its nearest neighbours by 0.217 of an organiser; every
  convergent reading (SF5, SF11 to SF15) files the golden (asserted).
- **Grid:** the partial and slipped paths (cells pooled by region, by region and sex, by region and age; errors kept;
  imputed kept; both; each with the correction on top) leave 2 to 12 regions off; none lands the golden (asserted).
  The nearest, cells pooled by region and sex with the correction, is 2 off and violates methods report 4.
- **Dominance:** the decisive move is the one correction that adds to each region in proportion to its young men
  rather than to its misses, so it moves organisers from the college regions, whose gaps are mostly the young people
  every count misses, to the regions whose adults are mostly on the roll: Larchfield and Glenwhite lose two each and
  Westerby one; Ardenmere, Hawksridge, Corran Valley, Drumlea and Nethermoor gain one each.

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | people aged 18 or over usually resident in each region on census day, counted or not (plan 2.1, SF1, SF2) |
| 2 | Unit of account | the region; electorates nest (concordance, SF6) |
| 3 | Attribution window | census day, 4 March 2025 (SF3) |
| 4 | As-of dating | the roll at the close of census day (plan 2.2) |
| 5 | Version basis | one census release, one survey file pair, one roll snapshot |
| 6 | Denominator | each cell's survey shares from its own sampled meshblocks |
| 7 | Weighting | none: one meshblock in 30 in every region, equal chances (methods report 2) |
| 8 | Window length | one day; the asks' window from the close of census day to the end of 30 June 2026, inside an extract to 30 September 2026 (SF16) |
| 9 | Boundary inclusivity | the asks' window excludes census day and includes 30 June 2026 (SF16) |
| 10 | Rounding path | shares unrounded, organisers whole by largest remainders (SF5) |
| 11 | Tie-break | none: the cut clears by 0.217 |
| 12 | Maturity and censoring | the survey's matching complete, no unresolved cases (methods report 3.2) |
| 13 | Order of operations | estimate, correct, subtract, share (plan 3) |
| 14 | Row order | the asks take each person's first enrolment or reinstatement by the country's time (SF17, SF20) |
| 15 | Duplicate resolution | the census's duplicates are its D records (SF8); the asks count each elector number once, the old platform's older records removed overnight as duplicates (SF17) |
| 16 | Identity normalisation | the roll at census day and the new platform carry the 2024 electorate numbers, the old platform the 2020 ones as on the 2023 roll (SF19) |
| 17 | Netting | removals reversed anywhere later in the extract netted, by a reinstatement of the record or an enrolment naming them (SF18) |
| 18 | Dimensional units | people; the old platform's local time and the new platform's UTC, filed in the dictionary (SF16) |
| 19 | Code and status semantics | M and N, C, D, V, O, W (SF8, SF9); removal codes by platform (SF18) |
| 20 | Integerisation | whole organisers, whole people in the asks |
| 21 | Clause scope | the plan for the allocation; the specification for the asks |
| 22 | Forward window contents | the 2027 campaign's organisers, decided on the census-day gap |

## Literal reader

Executing the plan, the specification and the methods report word for word leaves two places silent, the estimator and
the carry-down; every estimator that uses all the shipped evidence (the survey for coverage, the registrations for the
sex ratio) and every carry-down and convention in SF5 and SF11 to SF15 files the golden (asserted), while every reading
that drops the registrations files a default-path allocation; no literal reading of a filed sentence gives another
answer.

## Oracles

- The census workbook's national total and the roll's total: true under every handling, they rank nothing.
- The 2018-base estimates at 30 June 2024: another date and another base (a declared wrong-basis distractor), ruled
  out by the plan's census day.
- No published coverage estimate, gap or allocation ships; none.

## Ask sheet

- **Ask A, the people added to the roll in each region between census day and 30 June 2026 who had not been on it on
  census day (16 figures, whole people).** H18 home: the campaign's baseline, set beside each region's organisers in
  the Commission's plan (section 5). Path: `roll_transactions_2025_2026.csv` (TXN_ID, PROCESSED, TXN_TYPE, REASON,
  STATUS, ELECTOR_NO, PERSON_REF, ELECTORATE, ADDRESS_TYPE, REF_TXN), the data dictionary, the migration notes, the
  concordance, `roll_at_2023_general_election_by_electorate.csv` (ELECTORATE, REGION), the specification: six files,
  twelve columns.
  Primary device (re-sited after stage 4 round 2, where both readers kept all 32 figures through REF_TXN and the
  concordance's earlier numbers): D7, the true key elsewhere. An elector keeps one number for life, and the old platform
  opened a new record (PERSON_REF) at every enrolment it took, an elector's own included: a move to another electorate,
  or a second form, is an enrolment under the elector's number and a new reference, and that night its duplicate check
  removes the older record (03). No file says so and no REF_TXN joins them. One person a reference counts every mover
  as a new elector (52,050 more); a first transaction that is a removal does too; "anyone with a removal" leaves out
  the 705 new electors who sent a second form. Only an elector number followed through its records settles all three.
  Second device: D5, an interior population. Removals made before census day in error (the death matches of December
  to March, the January and February canvass) and put right in the window, by an enrolment on the old platform or a
  reinstatement on the new, put people on the roll who were not on it at census day: 330 in all, 6 to 45 a region.
  Counting enrolments only, or leaving out every enrolment that puts a removal right, misses them; each names a removal
  the extract, which starts on census day, does not hold.
  Third device, shared with ask B: D2, a label stored before a silent switch. Electorates are numbered in alphabetical
  order of name at each boundary review, and the old platform kept the 2020 review's numbers to the end; both reviews
  number 01 to 47, so every old number joins to a current electorate and nothing fails (44 of 47 numbers name another
  electorate, 29 in another region). Only the 2023 general election's roll carries the 2020 numbers, as a roll in its
  own right; the records force it (the reinstatements of old-platform removals restore the same region only under
  them, and the old platform's transactions by number follow the 2023 roll and not the census-day roll, checks.py).
  Hazards: each platform's time basis (filed), census-day transactions, rejected applications, overseas addresses,
  re-enrolments of electors removed in the window, the corrections of death removals made in the window.
- **Ask B, the electors removed from the roll in each region in that time because they had died (16 figures, whole
  people).** H18 home: the roll's cleaning baseline beside Ask A. Path: the same log, the dictionary's codes and
  REF_TXN, the migration notes' legacy codes, the concordance and the 2023 roll, specification 4: five files, ten
  columns.
  Primary device: D7 again, on another join. The new platform reinstates a removal the old platform made under the key
  the migration gave it, which the extract does not carry; netting only the removals a REF_TXN in the extract names
  keeps those corrected deaths (102 with the next device, 2 to 15 a region). Second device: D8, a clock against a filed
  cutoff: the extract runs to 30 September 2026, and a removal reversed after 30 June was still not a removal
  (specification 4); netting inside the window keeps 34 of them, in 14 regions. Third: the shared 2020 numbers.
  Hazards: the code reissue (old 01 deceased, new 01 a request; filed), the time basis (filed), census-day removals,
  the old platform's corrections by enrolment (REF_TXN in the extract).
- **The construction layer:** the call and the sixteen organisers; the cracker has them.
- **Main population zero-counts (asserted):** the call reads no transaction-log row, dictionary, migration note or 2023
  roll.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| A, new electors | the round-2 readers' reading: accepted enrolments at residential addresses in the window in each platform's time, people tied through REF_TXN, anyone with a removal in the window left out, enrolments that put a removal right left out, reinstatements no addition, the regions by the concordance's numbers: the movers counted, the second forms and the corrections of earlier removals dropped and the old platform's five months misplaced, all sixteen outside their counts | miss |
| B, removed for death | each platform's death codes in the window, reversals netted where a REF_TXN in the extract names them, the regions by the concordance's numbers: the old platform's removals reinstated on the new platform kept, the late reversals kept and the five months misplaced, fifteen of sixteen outside their counts | miss |

- Pair ceiling: 35.2 (weights 38 / 7 / 55: the cracker 46.7 on the main block, the instructions and 1 of the 32 ask
  figures; the mirror, R2, 23.7 on 8 of the 16 organisers, the instructions and the same ask figure)
- Mirror leakage: 3.1 per cent of ask weight (one ask figure, the asks reading no rung's construction)
- Measured by: generator/ceiling.py
- Sensitivity (ceiling.py on this build): the old platform's 2020 numbers found keep 0 of 32 (pair 34.4); with a person
  an elector number and the record test, 0 (34.4); with the corrections of earlier removals as additions, ask A whole,
  16 of 32 (48.1); with reversals tied by the record inside the window, 18 (49.8); with the late reversals, 32 (61.9).
  Each ask turns on three separate finds; two readers off the call who make every find but the last keep 22.0 to 52.9.

## Pre-ship check

- **The 10/10 rules re-read against the built pack.** Domain: the deciding quantity is each region's census-day adult
  population corrected for coverage the way census coverage measurement corrects it, dual-system estimates within
  post-strata with their correlation bias measured against demographic analysis's sex ratios; checks.py executes the
  analyst test on the clean truth (the dual-system estimates file the default path's eight wrong regions, the decisive
  step alone files the golden). Layers: the workbook layouts, the deaths split across two files, the provisional
  period, the renumbered electorates and every roll-log item are the systems' own and neutral on the call (R2); the
  call reads no transaction-log row, dictionary, migration note or 2023 roll (asserted). Three rules: no decoy, memo
  or earlier allocation ships; no field reading decides; executing every filed rule files the default path.
- **Judge:** v5r1 NOT_DETERMINISTIC and FIX_NOW (the unfiled UTC, filed), v5r2 DETERMINISTIC and APPROVE (Gate G
  method_or_model_selection and analytical_non_defect, Gate H pass); v5r3 on the shipping pack DETERMINISTIC and
  APPROVE, all 48 graded figures reproduced, Gate H pass.
- **Readers:** six scored readers in three rounds, all missing the call (five on the default path, one with the imputed
  records kept); rounds 1 and 2 kept 32 of 32 ask figures through documented devices, so the asks were re-sited;
  round 3 on 5b89c291378b1d76 kept 1 and 0 of 32 (3.1 and 0.0 per cent), score_reader exit 0 on both.
- **Free gates (2026-10-20):** checks.py 198 of 198, verify.py PASS, two builds byte-identical, target.zip
  5b89c291378b1d76 cut from the final build (20 files), figures_check.py 77 of 77, precut.py 51 checks clean,
  voice-check clean, guard.py surface clean and heart WARN (answered in the draw), ceiling.py pair 35.2.
- **leak.py REVIEW lines, each harmless:** the field operations summary names the sixteen regions (the call is a list
  of region names), and the methods report and series notes use the survey's and the registrations' own words without
  naming a dependence, demographic analysis or a sex ratio.

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
- 2026-10-20, stage 4: architecture 3 itself, the county estimate over two overlapping lists sampled separately,
  each tested well counted at one over its chance of selection from either list. The judge (run v3r1) found it
  DETERMINISTIC and APPROVE (Gate G method_or_model_selection, analytical_non_defect; Gate H analytical), but both
  scored readers landed the call and all 32 ask figures: reader A by the inclusion probabilities, reader B by the
  post-stratified estimator. The design report must describe the two lists and their separate draws for the estimate
  to be determinate, and once described the dual-frame estimator is executed as a work order; the routing county on
  the retest requests fell to a consistency check of the request's county against the first kit's. Spent on Gate F.
- 2026-10-20, at the v4 draw: a coarse privacy-preserving linkage key whose chance agreements inflate each county's
  linked count, corrected by the expected chance matches: the lesson task468 v4 teaches (false links for common
  identifiers), shipped in this lane today.
- 2026-10-20, at the v4 draw: the dual-frame world with a nonresponse weighting class added: stacks a second step on a
  rung both readers already executed, and the weighting class rests on a missing-at-random assumption a judge reads as
  open.
- 2026-10-20, at the v4 draw: an annual quantity read from a seasonal record: an annual estimand announces the season,
  and the driver is task476's (onset season against inspection timing).
- 2026-10-20, at the v4 draw: persons registered at crowded addresses as a second absence stratum: for the audited
  persons the address context would have to ship as a column or an address-member table, either of which displays it.
- 2026-10-20, at the v4 draw: school proficiency rates from point-estimate classification against expected counts
  (plausible values): the estimand would have to name an expected count, which files the method.
- 2026-10-20, at the v4 draw: chained volume components summed: reads as a unit's semantics (chained dollars are not
  additive), so the decisive step would be data semantics.
- 2026-10-20, at the v4 draw: the register's registration lag completed by its delay distribution: maturity_censoring,
  banned at the draw against task250.
- 2026-10-20, at the v4 build: the asks' first devices (rejected messages sent again, late reports, former residents'
  deaths): every one is executed by a careful solver who joins the hub's acknowledgements and applies the filed
  residency condition, so the cracker landed both asks; re-sited onto departures and deaths the register annulled as
  entered in error, found only in the persons' own histories.
- 2026-10-20, at the v4 build: the year-end batch as the deaths' primary: determinate only with a filed local-time
  convention, which a careful solver executes; kept as a hazard shared by both asks.
- 2026-10-20, at the v4 build: persons removed after an address investigation who had died before it (registered when
  they died), to make residency two-sided: with the year-end batch and the annulled deaths a three-error reading
  cancelled back to the golden in 21 of 24 municipalities; removed, residency now one-sided.
- 2026-10-20, at the v4 build: a third ask, former residents living abroad on 1 January 2026, with non-resident records
  never closed for persons who came back: determinate only with a filed re-registration condition, which hands the
  device over; dropped.
- 2026-10-20, at the v4 build: the national circular migrants' gaps of one to six years: the seasonal-work towns'
  long-gap migrants then sat in a seven-person cell of stay by earlier departure by first settlement, and that cross
  filed six with a municipality 0.1 from the line; national gaps widened to 1 to 14 years, every cross now files nine.
- 2026-10-20, stage 4: architecture 4 itself, the register's erroneous enumerations post-stratified by the migration
  career rebuilt from the event history. Both scored readers on target.zip b6990395f2efabc2 landed the call
  (score_reader exit 1 on each, 2 of 2 call figures). Reader A fitted a logistic model with a returnee flag and years
  since the last IMM; reader B built cells of country of birth by years since the last arrival by an earlier
  emigration. Report 5's "the respects that bear on it" plus 12,000 audited persons with histories invites testing
  which characteristics predict absence, and time since immigration and return migration are the field's textbook
  covariates, so the step was the reflex rather than the analysis a solver skips. Both readers also executed both
  asks' devices: the annulled departures and deaths came from a check of the hub's log against the register's ANN
  events, and the year-end batch from converting UTC to CET. They missed the 48 ask figures only by counting messages
  sent in 2025 whatever the event date, a reading the v4 spec's "departures abroad in 2025 ... from the messages ...
  sent in 2025" left open once "with a departure date in 2025" was dropped (a fork, not a device). Spent on Gate F.
- 2026-10-20, re-root: architecture 4 (the register over-coverage audit) spent at Gate F when both readers
  post-stratified the audit on the field's textbook covariates; architecture 5 is a fresh world (a census and its
  post-enumeration survey) whose decisive step is a judgment the textbook estimator takes for granted.
- 2026-10-20, at the v5 draw: council membership set by population bands on the census-day population, a threshold
  scorecard over the districts near a band edge: shape 10 banned against task251, and the same call shape as v4.
- 2026-10-20, at the v5 draw: one representation quota for every district, set as the lowest that keeps the councils'
  total within a statutory cap: a near-uniform correction is absorbed by the quota itself (it rises with the
  populations), so most districts' councillors do not move and only the setting discriminates.
- 2026-10-20, at the v5 draw: seats apportioned among districts by a divisor method: a relative allocation that a
  correction proportional to each district's men aged 18 to 49 barely moves (0.05 of a seat for a six-seat district).
- 2026-10-20, at the v5 draw: an anchor block moved to the end of a speeded new form, not-reached responses scored
  wrong: item response equating again in this slot (architecture 2's family, anchor contamination), and a not-reached
  code read as missing is data semantics.
- 2026-10-20, at the v5 draw: a scheduled-date field the office re-aligns once a case starts, which back-tests
  perfectly on closed cases: the re-alignment is a field reading, and the guard's validated-decoy shape.
- 2026-10-20, at the v5 draw: decisive generator G16 (method selection) and G12 (absence of record against record of
  absence): the population/G16 signature is spent in six builds and G12 is banned against task250; G8 (reachability
  against magnitude) states this step honestly and is unspent with this gap.
- 2026-10-20, stage 2: a uniform world (one unsettled share and one coverage for every region type) left the
  dual-system and golden allocations three regions apart, too few for a ladder whose decisive rung must carry the call.
- 2026-10-20, stage 2: a world with region types far apart in their unsettled shares moved eight regions, but the
  carry-down then forked: sharing each age group's extra men on each region's census misses rather than on its men
  gave another allocation in eight regions, a step no filed sentence closes. Seed 505's middle world moves eight
  regions and both carry-downs file the same allocation (asserted, SF11).
- 2026-10-20, stage 2: each region's adults not on the roll as graded figures: the golden's readings (SF11 to SF15,
  the men's total, one band) spread them by 68 to 304 people a region while the organisers stay fixed, so the gap is
  not graded and the organisers are.
- 2026-10-20, stage 4 round 1 on target.zip 7b7e6acddefeb6b8: both readers missed the call on the default path (8
  regions off), each reading the vital and border series as an alternative it did not need, question 6 analytical;
  both kept all 32 ask figures (score_reader exit 1 on the asks). They found the new platform's UTC through its first
  stamp (3 August 12:32 against the notes' Monday 4 August) and the provisional transfers' hours, the movers through
  the shared person reference (an earlier removal) or the elector-number range (below 40,000,000, a boundary the
  generator had drawn round), and executed the filed codes and reinstatements. The asks were re-sited: the old platform
  given a person reference per enrolment tied only through REF_TXN (moves, and corrections by re-enrolment), its
  electorates the 2020 review's numbers, and the number counter run on from census day.
- 2026-10-20, judge v5r1: NOT_DETERMINISTIC and FIX_NOW on the asks: the new platform's UTC was inferred, never filed,
  and its literal reading moves both columns; the time basis is now filed in the dictionary's PROCESSED (the WHAT, not
  the conversion), so the clock is a hazard. The thread's residual age-range note came from demographic analysis built
  without the 1925 to 1990 deaths workbook (men 50 to 64 then 1.8 per cent short); the deaths were re-split at 1944/1945
  and the movements given from 1925, so the workbook missed leaves every age range and mode of the correction on the
  golden (asserted).
- 2026-10-20, stage 4 round 2 on target.zip 5402dd6ec2786aea: both readers again missed the call on the default path
  (question 6 analytical) and kept all 32 ask figures (score_reader exit 1 on the asks). Reader B placed the old
  platform through the concordance's NUMBER_BEFORE_2024_REVIEW and reader A "remapped" it the same way; both tied the
  moves and the corrections through REF_TXN, which the dictionary called "the earlier transaction this one completes or
  reverses". The judge (v5r2) found the build DETERMINISTIC and APPROVE. The asks were re-sited: the 2020 numbering
  left the concordance for the 2023 general election's roll, a file with its own use; the old platform's moves and
  second forms open a new record under the elector's own number and its overnight duplicate check removes the older
  one, with no REF_TXN; removals made before census day and put right in the window add people; the new platform's
  reinstatements of old-platform removals name the keys the migration gave them; the extract runs to 30 September
  2026, so a reversal after the window still nets.
