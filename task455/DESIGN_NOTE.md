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
  The wage records show continuity, read the way the field reads successor and predecessor flows: from the old account's
  side, a new account continues a business when most of the workers an account paid in its last quarter with employment
  are on the new account's payroll that quarter or the next. Read from the new account's side (most of its first-quarter
  workers from one account that then stopped reporting), the take-overs whose new owners hired from the first day look
  like births and the start-ups staffed from a large closed payroll look like continuations, and the call goes to
  Caldmere instead of Quarrin.
- **World:** an unnamed state's Lornock Valley region (invented), seven counties (Brennock, Caldmere, Dunrath, Eskwell,
  Fennamore, Quarrin, Tolbeck), about 7,000 private establishments and 60,000 private jobs. Events of 2026 the data
  carries without naming: a fuel and convenience operator bought nineteen Caldmere stores at the start of the second
  quarter, re-registered each under a new account and reopened sixteen of them as markets, keeping every store's staff and
  hiring more from the first day; Tolbeck's new enterprise park drew twenty-one businesses from the other counties, each
  re-registered as a Tolbeck entity, twelve of them hiring for bigger premises; Quarrin's downtown storefront program
  filled twenty-four storefronts vacated in 2025 and early 2026 with new businesses; a 192-worker food distribution
  warehouse in Quarrin closed on 19 December 2025 and eight new businesses started early in 2026 with a few of its
  former workers each. Background: take-overs with and without a filed transfer in every county (dated in the first
  days of a quarter), smaller expansions and start-ups from closed payrolls in other counties and in 2025, 2025 closures
  whose staff an established employer of the same trade took on, two 2025 mergers, 2025 take-overs that changed hands
  inside a quarter, summer employers in the lake and recreation trades (a few keeping a worker through the winter),
  winter pauses over 2025 to 2026, closures with final pay in the next quarter, and the UI tax system's move from
  ZIP-based to geocoded county codes with the third-quarter 2025 reports.
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
  business's staff going on together from the closed account to the new one, often beside the new owner's own hires,
  and show a closed employer's workers scattering, a few of them into new businesses of their own.
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
10.8 per 100). The strong analyst who finds the wage records and links each new account to the account most of its
first-quarter workers came from still designates Caldmere, Dunrath and Eskwell (Caldmere at about 10.1), because the
buyer of nineteen Caldmere stores reopened sixteen as markets with every store's staff and more than as many again
hired from the first day, twelve of Tolbeck's park arrivals did the same in bigger premises, and eight Quarrin start-ups
staffed mostly by workers from a closed 192-worker warehouse look like its continuation. Read from the old account's
side (most of a closed account's last-quarter workers on one new account's payroll), the stores and the moves continue
businesses, the start-ups are births, Caldmere falls to 7.8, Tolbeck to 7.2, Quarrin keeps 9.5, and the designation is
Dunrath, Eskwell and Quarrin.

## Three rules

- Task type: Survey Research & Official Statistics, census-register-administrative-data-quality (administrative employer
  accounts conformed into the statistical units official business demography counts), which serves ETL.
- Domain test: the deciding quantity is each county's 2026 establishment birth rate as business demography measures it,
  a new establishment and not a continuing business under a new employer account, built by the field's employment-flow
  continuity test read from the predecessor's side (the share of the old unit's workforce that goes on to the new
  identifier, as in the successor and predecessor flows of linked employer and employee data).
- Swap: with hospital nouns ("which three counties' hospitals opened the most new wards") there is no employer account a
  business re-registers under after a sale or a move and no workforce that moves with it, so the task stops reading the
  same.
- Layer 1: the employer register (account keys, legal and trade names, worksite addresses in two formats from the 2025
  system change, two NAICS vintages, status, liability and registration dates, the predecessor field), the quarterly
  reports (monthly employment on the 12th against quarterly wages, county codes assigned from the ZIP code before the
  third quarter of 2025, zero reports from open accounts, final pay after a closure, winter pauses), the wage records
  (protected worker keys, a worker on two accounts in a quarter): each produced by the UI tax and wage systems, none
  placed to be caught.
- Layer 2: field_method; the decisive choice is the unit counted (an establishment, not an account opening) and which
  side of a worker flow settles continuity: the old account's workforce going on, not the new account's hiring.
- Decisive step: a new account continues a business when more than half of the workers an account paid in its last
  quarter with employment are on the new account's payroll that quarter or the next, that account employing no one after
  the new account's first month; neither the new account's own share, the filed predecessor, a shared address, a similar
  name nor an attribute match decides it.
- Not semantics: every field read correctly (the predecessor field, the addresses, names, industry codes, dates, the
  worker key) still leaves the expanded take-overs among the births and the start-ups staffed from a closed payroll among
  the continuations when the flow is read from the new account's side; nothing in any field marks either.
- Not rule application: the guideline defines a birth as a business that did not operate before under another employer
  account and names the events (a sale, a reorganisation, a change of legal form) without saying how continuity shows;
  executing it through the register's predecessor field, an address or name match, or the new account's share of its
  first workers designates the wrong counties.
- Analyst test: a strong analyst counts each county's new accounts first employing in 2026, nets off the register's
  predecessors and designates Caldmere, Eskwell and Tolbeck (the default path's Ends on, Caldmere at about 11.1 per 100);
  the stronger one links the rest through the wage records by where each new account's first-quarter workers came from
  and designates Caldmere, Dunrath and Eskwell (Caldmere at about 10.1).
- Estimand: the program guideline (`formation_counties_program_guideline_2027.pdf`) fixes the population (private
  establishments, counted in the county in which the worksite lies), the outcome (births in 2026: an establishment first
  reporting employment in 2026 whose business did not operate before under another employer account), the base (private
  establishments reporting employment in at least one month of the fourth quarter of 2025), the unit (the establishment)
  and the comparison (the three highest rates, compared unrounded).
- No decoy: no memo, draft, briefing or published figure carries a ranking or a birth count; the register's predecessor
  field is the UI program's own record of approved transfers, true where it is filled, and its dictionary entry says it
  is filled only on an application.
- No certified replay: no published or certified birth count ships, so nothing is recovered by reproducing figures.
- Lesson: a model learns that whether a new identifier continues an old unit is read from where the old unit's members
  went together, not from where the new identifier's members came from, a filed link, a shared location or a similar
  name; no build on file decides a unit's novelty from the predecessor's side of member flows.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 new accounts net of the register's predecessors (default path) | the guideline's "did not operate before under another employer account" and the predecessor field's entry send the solver to the field | `predecessor_account` is a column: a row predicate | netting the register's successorships is the first reflex | none | none | one filter | readable |
| R1 new accounts at the address of an account that closed set aside | the dictionary's "an employer that takes over a business without applying has no predecessor recorded" sends the solver looking for unfiled take-overs | the worksite address is a column; a self-join on it after normalising two address formats | address matching is the record-linkage reflex | none | none | one join | readable |
| R2 the new account's share: more than half of its first-quarter workers paid the quarter before by one account that then stopped reporting | the same dictionary entry; the worker key "the same for a worker in every account and quarter" | no column links accounts; a grouped self-join of the wage file by worker and quarter | the linkage an analyst who starts from the new accounts builds first: where did this account's workers come from | none | none | a share per new account | readable |
| R3 (decisive) the old account's share: most of a closed account's last-quarter workers on the new account's payroll | none: no sentence names a side, a share, a quarter or a flow | the same wage file read from each closed account's last payroll forward | not a reflex: the new account's share is the natural reading of a question about new accounts, and its distribution has no gap (births to 0.33, expanded take-overs from 0.30 to 0.46, start-ups from a closed payroll at 0.67 to 0.80) | none: no control or published count confirms a continuity | none: the battery finds nothing wrong with the netted counts | a share per closed account over the same self-join | silent |

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
| SF10 | more than half | over 50 per cent of the old account's last-quarter workers | 60, 70 or 80 per cent | same call, same counts | continuations carry 83 per cent or more, births take 33 per cent or less of any closed account's last-quarter workers (asserted) |
| SF11 | an account that then stopped reporting | its last month with employment before the new account's first month | none in the new account's first quarter; no stop test | same call, same counts | no 2026 new account took over inside a quarter (asserted) |
| SF12 | workers of the first quarter | paid in the first quarter with employment | on the payroll on the 12th of a month of that quarter | same call, same counts | 2026 take-overs change hands in the first days of a quarter's first month, before the 12th (asserted) |
| SF13 | on the new account's payroll | in the old account's last quarter or the next | the new account's first quarter only; the old account's last quarter and the three after | same call, same counts | asserted |
| SF14 | the old account's workers | paid in its last quarter with employment | also its last quarter with wages (final days paid in the new account's first quarter) | same call, same counts | asserted |
| SF15 | rates compared | unrounded | rounded to one decimal | same call | guideline 4.2 "compared unrounded"; no tie at one decimal (asserted) |
| SF16 | births of 2026 that changed hands within 2026 | the first account stays a birth, its successor a continuation | both births | same call | guideline 3.3; asserted |
| SF17 | a workforce going on together | any number of workers | five workers or more | same call, same counts | every unfiled continuation moved five workers or more (asserted) |
| SF18 | continuity read from | the old account's side (its workforce going on) | the new account's side (most of its first-quarter workers from one account) | Caldmere, Dunrath and Eskwell | not a reading of a term: guideline 3.3's subject is the business that goes on; the new account's side counts as births twenty-eight take-overs and moves whose whole staff went on, and as continuations start-ups that took 3.3 per cent or less of a closed payroll (asserted as rung 2) |

## Ladder

Built magnitudes (rates per 100 establishments reporting employment in 2025Q4; `checks.py` asserts each rung by name).

| Rung | Reading | Files | Dies to |
|---|---|---|---|
| 0 | new accounts first employing in 2026, net of the register's predecessors (default path) | Caldmere, Eskwell and Tolbeck (Eskwell 11.99, Caldmere 11.11, Tolbeck 10.78; Dunrath 10.19, Quarrin 9.85) | Caldmere's nineteen re-registered stores and Tolbeck's twenty-one relocations have no predecessor recorded, and their old accounts' staff went on to them |
| 1 | also set aside new accounts at the worksite address of an account that stopped reporting (146 matched) | Dunrath, Eskwell and Tolbeck (Eskwell 11.07, Tolbeck 10.46, Dunrath 9.55; Caldmere 7.55, Quarrin 6.72) | Quarrin's twenty-four storefront re-lets are new businesses (a different storefront trade the quarter after, or a vacancy of two quarters or more; a new owner and name; mostly new workers) and Tolbeck's relocations moved address |
| 2 | the new account's share: more than half of its first-quarter workers paid the quarter before by one account that then stopped reporting | Caldmere, Dunrath and Eskwell (Eskwell 11.46, Caldmere 10.11, Dunrath 9.95; Tolbeck 9.15, Quarrin 8.69) | sixteen of Caldmere's stores and twelve of Tolbeck's arrivals took on every worker of the old account and hired from the first day (the old staff 30 to 46 per cent of the first payroll), and eleven start-ups (eight in Quarrin, three in Fennamore) staffed 67 to 80 per cent from a large closed payroll took 3.3 per cent or less of it |
| 3 | the old account's share: more than half of a closed account's last-quarter workers on the new account's payroll that quarter or the next (golden) | Dunrath, Eskwell and Quarrin (Eskwell 11.33, Dunrath 9.79, Quarrin 9.50; Caldmere 7.83, Tolbeck 7.19) | stands |

- Other reflexes, each landing a named wrong set (asserted): every new account counted (Caldmere, Eskwell and Tolbeck);
  a trade-name match (Caldmere, Eskwell and Tolbeck); the address match restricted to the same industry and the quarter
  before (Dunrath, Eskwell and Tolbeck); the address match or a name match (Dunrath, Eskwell and Tolbeck); attribute
  linkage in the county or across counties (Caldmere, Eskwell and Tolbeck); the address match joined with the workforce
  test (Caldmere, Dunrath and Eskwell); any worker from a closed account (Caldmere, Dunrath and Eskwell); the new
  account's share at 80 per cent or with no stop test, and both shares at 50 or 80 per cent (Caldmere, Dunrath and
  Eskwell, Quarrin 9.62 under both shares). Either share designates the three but sets aside Quarrin's eight start-ups
  (Quarrin 8.57 against 9.50), missing Quarrin's births, set-aside count and rate.
- Winners and margins: golden third over fourth 9.50 against 7.83, 1.213x; the first county left out over the fifth by
  0.65; rung 1 third over fourth 1.265x; rung 0 Caldmere over Quarrin 1.128x; rung 2 Dunrath over Quarrin 1.145x and
  Caldmere over Quarrin 1.164x.
- Variants of the golden that converge (asserted): thresholds of 50 to 80 per cent of the old account's workers; the
  stop test by month, by quarter or dropped; the new account's payroll over one, two or four quarters; the old account's
  workers in its last quarter with employment or with wages; any minimum block of two to five workers; a worker on two
  accounts counted at the higher-paying one.
- Position and dominance: Quarrin is fifth on rungs 0 and 2 and sixth on rung 1; the decisive move (from the new
  account's side to the old account's) is the only correction that lowers Caldmere and restores Quarrin on a worker-flow
  rung; it moves Caldmere's births by 16, Tolbeck's by 12 and Quarrin's by 7.
- Grid: a Layer 1 slip (December employment or wages for the base, registration dates, zero reports read as operating)
  with rung 0, 1 or 2 never files Dunrath, Eskwell and Quarrin (the slips keep the call under the golden, asserted; the
  rungs move it).
- Worth: rung 0 moves the call and three counties' births, set-aside counts and rates; rung 1 moves the call and
  Quarrin's and Tolbeck's figures; rung 2 moves the call and every county's births, set-aside count and rate.

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
| 8 | Window length | the year's four quarters; continuity read over the old account's last quarter and the next | SF13 converges |
| 9 | Boundary inclusivity | more than half of the old account's last-quarter workers | C1: no share between 34 and 82 per cent (SF10) |
| 10 | Rounding path | rates compared unrounded, shown to one decimal; the gap from unrounded rates | guideline 4.2; the prompt's rounding sentence; no figure within 0.01 of a rounding edge (asserted) |
| 11 | Tie-break | none needed | no tie (asserted) |
| 12 | Maturity and censoring | births late in 2026 observed for one quarter; continuity needs only the first quarter | C1 |
| 13 | Order of operations | conform, find new accounts, set aside continuations, divide | C1 (set operations commute) |
| 14 | Row order | none matters | C1 |
| 15 | Duplicate resolution | none: one row per account and quarter, one wage row per worker, account and quarter | asserted |
| 16 | Identity normalisation | accounts by account number; workers by the protected key | dictionary; SF9 to SF14, SF17, SF18 |
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
whose buyer did not apply, so a literal reader cannot take it as the set of continuations. The sentence's subject is the
business that goes on, so the evidence is where that business's people went: in the wage records, most of the workers a
closed account paid in its last quarter with employment are on one new account's payroll that quarter or the next (83
per cent or more in every case), while no birth holds more than 33 per cent of any closed account's last-quarter
workers; every threshold, window, denominator and minimum block between those values selects the same accounts. The
new account's own share is not another reading of the sentence: it asks where a new account's workers came from, so it
calls a Pellworth market that kept every worker of the Halvard store it replaced a birth because it hired as many again,
and calls a three-person start-up that took two of a closed warehouse's 192 workers the warehouse going on. An address
match is evidence the data refutes, since Quarrin's matched storefronts are a different industry or followed a vacancy
of two quarters or more, carry a new owner and name and hire mostly new workers, and Tolbeck's relocated businesses
share no address with the accounts they continue.

## Oracles

None. No control, published figure or reconciliation column confirms any rung: the extract manifest gives row counts per
file; the county population estimates, the Secretary of State's entity filings and the program's grant disbursements
carry no establishment or birth counts; the register's predecessor field confirms the filed successorships on every rung
alike.

## Ask sheet

- **Ask A, 2025 births by county:** each county's 2025 births, counted as 2026's are, and its 2025 birth rate per 100
  private establishments reporting employment in the fourth quarter of 2024 (fourteen figures, counts whole, rates to
  one decimal). H18 home: a measure every county carries that the call does not turn on (the prior year the Secretary's
  announcement compares). Construction: the guideline's birth definition on 2025, continuity by the old account's
  workforce (2025 take-overs in every county, eight of them expansions, and five start-ups from two closed payrolls in
  Brennock and Dunrath). Primary device: D8, a clock read at the wrong grain: ten 2025 take-overs changed hands inside a
  quarter (Brennock, Dunrath and Fennamore two each, the other counties one), the old account's last payroll falling in
  the quarter's first or second month and the new account employing from the next; a continuity test that asks the old
  account to have stopped before the new account's first quarter (the stop the leak reader used) leaves every one a
  birth, while the month the old account last employed, read against the new account's first month, sets each aside.
  Hazards: H1 the summer employers and paused contractors that look new in 2025 on the extract's single 2024 quarter
  (the register's liability date is their first payroll years back, and "counted as 2026's are" points at the
  guideline's first reported employment); H2 the county coding (below; the prompt counts each establishment where its
  worksite lies); H3 the construction. Path: the quarterly reports, the register, the wage records, the guideline, the
  dictionary, the county codes and the manifest (seven files, eleven columns). Stops (built, every figure asserted
  outside its bin): the quarter-level stop (the cracker's path), births 120, 53, 106, 78, 83, 64 and 48 against 118,
  52, 104, 77, 81, 63 and 47 (Brennock to Tolbeck), every rate off by 0.11 to 0.18; the new account's share (rung 2),
  119, 54, 105, 79, 84, 65 and 49; the extract's window alone, every count high by the summer employers; the golden.
  Realism: take-overs close on any day, and an old owner's last payroll often runs into the quarter the new owner
  starts in.
- **Ask B, 2025 deaths by county:** each county's 2025 deaths (an establishment whose last month with employment fell in
  2025, that reported none in 2026 and whose business did not go on under another account) and its death rate on the
  same base (fourteen figures). H18 home: the other side of the year's business dynamics, beside the births.
  Construction: the accounts whose staff went on together to a new account in 2025 or January 2026 are not deaths.
  Primary device: D7, the true key elsewhere: twenty 2025 closures (Brennock and Eskwell four each, Dunrath and
  Fennamore three, the other counties two) were taken on by an established employer of the same trade (a remodeller,
  a law practice, a salon, a home care agency), their staff moving as a block to the buyer's existing account the next
  day, and two more joined a take-over as a merger; no new account is involved, so a death count that nets only the
  sources of the new accounts' continuations (the reader's) keeps all twenty-two, while following each closure's
  last-quarter staff to the next quarter's payroll (any account, new or established) sets them aside. Hazards: H3 final
  pay in the first quarter of 2026 after a December closure (a wage reading keeps them open); H4 accounts left open and
  filing zero reports (a status reading misses them); H5 inactivation dates processed months after the last payroll (an
  inactivation-year reading moves them); H6 winter pauses (twelve accounts employing no one for two to five months
  from October or November 2025, then again in 2026; a reading of December employment calls them closed); H2 the county
  coding. Path: the quarterly reports, the register, the wage records, the dictionary, the county codes, the guideline
  and the manifest (seven files, ten columns). Stops (built, every figure asserted outside its bin): the new accounts'
  sources only (the cracker's path), deaths 115, 56, 91, 57, 84, 98 and 48 against 110, 54, 88, 53, 80, 96 and 46,
  every rate off by 0.2 to 0.6; the same with the stop read by quarter, 117, 57, 93, 58, 86, 99 and 49; the new
  account's share, 123, 57, 94, 59, 86, 100 and 50; filed transfers only (the mirror), 131, 57, 97, 61, 87, 102 and 50;
  the golden (the next quarter, two or three quarters, thresholds of 50 to 80 per cent and any minimum block all agree).
  Realism: a practice or a crew taken on by a larger firm of its trade is the commonest small-business exit after a
  plain closure.
- **The chart:** each county's 2025 births and deaths as paired bars; its values are Ask A's and Ask B's counts.
- **Main population zero-counts (asserted):** no 2026 new account and no establishment in the 2025 fourth-quarter base
  is a summer employer resuming or a dormant account (the summer employers in the base keep a worker in every month);
  no in-quarter take-over, absorbed business or merger touches a 2026 new account or its source; every quarterly row the
  call reads (2025Q4 and 2026) carries the geocoded county; no 2026 new account straddles the year boundary on wages,
  registration or liability dates.
- **Hazard table (built):** H1 moves every Ask A count for a response reading the extract's window; H2 moves Ask A and
  Ask B rates for a response reading the quarterly rows' county before 2025Q3; H3, H4, H5 and H6 move Ask B's counts for
  a response reading wages, status, inactivation dates or December employment instead of the last month with
  employment; the construction (2025 expansions and start-ups) moves every Ask A and Ask B count on rung 2.
- **Referee:** none needed; no control ties only under the golden.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule) | Verdict |
|---|---|---|
| A, 2025 births and rates | links new accounts by the stop it used for 2026 (the old account silent from the new account's first quarter): the ten in-quarter take-overs stay births, every count and rate off | miss |
| B, 2025 deaths and rates | nets the predecessors and the sources of the continuing new accounts: the twenty-two closures taken on by established employers or merged stay deaths, every count and rate off | miss |

- Measured at stage 4: the second leak reader read continuity from the closed account's side (most of a closed
  account's last-quarter workers on one new account's payroll the next quarter), which also follows absorbed
  businesses and in-quarter take-overs, and landed the call and every ask figure but Caldmere's deaths (53 against 54);
  the devices hold the new-account path, the first reader's, and the pair ceiling below assumes one response on it.
- Mirror leakage: about 5 per cent of ask weight (a response on rung 0 counts the 2025 take-overs as births and their
  sources and the absorbed businesses as deaths in every county; it keeps the chart's layout criteria only).
- Pair ceiling: 34 (cracker 38 + 7 + 55 x 0.15 = 53.3, keeping the account list and the chart's layout; the second
  response on rung 2: 5 + 7 + 55 x 0.05 = 14.8; average 34.0), rerun from the generated rubric at build.

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
| winter pauses (no employment for two to five months from October or November 2025, then employing again) | the quarterly report cycle | quarterly reports | a pause read as a closure | none on the call (the base reads any month of 2025Q4; no pause began before 14 October 2025); Ask B (H6, ledgered) |
| summer employers keeping one worker through the winter | the quarterly report cycle | quarterly reports | none | none (in both bases under every reading) |
| take-overs dated in the first days of a quarter's first month (the old account paying its final days in the new account's first quarter) | payroll timing | quarterly reports, wage records | wages read as employment | none on the call (SF12, SF14) |

## Pre-ship check

- **Stage 4:** the first pass returned DETERMINISTIC, FIX_NOW on the two 2025 conventions (determinism_check_report.md);
  the one re-judge on the recut returned DETERMINISTIC, APPROVE (determinism_check_report_pass2.md), with the 2025
  liability-date filter and a next-quarter-only window as residual notes on supplementary figures. The window note is
  closed in the data for the shipped cut (the movers stay through the quarter after the new account's first, a
  take-over in the extract's last quarter dated on its first day; SF14 asserts the variant), together with the second
  reader's realism tells (the chain's store numbers out of sequence, a filed transfer under common ownership keeping
  the employer identification number in about three cases in ten); every graded figure and every assertion is
  unchanged from the judged cut, and no document or the prompt changed.
- **Gates:** generator checks 143 of 143 (the golden against the generator's truth for every county's 2026 births,
  set-aside accounts and 2025Q4 base, and for Ask A's births and Ask B's deaths; the three-rules block on the clean
  truth, R3a filing Caldmere, Eskwell and Tolbeck on the default path and Caldmere, Dunrath and Eskwell on the new
  account's side, R3b the golden; every rung and reflex by name; SF1 to SF18; the converging variants; mess
  neutrality; the asks' stops and the devices' separation from the call; H9 and H24; the realism sweep; the
  deliverables against figures.json); the independent verifier on its own pandas path (the old account's share and the
  next-quarter deaths test); two consecutive builds byte-identical (10 target files, 2 goldens, metadata.json,
  figures.json); target.zip cut from the final build and equal to target/ file by file; figures_check 85 of 85;
  voice-check PASS at 998 characters; precut 49 checks, 0 FAIL; leak.py REVIEW (no LEAK: county names in the
  guideline, golden digits inside wage amounts).
- **Input gates:** 10 files in four formats (csv, txt, pdf, xlsx); the wage records at 616,296 rows and the quarterly
  reports at 65,416; three distractors in metadata.json (the population estimates, the Secretary of State's filings,
  the program's grant disbursements), none read by the golden or an ask.
- **The 10/10 rules re-read against the built pack:** the decisive step is the field's continuity test read from the
  predecessor's side, executed on the clean truth in checks.py; the predecessor field, the addresses, names, industry
  codes and the new account's own share all read correctly still file a wrong set; the mess (address formats, NAICS
  vintages, ZIP-based county codes before 2025Q3, zero reports, final pay, winter pauses, take-over dates in a quarter's
  first days) is Layer 1, and no slip alone moves the call.
- **Golden realism:** the memo's title is its finding, with a source line under the table, a note from the guideline
  (accounts opened in 2026 that had not reported employment are not counted) and a chart titled with its 2025 finding;
  the workbook has named sheets, frozen panes, number formats by quantity, a filter and print titles on the account list
  and a notes sheet. Containers audited clean (scrub_producer_metadata).
- **House fixes:** H1 clean; H3 the rival clause in block 1 states a checked ordering (Caldmere and Tolbeck second and
  third on new accounts per 100); H9 the manifest and the dictionary name exactly the shipped files (asserted); H16
  every register date on or before the extract (asserted); H23 the set-aside ask reads "if any"; H24 no shipped file
  says the pack was built (asserted).
- **Guard:** heart WARN (strategy risk, organisation family, objective overuse; task82 differentiated); surface promotes
  task457 and task453 on the card pairing alone (same domain and objective; task457 also a register artifact and a
  ranked slate) and task82 on the same-driver signature, each differentiated on the card: task457 corrects faculty
  disclosures for the part of a year they could not see, task453 sets a seasonal-adjustment setting.

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
- 2026-10-15, stage 4: continuity read from the new account's side (more than half of its first-quarter workers paid
  the quarter before by one account that then stopped reporting), with every take-over keeping its size and no birth
  drawing over a third of its first workers from one account. Died to the leak reader, who built exactly that linkage
  from the wage file, landed Dunrath, Eskwell and Quarrin with every figure and hit every Ask A and Ask B figure
  (liability dates for the summer employers, the register's county for the base). The judge (DETERMINISTIC, FIX_NOW)
  found the 2025 birth definition and the 2025 county basis unpinned in the prompt, and the reader found "runner-up"
  read as the second-ranked county. Rebuilt in one pass: the take-overs' new owners hire from the first day and closed
  payrolls seed start-ups, so the new account's side files Caldmere, Dunrath and Eskwell and only the old account's side
  files the golden; Ask A's device moved to in-quarter take-overs and Ask B's to closures taken on by established
  employers; the prompt counts 2025 births as 2026's are, each establishment where its worksite lies, and asks for the
  first county left out.
