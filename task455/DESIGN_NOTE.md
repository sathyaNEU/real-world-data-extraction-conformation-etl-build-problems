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
- **Shape:** 01, a ranked list under a cap. Arithmetic: the designated three and the runner-up with its gap (4); each of
  the seven counties' 2026 births and birth rate (14); the count of new accounts set aside as continuing businesses in each
  county (7); then the asks (designed at stage 2, each on rows the call never reads): about 25 before the asks.
- **Strategy:** identity_resolution (G3 record versus operation decisive, G10 cross-dimensional duplication behind it).
  New UI accounts with first employment in 2026 are the obvious births. The employer register records a predecessor only
  when the new employer files to take over the predecessor's experience rating, which a buyer of a business with a high
  tax rate does not do; a shared address marks most continuing businesses but also every new business that took over a
  closed one's premises. Only the wage records show a continuing business: most of its first-quarter workers were employed
  together at one account that stopped reporting the quarter before. Counted that way, the county lifted by an acquired
  chain's re-registered sites falls out of the top three, and the county with the most re-let premises keeps its births.
- **World:** an unnamed state's Lornock Valley region (invented), seven counties (Brennock, Caldmere, Dunrath, Eskwell,
  Fennamore, Quarrin, Tolbeck), about 7,100 private establishments and 70,000 private jobs. The pack carries the state
  Labor Market Information (LMI) bureau's extract of the UI employer register (accounts, registration and liability dates,
  legal names and trade names, worksite addresses, ownership, industry codes on two NAICS vintages, the predecessor field,
  status), the quarterly establishment reports for 2024Q4 to 2026Q4 (monthly employment, wages, county; the spine, about
  60,000 rows), the quarterly wage records for the region's private employers (hashed worker identifiers, about 600,000
  rows), the Commerce Department's program guideline (the designation rule and the birth definition), a data dictionary, an
  extract manifest and distractors (county population estimates, the grant applications log). Forcing fact: the
  legislature's 2027 to 2029 appropriation requires the designation by 30 June 2027; the extract is dated 14 May 2027,
  after the 2026 fourth-quarter reports were due. The measure is a closed year because the program guideline designates on
  the latest full year; the call (which counties receive 2027 to 2029 grants) faces forward.
- **Forum and forcing event:** minister_or_cabinet (the Commerce Secretary designates), budget_or_appropriation.
  Organisation government_agency; role research_desk (the LMI bureau's business dynamics economist). Personas from
  `guard.py names --geo "United States" --seed 3455` and `--seed 2455`: Kristy Townsend (the economist), Brandon Compton
  (the Commerce Department's program director), Chelsey Hensley (the UI tax unit's employer accounts supervisor).
- **Data-native sentence:** in the UI program an employer that buys or reorganises a business gets a new account and
  inherits the predecessor's tax rate only if it files for it, so the register records the continuity of the filers alone,
  while the wage records show every continuing business's staff arriving as a block from an account that stopped
  reporting the quarter before, and a new business in a closed one's premises hiring its own.
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

1. Read `lornock_ui_employer_register.csv` and `qcew_establishment_quarters_2024_2026.csv`; keep private accounts and each
   account's county of location.
2. A birth is an account whose first quarter with employment is in 2026 (no employment reported from 2024Q4 to 2025Q4).
3. Set aside the accounts the register records with a predecessor (the filed successorships).
4. Divide each county's births by its private establishments with employment in 2025Q4 (the guideline's base) and rank.
5. Designate the top three.
- Ends on: Caldmere, Eskwell and Quarrin (designed: Caldmere at 10.5 per 100, lifted by the 19 sites of a hardware chain
  bought in May 2026 and re-registered under the buyer's new accounts without filing for the predecessor's rate).
- Golden: Dunrath, Eskwell and Quarrin (designed: Caldmere at 8.0 once the chain's sites are counted as the continuing
  businesses their workforces show; the address match also lands wrong, removing Quarrin's re-let premises and
  designating Dunrath, Eskwell and Tolbeck).

## Stump sentence

The default path counts each county's new employer accounts with first employment in 2026, net of the predecessors the
register records, and designates Caldmere, Eskwell and Quarrin (Ends on: Caldmere at about 10.5 per 100), because an
acquired chain re-registered its 19 Caldmere sites under new accounts without filing for the predecessor's rate; counted by
the workforces that arrived together from accounts that stopped reporting the quarter before, Caldmere falls to about 8.0,
Quarrin's new businesses in re-let premises stay births, and the designation is Dunrath, Eskwell and Quarrin.

## Three rules

- Task type: Survey Research & Official Statistics, census-register-administrative-data-quality (administrative employer
  accounts conformed into the statistical units official business demography counts), which serves ETL.
- Domain test: the deciding quantity is each county's 2026 establishment birth rate as business demography measures it,
  a new establishment and not a continuing business under a new employer account, built by the employment-flow continuity
  test official business statistics use (most of a new account's first workforce from one account that ceased).
- Swap: with hospital nouns ("which three counties' hospitals opened the most new wards") there is no employer account a
  business re-registers under to change its tax rate and no workforce that moves with it as a block, so the task stops
  reading the same.
- Layer 1: the employer register (keys, legal and trade names, addresses written several ways, two NAICS vintages,
  status and predecessor fields), the quarterly reports (monthly employment against quarterly wages, late and amended
  reports), the wage records (hashed workers, workers on two accounts in a quarter): each produced by the UI tax and wage
  systems, none placed to be caught.
- Layer 2: field_method; the decisive choice is the unit counted, an establishment and not an account opening, and the
  evidence that settles it, the workforce's continuity.
- Decisive step: a new account is a continuing business when most of its first-quarter workers were employed together at
  one account that stopped reporting the quarter before; neither the filed predecessor nor a shared address decides it.
- Not semantics: every field read correctly (the predecessor field, the addresses, the dates) still leaves the
  unreported continuations among the births and the re-let premises outside them; nothing in any field marks either.
- Not rule application: the guideline defines a birth as a new business, not a business continuing under another
  account, and no filed rule says how continuity shows; executing the definition through the register's predecessor field
  or an address match still designates the wrong counties.
- Analyst test: a strong analyst counts each county's new accounts with first employment in 2026, nets off the register's
  predecessors (and, more careful, the accounts sharing an address with one that closed), and designates Caldmere, Eskwell
  and Quarrin (or Dunrath, Eskwell and Tolbeck with the address match); the default path's Ends on.
- Estimand: the program guideline (`lornock_formation_program_guideline_2027.pdf`) fixes the population (private
  establishments in each county), the outcome (births in 2026: a business first reporting employment in 2026 that did not
  operate before under another employer account), the base (private establishments with employment in 2025Q4), the unit
  (the establishment) and the comparison (the three highest rates).
- No decoy: no memo, draft, briefing or published figure carries a ranking or a birth count; the register's predecessor
  field is the UI program's own record of filed successorships, true where it is filled.
- No certified replay: no published or certified birth count ships, so nothing is recovered by reproducing figures.
- Lesson: a model learns that an administrative identifier opening is not a statistical unit's birth, and that the
  continuity an official count needs is read from the flow of the unit's members across identifiers, not from a filed
  link or a shared location; no build on file decides a unit's novelty from member flows.

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
