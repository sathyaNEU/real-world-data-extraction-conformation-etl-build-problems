# task150: Sorrel Creek School District RE-6, where the 2025 bond's 24 elementary classrooms go (architecture 1)

Private, never ships. A new build (wave 4), numbered from seed FC21. The seed (a suburban district placing a bond's 24
classrooms across seven elementary schools, at most eight a site, in order of each school's five-year average projected
enrollment above rated capacity) was read at its header and Situation only. Its world, decision and quantity are kept.
Its mechanism (pupils per new home by the age of the home, against a developer-agreement template of 0.45) is not kept:
a pupil yield by housing age is task134's ground (a raised allowance's yield by what stands on each lot) and the seed's
decoy-era template. The pitfall is re-found from how a district's enrollment records come to exist: between one October
count and the next, a pupil promotes, repeats, moves to another attendance area or leaves the district, and new pupils
arrive from outside the district; the field's grade progression ratio nets all of that into one ratio struck on the
receiving class.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task150.json`, architecture v1, registered 2026-10-16; `guard.py check` WARN (overuse.objective, repeat.gate_g), answered below; the older same-driver signature (time, G6, forecasting) against task125 v2 and task501 v3 lineage differentiated on the card; nearest drivers 0.08 (task451 v2) and under |
| Domain / task type | `sociology-demography` (client domain), task type `population-estimation-demographic-projection` (serves Forecasting): a school-by-school enrollment projection is a small-area cohort-component projection, cohorts aged through grades, kindergartens from births five years earlier, migration between areas and from outside. Education & Learning Sciences has no task type serving Forecasting that fits (early warning is a pupil-level risk model) and the seed's Policy & Education label is a house domain mapping to it and to political science |
| Objective | Forecasting & Predictive Modeling: each school's average projected October K-5 enrollment over the five school years 2028-29 to 2032-33, a window not open at the decision (the board adopts the placement schedule in November 2026 so design and construction run through 2027-28) |
| Shape | `05` allocation to a fixed total: 24 classrooms over seven schools, two figures a school (the classrooms its projection calls for, the classrooms placed), the call, the chart, and two ask tables (counted in `## Ask sheet`) |
| Decision | `allocation_to_total`, answer unit `count` (classrooms per school, whole numbers) |
| Mechanism | gap time (decisive: every progression ratio is a statement about the classes that history held; the decision bets on classes of another size fed by senders of another size) with population (the population each flow is a rate on); pattern none; generators G6 (the mix of own pupils, outside arrivals and transfers inside each next-grade count shifts as the bases change), G16 (the gross-flow model against the net ratio, which the data separates), G13 (the five-year window); Gate G `forecasting`; strategy `population_selection` (which population each flow is a rate on: the sending school's pupils for exits and transfers, no population for outside arrivals) |
| Layer 2 family / pattern | `field_method`; `sociology-demography/population-estimation-demographic-projection/2` (gross migration flows, not net rates; the system stays closed; origin-destination flows, internal migrants sum to zero). Here the areas are seven attendance areas, the migrants are pupils between October counts, and the outside arrivals come at a count each school's history pins |
| Furniture | forum `trustees_or_governors` (the board of education adopts the schedule), forcing event `vote_or_meeting` (the November adoption), organisation family `university_or_school`, role family `research_desk` (the planning and enrollment analyst), context artifact `filed_standard` (the board's placement standard), calibration `none`, opening `question-first`, question form `where` |
| Spine | the student information system's October membership snapshots, one row per pupil enrolled in K-5 on one October count day, 2013 to 2026 in two layouts (constructed, 76,597 rows) |
| Deliverables | `classroom_placement_2028-33.xlsx` (the schedule, each school's classrooms needed and placed, the projection behind it, the two ask tables), `enrollment_vs_capacity_2026-33.png` (each school's October enrollment 2013 to 2026 and the projection to 2032 against its rated capacity) |
| People | drawn with `guard.py names --geo "United States" --seed 150` (first names checked clean): Stacy Frazier (executive director of planning and enrollment, the requester; not in the prompt), Mariah Henry (student information systems manager), Joseph Hanson (GIS analyst), Troy Medina (director of facilities), Brian Owen (Brandt County vital records registrar) |

**Guard.** `guard.py check` on the registered card: WARN `overuse.objective` (Forecasting in 6 of the last 12: this is
the Forecasting lane) and `repeat.gate_g` (forecasting beside task148, a credit-loss allowance on a loan servicing
history that shares no other axis). The first draft (gap population, G16) blocked on the spent signature (population,
G16, method_or_model_selection) against task104, task134 v1, task501 v4 and task70 v2; population with G6 or G14 blocked
inside the batch. Redrawn honestly: the decisive gap is time (the past ratios describe classes of another size), the
generator G6, Gate G forecasting, with two differentiation lines on the card (task125 v2 filters recruits out of a
rotating panel; task501 v3 paces a draw against a deadline).

**Same-puzzle and same-driver tests.** Gap time, decisive G6, decision `allocation_to_total`, Gate G `forecasting`: no
build in the last twelve (task455 to task149) carries either triple (task145 is time, G16, allocation; task149 time,
G14; task461 time, G13). The older matches are differentiated on the card.

**Abstraction test.** Stripped of nouns: a unit's next count is its own members carried at a rate on its own base,
plus arrivals from outside that come at a steady count whatever the base, plus transfers from sibling units at a rate on
each sender's base; a ratio of next count to this count struck on the receiver carries the past proportion of arrivals
to base forward. Read by mechanism rather than score, the nearest are: task89 (a trailing net rate already contains a
known inflow schedule, so adding the schedule counts it twice: there the inflow is a filed schedule added on top, here
nothing is scheduled, the net ratio is the whole forecast and its error is scaling, not double counting, plus a closed
system of transfers on the sender's base); task98 v2 lineage (arrivals register with members in place and consume no
unit: a unit count, not a flow rate); task46 (a rate stationary in cumulative exposure: a clock, here no clock); task145
(units differ in which value they hold fixed across a conversion: a mix of two holder types, here the mix is of flow
types each with its own base); task144 (seeded adoptions spread through follower reach: a network multiplier, here no
multiplier, a rate on the sending area's pupils). None shares the latent structure, the default path and the correction.

**Data-native sentence.** A district's October counts are linked pupil records: between one count and the next a pupil
promotes or repeats at the school, moves to another attendance area (the move is decided by the family in the area it
leaves, so it scales with that area's pupils), or leaves the district, and pupils arrive from outside the district into
grades 1 to 5 at the pace homes and rentals turn over (about 75 a year at Fifth Street and Prairie Rose in every year
since 2014, whatever the size of the classes they join); Ortega's births have fallen by a third since 2017, Fifth
Street's by a quarter since 2012, and Prairie Rose's have risen by half since 2015, so the next five years' classes are
not the sizes the progression ratios were struck on.

**Sources read, one line each.** `guard.py mechanisms --objective forecasting` (61 builds): no driver on file makes a
next-period count a sum of flows each on its own base (the nearest structures are a net rate containing a scheduled
inflow, task89; a two-holder mix, task145; a network multiplier, task144). `layer2-rigor-patterns.md`: sociology,
population projection line 2 (gross flows, not net rates; the system stays closed) is the client's line for the step;
line 1 (age the cohorts, do not trend totals) is the rung below the default; urban forecasting line 1 (back-test from
the origin) is how the data separates the candidates. `two-layer-task-design.md`: "the data's real structure" and "a
forecast validated out of sample". `strategies.md` F7 (who is in the denominator) and F6 (the natural fit wrong out of
sample) are the family record. The seed's header and Situation (FC21) for the world, decision and quantity only.

**World.** Sorrel Creek School District RE-6 serves about 5,400 pupils in kindergarten to grade 5 at seven attendance-
area elementary schools in a suburban part of Brandt County on Colorado's northern Front Range. Ortega Elementary sits
among the 1990s apartment complexes along the state highway; Bluestem and Kessler serve the subdivisions east and south
of it, where Ortega families buy their first houses; Fifth Street serves the old town core, its rental duplexes and the
apartments by the regional hospital and the community college; Lincoln is the old core's second school, small and full;
Prairie Rose serves a 1970s ranch-house neighborhood where young families have been replacing the first owners; North
Fork serves the stable north side. Voters approved a $96.5 million bond in November 2025 whose Elementary Capacity
program funds 24 permanent classrooms, built during 2027-28 and in use for the five school years 2028-29 to 2032-33. The
board adopted its placement standard (Board Policy FEA-R2) on March 12, 2026; the planning office prepares the placement
schedule from the October 1, 2026 count for adoption at the November 12, 2026 board meeting. The planning office pulled
the student system's October snapshots, the county's births file, the GIS office's address counts and the facilities
capacity report by Friday October 9, 2026 (the as-of).

## Default path

1. Stitch the two October membership exports (2013 to 2018 pipe-delimited with local school, grade and entry codes and US
   dates; 2019 to 2026 CSV with state codes and ISO dates) through the school code list (Southeast became Kessler in 2020)
   into each school's K-5 count by grade on each October count day.
2. For each school and grade transition (K to 1, ..., 4 to 5), the five-year grade progression ratio: this October's
   next-grade count over last October's grade count, summed over the transitions 2021-22 to 2025-26.
3. Each school's kindergarten as its attendance area's resident births five years earlier (the county file) times the
   kindergarten-to-births ratio of the last five Octobers, with births for 2026 and 2027 at the 2023-25 average.
4. Roll each school from the October 1, 2026 count to October 2032 and average the five counts 2028 to 2032.
5. Excess over rated capacity (the capacity report), the standard's classroom need (excess over 24, rounded up), and the
   placement in order of excess, at most eight a site, until the 24 are placed.

Ends on: Bluestem 7, Fifth Street 3, Lincoln 6, Kessler 0, Prairie Rose 8, Ortega 0, North Fork 0 (needs Bluestem 7, Fifth Street 5, Lincoln 6, Kessler 4, Prairie Rose 8, Ortega 0, North Fork 1).
Golden: Bluestem 4, Fifth Street 5, Lincoln 6, Kessler 2, Prairie Rose 7, Ortega 0, North Fork 0 (needs Bluestem 4, Fifth Street 5, Lincoln 6, Kessler 3, Prairie Rose 7, Ortega 0, North Fork 1).

## Stump sentence

Projecting each school by its five-year grade progression ratios and kindergarten-to-births ratio places Bluestem 7,
Fifth Street 3, Lincoln 6 and Prairie Rose 8, with none at Kessler (Ends on); the step that lands it there is carrying
ratios struck on each school's own classes, when pupils arriving from outside the district come at a steady count each
fall whatever the size of the class they join and pupils moving between attendance areas come at the rate of the school
they leave, so Prairie Rose's growing classes and the two subdivisions Ortega's shrinking classes feed are projected too
high and Fifth Street's shrinking classes too low; projected flow by flow the 24 go Bluestem 4, Fifth Street 5, Lincoln 6,
Kessler 2 and Prairie Rose 7.

## Three rules

- **Task type:** sociology-demography, population-estimation-demographic-projection (serves Forecasting): a small-area
  cohort-component projection of each attendance area's K-5 pupils over the school years 2028-29 to 2032-33, cohorts aged
  through grades, kindergartens from births five years earlier, migration between areas and from outside the district,
  the five-year average set against each school's rated capacity.
- **Domain test:** the deciding quantity is each school's projected October K-5 enrollment by grade, estimated the way
  applied demographers project small areas: a cohort-component model with gross migration, exits and moves between areas
  as rates on the population at risk where they start and arrivals from outside the system as counts, set against the
  net cohort-progression ratio the school-planning textbook uses.
- **Swap:** "where should the 24 new beds go across our seven hospitals" keeps a capacity against a projected census,
  but patients do not age through grades from births five years earlier, no family moves its child between catchments
  grade by grade and no stream of arrivals joins a class at a steady count, so the quantity that decides here (each
  grade's exits, moves and arrivals on their own bases) has nothing to attach to.
- **Layer 1:** the 2019 student-system conversion (two layouts: pipe-delimited with local school, grade and entry codes
  and US dates before; a CSV with state codes and ISO dates after); pupils keyed by a local number with the state ID
  beside it before 2019 (a few blank, recovered through IT's conversion crosswalk) and by the state ID after; Southeast
  Elementary renamed Kessler in 2020 under the same building; October count days moved to the nearest school day; the
  county's births geocoded to attendance areas with births outside the district and births not geocoded in their own
  rows and 2025 provisional. Each is what these systems write; none moves the call (R2 assertions in `checks.py`).
- **Layer 2:** `field_method`, the gross-flow cohort-component projection: each between-October flow on its own base,
  exits and transfers on the school a pupil leaves, outside arrivals as each school's steady count per grade; the history
  shows arrivals flat at Fifth Street and Prairie Rose while Fifth Street's classes shrank by a quarter and Prairie Rose's
  grew by a half, and Ortega's transfers to Bluestem and Kessler rising and falling with Ortega's classes; the net ratio
  struck on the receiving class misses the 2020-26 counts out of sample by 7 to 9 per cent at those schools.
- **Decisive step:** projecting each grade with exits and moves to other schools at the rate of the school the pupil
  leaves, and arrivals from outside the district at each school's steady count per grade, so Ortega's shrinking classes
  send Bluestem and Kessler fewer pupils, Fifth Street keeps its stream of arrivals while its own classes shrink, and
  Prairie Rose's arrivals do not grow with its classes.
- **Not semantics:** no field, code, unit or definition says how a flow scales; the entry codes, grade and school codes,
  the state IDs, the births' status and the capacity report are read correctly on the easy route too, and an analyst who
  reads every one of them correctly and projects by progression ratios (or by any ratio struck on the receiving class)
  files the default.
- **Not rule application:** the strict rule 3 test on every shipped sentence that bears on how the figure is computed:
  the prompt; Policy FEA-R2 sections 1 to 6 (the program, the definitions of K-5 enrollment, projected enrollment, the
  five-year average, rated capacity and classroom need, the order, the cap, the reserve, the tie-break, who prepares the
  projection); the student-system notes (what each field and the snapshot hold, the codes); the births file notes (what
  is counted, geocoding, provisional status); the capacity report's notes. Executed word for word they fix the target, the
  arithmetic of need and the placement, and give no projection: none names a method, a ratio, a rate or how arrivals or
  moves behave, and the one literal combination they admit with the field's standard projection (progression ratios)
  files the default (`R3s` in `checks.py`). The behaviour the decisive step turns on is inferred from the data, and the
  data rejects the rivals by a visible margin out of sample (Ladder).
- **Analyst test:** a strong analyst who stitches the two layouts, links pupils across Octobers, reads the births and the
  standard correctly and projects each school by its five-year progression ratios and kindergarten-to-births ratio files
  Bluestem 7, Fifth Street 3, Lincoln 6, Kessler 0 and Prairie Rose 8 (Ends on); the 3-year, latest-year, 8-year and
  all-year ratios, trended ratios, cohort-change differences and a district control total file other wrong schedules, as
  do component models carrying arrivals or transfers on the receiving class; only exits and transfers on the school they
  leave with arrivals as steady counts files Bluestem 4, Fifth Street 5, Lincoln 6, Kessler 2 and Prairie Rose 7
  (executed in `checks.py` on the clean truth and on the pack).
- **Estimand:** Policy FEA-R2 section 2 with the prompt: each school's K-5 pupils expected on the October count days of
  2028 to 2032 (school years 2028-29 to 2032-33) under the attendance areas in effect on October 1, 2026, pupils not yet
  enrolled or not yet born included, averaged over the five counts and set against its rated capacity in the facilities
  capacity report, in `target/BP_FEA-R2_elementary_classroom_placement.pdf`. Population (members not yet observed
  included), outcome, window, unit and comparison are filed; the method is not.
- **No decoy:** no memo, earlier projection, consultant study, state projection or stakeholder figure states or argues an
  enrollment projection, a ratio or a placement; the capacity report gives capacity; the distractors (the facility
  condition assessment and the meal eligibility counts) rank nothing on enrollment.
- **No certified replay:** nothing certified or published is reproduced to recover a method; the flows are estimated
  from the raw linked records, and the back-test is the analyst's own on the history, not a shipped table.
- **Lesson:** a school's next-grade count is a sum of flows that scale with different populations, exits and moves with
  the class a pupil leaves and arrivals from outside with nothing in the district, so a progression ratio carries the past
  share of arrivals and the past size of a sending area's classes into classes of another size; projecting each flow on
  its own base is the demographer's gross-migration cohort-component model, and no build on file teaches it (task89's net
  rate that already contains a filed inflow schedule is the nearest, a double count, not a scaling error in a closed
  system of areas).

## Readability screen

Six tests per rung (`stumping` 2.1): 1 filed sentence, 2 schema, 3 reflex, 4 control bench, 5 hygiene, 6 linear.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 (the default path) five-year progression ratios and kindergarten-to-births ratio | no | no | yes: the school-planning textbook | no | no | yes: one ratio a grade | readable |
| R0a the 3-year, latest-year, 8-year or all-year ratios | no | no | yes: the window choice | no | no | yes | readable |
| R1 each ratio trended over the window | no | no | yes: a trend | no | no | no | readable |
| R1c cohort change differences (next grade less this grade) | no | no | yes: the additive alternative | no | no | yes | readable |
| R1d the schools raked to a district total from district-level ratios | no | no | yes: a control total | no | no | yes | readable |
| R2a components (exits, transfers, arrivals) each as a share of the receiving class | no | yes: the entry codes split the ratio | yes: decomposing the ratio | no | no | no | readable |
| R2b exits on the school left, arrivals and transfers in as steady counts | no | yes: entry codes and linked IDs | no | no | no | no | silent |
| R2c exits and transfers on the school left, arrivals as a share of the receiving class | no | yes | no | no | no | no | silent |
| R3 (decisive) exits and transfers as rates on the school the pupil leaves, outside arrivals as each school's steady count per grade | no: no sentence says how a flow scales, names arrivals or transfers, or a method | no: no column holds a flow or a rate; the flows come from linking pupils across two layouts and an ID crosswalk | no: the ratio is the reflex, and decomposing it puts each flow on the receiving class | no: no projection, control total or certified figure ships | no: nothing in the files is wrong | no: a linked-record flow table, a seven-area matrix of moves, then the cohort roll | silent |

## Semantic fork table

Every row is asserted in `generator/checks.py`.

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "the 24 elementary classrooms in our 2025 bond" | the Elementary Capacity program's 24 classrooms | none ships | same | FEA-R2 section 1 |
| SF2 | "school by school", "our seven elementary schools" | the seven attendance-area schools | the preschool or a program site | none other ships | FEA-R2 section 1; the school code list |
| SF3 | "projected enrollment" | K-5 pupils expected on each October count day 2028 to 2032 under the October 1, 2026 attendance areas, pupils not yet enrolled or born included | the pupils enrolled today aged forward (no new kindergartens) | not the standard's population | FEA-R2 section 2(b) ("including pupils who are not yet enrolled or not yet born") |
| SF4 | the window | October 2028 to October 2032 (2028-29 to 2032-33) | 2027-28 to 2031-32 | not the standard's window | FEA-R2 sections 1 and 2(b) |
| SF5 | "average" | the mean of the five counts | the peak year | not the standard | FEA-R2 section 2(c) |
| SF6 | "rated capacity" | permanent classrooms, the capacity report | with portables | not the standard | FEA-R2 section 2(d); the report's note |
| SF7 | "the classrooms its projected enrollment calls for" | the standard's classroom need, uncapped | capped at eight | that is "placed" | FEA-R2 sections 2(e) and 3 |
| SF8 | "the classrooms it is placed" | the standard's order, need and cap until 24 | proportional shares | not the standard | FEA-R2 section 3 |
| SF9 | K-5 enrollment | primary enrollments in kindergarten to grade 5, each pupil once | with preschool | not the standard | FEA-R2 section 2(a); preschool is not in the membership export |
| SF10 | the projection base | the October 1, 2026 count | the 2025 count | not the as-of | FEA-R2 section 2(b) (projected from the district's records through the October 1, 2026 count) |
| SF11 | births 2025 | provisional as filed | completed by a late-registration share | same call (asserted) | none needed |
| SF12 | births not geocoded and outside the district | out of the areas' births | spread pro rata | same call (asserted) | the births notes |
| SF13 | "expected" | the expected count | a high case | the standard's expected value | FEA-R2 section 2(b) |
| SF14 | rounding path | unrounded average, excess over 24 rounded up once | the average rounded first | same call (asserted) | FEA-R2 section 2(e) |
| SF15 | ties in the order | none arises | the larger October 2026 count | same call | FEA-R2 section 3; margins asserted |
| SF16 | classrooms left over | none (needs total 26 against 24) | the reserve | same call | FEA-R2 section 3 |

## Ladder

Measured on the shipped files by `generator/calc.py` and asserted in `generator/checks.py` (the clean truth gives the same
default and golden, R3a); every placement is the classrooms at Bluestem, Fifth Street, Lincoln, Kessler and Prairie Rose
(Ortega and North Fork 0 on every rung unless stated). Rated capacities (Fifth Street 667, Lincoln 640, Ortega 703,
Bluestem 710, Prairie Rose 833, Kessler 651, North Fork 577) are the capacity report's.

| Rung | Construction | Placement B, P, C, D, E | Dies to |
|---|---|---|---|
| R0 (default) | five-year progression ratios, kindergarten-to-births ratio | 7, 3, 6, 0, 8 | arrivals are a steady count (Fifth Street, Prairie Rose) and Ortega's transfers fall with its classes (Bluestem, Kessler); out of sample from 2019 the ratios come out 8.2 per cent low at Fifth Street and 8.3 high at Prairie Rose by 2026 |
| R0a | 3-year ratios | 6, 4, 6, 0, 8 | as R0 |
| R0b | latest-year ratios | 6, 0, 5, 6, 7 | as R0, and one year's noise |
| R0c | 8-year, all-year or mean-of-ratios | 7, 3, 6, 0, 8 | as R0 |
| R1 | ratios trended over 8 years | 5, 7, 5, 0, 7 | the trend follows the past shift, not the classes the window brings |
| R1c | cohort change differences (five or all years) | 7, 3, 6, 0, 8 | exits are a rate, not a count; out of sample 6.9 per cent low at Fifth Street |
| R1d | five-year ratios raked to a district total | 5, 4, 5, 2, 7 (one left) | the district total carries the same scaling |
| R1e | district ratios split by school share | 5, 4, 5, 2, 0 (Ortega 3, five left) | the shares carry the past mix |
| R2a | components each as a share of the receiving class | 7, 3, 6, 0, 8 | the same arithmetic as R0 |
| R2b | moves in as counts, arrivals as counts | 6, 5, 6, 0, 7 | Ortega's moves to Bluestem rose and fell with Ortega's K-4 base (correlation asserted over 0.6; 9.3 to 11.8 per 100 Ortega pupils every year as the count ran 58 to 93); out of sample the counts miss Bluestem at 3.3 per cent a year against 1.3 |
| R2c | moves on the school left, arrivals as a share of the receiving class | 4, 4, 6, 2, 8 (last five: 4, 5, 6, 1, 8) | arrivals stayed flat while classes shrank or grew; out of sample 6.6 per cent low at Fifth Street and 8.6 high at Prairie Rose |
| golden (R3) | exits and moves on the school left, arrivals as steady counts | 4, 5, 6, 2, 7 | (the golden) |

- **Every construction of the golden** (C1, B2): rates and arrivals from every transition since 2014, the last ten, eight,
  five or three; kindergarten ratios over all or the last five; births for 2026-27 at the 2023-25 average, the 2025 value
  or the 2019-25 trend; arrivals averaged over all years or the last five or three; the 2018-19 conversion transition
  dropped; the kindergarten ratio as a mean of ratios; exits and moves by grade: one placement and one set of needs (Prairie
  Rose 7, Lincoln 6, Fifth Street 5, Bluestem 4, Kessler 3, North Fork 1, Ortega 0), every school's excess inside its
  24-pupil bin (ranges: Fifth Street 102 to 114, Lincoln 128 to 135, Bluestem 80 to 92, Prairie Rose 150 to 162, Kessler 56
  to 64, North Fork 7 to 18, Ortega below capacity).
- **One sigma** (B4). Parametric sampling error of each school's excess (400 draws of every rate, arrival count and
  kindergarten ratio) 4.7 to 7.8 pupils; the golden excesses (Fifth Street 108.6, Lincoln 131.2, Bluestem 88.5, Prairie
  Rose 152.1, Kessler 60.0, North Fork 9.9) each sit at least one standard error inside the bin, the tightest Bluestem
  (7.5 against 6.1) and Prairie Rose (8.1 against 7.7); Ortega's average is 92 below capacity. Flip condition: a school's
  need moves only if its five-year average moves across a multiple of 24 above capacity.
- **The data rejects the default and every rival** (L4, L5). Fitted on the transitions to 2019 and run from the 2019 count
  to 2026 with the births on file: the gross-flow projection misses every school's 2026 count by 5.0 per cent or less
  (Ortega 5.0, the rest 2.4 or less); five-year ratios come out 8.2 low at Fifth Street and 8.3 high at Prairie Rose;
  arrivals as a share 6.6 low and 8.6 high; moves in as counts miss Bluestem at 3.3 per cent a year against 1.3; cohort
  differences 6.9 low at Fifth Street. In sample, Fifth Street took 66 to 89 arrivals a year as its K-4 base fell from 741
  to 639, Prairie Rose 61 to 81 as its base rose from 532 to 752, and Ortega's moves to Bluestem follow Ortega's base.
- **Position and dominance.** The decisive step moves four of seven placements (Bluestem 7 to 4, Fifth Street 3 to 5,
  Kessler 0 to 2, Prairie Rose 8 to 7; Lincoln 6, Ortega and North Fork 0 under every method) and three needs (Bluestem 7
  to 4, Prairie Rose 8 to 7, Kessler 4 to 3); every lower rung places another schedule; no rung places the golden. The
  nearest rival is R2c on the last five transitions (Prairie Rose 8 and Kessler 1).
- **Worth.** Graded: the placement and each school's classroom need; never an intermediate a valid method could skip.

## Closure table

Each row's assertion is in `checks.py` (C1 to C22).

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | each school's K-5 primary enrollments on the 2028 to 2032 count days under the 2026 attendance areas, pupils not yet enrolled or born included | filed (FEA-R2 2(a), 2(b)); SF3, SF9 |
| 2 | Unit of account | a pupil, once, at the school of primary enrollment; a classroom of 24 | filed (FEA-R2 2(a), 2(e)) |
| 3 | Attribution window | a pupil belongs to the October count day of the school year | filed (FEA-R2 2(a)); the snapshots |
| 4 | As-of dating | the October 1, 2026 count; files pulled by October 9, 2026 | FEA-R2 2(b); the export manifest |
| 5 | Version basis | one snapshot per count day; the capacity report of September 2026 | asserted (one snapshot per year) |
| 6 | Denominator | rated capacity, permanent classrooms | FEA-R2 2(d); SF6 |
| 7 | Weighting | each school on its own; rates pooled over grades or by grade | C1 asserted (pooled, by grade) |
| 8 | Window length | the history 2013 to 2026 | C1 across windows (all, 8, 5, 3) |
| 9 | Boundary inclusivity | the count day in or out of an entry date | asserted neutral (no entry on a count day) |
| 10 | Rounding path | unrounded average, excess, need rounded up once | FEA-R2 2(e); SF14 |
| 11 | Tie-break | none arises | FEA-R2 3; margins asserted |
| 12 | Maturity and censoring | 2025 births provisional; every count day complete | SF11 asserted |
| 13 | Order of operations | counts, flows, rates, projection, average, excess, need, order, cap | design; the method forced by the data (Ladder) |
| 14 | Row order | none matters | asserted (exports read in reverse) |
| 15 | Duplicate resolution | one primary row per pupil per count day | asserted (unique state ID per snapshot) |
| 16 | Identity normalisation | state ID across layouts; the crosswalk for blanks | the export notes; asserted |
| 17 | Netting against gross | flows kept gross | design |
| 18 | Dimensional units | pupils; classrooms of 24 | FEA-R2 2(e) |
| 19 | Code and status semantics | grade, school and entry codes in two layouts | the export notes; never the stump |
| 20 | Integerisation | the need rounded up; placement whole classrooms | FEA-R2 2(e), 3 |
| 21 | Clause scope | FEA-R2 covers the Elementary Capacity program only | filed |
| 22 | Forward window contents | five count days, kindergartens born 2023 to 2027 | the births file to 2025; 2026-27 births projected, C1 asserted |

## Literal reader

Executing the prompt, Policy FEA-R2, the student-system notes, the births notes and the capacity report word for word
fixes the target (each school's K-5 pupils expected on the October count days of 2028 to 2032 under the 2026 attendance
areas, new kindergartens included, averaged, against rated capacity) and the whole arithmetic from the average to the
placement; it leaves only the projection's method open, and every reading of every term converges on the golden's
placement or violates a quoted line (SF1 to SF16). The easy answers come from easy methods on the same literal target
(ratios on the receiving class, in any window, trended, differenced or raked), never from another reading.

## Oracles

- The capacity report: rated capacity, teaching stations and the portables on each site, no enrollment and no ranking;
  confirms capacity under every method. Its other assigned rooms vary with each building's program rooms and its portables
  include spares and rooms in other use, so it ties to neither ask's figures.
- The October counts and the births themselves: the history every method fits; nothing in them ties only under the
  golden.
- The distractors (the facility condition assessment, the October meal eligibility counts): rank nothing on enrollment;
  the meal counts tie to the October 1, 2026 count under every method (SEP4); the call and both asks unchanged with both
  deleted (SEP1, SEP2).
- Nothing ties only under the golden: no projection, control total or certified figure of 2028 to 2032 ships.

## Ask sheet

**Main call's declared row population:** the two October membership exports (every K-5 row and column), the ID
crosswalk, the school code list, the births file, the capacity report and Policy FEA-R2. Device and hazard rows in it:
0 (asserted, SEP1 to SEP3: the call computed from those files alone is the golden, and the sections, section enrollment,
preschool and special education files are read only by the asks). Neither ask is keyed to the call, its construction or
its figures; they share no primary device.

**Ask A. Each school's homeroom classes meeting on October 1, 2026, in kindergarten to grade 2 and in grades 3 to 5**
(14 figures).
- H18 home: the building case for the placement (how many classes each school runs this fall in its permanent
  classrooms), a measure every school carries that the call does not turn on; in the board packet's words ("homeroom
  classes").
- The unit, filed once in the student-system notes (stage 4 repair of the judge's Gate E finding), in the system owner's
  voice: "For class-size reporting the district counts classes, not sections. A homeroom class is one room in one
  session (FULL, AM or PM), whatever the number of homeroom section rows or teachers of record in it, and it is counted
  in the grade or grades of the pupils enrolled in it. A class meets on a day when one of its sections is open that day
  with at least one pupil enrolled." It settles the combination and co-taught sections, the half-day pairs, the
  placeholder (no pupil), the sections ended or opened around the count day (none starts or ends on October 1, A4) and
  the band.
- Golden (`figures.json` `ask_a_homeroom_classes`, K-2 and 3-5, unchanged by the repair): Fifth Street 17 and 17,
  Lincoln 19 and 15, Ortega 19 and 13, Bluestem 15 and 20, Prairie Rose 21 and 20, Kessler 15 and 17, North Fork 13 and 13.
- Primary device A3 (D2, a label stored before a silent switch): in the September rebalance every school opened a class
  for a grade that came in above the spring master schedule on a spare section the schedule had built for a
  neighbouring grade; the section keeps its course. Ten such classes cross the band line, five each way (grade 3
  classes on spare HR-2 sections at Fifth Street, Kessler, North Fork and Prairie Rose, two there; grade 2 classes on
  spare HR-3 sections at Ortega, two there, Bluestem, Lincoln and Prairie Rose), and four stay inside a band (Fifth
  Street, Kessler, Ortega, Prairie Rose), one to four a school. Every school's net shift by course code is nonzero
  (Ortega two out of K-2, Bluestem and Lincoln one out, the other four one in), so the filed count executed with each
  class's grade read off its sections' course codes misses all 14 figures (A3g, A7); the pupils' grades on the October 1
  count (a join through the section enrollment lines) put each class in its band. Only the cross-file cut shows it: the pupils' earlier lines in the grade's other classes end the school day
  before the class opened (A7c).
- Second devices A1 and A2 (now executed by anyone who reads the notes): combination and co-taught classes on two
  sections, half-day kindergarten pairs in one room.
- Hazards: HA1 a homeroom section ended on September 18 when its teacher left, the class re-opened as a new section in
  the same room on September 21 (Bluestem grade 4, Lincoln grade 1); HA2 a placeholder section with no pupils (North
  Fork grade 4, room TBD); 19 withdrawals with lines ending October 2 to 8 and 11 late enrollees from October 5 (neither
  moves a figure); intervention sections in the resource rooms.
- Stops (measured, `calc.ask_a`, A3 to A3g), every alternative reading against the golden: section rows (14 of 14 off,
  ruled out by "whatever the number of homeroom section rows"); merged by teacher (14 of 14 off, "teachers of record",
  "one session"); merged by room alone (off at the three half-day K-2 bands, "one room in one session"); every fall
  homeroom section (14 of 14 off, "open that day with at least one pupil enrolled"); classes without the pupil test (off
  at North Fork 3-5, "at least one pupil enrolled"); classes without the date filter (the same figures, converging);
  classes banded by course code (14 of 14 off, "counted in the grade or grades of the pupils enrolled in it"); the golden.
- Span: the sections export, the section enrollment export, the October membership, the student-system notes (4 files);
  13 columns.
- Realism: a student system schedules a combination class one section per grade and a co-taught class one section per
  teacher; a scheduler rebalancing in September reuses an unfilled section rather than building a new one, and the
  course it was built with stays on it.

**Ask B. At each school with a preschool (Ortega, Fifth Street, Kessler, North Fork), the children enrolled in its
preschool classes on October 1, 2026 and the classrooms those classes use** (8 figures).
- H18 home: building use outside the K-5 rated capacity the standard places on, a measure every hosting school carries
  that the call does not turn on; in the preschool office's words ("children enrolled", "classrooms").
- Filed in the roster's own notes sheet (stage 4 repair of the judge's itinerant note and the reader's classroom
  question, and the re-read's two points), in the special education department's voice: "Case school: the elementary
  school whose special education team holds the child's IEP case." "State ID: the child's state-assigned student ID, the
  key for a child across this roster and the preschool registration platform; a child is counted once however many
  enrollment rows the platform holds for them." "Service model: ECSE classroom, a district preschool class taught by an
  early childhood special education teacher; Inclusive classroom, a district preschool class the child attends with
  special education support; Itinerant, special education services at the child's home or community preschool. A child
  served itinerantly is not enrolled in a district preschool class." "Classroom: the school and room where the child's
  class meets. A morning and an afternoon class in the same room share the classroom."
- Construction: the platform's enrollments open on October 1 at the site plus the roster's children whose class meets at
  the site (the school in the Classroom), each child once by state ID; classrooms as the distinct rooms.
- Golden (`figures.json` `ask_b_preschool`, unchanged by the repair): Fifth Street 88 children and 4 classrooms, Ortega
  94 and 4, Kessler 51 and 3, North Fork 35 and 3.
- Primary device B3 (D7, the true key in another field): the special education classrooms are district programs, and at
  every site the team holds the case of a child whose class meets at another site (Ortega's at Fifth Street, Fifth
  Street's at Kessler, Kessler's at Ortega and North Fork, North Fork's at Kessler). The roster is listed by case school;
  grouped by its own key it misses all 8 figures (Fifth Street 89 and 5, Ortega 93 and 5, Kessler 50 and 5, North Fork
  36 and 4).
- Second devices B1 (D4, a reporter absent: the special education classroom children are not on the platform; the
  platform alone gives 77, 79, 32 and 29 children) and B2 (D1, one child under two keys: a re-registered child under two
  platform records at every site, and inclusive children on both sources).
- Hazards: HB1 morning and afternoon half-day classes share a room (Ortega, Fifth Street, Kessler), so classes counted as
  classrooms overcount there; HB2 a child who moved sites in September (North Fork to Kessler, Fifth Street to Ortega;
  the old enrollment ended) and three September withdrawals; a waitlist offer starting October 5.
- Stops (measured, `calc.ask_b`, B2 to B2f), every alternative reading against the golden: the platform alone by state ID
  and room (8 of 8 off, ruled out by "ECSE classroom, a district preschool class"); platform child records and class
  names (8 of 8 off, "a child is counted once however many enrollment rows the platform holds"); the roster grouped by
  case school (8 of 8 off, "Classroom: the school and room where the child's class meets");
  the itinerant children added (92, 96, 54, 37: over at 4 of 4, "not enrolled in a district preschool class"); classes
  counted as classrooms (over at the three half-day sites, "share the classroom"); the two sources added without
  matching children (over at 4 of 4); the golden.
- Span: the platform export, the special education roster and its notes (2 files); 10 columns.
- Realism: a registration platform opens a new child record on each application; special education preschool placements
  are made through the special education system, and a district classroom serves children whose cases sit with their
  home school's team.

**The chart** (about 5 criteria): seven panels, each school's October K-5 counts 2013 to 2026 (from the membership
exports) and the projection 2027 to 2032, rated capacity drawn across each, and capacity with its placed classrooms from
2028.

**Hazard table**

| Hazard | Root cause | Moves | Per-ask delta |
|---|---|---|---|
| HA1 a section ended mid-September | a teacher's departure | Ask A, 2 schools | +1 at Bluestem 3-5 and Lincoln K-2 on the every-section stop |
| HA2 a placeholder section | a class planned in spring that did not open | Ask A, 1 school | +1 at North Fork 3-5 without the pupil test |
| HB1 sessions sharing a room | half-day programs | Ask B, 3 sites; Ask A's half-day kindergartens share the cause | +2 to +3 classrooms counting classes |
| HB2 a September site change or withdrawal | a family move | Ask B, 4 sites | +1 child on an undated count |

**Referee.** For Ask A, the pupils' grades on the October 1 count; for Ask B, the school in the roster's Classroom and the
state ID on both sources. Each is a field the golden reads, not a control: no file ties only under the golden.

| Ask figures | Cracker's path | Cracker's value | Verdict |
|---|---|---|---|
| A homeroom classes, K-2 and 3-5 (14) | the filed class count executed on the sections (one room in one session, open on October 1 with a pupil enrolled), each class's grade read off its sections' course codes | each school's September classes on spare sections from the other band shift its bands by one or two: every figure off | miss |
| B children and classrooms (8) | the platform's enrollments open on October 1 and the roster's in-class children, each child once by state ID, itinerant children out, rooms distinct, the roster's children placed by its case school | every site gains or loses a child and a room to another site: every figure off | miss |
| the chart | the cracker's projection drawn as the golden draws it | the history, capacity and its own projection | outside |

Mirror leakage: about 16 per cent of the ask weight (the mirror runs the same ask paths as the cracker and keeps only the
chart's structural criteria: the panels, the history, a projection line and the capacity lines).
Pair ceiling: 39 (on a rubric of about 32 for the call and needs, 7 for instructions and 61 for the asks: the cracker 32
plus 7 plus the chart's 9, 48; the mirror keeps the placements and needs every method shares, Lincoln's, Ortega's and
North Fork's placements and Fifth Street's, Lincoln's, Ortega's and North Fork's needs, about 14, plus 7 and the chart's 9,
30; 22 ask figures held on both paths).

## Tried and rejected

- The seed's mechanism (pupils per new home by the age of the home, against a developer-agreement template of 0.45):
  rejected at the draw, a yield by housing age is task134's ground and the template is a decoy-era official rival.
- A births-to-kindergarten ratio pooled across the district against each area's own ratio: rejected at the draw, a
  pooled against a stratified rate is a reflex and the field's textbook already stratifies.
- A charter school opening and drawing kindergartners from nearby areas, sized on one past opening: rejected at the
  draw, the decisive step would rest on a single past event and the opening would be a dated cause stepping the series.
- Capacity-censored enrollment (overflow pupils sent to other schools when a grade fills): rejected at the draw, the
  estimand would have to name residence or attendance, and either filing hands over the step or leaves a fork.
- Gap population with G16 (the first draft): the signature (population, G16, method_or_model_selection) is spent in
  four older builds; redrawn as gap time, G6, Gate G forecasting, which is the honest reading of the step.
- A world with the forward shifts only after the history (feeder births falling after 2020, arrivals schools' births
  falling after 2022): the closed record blessed the progression ratios (back-test errors of GPR and of the gross-flow
  model within a point of each other), the validated-decoy architecture the guard blocks; redrawn so each shift is
  already under way in the history (Fifth Street's births fall from 2012, Prairie Rose's rise from 2011, Ortega's peak
  in 2017) and the five-year ratios miss the 2020-26 counts by 7 to 9 per cent at those schools out of sample.
- Not-geocoded and late-registration counts drawn binomially per area: on small areas they moved single years' births
  by up to 5 per cent, so the pack's default and the clean truth's sat on either side of Bluestem's bin edge (6 against
  7); replaced by fixed shares of each area's births (never shipped per area), and Bluestem's target excess set to 86 so
  the default's Bluestem (146.6 on the pack, 147.3 on the truth) clears its edge while the golden keeps one sigma.
- Preschool rooms laid out so the missing special education room and the doubled morning and afternoon class names
  cancelled (the naive classroom count right at every site): rearranged so the two errors no longer offset (B2'').
- A capacity report whose other assigned rooms were six at every school without a preschool, so the preschool sites'
  excess over six was Ask B's classroom figure (an oracle): program rooms now vary by building and portables include
  spares and rooms in other use.
- Half-day kindergarten pairs under two teachers: the teacher merge landed the three half-day bands; one teacher teaches
  both sessions, as half-day kindergarten runs (A3').
- "The 2019 migration" for the student-system move in the notes and the manifest: it echoed the stump's vocabulary for
  a reader scanning the pack; renamed the 2019 conversion, IT's own word for it.
- Ask A's unit left to the plain meaning of a homeroom class, asserted only as a data fact: the stage 4 judge read the
  notes' "section ... meets in a room and session" as the unit and counted section rows (Gate E, FIX_NOW). The unit is
  now filed in the student-system notes as the district's class count; filed, it hands a careful reader the
  combination, co-taught and half-day devices, so the ask's silent device is the September rebalance (a spare
  section's course stored before the switch), which the filed count's own words resolve only through the pupils'
  grades.
- Ask B's roster without notes, the itinerant children and a room shared by morning and afternoon classes left to plain
  meaning: the judge noted the first and the reader raised the second; both filed in the roster's notes sheet, which
  hands over the old children device to a reader of the roster, so the roster now lists children by the team that holds
  the case and the class's school sits in the Classroom (the true key in another field).
- A September rebalance with one cross-band class at every school, six of the seven a grade 3 class on an HR-2
  section: the stage 4 re-read found the concentration on the band line could read as planted. Remixed to both
  directions (five each way), one to four off-code sections a school beside the four inside a band, every school's net
  shift by course code still nonzero (A7); every golden figure unchanged.
- An ECSE classroom defined as "a district early childhood special education classroom", the platform's repeat rows
  left to the hygiene check: the re-read could not find a sentence putting those children in preschool classes, or one
  counting a child once across the platform's rows; both filed in the roster's notes.

## Build record

Stage 3, built 2026-10-16 from `task150/generator/build.py` (seed 50).

- Pack: 16 files, 4 formats (csv, pdf, txt, xlsx); the largest `october_membership_2019-2026.csv`, 44,314 rows, the spine
  76,597 pupil rows over 14 count days; distractors `facility_condition_assessment_2025.xlsx` and
  `meal_eligibility_2026-10.csv` (metadata.json).
- Main call from the shipped files: Prairie Rose 7, Lincoln 6, Fifth Street 5, Bluestem 4, Kessler 2 (needs 7, 6, 5, 4, 3,
  North Fork 1, Ortega 0; 26 against 24). Excess over rated capacity 152.1, 131.2, 108.6, 88.5, 60.0, 9.9 and Ortega
  -91.8; standard errors 7.7, 4.7, 7.7, 6.1, 6.3, 5.2. The default (five-year progression ratios) Bluestem 7, Fifth Street
  3, Lincoln 6, Prairie Rose 8 on the pack and the clean truth alike. Every construction one schedule (B2).
- Mess variants (R2): the 2019-26 export alone, linking by the SASID on the row, Kessler fitted on its post-rename
  Octobers, births not geocoded spread pro rata, 2025 births completed: the golden schedule and needs in every case.
- Gates: `checks.py` 132 assertions, 0 failed; `verify.py` agrees on its own pandas code path (placement, needs, three
  constructions, the default, all 22 ask figures, the workbook and the write-up); two byte-identical builds (target,
  goldens, metadata.json, submission.md, figures.json, target.zip); container audit clean on the pack and the goldens;
  `figures_check.py` 41 figures, 0 absent; `precut.py` 49 checks, 0 FAIL; `voice-check.py` PASS (785 characters);
  `leak.py` REVIEW, no LEAK (answered below); `guard.py heart` WARN (overuse.objective, answered under Draw); `guard.py
  surface` promotes task125 at surface 0.077 on the cards' same-driver signature (gap time, G6, Gate G forecasting) and the
  shared filed_standard context artifact, differentiated on the card (task125 v2 filters recruits out of a rotating panel;
  here nothing is filtered and the step is the population each flow is a rate on); the adjudicated clone read is the
  author's call.
- Golden realism and house fixes: the workbook's title states the placement, the need computed from the unrounded
  average, number formats, frozen headers, a total row, a notes sheet with the method, its back-test and the sources; the
  chart's title states the finding, the placed schools in the accent colour, capacity labels clear of the lines; the
  manifest's names equal the shipped set (G5, H9); every file the write-up names ships (GD8, H8); no record dated after
  the pull bar the sections' planned end dates (C4, H16).
- Stage 4 (the leak reader clean on Q1 to Q6 with the decisive step analytical; the rule 3 audit PASS; the judge
  NOT_DETERMINISTIC on supplementary answer 2 only, FIX_NOW, with the main call reproduced exactly and Gate H analytical)
  and the repair: the class count filed in the student-system notes; the roster's notes sheet (case school, service
  models with the itinerant children out of class, the classroom as a room shared by morning and afternoon classes);
  the September rebalance in the sections and the case schools in the roster as the asks' silent devices. Every
  alternative reading asserted against the golden (A3 to A3g, B2 to B2f). Against the stage 3 cut 0018d35 the main
  call's files (both membership exports, the crosswalk, the code list, the births file and its notes, the capacity
  report, the policy, the two distractors and the preschool platform) are byte-identical and every figures.json value is
  unchanged, the call, the needs, the default, the rivals, the projection and both asks' goldens included; the sections,
  the section enrollment, the roster, the student-system notes and the manifest moved. `checks.py` 143 assertions, 0
  failed; verify agreeing; two byte-identical builds; figures_check 41 of 41; precut 49; voice-check PASS on the
  unchanged prompt; leak.py REVIEW, no LEAK; container audit clean; heart WARN answered; surface as at stage 3.
- Stage 4 close: the re-judge on the repair cut b475530 DETERMINISTIC and APPROVE, the main call and both ask tables
  reproduced, Gates G and H pass (`determinism_check_report.md`; its optional prompt pin on validation not taken, it
  files the HOW); the re-read clean on the main call, its two items fixed with every golden figure frozen: the rebalance
  remixed (A7) and the roster's notes extended (B0). Against b475530 the main call's files, the student-system notes,
  every figures.json value and the write-up are byte-identical; the sections, the section enrollment, the roster and the
  manifest moved. `checks.py` 143 assertions, 0 failed; verify agreeing; two byte-identical builds; figures_check 41 of
  41; precut 49; voice-check PASS; leak.py REVIEW, no LEAK; container audit clean; heart WARN answered; surface as before.

## Pre-ship check

The 10/10 rules read again against the shipped cut.
- Domain: the deciding quantity is each school's projected October K-5 enrollment by grade, built as a small-area
  cohort-component projection with gross flows; two judges and the rule 3 audit read it as the field's own method, and
  the swap test breaks it.
- Two layers: the mess (two student-system layouts and the conversion crosswalk, blank state IDs, the Southeast rename,
  moved count days, geocoded and provisional births) is what the systems write and stays neutral (R2a to R2f); the
  analysis decides: five-year progression ratios file Bluestem 7, Fifth Street 3, Lincoln 6 and Prairie Rose 8 on the
  clean truth and the pack alike (R3a).
- Rule 3: nothing is planted, no field reading decides the call, and the shipped HOW sentences name records, never a
  method (R3s); the decisive step is analytical.

## Leak review

`leak.py --asof 2026-10-09` on the stage 4 close cut: REVIEW, no LEAK. One line per REVIEW line.

- Sweep 3, the policy carries 12 of 13 words of the call: section 1 lists the seven schools the program places among, in
  the board's code order, with no figure and no order of need; the estimand's filing, harmless.
- Sweep 4, the policy, the births notes, the student-system notes and the legacy export (school names, pupils, counts,
  births, outside, district): the schools' own names and record words; none names a method, a ratio, a rate or how
  arrivals or moves behave (R3s asserted); the notes' class count defines an ask's unit, not the call's; harmless.
- Sweep 6, the capacity report, the condition assessment, the membership export, the sections, the preschool platform and
  the special education roster name the schools beside numbers: records by school (capacity, condition, pupils, sections,
  enrollments, cases), none ranks the schools on the placement; harmless.
- Sweep 9, the sections' 288 dates after the pull: each section's planned end, May 27, 2027 (H16 allow-list, C4);
  harmless.
- Round 3, the coordinator's targeted re-read on 40a2abe: clean; the main call analytical, nothing planted, both asks
  read one way from the filed text. Its residual note, that the whole-section off-codes look interlocking, is accepted:
  spring-built sections repurposed in September carry their course whole.
- The births file's boundaries in effect 08/01/2026 are the areas the policy names as in effect on October 1, 2026: the
  pack records no attendance-area change between the two dates, the policy's one change clause concerns changes after
  October 1 (C1b); no fix.
