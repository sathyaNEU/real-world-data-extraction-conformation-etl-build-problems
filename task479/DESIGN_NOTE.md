# task479 design note

Status lives in `pipeline.json`; this note holds the design. Architecture 1, drawn 2026-10-20 from seed ET36.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task479.json` (architecture v1), registered 2026-10-20 after a pull. Guard
  WARN only, answered here: `overuse.objective` (ETL in 8 of the last 12): the lane is ETL by assignment. People:
  Samantha Walter (the Flood Insurance Program Manager, owner of the guidelines) and Debbie Brady (the Outreach
  Coordinator, author of the close-out), both from `guard.py names --geo us --seed 479`, neither on any other card. Nearest driver on file task130 v4 at 0.11 (a cover paying for events first
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
  carriers ready to quote the owners of elevated insured buildings in five member counties from March 2027. Its
  placement guidelines fix the five as the counties with the lowest expected claim rate: the paid building claims that
  the floods of 2001 to 2025 would bring the county's elevated insured buildings (NFIP building coverage in force on
  30 September 2026, the lowest floor at or above the base flood elevation) as they stand on 30 September 2026, per
  1,000 of their building-years. Forward facing: the pilot's insurers write from March 2027 on the designation the
  Authority files by 1 December 2026.
- **Shape:** `01`, a ranked list under a cap: the fourteen counties' rates (14), the five and the county next in line,
  a bar chart with the five marked, the conformed table of 11,060 elevated insured buildings, and two asks of fourteen
  counties times two figures (56): the criteria come from the structure, none stacked.
- **Strategy:** `other`, named in the card's notes: a counterfactual replay of each past loss on the building as it now
  stands, the as-if of flood loss avoidance. `population_selection` would be the nearest label and is banned in the
  current window (task471, task271), and it misdescribes the move, which changes no building's membership in the book.
  Gate G `etl_conformance`; gap `population` then `time`; pattern none, generators G4 (the risk the record measured is
  no longer the risk the building carries), G13 (the record's years against the pilot's), G19 (the guidelines' table).
  Layer 2 family `estimand_identification` (the right counterfactual), pattern `own:a past flood recurs on an elevated
  building only where its water stood above the new lowest floor`.
- **Data-native sentence:** 2,204 of the 11,060 elevated insured buildings reached that standing through the
  authority's elevations after the floods of 2005, 2008, 2016, 2020 and 2024, to the base flood elevation plus one foot
  on the rivers and two on the coast, and the record keeps the claims they filed on their old floors; on the coast none
  of 1,535 such claims stood above the floor the building has now, but the 2016 river flood stood above the base flood
  elevation by two to three feet across the low reaches of Dunholme and Kettlemoor, so 352 of Dunholme's 443 and 276 of
  Kettlemoor's 338 claims of 2016 on buildings elevated since would come again, and only each claim's water (the floor
  it was rated on plus the depth above it) against the floor the building has now says which.
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

1. Reads the placement guidelines: the elevated insured buildings (a building policy in force on 30 September 2026,
   the lowest floor on it at or above the base flood elevation), the paid building claims the floods of 2001 to 2025
   would bring them as they stand, per 1,000 building-years of their cover from 2001 to 2025; the five lowest counties
   take the pilot and the sixth is next in line.
2. Conforms the policy history (building policies only, a condominium association's policy as one building, the
   union of each building's policies counted once), the claims extract's two layouts (UTC timestamps, legacy and
   current occupancy codes, NGVD 1929 elevations converted with the county offsets) and paid building claims only.
3. Reads "as they stand" against the buildings' own history: a building elevated since a claim now stands above the
   flood level, so the claims it filed on the floor it had before (the policy history's raised floor, the register's
   completed elevations through the crosswalk) are not claims of the building as it stands and are dropped, its later
   claims kept.
4. Divides each county's remaining claims by its buildings' building-years and takes the five lowest.

**Ends on:** Kettlemoor, Dunholme, Wickmere, Amberjack Bay and Thornock, with Lisgrove next in line (Kettlemoor 1.7 and
Dunholme 2.1 per 1,000 building-years, the lowest in the authority, once their 2016 claims on the old floors go).

**Golden:** Wickmere, Amberjack Bay, Thornock, Lisgrove and Saltreach, with Eastmarsh next in line (2.6, 2.6, 2.8, 3.0,
3.0, then 3.7); Dunholme at 23.0 and Kettlemoor at 21.7 stay out, because 352 and 276 of their 2016 claims would come
again on the floors the buildings have now.

## Stump sentence

The default path drops every claim a building filed before it was elevated and puts Dunholme and Kettlemoor in the
pilot, because it never asks whether the 2016 water would still have reached the raised floors; each claim records the
water's depth above the floor the building then had and that floor's elevation, and the 2016 water stood above the new
floors of most buildings elevated after it in both counties.

## Three rules

Task type: data-integration-record-linkage-entity-resolution (General Statistics & Data Science): FEMA's NFIP policy history and its claims extract in two layouts, conformed at the building grain (building policies only, each building's policies unioned, claims joined to the policy and the building, elevations on one datum) into one table of the elevated insured buildings with the claims each would bring as it stands, a task type serving Data Extraction & Conformation (ETL).

Domain test: the deciding quantity is each county's expected paid building claims per 1,000 building-years for the elevated insured buildings as they stand, worked the way flood loss avoidance works a mitigated building's exposure: a raised building is spared exactly the past floods whose water stayed below its new lowest floor, each flood's water fixed by the claim's depth above the floor it was rated on; in a methods field the setting is another field's, so the swap is of the method, and replacing the replayed record with the record as filed, or dropping every claim filed on an old floor, moves the call.

Swap: "which five districts' schools get the insurer's pilot, on the storm-damage claims filed before their roofs were replaced" keeps a history and a change but loses the step: no water surface stands at a level against a floor height, so nothing says which past storms a new roof would have stopped, and the replay the call turns on does not exist.

Layer 1: the claims extract in two layouts (FEMA renamed the fields with its 2023 release and writes dates in UTC), legacy and current occupancy codes, water depths in inches against floor and flood elevations in feet, certificates before 2012 on NGVD 1929 beside NAVD 1988 with the county offsets, a building's several policies (rewrites with a prior policy number, mid-term cancellations, lapses, the Gulfline Mutual book moving to NFIP Direct), unit owners' and contents policies beside building policies, condominium associations insuring a building with its unit count, claims closed without payment beside paid claims; each is how the producing system writes, nothing is placed to be caught, and checks.py asserts each one mishandled keeps the call.

Layer 2: estimand_identification, the right counterfactual: the guidelines count the claims the record's floods would bring each building as it stands, and the choice that flips the call is replaying each claim's water against the building's present floor, keeping a flood where its water stood an inch or more above that floor, instead of keeping the record as filed or dropping every claim filed on an older floor.

Decisive step: for each claim of an elevated insured building filed on a floor lower than the one it has now, the flood's water elevation (the floor it was rated on plus its recorded depth, on one datum) set against the present lowest floor elevation, the claim counted where the water stood an inch or more above it, which keeps 352 of Dunholme's and 276 of Kettlemoor's 2016 claims and none of the coast's 1,535.

Not semantics: every field, unit and definition read correctly (depth in inches above the floor the claim was rated on, elevations in feet on a stated datum, building policies only, an association's building once, paid claims only) still leaves the easy route dropping every claim a raised building filed on its old floor, because no field says an elevation protects only against floods below its new floor; the step is a counterfactual the analyst builds from two fields no file compares, not a reading.

Not rule application: the guidelines fix the population (elevated insured buildings on 30 September 2026), the outcome (paid building claims the floods of 2001 to 2025 would bring them as they stand), the unit (per 1,000 building-years of 2001 to 2025) and the comparison (the five lowest), and no rule or procedure says how a raised building's earlier claims carry to it now; executing every filed rule with those claims dropped files Kettlemoor and Dunholme, and with them kept files Ravensholt and Hensby.

Analyst test: a strong analyst who conforms every file and reads every rule, taking each building as it stands by dropping the claims it filed before its elevation, files Kettlemoor, Dunholme, Wickmere, Amberjack Bay and Thornock (the default path's Ends on, Kettlemoor at 1.7 and Dunholme at 2.1 per 1,000 building-years); one who keeps the record as filed files Wickmere, Lisgrove, Thornock, Ravensholt and Hensby; only the replay of each earlier claim's water against the present floor files the golden five; checks.py runs all three on the clean truth (R3a, R3b).

Estimand: the authority's placement guidelines (filed in the pack): the population (buildings with an NFIP building policy in force on 30 September 2026 whose lowest floor elevation on it is at or above its base flood elevation, an association's building once), the outcome (the paid building claims that the floods of 2001 through 2025 would bring those buildings as they stand on 30 September 2026), the unit (per 1,000 building-years, each day of building cover from 2001 to 2025 counted once, 365.25 days a year) and the comparison (the five counties with the lowest rate, the sixth next in line).

No decoy: nothing is planted: the policies, the claims, the grants register and the crosswalk are the systems' own records, the guidelines state the basis without a method, and no memo, earlier ranking, staff draft or stakeholder figure ranks the counties or treats the elevated buildings one way; the close-out's table counts outreach, not losses.

No certified replay: no certified, published or earlier county figure ships, so nothing is recovered by reproducing a number; the replay is built from each claim's own depth and floor and the building's present floor.

Lesson: a loss history recorded before units were changed says only what the changes leave standing: a raised building is spared the floods that stayed below its new floor and nothing else, so dropping or keeping its history whole both misstate today's book; no build on file replays a past event against a protection a unit acquired later.

## Readability screen

Each rung, the sentence or file a reader would have to read to take it, and whether any shipped text hands it over.

| Rung | What takes the reader there | Verdict |
|---|---|---|
| R0 every paid building claim as filed | the guidelines' paid building claims (2.3) read on the claims extract without "as they stand" | readable |
| Layer 1: two layouts, UTC dates, inches against feet, the datum, building policies only, associations once, rewrites and the transfer | the dictionary's field lines and the guidelines' definitions (2.1 to 2.4) | readable |
| R1 (default path) the claims a raised building filed on its old floor dropped | "as they stand" (3.1) beside the policy history's raised floors and the register's completed elevations | readable |
| R2 the raised buildings on their years since the elevation, or on the rate of the county's buildings never raised | the same, with the building-years cut to the new floor's years or a class rate put on the raised buildings | readable |
| R3 the raised buildings protected up to the base flood elevation | the guidelines' elevated building, defined against the base flood elevation (2.2) | readable |
| R4 (decisive) each earlier claim's water replayed on the floor the building has now | nothing: no sentence says a past flood comes again on a raised building where its water stood above the new floor; the dictionary gives the depth as water above the lowest floor and the claim's floor as the building's rating for the claim, and no file compares a claim's floor with the building's present one | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | insured building | a building policy in force: dwelling, general property or association policy with building coverage | unit owners' and contents policies as insured buildings | same call | guidelines 2.1 |
| SF2 | elevated insured building | lowest floor at or above the base flood elevation on the building policy in force on 30 September 2026 | buildings with no base flood elevation (zone X) included | same call | guidelines 2.2, second sentence |
| SF3 | a building's claims | the claims under its building policies | every claim carrying the building identifier (tenants' contents claims, unit owners' claims) | same call | guidelines 2.3, first sentence |
| SF4 | paid building claim | a building payment made; contents only, Increased Cost of Compliance only and closed without payment are not | claims closed without payment counted | same call | guidelines 2.3 |
| SF5 | building-years | each day of building cover from 1 January 2001 to 31 December 2025 counted once, over 365.25 | policies' days summed | same call (a building's policies never overlap) | guidelines 2.4 |
| SF6 | in force on 30 September 2026 | a policy whose cover includes that day: from its first day to the day before its cancellation or expiration | the extract's ACTIVE status on 2 October 2026 | same call (asserted) | guidelines 2.2 names 30 September 2026; the dictionary's cancellation and expiration lines |
| SF7 | the floods of 2001 through 2025 | losses dated 2001 to 2025 in local time | the 2023 layout's UTC date | same call | the dictionary: the 2023 layout writes UTC timestamps; losses are dated where the building stands |
| SF8 | "as they stand on 30 September 2026" | each building with the floor it has on that day, its record's floods replayed on it | the record as filed (the buildings as they were when they claimed) | Wickmere, Lisgrove, Thornock, Ravensholt and Hensby | guidelines 3.1: as they stand on 30 September 2026 |
| SF9 | the window of a raised building | its building-years from 2001 to 2025 and every flood of those years | only the years since its elevation | Kettlemoor in, Saltreach out | guidelines 2.4 and 3.1: the floods of 2001 through 2025, building-years from 1 January 2001 |
| SF10 | elevations | feet on one datum, NGVD 1929 records converted with the county offset | unconverted | same call | the dictionary's datum line and the offsets file |
| SF11 | water depth | inches above the floor the claim was rated on | read as feet | Wickmere, Lisgrove, Thornock, Ravensholt and Hensby (every claim replays) | the field names (WATER_DEPTH_IN, waterDepthInches) and the dictionary |
| SF12 | a replayed claim is paid | the water an inch or more above the present floor | any water above it | same call (no replayed claim stands within two inches of the floor, asserted) | the record: every building-policy claim with an inch or more of water was paid, every one with less closed without payment |
| SF13 | the five and the next | the five lowest rates, the sixth next in line; compared unrounded or at one decimal | none | same call (no tie straddles the fifth place, asserted) | guidelines 4.1 |
| SF14 | the association's building | one building, its association policy's claims only | its unit owners' policies as buildings | same call | guidelines 2.1 |

## Ladder

Built values from the cut pack (generator/checks.py L1 to L8), per 1,000 building-years at one decimal.

| Rung | Route | The five | Next in line | Dunholme, Kettlemoor |
|---|---|---|---|---|
| R0 | every paid building claim as filed | Wickmere 3.8, Lisgrove 4.2, Thornock 5.0, Ravensholt 6.2, Hensby 10.6 | Amberjack Bay 21.6 | 55.2, 48.8 |
| R1 (default path) | claims filed on a floor lower than the present one dropped | Kettlemoor 1.7, Dunholme 2.1, Wickmere 2.6, Amberjack Bay 2.6, Thornock 2.8 | Lisgrove 3.0 | 2.1, 1.7 |
| R2a | raised buildings on their years since the elevation | Wickmere 2.6, Kettlemoor 2.6, Thornock 2.8, Amberjack Bay 2.9, Lisgrove 3.0 | Dunholme 3.4 | 3.4, 2.6 |
| R2b | raised buildings at the rate of the county's buildings never raised | Amberjack Bay 1.9, Saltreach 2.5, Kettlemoor 2.5, Wickmere 2.6, Thornock 2.8 | Lisgrove 3.0 | 4.1, 2.5 |
| R3 | raised buildings protected up to the base flood elevation | Wickmere 2.6, Thornock 2.8, Lisgrove 3.0, Amberjack Bay 3.1, Hensby 5.2 | Ravensholt 5.4 | 27.8, 25.6 |
| Golden | each earlier claim's water replayed on the present floor | Wickmere 2.6, Amberjack Bay 2.6, Thornock 2.8, Lisgrove 3.0, Saltreach 3.0 | Eastmarsh 3.7 | 23.0, 21.7 |

- Dominance: the golden and R1 differ on the five by Kettlemoor and Dunholme against Lisgrove and Saltreach, and on the
  county next in line; every rung below the golden files a wrong five (asserted).
- Separation: the golden's fifth is 3.0 and its sixth 3.7, so no rate within 0.7 straddles the fifth place; R1's
  Kettlemoor and Dunholme stand 1.3 and 0.9 under its sixth, R2a's Kettlemoor 0.8 under its sixth, R2b's 0.5, and
  R3's Saltreach 0.8 over R3's fifth (generator/checks.py L8).
- On the clean truth (R3a) the world's own replay (each flood's water against the floor of 30 September 2026) files
  the same five and the same next.

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | elevated insured buildings in force on 30 September 2026 in the fourteen member counties | filed (guidelines 2.1, 2.2; SF1, SF2, SF14) |
| 2 | Unit of account | buildings and their paid building claims; rates per 1,000 building-years | filed (2.3, 2.4, 3.1) |
| 3 | Attribution window | the floods of 2001 through 2025, losses dated in local time | filed (3.1; SF7, SF9) |
| 4 | As-of dating | the extract of 2 October 2026; the floor and cover of 30 September 2026 | filed (3.2, 2.2) |
| 5 | Version basis | the records as extracted; nothing is restated | C1 |
| 6 | Denominator | the county's elevated insured buildings' building-years | filed (2.4, 3.1) |
| 7 | Weighting | none: claims counted, building-years summed | filed |
| 8 | Window length | twenty-five years | filed |
| 9 | Boundary inclusivity | 1 January 2001 to 31 December 2025 inclusive; at or above the base flood elevation | filed (2.2, 2.4) |
| 10 | Rounding path | rates and building-years unrounded until printed to one decimal | prompt; the five do not move at either (SF13) |
| 11 | Tie-break | none arises at the fifth or sixth place (asserted) | C1 |
| 12 | Maturity and censoring | the window closed nine months before the extract; every claim of 2001 to 2025 is closed | C1, asserted |
| 13 | Order of operations | conform the policies, take the population, join the claims, replay, count | the counts commute (each claim on one building) |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | one row per policy and per claim; a building's policies unioned | filed (2.4); asserted |
| 16 | Identity normalisation | FEMA building identifiers as written in the policy and claims extracts | dictionary |
| 17 | Netting against gross | none: claims counted, not paid amounts | C1 |
| 18 | Dimensional units | depth in inches, elevations in feet | field names and dictionary (SF10, SF11) |
| 19 | Code and status semantics | occupancy codes, condominium indicator, claim status, cancellation reasons | dictionary; never the stump |
| 20 | Integerisation | claims are counts | C1 |
| 21 | Clause scope | "as they stand" applies to every building in the population, raised or not | filed (3.1) |
| 22 | Forward window contents | the 2027 pilot rated on the floods of 2001 to 2025, the buildings as they stand on 30 September 2026 | filed |

## Literal reader

The guidelines executed word for word fix the population, the outcome, the window, the unit and the comparison, and
they ask for the claims the record's floods would bring each building as it stands: for a building never raised that
is its paid claims, and for a raised building the literal question is whether each flood would still enter it. The
records answer it: each claim carries the water's depth above the floor it was rated on and that floor's elevation, the
policy carries the building's floor now, and every claim with an inch or more of water above its floor was paid. A
literal reader who drops the raised buildings' earlier claims has answered a different question (what they filed after
the elevation), which 3.1's window, every flood of 2001 to 2025, rules out; every other reading converges or violates
a quoted sentence (fork table). Re-run on the finished pack at stage 3.

## Oracles

- The record's own payment rule: every claim under a building policy with an inch or more of water above the floor it
  was rated on carries a building payment (44,655 of 44,655) and every one with less closed without payment (2,444),
  which fixes the replay's threshold without a sentence saying so (O1).
- Gorran's buildings elevated after the 2008 flood filed 37 claims in 2016 on their raised floors, wherever the 2016
  water stood above them: the record's own evidence that a raised floor floods when the water stands above it, which
  the default path's premise contradicts (O2). It carries no county rate.
- The close-out's building policies in force on 31 December 2025 by county tie to the policy history under every
  handling of the population's conventions (it counts building policies of all buildings), confirming the conformance
  of the policies and arbitrating nothing about the replay (O3).
- No control ties only under the golden on the asks: the register's federal share obligated per project ties under
  both readings of the property shares, and nothing states a county's 2026 losses (B9, A12).

## Ask sheet

- **Ask A, the claims on losses in 2026 that carry a building payment and the building payments made on them as of the
  extract, by county (fourteen counties, two figures each, whole claims and whole dollars).** H18 home: the season the
  pilot's counties have just had, which the guidelines (5.1) put beside the designation. Path: the 2023-layout claims
  extract (claim, policy, building, county, date of loss in UTC, report date, status, payments), the policy history
  (each policy's dates, company, prior policy number, condominium indicator), the member counties, the guidelines.
  Primary device: D1, a replay under fresh ids beside genuine same-day pairs. Gulfline Mutual left the NFIP on 1 July
  2026 and its book moved to NFIP Direct under new policy numbers; the June flood's claims Gulfline had opened and
  advanced on but not closed were closed on its records at the advance and re-entered by NFIP Direct under new claim
  numbers and the new policies, each carrying the claim's payments to date (the advance included), so one loss is two
  records on two policies, the second policy not in force on the date of loss. Beside them stand the genuine pairs: a
  condominium association's claim and its ground-floor unit owners' claims on the same building and day, all to be
  counted, and NFIP Direct's own late reports of June losses on the new policies, with no Gulfline record. Every
  record is valid as written; only the policy chain (the new policy's prior number, the same building and day, the same
  damage) shows which records are one claim. Every county carries re-entries, pairs and late reports (A3 to A5).
  Hazards: claims closed without payment and contents-only claims (no building payment); Increased Cost of Compliance
  payments (not building payments); the UTC date of loss (a local evening loss on 31 December is dated 1 January).
- **Ask B, the buildings in the authority's elevation and acquisition projects not completed on 30 September 2026 and
  the federal share obligated to them, by county (fourteen counties, two figures each, whole buildings and whole
  dollars).** H18 home: the buildings about to join the pilot's population and the money the authority still has in
  them, the guidelines' second figure (5.1). Path: the grants export's Projects (cost share, applicant), Properties
  (measure, community, approved cost, federal share, status) and Inspections (the final inspection of the completed
  measure) sheets, the member counties' communities, the guidelines.
  Primary device: D2, a label stored before a silent switch. The authority's grants system took over the projects
  approved before 12 January 2026 from its earlier tracker, which kept them at their status of that day: 93 of their
  properties completed since show Under construction or Approved, and only a passed final inspection in the Inspections
  sheet, after the status date, shows the measure done (every county, B3). With it, D6, an allocation at the wrong
  weight: the earlier tracker held the federal share on the project and spread it evenly over the properties, so
  those projects' property shares are equal while their approved costs differ; the projects' totals tie either way
  and only the share against the approved cost and the project's federal cost-share percentage shows it (B5).
  Hazards: withdrawn properties (no share, not pending); a joint project's applicant county against the property's
  community; acquisitions and elevations both counted.
- **The construction layer:** the call, the fourteen rates, the chart and the conformed table; the cracker has them.
- **Main population zero-counts (asserted):** the call reads no 2026 loss, no register, crosswalk or inspection row:
  with the 2026 claims, the register and the crosswalk removed the fourteen rates are unchanged (S1), and the asks read
  no claim of 2001 to 2025 and no rate (S2).
- **Hazard table (asserted):** A6 to A9 and B6 to B8 in checks.py; none moves the call.
- **Referee:** none; no file states a county's 2026 losses or pipeline.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| A, claims on 2026 losses with a building payment, and the payments | the battery's path: claim numbers unique, no repeated row; a building and date of loss carried by more than one claim resolved to the latest record; keeps 0 of 28 | miss |
| B, buildings in projects not completed, and the federal share | the register read as it stands: properties pending while their status says so, at the federal share the register gives; keeps 0 of 28 | miss |

- Mirror leakage: 0.0 per cent of ask weight on the cut pack (generator/ceiling.py: the mirror builds both asks the
  cracker's way and keeps none of 56).
- Pair ceiling: 35.0 on the cut pack (weights 38 / 7 / 55: the cracker keeps the main block and instructions, 45.0;
  the mirror at the default path keeps nine of the fourteen rates and instructions, 25.0). Deeper paths are priced in
  the script's route table: merging the transfer's records by the policy chain keeps ask A's fourteen claim counts
  (and its payments only at the record carrying the claim's payments to date); reading completion from the final
  inspections keeps ask B's fourteen building counts (and its shares only at the approved cost times the cost-share
  percentage). Re-measured by the stage 4 reader.
- Measured by: generator/ceiling.py on the cut pack.

## Pre-ship check

- **The 10/10 rules re-read against the built pack.** Domain: the deciding quantity is each member county's expected
  paid building claims per 1,000 building-years for its elevated insured buildings as they stand, and the step is flood
  loss avoidance's own: a raised building is spared exactly the past floods whose water stayed below its new floor, the
  water fixed by each claim's floor and depth; a noun swap leaves no water surface against a floor height. Layers: the
  mess (two claims layouts with UTC dates, occupancy codes across the 2021 change, inches against feet, NGVD 1929
  certificates, rewrites and the Gulfline transfer, unit owners' and contents policies, claims closed without payment)
  is the producing systems' own and keeps the call when mishandled (R2a to R2i). Three rules: no decoy, memo, ranking
  or county rate ships (R1, R3c); no field reading decides (every field read correctly, the claims filed on old floors
  dropped still put Kettlemoor and Dunholme in, R3a); no filed rule says how a raised building's earlier claims carry
  to it now.
- **Readers:** READERS_LINE
- **Judge:** JUDGE_LINE
- **Free gates (2026-10-21):** checks.py 0 failed (input gates G1 to G7, dates D1 to D3, pins P1 to P4, SF1 to SF14,
  L1 to L8, O1 to O3, R1 to R3c, S1 to S3, A1 to A12, B1 to B10, E1 to E5, F1 to F6), verify.py 10 of 10
  independently (pandas, its own code path), two builds byte-identical, target.zip cut from the final build (13 files,
  sha256 233e7da88d23d2c3), figures_check.py 97 of 97, precut.py 51 checks clean, voice-check PASS, guard.py heart
  WARN on objective overuse only (nearest driver task130 v4 at 0.11), surface no hard tell after the export manifest's
  columns were renamed (the promoted pairs carry card-level likeness only), containers clean, generator/ceiling.py pair
  ceiling 35.0 with mirror leakage 0.0.
- **leak.py REVIEW lines, each harmless:** 2.1 is the guidelines' section number; the guidelines and the close-out
  carry the call's words because they name the pilot and list the fourteen counties, ranking none; the dictionary, the
  guidelines and the close-out use policy, record, lowest and floods in their own sense and none names the replay, the
  transfer's re-entries or the tracker's statuses; the dates after the extract are the active policies' term
  expirations and the projects' periods of performance, forward by nature.

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
- Every insured building as the population (2026-10-20, stage 2): the buildings below the base flood level carry the
  counties' whole flood history, so the lowest rates fell to the upland counties with or without the replay, and the
  replay moved no county across the fifth place; the population narrowed to the elevated insured buildings the pilot's
  insurers will quote, where the raised buildings are a third of some counties' book.
- The re-entered transfer claims carrying only NFIP Direct's own payments (2026-10-20, stage 2): summing every
  record's payment then lands each county's payments, so the payment half of ask A carried no device; the re-entry
  carries the claim's payments to date, as NFIP Direct's record of a transferred claim does.
- The Saltreach surge of 2005 a foot under the base flood level and Kettlemoor's 2016 middle reach 0.6 feet under it
  (2026-10-20, stage 2): the protection-to-the-base-flood-level rung (R3) and the class-rate rung (R2b) each filed the
  golden five; with the 2005 surge 0.6 feet under the level in Saltreach (still two feet and more under the raised
  floors) and Kettlemoor's middle reach a foot under it, both rungs file a wrong five.
- A persona pair whose first name the names script does not return (2026-10-20, stage 2): replaced with Samantha
  Walter from `guard.py names --geo us --seed 479`.
- Contents-only and unit owners' records joined to the building rate (2026-10-20, stage 2): neither moves the call,
  so they stay Layer 1 under 2.1 and 2.3 rather than a device.
