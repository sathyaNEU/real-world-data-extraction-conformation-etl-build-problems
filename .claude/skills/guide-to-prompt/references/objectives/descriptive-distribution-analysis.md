# Descriptive & Distribution Analysis

**Axis 1 analytical objective.** Canonical label, do not rename it and do not invent new ones.

> The decision turns on how a population is composed or how a metric is distributed, not on why it moved.

## Where the examples live

The worked prompts for this objective are filed by **prompt shape** in `../shapes/`, written in
the current format: prose, first person, one committed call, one to three named files, and the
generated rubric's 25 criteria coming from the structure of the answer rather than from a list of
asks.

**Shapes that carry this objective.** **14 Cuts of a distribution** is the native shape, and eight more default here under our roster: **01 Ranked list under a cap**, **04 Setting one dial**, **05 Allocation to a fixed total**, **06 Sequenced schedule under capacity**, **08 Rule replayed on history**, **09 Funnel or chain of stages**, **10 Scorecard against thresholds** and **16 Indicators into one score**.

Nine of the eighteen shapes land here, which is a clone risk: run `python3 .claude/skills/fingerprint/guard.py recent` for what the last few builds were tagged before you draw, and reach for Forecasting where the evidence pins a future value.

## The rule for reading them

**Never copy any example into a build. Not the scenario, not the entity, not the metric, not the
file names, not the wording of a single ask.** The examples show what a task in this objective can
be about and how a finished prompt reads. What every example shares, and what you take from it, is
the **shape of the decision**: a stakeholder with one call to make, a forcing event, and evidence
that pins exactly one answer down. Then draw a fresh domain, subdomain, entity and decision of your
own, and run it through the fingerprint guard (`../../../fingerprint/SKILL.md`) and the anti-clone
draw in `../../../stumping/SKILL.md` Part 6.1 before the ladder is written. A build that lifts any
scenario, wording or file name from the library is a clone, and the review reads it as one.
