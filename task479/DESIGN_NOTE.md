# task479 design note

Status lives in `pipeline.json`; this note holds the design. Architecture 6, drawn 2026-10-21 after architectures 1
to 5 were spent at stage 4; nothing of any earlier world or decisive step is kept (the ask devices that held in
architectures 3 and 5 are re-skinned).

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task479.json` (architecture v6, lineage v1 to v5 spent), registered
  2026-10-21 after a pull. Guard WARN only, answered here: `overuse.objective` (the lane), `people.first` (Michelle,
  drawn by `guard.py names --geo us --seed 4796`). Redrawn at the draw: gap population with G17, then time with G13,
  then population with G16 (same-puzzle blocks against task471, task178 and task480) to gap time with G16, Gate G
  `signal_vs_noise_or_hold`, differentiation lines for task130, task148 and task241. People: Steven Coleman and
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

To be written at stage 2 from the generator's clean truth.

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
