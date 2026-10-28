# determinism-check report, task177, 2026-10-28 (pass 2)

## Verdict
NOT_DETERMINISTIC

**Disposition:** SEND_BACK: the fork lives in a shipped input file (`tb_cpn_mf07_microfinance_guardrails.pdf`, section 3), not in a solution block, so closing it changes what solvers read and invalidates prior model runs; a rerun is required after the fix.

**Stumping type:** mechanism: forecasting (also method_or_model_selection), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The pass-1 FIX_NOW (adding `parent_code` to `cic_member_directory_202612.csv` so BNK0115 reports for BNK0102 by a machine-readable field, mirroring the Salandi `successor_code` mechanism) did patch the directory, and the directory now links both pairs by field, not by name. But the judge thread found the fix did not reach far enough: `tb_cpn_mf07_microfinance_guardrails.pdf` section 3, the one shipped document that states the counting rule, only ever describes merging by succession, "loans reported under the member code of an institution it succeeded, count as that institution's", and never states that a `parent_code` / business-correspondent relationship makes two codes "one institution" for counting. The directory's own `institution` column, moreover, gives BNK0102 and BNK0115 two different institution-name strings ("Gandhamardan Gramya Bank" vs "...- BC Portfolio"), so a rigorous solver who reads the policy literally and merges only the succession case it names reaches 2,652 borrowers / INR 860.0 lakh instead of the committed 2,528 / INR 821.3 lakh, with every one of the 14 branch cells shifted. This is the same fork as pass 1, relocated from the directory (which now has a merge field) to the governing policy text (which never authorizes using it). It affects supplementary ask 2, held to the same determinism bar as the main call by the judge's global rule.

The main recommendation is untouched and well-forced: the judge thread independently rebuilt the group-state bucket counts (9,082/3,372/412/14) from the Kshetra parquet and pool tape and reproduced the forecast exactly (278.1 → 300), and the two named naive alternatives (100, 200) are genuine analytical traps, not semantic ones.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Pool loans by carried state (none/one/two/3+) | 9,082/3,372/412/14 | 9,082/3,372/412/14 | yes |
| Weighted forecast | 278.1 → 300 | reproduced from parquet + pool tape | yes |
| Guardrails total (parent+successor merge, as filed) | 2,528 / INR 821.3 lakh | 2,528 / 821.3, all 14 branch cells | yes |
| Guardrails total (successor-only reading) | none | 2,652 / INR 860.0 lakh, all 14 branch cells shift | a defensible second answer |
| SFB0014 duplicate-account dedup | 2,122 pairs, later report kept | 2,122 pairs confirmed, each with one leg dated exactly 2026-03-13 | yes, file-forced and unambiguous |

I independently re-read `tb_cpn_mf07_microfinance_guardrails.pdf` with `pdftotext -layout` (not a flattened text dump; the file has no tables to drop) and confirmed section 3's operative sentence verbatim: "A lending institution is counted once: loans an institution reports under more than one member code, including loans reported under the member code of an institution it succeeded, count as that institution's." This sentence is genuinely dual-readable, as a general "any institution with multiple member codes merges" rule with succession given only as an included example (which would license the Gandhamardan merge), or as a rule whose only stated merge mechanism is succession (which would not). Both readings are grammatically available from the shipped text alone, and the directory's `institution` column actively supports the narrower reading by giving BNK0102 and BNK0115 different institution-name strings. That dual readability is itself the Gate C failure: a decisive term ("an institution," for counting purposes) is not pinned by the shipped files to one meaning.

## Competing answers that survived
- **Ask 2 (guardrails table), Gandhamardan parent-code merge.** Golden reading: `parent_code` is read as establishing common institutional identity, same as `successor_code` → 2,528 / 821.3 lakh. Alternative reading: CPN-MF-07 section 3 only names succession as a merge mechanism, and the directory's own `institution` field treats BNK0102/BNK0115 as different reporting entities, so `parent_code` is a directory cross-reference, not a counting-rule trigger → 2,652 / 860.0 lakh, every branch cell shifts by 5 to 15 borrowers and INR 1 to 5 lakh. The shipped policy document does not close this fork with an explicit sentence naming `parent_code` or a parent/BC-portfolio relationship; it is closed only by extending "more than one member code" to cover a case the policy's one worked example does not. No other fork (population, as-of dating, SFB0014 dedup, holding period, rounding, SF1 to SF13 in the design note's own fork table) survived; the judge independently re-derived each and found the other readings closing to "same call."

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | ≥10 | 16 | yes |
| Format mix | ≥3 formats | csv, parquet, pdf, xlsx (4) | yes |
| Large file | ≥25,000 rows or large DB | kshetra parquet 776,608 rows; collectpro FY2023-24 333,018; FY2024-25 445,272; bureau review 54,991 | yes |
| Distractors named, unused | ≥2 named in metadata.json, none in a file name | 3 named (pvm_credit_life_claims_2023-2026.csv, pvm_field_officer_postings_2026.csv, pvm_portfolio_report_FY2024-25_to_FY2026-27.xlsx), each with why_relevant/why_unused/ruled_out_by; no file name labels a distractor | yes |
| Deliverables | 1 to 3, all in golden | 2 (pool_90dpd_forecast.xlsx, pool_purchase_note.docx), both present under golden/ | yes |
| Asks multi-dimensional, unit/rounding stated | required | ask 1: single count, nearest 100; ask 2: 14 branches × 2 figures, INR lakh to one decimal, both stated in prompt.txt's last sentence | yes |
| Prompt shape / rubric ≥25 criteria | required | prompt shape identifiable (forecast + 14-branch table + one chart); design note's ask sheet alone carries 28 graded figures for ask A plus the main call and critical components; generator/ceiling.py encodes the 38/7/55 weight split | yes (not independently recounted from a shipped rubric file, but comfortably over 25 on the design note's own tally) |
| Not LLM-generated; goldens read as real work product | required | hygiene PASS per judge thread: mixed date conventions (DD/MM/YYYY CollectPro vs ISO Kshetra), a genuine bureau-conversion/BC-portfolio naming irregularity, a real duplicate-account artifact (SFB0014/renumbering), no provenance/benchmark disclosure found | yes |

## Gate G reconciliation
Judge thread (pass 2): mechanism `forecasting` (also `method_or_model_selection`), stumping_family `analytical_non_defect`, surface_read_dependency `no`, sole_data_defect `no`.

Design note / card: `## Three rules` names the decisive step as conditioning each loan's six-month default on "how many members its group was carrying at its last meeting," classified `analytical`; the card's `gate_g` field is `binding_constraint`, with `stump_class: analytical`, `analyst_test` and `domain_test` both filed. The design note's own pre-ship check reaffirms this on the built pack ("the decisive step is still analytical... not semantics, not rule application, nothing planted").

No mismatch on the main call: this reconciliation is unchanged from pass 1. The judge's `forecasting`/`method_or_model_selection` and the card's `binding_constraint` read the same mechanism (a group-level capacity limit forcing the correct conditioning unit for a forward projection) from two adjacent angles, both FINE-numbers, non-surface-read-rejection shapes. No distractor was named as the surface read carrying the task.

The new finding (the guardrails merge fork) sits entirely inside supplementary ask 2 and does not touch Gate G or Gate H for the main call: it is a Gate C (`competing_defensible_answer`) failure on a supplementary answer, not a stumping-type or domain-use problem. The design note's own ask-sheet section for Ask A already names the exact device ("Salandi's conversion... and Gandhamardan's correspondent portfolio... counted as separate lenders" as a listed mirror device, stops +4 to +15), the author's own paper argument anticipated this exact wrong reading as a mirror device to be ruled out, but the pass-1 fix ruled it out only in the data (the directory field), not in the one document whose text a literal reader is bound to.

## Stump power (Gate F)
Unchanged from pass 1 and not implicated by the new finding: the main call's two named naive alternatives (member-level payment status → 100; "group carried anyone" flag → 200) are the kind of trap a strong model plausibly falls for, both requiring recognition that risk is carried at the group's meeting-level state, not the individual, and that "carrying two" is not equivalent in severity to "carrying one." Textbook forecasting/method-selection route (`stumping` 1.3), a landable call.

## Findings, ranked
1. **(Blocking determinism, SEND_BACK) Ask 2's Gandhamardan merge is still not file-forced, the fork moved, not closed.** The pass-1 fix added `parent_code` to the directory CSV, which was the correct repair for the directory, but `tb_cpn_mf07_microfinance_guardrails.pdf` section 3 was never updated to say a `parent_code` relationship (as opposed to only a `successor_code` one) makes two bureau member codes "one lending institution" for guardrail counting. The directory's own `institution`-name column still gives BNK0102 and BNK0115 different strings, so a solver who reads the policy's one worked example literally (succession only) and declines to extend it to a parent/BC-portfolio relationship reaches a different, equally defensible 14-branch table (2,652 / 860.0 lakh vs. the golden's 2,528 / 821.3 lakh). Because the fix is to a shipped document's operative text, it changes what solvers see and requires a rerun (SEND_BACK, not FIX_NOW), even though no model-facing file outside the one PDF needs to change and the main forecast, the ledger, and every other golden figure stay untouched.

## Next action for the author
Rewrite `tb_cpn_mf07_microfinance_guardrails.pdf` section 3's counting sentence so it states, in one clause, that a lending institution is counted once across every member code it reports under, for whatever reason the directory links them (succession, or a parent/correspondent/BC-portfolio relationship), rather than naming only the succession case as a worked example. This pins the supplementary ask 2 answer to a single reading without changing the directory, the ledger, the pool tape, or the main forecast. Because this is a shipped input document's text, treat it as a SEND_BACK repair (regenerate the PDF in `generator/`, rebuild, re-verify the two byte-identical builds, and re-run the one licensed re-judge) rather than an in-house solution edit; no other golden figure, deliverable, or the main recommendation needs to change.
