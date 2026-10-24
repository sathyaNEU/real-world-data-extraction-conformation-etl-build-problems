# determinism-check report, task482, 2026-10-24 (pass 3, round 2 pack, target.zip sha256 632eeb37...c9765)

## Verdict
NOT_DETERMINISTIC (narrow: underspecified_objective on one half-cent tie; the 16-district set and the PL block are forced)
**Disposition:** FIX_NOW
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect (borderline), surface_read_dependency: no (borderline), sole_data_defect: no

## Why
LD-1053 (Dunrenmont City Schools) has fee 11,537.50 x 15% = exactly 1,730.625. The prompt says "nearest cent" and no shipped file sets a tie rule. Half-up gives 1,730.63; the golden's 1,730.62 (memo OG-2526-1053) is the generator's Python `round(x, 2)` on a binary float, i.e. an artifact, not a filed convention. The same tie moves the headline: exact sum of the 16 credits is 25,479.375, so a half-up reader files 25,479.38 against the golden's 25,479.37 (sum of individually rounded credits; the sum-then-round reading is a second fork). Critical Component 2, the Final Recommendation total and one memo row are affected. The district set (16), the PL block (18 districts, USD 9,250.00) and 33 of 34 memo rows are unaffected.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Eligible and assessed students | 26,497 | 26,497 (eligibility Y + crosswalk + Submitted sessions) | yes |
| Roster band counts | Table 8 | 6,429 / 7,177 / 7,274 / 7,241 / 1,469 | yes |
| Districts owed outcomes credit | 16 | 16, same LD ids (own EM latent regression, 179-point grid) | yes |
| Outcomes credit total | 25,479.37 | 25,479.375 exact | set yes; cent no (tie) |
| PL shortfall total | 9,250.00 / 18 districts | 9,250.00 / 18 | yes |
| Memos | 34 | 34 | yes, except LD-1053 cent |
| Easy route (district-averaged PVs) | design note 32,137.49 / 19 | 32,137.50 / 19 | set yes; 1 cent note drift (same tie class, outside the golden) |

## Competing answers that survived
1. Half-cent tie: 1,730.62 (golden) vs 1,730.63 (half-up); total 25,479.37 vs 25,479.38. No shipped rule closes it. The design note's fork row 10 and 11 claim no tie ("no district within 4.8 points") but cover the share against the benchmark, not the fee x percentage product. Only 5 products in the pack are ties; only LD-1053's belongs to a credited district.
2. Method (PV-average, 19 districts, USD 32,137.50, vs district-aware refit, 16): this is the intended Layer 2 stump, open by design. Six district-conditioned specifications all give the same 16, smallest gap 4.4 points (LD-1047). Not a defect; see Gate H.
3. Closed correctly: PD `hours` column (3.0 on LL-210/LL-233 rows) vs catalog lengths (the catalog governs; the column gives 3 districts, USD 1,000); apply-to invoice (layout PDF's "open subscription invoices for the following term" excludes add-on, lab-kit and true-up invoices; "any open invoice" would change five rows, so the layout text is load-bearing and sufficient). No session within a day of a term boundary.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 | yes |
| Formats | 3 or more | 4 (csv, pdf, xlsx, docx) | yes |
| Large file | 25,000+ rows | 304,109 (item responses); 5 files over 25,000 | yes |
| Distractors | 2+ in metadata, none labelled by name | teacher_implementation_survey_spring2026.csv, renewal_forecast_2026_27.xlsx; names are not labels; neither feeds a graded figure; judge reproduced that no figure reads them | yes |
| Distractor relevance | weighable, ruled out by a shipped fact | settlement is on assessed achievement and delivered sessions; plausible, none answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, csv), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 4 asks over 58 districts; the prompt states half hour and cent (but not the tie rule) | partial (tie) |
| Prompt shape and 25+ criteria | identifiable, 25+ | per-district results, hours, credits and 34 memos are separately gradable; the rubric is generated and I did not see it | not verified |
| Not LLM-reading, golden realism | yes | judge found no authoring leaks; golden realism not re-judged here | no finding |

## Gate G reconciliation
Judge: no shipped artifact ranks districts wrongly; the declared distractors are not wrong-basis (metadata `wrong_basis_distractors` is empty) and the judge named the contractor's plausible values (a real deliverable, not a declared distractor) as the surface read that carries the default path. Design note: same (L1 default, 19 districts), which it declares as the real deliverable and not a decoy. Match. Mechanism (method/model selection, population-model misspecification) matches the note's `field_method`. Finding to watch: the golden rationale "credit districts that met their benchmark" leans toward "reject the reported read"; the judge classed surface_read_dependency as no, borderline.

## Stump power (Gate F)
Good if the golden is accepted. A strong analyst who cleans everything and averages the shipped PVs (or EAPs) files 19 (or 25) districts, not 16. The bias is real: a district-free refit reproduces the PVs. Gate H line: domain pass; layers pass (Layer 1 re-keyed ids, state codes, abandoned vs submitted sessions, series hours, invoice mix; Layer 2 district-aware latent regression for subgroup proficiency shares); decisive_step analytical. This matches the note's Three rules and analyst test. The thread also reports that the field's secondary-analysis practice is that the conditioning model must include the grouping variable, which is a standard method, so the blind readers' result should be weighed with it (the judge could reach the golden by applying it).

## Findings, ranked
1. Half-cent tie at LD-1053 and the two total conventions (sum of rounded vs rounded sum): unfiled, golden rests on float rounding. Gates C and E on the headline total and one memo.
2. Optional: the prompt names no estimand sentence for the share ("from its own students' responses"); file only the WHAT, never the method. The judge calls this optional, not required; the 10/10 rules bar filing the HOW.
3. Design note's default-path total reads 32,137.49 against 32,137.50 recomputed (same class); correct when the rounding rule is fixed.

## Next action for the author
Remove the tie rather than file a method: change LD-1053's seats or price in the generator so fee x percentage is not a half-cent, check the other credited products for ties in `checks.py`, regenerate, and update the total, Critical Component 2, the LD-1053 memo and the sheet. (Alternative: file "round half up to the cent, each credit rounded before summing" in the prompt, regenerate the golden with decimal half-up, total 25,479.38 and memo 1,730.63, then re-judge once.) Stage 4 then proceeds.
