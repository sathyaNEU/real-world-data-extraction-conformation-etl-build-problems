# task468 design note: the 2027 hospital quality bonus, on deaths the linkage found and the deaths it missed

Status lives in `pipeline.json`; this note holds the design of architecture 4, drawn fresh on 2026-10-20 under the
author's rule (no task is retired; a spent architecture is re-rooted until one ships). Read `## Tried and rejected`
first: architectures 1 (transit nominations), 2 and 3 (specialty pharmacy staffing) are spent, each to an isolated reader
who took the careful construction the record displayed.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task468.json` (architecture v4), registered 2026-10-20 after a pull. Guard
  check WARN only after redrawing four blocked axes: the organisation family (government_agency, against task248 and
  task177: the decision moved from the state Medicaid agency to a nonprofit Medicaid health plan), the role family
  (policy_adviser, against task177: finance_controller), the forcing event (purchase_order_or_contract, against task177:
  the plan's statutory filing of its 2027 value-based arrangements) and the decisive generator (G12 with population and
  method selection is spent in task268 v2 and five older builds: G3, a link record is not a death, ahead of G12 and
  G14), with differentiation lines against task126 v1, task450 v1 and task469. WARNs answered: method_or_model_selection
  repeats task271 and is the Gate G of 9 of the last 12 builds (the decisive move is an estimator the record's two
  control groups force, and no other Gate G is honest); the persona first name Nathan appears in task181.
- **Pairing:** Healthcare Delivery & Health Economics / payment-claims-health-plan-analytics / Data Extraction &
  Conformation (ETL). The plan's measure dataset is conformed from sources never designed to join: its own inpatient
  claims, a delegated medical group's encounter submissions (another layout, with voids and replacements), the member
  enrollment file, the claims activity file, the state Office of Vital Records' death linkage for plan members, the
  plan's mortality risk scores and the network roster; the call turns on what that dataset says each hospital's 30-day
  deaths were.
- **Shape:** 10, a scorecard: each of 14 network hospitals' fiscal 2026 risk-adjusted 30-day mortality ratio (observed
  over expected) against the bonus line of 1.15, with whether it keeps its 2027 Hospital Quality Bonus; criteria from
  each hospital's ratio and verdict (28), the count losing it (1), the asks and the chart.
- **Strategy:** other (a linked outcome count corrected for the linkage's own false links and missed links, each
  measured on a control group inside the record), decisive generator G3 (a link record is not a death), with G12 (no link
  is not survival) and G14 (the error rates are conditional on the member's identifier class).
- **World:** the United States, an unnamed state that covers adults regardless of immigration status through Medicaid
  managed care, so members can be enrolled without a Social Security number. Halbrook Community Health Plan, a nonprofit
  Medicaid plan (about 310,000 members), pays each of its 14 network hospitals a Hospital Quality Bonus of 2 per cent of
  inpatient payments in contract year 2027 unless the hospital's ratio for fiscal 2026 index admissions (July 2025 to
  June 2026) exceeds 1.15. Deaths after discharge reach the plan only through the state Office of Vital Records'
  probabilistic linkage of plan members to the state death file. Personas from `guard.py names --geo "United States"
  --seed 468`: Wendy James (Vice President, Provider Contracting and Payment, who owns the call), Nathan Hawkins (the
  plan's quality measurement analyst) and Eric Thomas (manager of the Office of Vital Records Linkage Unit).
- **Forcing fact:** the plan files its 2027 value-based payment arrangements with the state by 1 November 2026; the
  bonus decision is set on the fiscal 2026 index admissions with deaths through 30 July 2026. The call faces forward
  (who is paid the 2027 bonus); its quantity is the closed fiscal 2026 year, which the bonus terms name as the basis
  (retrospective, with its reason: a pay-for-performance bonus is earned on a closed measurement year).
- **Forum and forcing event:** executive_team (the plan's executive team approves the filing),
  statutory_or_regulatory_filing; organisation other (a nonprofit Medicaid health plan); role finance_controller.
- **Data-native sentence:** the linkage keys a member to the death file by Social Security number when the enrollment
  file has one and by name, date of birth and sex when it does not, so for the members enrolled without one it invents
  deaths for those whose names are common and misses deaths for those whose surnames are written two ways; the
  obstetrics hospital's young mothers without a number carry the commonest surnames in the state, and the dialysis
  hospital's patients without a number carry compound surnames and die often, so one hospital's ratio is inflated by
  deaths that did not happen and the other's deflated by deaths the linkage never found.
- **The WHAT screen.** Population: the measure's index admissions at each hospital (the specification's index, transfer
  and exclusion rules); outcome: death from any cause within 30 days of the admission date, in hospital or after
  discharge (the specification defines the event, not a source); window: fiscal 2026 admissions, deaths to day 30;
  unit: the ratio of observed to expected deaths, expected from the plan's risk scores; comparison: each hospital against
  1.15. The decisive step settles none of them: it is how the deaths after discharge are estimated from a linkage whose
  errors the record measures (HOW, forced by the data's structure: links on members whom later claims show alive, and
  deaths recorded on later inpatient claims that the linkage did not find).

## Default path

1. Conform the plan's inpatient claims and the medical group's encounter submissions into fiscal 2026 index admissions
   under the specification (voided encounters out, replacements kept, a transfer joined into one stay, the listed
   exclusions applied).
2. Count each index admission's death within 30 days of admission: the discharge status "expired" for deaths in the
   stay, and the Vital Records linkage for deaths after discharge.
3. The careful analyst's reflexes: add the deaths that a later inpatient claim records (discharge status expired) which
   the linkage did not return, and drop the links on members who have claims after their linked date of death.
4. Divide each hospital's deaths by its expected deaths from the risk scores and withhold the bonus above 1.15.

Ends on: the obstetrics hospital loses the bonus on deaths the linkage invented and the dialysis hospital keeps it on
deaths the linkage missed (the ratios are fixed at calibration and written into `## Ladder`).
Golden: each hospital's deaths after discharge corrected class by class (Social Security number on file or not,
compound surname or not): the uncontradicted links less the false links expected at the rate measured on members whose
later claims show them alive, divided by the share of deaths the linkage finds, measured on the deaths later inpatient
claims record; the obstetrics hospital keeps the bonus and the dialysis hospital loses it.

## Stump sentence

The default path counts each hospital's in-stay deaths and linked deaths, adds the deaths later claims record and drops
the links later claims contradict, and withholds the bonus from the obstetrics hospital while the dialysis hospital
keeps it, because for members enrolled without a Social Security number the linkage invents deaths among common names
and misses deaths among compound surnames, and the reflex repairs reach only the members whose later claims happen to
show it; corrected at the error rates the two control groups measure, the obstetrics hospital keeps the bonus and the
dialysis hospital loses it.

## Tried and rejected` first. Architecture 1 (the Larkhaven transit nominations) and architecture 2 (the same pharmacy
world, developed by months since first fill) are spent; their records are in the card's lineage and the lines below.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task468.json` (architecture v3), registered 2026-10-19 after a pull. Guard
  check WARN only: `repeat.gate_g` (forecasting, as task249 v3 two builds back; the mechanism here is a development by
  months in the current episode of therapy, and task249's is a calibration drift, so the two share a Gate G label and
  nothing else) and `driver.near` against this slot's own v2 at 0.41, differentiated on the card (v2's clock was months
  since first fill, which is v3's analyst test). Shape 05; v2's draw axes kept (the world is unchanged, the decisive
  step is new).
- **Pairing:** Healthcare Delivery & Health Economics / payment-claims-health-plan-analytics / Data Extraction &
  Conformation (ETL). Two pharmacy benefit managers' specialty claim files (the outgoing PBM's January 2019 to December
  2025, the incoming PBM's from January 2026) are conformed into one record of fills by plan member, drug class and
  date, repriced at the incoming PBM's 2026 schedule; the call is the program's staffing, which turns on what that
  record says the members now on therapy will cost over the program year.
- **Shape:** 05, an allocation: the plan's Specialty Clinical Pharmacy Program staffs each of nine specialty classes
  with one clinical pharmacist for each $1.5 million of the class's managed spend for July 2026 to June 2027, or part
  (charter 3.1); managed spend is the 2026-schedule cost of the fills the class's members on therapy on 30 June 2026
  will receive in the program year (charter 2.1, 2.2). Criteria: the nine classes' pharmacists (9), the total (1), the
  nine classes' managed spend (9), the nine classes' rebates on 2025's fills (9), the chart with its parts (3) and the
  file (1), 32 in all.
- **Strategy:** composition_mix (the conditioning property is how long the member's current episode of therapy has run;
  the caseload's mix on it moved when members who had stopped came back), decisive generator G13 (the program year is a
  horizon the record covers only through members who have passed each month of an episode), with G6 and G14.
- **World:** the United States, an unnamed state. Merrow Health Plan, a nonprofit regional plan (about 482,000
  members). Its pharmacy benefit moved from Orrin Rx (to 31 December 2025) to Tallis Pharmacy Services (from 1 January
  2026). The January 2026 formulary bulletin removed step therapy for the weight-management GLP-1s, the severe-asthma
  biologics and the CGRP migraine drugs; new members started them in numbers and members who had stopped them since
  2023 came back. A hepatitis C outreach drive ran from May 2025. Personas from `guard.py names --geo "United States"
  --seed 468`: Erik Marks (Director of Pharmacy), John Henry (the plan's pharmacy data analyst), Caleb Fischer
  (Tallis's account manager).
- **Forcing fact:** the program year began on 1 July 2026; the staffing is set on the claims through 30 June and goes
  to the executive team at its first August meeting (charter 3.1). The call faces forward: the spend is the twelve
  months from July 2026, none of it observed.
- **Forum and forcing event:** executive_team, budget_or_appropriation; org family other (a nonprofit health plan, an
  insurer); role operations_director.
- **Data-native sentence:** a specialty member's spend over the next year depends on how long their current run on the
  drug has lasted (loading fills, early discontinuation, the near-lifelong persistence of those who stay), and a member
  who stopped and came back starts that run again; the 2026 caseloads of the three step-therapy classes hold 261 of
  1,846 (GLP), 81 of 287 (AST) and 268 of 941 (CGR) members back on the drug after a lapse, against 2 to 11 a year
  earlier, so any clock started at a member's first fill puts them with the persistent long-standing members.
- **The WHAT screen.** Population: the members on therapy in a class on 30 June 2026, by days' supply (charter 2.1),
  none added after; outcome: the 2026-schedule cost of their fills in the class (2.2); window: dispensed 1 July 2026 to
  30 June 2027 (2.2); unit: dollars, then whole pharmacists at $1.5 million or part (3.1); comparison: none, each class
  staffed on its own spend. The decisive step settles none of them: it is how the caseload's unobserved twelve months
  are estimated, and which clock indexes the development (HOW, forced by the data's structure: members back after a
  lapse spend like new starters at the same month of their episode, and the caseload's share of them moved).
- **Sources, one line each:**
  - `stumping/references/client/layer2-rigor-patterns.md`, payment-claims 1 and 4: completion and exposure; here the
    exposure clock is months in the current episode of therapy (pharmacy persistence work's new-user and re-initiation
    episodes), which no build on file carries.
  - `stumping/references/strategies.md` F5 and F7: a pool whose mix moved on a property rebuilt from a history (the
    episode), and replacements that restart a curve (132, a failed item restarts at the bottom of its wear curve).
  - `dataset-generation/references/layer1-messiness.md`: two PBM layouts, reversals and rebills, re-keyed member
    identifiers, 10- and 11-digit NDCs, contract repricing, mail-order long supplies; none on the decisive step.

## Default path

1. Conform `orrin_rx_specialty_claims_2019_2025.csv` and `tallis_specialty_claims_2026h1.csv`: drop reversed claims,
   link members through `member_id_crosswalk_2026.csv`, convert Orrin's 10-digit NDCs to 11 digits and map each to its
   class through `tallis_specialty_drug_list_2026.csv`, price each fill at `tallis_specialty_price_schedule_2026.xlsx`.
2. Take each class's caseload: the members whose fill's days' supply reaches 30 June 2026 (charter 2.1).
3. See that the program year is unobserved and that a member's next year depends on how long they have been on the
   drug; build each class's development of next-twelve-months spend by months since the member's first fill in the
   class from every month end whose twelve months the record holds, and apply it at each caseload member's months.
4. Staff one pharmacist per $1.5 million or part.

Ends on: 57 pharmacists, IMM 14, MS 7, ONC 6, HCV 1, GLP 8, HIV 6, AST 5, CF 4, CGR 6 (the first-fill development puts
the members back after a lapse with the persistent long-standing members: GLP 7.48, AST 4.23, CGR 5.62 pharmacists of
spend).
Golden: 54 pharmacists, IMM 14, MS 7, ONC 6, HCV 1, GLP 7, HIV 6, AST 4, CF 4, CGR 5, from the same development indexed
by months since the start of the member's current episode of therapy (a fill more than 60 days after every earlier
supply ran out starts one), applied at each caseload member's own months.

## Stump sentence

The default path develops each class's caseload by months since each member's first fill in the class and files 57
pharmacists with GLP 8, AST 5 and CGR 6, because the members who came back to those drugs in 2026 after a lapse are
counted at their first fill's months with the persistent long-standing members; developed by months since the current
episode began, the classes take GLP 7, AST 4 and CGR 5, 54 in all.

## Three rules

Task type: payment-claims-health-plan-analytics: two PBMs' specialty claim files conformed into one repriced record of fills by plan member, class and date, from which each class's program-year spend for its members now on therapy is projected, a task type serving Data Extraction & Conformation (ETL).

Domain test: the deciding quantity is each specialty class's spend over the program year for the members on therapy today, and the field's estimator is a persistence-and-cost development by months in the current episode of therapy (new-user and re-initiation episodes separated by a permissible gap, as pharmacy persistence work defines them), applied at each member's own months; the trailing year, the run-rate, last year's caseload and a clock started at first fill each move pharmacists between classes.

Swap: "the hospital's wards staffed by the bed-days their current inpatients will use" keeps an arithmetic shape but loses why it moves: a ward census has no fill, no days' supply, no lapse between episodes of a drug and no member coming back to a therapy they stopped, and the step-therapy change that brought them back has no counterpart.

Layer 1: Orrin Rx's file with reversals as negative lines and rebills under new claim numbers; Tallis's file with a status column, resubmissions and its own member numbers linked through the plan's crosswalk; 11-digit NDCs against Orrin's hyphenated 10-digit; Orrin's paid amounts at its own contract against the Tallis 2026 schedule; 28-, 30-, 84- and 90-day supplies with mail-order packages; late refills inside an episode. Each is the PBMs' systems as they run; none decides the call.

Layer 2: forecast_uncertainty, a development of spend by months in the current episode of therapy conditional on the months each current member has reached, estimated from every member who has passed each month of an episode.

Decisive step: indexing the development by months since the member's current episode of therapy began, so a member back on the drug after a lapse is projected like a new starter at that month, instead of by months since the member's first fill in the class (or last year's caseload, the trailing year, the run-rate).

Not semantics: every field read correctly (reversals, crosswalk, NDCs, the schedule, days' supply, the charter's caseload, spend and window) still leaves the careful route developing by months since first fill, because no field marks an episode, a lapse or a return; the episodes have to be built from each member's fill history across both PBMs' files, and the choice of clock is a modelling choice the record tests.

Not rule application: the charter fixes the caseload, the window, the prices and the staffing rule; no rule or procedure says how the caseload's next twelve months are projected or which clock indexes them, and executing every filed rule with the first-fill development files 57 pharmacists, so the step no rule performs is the episode clock.

Analyst test: a strong analyst who conforms both files, reads every charter rule and develops the caseload by months since each member's first fill files 57 pharmacists with GLP 8, AST 5 and CGR 6 (the default path's Ends on); counting the months from the start of each member's current episode files 54 with GLP 7, AST 4 and CGR 5.

Estimand: the Specialty Clinical Pharmacy Program charter (2.1 the members on therapy in a class on 30 June 2026 by days' supply; 2.2 the plan's spend on their fills in the class dispensed 1 July 2026 to 30 June 2027 at the Tallis 2026 schedule plus its fee, before cost sharing; 3.1 one pharmacist per $1.5 million or part), in the charter PDF.

No decoy: nothing is planted; the claim files are the PBMs' extracts as delivered, the drug list and schedule are Tallis's, the bulletin is the committee's notice of the step-therapy change and names no return, and no memo, draft or briefing argues a projection method or a staffing.

No certified replay: no published or certified figure reproduces under one projection only; Orrin's trend report (a distractor) states past spend by class on Orrin's prices and no staffing.

Lesson: a member's forward cost runs on the clock of their current episode of therapy, so a member who stopped and came back is a new user again; the decisive skill is to rebuild episodes from the fill history and index the development by them, which no build on file teaches.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0, the trailing year (62) | "managed spend for the program year" invites last year's spend: fires | the claim files' spend columns: fires | trailing-twelve-months spend is the budget reflex: fires | none | none | one sum per class: fires | readable |
| R1, the June run-rate times twelve (78) | none | the fill dates: fires | annualising the latest month: fires | none | none | one product: fires | readable |
| R2, last year's caseload's following year per member (62) | charter 2.1 names a caseload on a day, so a past caseload on the same day is the natural analog: fires | none | the cohort analog: fires | the record holds last year's caseload's full year: fires | none | one ratio per class: fires | readable |
| R2b, a development from first fill applied to every caseload member (45) | none | none | the textbook persistence curve starts at the first fill: fires | none | none | one curve per class: silent | readable |
| R3, the development by months since first fill at each member's months (57) | none | the first fill is the first row per member and class: fires | tenure since first fill is the careful analyst's reflex (architecture 2's reader took it): fires | the three earlier Junes' back-tests pass it (mean errors 3.6 and 3.0 per cent): fires | none | a cell per class and month: silent | readable |
| G (decisive), the same development by months since the current episode began (54) | no document names an episode, a lapse, a restart, a return, persistence or months on therapy (R1 assertion): silent | no column carries a start, a gap or an episode; episodes are built from each member's fill history across both files through the crosswalk: silent | the reflex clock is the first fill: silent | the back-tests pass both clocks equally, since returns were rare before 2026: silent | every file reconciles and no row is anomalous; a late refill and a return look alike until the gap is measured: silent | a cell per class and episode month over 78 month ends: silent | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | caseload | members whose fill's days' supply reaches 30 June 2026 | members with any fill in the last 30, 60 or 90 days | another caseload | charter 2.1 "a fill ... has a days' supply that reaches it" |
| SF2 | managed spend's price | units times the 2026 schedule's unit price plus its fee, before cost sharing | Orrin's paid amounts for the 2019 to 2025 fills, plan paid net of copay | Orrin's amounts give IMM 13 (asserted) | charter 2.2 "priced at the Tallis 2026 specialty price schedule ... before member cost sharing" |
| SF3 | the program year | fills dispensed 1 July 2026 to 30 June 2027 | days of supply falling in the year | none ships | charter 2.2 "dispensed from July 1, 2026 to June 30, 2027" |
| SF4 | a drug's class | its class code in Tallis's drug list | Orrin's product descriptions | same call: every NDC is listed (asserted) | charter 1.2 |
| SF5 | pharmacists | one per $1.5 million or part, a ceiling | rounding to the nearest | none ships | charter 3.1 "or part of $1.5 million" |
| SF6 | the duration cap | every month to 36, then pooled | capped at 12, 24 or 48 | same call (asserted) | the data |
| SF7 | the duration grain | single months | three- or six-month bands; the development chained month to month | same call (asserted) | the data |
| SF8 | a member filling in early 2019 | started before the file, pooled with the longest durations | started at that fill | another staffing | the transition notes: "may have been on the drug for years before that" |
| SF9 | managed spend's rounding | the nearest million | under every reading of SF6, SF7 and SF13 | same million in every class (asserted, nearest edge 0.13 million) | the data |
| SF10 | rebates on fills dispensed in 2025 (ask) | contract quarters 2025-Q1 to 2025-Q4 and January 2025 | the contract year read as the calendar year | the ask's figures move | the statement's units tie to the claims only on a February-to-January contract year (asserted) |
| SF11 | whose spend | the caseload members' fills only | every fill in the class in the program year | none ships | charter 2.2 "the plan's spend on its caseload members' fills in the class" |
| SF12 | a member across the PBM change | one member through the crosswalk | every Tallis member a new start | another staffing (asserted) | the crosswalk; the transition notes |
| SF13 | the lapse that starts a new episode | more than 60 days after every earlier supply ran out | 30, 90 or 180 days | same call (asserted): inside an episode a refill is never more than a few days late, and a return comes six months or more after the supply ran out | the data |

## Ladder

- **R0, the trailing year (62 pharmacists).** IMM 16, MS 8, ONC 8, HCV 4, GLP 6, HIV 6, AST 5, CF 4, CGR 5. Dies to the
  caseload: the year's spend includes members who stopped, the outreach's finished hepatitis C courses and loading fills.
- **R1, the June run-rate times twelve (78).** IMM 15, MS 8, ONC 8, HCV 4, GLP 14, HIV 6, AST 9, CF 4, CGR 10. Dies to
  the same fact and to June's new starters' loading fills.
- **R2, last year's caseload's following year per member (62).** IMM 14, MS 7, ONC 6, HCV 1, GLP 10, HIV 6, AST 6, CF
  4, CGR 8. Dies to the durations: the step-therapy classes' caseloads are mostly 2026 starters and returners.
- **R2b, the development from first fill applied to every caseload member (45).** IMM 12, MS 7, ONC 3, HCV 1, GLP 5,
  HIV 6, AST 3, CF 4, CGR 4. Dies to the caseload: its members have already reached their months.
- **R3, the analyst test: the development by months since first fill (57).** IMM 14, MS 7, ONC 6, HCV 1, GLP 8, HIV 6,
  AST 5, CF 4, CGR 6 (quotas GLP 7.48, AST 4.23, CGR 5.62). Dies to the record: members back after a lapse, early in
  the new episode, spend 0.53 (ONC), 0.43 (AST) and 0.56 (CGR) of what continuing members at the same months since
  first fill spend, and about what new starters at the same episode month spend (0.86 to 1.06); the caseload's share
  of them moved from 2 to 11 members a class to 81 to 268 in the step-therapy classes.
- **G, the decisive move (54).** IMM 14, MS 7, ONC 6, HCV 1, GLP 7, HIV 6, AST 4, CF 4, CGR 5; quotas 13.33, 6.67, 5.33,
  0.17, 6.67, 5.33, 3.33, 3.33, 4.66; managed spend 20, 10, 8, 0, 10, 8, 5, 5, 7 million.
- **Margins:** every reading in the fork table files the golden; R3 sits 0.48 (GLP), 0.23 (AST) and 0.62 (CGR) of a
  pharmacist past the golden's bin edges; every rung differs from the golden in at least three classes and the total.
- **Position, separation and dominance:** R0 and R1 err on the short-course and loading classes; R2 and R3 err only
  on the step-therapy classes, R2 more; R2b errs the other way. Only the episode clock moves GLP, AST and CGR down from
  R3 without moving another class.
- **Worth on the graded quantities:** the call (6), each class's pharmacists (2), each managed spend (1.5): R3 keeps 6
  of 9 pharmacists and 6 of 9 spends (main 21.0 of 37.5, generator/ceiling.py).
- **Grid:** Orrin's own prices move IMM (SF2, charter 2.2 rules them out); the crosswalk ignored moves several classes
  (SF12); every reading of SF6, SF7 and SF13 files the golden.

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | the members on therapy in each class on 30 June 2026 by days' supply (charter 2.1); no member added after (SF11) |
| 2 | Unit of account | the member in a class; spend in dollars, pharmacists whole |
| 3 | Attribution window | fills dispensed 1 July 2026 to 30 June 2027 (charter 2.2, SF3) |
| 4 | As-of dating | the claims through 30 June 2026 (charter 3.1); both files end there |
| 5 | Version basis | one version of every file; reversed claims out (charter 2.2 "A reversed claim is not spend") |
| 6 | Denominator | none: each class's spend is a total |
| 7 | Weighting | each caseload member once at their own months; the development cells pool every month end |
| 8 | Window length | twelve months |
| 9 | Boundary inclusivity | a fill whose days' supply reaches 30 June counts (2.1: "dispensed on or before that day") |
| 10 | Rounding path | spend unrounded to the staffing, rounded to the million for reporting (SF9) |
| 11 | Tie-break | none: each class is staffed on its own spend |
| 12 | Maturity and censoring | the program year is unobserved; the development uses only month ends whose twelve months the record holds; members filling in early 2019 pooled with the longest durations (SF8) |
| 13 | Order of operations | conform, price, caseload, episodes, development, projection, ceiling |
| 14 | Row order | no dependence |
| 15 | Duplicate resolution | a reversed claim and its original out, the rebill kept; Tallis R lines out with their claims, resubmissions kept |
| 16 | Identity normalisation | Orrin keys and Tallis numbers to plan member IDs through the crosswalk (SF12) |
| 17 | Netting | spend before cost sharing (SF2) |
| 18 | Dimensional units | 10-digit 5-3-2 NDCs padded to 11; units per package from the drug list and schedule |
| 19 | Code and status semantics | class codes from the drug list (SF4); Orrin REVERSAL and Tallis R lines; never the stump |
| 20 | Integerisation | pharmacists a ceiling at $1.5 million (SF5) |
| 21 | Clause scope | charter 2 and 3 for the call, 4.1 and the prompt for the rebates; the bulletin's step-therapy change from January 2026 |
| 22 | Forward window contents | the twelve months from July 2026, none observed; the call faces forward |

## Literal reader

Executed word for word, the charter fixes the caseload (2.1), the spend's basis and window (2.2) and the staffing rule
(3.1), and leaves one thing open: how the caseload's spend over the unobserved program year is estimated. The candidates
are the trailing year (R0), the run-rate (R1), last year's caseload (R2), a development from first fill applied to
everyone (R2b), the development by months since first fill (R3) and the development by months in the current episode
(G). The data separates them: a member's next twelve months depend on how long their current run on the drug has
lasted; members back after a lapse spend 0.43 to 0.56 of continuing members at the same months since first fill and
0.86 to 1.06 of new starters at the same episode month (checks.py, oral oncology, severe asthma, CGRP); and the
step-therapy classes' caseloads now hold 81 to 268 such members. Every reading of G's construction (gaps of 30 to 180
days, caps 12 to 48, one-, three- and six-month bands, the month-to-month chain) files the same 54 and the same spend
to the million (checks.py). Every write-up step names the file and rule it executes.

## Oracles

None. Nothing ships a staffing, a projection or a past caseload's cost; Orrin's trend report (a distractor) gives
2024 to 2025 spend by class on Orrin's prices and ranks no staffing; the medical-benefit drug list (a distractor) is
outside the program by charter 1.1; the back-tests a solver may run pass the first-fill clock and the episode clock
alike. The rebate statement is the ask's file and the projection never reads it.

## Ask sheet

- **Ask A, each class's manufacturer rebates on its fills dispensed in 2025 (nearest thousand dollars): nine figures.**
  H18 home: charter 4.1 reports each class's rebates on the previous year's utilization beside its staffing. Path:
  `orrin_rx_rebate_statement_2025.xlsx` (invoice quarter, contract quarter, product, class code, channel, units,
  rebate) and the Orrin claims for January 2025.
  Primary device: D8, periods off the calendar. Orrin's rebate contract year runs February to January, and the
  statement labels its periods 2024-Q1 to 2025-Q4 with no month or date anywhere; read as calendar quarters, contract
  year 2025 (February to December 2025, Orrin's run-off ending in December) drops January 2025's fills, which sit in
  contract quarter 2024-Q4 at the 2024 contract's lower rate per unit. Only reconciling the statement's units to the
  claims finds it: on calendar quarters 133 of 136 product-quarters fail to tie, on February-to-January quarters every
  one ties.
  Hazard: D6, each product-quarter's rebate stands on each of its two to four channel lines, the same amount on each
  (architecture 2's reader caught it on sight; it stays as a hazard that moves every figure).
  Stops (asserted, checks.py and generator/ceiling.py): the contract year read as the calendar year, each
  product-quarter once, misses 9 of 9; every 2025 line summed misses 9 of 9; the 2025 invoices, each product-quarter
  once, miss 8 of 9 (cystic fibrosis coincides); the February-to-January reading with January 2025 at 2024-Q4's rate
  per unit gives all 9.
  Realism: rebate contracts run on the manufacturer's contract year, and statements report the contract's own periods;
  per-unit rates change at the contract year.
- **The construction layer:** the caseloads, the nine managed spends and the chart; the cracker has them.
- **Separation (asserted):** the call reads no rebate; the statement is not read by the projection.
- **Referee:** none.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| A, each class's rebates on its fills dispensed in 2025 | counts each product-quarter's rebate once (the repetition is seen) and takes contract quarters 2025-Q1 to 2025-Q4 as calendar 2025; January 2025's fills, in contract quarter 2024-Q4, are left out | miss |

- Mirror leakage: 11.1 per cent of ask weight (the best mirror, R3, takes the 2025 invoices and keeps cystic fibrosis
  only: generator/ceiling.py).
- Pair ceiling: 39.3 (planning weights 38 / 7 / 55: the call 6, each class's pharmacists 2, each managed spend 1.5, each
  rebate 55/9; the cracker keeps the main block and instructions, 44.5; the mirror on R3 keeps 6 pharmacists, 6 spends
  and 1 rebate, 34.1; average 39.3), rerun from the generated rubric at ship.
- Measured by: generator/ceiling.py on the cut pack.

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
