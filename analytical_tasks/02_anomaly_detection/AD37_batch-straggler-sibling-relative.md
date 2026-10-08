# AD37 — Straggler detection in batch jobs: slow compared to what?

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Speculative execution and straggler mitigation in large batch platforms (backup tasks in MapReduce-style systems at Google, Microsoft and Alibaba) |
| Domain | Cloud infrastructure / batch computing |
| Task shape | 04 · Setting one dial (the straggler multiplier k that launches a backup instance) |
| Core method | Instance duration relative to the median of sibling instances in the same task (same job and task name), evaluated at the time a backup decision would be made; replay of launch rule on completed tasks: tail-latency reduction versus extra instances |
| Analytical stump | Global duration thresholds flag every instance of long-running tasks and never fire for slow instances of short tasks. Stragglers are only meaningful relative to siblings doing the same work. Evaluating with final durations ignores that the decision is made while siblings are still running |
| Primary sources | Alibaba cluster-trace-v2018 (batch_task and batch_instance tables) |

## 1. The real-world situation

A batch platform team wants to enable speculative backups. The prototype launched a backup for any instance running longer than the
95th percentile of all instance durations; it launched backups for whole stages of heavy tasks while doing nothing for slow instances
of short ones, and the extra load slowed the cluster.

## 2. The decision (one deterministic recommendation)

**The multiplier k (grid 1.2–3.0, step 0.1) that maximises task-completion-time reduction subject to extra instances ≤ 5% of all
instances.**

Rules (platform memo):

* Data: batch_instance and batch_task for one day (in the memo); tasks with ≥ 10 terminated instances; instance duration = end − start.
* Sibling median: at the moment 75% of a task's instances have finished, compute the median duration of finished siblings, m.
* Launch rule: any unfinished instance whose elapsed time exceeds k × m at that moment, or later reaches k × m, gets one backup.
* Backup completion: backup duration drawn deterministically as m (the memo's replay convention); instance finishes at the earlier of
  original end and backup end.
* Task completion = max instance finish; reduction = original − replayed, summed over tasks.
* Extra instances = number of backups; constraint ≤ 5% of instances in scope.

## 3. Why capable analysts get it wrong

* Global percentiles mix tasks with very different work sizes.
* Decisions must use only information available at decision time; final sibling medians include the straggler itself.
* Smaller k always helps completion time; the constraint on extra load determines the answer.
* Tasks with few instances have unreliable medians; the memo filters them.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `batch_instance.tar.gz` (one-day extract) | CSV | ~100M (extract ~20M) | Alibaba clusterdata (cluster-trace-v2018) | Alibaba clusterdata terms (open for research; cite) | Instances: start, end, status, machine |
| 2 | `batch_task.tar.gz` | CSV | ~14M (extract ~1M) | Same | Same | Tasks: job, task name, instance count |
| 3 | `machine_meta.tar.gz` | CSV | ~4k | Same | Same | Machines (context) |
| 4 | `schema.txt` | Text | — | Same | Same | Field definitions |
| 5 | `platform_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `prototype_global_p95_replay.csv` | CSV | ~1k | Task author | — | Prototype results |
| 7 | `dean_ghemawat_backup_tasks_citation.pdf` | PDF | — | Cite | Cite | Backup tasks |
| 8 | `instances_in_scope.parquet` | Parquet | ~5M | Derived | Same | Filtered instances |
| 9 | `replay_reference_tasks.json` | JSON | ~10 | Task author | — | Hand-checked tasks |
| 10 | `day_selection.json` | JSON | 1 | Task author | — | Day in scope |

## 5. Deterministic solution path

1. Extract the day; filter terminated instances and tasks with ≥ 10 instances.
2. For each task, find the 75% completion moment and sibling median.
3. For each k, apply the launch rule; replay finishes; sum reductions and backups.
4. Choose k meeting the constraint with maximum reduction; contrast with the prototype.

## 6. Wrong paths (method errors, not misreadings)

**A — global percentile threshold.** Wrong instances backed up.

**B — sibling median from final durations.** Look-ahead; optimistic.

**C — ignoring the extra-load constraint.** Chooses the smallest k.

**D — including tasks with few instances.** Unstable medians.

## 7. Why the stump is analytical, not semantic

Fields, rules and replay conventions are specified. The traps are relative-versus-global baselines and decision-time information.

## 8. Draft task prompt (prose)

> Pick the straggler multiplier for speculative backups by replaying the rule in the platform memo on one day of the Alibaba trace. Provide
> `k_sweep.csv` (k: backups, share of instances, completion-time reduction), `tradeoff_curve.png`, and a one-page `backup_setting.pdf` comparing
> with the global-percentile prototype.

## 9. Deliverables

* `k_sweep.csv`, `tradeoff_curve.png`, `backup_setting.pdf`.

## 10. Where 25+ rubric criteria come from

* k; 19 sweep rows' backups and reductions (sampled checks); reference tasks; prototype contrast.

## 11. Golden-output checklist

* Filters; decision-time median; launch rule; replay; constraint; choice.

## 12. Build notes (scope tuning)

* Pick a day with diverse task sizes; publish reference tasks.
* Confirm the constraint binds within the grid.
