# task193 design note

Triaging which signals a capped assessment team takes, when one member of the comparison set dominates it.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task193.json`, filed and committed with this note |
| Domain, task type | pharmacology-pharmacoepidemiology-safety, `safety-signal-detection` |
| Objective | Anomaly Detection & Diagnostics |
| Shape | 16 |
| Decision | designation_set, set_of_items |
| Gate G | `signal_vs_noise_or_hold`; decisive generator G5, G8 |
| Strategy | `population_selection` |
| Layer 2 | `estimand_identification`, own pattern `own:comparison-set-holding-the-measure-down` |
| World | Denmark, national medicines agency |
| As-of date | 2027-02-08 |
| Guard | registered at WARN; the differentiation lines are in the card |

**Data-native sentence.** To be written with the default path, from this pack's own generating process.

**Sources read.** `analytical_tasks/02_anomaly_detection/` (seed): the decision shape only, per the card's `slot_note`;
`guard.py mechanisms --objective anomaly-detection`, read before the draw, with the driver measured
against every card on file by `guard.py nearest`.

## Default path

To be written at stage 2, before any data is cut.

**Ends on:** to be written.
**Golden:** to be written.

## Stump sentence

A competent solver computes each product's proportional reporting ratio against the whole database, takes the ones above the filed threshold within the hours the contract allows, and leaves out the products whose measure is depressed by the one product that dominates the reaction's reports.

## Tried and rejected

- (nothing yet)
