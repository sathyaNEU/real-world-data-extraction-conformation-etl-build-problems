"""task268's submission.md, drafted from the figure set deliver.figures builds: every number is emitted, never
typed."""
import common as K
from deliver import names


def write(R, F):
    pg = "partner-gateway"
    over = F["over"]
    sli, bud = F["sli"], F["budget"]
    L = ["## Tags", "",
         "**Domain:** General Statistics & Data Science (missing data, censoring and measurement error).",
         "**Analytical objective:** Descriptive & Distribution Analysis.", "",
         "## 1. Final Recommendation", "",
         "**Five internal services ran over their 2026 latency error budget and each gets a reliability engineer for "
         "the first half of 2027: %s.**" % names(over),
         "Partner-gateway's December SLI is %s%% against its %s%% budget once each kept span counts at its trace's "
         "edge keep share. Not partner-gateway at %s%%, its own spans reweighted hour by hour on its own count, because "
         "the store kept them with the traces journey-search, seat-map and booking started at very different shares. "
         "Not the kept spans' own share, which passes journey-search, places, seat-map and partner-gateway (%s%%, "
         "%s%%, %s%% and %s%%)." % (sli[pg], bud[pg], F["pg_service_hour"], F["kept_share"]["journey-search"],
                                    F["kept_share"]["places"], F["kept_share"]["seat-map"], F["kept_share"][pg]),
         "", "## 2. Critical Components", "",
         "1. Partner-gateway's December 2026 latency SLI is **%s%%** against a **%s%%** budget." % (sli[pg], bud[pg]),
         "2. Journey-search is at **%s%%**, places **%s%%**, seat-map **%s%%** and notifications **%s%%**, each against "
         "a **%s%%** budget." % (sli["journey-search"], sli["places"], sli["seat-map"], sli["notifications"],
                                 bud["journey-search"]),
         "3. Fares is at **%s%%**, tickets **%s%%** and accounts **%s%%** against **%s%%**, booking **%s%%** and "
         "payments **%s%%** against **%s%%**." % (sli["fares"], sli["tickets"], sli["accounts"], bud["fares"],
                                                  sli["booking"], sli["payments"], bud["booking"]),
         "", "## 3. Step-by-Step Solution", "",
         "1. Read PR-SLO-3: a service's latency SLI is the share of the requests it handled in December 2026, in "
         "Lisbon time (UTC all month), whose server span exceeded its section 4 threshold, whether or not the "
         "tracing store kept a span for it; a breach is an SLI over its budget.",
         "2. Kept the server spans in trace_spans_2026-12.parquet, dropping the GET /healthz probes and the rows "
         "re-sent under a repeated span_id, and linked each to its trace's root, the server span with a blank "
         "parent_span_id: every internal service's span sits in a whole trace an edge service started.",
         "3. For each edge service and hour, divided its RequestCount in lb_target_group_requests_2026-H2.csv (target "
         "groups through service_catalogue_2026.xlsx) by the root spans it kept: the weight of every span in the "
         "traces it started that hour.",
         "4. Summed each service's weighted spans over its threshold and divided by its December RequestCount: "
         "partner-gateway %s%%, journey-search %s%%, places %s%%, seat-map %s%% and notifications %s%%, the other "
         "five under budget." % (sli[pg], sli["journey-search"], sli["places"], sli["seat-map"],
                                 sli["notifications"]),
         "5. Compared each SLI to one decimal with its budget: %s breach and get a reliability engineer for January to "
         "June 2027." % names(over),
         "6. Releases and rollbacks (PR-SLO-3 section 5.1): replayed production's changes in time order, the "
         "successful production deploys in production_deployments_2026.json before each deployment's first revision "
         "in cluster_rollout_history_2026.csv (14 April), then every later revision there, where on-call undos, "
         "hotfix images and restarts also appear and images name their commit; a commit's first time in production "
         "is a release, a change to a commit first released before the running one a rollback: partner-gateway %s "
         "releases and %s rollbacks, the rest in block 4." % (F["releases"][pg], F["rollbacks"][pg]),
         "7. Cost by half (section 5.3): each line in cloud_billing_2026.csv to its service tag, a line tagged only "
         "with a team to the service of the resource that replaced it in cloud_resources_2026.csv, US dollar lines at "
         "their invoice's rate in cloud_invoices_2026.csv, VAT and the support plan out, credits netted, dated by "
         "usage: partner-gateway EUR %s and EUR %s, the rest in block 4." % tuple(F["cost_eur_text"][pg]),
         "8. Incident minutes by half (sections 5.2 and 5.4): each incident in incidents_2026.csv matched to its "
         "status page post by component and time, its end the last of its components back to operational, each "
         "service counted from the moment incident_timeline_2026.csv names it, overlaps once, the halves split at "
         "1 July 00:00 Lisbon time: partner-gateway %s and %s minutes, the rest in block 4." % tuple(
             F["minutes_text"][pg]),
         "", "## 4. Deliverable Answers", "",
         "### %s" % K.DOCX_OUT, "",
         "1. Names the services that ran over their 2026 latency error budget: %s." % names(over),
         "2. Every service's December 2026 latency SLI beside its error budget, per cent to one decimal:"]
    for s in K.SVC:
        L.append("   - %s: SLI %s against a budget of %s, %s" % (s, sli[s], bud[s],
                                                               "over" if F["ran_over"][s] == "yes" else "within"))
    L += ["3. A bar chart after the table of each service's SLI with its own error budget marked on its bar, the "
          "services over budget in red.", "",
          "### %s" % K.CSV_OUT, "",
          "1. A row per service; SLI and budget in per cent to one decimal, minutes whole, costs in whole euros:"]
    for s in K.SVC:
        L.append("   - %s: SLI %s, budget %s, ran over %s, %s releases and %s rollbacks in 2026, customer-facing "
                 "incident minutes %s in the first half and %s in the second, cost EUR %s and EUR %s"
                 % (s, sli[s], bud[s], F["ran_over"][s], F["releases"][s], F["rollbacks"][s], F["minutes_text"][s][0],
                    F["minutes_text"][s][1], F["cost_eur_text"][s][0], F["cost_eur_text"][s][1]))
    text = "\n".join(L) + "\n"
    F["sections"] = ["2.1", "2.2", "3.1", "3.2", "5.1", "5.2", "5.3", "5.4"]
    return text, F
