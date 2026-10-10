# determinism-check report, task131, 2026-10-10

Pass 3. This is the one re-judge after pass 1's FIX_NOW. Pass 2 did not run (no `Agent` tool) and returned no verdict. Invoked at /build stage 5 under the author's in-session request to replace task130.

**Process note.** This session also had no `Agent` tool, so no separate judge thread could be spawned. As in pass 1, and as the invocation allowed, the judge review ran in the orchestrator's own thread under the same isolation:

- It read only a fresh unzip of `target.zip` at `/tmp/determinism-check-task131-pass3-1791668690/target/` (byte-identical to `task131/target/`), `prompt.md`, the graded blocks of `submission.md`, `golden/` (checked against the blocks) and the verbatim v3 judge prompt.
- It wrote `/tmp/determinism-check-task131-pass3-1791668690/verdict.md` before opening `metadata.json`, `DESIGN_NOTE.md` or pass 1's report.
- The generator, `checks.py` and `verify.py` were never opened. It used local tools only.
- This isolation is weaker than a spawned thread, because the same context did the extraction.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor (interference: the card is the randomisation unit, the membership is the rollout unit), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Every graded figure reproduces from the pack to the stated rounding. The call is forced by three things together:

- The prompt sets the estimand as the offer "on every member card".
- `st26_offer_catalogue.json` shows allocation by card, with rewards "credited to the card used at the till".
- The parquet shows the spillover directly. Control cards with a Wochenauswahl sibling fall CHF 0.79 per card-week against pure-control cards, so the all-card contrast breaks MP-3 section 4's "against the same change without it".

On memberships whose cards all drew one cell, the Frischbonus leads at 0.4930 against the Wochenauswahl at 0.3409. Every interference-aware estimator gives the same winner and runner-up:

- single-card memberships: 0.492 / 0.341
- card-weighted share regression over all 24,000 memberships: 0.496 / 0.321

No gate failed.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Frischbonus per active card-week (parquet `gross_margin_chf` less `reward_cost_chf`, W15-22 vs W29-34, zero weeks filled; `st26_offer_allocation.csv` cell; `member_cards.csv` membership; same-cell memberships, minus K) | 0.49 | 0.4930 | yes |
| Wochenauswahl | 0.34 | 0.3409 | yes |
| Dreifachpunkte | 0.27 | 0.2679 | yes |
| Monatsziel | 0.16 | 0.1632 | yes |
| Runner-up gap | 0.15 | 0.1520 | yes |
| Active cards 2027 (`programme_plan_2027.xlsx`, Active cards, Total, 2027 plan) | 37,920 | 37,920 | yes |
| Frischbonus 2027 value, CHF k (x52 x 37,920, unrounded, MP-3 s5) | 972 | 972.04 | yes |
| Wochenauswahl value | 672 | 672.26 | yes |
| Dreifachpunkte value | 528 | 528.16 | yes |
| Monatsziel value | 322 | 321.71 | yes |
| St. Gallen Stadt A/B/C/D (July network, region's own K) | 0.55/0.30/0.21/0.40 | 0.5478/0.2977/0.2116/0.4027 | yes |
| Fürstenland | 0.42/0.20/0.09/0.25 | 0.4178/0.2031/0.0865/0.2523 | yes |
| Rheintal | 0.41/0.19/0.09/0.28 | 0.4087/0.1894/0.0904/0.2822 | yes |
| Thurgau Ost | 0.47/0.24/0.15/0.30 | 0.4669/0.2392/0.1504/0.3021 | yes |
| Toggenburg | 0.45/0.27/0.14/0.32 | 0.4484/0.2693/0.1365/0.3222 | yes |
| Appenzellerland | 0.58/0.33/0.22/0.41 | 0.5783/0.3313/0.2192/0.4071 | yes |
| PNG chain row and all 24 cells, title, outline, runner-up mark | as submitted | match | yes |
| Golden memo: Monatsziel "moved more spend than any other offer during the test" | most | gross-sales lift W23-34, same-cell: C 12.79 vs D 10.06, B 11.58, A 9.69 | yes |
| Golden memo: Dreifachpunkte "fell back after the first six weeks" | fades | net lift W23-28 is 3.10, W29-34 is 0.27 | yes |
| Golden memo: "Read card by card, the Wochenauswahl would have come out first" | D first | all cards: D 0.708, C 0.556, A 0.541, B 0.348 | yes |

## Competing answers that survived
None survived as a defensible alternative. Each fork tested:

- **Card-level read over all allocated cards (the stump):** the Wochenauswahl wins at 0.71. The data close it (sibling losses as above). Residual risk: the prompt's "measured the way the programme measures offers", taken with MP-3 s4's "Every card allocated to the test is an active card", is the best textual case for this answer. The golden memo's own footnote repeats that sentence while its estimate excludes 20,195 of 37,298 allocated cards (54 per cent).
- **Own plus sibling-share card regression, multi-card memberships:** C 0.511 vs A 0.505, a narrow flip that pass 1 also saw. It extrapolates a linear spillover model when the full-rollout state is observed directly (pure CC memberships give 0.16), so it is not a reasonable choice. Recorded because a regression-minded solver can reach it.
- **Main cards only:** D 0.679 vs A 0.659. It carries the same interference, so it is not licensed.
- **Regional control versus chain control for the grid:** cells move by up to 0.15 (Thurgau Ost A goes from 0.47 to 0.62). "The same change without it" read by region favours the region's own control. Not equally licensed, but it is the softest point in the grid.
- **January regions:** the SGS, FUE, RHT and APZ rows move (SGS A 0.57, RHT A 0.43). Closed by MP-3 s6 and the network docx.
- **Rounded-then-scaled values** (0.49 x 52 x 37,920 = 966k): closed by MP-3 s5 "carried unrounded" and the prompt's nearest-thousand clause.
- **Margin:** A minus D is 0.152 with sampling SE 0.204 (z = 0.75), and A tops 66 per cent of membership bootstraps. This is thin-but-clean: MP-3 pins the point estimator, every rigorous solver computes the same 0.49 against 0.34, and the prompt rules out a hold. A significance-first solver still lands on A, the only offer clearly above control (z about 2.4).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | 10+ | 14 | yes |
| Distinct formats | 3+ | 8 (csv, parquet, xlsx, pdf, docx, json, md, txt) | yes |
| Largest row count | 25,000+ or large DB | 611,400 (`card_week_sales_2026w15_w34.parquet`) | yes |
| Distractors declared, unlabelled | 2+ in metadata.json, no file name labels one | 3 (footfall, member panel, competitor price checks); names neutral | yes |
| Distractors relevant but unused | same world, weighable | same branches and regions; the panel's "noticed a new offer" by January region invites use; none ranks the offers | yes |
| Distractor answering a graded quantity | reproduces, and a shipped fact rules it out | none produces an offer ranking or a graded figure | n/a |
| Deliverable count | 1 to 3 | 2 (docx, png) | yes |
| Format family | none required | n/a | n/a |
| Multi-dimensional asks | not stacked lookups | 4-offer ranking with values, runner-up gap, 6x4 grid plus chain row, chart structure | yes |
| Goldens present | every named file | `golden/programme_offer_2027.docx`, `golden/offer_grid_2027.png` | yes |
| Units and rounding stated | every ask | CHF to two decimals per card-week; programme values "rounded to the nearest thousand" | yes |
| Prompt shape, 25-criteria floor | identifiable, 25+ | shape 07 grid: 24 cells + 4 chain + 8 ranking/value + gap + call + chart parts | yes |
| Realism | nothing reads LLM-generated | prose, memo and slide read as real work products; one statistical tell in the data (Findings 1) | yes, with risk |

Pass 1 FIX_NOW repairs, verified:
1. MP-3 text unchanged. Section 4 reads word for word as pass 1 quoted it. The design note now says the full rollout "is set by the prompt" (DRAW table, Stump strategy row). **Done.**
2. Prompt: "programme values are rounded to the nearest thousand". **Done.**
3. `target/network_changes_2026-07-01.docx` and `golden/programme_offer_2027.docx` have `docProps/app.xml` set to Microsoft Office Word 16.0 on Normal.dotm, with Words 195 and 499 against content of about 200 and 540 tokens. **Done.**
4. `MP-3_measuring_offers_rev3.pdf` is 595.3 x 841.9 pt, and both docx files are w:pgSz 11906 x 16838. All A4. **Done.**

## Gate G reconciliation
| Field | Judge | Design note |
|---|---|---|
| mechanism | statistical_rigor (interference) | method_or_model_selection (unit of analysis) |
| stumping_family | analytical_non_defect | analytical_non_defect |
| surface_read_dependency | no | no |
| sole_data_defect | no | no |

The family and all flags agree. The two mechanism labels name the same insight, and both are FINE-numbers shapes that pass Gate G, so the build reads the same shape from the outside as from the inside. The judge did not name any declared distractor as the surface read. The one Gate G exposure is unchanged from pass 1: a strict reviewer could call the card-to-membership swap a single_conceptual_flip. The defence holds, because the card-level figure is a biased estimate on a different population, not a correct number read through the wrong lens.

## Stump power (Gate F)
Good on the main call.

- A strong model that applies MP-3 to every allocated card files the Wochenauswahl at about CHF 1.40m. It then fails the call, all four ranks and values, the runner-up and all 24 grid cells at once.
- No file documents the spillover, and the decisive check needs a membership join that the prompt never mentions.
- The Monatsziel decoy is honest: it really did move the most spend, and net margin closes it.
- Too-easy signals: the Dreifachpunkte launch spike and the Monatsziel spend are both disarmed by MP-3 rules (s3 and s2). They test rule-reading, so the stump rests on one insight. No lever recommended.

## Findings, ranked
1. **Calibrated region-by-cell offer effects (realism risk; not FIX_NOW).** This is in `card_week_sales_2026w15_w34.parquet`.
   - The regional control means now spread from -1.86 to -2.14, which is the pass 1 repair.
   - The offer-minus-control effects across the six regions still have an SD of 0.055 to 0.070, where honest sampling at about 400 to 800 cards per cell gives about 0.5.
   - The A>D>B>C order holds in every region with near-constant offsets (A minus D from 0.13 to 0.17).
   - Any sub-split is noisy: split-half A/D is 0.32/-0.01 against 0.68/0.69, and the branch-level effect SD is about 1.5.
   - A reviewer who computes standard errors will read the regional table as placed rather than sampled. The design note records this as residual by construction.
   - Fixing it changes what solvers see and is SEND_BACK-sized, so it is the author's call. It is not a determinism defect.
2. **Golden footnote contradicts the golden's own method (optional FIX_NOW, `golden/programme_offer_2027.docx`).** Footnote 1 says "Every allocated card is an active card" while the table excludes mixed-membership cards. Reword it to keep the zero-week rule and say that the figures read the memberships whose cards all drew one cell. This is a golden-only edit with no pack change.
3. **Uniform container stamps (cosmetic, optional, input_files).** Every Office file in `target/` carries modified 2026-09-14T09:30:00, including the 12 June network notice and the plan marked "Version 2, 9 Sep". Stagger them to each document's own history.
4. **Grid control basis (watch).** The regional control and the chain control differ by up to 0.15 per cell. The memo's footnote 2 could say "against the region's own control cards" without hinting at the main move.

## Next action for the author
Ship to the portal as built. If you want to close the one forensic exposure first, decide on Finding 1 before the portal run, because it means regenerating the card-week facts.
