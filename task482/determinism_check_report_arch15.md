# determinism-check report, task482, 2026-10-31

## Verdict
NOT_DETERMINISTIC (underspecified_objective)
**Disposition:** SEND_BACK
**Stumping type:** mechanism: other (counterfactual costing with deferral adjustment), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Read literally, F-17 s.2 and s.4 cost "the plan year's services" from the 2025 claims. That gives 35.81 / 36.64 / 37.04 (+0.83 / +1.23), both inside USD 1.90, so the literal answer is 3,000, not the golden's 2,000. The golden needs a deferred-work add-on (2025 predetermination estimates the maximum reduced, their procedures claimed after 1 Jan 2026 added to 2025 persons at 2027 fees, baseline left at actual claims) that no shipped text states. The design note's own `Not rule application` line says no filed rule adds that work, so the decisive rule is withheld and the call is not forced.
Thread's source: /tmp/determinism-check-task482-r1/verdict.md.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Covered persons / months | 6,934 / 76,380 | same | yes |
| Cost at 1,500 / 2,000 / 3,000 | 2,735,231.20 / 2,853,526.70 / 2,914,027.70 | same | yes (only under the add-on) |
| Per month, increases | 35.81, 37.36, 38.15; 1.55, 2.34 | same | yes |
| Put-off work | 103 members, 94,459.50 | same (reduced lines only: 79,769.00) | yes, one population of two |
| Without add-on | none | 1.23 at 3,000 | literal reading gives 3,000 |
| Ask 3 by quarter | 322/313 ... 195/177 | same | yes (UTC and E-id forks derivable) |
| Ask 4 ortho dollars | 310.41 / 16,590.05 / 41,200.84 | same | yes |
| Ask 4 child counts | 1 / 39 / 43 | 2 / 40 / 43 by band date plus treatment_months | no, needs a zero-owed drop |

## Competing answers that survived
- Main call: no add-on gives 3,000; add-on in the baseline too gives +1.28 / +2.08; reduced lines only gives +1.46 / +2.16 (all keep 2,000). The shipped rule that would close it is absent.
- Deductible basis: 34 D4910 lines with no deductible; re-applying the SPD gives 35.79 / 37.34 / 38.13.
- Put-off population in CSV ask 2: 94,459.50 against 79,769.00.
- CSV schema: the prompt never requests the put-off or cost columns that ask 2 grades.
- Ortho "still in treatment": 2/40/43 against 1/39/43; blank member_ref on OC03294 gives 44 children and 42,272.27 for 2026.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats | 10+ / 3+ | 19 / csv, pdf, xlsx | yes |
| Large file | 25,000+ rows | 49,271 and 96,424 rows | yes |
| Distractors | 2+ in metadata, none named in a file name | 4 named (network access, admin fees, two accumulator files) | yes on count; the accumulator files likely feed the reconciliation, so check they are unused by the solution |
| Deliverables | 1 to 3, all in golden | 3, all present | yes |
| Asks | unit and rounding stated | cents stated; CSV columns for ask 2 not asked | no |
| Rubric 25+ criteria, shape identifiable | | not measured here | not checked |
| Reads as real | | judge found nothing LLM-like | yes |

## Gate G reconciliation
Thread: surface_read_dependency no, sole_data_defect no, analytical_non_defect. The design note's stump sentence has the same default path (static continuance, 3,000 at 1.23), so the mechanism matches. The declared distractors are not the surface read. The mismatch is on determinism, not on type: the note concedes that no filed rule adds the work. No Gate G ban.

## Stump power (Gate F)
The easy route is the literal F-17 reading, so a model landing 3,000 is a defensible-reading model, not an analytically wrong one. Gate H, decisive step: the thread says analytical but borderline hidden rule; I class it as a withheld rule, to be settled by filing the estimand (the WHAT) in the pack.

## Findings, ranked
1. Main call rests on an unfiled deferred-work add-on; literal reading gives 3,000 (SEND_BACK).
2. CSV ask 2 totals not derivable (population fork 94,459.50 / 79,769.00; columns never requested).
3. Deductible basis fork on 34 lines (0.02 on printed per-month figures).
4. Ortho counts depend on an unstated "in treatment" test; OC03294 unlinkable.
5. Spec: confirm the accumulator distractors are unused.

## Next action for the author
File the estimand (WHAT only: the 2025 costing includes work the 2025 predeterminations planned that the maximum pushed past the plan year, whenever done) in F-17 or the prompt, leaving the lines and window method open; then name the CSV columns, pin the deductible basis and the "in treatment" test, and rebuild.
