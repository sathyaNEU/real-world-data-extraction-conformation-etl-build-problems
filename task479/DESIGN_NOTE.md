# task479 design note

Status lives in `pipeline.json`; this note holds the design. Architecture 3, drawn 2026-10-21 after architecture 1
(NFIP claims replayed on elevated buildings) and architecture 2 (a lodging panel benchmarked to annual receipts) were
spent at stage 4; nothing of either world or step is kept.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task479.json` (architecture v3, lineage v1 and v2 spent), registered
  2026-10-21 after a pull. Guard WARN only, answered here: `overuse.objective` (the lane is ETL by assignment),
  `repeat.decision` and `repeat.question_form` against task480 (a set of groups over a line is a designation, and a
  designation asks which). Redrawn at the draw: the first candidate (electric school bus depots' on-peak charging,
  front-loaded sessions) has no task type serving ETL outside data integration and emissions inventories, both banned
  against the last three builds; GSDS data integration BLOCKed on pairing and subdomain against task486. Generator G13
  first BLOCKed `test.same_puzzle_older` (task229, task242, task476); G1 (a rate on the uncapped value applied to the
  capped one) is the honester label. People: Gregory Valdez and Claire Grant, from `guard.py names --geo us --seed
  479`.
- **Pairing:** Healthcare Delivery & Health Economics, task type `payment-claims-health-plan-analytics`, which serves
  ETL: a third-party administrator's 2025 claims, enrollment and the stop-loss carrier's large claimant report
  conformed at the group and member grain and restated onto the groups' 2027 retained-claims basis.
- **The decision and the quantity:** the administrator sends a funding true-up notice to each self-funded employer
  group whose expected 2027 retained claims per member per month (the claims the plan pays itself after specific
  stop-loss at the unchanged $250,000 attachment) exceed the 2027 funding rate the employer set in September.
  Forward facing: 2027 has not begun.
- **Data-native sentence:** a member whose 2025 claims already passed the attachment costs the plan exactly $250,000
  in 2027 whatever the trend, and one just under it costs only what trend lifts it to the attachment; the groups with
  the most such members carry several per cent of their retained claims in members the trend cannot raise.
- **Shape:** `10`, a scorecard of metric-threshold checks in one file: each of the sixteen groups' expected 2027
  retained PMPM against its elected claims component (16), the notice set, a chart, and two asks of sixteen groups
  times two figures (64).
- **Strategy:** `other` (the leveraging of a fixed per-member ceiling under trend); Gate G `forecasting`; gap `time`;
  generators G1, G13. Layer 2 family `estimation_fit`, pattern `own:a trend applied to claims before a per-member cap,
  not to the capped total`.

- **Sources, one line each:** seed ET36 (the lane and number only); the health plan actuary's leveraging of a fixed
  deductible under trend (the excess layer grows faster than trend and the retained layer slower), stated in no
  shipped document; the client's payment-claims rigor patterns (run-out, incurred against paid, reversals), used as
  Layer 1 only.
- **Same-puzzle test:** gap time, decisive generator G1, decision designation_set against the last twelve builds,
  lineage included: no match; task198 and task255 are differentiated on the card.
- **Abstraction test:** task198 (a lesser-of censoring hides an entitlement) recovers a hidden value; task255 fits a
  tail between floors and ceilings; task64 v2 runs a filed capacity ceiling as a stateful allocation. None grows units
  before a fixed per-unit ceiling to carry a capped total forward.
- **WHAT screen:** the memo files the population (the sixteen groups), the outcome (retained claims: incurred claims
  less specific reimbursements due, at the $250,000 deductible), the window (2027, on 2025 experience paid through
  March 2026 and 7.5 per cent trend a year), the unit (per member per month over 2025 member months) and the
  comparison (above the elected claims component). The decisive step settles none of them: it is how an unobserved
  2027 quantity is projected from the 2025 record when the deductible is fixed and the trend acts on claims.

## Default path

A strong analyst with every field read correctly:

1. Reads the renewal assumptions: 2025 incurred claims paid through 31 March 2026, 2025 member months, trend 7.5 per
   cent a year for two years, retained claims net of specific reimbursements due at the $250,000 deductible, rebates
   not netted, a notice where the expected 2027 retained PMPM exceeds the elected claims component.
2. Conforms the two claims lag reports (dollars against cents, the re-sent May 2026 counted once), counts 2025
   member months, and takes each group's 2025 reimbursements due from the large claimant report's eligible excess.
3. Computes each group's 2025 retained PMPM and trends it two years at 7.5 per cent, the standard renewal projection.
4. Compares with the claims components.

**Ends on:** notices to G1052, G1063, G1074, G1096, G1118, G1130, G1152, G1163 and G1174

The six beyond the golden stand 1.6 to 2.5 per cent over their rates on that path.

**Golden:** notices to G1052, G1118 and G1163 only (515, 600 and 707 against 495, 581 and 683); G1063, G1074, G1096,
G1130, G1152 and G1174 fall 1.5 to 2.5 per cent under their rates.

## Stump sentence

The default path trends each group's 2025 retained claims PMPM and files notices to G1052, G1063, G1074, G1096, G1118, G1130, G1152, G1163 and G1174, because it never asks how much of the trend lands above the fixed $250,000 deductible: a member already over it costs the plan $250,000 in 2027 whatever the trend, and one just under it only what trend lifts it to the deductible.

## Three rules

Task type: payment-claims-health-plan-analytics (Healthcare Delivery & Health Economics): a third-party administrator's claims lag reports, enrollment and the stop-loss carrier's large claimant report conformed at the group and member grain and restated onto each self-funded group's 2027 retained-claims basis, a conformation serving Data Extraction & Conformation (ETL).

Domain test: the deciding quantity is each group's expected 2027 retained claims per member per month under specific stop-loss, worked the way health plan actuaries project a self-funded plan's retained layer: trend acts on each member's claims and the fixed specific deductible is applied after, so the retained layer grows slower than trend and the excess layer faster, the leveraging of a fixed deductible.

Swap: "which school districts' 2027 transport budget needs a top-up, from 2025 costs trended" keeps a total and a trend and loses the step: there is no per-member deductible a reinsurer absorbs above, so trending the total is right and the call does not move.

Layer 1: the claims lag report in two layouts across the June 2026 platform upgrade (MM/YYYY dollars against YYYY-MM cents, May 2026 sent by both), 2024 incurred claims paid in 2025 and 2025 claims paid after the March 2026 run-out, the carrier's 12/15 basis and its own claimant numbers, five policies renumbered at the 2026 renewal, member ids reissued at the 2026 payroll vendor changes; each is how the producing system writes, nothing is placed to be caught, and checks.py asserts the main call holds under the mishandlings that can reach it (L1b, SF4, SF5).

Layer 2: estimation_fit, a nonlinearity in the projection: the choice that flips the call is trending each member's claims before the fixed deductible instead of trending the retained total, which carries 15.6 per cent of trend on every dollar of the retained claims of members the deductible caps.

Decisive step: each group's 2025 claims trended two years at 7.5 per cent, less each large claimant's trended claims above $250,000, over 2025 member months, which leaves G1063, G1074, G1096, G1130, G1152 and G1174 under their rates.

Not semantics: every field, unit and definition read correctly (incurred and paid months, cents, the eligible excess, the 12/15 basis, the policy schedule, rebates not netted) still leaves the easy route trending the retained PMPM, because no field or sentence says the trend must act on claims before the deductible; the step is a property of a capped sum, not a reading.

Not rule application: the memo fixes the experience, the trend rate, the deductible, the retained-claims definition and the comparison, and no rule or procedure says how the 2027 retained layer is projected from 2025; executing every filed rule on the retained total files the default nine.

Analyst test: a strong analyst who conforms every file and reads every rule, trending each group's 2025 retained claims PMPM by 7.5 per cent a year, files notices to G1052, G1063, G1074, G1096, G1118, G1130, G1152, G1163 and G1174 (the default path's Ends on); one who holds only the members already over the deductible at $250,000 files G1052, G1118, G1152 and G1163; only trending every member before the deductible files the golden three; checks.py runs both on the clean truth (R3a, R3b).

Estimand: the renewal assumptions memo (mba_2027_renewal_assumptions.pdf, sections 2 to 5): the population (the sixteen self-funded groups), the outcome (expected 2027 retained claims: incurred claims less the specific reimbursements due above the $250,000 deductible, rebates not netted), the window (2027, on claims incurred in 2025 and paid through 31 March 2026, trend 7.5 per cent a year for two years), the unit (per member per month over 2025 member months) and the comparison (above the claims component of the elected 2027 rate).

No decoy: nothing is planted: the lag reports, the enrollment, the carrier's report and advisories and the elections are the systems' own records, the memo states the basis without a projection method, and no earlier estimate, renewal worksheet or staff figure ranks the groups or trends the retained total.

No certified replay: no certified, published or earlier 2027 figure ships; the projection is built from each member's 2025 claims and the stated trend.

Lesson: a total kept under a fixed per-unit ceiling does not grow at the rate its units grow: units at the ceiling stop growing, units near it grow only to it, so a renewal projection trends claims before the deductible; no build on file projects a capped sum forward.

## Readability screen

Each rung, the sentence or file a reader would have to read to take it, and whether any shipped text hands it over.

| Rung | What takes the reader there | Verdict |
|---|---|---|
| R0 gross claims trended, stop-loss ignored | the memo read without section 4 | readable |
| Layer 1: two layouts, run-out, the carrier's basis, renumbered policies and members | the dictionary, the policy schedule, the memo's section 2 | readable |
| R1 (default path) 2025 retained PMPM trended two years | sections 2 to 4 of the memo: the experience, the trend, retained claims defined | readable |
| R2 the members over the deductible held at it, the rest trended uncapped | the large claimant report's eligible excess read as the only members the deductible touches | readable |
| R3 (decisive) every member trended, the deductible applied after | nothing: no sentence orders trend before the deductible, the memo defines retained claims for a contract year, and the large claimant report is the carrier's 2025 record, not a projection | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | rebates | not netted from claims | netted | no notices at all | memo section 4: "are not netted from claims" |
| SF2 | the experience | 2025 incurred, paid through 31 March 2026 | all 2025 incurred paid to September 2026 | same call (asserted) | memo section 2 |
| SF3 | the re-sent May 2026 | one cell per group, month and category | both copies | same call (no 2025 experience moves) | the cells' identical keys |
| SF4 | 2025 member months | a member enrolled in the month | persons | same call (identical in 2025, asserted) | memo section 2 |
| SF5 | two years of trend | compounded, 1.075 squared | 15 per cent simple | same call (asserted) | memo section 3 |
| SF6 | exceed | strictly above the claims component | at or above | same call (no group within 0.9 per cent, asserted) | memo section 5 |
| SF7 | reimbursements | due (above the deductible) | reimbursed to date | the default with G1141 added | memo section 4: "reimbursements due" |
| SF8 | a claimant's group | through the 2025 policy schedule | the member id's group | same call (one policy per group, asserted) | the policy schedule |

## Ladder

Built values from the cut pack (generator/checks.py L1 to L4, C2, C3), expected 2027 retained PMPM, whole dollars.

| Rung | Route | Notices | G1063, G1130, G1152 against rates 885, 871, 831 |
|---|---|---|---|
| R0 | gross trended | eleven groups | 1069, 1090, 844 |
| R1 (default path) | 2025 retained trended | G1052, G1063, G1074, G1096, G1118, G1130, G1152, G1163, G1174 | 904, 893, 844 |
| R2 | members over the deductible held at it, the rest uncapped | G1052, G1118, G1152, G1163 | 870, 861, 844 |
| Golden | every member trended, the deductible after | G1052, G1118, G1163 | 863, 852, 818 |

- Dominance: the default files six groups the golden does not, each 1.6 to 2.5 per cent over its rate on that path
  and 1.5 to 2.5 per cent under it on the golden (C2, C3); R2 keeps G1152, whose five members just under the
  deductible cross it after trend.
- The leverage is identity, not a fit: each member over $250,000 in 2025 adds $250,000 x 0.155625 to the default and
  nothing to the golden, so no estimator family exists to close (L4: the pack's golden equals the truth's to the cent).

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | the sixteen self-funded groups | filed (memo 1, 5) |
| 2 | Unit of account | retained claims dollars per member per month | filed (4, 5) |
| 3 | Attribution window | 2025 incurred, paid through 31 March 2026 | filed (2; SF2) |
| 4 | As-of dating | the extract of 5 October 2026 | manifest |
| 5 | Version basis | the latest cell per key; the carrier's report of May 2026 | SF3 |
| 6 | Denominator | 2025 member months | filed (2; SF4) |
| 7 | Weighting | none | C1 |
| 8 | Window length | twelve months of experience, two years of trend | filed (2, 3) |
| 9 | Boundary inclusivity | above the claims component | filed (5; SF6) |
| 10 | Rounding path | unrounded until printed to the dollar | prompt |
| 11 | Tie-break | none (no group within 0.9 per cent) | C2 |
| 12 | Maturity and censoring | the experience's run-out closed at March 2026 | filed (2) |
| 13 | Order of operations | trend, then the deductible, then divide | the estimand's 2027 retained claims; the identity in L4 |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | one cell per key | SF3 |
| 16 | Identity normalisation | claimants to groups through the 2025 policy schedule | SF8 |
| 17 | Netting against gross | rebates not netted; reimbursements due | filed (4; SF1, SF7) |
| 18 | Dimensional units | dollars and cents | the dictionary |
| 19 | Code and status semantics | Medical and MED, Pharmacy and RX | the dictionary; never the stump |
| 20 | Integerisation | none | C1 |
| 21 | Clause scope | the deductible applies to every member | filed (4) |
| 22 | Forward window contents | 2027 under the unchanged deductible, no plan change | filed (1, 4) |

## Literal reader

The memo executed word for word fixes the experience, the trend, the definition of retained claims and the comparison,
and asks for the 2027 retained claims a year before 2027 begins: the literal question is the claims the plan will pay
in 2027 net of reimbursements above $250,000 on each member's 2027 claims, which the 2025 record answers only once each
member's claims are carried to 2027. A literal reader who trends the retained total has carried 2025's reimbursements,
not 2027's; every other reading converges or violates a quoted sentence (fork table). Re-run on the finished pack.

## Oracles

- The large claimant report's eligible excess ties to total incurred less $250,000 for every claimant under every
  handling (O1); it is the carrier's 2025 figure and arbitrates nothing about 2027.
- The rebate statement and the cost survey are distractors (metadata.json); neither ranks the groups on 2027.
- No control ties only under the golden on the asks.

## Ask sheet

- **Ask A, each group's January to August 2026 member months and paid claims per member per month (sixteen groups,
  two figures each, whole member months and the cent).** H18 home: each group's current-year run, a second measure
  every group carries beside the notice. Path: the enrollment file's 2026 rows (member id, subscriber, birth date,
  sex, relationship, group, month), both lag reports' 2026 incurred cells, the dictionary. Primary device: D7, the
  same members under two key schemes: fourteen employers changed payroll vendor between May and July 2026, their
  members were reissued new member and subscriber ids, and the old ids stayed on file for one or two months, so a
  person appears twice in those months under ids that share nothing; only the group, birth date, sex and relationship
  tie them. Hazards: the re-sent May 2026 cells, cents, 2025 incurred claims paid in 2026.
- **Ask B, each group's members Arbor Ridge flagged in its 2026 specific advisories and their claims to date as last
  reported (sixteen groups, two figures each, whole members and whole dollars).** H18 home: the 2026 large claims the
  notice's experience does not see, which the account managers carry to the employers. Path: the advisories (date,
  claimant number, policy, member reference, claims to date), the 2026 policy schedule, the enrollment file. Primary
  device: D7, a prior-id chain: when a member's id was reissued, Arbor Ridge opened a new claimant file under the new
  id carrying the claims to date, so one member is two claimants; only the enrollment's person attributes join the
  two member references. Hazards: each advisory restates claims to date (summing rows overstates), reprocessing lowers
  some latest figures (the highest overstates), five policies renumbered at the 2026 renewal.
- **The construction layer:** the call, the sixteen retained figures and the chart; the cracker has them.
- **Main population zero-counts (asserted):** the call reads 2025 incurred cells paid through March 2026, 2025
  enrollment rows and the 2025 large claimant report; every ask device sits in 2026 rows (X1, SF4).
- **Hazard table (asserted):** A2 and B2, B3 in checks.py; none moves the call.
- **Referee:** none.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| A, January to August 2026 member months and paid PMPM | enrollment rows per member id and month, one cell per lag key; keeps 4 of 32 | miss |
| B, flagged members and their claims to date | the latest advisory per claimant number, the group through the 2026 policy schedule; keeps 4 of 32 | miss |

- Mirror leakage: 12.5 per cent of ask weight on the cut pack (8 of 64 figures, the two groups no device touches).
- Pair ceiling: 35.5 on the cut pack (weights 38 / 7 / 55: the cracker keeps the call, instructions and 8 of 64 ask
  figures, 51.9; the mirror at the default path misses the set, keeps 3 of 16 retained figures and the same 8, 19.1).
  Re-measured by the stage 4 readers.
- Measured by: generator/ceiling.py on the cut pack.

## Pre-ship check

READERS_LINE

JUDGE_LINE

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
- Architecture 1, NFIP claims replayed on the elevated buildings as they stand (2026-10-21, spent at stage 4): reader 1
  quoted guidelines 3.1 ("would bring ... as they stand") as the decisive text, replayed each claim's water on the
  present floor and landed the call, every rate and 30 of 72 figures; reader 2 missed on the claims since elevation
  but took ask B's counts from the final inspections; the judge NOT_DETERMINISTIC FIX_NOW on ask B's share, completion
  and county keys and called the estimand's wording an announcement. The estimand that files a counterfactual names
  it; re-rooted to architecture 2 in a fresh world.
- Architecture 2, the lodging Monitor benchmarked to the Department's annual receipts (2026-10-21, spent at stage 4):
  both scored readers computed each county's Department-to-Monitor ratio for every published year as their first
  calibration, saw the straight-line drift and carried it a year, landing the call, every growth figure and most ask
  figures (exit 1, 50 and 54 of 80); both also used the register's county for the transferred properties and linked
  the crosswalk gaps. A drift that the first diagnostic of a benchmarked series prints is no stump; re-rooted to
  architecture 3 in a fresh world.
