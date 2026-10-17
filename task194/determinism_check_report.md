# task194 determinism verdict

**Verdict:** NOT_DETERMINISTIC (competing_defensible_answer, with margin_or_boundary_fragility on the graded integers)
**Disposition:** SEND_BACK. The effect-pricing evidence (the seven closed placement quarters and the quarter before each) has to be re-cut with real sampling noise and a gap the candidate pricings can be separated on, and one sentence must fix the counterfactual. This changes what solvers see, so a rerun is required.
**Fix location:** input_files (series / placement-quarter rows), plus one charter or prompt sentence.

## Reproduction table
All recomputed from target/ with my own code (deduped, in-scope per spec 2.2/2.3, strata from hac_stratum_rates.csv).

| Item | Submission | Mine | Note |
|---|---|---|---|
| Unit-quarter series | ties row for row | 215/215 rows tie on observed; 214 tie on episodes; expected within 0.0006 | one row, 41310 2026-27 Q1, is 1 episode short (1,235 vs 1,236) if the data dictionary's dedupe key (patient, admission, DRG, no unit) is applied literally. The cross-unit pair 41350/41310 is the only acute pair. The shipped series and activity_summary_monthly keep both. |
| Eligible units | 12 | 12 (9 excluded: IP-01..IP-09 units) | row-set fork, see C3 |
| Orth ratio / planned expected / excess | 1.23 / 204 / 46.4 | 1.2277 / 203.86 / 46.41 | divisor is all-care-type separations (activity_summary_monthly). On in-scope episodes it is 218.9 / 49.8. Planned_separations says "all care types", so forced. |
| Alderbrook GM Dec-quarter excess | 36 | 36.35 | highest of all units |
| Stonecreek Vascular | worst ratio, 508 planned, 14.8 excess, avoids 6 | 1.292, 14.82, 5.64 | ok |
| Avoided, 12 units (share 0.3809 pooled) | 18,12,8,6,6,4,3,2,2,1,1,1 | 17.68, 11.66, 8.09, 6.08, 5.65, 3.64, 2.64, 2.13, 2.08, 1.32, 1.32, 0.63 | reproduces |
| Share that reproduces all 12 | | 0.3775 to 0.3985 | pooled 0.3809 sits 0.0034 above the floor |
| Hospital 2026 (episodes / compl. / rate) | A 38,249/4,017/109.0; S 23,179/2,525/112.2; M 19,733/2,016/110.3; C 2,340/234/111.6 | 38,249/4,017/109.006; 23,179 (23,178 if the cross-unit pair is collapsed)/2,525/112.224; 19,733/2,016/110.323; 2,340/234/111.640 | facility taken per unit-month from activity_summary_monthly |
| Sub-acute / MH by quarter (10 rows) | 901/50 ... 809/47 | identical | monthly summary equals the extract deduped on (patient, admission, DRG) exactly; raw rows are 10 to 12 percent higher |
| Complication groups (16 values) | G1 2,070/997 ... G8 1,058/478 | identical | any complication in the group, CIS units from hac_detail, non-CIS units from the first category, 2026 revision from 1 July 2026 (manifest) |

## The four questions

### 1. Method forced, or forced only by data that cannot separate the candidates?
Both failure sides appear, on different parts of the record.

**Pricing candidates the bundle leaves standing.** Let b be the unit's pre-arrival ratio, E the assessment-quarter expected and O the observed. For the seven closed placements (IP-01 has no data under 4.0), avoided = bE − O. Applied to the 12 units:

| Pricing | Orth | Gen Surg | Mar GM | top |
|---|---|---|---|---|
| A. share of own excess, pooled 0.381 (submission) | 17.7 | 11.7 | 8.1 | Orth |
| A, share mean / median / LS | 17.7 / 17.9 / 17.7 | 11.7 / 11.8 / 11.7 | 8.1 / 8.2 / 8.1 | Orth |
| A, baseline = previous quarter | 18.0 | 11.9 | 8.2 | Orth |
| A, baseline = closed at decision date (8-week rule) | 17.6 | 11.6 | 8.0 | Orth |
| A, baseline = all other quarters (share 0.320) | 14.8 | 9.8 | 6.8 | Orth |
| A, baseline = last 4 pre quarters (0.339) | 15.7 | 10.4 | 7.2 | Orth |
| B. constant ratio-point drop (0.081 per expected) | 16.6 | 22.7 | 7.5 | **Gen Surg** |
| C. constant percent of counterfactual (7.0 percent) | 17.6 | 21.8 | 8.0 | **Gen Surg** |
| D. constant complications (8.5 per quarter) | 8.5 | 8.5 | 8.5 | no ranking |

**Fork.** Pricing B or C moves the recommendation to Alderbrook General Surgery. Their gap over Orth is 6.2 and 4.2 complications.

**What separates A from B and C.** On the printed numbers the register is not ambiguous. The avoided/excess share has CV 5 percent (0.34 to 0.40). Avoided per unit of expected has CV 53 percent. corr(avoided, excess) = 0.992, corr(avoided, E) = −0.28. Read as exact, A wins by a wide margin.

**Does the record's noise match the process it claims?**
- Ordinary unit-quarters (placement quarters removed): pooled chi-square 198.5 on 185 df, 1.07 per df, p = 0.24. These are plausibly Poisson.
- Placement quarters: the seven shares around the pooled share have Poisson-scaled chi-square **0.006 on 6 df** (cdf about 5e-9). The Poisson sd of one share is 0.35 to 1.0, but the observed spread is 0.02. Each assessment-quarter O equals E·(b − 0.381·(b − 1)) to within 0.1 to 0.8 of a complication.
- The quarter before each placement also sits on the earlier-quarters mean: ratios of 1.277 vs 1.273, 1.373 vs 1.370, 1.286 vs 1.276, 1.083 vs 1.085, 1.192 vs 1.185, 1.512 vs 1.508, 1.166 vs 1.162. Chi-square is 0.014 on 7 df against an expected sd of about 0.08. Those quarters are not sampled either.

**Which side?** The design sits on the first side for the evidence that carries the pricing (candidates agree, or are cleanly separated, only because the placement quarters have no sampling noise). On honest Poisson error it falls on the second side:

| Model | chi-square on 6 df |
|---|---|
| A | 0.007 |
| B | 1.19 |
| C | 0.80 |
| D | 0.38 |

The likelihood ratio of A over B is exp(1.18/2) = 1.8 to 1. The pooled share's Poisson SE is ±0.20 (95 percent interval −0.01 to 0.77).

**Rounding claims more precision than the data carries.** The Orth − General Surgery gap of 6 has an honest SE of about 4.5. That comes from ±0.20 on the share times 15.8 for the excess difference, plus Poisson error on the two units' 10-quarter ratios (excess 46.4 ± 5.6 and 30.6 ± 6.5). Under A the ranking does not depend on the share. It rests only on the excess difference of 15.8 ± 8.6, about 1.8 sigma. The graded whole numbers (18, 12, 8, ...) are exact only on the noise-free register.

**Window (P1).**
- Spec 3.3/3.4 fix "specification period to date" for the ratio and the per-separation expected. So the window is closed.
- If the last 4, 6 or 8 quarters were used (not licensed), Orth stays first (17.3, 16.6, 16.9). The 12 figures move: General Surgery 6.9, 8.8 or 11.8, and the gap 10.4, 7.8 or 5.1. The 4-quarter window also moves Orth to 17.
- Recommendation: does not move.

### 2. Graded figures off the rounding edge?
No. Several are within 0.2 of an edge.

**Avoided counts, at the pooled share 0.3809.** Distance is to the nearest .5.
- Orth 17.68, 0.18 from 17.5.
- General Surgery 11.66, 0.16.
- Stonecreek Vascular 5.65, 0.15.
- Alderbrook Respiratory 3.64, 0.14.
- Marrowfield Surgical 2.64, 0.14.
- Stonecreek Renal 0.63, 0.13.
- Share-of-excess window 0.3775 to 0.3985 for all 12; the pooled share is 0.0034 above the floor.

**Effect of one more episode.**
- One additional complication in any one of the seven placement quarters lowers the pooled share by 0.0065. That puts it below 0.3775. Orth becomes 17.4, Vascular 5.5 or below, Respiratory 3.5 or below, Surgical Services 2.5 or below, Renal 0.5 or below.
- Taking the baseline "closed at decision date" gives share 0.3790 and Orth 17.59. Taking "all other quarters" gives 14.8 and breaks eight of twelve figures.

**Hospital-year adjusted rates** (edge distance, then one-complication sensitivity):

| Hospital | Rate | Distance to edge | One complication |
|---|---|---|---|
| Alderbrook | 109.006 | 0.044 (1.6 complications) | ±0.027 |
| Stonecreek | 112.227 (112.224 if the pair is not collapsed) | 0.023 to 0.026 (0.5 complication, to 112.25) | one more gives 112.27, which rounds to 112.3 |
| Marrowfield | 110.323 | 0.027 (0.49 complication, to 110.35) | one more gives 110.378, which rounds to 110.4 |
| **Carrowdean** | 111.640 | **0.0099** (to 111.65) | ±0.477 |

For Carrowdean, an expected total lower by 0.017 flips it to 111.7. That is the removal of one low-stratum episode (rate 0.027), or of any episode with rate above 0.017 in the H4 set. One more complication gives 112.1.

**Hospital rate definition.** Spec 3.2 defines the adjusted rate for a unit only. Pooled O/E × 96.5 follows 3.1 ("group of episodes"). The episode-weighted mean of unit rates gives 108.6, 111.8, 109.7 and 111.7 instead, and the unweighted mean gives 110.2, 112.8, 113.2 and 111.6. Pooled is the licensed reading but is inferred.

### 3. Does any shipped file rank or score the candidates on the question?
No. Nothing prices the avoided complications and nothing ranks the units on that question.
- quality_dashboard_2026q2.xlsx is a one-quarter position table in hospital order, with a note saying it is not a projection. It shows Marrowfield Orthopaedics at 138.0, the highest among the 12, but ranks nothing.
- unit_indicator_series.csv carries ratios and rates by unit-quarter, with no ordering.
- The hygiene, nursing and experience files are unit-level colour.

Gate G (file) is clear. No quote.

### 4. Is the counterfactual branch recoverable without unlicensed inference?
Not by a literal reader.

**Shipped text for each branch.**
- Charter 4.3: avoided = "the complications the unit would have recorded over the assessment quarter without the embedded team, less the complications it records over that quarter with the team there".
- 4.4: assessed on planned separations.
- Spec 3.4: planned separations × expected-per-separation over the specification period gives the expected complications.
- Spec 3.3: the specification-period ratio is the unit's standing.
- 4.1: the placement is decided "on the indicator data closed at the time".

**"Without" branch.** No sentence equates it with standing × expected. That identity, with standing taken from the pre-arrival record, appears only in the write-up (step 6: "against what its unit stood at over its own closed quarters before the team arrived"). Competing counterfactuals are all compatible with 4.3:
- expected alone (ratio 1);
- the whole-period ratio;
- the previous quarter;
- the closed-at-decision record.
The first two give different shares (above).

**"With" branch.** For the future quarter it is not observable. Nothing says a placement removes a fixed share of the excess. That follows only from the pattern in the register.

**Net.** A literal reader can execute the filed expected (3.4) and the filed standing (3.3). The effect model, and so the "with" branch, has to be inferred from seven quarters whose only support is the noise-free fit above. By the standing rule this is an open fork.

## Other probes

**P2.** The files leave several readings standing: A (mean, median, pooled, LS), B, C, D, and four baselines. Under A the ranking never moves (Orth 1st, General Surgery 2nd). Under B or C the call flips to General Surgery. The graded integers move under every baseline other than "before arrival": All other quarters moves eight of twelve; the last-4 baseline moves Orth to 16, General Surgery to 10, and so on. The files do not force one reading by text. The numbers force it only by the zero-noise fit.

**P3.**
- Hospital figures: forced by facility per unit-month (activity_summary_monthly) and spec 2.2/2.3. Two soft spots:
  - Stonecreek episodes are 23,179 if the cross-unit pair 41350/41310 is two separations (as monthly summary reports), or 23,178 if the data dictionary's dedupe key (no unit) is applied literally. The rate is 112.2 either way.
  - Pooled versus mean-of-unit-rates is the definitional choice noted above.
- Sub-acute / MH by quarter: forced. activity_summary_monthly (separations, episodes_with_complication) equals the extract deduped on patient, admission, DRG exactly. Raw rows would give 1,005 / 56 and so on.
- Group counts: forced given three things.
  - Revision date. The manifest says the 2026 list is in force from 1 July 2026, and HAC13 ends 30 Jun 2026.
  - Detail from hac_detail_extract for CIS units, first category from the episode table otherwise (manifest "omits" column and the register flag).
  - Any-complication-in-group. A first-category-only count would give G1 1,618 / 814 and similar.
  Alternatives not licensed: a 1 Jan 2026 switch gives G1 1,895 / 814, and no switch gives 2,156 / 814.

**Row set (C3).** The prompt asks for "a row for each eligible unit". Charter 4.2 as written includes 41511 and 41512 (acute inpatient, 5 closed quarters, not placed). They are excluded only by inference (closed 30 Sep 2025, no planned separations). Without that inference the file has 14 rows. IP-01's unit 41360 is excluded by a boundary reading of "previous twelve closed quarters" (assessment quarter 2023-24 Q4 is the 12th back). Under a start-date reading of "three years" it would be eligible: 13 rows, avoided 7.0. Neither changes the recommendation.

**Other.** Planned separations are "all care types" and the all-care-type divisor is licensed. The 5-quarter history of 41510 under clause 3.6 is fine.

## Gate lines

**Gate G line.**
- mechanism: method_or_model_selection (effect pricing for a forward quarter), with a forecasting element.
- stumping_family: analytical_non_defect; surface_read_dependency: no; sole_data_defect: no.
- No shipped number is wrong, and deleting the dashboard and the series' wrong-looking readings leaves the pricing step standing.
- It is not a lens swap in the banned sense. But under A the winner is decided by planned excess (standing × planned activity), and the share only scales it, so the difficulty reduces to a one-parameter calibration. The register's role is to separate A from B and C, and it does so only through zero-noise data.

**Gate H line.**
- domain: pass. Indirect standardisation against published stratum rates, and pricing an intervention from closed placements, are what a hospital quality unit estimates. Swapping in "school" and "visits" does not make the call sentence read the same.
- layers: pass. Layer 1 is the 2022/2026 list revision, the 41511/41512 amalgamation, site realignments, sub-acute duplicates and uncoded comorbidity. Layer 2 is pricing avoidable excess on planned activity rather than total or current excess.
- decisive_step: analytical. A strong analyst who read everything would file Alderbrook General Medicine (36 above expectation), Stonecreek Vascular (worst ratio), Alderbrook General Surgery (largest forecast complications) or pricing B or C (General Surgery).
- Caveat: the intended regression-to-the-mean contrast ("not the quarter the placement was decided on") does not discriminate in this data. The decision quarter equals the earlier mean to ±0.01, so that route gives identical graded integers (shares 0.388 vs 0.381).

## Gates in order
- **H:** passes (domain used, two layers, analytical step) but see the caveat above.
- **G:** passes.
- **A:** passes. All 12 + 16 + 10 + 4 graded groups reproduce, as does the main list. Step 1 "ties row for row" holds only if the dedupe key includes unit.
- **B:** passes. All decisive facts are shipped (manifest gives the revision date). The counterfactual identity and the effect model are not stated.
- **C:** **FAILS.** Competing defensible pricing (B, C) flips the call, separated from A by a noise-free fit (chi-square 0.006 on 6 df) that real sampling would not produce. Several graded integers sit 0.13 to 0.18 from the edge, and the hospital rate for Carrowdean 0.01. The row set can be 12, 13 or 14.
- **D:** the difficulty is analytical, but it depends on the A-vs-B fork.
- **E:** the prompt does not pin the counterfactual or the eligible-row set; both rest on inference.
- **F:** the trap that would catch strong models is "rank by Dec-quarter excess or by worst ratio". That works. The pricing step (A vs B/C) catches models for a reason the files do not settle by text.

## Stump power
The Dec-quarter position and the worst-ratio unit are plausible lures and a strong model would likely avoid them by applying 3.3/3.4. Pricing B or C is the realistic wrong turn and is statistically as good as A on the stated noise. The failure there is a semantic lottery on the counterfactual, not a clean analytical miss.

## Fix
1. Re-cut the seven placement quarters and the quarters before them with Poisson sampling noise, and size the effect and the spread of pre-ratios so that A is separated from B and C by well more than their sampling error (at least 4 or 5 degrees of discrimination at chi-square 1 per df), or file the effect model in the charter (e.g. "the team is assessed against the unit's ratio over its closed quarters before arrival; the effect scales with the unit's excess").
2. File one sentence for the counterfactual: "without the team" = planned expected × the unit's ratio over the specification period to date, and the "with" branch's baseline window.
3. Pin the eligible set (closed units, the twelve-quarter anchor) and the dedupe key (include or exclude unit).
4. Move the share or the hospital denominators off their rounding edges. Carrowdean is within 0.01 of 111.65.
