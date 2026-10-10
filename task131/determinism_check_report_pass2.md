# determinism-check report, task131, 2026-10-10 (pass 2, NO VERDICT)

## Verdict
NONE. The judge thread was not spawned, so this pass produced no verdict.
**Disposition:** none. This pass does not count as the post-FIX_NOW re-judge.
**Stumping type:** not classified (no judge thread ran).

## Why
The orchestrator ran inside a session that did not give it the `Agent` tool, so it could not spawn the one isolated `general-purpose` judge thread the contract requires. The orchestrator did not judge the build itself and did not start a substitute thread by another route (for example a CLI subprocess). Either would have replaced the reviewer's standard, applied in isolation, with the orchestrator's own reading, and spent the one re-judge on a method the pipeline does not recognise.

How far the pass got:
1. Inputs verified: `prompt.md`, `target.zip` (14 files), `submission.md`, `metadata.json`, and both golden deliverables are present.
2. Blocks extracted from `submission.md`: Final Recommendation, three Critical Components, six Solution Steps, and Deliverable Answers for `programme_offer_2027.docx` (asks 1 to 4) and `offer_grid_2027.png` (asks 1 to 2).
3. Fresh unzip at `/tmp/determinism-check-task131-20261010T214335/target/`.
4. `guidelines/determinism_judge_system_prompt.md` read (v3, 2026-08-18).
5. Spawn: BLOCKED, `Agent` tool not available. No retry was attempted inside this pass.

The design note, the generator and pass 1's report were not opened. Gate G reconciliation needs a judge classification first, so the design note stays unread until a thread has returned.

## Recomputation ledger
Not produced. Every figure moved after pass 1 (the regional summer declines were reworked), and none of the current figures (Frischbonus 0.49 / Wochenauswahl 0.34 / Dreifachpunkte 0.27 / Monatsziel 0.16 per card-week, CHF 972 / 672 / 528 / 322 thousand, 37,920 active cards, the 24 regional cells) has been checked independently in this pass. Pass 1's ledger does not apply to them.

## Competing answers that survived
Not assessed.

## Spec gates
These were checked mechanically by the orchestrator against the fresh unzip. They are independent of the judge.

| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | 10+ | 14 | yes |
| Distinct formats | 3+ | 8 (csv, docx, json, md, parquet, pdf, txt, xlsx) | yes |
| Largest row count | 25,000+ in one file | 611,400 (`card_week_sales_2026w15_w34.parquet`) | yes |
| Distractors declared | 2+ in `metadata.json`, none labelled in file names | 3 declared (footfall, member panel, competitor prices); no file name labels one | yes |
| Distractors same-world and non-answering | look relevant, do not rank offers or give a graded quantity | footfall (branch x week door counts), panel (regional satisfaction and offer awareness), competitor price index: all tied to the same branches and regions, none carries an offer-level value | yes (judge did not confirm whether any is load-bearing) |
| Deliverable count | 1 to 3 | 2 (docx, png) | yes |
| Deliverables present | every named golden | `golden/programme_offer_2027.docx`, `golden/offer_grid_2027.png` (1500 x 960) | yes |
| Units and rounding stated | every ask | per card-week in CHF to two decimals; programme values in CHF thousands, rounded to the nearest thousand | yes |
| Multi-dimensional asks | not stacked lookups | ranked four-offer table, runner-up gap, 6 x 4 regional grid plus chain row | yes |
| Prompt shape and 25-criteria floor | shape identifiable, 25+ | shape 07 (grid); 24 regional cells + 4 chain values + 4 programme values + call + runner-up + gap + chart elements, well over 25 | yes |
| Realism (containers) | Office containers, A4 | both docx: Microsoft Office Word 16.0, Normal.dotm, real word/page counts, A4 (11906 x 16838 twips); PDF MediaBox 595.3 x 841.9 pt (A4) | yes |
| Realism (prose) | no LLM tells | no em dashes in prompt or submission; a prose read is the judge's job and was not done | not assessed |

## Gate G reconciliation
Not performed. There is no judge classification to compare against the design note.

## Stump power (Gate F)
Not assessed.

## Findings, ranked
1. The pass did not run, so no determinism finding exists for the reworked figures. Pass 1's FIX_NOW stays unresolved until a judge thread confirms the repairs and recomputes the moved figures.
2. No spec-gate failure was found in the mechanical checks above.

## Next action for the author
Re-invoke the rehearsal from a session where the orchestrator has the `Agent` tool. Record that run as pass 3, which is the actual post-FIX_NOW re-judge, because this pass returned no verdict.
