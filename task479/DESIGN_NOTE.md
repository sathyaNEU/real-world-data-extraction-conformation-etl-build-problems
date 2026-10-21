# task479 design note

Status lives in `pipeline.json`; this note holds the design. Architecture 6, drawn 2026-10-21 after architectures 1
to 5 were spent at stage 4; nothing of any earlier world or decisive step is kept (the ask devices that held in
architectures 3 and 5 are re-skinned).

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task479.json` (architecture v6, lineage v1 to v5 spent), registered
  2026-10-21 after a pull. Guard WARN only, answered here: `overuse.objective` (the lane), `people.first` (Michelle,
  drawn by `guard.py names --geo us --seed 4796`). Redrawn at the draw: gap population with G17, then time with G13,
  then population with G16 (same-puzzle blocks against task471, task178 and task480) to gap time with G16, Gate G
  `signal_vs_noise_or_hold`, differentiation lines for task130, task148 and task241; shape 10 to 15 at stage 3 (ban.shape against task272, drawn meanwhile). People: Steven Coleman and
  Michelle Patrick.
- **Pairing:** Healthcare Delivery & Health Economics, task type `payment-claims-health-plan-analytics`, which serves
  ETL: the administrator's claims lag reports in two layouts, the eligibility file and the carrier's specific
  reimbursements conformed by member employer and plan year and restated as each employer's expected 2027 retained
  claims.
- **The decision and the quantity:** the trust's trustees surcharge the January 2027 contributions of the member
  employers whose expected 2027 retained claims per member per month exceed the claims component of the 2027
  contribution each employer elected. Forward facing: 2027 has not been incurred.
- **Data-native sentence:** most member employers cover fewer than three hundred members, so one member's large claim
  moves a year's experience by more than employers truly differ, and three years of a small employer's own record say
  little about its expected claims.
- **Strategy:** `uncertainty_hold`; Gate G `signal_vs_noise_or_hold`; gap `time`; generators G16, G17. Layer 2 family
  `forecast_uncertainty`, pattern `own:each unit's expected level read as its own short noisy history weighted against
  the pool by the share of its spread that is signal`.

## Default path

A strong analyst with every field read correctly:

1. Reads the memo: an employer is surcharged when its expected 2027 retained claims PMPM exceed the claims component
   of its elected 2027 contribution, the evidence the trust's 2023 to 2025 experience, each year's retained claims
   trended at 7 per cent a year to 2027.
2. Conforms the two lag reports (the May 2026 cells once), takes each year's claims paid through March of the next,
   nets Westerby's reimbursements through the policy schedule, counts member months, and trends each employer's three
   years to a member-month weighted 2027 PMPM.
3. Compares each employer's trended experience with its claims component.

**Ends on:** CR104, CR109, CR136, CR167 and CR176 surcharged

On that path CR104, CR109 and CR136 stand at $578.2, $628.4 and $672.6 against claims components of $548.88, $583.93
and $594.31, and CR113, CR118, CR131 and CR149 at $459.6, $445.6, $452.5 and $421.5 against $475.30, $467.01, $468.10
and $445.54.

**Golden:** CR113, CR118, CR131, CR149, CR167 and CR176 surcharged; weighed by credibility (Buhlmann-Straub, k of
7,285 member months, the trust's level $500.25), CR104, CR109 and CR136 fall to $511.2, $522.5 and $557.9 and CR113,
CR118, CR131 and CR149 rise to $492.5, $488.5, $486.1 and $466.0.

## Stump sentence

The default path trends each employer's own 2023 to 2025 retained claims to 2027 and files CR104, CR109, CR136, CR167 and CR176 surcharged, because it never asks how much of a small employer's three years is chance: one member's large claim moves a forty-member employer's year by more than the employers truly differ, so the small employers with high experience are expected near the trust's level and under their claims components, and the small employers with low experience, whose claims components sit well under the trust's level, are expected over them.

## Three rules

Task type: payment-claims-health-plan-analytics (Healthcare Delivery & Health Economics): the administrator's claims lag reports in two layouts, the eligibility file and the carrier's specific reimbursements conformed by member employer and plan year into each employer's retained claims per member month, a conformation serving Data Extraction & Conformation (ETL).

Domain test: the deciding quantity is each member employer's expected 2027 retained claims per member per month, worked the way a health plan actuary experience-rates small groups: the group's own experience weighed against the pool's by its credibility, which the pool's own experience sets from how far each group's years spread around its own mean against how far the groups' means spread around the pool's (Buhlmann-Straub), the claims capped at the specific deductible.

Swap: "which stores' expected 2027 shrinkage exceeds their budget, from three years of losses" keeps a short noisy history per unit and loses the step's ground: no member claim distribution capped by a specific deductible, no pool of groups underwriting each other, no experience rating whose credibility the pool's own claims set.

Layer 1: the claims lag report in two layouts across the May 2026 platform move (MM/YYYY dollars against YYYY-MM cents, May sent by both), Westerby's reimbursements keyed by policy numbers rewritten at the 2025 renewal, member ids reissued at the summer 2026 eligibility move; each is how the producing system writes, nothing is placed to be caught, and checks.py asserts the call holds under them (SF2, SF3, X1).

Layer 2: forecast_uncertainty, the evidence judged with its uncertainty: the choice that flips the call is reading each employer's expected claims as its experience weighed by the share of its spread that is signal, instead of the experience itself.

Decisive step: estimating each employer's expected 2027 retained PMPM by credibility against the trust's level, which puts CR104, CR109 and CR136 (34 to 98 members, experience raised by a few large claims) under their claims components and CR113, CR118, CR131 and CR149 (48 to 155 members, low experience, claims components well under the trust's level) over theirs.

Not semantics: every field, unit and definition read correctly (the two lag layouts, cents and dollars, the reimbursements and policy numbers, member months, retained claims before rebates) still leaves the easy route comparing each employer's own trended experience with its claims component, because no field says how much of an employer's experience is chance; the step is the inference that a small group's three years are mostly noise, which the spread of the employers' years shows and no sentence says.

Not rule application: the memo fixes the population, outcome, window, unit and comparison and names the evidence and the trend, and no rule says how an employer's expected claims are read from it; executing every filed rule on each employer's own experience files CR104, CR109, CR136, CR167 and CR176 surcharged.

Analyst test: a strong analyst who conforms every file and reads every rule, taking each employer's own trended experience as its expected claims, files CR104, CR109, CR136, CR167 and CR176 surcharged (the default path's Ends on); one who takes 2025 alone files the same; one who takes the trust's level for every employer adds CR181; only weighing each employer's experience by its credibility files the golden six; checks.py runs them on the clean truth (R3a, R3b, R3c).

Estimand: the renewal review memo (crbht_2027_renewal_review.pdf, sections 2 and 3): the population (each member employer's members in plan year 2027, the plan and employers unchanged), the outcome (retained claims, net of Westerby's specific reimbursements and before pharmacy rebates), the window (plan year 2027), the unit (per member per month) and the comparison (exceeding the claims component of the elected 2027 contribution), the evidence the trust's 2023 to 2025 experience for every employer, each year's retained claims trended at 7 per cent a year to 2027.

No decoy: nothing is planted: the lag reports, eligibility, reimbursements, high-cost report and elections are the producing systems' records, the memo states the basis without a method, and no projection, rating, earlier review or published figure ranks the employers on 2027.

No certified replay: no certified or published credibility, manual rate or projection ships; the method is not recovered by reproducing any figure.

Lesson: an expected level read from a short record is the record weighed against the pool by how much of its spread is signal, and for a small health group three years of claims are mostly the luck of a few members; no build on file estimates each unit's level by shrinking its own noisy record toward the pool by a credibility the pool's own spread sets.

## Readability screen

Each rung, the sentence or file a reader would have to read to take it, and whether any shipped text hands it over.

| Rung | What takes the reader there | Verdict |
|---|---|---|
| R0 the trust's level for every employer | the memo's "the trust's experience" | readable |
| Layer 1: two layouts, reimbursements by policy, reissued ids | the dictionary and the policy schedule | readable |
| R1 2025 experience alone, trended | the lag report | readable |
| R2 (default path) each employer's three years trended | the memo and the lag report | readable |
| R3 (decisive) each employer's experience weighed by its credibility | nothing: no sentence names credibility, a manual rate, a pooling point or a full-credibility standard; the plan summary describes the design and the stop-loss only | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | completeness of each plan year | claims paid through March of the next are complete | a lag allowance | same call | memo section 3; every cell within three months (SF1) |
| SF2 | May 2026 in both lag reports | one cell | both | same call (May 2026 carries no 2023 to 2025 claims beyond March; identical cells, asserted) | the manifest's coverages; SF2 |
| SF3 | member months | a member enrolled in the month | persons | same call (no reissued id before July 2026, asserted) | memo section 2; SF3 |
| SF4 | pharmacy rebates | before rebates | net | not filed alternatives | memo section 2 |
| SF5 | trend | each year's retained claims at 7 per cent a year | each claimant trended before the deductible | same call (asserted, L1b) | memo section 3 |
| SF6 | the experience window | incurred 2023 to 2025, paid through March of the next | with 2026 to date | not filed alternatives | memo section 3, "2026 are not yet complete and are not part of the review" |
| SF7 | the credibility form | Buhlmann-Straub with member-month weights, the trust's member-month level the complement | the employers' simple mean as complement; limited fluctuation at 1,000 to 3,000 lives; trend before the deductible | same call (asserted, L1b, C2) | checks.py L1b and C2 |
| SF8 | the reimbursements | the claims over $150,000 in full | partial | same call (asserted) | SF8 |

## Ladder

Built values from the cut pack (generator/checks.py L1 to L4, C2, C3), expected 2027 retained PMPM, dollars.

| Rung | Route | Surcharged | CR104, CR109, CR136 / CR113, CR118, CR131, CR149 |
|---|---|---|---|
| R0 | the trust's level ($500.25) for every employer | the golden six and CR181 | 500.3 each |
| R1 | 2025 experience alone | CR104, CR109, CR136, CR167, CR176 | 883.8, 634.8, 623.4 / 331.6, 365.2, 349.9, 396.9 |
| R2 (default path) | each employer's three years | CR104, CR109, CR136, CR167, CR176 | 578.2, 628.4, 672.6 / 459.6, 445.6, 452.5, 421.5 |
| Golden | credibility-weighted (Buhlmann-Straub) | CR113, CR118, CR131, CR149, CR167, CR176 | 511.2, 522.5, 557.9 / 492.5, 488.5, 486.1, 466.0 |

- Dominance: every credibility form sits on one side of each employer's claims component, 2.4 per cent or more from it
  (C2), and each employer the two sets differ on stands 2.4 per cent or more the other way on its own experience (C3).
  CR181, the largest employer, is under on every form but over at the trust's level, so the call is not "the trust's
  level for everyone".
- The data separates the readings: the employers' years spread around their own means by an expected process variance
  of 14.4 million per member month against a variance of the true levels of 1,973, so an employer needs 7,285 member
  months for its experience to count for half.

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | each member employer's members in 2027 | filed (memo 2) |
| 2 | Unit of account | per member per month | filed (memo 2) |
| 3 | Attribution window | plan year 2027 | filed |
| 4 | As-of dating | the extracts of 7 October 2026 | manifest |
| 5 | Version basis | one cell per employer, month, paid month and category | SF2 |
| 6 | Denominator | member months | filed (SF3) |
| 7 | Weighting | member months | SF7 (every form one call) |
| 8 | Window length | plan years 2023 to 2025 | filed (SF6) |
| 9 | Boundary inclusivity | exceed is strictly over | C2 (no employer within 2.4 per cent) |
| 10 | Rounding path | unrounded against the claims component | prompt |
| 11 | Tie-break | none | C2 |
| 12 | Maturity and censoring | each year complete by March | SF1 |
| 13 | Order of operations | conform, net, trend, weigh, compare | commutes (SF5) |
| 14 | Row order | none | commutes |
| 15 | Duplicate resolution | May 2026 once | SF2 |
| 16 | Identity normalisation | employer ids across layouts | the dictionary |
| 17 | Netting against gross | net of reimbursements, before rebates | SF4, SF8 |
| 18 | Dimensional units | cents against dollars | the dictionary |
| 19 | Code and status semantics | MED and RX | the dictionary; never the stump |
| 20 | Integerisation | none | commutes |
| 21 | Clause scope | the test applies to every employer | filed |
| 22 | Forward window contents | 2027 not yet incurred, plan and employers unchanged | filed (memo 2) |

## Literal reader

The memo executed word for word asks for each employer's expected 2027 retained claims PMPM from the trust's 2023 to
2025 experience trended to 2027; the literal question is what an employer's members are expected to cost, which for a
small employer its own three years answer only in part, the trust's experience supplying the rest. A literal reader
who takes an employer's own trended experience as its expectation has assumed its record carries no chance, which the
spread of its years contradicts; every other reading converges or violates a quoted sentence (fork table). Re-run on
the finished pack.

## Oracles

- No shipped file carries an expected claims figure, a manual rate, a credibility or a ranking of the employers on 2027.
- The rebate statement, the roster and the broker survey are distractors (metadata.json); none ranks the employers on
  2027.
- No control ties only under the golden on the asks.

## Ask sheet

- **Ask A, each employer's July to September 2026 member months (eighteen figures, whole numbers).** H18 home: the
  member months the third-quarter contributions are billed on, the base a surcharge is billed against (memo section
  4). Path: the eligibility file. Primary device: D7, codes reissued: Hallam moved every employer to a new member-id
  scheme in July or August 2026, reissuing each member from the move month, while about two fifths of the families
  kept their old ids on the file for one or two more months; only birth date, sex and relationship within the
  employer tie the two ids. Hazards: the subscriber id changes too.
- **Ask B, each employer's members on the 2026 high-cost claimant report and their claims paid to date as last
  reported (eighteen employers, two figures each, whole numbers and whole dollars).** H18 home: which employers carry
  large claims into 2027 (memo section 4). Path: the high-cost report (report month, member id, employer, paid to
  date), the eligibility file. Primary device: D1, the same records under two key schemes: the report carries each
  member under the id the eligibility file carried that month, so a member reported before and after the move appears
  as two members, each with claims to date. Hazards: the latest row, not the highest or the sum.
- **The construction layer:** the call, the eighteen decisions and the chart; the cracker has them.
- **Main population zero-counts (asserted):** the call reads 2023 to 2025 eligibility, the lag cells, the
  reimbursements and the elections; every reissued id sits in July 2026 or later and the high-cost report is read by
  ask B only (X1).
- **Hazard table (asserted):** A1 to A3, B1, B2 in checks.py; none moves the call.
- **Referee:** none.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| A, July to September member months | a row per member id and month, no repeated key to resolve; keeps 0 of 18 | miss |
| B, high-cost members and claims to date | the latest row per member id; keeps 2 of 36 | miss |

- Mirror leakage: 3.7 per cent of ask weight on the cut pack (2 of 54).
- Pair ceiling: 36.6 on the cut pack (weights 38 / 7 / 55: the cracker keeps the call and instructions, 47.0; the
  mirror at the default path misses the set and keeps 11 of 18 decisions, 26.1). Re-measured by the stage 4 readers.
- Measured by: generator/ceiling.py on the cut pack.

## Pre-ship check

- Readers (two Sonnet, medium, fresh unzips of target.zip, the neutral brief, 2026-10-21): both took each employer's own trended experience and filed CR104, CR109, CR136, CR167 and CR176 (the default path); score_reader.py exit 0 for both, call missed, asks 2 of 54 (3.7 per cent); both named no sentence carrying the decisive step and called the review lines harmless.

- Judge (hand-built brief, Sonnet, medium): DETERMINISTIC, APPROVE; the set reproduces under Buhlmann-Straub, limited fluctuation at 1,000 and 3,000 lives and k from half to twice its estimate; Gate G method_or_model_selection, analytical_non_defect, surface_read_dependency no; Gate H domain pass, layers pass, decisive_step analytical. Report: determinism_check_report.md.
- The 10/10 rules re-read against the built pack: the decisive step is credibility (analytical), the mess (two lag layouts, policy rewrites, reissued ids) is Layer 1 and moves no decision.

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
- Architecture 3, self-funded groups' 2027 retained claims under a fixed specific deductible (2026-10-21, spent at
  stage 4): reader 2 re-applied the $250,000 deductible to each large claimant's trended claims and landed the call
  (exit 1, 22 of 80); reader 1 trended the retained total and missed (exit 0, 9 of 80). Leveraging under a fixed
  deductible is textbook to a strong reader once a fixed deductible and a claimant list sit side by side; both readers
  missed both ask devices (reissued member ids, a reopened claimant file), which are worth re-skinning.
- Architecture 4, a charter network's spring benchmark rescored for rapid guessing (2026-10-21, spent at stage 4):
  both scored readers took the vendor's scores and missed the call, but the judge returned DETERMINISTIC and SEND_BACK
  on Gate G (planted_defect_flip): leaving out rapid-guessed responses is cleaning contaminated rows, the stump
  collapses on clean data, and the vendor's score report is a shipped figure that ranks the campuses wrongly. The asks
  leaked 85.7 per cent because a temporary id register and two named rosters documented both devices. A decisive
  step that removes bad responses is Layer 1, and any shipped report of the easy route's figure is a Gate G artifact.
- Architecture 5, a schools health cooperative's 2026 plan year completed under each district's 2026 deductible (2026-10-21, spent at stage 4): both scored readers completed each district's January to June 2026 by the 2025 factor of its 2026 plan, naming deductible leveraging unprompted, and landed the call and every expected PMPM (exit 1, 32 of 64 each); reader 7 also resolved ask A's reissued ids on person attributes, while ask B's reopened claimant files held for both. A field-standard correction whose inputs (a design history and per-unit experience by design) sit side by side in the pack is found by a strong reader; the judge thread was stopped as moot.
- Adverse selection in dual-option employers as the decisive step (2026-10-21, screened at the draw): a simulation of members choosing the high-deductible plan by their own risk put the electees' plan-year factor at 1.06 to 1.12 against 1.19 for a whole-employer move, but a dual-option employer's blended factor stayed within 0.005 of its own history and plan-level pooling is dominated by the non-electees' claims, so neither the easy route nor plan pooling moved the call.
