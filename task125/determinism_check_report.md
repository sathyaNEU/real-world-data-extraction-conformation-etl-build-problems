# Determinism verdict, task125 (isolated judge; only target/ read)

**Verdict:** NOT_DETERMINISTIC (underspecified_objective / prompt_ambiguity on one clause; every graded figure otherwise reproduces).
**Disposition:** FIX_NOW. Pin the base quarter in one clause of the prompt (and, optionally, the flow denominator). No data or golden figure moves; no rerun needed beyond solvers reading the pinned text.

## Why
The prompt's only statement of the comparison sample is "from the latest quarter with all five waves' visit histories". Read literally, that is July to September 2026 (call records exist for all five intakes 2025Q3 to 2026Q3; also true of 2026Q1 and 2026Q2). The golden needs January to March 2026, the one quarter whose five intakes all carry SIX-visit histories. That reading is reached only by inferring that "visit histories" means uncapped histories. The base quarter moves the graded figures (below), so this is an open fork closed by inference.

## Evidence (all recomputed from target/)
Method used: interview visit = visit_no of the outcome-110 call (one per serial); join on serial[:9]; drop visit 4-6 households from the waves that capped intakes occupy; rake (IPF from weight 1, region and 7 age x sex controls) to convergence; gap = capped (trimmed) rate less full-sample rate. Raking from weight 1 reproduces the file weights (max abs diff 0.005) and published 5.4273/59.875 for 2026Q1; file weights give 5.589/58.879 (2026Q2), 5.862/58.539 (2026Q3).

| Item | Golden | Recomputed | Reproduced |
|---|---|---|---|
| UR gap AMJ26, JAS26, OND26, JFM27, AMJ27, JAS27 | .21,.39,.53,.62,.47,.28 | .213,.393,.532,.619,.473,.276 | yes |
| ER gap, same quarters | -.79,-1.42,-1.97,-2.44,-1.88,-1.19 | -.791,-1.420,-1.971,-2.442,-1.881,-1.191 | yes |
| UR rise AMJ-JAS 2026 / cap share / labour market | .27 / .18 / .09 | .2731 / .1798 / .0933 | yes |
| Six-visit UR 5.38, 5.47; ER 59.67, 59.96; ER published change -0.34, cap -0.63, LM +0.29 | as stated | 5.376, 5.469; 59.670, 59.959; -0.340, -0.63, +0.289 | yes |
| Wave sets 1; 1-2; 1-3; 1-4; 2-5; 3-5 and back to six from AMJ 2028 | as stated | FI-2026/04 (issued from 1 Apr 2026), prompt (six back 1 Apr 2027), methods note s.1 rotation | yes |
| Visits to JAS26 intake by region (VEL, CAR, PEL, HAS, TIR, DUN) | 3866, 2378, 1851, 1629, 1408, 1282 | same after dropping 381 duplicate uploads (serial+visit_no) | yes |
| Flow share (matched on serial[:9], sex, DOB) | 31.65 (75/237), 25.19 (34/135), 37.96 (52/137), 24.11 (27/112), 30.12 (25/83), 29.03 (27/93) | identical | yes |
| Employed weekly hours JAS26, 000 (CATI converted) | 26679.5, 16124.7, 12659.1, 10624.5, 9734.0, 7648.3 | identical | yes |

Robustness of the gap itself: re-raking to base-quarter controls vs target-quarter controls vs starting from file weights gives identical gaps to 3 dp, so no control/start-weight fork. Capped intakes' interview yield at visits 1-3 is unchanged (e.g. visit 1: 1917 in 2026Q1 vs 1856 and 1875 in 2026Q2/Q3; visit 2: 957 vs 952/983; visit 3: 517 vs 533/524), so the "remove late households, nothing else changes" counterfactual is supported by the data. Wrong paths in the golden text check out: weights kept without re-raking gives UR gaps .245,.453,.612,.722,.567,.337 and ER -1.22 ... -3.93 (overstated); constant wave-1 gap leaves 0.27 to the labour market.

### Fork 1 (FINDING, FIX_NOW): base quarter, "latest quarter with all five waves' visit histories"
Quoted clause executed word for word. Candidates and what each gives (UR gap JAS26, OND26, JFM27, AMJ27, JAS27):
- 2026Q1 (golden): .39 .53 .62 .47 .28
- 2025Q4 (waves 1-4 only have histories): .41 .53 .67 .39 .19
- 2026Q2 (wave 1 already capped, untrimmable): .15 .30 .42 .49 .29
- 2026Q3 (the literal "latest"; waves 1-2 already capped): .00 .14 .26 .36 .36
Only 2026Q1 can support a trim-the-late-visits counterfactual, and it is uniquely the quarter whose five intakes are all uncapped with histories (2025Q1 is the first call-record intake). But "latest" is then vacuous and the literal word picks 2026Q3, a base that returns a zero JAS26 gap. The clause lands on the graded path only after the solver infers "visit histories" = six-visit histories. Per the brief that is OPEN.
Direction clause: "published less six-visit" executes cleanly: UR gap positive (.39 ...), ER gap negative (-1.42 ...). No fork. The ER sign differs from UR only because late-visit households are mostly employed, which the data shows.
Does naming the base quarter hand over the analysis? No on balance. It files the WHAT (reference sample) that was genuinely ambiguous: the base choice moves figures by 0.02 to 0.5 point, far past rounding. It does not file the HOW: placing capped intakes by wave through the rotation, re-raking, and the change-in-gap attribution are untouched. Mild hint only: "all five waves" tells a solver that later waves matter, which weakens the wave-1-only trap a little. Prefer wording that names the quarter without the "all five waves" hint, e.g. "from January to March 2026, the last quarter fielded entirely under six visits".

### Fork 2 (FINDING, minor, FIX_NOW): flow denominator
Prompt: "the share of April to June unemployed respondents employed". Literal denominator is all April to June unemployed respondents: VEL 75/294 = 25.51, CAR 34/181 = 18.78, PEL 52/170 = 30.59, HAS 27/149 = 18.12, TIR 25/119 = 21.01, DUN 27/106 = 25.47. Golden uses only those re-interviewed (797 of 1019), which is methods note s.6 ("flows ... on the people interviewed in both ... unweighted"), but the prompt never says "flow" or "interviewed in both". Closed by the methods note only if the solver recognises the ask as a flow. Pin with "of those interviewed in both quarters". Matching key: serial[:9]+sex+DOB is the only stable identity (person_no matches 106 of 799 pairs with different DOB), so the key is closed by the data. Region identical across quarters (0 mismatches).

### Fork 3 (checked, NOT open): telephone hours
CATI actual_hours carry minutes only in .00/.15/.30/.45 (hh.mm); CAPI carry .00/.25/.50/.75 (decimal). Dictionary is silent. The release table (hls_release_tables_2026q2.xlsx, Table 1 "Total actual weekly hours (000)") settles it: converting CATI hh.mm to decimal hours and weighting reproduces the published total in ALL 14 quarters to 0.1 (e.g. 2026Q2: converted 83,589.1 = published 83,589.1; raw 83,305.1; 2026Q1: 85,326.1 vs raw 85,054.3; 2023Q1: 82,267.0 vs raw 82,005.6). The raw reading is contradicted by every published total, so the shipped files force the conversion. The two readings differ by about 0.3 per cent (VEL 26,679.5 converted vs 26,591.4 raw), which does matter to the graded cell, but it is reconcilable to a published number, not an inference. Judged closed. Advisory only: it remains a data-semantics ask (ask-level, allowed).

### Minor
- "how much ... is the labour market": unit not stated (point 0.09 vs 33 per cent of the rise). "Rates, gaps and shares to two decimals" points to points; low risk. Say "in points".
- Dedup of 381 double-uploaded JAS26 records and the 10-character serial are Layer-1 mess closed by methods note s.2 (visit = serial + visit number) and extract notes. Closed.
- LM share = six-visit change (5.47-5.38) follows from the prompt's own "six visits all along"; the cap being in AMJ26 already is a stated fact (FI-2026/04, extract notes, call records max 3 visits). Closed.

## Files/Hygiene: PASS
12 files; formats md, pdf (3), json, csv (3), parquet, xlsx (2) = 6 formats; person file 490,398 rows, call records 110,684. Distractors unused by the solution: jobseeker_support_claimants csv, field_staffing json, FI-2024-03 (superseded). Fictional Merrowland, dates consistent with 20 Oct 2026 extract, no authoring leakage seen in the text files. No exclusion-level finding.

## Stump power (Gate F)
Reasonable. Easy routes fail with specific wrong answers: treat the cap as a wave-1 effect (constant 0.21 gap, whole 0.27 to the labour market), carry the wave-1 difference into later waves (overstates), keep weights without re-raking (UR .245 ... .722, ER down to -3.93). Asks add independent traps (CATI hh.mm, 381 duplicate uploads, check digit, DOB matching). Expect top responses to lose on several asks.

## Stumping type (Gate G)
mechanism: decomposition_attribution (with a rotation-panel forecast of the gap path); stumping_family: analytical_non_defect; surface_read_dependency: no; sole_data_defect: no. Published rates are correct; the difficulty is attributing a correctly reported rise to cap vs market using the rotation structure. Clean-data test: still stumps.

## Three rules (Gate H)
domain: pass, layers: pass (Layer 1: duplicate uploads, 9/10-character serials, hh.mm telephone hours, rebased controls; Layer 2: panel-rotation counterfactual re-estimated with the raked estimator, change-in-gap attribution), decisive_step: analytical.
The field's own analysis (nonresponse/field-effort bias under a rotating panel, estimator re-run on a counterfactual sample) decides the answer; the easy route (wave-1 difference, or gap on kept weights) gives "the rise is real" or an overstated gap. Borderline note: the rotation and cap dates are stated, so placement could be read as rule application; the estimation (trim, re-rake, difference the gap) keeps it analytical.

## Fix
prompt: replace "from the latest quarter with all five waves' visit histories" with an explicit base (January to March 2026, last quarter fielded wholly under six visits); add "of those interviewed in both quarters" to the flow ask; say "in points" for the labour-market share. Input files and goldens unchanged.
