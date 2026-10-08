# Prompt shapes, the picker

**A prompt shape is named for where its many rubric criteria come from.** A task ships one to
three deliverables with uncapped but multi-dimensional asks, which is a small, honest prompt, so
the generated rubric's 25-criteria floor cannot be reached by stacking asks. It has to come from the **structure of the answer**. A ranked list under a cap
grades every candidate's score. A forecast across many periods grades every period. A grid grades
every cell. Pick the shape whose structure your data and your decision already have, and the
criteria fall out of it.

**Read this file to choose, then load exactly one shape file.** Each shape file carries what the
shape is, where its criteria come from, how to size it past 25, what makes it hard rather than
merely long, and four worked prompts from the client's library.

> **Then read [`../prompt-voice.md`](../prompt-voice.md), which is where the prompt actually gets
> written.** The shape decides where the criteria come from. The voice file decides what the
> request sounds like, and that is a batch-level gate: 17 of 18 consecutive prompts of ours
> opened in first person with a role verb in clause one, 12 of them with the
> literal words "I run", and 18 of 18 shipped a PDF. The 72 worked prompts below vary their
> openings much more than we have, and reading four of them in one sitting is exactly when the
> single voice gets picked up.

**The eighteen are ideas, not a menu.** They are patterns that have been seen to carry a rich
rubric. If your data and decision suggest a different structure that earns the criteria honestly,
use it, and write the criteria arithmetic into the design note the way these files do. Treat the
eighteen as inspiration and the arithmetic as the discipline.

---

## The index

| # | Shape | The criteria come from | Canonical Axis 1 objective | Files |
|---|---|---|---|---|
| [01](01-ranked-list-under-a-cap.md) | Ranked list under a cap | Every candidate's score, the in-or-out call, the first one below the line | Descriptive & Distribution | 2 |
| [02](02-forecast-across-many-periods.md) | Forecast across many periods | Every period's forecast value | **Forecasting & Predictive Modeling** | 2 |
| [03](03-bridge-between-two-totals.md) | Bridge between two totals | Each reconciling item on the walk, on both sides | Data Extraction & Conformation (ETL) | 2 |
| [04](04-setting-one-dial.md) | Setting one dial | The outcome at every allowed setting | Descriptive & Distribution | 2 |
| [05](05-allocation-to-a-fixed-total.md) | Allocation to a fixed total | Each bucket's amount and what it buys | Descriptive & Distribution | 2 |
| [06](06-sequenced-schedule-under-capacity.md) | Sequenced schedule under capacity | Each item's finish period, the running total per period | Descriptive & Distribution | 2 |
| [07](07-grid-of-cells.md) | Grid of cells | Every cell in the grid | **Experiment & Causal Analysis** | 2 |
| [08](08-rule-replayed-on-history.md) | Rule replayed on history | Each period's four outcome cells against its ceiling | Descriptive & Distribution | 2 |
| [09](09-funnel-or-chain-of-stages.md) | Funnel or chain of stages | Each stage's volume, rate and unit cost | Descriptive & Distribution | 2 |
| [10](10-scorecard-against-thresholds.md) | Scorecard against thresholds | Each metric-against-threshold check per segment | Descriptive & Distribution | **1** |
| [11](11-before-and-after-with-a-control.md) | Before and after with a control | Each unit's two effects and its pre-period check | **Experiment & Causal Analysis** | 2 |
| [12](12-drill-down-to-one-leaf.md) | Drill-down to one leaf | The piece of the movement at each drill level | **Root-Cause Analysis** | 2 |
| [13](13-scenarios-and-the-flip-point.md) | Scenarios and the flip point | Each scenario cell, the earliest failure, the flip point | **Forecasting & Predictive Modeling** | 2 |
| [14](14-cuts-of-a-distribution.md) | Cuts of a distribution | Each percentile cut in each segment | Descriptive & Distribution | 2 |
| [15](15-fields-conformed-to-one-schema.md) | Fields conformed to one schema | Each target field, on its source and its transformation | Data Extraction & Conformation (ETL) | 2 |
| [16](16-indicators-into-one-score.md) | Indicators into one score | Each indicator as it enters the index | Descriptive & Distribution | 2 |
| [17](17-periods-around-a-change-point.md) | Periods around a change point | Each observed period around the change | **Anomaly Detection & Diagnostics** | **1** |
| [18](18-hypotheses-versus-evidence.md) | Hypotheses versus evidence | Each cause-against-evidence cell | **Root-Cause Analysis** | 2 |

## About that objective column

**The shape does not fix the tag.** The objective comes from what the analyst has to
*produce*, decided in step 2 of the skill, and reading it off this table instead is how a build
gets mistagged. The column says which of our **eight** canonical labels the shape most naturally
carries, and several shapes carry two depending on how the decision is cut, which each shape file
spells out. No shape defaults to Opportunity Sizing & Decision Support or to Data Quality
Monitoring & Alerting, so for those two the tag comes from the objective's discriminating test in
`../SKILL.md` Step 2, never from this column.

The client's own page tags many of these examples "Opportunity Sizing & Decision
Support", which is one of our eight objectives
(`../objectives/opportunity-sizing-decision-support.md`), and two "Comparative analysis and
explanation", which **is not a valid Axis 1 label here**: a task tagged outside the eight is
rejected on the tag alone. The page labels are not carried on the imported examples, so the shape
files do not mark which ones the client tagged Opportunity Sizing.

**Two drifts to watch when you pick.**

1. **Nine of the eighteen default to Descriptive & Distribution Analysis**, so a batch that picks
   shapes without checking the tag drifts there and the clone check reads a repeated driver.
   Before drawing, run `python3 .claude/skills/fingerprint/guard.py recent` and check what the
   last few builds were tagged.
2. **Forecasting & Predictive Modeling is the most wanted objective and the
   tiebreak.** Shapes 02 and 13 carry it natively, and 04 and 06 carry it whenever the bar has to
   be cleared over a window that has not closed or the banked total rests on a rate the history
   pins down. Prefer those when two pairings are otherwise equal.

## The criteria arithmetic, at a glance

Size the shape on paper before you draw a single file. Every shape file carries its own version
of this, and the pattern is always the same: **one repeated structural unit, times the number of
times it repeats, plus the decision furniture.**

| Structural unit | Times | Gives |
|---|---|---|
| Candidate, period, bucket, item, stage, cell, field, indicator, tract | 10 to 20 | 10 to 20 |
| A second figure on the same unit (its rank, its gate verdict, its scaling range, its cost) | same | doubles it |
| The committed call, the runner-up, the gap, the flip threshold | once each | 3 to 4 |
| The chart with its parts named (series, ordering, labelled threshold line at its value, annotation, title stating the finding) | once | 5 to 7 |
| The deliverables themselves, present and named | 1 to 3 | 1 to 3 |

If the arithmetic lands under 25 the fix is a **denser structure**, more units or a second figure
on each unit, never more asks bolted on the side. If it lands well over 25 that is fine, there is
no ceiling.

## Two things the shape does not give you

**A shape is not a mechanism, and it is not a stump.** The shape decides where the criteria come
from. `../../../stumping/SKILL.md` decides why the task is hard, and the bar requires at least
one model genuinely stumped. Every shape file has a "what makes it hard rather
than long" section, and that section is the seam where the shape meets the ladder: a shape worked
without it is a wide, easy task that the whole field answers, which fails the average bar from the
other direction.

**Reusing a shape is legitimate; reusing the driver is a clone.** Two builds can both be a ranked
list under a cap. They cannot both turn on the same insight, the same decisive rung or the same
calibration form. `../../clone-check/SKILL.md` carries the discrimination, and the pre-flight is
run while the draw is fixed and the data is not yet cut.

## The rule that governs every prompt in these files

**Never copy any example into a build. Not the scenario, not the entity, not the metric, not the
file names, not the wording of a single ask.** They exist to show what a task in a shape can be
about and how a finished prompt reads. Read a few, then draw a fresh domain, subdomain, entity,
metric and decision through the anti-clone draw in `../../../stumping/SKILL.md` Part 6. A build
that lifts any scenario, wording or file name is a clone and the review reads it as one.

What transfers is the **shape**, and only the shape.
