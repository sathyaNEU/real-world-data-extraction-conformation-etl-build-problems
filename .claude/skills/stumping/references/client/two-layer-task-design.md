# Two-layer task design (the client's standard)

Real data work first, then the analytical step that decides the answer. Every task is built and reviewed against this.

## The three rules

Every task is built and reviewed against three rules. They exist for one reason: tasks are training data, and a task is only useful if getting it right teaches a model something real.

1. **The task must really use its domain**, not just borrow its vocabulary.
2. **Every task has two layers**: realistic messy data, and real analytical rigour that decides the answer.
3. **Planted traps, data semantics and rule application can appear in a task, but none of them can be the decisive stump.**

### Rule 1: the task uses its domain

Every task is assigned a domain and a secondary domain. The task does the kind of analysis that domain is about, close to one of its task types (`../../../guide-to-prompt/references/domains/README.md`). The domain cannot be just the setting or backdrop for a generic question. The client keeps two example prompts for every task type on its taxonomy page.

**The quick test:** swap the nouns to another field ("hospital" for "school", "megawatt-hours" for "visits"). If the task reads exactly the same, the domain is only a backdrop.

| | Prompt | Why |
|---|---|---|
| Good | Quantitative Finance, alpha research: decide whether to allocate capital to a sentiment signal with a strong backtest, using a cost-adjusted, factor-neutral Sharpe ratio over 2015 to 2024, measured point in time. | Validating a return signal is the core work of alpha research. |
| Bad | Energy Systems & Utilities as a backdrop: which three substations get the upgrade grant, ranked by the score in the grant rules? | The answer comes from applying a stated score; swap in schools and it reads the same. |
| Good | Biomedical & Clinical Research, survival analysis: decide whether the new maintenance regimen lengthens time to relapse, measured from randomisation to relapse, with patients who leave the study treated as censored. | Time-to-event analysis with censoring is the core work of survival analysis. |
| Bad | Epidemiology & Public Health as a backdrop: which clinics qualify for the outreach fund under the eligibility criteria? | Checking criteria against a list; no risk, rate comparison or outbreak signal decides the answer. |

A decision framing such as "which clinics" is fine. What matters is whether the quantity that decides it is something the field would estimate, model or test.

### Rule 3: three kinds of stump are banned as the decisive step

These can appear in a task, because real tasks always involve some field reading and rule following, but none of them can be what decides the answer. Something genuinely analytical must still stand between the solver and the right answer. A task decided by one of these is sent back, even if it is deterministic and correct.

1. **Planted defects, decoys and hidden rules**: something inserted only so that catching it flips the answer. A block of hourly readings secretly copied from the week before, so finding the copy is what changes the ranking. A staff memo written to argue for the wrong answer, where rejecting the memo is what decides the call.
2. **Data semantics**: the answer flips only on reading a field, code, unit or definition correctly. The answer flips only once you notice the school capacity column also counts preschool seats, or once you read that a rainfall column holds multi-day totals, not daily values.
3. **Rule application**: the answer comes from applying stated rules correctly, however many steps there are. Ranking programmes by checking six listed eligibility criteria and applying a stated score. Working out which company held a licence on a given date by following the transfer records.

**The test.** Could a strong analyst who cleaned the data and read every rule correctly still get the answer wrong by doing the analysis the easy way? If yes, the stump is analytical and valid. If no, it is semantics or rule application. Choosing the right estimand or unit of analysis counts as analysis.

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

The client's own examples: files whose layout changes across years, or tables inside PDFs that must be extracted; joins across sources with imperfect keys, like codes in one file and names in another; a preliminary release and a revised release that overlap, so you must decide which to use; fiscal and calendar years mixed, local time and UTC mixed, or values in thousands in one file and units in another. Layer 1 complicates the problem and can help stump the model, but it is never the decisive step (rule 3).

**Messy is not planted.** If you would never see it in the real source, and it exists only so that catching it decides the answer, it is a planted defect, not Layer 1: a copied or backfilled block, a swapped or reversed series, a hidden year-to-date column, a decoy memo or staff draft written to carry the wrong answer, a stakeholder figure that is wrong only so the task can overturn it.

## Layer 2: the analysis decides

The recommendation turns on doing the analysis correctly. The failure being built on is the natural mistake of a capable analyst who takes the obvious route, not a hidden trick. Five families, each the `layer2_family` key on a fingerprint card:

- **Estimand and identification** (`estimand_identification`): the right counterfactual, staggered adoption, contamination and spillover, regression to the mean, selection on the outcome, Simpson's paradox across strata.
- **Estimation that fits the data** (`estimation_fit`): censoring and truncation, interval-censored or rounded values, survivorship, small-sample bias, clustered errors, weighting and post-stratification, ratio of totals against mean of ratios, chain-linked aggregation, decomposition.
- **Forecasting and uncertainty** (`forecast_uncertainty`): backtests without leakage, conformal or bootstrap intervals, simultaneous against pointwise bounds, model choice on out-of-sample error.
- **Allocation under real constraints** (`allocation_constraints`): fixed-point allocations, max-min choices, capacity and queueing, the order in which a rule applies caps and tests.
- **The field's own method done right** (`field_method`): credibility weighting, development triangles, exposure windows, survey construction from microdata, market definition, intention to treat.

The client's own examples of the kind of choice an expert recognises: comparing against the right group (in a staggered rollout, each wave against units not yet treated, not a simple before and after); handling the data's real structure (time to an event with people who left the study early treated as censored); judging the evidence (a guardrail metric read with its confidence interval, not only "it was not significant"); validating a forecast properly (testing it only on data it was not built on).

Every client domain but three (Physical & Environmental Sciences, Energy Systems & Utilities, Human Factors & Ergonomics) has its rigor patterns in `layer2-rigor-patterns.md`, grouped by task type. Use them to see what a methodological pitfall looks like in that field, then build your own version: a card's method is the textbook route a strong solver takes, so the stump is the judgment the method takes for granted and the data settle (`../../SKILL.md` 1.3), and the card's pin is filed as the estimand and the design, never as a sentence naming the method.

## Keeping the answer deterministic without a plant

A rigour-led task still has exactly one defensible answer. What pins it is the question and the stated standard, not a planted clue.

- **Define the estimand precisely** in the prompt or a supplied standard: population, outcome, window, unit and comparison.
- **Let the design imply the method.** A randomised design means an intention-to-treat difference on the randomised unit. A staggered rollout means comparisons against units not yet treated. Censored durations mean a survival estimate at the stated day.
- **Rule out reasonable alternatives with the data's own structure**, not with a decoy document that argues for the wrong one.
- **Do not pin the method by replaying certified figures.** Leaving the method unstated and shipping published or certified figures that only one reading reproduces was the most common pin in accepted tasks. It is saturated and capped at review. State the method or the standard, and let the analysis be the hard part.

## The check before a build ships

Answer every point in one line in the design note.

1. The task does its domain's own analysis, close to one of the domain's task types, and the swap test breaks it: with another field's nouns in, the task no longer reads the same.
2. The inputs take real work to put in order, and none of that work is a planted defect.
3. The step that flips the recommendation is a methodological choice, not catching something planted, not reading a field, code, unit or definition correctly, and not applying stated rules.
4. The analyst test holds: a strong analyst who cleaned the data and read every rule correctly still gets the answer wrong by doing the analysis the easy way, and the design note names that route and its wrong answer.
5. The prompt or a supplied standard defines what to measure precisely enough that only one method is defensible.
6. There is no decoy memo, staff draft or briefing written to carry the wrong answer.
7. The method is not hidden and then recovered by reproducing certified or published figures.
8. The lesson a model learns from getting it right is not one an earlier task already teaches.
