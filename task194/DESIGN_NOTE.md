# task194 design note

Placing a scarce improvement team when the unit standing worst is partly standing worst by chance.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task194.json`, filed and committed with this note |
| Domain, task type | healthcare-delivery-health-economics, `provider-quality-risk-adjustment` |
| Objective | Anomaly Detection & Diagnostics |
| Shape | 11 |
| Decision | pick_one_of_n, named_option |
| Gate G | `method_or_model_selection`; decisive generator G14, G18 |
| Strategy | `causal_design` |
| Layer 2 | `estimand_identification`, own pattern `own:reversion-against-effect-in-a-chosen-worst-unit` |
| World | Australia, hospital network |
| As-of date | 2027-03-15 |
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

A competent solver builds each unit's last-quarter rate of the outcome, confirms it against the dashboard, ranks the units and embeds with the worst, which is the unit with the most room to revert rather than the unit an embed moves most.

## Tried and rejected

- (nothing yet)
