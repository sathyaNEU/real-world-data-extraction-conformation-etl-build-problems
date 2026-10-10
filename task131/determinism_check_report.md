# determinism-check report, task131, 2026-10-10

Pass 1. Invoked at /build stage 5 under the author's request in session to replace task130.

**Process note.** The orchestrator had no `Agent` tool in this environment, so no separate judge thread could be spawned. The judge review was run in the orchestrator thread under the same isolation. It read only the fresh unzip at `/tmp/determinism-check-task131-1791667861/target/`, `prompt.md`, the graded blocks of `submission.md`, and the verbatim v3 judge prompt (`guidelines/determinism_judge_system_prompt.md`). It wrote `/tmp/determinism-check-task131-1791667861/verdict.md` before `DESIGN_NOTE.md`, `metadata.json` or the golden files were opened. The generator, `checks.py` and `verify.py` were never opened. It used local tools only and no server tools. Treat this as weaker isolation than a spawned thread, because the same context did the extraction.

## Verdict
DETERMINISTIC
**Disposition:** FIX_NOW
**Stumping type:** mechanism: statistical_rigor (interference: card is the randomisation unit, membership is the rollout unit), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
MP-3 rev 3 pins the metric (net margin after reward cost), the windows (W15-W22 baseline, W29-W34 run rate), zero-filled card-weeks, the annual value (x52 x the plan's 37,720 active cards, rounded once) and the 1 July 2026 regions. The test is randomised by card (`st26_offer_catalogue.json`, `allocation.unit: card`, rewards credited to the card used at the till), and cards of one membership visibly shift baskets toward the offer card. The card-level contrast therefore overstates the "on every member card" effect. Read on memberships whose cards all drew one cell, the Frischbonus leads at 0.49 against 0.34, and every committed figure reproduces exactly. No gate failed.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Frischbonus, per active card-week (same-cell memberships; parquet gross_margin_chf less reward_cost_chf, allocation cell, member_cards membership_no) | 0.49 | 0.4926 | yes |
| Wochenauswahl | 0.34 | 0.3396 | yes |
| Dreifachpunkte | 0.26 | 0.2630 | yes |
| Monatsziel | 0.16 | 0.1612 | yes |
| Active cards 2027 (`programme_plan_2027.xlsx` Active cards, Total, 2027 plan) | 37,720 | 37,720 | yes |
| Frischbonus 2027 value, CHF k | 966 | 966.2 | yes |
| Wochenauswahl 2027 value | 666 | 666.1 | yes |
| Dreifachpunkte 2027 value | 516 | 515.9 | yes |
| Monatsziel 2027 value | 316 | 316.2 | yes |
| Runner-up gap per card-week | 0.15 | 0.1530 | yes |
| St. Gallen Stadt A/B/C/D | 0.55/0.30/0.21/0.40 | 0.5504/0.2965/0.2083/0.4030 | yes |
| Fürstenland | 0.42/0.20/0.08/0.25 | 0.4178/0.2017/0.0830/0.2523 | yes |
| Rheintal | 0.41/0.19/0.09/0.28 | 0.4114/0.1883/0.0872/0.2824 | yes |
| Thurgau Ost | 0.47/0.24/0.15/0.30 | 0.4668/0.2380/0.1469/0.3023 | yes |
| Toggenburg | 0.45/0.27/0.13/0.32 | 0.4509/0.2680/0.1332/0.3224 | yes |
| Appenzellerland | 0.58/0.33/0.24/0.41 | 0.5787/0.3306/0.2373/0.4078 | yes |
| PNG chain row | 0.49/0.26/0.16/0.34 | same | yes |
| Monatsziel "moved the most spend" (memo prose) | most | gross sales lift W23-W34, card level: C 13.29 vs B 10.90, D 10.43, A 9.14 | yes |
| Dreifachpunkte "fades after launch" | fades | net lift W23-W28 vs W29-W34: B 3.21 down to 0.26 (same-cell) | yes |

Regions use `network_changes_2026-07-01.docx` (2209 to 6101, 4105 to 4101, 3107/3112/3115 to St. Gallen Stadt). The January-register misread moves cells in four regions (for example Rheintal A 0.44, St. Gallen Stadt A 0.57), so the device is gradable.

## Competing answers that survived
None survived as a defensible alternative to the main call. The forks tested:

- **Card-level over all allocated cards** (the intended trap): Wochenauswahl 0.71 > Monatsziel 0.55 > Frischbonus 0.54 > Dreifachpunkte 0.35, giving Wochenauswahl at about CHF 1,387k. The data closes it. Offer cards in mixed memberships gain +0.17 to +0.28 baskets per week against about 0 in same-cell memberships, and control cards with an offer sibling change by -2.47 CHF per week against -2.00. **Residual risk:** MP-3 s4 says "Every card allocated to the test is an active card", which a literal reviewer can read as a sample rule licensing the card-level answer. Only the prompt ("goes on every member card") states the full-rollout estimand. MP-3 does not, although the design note says it does (see Findings 2).
- **Household share regression, all 24,000 memberships:** A 0.50 / D 0.32 / B 0.28 / C 0.26. The call and runner-up are unchanged. The headline is about CHF 973k and Monatsziel moves 0.16 to 0.26, so it is a supplementary-figure fork, but it is not MP-3's difference-of-means form.
- **Own plus sibling-share card regression, multi-card memberships:** C 0.513 vs A 0.504, a narrow flip. It needs a linear-spillover model that MP-3 does not use, so I judge it unreasonable here. It is recorded because a regression-minded solver could reach it.
- **Single-card memberships only, and multi-card same-cell only:** identical to the golden at 2 dp.
- **Thin gap in noise terms:** A minus D is 0.153 with SE 0.204 (z about 0.75, a membership bootstrap agrees). Every rigorous MP-3 solver gets the same point estimate, so this is thin-but-clean, not margin_or_boundary_fragility. A statistics-first reviewer may still call the test underpowered to separate the two leaders.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | 10+ | 14 | yes |
| Distinct formats | 3+ | 8 (csv, parquet, xlsx, pdf, docx, json, md, txt) | yes |
| Large file | 25,000+ rows or large DB | parquet 611,400 rows | yes |
| Distractors declared, unlabelled | 2+ in metadata.json, none named as such | 3 (footfall, member panel, competitor price checks); file names neutral | yes |
| Distractors relevant but unused | same world, weighable | all three are Talwerk branch or member data; the member panel's "noticed a new offer" and January sample frame invite use; none ranks the offers | yes |
| Distractor answering the question rules itself out | n/a | none produces an offer ranking or a graded figure | n/a |
| Deliverables | 1 to 3 | 2 (docx, png) | yes |
| Format family | none required | n/a | n/a |
| Multi-dimensional asks | not stacked lookups | 4x2 ranking, gap, 6x4 grid plus chain row, chart structure | yes |
| Goldens present | every named file | `golden/programme_offer_2027.docx`, `golden/offer_grid_2027.png` | yes |
| Units and rounding stated | every ask | per card-week "CHF to two decimals" yes; programme value "in CHF thousands" with no rounding stated | **partial** |
| Prompt shape and 25-criteria floor | shape identifiable, 25+ | shape 07 grid: 24 cells + 4 chain + 8 ranking + gap + headline pair + chart parts, well over 25 | yes |
| Realism | nothing reads LLM-generated | prose and goldens read as real work products; container and data tells below | **partial** |

## Gate G reconciliation
| Field | Judge | Design note |
|---|---|---|
| mechanism | statistical_rigor (interference) | method_or_model_selection (unit of analysis) |
| stumping_family | analytical_non_defect | analytical_non_defect |
| surface_read_dependency | no | no |
| sole_data_defect | no | no |

The family and all three flags agree. The mechanism labels differ but name the same insight (reading a card-randomised test at the membership), and both are FINE-numbers shapes that pass Gate G. There is no inside/outside shape mismatch. The judge did not name any declared distractor as the surface read. The one Gate G risk is a reviewer calling the card-to-membership swap a single_conceptual_flip. The design note's lens-swap test (a different population, about 42 per cent of cards, with figures that are not a relabelling) is the right defence, and the judge's read supports it.

## Stump power (Gate F)
Moderate to good. A strong model that applies MP-3 to every allocated card, which s4's wording invites, files Wochenauswahl at about CHF 1.39m. Nothing in the prompt names the membership join, and the decisive move needs a group property computed through `member_cards.csv`. Too-easy signals: the two secondary rungs are pre-disarmed by the standard, so they test rule-reading rather than analysis. The Dreifachpunkte launch spike is closed by the MP-3 s3 run-rate window and Monatsziel's spend by the s2 net-margin definition. The whole stump therefore rests on one insight. No lever is recommended. Do not add membership wording anywhere.

## Findings, ranked
1. **Calibrated cell means (realism and data-honesty risk; not FIX_NOW).** In `card_week_sales_2026w15_w34.parquet`, the six regional control means sit between -1.985 and -2.013 while their SEs are 0.30 to 0.45. Single-card and multi-card same-cell subsets match the chain effects to the third decimal, and every region repeats the A>D>B>C ordering with near-constant offsets. Honest sampling cannot produce this (the design note's "regional targets are forced per area" is the cause). A reviewer who computes standard errors will read the pack as fabricated, and will also see that the 0.15 decisive gap is under one SE. The fix is to regenerate with honest per-stratum noise and re-judge, which is SEND_BACK-sized. It is the author's call, because it would also unsettle the estimator convergence the build relies on.
2. **The design note says MP-3 states the full-rollout estimand, and the shipped PDF does not.** The DRAW table and "The decisive move" item 1 say the standard defines "incremental net margin per active card-week if every card carried the offer". Shipped MP-3 s4 says only "...against the same change without it, and it is stated per active card-week. Every card allocated to the test is an active card." The estimand is pinned by the prompt alone, and the s4 sentence is the best textual argument for the card-level decoy. FIX_NOW: correct the design note to describe what ships. Do not add rollout wording to MP-3, because it would hint the move.
3. **Rounding not stated for the CHF-thousands figure (FIX_NOW, `prompt.md`).** "as a single amount in CHF thousands" fixes the unit but not the rounding, so 966 and 966.2 are both licensed. Change it to "in CHF thousands, rounded to the nearest thousand" in the first paragraph, and use the same wording for the four programme values in the second.
4. **docx container tell (FIX_NOW, generator post-processing).** `docProps/app.xml` reads `<Application>Microsoft Excel</Application>` with Words and Characters 0 in both `target/network_changes_2026-07-01.docx` and `golden/programme_offer_2027.docx`. Set Microsoft Office Word with real counts. Rebuild target.zip from the generator.
5. **Cosmetic (FIX_NOW, optional).** `MP-3_measuring_offers_rev3.pdf` is US Letter, and a Swiss co-operative standard would be A4.

## Next action for the author
Apply Findings 2 to 4 in the generator and prompt (design-note wording, rounding clause, docx app properties), rebuild the pack and re-judge once. Before that, decide whether Finding 1's calibrated means are acceptable risk or warrant regenerating the card-week facts with honest noise.
