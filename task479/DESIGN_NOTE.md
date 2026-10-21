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
- **Strategy:** `other` (the leveraging of a fixed per-member ceiling under trend); Gate G `forecasting`; gap `time`;
  generators G1, G13. Layer 2 family `estimation_fit`, pattern `own:a trend applied to claims before a per-member cap,
  not to the capped total`.

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
