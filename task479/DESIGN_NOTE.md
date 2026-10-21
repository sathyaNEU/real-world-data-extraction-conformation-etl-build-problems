# task479 design note

Status lives in `pipeline.json`; this note holds the design. Architecture 5, drawn 2026-10-21 after architectures 1
to 4 were spent at stage 4; nothing of any earlier world or decisive step is kept (the ask devices that held in
architecture 3 are re-skinned).

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task479.json` (architecture v5, lineage v1 to v4 spent), registered
  2026-10-21 after a pull. Guard WARN only, answered here: `overuse.objective` (the lane), `repeat.gate_g` against
  task178 and task179 (a full plan year projected from its first half is a forecast), `people.first` (James, drawn by
  `guard.py names --geo us --seed 479`). Redrawn at the draw: generators G7 then G6 and G3 (spent signatures) to G4,
  the attribution at the plan-design transition. People: Brady Cooper and James Hernandez.
- **Pairing:** Healthcare Delivery & Health Economics, task type `payment-claims-health-plan-analytics`, which serves
  ETL: the plan administrator's claims lag report, the enrollment file and the plan design history conformed by
  district and restated from January to June 2026 onto the full 2026 plan year.
- **The decision and the quantity:** the cooperative's trustees raise the January 2027 contributions of the member
  districts whose expected full 2026 plan-year plan-paid claims per member per month exceed the claims component of
  their 2026 contribution rate. Forward facing: July to December 2026 has not been incurred.
- **Data-native sentence:** a plan pays little in the first months of a plan year while its members meet their
  deductibles, less the higher the deductible; four districts moved from a $500 to a $3,000 deductible on 1 January
  2026, so their own 2025 says how a $500 plan year falls, not a $3,000 one.
- **Strategy:** `composition_mix`; Gate G `forecasting`; gap `time`; generators G4, G13. Layer 2 family
  `forecast_uncertainty`, pattern `own:a partial plan year completed by the share its months carry under the year's own
  benefit design`.

## Default path

A strong analyst with every field read correctly:

1. Reads the memo: a district's contribution rises when its expected plan-paid claims PMPM for plan year 2026 exceed
   the claims component of its 2026 rate, the evidence its January to June 2026 claims (paid through 30 September)
   and the cooperative's 2025 experience.
2. Conforms the two lag reports (the May 2026 cells once), counts member months, sees that January to June 2025 carries
   less than half of every district's 2025 plan year, and completes each district's January to June 2026 PMPM by its
   own ratio of plan year 2025 PMPM to January to June 2025 PMPM (the year-over-year form, January to June 2026 over
   January to June 2025 times plan year 2025, is the same number).
3. Compares with the claims component.

**Ends on:** MV03, MV25 and MV36 raised

On that path MV07, MV21 and MV47 read $438.8, $451.3 and $446.1 against claims components of $459.80, $475.87 and
$468.15.

**Golden:** MV03, MV07, MV21, MV25, MV36 and MV47 raised; MV07, MV21 and MV47 complete to $482.3, $498.3 and $488.2
on plan MVC's 2025 factor (1.1705) where their own 2025 on plan MVA gives 1.0649, 1.0601 and 1.0695.

## Stump sentence

The default path completes each district's January to June 2026 plan-paid claims by its own 2025 and files MV03, MV25 and MV36 raised, because it never asks whether a plan year's claims fall the same way under a different deductible: Brantmoor, Farrowdale and Northam Vale moved from the $500 plan to the $3,000 plan in 2026, whose first half carries less of the year, and they are short of their claims components.

## Three rules

Task type: payment-claims-health-plan-analytics (Healthcare Delivery & Health Economics): the administrator's claims lag reports in two layouts, the eligibility file and the benefit designs conformed by district and plan and restated from January to June 2026 onto the full 2026 plan year, a conformation serving Data Extraction & Conformation (ETL).

Domain test: the deciding quantity is each district's expected plan-year plan-paid claims per member per month, worked the way a health plan actuary completes a partial plan year: plan-paid claims are seasonal within a plan year because members satisfy deductibles first (deductible leveraging), so the completion factor for a part year is a property of the benefit design and is taken from experience on that design.

Swap: "which stores' full-year sales exceed their budget, from January to June" keeps a part year completed by a seasonal factor and loses the step: no deductible resets each January, so a store's own last year is its seasonal pattern and nothing about a change in how the customer pays moves where the year's sales fall.

Layer 1: the claims lag report in two layouts across the May 2026 platform move (MM/YYYY dollars against YYYY-MM cents, May sent by both), the plan design table inside a PDF, member ids reissued at the summer 2026 payroll move, policy numbers rewritten at the 2026 stop-loss renewal; each is how the producing system writes, nothing is placed to be caught, and checks.py asserts the call holds under them (SF3, SF4, X1).

Layer 2: forecast_uncertainty, the reference pattern a part year is completed by: the choice that flips the call is completing each district's first half by the plan-year factor of its 2026 benefit design, measured on the districts that ran that design through 2025, instead of by the district's own 2025 under a different design.

Decisive step: completing Brantmoor, Farrowdale, Isenbrook and Northam Vale's January to June 2026 claims by plan MVC's 2025 factor (1.1705, Eversley Plains, Kestrel Point and Pellow Ridge pooled) rather than their own 2025 factors on plan MVA (1.0601 to 1.0695), which puts MV07, MV21 and MV47 over their claims components.

Not semantics: every field, unit and definition read correctly (the lag report's two layouts, cents and dollars, the plan codes, the deductibles, member months, plan-paid gross of stop-loss and before rebates) still leaves the easy route completing each district by its own 2025, because no field says a plan year's claims fall differently under another deductible; the step is the inference that the seasonal pattern belongs to the benefit design, which the 2025 factors by plan show and no sentence says.

Not rule application: the memo fixes the population, outcome, window, unit and comparison and names the evidence, and no rule says how a part year is completed or from which districts' experience; executing every filed rule with each district's own 2025 files MV03, MV25 and MV36 raised.

Analyst test: a strong analyst who conforms every file and reads every rule, completing each district by its own 2025, files MV03, MV25 and MV36 raised (the default path's Ends on); one who completes every district by one cooperative-wide factor files MV03 and MV25; one who doubles January to June files none; only completing each district by its 2026 plan's 2025 factor files the golden six; checks.py runs them on the clean truth (R3a, R3b, R3c).

Estimand: the contribution review memo (mvshc_contribution_review_january_2027.pdf, sections 2 and 3): the population (each member district's plan in plan year 2026), the outcome (plan-paid medical and pharmacy claims, gross of specific stop-loss reimbursements and before pharmacy rebates), the window (plan year 2026, January to December 2026), the unit (per member per month over the district's member months) and the comparison (exceeding the claims component of the 2026 contribution rate), the evidence January to June 2026 incurred claims paid through 30 September 2026 and the cooperative's plan year 2025 experience paid through 31 March 2026.

No decoy: nothing is planted: the lag reports, eligibility, designs, advisories and rates are the producing systems' records, the memo states the basis without a method, and no projection, earlier review, actuarial report or published figure ranks the districts on plan year 2026.

No certified replay: no certified or published completion factor or projection ships; the method is not recovered by reproducing any figure.

Lesson: a part year is completed by the seasonal pattern of the process that generates it, and in a health plan that pattern belongs to the benefit design, since members meet a deductible before the plan pays; a district that changed design has no history of its own new year, so its factor comes from experience on the design it now runs; no build on file completes a partial period by a pattern borrowed from units under the same regime.

## Readability screen

Each rung, the sentence or file a reader would have to read to take it, and whether any shipped text hands it over.

| Rung | What takes the reader there | Verdict |
|---|---|---|
| R0 January to June doubled | the memo's plan-year window | readable |
| Layer 1: two layouts, reissued ids, policy rewrites | the dictionary and the manifest | readable |
| R1 one cooperative-wide 2025 factor | the memo's "the cooperative's experience in plan year 2025" | readable |
| R2 (default path) each district's own 2025 factor | the lag report by district | readable |
| R3 (decisive) each district's 2026 plan's 2025 factor | nothing: no sentence ties a plan year's seasonality to the deductible or names a completion factor, the designs PDF lists the plans and the moves without a word on claims timing | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the form of the completion | plan-year PMPM over January to June PMPM, pooled ratio of totals | mean of the districts' ratios; paid share over twice the January to June member months; own 2025 times the design relativity | same call, every figure in its ten-dollar bin (asserted) | checks.py SF1, SF1b |
| SF2 | completeness of the periods | January to June 2026 paid through September and 2025 paid through March 2026 are complete | a lag allowance | same call | memo section 3; every cell within three months (SF2) |
| SF3 | May 2026 in both lag reports | one cell | both | not filed alternatives (identical cells, asserted) | the manifest's coverages; SF3 |
| SF4 | member months | a member enrolled in the month | persons | same call (no reissued id before July 2026, asserted) | memo section 2; SF4 |
| SF5 | pharmacy rebates | before rebates | net | not filed alternatives | memo section 2 |
| SF6 | specific stop-loss | gross | net of reimbursements | not filed alternatives | memo section 2 |
| SF7 | the plan year | January to December 2026 | the districts' fiscal year | not filed alternatives | memo section 2; the designs PDF |
| SF8 | exceed | strictly over | at or over | same call (no district within 2.5 per cent, C2) | memo section 2 |

## Ladder

Built values from the cut pack (generator/checks.py L1 to L4, C2, C3), expected plan year 2026 plan-paid PMPM, dollars.

| Rung | Route | Raised | MV07, MV21, MV47 (claims components 459.80, 475.87, 468.15) |
|---|---|---|---|
| R0 | January to June as it stands | none | 412.0, 425.7, 417.1 |
| R1 | one cooperative-wide factor (1.0911) | MV03, MV25 | 449.6, 464.5, 455.1 |
| R2 (default path) | each district's own 2025 factor | MV03, MV25, MV36 | 438.8, 451.3, 446.1 |
| Golden | each district's 2026 plan's 2025 factor (MVA 1.0629, MVB 1.1218, MVC 1.1705) | MV03, MV07, MV21, MV25, MV36, MV47 | 482.3, 498.3, 488.2 |

- Dominance: every district sits at least 2.5 per cent off its claims component on the golden (C2), and each of the
  three the golden adds stands at least 2.5 per cent under it on its own 2025 (C3). MV32 (Isenbrook) moved too and
  stays under on every route, so the call is not "every district that moved".
- The data separates the readings: the 2025 factors by plan are 1.0629, 1.1218 and 1.1705, and each district's own 2025
  factor sits within 0.007 of its plan's, so a district's history speaks for its design and not for the district.

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | each member district's plan in plan year 2026 | filed (memo 2) |
| 2 | Unit of account | per member per month over member months | filed (memo 2) |
| 3 | Attribution window | plan year 2026, January to December | filed (SF7) |
| 4 | As-of dating | the extracts of 6 October 2026 | manifest |
| 5 | Version basis | one cell per district, month, paid month and category | SF3 |
| 6 | Denominator | member months | filed (SF4) |
| 7 | Weighting | pooled ratio of totals within a plan | SF1 (every form in one bin) |
| 8 | Window length | January to June 2026 against plan year 2025 | filed (memo 3) |
| 9 | Boundary inclusivity | exceed is strictly over | SF8 |
| 10 | Rounding path | unrounded against the claims component, reported to ten dollars | prompt |
| 11 | Tie-break | none (no district within 2.5 per cent) | C2 |
| 12 | Maturity and censoring | both periods complete | SF2 |
| 13 | Order of operations | conform, count, complete, compare | commutes |
| 14 | Row order | none | commutes |
| 15 | Duplicate resolution | May 2026 once | SF3 |
| 16 | Identity normalisation | district ids across layouts | the dictionary |
| 17 | Netting against gross | gross of stop-loss, before rebates | SF5, SF6 |
| 18 | Dimensional units | cents against dollars | the dictionary |
| 19 | Code and status semantics | MED and RX, plan codes | the dictionary and the designs PDF; never the stump |
| 20 | Integerisation | none | commutes |
| 21 | Clause scope | the test applies to every district | filed |
| 22 | Forward window contents | July to December 2026 not yet incurred | filed (memo 2 and 3) |

## Literal reader

The memo executed word for word asks for each district's expected plan-paid PMPM over plan year 2026 from its January
to June 2026 claims and the cooperative's 2025 experience; the literal question is what share of a plan year's claims
January to June carries for a plan running the district's 2026 design, which the 2025 experience answers by design. A
literal reader who completes a district by its own 2025 has assumed its 2026 year falls like its 2025 year, which the
2025 factors by plan contradict for the four that changed plan; every other reading converges or violates a quoted
sentence (fork table). Re-run on the finished pack.

## Oracles

- No shipped file carries a completion factor, a projection or a ranking of the districts on plan year 2026.
- The rebate statement, the fiscal 2026 receipts and the state survey are distractors (metadata.json); none ranks the
  districts on plan year 2026.
- No control ties only under the golden on the asks.

## Ask sheet

- **Ask A, each district's July to September 2026 member months (sixteen figures, whole numbers).** H18 home: the
  member months the third-quarter contributions are billed on, the base an increase is billed against (memo section
  4). Path: the eligibility file (member id, subscriber id, relationship, birth date, sex, district, month). Primary
  device: D7, codes reissued: every district moved its payroll to the county system in July or August 2026 and its
  members were reissued new ids from the move month, while about two fifths of the families kept their old ids on
  the file for one or two more months; only birth date, sex and relationship within the district tie the two ids.
  Hazards: the subscriber id changes too.
- **Ask B, each district's members on 2026 specific advisory and their incurred claims to date as last reported
  (sixteen districts, two figures each, whole numbers and whole dollars).** H18 home: where a district's year rests on
  a few large claims (memo section 4). Path: the advisories (claimant number, policy, member ref, incurred to date),
  the policy schedule (2026 policy numbers, four rewritten), the eligibility file. Primary device: D1, a resubmission
  that opens no second case: Granfield opened a new claimant file when a member's id changed and carried the claims to
  date onto it, so the latest advisory per claimant number counts the member twice. Hazards: reprocessing lowers some
  latest figures (the latest, not the highest); the 2026 policy numbers.
- **The construction layer:** the call, the sixteen expected PMPM figures and the chart; the cracker has them.
- **Main population zero-counts (asserted):** the call reads 2025 and January to June 2026 eligibility, the lag
  cells, the designs and the rates; every reissued id sits in July 2026 or later and the advisories are read by ask B
  only (X1).
- **Hazard table (asserted):** A1, A2, B1 to B4 in checks.py; none moves the call.
- **Referee:** none.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| A, July to September member months | a row per member id and month, no repeated key to resolve; keeps 0 of 16 | miss |
| B, members on advisory and claims to date | the latest advisory per claimant number; keeps 0 of 32 | miss |

- Mirror leakage: 0.0 per cent of ask weight on the cut pack (0 of 48).
- Pair ceiling: 36.5 on the cut pack (weights 38 / 7 / 55: the cracker keeps the call and instructions, 45.0; the
  mirror at the default path misses the set and keeps 12 of 16 expected PMPM figures, 28.0). Re-measured by the stage 4
  readers.
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
