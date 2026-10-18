# task268 design note

A quick-commerce grocer's one weekday dark-store pilot for 2027, among six candidate metros, decided on each core's delivery-weighted density.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task268.json`, architecture v1, registered 2026-10-18. The grocer is an online retailer (`retailer_or_ecommerce`); its board decides the pilot metro (`board_of_directors`); the pilot's launch forces it (`launch_or_rollout`); the requester is the vice president of network expansion (`operations_director`); no context artifact (`none`): the grocer's expansion log of its home-metro launches ships as a distractor; no calibration organ. `guard.py check` BLOCKed on the same-puzzle and same-driver tests (population gap, pattern E, a pick, method_or_model_selection) against older builds and passes with a differentiation line for each on the card; WARNs answered in item 9.
2. Pairing: Survey Research & Official Statistics (client domain) / small-area-estimation / Descriptive & Distribution Analysis. The task type's own object decides the call: each core tract's weekday presence, a small-area estimate made by carrying a national survey's rate onto complete administrative counts (the synthetic estimator), within the strata where the rate holds. The setting is a grocer's siting decision; the seed's domain (supply chain, quick-commerce siting) is kept as the world.
3. Niche: a grocer that delivers by e-bike within twenty minutes on weekdays from 9:00 to 18:00 choosing, among six metros whose cores the planning map fixes, the one where the people present on an average weekday are densest, weighted by the people present.
4. Call and shape: where the pilot goes (`pick_one_of_n`, question form where). Shape 14 (cuts of a distribution): the people present in each core distributed over its tracts' densities, each core's delivery-weighted density (the presence-weighted mean of tract density) with the share of its people present in its densest tracts.
5. Gate G `method_or_model_selection` (the strata of the synthetic estimator: the on-premises share pooled within industry group against within industry group and the type of county the worker lives in), strategy `composition_mix` (the cores' flows draw their workers from a different mix of county types than the survey's), decisive generator G14 (the survey's pooled share does not apply to a core's pool of commuters), then G6 (the composition differs core by core) and G2 (a job held is not a person present each weekday).
6. Data-native sentence: the commuting table records each primary job once, at the employer's tract, from wage records that never see whether the worker goes in; the survey records the days each respondent spent on the employer's premises and the type of county they live in, and office workers who live in outlying counties or outside the metro come in far less often than central-county ones, so a core whose offices draw from the exurbs holds far fewer people on a weekday than its jobs suggest.
7. Sources, one line each:
   - The client's rigor library, small-area-estimation patterns 1 (Fay-Herriot shrinkage) and 2 (benchmark to the reliable total): this build's estimator is the synthetic one, rates carried onto complete counts, and its pitfall is the homogeneity of the carried rate within its strata; no area-level model and no benchmark.
   - task448 (survey research, a register completed within filing-route strata): coverage of producers measured where two lists overlap; here a presence rate measured in a national sample is carried onto flows within residence strata, and the target is a density.
   - task256 in this lane (a reference group's body measurements carried through two recorded measurements): a multivariate distribution carried through covariates; here a one-dimensional rate within strata.
   - task264 and task261 in this lane (survey weights, replicate variance): the survey's weights are used plainly here; the decisive step is the strata, not the weighting.
   - task254 (urban network analysis of bus pace): an urban setting with no presence to estimate.
8. People, drawn with `guard.py names --geo "United States" --seed 268`: Megan Swanson (vice president of network expansion, the requester) and Carolyn Cook (director of location analytics, author of the board paper's method appendix). Nathan Watkins and Elizabeth Walton were set aside (first names on file). Invented names (Larderline, Quillmere, Tessavon, Halberdine, Corrisford, Dunnaway, Ashcombe) screened against every US city and county name (no word within two edits, none containing a real distinctive word); the counties are screened the same way at build.
9. WARNs answered: `overuse.gate_g` (method_or_model_selection, 5 of the last 12): the decisive step chooses the strata of a synthetic estimator, a method choice, and no other mechanism describes it honestly; the batch varies elsewhere (a survey-research small-area estimate, shape 14, a where question, an online retailer, a pptx board deck).

## Default path

1. Read the board paper: the pilot goes to the metro whose core has the highest delivery-weighted density, the people present in the core's tracts on an average weekday per km² of land, each tract weighted by its people present; the six cores' tracts are listed.
2. Residents of each core tract from the census population table; land area from the gazetteer.
3. From the commuting table (its main and auxiliary files), each core tract's primary jobs held by people living in another tract and its residents' primary jobs in another tract.
4. People present in each tract: residents, less residents working in another tract, plus people from other tracts working in it (the commuter-adjusted daytime population).
5. Each core's delivery-weighted density: the sum over its tracts of people present squared over land area, divided by the core's people present; the highest wins.

Ends on: Halberdine (the highest density with every job present every weekday).
Golden: Tessavon.

## Stump sentence

The default path sends the pilot to Halberdine because it counts every primary job in the commuting table as a person at work in its tract on every weekday; carrying the national survey's share of weekdays on the employer's premises onto each flow by industry group alone moves it to Corrisford, whose port and logistics jobs the survey's trade and transport share keeps nearly whole, and carried by industry group and the type of county the worker lives in, the share puts Tessavon first, because Halberdine's head offices and Corrisford's port draw most of their workers from outlying counties and beyond, who spend far fewer weekdays on the premises, while Tessavon's offices draw from their own county.

## Three rules

Task type: small-area-estimation (Survey Research & Official Statistics), which serves Descriptive & Distribution Analysis: each core tract's weekday presence is a small-area estimate built by the synthetic estimator from a national survey and complete administrative counts.
Domain test: the deciding quantity is each core tract's weekday presence, which the field estimates for small areas by carrying a rate measured in a national survey (the share of days on the employer's premises) onto complete administrative counts (the commuting table's flows) within strata where the rate holds; the call turns on choosing those strata.
Swap: "the metro whose core has the most people present per km² on a weekday, its commuting flows carried at the survey's on-premises share for each flow's industry group and county type of residence" with megawatt-hours for people present has no sample of members, no register of attachments and no carried rate whose strata must match the counts, so the sentence stops making sense.
Layer 1: the commuting table's main and auxiliary files (the agency's split by state of residence); the census table's GEO_ID with its summary-level prefix against the gazetteer's GEOID (two Census products); land area in square metres and square miles, and water-only tracts with no land (the gazetteer); the survey's two-digit NAICS sectors and ranges (31-33, 44-45) against the commuting table's three industry groups (two producers' codings); twelve monthly survey waves each weighted to its month (the survey's design); the delineation file's header rows, footnotes and county codes as text (the OMB release). Nothing is placed to be caught.
Layer 2: estimation_fit, the synthetic estimator's strata: the on-premises share pooled within industry group against the share within industry group and the type of county the worker lives in, which flips the call.
Decisive step: carrying the survey's share of days on the employer's premises onto each commuting flow within the strata the share varies across, industry group and the type of county the worker lives in, so that cores drawing their workers from outlying counties and beyond are credited with the presence those workers give.
Not semantics: every field read correctly (the commuting table's primary jobs by home and work tract, the survey's days worked on the premises and at home, the delineation file's county types) still leaves the easy route on Corrisford, because the error is carrying one share per industry group onto flows whose residence mix differs from the survey's, an estimation choice that no field, code or definition settles.
Not rule application: the board paper defines what is measured (the people present in each core tract on an average weekday, per km² of land, weighted by people present) and no filed rule says how presence is estimated, which survey strata carry the share, or that the share varies with where workers live; executing every stated rule leaves the estimator open, and the natural one files Corrisford.
Analyst test: a strong analyst who reads the commuting table as primary jobs by home and work tract and the survey's days on premises correctly carries the survey's on-premises share for each industry group onto every flow and picks Corrisford (the default path, every job present, picks Halberdine); carried at the share for the flow's industry group and the county type its workers live in, the same flows pick Tessavon.
Estimand: the people present in each core tract on an average weekday of the 2027 pilot (its residents, except those at a workplace in another tract that day, and the people from other tracts at a workplace in it that day), per km² of land, each tract weighted by its people present, over the core's tracts as the planning map lists them, on an average weekday of the 2027 pilot, compared across the six cores; filed in the board paper (board_paper_pilot_metro_2027.pdf).
No decoy: nothing is planted; the ACS commuting table, the survey and the commuting table are each what their producer releases, no memo, draft or stakeholder figure argues for a metro, and the expansion log, a distractor, answers another question (the grocer's own launches).
No certified replay: no published or certified figure reproduces the method; the survey publishes no presence and no on-premises share by county type, and nothing is recovered by matching figures.
Lesson: a rate carried from a survey onto complete counts holds only within strata where it is homogeneous; when it varies with a characteristic whose mix differs between the survey and the small areas (where commuters live), the pooled rate misstates the areas that draw from the tails. No build on file teaches the synthetic small-area estimator's homogeneity: task448 completes coverage within filing-route strata and task256 carries a multivariate distribution through recorded measurements.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 every primary job present every weekday (the default path) | the board paper counts the people at a workplace in the tract that day and names no attendance; the commuting table's documentation says it records primary jobs by home and work tract | the commuting table's flows, residents from the population table | the commuter-adjusted daytime population, the Census Bureau's own published concept | none | none | residents less out-commuters plus in-commuters, one sum per tract | readable |
| R0 hazard: the ACS share working from home taken off each flow by the worker's county of residence | none | the ACS table's worked-from-home line per county | remove the fully remote | none | none | one factor per flow | readable |
| R1 the survey's share of weekdays on the employer's premises carried by industry group | none | the survey's NAICS sector against the commuting table's three industry groups, crosswalked in the commuting table's documentation | carry the survey's rate on the classifier the counts carry | none | none | one rate per group | readable |
| (decisive) R2 the share carried within industry group and the type of county the worker lives in, relative to the workplace's metro | none: no document speaks of strata, of where workers live or of a share varying with it; the board paper files only what is counted | the survey carries the residence relation as one of its eleven classifiers; the commuting table carries no residence type, which each flow gets only from its home tract's county through the delineation file against the work tract's metro (three files, no header join) | the reflex carries the share on the counts' own classifier, industry group | no shipped figure states a tract's or a core's presence, or an on-premises share by anything | GEO_IDs normalise and join once each, keys unique, county codes text; nothing for the battery | a weighted sum over flows with shares from a cross-tabulation; no ratio of shipped figures | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | people present | a tract's residents, except those at a workplace in another tract that day, and the people from other tracts at a workplace in it that day | residents alone; workers alone | other calls | the board paper's definition sentence, quoted whole in the literal reader |
| SF2 | residents | the census population table's total population of the tract (ACS 2018-2022 five-year) | households; people 16 and over | same call | the paper's "residents as the census population table counts them"; one population table ships |
| SF3 | workers | the people whose primary job the commuting table records at the work tract, in both its parts | the main part alone, leaving out the workers living in another state | same call, other figures | the commuting table's documentation (the auxiliary part holds the jobs of workers living in another state) and the paper's "workers as the commuting table records their primary jobs"; same call asserted |
| SF4 | at a workplace that day | on the employer's premises that weekday: the survey's weekdays at the employer's premises over the five weekdays of its reference week | over the days worked | same call, other figures | the paper's "an average weekday" (a weekday of leave is a weekday away from the workplace); same call asserted |
| SF5 | an average weekday of the pilot | the latest releases as they stand: the 2022 commuting table, the 2018-2022 population, the survey's twelve monthly waves to September 2026 | the latest wave alone; a trend carried to 2027 | same call | the paper's "as the latest releases stand, with no growth projected"; an average weekday of a year needs the year's waves; same call asserted on the September wave alone |
| SF6 | per square kilometre of land | ALAND in square metres over a million | ALAND_SQMI times 2.589988; land and water together | same call, same figures | the gazetteer's two land columns agree at the reported rounding (asserted); "land" rules out water |
| SF7 | the core | the tracts the planning map lists for the metro | the central county; tracts touching the core | other figures | the paper's "the core's tracts as the planning map lists them" |
| SF8 | delivery-weighted density | the sum over the core's tracts of people present times their density, over the core's people present | the unweighted mean of tract densities; the core's people over its land | other calls | the paper's "averaged over the core's tracts with each tract weighted by its people present" |
| SF9 | a tract with no land | no density and nobody present; it adds nothing | a division by zero | same call | the gazetteer's ALAND 0 and the population table's 0 for the water tract (asserted) |
| SF10 | a survey respondent's industry group | the commuting table's three groups by NAICS sector, as its documentation lists them (goods producing 11, 21, 23, 31-33; trade, transportation and utilities 22, 42, 44-45, 48-49; all other services 51 to 92) | utilities with goods producing | same call | the documentation's list (asserted) |
| SF11 | the type of county a worker lives in | the survey's residence relation (a central county of the workplace's metro, an outlying county of it, outside it), built for each flow from the home tract's county and the delineation file against the work tract's metro | same county, another county, another state | same call, other figures | the codebook's definition by the OMB delineation; same call asserted |
| SF12 | the survey's weights | each respondent's final weight | unweighted | same call, same figures | the codebook's estimation note; the figures converge (asserted at the reported rounding) |
| SF13 | the twelve waves | pooled, each wave weighted to its month | each month equal | same call, same figures | each wave's weights total its month's employed adults within half a per cent (asserted) |
| SF14 | the share in dense tracts | people present in tracts of 20,000 or more per km² over the core's people present | the count of such tracts; more than 20,000 | same call | the prompt's wording; no tract within 3 per cent of 20,000 under any route (asserted) |
| SF15 | residents working in their own tract | in the tract all day either way, neither taken off nor added | taken off as away at work | other figures | the paper's "at a workplace in another tract"; asserted |
| SF16 | respondents with no usual workplace or a workplace outside any metro | outside every stratum the flows need | pooled into a stratum | same call, same figures | the codebook's code 4 (asserted) |
| SF17 | service hours | the pilot's weekday delivery window, 9:00 to 18:00; the estimand is the weekday's people present | an hour-by-hour profile | same call | the paper's estimand counts people present that day; nothing shipped places workers by hour |
| SF18 | ties | none | none | none arises | no two cores within 1.15 on the golden (asserted) |
| SF19 | rounding | every figure from unrounded values, rounded once as the prompt states | rounding presence before the density | same call | the prompt's rounding sentence; each graded figure's distance to its rounding edge asserted |

## Ladder

Built and measured on the cut pack (`generator/analysis.py`, every pick, margin and position asserted in `checks.py`). Delivery-weighted density, people present per km²:

| Rung | Construction | Halberdine | Quillmere | Corrisford | Tessavon | Ashcombe | Dunnaway | Pick (margin) | What kills it |
|---|---|---|---|---|---|---|---|---|---|
| R0 (default) | every primary job present every weekday | 55,800 | 42,700 | 42,700 | 39,200 | 15,500 | 21,700 | Halberdine (1.31) | the survey's weekdays on the premises: a job is not a person at work every weekday |
| Hazard | the ACS share working from home taken off by county of residence | 51,600 | 38,700 | 39,300 | 36,000 | 15,600 | 19,900 | Halberdine (1.31) | the same: the fully remote are a small part of the weekdays away |
| Route | one survey share for every job | 33,100 | 25,500 | 27,300 | 25,400 | 16,300 | 14,700 | Halberdine (1.21) | the survey's shares differ by industry group |
| R1 | the survey's share by industry group | 26,600 | 20,800 | 32,300 | 22,900 | 15,600 | 16,100 | Corrisford (1.22) | within each group the share falls with where the worker lives, and the cores' flows draw from another mix than the survey's |
| Route | the share by the type of county the worker lives in alone | 23,000 | 22,700 | 17,200 | 30,600 | 15,400 | 14,100 | Tessavon (1.33) | the same call, other figures: the groups' shares differ within each county type |
| R2 (golden) | the share by industry group and the type of county the worker lives in | 18,400 | 18,800 | 21,700 | 28,800 | 15,100 | 15,500 | Tessavon (1.33) | none |
| Variants of R2 | the survey unweighted; each wave weighted equally; days on the premises over days worked | | | | | | | Tessavon (1.33 to 1.34) | the same call; the unweighted and equal-wave shares move no printed figure, days worked moves them |

Survey shares of weekdays on the employer's premises (FINALWT, twelve waves): all other services 74.2 central county, 44.1 outlying, 11.7 outside (51.4 pooled); trade, transportation and utilities 90.2, 80.3, 34.9 (81.7); goods producing 91.1, 90.8, 81.4 (90.0). The survey's residence mix: other services 0.48, 0.30, 0.22; trade 0.59, 0.31, 0.10; goods 0.54, 0.36, 0.10. The cores' inflows: Halberdine's other-services workers 0.31, 0.27, 0.42 (its head offices' staff across the state and beyond appear at the establishment); Corrisford's trade and transport workers 0.28, 0.22, 0.50 (the port's drivers and logistics staff); Tessavon's every group 0.89 to 0.90 from its own county.

Position and separation: Tessavon 4th at R0, on the hazard and on the one-share route, 3rd at R1, never first before R2 and never second on a rung; every rung's margin 1.21 or more, the final 1.33. Every correction walks Halberdine down; only the decisive move reverses Corrisford and Tessavon. Dominance: Tessavon's lift from R1 to R2 relative to Corrisford's (1.26 against 0.67, a factor of 1.87) over Corrisford's R1 advantage (1.41) is 1.33. Clean-data test: the generator's truth runs the same ladder before any mess, asserted (R3a, R3b). Worth: the decisive step is the whole stump on the pick; R0 and R1 each name their own metro, and the hazard and the one-share route land on R0's.

Per-core figures under R2: people present 265,000 Halberdine, 251,000 Quillmere, 313,000 Corrisford, 417,000 Tessavon, 371,000 Ashcombe, 330,000 Dunnaway; share in tracts of 20,000 or more per km² 37, 42, 47, 43, 2 and 31 per cent. Every route other than R2 moves each core's figures off these.

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | residents of the core tracts (the census population table) and workers at them (primary jobs in the commuting table, both parts) | filed: the board paper; SF2, SF3 |
| 2 Unit of account | a person present in a tract on a weekday | filed: the board paper |
| 3 Attribution window | an average weekday of the 2027 pilot, from the latest releases as they stand | filed: the board paper |
| 4 As-of dating | the 2022 commuting table, the 2018-2022 population, the survey's waves to September 2026 | C1: one vintage of each ships |
| 5 Version basis | one release of each source | C1 |
| 6 Denominator | each tract's land in km² | filed; SF6 |
| 7 Weighting | tracts by their people present; respondents by their final weights | filed: the board paper, the codebook; SF12 converges |
| 8 Window length | the survey's twelve monthly waves | SF5, SF13 |
| 9 Boundary inclusivity | 20,000 or more per km² for the dense-tract share; 150 to 450 m² inclusive for Ask A | the prompt; C1: no tract within 3 per cent of 20,000, no unit within 2 per cent of a size bound (asserted) |
| 10 Rounding path | unrounded figures, rounded once as the prompt states | the prompt; SF19 |
| 11 Tie-break | none arises | C1: no two cores within 1.15 (asserted) |
| 12 Maturity and censoring | none: a closed commuting year and closed survey waves | C1 |
| 13 Order of operations | the share per flow, then presence per tract, then the core's weighted density | C1 (linear) |
| 14 Row order | none | C1: asserted over permutations |
| 15 Duplicate resolution | none in the main files | C1: keys unique (asserted) |
| 16 Identity normalisation | the population table's GEO_ID with its summary-level prefix against the gazetteer's GEOID; tract codes as text with a state's leading zero | C4: every core tract joins once normalised (asserted); unnormalised, a whole state fails to join, loudly |
| 17 Netting against gross | residents working in their own tract neither taken off nor added | SF15 |
| 18 Dimensional units | square metres and square miles of land; square feet in the listings | SF6; Ask A |
| 19 Code and status semantics | the survey's residence relation and day counts; the delineation's Central and Outlying | dictionary: the codebook, the delineation file |
| 20 Integerisation | people present to the nearest thousand from unrounded sums | the prompt |
| 21 Clause scope | the paper's density sentence governs the pick; the prompt's figures are per core | filed |
| 22 Forward window contents | the 2027 pilot's weekdays, no growth projected | filed: the board paper |

## Literal reader

Executed word for word, the board paper sends the pilot to the metro whose core has the highest delivery-weighted density: the people present in each of the core's tracts (as the planning map lists them) on an average weekday of the pilot, per km² of the tract's land, averaged over the core's tracts with each tract weighted by its people present; a tract's people present are its residents (as the census population table counts them), except those at a workplace in another tract that day, and the people from other tracts at a workplace in it that day (workers as the commuting table records their primary jobs), as the latest releases stand with no growth projected. How many of a tract's workers are at the workplace on an average weekday is in no count: the one shipped source for it is the working-arrangements survey's weekdays on the employer's premises, which within each industry group fall with where the worker lives relative to the workplace's metro, and the flows into and out of each core tract carry both, so the share carried within industry group and residence type gives the golden. Every job present (R0) and the ACS share working from home (the hazard) count people the survey shows away; one share per industry group (R1) applies the survey's residence mix to flows whose mix is another. SF2 to SF19 converge or are ruled out by a quoted sentence, asserted.

## Oracles

- No shipped file states a tract's or a core's people present, a density, an on-premises share by residence type or by core, or a ranking of the metros; the survey's codebook gives definitions and its estimation note only.
- The ACS commuting table (a distractor) states each county's workers by means of transportation, worked from home among them; it confirms no rung (the hazard lands on R0's metro).
- The County Business Patterns extract (a distractor) counts county employment by sector; it ties to nothing graded.
- Ask referees: none ships. No file states a count of vacant units, a median rent or a count of either competitor's dark stores; each ask's device is found only by an inconsistency inside its own records.

## Ask sheet

The asks are decoupled from the call: neither reads the commuting table, the survey, the population table or the gazetteer, and the call computes identically with both ask files deleted (asserted). Both read the planning map's core tracts, which carry no ask organ. They are the premises and competition lines every candidate carries in the board pack.

**Ask A. For each core, how many ground-floor retail or flex units of 150 to 450 m² were available to lease on 30 September 2026, and their median asking rent per m² a year (12 figures).**
- H18 home: the pilot needs a ground-floor unit in the chosen core; the board pack's premises line for every candidate, a measure the call does not turn on.
- Use: the workbook's premises sheet and the deck's site line.
- Path: retail_space_listings_20261001.csv (listing_id, broker, address, suite, census_tract, floor, property_type, space_sf, asking_rent, rent_basis, status, status_date, date_listed), the planning map's core tracts: two files, fourteen columns.
- Primary device (D6, a rollup above its parts): where two suites of a ground floor are on the market, the broker posts each suite and, in about half the buildings, the floor as one listing too, its suite blank, its size the suites' sum and its rent their area-weighted mean; every core has one or two such floors whose combined size sits inside 150 to 450 m². Listing ids unique, no exact duplicate, address and suite unique, a blank suite also on genuine single-unit buildings: the battery finds nothing. Found only by the inconsistency inside the records: a blank-suite listing at an address whose suites are all listed, its size exactly their sum.
- Its over-cleaning half: one unit per address merges the genuine suites of buildings with no combined listing.
- Hazards: units leased on 1 October show Leased with that date in the export (available on 30 September); rents quoted per square foot a year, per square foot a month or as a monthly total; sizes in square feet; upper floors, office space and listings posted after the date.
- Stops (prototype): every available listing counted (the cracker) 8, 11, 6, 13, 8 and 6 units against 7, 9, 5, 11, 7 and 5, every median 6 to 16 dollars high; the export's status read as it stands, each count off by one either way; one unit per address, 10 of 12 figures off; the answer.
- Realism: listing platforms carry a building's combined floor beside its suites; a broker markets both ways.

**Ask B. For each core, how many dark stores each of the two competitors was delivering from on 30 September 2026 (12 figures).**
- H18 home: the board pack's competition line for every candidate, a measure the call does not turn on.
- Use: the workbook's competition sheet and the deck's market line.
- Path: competitor_locator_scrapes_2026.csv (scrape_date, brand, store_code, store_name, address, unit, latitude, longitude, census_tract, services, hours), the planning map's core tracts: two files, twelve columns.
- Primary device (D5, out-of-scope rows known only by structure): both competitors list independent convenience shops that fill their delivery orders beside their own dark stores, in the brand's own naming and with Delivery among the services; every core has one or two, each in both locators at the same address and unit. Store codes unique within a brand and scrape, no exact duplicate: the battery finds nothing. Found only by the cross-brand cut: a store one competitor runs cannot be in the other's locator.
- Its over-cleaning half: dropping every address both brands list (without the unit) also drops the two brands' dark stores sharing a building in Quillmere and Tessavon.
- Hazards: pickup points (Pickup only); stores closed or opened during the year; a store moved under its code; stores just outside a core.
- Stops (prototype): the 30 September scrape's delivering stores (the cracker) each cell one or two high; one per street address, the co-located cells low; the answer.
- Realism: quick-commerce platforms list partner shops in their store finders, and a shop partners with more than one platform.

Main population zero-counts: device and hazard rows in the commuting table, the population table, the gazetteer, the delineation file, the survey and the board paper: 0 (the ask files are their own; asserted at stage 3 with the call identical when both are deleted).

| Hazard | Asks moved | Per-ask delta (prototype) |
|---|---|---|
| leased the day after the date | A | the count one low per such unit when the export's status is read as it stands |
| rent quoted per month or as a total | A | the median moved when read as a yearly rate per square foot |
| pickup points | B | each cell high by the core's pickup points when every listed point counts |
| a store moved under its code | B | the cell of the old and the new tract |

Referee: none (Oracles).

| Ask figure | The cracker's figure against the golden | Cracker (lands the call, runs the battery: exact duplicates, key uniqueness on listing_id, on address and suite and on brand, store code and scrape, unmatched tracts; reads every rent basis and status date; executes the prompt's filters) |
|---|---|---|
| A, each core's units (6) | one or two high | miss |
| A, each core's median rent (6) | 6 to 16 dollars high | miss |
| B, each competitor's dark stores in each core (12) | one or two high | miss |

Mirror leakage: 0 per cent of the ask weight (the mirror takes the asks the same way; `cracker.py` scores both).
Pair ceiling: 28.5 (the cracker 45 on the call, its components and instruction-following, none of the asks; the mirror 12; rerun on the generated rubric at stage 3).
Measured by: `generator/cracker.py`, on the design prototype at stage 2 and on the cut pack from stage 3 (checks.py runs it): the cracker keeps 0 of 24 ask figures (A 0 of 12, B 0 of 12), the mirror the same, the over-cleaner 10 of 24; pair ceiling 28.5.

## Build record

- Generator: `common`, `world` (the six metros' tracts, residents, jobs and commuting flows on per-metro random streams, the survey's twelve waves), `records` (the exports), `askworld` (the listings and the locator scrapes), `docs` (the board paper, the codebook, the commuting notes, the manifest), `analysis` (every figure from the shipped pack), `deliver` (the goldens, figures.json, metadata.json), `checks` (124 assertions), `verify` (independent, pandas), `cracker`, `postprocess`, `build`. Seed 268 with per-metro streams (Halberdine 0, Quillmere 3, Corrisford 40, Tessavon 9, Ashcombe 80, Dunnaway 4), each chosen so every graded figure sits clear of its printed edge, the square-mile land variant prints the same, no tract lies within 2 per cent of 20,000 per km² and each rung lands within 4 per cent of its calibration.
- Pack: 16 files (CSV, TXT, XLSX, PDF); the commuting table's main part 129,954 rows, its auxiliary part 10,992, the survey 60,591; distractors the ACS means-of-transportation table, County Business Patterns and the Trenstead launch log (`metadata.json`).
- Gates: checks green, `verify.py` 0 mismatches, two builds byte-identical, `figures_check.py` 56 of 56, `target.zip` cut; leak.py (as of 2026-10-06) REVIEW on sweeps 3 and 4 only; guard.py surface clean (no persona in the pack); guard.py heart BLOCK on the registration window only (ban.role and ban.strategy against task165, test.same_driver against task167 v2), nearest driver task253 v1 at 0.10; the cracker on the cut pack keeps 0 of 24 ask figures, the over-cleaner 11 of 24.
- Stage 4 (2026-10-18). Leak reader: no decisive-step sentence, no ranking or helper file; question 6 "a stated procedure combined with an analytical choice", naming attendance by sector and home relation from the codebook's HOMEREL; it committed the golden call (Tessavon 28,805 against Corrisford 21,709) and every core density: `score_reader.py` exit 1, Gate F failed. Judge thread (from the agent's brief, the agent having no Agent tool): NOT_DETERMINISTIC on two asks only, SEND_BACK by the gate table; the call forced under every reading tried; Gate G statistical_rigor and analytical_non_defect; Gate H domain, layers and decisive step pass. Its findings: people present in three cores turn on typing a resident's workplace outside any metropolitan area as HOMEREL 3 (the golden) or 4 (the codebook); the dark-store counts need the partner-shop rule, which nothing shipped states. Architecture 1 spent (`## Tried and rejected`).

## Tried and rejected

- The seed's own stump, residential density against daytime presence, rejected at the draw on 2026-10-18: with the estimand filed as the people present, choosing presence over residents is reading the estimand (data semantics); left unfiled, the call is not determinate.
- Network ride times against straight-line catchments (urban network analysis), rejected at the draw: a filed twenty-minute ride makes the street network the literal method, so the decisive step would be rule application.
- The plug-in bias of the weighted density from noisy survey counts per tract, rejected at the draw: the same insight as task253 (sampling noise counted as signal).
- Attendance conditioned on commute distance as a continuous covariate, rejected at the draw: the functional form opens forks on every graded figure; the county type of residence carries the same structure with nothing to choose.
- A mobile-device presence panel, rejected at the draw: a column holding the deciding quantity scaled, which R1 forbids and which reads the call off.
- Six distinct winners on six rungs, tried in the prototype on 2026-10-18: consecutive corrections move the cores too little to clear 1.15x margins at every rung; the ladder keeps three rungs with their own winners (every job present, the share by industry group, the share by industry group and county type) and the work-from-home reflex as a hazard landing on rung 0's metro.
- The draw's prototype shares (other services 0.80, 0.45, 0.20 against a survey mix of 0.45, 0.30, 0.25 in every industry), set aside at stage 2 on 2026-10-18: a quarter of every industry's workers living outside their workplace's metro is not the national pattern; with the survey's mix by industry (other services 0.48, 0.30, 0.22) and the realistic shares, two office cores cannot both clear 1.15, so Corrisford became a port and logistics core whose drivers and remote sales staff, living mostly outside the metro, are seldom on the premises.
- The draw's registration slot, set aside at the end of stage 2 on 2026-10-18: the draw-time `guard.py check` ran before the pull that brought in task165 (composition_mix, operations_director, registered at 14:10) and task167 v2 (population, E, method_or_model_selection, 06:59), so the card filed at 16:11 carries ban.strategy, ban.role and test.same_driver BLOCKs against them; three conditioning-transfer drivers in one batch is the template the bans exist for, and the composition stump is this seed's own pitfall, so the design is kept and the card re-registered once the batch has moved past them.
- Architecture 1 (the survey's share of weekdays on the premises carried onto each commuting flow within industry group and the type of county the worker lives in), spent at stage 4 on 2026-10-18: the isolated reader, working the cut pack cold at medium effort, carried the share by industry group and HOMEREL onto every flow as a matter of course and committed Tessavon at 28,805 against Corrisford's 21,709 (`score_reader.py` exit 1, the call 5 of 5, every core density); the decisive rung was readable through the schema, because the survey carries the residence relation as a column the codebook defines against the workplace's metropolitan area, which types every flow through the delineation file, and an analyst carrying a survey rate onto counts carries it on every classifier the two sources share, so the stratum the design called decisive is the careful analyst's reflex. The judge found the call forced and Gate H passing, and two ask forks (a workplace outside any metropolitan area is HOMEREL 4 in the codebook where the golden typed those flows 3; Ask B's partner-shop rule unfiled). In this world a stratification the survey's own columns invite cannot carry the stump; the re-root draws a decisive step no classifier the sources share can reach.
