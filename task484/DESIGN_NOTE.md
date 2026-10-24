# task484 design note: a state population unit's 2027 revenue-sharing tiers (architecture 1)

Drawn 2026-10-20 from seed ET41's number, re-worlded at the draw (see Tried and rejected).

## Draw

- **Pairing.** Client domain survey-research-official-statistics (house domain demographic-social-science, housing),
  task type census-register-administrative-data-quality, objective Data Extraction & Conformation (ETL): the 2020
  census base, the cities' certificate-of-occupancy exports from their own permit systems, demolition records, the
  ACS occupancy rates, the group quarters survey and an electric utility's residential account history are conformed
  into one housing-unit-method population estimate per city.
- **Decision.** How many, and which, of the state's cities near the line stand at 50,000 residents or more on
  1 April 2026, and so move into the upper tier of the 2027 municipal revenue-sharing formula. Forward facing: the
  tiers fund 2027.
- **The quantity.** Each city's household population (occupied housing units times persons per household) plus
  its group quarters residents on 1 April 2026.
- **Data-native sentence.** Apartment buildings completed in the last two years fill over a year or more after they
  open, so the city's stock occupancy rate, applied to every housing unit, counts as households the units still
  standing empty, most in the cities that built most; the utility's account history, which covers only the cities in
  its territory, records month by month how earlier buildings filled after opening.
- **Default path.** The housing unit method with each city's ACS occupancy on every unit.
- **Golden.** The same for the stock; the units completed since the start of 2024 at the occupancy the lease-up
  record gives for their months since completion.
- **Shape.** 01, a list: the upper-tier cities and their count, twelve cities by two housing figures, and the
  memo's chart.
- **Guard.** WARN (objective and Gate G overuse); nearest task43 at 0.06; personas Kimberly Rogers and Martin Booth
  from guard.py names; off the seasonal-adjustment subdomain and composition_mix (lane reservations).

## Default path

1. Read the rules: the twelve cities; population on 1 April 2026 by the housing unit method, occupied housing units
   times the 2020 average household size plus the 2026 group quarters residents; housing units are the 2020 units
   plus certificate-of-occupancy completions to 31 March 2026 less demolitions; the upper tier at 50,000 or more.
2. Conform the three permit systems' exports to one table of completions by city, subtract the demolitions, add the
   group quarters survey.
3. Turn housing units into occupied units at each city's ACS 2020-2024 occupancy rate (the housing unit method's
   standard occupancy input), multiply by household size, add group quarters, compare with 50,000.

Ends on: Ashford, Carver Springs, Eastlake, Fairhaven, Harlow, Juniper Falls and Linden in the upper tier

Golden: Fairhaven and Linden in the upper tier

## Stump sentence

The default path applies each city's ACS occupancy rate to every housing unit and puts Ashford, Carver Springs,
Eastlake, Fairhaven, Harlow, Juniper Falls and Linden in the upper tier; the apartment buildings opened since 2024
fill over a year or more after their certificates of occupancy, which the utility's account history shows month by
month for the buildings in its five cities (about half full at six months, three quarters at a year), and only
counting each new building at the share a building of its age had reached puts Fairhaven and Linden alone over the
line.

## Three rules

Task type: Survey Research & Official Statistics, census-register-administrative-data-quality, which the taxonomy tags for ETL: conforming the census base, three permit systems' certificate-of-occupancy exports, demolitions, ACS occupancy, the group quarters survey and a utility's account history into housing-unit-method population estimates per city.

Domain test: the quantity that decides the call is each city's household population on 1 April 2026, worked as official population estimates work it by the housing unit method (units times occupancy times persons per household); the field's step here is recognising that newly completed units are not occupied at the stock's rate and estimating their occupancy by age from an administrative record of how buildings fill.

Swap: "which clinics' patient panels exceed the line, counting each new clinic's capacity at the network's average utilisation" keeps the words and loses the step: nothing in the clinic case is a housing stock whose new units sit empty while they lease up, with a utility record of accounts opening unit by unit after each building's certificate of occupancy.

Layer 1: three permit systems with their own layouts, date formats and building type codes (one of them changing codes in 2025); demolition permits; ACS five-year estimates beside the 2020 census; a utility that serves only five of the twelve cities and names them in capitals; each the agency's own export, each asserted neutral on the call (checks.py R2).

Layer 2: estimation_fit. The methodological choice is the occupancy of the units built since the census: the city's ACS rate, the 2020 census rate, or each new building's occupancy at its age from the record of how buildings fill.

Decisive step: estimating the occupancy of each apartment building opened since the census by its months since its certificate of occupancy, from the lease-up the utility's account history records for the buildings it serves, and carrying that to every city, instead of applying the city's stock occupancy rate to new units.

Not semantics: every field read correctly (certificate dates, building type codes, meters and active accounts, ACS occupied and total units) still leaves the stock-rate route on the wrong cities; no field or sentence says new buildings fill slowly, the account history shows it.

Not rule application: rule 2.2 files the population, its components and the estimate date, but not the occupancy of the city's units on 1 April 2026; no rule or note says how that occupancy is estimated, and executing every stated rule with the ACS rate files seven cities.

Analyst test: a strong analyst who reads every field and rule correctly and runs the housing unit method with each city's ACS occupancy rate puts Ashford, Carver Springs, Eastlake, Fairhaven, Harlow, Juniper Falls and Linden in the upper tier designated (the default path's Ends on); only counting new buildings at their lease-up occupancy puts Fairhaven and Linden.

Estimand: rules 2.1 to 2.3 (revenue_sharing_tier_rules_2027.pdf) file the population (the twelve cities), the outcome (persons in occupied housing units plus group quarters residents), the date (1 April 2026), the unit (residents, by the housing unit method with the 2020 household size and the 2026 group quarters survey) and the comparison (50,000 or more).

No decoy: nothing is planted to be caught; every permit, account and survey record is what the generator built, no earlier estimate, memo or list ships, and no document mentions lease-up or vacancy in new buildings.

No certified replay: no certified or published figure is reproduced to recover the method; the fill by age comes from the utility's own monthly accounts.

Lesson: a housing-unit estimate's occupancy input is the stock's, and units completed in the last two years are not at it: they fill over many months after opening, so the stock rate counts households not yet there, most where the city built most; a record of how buildings filled by age carries the right occupancy to every city. No build on file estimates a stock's occupied share by the age of its additions.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0, the 2020 census occupancy on every unit (seven cities) | rule 2.2 "occupied housing units": fires | census occupied units: fires | none | none | none | a ratio | readable |
| R1, the ACS occupancy on every unit, the default path (seven cities) | none | ACS occupied and total: fires | the housing unit method's occupancy input: fires | none | none | a ratio | readable |
| R2, the covered cities' own accounts, the rest at the ACS rate (five cities) | none | active accounts: fires | none | none | none | a substitution | readable |
| G (decisive), every new building at its age's occupancy from the fill record (two cities) | no clause names new units' occupancy | no column holds a fill share | no method fills new units by age | none | none | none | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | population | household population plus group quarters | household population only | not the rule's quantity | rule 2.2 |
| SF2 | housing units | 2020 units plus completions to 31 March 2026 less demolitions | permits issued | not the rule's units | rule 2.2 |
| SF3 | average household size | the 2020 census figure | an ACS figure | not the rule's figure | rule 2.2 |
| SF4 | 50,000 or more | at or above | above | same call (no family value within 400, asserted) | rule 2.3 |
| SF5 | a building's age | months from its certificate-of-occupancy month to April 2026 | days to 1 April | same call (asserted by the family) | the monthly bills |
| SF6 | the ACS occupancy | occupied over total housing units | one less vacant over total | same call (identical) | the ACS table |
| SF7 | group quarters | the 2026 survey's residents | the 2020 census group quarters | not the rule's count | rule 2.2 |
| SF8 | the files the call reads | census, permits, demolitions, ACS, group quarters, utility | school enrollment, voter registration | same call (asserted) | rule 2.2 |

## Ladder

Built figures, read from the cut pack by `generator/checks.py` (residents on 1 April 2026, against 50,000).

- **R0, the 2020 census occupancy on every unit (seven cities).** As R1.
- **R1, the ACS occupancy on every unit, the default path (seven).** Ashford 51,515, Carver Springs 51,004, Eastlake
  50,543, Harlow 50,612, Juniper Falls 51,498 over the line. Dies to the utility's account history: buildings in it
  are about half occupied six months after opening and three quarters at a year.
- **R2, the covered cities' own accounts with the rest at the ACS rate (five).** Ashford and Harlow fall below; the
  uncovered boom cities stay over.
- **G (Fairhaven 52,309, Linden 51,629; Ashford 49,270, Dunmore 49,180 the nearest below).** The truth (every
  building's fill known, generator only) puts the same two over, every city within 400 of it.
- **Margins:** every family member (accounts over meters pooled, the mean of buildings' shares, a fitted exponential
  fill, the covered cities at their March 2026 accounts, the curve only for buildings opened since 2023) at least 400
  residents from the line in every city; every city R1 flips 500 or more over it.
- **Worth:** R1 lists both golden cities and five others; the asks carry the pair (Ask sheet).

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | the twelve cities (rule 2.1) |
| 2 | Unit of account | the city; residents |
| 3 | Attribution window | completions 1 April 2020 to 31 March 2026 (SF2) |
| 4 | As-of dating | 1 April 2026; exports compiled by 14 October 2026 |
| 5 | Version basis | ACS 2020-2024 five-year; 2020 census base |
| 6 | Denominator | none |
| 7 | Weighting | none |
| 8 | Window length | six years of completions |
| 9 | Boundary inclusivity | 50,000 or more (SF4) |
| 10 | Rounding path | residents unrounded before the comparison; housing in whole units |
| 11 | Tie-break | none |
| 12 | Maturity and censoring | the fill record's later months carry fewer buildings; the tail mean beyond them |
| 13 | Order of operations | conform, units, occupancy, household size, group quarters, comparison |
| 14 | Row order | none |
| 15 | Duplicate resolution | a re-issued permit counted once, in the year of the first (asks) |
| 16 | Identity normalisation | cities as the census base names them; the utility's capitals |
| 17 | Netting | demolitions netted against completions |
| 18 | Dimensional units | housing units, residents, months |
| 19 | Code and status semantics | building type codes through the code table; never the stump |
| 20 | Integerisation | none before the comparison |
| 21 | Clause scope | rule 2 the tiers, rule 3 the housing authorized |
| 22 | Forward window contents | the 2027 tiers set on the 1 April 2026 estimate (Draw) |

## Literal reader

Executed word for word, the rules fix the cities, the components (occupied units times the 2020 household size plus
group quarters), the housing units, the date and the line. The occupied units on 1 April 2026 are not observed, so
they are estimated: the candidates are the 2020 census occupancy, the ACS occupancy, and occupancy by building age
from the utility's account history. The data separate them: buildings in the account history are near the stock's
occupancy only after about two years and about half full at six months, so every variant that counts new buildings
by age puts Fairhaven and Linden alone over the line, and both stock rates put seven (checks.py).

WHAT screen (stumping 1.2): population, rule 2.1; outcome, rule 2.2 (residents in occupied units plus group
quarters); date, rule 2.2; unit, rule 2.2 (the housing unit method's components); comparison, rule 2.3. The decisive
step settles none of them: it is how the filed occupied units are estimated for buildings that opened recently.

## Oracles

None. No control, published estimate or reconciliation ties only under the golden: no city population estimate
ships, and the voter and school files are counts of other things.

## Ask sheet

- **Ask A, each city's single-family units authorized by permits first issued in 2025: 12 figures.** H18 home:
  rule 3.1, the Committee's review of housing growth beside the tiers. Path: the three permit exports, the building
  type code table, the rules. Devices: D7, the true key elsewhere: a permit that lapsed before work began was issued
  again under a new permit number, and only the parcel and project show the building was permitted before; D3, code
  vintage: townhouse rows carry several units on one permit and are single-family only by the code table.
- **Ask B, each city's multifamily units authorized the same way: 12 figures.** Same path; stalled apartment
  projects re-permitted in 2025 carry the device in every city.
- **The construction layer:** the upper-tier cities and their count.

| Ask | Cracker (every 2025 permit, classed by the code table) | Mirror (ACS occupancy) |
|---|---|---|
| A, single-family (12) | miss | miss |
| B, multifamily (12) | miss | miss |

Pair ceiling: 35.5 (cracker 45.0 with the call and no ask figure; mirror 26.0, two of four main figures)

Mirror leakage: 0.0 per cent of ask weight

Measured by: generator/ceiling.py

## Tried and rejected

- 2026-10-20, at the draw: ET41's own world, broadband grant allocation from the FCC map: served, underserved,
  reliable technology, enforceable commitments and the location fabric are filed BEAD definitions and the base is a
  recorded count, so every lever was a filed definition, a fabric clean-up (Layer 1) or maturity of pending
  challenges; re-worlded.
- 2026-10-20, at stage 4 (architecture 1 spent): isolated reader 2 (sonnet, medium, fresh unzip) landed the call
  (Fairhaven and Linden) and all 24 ask figures. It read rule 2.2's "occupied housing units on 1 April 2026" as units
  occupied, not units existing, saw in the utility file that premises first billed after January 2021 start near
  empty while the older ones sit flat at 0.947, built the lease-up curve and applied it to every city; and it keyed
  the permits on city and parcel, which exposed every expired-and-reissued permit. Lessons: a fill record whose new
  premises begin at zero beside a flat stock is a ready-made curve one step from use, so it is the reflex, not a
  skipped step; the word "occupied" in the estimand points at it; a parcel key exposes re-issues to any hygiene
  pass. Reader 1 and the judge were stopped.
- 2026-10-24, architecture 2 draw: the payroll survey's birth-death model against the lagged QCEW census (reserved
  in task482's note). The months after the benchmark need a forecast of the net birth-death residual, and no filed
  criterion closes that carry-forward family; survey-research/etl is also under ban.pairing while task483 sits in
  the window. Not drawn.
- 2026-10-24, architecture 2 draw: a health plan's paid claims completed by received-date development after a
  processing speed-up. Spent in task451 (received-date development against the paid-date chain ladder).
- 2026-10-24, architecture 2 draw: a scanner-data price index's chain drift under sales, a multilateral index
  against linked Tornqvist. Spent in task463.
- 2026-10-24, architecture 2 draw: the variance of a year-on-year change over an overlapping member panel (a cost
  growth target read through a confidence interval). Spent in task195 (the paired difference), where a reader landed
  it.
- 2026-10-24, architecture 2 draw: rapid guessing read from response times. Spent in task479 (Gate G
  planted_defect_flip).
- 2026-10-24, architecture 2 draw: an aerial survey's intermittent plumes annualised as detections over overflights.
  That is task478 architectures 1 to 4's insight (detections over the coverage that could have seen them), and
  readers landed it there.
- 2026-10-24, architecture 2 draw: orphan wells' methane from a measurement campaign after worst-first plugging. The
  surviving wells' domain is one hygiene filter from the golden: a reader who counts unplugged wells drops the
  plugged ones from the sample too, so the reflex lands it.
- 2026-10-24, architecture 2 draw: an inventory base year recalculated after a method change, where the per-class
  recalculation (the reflex) is wrong because worst-first replacement left a cleaner surviving stock. Unspent at the
  slot screens, but its natural world is gas distribution mains, which is task476's (a niche repeat); a vehicle
  fleet's model-year rates tangle age with model year and reopen the family. Carried to the next draw as a lead, not
  drawn.
