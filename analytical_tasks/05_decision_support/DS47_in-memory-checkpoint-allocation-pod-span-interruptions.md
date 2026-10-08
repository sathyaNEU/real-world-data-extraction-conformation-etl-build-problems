# DS47 — Which training programmes get next quarter's in-memory checkpointing, when a job's interruptions come with every pod it spans

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Product Analytics · ML training platform reliability |
| Mirrors | Allocating failure-recovery capacity on per-unit failure rates that hide a per-domain component (in-memory checkpointing and hot spares for large training runs at AI labs and cloud providers, replica placement across racks and availability zones, carrier capacity priced on per-parcel loss rates that hide per-hub incidents) |
| Decision shape | An allocation under a cap: in-memory checkpointing next quarter for training programmes totalling at most 4,096 GPUs, among six programmes |
| Committed call | The programmes covered, and the GPU-hours the allocation saves next quarter, in thousands |
| Gap · Pattern | Gap 1 (time) over Gap 2 (population) · E12, a correct rate carried onto a different book (interruptions per GPU-hour are correct for last quarter's placements, but each job also takes a fabric term once for every pod it spans, and next quarter's plan spreads one programme across six pods a job), with the population a flag suggests (E33) at rung 1 |
| Gate G mechanism | forecasting, with decomposition_attribution |
| Measured traps engaged | #13 validates on one population, applies to another · #5 takes the population a flag or filter suggests · #7 uses the ready-made measure |
| Calibration form | Existing-book actuals: last quarter's job book, every job with its GPUs, its pods from the placement log, its hours and every termination joined to the node and fabric health events before it |
| Driving force | Every interruption idles a whole job, so the feature is worth most where big jobs are interrupted often. Interruptions come from two sources: a node failing, at a rate per GPU-hour, and a pod's fabric failing, which stops every job with GPUs in that pod however few it has there. Last quarter's rates per GPU-hour are exact for last quarter's placements. Next quarter the scheduler spreads the RL programme's 256-GPU jobs across six pods each, and its interruptions rise 4.7× while its GPU-hours do not move. |

## 1. Situation

An AI lab's training platform will offer in-memory checkpointing next quarter: snapshots to peer hosts every ten minutes and restarts in
four minutes, against hourly disk checkpoints and 38-minute restarts today. Spare host memory limits it to programmes totalling 4,096
GPUs. Six programmes have applied (P1–P6), and the capacity policy funds programmes in order of GPU-hours saved per GPU covered until
the 4,096 are used. The reliability dashboard counts interruptions by programme, and the sweep programme tops it every week.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the incident log, the scheduler's termination records, the health events, the placement log, the
  job book and next quarter's capacity and placement plans. No stakeholder read is overturned: the sweep programme really does log the
  most incidents, and the large pretraining jobs really are the most expensive to interrupt. The difficulty is how often each programme's
  jobs will be interrupted next quarter.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the dashboard and every voice. Each programme's own interruption rate per GPU-hour, carried onto next
  quarter's plan, still covers P1, P2 and P6.
* **Instrument repair.** Give the platform a perfect record of every interruption and its cause. Last quarter's rates become exact and
  still describe last quarter's placements; P3's jobs have not yet run across six pods, so no record of the past shows the rate they will
  have.
* **Lens swap.** The naive read and the answer differ in moment and unit: last quarter's book at a rate per GPU-hour, against next
  quarter's placement, where a fabric term is paid once per pod a job spans.

## 3. The driving force

A strong solver ignores the dashboard's incident counts, builds interruptions as the SLO defines them, from scheduler terminations joined
to the health events before them, and values the feature for each programme as interruptions per job-hour × 59 minutes saved × the job's
GPUs. It carries each programme's own rate per GPU-hour onto next quarter's plan, which is exact for last quarter: the rates reproduce every
programme's count. That covers P1, P2 and P6, the programmes with the largest jobs. But the rates differ 3.2× between programmes for a
reason the job book shows when jobs are compared: a pod's fabric fails about once every 574 pod-hours and stops every job with GPUs in it,
so a job's rate is a node term per GPU-hour plus a fabric term per pod spanned. The two terms reproduce every programme and every job.
Last quarter P3 ran each 256-GPU job in one pod. Next quarter's placement plan fills fragments for it, six pods a job, and its interruptions
go from 21 to 97 while its GPU-hours stay the same. Per GPU covered, P3 is worth 2.3× P6.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The reliability dashboard: last quarter's interruption counts by programme, covering the most-interrupted first | P4, P5 and P1; 34 thousand GPU-hours (−74%) | The platform's own weekly view, and the sweeps lead it by 7× | The capacity policy: the feature goes by GPU-hours saved per GPU covered next quarter, not by past incidents |
| 1 | Each programme's interruptions per job-hour from the incident log's infrastructure category, × 59 minutes × job GPUs, on next quarter's plan | P1, P4 and P2; 37 thousand (−71%) | Forward-looking and valued as the policy asks, on the platform's own incident categories | The SLO: an unplanned interruption is a termination with a node or fabric health event in the five minutes before it. Joined, 156 flagged terminations were graceful pre-emptions, and 152 fabric stops sit under "application" as collective timeouts |
| 2 | SLO interruptions, pooled into one rate per GPU-hour across last quarter's book, on next quarter's plan | P1, P2 and P6; 160 thousand (+24%) | The right population, and the rate reproduces the cluster's 188 interruptions | The job book: rates per GPU-hour differ 3.2× between programmes (one per 107,500 GPU-hours on the large jobs, one per 33,700 on the 64-GPU sweeps), so the pooled rate reproduces no programme |
| 3 | **Decisive:** the two-term law that reproduces every programme and every job, a node term per GPU-hour plus a fabric term per pod spanned, applied to next quarter's placement plan | **P1, P3 and P2; 129 thousand GPU-hours** (P3 4th of six on rung 0) | — | — |

* **Figure shape.** Rungs 0 to 2 walk the saving up from 34 to 160 thousand; the decisive move reverses it to 129. Every other cell sits at
  least 10.8% away.
* **Position table.** P3, the programme that enters only at rung 3, is 4th on rung 0, 6th on rung 1 and 4th on rung 2. P6, covered at rung
  2, leaves; P4 and P5, covered at rungs 0 and 1, leave. Rung margins per GPU covered: P1 over P4 1.23× at rung 1, P1 over P2 2.0× at rung
  2, P1 over P3 1.72× at rung 3, and at the cut P2 over P6 2.0×.
* **Discriminator dominance.** P6 carries a 2.0× advantage per GPU over P3 into rung 3 (14.2 against 7.1 GPU-hours). Under the two-term law
  on the plan P3 is worth 23.8 and P6 10.2: P3 keeps 3.34× its rung-2 figure and P6 0.72×, an edge of 4.66 against the required
  1.2 × 2.0 = 2.4, past the 3.12 that headroom asks.
* **Partial correction priced (L3).** No half-applied law covers P3. Carrying each programme's own rate per GPU-hour onto the plan, which is
  the two-term law at last quarter's placements, covers P1, P2 and P6 for 115 thousand (−10.8%), P6 2.0× ahead of P3 per GPU. Charging the
  fabric term once per job instead of once per pod spanned covers the same three for 46 thousand (−64%), P6 1.27× ahead.
* **Grid.** Population (incident category, SLO join) × rate (pooled per GPU-hour, per programme, two-term law on the plan) = 6 cells. The
  incident category covers P1, P4 and P2 under the first two rates, and its two-term fit returns a negative node rate, because
  pre-emptions crowd the small-job programmes. Under the SLO population only the two-term law on the plan covers P1, P2 and P3, at 129
  thousand; the nearest other figure is 115 thousand (−10.8%), per-programme rates, which equal the law at last quarter's placements.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The SLO defines an interruption; the placement plan lists pods; the fabric runbook says a pod's switches can drop
   collectives. No document says interruptions scale with pods spanned, or that P3's new placement multiplies its exposure.
2. **The book pins the law, as a construction.** The two terms reproduce all six programmes' counts and 211 of 211 jobs within one
   interruption. One rate per GPU-hour reproduces the cluster total and no programme; per-programme rates reproduce each programme and miss
   every job whose placement changed during the quarter. The fabric term exists in no column: it needs the placement log's pod list per
   job joined to fabric events per pod.
3. **No arithmetic symptom.** Terminations reconcile to the scheduler, health events to the telemetry, GPU-hours to the capacity plan,
   and every rung's allocation fits under 4,096 GPUs.
4. **Not a row predicate.** A job's exposure is a sum over the pods it spans of pod-hours times the fabric rate, plus its GPU-hours times the
   node rate, and the value multiplies by the GPUs each interruption idles.
5. **The enumeration is arithmetic.** No column holds a fabric exposure or a forward interruption count.
6. **No cutover date.** Next quarter's placement is a plan, and nothing in the book steps; the law is fitted across jobs, not across time.
7. **Survives deletion.** No wrong number exists to delete. Without the dashboard or any voice, per-programme rates still cover P6.

## 6. The calibration corpus

* **Form.** Last quarter's job book: 211 jobs with their programme, GPUs, pods (from the placement log), hours and terminations, each
  termination joined to the node and fabric health events in the five minutes before it, and the incident log's category for each.
* **What it certifies.** The SLO population (188 unplanned interruptions; the incident category totals 195 with a different make-up) and
  the two-term law: one node interruption per 402,000 GPU-hours and one fabric stop per 574 pod-hours.
* **Twin pair.** Two 512-GPU ad hoc jobs are identical on every job-book column but placement: same model, same hours, same checkpoint
  size and priority. One ran in two pods and was interrupted 10 times; the other, moved after a pod's maintenance, ran across five pods and
  was interrupted 21 times (2.1×). Only the placement-log join separates them.
* **Resemblance points at the decoy.** By GPUs per job and hours, P6 most resembles the programme that gained most from the feature in
  its pilot on the sister cluster.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The capacity policy: the feature covers programmes totalling at most 4,096 GPUs, funded in order of GPU-hours saved per
  GPU covered; a programme that does not fit is skipped. The SLO's definition of an unplanned interruption. The feature's specification:
  ten-minute snapshots and four-minute restarts, against hourly checkpoints and 38-minute restarts, 59 minutes saved per interruption.
  Next quarter's capacity plan (2,184 running hours) and placement plan, by programme.
* **Empirical pins.** The interruption population and the two-term law, from the job book.
* **Voices.** The reliability lead: "The sweeps are interrupted more than everyone else put together." The pretraining lead: "Our runs
  are the most expensive thing on the cluster to interrupt." The scheduler team: "Placement is about utilisation, not reliability."
* **Licensed wrong basis.** The policy records that the quarterly review sees the reliability dashboard's incident counts.

## 8. Determinism by construction

* **Health-event window.** Every unplanned termination's health event falls within two minutes before it; windows of three to ten minutes
  give the same 188.
* **Placement.** The plan fixes each programme's pods per job for the quarter: P1 8, P2 4, P3 6, P4 1, P5 1, P6 2; pods hold 256 GPUs.
* **Fit.** The two-term law is exact on the book; Poisson and least-squares fits agree to the third figure on both rates.
* **Rounding.** The saving is 128,973 GPU-hours, clear of the thousand edges; the cut at 4,096 GPUs is exact, and P6, next in line, does
  not fit.

## 9. Prompt sketch and deliverables

> Next quarter our in-memory checkpointing can cover at most 4,096 GPUs, and six training programmes want it. Our reliability lead points
> out that the sweep jobs are interrupted more than everyone else put together. Tell me which programmes get it and how many GPU-hours it
> saves us next quarter, in thousands, as the line for the capacity plan. Send `checkpoint_allocation.xlsx`, a chart
> `interruptions_by_programme.png`, and a one-page `capacity_plan_note.pdf`.

* `checkpoint_allocation.xlsx` — the six programmes under each rung construction with the two fitted rates (ask C), the utilisation sheet
  (ask A) and the storage sheet (ask B).
* `interruptions_by_programme.png` — for each programme, last quarter's and next quarter's interruptions per job split into node and
  fabric terms as stacked bars, with P3's placement change annotated and the funding cut marked.
* `capacity_plan_note.pdf` — the programmes covered, the saving, and why the sweeps are not covered.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 32 pods, last quarter's GPU utilisation. *Device:* GPUs split into partitions
  report each partition as a separate device in the telemetry, as its guide documents, and four inference pods run partitioned. Counting
  devices as GPUs overstates those pods' capacity and understates their utilisation.
* **Ask B (device-carried).** For each of the six programmes, last quarter's checkpoint data written, in terabytes. *Device:* incremental
  checkpoints reference shards written earlier, recorded in each checkpoint's manifest, as the storage guide documents. Summing every
  checkpoint's listed size counts referenced shards again.
* **Ask C (validity).** For each of the six programmes, next quarter's interruptions and GPU-hours saved per GPU covered under the four rung
  constructions, and the two fitted rates.
* **Decoupling.** Clearing the two-term law changes no figure in asks A or B. Device telemetry and checkpoint manifests touch no
  termination, health-event or placement record.

## 11. Rubric arithmetic

32 pods (ask A) + 6 programmes (ask B) + 6 programmes × 4 constructions + 2 rates (ask C) + the programmes covered, the saving and the
margin at the cut + 5 named chart parts + 3 files ≈ 75 criteria.

## 12. World-building constraints

* Programmes: P1 1 job × 2,048 GPUs, 8 pods; P2 1 × 1,024, 4 pods; P3 4 × 256, 1 pod last quarter and 6 next; P4 16 × 64, 1 pod; P5 4 ×
  128, 1 pod; P6 2 × 512, 2 pods. Rates: one node interruption per 402,000 GPU-hours, one fabric stop per 574 pod-hours; 2,184 hours.
* Interruptions last quarter (SLO): P1 41.6, P2 20.8, P3 20.8, P4 66.4, P5 18.0, P6 20.8; next quarter P3 96.8, the rest unchanged.
  Incident-category counts: P4 144.6 (139 of them pre-emptions), P5 20.2, P1 11.1, P3 8.1, P2 5.6, P6 5.6.
* GPU-hours saved per GPU covered, two-term law on the plan: P1 40.9, P3 23.8, P2 20.4, P6 10.2, P5 4.4, P4 4.1; pooled rate: P1 57.0, P2
  28.5, P6 14.2, P3 7.1. Savings: rung 0 34, rung 1 37, rung 2 160, answer 129 thousand; partial cells 115 and 46 thousand.
* Device telemetry and checkpoint manifests are independent of every main-call record.
