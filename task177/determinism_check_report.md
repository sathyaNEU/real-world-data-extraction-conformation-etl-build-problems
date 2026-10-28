# determinism-check report, task177, 2026-10-28

## Verdict
NOT_DETERMINISTIC

**Disposition:** FIX_NOW — pin a `successor_code`/`status_date` for BNK0115 in `cic_member_directory_202612.csv` (the same mechanism already used for MFI0447/SFB0029) so the Gandhamardan institution-merge is forced by a file field rather than inferred from a naming convention. No golden figure, no part of the main forecast, and no graded value changes; no model rerun required.

**Stumping type:** mechanism: forecasting (also consistent with method_or_model_selection), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The judge thread independently rebuilt the 1,554,898-row meeting ledger from the two CollectPro exports, the Kshetra parquet and the migration map, and reproduced CRITICAL_COMPONENTS exactly (9,082 / 3,372 / 412 / 14 loans by group-carried state; 97 groups holding 426 loans) and the weighted forecast (278.1 → 300). The main recommendation is forced: no competing route survives the shipped ledger's own contrast between groups carrying one versus two members at once.

Supplementary ask 2 (the 14-branch guardrails table) fails Gate C/E. `cic_member_directory_202612.csv` gives an explicit `successor_code`/CONVERTED mechanism linking MFI0447 to SFB0029 (Salandi), but no equivalent field links BNK0102 ("Gandhamardan Gramya Bank") to BNK0115 ("Gandhamardan Gramya Bank - BC Portfolio") — both rows are plain ACTIVE with blank `successor_code`. The golden's branch table (2,528 borrowers / INR 821.3 lakh) only reproduces if a solver merges Gandhamardan's two member codes by reading the institution-name string pattern; a solver who merges only the field-flagged Salandi pair and treats Gandhamardan's two codes as distinct lenders (equally defensible, since the directory schema supplies a dedicated closure mechanism for exactly this and simply does not use it here) reaches 2,652 borrowers / INR 860.1 lakh, with every one of the 14 branch cells changed. This affects supplementary ask 2, which per the judge's global rule is held to the same determinism bar as the main call.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Ledger row count | 1,554,898 | 1,554,898 | yes |
| Pool loans by carried state (none/one/two/3+) | 9,082/3,372/412/14 | 9,082/3,372/412/14 | yes |
| Groups carrying 2+ / loans | 97 / 426 | 97 / 426 | yes |
| Weighted forecast | 278.1 → 300 | 9,082×0.0034 + 3,372×0.0311 + 412×0.3115 + 14×1.00 = 278.1 | yes |
| Guardrails total (merged reading) | 2,528 borrowers / INR 821.3 lakh | 2,528 / 821.3, matches all 14 branch cells | yes, but not uniquely forced (see below) |
| Guardrails total (unmerged Gandhamardan reading) | — | 2,652 borrowers / INR 860.1 lakh | a defensible second answer |

## Competing answers that survived
- **Ask 2 (guardrails table), Gandhamardan institution merge.** Golden reading: merge BNK0102 and BNK0115 by institution-name pattern → 2,528 / 821.3 lakh, every branch cell as filed. Alternative reading: treat them as two separate lenders (licensed by the fact that the directory's own schema has a dedicated `successor_code` field for exactly this kind of merge, used for Salandi, and left blank for Gandhamardan) → 2,652 / 860.1 lakh, every one of the 14 branch cells shifts. The shipped file does not close this fork with a machine-readable rule; it is closed only by recognizing a naming convention ("- BC Portfolio" suffix), which is a defensible-but-not-forced inference. This is the one open fork found; no other fork (population, as-of dating, SFB0014 dedup, holding period, rounding, etc.) survived — all other design-note semantic-fork-table entries print "same call" or are closed by a quoted file sentence, confirmed by the judge's own re-derivation.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | ≥10 | 16 | yes |
| Format mix | ≥3 formats | csv, parquet, pdf, xlsx (4) | yes |
| Large file | ≥25,000 rows or large DB | kshetra parquet 776,608 rows; collectpro FY2023-24 333,018; FY2024-25 445,272; bureau review 54,991 | yes |
| Distractors named, unused | ≥2 named in metadata.json, none in a file name | 3 named (pvm_credit_life_claims_2023-2026.csv, pvm_field_officer_postings_2026.csv, pvm_portfolio_report_FY2024-25_to_FY2026-27.xlsx), each with why_relevant/why_unused/ruled_out_by; no file name labels a distractor | yes |
| Deliverables | 1–3, all in golden | 2 (pool_90dpd_forecast.xlsx, pool_purchase_note.docx), both present under golden/ | yes |
| Asks multi-dimensional, unit/rounding stated | required | ask 1: single count, nearest 100; ask 2: 14 branches × 2 figures, INR lakh to one decimal — both stated in prompt.txt's last sentence | yes |
| Prompt shape / rubric ≥25 criteria | required | prompt shape identifiable (forecast + 28-cell branch table + chart note); ceiling.py in generator/ encodes rubric weight split 38/7/55 consistent with spec; an actual rubric criteria count was not independently recomputable from the task folder alone | not independently verified (no blocking concern found) |
| Not LLM-generated; goldens read as real work product | required | hygiene PASS per judge thread: mixed date conventions (DD/MM/YYYY CollectPro vs ISO Kshetra), a real institution-naming irregularity, a genuine duplicate-account artifact (SFB0014), no provenance/benchmark disclosure found | yes |

## Gate G reconciliation
Judge thread: mechanism `forecasting` (also consistent with `method_or_model_selection`), stumping_family `analytical_non_defect`, surface_read_dependency `no`, sole_data_defect `no`.

Design note / card: `## Three rules` names the decisive step as conditioning each loan's six-month default on "how many members its group was carrying at its last meeting," classified `analytical`; the card's `gate_g` field is `binding_constraint` (the per-meeting group capacity — one short member carried, not two). The card's `stump_class` is `analytical`, with `analyst_test` and `domain_test` both filed.

These are not in conflict: `binding_constraint` (the card's own fingerprint-taxonomy label for the per-meeting capacity limit) and the judge's `forecasting`/`method_or_model_selection` read the same mechanism from two adjacent angles — a capacity limit that forces the correct conditioning unit for a forward projection — and both are FINE-numbers, non-surface-read-rejection shapes. No distractor was named as the surface read carrying the task (the judge found the pool tape's own `dpd_at_cutoff` column, not a distractor file, as the "reported-looks-fine" surface a naive solver under-reads). No reconciliation mismatch found between the judge's Gate G/H calls and the design note's own ladder and three-rules block; both independently land on the same decisive step (group-conditional default rate, not member-level or binary-flag reads).

## Stump power (Gate F)
The judge's assessment stands: every pool loan shows `dpd_at_cutoff = 0` (all current at the cut-off), so a model reading only the pool tape's own trailing status sees no risk signal and must reach into history. The two natural wrong routes are well-grounded and specific: (a) scoring each loan off the member's own last-meeting payment (treats "carried" as a stable safe/unsafe flag, not a point-in-time distress signal) → ~100; (b) collapsing group support into a binary "did the group carry anyone" flag (prices a group carrying two the same as one carrying one, losing the escalating 0.34/3.11/31.15/100 per cent gradient) → ~200. Both are provable analytical errors, not coin-flips, and the design note's own ladder (rungs 0–3, 94.7/119.5/183.1/278.1) corroborates the separation. This is a textbook forecasting/method-selection route (`stumping` 1.3: the field's own static-pool roll-rate method, applied to the right conditioning unit) and is a landable call, not evidence of staleness.

## Findings, ranked
1. **(Blocking determinism, FIX_NOW) Ask 2's Gandhamardan merge is not file-forced.** `cic_member_directory_202612.csv` leaves BNK0102/BNK0115 unlinked by any machine-readable field, unlike the Salandi pair. A diligent solver who declines to infer the merge from the institution-name suffix reaches a different, equally defensible 14-branch table (2,652 / 860.1 lakh vs. the golden's 2,528 / 821.3 lakh). This is a Gate C/E failure on a supplementary answer, disqualifying under the judge's global rule even though the main recommendation is untouched.
2. **(Non-blocking) Rubric criteria count not independently re-derivable from the task folder.** `generator/ceiling.py` encodes the 38/7/55 weight split the spec requires, but no shipped rubric file lets this reviewer count criteria directly. Not treated as a finding against the task; flagged only for completeness.

## Next action for the author
Add an explicit `successor_code` (pointing BNK0115 to BNK0102) and a `status_date` to `cic_member_directory_202612.csv`, mirroring the Salandi row's mechanism, so the Gandhamardan institution-merge for supplementary ask 2 is pinned by the file instead of left to a naming-convention inference. This is an in-house `generator/bureau.py` (or wherever the directory CSV is built) edit; rebuild, re-verify the two byte-identical builds, and reship — no change to the main forecast, the ladder, or any other golden figure, and no model rerun is required.
