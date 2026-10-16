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
| Spine | the student information system's October membership snapshots, one row per pupil enrolled in K-5 on one October count day, 2013 to 2026 in two layouts (constructed, about 75,000 rows) |
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
