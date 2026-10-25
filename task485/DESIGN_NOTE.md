# task485 design note

Status lives in `pipeline.json`; this note holds the design. Architecture 1, drawn 2026-10-25. The seed (ET42, an
employer index of entry-level wage reliance from H-1B labour condition applications) was screened at the draw and its
world set aside (`## Tried and rejected`); the slot is re-worlded, as this lane's task482 and task484 were, into a
boundary commission's electoral review, keeping the seed's shape of a designation read from a conformed
administrative register whose records are not yet the thing the decision counts.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task485.json` (architecture v1), registered 2026-10-25 after a fetch of
  main. The window the axis bans read (task184, task302 and task301, the live cards filed last) closes the strategies
  informative_censoring, causal_design and population_selection, the forums council_or_assembly, line_manager_or_team
  and executive_team, the forcing events period_close, cutover_or_migration and budget_or_appropriation, the
  organisations local_government, retailer_or_ecommerce and foundation_or_funder, the roles programme_officer,
  operations_director and research_desk, the context artifacts planning_thread, other and register, and the shape
  other. The draw's honest labels clear all of them: the decision is the Commission's, not the council's (a national
  boundary commission, government_agency; its members agree the areas its draft recommendations address at a
  meeting, committee_or_panel and vote_or_meeting), the requester is its review manager for the district
  (policy_adviser), and the stakeholder's own file is its technical guidance on electorate forecasts
  (filed_standard).
- **WARNs answered.** `test.same_puzzle_older` (time, E, designation_set against task235 and task445) and
  `test.same_driver_older` (time, E, etl_conformance against task481) are differentiated on the card: none of them has
  a unit whose count builds up toward a settled level over rounds after it is created, or a forecast that has to age
  units that do not yet exist to the horizon. `overuse.org_family` (government_agency in 40 builds): the Commission is
  the body that decides a warding pattern, and the council's electoral services only supply the data.
  `repeat.question_form` (which, against task302 and task301): the Commission names the wards whose pattern it must
  change, so the question asks which.
- **Pairing:** Survey Research & Official Statistics, task type `census-register-administrative-data-quality`, which
  serves ETL: six published registers at property level in two election management system layouts, the old system's
  notices of alteration, the address register, the council's completions monitoring and housing trajectory, and the
  polling district and ward schedules, conformed into each ward's electors on the register to be published after the
  2032 canvass.
- **The decision and the quantity:** an unnamed UK-like country with individual electoral registration and an annual
  canvass, whose Local Government Boundary Commission reviews a district of 23 wards and 43 councillors, last warded
  by the 2014 order. The Commission bases a warding pattern on the electorate five years after its final
  recommendations (due June 2027): the electors on the register to be published on 1 December 2032. A ward whose
  electors per councillor on that register would lie more than 10 per cent from the district's average fails the
  Commission's electoral equality test, and its pattern must change. At its meeting of 17 November 2026 the Commission
  agrees which of the 23 wards fail at today's boundaries and councillor numbers, and the draft recommendations
  address those.
- **Timing (the pack's present is October 2026).** Registers published 1 December 2020 to 2025: Electra held 2020 and
  2021 and was switched off on 4 March 2022 (its reports exported that day, the 2020 report from its archive of that
  register as published, the 2021 report from the register it then held); the new system holds 2022 to 2025. The
  polling district review took effect with the 2023 register (the 2022 register in the new system still carries the
  2014 scheme's districts). Completions monitoring and the trajectory to 30 September 2026; the address register
  extract of 12 October 2026; the Commission's letter of 2 March 2026 fixing the dates.
- **Shape:** `10`, a scorecard against thresholds: each ward's 2032 electors, its electors per councillor and its
  variance from the average against the 10 per cent line, beside the call and the finding for each ward, with one
  ask of 23 figures on the old system's last register.
- **The default path holds the field's method (stumping 1.1b).** Conform the 1 December 2025 register to wards, add
  every dwelling first in use since its last alteration and every dwelling the council's trajectory places before the
  2032 register at the settled stock's electors per dwelling (by dwelling type, from the 2025 register over the
  dwellings in use), keep each existing dwelling at its 2025 count, and test each ward's variance. That is the method
  the Commission's guidance describes in general terms (the dwellings in use today and the new dwellings the
  trajectory expects) and the one an electoral administrator builds first.
- **The decisive step:** that method's precondition is that a dwelling's electors are on the register at the settled
  ratio from the canvass after it is built. They are not: a household joins the register over the canvasses after it
  moves in (the completeness-by-length-of-residence the electoral field measures), so the estates completed since
  2024 hold well under their settled electors on the 2025 register and will reach them by 2032, while the dwellings
  the trajectory places in 2030 to 2032 will still be young at the 2032 canvass. The registers' own canvasses show
  each completion cohort's electors per dwelling rising canvass by canvass toward the settled stock's; ageing every
  dwelling, built or to be built, to its number of canvasses on 1 December 2032 moves wards across the 10 per cent
  line in both directions. A uniform completeness factor (the national share of adults on the register) moves no
  ward, since every variance is a ratio to the district's own average.
- **Data-native sentence:** on the registers' own property rows, a dwelling holds 0.45 of the settled stock's
  electors per dwelling at its first canvass, 0.69 at its second and 0.83 at its third, so the 2,089 dwellings
  Lorrimere West, Caldenstow Park and Quenbrook completed from April 2024 are counted on the 2025 register at about
  half what they will hold in 2032, and the 861 the trajectory places at North Lorrimere and Tibberfield Fields from
  April 2030 will hold well under it then.
- **People:** drawn with `guard.py names --geo uk --seed 485` (Maurice Evans, Megan Stewart, Jean Grant, Donald
  Hayes, Conor Porter, Gordon Hope): Megan Stewart, the Commission's review manager for the district and requester;
  Donald Hayes, the district's electoral services manager who supplied the data. Owners in file properties and
  sign-offs only.

## Three rules

Task type: Survey Research & Official Statistics, census-register-administrative-data-quality, which serves ETL in the taxonomy (registers conformed across two system layouts, an address register and a planning trajectory into an electorate the register only partly holds yet).
Domain test: the quantity that decides is each ward's electors on the register to be published after the 2032 canvass, against the district's average electors per councillor; electoral statistics measure a register's completeness by the elector's length of residence, and the field's forecast adds new dwellings at an electors-per-dwelling ratio, so the decisive analysis is the register's coverage of a dwelling's electors by the number of canvasses since the dwelling came into use, read from the register's own canvasses and applied dwelling by dwelling at the 2032 canvass.
Swap: "which of the district's 23 school catchments will be more than 10 per cent from the average pupils per form of entry in 2032" (catchments for wards, pupils for electors) has no build-up to age: a pupil is on roll from the day of admission and no canvass adds pupils a year at a time, so the step has nothing to act on and the task reads differently.
Layer 1: the register in two election management system layouts (2020 and 2021 by Electra's property reference, pipe-delimited after a title block with every entry counted in TOTAL; 2022 to 2025 by UPRN in the new system after the March 2022 migration, through the migration's cross-reference), the 2022 register's polling districts on the 2014 scheme and the 2023 review's renamed districts with streets moved in three wards, franchise markers (attainers, overseas electors on the register for parliamentary elections only, local-only electors), the address register's alternative, provisional and historical records and its buildings holding flats beside each approved record, building control's completion dates against the address register's in-use dates, dwelling types in two vocabularies, the trajectory in monitoring years (April to March) against canvass years (register published 1 December) with its 2026/27 column holding October to March only; each written by the system that holds it, none placed to be caught, each asserted neutral on the call (R2).
Layer 2: field_method, a register's build-up: a dwelling's electors reach the register over several canvasses after it comes into use, so the 2025 register is censored low exactly at the estates still building up and the settled ratio is wrong for dwellings that will be young in 2032; the choice that flips the call is ageing every dwelling to its canvass count on 1 December 2032 on the build-up the registers' own canvasses show.
Decisive step: recognising that the settled stock's electors per dwelling holds only for dwellings several canvasses old, reading from the registers how each completion cohort's electors per dwelling rises canvass by canvass toward the settled level of its dwelling type, and applying that build-up to every dwelling in use since 2019 and every dwelling the trajectory places before the 2032 register, at its number of canvasses on 1 December 2032.
Not semantics: with every field read correctly (UPRNs across the two layouts and the cross-reference, the 2014 and 2023 polling district schemes, franchise markers and attainers, the address register's approved records and their states, monitoring years against canvass years), the easy route still files the wrong wards, because no field records that a dwelling's electors are still joining: an estate completed in 2025 shows an ordinary property with fewer electors than its neighbours, and nothing says how many it will hold in 2032.
Not rule application: the Commission's guidance files the WHAT (the local government electors on the register published on 1 December 2032, at today's boundaries and councillor numbers, against the district average, with the trajectory's dwellings as the council phases them) and no clause says how a dwelling's electors are projected, so executing every filed rule is the default path. Measured on the cut pack (23 wards): the enumerated family (the settled ratio by type, the district's ratio, the ratio today's new estates show, a uniform completeness factor, the recent estates caught up alone, the future dwellings aged alone, every dwelling aged) files five distinct sets of wards; the standing family (the build-up read from the 2022 to 2025 panel or the 2020 to 2025 panel, pooled or by dwelling type, from the 2025 register's cross-section pooled or by type, or each young dwelling's own 2025 count carried by the curve's rise) files one set, the golden's, across seven constructions, Caldenstow Park between 12.1 and 12.4 per cent, Lorrimere West between 12.7 and 13.1 and Lorrimere North between 6.2 and 6.6; what rules the default out is one group-by of the new dwellings' register rows on canvasses since they came into use, which no file prints and no clause asks for, and each half use of it (the recent estates caught up alone, the future dwellings aged alone) files a wrong set.
Analyst test: A strong analyst conforms the 1 December 2025 register to wards, adds every dwelling first in use since its last alteration and every dwelling the trajectory places before the 2032 register at the settled stock's electors per dwelling by type, keeps each existing dwelling at its 2025 count, and files Ebborby, Kettermere, Lorrimere North and Tibberfield, missing Lorrimere West, Caldenstow Park and Quenbrook, whose estates completed since 2024 are still joining the register.
Estimand: each ward's local government electors on the register published on 1 December 2032 (every dwelling in use by its 31 October determinations, the trajectory's dwellings as the council's 30 September 2026 trajectory phases them, completions falling evenly through each monitoring year), divided by its councillors and compared with the district's 2032 electors over 43 councillors, a ward failing where it lies more than 10 per cent from that average; filed in the Commission's technical guidance on electorate forecasts and its letter of 2 March 2026.
No decoy: nothing is planted; the registers, notices, address records, completions and trajectory are the council's own records as its systems write them, no forecast, memo, draft or stakeholder figure carrying a wrong answer ships, and the estates still building up are ordinary new housing whose residents register as residents do.
No certified replay: no certified or published figure is reproduced to recover the method; no published register total ships, and the build-up is read from the registers themselves.
Lesson: a register's count at a new dwelling builds up over the canvasses after it comes into use, so a five-year electorate forecast has to age every dwelling, built or still to be built, to its canvass count at the horizon, because both the settled ratio and the ratio new estates show today are wrong for most of them; no build on file teaches it (task451 and task445 complete closed periods from arrival lags, task480's age curve is a falling rate of use, none ages units that do not yet exist to the horizon).

## Layer 1 inventory

| Item | System that writes it | File | Natural mishandling | Effect on the call (checks.py) |
|---|---|---|---|---|
| two register layouts: Electra's pipe-delimited report by property reference with every entry in TOTAL, the new system's by UPRN | Electra; the new election management system | the two ELECTRA reports; ems_property_electorate_2022-2025.csv | Electra's TOTAL read as electors in a six-register panel | none: the panel 2020 to 2025 files the golden either way (R2) |
| the migration's cross-reference, UPRNs matched on the address where Electra held none | the migration in March 2022 | ems_migration_property_xref_2022-03.csv | Electra's rows left unlinked | none: the golden reads the new system's registers; the six-register panel links every row (asserted) |
| the 2022 register's districts on the 2014 scheme, the 2023 review's renamed districts and moved streets | the new system; the 2023 review | the register, the review schedule, the ward list | 2022's codes matched against the 2023 scheme | loud (no 2014 code is a 2023 code); a register UPRN's gazetteer ward always equals its district's ward (asserted) |
| attainers, overseas electors and local-only electors in their own columns | the new system's report | the register | attainers or overseas electors added to the electors, local-only electors taken out | none (R2) |
| alternative, provisional and historical address records, buildings holding flats | the gazetteer | llpg_extract_2026-10-12.csv | every logical status kept, the buildings counted as dwellings | none (R2) |
| building control's completion date against the gazetteer's in-use date | Planning Policy; the gazetteer | the completions schedule; the gazetteer | the completion date taken as the date in use | none (R2) |
| dwelling types in two vocabularies (RD02 to RD06; House, Bungalow, Flat, Maisonette) | the gazetteer; the completions schedule | the same two files | types from the completions schedule | none (R2) |
| monitoring years against canvass years; the 2026/27 column holding October to March | Planning Policy | housing_trajectory_2026-09-30.xlsx | the 2026/27 column spread over April to March | none (R2) |
| the old system's 2021 report as the register it held when it was switched off | Electra's export of 4 March 2022 | ELECTRA_PROPERTY_ELECTORATE_REV_2021.txt | read as the register as published | none on the call (the six-register panel files the golden either way); the ask's device |

## Default path

1. Conform the 1 December 2025 register to wards: each property's local government electors (attainers and overseas
   electors out, local-only electors in) through its UPRN to the gazetteer's ward.
2. Take the settled stock's electors per dwelling by type from that register (houses 1.84, flats 1.22).
3. Add every dwelling the gazetteer shows first in use after 31 October 2025 at that ratio.
4. Add every dwelling the trajectory expects by the 2032 register at that ratio, each monitoring year's completions
   falling evenly through it, the house and flat mix of each year the site's remaining mix, 2032/33's April to
   October completions in.
5. Keep each dwelling on the 2025 register at its 2025 count, divide each ward's total by its councillors and compare
   with the district's average.

Ends on: four wards fail (Ebborby, Kettermere, Lorrimere North and Tibberfield); Lorrimere West, Caldenstow Park and Quenbrook meet the test.

Golden: five wards fail (Lorrimere West, Caldenstow Park, Quenbrook, Ebborby and Kettermere); Lorrimere North and Tibberfield meet the test.

## Stump sentence

The default path keeps every dwelling on the 1 December 2025 register at its 2025 count and adds the dwellings still to come at the settled stock's electors per dwelling, and files four wards, Ebborby, Kettermere, Lorrimere North and Tibberfield; but a dwelling's electors join the register over the canvasses after it comes into use, 0.45 of the settled level at its first canvass and 0.83 at its third on the registers' own rows, so the estates Lorrimere West, Caldenstow Park and Quenbrook completed from 2024 will hold far more electors in 2032 than they do now and the North Lorrimere and Tibberfield sites completing from 2030 far fewer than the settled level: aged to their canvasses on 1 December 2032, Lorrimere West (+12.8), Caldenstow Park (+12.2) and Quenbrook (+15.3) cross the line, Lorrimere North (+6.5) and Tibberfield (+4.1) come inside it, and five wards fail.

## Readability screen

Measured on the cut pack (`generator/golden.py`; the ladder below gives each rung's set).

| Rung | What the response does | What in the pack points at it | Verdict |
|---|---|---|---|
| L0 the 2025 register as it stands | each ward's electors on the latest register against its average | the register is the electorate today | readable |
| L1 the default path | the 2025 register, plus the dwellings since and the trajectory's at the settled stock's electors per dwelling by type | the guidance's general method (dwellings in use today, the trajectory's new dwellings) | readable |
| L1b the ratio today's new estates show | new dwellings at the electors per dwelling the 2025 register shows at the dwellings completed since October 2020 | the register's new-dwelling rows | readable |
| L1c a uniform completeness factor | every ward's forecast divided by one share of adults on the register | the field's coverage studies | readable |
| L2a the recent estates caught up alone | the dwellings on the 2025 register still building up taken to the settled level, the dwellings to come at it | the new estates' low counts on the 2025 register | readable |
| L2b the dwellings to come aged alone | the trajectory's dwellings aged to their canvasses in 2032, today's dwellings at their 2025 counts | the registers' new-dwelling rows read for the trajectory only | silent |
| G every dwelling aged (decisive) | each dwelling in use since 2019 and each the trajectory places by the 2032 register at the settled level of its type times the share its canvass count holds on the build-up the registers show (0.08 on rolling registration alone, 0.45, 0.69, 0.83, 0.91, 0.96 and 0.97 at its first to sixth canvass) | nothing names a build-up: the registers list each property's electors, the canvass report states when a property is first canvassed, and no file relates a property's electors to its canvasses | silent |

L1 and L1c land the same four wards: a uniform factor divides every ward alike and moves no variance. L1b, the new
estates' ratio, pulls the late sites and the average down and files Kettermere and Lorrimere North. L2a reads the
low counts right and leaves the late sites full, filing seven wards; L2b reads the build-up for the trajectory alone
and files two.

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the electorate | local government electors aged 18 or over on the register | entries with attainers; parliamentary electors | another basis | guidance section 1 |
| SF2 | the forecast register | the revised register published 1 December 2032 | the register after the 2031 or 2033 canvass | another forecast | the letter of 2 March 2026 |
| SF3 | the average | the district's 2032 electors over 43 councillors | the mean of the wards' electors per councillor | same call (asserted) | guidance section 2 and the letter |
| SF4 | more than 10 per cent | strictly more than 10 per cent above or below | 10 per cent or more | same call: no ward within 2.1 points of the line (asserted) | guidance section 2 |
| SF5 | the wards tested | today's 23 wards with their 2014 councillor numbers | a proposed pattern | another question | guidance section 2 |
| SF6 | a dwelling's ward | the gazetteer's ward code | the ward of its polling district | identical: every 2025 register UPRN's gazetteer ward is its district's ward (asserted) | the records |
| SF7 | a dwelling's date in use | the gazetteer's in-use date | building control's completion date | same call (asserted) | the canvass report (properties in use on 31 August) |
| SF8 | the canvass a dwelling first meets | the canvass of the year it is in use on 31 August | the year it is completed | same call (asserted) | the canvass report |
| SF9 | what reaches a register | applications determined by 31 October | applications to 1 December | same call (asserted) | the canvass report |
| SF10 | a dwelling's type | the gazetteer's class (RD02 to RD04 houses, RD06 flats) | the completions schedule's type | same call (asserted) | the field guide |
| SF11 | completions within a monitoring year | evenly through it, the 2026/27 column over October to March | each year's completions at its start | same call (asserted) | the trajectory's Notes sheet and its column heading |
| SF12 | the 2032/33 column | April to October 2032's completions in, at their canvass counts | the whole year in; none of it | same call (asserted) | the Notes sheet and the canvass report |
| SF13 | each year's house and flat mix | the site's remaining mix | the site's whole mix | same call (asserted) | the Notes sheet |
| SF14 | dwellings after the trajectory's years | not counted (2033/34 onwards, outline permissions with no phasing) | counted | another forecast | guidance section 3 |
| SF15 | the settled level | dwellings at their seventh canvass or later | from the fifth, sixth, eighth or ninth | same call (asserted) | the records converge |
| SF16 | the build-up's panel | the 2022 to 2025 registers, pooled | the 2020 to 2025 registers; by dwelling type; the 2025 register's cross-section | same call (asserted, seven constructions) | the records converge |
| SF17 | the settled stock's 2032 electors | each dwelling at its 2025 count | each at the settled level of its type | same call (asserted) | the records converge |
| SF18 | a young dwelling's 2032 electors | the settled level of its type times its canvass count's share | its own 2025 count carried by the curve's rise | same call (asserted) | the records converge |
| SF19 | dwellings in use after the 2025 register | every approved residential record in use after 31 October 2025 that the 2025 register does not list | the completions schedule's plots | same call (asserted) | the gazetteer |
| SF20 | Electra's TOTAL in a panel | TOTAL less attainers and overseas electors | TOTAL | same call (asserted) | the field guide |

The live readings of the deciding quantity (SF15, SF16, SF17, SF18) are asserted as a cross product, 5 by 6 by 2 by
2 constructions (120), each filing the golden five, the nearest ward 1.3 points from the line in any of them.

## Ladder

Measured on the cut pack (`golden.py`; `checks.py` asserts each on the pack and L1, L2a and G on the world's clean
truth).

| Rung | Wards failing | Flips from the golden | Call kept |
|---|---|---|---|
| L0 the 2025 register as it stands | none | 5 | no |
| L1 the default path | Ebborby, Kettermere, Lorrimere North, Tibberfield | 5 | no |
| L1b the ratio today's new estates show | Kettermere, Lorrimere North | 5 | no |
| L1c a uniform completeness factor | Ebborby, Kettermere, Lorrimere North, Tibberfield | 5 | no |
| L2a the recent estates caught up alone | the golden five with Lorrimere North and Tibberfield | 2 | no |
| L2b the dwellings to come aged alone | Ebborby, Kettermere | 3 | no |
| G every dwelling aged | Lorrimere West, Caldenstow Park, Quenbrook, Ebborby, Kettermere | none | yes |

On the default path Lorrimere West sits at +7.5, Caldenstow Park +3.8, Quenbrook +3.7, Lorrimere North +14.9 and
Tibberfield +15.4; on the golden at +12.8, +12.2, +15.3, +6.5 and +4.1. Kettermere (+15.6 on the golden) is outside on
every rung from L1 and Ebborby (-12.3) on every one from L1 but L1b, where the new estates' low ratio pulls the
average down and Ebborby to -10.0, so the call turns on five wards. On L0 no ward is outside (Harnwick nearest at
+8.1), and every other ward sits within 6.8 points of the average on the default path and within 7.0 on the golden.
The nearest golden wards to the line are Caldenstow Park at 2.2 points outside and Ebborby at 2.3, and across the
standing family's seven constructions none comes nearer than 2.1.

## Closure table

| Axis | Reading | Move |
|---|---|---|
| 1 Population | every dwelling in use by the 2032 register's 31 October determinations: today's, and the trajectory's to come | filed (guidance 3); SF14, SF19 |
| 2 Unit of account | local government electors per councillor | filed (guidance 1, 2); SF1 |
| 3 Attribution window | the register published 1 December 2032 | filed (the letter); SF2 |
| 4 As-of dating | the 2025 register, the gazetteer of 12 October 2026, the trajectory at 30 September 2026 | filed (the field guide, the trajectory) |
| 5 Version basis | each register as published; the trajectory at its base date | filed; C1 |
| 6 Denominator | the district's 2032 electors over 43 councillors | filed (guidance 2, the letter); SF3 |
| 7 Weighting | none: wards are totals | C1 |
| 8 Window length | the trajectory's monitoring years to 2032/33's April to October | filed (the Notes); SF11, SF12 |
| 9 Boundary inclusivity | more than 10 per cent | filed (guidance 2); SF4, margins asserted |
| 10 Rounding path | findings on unrounded variances | the prompt's closing sentence; C1 |
| 11 Tie-break | none: no ward within 2.1 points of the line | asserted |
| 12 Maturity and censoring | every dwelling aged to its canvass count on the build-up the registers show | the decisive step; SF15 to SF18 asserted |
| 13 Order of operations | electors by dwelling, then by ward, then the average | C1 |
| 14 Row order | none: every figure is a set computation | C1 |
| 15 Duplicate resolution | the gazetteer's alternative records share their UPRN with the approved one | the field guide; R2 asserted |
| 16 Identity normalisation | UPRNs across the systems, Electra's references through the cross-reference | the field guide; SF6 |
| 17 Netting against gross | none on the call; the ask's notices net additions against deletions | the field guide |
| 18 Dimensional units | electors and dwellings, whole | C1 |
| 19 Code and status semantics | logical statuses and states, classes, franchise markers | filed (the field guide); SF10, SF20 |
| 20 Integerisation | the trajectory's even spread is fractional; findings on unrounded totals | the Notes; C1 |
| 21 Clause scope | today's boundaries and councillor numbers | filed (guidance 2); SF5 |
| 22 Forward window contents | the dwellings to come and today's young ones aged to 2032 | the decisive step; SF11 to SF18 asserted |

## Literal reader

Executing the prompt and every filed sentence word for word: the guidance defines the electorate as the local
government electors on the register published on 1 December of the forecast year, which the letter fixes at 2032,
and counts the electors expected at every dwelling then in use, today's and the trajectory's, at today's boundaries
and councillor numbers. No file holds the 2032 register, so a literal reader must project each dwelling's electors to
it; the guidance says how many dwellings and when, never how many electors each will hold. The 2025 register gives
each existing dwelling's electors today, and the canvass report says a property is first canvassed in the year it is
in use on 31 August. Keeping a dwelling completed in 2025 at its 2025 count assumes its household will add no
elector over six more canvasses, and adding a dwelling completed in 2032 at the settled stock's ratio assumes its
household is fully registered at its first canvass; the registers' own rows contradict both, showing each cohort of
new dwellings rising canvass by canvass to the settled level. The golden is the projection that ages every dwelling
to its canvass count on 1 December 2032.

## Oracles

No file ties only under the golden or only on a wrong read. No shipped file states a ward's 2032 electorate, a
dwelling's expected electors, a build-up or a completeness rate, or ranks the wards on electoral equality: the
registers list each property's electors, the gazetteer and the completions list dwellings, the trajectory phases
sites, the guidance and the letter state rules and dates, and the canvass report states the 2025 canvass's totals,
which every handling of the 2025 register reproduces. No published register total ships for any earlier year. The
ask's referee: the notices of alteration, whose January to March 2022 entries are each present in Electra's 2021
report, the device's evidence and never an answer.

## Ask sheet

The call's declared population is the new system's 2022 to 2025 registers' local government electors by UPRN, the
gazetteer's residential records, the completions schedule's plots and the trajectory's phasing. Ask A reads Electra's
2021 report and its notices of alteration, which the call never reads (the golden builds the build-up on the new
system's registers; emptying both Electra files, or reading the 2021 report as it stands, leaves every call figure
identical, asserted). The SNPP 2022-based projections and the council tax valuation list ship as distractors: the
guidance counts electors at dwellings, and no golden figure opens either (asserted).

- **Ask A, each ward's local government electors on the register published on 1 December 2021, whole electors (23
  figures).** H18 home: a measure every ward carries that the call does not turn on, its electorate on the last
  register the old system published, the start of the series the Commission tabulates beside its forecast. User: the
  review manager, whose report sets each ward's registered electorate since 2021 beside the forecast. Primary device
  (silent, D2 a later snapshot that looks final): Electra was switched off on 4 March 2022 and both its reports were
  exported that day, the 2020 report from its archive of that register as published and the 2021 report from the
  register it then held, which had the notices of 4 January, 1 February and 1 March 2022 applied; both title blocks
  read REVISED REGISTER and RUN 04/03/2022. Each property's TOTAL less its attainers and overseas electors therefore
  carries the January to March 2022 additions and deletions, 678 electors net over the district and between 9 and
  65 in every ward. The remedy is a reconstruction: back each 2022 notice's local government entries out of the
  report (an addition taken off, a deletion put back, by its district's ward; an F entry and an attainer are not
  electors, a K entry is). Twin: the 2020 report, exported the same evening, is the register as published, so the
  run date marks neither. Mirror device (seen): TOTAL counts attainers and overseas electors (the field guide).
  Hazards: the 2014 districts to wards through the review's schedule, the attainers' and overseas electors' notice
  rows, the 2021 notices that altered the 2020 register. Files and columns: the 2021 report (PD, PROPREF, TOTAL,
  ATTAINERS, OVERSEAS), the notices (NOTICE, PD, ACTION, FRANCHISE, ATTAINS_18), the review schedule
  (replaces_district, ward), the ward list, 4 files and 12 columns. Stops: the report as labelled (the cracker, 0 of
  23), TOTAL as the electors (0 of 23), the additions taken off without the deletions put back (0 of 23), every
  2022 notice row backed out with the attainers and overseas electors (0 of 23), every notice of 2021 and 2022
  backed out (1 of 23), the 2022 notices backed out without the local-only electors (5 of 23), the golden. Forcing
  figure: the dwellings the gazetteer shows first in use after 31 October 2021 hold electors in the 2021 report, and
  every one of them is an addition in the 2022 notices; backed out, none holds one. Realism: an election management
  system keeps the current register live with its alterations applied and archives each earlier one at publication,
  so an export taken at a switch-off gives the archived registers as published and the live one as it then stood.
One device ask, by design. The construction layer is the chart, each ward's 2032 variance against the 10 per cent
lines, which the cracker has with the call and the mirror misses with it.

Main population: the call reads no Electra file, no notice and no attainer or overseas column (checks.py
separation, each emptied or misread with every call figure identical); the ask reads no new-system register, no
gazetteer record, no completion and no trajectory row.

| Ask | What the cracker does | Cracker |
|---|---|---|
| A | reads Electra's 2021 report as the register it is labelled, each property's TOTAL less its attainers and overseas electors, by its 2014 district's ward | miss |

Measured on the cut pack: the cracker keeps 0 of 23 ask figures and scores 45.0 with the call; the mirror keeps 0 of
23 and scores 12.0 off it; the best half-handled response keeps 5 of 23.

Pair ceiling: 28.5 (the cracker 45.0 on the call with no ask figure, the mirror 12.0 off it with none).

Mirror leakage: 0.0 per cent of ask weight.

Measured by: generator/ceiling.py on the cut pack.

## Architecture 1 record (spent 2026-10-25)

Zip 237917da9ecb5387a7250b4fde842cf2 (checks.py 58 PASS, verify.py 10 of 10, precut 51 checks with no FAIL, pair
ceiling 28.5, leak.py REVIEW with no LEAK, guard heart WARN). Round 1: both scored readers (sonnet, medium, fresh
copies) landed the call, the golden five, and score_reader exited 1 on both (asks 6 and 2 of 25). Reader A held the
settled stock flat and fitted the share of the settled level a new dwelling holds to its age since completion on the
2022 to 2025 registers (about 0.08 in its first quarter, 0.45 at a year, 0.80 at two and a half years, 1.0 from about
six), applied it to every completion since April 2014 and every trajectory dwelling, and filed Kettermere +16.1,
Quenbrook +14.8, Caldenstow Park +13.9, Lorrimere West +13.2 and Ebborby -13.4. Reader B built the same
electors-per-dwelling curve by age and type and filed the same five. Both named the step an analytical choice nothing
in the pack states. Both also found ask A's device: the 2021 report's run date (4 March 2022) and the notices beside it
told them the report held the January to March 2022 alterations, and both backed them out, missing the golden on
handling only (reader A 4 of 23 wards exact; reader B also removed additions it took to be under 18). The judge thread
(v1r1) returned DETERMINISTIC and APPROVE (Gate G forecasting and etl_conformance, analytical_non_defect; Gate H domain
and layers pass, decisive step analytical); it was not taken to a report, the call being spent. The readers' realism
notes: the settled stock barely moves from 2020 to 2025, the ramp is a near-exact exponential alike in every ward and
type, the trajectory's site sizes are round, and no register row lacks a UPRN.

## Tried and rejected
- 2026-10-25, at the draw: the seed's own world, each employer's FY2025 H-1B workers at Level I read from labour
  condition applications through USCIS's employer data hub, positions converting to approved petitions at very
  different rates by petition type (cap lottery against continuations) so the position share overstates Level I where
  it sits in new employment: the per-type apportionment is one join and one group-by once seen, the hub's initial and
  continuing columns invite it, and the employer-level conversion that leaves the share unchanged is the only partial
  fix; the cheapest licensed member is the golden, a single insight a reader has or does not. Not drawn.
- 2026-10-25, at the draw: the FY2027 weighted wage-level selection, each employer's Level I intake read through
  selection probabilities by level: executing the stated selection procedure is rule application, and its separation
  from the linear reading is small (Level I at 0.174 against 0.154 on a plausible pool). Not drawn.
- 2026-10-25, at the draw: regression to the mean and retransformation bias (spent in five slot notes each), landfill
  first-order decay (set aside three times in this lane against task480), overdose deaths with unspecified drugs
  (task455 v1's certificates corrected by drug class), age heaping (task230's rejected draw), areal interpolation
  (task253), a business register's head-office employment (a reflex join once the local unit register ships), a
  housing trajectory's lead-in times for unstarted sites (the trajectory reproduces the started sites by construction
  and fails forward on the rest, a validated decoy), spiralled forms in a random-groups equating (a balance check is a
  reflex and presmoothing forks the cut), a business register's industry codes maturing with the enterprise's age (a
  completion reskin). Spent or not drawn.
- 2026-10-25, architecture 1 (each dwelling's electors aged to its canvasses on the 2032 register on the build-up the
  registers show), spent at stage 4: both scored readers fitted electors per dwelling to the dwelling's age since
  completion on the property-level registers and applied the ramp to every dwelling built and to come, landing the
  golden five. A register panel at property level beside every new dwelling's completion date makes a new unit's ramp to
  the settled level the forecaster's first move, not a skipped step; task484 v1's lease-up curve (a fill record of
  earlier additions beside a flat stock) was the same insight and fell the same way, and the draw's slot screen missed it
  because it searched the mechanism's words (build-up, canvass, register) rather than the setting's (lease-up,
  occupancy, new premises). The ask's switch-off device fell to the report's own run date beside a notices file: a
  file-level stamp that differs from the register's date is read by every careful reader.

