# determinism-check report, task446, 2026-10-21

## Verdict
DETERMINISTIC (main call 78 groups; every golden figure recomputed from target.zip, sha256 72419f5f...2973a3)
**Disposition:** FIX_NOW (optional, small): pin the cohort window for the one-decimal band figures. The call needs no change.
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Read literally, CRM-07 pins the book (4.1), outcome (4.2), flag (3.2), membership (2.2) and exposure (1.3, 6.1, 6.2): 913 groups, 165 flagged, 127 flagged on a customer. The closed-cohort counts (120/240, 11/176, 50/3092) give 77.96 arrivals, 78 under every kind-of-flag rate construction tried (77.9 to 78.2). The pooled flagged rate (131/416) gives 64.1: the analytical trap, not a fork, because the filed back-test criterion (5.2) ranks the split first (max miss 3.9% against 14.4%).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Book at 30 Sep 2026 (group register, watch_list_history) | 913 | 913 | yes |
| Flagged / flagged on a customer (ews_entity_signals, obligor master, GLEIF) | 165 / 127 | 165 / 127 | yes |
| Cohort rates 2022-25 | 50.0% / 6.25% / 1.62% | 120/240, 11/176, 50/3092 | yes |
| Back-test max miss, split / pooled | 3.9% / 14.4% | 3.9% / 14.4% | yes |
| Expected arrivals | 78.0 | 77.96 | yes |
| Bands (groups, £m, flagged, arrivals, £m arriving) | 201/499.9/34/16.2/38.5; 304/3112.0/54/25.8/257.1; 248/6936.6/46/21.9/596.8; 120/8402.7/20/9.0/576.3; 40/6712.2/11/5.1/826.8 | identical | yes |
| Total | 913/25663.4/165/78.0/2295.5 | identical | yes |

## Competing answers that survived
- Soft fork in the asks only: a two-way split (customer-flagged against the rest) gives a call of 78.2 (still 78) but bands 16.3/25.9/22.0 and £38.6m/£258.2m/£597.8m, which differ from the golden at one decimal. Its back-test is worse (max 4.8%, mean 3.9% against 2.5%), so 5.2 ranks the golden first, but the margin is not wide. Closing rule meant: 4.3 and 1.2 (design note SF3). The 2025-only window gives band 4 as 9.1 against 9.0 (design note records this window as same call, not band-checked in the note's text).
- "Customer" read as ACTIVE status only gives 73.8 (74): a wrong reading, since customer_since <= date is the stated opening date. Not a stump; no change required.
- UTC cut-off instead of UK time moves 10 groups between bands; closed by the literal UK time in 1.3 and 6.1.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 17 | yes |
| Formats | 3+ | 6 (md, xlsx, csv, docx, pdf, txt) | yes |
| Large file | 25,000+ rows | 125,975 (ews_entity_signals) | yes |
| Distractors | 2+ in metadata.json, none named by file | internal_rating_master_scale_2026.xlsx, group_economics_uk_outlook_oct2026.xlsx; names unlabelled | yes |
| Distractor quality | unused, relevant, ruled out by a shipped fact | ratings dated 30 Sep 2026 only (would leak the future into past cohorts); judge found neither reproduces a graded figure | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, svg), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 5 bands x 5 measures plus total, whole number / one decimal / £m one decimal | yes |
| Prompt shape and rubric | shape identified, 25+ criteria | shape 05 (allocation to a fixed total); about 35 gradable cells and chart items by count; not measured by a generated rubric here | yes (by count) |
| LLM-generated reading | none | judge found none; mild note only: all LEIs share the 213800 prefix | yes |

## Gate G reconciliation
Judge: mechanism forecasting, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: Layer 2 is estimand_identification (composition shift), decisive step is forecasting each flagged group at the conversion of its own kind of flag instead of the pooled rate; no decoy declared as carrying the task. The judge names neither declared distractor as the surface read. Match: no mismatch found. Gate G: analytical_non_defect, passes. (The card was not separately opened; the reconciliation used the design note's Three rules and fork table.)

## Gate H
domain: pass, layers: pass (Layer 1 GLEIF dates, LEI against Companies House keys, UK time against UTC, EUR/USD facilities; Layer 2 hit rates by the member that raised the flag, validated on closed cohorts), decisive_step: analytical. This matches the note's Three rules. The easy route (pooled flagged rate) files 64.

## Stump power (Gate F)
Moderate to good. A strong model that reads CRM-07 computes the pooled flagged rate and files about 64, missing that a flag raised only on a non-lent-to member converts at 6.25% against 50.0%. A solver who tests the split against the closed cohorts finds it. The two-way variant still gets the headline, so the call is partly forgiving; the asks (facilities counted in every group with a member on them, end-of-day BST limit versions, GLEIF-placed customers, one-decimal arrivals) carry the rest. The decisive step is a method choice the filed back-test criterion selects, not a pure textbook-route call; the main thread should weigh it with the blind readers' result.

## Findings, ranked
1. Soft fork on the band figures: kind-of-flag split versus two-way split (and a single-cohort window) moves band arrivals by 0.1 at one decimal while the call stays 78. Closed by 4.3 and 1.2 only by inference; a window clause in the prompt would pin it.
2. "Customer" ACTIVE-status reading gives 74: semantic edge, no action required.
3. Cosmetic: shared 213800 LEI prefix.

## Next action for the author
Optional: add "from the 2022 to 2025 cohorts taken together" to prompt.txt (or confirm in checks.py that the two-way split and 2025-only window cannot move a one-decimal band figure by filing the window in a shipped rule), then ship. Rule: file the WHAT (window), not the HOW (split), so the decisive step is not turned into rule application.
