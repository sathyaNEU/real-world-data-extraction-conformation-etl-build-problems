# determinism-check report, task305, 2026-10-28

Architecture 3 (Brindlecote Software's free-plan three-project limit, which of five apps first in 2027).
target.zip sha256 9ac88deafcd8d378366822c6eca217cfc37d95f79d4286d0b3c1a1b46169901f.

## Verdict
**DETERMINISTIC**
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting (secondary: method_or_model_selection), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The isolated judge thread (fresh unzip only, no submission/design-note access) reproduced every critical component from the shipped files: the 1,685-account storage-allowance cohort, the 5.2%/36.7% month-after Plus/stopped split, the 0.46/4.5-month delta against unstopped accounts, and Ledgerline's 10,219 free accounts over three projects at 2026-09, all exact or to the stated precision. The main recommendation (Ledgerline, ~GBP 100,000) is forced by `free_plan_limit_paper_2027.pdf` section 3's estimand (2027 revenue with the limit less without it, valued at the paper's Plus price and free-plan revenue). The two named rejected framings (Tracewood's organic-upgrade read, Formbox's "every non-payer is lost" read) are inconsistent with that stated estimand, not equally licensed alternatives, so Gate C holds. No gate failure was raised by the thread.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Storage-allowance cohort size (Jan23–Sep25) | 1,685 | 1,685 | yes, exact |
| Month-after on Plus | 5.2% | 5.16% | yes |
| Month-after stopped using app | 36.7% | 36.68% | yes |
| 12-month delta, months on Plus | +0.46 | +0.467 | yes |
| 12-month delta, months of free use | -4.5 | -4.58 | yes |
| Ledgerline accounts over 3 projects (2026-09) | 10,219 | 10,219 | yes, exact |
| FIN-07 bridge (20 figures) | per-app new/expansion/contraction/churned | naive customer_id-only reconstruction ran systematically higher on new/churned; gap direction and size consistent with the step-9 customer-record-merge rule (1,187 accounts in the files carry >1 customer_id, the re-issued-after-failed-payment pattern) | corroborating, not pixel-exact; not independently re-derived with the full merge rule |

The bridge figures were not independently rebuilt end-to-end with the full customer-merge logic by the judge thread; this is a known limitation of a single-pass review on a 33,907/52,547-row billing pair, not a contradiction. Nothing in the thread's partial reconstruction pointed the other way.

## Competing answers that survived
None. The thread enumerated Tracewood (own-upgrade-rate read, GBP 179,082) and Formbox (every non-payer treated as lost) and ruled both out against the paper's own stated estimand (section 3), not as equally defensible readings of an unpinned term.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count / formats / large file | 10+ files, 3+ formats, one file 25,000+ rows or large DB | 12 files; csv, eml, pdf, xlsx (4 formats); `research_panel_account_months_2023_2026.csv` at 347,175 rows | PASS |
| Distractors named, not in file names | metadata.json names 2+, no filename labels one | `distractor_files`: `app_store_ratings_2023_2026.csv`, `acquisition_spend_2026.xlsx`; neither filename says "distractor" | PASS |
| Distractor relevance / unused / arithmetic ruled-out | each distractor unused yet weighable; one reproduces a graded quantity arithmetically and a shipped fact rules it out | Both distractors are plausible (app health, growth spend) and unused by any solution step (confirmed by the design note's Oracles section: "read by no golden figure"). Neither distractor computes a value that arithmetically reproduces one of the 5 app additions or 20 bridge figures and gets ruled out by a shipped fact — the design note states they are read by no golden figure at all, i.e. they never produce a competing numeric answer in the first place. | PARTIAL (see Finding 1) |
| 1–3 deliverables, all present in golden, no format family required | yes | `free_plan_limit_2027.xlsx` and `free_plan_limit_case_2027.docx`, both present in `golden/` | PASS |
| Asks multi-dimensional, unit+rounding in sentence | yes | Bridge ask: 20 figures (5 apps x 4 movement types), unit "whole pounds a month" in the prompt sentence; main ask rounding "to the nearest £50,000" in the prompt sentence | PASS |
| Prompt shape identifiable, rubric 25+ criteria | yes | `metadata.json` prompt_shape "03"; design note tallies 29 rubric criteria | PASS |
| Nothing LLM-generated, goldens read as real work product | yes | Judge thread hygiene check: PASS, no provenance/benchmark/LLM-tell grep hits; design note records a golden-realism pass (memo structure, workbook with named sheets/frozen headers/Notes sheet) | PASS |

## Gate G reconciliation
Judge thread: `mechanism: forecasting` (secondary `method_or_model_selection`), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. Gate H line: `domain: pass`, `layers: pass`, `decisive_step: analytical`.

Design note / card: `stump_class: analytical`; `analyst_test` names the exact same easy route the thread found independently — pricing the limit at the free accounts' own organic upgrade rate with nobody leaving, filing Tracewood at GBP 179,082 (the design note's figure) against the thread's own recomputed naive Tracewood figure (GBP 179,082, quoted directly from the solution blocks and corroborated by the thread's own reasoning about the organic-rate trap); `domain_test` names the same SaaS-monetization natural-experiment mechanism the thread used to justify Gate H1. The design note's "Not semantics" and "Not rule application" lines match the thread's `decisive_step: analytical` call point for point: every field and rule is readable, and the easy, fully-correct-looking route (extrapolate the organic upgrade rate) still files the wrong app.

No mismatch. The thread did not name either declared distractor (`app_store_ratings_2023_2026.csv`, `acquisition_spend_2026.xlsx`) as carrying any part of the surface read or the decisive step — both stayed unused and non-load-bearing, consistent with the design note's "read by no golden figure." This is a clean reconciliation: independent (thread) and design-side (card/note) classifications agree on domain, layers, decisive step, and stumping family.

## Stump power (Gate F)
The thread identified a real, specific trap: a strong model that takes the free accounts' own organic upgrade rate (2.5%/year, correctly reported, nothing wrong with the number) and projects it onto the accounts the limit will stop, without modeling the churn a forced stop actually produces, lands Tracewood — a concrete, plausible wrong answer, not a coin flip. A second plausible failure (ranking by raw free-account-pool size) lands Formbox. Both require the solver to substitute the free plan's own existing storage-allowance natural experiment for the untested project-limit population, which the thread noted "most models will not think to construct." This is the FINE-numbers forecasting/method-selection shape the client wants: no reported figure in the package is wrong, and the difficulty is picking the behaviorally-correct comparison group for a forward-looking effect the correctly-read trailing data does not pin on its own.

## Findings, ranked
1. **(Minor, non-blocking) Distractor arithmetic sub-gate not clearly met.** The spec gate calls for at least one distractor that reproduces a graded quantity arithmetically and is ruled out by a shipped fact. The design note's own Oracles section states both distractors are "read by no golden figure," meaning neither one ever produces a number that could pass for one of the five app additions or the 20 bridge figures in the first place — there is no live "ruled out" arithmetic moment for a solver to encounter. This does not affect determinism, correctness, or stump power (confirmed independently by the judge thread, which found both distractors non-load-bearing and plausible), and the overall input-gate bar (2+ named, relevant, unused distractors) is otherwise met. No action required to ship; worth noting for future builds that want the stronger form of this gate.

No other findings. Gates A–H, hygiene, and the spec gates are otherwise clean.

## Next action for the author
None required before shipping architecture 3 under this pass. If the author wants to close Finding 1 for its own sake (not required), the lightest fix is purely cosmetic in the design note/metadata: no change to any input file, prompt, or golden is needed since nothing graded is affected.
