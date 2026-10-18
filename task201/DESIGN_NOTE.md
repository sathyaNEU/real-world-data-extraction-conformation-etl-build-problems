# task201 design note

Biomedical & clinical research, `genomics-gwas-high-dimensional-association`, Anomaly Detection &
Diagnostics (task180 to task227, oviya13ya). Seed AD24 supplies the decision shape only, one scarce
investigation to one of N candidates.

**No architecture is drawn and no card is registered.** The first candidate was screened to death before
any design, which is the intended use of the four checks. The measurements are below.

## Tried and rejected

### Candidate 1, separating confounding inflation from polygenic signal, killed at the draw (2026-10-18)

**The dichotomy, run first.** The filed quantity is each contributing cohort's **confounding inflation**,
the expected chi-square where polygenic signal is absent, in dimensionless inflation units to two
decimals. It is **unobserved**: the record carries test statistics that are the sum of confounding,
polygenic signal and sampling noise, and the decomposition is printed nowhere. So this is branch A, where
two estimators of one quantity can stand, and the rest of the screen applies.

**The world and the two routes.** A consortium meta-analysis with seven contributing cohorts; which cohort
gets the one re-genotyping and QC pass before the meta-analysis freezes. The easy route is the genomic
inflation factor, which the field has used as a convention for thirty years and which equals
`intercept + slope x median(LD score)`, so the cohort with the most power looks the most confounded. The
decisive route is the regression of chi-square on LD score, whose intercept is the confounding and whose
slope is the polygenic signal, which the field has an actual estimator for rather than a convention.

**The non-invariance profile (1.2b), profiled over the intercept with the slope free, against a printed
precision of 0.01.**

| LD score range | bottom-LD bin names | intercept set within 2 log-lik units | width against printed 0.01 |
|---|---|---|---|
| 1 to 300 | **the golden cohort** | [1.1167, 1.1371] | 0.0204, **2x** |
| 8 to 120 | **the golden cohort** | [1.1110, 1.1431] | 0.0321, **3x** |
| 25 to 80 | **the golden cohort** | [1.1011, 1.1594] | 0.0583, **6x** |
| 35 to 70 | the loud cohort (lands wrong) | [1.0831, 1.1794] | 0.0962, **10x** |

The self-measurement **is** non-invariant, which is why the profile is bounded at all rather than flat like
task200's dark figure. But it is nowhere tight enough: even at its sharpest the set is twice the printed
precision, so the intercept cannot be graded to two decimals at any setting.

**The sixth screen, and the enumerated sweep in full.** Nine ways the pack measures a cohort's confounding
inflation, at the realistic LD range where identification is sharpest. **Three reach the golden besides the
decisive route**, and all three are the same move: read the region where the signal is absent.

| Route | Names | Verdict |
|---|---|---|
| 1 genomic inflation factor, median chi-square (easy route) | loud | lands wrong |
| 2 mean chi-square over all variants | loud | lands wrong |
| 3 LD score regression intercept (decisive) | golden | the golden route |
| 4 mean chi-square in the bottom 5 per cent of LD score | **golden** | **reaches it** |
| 5 mean chi-square in the bottom quintile of LD score | **golden** | **reaches it** |
| 6 inflation factor on the lowest-LD decile only | **golden** | **reaches it** |
| 7 inflation factor after dropping the top 5 per cent of statistics | loud | lands wrong |
| 8 lambda rescaled | loud | lands wrong |
| 9 twice the mean of the lower half of the statistics | loud | lands wrong |

**Why there is no window, and the rule it earns.** One dial controls both failures. The LD score range is
simultaneously the leverage that identifies the intercept and the distance between the low-LD region and
the bulk. Widen it and the regression pins the intercept while the low end becomes a clean null that
publishes it; narrow it and the low end is contaminated enough to land wrong while the regression loses
the leverage and the profile balloons to ten times the printed precision. Measured at four ranges, there is
no setting where the profile is usable and the null region is not readable.

**The rule, which closes a family rather than a build.** An identification of the form *estimate the
nuisance where the signal vanishes* fails the sixth screen by construction: the region where the signal
vanishes is a subset that publishes the nuisance, and the leverage that makes the identification sharp is
exactly what makes that subset pure. This is task198 architecture 4's "censoring is revelation" with a null
region in place of a censored one, and it closes every regression-on-a-covariate identification whose
nuisance is the intercept: LD score regression, negative-control regions, calibration nulls, blank-sample
baselines. Price it with one computation before drawing: compute the nuisance from the lowest bin of the
covariate alone and see which candidate it names.

### Candidate 2, fine-mapping which variant in a locus is causal, killed at the draw (2026-10-18)

**The data-native sentence, written first as instructed, and writing it is what exposed the problem.** The
decisive step cannot be "do fine-mapping", because a lead variant not being the causal one is the first
thing any geneticist knows. So the sentence has to name what the standard pipeline gets wrong here, and
attempting it raises a structural question: **under the standard single-causal-variant model the causal
variant has the largest expected z, because its LD with itself is 1.** So the lead can differ from the
causal variant in only three ways, and each was measured.

| Branch | Premise holds? | Condition 2, sixth screen | Condition 1, family on the name |
|---|---|---|---|
| A equal power, one causal variant | **no**: lead by z is the causal variant | **lead by p-value and largest absolute effect both reach it** | closed: all 4 methods x 4 priors name it |
| B the causal variant poorly imputed | yes, lead 5 against causal 7 | **worst imputation quality reaches it**, one column sorted | **open: 2 names.** ABF, sum-of-single-effects and stepwise name 5; stochastic search names 7 |
| C two causal variants in the locus | yes, lead 9 against causal 7 | none reaches it | **open: 2 names.** Three methods name 9, stochastic search names 23, none names 7 |

**Each branch dies, and on a different one of the three tests.**

- **A dies on the reflex sweep.** The family is closed exactly where there is no stump: the answer is the
  lead variant, so one column sorted gives it and the standard pipeline applied competently reaches the
  golden. The coordinator's rule applies in full, the stump is spent whatever the screens say.
- **B dies twice.** The family is open on the graded name, three of four licensed methods naming the wrong
  variant, which is the one-computation death condition 1 was set to catch. And `argmin(INFO)` publishes
  the answer, which is architecture 4's shape with an imputation column in place of a censored set.
- **C dies on condition 1, and more deeply on the graded object.** With several causal variants the records
  fix a **set**, not a name, so which element is called "the" answer is arbitrary; no method named the one
  designated and the three that agreed agreed on a tagger.

**The rule it earns, and it is the sixth time one number has sat on both sides today.** The perturbation
that separates the lead variant from the causal one is the perturbation the licensed methods disagree
about, because that is what the methods differ in handling: attenuation in branch B, multiplicity in
branch C. With equal power and one causal variant every method agrees and the answer is the lead. **So the
method family closes only when the answer is trivial, and any departure that moves the answer off the lead
is a departure that opens the family.** There is no fourth way for the lead to differ from the causal
variant, so fine-mapping cannot carry a records-fixed named answer with a closed family on this ground.

**Branch C's second finding is worth keeping separately**, because it is about the graded object rather
than the method: where the well-posed answer to "which one" is a set, a build that grades a name is
grading an arbitrary element of it, and no amount of margin fixes that.
