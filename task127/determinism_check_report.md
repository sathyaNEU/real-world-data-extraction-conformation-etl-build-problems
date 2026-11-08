# determinism-check report, task127, 2026-11-08

## Verdict
DETERMINISTIC, with SOLUTION_WRONG (minor): Critical Component 2's control count "5 in 211" does not reproduce (judge gets 6 in 211, variant 4 in 212). No graded figure moves.
**Disposition:** FIX_NOW (solution text only; solver-facing files unchanged)
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no
Cut judged: target.zip md5 5cdd0b1c832b14d86795fcb72e3bc9bd. Thread: one sonnet/medium general-purpose thread, scratch /tmp/determinism-check-task127-1794096432/ (the main session spawned it on my brief; verdict.md there).

## Why
Own PD x LGD x EAD ranks Kinloch + Ridgeway first (NZ$3,055k). Eight Ruahine borrowers take 52 to 83 percent of 2026 receipts from Matai and one from Ridgeway; their default transmission (13 of 31 against about 2 percent where the payer kept trading) lifts Kinloch + Matai to NZ$3,352k to 3,364k, above Matai + Ridgeway (3,240k) and Kinloch + Ridgeway (3,098k). Call holds for any transmission rate above about 0.28 and for every estimator tried (0.39 to 0.42). Envelope enumeration confirms Kinloch + Matai first at NZ$5.8m of lines.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| CC1 dependants of Matai / Ridgeway | 8 / 1 | 8 / 1 (10 and 1 above 50 percent, 2 not in run); stable on 2025 receipts, any threshold 7 to 51 percent | yes |
| CC2 treated group | 13 of 31 | 13 of 31 | yes |
| CC2 control group | 5 of 211 | 6 of 211 (variant 4 of 212) | NO |
| Constant in step 4 | 0.3957 | 0.391 to 0.4005 | approx (rounds to same bins) |
| CC3 Matai package | NZ$1,750,000 (own 822,000) | 1,741k to 1,764k (own 821,940) | yes after rounding |
| Ask 2 write-offs | Matai 1,750 / Kinloch 1,600 / Ridgeway 1,500 / Marlowe 1,050 / Selwyn 700 / Brightwater 450 / Coastline 350 / Northgate 250 (k) | own figures 1,611 / 1,444 etc.; Ridgeway about 1,487k | yes |
| Total | NZ$3,350,000 | 3,352k to 3,364k | yes |
| Ask 3 security values | 6,321 / 4,914 / 794 / 7,333 / 1,431 / 3,532 / 7,549 / 2,877 | identical | yes |
| Ask 4 commitments | 5,250 / 10,022 / 6,650 / 7,800 / 4,350 / 3,200 / 2,743 / 1,750 | identical | yes |
| Ask 5 sector shares | 6.4 / 8.2 / 6.0 / 4.2 / 8.5 / 9.4 / 6.5 | identical | yes |

## Competing answers that survived
1. Ignore dependants: Kinloch + Ridgeway, NZ$3,050,000. The easy route; the 13 of 31 evidence makes ignoring it an analytical omission. The prompt's "through the borrowers it takes on" and terms of reference 3.5 license the knock-on but do not state it. Residual determinism risk, closed by the data and the terms, not by a filed rule.
2. Gross 13 of 31 with no baseline: Matai NZ$1,800,000 and total NZ$3,400,000; call unchanged, two graded figures move. "Keep off the book" implies the incremental effect, so the baseline-subtracted estimand is the forced one (per-dependant "13/31 minus own PD" gives NZ$1,749,629, same as golden).
3. Security at 2026Q3 instead of Q4 (Matai 6,220k): closed by "31 December 2026" and "latest published value". Note the Q4 release is dated 2027-01-21, one day after the 20 January watch list.
4. "Performing" read as run stage below 3 gives every sector share 0.1 to 0.2 lower: closed by the default definition in the validation PDF (7 stage-2 borrowers are in default in the register).
5. Recalibrating PDs from the validation PDF: closed by terms of reference 3.4.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 | yes |
| Formats | 3 or more | csv, xlsx, pdf | yes |
| Large file | 25,000 rows or more | business_account_transactions 281,664 rows | yes |
| Distractors | 2 or more in metadata.json, none labelled by file name | sector_risk_appetite_2027.pdf, regional_economic_indicators_2019-2026.csv; names carry no label | yes |
| Distractors unused yet weighable, none answers a graded quantity | required | judge found neither carries the call; neither named as the surface read | yes (judge-level) |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, docx), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | required | asks 2 to 5 are 8-borrower or 7-sector tables, units and rounding in prompt | yes |
| Prompt shape, rubric 25 or more criteria | required | shape identifiable (pick under an envelope with per-borrower and per-sector grids); the rubric is generated and I did not count it | not verified here |
| No LLM tells, goldens read as work products | required | judge found none; docx realism not separately read | yes (judge-level) |

## Gate G reconciliation
Thread: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: Strategy causal_design (spillover), counterfactual model of the package (obligors treated as independent), stump_class analytical. These agree in substance; no mismatch. The declared distractors are not the surface read that carries the task, so they are not too load-bearing. Easy route (own expected loss) gives Kinloch + Ridgeway; the thread notes it is wrong on clean data, so the stump survives deleting every wrong number. Minor: the design note's stump sentence cites the default path as NZ$3.00 million against NZ$3,050,000 in the submission and the thread; reconcile the wording.

## Gate H
domain: pass, layers: pass, decisive_step: analytical. Layer 1 is the 2023 account renumbering, the register keyed three ways, valuer-reference dates and former company names; Layer 2 is estimating default carry-over from payer to dependants against a no-default comparison, then package selection under the envelope. The design note's Three rules lines (No decoy, Not semantics, Not rule application) concur. The decisive step is not a textbook-method landing: the dependence has no column and the rate must be estimated from the register, so the main thread need not discount it as a landable standard method.

## Stump power (Gate F)
Good. A strong model that reads every file but ranks on own PD x LGD x EAD files Kinloch + Ridgeway at NZ$3,050,000. The deciding link is reachable only via the crosswalk, loan-account resolution and a treated/control comparison. The design note's own family check shows Matai's figure spreading NZ$21,161 inside one NZ$50,000 bin across 48 method variants. The thread does flag one risk: it did not find the dependants a stated requirement, only licensed by the prompt wording and terms 3.5.

## Findings, ranked
1. Critical Component 2 and Solution step 4: "5 in 211 borrower-years" (and constant 0.3957, also in the design note's golden row "13 of 31 less 5 of 211, 0.396") does not reproduce; judge gets 6 in 211 (0.391) on the natural reading, 4 in 212 on a variant. All graded figures still round identically (Matai NZ$1,750,000, total NZ$3,350,000), so this is a SOLUTION_WRONG on the filed solution only. Fix: state the control definition (borrower-years in 2022 to 2025, payer kept trading, borrower not already in default) and make the count and constant match it, or restate as 6 in 211 and 0.391. Note the restated constant must still round every graded figure to the same bin (Kinloch + Matai tips to NZ$3,400,000 only above c = 0.4005).
2. Residual fork (ask 2 and the call): the baseline-subtracted estimand is not filed; the gross 13/31 reading moves Matai to NZ$1,800,000 and the total to NZ$3,400,000. The judge accepts "keep off the book" as forcing incremental effect. Optionally state the estimand in the solution text (the WHAT, not the HOW).
3. Residual fork (ask 3): 2026Q3 vs Q4 index; closed by the reporting date but the Q4 release (2027-01-21) postdates the watch list by a day.
4. Minor wording: design note stump sentence says NZ$3.00 million for the default path against NZ$3,050,000 shipped.

## Next action for the author
Edit submission.md Critical Component 2 and Solution step 4 (and the design note's golden row) so the control count, definition and constant agree with the reproducible figure, leaving the prompt, target/ and goldens untouched; then re-judge once under /build stage 4's FIX_NOW rule.
