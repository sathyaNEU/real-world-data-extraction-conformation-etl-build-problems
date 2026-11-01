# Determinism check, task311

Each round's isolated judge read only the prompt, the cut bundle and the submission's graded blocks, wrote its own derivation first, then compared. Verdicts verbatim.

## Round 1 (2026-11-01, target.zip 08eedf9f)



**Order kept:** yes. I wrote derivation.md (own derivation from target/ only) before opening graded_blocks.md, then compared.

- **Verdict:** NOT_DETERMINISTIC
- **Disposition:** SEND_BACK. The projection of the boosted standard error must be filed (or forced by the data) so that each graded share and the runner-up's matching boost are one number; this changes what solvers do, so a rerun is required.
- **Why:** The terms (wexcombe_boost_terms_2027.pdf s.3) ask for "one minus the ratio of the SE with the boost to the same SE without it, both as the Centre would publish them", but no shipped text says how a boosted SE is projected from the 2025 wave, and the defensible projections give different graded cells. The main call (Central Valley, runner-up Lakeshore) survives every variant I ran, but the supplementary cells (shares, the runner-up's matching boost) do not. Gates B/C/E fail on supplementary questions 1 and 4. Label: underspecified_objective / competing_defensible_answer (margin_or_boundary_fragility for the match boost).
- **Evidence:**
  - Reproduced: Table 2 of the technical report exactly (n 697/2479/1196/1193/2503; estimates 22.2/8.5/8.4/15.6/8.4; SE 3.97/0.84/0.79/2.05/0.86; deff 6.36/2.27/0.97/3.79/2.40). Join: Northmark 2025 areas and Ostrander CVL-nnn -> 2nnn, LKS-nnn -> 3nnn are post-2024 numbers (the 20 supplement areas CVL-061..080 with 5 completes each confirm it; Table 1 totals match); weights file is pre-2024 keyed, mapped by the concordance; strata = reorganised regions plus the CV supplement. 2024 block reproduced with the 2024-04-22 numbering cut: North 701/25.4/5.21, CV 2507/7.6/0.98, Lakeshore 1203/7.1/0.78, SUP 1207/13.0/1.65, Metro 2525/7.2/0.62.
  - Golden's method (stratum ANOVA components, between-variance floored at 0, baseline = model variance) reproduces: CV 44.3, Lakeshore 29.4, Metro 6.8, SUP 6.3, North 4.4, and Lakeshore needs 27 per area.
  - Surviving forks (all on shipped text read literally):
    1. Baseline. The words "as the Centre would publish them" read literally make the denominator the published 2025 SE (observed variance), not a modelled one. Then: CV 30 (29.9), Lakeshore 27, and Lakeshore matches at 14 per area, not 27 (Bernoulli within-variance: CV 31, Lakeshore 28, 15). Same call, different cells.
    2. Within-area variance estimator. Stratum-pooled ANOVA gives North 4.4 (4%), SUP 6.3 (6%); Bernoulli p(1-p) gives North 5.2 (5%), SUP 7.0 (7%). The whole-per-cent cells flip.
    3. Between-component floor. Without the zero floor (subtract the within reduction from the observed variance) CV is 69%, Lakeshore 31%; with it 44% and 29%. The CV supplement stratum (5 completes per area, huge weights) drives the sensitivity.
    4. "Match" = unrounded share (27 per area) or whole-per-cent share (26 per area).
  - 2024 numbering cut: the case export switches from old to new area numbers between 2024-04-08 (last old-only number) and 2024-04-22 (first new-only number); cuts at 04-09 to 04-21 give different 2024 cells (North 675/27.4/5.39 and so on). Only the data (and not any filed sentence) separates them; this is an ask-side semantics point, not the main call.
  - Naive route: hold the 2025 design effect (SE scales with the root of n) gives CV 18%, Lakeshore 29%, North 39% and so picks Lakeshore, wrong. Real, analytical.
- **Files/Hygiene:** PASS. 11 files; formats csv, xlsx, pdf, json, txt; northmark export 39,976 rows; distractors present (pharmacy register, fieldwork quotes, health_regions list); no exclusion-level finding. The quotes workbook is correctly irrelevant to placement. Technical report and terms are internally consistent with the data.
- **Stump power:** Strong. The easy route (constant design effect, or the largest-SE region) picks Lakeshore or North; the correct route needs the between/within variance split and the supplement stratum's 5-interview take, which puts the boost in the Central Valley. A strong model plausibly fails, but the graded cells beyond the call are not pinned.
- **Stumping type:** `mechanism: method_selection`, `stumping_family: analytical_projection (FINE-numbers: variance decomposition)`, `surface_read_dependency: no`, `sole_data_defect: no`. Passes Gate G, the difficulty is the choice of how to project a clustered-sample variance, not a rejected surface read.
- **Three rules:** `domain: pass`, `layers: pass`, `decisive_step: analytical`. The field's own analysis (design-effect and variance-component planning of a survey boost, with the supplement stratum's tiny take) decides it; the easy route a strong analyst takes, holding the 2025 design effect, gives Lakeshore at 29% against Central Valley's 18%, the wrong region.
- **Fix:** prompt/terms (input_files): file the WHAT of the projection so the cells are single numbers: that the 2027 standard error with and without the boost both come from the same projected variance (or that the without-boost figure is the published 2025 SE), that between-area and within-area components are estimated by one-way analysis of variance per stratum with a negative between-component set to zero, and that "match" means the unrounded share (or the rounded one). Then regenerate figures and re-check that North and SUP whole-per-cent shares are the same under any filed estimator. The main call and the stump stay frozen.

## Round 2 (2026-11-01, target.zip 2ec516f2)

- **Verdict:** DETERMINISTIC
- **Disposition:** FIX_NOW. Lead the runner-up answer with 27 interviews per area (the prompt asks per area; 2,700 total is the same figure) and compare unrounded shares; no model rerun, files untouched.
- **Why:** The main call is forced: Central Valley 44% against Lakeshore 29%, with the naive routes failing (SRS puts North first at 39%; a design-effect projection that holds the 2025 weighting effect puts Lakeshore first at 29% against Central Valley 18%). The shipped Table 2 ICC (stated "for planning") and the terms' "both reckoned in the same way for the 2027 design" fix a weighted variance-component projection, and every committed figure reproduces. Residual softness (below) is on whole-per-cent shares and the runner-up boost only, not on the call.
- **Evidence:**
  - Reproduced: Table 1 completes exactly (N 700, CV 2504, LKS 1210, SU 1162, Metro 2516). Table 2 estimates, SEs and design effects exactly (CV 8.97/1.013/3.11, LKS 6.85/0.682/0.88, N 25.12/4.561/7.69). Ostrander CVL-nnn and LKS-nnn are the post-2024 numbers 2000+nnn and 3000+nnn.
  - Golden shares reproduce: CV 43.91, LKS 29.16, SU 13.93, Metro 7.77, N 3.62.
  - Runner-up boost: Lakeshore overtakes at 27 per area (43.66 at 26, 44.39 at 27 against 43.91).
  - Critical components reproduce: supplement take 5 to 20, weighting effect 3.37 to 1.57, North between-area share 89%.
  - 2024 reproduces exactly: N 702/24.4/3.98, CV 2506/8.6/1.09, LKS 1207/8.2/0.84, SU 1164/12.3/1.70, Metro 2522/8.9/0.75.
  - The Northmark numbering cutover is recoverable from the data alone. Code 2081 (pre-only) appears on 19 April and 5059 (post-only) on 22 April. A 1 April cut leaves only 275 areas with erratic takes, while the 22 April cut gives 300 areas with uniform takes per stratum.
  - Residual forks (none changes winner or runner-up):
    - Method fork. A method-of-moments split of the 2025 data, or subtracting the model reduction from the published variance, gives CV 49 to 56% and LKS 34 to 35%, with b* 23 to 29. The shipped ICC and the "reckoned the same way" wording favour the golden.
    - Rounding fork. Comparing rounded shares would give 28 rather than 27, since 44.39 and 43.91 both round to 44.
    - Unit fork. The "smallest boost" answer could be read as 27 per area or as 2,700 total.
    - 2024 SE under old strata. LKS comes out 0.85 against 0.84, but the report defines the strata as the five regions.
- **Files/Hygiene:** PASS. 11 files in 5 formats (csv x4, xlsx x2, txt x2, json, pdf x2). Distractors are the pharmacy register and the fieldwork quotes. Two vendors' code frames and date formats differ (realistic Layer 1 mess). Timeline coherent (export June 2025, report Nov 2025, terms Oct 2026). No authoring disclosures seen. Synthetic but plausible.
- **Stump power:** Good. The decisive trap is that the Central Valley's design effect of 3.11 with ICC 0 is weighting from the 20-area supplement stratum (about 5 completes each), which an equal per-area boost removes. A strong model that scales the design effect by cluster size or uses SRS names North or Lakeshore. The North ICC of 0.184 also defeats the SRS route.
- **Stumping type:** mechanism: method_or_model_selection (variance projection); stumping_family: analytical_non_defect; surface_read_dependency: no; sole_data_defect: no. The published SEs are correct and the difficulty is projecting them under a changed design.
- **Three rules:** domain: pass, layers: pass, decisive_step: analytical. Survey-sampling variance projection is the field's own work, and the swap test fails to preserve it. Layer 1 is the two vendors' formats, the reorganised area numbering and the mid-April numbering cutover. Layer 2 is the variance-component projection. The easy route (SRS scaling, or a deff-scaling that keeps the 2025 weighting effect) files North at 39% or Lakeshore at 29% with Central Valley at 18%.
- **Fix:** solution, wording only: state the runner-up answer as 27 interviews per area; optionally state that shares are compared unrounded. No change to the prompt or files.


## Round 3 (2026-11-01, target.zip 2ec516f2, the FIX_NOW re-judge)

- **Verdict:** DETERMINISTIC
- **Disposition:** APPROVE. No repair needed, no rerun. Optional, low risk: the 2024 North SE has a 3.98 / 3.94 fork (see Evidence) that the shipped Technical Report section 4 already closes, so no edit is required.
- **Why:** My blind derivation from the bundle matches every committed answer. Central Valley is funded (44%), Lakeshore is runner-up (29%) and needs 27 more interviews per area, and the 2024 restated block reproduces. The answer is forced by: boost = 1200 / post-2024 areas per area; weights fall to dw*occ/(m+b) (Tech Report s.3); Table 2 ICC splits the between-area and within-area variance. Central Valley wins because the 20-area supplement stratum has only 5 completes per area (34% of CV weight). Gates A-E pass.
- **Evidence:** All recomputed from the microdata.
  - Tables 1 and 2 reproduce: completes 700/2504/1210/1162/2516; answering 695/2476/1203/1153/2501; estimates 25.1/9.0/6.8/13.5/7.2; SE 4.56/1.01/0.68/1.40/0.78. ANOVA ICC from the microdata is 0.184/0/0/0.032/0.027.
  - Shares removed, ICC-split area-by-area projection: North 3.6 -> 4, CV 43.9 -> 44, Lakeshore 29.2 -> 29, SUP 13.9 -> 14, Metro 7.8 -> 8.
  - Robustness checks:

    | Variant | Rounded shares | Lakeshore per-area boost |
    |---|---|---|
    | Unrounded ICC | same | 27 |
    | Kish-deff x cluster-deff projection | same | 27 |
    | Stratum-specific variance components | same (CV 44.15) | 27 |
    | Lakeshore at 26 per area | 43.66-43.78, below the winner's 43.9-44.1 | n/a |
    | Lakeshore at 27 per area | 44.39-44.5, above the winner | n/a |

  - 2024 numbering: Northmark 2024 cases use old IDs before 22 April 2024 and new IDs from then. Old-only ID 2081 appears 19 April, new-only ID 5059 appears 22 April, and per-area takes become constant only with this cutover. A 1 April cutover drops 5 cases and distorts the regions. The result is 8101 completes in total.
  - 2024 restated, cut 22 April: North 702 / 24.4 / 3.98; CV 2506 / 8.6 / 1.09; Lakeshore 1207 / 8.2 / 0.84; SUP 1164 / 12.3 / 1.70; Metro 2522 / 8.9 / 0.75. This matches the author's block.
  - Surviving forks, none changing a graded figure except one:
    - North 2024 SE is 3.98 with restated regions as strata. A domain-in-old-strata reading gives 3.94. Tech Report s.4 files "five health regions" as strata, and only that convention reproduces Table 2's North 4.56 (the old-strata variant gives 4.54). Treated as closed.
    - The 22 April cutover and the Ostrander CVL-n / LKS-n -> 2000+n / 3000+n mapping are inferred, but the data fix each uniquely. Table 2 reproduces only with this mapping, and every Ostrander area hits its stratum take.
    - Wrong-basis routes: SRS sqrt(n/n') puts North first (39%). Region-level deff scaling puts Lakeshore first (29%) with CV at 18%. Pre-reorg area counts (Lakeshore 102) give a non-integer per-area boost. All are ruled out by the filed text, not by an unstated rule.
- **Files/Hygiene:** PASS. 11 files in 5 formats (csv x4, xlsx x2, txt x2, json, pdf x2); two files exceed 25k rows (the Northmark export has 39.7k). Distractors: the fieldwork quotes workbook and the pharmacy register. Both name vendors and costs, but neither decides the placement. Real-looking operational mess: mixed date formats (dd/mm/yyyy against ISO), two vendors' code frames, mid-wave renumbering, reissues. No authoring disclosures seen. No exclusion-level finding.
- **Stump power:** Strong. The tempting routes are SRS or region-level deff scaling off Table 2, or the "obvious" winner North (widest SE), and they land on North or Lakeshore. The route that gets Central Valley right needs the supplement stratum's 5-per-area take, the weight dilution under the boost, and the ICC-based variance split. A strong analyst with correct cleaning can still file Lakeshore at 29%. The 2024 cutover adds a second sub-step.
- **Stumping type:** `mechanism: method_or_model_selection` (variance projection under a design change), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. Table 2 and the published SEs are fine, and the difficulty is projecting design variance with weights and clustering rather than catching a wrong reported read.
- **Three rules:** `domain: pass`, `layers: pass` (L1: renumbered areas, two vendors with different code frames, reissues, the Northmark mid-wave ID cutover, pre/post-reorg regions; L2: ICC-based design-variance projection of a boost with weight reallocation), `decisive_step: analytical`. The field's own analysis is survey sample-design planning (deff, ICC, weight dilution). The easy route is Table 2's deff or SRS scaling, which gives Lakeshore (29%) or North (39%), not Central Valley (44%).
- **Fix:** none.

