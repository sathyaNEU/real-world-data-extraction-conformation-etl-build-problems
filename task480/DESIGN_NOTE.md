# task480 design note: the 2026 municipal population estimates and the road aid formula's urban tier

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first.

## Draw

Architecture 3, drawn 2026-10-31 after architecture 2 (the vehicle retirement program's NOx counties) was spent at
stage 4 of its 10-30 reship (judge pass 2 SEND_BACK). Card `.claude/skills/fingerprint/cards/task480.json` (v3),
registered 2026-10-31T19:27:22Z; guard check WARN only.

- **Pairing.** Survey Research & Official Statistics / census-register-administrative-data-quality (client domain
  survey-research-official-statistics), objective Data Extraction & Conformation (ETL): a state data center conforms
  the county address points, the certificates of occupancy and demolition permits, the group quarters list and the
  2020 census block groups into the 1 July 2026 municipal population estimates it certifies to the state.
- **Shape 10, a scorecard against a threshold.** Each municipality's estimated residents on 1 July 2026 against the
  10,000 that the state's municipal road aid formula moves to its urban tier; the call is the set of municipalities at
  or over the line.
- **Decision.** designation_set, answer unit set_of_items, question form what; forum the Secretary of Community and
  Economic Development, who signs the aid determination (minister_or_cabinet), forcing event the statutory
  certification of the estimates by 15 December 2026 (statutory_or_regulatory_filing), org family
  research_or_statistics_office, stakeholder the state demographer (statistical_office_head).
- **Strategy.** composition_mix, decisive generator G13 (horizon mismatch): persons per occupied dwelling, measured on
  the 2020 stock, is applied to the 2026 stock it no longer describes; Gate G method_or_model_selection; Layer 2 family
  estimation_fit, pattern own:persons-per-dwelling-by-dwelling-age-in-the-housing-unit-method.
- **Data-native sentence.** A dwelling's household fills when the dwelling is new and thins as it ages: young families
  buy into new subdivisions and their children leave a decade or two later, so persons per occupied dwelling is a
  property of the dwelling's age, not of the place; a municipality's 2020 census average holds the age mix its stock
  had then, and the subdivisions built since 2020 sit in a few municipalities while others' stock has aged.
- **Sources.** The housing unit method (occupied dwellings times persons per occupied dwelling, plus group quarters)
  is the official subcounty estimator and this build's default path; the decisive step is the precondition it takes
  for granted, one persons-per-dwelling figure for a place's whole stock (`stumping` 1.3 and 1.4). Set aside earlier
  on file: the housing unit method as a golden (task176, the textbook at the bottom of the ladder) and dwelling
  completions lagging consents (task174); here the method is the default and its precondition the step.
- **WARNs answered.** shell.repeat reads architecture 2's prompt until this architecture's prompt is written.
- **Differentiation** (card): task229, task242, task476, task174, task461 and task501 share the structural triple
  (time, G13, method_or_model_selection) on cards, each with one line naming how its driver differs.
- **Personas** (`guard.py names --geo "United States" --seed 480`): Laura Rubio, Chad Neal.

- **Shell** (read off `prompt.txt`): question form what, second-sentence opener the, rounding opener report,
  deliverables svg+xlsx; architecture 2's was which, send, give, docx+xlsx.
- **Data-native sentence, as built.** Tamarack County's towns were built in waves of subdivisions (Maple Ford's from
  1997 to 2015, Cedar Run's since 2019), and the household a dwelling holds rises for its first few years and thins over
  the next two decades as the children who came with it leave, so a town's 2020 persons per dwelling is the average of
  its stock at the ages it had in 2020, which is not the stock it has in July 2026.
- **Retrospective date, forward call.** 1 July 2026 has passed, but no count of it will ever exist; the certification
  fixes the tier for the 2027 aid year, a window not yet open (`CLAUDE.md`, the call is forward facing by default).

## Default path

The pipeline a strong analyst builds from the prompt's words and the files' grain, the field's own estimator in it:

1. Read the Act and the program statement: the population is the municipality's residents on 1 July 2026, the persons
   whose usual residence is a dwelling in it on its 1 July boundaries plus its group quarters residents from the 2026
   survey; the urban tier is 10,000 or more.
2. Count each municipality's dwellings standing on 1 July 2026: the roll's living units by parcel, plus the 2026
   certificates of occupancy on lots the roll holds as vacant (each building once), less the dwellings demolished in
   2026 on completed permits.
3. Apply the housing unit method, the official subcounty estimator: each municipality's 2020 persons per dwelling
   (2020 household population over 2020 housing units, from the census history, the Town and the Village of Ivydale
   together) times its 2026 dwellings, which carries the 2020 occupancy and the 2020 persons per occupied dwelling in
   one ratio.
4. Add the group quarters residents from the 2026 survey and compare each municipality with 10,000.

**Ends on:** Dunmore, Juniper and Maple Ford: the 2020 ratio puts the Town of Maple Ford at 10,451 and the Town of
Cedar Run at 9,735.

**Golden:** Dunmore, Juniper and Cedar Run: with persons per dwelling estimated by the dwelling's type and age across
the 2020 block groups and applied at each dwelling's age on 1 July 2026, Cedar Run holds 10,787 residents and Maple Ford
9,611 on the eight-band profile, and 10,348 to 10,813 and 9,013 to 9,623 across the golden family (age bands of three to
ten years, with or without an age profile of its own for each dwelling type, or a fitted life-cycle curve).

## Stump sentence

The default path files Dunmore, Juniper and Maple Ford because step 3 holds each municipality's 2020 persons per
dwelling for July 2026, but a dwelling's household rises for a few years and thins for decades, so the ratio
overstates Maple Ford's 1997 to 2015 subdivisions, now 11 to 29 years old, and understates the 1,600 homes Cedar Run
has finished since the census; estimated by the dwelling's age across the 2020 block groups, Cedar Run reaches 10,000
and Maple Ford does not.

## Three rules

**Task type:** census register administrative data quality (`census-register-administrative-data-quality`), serving
the ETL objective: the assessor's roll, the inspectors' certificate and demolition logs, the census block groups, the
census history and the boundary register conformed into each municipality's dwelling stock and residents on the
estimate date, with the registrar's resident births and deaths placed by address.

**Domain test:** the deciding quantity is each municipality's resident population on 1 July 2026, which an official
statistics office estimates for places between censuses by the housing unit method (dwellings standing times the
persons a dwelling holds, plus group quarters residents), the persons a dwelling holds being the one input a state
data center has to estimate rather than count.

**Swap:** "what municipalities reach 10,000 residents on 1 July 2026" becomes "what wind farms reach 10,000
megawatt-hours in July 2026": a turbine's output has no household that fills and empties over the turbine's life, no
census that measured it by small area and no dwelling stock aging through a life cycle, so the step that decides has
nothing to act on.

**Layer 1:** what these systems produce, none of it on the decisive step.
- The assessor's roll is one row per parcel: a two-family house or an apartment building is one parcel with its
  living units, a townhouse unit its own parcel, a lot whose house came down or is not yet finished vacant land.
- Year built is a calendar year, and a few old houses carry the assessor's placeholder 0.
- Inspectors issue a temporary certificate before the final one on about three buildings in ten, and certificates
  for commercial buildings, accessory buildings and additions sit in the same log.
- Demolition permits include garages, barns and permits that expired with the building standing.
- The census history holds each census's municipalities on that census's boundaries: annexations by tax key, and the
  Town of Ivydale until its 2024 consolidation into the Village.
- The census block group file carries the Census Bureau's two header rows.
- Post offices serve several municipalities each, so the written city on a vital record is often not the municipality.
- The death registration system's January 2026 release codes residence from the address; the earlier release coded it
  from the written city.

**Layer 2:** estimation_fit (persons per dwelling modelled on the dwelling's age across the census's small areas).
A place's average at the last census carries the age mix its stock had then; the expert estimates the per-dwelling
yield by dwelling age across small areas, checks it on the censuses before, and applies it at each dwelling's age on
the estimate date.

**Decisive step:** estimating the persons a dwelling holds by its type and its age across the 2020 block groups (a
cross-sectional fit of each block group's household population on its dwellings counted by age) and applying that
life-cycle profile at each dwelling's age on 1 July 2026, instead of holding each municipality's 2020 persons per
dwelling.

**Not semantics:** every field read right (living units, year built and its placeholder, temporary and final
certificates, completed and expired permits, the census header rows, the boundary register, the survey's residents)
still leaves the persons per dwelling to be estimated, and the default path reads each of them correctly and lands
Maple Ford.

**Not rule application:** no filed rule or procedure says how the persons in a dwelling are estimated; the Act and the
statement file only the residents counted, the date, the boundaries and the group quarters source, so executing
every filed rule still leaves the analyst at the housing unit method's default. The enumerated family (the 2020 ratio,
persons per dwelling by type, the 2010 to 2020 trend, persons per dwelling by year built, the age profiles) spreads
Cedar Run from 9,311 to 10,944 and Maple Ford from 8,700 to 10,451 and files four different sets; the standing family
(nine age profiles: bands of three to ten years, each with and without type-specific profiles, and a fitted curve)
spreads Cedar Run 10,348 to 10,813 and Maple Ford 9,013 to 9,623 and files one; the ruling-out is quiet: no sentence or column does it, only the backcast the
analyst has to build (on this build's stock the age profile reproduces the 2010 and 2000 household populations at a
mean error of 1.7 and 2.0 per cent, the 2020 ratio at 4.5 and 6.5, persons per dwelling by year built at 7.4 and 13.5;
the judge's own rebuild measured the profile at 2.3 to 3.7 and the ratio at 3.8 and 6.4, the same order).

**Analyst test:** a strong analyst who counts the 2026 dwellings correctly and applies the housing unit method with
each municipality's 2020 persons per dwelling files Dunmore, Juniper and Maple Ford (Maple Ford 10,451, Cedar Run
9,735, the default path's `Ends on:`); modelling persons per dwelling on dwelling age files Dunmore, Juniper and Cedar
Run.

**Estimand:** the Municipal Road Aid Act, s. 84.21 (4) and (6) (`municipal_road_aid_act_excerpt.pdf`): the population
is the number of residents on 1 July of the year before the aid year as certified by the state data center, and an
urban municipality has 10,000 or more; the Center's program statement, section 2
(`municipal_estimates_program_statement_2026.pdf`): the persons whose usual residence on 1 July is a dwelling within
the municipality's boundaries in force that day, plus the residents its group quarters survey records.

**No decoy:** nothing is planted to be caught: no memo, prior estimate, consultant's table or stakeholder figure states a
persons per dwelling, a municipal estimate or a tier, and the census history and block groups are the counts the
census published.

**No certified replay:** no shipped figure is reproduced to recover a method: nothing certifies a 2026 estimate or a
persons-per-dwelling figure, and the earlier censuses check the profile out of sample rather than calibrate it.

**Lesson:** the yield a stock of units carries is a property of each unit's age, not of the place, so a place's
census average carried forward misses wherever the stock's age mix has moved since; no build on file teaches it (the
housing unit method was spent as a golden in task176 and the permit-to-completion lag in task174).

## Survivor anatomy

Actor: the deciding property, the persons a dwelling holds at its age, has no column in any file: the roll holds year
built, the census holds each block group's household population, and the relation between them is stored nowhere; the
only per-place ratio the files give (the 2020 household population over housing units) is the default's.

Link: the signal is read by counting the roll's dwellings by age inside each 2020 block group (CENSUS_BLOCK_2020) and
fitting the block groups' household population on those counts, a cross-file comparison the housing unit method never
asks for, since it asks for one ratio per place; no sentence invites it.

Reflex: the field's named estimator for the quantity, the housing unit method with each municipality's 2020 persons per
dwelling, is rung 0 and files Dunmore, Juniper and Maple Ford; its standard refinements (persons per dwelling by type,
the census-to-census trend) also file wrong sets.

Back-test: the textbook route validates on the checks a solver runs on it: the 2020 ratio reproduces every
municipality's 2020 census from the 2020 stock exactly, and its county total for July 2026, 101,957, sits on the
Census Bureau's Vintage 2025 county path (100,413 in July 2025, rising about 1,375 a year) as closely as the golden's
101,370; the record that refutes it is the municipal backcast to 2010 and 2000, which the method never asks for.

Second use: every file the decisive step reads sits in the pack for its own reason: the roll, the certificates and the
demolitions are the dwelling count the housing unit method needs anyway, the 2020 block groups and the census history
are the census base every estimates office holds, and the boundary register sets the boundaries; delete the decisive
step and no file drops out.

Shock: the movement the step recovers reads as ordinary: Cedar Run's growth is plain in the certificates and the
default already adds it at the 2020 ratio, and Maple Ford's loss has no event at all; the golden three are no top
three of the 2020 population (Juniper, Dunmore, Maple Ford), the 2026 dwellings (Dunmore, Juniper, Fallon), the births
(Cedar Run, Dunmore, Harwick), the deaths (Dunmore, Juniper, Fallon) or the dwellings added since 2020 (asserted in
`checks.py`); risk recorded: Cedar Run adds the most dwellings since 2020, so an analyst who simply believes the
fastest-growing town is undercounted moves it without the method, and Maple Ford still stays in.

Pins: the Act (s. 84.21 (4), (6)) and the program statement (section 2) file the WHAT: residents on 1 July of the year
before the aid year, usual residence in a dwelling inside the 1 July boundaries, the group quarters survey's residents,
10,000 or more; no filed sentence names persons per dwelling, dwelling age, a census ratio, a block group or a method,
and deleting any one of them leaves the call where the data put it.

## Readability screen

| Rung | 1 filed sentence | 2 schema | 3 reflex | 4 control bench | 5 battery | 6 linear | 7 dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| Each municipality's 2020 persons per dwelling (the default) | no | fires: the census history's household population and housing units sit side by side | fires: the housing unit method as the field states it | no | no | fires: one ratio per place | no | readable |
| Persons per dwelling by type, county-wide | no | fires: the roll's land use codes | fires: the method's standard refinement | no | no | no | no | readable |
| The 2010 to 2020 trend in persons per dwelling carried to 2026 | no | fires: three censuses in one workbook | fires: a census-to-census trend | no | no | fires: one extrapolation | no | readable |
| Persons per dwelling by year built, held for 2026 | no | fires: YEAR_BUILT on every roll row | no | no | no | no | no | readable |
| (decisive) Persons per dwelling by the dwelling's age across the 2020 block groups, applied at each dwelling's 2026 age | no. No sentence names persons per dwelling, age, a block group or a fit; the statement files only who is counted | no. No column holds a dwelling's household or its age effect; year built is a date and the block code a location | no. Every reflex of the method lands wrong (the 2020 ratio, by type, the trend) | no. The Census Bureau's county estimates tie under every basis; nothing ranks the municipalities | no. The battery (duplicate certificates, expired permits, placeholders, header rows, boundaries) comes back clean on the wrong path | no. A fit across 111 block groups and eight age bands applied to 49,000 dwellings | no. Every file has its own use (Survivor anatomy, Second use) | silent |

The decisive quantity is named by no sentence and no column, every reflex of the field's method lands wrong, no
control sees it, and the battery is clean. It is the record's own structure: the 2020 block groups' household
population rises and falls with the age of the dwellings they hold, and only an analyst who asks what a dwelling's
household does as the dwelling ages finds it.

## Semantic fork table

One row per term of the main ask and per convention its computation rests on, and for the asks' residence. The calls
are measured on the build by `checks.py`.

| Id | Term or convention | Golden reading | Alternative reading | Call under the alternative | Ruled out by |
|---|---|---|---|---|---|
| SF1 | residents | usual residents of the municipality's dwellings plus the group quarters survey's residents | household population alone | refused | program statement, section 2 ("the persons whose usual residence on that date is a dwelling in the municipality, and the residents of its group quarters") |
| SF2 | on 1 July 2026 | dwellings standing on 1 July (certificates through 30 June) | standing on 30 June | same call (asserted) | the Act, s. 84.21 (4) ("on July 1 of the year before the aid year") |
| SF3 | the municipality | on its boundaries in force on 1 July 2026 (the 2021 annexation in Juniper) | on the 2020 census boundaries | same call (asserted) | program statement, section 2 ("within the municipality's boundaries in force on 1 July") |
| SF4 | reach 10,000 | 10,000 or more | more than 10,000 | same call: no estimate within one resident of the line (asserted) | the Act, s. 84.21 (6) ("whose population is 10,000 or more") |
| SF5 | group quarters residents | the survey's residents on 1 April 2026 | its licensed beds | same call (asserted) | program statement, section 2 ("those recorded ... by the Center's annual survey of group quarters") |
| SF6 | group quarters residents | the 2026 survey | the 2020 census group quarters | same call (asserted) | program statement, section 2 |
| SF7 | household population in 2020 | P15_001N, population in households | P1_001N, total population, with the survey added again | same call (asserted) | the block group file's own label row ("Population in households") |
| SF8 | a dwelling's completion | its first certificate, temporary or final | its final certificate only | same call (asserted) | same call |
| SF9 | a demolition | a completed permit | any permit issued | same call (asserted) | the permit's STATUS and COMPLETED |
| SF10 | year built 0 | an old house kept in the oldest band | dropped | same call (asserted) | same call |
| SF11 | a dwelling's age from its year built | mid-year of the year built | the start of the year | same call (asserted) | same call |
| SF12 | a dwelling's age from its year built | mid-year of the year built | the end of the year | same call (asserted) | same call |
| SF13 | dwellings standing on 1 July 2026 | the roll plus the 2026 certificates on vacant lots | the roll of 1 January alone | same call on the eight-band profile (asserted); refused | program statement, section 2 (usual residence "on that date") |
| SF14 | a written city of residence | a post office's city | a municipality's name | asks only: every written city is a municipality's name, so the reading is computable (asserted) | the address points' POSTAL_CITY beside MCD |
| SF15 | a birth's municipality | the municipality the residence address lies in (the address points' MCD) | the written city | asks only: every municipality's births move by 4 or more (asserted) | program statement, section 3 ("in the municipality in which the mother lived"); the address points |
| SF16 | a death's municipality | the residence address's municipality | the written city | asks only: every municipality's deaths move by 3 or more (asserted) | program statement, section 3; the address points |
| SF17 | a death's municipality | the residence address's municipality | the registrar's residence code | asks only: every municipality's deaths move by 3 or more (asserted) | the code is the written city's on every death before 1 January 2026 and the address's after (asserted) |
| SF18 | a birth | each live-born infant (twins two records, two births) | each delivery | asks only: refused | program statement, section 3 ("each live-born child one birth") |

## Ladder

Measured on the build (`generator/figures.json`, `rungs`), Cedar Run and Maple Ford, residents on 1 July 2026:

| Rung | Construction | Cedar Run | Maple Ford | Set filed |
|---|---|---|---|---|
| 0 | the housing unit method with each municipality's 2020 persons per dwelling (the default) | 9,735 | 10,451 | Dunmore, Juniper, Maple Ford |
| 1 | persons per dwelling by type, fitted on the 2020 block groups | 9,717 | 8,700 | Dunmore, Juniper |
| 2 | the 2010 to 2020 trend in each municipality's persons per dwelling carried to 2026 | 9,311 | 10,195 | Dunmore, Juniper, Maple Ford |
| 3 | persons per dwelling by year built (2020 block groups), each dwelling holding its 2020 level | 10,944 | 10,247 | Dunmore, Juniper, Cedar Run, Maple Ford |
| 4 | the golden: persons per dwelling by type and age across the 2020 block groups at each dwelling's 2026 age (eight bands: 10,787 and 9,611) | 10,348 to 10,813 | 9,013 to 9,623 | Dunmore, Juniper, Cedar Run |

Every other municipality stays at least 400 below the line on every rung but rung 1 (Fallon 9,887 there), and Dunmore
and Juniper at least 2,000 above (asserted).

## Closure table

| # | Axis | Reading chosen | Closure |
|---|---|---|---|
| 1 | Population | usual residents of the municipality's dwellings plus its group quarters survey residents | filed (statement, 2); SF1 |
| 2 | Unit of account | the municipality; the dwelling unit within it | filed (Act, 84.21 (3), (4)) |
| 3 | Attribution window | residence on 1 July 2026; births and deaths dated 1 July 2025 to 30 June 2026 | filed (Act, 84.21 (4); statement, 3); SF2 |
| 4 | As-of dating | dwellings standing on 1 July 2026; the roll of 1 January plus the certificates and demolitions to 30 June | filed (statement, 2); SF13 |
| 5 | Version basis | a building's first certificate, temporary or final | C1: SF8 asserted |
| 6 | Divisor and denominator | none in the call; the persons per dwelling fitted per dwelling, vacancy inside it | C1 on the golden family |
| 7 | Weighting | ordinary least squares on block groups | C3: the band sets and the fitted curve file the same three (asserted) |
| 8 | Measurement window length | the estimate date; one year for the vital events | filed |
| 9 | Boundary inclusivity | 10,000 or more | filed (Act, 84.21 (6)); SF4 |
| 10 | Rounding path | the tier from the unrounded estimate; births and deaths whole counts | filed (the prompt); C1 |
| 11 | Tie-break | none | not applicable |
| 12 | Maturity and censoring | the 2026 completions counted at their certificates | filed (statement, 2); SF13 |
| 13 | Order of operations | the stock, the fit, the 2026 application, the group quarters added | C1 |
| 14 | Row order | order-free | C1 |
| 15 | Duplicate resolution | one completion per building (temporary and final certificates once) | SF8 asserted |
| 16 | Identity normalisation | tax keys as the roll issues them; annexed parcels by their current key and prior key | filed (the boundary register) |
| 17 | Netting against gross | demolitions netted on completed permits | SF9 asserted |
| 18 | Dimensional units | persons and dwelling units | C1 |
| 19 | Code and status semantics | land use codes, certificate types, permit statuses, the census labels | the files' own descriptions; SF7 |
| 20 | Integerisation | whole residents compared unrounded | C1 |
| 21 | Scope of a stated clause | s. 84.21 (6) applies to each municipality on its own population | filed |
| 22 | Forward window contents | the 2027 aid year follows the certified population; nothing after 1 July 2026 enters it | filed (Act, 84.27 (2), (3)) |
| + | Persons per dwelling | by type and age across the 2020 block groups | the method, never filed; C3 across the golden family, the backcast separating it from every rung (asserted) |

## Literal reader

The prompt, the Act and the program statement, executed word for word, fix the estimand: the persons whose usual
residence on 1 July 2026 is a dwelling within each municipality's boundaries in force that day, plus the residents the
2026 survey records for its group quarters, compared with 10,000 or more (SF1 to SF13). No filed sentence says how the
persons a dwelling holds are estimated. The data force it: the 2020 block groups' household population rises and falls
with the age of the dwellings they hold, and the profile fitted to them reproduces the 2010 and 2000 censuses'
household populations from the dwellings standing then at a mean error of 1.7 and 2.0 per cent, where each
municipality's 2020 ratio misses by 4.5 and 6.5 per cent and persons per dwelling by year built by 7.4 and 13.5. The
default's three come from the method, not from a reading. The asks' readings: a birth or death is placed where the
mother or decedent lived (statement, 3), and the address points carry each address's municipality beside its post
office's city (SF14 to SF17).

## Oracles

- **What ships no figure.** No file states a 2026 estimate, a persons per dwelling, a tier or a prior certification;
  nothing ranks the municipalities against 10,000.
- **The Census Bureau's county estimates** (distractor). A county total ties under every basis: the default's July 2026
  county total (101,957) and the golden's (101,370) both sit on the Bureau's path, and no municipality appears in it.
- **The Department of Transportation's road miles** (distractor). A formula factor the Department certifies on its own
  (84.23 (2), (3)); unused by the call and the asks.
- **The census history.** It shows each municipality's household population and housing units at three censuses; read
  as a trend it lands rung 2, and only the backcast built from the dwelling stock separates the readings.
- **The asks' referee: the address points.** They give each address's municipality beside its post office's city and
  arbitrate the births and deaths without naming a count; the call never reads them.

## Ask sheet

**The main call's declared population:** the roll, the certificates of occupancy, the demolition permits, the 2020
block groups, the census history, the boundary register and the group quarters survey. Zero ask device rows in it: the
births, the deaths and the address points are read by no step of the call, and deleting them leaves the call (they
enter neither `methods.stock` nor `methods.rungs`).

**Ask A: each municipality's resident births from 1 July 2025 to 30 June 2026** (14 figures, whole counts; statement,
3: a birth by its date, in the municipality in which the mother lived).
- H18 home: the Center reports each municipality's births beside its estimate, a measure every municipality carries
  that the call does not turn on.
- Use: the Center's components report and the municipalities' own planning read the births.
- Primary device, D7 (the true key elsewhere): the birth record's RES_CITY is the city the mother writes, the post
  office's in most towns (every written city is some municipality's name, so the tabulation by city is complete and
  plausible); the municipality comes from the residence address on the county's address points.
- Hazards: twins are two records (each infant a birth); out-of-window births filed in July 2025 (dated by birth, not
  filing); suffixes spelled out or abbreviated and units written three ways (normalised right).
- Path: births_tamarack_residents_2025-2026.csv (CHILD_DOB, RES_STREET, RES_CITY, RES_ZIP) to
  tamarack_address_points_2026-07.csv (ADD_NUM, ST_NAME, ST_TYPE, MCD, POSTAL_CITY) with the statement. Three files.
- Stops: golden (address points); the written city, Dunmore 190 against 111 and Harwick 52 against 101; the ZIP code's
  post office, the same.
- Realism: mothers write their mailing city; post offices do not follow municipal lines.

**Ask B: each municipality's resident deaths from 1 July 2025 to 30 June 2026** (14 figures, whole counts; statement,
3: a death by its date in the municipality in which the decedent lived, a group quarters resident in the facility's).
- H18 home: the Center reports each municipality's deaths beside its estimate.
- Use: as Ask A.
- Primary device, D2 (a label stored before a silent switch): RES_MCD_CODE is the registrar's coded municipality, taken
  from the funeral director's written city on deaths before the January 2026 release and from the address after; read
  as the municipality it moves every figure (Dunmore 270 against 244, Glenmoor 15 against 29).
- Hazards: the written city (a second wrong reading, D7's cause shared); nursing facility decedents at the facility's
  address; out-of-window deaths filed in July 2025.
- Path: deaths_tamarack_residents_2025-2026.csv (DATE_OF_DEATH, RES_STREET, RES_CITY, RES_MCD_CODE) to the address
  points. Two files.
- Stops: golden (address points); the registrar's code; the written city.
- Realism: a registry release that recodes a field from a date leaves the earlier records as they were coded.

**Hazard table.** The post offices' cities (both asks: the cause the two devices share). Twins and out-of-window filings
(repaired right). Facility addresses (repaired right).

**Cracker sheet.** The cracker lands the call, runs the hygiene battery and executes every filed rule; for the asks it
places births by their written city and deaths by the registrar's residence code (`generator/ceiling.py` on the cut pack).

| Row (cracker) | Cracker's figure | Golden | Verdict |
|---|---|---|---|
| births Dunmore | 190 | 111 | miss |
| births Juniper | 139 | 98 | miss |
| births Cedar Run | 129 | 167 | miss |
| births Maple Ford | 55 | 84 | miss |
| births Ashgrove | 38 | 57 | miss |
| births Barrow | 39 | 35 | miss |
| births Elk Prairie | 9 | 18 | miss |
| births Fallon | 131 | 86 | miss |
| births Glenmoor | 45 | 64 | miss |
| births Harwick | 52 | 101 | miss |
| births Ivydale | 47 | 40 | miss |
| births Kessler | 13 | 26 | miss |
| births Lorne | 49 | 22 | miss |
| births Northfield | 42 | 69 | miss |
| deaths Dunmore | 270 | 244 | miss |
| deaths Juniper | 216 | 182 | miss |
| deaths Cedar Run | 63 | 72 | miss |
| deaths Maple Ford | 44 | 64 | miss |
| deaths Ashgrove | 22 | 37 | miss |
| deaths Barrow | 116 | 104 | miss |
| deaths Elk Prairie | 17 | 24 | miss |
| deaths Fallon | 146 | 138 | miss |
| deaths Glenmoor | 15 | 29 | miss |
| deaths Harwick | 28 | 40 | miss |
| deaths Ivydale | 55 | 51 | miss |
| deaths Kessler | 15 | 22 | miss |
| deaths Lorne | 49 | 37 | miss |
| deaths Northfield | 14 | 26 | miss |

**Mirror sheet.** The mirror stops at the default (Dunmore, Juniper, Maple Ford) and takes the same readings: it misses
all 28 ask rows, keeping the chart's two asked parts, a bar for each municipality and the 10,000 line (2 of 30 ask
criteria).

**The full includer.** A response that places every birth and death by address keeps all 28; nothing in the pack
announces the post offices' reach, so it is a response that already knows vital records are geocoded, and it is
priced here as the asks' known exposure.

Mirror leakage: 6.7 per cent of ask weight.

Pair ceiling: 32.2 (the cracker 38 + 7 + 55 x 2/30 = 48.7, keeping the chart's two asked parts and none of the 28 ask
figures; the mirror 5 + 7 + 55 x 2/30 = 15.7).

Measured by: generator/ceiling.py on the cut pack.

## Leak check

`leak.py --asof 2026-10-30` REVIEW with no LEAK: sweep 4 (the program statement carries the estimand's own words;
ruled harmless in the report) and sweep 6 (five record files name municipalities beside numbers and rank nothing; the
reader ruled each harmless). The reader read three times (the second after the prompt changed, the third after the
statement changed): no sentence names the decisive step, no file ranks or helps, Q6 an analytical choice each time; its
twins point closed by the statement's section 3, its realism points fixed (no placeholder state code, each facility on
its own street, varied street names, the census history authored by the Office).

## Determinism judge

Pass 3 (`determinism_check_report_pass3.md`): DETERMINISTIC, FIX_NOW. Gate G method_or_model_selection,
analytical_non_defect, surface_read_dependency no; Gate H pass. Fixed: the chart answer's dark bars, the backcast errors
stated as an ordering, births and deaths as whole counts. Pass 4 (`determinism_check_report_pass4.md`, the one
re-judge): DETERMINISTIC, FIX_NOW on solution wording only: the eight-band figures reproduce once the solution files the
four dwelling types by land use code and the placeholder year, now in steps 1 and 2; the thread's own 24 variants put
Cedar Run at 10.4k to 11.1k and Maple Ford at 9.2k to 9.5k, the same call. Residual risk both passes name: no sentence
files a selection criterion, so the call rests on the solver running the backcast (a filed back-test is barred here by
the two builds before it).

## Pre-ship check

- **2026-10-31 ship of architecture 3 (target.zip 957b43dae6f8e26f).** Free gates on the final cut: checks 255, verify
  agreeing, two byte-identical builds, figures_check 43 of 43, precut 0 FAIL 0 WARN, voice-check clean (what, for,
  report, svg+xlsx), leak.py REVIEW with no LEAK, ceiling.py pair 32.2 and mirror leakage 6.7, guard.py surface exit 0
  and heart WARN.
- **Three rules, re-read on the built pack.** The domain decides (the housing unit method's per-dwelling yield, modelled
  on dwelling age); Layer 1 is what the assessor's, the inspectors', the census's, the registrar's and the county's own
  systems write and decides nothing; the decisive step is analytical: the analyst who conforms every file and applies the
  method with each municipality's 2020 persons per dwelling files Maple Ford in place of Cedar Run (asserted on the
  clean truth), and only a dwelling-age profile, checked against the earlier censuses, files the golden three.

## Tried and rejected

- 2026-10-20, at the draw: the seed's own quantity, each NUTS 2 region's GDP per head in PPS against 75 and 100 per
  cent of the EU-27 average: every input (regional GDP, average population, national PPPs, the EU average) is a
  published aggregate, so the categorisation is arithmetic once the NUTS version, the average and the vintage are
  read; the seed's three moves are data semantics and rule application by construction.
- 2026-10-20, at the draw: putting an estimate into the seed's quantity: rebuilding regions across a NUTS boundary
  that splits a NUTS 3 unit is task474 v1's and task476 v1's spent split driver; a nowcast of the latest year's
  regional GDP is Forecasting with an open estimator family; carrying the national statistics institute's coming
  benchmark revision into the regional figures through the overlap years recovers the institute's method from its
  own published vintages (a certified replay); a register's population over-coverage is the census-register ground
  task471, task448 and task455 have spent.
- 2026-10-20, at the draw: other worlds screened before this one: attendance rebuilt from tickets by a show-up rate
  conditioned on booking lead time (composition_mix sat in the ban window behind task481, and a yield conditioned
  on a per-case property and measured where the record is complete is task473's driver); length of stay from
  stock over entries by Little's law (one divide, readable); weekly overtime from biweekly totals (the after-migration
  ratio per site lands the golden); direct-store-delivery shortages against theft (the warehouse-supplied categories
  are an unaffected subset that ranks stores with no model); a pooled percentile from published percentiles (the
  "never average percentiles" reflex reaches the mixture).
- 2026-10-20, stage 2: the under-registration rising with meter age, fitted by age: linear, quadratic and banded fits
  of a slope of 0.3 points a year moved the town-centre zones' indices by 0.05 to 0.1 across forms, so the graded
  indices forked; the meters' error is now one level for the mechanical fleet, varying meter to meter.
- 2026-10-20, stage 2: the town-centre flats exchanged last and the suburbs first with only a class-level summer:
  every pooled control landed within 0.5 points of the golden by composition (already-exchanged suburbs match the
  exchanged suburbs), so the first reflex reached the call; the rollout now opens and closes on town-centre zones and
  2024 was a normal year, so every pooled and tariff route over-corrects.
- 2026-10-20, stage 2: route reads spread nine days either side of the quarter end with estimated reads at 4 per
  cent: the smeared mechanical quarters put the per-meter averages 0.4 to 1.0 points under the volume share and pulled
  the tariff route's per-meter median onto the golden; reads now fall within three days of the quarter end and 1.5
  per cent are estimated.
- 2026-10-20, stage 2, asks: contracts in force at the end of 2025 (no device a reader would not adjudicate from the
  status and date columns); mains failures across a work-management cutover (migration duplicates are executed by
  the hygiene battery, proven-in-production Part 2); asbestos-cement length across a material-code renumbering (the
  old code book is nowhere in the pack, so the device is not fair).
- 2026-10-21, architecture 1 spent at stage 4 (the water utility's zone leakage index, the old meters'
  under-registration read across the staggered smart-meter exchange against same-type premises whose meters did not
  change): scored leak reader 2 landed the call, eight zones at 4.3 per cent, by netting each exchanged meter's step
  against unchanged premises of the same type and checking it with a placebo, and reader 1 filed seven with type
  controls stratified by consumption band, so the matched comparison is a medium reader's reflex once a staggered
  rollout is visible; both readers kept all 32 ask figures (the SCADA UTC stamps fell to the daylight-saving shift of
  the night profile, the GIS 2008 install-year placeholder to its spike and the works register); the judge returned
  DETERMINISTIC with FIX_NOW on the 4.3 per cent figure, whose estimator family spans 3.5 to 4.5 per cent against a
  printed unit of 0.1. Re-rooted fresh by the author's rule: no staggered rollout or treated-against-untreated
  comparison in the new world, every graded figure printed at the precision its estimator family supports, and no ask
  device a clock profile or a value spike can find.
- 2026-10-21, stage 2: the 2027 program's model years 2001 to 2010: their 2027 ages, 17 to 27, sit at the thin old end
  of the readings, where an exponential decay of yearly miles fits the one-year means as well as the quadratic
  (chi-square 33 against 33 on 27) and puts every county 4 to 5 per cent higher, so the whole tons forked across
  forms the record cannot separate; the program now takes model years 2005 to 2014, whose 2027 ages lie inside the
  bulk of the readings, and the fifteen-member family agrees in every county.
- 2026-10-21, stage 2: first sales centred three months before the model year began: the cumulative curve then has an
  intercept, and fits through the origin or of the lifetime average moved every county by 4 to 7 per cent; first
  sales now centre on 1 January of the model year.
- 2026-10-21, stage 2: county-by-county curves on the counties' first random draws spread up to 9 per cent around the
  pooled curve; each county's draw is now the one whose own curve agrees with the pooled one, and its intensity sets
  its level mid-bin.
- 2026-10-21, stage 2, asks: station numbers given again only between counties whose drivers do not cross left three
  counties' counts unchanged under the current licence; each reissued pair now shares a commuting corridor.
- 2026-10-21, stage 2: a lane computer's re-sent March 2025 rows (exact repeats at one station): a copied block is a
  plant kind even when the call ignores it; removed.
- 2026-10-21, stage 4 round 1, ask B: the station register's licensed_since column: both scored readers compared each
  test date with it, took the 2024 report's county before it, and kept all twelve station figures (score_reader 20 of
  44 each, call missed by both on the default path); the register now carries no licence date, so the reissue is a
  cross-file conflict and the hand-over is the pause in the number's own tests.
- 2026-10-21, stage 4 round 2, ask B: with no licence date on the register, reader C still split each reused number
  at the pause in its tests and kept all twelve station figures, and reader D kept seven from the 2024 report's
  closure dates; a station number reused across counties is a map every careful reader reconciles, so the station
  ask is retired, the register stays as a declared distractor, and the ask layer is the pilot (0 of 8 for all four
  readers).
- 2026-10-31, architecture 2 spent at stage 4 of its 10-30 reship (judge pass 2, `determinism_check_report_pass2.md`):
  NOT_DETERMINISTIC and SEND_BACK. Guidelines 3.3 file the reading as the evidence and no criterion selects the
  cumulative curve's form: a linear cumulative fit files six counties (Dunmarsh at 10.29 tons) against the golden's five,
  though the readings reject it (chi-square 5,820 against 30), and the pilot ask's "retired" (679 against 741) rests on
  a code meaning. The first judge (10-21) had approved with both as watch items. The sentence that would close the first
  fork names the decisive step (a fitted mileage curve), so the fork is the stump and the slot re-roots.
- 2026-10-31, stage 2: a filed back-test criterion (the profile chosen by how well it carries one census to the next):
  task130 and task156 directly before this draw both ride a filed back-test, which `determinism-check` §1 bars in
  consecutive builds; the earlier censuses ship as the census history every estimates office keeps, and the backcast
  is the analyst's to build.
- 2026-10-31, stage 2: block groups chunked by building order alone made every 2026 dwelling of Cedar Run's new
  subdivisions a block group with no 2020 population; a block group holding fewer than 120 dwellings in 2020 now joins
  its neighbour, so the new subdivisions sit in block groups the census measured.
- 2026-10-31, stage 2: the golden set was the top three municipalities by 2026 dwellings (Dunmore, Juniper, Cedar Run)
  and by births; Fallon now holds an apartment district of 1966 to 1983 and Harwick a larger subdivision since 2018, so
  neither sort names the golden three.
- 2026-10-31, stage 2: Cedar Run's golden margin rested on its 2026 completions (the roll alone put two band sets under
  10,000); its 2019 to 2026 era was raised so the eight-band profile holds on the roll alone (SF13) while the default
  stays 265 under.
- 2026-10-31, stage 2, asks: mothers writing their municipality four times in ten made Dunmore's births by written city
  2.3 times its true count, a birth rate a demographer would question; the share is now two in three and every figure
  still moves by 4 or more.
- 2026-10-31, stage 4, judge pass 3 FIX_NOW (DETERMINISTIC): the chart answer named dark bars the prompt never asked
  for (dropped; the chart's asked parts are the bars and the line); the critical components' backcast errors to one
  decimal did not reproduce on the judge's own rebuild (2.3 to 3.7 against 1.7 and 2.0), so they are stated as an
  ordering, and the estimates as the eight-band figures with the family's sides; "whole counts of the events" left a
  twins-as-one-delivery reading open, so the prompt asks for whole counts of births and deaths (SF18). The judge's type
  by age interactions widened the family to nine members, all filing the golden three.

- 2026-10-31, stage 4, the reader's second read: it still read twins as open (no sentence said a birth is a child), so
  the program statement's section 3 now counts each live-born child one birth; the census history's author is the
  Office, not the estimates manager, so the Center's files do not all read as one hand.
