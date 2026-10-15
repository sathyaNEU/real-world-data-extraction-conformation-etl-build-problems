# task455 design note

Architecture 2 (re-root, drawn 2026-10-15). Architecture 1 (the coroner's certificates corrected by the medical
examiner's error matrix) is in the card's lineage and the last line of `## Tried and rejected`.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task455.json`, architecture v2, registered 2026-10-15. Guard WARN only:
  three_rules.strategy_risk (identity_resolution; answered by the analyst test, which files the wrong counties with every
  field and rule read correctly), overuse.org_family (government_agency) and overuse.objective (the slot is in the author's
  ETL lane). test.same_driver_older is differentiated against task82 v2 on the card.
- **Pairing:** Survey Research & Official Statistics / census-register-administrative-data-quality / ETL, own pattern
  establishment continuity from worker flows. Business demography counts enterprises, while the state's unemployment
  insurance (UI) program counts employer accounts: a business that changes its legal form, is bought or reorganises opens a
  new account, and official business statistics separate a birth from a continuing business by the continuity of its
  production factors, above all its workforce. The Lornock Valley's seven counties are ranked on their 2026 establishment
  birth rates, and the state Commerce Department designates the top three as Formation Counties for its 2027 to 2029
  grants.
- **Why this task type:** the six ETL-serving task types are all in recent use; register quality is the one whose own
  subject is the gap between an administrative unit (the employer account) and the statistical unit (the establishment),
  and none of its builds on file (task448's capture by route, task457's disclosure timing, task455 v1's certificate
  misclassification) touches unit continuity.
- **Shape:** 01, a ranked list under a cap. Arithmetic: the designated three and the runner-up with its gap (3); each of
  the seven counties' 2026 births and birth rate (14); the count of new accounts set aside as continuing businesses in each
  county (7): 24 before the asks; the asks add the 2025 births, deaths and their rates (28) and a chart (about 4).
- **Strategy:** identity_resolution (G3 record versus operation decisive, G10 cross-dimensional duplication behind it).
  New UI accounts first employing in 2026 are the obvious births. The employer register records a predecessor only when
  the new employer applies to take over the predecessor's experience rating, which a buyer of a business with a high tax
  rate does not do and a business re-incorporating as it moves does not report; a shared address marks the take-overs that
  stayed put but not the businesses that moved, and also marks every new business that opened in a closed one's premises.
  Only the wage records show a continuing business: more than half of its first-quarter workers were paid the quarter
  before by one account that then stopped reporting. Counted that way, the county lifted by an acquired chain's
  re-registered stores and the county lifted by an enterprise park's relocations both leave the top three, and the
  county with the most re-let storefronts keeps its births.
- **World:** an unnamed state's Lornock Valley region (invented), seven counties (Brennock, Caldmere, Dunrath, Eskwell,
  Fennamore, Quarrin, Tolbeck), about 7,000 private establishments and 60,000 private jobs. Events of 2026 the data
  carries without naming: a fuel and convenience operator bought nineteen Caldmere stores at the start of the second
  quarter and re-registered each under a new account; Tolbeck's new enterprise park drew twenty-one businesses from the
  other counties, each re-registered as a Tolbeck entity; Quarrin's downtown storefront program filled twenty-four
  storefronts vacated in 2025 and early 2026 with new businesses. Background: take-overs with and without a filed
  transfer in every county, summer employers in the lake and recreation trades, closures with final pay in the next
  quarter, and the UI tax system's move from ZIP-based to geocoded county codes with the third-quarter 2025 reports.
- **Files:** `ui_employer_register_extract_2027-05-14.csv` (accounts, legal and trade names, FEIN, worksite address,
  geocoded county, industry code and vintage, registration and liability dates, status and inactivation date,
  predecessor account and transfer date); `qcew_private_establishments_2024q4_2026q4.csv` (the spine: account and quarter,
  county as assigned, industry, monthly employment, total and taxable wages; about 60,000 rows);
  `ui_wage_records_2024q4_2026q4.txt` (pipe-delimited, protected worker key, account, quarter, wages; about 650,000
  rows); `formation_counties_program_guideline_2027.pdf` (the Commerce Department's guideline: designation rule, birth
  definition, base, county, data); `lmi_research_extract_dictionary.xlsx`; `extract_manifest_2027-05-14.csv`;
  `lornock_county_codes.csv`; distractors: `lornock_county_population_estimates_2020_2026.csv`,
  `sos_new_entity_filings_2025_2026.csv` and `formation_grant_disbursements_fy2026.xlsx`.
- **Forcing fact:** the legislature's 2027 to 2029 appropriation requires the designation by 30 June 2027; the extract
  is dated 14 May 2027, after the 2026 fourth-quarter reports were due on 30 April. The measure is a closed year because
  the guideline designates on the latest full year; the call (which counties receive 2027 to 2029 grants) faces forward.
- **Forum and forcing event:** minister_or_cabinet (the Commerce Secretary designates), budget_or_appropriation.
  Organisation government_agency; role research_desk (the LMI bureau's business dynamics economist). Personas from
  `guard.py names --geo "United States" --seed 3455` and `--seed 2455`: Kristy Townsend (the economist), Brandon Compton
  (the Commerce Department's program director), Chelsey Hensley (the UI tax unit's employer accounts supervisor).
- **Data-native sentence:** in the UI program an employer that buys, moves or reorganises a business gets a new account
  and inherits the predecessor's tax rate only if it applies for it, so the register records the continuity of the
  applicants alone and the address only of those that stayed put, while the wage records show every continuing
  business's staff paid as a block the quarter before by an account that then stopped reporting, and a new business in
  a closed one's premises hiring mostly its own.
- **Sources, one line each:**
  - `stumping/references/client/measured-drivers.md`, the held group: the decisive step defines the unit (an
    establishment birth, not an account opening) upstream of every graded figure; traps 2 (counts file rows, not the real
    unit) and 18 (joins only on the visible key) have held tasks behind them.
  - `stumping/references/client/two-layer-task-design.md`, field_method: business demography's continuity rules, the
    field's own construction of a statistical unit from administrative records.
  - `dataset-generation/references/layer1-messiness.md`: employer register keys, address formats, two NAICS vintages, late
    quarterly reports, workers on two accounts in a quarter; none on the decisive step.
- **Same-puzzle and abstraction:** gap population, generators G3 and G10, Gate G etl_conformance, decision
  ranked_slate_under_cap. Nearest drivers on file 0.05 to 0.06 (task87, task98, task58, task127); none decides whether a
  new identifier is a new unit from the members who move with it.

## Default path

1. Read `ui_employer_register_extract_2027-05-14.csv` and `qcew_private_establishments_2024q4_2026q4.csv`; take each
   account's county from its rows.
2. A new account is one whose first month with employment falls in 2026 (no employment reported from October 2024 to
   December 2025).
3. Set aside the new accounts the register records with a predecessor (the filed successorships).
4. Divide each county's remaining new accounts by its private establishments that reported employment in the fourth
   quarter of 2025 (the guideline's base) and rank.
5. Designate the top three.
- Ends on: Caldmere, Eskwell and Tolbeck (built: Eskwell 11.99, Caldmere 11.11 and Tolbeck 10.78 per 100, above
  Dunrath's 10.19 and Quarrin's 9.85).
- Golden: Dunrath, Eskwell and Quarrin (built: Eskwell 11.33, Dunrath 9.79 and Quarrin 9.50 per 100; the runner-up
  Caldmere 7.83, the gap 1.67, shown 1.7).

## Stump sentence

The default path counts each county's new employer accounts first employing in 2026, net of the predecessors the
register records, and designates Caldmere, Eskwell and Tolbeck (Ends on: Caldmere at about 11.1 and Tolbeck at about
10.8 per 100), because a fuel and convenience operator bought nineteen Caldmere stores and re-registered each under a
new account without applying for the seller's rate, and twenty-one businesses moved into Tolbeck's new enterprise park
under new accounts without a filed transfer; matching addresses catches the stores but not the moves, and also removes
Quarrin's new businesses in vacated storefronts (Dunrath, Eskwell and Tolbeck). Counted by whether most of a new
account's first-quarter workers were paid the quarter before by one account that then stopped reporting, Caldmere falls
to 7.8, Tolbeck to 7.2, Quarrin keeps its storefront births at 9.5, and the designation is Dunrath, Eskwell and
Quarrin.

## Three rules

- Task type: Survey Research & Official Statistics, census-register-administrative-data-quality (administrative employer
  accounts conformed into the statistical units official business demography counts), which serves ETL.
- Domain test: the deciding quantity is each county's 2026 establishment birth rate as business demography measures it,
  a new establishment and not a continuing business under a new employer account, built by the employment-flow continuity
  test official business statistics use (most of a new account's first workforce paid the quarter before by one account
  that then stopped reporting).
- Swap: with hospital nouns ("which three counties' hospitals opened the most new wards") there is no employer account a
  business re-registers under after a sale or a move and no workforce that moves with it as a block, so the task stops
  reading the same.
- Layer 1: the employer register (account keys, legal and trade names, worksite addresses in two formats from the 2025
  system change, two NAICS vintages, status, liability and registration dates, the predecessor field), the quarterly
  reports (monthly employment on the 12th against quarterly wages, county codes assigned from the ZIP code before the
  third quarter of 2025, zero reports from open accounts, final pay after a closure), the wage records (protected worker
  keys, a worker on two accounts in a quarter): each produced by the UI tax and wage systems, none placed to be caught.
- Layer 2: field_method; the decisive choice is the unit counted (an establishment, not an account opening) and the
  evidence that settles a new account's continuity, the movement of its workforce.
- Decisive step: a new account is a continuing business when more than half of the workers it paid in its first quarter
  were paid the quarter before by one account that then stopped reporting employment; neither the filed predecessor, a
  shared address, a similar name nor an attribute match decides it.
- Not semantics: every field read correctly (the predecessor field, the addresses, names, industry codes, dates) still
  leaves the unfiled sales and relocations among the births and the storefront re-lets with the continuations; nothing in
  any field marks either.
- Not rule application: the guideline defines a birth as a business that did not operate before under another employer
  account and names the events (a sale, a reorganisation, a change of legal form) without saying how continuity shows;
  executing it through the register's predecessor field, an address match or a name match designates the wrong counties.
- Analyst test: a strong analyst counts each county's new accounts first employing in 2026, nets off the register's
  predecessors and designates Caldmere, Eskwell and Tolbeck (the default path's Ends on, Caldmere at about 11.1 per 100);
  the more careful one also sets
  aside new accounts at the address of an account that closed and designates Dunrath, Eskwell and Tolbeck.
- Estimand: the program guideline (`formation_counties_program_guideline_2027.pdf`) fixes the population (private
  establishments, counted in the county in which the worksite lies), the outcome (births in 2026: an establishment first
  reporting employment in 2026 whose business did not operate before under another employer account), the base (private
  establishments reporting employment in at least one month of the fourth quarter of 2025), the unit (the establishment)
  and the comparison (the three highest rates, compared unrounded).
- No decoy: no memo, draft, briefing or published figure carries a ranking or a birth count; the register's predecessor
  field is the UI program's own record of approved transfers, true where it is filled, and its dictionary entry says it
  is filled only on an application.
- No certified replay: no published or certified birth count ships, so nothing is recovered by reproducing figures.
- Lesson: a model learns that an administrative identifier opening is not a statistical unit's birth, and that the
  continuity an official count needs is read from the flow of the unit's members across identifiers, not from a filed
  link, a shared location or a similar name; no build on file decides a unit's novelty from member flows.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 new accounts net of the register's predecessors (default path) | the guideline's "did not operate before under another employer account" and the predecessor field's entry send the solver to the field | `predecessor_account` is a column: a row predicate | netting the register's successorships is the first reflex | none | none | one filter | readable |
| R1 new accounts at the address of an account that closed set aside | the dictionary's "an employer that takes over a business without applying has no predecessor recorded" sends the solver looking for unfiled take-overs | the worksite address is a column; a self-join on it after normalising two address formats | address matching is the record-linkage reflex | none | none | one join | readable |
| R2 attribute linkage (address or similar name, same industry, the old account stopping the quarter before, similar size) | none | names, NAICS codes and monthly employment are columns | probabilistic record linkage on visible attributes is the strong analyst's reflex | none | none | a scored join | readable |
| R3 (decisive) workforce continuity | none: no sentence names the workforce, a share, a quarter or a flow | no column links a new account to the account its workers came from; the link is built from about 650,000 wage rows by worker, quarter and account | not a reflex: every attribute linkage leaves Tolbeck's relocated businesses among the births, and an any-overlap test removes Quarrin's storefront births with the take-overs | none: no control or published count confirms a continuity | none: the battery finds nothing wrong with the netted counts | a per-account share over a grouped self-join of the wage file | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | first reported employment | the first month with monthly employment above zero | the first quarter with wages | same call | guideline 3.3 "first reported employment"; no 2026 new account has wages before its first month with employment across the year boundary, same counts (asserted) |
| SF2 | first reported employment | the quarterly reports | the register's liability date in 2026 | same call | same accounts and counts (asserted) |
| SF3 | first reported employment | the quarterly reports | the register's registration date in 2026 | same call | guideline 3.3 (a registration is not employment); every 2026 new account opened in 2026, same counts (asserted) |
| SF4 | new account | no employment in any month from October 2024 to December 2025 | no report of any kind before 2026 | same call | no 2026 new account filed a report before 2026 (asserted) |
| SF5 | base | reported employment in at least one month of 2025Q4 | December 2025 employment only | Dunrath, Eskwell and Quarrin; counts differ | guideline 3.4 "in at least one month of the fourth quarter of 2025"; same call either way (asserted) |
| SF6 | base | monthly employment | wages in the quarter | same call | guideline 3.4 "reported employment"; same call (asserted) |
| SF7 | county | the county in which the worksite lies (register; quarterly rows from 2025Q3) | the quarterly row's code | same call | guideline 3.2; every row the call reads is from 2025Q4 or later, where the codes agree (asserted) |
| SF8 | private | ownership code 5 | none | same call | the extract carries private accounts only |
| SF9 | did not operate before under another account | not a filed successor and not a workforce continuation | a filed successor whose workforce did not move | same call | every filed successor's workforce moved with it (asserted) |
| SF10 | more than half | over 50 per cent of the first-quarter workers from one account | 60, 70 or 80 per cent | same call, same counts | continuations at 80 per cent or more, births at 40 per cent or less (asserted) |
| SF11 | an account that then stopped reporting | no employment in the new account's first quarter or later | dropped (most workers from one account, whatever it did after) | same call, same counts | no birth draws over 40 per cent of its first workers from any one account (asserted) |
| SF12 | workers of the first quarter | paid in the first quarter with employment | on the payroll on the 12th of a month of that quarter | same call, same counts | continuations change hands at a quarter's start (asserted) |
| SF13 | paid the quarter before | the quarter before the first quarter | any earlier quarter (the worker's last prior account) | same call, same counts | asserted |
| SF14 | continuity, two-sided | the new account's share | also more than half of the old account's workers moving | same call, same counts | every continuation carries at least 70 per cent of the old account's workers; no birth takes over 40 per cent of an account's workers (asserted) |
| SF15 | rates compared | unrounded | rounded to one decimal | same call | guideline 4.2 "compared unrounded"; no tie at one decimal (asserted) |
| SF16 | births of 2026 that changed hands within 2026 | the first account stays a birth, its successor a continuation | both births | same call | guideline 3.3; asserted |

## Ladder

Built magnitudes (rates per 100 establishments reporting employment in 2025Q4; `checks.py` asserts each rung by name).

| Rung | Reading | Files | Dies to |
|---|---|---|---|
| 0 | new accounts first employing in 2026, net of the register's predecessors (default path) | Caldmere, Eskwell and Tolbeck (Eskwell 11.99, Caldmere 11.11, Tolbeck 10.78; Dunrath 10.19, Quarrin 9.85) | Caldmere's nineteen re-registered stores and Tolbeck's twenty-one relocations have no predecessor recorded, and their first-quarter workers are the closed accounts' staff |
| 1 | also set aside new accounts at the worksite address of an account that stopped reporting (146 matched) | Dunrath, Eskwell and Tolbeck (Eskwell 11.07, Tolbeck 10.46, Dunrath 9.55; Caldmere 7.55, Quarrin 6.72) | Quarrin's twenty-four storefront re-lets are new businesses (a different storefront trade the quarter after, or a vacancy of two quarters or more; a new owner and name; mostly new workers) and Tolbeck's relocations moved address |
| 2 | attribute linkage: address or similar name, same industry, the old account's last quarter the one before, similar size | Eskwell, Quarrin and Tolbeck in the same county (Tolbeck 10.13); Dunrath, Eskwell and Tolbeck across counties or with the address (Tolbeck 7.84) | the stores and most relocations re-registered under their own self-reported industry codes and new names, and a nearby closure's attributes fit many births |
| 3 | workforce continuity: more than half of the first-quarter workers paid the quarter before by one account that then stopped reporting (golden) | Dunrath, Eskwell and Quarrin (Eskwell 11.33, Dunrath 9.79, Quarrin 9.50; Caldmere 7.83, Tolbeck 7.19) | stands |

- Other reflexes, each landing a named wrong set (asserted): every new account counted (Caldmere, Eskwell and Tolbeck);
  a trade-name match (Caldmere, Eskwell and Tolbeck: the stores were rebranded, most relocations renamed); the address
  match restricted to the same industry and the quarter before (Dunrath, Eskwell and Tolbeck); the address match or a
  name match (Dunrath, Eskwell and Tolbeck); the address match joined with the workforce test (Caldmere, Dunrath and
  Eskwell: the re-lets go); any worker paid the quarter before by an account that then stopped reporting (171 set aside,
  32 of them in Quarrin, whose storefront births hire some of the closed shops' staff: Caldmere, Dunrath and Eskwell).
- Winners and margins: golden third over fourth 9.50 against 7.83, 1.213x; runner-up over the fifth by 0.65; rung 1
  third over fourth 1.265x; rung 0 Caldmere over Quarrin 1.128x keeps every rung-0 variant off the golden; Tolbeck
  under the address and attribute rungs (10.46, 10.62, 10.13) stays above Quarrin's golden 9.50.
- Variants of the golden that converge (asserted): thresholds of 50 to 80 per cent (births draw at most 33 per cent
  of their first workers from one account, continuations at least 85 per cent); without the stopped-reporting
  condition; two-sided (every continuation carries at least 83 per cent of its old account's workers); the worker's
  last account in any earlier quarter; a worker on two accounts counted at the higher-paying one.
- Position and dominance: Quarrin is fifth on rung 0 and sixth on rung 1; the decisive move is the only correction
  that lowers Tolbeck and restores Quarrin; it moves three counties' births by 19 to 24.
- Grid: a Layer 1 slip (December employment or wages for the base, registration dates, zero reports read as
  operating) with rung 0 or 1 never files Dunrath, Eskwell and Quarrin (the slips keep the call under the golden,
  asserted; the rungs move it).
- Worth: rung 0 moves the call and three counties' births, set-aside counts and rates; rung 1 moves the call and
  Quarrin's and Tolbeck's figures.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | private establishments in the seven counties; births among accounts first reporting employment in 2026 | guideline 3.1 to 3.3; C1 for the extract's coverage (private accounts only, SF8) |
| 2 | Unit of account | the establishment (one worksite per account in the region) | guideline 3.1; no account reports two worksites (asserted) |
| 3 | Attribution window | births with a first month of employment in January to December 2026 | guideline 3.3; no continuation or birth straddles the year boundary on wages (SF1) |
| 4 | As-of dating | the reports held at the extract of 14 May 2027, after the 2026 fourth-quarter due date | guideline 5.1; every 2026 new account's reports through 2026Q4 are in the extract (asserted) |
| 5 | Version basis | the quarterly report as held (amendments replace) | one row per account and quarter (asserted) |
| 6 | Denominator | establishments reporting employment in at least one month of 2025Q4 | guideline 3.4 (SF5, SF6) |
| 7 | Weighting | none: counts and a ratio | the guideline's rate |
| 8 | Window length | the year's four quarters; continuity read over one quarter | SF13 converges |
| 9 | Boundary inclusivity | more than half | C1: no share between 40 and 80 per cent (SF10) |
| 10 | Rounding path | rates compared unrounded, shown to one decimal; the gap from unrounded rates | guideline 4.2; the prompt's rounding sentence; no figure within 0.01 of a rounding edge (asserted) |
| 11 | Tie-break | none needed | no tie (asserted) |
| 12 | Maturity and censoring | births late in 2026 observed for one quarter; continuity needs only the first quarter | C1 |
| 13 | Order of operations | conform, find new accounts, set aside continuations, divide | C1 (set operations commute) |
| 14 | Row order | none matters | C1 |
| 15 | Duplicate resolution | none: one row per account and quarter, one wage row per worker, account and quarter | asserted |
| 16 | Identity normalisation | accounts by account number; workers by the protected key | dictionary; SF9 to SF14 |
| 17 | Netting against gross | births and continuations are disjoint sets of new accounts | C1 |
| 18 | Dimensional units | establishments, workers | the files |
| 19 | Code and status semantics | ownership, status, predecessor and county codes | dictionary; SF7, SF8; same call |
| 20 | Integerisation | counts whole | C1 |
| 21 | Clause scope | the guideline's definitions apply to each county separately | guideline 2.1 |
| 22 | Forward window contents | none: the designation reads the closed year 2026 | retrospective by the guideline's rule (the latest full year), the call (grants for 2027 to 2029) faces forward |

## Literal reader

Executed word for word, the guideline counts in each county the establishments that first reported employment in 2026
and whose business did not operate before under another employer account, a business sold, reorganised or changed in
legal form and going on under a new account not being a birth; it names no evidence for continuity. The register's
predecessor field is, by its dictionary entry, the record of approved transfer applications and holds no take-over
whose buyer did not apply, so a literal reader cannot take it as the set of continuations. The pack shows continuity in
one place: the wage records, where a continuing business's first-quarter workers were paid together the quarter before
by an account that then stopped reporting (80 per cent or more of them in every case), while a birth draws 40 per cent
or less from any one account; every threshold, quarter and two-sided reading between those values selects the same
accounts. An address match is not another reading of a term: it is evidence the data refutes, since Quarrin's matched
storefronts are a different industry or followed a vacancy of two quarters or more, carry a new owner and name and hire
mostly new workers, and Tolbeck's relocated businesses share no address with the accounts they continue.

## Oracles

None. No control, published figure or reconciliation column confirms any rung: the extract manifest gives row counts per
file; the county population estimates, the Secretary of State's entity filings and the program's grant disbursements
carry no establishment or birth counts; the register's predecessor field confirms the filed successorships on every rung
alike.

## Ask sheet

- **Ask A, 2025 births by county:** each county's 2025 births and its 2025 birth rate per 100 private establishments
  reporting employment in the fourth quarter of 2024 (fourteen figures, counts whole, rates to one decimal). H18 home: a
  measure every county carries that the call does not turn on (the prior year the Secretary's announcement compares).
  Construction: the guideline's birth definition on 2025, continuity by workforce (2025 take-overs in every county). Primary
  device: D5, out-of-scope rows known only by structure: the valley's summer employers (lake and recreation trades) and
  a few paused contractors report employment only from May, so on the extract's single 2024 quarter they show none and
  look new in 2025; the register's liability date carries their first payroll years back (about 100 accounts, every county).
  Hazards: H1 the county coding (below); H2 the 2025 take-overs (construction). Path: the quarterly reports, the register,
  the wage records, the guideline, the dictionary, the county codes and the manifest (seven files, eleven columns). Stops
  (built, every figure asserted outside its bin): the extract's window with the quarterly rows' county (the cracker's
  path), births 134, 64, 123, 98, 96, 83 and 53 against 118, 52, 104, 77, 81, 63 and 47 (Brennock to Tolbeck), every rate
  off; the window alone, every count high by 10 to 23; the liability test with the quarterly rows' county, every count off
  by 1 to 3 and every rate off by 0.2 to 0.7; no workforce test (the mirror), every count high; the golden. Realism:
  summer employers file zero reports from October to April and their liability dates are their first payrolls.
- **Ask B, 2025 deaths by county:** each county's 2025 deaths (an establishment whose last month with employment fell in
  2025, that reported none in 2026 and whose business did not go on under another account) and its death rate on the
  same base (fourteen figures). H18 home: the other side of the year's business dynamics, beside the births. Construction:
  the accounts whose staff moved as a block to a new account in 2025 or January 2026 are not deaths. Primary device: D2, a
  label stored before a silent switch: the UI tax system assigned each worksite's county from its ZIP code until geocoding
  took effect with the third-quarter 2025 reports, so the earlier quarterly rows of the worksites in the minority part of
  the ZIP codes that cross a county line carry the neighbouring county; the base and every death before July 2025 read
  from those rows move (the register's county is the geocoded one). Hazards: H3 final pay in the first quarter of 2026
  after a December closure (a wage reading keeps them open); H4 accounts left open and filing zero reports (a status
  reading misses them); H5 inactivation dates processed months after the last payroll (an inactivation-year reading moves
  them). Path: the quarterly reports, the register, the wage records, the dictionary, the county codes, the guideline and
  the manifest (seven files, ten columns). Stops (built, every figure asserted outside its bin): the quarterly rows'
  county (the cracker's path), deaths 112, 58, 93, 55, 86, 100 and 45 against 115, 56, 91, 57, 84, 98 and 48, every rate
  off by 0.3 to 0.7; filed transfers only (the mirror), every count high by 1 to 16; wages for employment, every count
  low by 2 to 7; the golden. Realism: county geocoding projects replace ZIP-based assignment on a stated quarter, and
  border ZIPs are common in a rural valley.
- **The chart:** each county's 2025 births and deaths as paired bars; its values are Ask A's and Ask B's counts.
- **Main population zero-counts (asserted):** no 2026 new account and no establishment in the 2025 fourth-quarter base
  is a summer employer resuming or a dormant account; every quarterly row the call reads (2025Q4 and 2026) carries the
  geocoded county; no 2026 new account straddles the year boundary on wages, registration or liability dates.
- **Hazard table (built):** H1 (the county coding) moves every Ask A and Ask B rate and every count by 1 to 3; H2 (the
  2025 take-overs) moves every Ask A count and, as their sources, every Ask B count; H3, H4 and H5 move Ask B's counts
  for a response reading wages, status or inactivation dates instead of employment.
- **Referee:** none needed; no control ties only under the golden.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule) | Verdict |
|---|---|---|
| A, 2025 births and rates | takes new accounts by the extract's window and the quarterly rows' county: every county's births high by the summer employers, every rate off | miss |
| B, 2025 deaths and rates | takes each death's and each base establishment's county from its quarterly row: every rate off, several counts off | miss |

- Mirror leakage: about 5 per cent of ask weight (a response on rung 0 counts the 2025 take-overs as births and their
  sources as deaths in every county; it keeps the chart's layout criteria only).
- Pair ceiling: 31 (cracker 38 + 7 + 55 x 0.05 = 47.8; mirror 5 + 7 + 55 x 0.05 = 14.8; average 31.3), rerun from the
  generated rubric at build.

## Layer 1 inventory

Each item, the system that writes it, its file and its natural mishandling; the R2 block in `checks.py` asserts the
golden method with the item mishandled.

| Item | System | File | Mishandled | Effect (asserted) |
|---|---|---|---|---|
| two address formats (legacy-migrated accounts in mixed case with words spelt out, accounts opened since 1 January 2025 in USPS capitals) | the UI tax system's 2025 replacement | register | matched raw | none on the golden (addresses unread) |
| two NAICS vintages | the register's coding on registration (2017 before 2025) | register, quarterly reports | compared raw | none on the golden |
| ZIP-based county codes before 2025Q3 | the UI tax system's geocoding project | quarterly reports | read as the worksite's county | none on the call (rows read are geocoded); Ask A and B (D2, ledgered) |
| zero reports from open accounts | the quarterly report cycle | quarterly reports | an open account read as operating | none on the call (employment read) |
| final pay after a closure | payroll timing | quarterly reports, wage records | wages read as employment | none on the call (no 2026 new account affected); Ask B (H3, ledgered) |
| monthly employment on the 12th against quarterly wages | the QCEW report form | quarterly reports | wages read as employment | none on the call (SF1, SF6) |
| a worker on two accounts in a quarter | job changes | wage records | the worker counted at one account | none on the call (shares computed per account) |
| liability and registration dates | the register | register | registration read as first employment | none on the call (SF2, SF3); Ask A (D5, ledgered) |
| status and inactivation dates processed after the last payroll | the UI tax unit | register | status read as operation | none on the call; Ask B (H4, H5, ledgered) |

## Pre-ship check

- **Gates:** generator checks 122 of 122 (the golden against the generator's truth for every county's 2026 births,
  set-aside accounts and 2025Q4 base, and for Ask A's births and Ask B's deaths; the three-rules block on the clean
  truth, R3a filing Caldmere, Eskwell and Tolbeck and R3b the golden; every rung and reflex by name; SF1 to SF16; the
  converging variants; mess neutrality; the asks' stops; the separation of the device rows from the call; H9 and H24;
  the realism sweep; the deliverables against figures.json); the independent verifier on its own pandas path; two
  consecutive builds byte-identical (10 target files, 2 goldens, metadata.json, figures.json); target.zip cut from the
  final build and equal to target/ file by file; figures_check 85 of 85; voice-check PASS at 986 characters; precut 49
  checks, 0 FAIL.
- **Input gates:** 10 files in four formats (csv, txt, pdf, xlsx); the wage records at 608,789 rows and the quarterly
  reports at 65,564; three distractors in metadata.json (the population estimates, the Secretary of State's filings,
  the program's grant disbursements), none read by the golden or an ask.
- **The 10/10 rules re-read against the built pack:** the decisive step is the field's continuity test on the workforce,
  executed on the clean truth in checks.py; the predecessor field, the addresses, names and industry codes all read
  correctly still file a wrong set; the mess (address formats, NAICS vintages, ZIP-based county codes before 2025Q3,
  zero reports, final pay) is Layer 1, and no slip alone moves the call.
- **Golden realism:** the memo's title is its finding, with a source line under the table, a note from the guideline
  (accounts opened in 2026 that had not reported employment are not counted) and a chart titled with its 2025 finding;
  the workbook has named sheets, frozen panes, number formats by quantity, a filter and print titles on the account list
  and a notes sheet. Containers audited clean (scrub_producer_metadata).
- **House fixes:** H1 clean; H3 the rival clause in block 1 states a checked ordering (Caldmere and Tolbeck second and
  third on new accounts per 100); H9 the manifest and the dictionary name exactly the shipped files (asserted); H16
  every register date on or before the extract (asserted); H23 the set-aside ask reads "if any"; H24 no shipped file
  says the pack was built (asserted).
- **Guard:** heart WARN (strategy risk, organisation family, objective overuse; task82 differentiated); surface promotes
  task82 only (the same-driver signature the card differentiates).

## Tried and rejected

- 2026-10-13, draw: the seed's ICD-9 to ICD-10 comparability bridge as the mechanism. Rejected: a documented-break bridge is the family task453 spent (a level shift removed before seasonal adjustment).
- 2026-10-13, draw: the provisional-count completion for deaths pending investigation. Rejected: task451's driver (a period total not yet observed, completed from the history of how amounts arrive).
- 2026-10-13, draw: survey-research-official-statistics x ETL now. Rejected by the guard (ban.pairing against task453); the build waits two draws.
- 2026-10-15, draw resumed: the paused draft's two reviews (2022 and 2025) showing steady sensitivity and specificity while predictive values move. Rejected: the second review is a control bench that tests the error model for the solver; one full review of 2025 measures the error matrix and the decisive step is where the false listings come from. The draft's organisation (the county council certifying under a state filing) collided with a live build's forcing event and organisation family (task141); the decision moved to the recovery foundation that holds the settlement share, its trustees releasing phase two at the close of phase one.
- 2026-10-15, stage 4: Ask A as each year's file at its close and the deaths added since, 2019 to 2025, carried by the out-of-state deaths' exchange receipt dates. Died: the leak reader joined the receipts and hit all seven close counts (a work order, not a silent device, and the 2025 close count tied to the review's 408 rows), and the judge returned 'added since' as a gross or net fork (FIX_NOW).
- 2026-10-15, stage 4: Ask B on one report per unit with the criteria and the address split between them. Died: the reader keyed patients by incident, sex and age, took the criteria, address and outcome from any report and hit all 24 quarters; patients with no address on any report were a residence fork (judge).
- 2026-10-15, architecture 1 spent at stage 4: the coroner's certificates corrected through the medical examiner's 2025
  error matrix by drug class held the call against both leak readers (4.5 and 8.4 per cent, the first year only), but the
  one re-judge after the workbook asks' FIX_NOW returned NOT_DETERMINISTIC, SEND_BACK: which drugs and certificate codes
  make the stimulant class was never filed, and reading the certificate's stimulant as T43.6 alone (184 against 247, 25.5
  per cent) or keeping cocaine apart (189, 25.0; 21.8 or 26.7 with cocaine among the other drugs) moved the graded 2026
  count, baseline and change. Filing the classes would have handed over the decisive construction, so the slot re-roots.
- 2026-10-15, design (paper, architecture 2): the first ladder's default path filed Caldmere, Eskwell and Quarrin, but a
  strict address match (same industry, the old tenant stopping the quarter before) removed none of Quarrin's re-lets
  and landed the golden by a wrong method. Died on paper; Tolbeck's relocations, which no address method catches, now
  hold every attribute linkage on a wrong county.
- 2026-10-15, build: the cross-county attribute linkage (same six-digit industry, the old account's last quarter the one
  before, size within a quarter) landed the golden set by coincidence, its false matches falling evenly on every county.
  Died at the first build; the re-registered stores and most relocations now carry the industry code their new owners
  reported at registration, as new registrations do, and the linkage files a set with Tolbeck.
