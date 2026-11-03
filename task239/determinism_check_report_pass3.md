# determinism-check report, task239, 2026-11-03 (the repaired reship cut, target.zip 96f49ade, the one re-judge)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated thread (Sonnet, medium) read only a fresh unzip of the cut and the prompt, wrote its derivation before it
opened the graded blocks (order kept), and recomputed every figure. WI-SV-03 4.1 and 4.2 define a team's level as the
score a member is expected to give, so the loading is on the between-team factor with the members' sampling noise
taken out: TC01 to TC10 stay at about 0.9 and TC11 and TC12 are withdrawn at about 0.0, 0.13 or more above the line and
0.7 or more under it. No return-handling fork it computed moves the decision or the one-decimal loadings.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Returns that count | 11,482 | 11,482 | yes |
| Reported teams, returns used | 1,016, 8,323 | 1,016, 8,323 | yes (each channel read by the team list in force) |
| Loadings, TC01 to TC10 | 0.9 at one decimal | 0.89 to 0.94 (ML and principal axis agree) | yes |
| Loadings, TC11 and TC12 | 0.0, any value from -0.2 to 0.2 | 0.01 to 0.02 | yes |
| Plans per item, targets and agreed | 24 figures | all 24, drafts included as the note files; the same with the page ordered on rounded or unrounded figures | yes |
| The slide | loadings against the 0.75 line | consistent with ask 1 | yes |

## Competing answers that survived
None moves the call or ask 1 and 3. Forks tried: the five reused codes read as the current team, as no team or by
channel; dedupe before or after the filters; no dedupe at all (teams 1,030 to 1,061, complete returns 8,605 to 9,107):
TC01 to TC10 at 0.88 to 0.92 in each, TC11 and TC12 at 0.01 (0.08 to 0.10 with no dedupe at all). On ask 2 the judge
records a medium residual risk: nothing filed says that the integers saved from 1 to 5 November are rows of the team's
page; it inferred the reading from the integers' distribution (1: 140, 2: 105, 3: 83), which matches the page ranks of
the code-held targets (1: 202, 2: 148, 3: 100) and not item numbers (read as item numbers, TC01 would be 226 plans and
149 agreed). Missing the tablets' list reload or the re-sent sessions moves ask 2 by 1 to 5 per item.

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
stump_class analytical; its Gate H line (domain pass, layers pass, decisive_step analytical: the easy route factors
the team-mean correlations and files eight) matches the card's analyst_test and domain_test. No distractor named as a
surface read.

## Stump power (Gate F)
Good: a capable analyst who cleans the returns and reads every rule can still factor the team means and file eight, or
the members' answers and file none; only the between-team estimate files ten. The cleaning is Layer 1 and moves no call.

## Findings, ranked
1. Ask 2's integer targets read as page rows by inference (medium residual risk). The thread's optional fix, a
   methodology sentence saying the early-November export stores a target as its row on the team's page, is declined:
   it would file the device's own resolution, making the ask executable for a careful solver, and it would change a
   solver-visible file after the judged cut. The decline and the risk are recorded in the design note's ask sheet.

## Next action for the author
Ship the judged cut unchanged.
