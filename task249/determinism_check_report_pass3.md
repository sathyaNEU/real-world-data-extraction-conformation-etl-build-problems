# determinism-check report, task249, pass 3, 2026-11-01

## Verdict
DETERMINISTIC (no SOLUTION_WRONG)
**Disposition:** APPROVE
**Stumping type:** mechanism: decomposition_attribution, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Re-check reship (header renames, regulations 3.3 and 3.6 sentences, prompt without form count, data_notes.md removed; target.zip sha256 prefix fe00c50c). Reg 7.2 files the estimand as a counterfactual. Executed literally on the shipped bundle it gives the six flagged forms (A, B, C, D, G, H) with at least 0.43 margin to the 1.0 line, and both ancillary tables reproduce exactly. Every graded figure is unchanged from the golden. Judge thread: one pass, sonnet, isolated at /tmp/determinism-check-task249-run3 (verdict.md there). Note: my runtime had no Agent tool, so the main session spawned the thread from my judge_brief.md.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Resit sittings 2027 | 6,373 | 6,373 | yes |
| Gain per resit sitting (A,B,C,D,E,F,G,H,I,J) | A,B,C,D,G,H >= 1.4; others <= 0.6 | 1.70, 1.74, 2.37, 1.83, 0.57, 0.17, 1.64, 1.90, 0.44, 0.54 | yes |
| Excess on shown items (A,B,C,D,G,H) | >1.0 on A,C,G,H; ~0.5 on B,D | 1.44, 0.48, 1.80, 0.49, 1.14, 1.16 | yes |
| Recognised-item time ratios | 0.6 / 0.7 / 0.8 | 0.60 / 0.72 / 0.80 | yes |
| First-timer time expiry B, D, I | 36 to 48 percent | 40.5, 36.2, 47.6 | yes |
| Ask 2 workstation/power, A..J | 39,43,29,39,40,46,45,37,51,44 | identical | yes |
| Ask 3 link down, A..J | 64,71,53,60,73,75,71,72,84,60 | identical | yes |

## Competing answers that survived
None on the main call or the asks as filed. Tested and rejected: gain over previous sitting (nine forms, rejected by 7.2); shown-item excess only (A,C,G,H; rejected, 7.2 counts items answered only because time was freed); exact-item exposure ignoring item-model siblings (A,B,D,G only; closed by 7.2 wording, reg 3.4 and the bank item_model, with the 0.80 sibling time ratio in the data); excluding trial-only exposure (no change).
Advisory, residual in ask 2: 32 sittings carry NET_LOST, WS_FAIL, NET_BACK on one client with no resume and no incident report (2 to 5 per form). A reader counting every in-sitting WS_FAIL would add them. The golden excludes them (the client kept logging; 3.6 and the prompt word "interrupted"). Not a fail, but the cheapest remaining fork; one solution-text sentence would close it, or a filed sentence if the author wants it shut in the pack. No log dictionary ships.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | >= 10 | 16 | yes |
| Formats | >= 3 | 4 (csv, xlsx, pdf, eml) | yes |
| Large file | >= 25,000 rows | workstation_event_log 59,240; results r3 24,061 plus r4 9,501 | yes |
| Distractors | >= 2 in metadata, none named in a file | 4 (practice orders, centre capacity, panel log, panel minutes); file names do not label them | yes |
| Distractor use | unused by the solution, weighable | not used; review bookings are used only as an exposure source; no distractor reproduces a graded quantity per judge | yes |
| Deliverables | 1 to 3, all in golden | 2, both present in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 10-form tables, "whole numbers" stated | yes |
| Prompt shape / rubric | shape identifiable, >= 25 criteria | shape 10 in metadata; rubric is generated and not visible here, not verified | shape yes, count unverified |
| Reads as real | no LLM tells | no authoring leakage found by judge; minor: reg 3.6 "amended 9 June 2027" with no earlier text shipped, harmless, could be dropped | yes |

## Gate G reconciliation
Thread: mechanism decomposition_attribution, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: stump is the time the recognised items free, spent on later items on speeded forms (B, D), against the natural shown-item excess; no decoy, nothing planted. Match. The declared distractors are not named by the thread as the surface read. Gate G passes: no shipped artifact ranks the forms wrongly.

## Gate H line
domain: pass (psychometric item-exposure and speededness estimation); layers: pass (Layer 1 export layouts, units, renumbering, number chains, UTC/IST; Layer 2 the 7.2 estimator with time-freed answers and sibling recognition); decisive_step: analytical.
The note's decisive step (count items reached only in freed time, add to the shown-item excess) agrees with the thread. 7.2 files only the counterfactual, not the method, so this is the WHAT, not the HOW; the card's stump_class and analyst_test were not separately opened beyond the note's Three rules, which match.

## Stump power (Gate F)
Good per the thread: three natural routes give wrong sets (nine forms, four forms, four different forms), and the time and sibling mechanisms must be found in the data. The decisive step is not classed analytical merely because the method is standard. The main thread should still weigh it against the note's ladder: a strong solver who discovers the speededness effect lands the call, and the flagged set has wide margins, so only a solver who stops at shown items or exact items misses.

## Findings, ranked
1. Advisory only: the WS_FAIL-between-NET_LOST-and-NET_BACK exclusion in ask 2 (32 sittings) is not filed in the pack.
2. Minor: reg 3.6 "amended" tag with no prior text.
3. Rubric criterion count not verifiable from the folder.

## Next action for the author
Optionally add the one-sentence exclusion to the solution text (or a filed sentence in the regulations); otherwise ship.
