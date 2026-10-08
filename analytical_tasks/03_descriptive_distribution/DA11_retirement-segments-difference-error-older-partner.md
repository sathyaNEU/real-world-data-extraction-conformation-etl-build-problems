# DA11 — The segment structure a retirement-products committee adopts, when adjacent age groups look the same one interval at a time and differ as a difference

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Economics · household finance and retirement-product design |
| Mirrors | Deciding how many tiers to build from survey or model-imputed estimates, where adjacent tiers' estimates share sampling and imputation draws (audience tiers on imputed income at Meta and Google, CRM revenue tiers from enrichment models, household accounts placed by the primary holder when the product keys on another member) |
| Decision shape | A structure the body adopts: which adjacent age groups share a product segment, scored by the committee's rule on whether their median net worth differs by more than 1.96 standard errors of the difference |
| Committed call | The segments (runs of adjacent age groups) and each segment's median net worth to the nearest $1,000 |
| Gap · Pattern | Gap 3 (objective) over Gap 2 (population) · E22, the deciding comparison (the difference's own error) against its components read one at a time, with E29 (households placed by the older partner, through the full data) below it and a control set blind to covariance (L1) |
| Gate G mechanism | signal_vs_noise_or_hold, with method_or_model_selection |
| Measured traps engaged | #20 leaves the deciding comparison unstated · #6 treats a mixed segment all one way · #12 stops at the first control that passes · #15 follows the requester's hunch over the rule |
| Calibration form | Published control set with a reproduction clause: the official bulletin's 2022 medians and standard errors by age group (12 cells), which the research memo makes the condition of any method used |
| Driving force | Each group's median carries a standard error from 999 replicate weights and five implicates, and those errors are not independent between neighbours. The same strata drive both groups in every replicate, and the same imputation draws move both groups' business and housing wealth in every implicate. The error of a difference computed within each replicate and implicate is a third to a half smaller than √(SE₁² + SE₂²). The bulletin publishes no difference, so the control set certifies every per-group figure and is blind to the comparison that decides. |

## 1. Situation

A life insurer's retirement-products committee is setting its 2027 range: one product per segment, each segment a run of adjacent age
groups (under 35, 35–44, 45–54, 55–64, 65–74, 75 and over). Its rule keeps two adjacent groups apart when the difference of their median
net worth exceeds 1.96 standard errors of that difference. The product brief places each household by the age of its older partner,
because the annuity's start is keyed to the older partner. The pack holds the national household-wealth survey's summary extract (five
implicates per family), the full public data, the 999 replicate-weight file, the variance guide, the official bulletin's published 2022
tables and the research memo. The committee meets on 27 January.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the extract, the implicates, the replicate weights and the bulletin's published medians and errors.
  The survey's reference-person grouping is a correct convention, and nobody's reading of their own numbers is overturned. The difficulty
  is the error of a comparison the bulletin never prints, for a grouping it does not use.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the actuary's and the product director's views and the partner's licensed basis. Per-group medians and errors
  still reproduce the bulletin exactly, and overlapping intervals still look like the same market.
* **Instrument repair.** Remove imputation altogether and the sampling covariance between neighbouring groups (shared strata and
  replicates) still halves several differences' errors. Regrouping by the older partner survives any instrument, because the survey's
  reference person is fixed by design.
* **Lens swap.** The two reads are about different populations. Bulletin groups place 1,140 couples by a reference person who is the
  younger partner, and the product's groups place them by the older one.

## 3. The driving force

A strong solver averages the five implicates' weighted medians, takes sampling variance from the replicate weights and adds 6/5 of the
between-implicate variance. It reproduces all twelve bulletin cells to the dollar, regroups households by the older partner's age as the
brief requires, then tests each adjacent pair with the textbook error of a difference, √(SE₁² + SE₂²). Two pairs fall just short and merge,
and the actuary's overlapping intervals agree. But the two medians are not independent estimates. In every one of the 999 replicates the
same strata are dropped from both groups, and in every implicate the same draws of business and housing wealth move both. The
difference's own error, computed by taking the difference inside each replicate and each implicate and then combining, is 0.50 and
0.61 of the textbook figure for those two pairs. Both clear 1.96. The bulletin, the only control, publishes groups and never differences,
so nothing a solver checks contains a covariance.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Five implicates stacked as 5× the families, weighted medians, simple-random-sample errors, bulletin groups | Six segments, every group its own (tiny errors split every pair) | Every row used, the weights applied, the medians close to the bulletin | The reproduction clause: stacked errors miss all 6 of the bulletin's published errors by 55% to 70% |
| 1 | Implicate-averaged medians, replicate and imputation variance per group (12 of 12 bulletin cells), √(SE₁² + SE₂²) on bulletin groups | Three segments: under 35 / 35–54 / 55 and over | The certified method, reproducing every published cell | The product brief places each household by its older partner, and 1,140 couples' older partner is not the reference person |
| 2 | Same per-group method on older-partner groups (age from the full data's partner record), √(SE₁² + SE₂²) | Two segments: under 35 / 35 and over | The certified method on the product's own population | The replicate file: neighbouring groups' replicate medians move together (correlation 0.55 to 0.72), so √(SE₁² + SE₂²) overstates every difference's error |
| 3 | **Decisive:** each adjacent difference computed inside every replicate and implicate, its error combined from those, on older-partner groups | **Four segments: under 35 / 35–44 / 45–64 / 65 and over** | — | — |

* **Structure shape.** Each rung adopts a different structure: six, three, two and four segments. The two cuts the answer adds (35–44
  against 45–54, and 55–64 against 65–74) appear only when the comparison's own error is used on the product's groups. Segment medians
  are $41,000 / $153,000 / $252,000 / $386,000.
* **Partial correction priced (L3).** A solver who computes differences within implicates but takes their sampling error by
  √(SE₁² + SE₂²), or within replicates but adds the two groups' imputation variances separately, captures half of the covariance. Its
  test statistics for the two decisive pairs land at 1.81 and 1.69, both short of 1.96, so it adopts rung 2's two segments.
* **Grid.** Grouping (bulletin or older partner) × error (stacked, per-group textbook or the difference's own) gives 6 cells and 6
  different structures. Bulletin groups with the difference's own error give five segments (cuts at 35, 45, 55 and 65).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The committee's rule names "the standard error of the difference". The variance guide shows how to get a
   statistic's error from replicates and implicates. No document applies it to a difference, or warns that groups' errors covary.
2. **Corpus blind for a computable reason.** *Every published bulletin cell is a single group's statistic, so the covariance between
   groups enters none of the twelve controls.* Per-group reproduction is exact under rungs 1 to 3 alike.
3. **No arithmetic symptom.** Medians, errors, weights and implicate counts all reconcile, and the textbook formula gives sensible, positive
   errors that look conservative.
4. **Not a row predicate.** The decisive quantity is a variance of a difference across 999 replicates and five implicates, a construction
   over the whole design.
5. **The enumeration is arithmetic.** Which pairs separate follows from ten combined variances (five pairs, sampling and imputation parts),
   computed rather than read.
6. **No cutover date.** One survey wave, and nothing steps.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, the textbook formula is still what most analysts write.

## 6. The calibration corpus

* **Form.** The official bulletin's 2022 tables: the median net worth and its standard error for each of the six age groups, on the
  survey's reference-person convention, reproduced by the research memo's clause as the gate for any method.
* **What it pins.** The per-group method: implicate-averaged weighted medians, sampling variance from the 999 replicates on the first
  implicate with the guide's multiplicity factor, and imputation variance at 6/5 of the between-implicate spread. Stacking misses all six
  errors, and averaging-without-imputation-variance misses four.
* **What it is blind to.** Covariance between groups (above).
* **Twin pair.** Pairs 35–44 against 45–54 and 45–54 against 55–64, on older-partner groups, are identical on everything the textbook
  formula sees: a difference of $68,000 and component errors whose root-sum-square is $45,300 (z = 1.50 for both). Their own errors are
  $22,600 and $45,300 (2.0×), giving z = 3.0 and 1.5. Only the within-replicate, within-implicate difference separates them.
* **Resemblance points at the decoy.** The bulletin's own age chart draws each group's 95% interval side by side, and on it the
  neighbours of 35–44 and of 55–64 overlap, the picture the overlap reading takes as "no difference".

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The committee's rule: "Two adjacent age groups are separate segments when the difference of their median net worth
  exceeds 1.96 standard errors of the difference; otherwise they share a segment." The product brief: "A household is placed by the age of
  its older partner." The research memo: "Any method used must reproduce each of the bulletin's 2022 medians and standard errors by age
  group." The memo also fixes the weighted-median definition.
* **Empirical pins.** The per-group method, from the bulletin.
* **Voices.** The appointed actuary: "If two groups' confidence intervals overlap, they are the same market." The product director: "The
  bulletin's age groups are the industry standard; segment on them as published."
* **Licensed wrong basis.** The memo records that the distribution partner segments by overlap of the bulletin's 95% intervals and will
  present its own structure to the committee.

## 8. Determinism by construction

* **Margins on the test.** Under the correct method every pair's statistic sits at least 0.30 from 1.96 (6.8, 3.0, 1.5, 2.3, 0.8). Under
  the textbook method they sit at 4.9, 1.50, 1.50, 1.40 and 0.60.
* **Older partner.** Every couple has both ages recorded in the full data, and no couple is split by a same-age tie.
* **Replicate count.** Using all 999 replicates or the guide's first 200 moves no statistic by more than 0.05.
* **Segment medians.** Pooled across implicates with the memo's percentile definition. None lies within $500 of a rounding boundary.

## 9. Prompt sketch and deliverables

> Before the committee fixes next year's product range on 27 January, I need the segment structure: which age groups get a product of
> their own and which share one, under our separation rule. The actuary believes overlapping intervals mean the same market. Give me the
> segments and each segment's median net worth to the nearest thousand dollars, as the table the committee adopts, and send
> `segment_build.xlsx` with the sheets below, plus `pair_tests.png`.

* `segment_build.xlsx` — the per-group estimates reproducing the bulletin, the older-partner regrouping, for each adjacent pair the
  difference with its own standard error and the textbook error (ask C), the persistency sheet (ask A) and the premium sheet (ask B).
* `pair_tests.png` — each adjacent pair's difference as a point with two error bars (its own error and √(SE₁² + SE₂²)), the 1.96
  threshold drawn as a band, the adopted cuts marked, and the twin pairs annotated.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** 13-month persistency of the insurer's four existing retirement products for each quarterly issue
  cohort of 2025. *Device:* a policyholder switching products is recorded as a lapse of the old policy and a new issue linked by a
  conversion number, as the policy-administration guide documents. Counting conversions as lapses understates persistency by 3 to 9 points
  in 11 of 16 cells.
* **Ask B (device-carried).** Average annualised premium per new policy by distribution channel (four channels) in 2023, 2024 and 2025.
  *Device:* the premium field holds the modal premium for the policy's payment frequency, as the data dictionary states. Treating it as
  annual understates monthly and quarterly payers by factors of 12 and 4.
* **Ask C (validity).** For each of the five adjacent pairs on older-partner groups, the difference of medians, its own standard error and
  √(SE₁² + SE₂²).
* **Decoupling.** The policy-administration system shares no row with the survey. Clearing the within-replicate difference changes no
  figure in asks A or B.

## 11. Rubric arithmetic

4 products × 4 cohorts (ask A) + 4 channels × 3 years (ask B) + 5 pairs × 3 figures (ask C) + the four segments and their four medians + 4
named chart parts + 2 files ≈ 57 criteria.

## 12. World-building constraints

* Older-partner group medians ($ thousands): 41 / 153 / 221 / 289 / 370 / 410. Differences are 112, 68, 68, 81 and 40. Textbook errors
  are 22.9, 45.3, 45.3, 57.9 and 66.7. Own errors are 16.5, 22.6, 45.3, 35.2 and 50.0.
* 1,140 couples have an older partner who is not the reference person. Bulletin groups give the three-segment rung-1 structure under the
  textbook error and five segments under the difference's own error.
* Stacking shrinks every error by more than half and splits all five pairs.
* The bulletin's twelve cells reproduce exactly under the per-group method. Replicate correlations between neighbouring groups run 0.55 to
  0.72.
* The policy-administration system touches no survey row.
