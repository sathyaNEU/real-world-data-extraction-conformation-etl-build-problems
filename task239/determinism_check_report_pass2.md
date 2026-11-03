# determinism-check report, task239, 2026-11-03 (the 11-03 reship cut, target.zip 37472ed9)

## Verdict
DETERMINISTIC (SOLUTION_WRONG in a minor sense: the loadings were given as bands while the prompt asked two decimals)
**Disposition:** FIX_NOW
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated thread (Sonnet, medium) read only a fresh unzip of the cut and the prompt, wrote its derivation before it
opened the graded blocks (order kept), and recomputed every figure. Read literally, WI-SV-03 4.1 and 4.2 file the
teams' own levels, so the factor is fitted to the between-team covariance net of the members' covariance: TC01 to TC10
load 0.89 to 0.94 and TC11 and TC12 about -0.02, ten items stay. The factor on team means keeps eight and the member-level
factor none; 4.1 rules both out as the estimand.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Returns that count | 11,482 | 11,482 | yes |
| Reported teams, returns used | 1,016, 8,323 | 1,016, 8,323 | yes (placement by channel; the reused codes read every other way move loadings 0.003 or less) |
| Loadings, TC01 to TC10 | 0.80 or more | 0.89 to 0.94 (ML, PAF, minres, EM two-level within 0.01) | yes as bands |
| Loadings, TC11 and TC12 | under 0.25 | -0.02 to -0.035, sign arbitrary | yes as bands |
| Plans per item, targets and agreed | 24 figures | all 24, with Draft plans counted | yes |
| Plans excluding Draft | | TC01 143 against 162, every target moves, agreed unchanged | the one surviving fork |

## Competing answers that survived
1. Whether a Draft plan is a plan "on the dashboard": no shipped file defined it (rated low by the judge, since the
   export is the dashboard's). Closed at the repair: the dashboard note now files that the dashboard holds a plan from
   the leader's first save, a draft until it is sent, with the manager until agreed.
2. Loadings asked to two decimals: the estimators part by 0.01 there and TC11 and TC12's sign is arbitrary. Closed at
   the repair: the loadings are asked to one decimal, where every deterministic estimator gives TC01 to TC10 0.9, and
   TC11 and TC12 are graded as any value from -0.2 to 0.2 of either sign (under 0.25 in size, the frozen component).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 13 | yes |
| Formats | 3 or more | csv, docx, pdf, xlsx | yes |
| Large file | 25,000 rows | 219,652 | yes |
| Distractors | 2 named in metadata.json | 2 | yes |
| Deliverables | 1 to 3 | 2 | yes |
| Asks with unit and rounding | each | rounding at the close | yes |

## Gate G reconciliation
The thread's mechanism (method_or_model_selection) and family (analytical_non_defect) match the card's gate_g and its
stump_class analytical; its Gate H line (domain pass, layers pass, decisive_step analytical) matches the card's
analyst_test and domain_test. No distractor named as a surface read.

## Stump power (Gate F)
Good: the easy routes (team means, or members' answers) withdraw TC09 and TC10 or everything; only the team level read
as latent keeps them. The judge expects partial stumping, since a capable analyst may take the estimand off 4.1.

## Findings, ranked
1. The loadings' precision against the prompt (fixed: one decimal, the withdrawn pair's band of either sign).
2. Draft plans unfiled (fixed: the dashboard note's sentence).

## Next action for the author
The one re-judge a FIX_NOW gets, on the repaired cut.
