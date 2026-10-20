# task479 design note

Status lives in `pipeline.json`; this note holds the design. Architecture 1, drawn 2026-10-20 from seed ET36.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task479.json` (architecture v1), registered 2026-10-20 after a pull. Guard
  WARN only, answered here: `people.first` (Christina, one older build) and `people.last` (Drake, one older build), both
  drawn by `guard.py names --geo us --seed 479` and neither in the last twelve; `overuse.objective` (ETL in 8 of the
  last 12): the lane is ETL by assignment. Nearest driver on file task130 v4 at 0.11 (a cover paying for events first
  reported inside its window), which shares no structure with this one. `test.same_puzzle_older` against task464 v1
  and `test.same_driver_older` against task450 v2 are answered by the card's differentiation lines.
- **Redrawn at the draw, and why the replacements are the honester labels.** The first card BLOCKed on four axes. The
  context artifact moved from `filed_standard` (task271's) to `close_out_summary`: the program manager works from the
  authority's 2025 outreach close-out, which the asks build on, while the placement guidelines are the pack's governing
  document rather than the stakeholder's working file. The forcing event moved from `launch_or_rollout` (task271's) to
  `statutory_or_regulatory_filing`: what forces the call now is the pilot plan the authority files with the State
  Department of Insurance by 1 December 2026, on which the department approves the participating carriers' rates for
  the five counties; the March 2027 launch follows from it. The gap moved from `time` first to `population` first and
  the decisive generator from G13 to G4: the claims history is a correct record of buildings that are no longer the
  buildings the pilot insures (G4, who holds the risk now), which the time framing also describes but less exactly.
  Gate G moved from `method_or_model_selection` (9 of the last 12) to `etl_conformance`: the decisive step produces the
  conformed table's own field, each insured building's claims as it now stands, judged against the guidelines' contract.
- **Seed:** ET36 (a state regulator's catastrophe unit compares NFIP experience across states and flood zones to
  target outreach for private-market flood products; written against earned premium, policy counts against insured
  units). Kept: the world (NFIP policy terms and claims as FEMA shares them with floodplain managers), the decision
  (where outreach for private-market flood products goes, on each area's flood loss experience) and the quantity (paid
  claims per insured building). The seed's mechanisms (earning by policy effective year, condominium master policies'
  unit counts) are not the stump: the guidelines file the basis and the unit, and each is Layer 1 the analyst executes.
- **Pairing:** General Statistics & Data Science, task type `data-integration-record-linkage-entity-resolution`, which
  serves ETL. The work is data integration: the NFIP claims extract (two layouts), the policy terms extract and the
  authority's grants-system export of mitigation projects (keyed to its own property numbers, joined to FEMA's
  property identifiers through a crosswalk) conformed at the building grain into one table of the buildings insured on
  30 September 2026 with the claims each would file in a repeat of the record's floods. In a methods field the setting is
  another field's, so the swap is of the method: replacing the integrated as-it-stands record with the record as filed,
  or with a blanket treatment of the mitigated buildings, moves the call. Objective: Data Extraction & Conformation.
- **The decision and the quantity:** the Tarrow Sound Regional Flood Authority, a special district of fourteen Gulf
  Coast counties that runs their floodplain management and flood insurance outreach, has two admitted private flood
  carriers ready to quote NFIP policyholders in five member counties from March 2027. Its placement guidelines fix the
  five as the counties with the lowest expected paid building claims per 1,000 insured buildings a year, for the
  buildings with NFIP building coverage on 30 September 2026, from the paid building claims those buildings filed while
  insured in the flood years 2001 to 2025, each building taken as it stands on 30 September 2026. Forward facing: the
  pilot's carriers write from March 2027 and the plan is filed by 1 December 2026.
- **Shape:** `01`, a ranked list under a cap: fourteen counties times two figures (the expected claims per 1,000 and
  whether the county is in the pilot: 28), the five, the runner-up and the gap (3), a chart with its parts (4), the files
  (2) and the asks (to be designed at stage 2): the criteria come from the structure, none stacked.
- **Strategy:** `other`, named in the card's notes: a counterfactual replay of each past loss on the building as it now
  stands, the as-if of flood loss avoidance. `population_selection` would be the nearest label and is banned in the
  current window (task471, task271), and it misdescribes the move, which changes no building's membership in the book.
  Gate G `etl_conformance`; gap `population` then `time`; pattern none, generators G4 (the risk the record measured is
  no longer the risk the building carries), G13 (the record's years against the pilot's), G19 (the guidelines' table).
  Layer 2 family `estimand_identification` (the right counterfactual), pattern `own:a past flood recurs on an elevated
  building only where its water stood above the new lowest floor`.
- **Data-native sentence:** the authority elevated about two thousand buildings after the floods of 2005, 2008 and
  2016 to the regulatory flood level plus one or two feet, and the record keeps every claim those buildings filed
  before; on the coast the 2005 and 2020 surges stood below the new floors almost everywhere, but the 2016 river flood
  was a far rarer event than the regulatory flood in Dunholme and Kettlemoor and its water stood two to five feet above
  that level across much of both floodplains, so a repeat would still enter many buildings elevated after it, and only
  each claim's water level against the floor the building now has says which.
- **Sources, one line each:** seed ET36 (the world, the decision and the quantity, never its mechanisms); the client's
  data-integration rigor patterns (propagate linkage error, weight agreement by informativeness, resolve pairwise links
  into entities), none of which is the decisive step here, the linkage being by recorded identifiers and a crosswalk;
  strategies F7 (replacements that restart a curve, task132) and F1 (a clock the closed window never exercised) as the
  nearest families, neither of which replays an event against a changed protection; FEMA's loss avoidance studies as
  the field's practice for a mitigated building's exposure (an event's water against the building's new elevation),
  stated in no shipped document.
- **Same-puzzle test:** gap population, decisive generator G4, decision ranked_slate_under_cap against the last twelve
  builds, lineage included: no match; task464 v1 matches as an older build and is differentiated on the card (a fitted
  response with undated changes, against dated projects and no fit). Same-driver test (population, G4, etl_conformance):
  task450 v2 older, differentiated on the card.
- **Abstraction test:** the nearest drivers stripped of nouns (task130 v4, a cover priced on events reported inside its
  own window; task85, a unit's own observation window from an intermediary's lead time; task184, the event-hour an event
  could have happened in) carry no history replayed against a protection a unit acquired later. task472 (same lane, same
  day) replays a shortened job to the next window an outside schedule permits; here nothing is shortened and no window
  quantises anything: each past event's own level meets the unit's present protection.

## Default path

A strong analyst with every field read correctly:

1. Reads the placement guidelines: the buildings with NFIP building coverage in force on 30 September 2026, their paid
   building claims in the flood years 2001 to 2025 while insured, per 1,000 insured building-years, each building as it
   stands on 30 September 2026; the five lowest counties take the pilot.
2. Conforms the claims extract's two layouts, the policy terms (renewals, cancellations, reinstatements, condominium
   master policies as one building) and the crosswalk from the authority's property numbers to FEMA's.
3. Reads "as it stands" against the authority's mitigation register: buildings bought out are not in the book, and a
   building elevated or floodproofed since a claim is now protected, so its claims filed before the project are dropped
   and its claims after the project kept.
4. Divides each county's remaining claims by its buildings' insured years and ranks the fourteen counties.

**Ends on:** a pilot of Saltreach, Larkspur Bay, Dunholme, Kettlemoor and a fifth county (figures measured on the cut
pack at stage 2), Dunholme and Kettlemoor entering because their 2016 claims, filed before the 2017 to 2021 elevations,
are dropped.

**Golden:** Dunholme and Kettlemoor stay out: their 2016 claims count again wherever the 2016 water stood above the floor
the building has now, and the pilot is Saltreach, Larkspur Bay and three counties the default path ranks sixth and
below (figures measured on the cut pack at stage 2).

## Stump sentence

The default path drops every claim a building filed before it was elevated and puts Dunholme and Kettlemoor in the
pilot, because it never asks whether the 2016 water would still have reached the raised floors; the claims record each
building's water depth above the floor it had and the building's floor elevations, which put the 2016 water above the
new floors of many buildings in both counties.

## Three rules

Task type: data-integration-record-linkage-entity-resolution (General Statistics & Data Science): the NFIP claims extract in two layouts, the policy terms extract and the authority's grants-system export of mitigation projects, keyed to its own property numbers and joined to FEMA's property identifiers through a crosswalk, integrated at the building grain into one conformed table of insured buildings with the claims each would file as it now stands, a task type serving Data Extraction & Conformation (ETL).

Domain test: the deciding quantity is each county's expected paid building claims per 1,000 insured buildings a year for the buildings insured today as they now stand, worked the way flood loss avoidance works a mitigated building's exposure: a raised building is spared exactly the past floods whose water stayed below its new lowest floor, each flood's water level fixed by the claim's recorded depth above the floor of the day; in a methods field the setting is another field's, so the swap is of the method, and replacing the integrated record with the record as filed, or dropping every pre-project claim of a mitigated building, moves the call.

Swap: "which five hospitals' wards get the private insurer's pilot, on the readmissions their patients filed before the wards were renovated" keeps a history and a change but loses the step: no water surface stands at a level against a floor height, so nothing says which past events a renovation would have stopped, and the replay the call turns on does not exist.

Layer 1: the claims extract in two layouts (FEMA renamed fields with its 2023 data release), timestamps in UTC, water depths in inches against floor and flood elevations in feet, older elevation certificates on NGVD 1929 beside NAVD 1988 with the county offsets, policy terms with renewals, mid-term cancellations, reinstatements and condominium master policies carrying unit counts, contents-only policies beside building policies, claims closed without payment beside paid claims, and the grants system's own property numbers with multi-property and withdrawn projects; each is how the producing system writes, nothing is placed to be caught, and checks.py will assert each mishandled one keeps the call.

Layer 2: estimand_identification, the right counterfactual: the guidelines rate each building as it stands, and the choice that flips the call is replaying each past claim against the building's present floor, keeping a flood where its water stood above the raised floor, instead of keeping the record as filed or dropping every claim filed before a project.

Decisive step: for each claim a building insured today filed before it was elevated or floodproofed, the flood's water level (the claim's lowest floor elevation plus its recorded depth) set against the building's present lowest floor elevation, the claim counted again where the water stood above it, which keeps much of Dunholme's and Kettlemoor's 2016 claims and almost none of the coast's 2005 claims.

Not semantics: every field, unit and definition read correctly (depth in inches above the lowest floor of the day, floor and flood elevations in feet on a stated datum, building coverage only, a condominium master policy as one building, paid claims only) still leaves the easy route dropping every pre-project claim of an elevated building, because no field says a project protects only against floods below its new floor; the step is a counterfactual the analyst builds, not a reading.

Not rule application: the guidelines fix the population (buildings with NFIP building coverage on 30 September 2026), the outcome (paid building claims), the window (flood years 2001 to 2025, while insured), the unit (per 1,000 insured building-years) and the comparison (the five lowest counties), and no rule or procedure says how a mitigated building's earlier claims carry to it now; executing every filed rule with those claims dropped, or kept, files the wrong five.

Analyst test: a strong analyst who conforms every file and reads every rule, taking each building as it stands by dropping the claims filed before its elevation, puts Dunholme and Kettlemoor in the pilot (the default path's Ends on); one who keeps the record as filed leaves out Saltreach and Larkspur Bay; only the replay of each pre-project claim against the present floor files the golden five; checks.py will run all three on the clean truth.

Estimand: the authority's private flood placement guidelines (filed in the pack): the population (buildings with NFIP building coverage in force on 30 September 2026 in a member county, a condominium master policy's building as one building), the outcome (the paid building claims those buildings filed while insured, each building taken as it stands on 30 September 2026), the window (flood years 2001 to 2025, the years each building was insured), the unit (claims per 1,000 insured building-years) and the comparison (the five counties with the lowest figure).

No decoy: nothing is planted: the claims, the policy terms, the register and the crosswalk are the systems' own records, the guidelines state the basis without a method, and no memo, earlier ranking, staff draft, briefing or stakeholder figure ranks the counties or treats the mitigated buildings one way.

No certified replay: no certified or published county figure ships, so nothing is recovered by reproducing a number; the replay comes from each claim's own depth and the building's floor elevations.

Lesson: a loss history recorded before units were changed says only what the changes leave standing: a raised building is spared the floods that stayed below its new floor and nothing else, so dropping or keeping its history whole both misstate today's book; no build on file replays a past event against a protection a unit acquired later.

## Tried and rejected

- The seed's own mechanisms as the decisive step (2026-10-20, screened at the draw): earning premium by term rather
  than by policy effective year is a stated accounting rule (rule application), and a condominium master policy's unit
  count read as units is a field reading (data semantics); both stay in the pack as Layer 1 under filed sentences.
- A catastrophe-adjusted expected loss ratio by county (2026-10-20, screened): the estimator family for an expected
  catastrophe loss from a short record is open (window mean, frequency from a long declarations record times the
  window's severity, a fitted severity tail), so the graded figure forks, and filing the method makes it rule
  application.
- Event-clustered confidence bounds on each county's loss ratio (2026-10-20, screened): a variance-only correction that
  widens every interval, so the conservative reflex lands the hold; and the annual series shows the spread directly.
- The Risk Rating 2.0 glide path's full-risk premium for policies still capped (2026-10-20, screened): every policy
  transitioned within one year, so the full-risk premium is censored at the same multiple for all of them and the
  distribution beyond it is not identified; the cap itself is a statutory rule.
- The latest event's claims completed by days since landfall, and open claims from their adjusters' damage estimates
  (2026-10-20, screened): the first is task181's route-specific delay and task451's arrival history, the second is a
  policy-terms computation (rule application).
- Claims linked to policies by quasi-identifiers to rate premium bands (2026-10-20, screened): linkage error correction
  is spent (task449, task468) and a fusion through shared attributes is task465's.
- Policy tenure from originalNBDate with left truncation (2026-10-20, screened): task133's delayed entry.
- Rating each insured building at the claim rate of buildings in its present condition (2026-10-20, screened): the
  policy terms carry an elevated-building indicator for every term, so the rate by present state is one group-by on a
  visible column, the opponent's stratification reflex; kept as a wrong rung (it gives a raised building the later rate
  of elevated buildings in general, which on the river is the low rate of buildings never in a 2016-sized flood).
- Bridge deck deterioration from inspection pairs of different lengths (2026-10-20, screened in another world): per-year
  normalisation, the obvious correction, lands within rounding of the interval-aware estimate on fair decks, so the
  lever is too small.
