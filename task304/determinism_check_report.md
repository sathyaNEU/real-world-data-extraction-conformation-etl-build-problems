# determinism-check report, task304, 2026-10-27

Judged zip: target.zip, sha256 5194480e429f78f193432468db474436e77512f2e90680f723281c92530d1976 (13 files, fresh unzip at /tmp/determinism-check-task304-r1/target/). Pass file used: determinism_check_report.md (no earlier report existed). Thread verdict: /tmp/determinism-check-task304-r1/verdict.md. prompt.txt is present (no legacy prompt.md).

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The plan paper files the estimand (population at 30 Sep 2026 less litigation and receiver accounts, first reach of two payments in arrears in 2027, no allowance for closures, planning rates, 15 per cent cut). The forecast method is open. Every term-aware method the judge built puts First-time buyer 2019-21 at 7.4 to 10.5 avoided (10 at the nearest ten) and High LTV 2022-24 at 4.3 to 4.7 (under 5). A back-test fitted to Aug 2025 and run to Sep 2026 separates the candidates: term-state model 408 FTB entries against actual 408, term-blind 385, payment-rise-only 396. The term-blind model puts High LTV first (4.5 against 2.9), so the stump is real. Gate C weak point: no file tells the solver to model the term-increase state; it is reachable from shipped data alone.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| CC1 FTB term raised at 2026 switch | 7,129 of 16,455 | 7,129 of 16,455 (history parquet) | yes |
| CC1 median extension | 10 years | 119 months | yes |
| CC1 median payment rise, raised / kept | 10% / 26% | 9.8% / 25.9% (5,687 kept) | yes |
| CC2 accounts with term raised 2024 | 347 | 347 | yes |
| CC2 two+ behind by Sep 2026 | 81 | 81 | yes |
| CC2 within eight months | 4 | 4 (3 if strictly under 8) | yes, boundary note |
| Planning rates | 4.5, 7.4, 1.9, 10.7% | reproduced | yes |
| CC3 avoided, FTB / HLTV / SO / BTL | 10 / <5 / <5 / <5 | 8.7 to 10.5 / 4.49 / 0.6 / 1.2 | yes (own chain 8.7 and cohort hazard 10.5 both bin to 10) |
| Ask A orders made or varied | 34 / 71 / 9 | 34 / 71 / 9 | yes |
| Ask A suspended on terms | 27 / 56 / 9 | 27 / 56 / 9 | yes |
| Ask A open claims 30 Sep 2026 | 17 / 43 / 2 | 17 / 43 / 2 | yes (needs possession register) |
| Ask B sold | 20 / 24 / 4 | 20 / 24 / 4 | yes |
| Ask B sold at a loss | 7 / 24 / 2 | 7 / 24 / 2 | yes |
| Ask B average loss | 4,500 / 33,300 / 3,300 | 4,495 / 33,327 / 3,314 | yes |

## Competing answers that survived
No fork flips a graded answer. Three minor notes, recorded as the thread gave them:
1. "Against the next best book" can be read as the book's own figure or as a margin; both round to about 10, so no graded figure moves.
2. "Within eight months" gives 4 or 3 by its boundary (critical component 2 only; no workbook figure).
3. The open-claim counts rest on the possession register: Ridley Varga never reports an eviction, and without the register the counts are 52 / 79 / 7 against 17 / 43 / 2. The register route is the shipped one; the `statement` choice (latest or first) moves nothing at the stated rounding.

Residual (not a fork on the call): the forecast method is unfiled. A term-blind or run-rate reading gives High LTV first (about 4.9 against 2.7 to 2.9). The judge calls this a competent-analyst error, supported by the 2023 to 2025 cohorts (882 accounts: hazard 0.1% in months 1 to 8, 1.0% in months 9 to 15, 2.1% from month 16). Risk: a reviewer may find the term-blind reading defensible.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / large file | 10+ / 3+ / 25,000+ rows | 13 / 4 (csv, parquet, pdf, xlsx) / history parquet 4,260,553 rows | yes |
| Distractors | 2+ in metadata.json, none file-labelled | 4 named (house price index, contact centre volumes, board risk appetite statement, rate card); no file name labels one; the judge found them relevant enough to weigh and unused by the solution | yes |
| Distractor does not answer a graded quantity | none does | none answers one (judge) | yes |
| Deliverables | 1 to 3, all in golden | 2 (paper PDF, workbook xlsx), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | per-book, per-period cuts with unit and rounding in the sentence (nearest ten, nearest hundred pounds) | yes |
| Prompt shape / rubric 25+ | identifiable, 25+ | shape "other" (book chosen, avoided against next best, plus caseload and loss asks); about 3 paper plus 18 workbook figures plus components; the rubric is portal-generated, so the count is estimated, not verified | yes (estimated) |
| Prompt form | one paragraph, question first, under 1,000 chars | 803 chars, one paragraph | yes |
| Not LLM-generated / goldens real work products | yes | the judge found no authoring disclosures; golden realism was not independently read here | yes (judge hygiene) |

## Gate G reconciliation
Thread: mechanism forecasting, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: stump_class analytical, a forecast with forbearance as a state; the note's ladder files the enumerated family on High LTV (4.5 against 2.9) and the standing family on FTB (8.0 to 11.9). Match. The thread did not name a declared distractor as the surface read: its easy route is the term-blind roll-rate chain, which is not a shipped artifact, and the four metadata distractors played no part. The thread's own chain gives FTB 8.7 against the note's 9.0, and both bin to 10. No finding. (The card has no mechanism or stumping_family fields to compare.)

## Gate H line
domain: pass, layers: pass, decisive_step: analytical. The design note's Three rules agree (domain test: an arrears-entry hazard with forbearance as a state; Layer 1: product-code dashes, re-sent rows, loan-part rows, relabelled books; Layer 2: seasoning of term-extended accounts; no decoy; not semantics; not rule application). The thread's reading of the decisive step is not "the field's standard method applied without judgment": it needed the extension event derived from remaining_term_months and the delayed hazard estimated from earlier cohorts.

## Stump power (Gate F)
Moderate to good. The easy route is a term-blind or payment-rise-only roll-rate or run-rate chain, which files High LTV first at about 4.5 to 4.9. Only a solver who derives the term-increase event, sees the delayed hazard in the 2023 to 2025 cohorts and carries it forward lands the call. Strong models read everything, so a miss is plausible but not certain. No scored reader was run (STOP block), so this is the judge's read only.

## Findings, ranked
1. No blocking finding.
2. Watch: the forecast method is unfiled, so the golden rests on a term-aware method being the competent one. The back-test and cohort hazard support it.
3. Minor: the three ambiguities above (margin reading, eight-month boundary, register dependency for open claims).
4. Cosmetic: the litigation file is named 2023-01 but starts in February 2022.

## Next action for the author
Proceed with the pre-ship checks. No fix is required. If the planned generator rebuild changes the prompt or the zip, run a second pass on the new zip, since this verdict is for sha256 5194480e429f78f193432468db474436e77512f2e90680f723281c92530d1976 only.
