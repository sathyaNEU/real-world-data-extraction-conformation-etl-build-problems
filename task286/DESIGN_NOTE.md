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
| Objective | Descriptive & Distribution Analysis: how each shortlisted area's homes divide by the weeks nobody used them in the year to 27 September 2026, and where the tail of homes left unused for half the year or more is largest |
| Decision | which shortlisted community area the pilot runs in, the one with the most such homes (`pick_one_of_n`). A retrospective quantity for a forward call: the pilot works through 2027 with the homes standing empty now, and a home's emptiness is read off its last year of use; nothing is forecast, so the tag stays Descriptive |
| Shape | 01: every shortlisted area's count of homes left unused for 26 or more weeks (8), the call, runner-up and gap (3), two asks of one figure per area (16), the chart's parts (one bar per area, three segments, segment labels, about 4) and the two files (2): about 33 criteria from the structure |
| Gap / pattern / generators | `population` (which homes are in the population left unused); pattern `none`; `G16` decisive (the measurement model a week of use is read with), `G12` (the council tax record's absence of an empty status read as a record of use, rung 0) |
| Gate G | `decomposition_attribution`: each home's correctly metered volume is split between a steady flow that has nothing to do with use and the use itself |
| Strategy | `population_selection`; Layer 2 family `estimation_fit`; pattern `own:occupancy-read-from-day-to-day-variation-where-leaks-flow-steadily` |
| Forum, forcing event, org family | `minister_or_cabinet` (the housing minister announces the pilot area on the agency's recommendation), `launch_or_rollout` (the pilot opens in April 2027), `government_agency` (a national housing agency in England) |
| Role | the agency's housing evidence lead, preparing the area recommendation (`research_desk`) |
| Context artifact | `published_series`: the census 2021 tables and the councils' Council Taxbase returns sit beside the administrative extracts the agency was sent |
| Calibration | none |
| Personas | Toby Hunt (the agency's housing evidence lead, the golden's author), Melissa Robson (the pilot's programme manager, author of the terms of reference), Tracy Hawkins (Pennimouth Water's data sharing officer), Robert James (Teversby District Council's revenues manager, drawn and not named in the pack), from `guard.py names --geo england --seed 286`; Abigail Ford, Lindsey Craig, Stacey King, Sheila Garner, Adrian Collins and Richard Morley from the same draw were dropped on `people.first` |
| Fiction as-of date | 2026-10-19 (the evidence lead's working date and the pack's export date; the meter extract runs to 4 October 2026, the council tax extracts are taken on 5 and 6 October 2026, the gazetteer on 7 October and the rating list on 8 October) |
| Guard | `guard.py check` on the first draft BLOCKed `ban.pattern` (G3, record versus operation, against task399), `test.same_puzzle` against task210 and the older same-puzzle and same-driver signatures (population, G3 or G16, `method_or_model_selection`, spent in eight builds). Redrawn: decisive generator G16, Gate G `decomposition_attribution`, which is the honester key anyway, because the meter's volume is correctly reported and the decisive step splits it between two sources rather than choosing between two defensible methods. The register-time check is WARN only, answered below |

**The world.** The National Homes Agency (an invented national housing agency in England) runs Homes in Use, a
pilot that from April 2027 puts an empty homes officer, repair grants and a leasing offer into one community area
of an invented coastal county, working with the owners of homes that stand empty. The pilot's terms of reference
file the WHAT (4.1 to 4.3): the pilot goes to the shortlisted community area with the most homes nobody used for at
least 26 of the 52 weeks from Monday 29 September 2025 to Sunday 27 September 2026, every self-contained home on the
county gazetteer counting however it is taxed or let, a week counting as a week of use when anybody lived in,
stayed at or used the home on any day of it. The evidence is Pennimouth Water's daily smart meter totals for every
home in the shortlisted areas (shared under a data sharing agreement for the pilot), the water company's match of
its properties to the county address gazetteer, the gazetteer itself, the two councils' council tax extracts
(Teversby District Council replaced its revenues system on 5 May 2026, so its records come as an archive to 4 May
and a new extract), the business rates list's self-catering entries, the census 2021 household spaces table with
its output area lookup, the councils' October 2025 Council Taxbase returns and the 2024 Housing Needs Assessment.

**Why the world moved.** DA36 sends one volunteer moderator to the category whose moderation load grew most. Its
load is a count of logged actions, and whatever decides the count is a routing or credit rule (which queue a
cross-list reaches, which action earns a credit) or which category an item belongs to: rule application or data
semantics under the 10/10 rules, and the swap test reads it the same for any review queue. No task type that
serves Descriptive & Distribution in Product Analytics carries a measurement the field would model there. The
number keeps its objective and moves to General Statistics & Data Science, where reading a population through an
instrument with a structured error is the task type itself.

**Data-native sentence.** Pennimouth Water's meters register every litre that passes them, and in Orrimouth's
neglected terraces, emptied after the fish dock's processing plant closed in December 2021 and never handed back
to the council, a worn cistern valve or a weeping supply pipe runs on with nobody there to hear it, so an empty
home registers the same few hundred litres every day, which reads as a household in any weekly or yearly total and
shows only in the home's own run of days.

**Guard answers (register time, WARN only).** `people.first` (Robert against task104, one older build): a common
first name drawn by the tool, kept. `overuse.org_family` (`government_agency` in 39 builds): a national housing
agency choosing a pilot area is a government agency by kind; the axis is free in the window. `repeat.gate_g`
(`decomposition_attribution` against task399 and task211): the honest key, and the mechanisms share nothing
(task399 books delay minutes to a cause, task211 tells an artificial excursion from washout by its decay; here a
home's metered volume is split between a leak and use by its constancy). NOTE lines `test.same_puzzle_older`
(task260, task464 v8) and `test.same_driver_older` (task236, task464 v8) are differentiated on the card. Nearest
drivers 0.08 (two undrawn task307 entries) and 0.06 (task485, task476 v5, task464).

**Prompt gate answers.** `voice-check.py` passes with two WARNs. The attributed-opinion WARN is the ask's own
standard ("as the Council Taxbase return defines them"), which names the definition the ask's figure is counted
on, not anybody's view. The shell WARN (deliverable set png and xlsx at 22 per cent against a 20 per cent quota) is
answered at the role level: a workbook and one chart is what an evidence lead sends a minister's office; the
question form is `where` (the card's own) and the rounding sentence opens with "Every count", both under quota.

## Three rules

- **Task type:** `missing-data-censoring-measurement-error` in General Statistics & Data Science, serving
  Descriptive & Distribution Analysis: each home's weeks without use measured through an instrument (its water
  meter) whose error is structured, and the population left unused described area by area.
- **Domain test:** the deciding quantity is each home's weeks without use; the water industry's own test for it is
  the void read, a week in which the meter registers no consumption or less than a low volume, and here that test
  is rung 2 of the ladder and files the wrong area.
- **Swap:** "Orrimouth takes the pilot because its homes nobody used are found once each meter's steady flow is
  split from use": with a generic summary of the measurement (litres a week under any line, litres a year) in place
  of the model of the measurement, the sentence names Ellingsea, so the call lives in the task type's own object
  (a measurement with an additive error identified by its signature), not in the housing nouns.
- **Layer 1:** Teversby's two council tax layouts (the archive of its previous revenues system closed 4 May 2026,
  the new system from 5 May, written by the migration); properties the water company's July 2026 address matching
  left without a UPRN (billing address and postcode only); meter exchanges with two rows on the exchange day and
  estimated days spread evenly across a communication gap (both written by the meter head end); UTC meter days
  against Monday-to-Sunday weeks; census output areas carried to community areas by the county's best-fit lookup;
  the rating list keyed by its own BA reference, linked to the gazetteer through the gazetteer's cross-reference,
  with a holiday site's cottages under one entry; dates in two formats (the archive's dd/mm/yyyy, ISO elsewhere).
  Nothing is placed to be caught, and each item is neutral for the call and every critical component (SF7 to SF9,
  R2, asserted).
- **Layer 2:** `estimation_fit` on a measurement with a structured error: the meter registers, in some homes, a
  steady flow that is not use, and the methodological choice that flips the call is reading a week of use as a rise
  above the home's own steady level rather than as litres under a line.
- **Decisive step:** recognising that the meter's litres are use plus a steady non-use flow in some homes (a running
  cistern, a weeping supply pipe: near-identical litres day after day) and splitting the two in each home's own
  sequence of days, so a week counts as used only when its daily totals rise above that home's quiet level.
- **Not semantics:** every field is read right by the easy route: CONSUMPTION_L is the litres the meter registered
  in the UTC day and the easy route uses it as exactly that; what makes it wrong is treating registered litres as
  use, which no field, code, unit or definition says either way, and on the clean truth, with every key and code
  right, the void read still files Ellingsea.
- **Not rule application:** no filed rule or procedure says how a week of use is read from a meter (terms of
  reference 4.3 says only who counts: anybody living, staying or using the home on any day), so executing every
  stated rule leaves the reading open. The enumerated family (25 routes in `checks.py`: void weeks under 1 to 1,400
  litres, no day over 1 to 150 litres, a year under 1 to 30 cubic metres, a week under a tenth of the home's median
  week, three council tax readings, the 2021 census, the void read joined to the council tax status) files four
  different areas, Ellingsea, Kittlesea, Tarnhithe and Brackwater, and never Orrimouth; the standing family (each
  week read against the home's own steady level, by the week's range or by the home's lowest day, at any margin
  from 30 to 75 litres) files Orrimouth and the same count in every area, a spread of 0 homes; and the ruling-out is
  quiet: only the homes' own runs of near-identical daily totals refute the volume routes, which no column, document,
  control or count names.
- **Analyst test:** a strong analyst who cleans every file and reads every rule correctly counts each home's void
  weeks (no water, or under 300 litres in the week) and files Ellingsea at 161 homes against Orrimouth's 85, because
  a cistern running on in an empty home registers the same few hundred litres every day and every volume line reads
  it as a household.
- **Estimand:** terms of reference 4.1 to 4.3 (`homes_in_use_pilot_terms_of_reference_v1-2.pdf`): the shortlisted
  community area with the most homes (self-contained dwellings on the county gazetteer, however taxed or let) that
  nobody used for at least 26 of the 52 Monday-to-Sunday weeks from 29 September 2025 to 27 September 2026, a week
  counting as used if anybody lived in, stayed at or used the home on any day of it; every home in the areas is in
  the population, whether or not any record shows it empty.
- **No decoy:** nothing is planted to be caught: no document argues for Ellingsea, names a volume rule or a leak; the
  council tax records and the census are true records on their own bases (the housing needs assessment's census
  table is a declared wrong-basis distractor ruled out by terms of reference 4.1 and 4.3); the steady flows are
  physical, and the clean meter registers them.
- **No certified replay:** no published or certified figure reproduces under the golden or under the easy route; the
  Council Taxbase returns are district-wide counts the pack cannot rebuild, and nothing in the pack validates or
  refutes a reading of the meters except the homes' own daily totals.
- **Lesson:** a meter measures the instrument's quantity, not the behaviour, so reading behaviour from it needs a
  model of whatever else moves the meter, identified from the data's own signature; no build on file separates a
  constant additive error from a signal by its day-to-day constancy inside each unit's own series.

## Survivor anatomy

- **Actor:** a home's week of use, which no column holds: the meter file carries litres, the meter serial and the
  read type, and no file carries a leak flag, an occupancy marker or a void week.
- **Link:** the signal is a relation between one home's own consecutive meter days (their near-constancy when nobody
  is in), read across rows of the main file; no key, sentence or column invites the comparison.
- **Reflex:** the water industry's void read (a week with no consumption or under a low volume) sits at rung 2 and
  files Ellingsea at 161 homes; every void line from 1 to 1,000 litres files Ellingsea.
- **Back-test:** on the 288 homes the councils' records show unoccupied or exempt on 27 September 2026, the void read
  agrees with the truth on 93.8 per cent: the one labelled set a solver would validate against passes the easy
  route.
- **Second use:** the meter reads, the water company's UPRN match and the gazetteer are read by every route that
  counts homes, the easy one included; no file ships for the decisive step alone.
- **Shock:** the homes the step recovers read as ordinary households in every weekly or yearly total (their steady
  flows run 110 to 950 litres a day, median 266, a two-person household's volume), and Orrimouth tops no simple
  statistic of the pack (`checks.py` C7: homes, mean litres a day, homes with every day zero, lets on the list,
  long-term empty homes).
- **Pins:** the WHAT is filed once, in the terms of reference (4.1 to 4.3) in the agency's own form; no filed
  sentence names a threshold, a leak, a steady flow, a floor, a margin or a void rule, and deleting any of them
  leaves the method open rather than forced.

## Default path

1. Read the daily meter file and add the two rows of an exchange day into one meter day per property.
2. Join each water property to its UPRN through the water company's match and each UPRN to its community area
   through the gazetteer, placing the properties the match left without a UPRN by postcode.
3. Keep the 52 Monday-to-Sunday weeks from 29 September 2025 and sum each home's litres per week.
4. Read the void weeks the industry's way: a week in which the home's meter registered under 300 litres (a few days
   of one person's use), or none at all.
5. Count the homes with 26 or more void weeks in each area and name the area with the most.

- **Ends on:** Ellingsea, 161 homes (Kittlesea 120, Tarnhithe 116, Brackwater 94, Orrimouth 85).
- **Golden:** Orrimouth, 203 homes (Ellingsea 159, a gap of 44).

## Stump sentence

A competent analyst counts each home's void weeks from the daily meter totals (no water, or under 300 litres in the
week) and names Ellingsea with 161 homes, whose empty homes are mostly sound-plumbed flats; the step that lands it
there is reading a leak's steady daily flow as use, which keeps 119 of Orrimouth's 203 unused homes out of its count
and leaves Orrimouth fifth at 85.

## Readability screen

Tests: 1 filed sentence, 2 schema, 3 reflex, 4 control bench, 5 hygiene, 6 linear, 7 second use. The reflex row
is enumerated from the field's vocabulary for a home's weeks of use (void weeks, zero-consumption weeks, a low-use
threshold, annual low consumption, the declared occupancy status), never from the rungs beneath.

| Rung | 1 | 2 | 3 | 4 | 5 | 6 | 7 | Verdict |
|---|---|---|---|---|---|---|---|---|
| 0 council tax status on 27 September 2026 (Kittlesea) | no | status column | declared occupancy is a reflex | none | no | count | yes | readable |
| 1 census 2021 no usual residents (Tarnhithe) | the assessment's table | census column | a reflex for vacancy | none | no | sum | yes | readable |
| 2 void weeks under a low volume (Ellingsea) | no | litres column | the industry's void read | none | no | threshold | yes | readable |
| 3 (decisive) each home's steady flow split from use (Orrimouth) | no sentence names a leak, a floor or a margin | no column flags a steady flow | not a reflex: the field's reflex is rung 2 | no labelled sample scores a reading; the back-test validates rung 2 | the battery does not compare a home's days with each other | a per-home model, not one subtraction | every file it reads is read by rung 2 | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | home | every self-contained dwelling on the gazetteer | parent shells (blocks, holiday sites) counted | same call: shells carry no meter | ToR 4.2; asserted |
| SF2 | the window | the 52 weeks Monday 29 September 2025 to Sunday 27 September 2026 | the extract's 57 weeks | counts move, Orrimouth still first | ToR 4.1 |
| SF3 | a week of use | anybody in the home on any day of the week | lived in on most days of it | more homes counted | ToR 4.3 ("on any day of it, for however short a time") |
| SF4 | the most homes | a count of homes | a share of the area's homes | same call (21.8 against 21.3 per cent) | ToR 4.1 ("the most homes"); same call |
| SF5 | at least 26 | 26 or more weeks | more than 26 | same call | ToR 4.1 ("at least") |
| SF6 | the meter day | the UTC day by its date, in the Monday-to-Sunday week of that date | week boundaries an hour or a day off local time | same call (a one-day shift asserted) | same call |
| SF7 | an exchange day | both meters' rows added | one row kept | no count moves | same call; asserted |
| SF8 | estimated days | kept as the head end spread them | left out | no count moves | same call; asserted |
| SF9 | unmatched properties | placed by postcode | dropped | no count moves | same call; asserted |
| SF10 | lets and second homes | homes like any other | business-rated lets left out | counts move, Orrimouth still first | ToR 4.2 ("however it is taxed or rated and however it is let") |
| SF11 | how far a day must rise to be use | any margin from 30 to 75 litres over the week's quietest day | another margin in that corridor, or the home's lowest day as the floor | the same count in every area | same call (C3 corridor, asserted) |
| SF12 | a tie for first place | none | | Orrimouth 203 against 159 | same call |

## Ladder

| Rung | Route | Names | Its figure | Orrimouth | Margin |
|---|---|---|---|---|---|
| 0 | homes the council tax records show unoccupied, exempt or a second home on 27 September 2026 | Kittlesea | 140 | 81, fourth | 1.23 over Ellingsea's 114 |
| 1 | household spaces with no usual residents, census 2021, by the best-fit lookup | Tarnhithe | 121 | 61, fourth | 1.26 over Kittlesea's 96 |
| 2 | homes with 26 or more void weeks (under 300 litres) | Ellingsea | 161 | 85, fifth | 1.34 over Kittlesea's 120 |
| 3 | homes with 26 or more weeks whose days never rose above the home's own steady level | Orrimouth | 203 | | 1.28 over Ellingsea's 159 |

Dominance (`checks.py` C5): the decisive step adds 120 homes more to Orrimouth than to Ellingsea against a carried
advantage of 76 on the void read, 1.58 times it. Pricing of the cheap routes on the clean truth: 25 routes, none
naming Orrimouth (R3a); one route takes the decisive step and lands it (R3b).

## Closure table

| Axis | Reading | Move |
|---|---|---|
| 1 Population | every self-contained dwelling on the gazetteer in the shortlisted areas, whatever any record says of it | filed, ToR 4.2 and 4.4; C1 (parent shells carry no meter) |
| 2 Unit of account | the home (one water property, one UPRN) | filed, ToR 4.1 and 4.2; every home has one meter (asserted) |
| 3 Attribution window | a meter day falls in the week of its date | C1: weeks of seven meter days each, 52 of them per home (verify V2) |
| 4 As-of dating | the meter year as registered; asks on 27 September 2026 | filed in the prompt for the asks; the meter extract is final |
| 5 Version basis | one meter extract; one current list | C1: no revision in the pack |
| 6 Denominator | none for the call (a count); the share is a same-call reading | SF4 |
| 7 Weighting | none: homes counted once each | C1 |
| 8 Window length | 52 weeks | filed, ToR 4.1 |
| 9 Boundary inclusivity | 26 weeks counts ("at least") | filed, ToR 4.1; SF5 same call |
| 10 Rounding path | counts are whole homes | C1: integers throughout |
| 11 Tie-break | not needed | SF12 |
| 12 Maturity and censoring | every week of the window is observed for every home | C1: 52 complete weeks for every property (verify V2) |
| 13 Order of operations | add exchange rows, then cut the window, then read weeks | C1: every order gives the same counts (SF7) |
| 14 Row order | none matters | C1 |
| 15 Duplicate resolution | two rows on an exchange day are two meters, added | SF7, same call |
| 16 Identity normalisation | water property to UPRN through the match, postcode for the unmatched | SF9, same call |
| 17 Netting against gross | none | n/a, asserted inert |
| 18 Dimensional units | litres throughout | units in the column name |
| 19 Code and status semantics | read type ACTUAL or ESTIMATED; status words in the council tax files | SF8 same call; the asks' own definition (CTB return) |
| 20 Integerisation | whole litres, whole homes | C1 |
| 21 Clause scope | ToR 4.3's "any day" covers every day of the week | filed |
| 22 Forward window contents | none: the call's quantity is a closed year | n/a |

## Literal reader

Executed word for word, the terms of reference ask for the homes nobody lived in, stayed at or used on any day of
at least 26 of the 52 weeks; the pack's only record of use is each home's meter, so the literal reader has to read
use from registered litres, and a reader who does it literally on every home finds homes whose litres are the same
to within a few litres on every day of the year, which no household's use is, while homes with people in them vary
by 80 litres or more inside every week. The literal reading is therefore the golden's (a week is used when its days
rise above the home's own quiet level), the easy answer comes from an easy method on the same literal estimand (a
volume line), and every convention the computation needs is closed in the fork table, same call or by a quotable
sentence.

## Oracles

None ships. No control scores a reading of the meters (no labelled occupancy sample, no void list, no leak report);
the only labelled set a solver could validate against, the homes the councils show unoccupied, agrees with the void
read on 93.8 per cent (C6), so it confirms the easy route rather than the golden. The Council Taxbase returns are
district-wide and cannot be rebuilt from the pack, so they neither confirm nor refute ask 1. The housing needs
assessment's table is the declared wrong-basis distractor.

## Ask sheet

**Ask 1. The councils' own count: long-term empty homes on the council tax records on 27 September 2026, as the
Council Taxbase return defines them (8 figures, one per area).** H18 home: a reconciliation beside the call, the
councils' count of empty homes against the meters' (the minister's briefing compares them). Primary device D2 (a
label stored before a silent switch): Teversby's new system restarts every carried account at go-live (5 May
2026) with its furnishing blank, and the archive holds the spell's start; second device D1 (one event across
records): an empty home that changed hands is one dwelling's spell across two accounts, and in Teversby the spring
2026 sales (three in each area, completed between 30 March and 1 May) leave the carried account's own legacy
account starting under six months before the count date, so a reader who follows the new system's Legacy Account
link to that one account and stops is short in every Teversby area. Hazards: unoccupied but furnished is a second
home, not long-term empty; exempt classes are left out; two date formats. Files: the Teversby extract and archive,
the Swanholt extract, the gazetteer, the Council Taxbase returns (5 files, 14 columns on the path). Stops: the new
system read alone (0 in every Teversby area), the link followed one account (Brackwater 27, Wennaby 7, Quellby 13,
Tarnhithe 10), the golden (30, 10, 17, 14; Orrimouth 20, Crackmoor 15, Ellingsea 39, Kittlesea 6). Pin test: the
sentence carries the date and the return's definition; the devices sit in which records are one dwelling's spell,
which neither names. Realism: a revenues migration that carries open accounts with an opening date is how such
systems are loaded.

**Ask 2. Homes on the business rates list as self-catering holiday lets on 27 September 2026 (8 figures, one per
area).** H18 home: a reconciliation beside the call, the homes taxed as businesses that no council tax count sees.
Primary device D6 (a quantity one grain below its line): a holiday site's single list entry covers every cottage on
the site, found only as the gazetteer children of the site's parent shell, which carries the entry's cross-reference
(every area has a site, so every figure moves); second device D2: entries the list deleted with effect from 31 March
2026, when the let missed the letting test, are off the list that day. Files: the rating list extract and the
gazetteer (2 files, 9 columns). Stops: entries counted (Brackwater 8, Wennaby 6, Quellby 1, Tarnhithe 40, Orrimouth
7, Crackmoor 2, Ellingsea 20, Kittlesea 19), deleted entries kept, the golden (13, 10, 6, 51, 9, 7, 23, 27).

**Separation.** Zero ask device rows in the main call's population: the call reads the meter file, the match and
the gazetteer's dwelling rows; the devices sit in council tax rows, rating entries and the gazetteer's parent
shells, and deleting every council tax, rating list and census row leaves the call and every critical component
(asserted). Hazards shared: the gazetteer's area for each UPRN (both asks, no delta).

| Ask | What the cracker does | Figures kept | Verdict |
|---|---|---|---|
| 1 long-term empty homes | merges consecutive unfurnished accounts in each system, follows Legacy Account to the one legacy account it names and takes that account's start | 4 of 8 (the Swanholt areas) | miss |
| 2 self-catering homes | drops deleted entries, joins each entry through the gazetteer cross-reference and counts one home per entry | 0 of 8 | miss |

- **Pair ceiling:** 42.2 (cracker 58.8 on the call with 4 of 16 ask figures; mirror 25.8 off the call with the same
  ask handling).
- **Mirror leakage:** 25.0 per cent of the ask weight.
- **Measured by:** `generator/ceiling.py`, run on `target.zip`.

## Gate answers

- **Stage 3 gates on the hand-off cut.** `checks.py` 64 assertions, 0 failed (the three rules R1 to R3c, the ladder
  C1 to C7, SF1 to SF12, the asks' devices, the realism sweep, the input gates); `verify.py` 20 checks, 0 failed,
  reading only `target.zip` (meter, match, gazetteer, both council tax layouts, the rating list, every PDF through
  pypdf, with a positive control per document); two consecutive builds byte-identical (target.zip, both goldens,
  figures.json, metadata.json); `figures_check.py` 64 of 64; `precut.py` 61 checks, 0 FAIL; `ceiling.py` pair 42.2,
  mirror 25.0 per cent; the producer-metadata audit clean on target/ and golden/; every PDF reads the same under
  pypdf strict and lenient, poppler and pdfminer.
- **Input gates.** 13 files in four formats (parquet, csv, xlsx, pdf); the meter file holds 2,286,365 rows;
  distractors declared in `metadata.json`: the census table, its best-fit lookup and the housing needs assessment
  (the declared wrong-basis distractor, ruled out by terms of reference 4.1 and 4.3).
- **`leak.py --asof 2026-10-19`: REVIEW, no LEAK.** Sweep 4 flags the four PDFs for sharing three to ten terms
  with the stump paragraph: every term it lists is a noun of the world (the area names in the terms of
  reference's shortlist and the assessment's census table, agency, housing, census, counts, October, record,
  gazetteer), none of the move's own words (litres, steady, volume, measurement, signature, reading) appears in
  any document, and `verify.py` V17 asserts no document mentions a leak, a steady, continuous or constant flow or a
  running cistern; harmless. Sweep 11 repeats the prompt gate's two WARNs, answered under `## Draw`.
- **`guard.py heart`: WARN** (people.first, overuse.org_family, repeat.gate_g, answered under `## Draw`; the older
  same-puzzle and same-driver notes differentiated on the card); nearest text 0.05 (task476 v5, task310).
  **`guard.py surface`:** no pair promoted for task286; the personas found in the cut pack are Melissa Robson, Toby
  Hunt and Tracy Hawkins, all drawn.
- **Open for the reader and the judge.** Whether the pack makes the steady-flow reading the literal one for a
  reader who has never seen it (the literal-reader paragraph argues it does: no household's use repeats to within
  a few litres all year, and the margin corridor is 30 to 75 litres); whether ask 1's Teversby stitch (Legacy
  Account, then the dwelling's earlier archive accounts by valuation list reference) is forced by the files as
  shipped; whether the 2021 census table reads as a distractor rather than a rung the prompt invites.

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
- 2026-11-07, at design: a second-homes ask (the councils' second homes on the count date) dropped, because every
  device it could carry (a furnishing flag blank after the migration, a furnished empty home counted as a second
  home) is read straight off the definition or the archive, so the cracker would keep all eight figures.
- 2026-11-07, at design: the water company's field specification and the council's field sheet cut from the pack;
  a file whose job is to describe columns hands over the structure, so each file now carries its conventions in its
  own headers (READ_DATE_UTC, CONSUMPTION_L, status words).
- 2026-11-07, at design: the first census build named Orrimouth (its empties counted in 2021); Orrimouth's homes
  emptied after the processing plant closed in December 2021, and spring 2021 second homes were often lived in, so
  the census now names Tarnhithe.
