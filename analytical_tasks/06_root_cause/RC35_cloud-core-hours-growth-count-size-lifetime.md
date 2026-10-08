# RC35 — Compute consumption up 35%: more VMs, bigger VMs, or VMs that never get deleted?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Cloud cost spikes at any company (FinOps): spend = resources × size × time running, where the levers (quotas, rightsizing, lifecycle policies) differ by driver |
| Domain | Cloud infrastructure / FinOps |
| Task shape | 03 · Bridge between two totals (core-hours in week 1 → week 4 of the trace, bridged by active-VM count, core-size mix and hours active per VM, by workload category) |
| Core method | Core-hours in a period = Σ over VMs active in the period of cores × hours of overlap; LMDI decomposition of the change into active VM count, size (cores per active VM), and duty (hours active per active VM in the period), additionally split by workload category; lifetimes analysed with censoring-aware methods only for context |
| Analytical stump | The obvious decomposition uses VMs created in each period × average size × average lifetime. That mixes flows with stocks: long-lived VMs created before the period dominate core-hours, and lifetimes of VMs still running at the end of the trace are censored, so "average lifetime" from completed VMs is biased short. Short-lived VM churn inflates creation counts without adding much consumption, so a VM-count quota looks like the answer when it is not |
| Primary sources | Azure Public Dataset — Azure VM trace 2019 (AzurePublicDatasetV2: VM table with creation and deletion times, core and memory buckets, workload category, CPU utilisation) |

## 1. The real-world situation

A platform team's compute consumption, measured in core-hours, rose 35% between the first and last week of a month. Finance proposed a hard quota on
the number of VMs per subscription, reasoning that developers were creating too many VMs. The platform lead suspected that a few long-running,
larger VMs that were never deleted explained most of the growth. Different drivers imply different controls: count quotas, rightsizing, or
lifecycle (auto-deletion) policies.

## 2. The decision (one deterministic recommendation)

**The control adopted — VM-count quota, rightsizing, or lifecycle policy — mapped to the largest LMDI effect (count, size, duty), with the bridge in
core-hours by workload category.**

Rules (FinOps memo):

* Data: Azure VM trace 2019 VM table; trace time in seconds from the trace start; week 1 = days 0–6, week 4 = days 21–27.
* Cores per VM: the memo's mapping of core-count buckets to representative cores (bucket midpoints as specified); VMs with unknown buckets
  excluded and counted.
* Active in a week: created before the week ends and (deleted after the week starts or never deleted within the trace).
* Overlap hours: hours of the week during which the VM existed.
* Core-hours = Σ cores × overlap hours.
* Factors per workload category c (interactive, delay-insensitive, unknown): N_c = active VMs; S_c = core-hours-weighted cores per active VM
  (Σ cores × overlap ÷ Σ overlap); D_c = overlap hours per active VM. Core-hours_c = N_c × S_c × D_c.
* LMDI-I effects for N, S, D summed over categories; closure exact.
* Control mapping: count effect → quota; size effect → rightsizing; duty effect → lifecycle policy.
* Context (not used in the decision): Kaplan–Meier lifetime curve of VMs created in week 1, with VMs alive at trace end censored.

## 3. Why capable analysts get it wrong

* VM creation counts are the most visible metric and they grew fastest.
* Lifetimes of long-running VMs are censored in any finite trace.
* Short-lived VMs dominate counts but not consumption.
* Mix across workload categories changes the averages.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `vmtable.csv.gz` | CSV | ~2.7M VMs | Azure Public Dataset V2 (VM trace 2019) | CC BY 4.0 (Azure Public Dataset terms; verify) | VM lifetimes and attributes |
| 2 | `vm_cpu_readings-file-1-of-195.csv.gz` | CSV | ~6M | Same | Same | CPU readings (context; utilisation check) |
| 3 | `schema.csv` | CSV | ~20 | Same | Same | Field definitions |
| 4 | `core_bucket_mapping.json` | JSON | ~6 | Task author | — | Bucket → cores |
| 5 | `finops_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `finance_quota_proposal.xlsx` | XLSX | — | Task author | — | Creation-count analysis |
| 7 | `cortez_2017_resource_central_citation.pdf` | PDF | — | Cite | Cite | Trace background |

## 5. Deterministic solution path

1. Load the VM table; map buckets; flag unknowns; define weeks.
2. Active sets and overlap hours per week; core-hours by category.
3. Factors N, S, D; LMDI effects; closure.
4. Control mapping; Kaplan–Meier context; contrast with finance's creation-count analysis.

## 6. Wrong paths (method errors, not misreadings)

**A — creations × size × lifetime.** Uses flows; long-running VMs created earlier vanish from the analysis.

**B — lifetime from completed VMs only.** Censoring biases lifetimes short and hides the duty driver.

**C — unweighted mean cores per VM.** Small, short-lived VMs dominate the size factor.

**D — percentage changes added.** Multiplicative identity without LMDI leaves a residual.

## 7. Why the stump is analytical, not semantic

All fields are numeric trace attributes; the mapping and formulas are given. The trap is flow vs stock accounting and censoring.

## 8. Draft task prompt (prose)

> Finance wants a VM-count quota because compute consumption jumped 35%. Decompose the change with the FinOps memo's active-VM method and tell me
> which control fits. Provide `core_hour_bridge.csv` (effect by category), `core_hour_bridge.png`, and a one-page `finops_control_decision.pdf`.

## 9. Deliverables

* `core_hour_bridge.csv` — N, S, D effects by workload category and totals.
* `core_hour_bridge.png` — waterfall of core-hours with category stacks; inset Kaplan–Meier curve.
* `finops_control_decision.pdf` — control, bridge and why creation counts mislead.

## 10. Where 25+ rubric criteria come from

* Bucket mapping and exclusions: 2.
* Active VMs, core-hours by category and week: 6.
* Factors N, S, D by category and week: 9 (grouped).
* LMDI effects and closure: 4.
* Control mapping: 1.
* Kaplan–Meier context and contrast: 3+.

## 11. Golden-output checklist

* Active-set definition with censoring at trace end.
* Overlap-hour core-hours; weighted size factor.
* LMDI-I with exact closure.

## 12. Build notes (scope tuning)

* Confirm on the trace that creations grow faster than core-hours and that the duty or size effect, not the count effect, is the largest; if not,
  choose the subset of subscriptions in the memo where that holds and state the subset rule.
