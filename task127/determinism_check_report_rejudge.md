# determinism-check report (re-judge), task127, 2026-11-08

Cut: target.zip md5 340dec2a4c5e4d03f31d59d0c0d84d04 (16 files). Thread: one sonnet/medium pass, verdict at /tmp/determinism-check-task127-rejudge002509/verdict.md.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor (contagion against a control baseline, binding_constraint knapsack), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The thread recomputed every load-bearing value from the bundle. The call (Kinloch Engineering + Matai Valley Foods, NZ$3,350,000 at NZ$5.8m of lines) is unique; the runner-up pair (Matai + Ridgeway) is NZ$3,200,000, margin 150k. The one residual: terms 3.5 values write-off over every borrower on the book, and the dependant knock-on is implied rather than instructed; the thread judged it the intended analytical estimand, not an open fork.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Dependants of Matai / Ridgeway | 8 / 1 | 8 / 1 | yes |
| Exposed default rate | 13 of 31 | 13 of 31 | yes |
| Control rate | 5 of 211 | 4 of 199 or 4 of 207 depending on cohort choices | no, exact count differs; uplift 0.399 vs 0.3957, no rounded figure moves |
| Matai package | 1,750,000 | 1,749,979 | yes |
| Ridgeway package | 1,450,000 | 1,465,342 | yes (rounds to 1,450,000) |
| Kinloch / Marlowe / Selwyn / Brightwater / Coastline / Northgate | 1.60m / 1.05m / 0.70m / 0.45m / 0.35m / 0.25m | same | yes |
| Matai own expected write-off | 817,000 | 817,175 per design note, consistent | yes |
| Best pair | 3,350,000 | 3,350,000 | yes |
| Security values (8) | listed | all | yes |
| Commitments (8) | listed | all | yes |
| Sector shares (7) | listed | all | yes |

## Competing answers that survived
- Own expected write-off only: Kinloch + Ridgeway about NZ$3.0m. This is the intended default path, not a competing golden: the filed estimand (book with package against book without, members not yet in default included) excludes it.
- Raw 13/31 with no baseline: Matai 1,806k, rounds to 1,800,000, total 3,400,000, same pair. Differs in the headline and Matai line. The terms' comparison wording and the write-up's stated control group close it; the thread did not count it as an open fork.
- Baseline from dependants' run PDs: 1,747k, rounds to the same 1,750,000.
- Control count 5/211 vs 4/199 or 4/207: moves no rounded figure.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / large file | 10+ / 3+ / 25,000+ rows | 16 / csv, xlsx, pdf / 281,664 rows | yes |
| Distractors in metadata.json, none labelled by file name | 2+ | sector_risk_appetite_2027.pdf, regional_economic_indicators_2019-2026.csv; no file name labels one | yes |
| Distractor unused yet weighable, none answers a graded quantity | yes | The appetite PDF gives sector appetite and limits (Reduce on E and G) and the regional series gives economics; neither reproduces a graded figure, and the appetite PDF says it does not change how existing borrowers are managed | yes |
| 1 to 3 deliverables, all in golden | yes | 2 (xlsx, docx), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | per-borrower write-off, security, commitment, plus 7 sector shares; units and rounding in the prompt | yes |
| Prompt shape identifiable, 25+ criteria | yes | one grading line per borrower per quantity and per sector, about 40 gradable figures plus recommendation and components | yes |
| Not LLM-reading, goldens business-real | yes | thread found no provenance leakage; golden realism was checked at build | yes |

## Gate G reconciliation
Thread: mechanism statistical_rigor with a binding-constraint knapsack, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: stump_class analytical; stump is valuing each package at the borrower's own expected write-off against the golden with dependants' contagion. Match. The declared distractors (appetite PDF, regional indicators) were not named by the thread as the surface read; the surface read it named is the IFRS 9 own expected loss, a true record with no wrong ranking planted. No finding. Minor: the card's analyst_test says the easy route ends at about NZ$3.1m while the note and thread say NZ$3.0m; tidy the card.

## Gate H line
domain: pass, layers: pass, decisive_step: analytical. The thread names expected-credit-loss contagion estimated against a matched control, then chosen under the envelope. This matches the note's Domain test, Layer 1 and Layer 2, decisive step, and its `Not semantics`, `Not rule application` and `No decoy` lines. The decisive step is an estimand and rate estimated from dated defaults, not a field reading or an executed rule.

## Stump power (Gate F)
A strong solver ranking on own PD x LGD x EAD files Kinloch + Ridgeway at about NZ$3.0m and loses the call. A solver who finds the dependants but skips the baseline gets the right pair and a wrong headline (3.4m) and Matai line. Missing the legacy account resolution also drops the dependants. Not a textbook route a solver lands by method alone: the dependence and its uplift are found from the bank's own two tables, with no method filed. The main thread weighs this against the note's ladder.

## Findings, ranked
1. Low: the judge's control count does not reproduce 5 of 211 exactly (4 of 199 or 4 of 207), though the uplift and every rounded graded figure are unaffected. Confirm that the write-up states the control cohort rule so a reader reaches 211.
2. Low: dependant knock-on is implied by terms 3.5, not instructed; the thread classed it as the intended trap. Not recommended to change.
3. Trivial: the card's analyst_test figure (3.1m) differs from the note and thread (3.0m).

## Next action for the author
None required for determinism; optionally align the card's analyst_test figure to NZ$3.0m and proceed to ship.
