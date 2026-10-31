## Tags

**Domain:** General Statistics & Data Science (regression and classification model diagnostics: GPU busy time regressed on the prompt tokens a model computes and the tokens it generates, the specification chosen on its out-of-sample fit to an early-access tenant).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Give the stopgap cluster to docs-prod (Docs): its Q1 peak-week shortfall is 340 GPUs, in 2027-W13.**
Docs' eleven signed report-service contracts need about 250 GPUs at their contracted peaks once all are live, because each report call is its own session and lc2 computes its whole prompt. Not code-prod (Code, 300 GPUs short), which leads only when report calls are priced at Docs' GPU-seconds per request, a rate set by follow-up turns that re-send a document their session already holds. Not a costing at Docs' own rates per token, per session or per new session, or at the early-access tenant's cost per call or per report: each under-prices the report prompts and leaves Code first. Not a source pack shared across a report's calls either: each call opens its own session, and the tenant's busy time matches every call computing its whole prompt.

## 2. Critical Components

1. lc2 costs **0.248** GPU-milliseconds per prompt token it computes and **1.85** per completion token.
2. The eleven signed report-service contracts at their contracted peaks need about **250** GPUs once all are live.
3. docs-prod's shortfall peaks in **2027-W13**, against the **656** GPUs the fleet plan allocates it that week.

## 3. Step-by-Step Solution

1. Read stopgap_assignment_policy_2026-11.pdf: a week's requirement is the busiest hour's busy GPU-seconds over 2,520 (70 per cent busy), signed contracts count at contracted peak from the go-live Monday at their tier's calls and limits, and the cluster goes to the largest Q1 peak-week shortfall against the fleet plan.
2. Costed every pool's busiest-hour requests in q1_2027_capacity_intake.xlsx (Voice's requests per second times 3,600) at its Q3 GPU-seconds per request in capacity_closeout_2026Q3.pdf, as the policy files (Docs 1.6297).
3. Fitted gpu_busy_s on prompt_tokens and completion_tokens over the batch-prod hours tagged lc2-2026.05 in fleet_rollup_hourly_2026-01-01_2026-12-06.csv, where every request is one call and nothing is reused: 0.248 and 1.85 GPU-milliseconds.
4. Checked those rates on the early-access tenant's 894,042 report calls in docs_usage_by_org_daily_2026-09-01_2026-12-06.csv (5 October to 4 December; on those days the rollup's sessions_new exceeds billing's app and API sessions by one per call): on Amsterdam or UTC days, at the close-out's 1.6297 or the exact Q3 rate, they come within 2 per cent of the busy GPU-seconds docs-prod ran on those days above its other requests, where Docs' rate per request predicts about a fifth.
5. Priced each signed contract in report_service_commitments_2026-12-04.xlsx at its tier's calls per report times its prompt and completion limits per call at those rates, from its go-live week: about 250 GPUs once all eleven are live.
6. Subtracted each week's allocation in fleet_plan_2027Q1.xlsx: docs-prod's largest weekly shortfall is 340 GPUs, in 2027-W13, the largest of the six pools.
7. For the out-of-service table, joined fleetctl's cordon and uncordon steps with the console's cordons, uncordons and hand-completed jobs (Europe/Amsterdam times converted to UTC), counted eight GPUs per node from cordon to uncordon in November and gave each hour to the node's pool at the time (fleet_nodes_2026-12-06.csv), as the stopgap policy's section 6 counts them.
8. For acceptance, applied lease_schedule3_acceptance.pdf to the latest burn-in run of each fitted GPU serial and each node's latest all-reduce in nx7_fabric_results.csv finished before the 14:00 Amsterdam review (13:00 UTC), Gbit/s runs divided by 8 before the 360 GB/s line, racks as in nx7_handover_inventory_2026-12-04.csv.

## 4. Deliverable Answers

### stopgap_q1_2027.xlsx

1. The stopgap goes to docs-prod (Docs), Q1 peak-week shortfall 340 GPUs (2027-W13).
2. Out of service in November 2026, GPU-hours to the nearest 10 and the longest stay in hours:
   - chat-prod: 3,630 GPU-hours, longest 57.4 hours
   - code-prod: 1,110 GPU-hours, longest 33.7 hours
   - agents-prod: 1,470 GPU-hours, longest 57.0 hours
   - docs-prod: 1,260 GPU-hours, longest 57.1 hours
   - batch-prod: 810 GPU-hours, longest 56.0 hours
   - voice-prod: 1,250 GPU-hours, longest 55.9 hours
3. Accepted at the 4 December review, whole GPUs, with the node ids of any nodes held back:
   - R11: 48 GPUs accepted; nodes held back: nx7-2638
   - R12: 40 GPUs accepted; nodes held back: nx7-2653, nx7-2654
   - R13: 48 GPUs accepted; nodes held back: nx7-2662
   - R14: 64 GPUs accepted; nodes held back: nx7-2645

### pool_out_of_service_nov2026.png

4. A bar for each of the six pools, its November GPU-hours out of service labelled at the bar's end, chat-prod the longest bar, titled with the pool that lost the most.
