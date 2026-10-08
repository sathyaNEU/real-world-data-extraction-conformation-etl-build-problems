# DS47 — How often to checkpoint a long training job: failures do not arrive as a steady Poisson stream

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Checkpointing policies for large AI training runs and HPC jobs at AI labs and cloud providers (choosing intervals that balance overhead and lost work) |
| Domain | High-performance computing / ML infrastructure |
| Task shape | 04 · Setting one dial (the checkpoint interval for a 2,048-node job that minimises expected wasted time per day) |
| Core method | Empirical system-level failure process from node failure logs (job-scale failure rate = node rate × nodes, adjusted for correlated failures); time-between-failures distribution (Weibull fit, shape < 1); simulate the job with checkpoint cost C and restart R over the empirical inter-failure sequence (trace replay) for candidate intervals; compare with Young/Daly τ = √(2 C × MTBF) |
| Analytical stump | The Young/Daly formula assumes exponential (memoryless) failures with a stable MTBF. Real systems show bursty failures (decreasing hazard, correlated node failures after maintenance or software rollouts); the trace-based optimum differs, and MTBF from node counts × node MTBF ignores correlation |
| Primary sources | Los Alamos National Laboratory (LANL) HPC failure data (Computer Failure Data Repository; Schroeder & Gibson) |

## 1. The real-world situation

An ML infrastructure team runs multi-week jobs on a 2,048-node cluster. Checkpoints take 6 minutes; restarts take 10 minutes. The team set the
checkpoint interval using the Young/Daly formula with MTBF = node MTBF ÷ 2,048. Jobs still lose hours in failure bursts.

## 2. The decision (one deterministic recommendation)

**The checkpoint interval (minutes, from 10 to 240 in 5-minute steps) minimising expected waste per day under trace replay, and the waste of the
Young/Daly interval.**

Rules (infrastructure memo):

* Data: LANL failure records for the systems in memo (node ID, failure start time, root-cause category), production period only.
* Job-level failure sequence: take the system-level failure times of the largest LANL system in the memo and multiply each inter-failure
  interval by (system nodes ÷ 2,048), so that more nodes give proportionally shorter intervals, preserving the order and burst structure.
* Inter-failure times: fit Weibull (shape k, scale λ) for reporting; replay uses the empirical sequence.
* Waste per failure = time since last checkpoint + restart R; plus checkpoint overhead C per interval.
* Expected waste per day = total waste ÷ total days over the replayed period.
* Young/Daly: τ = √(2 × C × MTBF) with MTBF = mean inter-failure time.
* Choose the interval with minimum replayed waste.

## 3. Why capable analysts get it wrong

* Young/Daly is the standard formula.
* Failure bursts after events violate memorylessness.
* Node-count scaling ignores correlated failures (rack, switch, software).
* Replay against observed sequences captures clustering.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `LANL_failure_data_1996_2005.csv` | CSV | ~23k failures | USENIX CFDR (LANL data) | Public release (cite Schroeder & Gibson) | Failure records |
| 2 | `LANL_system_descriptions.csv` | CSV | ~22 systems | Same | Same | Nodes, processors, production dates |
| 3 | `lanl_data_readme.pdf` | PDF | — | Same | Same | Field definitions |
| 4 | `infrastructure_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `team_young_daly_setting.xlsx` | XLSX | — | Task author | — | Current setting |
| 6 | `daly_2006_citation.pdf` | PDF | — | Cite | Cite | Formula |
| 7 | `schroeder_gibson_2006_citation.pdf` | PDF | — | Cite | Cite | Failure characteristics |

## 5. Deterministic solution path

1. Build the job-scale failure sequence per memo.
2. Weibull fit (report); MTBF; Young/Daly τ.
3. Replay waste for each candidate interval; choose; compare.

## 6. Wrong paths (method errors, not misreadings)

**A — Young/Daly with node-scaled MTBF.** Misses bursts.

**B — exponential simulation instead of replay.** Same assumption.

**C — ignoring restart time.** Underestimates waste.

**D — using all systems' failures regardless of size.** Wrong scale.

## 7. Why the stump is analytical, not semantic

Data handling and replay are specified. The trap is assuming memoryless failures in a policy calculation.

## 8. Draft task prompt (prose)

> What checkpoint interval should our long training jobs use? Replay the LANL failure sequence as the infrastructure memo specifies and compare with the
> Young/Daly setting. Provide `interval_sweep.csv` (interval: waste per day), `inter_failure_distribution.png`, and a one-page `checkpoint_policy.pdf`.

## 9. Deliverables

* `interval_sweep.csv`, `inter_failure_distribution.png`, `checkpoint_policy.pdf`.

## 10. Where 25+ rubric criteria come from

* Chosen interval; waste at 10 intervals; Weibull k, λ; MTBF; Young/Daly τ and its waste; burst statistics.

## 11. Golden-output checklist

* Sequence construction; replay mechanics; overheads; sweep; choice.

## 12. Build notes (scope tuning)

* Confirm Weibull shape < 0.8 and the replay optimum differs from τ by ≥ 25%.
