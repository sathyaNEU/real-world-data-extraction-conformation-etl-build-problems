# task486 design note

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first.

Architecture 2, drawn 2026-10-21, re-rooted fresh after architecture 1 (a privacy-protected census release's small-area
counts for senior-services provider areas) was spent at stage 4 on the judge's SEND_BACK. The author's rule holds: no
retirement, a fresh rebuild. The new draw keeps the lane's objective and the task type and takes a new world.

## Draw

| Field | Value |
|---|---|
| Domain and task type | general-statistics-data-science / data-integration-record-linkage-entity-resolution (ETL) |
| Objective | Data Extraction & Conformation (ETL): seven sources (four HMIS exports, the coalition's database, the clinic's encounters, the outreach app) conformed into one count of people served, each person once |
| Niche | resolving a privacy-preserving linkage service's pairwise findings across four Continuums of Care's HMIS exports, a domestic violence coalition's comparable database and a health care for the homeless clinic into the people the region served in FY2026, the count the 2027 regional fund is split on |
| World | the Halvering Valley region of an unnamed U.S. state: four counties (Halvering, Melbray, Ondrava, Pyrenna), one Continuum of Care each, the Halvering Valley Homeless Data Partnership as the nonprofit HMIS lead and integrator, the counties' Regional Fund Committee |
| People | Kathleen Carlson (the Partnership's director of data, the requester), Joshua Bell (the state linkage unit's lead, redrawn on 2026-10-23 because Andrew appeared in task478), Gina Bryant (the Partnership's executive director); drawn with `guard.py names --geo us --seed 486` |
| Stakeholder | the Partnership's director of data, who heads the HMIS lead's data office (statistical_office_head) and prepares the 2027 allocation table for the Regional Fund Committee |
| Forum, forcing event | the Regional Fund Committee (committee_or_panel); the fiscal agent's 2027 contract renewals with each recipient, written at the adopted amounts from 1 January 2027 (purchase_order_or_contract) |
| The call | how much of the 2027 Halvering Valley Regional Homelessness Fund each Continuum and the DV coalition receive, under the committee's policy that splits the fund on the people each served in FY2026 (1 October 2025 to 30 September 2026), each person counted once across the region and placed with the Continuum of their latest FY2026 entry |
| Decision type, unit | allocation_to_total; currency, resting on counts of people |
| Shape | 05, allocation to a fixed total: each recipient's people served and amount (10) and the region's people (1); ask A adds 16 night cells and ask B 10 waits, 37 graded figures. Moved from 03 at stage 2: the bridge's opening items, each source's records with FY2026 service, need no linkage and every response banks them |
| Deliverables | `halvering_2027_fund_allocation.xlsx`: the allocation, the shelter nights by Continuum and quarter, the rapid re-housing waits by Continuum and household type, and a notes sheet |
| Card | `.claude/skills/fingerprint/cards/task486.json`, architecture v2, first registered 2026-10-21 03:15 UTC, re-filed on 2026-10-23 at stage 2 against that day's window, architecture 1 in its lineage with its fate |
| Guard | re-filed 2026-10-23 against the window task483, task275, task179: the forcing event budget_or_appropriation and the role research_desk were banned, so both were redrawn to what the policy and the requester actually are (the fiscal agent renews each recipient's 2027 contract at the adopted amount, the event that makes the figure due now, the committee's meeting being the forum; the requester heads the Partnership's data office, the HMIS lead's own data function). WARN only: three_rules.strategy_risk (identity_resolution; answered in `## Three rules`), repeat.gate_g (etl_conformance beside task483: the mechanism here is the resolution of pairwise findings into persons, task483's was a register's grain), overuse.objective (the lane's objective) |
| Nearest drivers | task471 v3 lineage 0.07, task98 v2 lineage 0.06, task249 v4 lineage 0.06 (distinct identifiers after an idle expiry, recovered by replay: a different mechanism), task448 0.05; `slots` on the mechanism's words (transitive closure, connected components, unduplicated count) and on the setting's (homeless, Continuum, shelter, outreach, HMIS) returned nothing on file |

**The decisive step.** The State Data Linkage Unit compares client records from different sources on hashed
identifiers and returns each compared pair's score and finding (LINK at 9.0 or more). Each finding concerns one pair; the
unit does not group records into people. A record that carries less identity (an outreach contact whose app holds only a
birth year, a coalition survivor, sent with birth year only by the coalition's confidentiality policy, a street intake
with an approximate date of birth) scores 12.0 against every client of that name, birth year and sex, so one such record
links to two different people. Merging every chain of links (connected components, the generic step and the industry
default) then joins two clients one source holds apart: 225 merged groups hold two records of one source. Resolving the
findings strongest first and refusing any link that would put two records of one source in one person, so each such
chain is cut at its weakest link, returns the people. The step is the task type's own, the client library's Layer 2
pattern 3 for data integration (pairwise matches resolved into consistent entities; chaining them miscounts entities).

**Data-native sentence.** A client record that gives only a birth year matches every client of the same name, year and
sex, so where two such clients sit in one source a single partial record links to both.

**Retrospective count, forward call.** The fund is for the 2027 contracts, a window not yet open; the quantity it is split
on is FY2026, closed on 30 September 2026, because the policy files last fiscal year's people served as the basis (the
reason this build's deciding count looks back).

## Default path

1. Read the pack as shipped: the four Continuums' HMIS client, enrollment, exit and services files (Melbray's dates
   month/day/year), the coalition's workbook, the clinic's encounters, the outreach app's contacts, the unit's pair file
   and the register.
2. Flag every record's FY2026 service under policy section 3: an HMIS enrollment entered on or before 30 September 2026
   and not exited before 1 October 2025, a coalition stay with a night in the year, a clinic encounter in the year at
   Street, Homeless Shelter or Transitional status, an outreach contact in the year, all on local dates.
3. Take the unit's LINK findings and merge every record linked to another directly or through other records (connected
   components over the 24,952 LINK pairs).
4. Count each merged group holding a record with FY2026 service once and place it under section 4 (the Continuum of its
   latest HMIS enrollment open in the year, else the coalition, else the Continuum of its latest contact or encounter).
5. Split the 18,000,000 dollars left after the 4 per cent set-aside in proportion and round each amount to the dollar.

Ends on: Halvering 7,964,889 dollars on 17,644 people, the region 39,874 people (Melbray 4,294,829, Ondrava 2,972,162,
Pyrenna 2,132,517, the coalition 635,602).
Golden: Halvering 7,993,704 dollars on 17,774 people, the region 40,023 people (Melbray 4,283,337, Ondrava 2,962,447,
Pyrenna 2,125,478, the coalition 635,035).

## Stump sentence

Merging every record the linkage unit linked, directly or through other records, files the region at 39,874 people and
Halvering at 17,644 people and 7,964,889 dollars, 28,815 dollars short, because a record carrying only a year of birth (an
outreach contact, a coalition survivor, a street intake with an approximate date) links to every client of that name,
year and sex, so 225 merged groups hold two records one source keeps apart; resolving the findings strongest first so
that no person holds two records of one source gives 40,023 people and Halvering 7,993,704 dollars.

## Three rules

Task type: data-integration-record-linkage-entity-resolution, in General Statistics & Data Science, a task type the
taxonomy tags for Data Extraction & Conformation (ETL).
Domain test: the deciding quantity is the number of distinct people across seven sources, the object of entity
resolution: the linkage unit's pairwise findings resolved into persons consistently with each source's own
one-record-per-person grain, because pairwise matches are not transitive; the field resolves a match graph by
constrained clustering, and the generic merge (connected components) changes every recipient's count and all five
amounts.
Swap: the setting is incidental (a hospital system's patients or a school district's pupils across linked registers read
the same), so the swap is of the method: put a generic summary in place of the resolution, counting every record (51,149
people) or merging every chain of links (39,874), and all five amounts change; what decides is the task type's own
object, distinct entities from non-transitive matches.
Layer 1: each Continuum's HMIS export in the HUD CSV layout stacked as sent, with four record-key schemes, Melbray's
vendor writing month/day/year and Ondrava's the FY2022 destination list; the coalition's workbook with birth year only by
its confidentiality policy; the clinic's encounters carrying housing status per encounter in the HRSA categories; the
outreach app's JSON lines in local time with UTC offsets; the pair file across both fiscal years in each source's own
keys; the winter respite's bed nights and 30-day exit rule; shelter stays left open after a client moved on; rapid
re-housing households moving between projects; Ondrava's vendor writing the household's move-in date on every member.
Each is what the source system produces, and none carries the stump.
Layer 2: field_method, the client's pattern 3 for data integration: pairwise links are not transitive, a person holds no
two records of one source, and a chain that would join two is cut at its weakest link.
Decisive step: resolve the unit's pairwise LINK findings into people strongest first, refusing any link that would put
two records of one source in one person, instead of merging every chain of links into one person.
Not semantics: with every key joined, Melbray's dates parsed, every status and code read and sections 3 and 4 applied
exactly, the analyst who takes the LINK findings as filed and merges every chain still files 39,874 people; no field,
code, unit or definition read differently moves that, because the error is in what merging does to findings against
records that carry less identity.
Not rule application: no shipped document says how findings become people (the method note says each finding concerns
one pair and the unit does not group records into people; the guide states each source's grain in that source's own
description). Enumerated family, nine constructions: no linkage, every chain merged on all records or on FY2026 records
only, the best link per source on either side or mutual, quarantine of contradicted records, and the constrained
resolutions; Halvering's amount runs from 28,815 dollars under the golden (every chain merged) to 29,977 over
(quarantine), and no construction that leaves two records of one source in a person or drops a finding no grain
contradicts keeps any of the five amounts. Standing family, the six constrained resolutions (strongest first under every
order of equal links, strongest first on FY2026 records only, and every optimum of the kept link score, of the summed
pair evidence and of the fewest people): spread exactly zero, all five amounts the golden. The easy route sits outside
the standing family, refuted by the grain, so the family's agreement is the closure Gate C needs and not a reflex; what
rules the easy route out is silent, 225 merged groups holding two records of one source that only a per-group count of
each source's records shows, and nothing in the pack names it.
Analyst test: with every field read and every rule applied, the analyst merges every record the linkage unit linked,
directly or through other records, counts the merged groups with FY2026 service and files Halvering 7,964,889 dollars on
17,644 people and the region 39,874 people; resolving the findings strongest first so no person holds two records of one
source gives Halvering 7,993,704 dollars on 17,774 people and the region 40,023.
Estimand: policy RF-2027 (regional_fund_policy_RF-2027.docx) sections 2 to 5: the 2027 Fund of 18,750,000 dollars less
the Partnership's 4 per cent, split among the four Continuums and the coalition in proportion to the people each served in
federal fiscal year 2026 (1 October 2025 to 30 September 2026), a person counted once for the region if any record of
theirs shows service under section 3 (a) to (d) and placed with one recipient under section 4, each amount rounded to
the nearest dollar with the Partnership's share taking the rounding; people across sources counted from the unit's
findings of its 8 October 2026 run on the FY2025 and FY2026 records (section 5), each source holding a person once
(partnership_extract_guide.txt).
No decoy: nothing is planted: the partial identities come from street outreach intakes and the coalition's
confidentiality policy, every LINK is the unit's honest finding on the hashed identifiers, and no memo, draft, briefing
or figure in the pack argues for merging chains or states a count of people served.
No certified replay: the pack certifies no count of people served and no allocation, so no published figure can be
reproduced to recover the method; the point-in-time count and the housing inventory are a one-night count and a bed
inventory on other bases, declared distractors.
Lesson: a match graph is not an equivalence relation: findings against records that carry less identity chain different
people together, so a count of people has to respect what each source already knows about its own records; no build on
file teaches resolving pairwise matches under source-uniqueness constraints (task468 is the linker's own frequency error,
task249 identifier expiry, task98 household registration).

## Readability screen

| Rung | What the response does | What in the pack points at it | Verdict |
|---|---|---|---|
| R0 no linkage | counts every source record with FY2026 service as a person (51,149) | section 3 says a person is counted once, and the pair file exists to say who is who | readable |
| R1 every chain merged (the default) | connected components over the LINK pairs (39,874) | the pair file, the method note's LINK definition and the textbook merge | readable |
| R2 chains merged on FY2026 records only | drops the records with no FY2026 service, then merges (39,895) | the policy's FY2026 window | readable |
| R3 (decisive) strongest first, no two records of one source in a person | resolves the findings into people under each source's grain (40,023) | nothing names it: the method note says each finding concerns one pair and the unit does not group records into people, and each source's grain sits in its own description in the guide; only a per-group count of records by source shows the 225 merged groups holding two of one source | silent |
| R4 quarantine | drops every link of a record linked to two records of one source (40,201) | follows from seeing R3's conflicts and declining to choose between the findings | readable |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | people served | a person counted once for the region if any record shows FY2026 service | each source's records counted (51,149) | 0 of 5 amounts | section 3: "A person is counted once for the region" |
| SF2 | one person across the sources | from the unit's findings for the run of 8 October 2026 | re-scoring pairs, or treating NONLINKs as links | not computed | section 5: the Partnership counts people from the unit's findings; no NONLINK pair sits inside a golden person (asserted) |
| SF3 | LINK | the pair file's finding (score 9.0 or more), as returned | another threshold on the score column | not computed | the method note's findings and section 5 |
| SF4 | dates in the year | local dates (section 3) | outreach contacts read in UTC | same call | C1: no outreach contact after 16:00 local on 30 September of either year (asserted) |
| SF5 | an enrollment open in the year | entered on or before 30 September 2026 and not exited before 1 October 2025 (section 3a) | a stay's nights in the year (exit after 1 October 2025) | same call | C1: no exit on 1 October 2025 (asserted) |
| SF6 | a coalition stay on any night of the year | nights from StayStart to the night before StayEnd (guide) | StayEnd read as a night | same call | C1: no stay ends on 1 October 2025 (asserted) |
| SF7 | a clinic encounter at street, shelter or transitional status | HRSA Street, Homeless Shelter or Transitional | any encounter (Doubling Up and Unknown counted) | 40,128 people, 0 of 5 amounts | section 3(c) names street, shelter or transitional housing |
| SF8 | placement | the Continuum of the latest HMIS enrollment open in the year, latest by entry date (section 4) | the latest enrollment of any year | not computed | section 4 "open in the year"; no placement tie across Continuums (asserted) |
| SF9 | the latest contact or encounter | any outreach contact or clinic encounter of the year | only encounters at a qualifying status | same call | C1: each person's contacts and encounters fall in one Continuum (asserted) |
| SF10 | rounded to the nearest dollar | each amount rounded, the Partnership's share taking the rounding dollar (section 2) | largest remainder to 18,000,000 | Ondrava a dollar lower | section 2's rounding sentence |
| SF11 | the amount split | 18,750,000 less 4 per cent, 18,000,000 | splitting 18,750,000 | 0 of 5 amounts | section 2 |
| SF12 | the records the run covers | the FY2025 and FY2026 records (section 5) | resolving FY2026 records only | same call | C1: the constrained resolution on FY2026 records only returns the golden (asserted) |
| SF13 | the recipient of a survivor also in HMIS | the HMIS Continuum where an enrollment is open in the year, else the coalition (section 4) | the coalition for every survivor | not computed | section 4's order |
| SF14 | a person's records | every source's records, the clinic's and the outreach team's included (section 3 c, d) | HMIS records only | not computed | section 3 |
| SF15 | Melbray's dates | month/day/year | day/month/year | not computed | the column carries days over 12 in the second place (asserted) |
| SF16 | the region | the five recipients' people together | the Continuums only | not computed | section 2's five recipients |
| SF17 | nights people spent | a person's night counted once | each stay's nights summed | 0 of 16 cells | the asking sentence (people spent nights; a person spends a night once) and the guide's night convention (a client is in a project each night from entry to the night before exit) |
| SF18 | night-by-night nights | bed-night services | the respite enrollment's span | 14 of 16 cells | the guide's night-by-night sentence |
| SF19 | emergency shelters and safe havens | project types 0, 1 and 8 | transitional housing included | not computed | the asking sentence names emergency shelters and safe havens |
| SF20 | FY2026's move-ins | a head of household's move-in date in the year | every row carrying a move-in date (Ondrava's members) | 0 of 10 | the guide: the move-in date is recorded for the head of household |
| SF21 | entry into rapid re-housing | the first entry of an unbroken rapid re-housing stay (a same-day move between projects continues it) | the move-in enrollment's own entry | 0 of 10 | the asking sentence's entry into rapid re-housing; C1: no rapid re-housing re-entry one or two days after an exit (asserted) |
| SF22 | the region's average | over all the region's move-ins of the type | the mean of the four Continuums' averages | 44.3 against 43.8 with children, 44.8 against 45.3 adults only | the asking sentence: the region over all its move-ins |
| SF23 | household type | with children (a member enrolled as a child) or adults without children | by the head's age | not computed | the asking sentence; HMIS RelationshipToHoH 2 is a child |

## Ladder

| Rung | Region people | Halvering people | Halvering amount | Amounts kept |
|---|---|---|---|---|
| R0 no linkage | 51,149 | 25,197 | 8,867,153 | 0 of 5 |
| R1 every chain merged (default) | 39,874 | 17,644 | 7,964,889 | 0 of 5 |
| R2 chains merged on FY2026 records only | 39,895 | 17,661 | 7,968,367 | 0 of 5 |
| R2b best link per source, either side, then chains | 39,878 | 17,648 | 7,965,896 | 0 of 5 |
| R2c best link per source, mutual, then chains | 40,039 | 17,787 | 7,996,354 | 0 of 5 |
| R3 golden (strongest first, no two records of one source) | 40,023 | 17,774 | 7,993,704 | 5 of 5 |
| R4 quarantine (contradicted records unlinked) | 40,201 | 17,920 | 8,023,681 | 0 of 5 |

Every rung below and above R3 misses all five amounts; the nearest, R2c, still leaves merged groups with two records of
one source. The constrained resolutions all return R3 (Not rule application above, asserted in checks.py F1).

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | people with a record showing FY2026 service under section 3, all seven sources; a closed year, nobody unobserved | filed (section 3); C1 on the FY2026-records-only reading (asserted) |
| 2 | Unit of account | a person across the sources | filed (section 3, "counted once for the region") |
| 3 | Attribution window | FY2026 on local dates | filed (sections 2, 3); C1 at both boundaries (asserted) |
| 4 | As-of dating | the extract of 14 October 2026, the run of 8 October 2026 | filed (section 5, the guide) |
| 5 | Version basis | the run of 8 October 2026, the only run shipped | filed (section 5) |
| 6 | Denominator | the five recipients' people together | filed (section 2) |
| 7 | Weighting | one per person | filed (section 2) |
| 8 | Window length | one fiscal year | filed (section 2) |
| 9 | Boundary inclusivity | entered on or before 30 September 2026, not exited before 1 October 2025 | filed (section 3a) and C1 (asserted) |
| 10 | Rounding path | each amount from its unrounded share, to the dollar | filed (section 2), the rounding dollar to the Partnership |
| 11 | Tie-break | the latest entry date; equal links in any order | C1: no placement tie across Continuums, every order of equal links the same people (asserted) |
| 12 | Maturity and censoring | an open enrollment is open | filed (the guide: still open at the extract) |
| 13 | Order of operations | resolve across both years, then flag FY2026 service | C1: resolving FY2026 records only returns the same people (asserted) |
| 14 | Row order | the pair file's order | C1 (asserted over shuffled orders of equal links) |
| 15 | Duplicate resolution | within a source none: each source holds a person once | filed (the guide's grains); the decisive constraint |
| 16 | Identity normalisation | the unit's findings on hashed identifiers, each source's own keys | filed (section 5, the method note) |
| 17 | Netting against gross | none | not applicable; no amount negative (asserted) |
| 18 | Dimensional units | people, dollars | one unit each |
| 19 | Code and status semantics | HRSA Street, Homeless Shelter and Transitional count; Doubling Up and Unknown do not | filed (section 3c and the guide's categories); never the stump |
| 20 | Integerisation | whole people, whole dollars | filed (section 2) |
| 21 | Clause scope | each of section 3's clauses over the year | filed |
| 22 | Forward window contents | the 2027 Fund's amount | filed (section 2); nothing forecast |

## Literal reader

Executing the prompt and every filed sentence word for word: section 5 counts people from the unit's findings, the method
note says a LINK is the unit's finding that two records very probably belong to the same person and that each finding
concerns one pair, and the guide says each source holds a person once (a Continuum's monthly duplicate review, the
coalition's intake, the clinic's registration, the app's one key per client). A literal reader who chains every LINK puts
two records of one source in one person 225 times and contradicts the guide; one who keeps every finding a grain allows,
strongest first, contradicts only the weaker findings of each conflicted chain, and every such resolution returns the
golden (F1). Where the text is silent (time zones at the year's edges, a stay ending on the year's first day, a
contact's Continuum, resolving FY2026 records only), the records make the readings converge (C1 rows above). The asks'
readings are pinned in their asking sentences (SF17 to SF23).

## Oracles

No file ties only under the golden or only on a wrong read. The pack holds no count of people served, no recipient total
and no allocation; the run summary's records per source and its LINK and NONLINK totals tie under every resolution; the
point-in-time count and the housing inventory are one-night and capacity figures that no construction reproduces. No
referee is needed: the grain each source files is the evidence, and it sits in the records' own descriptions.

## Ask sheet

**Ask A, nights people spent in each Continuum's emergency shelters (night-by-night included) and safe havens in each
quarter of FY2026, 16 figures.** H18: a component of each recipient's case, the shelter load behind the people it served.
Use: the committee reads the shelter nights beside each Continuum's share. Primary device (D1, one night on two stays): a
stay left open after the client moved on, its exit after the same person's next entry in the same Continuum, so summing
each stay's nights counts the overlap twice; a person's night counts once. Hazards: the respite's nights are bed-night
services (the guide); the exit night is not a night; an open stay runs to the night of 30 September 2026; Melbray's
dates. Path: hmis_enrollment (EntryDate, PersonalID, ProjectID, SourceCoC), hmis_exit (ExitDate, EnrollmentID),
hmis_services (DateProvided, RecordType), the register (ProjectType), 4 files and 10 columns. Stops: each stay's nights
summed 0 of 16 (the cracker), the earlier of two overlapping stays dropped 0 of 16, the respite read by its enrollment
span 14 of 16, a person's night once 16 of 16. Realism: shelters exit clients late when they leave without notice, and a
new intake elsewhere is how the system learns they moved.

**Ask B, average days from a household's entry into rapid re-housing to its move-in over FY2026's move-ins, households
with children and adults without children, each Continuum and the region, 10 figures.** H18: a component of each
recipient's case, the time to housing behind its rapid re-housing spending. Use: the committee reads how fast each
Continuum houses households. Primary device (D7, the true key on a prior enrollment): a household that moved from one
rapid re-housing project of the Continuum to another on the day it left the first, its move-in on the second project's
enrollment; where a family has a second adult the receiving project mostly enrolled that adult as head of household, so
the chain runs through the person and not the role. Hazards: Ondrava's vendor writes the household's move-in date on every
member (D6 grain against the guide's head-of-household sentence); households moving in twice in the year (the ask is per
move-in); Melbray's dates. Path: hmis_enrollment (EntryDate, MoveInDate, RelationshipToHoH, HouseholdID, PersonalID,
ProjectID), hmis_exit (ExitDate), the register (ProjectType), 3 files and 9 columns. Stops: each head's own enrollment's
entry 0 of 10 (the cracker), chained through heads of household only 5 of 10 (the adults-only figures, where no head
changes), every row carrying a move-in date 0 of 10, chained through the person 10 of 10.

Main population: the call reads no bed night, move-in date, overlap or transfer structure and the asks read no linkage
finding and no coalition, clinic or outreach row (checks.py X1, X2); the overlaps and transfers sit in enrollment rows
the call reads only for whether a record was open in the year, which neither changes (asserted).

| Ask | The cracker's path (lands the call, runs the hygiene battery, executes every filed rule) | Kept | Verdict |
|---|---|---|---|
| A | each stay's nights from entry to the night before exit, plus the respite's bed-night services, summed by Continuum and quarter | 0 of 16 | miss |
| B | each head of household's move-in date against the entry of the enrollment carrying it | 0 of 10 | miss |

Mirror leakage: 0.0 per cent of ask weight (the mirror reads both asks as the cracker does).
Pair ceiling: 28.5 (cracker 45.0, mirror 12.0); with the person-night repair on both responses 62.3, and with the
person-level chain on the cracker alone 66.2 against the mirror's 12.0, so ask A's single device is the layer's exposure
and the stage 4 readers measure it.
Measured by: task486/generator/ceiling.py, run on the cut pack.

## Leak sweep lines

leak.py on the final pack, 2026-10-23: REVIEW, no LEAK.
- Sweep 3, the guide and the policy carry 20 and 25 of the committed call's 26 distinctive words: the words are the five
  recipients' names and the policy's own title, which the policy defines; neither file carries any figure of the call.
  Harmless.
- Sweep 4, the guide, the policy and the method note carry 11 to 14 of the stump paragraph's terms (records, source,
  person, findings): the vocabulary of any record-linkage pack. None names the resolution; the method note's "each finding
  concerns one pair of records; the unit does not group records into people" is the service's statement of its own
  scope, the sentence determinism-check section 1 requires of a source whose links the golden corrects, and the guide's
  grains sit in each file's own description. Harmless; the readers' question 1 tests it.
- Sweep 6 (INFO), the point-in-time count names five of the six candidates: a declared wrong-basis distractor
  (metadata.json), a one-night count that section 2 of the policy rules out as the basis.
- Sweep 9, dates after the setting: clean once the generator kept rapid re-housing transfers inside the year and each
  Continuum's record stamps before its export.

## Pre-ship check

The 10/10 rules re-read against the built pack. Rule 1: the deciding quantity is the number of distinct people across
seven sources, resolved from pairwise findings that are not transitive, the task type's own object; swapping the setting
leaves it, swapping the method (counting records, merging every chain) moves all five amounts. Rule 2: Layer 1 is the
sources' own mess (vendor date formats and key schemes, the coalition's birth-year-only workbook, per-encounter housing
status, local times with offsets, the respite's bed nights, open and overlapping stays, member move-in rows), and
cleaning all of it leaves the default path at 39,874 people; Layer 2 is the resolution, which no cleaning performs.
Rule 3: nothing planted (every LINK is the unit's honest finding), no field reading decides (T1 runs the easy route on
the clean truth with every filed rule applied and files 7,964,889 dollars for the downtown Continuum), and no stated rule
does the resolution (the method note disclaims grouping; the guide states grains). The analyst test executes in
checks.py T1 and T4; the standing family agrees exactly (F1, 4,438 member runs); the asks read no linkage finding (X2).

## Tried and rejected

- 2026-10-21, the seed's world (ET43, U.S. pharmaceutical exports to Germany against Germany's imports from the U.S.):
  every lever is a filed concept (CIF against FOB valuation, country of origin against destination, recording date,
  classification) or an estimated rate small against the gap (freight margins by weight) or a composition rate of the kind
  task481 just spent (the asymmetry ratio by product mix, the re-dispatched share through Dutch hubs); dropped before any
  data was cut.
- 2026-10-21, survey research's census-register task type for this world: the honest home, but its ETL pairing was taken by
  task479's re-root (BLOCK ban.pairing, and ban.artifact on published_series); the build is filed in data integration.
- 2026-10-21, a single-area figure or a per-area allocation as the call: the allocation's decision type repeats task471's
  puzzle triple (population, none, allocation_to_total) and the per-dollar rounding cannot hold two unbiased estimators in
  one bin; the call is the census table itself, counts to the nearest ten.
- 2026-10-21, noise added to each cell at the block level with no structural zeros (the demonstration-data behaviour):
  four to five per cent of the county's residents landed in blocks with no housing, a symptom the hygiene battery flags
  and a share no production release would show; the release leaves such blocks empty, which also silences the device.
- 2026-10-21, block groups alike in age within a tract: the tract route then matched the golden on most counts and left
  two estimators in one bin for some and not others; block groups now differ in age within a tract, as they do, and the
  tract route is a rung (6 of 12 off).
- 2026-10-21, ask B's prior-number deaths left to chance: a death hazard spread over a decade put no unreported death under
  an earlier number in the four rural providers; the July 2026 review not held, and at least one such death per provider,
  give the device mass everywhere.
- 2026-10-21, each block's total held to its own precise count (as the production release holds block totals) with the
  age cells forced to it: on paper the drift between blocks turns into flattening inside each block toward the 46
  cells' even share, which moves a rural block's 60-and-over count only by the gap between its true share (about 31 per
  cent) and the cells' 35, a few residents per area against the 40 to 190 the per-cell processing moves; kept the
  per-cell processing, under which small blocks publish more residents than their housing would hold.
- 2026-10-21, architecture 1 (each provider area's census-day counts built from the release's block groups, cut groups split by census-day housing units, against the block sum), spent at stage 4: the judge returned NOT_DETERMINISTIC and SEND_BACK, competing_defensible_answer, because nothing shipped showed the published block counts biased, so the block sum read as a defensible estimate (Gates G and H passed); documenting the bias would leave the step to whoever reads the notes. Both scored readers filed the block sum (0 of 12) and kept all 12 service figures: the roster's meals_per_day capped the re-sent rows and the registry's links chained the earlier numbers, so both devices sat on the careful path.
- 2026-10-21, architecture 2 draw, screened before the entity-resolution step (each dead on file or on measurement):
  left truncation in an asset or licence register (task133's delayed entry, rejected again in task262, task257, task265);
  the oldest-old counted by extinct generations (task228); non-detects under several reporting limits (task189); triple
  collocation (task228); age heaping (task230's rejected draw); a lowered reporting threshold bridged by an overlap ratio
  (task481's conversion rates); a benchmark-to-indicator ratio carried past the last benchmark (task457's report against
  final); landfill first-order decay (task480's age-declining increments); load estimation from sparse samples (Jensen,
  task229); a staggered rollout of a measurement change (task453, and task480 v2's meter exchange in flight); pooled
  medians from brackets (the never-average reflex, task480's screen); degree-day temperature adjustment (fresh, but a
  per-unit degree-day regression is the textbook route and lands it); hedonic quality adjustment (the estimand's own words,
  constant quality, name the method, and the specification family forks); equipercentile against linear equating on random
  groups (task450's ground, a moderate stump); Fellegi-Sunter frequency weights (the linker's own error is task468's).
- 2026-10-21, architecture 2 draw, the card's first labels: population, G2 or G12 and method_or_model_selection repeat four
  older builds' signature (test.same_driver_older, test.same_puzzle_older against task142); relabelled G17 with G2 beside
  it and gate etl_conformance, the call being the region's conformed count with the resolution inside it. Then task251 v5
  entered the window and blocked local_government and operations_log: the integrator is the region's nonprofit HMIS lead
  and the context artifact the published point-in-time count.
- 2026-10-21, architecture 2 draw, the prototype (20,000 people over two fiscal years, half of the names drawn from a
  concentrated list): chaining every link left the region 387 short, 115 of the chained groups holding two records of one
  source and 112 holding two people with no such conflict. A merge with no conflict cannot be refuted by anything shipped,
  so the generator keeps every wrong link inside a conflict (no undetectable merge) and gives every partial record its own
  person among the records it links, or the resolved count would differ from the people served by a quantity no method
  can see.
- 2026-10-23, the linkage weights as first drawn (a birth month or day disagreement at -3.0 and -3.5): two different
  people of one name and year who agree on the month or the day alone scored 10.5 to 11.5 and linked, and 35 of 207
  merged groups then split one way under an exact constrained optimum and another strongest first; the disagreements
  weigh -6.0, as they do between true matches, and the generator's tidy step makes every licensed resolution return the
  same people (strongest first under any order of equal links, on FY2026 records only, and every optimum of three
  objectives).
- 2026-10-23, materiality at 24,000 to 30,000 households: the default path moved Halvering's amount by about 18,000
  dollars; 44,000 households, with the City's outreach team also meeting downtown single adults outside the street count,
  give 130 Halvering people and 28,815 dollars.
- 2026-10-23, the bridge as the graded shape (03): its opening items, each source's records with FY2026 service, need no
  linkage, so every response banks them; the graded structure is the allocation's buckets (05).
- 2026-10-23, ask B over households: 147 households moved in twice in FY2026, so an average per household forks; the ask
  is per move-in. Its figures needed placing mid-bin, so the move-in waits are drawn from their own stream after the
  world is fixed, with a knob by Continuum and household type.
- 2026-10-23, ask A's 16 cells beside ask B's 5: one repair (a person's night counted once) gave a solver 16 of 21 ask
  figures; ask B is split by household type, 10 figures.
- 2026-10-23, Melbray's enrollment keys written as E- and six digits: 875 ids collided and exits joined to the wrong
  stays; the vendor's key carries seven digits.
- 2026-10-23, the world's first names (Calvera, Mardell, Ostry, Pellam, Valley Street Medicine, Safe Harbor, Riverside,
  New Hope, Mercy Commons): house fix H21 against a register of U.S. counties, states and cities found Calvera two letters
  from California's Calaveras County and Pellam one from Pelham, with Sartell, Story County, Valley Stream, Safety Harbor
  and New Hope near the rest; renamed Halvering, Melbray, Ondrava, Pyrenna, Wayfarer Street Health, Hearthstone, Elm
  Street and Brightwater, Stepping Stone and Kestrel Commons, with Continuum codes HAL, MEL, OND and PYR chosen to keep
  the old codes' alphabetical order so no draw moved (every figure unchanged, asserted by the rebuild).
