# DA42 — Which tested effects an experimentation council classes as transferable to new markets, when some "complete" markets ran two versions

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Product Analytics · experimentation platform governance |
| Mirrors | Deciding which multi-market A/B results ship globally (experimentation platforms at Meta, Google and Amazon), when some markets' results mix two treatment versions after a mid-test change the completion flag does not show |
| Decision shape | A structure the body adopts: the partition of six tested effects into transferable and market-dependent, scored on whether each effect's prediction interval for a new market excludes zero under the council's pooling method |
| Committed call | Which of the six effects are transferable, with each one's prediction interval for a new market |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · the population a flag suggests (measured #5) gated by the council register's reproduction clause, with the market unit built from platform rows (S1) at rung 1 |
| Gate G mechanism | method_or_model_selection, with signal_vs_noise_or_hold support |
| Measured traps engaged | #5 takes the population a flag suggests · #1 reports a failed back-test, ships anyway · #2 counts file rows instead of the real unit |
| Calibration form | Published control set with a reproduction clause: the council register's pooled estimates, between-market spreads and prediction intervals for 18 past experiments |
| Driving force | Every market whose test ran to its planned end is flagged complete. The council pools only markets whose treatment version stayed constant through the market's exposure window, a rule that needs the release log's dated, market-scoped deployments joined against each market's window. The flag agrees for most markets, and disagrees exactly where a mid-test hotfix inflated one effect's markets and diluted another's. |

## 1. Situation

A consumer app's experimentation council decides which tested effects can ship to markets where they were never tested. Six effects ran
in 24 markets each, on three platforms. The governance standard lets an effect ship globally when its prediction interval for a new market
excludes zero, under the council's pooling method, and the register of past decisions publishes that method's outputs. The pack holds
results by market and platform with completion flags, experiment configurations with exposure windows, the release log, the register,
and the standard.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each market-platform estimate, each flag, each deployment record and each register entry. Nobody
  classifies the six effects and nothing reported is overturned. The difficulty is which markets belong in each pool.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the dashboard and both voices. Random-effects pooling over complete markets at the market grain still returns
  58 of 72 register figures and classes E1 and E3 as transferable.
* **Instrument repair.** Measure every market perfectly: a market that ran two versions still measured the mixture correctly. Which
  markets the pool admits is the council's rule, and it is pinned only by the register.
* **Lens swap.** The naive pool holds every complete market; the answer's pool drops the markets that changed version mid-test. Different
  markets in the pool, not the same markets reweighted.

## 3. The driving force

A strong solver skips the dashboard's averages, combines each market's platform rows into one estimate, as the standard's "each market is
one site" requires, and runs random-effects pooling with prediction intervals. It back-tests the register: 58 of 72 figures match. The 14
misses all sit in seven experiments that had a hotfix during the test. The release log records every deployment with its time and the
markets it reached, and the council pooled only markets whose treatment version held constant across their own exposure window. Effect
E1's hotfix shipped mid-test to six markets and lifted their estimates. Effect E2's reached five markets with a broken variant for a week
and pulled theirs down. Pooled on version-constant markets, E1's interval crosses zero and E2's clears it.

## 4. The ladder

| Rung | Construction | Adopts (transferable effects) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Mean of market effects with an interval from their spread | E1, E2, E3, E4, E5 | The dashboard's view, and five of six effects look positive almost everywhere | The register: simple averages return 12 of 72 published figures |
| 1 | Random-effects pooling over platform rows as sites | E1, E3, E4, E5 | The standard estimator on all the data | The standard: each market is one site; platform rows share a market's users and season |
| 2 | Random-effects pooling over complete markets, platform rows combined within each market | E1, E3 | Right unit, right estimator, and 58 of 72 register figures return | The register: all 14 misses are in the seven experiments with a hotfix during the test |
| 3 | **Decisive:** pooling over markets whose treatment version was constant through their exposure window (release log joined to each window) | **E2, E3** | — | — |

* **Structure shape.** Each rung adopts a different partition, and none before rung 3 contains E2 without E1.
* **Partial correction priced (L3).** A solver who drops version-changed markets but pools platform rows as sites adopts E2, E3 and E5,
  because platform-grain spreads stay too narrow. A solver who drops only the markets the results file marks with a declared-hotfix note
  misses four silent server-side changes and adopts E3 alone. Neither half lands on {E2, E3}.
* **Grid.** Estimator (mean or random effects) × unit (platform row or market) × pool (complete flag, declared notes, version-constant)
  = 12 cells. Eleven adopt a partition other than {E2, E3}, and the nearest misses it by one effect.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The standard says "each market is one site" and "the council's pooling method"; the register publishes outputs.
   No document says which markets a pool admits.
2. **Pattern B, a gate passed by one construction.** Version-constant pooling at the market grain returns 72 of 72 register figures. Complete
   markets at the market grain return 58, declared-note exclusion 64, platform rows 31 and simple means 12; every rival overstates the
   spread in the hotfixed experiments, so none ties in total. The pool is a construction: deployments filtered by market scope and time,
   compared against each market's exposure window.
3. **No arithmetic symptom.** Platform rows sum to market totals, assignment counts reconcile, and every hotfixed market's estimate is a
   valid, well-behaved number.
4. **Not a row predicate.** A market's admission depends on another file's dated events overlapping its own window.
5. **The enumeration is arithmetic.** No column marks a market as having run two versions.
6. **No cutover date.** Hotfixes fell on different dates in different experiments, and no series steps across markets.
7. **Survives deletion.** With every voice removed, market-grain pooling still returns 58 of 72 and adopts E1 and E3.

## 6. The calibration corpus

* **Form.** The council register: 18 past experiments, each with its pooled estimate, between-market spread and the two bounds of its
  prediction interval (72 figures), with that experiment's results, configurations and deployments.
* **What it certifies.** Random effects, the market unit and the interval form, which together return 58 figures.
* **What pins the pool.** The 14 figures only version-constant pooling returns.
* **Twin pair.** Register experiments X-09 and X-14 match on complete markets (22), mean effect, sample sizes and platform mix. Their
  published spreads are 0.06 and 0.12 (2.0×): X-09's two hotfixed markets were left out of its pool.
* **Resemblance points at the decoy.** By effect size and market count, E1 resembles the register's experiments that shipped.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The governance standard: an effect ships globally when its prediction interval for a new market excludes zero; each
  market is one site; a pooling method may be used for a shipping decision only if it reproduces every figure in the council register.
* **Empirical pins.** The pool's admission rule and the interval form, from the register.
* **Voices.** The growth product manager: "Five of six effects are positive in nearly every market; ship them." The experimentation
  analyst: "Platform rows are independent samples, so pooling them uses all the data."
* **Licensed wrong basis.** The standard records that the product council's dashboard averages market effects and will be on screen at the
  review.

## 8. Determinism by construction

* **Windows.** No deployment falls within 24 hours of a market's window boundary, so inclusive and exclusive comparisons agree.
* **Scope.** Every deployment record lists the markets it reached; none is global by default.
* **Interval.** The register's intervals use the random-effects spread and a t quantile with k − 2 degrees of freedom; other quantiles
  return at most 40 of 72.
* **Counts.** Every effect keeps at least 16 version-constant markets.

## 9. Prompt sketch and deliverables

> The council meets on Thursday to decide which of the six effects ship to markets we never tested in, and growth wants five of them out.
> Tell me which effects are transferable, scored on whether each one's prediction interval for a new market excludes zero, with the
> intervals, as the council's decision table. Send `transferability.xlsx`, a chart `prediction_intervals.png`, and a one-page
> `council_note.pdf`.

* `transferability.xlsx` — pooling for all six effects, the allocation-check sheet (ask A), the timing sheet (ask B) and the register
  table (ask C).
* `prediction_intervals.png` — each effect's pooled estimate with its prediction interval under the four rung constructions as a forest
  plot, zero marked, the hotfixed markets shown as hollow points, and the adopted partition labelled.
* `council_note.pdf` — the committed partition and why each rival pool fails the register.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 24 markets, the sample-ratio check p-value for the largest effect's test. *Device:*
  travellers appear in two markets' assignment logs with a home-market field, as the assignment guide documents; counting both rows
  produces false mismatches in five markets.
* **Ask B (device-carried).** For each effect, the median hours to first conversion in treatment. *Device:* event times are in the user's
  local clock and assignment times in UTC, as the event schema notes; mixing them shifts medians by up to nine hours.
* **Ask C (validity).** Register figures reproduced by each of the four constructions, and each effect's lower interval bound under each.
* **Decoupling.** Clearing the version-constant pool changes no figure in asks A or B.

## 11. Rubric arithmetic

24 markets (ask A) + 6 effects (ask B) + 4 reproduction counts and 6 × 4 lower bounds (ask C) + six classifications and two committed
intervals + 5 named chart parts + 3 files ≈ 74 criteria.

## 12. World-building constraints

* Hotfixes: E1 in 6 markets (estimates lifted), E2 in 5 markets (a broken variant for a week, estimates lowered); four silent
  server-side changes carry no declared note.
* Partitions: {E1–E5}, {E1, E3, E4, E5}, {E1, E3}, {E2, E3}; partial cells {E2, E3, E5} and {E3}.
* Register: 72 / 64 / 58 / 31 / 12 by construction. X-09 and X-14 match on every results column.
* Traveller rows and clock fields never touch a market estimate or a deployment.
