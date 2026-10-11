# Two-layer task design (the client's standard)

Real data work first, then the analytical step that decides the answer. Every task is built and reviewed against this.

Every task has two layers. **Layer 1 (data messiness)** is the data work: real data that has to be parsed, joined, reshaped and reconciled before any analysis can start. **Layer 2 (stumping strategies)** is the analysis: the methodological step that decides the recommendation. A strong task needs both, and Layer 2 is what decides it.

## Why the standard changed

The tasks are training data. A task is useful only if getting it right teaches a model something it does not already know. Hundreds of accepted tasks teach the same few lessons: back out an unstated rule from certified figures, catch a planted copied block, ignore the staff draft. A model learns each of those after a few examples. Analytical and methodological rigour does not saturate the same way, because every field has many distinct ways to get the analysis wrong.

## Layer 1: realistic data work

The data is hard to use for the reasons real data is hard to use. The solver has to put it in order before the analysis can start, which costs time and care but does not hide the answer. Field-specific techniques are in `../../../dataset-generation/references/layer1-messiness.md`.

- **Native formats.** Multi-sheet workbooks with header blocks and footnotes, files whose layout changes across years, tables inside PDFs, codebooks that must be applied, wide releases that must be reshaped.
- **Imperfect joins.** Codes against names, identifiers that change between systems, crosswalks between vintages and classification revisions, many-to-many links that need a stated rule.
- **Genuine overlap.** Two extracts covering overlapping periods, a revised release superseding a preliminary one, one entity under several spellings, resubmitted records.
- **Units, time and scale.** Fiscal and calendar years, local time and UTC, nominal and real values, rates on different bases.
- **Real coverage gaps.** Suppressed cells, survey skip codes, partial years, entities that enter and exit.

**Messy is not planted.** If you would never see it in the real source, and it exists only so that catching it decides the answer, it is a planted defect, not Layer 1: a copied or backfilled block, a swapped or reversed series, a hidden year-to-date column, a decoy memo or staff draft written to carry the wrong answer, a stakeholder figure that is wrong only so the task can overturn it.

## Layer 2: the analysis decides

The recommendation turns on doing the analysis correctly. The failure being built on is the natural mistake of a capable analyst who takes the obvious route, not a hidden trick. Five families, each the `layer2_family` key on a fingerprint card:

- **Estimand and identification** (`estimand_identification`): the right counterfactual, staggered adoption, contamination and spillover, regression to the mean, selection on the outcome, Simpson's paradox across strata.
- **Estimation that fits the data** (`estimation_fit`): censoring and truncation, interval-censored or rounded values, survivorship, small-sample bias, clustered errors, weighting and post-stratification, ratio of totals against mean of ratios, chain-linked aggregation, decomposition.
- **Forecasting and uncertainty** (`forecast_uncertainty`): backtests without leakage, conformal or bootstrap intervals, simultaneous against pointwise bounds, model choice on out-of-sample error.
- **Allocation under real constraints** (`allocation_constraints`): fixed-point allocations, max-min choices, capacity and queueing, the order in which a rule applies caps and tests.
- **The field's own method done right** (`field_method`): credibility weighting, development triangles, exposure windows, survey construction from microdata, market definition, intention to treat.

Every domain in `layer2-rigor-patterns.md` lists twenty rigor patterns grouped by task type. Use them to see what a methodological pitfall looks like in that field, then build your own version.

## Keeping the answer deterministic without a plant

A rigour-led task still has exactly one defensible answer. What pins it is the question and the stated standard, not a planted clue.

- **Define the estimand precisely** in the prompt or a supplied standard: population, outcome, window, unit and comparison.
- **Let the design imply the method.** A randomised design means an intention-to-treat difference on the randomised unit. A staggered rollout means comparisons against units not yet treated. Censored durations mean a survival estimate at the stated day.
- **Rule out reasonable alternatives with the data's own structure**, not with a decoy document that argues for the wrong one.
- **Do not pin the method by replaying certified figures.** Leaving the method unstated and shipping published or certified figures that only one reading reproduces was the most common pin in accepted tasks. It is saturated and capped at review. State the method or the standard, and let the analysis be the hard part.

## The six-point check before a build ships

1. The inputs take real work to put in order, and none of that work is a planted defect.
2. The step that flips the recommendation is a methodological choice, not catching something planted.
3. The prompt or a supplied standard defines what to measure precisely enough that only one method is defensible.
4. There is no decoy memo, staff draft or briefing written to carry the wrong answer.
5. The method is not hidden and then recovered by reproducing certified or published figures.
6. The lesson a model learns from getting it right is not one an earlier task already teaches.
