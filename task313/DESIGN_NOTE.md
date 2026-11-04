# task313 design note

Architecture 1, drawn 2026-11-04. Wave 10 (oviya1301), Opportunity Sizing & Decision Support. Seed OS15's world,
decision and quantity are kept: transitional-care nurse posts placed across a health system's hospitals in whole
posts, in proportion to the readmissions the service avoids, and the readmissions avoided a year. The seed's
pitfall (next-day transfers across town counted as readmissions, an episode-unit reading keyed through the
Medicaid plan's episode number) is a coding and identity stump that the clean-truth test kills, and is not used.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task313.json`, architecture v1, registered at the draw.
- **Pairing:** Healthcare Delivery & Health Economics / `patient-flow-beds-workforce-optimization`, drawn for
  Opportunity Sizing & Decision Support (the task type serves OS and F). The decision is a workforce placement:
  30 new neonatal transitional-care outreach posts across five maternity units for 2027/28, each unit's share
  following the readmissions the service will avoid among its eligible babies, and the readmissions the 30 posts
  avoid next year. Forward facing: the service starts on 1 April 2027 and the window is 2027/28.
- **Shape:** 05, allocation to a fixed total (each unit's posts and each unit's expected readmissions avoided),
  plus the total and the asks.
- **Strategy:** `causal_design`, Layer 2 family `estimand_identification`: the trial's intention-to-treat ratio
  is not the transportable effect, because the service acts only from its first home visit; read on the window
  after that visit (where the trial's own arms show the effect lives) and applied to each unit's readmissions
  that fall after its babies could first be seen.
- **Gap and generators:** gap time (the window the service can reach), then population; G7 operating window (a
  nurse can visit only after the community office knows the baby is home), G13 horizon (the window the trial
  measured is not each unit's reachable window), G14 conditioned yield.
- **Data-native sentence:** the community midwifery office learns of a discharge only when the maternity unit's
  notification reaches it, and two units' notifications routinely arrive one to five days after the baby goes
  home, while neonatal readmissions for jaundice and feeding cluster in the first four days after discharge; so
  a large share of those two units' readmissions happen before any outreach visit could, and nothing in either
  unit's own records says so.
- **Abstraction sentence (stumping Part 6):** "an intervention can act on a case only from a start that waits
  on a hand-off whose delay differs case by case and unit by unit, so a trial's whole-window effect carried as
  one ratio credits slow units with outcomes that fall before any start". Not writable against an approved
  build: 309 reads an effect class by class of event intensity (here the effect is constant once the service
  starts and what varies is how much of each case's window it reaches); 303 removes a shared upstream component
  logged by siblings in the same minute; 128 identifies an effect on over-capacity days; 105 is a catchment
  geometry; 106 a shared pool; 120 a storage identity. 105 v1 (spent on the portal) carried one filed season
  against one opening date; here each case's start comes from its own receipt time in a separate log, and the
  trial's effect has to be re-based before it is carried.
- **Spent mechanisms on the objective** (`guard.py mechanisms --objective opportunity-sizing-decision`, 19
  builds): 105 catchment nearer the new outlet; 106 a shared pool of spare legs; 116 groups with one signatory;
  118 the existing wedge plus the triangle; 120 inflow less storage gained; 127 the replaced wait's excess over a
  concurrent wait; 128 the effect read on over-capacity days; 301 a recorded state decaying between recordings;
  302 substitution inside the group; 303 the shared upstream minute; 304 a first sweep of a standing pool and a
  competing service; 305 the forced members' response; 306 units still to arrive in the roll; 307 wear only in a
  band; 308 sister units out together; 309 the effect class by class of intensity; 310 output capped by a limit;
  311 the between and within variance split; 464 the net flow with an injection. None spends a start gated by a
  per-case hand-off.
- **Slots screened** (`guard.py slots` on the mechanism and the setting): no note carries a hand-off-gated
  start; "readmission" hits are other mechanisms (task174's avoidance pathway, task190's linkage, task301's
  staggered post-discharge services); task308's note kills the ambulance-concurrency alternative and task174's
  the vacancy-chain alternative, both screened here and dropped.
- **Guard:** `check` PASS 2026-11-04, NOTE `test.same_puzzle_older` against task127's first architecture and
  `test.same_driver_older` against task259, both differentiated on the card; nearest driver 0.06. WARNs answered
  by redrawing: a persona's first name, the docx and xlsx deliverable set, the "where" question form (now how
  many, the form an allocation takes).
- **Furniture:** forum `funder_or_donor` (the integrated care board funds the posts and its specification fixes
  the allocation rule), forcing event `launch_or_rollout` (the service starts on 1 April 2027), organisation
  `hospital_or_health_provider`, role `programme_officer`, context artifact `close_out_summary` (the trial's
  final report), calibration `pilot_log` (the trial's randomisation list and contact log).
- **World:** England. Ravensby and Weald Integrated Care Board; Ravensby and Kellingworth Hospitals NHS
  Foundation Trust (Ravensby Royal Infirmary, Kellingworth University Hospital); Sedgefold and Wennby NHS Trust
  (Sedgefold Hospital, St Aldric's Hospital, Wennby Community Hospital, Copperfield Hospital, the trial site);
  Ravensby and Weald Community Health NHS Trust runs the community midwifery office and will host the posts.
  People from `guard.py names --geo england --seed 313`: Lucy Coates, Kathryn Thompson, Hugh Brown.
- **As-of date of the fiction:** 2 November 2026 (the planning pack). Planning basis: the twelve months to
  30 September 2026. Records run 1 April 2024 to 31 October 2026; the trial randomised 1 April 2024 to 31 March
  2026, its report is dated June 2026.
- **Sources:** every file is constructed in the organisations' own export forms (two maternity systems' discharge
  extracts, the community office's notification receipt log, the system's neonatal and paediatric admissions
  extract, the trial's randomisation list, contact log and final report, the service specification, code
  crosswalks, and the distractors); provenance, licence and the distractor list live in `metadata.json` outside
  `target/`.

- **Deliverables:** `outreach_posts_2027-28.xlsx` (the posts by unit, the readmissions avoided, and the two trial
  tables) and `outreach_posts_by_unit.svg` (one bar per unit, labelled). The deliverable set moved from png to svg
  at the prompt gate (png+xlsx over its corpus cap).

## Default path

Measured on the cut pack by `generator/verify.py` (`call(reached_only=False)`) and on the clean truth by
`generator/golden.py`; asserted in `generator/checks.py` (R3a).

1. Read SS-MAT-027: posts follow each unit's share of the readmissions the service is expected to avoid among its
   eligible babies (flagged on the discharge record, twins included) discharged home 1 October 2025 to 30 September
   2026; whole posts, then largest remainders.
2. Read the Copperfield final report: the outreach service cut unplanned readmission within 28 days with a risk
   ratio of 0.43, about 57 per cent.
3. Conform the two maternity systems (the RK csv; the SW workbook's two layouts and spaced NHS numbers), flag the
   eligible babies in the planning year, and key the admissions extract to them by NHS number or the master patient
   index, keeping emergency admissions (21, 22, 28, transfers inside the stay) within 28 days, once per baby.
4. Expected avoided at each unit = 0.57 x its eligible babies' readmissions (180, 168, 111, 86 and 101); posts by
   spec 7.

Ends on: posts of 8, 8, 5, 4 and 5 (Ravensby Royal, Kellingworth, Sedgefold, St Aldric's, Wennby) and about 375 readmissions avoided.
Golden: posts of 7, 9, 6, 3 and 5 and about 325 readmissions avoided.

## Stump sentence

Carrying the trial's 28-day ratio to every eligible readmission files posts of 8, 8, 5, 4 and 5 and about 375
readmissions avoided, because the outreach line can first reach a family only once the community midwifery office
holds the unit's discharge notification, and at Ravensby Royal and St Aldric's about half the notifications come on
paper with the signed discharge summary a day or more after the baby goes home, after a quarter of those units'
readmissions have already happened; on the readmissions each baby could be reached for, the posts are 7, 9, 6, 3
and 5 and the readmissions avoided about 325.

## Three rules

- **Task type:** Healthcare Delivery & Health Economics, patient-flow-beds-workforce-optimization, which serves
  Opportunity Sizing: a fixed nursing workforce placed across units in proportion to the outcomes it can change,
  sized from the addressable readmissions to the ones the service can still prevent.
- **Domain test:** the deciding quantity is the number of each unit's newborn readmissions a post-discharge outreach
  service can still prevent, the quantity a health services analyst builds by transporting a randomised trial's
  effect onto a target population's outcomes over the part of their course the service touches.
- **Swap:** put depots and faults for units and readmissions and nothing is left to decide: there is no trial
  ratio, no discharge notification travelling on paper with a signed summary, and no neonatal readmission curve
  front-loaded into the first two days at home, which is what makes a one-day hand-off decide a quarter of the
  outcomes.
- **Layer 1:** real export mess, none of it deciding (R2 in `checks.py`): the office log in UTC, transposed NHS
  digits on paper notifications, interface duplicates and amended notifications, two maternity systems with a
  layout change and spaced NHS numbers, blank NHS numbers resolved through the index, cross-trust hospital
  numbers, transfer rows, planned day cases, Copperfield's postnatal-ward rows under the mother.
- **Layer 2:** effect transport with an exposure window: the trial's ratio is the effect on families the service
  reached, so it applies only to the readmissions that fall after each baby could be reached, and that share
  differs by unit (73, 99, 98, 72 and 90 per cent) through how each unit's notifications travel.
- **Decisive step:** before the trial's ratio is applied, each unit's eligible readmissions are cut to those that
  came after the community office's receipt of that baby's notification (or 08:00 when it arrived outside the
  line's calling hours), a per-baby comparison of two instants held in two different logs.
- **Not semantics:** every field read correctly (UTC converted, both workbook layouts, the index, methods 21, 22
  and 28, the 28 days, twins in) still files 8, 8, 5, 4, 5 and 375 on the easy route; no code, field or
  definition separates the readmissions before the receipt from those after.
- **Not rule application:** SS-MAT-027 says posts follow the readmissions the service is expected to avoid and
  says nothing about which readmissions it can avoid; no filed rule ties the service's start to the receipt, so
  executing every stated rule with the report's ratio files the default.
- **Analyst test:** yes: a strong analyst who conforms every file and applies section 7 with the report's 0.43
  files posts of 8, 8, 5, 4 and 5 and about 375, because carrying a trial's whole-window ratio to the target
  population is the standard move and Copperfield's own trial validates it.
- **Estimand:** spec 3, 5, 7 and 8: each unit's share of the readmissions the 30 posts are expected to avoid
  among its eligible babies discharged home 1 October 2025 to 30 September 2026, a readmission being an emergency
  admission to any hospital in the area within 28 days, once per baby; whole posts by largest remainders; the
  readmissions avoided across the units to the nearest 25.
- **No decoy:** nothing is planted: no memo or note argues the whole-window carry, no rule is withheld against a
  stated one, and no document names a notification delay; the report states its result on its own linkage, which
  files the same bin as the full count.
- **No certified replay:** no certified or published figure is reproduced to recover the method; the report's
  ratio is used as the effect it is, and the golden recomputes it from the rows.
- **Lesson:** a trial's effect travels only over the part of each case's course the service can reach; where the
  start waits on a hand-off whose delay differs by unit, a unit's share follows its reachable outcomes, not its
  outcomes.

## Survivor anatomy

- **Actor:** the deciding property, whether a baby's readmission came after the office could pass it to the
  outreach line, has no column: it is a relation between the admission instant in the ICB extract and the receipt
  instant in the office's UTC log for the same baby; no file holds a delay, a route, a first-contact time for the
  five units or a reachable flag (R1).
- **Link:** the receipt is joined to the readmission through the baby's NHS number in two logs that never meet in
  any filed analysis (with the hospital number where a paper notification's digits are transposed); the trial's
  analysis never makes the comparison because at Copperfield the receipt is within the hour.
- **Reflex:** the field's reflex, a trial's risk ratio applied to the target population's outcome count, sits at
  rung 1 and files 8, 8, 5, 4, 5 and about 375.
- **Back-test:** the textbook route validates: at Copperfield the ratio on the readmissions after the first call
  equals the 28-day ratio (57 per cent both, SF10), the report's figure reproduces from the rows, and the default
  path reconciles to both maternity extracts and to the report's own counts.
- **Second use:** every file the decisive step reads has its own use: the office log is the referral record
  (spec 4) and carries amendments and duplicates; the admissions extract is the outcome source of the trial and
  of spec 5; the maternity extracts define eligibility; the contact log carries Ask B and the trial's lags.
- **Shock:** the change reads as ordinary: Ravensby Royal and St Aldric's give up one post each and Kellingworth
  and Sedgefold gain one; Ravensby Royal still has the most eligible babies and readmissions, so the golden is not
  an interval of eligible babies, readmissions or readmission rate.
- **Pins:** SS-MAT-027 files the WHAT in the commissioner's own genre (eligible babies, the referral route, the
  outcome, the posts, the allocation rule, the planning basis); no filed sentence names a receipt time, a delay,
  calling hours or a window after contact (R3c greps both PDFs).

## Readability screen

Each rung against the seven tests (1 filed sentence, 2 schema, 3 reflex, 4 control bench, 5 hygiene, 6 linear, 7
dedicated organ); the reflex row comes from the field's vocabulary for carrying a trial result to a population.

| Rung | 1 | 2 | 3 | 4 | 5 | 6 | 7 | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 caseload: posts by eligible babies (8, 7, 6, 4, 5; 375) | spec 6, sized to every eligible baby | the flag column | no | no | no | yes | no | readable |
| R1 the trial ratio on every eligible readmission (8, 8, 5, 4, 5; 375) | spec 7 and the report's ratio | the admissions extract | yes | the report and Copperfield's back-test agree | finds nothing | yes | no | readable |
| R2 one lag for every unit (the trial's lag to its first call, 8, 8, 5, 4, 5 and 350; a day, 9, 8, 5, 4, 4 and 325) | no | no | no | no | no | yes | no | readable |
| R3 each unit's median receipt lag (8, 8, 5, 4, 5; 350) | no | no | no | no | no | yes | no | readable |
| G (decisive) each baby's readmission against its own receipt (7, 9, 6, 3, 5; 325) | no sentence names a receipt, a delay or a window after contact | no column holds a delay, a route or a reachable flag | no: the reflex carries the whole-window ratio | quiet: Copperfield's trial agrees with every rung | no | no: a per-baby join of two instants across two logs and two clocks | every file it reads has its own use | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "readmission" | emergency admission (21, 22, 28; 81 inside a stay) | planned day cases (11 to 13) in | same call (asserted) | spec 5, emergency admission |
| SF2 | "within 28 days" | after discharge, to discharge plus 28 days | 27 or 29 whole days | same call (asserted) | spec 5; convergence |
| SF3 | eligible babies | the flag on the discharge record, twins in | twins out, as in the trial | same call (asserted) | spec 3, twins are eligible |
| SF4 | the planning basis | discharged home 1 Oct 2025 to 30 Sep 2026 | born in that window | same call (asserted) | spec 8 |
| SF5 | a baby counts once | babies readmitted | admissions | same call (asserted) | spec 5 |
| SF6 | the receipt clock | UTC converted to local | read as local | same call (asserted) | the log's received_utc header and Z suffix |
| SF7 | the receipt | the first Discharge home notification | the latest message, amendments in | same call (asserted) | convergence |
| SF8 | the earliest contact | the receipt in calling hours (08:00 to 19:00), else 08:00 | the receipt itself, plus 1 h or 2 h, a 09:00 opening, a 20:00 cut | same call in every combination (asserted) | convergence |
| SF9 | the trial's effect measure | risk ratio | incidence rate ratio on days at risk | same posts, 318.4 to 331.3, all in the 325 bin (asserted) | convergence |
| SF10 | the trial's window | readmissions after the earliest contact | the whole 28 days | same call (asserted) | convergence: Copperfield's receipts come within the hour |
| SF11 | the units | the five units of spec 3 | Copperfield included | Copperfield is not a candidate | spec 2 and 3 |
| SF12 | rounding the total | once, on the sum | each unit rounded, then summed | same bin (asserted) | the prompt's rounding sentence |
| SF13 | whole posts | largest remainders | each share to the nearest post | same posts (asserted) | spec 7 |
| SF14 | the ratio's source | the rows, every readmission keyed | the report's 0.43 on its own linkage | same bin, 316.7 and 321.3 (asserted) | convergence |
| SF15 | one effect or one per reason | the pooled ratio | reason-specific ratios carried to each unit's mix | same posts; the total moves (asserted) | the report: no interaction by gestation, feeding or primary risk reason |
| SF16 | a transfer inside one stay | one admission | a second admission | same call (asserted) | spec 5 |
| SF17 | Ask A, risk reason | every reason on the discharge record | the trial list's primary reason | Ask A moves (asserted) | the asking sentence |
| SF18 | Ask B, visits made and calls that reached the family | completed contacts | NA and TNA rows, or the short TEL and HV rows filed before 6 January 2025, counted | Ask B moves (asserted) | the asking sentence; the code list's in_use_from; every cut in the minute gap gives the same figures (asserted) |
| SF19 | Ask B, calls under a parent's number | counted for the baby | dropped | Ask B moves (asserted) | the asking sentence: a call to the mother reached the family |
| SF20 | Ask B, the window | contacts in the 28 days after discharge | later calls kept | Ask B moves (asserted) | the asking sentence |

## Ladder

Every rung priced on the cut pack (`checks.py` R3a and R3b; figures printed there):
- **Rung 0, caseload (8, 7, 6, 4, 5; 375):** posts by eligible babies, the reading of spec 6's sizing sentence;
  ruled out by spec 7.
- **Rung 1, the reflex (8, 8, 5, 4, 5; 375 on the report's 0.43, 370.6 on the rows):** the trial ratio on every
  eligible readmission.
- **Rung 2, one lag for every unit:** the trial's own lag to its first call (11.9 h) files 8, 8, 5, 4, 5 and 350; a
  day files 9, 8, 5, 4, 4 and 325; the trial's lag to its first visit (39.0 h) files 9, 8, 5, 4, 4 and 250.
- **Rung 3, each unit's median receipt lag (27.5, 0.7, 0.7, 17.8 and 0.9 h):** 8, 8, 5, 4, 5 and 350, because a
  median hides the paper half of the two slow units.
- **Decisive (7, 9, 6, 3, 5; 325):** each baby's readmission against its own receipt; reachable shares 73, 99, 98,
  72 and 90 per cent; the total 321.3, inside its bin with 8.8 and 16.2 to spare.
- **The visit-start reading (7, 10, 6, 2, 5; 200)** is refuted by the trial itself: readmissions in the first day
  after the earliest contact already differ by arm (8 of 2,092 against 31 of 2,134, ratio 0.26, upper bound 0.57).
- **Separation:** each rung files other posts; the default total sits two bins from the golden; the convention
  family (SF8, SF9) spans 318.4 to 331.3 and never leaves the 325 bin.

## Closure table

| Axis | Reading here | Closure |
|---|---|---|
| 1 Population | eligible babies of the five units discharged home in the planning year | spec 3 and 8; SF3, SF4, SF11 |
| 2 Unit of account | whole posts per unit; babies readmitted | spec 5 and 7; SF5, SF13 |
| 3 Attribution window | 28 days after discharge home | spec 5; SF2 |
| 4 As-of dating | the planning basis year, extracts of 2 November 2026 | spec 8; every planning-year window closes by 28 October 2026 |
| 5 Version basis | the final randomisation list; the first discharge notification | the final list is the only list shipped; SF7 |
| 6 Denominator | babies per arm in the trial; none in the allocation | the report's analysed counts; SF9 |
| 7 Weighting | none; shares of readmissions avoided | spec 7 |
| 8 Window length | 28 days; the planning year | spec 5 and 8 |
| 9 Boundary inclusivity | discharge home 1 Oct 2025 to 30 Sep 2026 inclusive; readmission after discharge to day 28 | spec 8; SF2 asserted |
| 10 Rounding path | posts by largest remainders; the total once to the nearest 25 | spec 7; SF12, SF13 |
| 11 Tie-break | none (no equal remainders) | asserted by the allocation |
| 12 Maturity and censoring | every planning-year baby has its full 28 days before the extract | asserted (no admission after the extract time) |
| 13 Order of operations | reachable readmissions, then the ratio, then the shares | C1: the ratio cancels in the shares |
| 14 Row order | none | not applicable |
| 15 Duplicate resolution | interface duplicates share an office_ref; one receipt per baby | SF7; R2 asserted |
| 16 Identity normalisation | NHS numbers spaced in SW, blank ones through the index, transposed digits through the hospital number | R2 asserted per item |
| 17 Netting against gross | none | not applicable |
| 18 Dimensional units | UTC against local time | SF6 |
| 19 Code and status semantics | admission methods, notification kinds, contact codes | the code lists; SF1, SF18; never the stump |
| 20 Integerisation | whole posts | spec 7 |
| 21 Clause scope | spec 7 covers the five units; Copperfield outside | spec 2; SF11 |
| 22 Forward window contents | 2027/28 planned at the planning basis year's activity | spec 8, stated, no projection |

## Literal reader

Executed word for word on the cut pack: spec 3, 5, 7 and 8 file the population, the outcome, the allocation rule
and the planning basis; the prompt files the units of the answer and the rounding. Nothing filed says which
readmissions the service is expected to avoid, so the literal reader must decide it, and the easy answer (the
ratio on every readmission) is an easy method on the same literal estimand, not another reading of a term. Every
convention the computation needs (SF1 to SF16) is ruled out by a quoted sentence or converges on the same posts
and bin (asserted in `checks.py`); SF15 is the one reading that moves the total, and the report's interaction
tests rule it out.

## Oracles

- The trial report: its ratio agrees with every rung (at Copperfield the window question never arises), so it
  confirms the reflex and arbitrates nothing; its counts sit on the trial team's linkage.
- Copperfield's contact log: shows the first call following the office's receipt and the first visit a day or
  more later; with the trial's arms it separates a start at the call from a start at the visit; it says nothing
  about the five units.
- The office log: one receipt instant per notification; no delay, route or unit-level summary.
- The distractors (the LMNS dashboard of births and rates by unit, the community midwifery establishment by team):
  relevant to staffing, used by no rung.

## Layer 1 inventory

Each item, the system that writes it, its file and its natural mishandling; each mishandling leaves the posts and
the bin (R2 in `checks.py`):
- UTC receipts: the office's case system, `community_midwifery_notifications_2024-04_2026-10.csv`; read as local.
- Transposed NHS digits on paper notifications keyed by hand: same file; left unmatched.
- Interface duplicates (same office_ref) and amended notifications: same file; the latest message taken.
- Two maternity systems, the SW workbook's layout change in April 2026 and its spaced NHS numbers:
  `rk_maternity_postnatal_discharges_2024-04_2026-10.csv`, `sw_maternity_postnatal_discharges.xlsx`.
- Blank NHS numbers on PAS rows and cross-trust hospital numbers: `neonatal_paediatric_admissions_2024-04_2026-10.csv`
  and `mpi_baby_hospital_numbers.csv`; left unkeyed.
- Transfer rows inside one stay (method 81) and planned day cases (12, 13): the admissions extract; counted.
- Copperfield's postnatal-ward readmissions under the mother's NHS and hospital numbers: the admissions extract;
  left unmapped (moves only Ask A).
- Re-sent tablet contacts, calls under a parent's number, the 6 January 2025 code change: the contact log; Ask B
  only.

## Ask sheet

Planning weights 38 / 7 / 55. The call (five units' posts and the total) carries 38. The asks are the trial side
of the case, 24 figures: A, for each of the six risk reasons, the usual-care 28-day readmission rate and the risk
ratio for outreach (12); B, for each reason, home visits made and calls that reached the family per outreach baby
in 28 days (12).

- **Ask A, the effect by reason:** H18 home: a qualifier of the call, whether the ratio carried to the units holds
  across the reasons that make up their eligible babies, and their baseline risk. Path: the final list (Hospital
  No, NHS No, Arm), the SW workbook (Hospital No, NHS No, Mother NHS No, Discharge date and time, Risk reasons, on
  both layouts), the reason codes, the admissions extract (provider, admitting_hospital, ward_type, nhs_number,
  hospital_number, admitted, admission_method), the index. Primary: Copperfield's PAS files a baby who returns to
  its postnatal ward under the mother's NHS and hospital numbers (D7, an infant under its mother's key), 88 rows,
  all at Copperfield; the report's counts were linked the same way, so reconciling to the report confirms the
  wrong path. Hazards: blank NHS numbers, cross-trust numbers, planned day cases, the trial list's primary reason.
  Pin test: the asking sentence pins the population (the babies the trial analysed), the grouping (every reason on
  the discharge record) and the rounding; no pin names a key or a ward.
- **Ask B, the contacts by reason:** H18 home: the audit trail of the service the posts deliver, per reason. Path:
  the contact log (contact_id, nhs_number, contact_datetime, contact_type, minutes), the code list, the final list,
  the SW workbook's Mother NHS No. Primaries: calls to a parent's mobile are filed under the mother's NHS number
  (D7, 4,000 or more rows); before the code update of 6 January 2025 a visit with no access or an unanswered call
  was filed as HV or TEL with the few minutes it took (D2, a label stored before a silent switch). Hazards: re-sent
  contacts under one contact_id, calls after day 28, contacts for Copperfield's babies after the trial, NA and TNA
  rows. Pin test: the sentence pins visits made, calls that reached the family, per baby and the 28 days; no pin
  names a code, a date or a parent.
- **Main population zero-counts:** mother-keyed admission rows at the five units 0; contact rows for planning-year
  babies of the five units 0 (asserted). The call's total holds with the mother rows unmapped (316.7, SF14).
- **The full includer:** a response that maps the mother rows in both files and splits the pre-update clusters
  keeps all 24, a known limit; one that maps the mothers only keeps Ask A (12 of 24); one that splits the code
  switch only keeps the six visit figures.
- **Realism:** babies readmitted for phototherapy with their mothers on a postnatal ward, nurses ringing the
  mother's mobile, and an app that had no code for a failed attempt until a release are ordinary in community
  neonatal services.

Pair ceiling: 29.2 (the cracker on the call at 45.0 with 0 of 24 asks; the mirror off the call at 13.3 with 0 of 24).
Mirror leakage: 0.0 per cent of ask weight.
Measured by: generator/ceiling.py on the cut pack (digest printed by the script).

| Ask figure | Cracker (keys by NHS number and index, mother rows and the code switch unseen) | Golden | Cracker |
|---|---|---|---|
| A BFP usual-care rate | 4.9 | 6.1 | miss |
| A BFP risk ratio | 0.67 | 0.64 | miss |
| A EDC usual-care rate | 5.1 | 6.6 | miss |
| A EDC risk ratio | 0.41 | 0.40 | miss |
| A LPT usual-care rate | 6.6 | 8.5 | miss |
| A LPT risk ratio | 0.30 | 0.35 | miss |
| A SPH usual-care rate | 4.3 | 5.7 | miss |
| A SPH risk ratio | 0.86 | 0.65 | miss |
| A VJD usual-care rate | 6.4 | 7.9 | miss |
| A VJD risk ratio | 0.60 | 0.49 | miss |
| A WTL usual-care rate | 5.7 | 6.2 | miss |
| A WTL risk ratio | 0.31 | 0.29 | miss |
| B BFP home visits | 1.27 | 1.24 | miss |
| B BFP calls | 1.58 | 2.81 | miss |
| B EDC home visits | 1.23 | 1.20 | miss |
| B EDC calls | 1.47 | 2.60 | miss |
| B LPT home visits | 1.83 | 1.80 | miss |
| B LPT calls | 1.74 | 2.93 | miss |
| B SPH home visits | 1.38 | 1.33 | miss |
| B SPH calls | 1.55 | 2.59 | miss |
| B VJD home visits | 1.51 | 1.48 | miss |
| B VJD calls | 1.51 | 2.54 | miss |
| B WTL home visits | 1.55 | 1.53 | miss |
| B WTL calls | 1.83 | 3.02 | miss |

## Leak review

`leak.py task313 --asof 2026-11-02`, verdict REVIEW, no LEAK; sweeps 1, 2, 5, 7, 9, 10, 11 and 12 clean. Each REVIEW
line ruled here:
- Sweep 3, the specification carries the committed call's words: it names the five units and the 30 funded posts,
  the candidates and the stated decision parameter; it holds no post, share or readmission figure per unit.
  Harmless.
- Sweep 4, the final report (effect, report, hospital, allocation, community, contact): ordinary trial-report
  vocabulary for its arms, outcome and subgroups; it names no receipt time, delay or window after contact (R3c
  greps it). Harmless.
- Sweep 4, the specification (report, eligible, hospital, office, allocation, notification): section 4 says babies
  are referred through the community midwifery office, which receives each unit's discharge notifications. It is
  the service's referral route in the commissioner's genre and states no timing and no relation between the
  receipt and readmission; it is the sentence a reader is most likely to quote, so it is named to the stage 4
  reader as open rather than ruled away.
- Sweep 6, the LMNS dashboard names the units beside births and monthly rates: a declared distractor, ranking
  nothing on posts or readmissions avoided and read by no rung. Harmless.
- Sweep 8, NB_RISK_FLAG: the RK maternity system's own field for the newborn feeding or jaundice risk indicator
  (the SW system's "Newborn risk flag"), the flag spec 3 names; not a generator's truth column. Harmless.
- Sweep 12 first returned LEAK on the report (nine names shared with the data files' headers and first rows,
  among them nurse, team, discharged and the arm labels); fixed in the generator by renaming the contact log's
  staff column, the admissions extract's trust and discharge columns and the establishment's team column, and by
  the report's own labels (Intervention, Comparator, Neonatal outreach, Usual community care).
- Guard: `surface` lists the personas Hugh Brown, Kathryn Thompson and Lucy Coates, all from `guard.py names`;
  `heart` WARN only for the svg+xlsx deliverable pair repeating task462's (an ETL build in another domain), with
  the two older NOTEs answered at the draw; nearest driver 0.06.

## Tried and rejected

- Seed OS15's own mechanism (adult next-day transfers across town counted as readmissions, the Medicaid plan's
  episode number grouping the stays): with every key and disposition code correct the easy route excludes the
  transfers and lands, so the stump is a coding and identity reading (data semantics) and fails the clean-truth
  test; not built.
- Adult transitional-care posts, the first visit gated by each hospital's discharge summary (2026-11-04, measured
  on a prototype of the clean truth): at the realistic edge (two tertiary centres' summaries 38 to 42 per cent
  late, weekend discharges, surgical front-loading) the post-visit share ran 0.69 to 0.85, a contrast of 1.23x;
  under the seed's proportional rule the golden and default allocations were identical in every seed (C10 N8
  R5 S4 L3), because the shift is half a post; under a fill-by-rank rule the golden ranking ratios sat at 1.00
  to 1.06, the allocation was seed-hostage, and counting per visited patient against per eligible patient
  flipped the allocation on its own (a live main-call fork); the fixed-lag partial correction recovered half the
  contrast in the same direction. Dead on magnitude; moved to the neonatal pathway, where readmissions cluster
  in the first days after discharge.
- Adult transitional-care posts against the trial's own yield as a designation threshold: the benchmark rests on
  the trial's control arm (noisy) and any gap between estimators of the effect lands on the comparison; dropped
  for the proportional rule once the neonatal contrast made it carry.
- Adult transitional-care posts with the effect read only where patients are not already on a specialist nurse
  caseload (provision elsewhere), and the effect read on readmissions related to the index condition: each is an
  effect carried class by class to a different mix, task309's approved abstraction; not drawn.
- Ambulance shifts sized by the late calls an added crew would have reached: task308's screen records readers
  splitting availability from geography misses and replaying dispatch; dead on file.
- Social homes sized by the relets their transfer tenants release (vacancy chains): task174's screen records the
  chain as the housing literature's own construct; dead on file.
- The interim randomisation list (to 31 December 2025, consented babies, four arms keyed wrongly) as Layer 1 beside
  the final list (2026-11-04): its ratio on 21 months files 300 against the final list's 325, so its natural misuse
  moved the total's bin and the item was not neutral; cut from the pack rather than re-dated to a neutral cut.
- Ask A as each arm's readmission rate by reason (2026-11-04): the cracker kept the three outreach cells no
  mother-keyed readmission reaches; re-sited onto the usual-care rate and the risk ratio, which every cell's
  device moves.
- The trial report on every readmission keyed (2026-11-04): its Table 2 then arbitrated the Ask A device (a
  reconciliation to 56 and 134 exposes the missing rows); the report now carries the trial team's own linkage (46
  and 108), whose ratio files the same bin as the full count.
- The first-baby subgroup in the report (2026-11-04): its interaction test came out at 0.05, which would have left
  a reason-specific transport arguable; the pre-specified set is gestation, feeding and the primary risk reason.
- Blank NHS numbers on 5 per cent of SW admissions (2026-11-04): leaving them unkeyed moved the total to 300;
  1.5 per cent (0.5 at RK) keeps the item neutral.
- The mother-keyed readmissions removed to keep the trial clean of devices (2026-11-04, earlier the same day):
  restored once the trial's ratio was shown to file the same bin with them unmapped (316.7 against 321.3).
