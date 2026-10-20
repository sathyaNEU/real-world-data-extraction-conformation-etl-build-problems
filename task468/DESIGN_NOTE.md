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
  claims extract (one row per bill, replacements and voids, a claims platform change on 1 January 2026), the delegated
  Carrisford Medical Group's encounter file (pipe-delimited, its own member numbers, MM/DD/YY dates, replacements and
  deletions), the enrollment extract, the members' service lines, the state Office of Vital Records' death linkage
  return, the plan's HIMM 3.2 risk scores and the network hospital list; the call turns on what that dataset says each
  hospital's 30-day deaths were.
- **Shape:** 10, a scorecard: each of 14 network hospitals' fiscal 2026 mortality ratio (deaths over expected deaths)
  against the bonus line of 1.15. Criteria: the count and the set (1), each hospital's verdict (14), the chart's parts
  (the ratios, the line, the losers marked: 3), each hospital's bonus at stake (14), the network total (1) and the file
  (1): 34.
- **Strategy:** other (a linked outcome count corrected for the linkage's own false links and missed links, each
  measured on a control group inside the record), decisive generator G3 (a link record is not a death), with G12 (no link
  is not survival) and G14 (the error rates are conditional on the member's identifier class).
- **World:** the United States, an unnamed state that covers adults regardless of immigration status through Medicaid
  managed care, so members can be enrolled without a Social Security number. Halbrook Community Health Plan, a nonprofit
  Medicaid plan, pays each of its 14 network hospitals a Hospital Quality Bonus of 2 per cent of inpatient payments in
  contract year 2027 unless the hospital's ratio for fiscal 2026 index admissions (July 2025 to June 2026) exceeds 1.15
  (specification 5.2). Deaths after discharge reach the plan through its own later bills and the state Office of Vital
  Records' probabilistic linkage of plan members to the state death file (SSN pass, then name, date of birth and sex).
  Varden Surgical Hospital's members without a number are young workers in for surgery or an injury, carrying the
  commonest surnames in the plan; Mercy Valley Medical Center runs the region's dialysis program, and its members
  without a number carry two-part surnames and die often; Brannock Medical Center's members without a number are mostly
  two-part surnames too. Personas from `guard.py names --geo "United States" --seed 468`: Wendy James (Vice President,
  Provider Contracting and Payment, who owns the call), Nathan Hawkins (the plan's quality measurement analyst) and Eric
  Thomas (manager of the Office of Vital Records Linkage Unit).
- **Forcing fact:** the plan files its 2027 value-based payment arrangements with the state by 1 November 2026; the
  bonus is set on the fiscal 2026 index admissions, whose last 30-day window closed on 30 July 2026, with claims paid
  through 30 September 2026 and the Office's return of 7 October 2026. The call faces forward (who is paid the 2027
  bonus); its quantity is the closed fiscal 2026 year, which the bonus terms name as the basis (retrospective, with its
  reason: a pay-for-performance bonus is earned on a closed measurement year).
- **Forum and forcing event:** executive_team, statutory_or_regulatory_filing; organisation other (a nonprofit Medicaid
  health plan); role finance_controller.
- **Data-native sentence:** the linkage keys a member to the death file by Social Security number when the enrollment
  file has one and by name, date of birth and sex when it does not, so for the members enrolled without one it links
  living members with common names to other people's deaths and misses deaths for members whose surnames are written
  in two parts; Varden's young workers without a number carry the commonest surnames and rarely die, and Mercy Valley's
  and Brannock's members without a number carry two-part surnames, so one hospital's ratio is inflated by deaths that
  did not happen and the others' deflated by deaths the linkage never found, and the plan's own records show both
  errors only for the members whose later claims or bills happen to.
- **The WHAT screen.** Population: the measure's index admissions at each hospital (specification 2.1 to 2.4); outcome:
  death from any cause on or before day 30 after the admission date, in hospital or after discharge (3.1; a hospital's
  deaths are the number of its index admissions that end in death, 3.2, the event and not a source); window: fiscal 2026
  admissions; unit: deaths over the sum of HIMM 3.2 scores (4, 5.1); comparison: each hospital against 1.15 (5.2). The
  decisive step settles none of them: it is how the deaths after discharge are estimated from a linkage the Office says
  errs both ways (HOW, forced by the data's structure: links on members whose later records show them alive, and
  deaths the bills record that the linkage did not find, both varying with the member's identifier class).
- **Sources, one line each:**
  - `stumping/references/client/layer2-rigor-patterns.md`, payment-claims: outcome ascertainment through linkage; here
    the correction is the epidemiologist's misclassification estimator (the share linked among known deaths, the share
    linked among the known living), stratified by what drives the linkage's error, which no build on file carries.
  - task456 (three capacity feeds' miss and false-flag rates identified by agreement) and task455 v1 (an error matrix
    from a medical examiner's review): both correct a classified count for its errors; here the errors are measured on
    control groups the claims system creates by itself, and the decisive move is the stratification the error rates
    need, not the identification of the rates.
  - `dataset-generation/references/layer1-messiness.md`: two payers' layouts, replacements and voids, a platform change,
    an NPI change, dates in four formats, a member crosswalk; each asserted neutral on the call.

## Default path

1. Conform Halbrook's inpatient claims and Carrisford's encounters into stays (voided and deleted bills out, each stay
   as last corrected, Carrisford member numbers through the enrollment file, both of Mercy Valley's NPIs), and keep the
   index admissions of specification 2.1 to 2.4.
2. Sum each hospital's HIMM 3.2 scores for the expected deaths.
3. Count each index admission's death within 30 days: patient status 20 on the stay or a stay continuing it, and the
   Office's linkage return for the deaths after discharge.
4. The careful analyst's reflexes, since the Office says it misses deaths and links members to deaths not theirs: add
   the deaths later bills record (status 20 inside the 30 days) that the linkage did not return, and drop each link a
   later service line, admission or live discharge contradicts.
5. Divide each hospital's deaths by its expected deaths and withhold the bonus above 1.15.

Ends on: four hospitals lose the bonus, Varden, Calloway, Northgate and Westover (Varden at 1.33), while Mercy Valley
(1.05) and Brannock (1.03) keep it.
Golden: each hospital's deaths after discharge corrected class by class (Social Security number on file; otherwise a
single or a two-part surname): among the index admissions neither recorded dead nor seen alive after day 30, the links
less the false links expected at the share of the class's living members linked, divided by the class's share of
recorded deaths linked less that false-link share; five lose it, Calloway (1.33), Mercy Valley (1.30), Northgate
(1.55), Brannock (1.25) and Westover (1.45), and Varden keeps it (1.03).

## Stump sentence

The default path counts each hospital's recorded deaths and the Office's links, adds the deaths later bills record and
drops the links later claims contradict, and files four losers with Varden at 1.33 and Mercy Valley (1.05) and
Brannock (1.03) keeping the bonus, because for members enrolled without a Social Security number the linkage links
living members with common names to other people's deaths and misses the deaths of members with two-part surnames, and
those repairs reach only the members whose later records happen to show the error; corrected class by class at the
rates the recorded deaths and the living members measure, Varden keeps the bonus and Mercy Valley and Brannock lose
it, five losers in all.

## Three rules

Task type: payment-claims-health-plan-analytics: a Medicaid plan's claims, a delegated group's encounters, enrollment, service lines and the state's death linkage conformed into a hospital outcome measure, a task type serving Data Extraction & Conformation (ETL).

Domain test: the deciding quantity is each hospital's 30-day mortality ratio, deaths over expected deaths, where the deaths after discharge come from a probabilistic linkage to vital records, and the field's estimator corrects a linked outcome count for linkage error (the share of true deaths found and the share of the living falsely linked, each measured on a validation group and applied within the strata that drive the error, as outcome-ascertainment studies do); counting links, or repairing only the links the records contradict, moves three hospitals.

Swap: "which schools lose a grant on the students who left without a diploma, as a state's enrollment records link them" keeps a count from a linkage but loses why it moves: no risk-adjusted 30-day mortality, no deaths the hospitals' own bills record as a validation group, no Social Security number missing by coverage rule, and no two-part surnames among a dialysis program's patients.

Layer 1: Halbrook's claims extract with replacements (0117) and voids (0118) and a platform change on 1 January 2026; Carrisford's pipe-delimited encounters with its own member numbers, MM/DD/YY dates, replacements and deletions; Mercy Valley's NPI change; transfers forming one stay; deliveries, children and discharges against advice to leave out; risk scores keyed by member, date and NPI; four date formats. Each is the systems as they run, and each handled the wrong way leaves the five losers unchanged (checks.py SF1 to SF7).

Layer 2: estimation_fit: the linked deaths corrected for the linkage's false links and missed links at rates measured on two control groups inside the record (the deaths the bills record, the members whose later records show them alive), stratified by the member's identifier class.

Decisive step: estimating each hospital's deaths after discharge class by class from the links among the admissions no control reaches, removing the false links the class's living members show and dividing by the share of deaths the class's recorded deaths show the linkage finds, instead of counting the links, repairing only the contradicted ones, or correcting at a network or match-pass rate.

Not semantics: every field and code read correctly (patient status 20, the replacements and voids, the linkage's passes, the enrollment's missing numbers, the specification's death within 30 days of admission, and the Office's sentence that its linkage misses deaths and links members to deaths not theirs) still leaves the careful route repairing the visible errors and filing Varden, Calloway, Northgate and Westover, because nothing marks which remaining links are false or which unlinked members died.

Not rule application: the specification fixes the index admissions, the outcome, the expected deaths and the 1.15 line; no rule or procedure says how deaths after discharge are estimated from an imperfect linkage, and executing every filed rule with the linked and recorded deaths files four losers with Varden among them, so the step no rule performs is the correction and its stratification.

Analyst test: a strong analyst who conforms both payers' stays, applies every specification rule, adds the deaths later bills record and drops the links later claims contradict files four losers, Varden (at 1.33), Calloway, Northgate and Westover, with Mercy Valley (1.05) and Brannock (1.03) keeping the bonus (the default path's Ends on); correcting the links class by class at the control groups' rates files five, Calloway, Mercy Valley, Northgate, Brannock and Westover.

Estimand: the Hospital Quality Bonus measure specification (2.1 to 2.4 the index admissions; 3.1 and 3.2 a hospital's deaths are the number of its index admissions whose member died, of any cause, by day 30 after admission; 4.1 and 4.2 expected deaths the sum of HIMM 3.2 scores; 5.1 and 5.2 deaths over expected, over 1.15 loses), in HCHP_Hospital_Quality_Bonus_2027_Measure_Specification.pdf.

No decoy: nothing is planted; the claims, encounters, enrollment and service lines are the systems' extracts as delivered, the linkage return and its methods note are the Office's own, the note's one sentence on error is the honest statement every linkage carries and gives no size, class or direction, and no memo, draft, dashboard or briefing ranks the hospitals on mortality or argues a method.

No certified replay: no published or certified mortality figure ships; the quality dashboard's readmission ratios (a distractor) measure another outcome on other stays and rank nothing the call reads.

Lesson: a linked outcome count is a classification with errors that vary with how well each record can be linked, so it is estimated, not counted, from the records' own validation groups within the strata that drive the error; repairing the errors you can see leaves the ones you cannot, which no build on file teaches.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0, recorded deaths and the links (4 lose, Varden 1.91) | specification 3.3 names the Office's linkage as a source of deaths: fires | the return file's rows carry a date of death per admission: fires | counting linked deaths is the default: fires | none | none | one join: fires | readable |
| R1, plus the deaths later bills record (4 lose) | 3.3 names the bills' status 20: fires | status 20 on later stays: fires | completing deaths from claims is a reflex: fires | none | none | one join: fires | readable |
| R2, less the links later claims contradict, the default path (4 lose, Varden 1.33, Mercy Valley 1.05, Brannock 1.03) | the Office's sentence on links not theirs sends a reader to look for contradictions: fires | service lines dated after a linked death: fires | dropping impossible links is the hygiene reflex: fires | none | claims after death is a standard check: fires | one filter: fires | readable |
| R3, one error corrected alone (false links only: 3 lose; missed deaths only: 6 lose) | the Office's sentence names both errors: fires | none | correcting the error one notices: fires | the recorded deaths or the living members: fires | none | one ratio: fires | readable |
| R4, both corrected at a pooled rate (network rate: 4 lose; by number on file or the link's pass: 5 lose with Varden; each hospital's own rate: 6 lose) | the sentence names both errors: fires | the return's MATCH_PASS column offers the pass as the stratum: fires | an average rate or each unit's own rate is the reflex: fires | the two control groups give the rates: fires | none | one estimator per hospital or pass: silent | readable |
| G (decisive), both corrected class by class (number on file; otherwise single or two-part surname), applied to the admissions neither control reaches (5 lose) | no document names a class, a surname's structure, a rate, a control group, a validation group or a correction (R3c): silent | no column carries a class: the surname's structure is read off the enrollment's last names, and the pass exists only on linked rows: silent | the reflex strata are the pass and the hospital: silent | the controls measure whatever strata a reader picks and refute nothing unless split by class: silent | every file reconciles, no row is anomalous: silent | an estimator per class and hospital over 34,500 admissions and three error rates: silent | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | index admission | specification 2.1 to 2.4: both payers' stays as last corrected, adults, no delivery DRG, no status 07, each member's first | Carrisford left out; voided bills kept; every eligible admission; deliveries or discharges against advice kept | same call (asserted, SF1a to SF1e) | specification 2.1 to 2.3; the five losers unchanged under each |
| SF2 | a hospital's deaths | the number of its index admissions whose member died by day 30 | the deaths the bills and the links record | the links as deaths file four losers with Varden | specification 3.1 and 3.2 (the event, not a source) and the Office's note: "some deaths of plan members are not found and some members are linked to a death that is not theirs" |
| SF3 | within 30 days | day 0 the admission date, deaths through day 30 | through day 29 | same call (asserted) | specification 3.1 |
| SF4 | expected deaths | the sum of the index admissions' HIMM 3.2 scores | another model or the scores of every admission | none ships; every index admission has a score (asserted) | specification 4.1 and 4.2 |
| SF5 | exceeds 1.15 | strictly greater | at or above | same call: no ratio within 0.05 of the line (asserted) | specification 5.2 |
| SF6 | a transfer | one index admission at the first hospital | the receiving stay counted apart | same call (asserted) | specification 2.4 |
| SF7 | Mercy Valley's stays | both NPIs | the first NPI only | same call (asserted) | the network hospital list; the extract notes |
| SF8 | the identifier class | number on file from ssn_last4; otherwise two-part surname from a space or hyphen in last_name | number on file split by surname too; a space only | same call (asserted, SF8a, SF8b) | the data: each reading selects the same five |
| SF9 | seen alive after day 30 | a service line, an admission or a live discharge dated after day 30 | service lines only; day 30 counted | same call (asserted, SF9a, SF9b) | the data |
| SF10 | the recorded deaths that measure the linkage's finding | every death the bills record inside the 30 days | deaths in hospital only | same call (asserted) | the data |
| SF11 | whose rates | each class's rates pooled across the network | each hospital's own class rates where its controls allow | same call (asserted) | the data |
| SF12 | the divisor | the share linked less the false-link share | the share linked | same call (asserted) | the data |
| SF13 | contradicted links among the admissions no control reaches | kept, the class's false-link share removing them in expectation | dropped first | same call (asserted) | the data |
| SF14 | which link is an admission's | the return row for that member and admission date | any of the member's links dated inside the 30 days | same call (asserted) | the Office's note ("Halbrook's member identifier and the admission date as Halbrook sent them") |

## Ladder

- **R0, the links as deaths (4 lose):** Varden 1.91, Calloway, Northgate, Westover; Mercy Valley 1.05 and Brannock
  1.05 keep. Dies to the Office's sentence and the bills: deaths the bills record are missing from the links, and some
  linked members are later seen alive.
- **R1, plus the deaths later bills record (4 lose):** the same four. Dies to the contradicted links.
- **R2, the default path: less the links later claims contradict (4 lose):** Varden 1.33, Calloway 1.31, Northgate 1.51,
  Westover 1.43; Mercy Valley 1.05, Brannock 1.03. Dies to the record: among the members later seen alive the
  linkage linked 20 of 1,179 single-surname members without a number and 12 of 21,855 with one, and it found 78 of 162
  recorded deaths of two-part-surname members without a number against 829 of 836 with one; the repairs reach only the
  members whose later records show the error.
- **R3a, the false links removed alone (3 lose):** Calloway, Northgate, Westover; Mercy Valley 1.04 and Brannock 0.98
  keep. Dies to the missed deaths.
- **R3b, the missed deaths added alone (6 lose):** Varden 1.70 with the golden five. Dies to the false links.
- **R4a, both corrected at one network rate (4 lose):** Varden 1.61; Mercy Valley 1.11 and Brannock 1.08 keep. Dies to
  the classes: the network rate is the members with a number.
- **R4b, both corrected by number on file, which is the link's pass (5 lose):** Varden 1.74 in, Brannock 1.12 out.
  Dies to the surnames: without a number, single surnames are linked to others' deaths at 1.7 per cent and found at 92
  per cent, two-part surnames at 0.5 and 48.
- **R4c, both corrected at each hospital's own rates (6 lose):** Varden 1.43 in; by number on file within each
  hospital, Varden 1.28 in. Dies to the controls: Varden's members are mostly alive and its recorded deaths have no
  member without a number, so its own rates borrow the network's or the pass's.
- **G, both corrected class by class (5 lose):** Calloway 1.33, Mercy Valley 1.30, Northgate 1.55, Brannock 1.25,
  Westover 1.45; Varden 1.03, Fairhaven 1.09 the highest keeper. Every hospital's class among the admissions no
  control reaches carries at least the links its false-link share expects, so no class's estimate falls below zero and
  a floored and an unfloored correction agree to the decimal (checks.py C1, C1b).
- **Margins:** every golden ratio at least 0.05 from 1.15 (Fairhaven 1.09 the nearest); every reading in the fork
  table files the same five; R2's distinguishing hospitals sit 0.18 (Varden), 0.10 (Mercy Valley) and 0.12 (Brannock)
  from the line.
- **Position and dominance:** R0 to R2 differ from the golden on the same three hospitals; R3 and R4 each fix one of
  them and keep another wrong; only the class-by-class correction moves Varden down and Mercy Valley and Brannock up
  together.
- **Worth on the graded quantities:** the call (10), each verdict (2): R2 keeps 11 of 14 verdicts (main 22 of 38),
  R3b and R4c 13 of 14 (26 of 38).
- **Grid:** every partial correction and every pooling is a named wrong set (R3a, R3b, R4a, R4b, R4c); the Layer 1
  mishandlings leave the five (SF1, SF6, SF7).

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | index admissions under specification 2.1 to 2.4, both payers (SF1); members not yet seen are irrelevant, the year is closed |
| 2 | Unit of account | the index admission; a hospital's deaths a count of admissions ending in death (3.2) |
| 3 | Attribution window | admissions July 1, 2025 to June 30, 2026; a death on or before day 30 (3.1, SF3) |
| 4 | As-of dating | claims paid through September 30, 2026; scores of October 2; the Office's return of October 7; every window closed July 30 |
| 5 | Version basis | each stay as last corrected; voided and deleted bills out (2.1, SF1b) |
| 6 | Denominator | expected deaths, the sum of HIMM 3.2 scores (4.2, SF4) |
| 7 | Weighting | none: each admission counts once in deaths and in expected deaths |
| 8 | Window length | 30 days after admission (3.1) |
| 9 | Boundary inclusivity | day 30 counts (3.1: on or before the 30th day); same call without it (SF3) |
| 10 | Rounding path | ratios unrounded against 1.15, reported to two decimals; no ratio within 0.05 of the line (SF5); each bonus figure 15 to 35 dollars off its cell's centre and the total 49 from its edge (checks.py A2, A2b, A3) |
| 11 | Tie-break | none: each hospital stands on its own ratio |
| 12 | Maturity and censoring | every window closed; the claims run two to fourteen months past day 30, the evidence of life after day 30 is what the record shows (SF9) |
| 13 | Order of operations | conform, index, expected, recorded deaths, classes, rates, correction, ratio |
| 14 | Row order | no dependence |
| 15 | Duplicate resolution | a duplicate bill voided, a duplicate encounter deleted; a death linked to several of a member's records counted once, on the index admission's record (SF14) |
| 16 | Identity normalisation | Carrisford member numbers through the enrollment file; Mercy Valley's two NPIs (SF7) |
| 17 | Netting | none on the call; the ask's payments net replacements and voids as each system recorded them (filed in the extract notes) and add each dispute award once |
| 18 | Dimensional units | probabilities summed to deaths; dates in four formats |
| 19 | Code and status semantics | patient status 20 a death in the stay, 02 a transfer, 07 against advice; delivery MS-DRGs; never the stump |
| 20 | Integerisation | none on the call; the bonus figures to the nearest $100 |
| 21 | Clause scope | specification 2 to 5 for the call, 5.3 and the prompt for the bonus at stake |
| 22 | Forward window contents | the 2027 bonus, set on the closed fiscal 2026 year |

## Literal reader

Executed word for word, the specification fixes the index admissions (2.1 to 2.4), the outcome as the member's death
by day 30 whatever its source (3.1, 3.2), the expected deaths (4) and the line (5.2), and the Office's note says its
linkage both misses deaths and links members to deaths not theirs, so the links are not the deaths and one thing is
left open: how each hospital's deaths after discharge are estimated. The candidates are the links counted (R0), with
the bills' deaths added (R1) and the contradicted links dropped (R2), one error corrected alone (R3), both corrected at a
network, pass or hospital rate (R4) and both corrected class by class (G). The data separates them: within the
members without a number, single surnames are linked to others' deaths at 1.7 per cent of the living and two-part
surnames at 0.5, and the linkage finds 92 per cent of the former's recorded deaths and 48 per cent of the latter's, so
a rate pooled across them misstates the hospitals whose members without a number are mostly one or the other; every
reading of the class-by-class correction in the fork table (four classes, a space only, each hospital's own class rates,
recorded deaths in hospital only, the plain divisor, contradicted links dropped first, evidence of life by service line
only or from day 30, links by member and date, deaths to day 29) files the same five (checks.py SF3, SF8 to SF14). Every
write-up step names the file and the rule it executes.

## Oracles

None. No file ranks the hospitals on mortality or states a death count, a ratio or a linkage error rate; the quality
dashboard (a distractor) gives readmission ratios on other stays and ranks nothing the call reads; the hospital profiles
(a distractor) list services; the Office's note states that the linkage errs and no size or direction; the control
groups measure whatever strata a reader picks and refute nothing unless split by class.

## Ask sheet

- **Ask A, each hospital's bonus at stake, 2 per cent of what Halbrook paid it for inpatient stays discharged in fiscal
  2026 (nearest $100), and the network total: fifteen figures.** H18 home: specification 5.3 states each hospital's
  bonus at stake in its notice and in the 2027 budget; the figure is the dollars each verdict moves. Use: the notices
  and the budget line. Path: hchp_ip_claims_extract_2026-10-05.csv (claim_number, type_of_bill,
  original_claim_number, billing_npi, statement_thru_date, paid_date, paid_amount), the extract notes (the two systems'
  replacement and void conventions), HCHP_Provider_Dispute_Log_IP_2026-10-01.xlsx (Provider NPI, Claim No., Discharge
  Date, Determination, Additional Payment, Payment Date), the network hospital list (both NPIs), the specification (5.3)
  and Carrisford's file layout (not Halbrook's payments): six files, sixteen columns.
  Primary device: D1, the same payment in two sources. Provider Disputes logs every determination with the additional
  payment it found and the day that payment was made. An overturned DRG dispute is paid by reprocessing the bill at the
  hospital's DRG, so its payment is also the replacement bill in the claims extract, paid that day and changing the
  stay's payment by exactly the award; a settled DRG dispute and every outlier and rate award are paid by Finance outside
  the claims system and appear only in the log. Neither file says which: the log's notes define the additional payment
  and its day, the extract notes the bills. Adding every paid award counts each reprocessed one twice; leaving the log
  out misses Finance's awards. The records show which is which: of the paid awards on bills in the extract, 212 are a
  replacement of the disputed claim paid on the award's day whose change equals the award to the cent, 266 have no bill
  after their determination, and none is neither (checks.py A16).
  Hazards: the replacement and void conventions (filed in the extract notes since the judge's first pass), decisions not
  yet paid and disputes pending, the amount disputed against the amount awarded, the award's payment day against the
  stay's discharge, Carrisford's own payments (5.3 leaves them out), the admission date for the discharge date, Mercy
  Valley's second NPI.
  Stops (asserted, checks.py A5 to A15 and generator/ceiling.py): every paid award added, the cracker's handling, misses
  all 15 (each hospital $261 to $2,157 high); the log left out misses all 15 ($303 to $2,059 low); every award decided,
  paid or not, misses all 15; the amount disputed misses all 15; awards by the day they were paid keeps 7 of 15; a
  replacement in its original's place, every line summed, every replacement added, the admission basis and Carrisford's
  payments added each miss all 15; the golden gives all 15 and equals the clean truth (A4).
  Realism: a plan's dispute unit logs every determination and its payment while the claims unit and Finance pay by their
  own routes; an analyst who reconciles the log with the claims finds the reprocessed awards, one who adds the log to the
  claims counts them twice.
- **The construction layer:** the call, the fourteen verdicts and the chart; the cracker has them.
- **Main population zero-counts (asserted):** the call reads no paid amount and no dispute: with every paid_amount
  blanked, or the dispute log emptied, the determination is unchanged (checks.py S1, S3).
- **Hazard table (asserted):** the dispute log's two channels move all 15 figures; the conventions move all 15 when
  misread; Carrisford's payments move the six delegated hospitals and the total; the admission basis moves all 15;
  Mercy Valley's second NPI unmapped moves Mercy Valley and the total; none moves the call.
- **Referee:** none; no file states a payment total or ties the log to the bills.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| A, each hospital's bonus at stake and the network total | keeps each bill as the system that paid it recorded it (the filed conventions), leaves Carrisford's stays out, takes stays discharged in fiscal 2026, maps both of Mercy Valley's NPIs, and adds every additional payment the dispute log shows made on those stays, so each award a reprocessed bill already carries is counted twice | miss |

- Mirror leakage: 0.0 per cent of ask weight (every rung builds the payments the cracker's way and misses all 15:
  generator/ceiling.py).
- Pair ceiling: 39.0 (weights 38 / 7 / 55: the call 10, each verdict 2, each of the 15 bonus figures 55/15; the cracker
  keeps the main block and instructions, 45.0; the best mirror, R3b or R4c, keeps 13 of 14 verdicts, 33.0; average
  39.0), rerun from the generated rubric at ship.
- Measured by: generator/ceiling.py on the cut pack.

## Pre-ship check

- **Three rules, re-read against the built pack.** Domain: the deciding quantity is each hospital's fiscal 2026 30-day
  mortality ratio, deaths over HIMM 3.2 expected deaths, with the deaths after discharge estimated from the Office's
  linkage corrected for its false and missed links class by class, the way outcome-ascertainment studies correct a
  linked count; on the clean truth the easy route files the default path's four and the correction alone the golden
  five (checks.py R1, R2). Two layers: the Layer 1 items in `## Three rules`, each asserted neutral on the call (SF1 to
  SF7, SF9, SF14); the ask's device lives in the dispute log and the paid amounts, which the call never reads (S1, S3).
  The decisive step is none of the three banned kinds: not a plant (R3c: no document names a class, a rate, a control
  group or a correction; no memo, draft or briefing ships), not data semantics (every term in the fork table read right
  still leaves the reflex repair on four losers), not rule application (R3: every filed rule executed with the links as
  deaths files a wrong set).
- **Convergence.** Every hospital's class among the admissions no control reaches carries at least its expected false
  links, so a floored and an unfloored estimate agree to the decimal (C1, C1b): the judge's first-pass difference
  (Calloway, Varden, Fairhaven at the first decimal) cannot recur under either reading.
- **Gates.** 14 files in 4 formats (csv, pdf, txt, xlsx); the service-line extract at 324,402 rows; two distractors
  (the readmissions dashboard and the hospital profiles), unread by the solution (S2); checks.py 70 rows green;
  verify.py from the bundle alone matches; two builds byte-identical (target.zip f511b179e6742bf8); figures_check.py,
  precut.py and voice-check.py exit 0; leak.py REVIEW, no LEAK; guard heart WARN (Gate G overuse, a first name in an
  older build), the surface screen promoting the same six card-axis pairs as at the draw, each answered by the
  differentiation lines on the card, the adjudicated clone check the author's to call; the containers normalised in
  build.py.
- **Bonus figures.** Each hospital's bonus 15.9 to 34.9 dollars off its cell's centre and the total 48.9 from its edge
  (A2, A2b, A3); the payments no longer land near round figures.
- **Pair ceiling.** 39.0 by generator/ceiling.py (the cracker adds every paid award and misses all 15; the best mirror on
  R3b or R4c, 33.0), mirror leakage 0; both shipping-pack readers kept 0 of 15.

## Leak check

`leak.py --asof 2026-10-09`: REVIEW, no LEAK. Each REVIEW line answered: the specification carries the hospital names
and the bonus's name (Exhibit A and section 1, the contract itself) and ranks nothing; the profiles list beds and
services; the layout, the specification, the Office's note and the extract notes share the measure's own words (deaths,
members, records, admissions, the Office) and name no class, rate, control group or correction; the dispute log and the
readmissions dashboard name the hospitals beside dispute amounts and readmission ratios, neither on the call.

Readers on the shipping pack (two, each on its own fresh unzip, scored; answers in `leak_check_report.md`): both missed
the call on the default path's four (Calloway, Northgate, Varden, Westover), each dropping the name-pass links a later
service line contradicts and adding no missed deaths; both kept 0 of 15 bonus figures, adding every paid dispute award
($7,086,700 against the golden $7,073,300); score_reader exit 0 twice. Question 1 quoted nothing that names the step;
question 6 an analytical choice both times; question 3 named the service-line extract (the plan's own member claims
activity, used by both for the reflex repair) and the Office's note (its one sentence on error is the incompleteness a
completed source must state). Round 1, on the earlier pack, had missed the call and read the then-unfiled conventions
off the amounts; that device is in `## Tried and rejected`.

Judge, pass 1 (`determinism_check_report.md`): DETERMINISTIC, FIX_NOW: file the replacement convention, align step 6
with the estimator (the floor), fix the encounter file's late copy and the near-round payment totals; all four fixed in
one generator pass. Pass 2 (`determinism_check_report_pass2.md`), the single re-judge on target.zip f511b179e6742bf8:
DETERMINISTIC, every graded figure reproduced (the five, all 14 bonus figures, the $7,073,300 total); Gate G
statistical_rigor and analytical_non_defect, Gate H domain, layers and decisive step pass. Its two wording items were
fixed in the write-up with the pack unchanged: the losers' subtotal (a figure no ask owes, its rounded rows and its
rounded sum a hundred apart) dropped, and step 8 now states the replacement's change for both systems. Its residual
note, Varden 3 deaths under the line on the measured rates, is the margin the call stands on; every estimator in the
fork table files the same five.

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

