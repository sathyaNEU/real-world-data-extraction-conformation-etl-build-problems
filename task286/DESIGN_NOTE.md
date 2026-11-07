# task286 design note

Architecture 1, drawn 2026-11-07. Which shortlisted community area the National Homes Agency's 2027 Homes in Use
pilot runs in: the area with the most homes nobody used for at least 26 of the 52 weeks from Monday 29 September
2025 to Sunday 27 September 2026, read from Pennimouth Water's daily smart meter totals for every home. The number
is fixed in Descriptive & Distribution Analysis by `START_HERE.md`; its seed (DA36, a preprint server's moderator
by category) supplied the objective only, for the reasons in `## Tried and rejected`.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task286.json`, architecture v1, registered 2026-11-07 |
| Client domain / task type | General Statistics & Data Science (`general-statistics-data-science`), `missing-data-censoring-measurement-error` (serves DD): a quantity read through an instrument whose error is structured, separated from the signal by the error's own signature |
| Objective | Descriptive & Distribution Analysis: how each shortlisted area's homes divide by the weeks nobody used them in the year to 27 September 2026, and where the tail of homes left empty for at least half the year is largest |
| Decision | which shortlisted community area the pilot runs in, the one with the most such homes (`pick_one_of_n`). A retrospective quantity for a forward call: the pilot works through 2027 with the homes standing empty now, and a home's emptiness is read off its last year of use; nothing is forecast, so the tag stays Descriptive |
| Shape | 01: every shortlisted area's count of homes left empty for 26 or more weeks, its rank and the call with runner-up and gap, then per-area asks and the chart's named parts; the arithmetic goes in `## Ask sheet` at stage 2 |
| Gap / pattern / generators | `population` (which homes are in the population left empty); pattern `none`; `G16` decisive (the measurement model a week of use is read with), `G12` (the council tax record's absence of an empty status read as a record of use, rung 0) |
| Gate G | `decomposition_attribution`: each home's correctly metered volume is split between a steady flow that has nothing to do with use and the use itself |
| Strategy | `population_selection`; Layer 2 family `estimation_fit`; pattern `own:occupancy-read-from-day-to-day-variation-where-leaks-flow-steadily` |
| Forum, forcing event, org family | `minister_or_cabinet` (the housing minister announces the pilot area on the agency's recommendation), `launch_or_rollout` (the pilot opens in April 2027), `government_agency` (a national housing agency in England) |
| Role | the agency's housing evidence lead, preparing the area recommendation (`research_desk`) |
| Context artifact | `published_series`: the census 2021 tables and the councils' Council Tax Base return sit beside the administrative extracts the agency was sent |
| Calibration | none |
| Personas | Toby Hunt (the agency's housing evidence lead, the golden's author), Melissa Robson (the pilot's programme manager, author of the terms of reference), Tracy Hawkins (Pennimouth Water's data sharing officer), Robert James (Teversby District Council's revenues manager), from `guard.py names --geo england --seed 286`; Abigail Ford, Lindsey Craig, Stacey King, Sheila Garner, Adrian Collins and Richard Morley from the same draw were dropped on `people.first` |
| Fiction as-of date | 2026-10-19 (the evidence lead's working date; the meter extract runs to 27 September 2026 and the council tax extracts are taken on 5 and 6 October 2026) |
| Guard | `guard.py check` on the first draft BLOCKed `ban.pattern` (G3, record versus operation, against task399), `test.same_puzzle` against task210 and the older same-puzzle and same-driver signatures (population, G3 or G16, `method_or_model_selection`, spent in eight builds). Redrawn: decisive generator G16, Gate G `decomposition_attribution`, which is the honester key anyway, because the meter's volume is correctly reported and the decisive step splits it between two sources rather than choosing between two defensible methods. The register-time check is WARN only, answered below |

**The world.** The National Homes Agency (an invented national housing agency in England) runs Homes in Use, a
pilot that from April 2027 puts an empty homes officer, grants for repairs and a leasing offer into one community
area of an invented coastal county, working with the owners of homes that stand empty. The pilot's terms of
reference file the WHAT: the pilot goes to the shortlisted community area with the most homes nobody used for at
least 26 of the 52 weeks from Monday 29 September 2025 to Sunday 27 September 2026, counting every self-contained
home in the area however it is taxed or let, a week counting as a week of use when anybody lived in, stayed at or
used the home on any day of it. The evidence is Pennimouth Water's daily smart meter totals for every home in the
shortlisted areas (shared under a data-sharing agreement for the pilot), the water company's match of its
properties to the county address gazetteer, the gazetteer itself, the two district councils' council tax
extracts (Teversby District Council moved to a new revenues system in May 2025, so its extract comes in two
layouts), the business rates list of self-catering lets, the census 2021 household spaces table with its output
area lookup, and the documents around them.

**Why the world moved.** DA36 sends one volunteer moderator to the category whose moderation load grew most. Its
load is a count of logged actions, and whatever decides the count is a routing or credit rule (which queue a
cross-list reaches, which action earns a credit) or which category an item belongs to: rule application or data
semantics under the 10/10 rules, and the swap test reads it the same for any review queue. No task type that
serves Descriptive & Distribution in Product Analytics carries a measurement the field would model there. The
number keeps its objective and moves to General Statistics & Data Science, where reading a population through an
instrument with a structured error is the task type itself.

**The 10/10 rules at the draw.** `stump_class` analytical. The deciding quantity (each home's weeks without use)
is one the field measures and models: the water industry's void read takes a home as empty in a week it draws no
water or less than a low volume, and the measurement-error analysis separates the instrument's structured error
(a customer-side leak's flow, which repeats from one day to the next) from use (which never does). Layer 1 is the
mess the councils' and the water company's systems make (two council tax layouts across a system move, properties
the water company could not match to a UPRN, meter exchanges with two rows on the exchange day, estimated reads
apportioned flat across a communication gap, UTC meter days against Monday-to-Sunday weeks, the census carried to
community areas by a best-fit lookup); none of it moves the call. Layer 2 decides: on the generator's clean truth,
with every key and code right, the void read still files the wrong area, because leaks are physical and the clean
meter records them.

**Data-native sentence.** Pennimouth Water's meters record every litre that passes them, and in Orrimouth's
long-neglected terraces a worn cistern valve or a weeping supply pipe runs on with nobody there to hear it, so an
empty home records the same few hundred litres every day, which reads as a household in any weekly or yearly
total and shows only in the home's own run of days.

**Default path (draft, priced on the clean-truth prototype, four seeds).**
1. Read the daily meter totals, adding the two rows of a meter-exchange day into one day per property.
2. Join each water property to its UPRN through the water company's match and each UPRN to its community area
   through the gazetteer, placing the properties the match left without a UPRN by postcode.
3. Give each day its Monday-to-Sunday week and sum each home's litres per week.
4. Read the void weeks the industry's way: a week in which the home drew no water, or less than a few days of one
   person's use (for example under 300 litres in the week).
5. Count the homes with 26 or more void weeks in each area and name the area with the most.
- Ends on: Ellingsea (on the prototype about 150 homes against Orrimouth's 115, ahead on all four seeds).
- Golden: Orrimouth (on the prototype 20 to 47 per cent ahead of the runner-up on all four seeds).

**Stump sentence (draft).** A competent analyst counts each home's void weeks from the daily meter totals (no
water, or under a few days of one person's use) and names Ellingsea, whose empty homes are mostly sound-plumbed
flats; the step that lands it there is reading a leak's steady daily flow as use, which drops Orrimouth, whose
neglected empty terraces run their cisterns all year, out of first place.

**Guard answers (register time, WARN only).** `people.first` (Robert against task104, one older build): a common
first name drawn by the tool, kept. `overuse.org_family` (`government_agency` in 39 builds): a national housing
agency choosing a pilot area is a government agency by kind; the axis is free in the window. `repeat.gate_g`
(`decomposition_attribution` against task399 and task211): the honest key, and the mechanisms share nothing
(task399 books delay minutes to a cause, task211 tells an artificial excursion from washout by its decay; here a
home's metered volume is split between a leak and use by its constancy). NOTE lines `test.same_puzzle_older`
(task260, task464 v8) and `test.same_driver_older` (task236, task464 v8) are differentiated on the card. Nearest
drivers 0.08 (two undrawn task307 entries) and 0.06 (task485, task476 v5, task464).

## Tried and rejected

- 2026-11-07, at the draw: seed DA36's world (moderation load by subject category) set aside, because its load is a
  count of logged actions decided by a routing or credit rule or by category membership, which is rule application
  or data semantics, and the swap test reads it the same for any review queue.
- 2026-11-07, at the draw: directions screened on this lane's spent ground and dropped before carding. Deleted or
  erased accounts in a user base (entities that enter and exit are Layer 1, task179's verdict and task276's
  screen); timed transit connections (task285's time-coincident abstraction); pharmacy shortage gaps (task303's
  co-occurrence driver); interpreter co-location (task114's co-presence); stadium sightlines (the task276 and
  task256 family); smoke-alarm current status (no decisive step beyond the textbook); residential segregation
  indices, vignette weighting, capture-recapture and multilevel regression with poststratification (each on the
  lane's screen lists in tasks 268 to 285).
- 2026-11-07, at the draw: the first card's generators G3 (record versus operation) BLOCKed on `ban.pattern`
  against task399, and the G16 plus `method_or_model_selection` signature with gap `population` is spent in eight
  builds; redrawn to G16 with `decomposition_attribution`, the honest Gate G key for a volume split between two
  sources.
