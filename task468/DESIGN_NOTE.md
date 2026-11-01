# task468 design note: Harrowmere's pressured-ward uplift, on the price change of dwellings that did not change

Status lives in `pipeline.json`; this note holds the design of architecture 5, drawn fresh on 2026-10-31 as a batch 1
re-root. Read `## Tried and rejected` first: architectures 1 (transit nominations), 2 and 3 (specialty pharmacy
staffing) were spent at stage 4, and architecture 4 (the Medicaid plan's linkage-corrected mortality bonus) was retired
by the batch audit, short of the survivor anatomy on the Reflex. Nothing of the healthcare world is kept.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task468.json`, architecture v5, registered 2026-10-31 after a pull;
  `guard.py check` on the filed card WARN only: overuse.org_family (government_agency carries 42 builds), kept because
  the body that pays a grant uplift on affordable homes is a housing investment agency and no other family is the
  honest one; the persona first names drawn first (Margaret, Duncan, Raymond, Derek) each sat in one older build and
  were redrawn from the same pool. Architectures 1 to 4 are in the card's lineage.
- **Pairing:** Survey Research & Official Statistics / seasonal-adjustment-official-time-series-production (serves
  forecasting and ETL) / Data Extraction & Conformation (ETL). The ward index is an official small-area price series
  compiled from administrative microdata: the price paid record (the 2015 to 2025 file, the 2026 yearly file and a
  monthly update whose A, C and D records add, correct, move and delete earlier records), a postcode lookup that carries a ward boundary review,
  and the city council's building control register in two systems' layouts. The call turns on which sales pairs the
  conformed dataset may hand the constant-quality index.
- **The ETL move (guide-to-prompt 1):** recover a per-case input a second file pins. Per sales pair, whether the
  dwelling had building work completed between its two sales is pinned by the building control register, at a grain
  (each completion's certificate date on each dwelling) the price paid record never carries. Reading the register
  correctly is not sufficient: its own use in the pack is the housing supply count, it shares no key with the sales,
  and the repeat-sales design is the field's constant-quality construction, so a careful compiler takes the pairing of
  the same dwelling as the quality control it is meant to be.
- **World:** Harrowmere, a fictional English city of twelve wards (fictional postcode area HW); the Harrowmere and Vale
  Housing Agency, a regional housing investment agency that pays grant on affordable homes; its Pressured Wards Uplift
  (GBP 12 million for 2027-28, shared among the wards whose constant-quality house prices rose more than 5 per cent
  from 2025 to 2026, in proportion to the affordable homes due to start on site there in the programme year); its Ward
  House Price Index methodology; Harrowmere City Council's building control service.
- **Shape 05, allocation to a fixed total:** the pot split among the wards over the line. Criteria: the set (1), each
  ward's verdict (12), each pressured ward's share (3), the shares summing to the pot (1), each ward's 2025 to 2026
  index change (12), the chart's parts (the changes, the line, the pressured wards marked: 3), the workbook (1), and the
  three asks (12 figures each).
- **Strategy:** population_selection (which sales pairs measure a constant-quality price change); Gate G etl_conformance
  (the conformed pairs judged against the methodology's contract); Layer 2 estimand_identification (the comparison the
  index promises, the same dwelling at the same quality, is not what every pair of its sales compares).
- **Furniture:** forum committee_or_panel (the Agency's Investment Committee), forcing event budget_or_appropriation (the
  2027-28 uplift allocation), organisation government_agency; none repeats the last three builds (task482 other,
  purchase order, manufacturer; task172 funder, vote, university; task125 executive team, vote, local government).
- **Shell:** question form which, the second sentence opening on the compilation ("Compile each ward's ..."),
  deliverables pdf and xlsx; architecture 4's shell (how-many, xlsx) is not reused.
- **Data-native sentence:** Pellbury is a grid of 1890s two-storey terraces whose lofts take a rear dormer, and in 2024
  and 2025 small developers bought the tired ones, most through companies, added a loft room and a rear extension under
  building regulations and sold them on in 2026, so the ward's 2026 standard sales carry houses that are larger than
  when they last sold at a standard price.
- **Abstraction sentence (tested against every approved build):** each unit's change in the price of an unchanged item
  is read from pairs of transactions on the same item, and a wave of items altered between their transactions in one
  unit, recorded only in a separate register of completed work that shares no key with the transactions, puts the
  alterations' value into that unit's price change. No approved build's abstraction is that sentence: task181 traced a
  shared resource's exposure out of a provider comparison, task463 chose a drift-free comparison for a transaction
  price index, task482's spent house price architectures (4 and 5) fitted attributes and aggregated a stock, and none
  removes the item's own change from a matched-item price change.
- **Same-puzzle and same-driver tests:** gap population, decisive generator G11 (a pair's eligibility for the index
  rests on a precondition the pair does not show), decision allocation_to_total, Gate G etl_conformance; the guard's
  structural tests clear on the filed card.
- **Personas** (`guard.py names --geo England --seed 468`): Sylvia Davison, the Agency's Director of Investment, who
  takes the uplift to the Investment Committee; Jodie Khan, the Agency's housing market analyst who keeps the index;
  Gillian Lawson, the council's building control manager, who sent the register.
- **Retrospective quantity, forward call:** the uplift is set for the 2027-28 programme year, a window not yet open;
  its test reads the latest complete calendar year's price change (2025 to 2026), as the programme rules file it.
- **Sources (all synthetic, license-clean, generated by `generator/`):** the price paid files and the January 2027
  update; the postcode lookup and the ward codes; the building control register; the Agency's index methodology,
  programme rules and 2027-28 pipeline; the providers' start-on-site claims; the request email; two distractors (the official local authority house price index, a hedonic series for the whole city, and the
  rent survey's ward medians).

## Survivor anatomy

Actor: the deciding property, whether a dwelling had building work completed between its two sales, has no column in any file; the price paid record holds no work and no dwelling identifier, the register holds no sale, and the property is a relation between two sales of one address and a completion certificate dated between them.
Link: no key ties a sale to a completion; the dwelling is the address, read from the price paid record's PAON, SAON and postcode and from the register's free-text site address (legacy) or its house number or name and postcode (Uniform), and no sentence in the pack invites the join: the register's own use in the pack is the supply count the request asks for.
Reflex: the field's method for a small-area constant-quality price change, a repeat-sales index on the pairs of each dwelling's consecutive standard sales by the methodology's least squares, is rung 1 and files Calder Bank, Kestrel Rise, Pellbury and Abbots Hollow; its usual filters (a six-month minimum hold, interval weights, a 3-sd residual trim, new dwellings' first sales out) file the same four.
Back-test: the textbook route validates; every ward's every-pair change for 2016 to 2025 runs with the city's official index within its ordinary spread, Pellbury's included, and the developers' works are a 2025 to 2026 wave, so nothing in the earlier record refutes the pairing of the same address as the quality control.
Second use: every file the decisive step reads sits in the pack for its own reason; the register carries the supply ask (net additional dwellings certified complete in 2026), the request names it for that reason, the price paid files and the postcode directory carry the index itself, and deleting the decisive step leaves all three in the pack.
Shock: Pellbury's every-pair change (6.0) is the third of the four over the line on that sort, not the largest; its building control completions per house in 2025 and 2026 sit mid-table (48 per thousand against 32 to 76); its 2024 and 2025 additional (company) entries sit second of the twelve, behind Fennick's student lets; the golden set is not an interval of the every-pair, median or 2026 sales sorts (asserted in checks.py, C6).
Pins: the WHAT sits in the methodology (constant quality, standard entries for dwellings, the May 2023 wards by postcode, consecutive sales of one address, least squares on year indicators) and the programme rules (more than 5.0 per cent, the pot, the pipeline's homes); no filed sentence names building work, a completion, the register or the developers, and deleting the methodology's "at the same quality" leaves the every-pair index as the literal reading, which is the fork SF1 records.

## Default path

1. Read the methodology (third edition): the ward index is a constant-quality repeat-sales index, standard entries for dwellings, pairs of each address's consecutive sales, least squares on year indicators, the May 2023 wards by postcode, the January 2027 update applied.
2. Load the three price paid files, apply the update by transaction identifier, keep category A entries of types D, S, T and F, and pair each address's consecutive sales.
3. Place each pair in its May 2023 ward through the postcode directory and fit each ward's annual index; take the 2025 to 2026 change.
4. Apply the programme rules: the wards over 5.0 per cent share GBP 12,000,000 in proportion to their 2027-28 starts in the pipeline.

Ends on: Calder Bank, Kestrel Rise, Pellbury and Abbots Hollow (Pellbury at 6.0 per cent on every pair)
Golden: Calder Bank, Kestrel Rise and Abbots Hollow (Pellbury at 3.1 per cent)

## Stump sentence

The default path fits the methodology's repeat-sales index on every pair of each address's consecutive standard sales and files Calder Bank, Kestrel Rise, Pellbury and Abbots Hollow, Pellbury at 6.0 per cent; the step that lands it there is taking the pairing of the same address as the constant quality the methodology asks for, when the developers who bought Pellbury's tired terraces in 2024 and 2025 completed a loft room and a rear extension under building control before selling them on, so those pairs price a larger house at the second sale, and with the pairs whose dwelling had a completion certificate between its two sales set aside Pellbury rose 3.1 per cent.

## Three rules

Task type: seasonal-adjustment-official-time-series-production (Survey Research & Official Statistics), which serves ETL: an official small-area price series conformed from administrative microdata, the price paid record, a postcode directory across a boundary review and a council register in two systems' layouts.
Domain test: the quantity that decides is each ward's constant-quality house price change, the official statistician's repeat-sales index fitted to pairs of sales of the same dwelling; its identifying assumption, that the dwelling is unchanged between its two sales, is what this record breaks in one ward, and the field's index on every pair is the default path.
Swap: put hospitals' bed-days or a utility's megawatt-hours in place of dwellings and there is no pair of sales of one asset, no price paid record, no building control completion and no constant-quality index; the task does not survive the swap.
Layer 1: the price paid record in three files, the last a monthly update whose A, C and D rows add, correct, move and withdraw entries (34 entries registered twice, prices keyed with two digits swapped, postcodes and categories corrected, late 2026 registrations); additional (category B) entries and type O; a postcode directory carrying the 2019 and May 2023 ward codes; the register's two exports (a legacy free-text site address in four layouts, a structured Uniform export with abbreviated streets); a pipeline on the April to March programme year with scheme statuses; dates in three formats. Each comes from the system that keeps it, none is placed to be caught, and every mishandling of it leaves the call (SF5 to SF8).
Layer 2: estimand_identification, the comparison an index promises: a constant-quality price change compares the same dwelling at the same quality, and a pair whose dwelling was enlarged between its sales compares two different goods; choosing the pairs that measure the estimand flips the call.
Decisive step: matching the council's building control completions to the sale addresses and setting aside every sales pair whose dwelling has a completion certificate dated between its two sales, before each ward's index is fitted.
Not semantics: every field, code and definition read correctly still leaves the easy route, because no field records which dwellings changed between sales; the repeat-sales pairing is itself the field's constant-quality device, and the change exists only as a relation between two sales of an address and a certificate in a second system with no shared key.
Not rule application: no filed rule names building work, the register or a pair to set aside, so executing the methodology and the programme rules on every pair files four wards; the enumerated family (the median change; every pair; every pair with a six-month hold, interval weights, a 3-sd trim, new dwellings' first sales out or the 2019 wards; the pairs spanning work set aside, with the work read as every completion, extensions and lofts only, by certificate or application date, matched on postcode and number or on the full address; the same with the update left unapplied) files three answers: the median's four (Abbots Hollow, Calder Bank, Eastholme, Gorsey Hill), every pair's four, and the golden three, the spread between the last two 2.8 points on Pellbury (6.0 against 3.1), and the ruling-out is done by the register alone.
Analyst test: a strong analyst applies the January 2027 update, keeps the standard entries for dwellings, pairs each address's consecutive sales, places them in the May 2023 wards by postcode, fits the methodology's least squares and files Calder Bank, Kestrel Rise, Pellbury and Abbots Hollow, sharing the uplift four ways; every field is read and both documents executed, and the call is wrong because Pellbury's 6.0 per cent carries the developers' loft rooms and extensions.
Estimand: hvha_ward_house_price_index_methodology.pdf sections 1 to 4 with the programme rules: population, standard entries for dwellings in each May 2023 ward; outcome, the change in the price of the same dwelling at the same quality; window, calendar 2025 to calendar 2026 on the record as updated in January 2027; unit, the ward; comparison, more than 5.0 per cent.
No decoy: nothing is planted to be caught; no memo, draft or published figure argues for Pellbury; the developers' purchases and resales are ordinary market entries, their works ordinary building control completions recorded beside every owner's extension, and the official city index is a mix-adjusted series with no ward detail.
No certified replay: no certified or published ward figure ships; the methodology states the estimator, so no reading is recovered by reproducing a published number.
Lesson: a repeat-sales index assumes each pair compares one unchanged asset; a model that gets this right learns to ask whether the assets themselves changed between transactions, and where the record of change lives, before trusting a matched-pair index, which no build on file teaches (task463 chose a drift-free comparison for transaction prices, task482's house price architectures fitted attributes and aggregated a stock, task181 traced a shared resource out of a provider comparison).

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| 0 the median standard price, 2025 against 2026 | none; the methodology rules it out as "the average price of whatever happened to sell" | price, date, postcode | the market report's reflex | the official index is city-wide only | runs it | one group-by | none | readable |
| 1 the methodology's index on every pair | sections 2 and 3 | every column it needs | the field's method | no ward figure ships to refute it | runs it | least squares | none | readable |
| 2 rung 1 with a hold, interval weights, a trim or new dwellings out | none | the dates and prices | a repeat-sales practitioner's filters | none | the trim runs | least squares | none | readable |
| 3 (decisive) the pairs spanning completed building work set aside | none names work, a certificate or the register | no column holds a change; an address join across two systems with no key, dated between two sales | not the index reflex | no file ties a sale to a completion | no battery item | not affine in a shipped column | the register, kept for the supply count | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "the change in the price of the same dwelling at the same quality" | the pairs whose dwelling had building work completed between the sales set aside | every pair of an address's sales | four wards (the default path) | methodology section 1, "at the same quality": an enlarged dwelling is not the same quality; Pellbury 6.0 against 3.1 asserted (C1, SF1) |
| SF2 | which building work | every completion on the dwelling | extensions, lofts and garage conversions only | same call and figures (asserted) | none needed |
| SF3 | when the work happened | the certificate date | the application's received date | same call and figures (asserted) | none needed |
| SF4 | the register's address | house number or name, flat and postcode | postcode and number alone | same call and figures (asserted) | none needed |
| SF5 | the monthly update | applied by transaction identifier | not applied | same call on both routes (asserted) | methodology section 2 |
| SF6 | standard entries | category A | categories A and B | moves the call (portfolio prices) | methodology section 2 |
| SF7 | a new dwelling's first sale | a standard sale | left out | same call (asserted) | methodology section 2 |
| SF8 | the ward | May 2023 boundaries by postcode | 2019 wards | same call (asserted) | methodology section 2 |
| SF9 | the estimator | least squares on year indicators, every pair | interval weights; a six-month hold; a 3-sd trim | same call (asserted) | methodology section 3 |
| SF10 | a pair in one calendar year | drops out | kept | no effect (zero rows) | methodology section 3 |
| SF11 | "more than 5.0 per cent" | the change to one decimal over 5.0 | unrounded | same call (no ward within 0.05) | programme rules section 2 |
| SF12 | shares | nearest pound, summing to the pot | other rounding | the three sum to GBP 12,000,000 (asserted) | programme rules section 3 |
| SF13 | which schemes count | Approved or In contract | with On hold and Bid | moves the shares | programme rules section 3 |
| SF14 | the programme year | 1 April 2027 to 31 March 2028 | calendar 2027 | moves the shares; no scheme on a boundary date (asserted) | programme rules section 3 and the pipeline's About sheet |

## Ladder

| Rung | Construction | Files | Dies to |
|---|---|---|---|
| 0 | each ward's median standard price, 2026 against 2025 | Abbots Hollow, Calder Bank, Eastholme, Gorsey Hill | the methodology's section 1: the average price of whatever sold is not the estimand |
| 1 | the methodology's index on every pair (the field's method) | Calder Bank, Kestrel Rise, Pellbury, Abbots Hollow | Pellbury's 2026 pairs include the developers' resales, each a larger house than at its first sale |
| 2 | rung 1 with a six-month hold, interval weights, a 3-sd trim, new dwellings' first sales out or the 2019 wards | the same four | the resales are ordinary long holds and ordinary residuals; no filter on the sales sees the work |
| 3 (decisive) | the pairs whose dwelling had building work completed between its sales set aside | Calder Bank, Kestrel Rise, Abbots Hollow | the golden |

- **Margins on the cut pack** (asserted in checks.py): on the golden route Abbots Hollow sits 0.8 points over the
  line and Eastholme, the nearest ward under it, 1.1 under; on the default path Pellbury sits 1.0 over, and 0.8
  over at the least across the rung-2 filters.
- **Pricing sequence.** (1) The residue the filed WHAT leaves is the change in the dwellings themselves, a
  reconstruction, not a knob. (2) Pellbury must move from 6.0 to under 5.0, and the pairs spanning work carry about
  3 points of it. (3) The one-group-by routes (median, by type, by year) each file a wrong set. (4) The match is
  exact (every completion's address parses to one dwelling, asserted), so no estimator variance enters. (5) and (6)
  No variance is corrected. (7) No subset of the sales prints the change. (8) The reflex sweep runs as code in
  routes.py and checks.py.
- **No free parameter.** The decisive step has nothing to set: a pair spans a completion or it does not, and every
  reading of the work (every completion or the enlarging ones, certificate or application date, full address or
  postcode and number) files the same figures to the published decimal.

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | standard entries for dwellings in Harrowmere | methodology section 2 |
| 2 Unit of account | the ward, May 2023 boundaries by postcode | methodology section 2 (SF8) |
| 3 Attribution window | calendar years by date of transfer | methodology sections 3 and 4 |
| 4 As-of dating | the record as updated in January 2027 | methodology section 2 and the rules' timetable |
| 5 Version basis | the update's A and C rows stand, D rows withdraw | the update's own Record Status column (SF5) |
| 6 Denominator | none (a ratio of prices) | not applicable |
| 7 Weighting | none, least squares on every kept pair | methodology section 3 (SF9) |
| 8 Window length | one calendar year against the year before | methodology section 4 |
| 9 Boundary inclusivity | more than 5.0 per cent | rules section 2; no ward within 0.05 (SF11) |
| 10 Rounding path | the change to one decimal, the share to the pound | methodology section 4, rules section 3 |
| 11 Tie-break | none needed | no ward at the line |
| 12 Maturity and censoring | 2026 entries registered by 29 January 2027 | the record as updated; same call either way (SF5) |
| 13 Order of operations | update, pair, set aside, fit, compare | C1 under every order of the first three |
| 14 Row order | file order | consecutive sales ordered by date, then identifier |
| 15 Duplicate resolution | an entry registered twice is withdrawn by the update | the update's D rows (SF5) |
| 16 Identity normalisation | an address is PAON, SAON, street and postcode | methodology section 3 (SF4) |
| 17 Netting against gross | none on the call | not applicable |
| 18 Dimensional units | pounds, per cent | the files |
| 19 Code and status semantics | category A and B, types D S T F O, statuses | the files' own values; the pipeline's About sheet |
| 20 Integerisation | shares to the pound summing to the pot | rules section 3 (SF12) |
| 21 Clause scope | "at the same quality" governs every pair | methodology section 1 (SF1) |
| 22 Forward window contents | the 2027-28 starts in the pipeline | rules section 3 (SF13, SF14) |

## Literal reader

Executing the methodology and the programme rules word for word gives each ward's change in the price of the same
dwelling at the same quality from 2025 to 2026, on standard entries for dwellings as updated in January 2027, fitted
by least squares to pairs of each address's consecutive sales; no file records which dwellings changed between their
sales, so every literal reading has to find out, and every reading that matches the council's building control
completions to the sale addresses and sets aside the pairs spanning one files Calder Bank, Kestrel Rise and Abbots
Hollow, while taking the pairing of the address as the quality control (an easy method on the same literal estimand,
not a reading of a sentence) files Pellbury as well.

## Oracles

- The official city index is a mix-adjusted series for the whole city; it ties within its spread on both routes and
  refutes no ward.
- The register's completions confirm nothing about prices on either path.
- The pipeline and the rules fix the shares once the set is known; they tie on both paths.
- none ties only under the golden.

## Ask sheet

Three asks, each a ward table the committee note's supply-and-activity section draws on, each on rows the call never
reads, each with a primary device that only a reconstruction across two files finds. Figures are the generator's
(`generator/figures.json`, `ask_a`, `ask_b_money`, `ask_c`); stops and deltas are asserted in `checks.py` (C8, C9).

**Ask A, each ward's net additional dwellings from building work certified complete in 2026 (12 figures).**
- H18 home: what the city added in housing beside what it did to prices, the request's own reason for the register.
- Files and columns: the register's two sheets (application, certificate, certificate date, work type, dwellings
  created and lost, house number or name, postcode), the price paid files, the postcode directory.
- Primary (D4, absence evidenced in a file no habitual join reaches): an approver's final certificate for a
  conversion reports the dwellings it creates and leaves the dwellings lost blank, and Uniform's one "Conversion"
  type covers houses split into flats and offices or halls turned into flats; a converted building lost a dwelling
  only where the price paid record shows it sold as one, so the loss is read from the other system.
- Hazards: a block's partial completion and its completion certificate carry the same dwellings; demolitions.
- Pin test: the sentence pins the ward, the year, "certified complete" and "net additional dwellings"; the device
  sits in what a blank means for one building, a dimension the pins leave open.

**Ask B, the money paid in each ward's 2026 additional price paid entries for dwellings (12 figures).**
- H18 home: company buyers' and repossessions' weight in each ward's market, beside the index.
- Files and columns: the price paid files and the update (price, date, postcode, type, category).
- Primary (D6, an event's quantity on every line it covers): a portfolio transfer's one price stands on each of its
  titles; the over-cleaning half is a company's same-day purchases of two or three dwellings of one development at
  one list price on separate deeds, which a same-day same-price grouping merges; only a price several times one
  dwelling's price in the ward marks a portfolio.
- Hazards: the update's category changes and late registrations.
- Pin test: the sentence pins the ward, the year, the category and "money paid"; the device sits in which entries
  are one transfer, a dimension the pins leave open.

**Ask C, each ward's affordable homes started on site in 2026 (12 figures).**
- H18 home: delivery so far in each ward, beside the 2027-28 starts the shares use.
- Files and columns: the providers' claims (provider, scheme, site postcode, homes, start, submitted, status), the
  pipeline's About sheet (the merger), the postcode directory.
- Primary (D1, the same records under two key schemes where the copy is not exact): Brackwell Homes claimed its 2026
  sites phase by phase; after its merger into Calderstone on 1 September 2026 Calderstone claimed each site again
  once, for all its homes, dated from the first start, under its own scheme reference; the re-claim matches no single
  earlier claim, only their sum at the postcode.
- Hazards: withdrawn claims for starts that slipped; programme-year quarter labels.
- Pin test: the sentence pins the ward, the year and "started on site"; the device sits in which claims are one
  start, a dimension the pins leave open.

**Main population zero-counts (asserted, C5):** no entry the money ask groups is a standard entry; no supply row
(new dwellings, conversions, demolitions) sets a sales pair aside; the claims file is not read by the call.

| Ask figures | Cracker (lands the call, runs the battery, executes every filed rule) | Mirror (stops at rung 1) | Verdict |
|---|---|---|---|
| A, 12 wards | drops the repeated certificate, reads a blank loss as none: 0 of 12 kept | sums every certificate: 0 of 12 | miss |
| B, 12 wards | counts a same-day same-price group once: 4 of 12 kept | sums every title: 4 of 12 | miss |
| C, 12 wards | drops claims that repeat another's postcode, start and homes: 5 of 12 kept | counts every claim: 3 of 12 | miss |

The full includer (blank losses read from the price paid record, only implausible shared prices grouped, the
re-claims matched to their sites' sums) keeps 36 of 36; it is a stress row, not the gate.

Pair ceiling: 40.7 (the cracker on the call at 58.75, the mirror off it at 22.69, keeping 9 and 7 of 36 ask figures).
Mirror leakage: 19.4 per cent of the ask weight.
Measured by: generator/ceiling.py (run on the cut pack)

## Leak check

`leak.py task468 --asof 2027-02-03`: REVIEW, no LEAK; sweep 11 (the prompt gate) clean. Each REVIEW line ruled here:
- The pipeline's "About" sheet: the Investment Team's own lines on the programme year, the scheme statuses, the
  Brackwell and Calderstone merger and who prepared it; it names no column of any other file. Harmless.
- The methodology (eight stump terms): the terms are the estimand's own words ("constant-quality", "dwelling",
  "address", "postcode") and generic ones ("record", "carries"); it names no building work, completion, register or
  developer. Harmless; the reader's question 1 asks it cold.
- The rents survey, the register and the pipeline name the wards beside numbers: rents, completions and homes, none
  a house price change; nothing ranks the wards on the index. Harmless.
- The pipeline's dates after the setting: planned starts and completions, a pipeline's forward dates by nature.
  Harmless.
- The field guide that first shipped with the price paid files was a dictionary (sweeps 1 and 12): dropped, and the
  files carry the publisher's header row.

## Tried and rejected

- 2026-10-17, at the draw: Urban & Regional Science for a transit seed: none of its task types serves ETL, so the
  pairing cannot be filed.
- 2026-10-17, at the draw: a passenger's average wait from the timetable's gaps (half the mean gap against the
  length-biased mean): generic arithmetic of any periodic service, so the domain reads as a backdrop, and it is not the
  data-integration task type's method (it survives as Ask C's device, which the 10/10 rules leave free).
- 2026-10-17, at the draw: two operators' stops linked across feeds to build combined corridor frequency: the right
  link is read off direction and stop sequence, a field reading, and the guard's identity risk lands on it.
- 2026-10-17, at the draw: delivered frequency from the planned schedule less cancellations cancelled by whole runs:
  needs a dispatch log, and a complete log counts delivered departures exactly, bypassing any estimate.
- 2026-10-17, stage 2: the review as a simple random sample of the unmatched events, its raw route mix the decisive
  step: a single insight the review file signposts (133 v1 died on a development sample pointing at its decisive
  step); the review is now a bus-day sample with one event each, so using it is R2 and weighting it is the move.
- 2026-10-17, stage 2: the composition varying by time band (trunk routes late in the afternoon only, pull-in deadheads
  at night): pooled and band-level shares gave different calls on Route 17, a grain fork (H14); lateness now flat
  through the day and out-of-service movements spread over it, so every stratification agrees.
- 2026-10-17, stage 2: Riverside failing on a four-an-hour timetable: Good Friday's Saturday service pulled its
  timetable average under four too, so the timetable rung landed on the golden; Riverside now runs five an hour and
  its afternoon runs went a quarter short of operators.
- 2026-10-17, stage 2: each candidate's lowest hourly average graded to one decimal: the weighted variants spread up
  to 0.3 on Route 2, so the prompt asks for the verdicts and the workbook carries the figures as supporting detail.
- 2026-10-17, stage 3: on-time shares to one decimal of a per cent: two routes' shares sat within a hundredth of a
  rounding edge, so the shares are graded to the whole per cent (every share further from its edge than one departure
  moves it, asserted); Hillcrest's lateness and timetable jitter moved so its share and its wait sit clear of their edges.
- 2026-10-17, stage 2: a scheduled-departures table from both feeds as an ask: a GTFS-literate cracker executes the
  calendar, calendar_dates and frequencies correctly, so no device held; replaced by the waits (an analytical device).
- 2026-10-17, stage 4: Ask A, Quinnell's April to June record by stop and service-day month: both outside readers
  found the file-head repeats by bus, stop and second and assigned the service days, the judge read the repeats as a
  fork, and no silent device reaches the record without touching the review's frame; dropped (the repeats, the 31
  March copy and the after-midnight service stay as Layer 1 on the call's path, asserted neutral).
- 2026-10-17, stage 4: Ask C, the scheduled wait on 13 May: the prompt's definition made the waiting-time paradox a
  literal integral both readers computed, the frequency window's end read two ways, and no representation of the feed
  hides a departure from a careful reader; dropped (the frequency trips now exact times, each block ending between
  two trips).
- 2026-10-17, stage 4: the on-time device as Quinnell's DeviationSec taken at arrival: both readers timed the
  departures from the timestamps and read the field as noise, and guidance 4.2's "as the AVL system records it"
  invited it; DeviationSec is now the departure against ScheduledDeparture, and the device is Arbor's minute-held
  schedule against the feeds' half minute.
- 2026-10-17, stage 4: Route 6's on-time share at 47.46, 0.04 from its edge (a reader rounding to one decimal first
  filed 48): the half-minute bands, set per transfer point, put every share at least 0.19 from its edge.
- 2026-10-17, stage 4: the eleven candidates named only by route colour in routes.txt (the judge's Gate B and E
  finding): Planning's candidate list now ships with each route's designated stop.
- 2026-10-17, stage 4: the on-time device as Arbor's minute-held schedule against the feeds' half minute: judge pass 2
  read the two schedule sources as an open fork (FIX_NOW), the pin naming the published timetable in guidance 4.1 and
  4.2 closed it, and reader round 3 then timed all eleven shares against the feeds. A device whose basis a filed
  sentence must name dies with the pin, and every other column the ask reads (the departure, the trip tie, the window,
  the days) is the call's own population, so no device on this ask can stay off the call's rows.
- 2026-10-19, repair: the stop-hour grain fork (reader round 3): the review drew 250 bus-days a month, so the
  stop-by-clock-hour cells held one to seven reviewed events and the minimum of thirteen noisy hourly estimates sat
  biased low; at 400 bus-days a month, with the within-bus-day draw on its own stream, every weighted grain (stop, stop
  and hour, band, month, vendor, the within-bus-day weight, counting-day reviews) files the golden and every raw grain
  the R2 slate (checks.py R3b, verify.py's stop-hour estimator).
- 2026-10-19, repair: replacing the dead on-time ask, measures tried on paper and dropped: the average scheduled wait
  (computed exactly from the feeds by any GTFS-literate solver, and "a weekday of current service" splits on the class
  days); missed trips from a dispatch log (it would hand every solver each route's delivered departures, the call's own
  quantity); APC boardings at the designated stops (doors open only in service, which would identify the out-of-service
  passes the review estimates); the fleet roster's asset tags moved between buses (it would move the review's bus-day
  join on the call's path); evening and Saturday counts (Quinnell's repeats and the cutover overlap are seen, not
  silent). The shelter ask takes none of the call's rows.
- 2026-10-19, architecture 1 spent (the transit nominations): four isolated readers landed the call, so the review
  weighted by its design was read off the memo's sampling procedure by every careful solver (Gate F, score_reader exit
  1), and judge pass 3 found the shelter ask NOT_DETERMINISTIC (no file states the moved-stop rule, and stating it
  hands over the device). The author chose to re-root.
- 2026-10-19, architecture 2 spent at stage 4 (the specialty pharmacists by months on therapy): the isolated reader
  projected the caseload by tenure since first fill from past month ends, its first move once it saw the program year
  unobserved, and landed the call (10 of 10) and 27 of 28 ask figures (score_reader exit 1); the bulletin's step-therapy
  sentence and the caseloads' 2026 starters made the duration mix visible, and the rebate statement's repeated
  product-quarter amount was caught on sight. A forward window over a record that shows the process invites the
  conditional development; the next architecture needs a decisive step the record does not display.
- 2026-10-19, architecture 3 drawn: the same world, the decisive step moved to the clock. Members who stopped a drug
  and came back after a lapse restart its persistence curve, so the development is indexed by months in the current
  episode; v2's first-fill development is now the analyst test's wrong answer (57 against 54). Tried first: a wave of
  returners 30 per cent of the step-therapy classes' past stoppers (GLP 177 of 1,809 back, first-fill clock only half
  a pharmacist off), raised to 60 per cent; a separation by back-test (both clocks pass the earlier Junes alike,
  returns being rare before 2026), replaced by the record's own comparison of returners with continuing members and
  new starters. The rebate statement's repeated product-quarter amount (caught on sight by v2's reader) kept as a
  hazard; the primary moved to the contract year's February start.
- 2026-10-19, architecture 3 spent at stage 4 (the specialty pharmacists by months in the current episode): the
  isolated reader built persistence by time since episode start, an episode broken by a gap of more than 100 days,
  because the refill gaps were a few days and the returns months, and landed the call (10 of 10; score_reader exit 1).
  A clock the gap distribution displays is not silent; architecture 4 is drawn fresh.
- 2026-10-20, the three architectures read together (the author's rule: no retirement, so a fresh architecture 4
  follows): architecture 1 fell to readers who read the review's weighting off the memo; architecture 2 (judged
  DETERMINISTIC and APPROVE) to a reader whose first move on an unobserved window was the tenure-conditioned
  projection; architecture 3 to a reader who read the episodes off the bimodal refill gaps. A forward window over a
  record that displays the process invites the careful reader's persistence model, and every clock the record shows
  plainly is a reflex at medium effort: the next architecture needs a decisive step the record does not display.
- 2026-10-20, architecture 4 calibration: the pooled rate by the link's pass was first the only stratification other
  than the class that the hospitals' mixes separated; hospital-by-pass rates also landed the golden set while each
  hospital's members without a number were mostly one surname type, and stopped doing so once Varden's members
  without a number became low-risk workers whose recorded deaths include none without a number, so its own rates
  borrow the pass's (R4c). Kept: the class is what drives the error, and a hospital's own rates are not identified
  where its controls are empty.
- 2026-10-20, architecture 4 build: dropping Carrisford's encounters moved Tamsin General (1.05) over the line on a third
  fewer admissions, so Layer 1 was not neutral; Tamsin General now sits at 0.93 and Calloway at 1.32, and every Layer 1
  mishandling leaves the five (SF1, SF6, SF7).
- 2026-10-20, architecture 4 build: a two-part surname read from a hyphen only puts most two-part surnames with the
  single ones and adds Varden; dropped from the fork table as no reading of the enrollment file (88 per cent of two-part
  surnames are written with a space), while a space-only reading files the five (SF8b).
- 2026-10-20, architecture 4 asks: interim bills carrying a stay's payment to date (a summed interim history double
  counts) and newborns billed under the mother's identifier (a stay-key deduplication drops them) were drafted for the
  bonus ask and dropped: the first is not how a plan's paid column behaves, the second reaches only the hospitals with
  deliveries, so no device moved all fifteen figures. The platform conversion's conventions move all fifteen and live
  in a column the call never reads.
- 2026-10-20, architecture 4 ask device: the CPS and platform replacement conventions, left unfiled, were the primary.
  Reader round 1 (on b1bc148c) read them off the amounts (CPS replacements centred on zero, 63 per cent negative, none
  on the platform) and confirmed them on hospital totals landing within a few dollars of round bonus figures, 15 of 15
  (score_reader exit 1), and the judge's first pass required the convention filed (inferable, not filed). A convention is
  a fork, not a device: filed in the extract notes, it is a hazard, and the device moved to the dispute log's awards
  that a reprocessed bill already carries. The base rates that had centred every bonus in its cell were retuned so each
  sits 15 to 35 dollars off centre.
- 2026-10-20, architecture 4 estimator: seven hospital classes with no links among the admissions no control reaches
  gave estimates below zero, which the golden floored and step 6 did not, so the judge's unfloored recompute differed
  at the first decimal (Calloway 189.5 against 189.8 deaths, Varden 24.3 against 24.5, Fairhaven 1.05 against 1.06).
  Filing a floor would be rule application on the decisive step; instead each such class now carries the links its
  false-link share expects (one more of its members found by the Office), so floored and unfloored agree (C1, C1b). The
  call is unchanged; Varden moves to 1.03 and Fairhaven to 1.09.
- 2026-10-31, architecture 4 retired at the batch audit (re-rooted, not repaired): it fell short of the survivor
  anatomy on the Reflex. Its golden was the field's own linkage-error correction (each class's false-link and
  missed-link rates applied to the Office's matches), so the field's named method sat at the top of the ladder,
  where a reader who knows record linkage applies it as a first move, and the Office's shipped match file was the key
  the link rode on; architecture 5 is drawn fresh in another client domain.
- 2026-10-31, architecture 5 draw: a constant-quality house price designation on hedonic attributes or a stock
  aggregation is spent (task482 architectures 4 and 5, both landed by readers who fitted the handbook's model); the
  draw keeps the field's repeat-sales index at rung 1 and moves the decisive step to the identifying assumption no
  sales file shows, the dwelling unchanged between its sales.
- 2026-10-31, architecture 5 stage 2: the developers' works at four to five residual standard deviations on a
  noise-only price model: a 3-sd residual trim on every pair dropped them and landed the golden set without the
  register; each dwelling now drifts about its ward's path (a spread growing with the holding period, as repeat-sales
  records show) and the works add 14 to 23 per cent, so no filter on the sales sees them (SF9).
- 2026-10-31, architecture 5 stage 2: owner works of every kind in the register, structural alterations among them:
  a reading that counts only enlarging work moved Kestrel Rise's published change by 0.2, a fork at the graded
  decimal; owners' works are now extensions, lofts and garage conversions, and every reading of "building work"
  files the same figures (SF2).
- 2026-10-31, architecture 5 stage 2: June 2021 postcode recodes split pairs across the recode and moved two wards'
  figures at the decimal between the literal address and a linked reading: dropped (SF4b).
- 2026-10-31, architecture 5 stage 2: a block of flats certified at its last flat's date let a flat's first sale
  precede its block's certificate, so a postcode-and-number match set aside pairs the full address kept (Calder Bank
  8.0 against 8.1): each block is now certified complete on one date (SF4).
- 2026-10-31, architecture 5 asks: the register's ward column holding the 2019 wards (a label stored before the
  boundary review) as Ask A's primary: an asking sentence naming the May 2023 wards kills it, and without one the
  register's own column is a literal reading of "ward", a fork; the column now carries the current wards and the
  primary is the approver's blank loss.
- 2026-10-31, architecture 5 asks: Ask B as a count of additional entries: every handling of the update reproduces
  the count (the battery's latest-version rule), so the count carried no device; the ask is the money paid.
- 2026-10-31, architecture 5 asks: Ask C's re-claims as one-to-one repeats of Brackwell's claims (postcode, start and
  homes): the battery's re-keyed-record match finds them; Brackwell now claims its sites phase by phase and
  Calderstone each site once, so a re-claim equals only the phases' sum.
- 2026-10-31, architecture 5 shock: Pellbury's 2024 and 2025 company purchases made it the largest count of
  additional entries in those years; the city-centre and student-let wards now carry their own company buying, and
  Pellbury sits second of the twelve.
- 2026-10-31, architecture 5 leak screen: the price paid field guide (a PDF listing every column) is a dictionary
  under leak sweep 1 and 12; dropped, and the price paid files carry the publisher's header row instead.
