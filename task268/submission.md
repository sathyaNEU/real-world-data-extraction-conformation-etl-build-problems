## Tags

**Domain:** General Statistics & Data Science (missing data, censoring and measurement error).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**Five internal services ran over their 2026 latency error budget and each gets a reliability engineer for the first half of 2027: journey-search, places, seat-map, partner-gateway and notifications.**
Partner-gateway's December SLI is 2.9% against its 2.0% budget once each kept span counts at its trace's edge keep share. Not partner-gateway at 1.4%, its own spans reweighted hour by hour on its own count, because the store kept them with the traces journey-search, seat-map and booking started at very different shares. Not the kept spans' own share, which passes journey-search, places, seat-map and partner-gateway (0.7%, 0.7%, 0.7% and 0.8%).

## 2. Critical Components

1. Partner-gateway's December 2026 latency SLI is **2.9%** against a **2.0%** budget.
2. Journey-search is at **1.3%**, places **1.5%**, seat-map **1.5%** and notifications **1.6%**, each against a **1.0%** budget.
3. Fares is at **0.6%**, tickets **0.6%** and accounts **0.7%** against **1.0%**, booking **0.4%** and payments **0.3%** against **0.5%**.

## 3. Step-by-Step Solution

1. Read PR-SLO-3: a service's latency SLI is the share of the requests it handled in December 2026, in Lisbon time (UTC all month), whose server span exceeded its section 4 threshold, whether or not the tracing store kept a span for it; a breach is an SLI over its budget.
2. Kept the server spans in trace_spans_2026-12.parquet, dropping the GET /healthz probes and the rows re-sent under a repeated span_id, and linked each to its trace's root, the server span with a blank parent_span_id: every internal service's span sits in a whole trace an edge service started.
3. For each edge service and hour, divided its RequestCount in lb_target_group_requests_2026-H2.csv (target groups through service_catalogue_2026.xlsx) by the root spans it kept: the weight of every span in the traces it started that hour.
4. Summed each service's weighted spans over its threshold and divided by its December RequestCount: partner-gateway 2.9%, journey-search 1.3%, places 1.5%, seat-map 1.5% and notifications 1.6%, the other five under budget.
5. Compared each SLI to one decimal with its budget: journey-search, places, seat-map, partner-gateway and notifications breach and get a reliability engineer for January to June 2027.
6. Releases and rollbacks (PR-SLO-3 section 5.1): replayed production's changes in time order, the successful production deploys in production_deployments_2026.json before each deployment's first revision in cluster_rollout_history_2026.csv (14 April), then every later revision there, where on-call undos, hotfix images and restarts also appear and images name their commit; a commit's first time in production is a release, a change to a commit first released before the running one a rollback: partner-gateway 42 releases and 9 rollbacks, the rest in block 4.
7. Cost by half (section 5.3): each line in cloud_billing_2026.csv to its service tag, a line tagged only with a team to the service of the resource that replaced it in cloud_resources_2026.csv, US dollar lines at their invoice's rate in cloud_invoices_2026.csv, VAT and the support plan out, credits netted, dated by usage: partner-gateway EUR 32,454 and EUR 37,711, the rest in block 4.
8. Incident minutes by half (sections 5.2 and 5.4): each incident in incidents_2026.csv matched to its status page post by component and time, its end the last of its components back to operational, each service counted from the moment incident_timeline_2026.csv names it, overlaps once, the halves split at 1 July 00:00 Lisbon time: partner-gateway 27 and 152 minutes, the rest in block 4.

## 4. Deliverable Answers

### reliability_review_2026.docx

1. Names the services that ran over their 2026 latency error budget: journey-search, places, seat-map, partner-gateway and notifications.
2. Every service's December 2026 latency SLI beside its error budget, per cent to one decimal:
   - journey-search: SLI 1.3 against a budget of 1.0, over
   - fares: SLI 0.6 against a budget of 1.0, within
   - places: SLI 1.5 against a budget of 1.0, over
   - seat-map: SLI 1.5 against a budget of 1.0, over
   - booking: SLI 0.4 against a budget of 0.5, within
   - payments: SLI 0.3 against a budget of 0.5, within
   - tickets: SLI 0.6 against a budget of 1.0, within
   - accounts: SLI 0.7 against a budget of 1.0, within
   - partner-gateway: SLI 2.9 against a budget of 2.0, over
   - notifications: SLI 1.6 against a budget of 1.0, over
3. A bar chart after the table of each service's SLI with its own error budget marked on its bar, the services over budget in red.

### service_sli_2026.csv

1. A row per service; SLI and budget in per cent to one decimal, minutes whole, costs in whole euros:
   - journey-search: SLI 1.3, budget 1.0, ran over yes, 47 releases and 1 rollbacks in 2026, customer-facing incident minutes 293 in the first half and 205 in the second, cost EUR 80,138 and EUR 93,336
   - fares: SLI 0.6, budget 1.0, ran over no, 40 releases and 3 rollbacks in 2026, customer-facing incident minutes 59 in the first half and 329 in the second, cost EUR 46,382 and EUR 49,856
   - places: SLI 1.5, budget 1.0, ran over yes, 31 releases and 3 rollbacks in 2026, customer-facing incident minutes 755 in the first half and 109 in the second, cost EUR 55,872 and EUR 62,482
   - seat-map: SLI 1.5, budget 1.0, ran over yes, 35 releases and 7 rollbacks in 2026, customer-facing incident minutes 337 in the first half and 72 in the second, cost EUR 19,292 and EUR 20,709
   - booking: SLI 0.4, budget 0.5, ran over no, 27 releases and 1 rollbacks in 2026, customer-facing incident minutes 461 in the first half and 220 in the second, cost EUR 41,796 and EUR 44,716
   - payments: SLI 0.3, budget 0.5, ran over no, 20 releases and 1 rollbacks in 2026, customer-facing incident minutes 329 in the first half and 232 in the second, cost EUR 23,584 and EUR 24,739
   - tickets: SLI 0.6, budget 1.0, ran over no, 23 releases and 3 rollbacks in 2026, customer-facing incident minutes 218 in the first half and 368 in the second, cost EUR 16,943 and EUR 18,862
   - accounts: SLI 0.7, budget 1.0, ran over no, 29 releases and 4 rollbacks in 2026, customer-facing incident minutes 100 in the first half and 227 in the second, cost EUR 22,156 and EUR 23,510
   - partner-gateway: SLI 2.9, budget 2.0, ran over yes, 42 releases and 9 rollbacks in 2026, customer-facing incident minutes 27 in the first half and 152 in the second, cost EUR 32,454 and EUR 37,711
   - notifications: SLI 1.6, budget 1.0, ran over yes, 26 releases and 3 rollbacks in 2026, customer-facing incident minutes 401 in the first half and 475 in the second, cost EUR 18,182 and EUR 18,612
