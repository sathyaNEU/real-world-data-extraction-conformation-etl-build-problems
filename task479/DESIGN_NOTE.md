# task479 design note

Status lives in `pipeline.json`; this note holds the design. Architecture 2, drawn 2026-10-21 after architecture 1
(NFIP claims replayed on elevated buildings) was spent at stage 4; nothing of architecture 1's world or step is kept.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task479.json` (architecture v2, lineage v1 spent), registered 2026-10-21
  after a pull. Guard WARN only, answered here: `overuse.objective` (ETL in 9 of the last 12): the lane is ETL by
  assignment. `test.same_driver_older` (time, G9, forecasting) against task133 is answered by the card's
  differentiation line. Redrawn at the draw: shape 01 (task484's) to 05, forcing event budget_or_appropriation
  (task480's) to season_or_peak, decisive generator G13 and then G16 (spent signatures) to G9, the panel's survival
  against the whole's acquisition of new members. People: Samantha Walter and Debbie Brady, from `guard.py names --geo
  us --seed 479`.
- **Pairing:** Survey Research & Official Statistics, task type `seasonal-adjustment-official-time-series-production`,
  which serves ETL: a monthly member panel benchmarked to the Department of Revenue's annual county receipts and
  restated onto that basis for the year the Department has not yet published. Objective: Data Extraction &
  Conformation.
- **The decision and the quantity:** a state lodging association matches its member counties' 2027 summer co-op
  marketing from a fixed Rising Destinations fund, split across the counties whose taxable lodging receipts grew at
  least five per cent from 2024 to 2025, in proportion to their 2025 receipts. The Department publishes 2025 in
  early 2027, after the season's co-op budgets close, so 2025 is restated from the association's monthly Lodging
  Monitor panel onto the Department's basis. The call is retrospective on its window (calendar 2025, closed) and forward
  on its release: the figure is the one the Department will publish, a year before it does.
- **Data-native sentence:** the Monitor panel was drawn in January 2018 from the members then reporting and takes no
  property opened since, so in the counties where hotels keep opening the Department's receipts have outgrown the
  panel's by a steady few points in every year both are known, while in a county that has been losing its non-member
  properties the panel has outgrown the Department; the 2024 ratio of the Department to the panel is a year behind 2025.
- **Strategy:** `forecast_method_backtest` (no back-test is filed: the pack lets an analyst ask how carrying the last
  benchmark by the panel's movement would have done in each earlier year). Gate G `forecasting`; gap `time`; generators
  G9, G13, G16. Layer 2 family `forecast_uncertainty`, pattern `own:benchmark-to-indicator ratio extrapolated on its own
  path past the last benchmark`.

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
