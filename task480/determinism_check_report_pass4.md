# determinism-check report, task480 (architecture 3, pass 4), 2026-10-31

## Verdict
DETERMINISTIC
**Disposition:** FIX_NOW (solution wording only; the main thread is applying it)
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The thread (verdict: /tmp/determinism-check-task480-pass4/verdict.md, run on a fresh unzip of the re-cut target.zip, sha256 957b43dae6f8e26f) recomputed the stock, births and deaths exactly and found the call forced by the out-of-sample test on the shipped 2000 and 2010 censuses. Cedar Run is over 10,000 and Maple Ford under it in every well-formed age-profile variant. The only defect: the quoted 10,787 and 9,611 do not reproduce, because the solution files neither the dwelling-type grouping nor the treatment of YEAR_BUILT = 0. The thread's own specification gives 10,675 and 9,451. The main thread is naming the four types by roll land use code, taking the placeholder year as 1900 and using OLS without an intercept; no figure moves. That edit is not re-judged by me.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Dwellings 1 Apr 2020 | 45,334 (census H1_001N) | 45,334; block-group gaps at most 6 | yes |
| Dwellings 1 Jul 2026 | roll + COs - demolitions | equal to active residential address points in all 14 municipalities | yes |
| Cedar Run, eight-band | 10,787 | 10,675 (24 variants: 10,409 to 11,101) | no (spec unfiled); side yes |
| Maple Ford, eight-band | 9,611 | 9,451 (variants: 9,157 to 9,547) | no (spec unfiled); side yes |
| 2020 persons per dwelling: Maple Ford, Cedar Run | 10,451; 9,735 | same | yes |
| Births (14, total 978) | ask 2 | all 14 equal | yes |
| Deaths (14, total 1,070) | ask 3 | all 14 equal; RES_MCD_CODE wrong on 97 | yes |
| Back-cast errors | ordering stated | profile 2.9%, 3.7%; municipality ratio 4.5%, 6.5%; block-group persons per dwelling 6.9%, 12.4% | ordering yes |
| Tier set | Juniper, Dunmore, Cedar Run | same | yes |

## Competing answers that survived
None survives the back-test. Municipality 2020 ratio (Juniper, Dunmore, Maple Ford), block-group persons per dwelling (four in, Cedar Run 10,709, Maple Ford 10,461) and countywide persons per dwelling (Fallon 10,021 in) all lose it. Residual: no shipped sentence files the selection criterion, so the call rests on the solver choosing to validate (Gate C, accepted as the analytical layer). Maple Ford's margin to the line is thin (about 3.9 to 5.5%) but every rigorous variant stays under.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files, formats, large file | 10+, 3+, 25,000+ rows | 14; csv, xlsx, pdf; address points 50,055 rows | yes |
| Distractors | 2+ in metadata.json, not labelled by file name | DOT road miles, county estimates v2025 | yes |
| Distractors relevant, unused, ruled out | | thin: the county file is county totals (cross-check only, does not decide the call); road miles belongs to another formula | yes, thin |
| Deliverables | 1 to 3, in golden | 2 (xlsx, svg) | yes |
| Asks multi-dimensional, unit and rounding | | 14-row tier, births and deaths; "whole counts" | yes |
| Prompt shape, 25+ criteria | | shape 10; 14 x 3 cells plus chart and call | yes |
| LLM tell / golden realism | | none seen by the thread; I did not audit goldens | yes (unaudited) |

## Gate G reconciliation
Thread: method_or_model_selection, analytical_non_defect, surface_read_dependency no, sole_data_defect no. Gate H: domain pass, layers pass, decisive_step analytical (swap test holds; the textbook 2020 ratio is the wrong route a strong analyst can take).
Card and design note (stump_class analytical; analyst_test: the 2020 ratio names the wrong municipalities; domain_test: housing unit method with an age-modelled yield; stump sentence: Cedar Run in, Maple Ford out): match. The declared distractors are not the surface read. Reading from the previous pass, the design note's ladder gave wider golden ranges (Cedar Run 10,348 to 10,813; Maple Ford 9,013 to 9,623) than the thread's variants; both sit on the same sides.

## Stump power (Gate F)
Good on paper. The textbook route files Maple Ford in and Cedar Run out; a solver who fits the age profile reaches the golden sides even if it skips the boundary adjustment, so the stump is method choice, not a lookup. The main thread should weigh that the strongest solvers know the housing unit method and may reach an age profile without prompting; no filed criterion forces it, and the reachability of an age-aware profile by a strong model is the open stump-power question. The deaths ask bites independently (97 deaths wrong on RES_MCD_CODE).

## Findings, ranked
1. FIX_NOW (wording): quoted eight-band estimates not reproducible without the filed type grouping and year-0 convention. Being fixed (land use codes, 1900 placeholder, OLS without intercept).
2. The chart (ask 4) varies 1 to 2% across valid specifications; gradable on sides and shape only.
3. Method not filed; call depends on the back-test (Gate C residual).
4. Critical component 2 on year-built persons per dwelling was not independently run (directional support only).
5. Thin distractors.

## Next action for the author
Finish the wording edit in step 1 and 2 of the solution (the four dwelling types by land use code, the year-0 placeholder as 1900, OLS without an intercept) and restate the critical component figures to match what that specification reproduces on the shipped bundle. A FIX_NOW has now been re-judged once; do not request a further pass for wording-only edits.
