# task230: start here

| | |
|---|---|
| Task | task230 |
| Objective (Axis 1) | Data Quality Monitoring & Alerting |
| Block | task228 to task252 |
| Lane owner | developer 3 (current owner and status: the root `START_HERE.md` on main) |
| Seed | DQ03, `analytical_tasks/08_data_quality_monitoring/DQ03_whether-an-event-volume-drop-is-an-instrumentation-inci.md` |

## Before you build

1. This file is the seed, not the design. Build with `/build` (`build-pipeline`) from stage 0; the design goes in `DESIGN_NOTE.md`, and this file is not edited once the build starts.
2. Keep the objective and the number. If `guard.py` blocks the seed's driver or pairing, redraw inside the same objective and keep `task230`.
3. Seeds in folders 01 to 07 were written before the client's two-layer standard. Their calibration corpus, twin pair, licensed wrong basis, colleague voices and withheld rule are idea material, never a build plan. Re-root the stump as a Layer 2 analytical pitfall (`stumping` Part 2, `stumping/references/client/layer2-rigor-patterns.md`) and keep Layer 1 to realistic mess (`dataset-generation/references/layer1-messiness.md`). `official_decoy` and `validated_decoy` are blocked.
4. A seed that names a house domain gets the client domain it sits in on its card (`guide-to-prompt/references/domains/README.md`).
5. Branch under your prefix (`.claude/authors/`), `<prefix>/task230-<slug>`, and set the task's Status in the root `START_HERE.md` on main when you start and when you ship.

## Seed index fields

- **title:** Whether an event-volume drop is an instrumentation incident or a mix shift toward a new client version
- **objective:** Data Quality Monitoring & Alerting
- **domain:** product-analytics · metric-definition-measurement-science
- **committed_call:** Which of the monitored event streams get an instrumentation incident opened this week.
- **driving_force:** A topline events-per-user metric can fall while every client segment is flat, because the user mix moved toward a low-baseline client. Decompose into within-segment rate and composition before calling an instrumentation loss.
- **technique:** product-analytics/metric-definition-measurement-science/3

## Seed note

## DQ03, Whether an event-volume drop is an instrumentation incident or a mix shift toward a new client version

| Field | Value |
|---|---|
| Objective | Data Quality Monitoring & Alerting |
| Client domain / task type | `product-analytics` / `metric-definition-measurement-science` |
| Layer 2 pattern | `product-analytics/metric-definition-measurement-science/3` |
| Layer 2 family | `estimand_identification` |
| Committed call | Which of the monitored event streams get an instrumentation incident opened this week. |

### The pitfall

A topline events-per-user metric can fall while every client segment is flat, because the user mix moved toward a low-baseline client. Decompose into within-segment rate and composition before calling an instrumentation loss.

### The tempting shortcut

Read the topline drop as lost events and open the incident.

### What pins the rigorous method

Segment sizes and rates are filed for both periods, and the incident policy defines an instrumentation loss as a within-segment fall.

### Making it a monitoring task

The object under analysis is the health of the data or of the pipeline that delivers it, and the committed call is a monitoring or alerting decision (what fires, what is flagged, held, reissued or escalated), forward facing by default. If the prompt could be retagged Anomaly Detection, Descriptive or Forecasting without changing a word, the tag fails.

### Layer 1

Draw the data work from `.claude/skills/dataset-generation/references/layer1-messiness.md` (the universal techniques and the domain's own): the pipeline's deliveries, check results, incident register and alert routing beside what was published, every piece of mess something the real system would produce.
