# DA47 — GPU fleet efficiency: the average job is not where the GPU-hours go

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | AI-infrastructure teams at labs and cloud providers reporting GPU utilisation (allocated versus used), deciding where to spend optimisation effort |
| Domain | ML infrastructure |
| Task shape | 03 · Bridge between two totals (job-weighted mean GPU utilisation → GPU-hour-weighted utilisation → fleet-level productive GPU-hours; the job-size class targeted for optimisation) |
| Core method | Per-job mean utilisation from minute-level GPU samples; GPU-hour weighting (allocated GPUs × duration); idle-allocated share; bridge from job-weighted to fleet-level metrics by job-size class (1, 2–4, 5–8, > 8 GPUs) |
| Analytical stump | Most jobs are small and short; the job-weighted mean describes them, while large multi-GPU jobs consume most GPU-hours. Optimisation priority depends on idle GPU-hours, which concentrate in classes that look fine on job-weighted averages |
| Primary sources | Microsoft Philly cluster traces (deep-learning training jobs, GPU utilisation samples) |

## 1. The real-world situation

An ML-platform team reported that "average GPU utilisation per job is 52%" and proposed optimising single-GPU jobs, which are the majority.
The infrastructure lead asked where idle GPU-hours actually accumulate across the fleet.

## 2. The decision (one deterministic recommendation)

**The job-size class targeted for optimisation: the class with the most idle allocated GPU-hours, with the bridge from the job-weighted mean
to the fleet-level productive share.**

Rules (infrastructure memo):

* Data: Philly job log (job ID, GPUs allocated, start, end, status) and per-minute GPU utilisation samples per machine-GPU mapped to jobs.
* Jobs: completed, failed or killed jobs with ≥ 10 minutes of samples; GPU utilisation per job = mean of its GPUs' minute samples.
* GPU-hours = GPUs × run hours; productive GPU-hours = GPU-hours × utilisation; idle allocated = GPU-hours − productive.
* Classes: 1, 2–4, 5–8, > 8 GPUs.
* Bridge: job-weighted mean → GPU-hour-weighted mean (difference split by class) → fleet productive share.
* Target: class with maximum idle allocated GPU-hours.

## 3. Why capable analysts get it wrong

* Job counts dominate dashboards.
* Weighting by consumption changes the picture when sizes are skewed.
* Idle capacity is a quantity (GPU-hours), not a rate.
* Failed and killed jobs still consumed allocated GPUs.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `cluster_job_log` | JSON | ~117k jobs | Microsoft Philly traces (GitHub msr-fiddle/philly-traces) | Released for research (repository licence; verify) | Jobs, attempts, GPU placement |
| 2 | `cluster_gpu_util` | CSV | ~40M | Same | Same | Per-minute GPU utilisation by machine/GPU |
| 3 | `cluster_machine_list` | CSV | ~550 | Same | Same | Machines |
| 4 | `philly_traces_readme.md` | Markdown | — | Same | Same | Schema |
| 5 | `jeon_2019_atc_citation.pdf` | PDF | — | Jeon et al., USENIX ATC 2019 (cite) | Cite | Trace analysis |
| 6 | `infrastructure_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `platform_team_report.xlsx` | XLSX | 4 | Task author | — | Job-weighted figures |
| 8 | `job_gpu_minutes.parquet` | Parquet | ~10M | Derived | Same | Job-level samples |

## 5. Deterministic solution path

1. Map utilisation samples to jobs via placements and times.
2. Per-job utilisation; GPU-hours; productive and idle.
3. Class aggregates; bridge; target.
4. Contrast with the platform report.

## 6. Wrong paths (method errors, not misreadings)

**A — job-weighted averages.** Small jobs dominate.

**B — excluding failed/killed jobs.** Idle allocation understated.

**C — machine-level utilisation without job mapping.** Mixes jobs.

**D — ranking classes by mean utilisation.** Rate, not idle quantity.

## 7. Why the stump is analytical, not semantic

Definitions and the target rule are specified. The trap is weighting by count rather than consumption.

## 8. Draft task prompt (prose)

> Where should GPU optimisation effort go? Compute utilisation by job-size class and the idle GPU-hours as the infrastructure memo specifies, and
> bridge the job-weighted figure to the fleet figure. Provide `class_utilisation.csv`, `idle_gpu_hours.png`, and a one-page
> `optimisation_target.pdf`.

## 9. Deliverables

* `class_utilisation.csv`, `idle_gpu_hours.png`, `optimisation_target.pdf`.

## 10. Where 25+ rubric criteria come from

* 4 classes × (jobs, GPU-hours, utilisation, idle) = 16; bridge items; target; status handling; contrast.

## 11. Golden-output checklist

* Sample-to-job mapping; inclusion rule; weighting; idle computation; bridge; target.

## 12. Build notes (scope tuning)

* Confirm that the class with the lowest job-weighted utilisation is not the class with the most idle GPU-hours.
