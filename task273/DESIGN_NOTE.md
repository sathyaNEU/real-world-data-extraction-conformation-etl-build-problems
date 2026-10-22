# task273 design note

Architecture 1, drawn 2026-10-22 (wave 5, Descriptive lane, sathay3012). Seed DA23's world (an open-source security fund's maintainer stipends) was set aside at the draw (`## Tried and rejected`); the slot draws a new world in the same objective. Mirrendale Payroll runs a payroll and tax-filing platform for employers and accounting firms, and its year-end peak (the first weeks of January, before the 31 January wage-statement deadline) brings several times its usual traffic. Its readiness standard gives every public API endpoint a 99th-percentile response time of at most 800 milliseconds at the forecast peak-hour volume, measured at the platform's edge, and the platform team fixes every endpoint that would breach it before the 4 December 2026 code freeze. The November load tests ran each endpoint at its forecast peak volume with closed-loop test clients, each sending its next request only after the last returned, against the endpoint's pods behind a round-robin balancer, with every pod's garbage-collection log captured. Theresa Meyers, the platform's capacity planner, needs the number of endpoints to fix, and which.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task273.json`, architecture v1, registered 2026-10-22. `guard.py check` on the filed card: WARN only. `people.first` (Zachary, one older build, task141): drawn by `guard.py names --seed 273`, a single older use. `repeat.gate_g` and `repeat.decision` (task249, a resit cohort's gain carried through a sitting's time limit): a different mechanism and another field; a readiness list is a set by nature. `repeat.deliverables` (task252, a workbook and a chart): what a readiness review files. The decisive generator G12 repeats seven older signatures (task180 v4, task196 v2, task255 v1, task268 v2, task271 v3, task456, task462), each differentiated on the card: none has a client whose own blocking removes the observations exactly while the server stalls. G18 (the textbook correction resisted) is the second generator, G17 the third.
2. Pairing: General Statistics & Data Science (client domain) / missing-data-censoring-measurement-error / Descriptive & Distribution Analysis. The task type's own object, data missing because of the outcome and rebuilt from the mechanism the records hold, decides the call; the setting is a software platform's capacity review, and the swap is of the method (General Statistics' rule): replacing the rebuilt distribution with the recorded percentile, or with the back-fill that ignores the balancer, changes which endpoints are fixed.
3. Niche: a closed-loop load test whose clients stop sending while the pod they reached is paused for garbage collection, so the requests customers would send in that time are missing from the record, while each pod's GC log says when and for how long it was paused.
4. Call and shape: how many of the 24 public endpoints must be fixed before the code freeze, and which (`designation_set`, question form how many). Shape 14 (cuts of a distribution): each endpoint's 99th percentile against the 800-millisecond standard.
5. Gate G `method_or_model_selection` (the recorded percentile, the textbook back-fill and the rebuilt distribution are three estimators of one filed quantity, the data's structure ruling the first two out), strategy key `population_selection` (the recorded requests are a sample the clients' own blocking selected against the slow moments; the decisive step restores the population of requests customers would send), generators G12, G18, G17.
6. Data-native sentence: each test client sends its next request only after the last returns, and every pod stops the world for garbage collection; while a pod is paused the clients that reached it send nothing, so the requests customers would send during the pause never enter the record, and the pod's GC log, at another grain than the request log, says exactly when and for how long it was paused.
7. Sources, one line each:
   - The client library's missing-data patterns (Rubin's rules, errors in a covariate, delta-adjusted MNAR): the missingness here is not at random and its mechanism is recorded, so nothing is assumed; this build's pattern is `own:requests-a-closed-loop-client-never-sent-rebuilt-from-each-pods-pause-record`.
   - Coordinated omission, the performance-engineering name for this sampling: its textbook repair (HdrHistogram's back-fill at the expected interval) credits each blocked client with every request it would have sent to the server that stalled, which holds for one server and overstates a pause on one pod behind a balancer, and back-fills endpoints whose slow responses are slow on their own rather than stalled.
   - task264 in this lane (members drawn in proportion to their events): a sampling weight proportional to a known count; here no weight is known per record, and the missing requests are rebuilt from a timeline in another file.
   - stumping 1.6a: an unobserved quantity (the response times customers would see at the peak), a construction across two grains (requests and pauses), inputs varied enough (pause lengths, pause frequencies, pod counts and service-time tails differ by endpoint) that no column of the GC log, its pause share or its longest pause, names the set.
8. People, drawn with `guard.py names --geo "united states" --seed 273`: Theresa Meyers (capacity planner, the requester), Zachary Mendoza (vice president of platform engineering, who owns the readiness standard). Invented names (Mirrendale Payroll and its services) are screened in `checks.py` (H21).

## Default path

1. Read the readiness standard: an endpoint is fixed before the freeze when, at its forecast peak-hour volume, fewer than 99 percent of the requests customers send it get their complete response within 800 milliseconds (2.1), shown by its run of record, the last complete run of the November campaign, minutes 3 to 13 (3.2).
2. Conform the two tools' results: JMeter's JTL (timeStamp at the sample's start, elapsed in milliseconds) and k6's CSV (timestamp at the response's completion, metric_value in milliseconds), keyed by endpoint code.
3. Take each endpoint's last complete run (the first runs of EP05, EP13 and EP20 stopped early) and its measurement, the ten minutes after the first three.
4. Read each endpoint's 99th percentile of the recorded response times.
5. Name the endpoints over 800 milliseconds.

Ends on: EP02, EP16 and EP22 (three endpoints, at 874, 963 and 1,084 ms).
Golden: EP01, EP02, EP05, EP16 and EP22 (five endpoints).

## Stump sentence

A competent analyst who conforms the JMeter and k6 results, takes each endpoint's last complete run without its warm-up and reads the 99th percentile of the recorded response times names three endpoints for the freeze list, EP02, EP16 and EP22, because each test client sent its next request only after the last returned, so while a pod was paused for garbage collection the clients that had reached it sent nothing, and the record holds one slow request per blocked client where customers, whose requests keep arriving whatever state a pod is in, would meet the pause many times; only the response times rebuilt over arrivals spread across the measurement window and the service's pods, each taking a recorded service time and held by its pod's pauses from the GC log, put EP01 and EP05 over 800 milliseconds as well and name five, while HdrHistogram's back-fill names ten by crediting each blocked client with every request it would have sent to the paused pod.

## Three rules

Task type: missing-data-censoring-measurement-error (General Statistics & Data Science), which serves Descriptive & Distribution Analysis in the taxonomy.
Domain test: the quantity that decides the call is each endpoint's 99th-percentile response time over the requests customers would send at the peak, a distribution no file observes: the test recorded a sample its own clients' blocking selected against the slow moments (coordinated omission, in performance engineering's name), and the estimator that recovers the population's distribution rebuilds the missing requests from the mechanism the records hold, each pod's pause timeline and the service times, as missing-data analysis does when the missingness depends on the outcome and its mechanism is recorded.
Swap: General Statistics' rule swaps the method: replace the distribution rebuilt over customers' arrivals with the recorded requests' percentile and the freeze list loses EP01 and EP05; with HdrHistogram's back-fill it gains EP06, EP07, EP08, EP19 and EP20. A swap of the nouns ("which of our 24 checkout lanes need a second cashier, from a survey of shoppers who each queued once") loses the mechanism that decides: no shopper waits for a till to restart before joining the queue, so nothing is missing because of the outcome.
Layer 1: two load-test tools after the move to k6 on 13 November, with different time conventions (JMeter stamps a sample's start in epoch milliseconds, k6 the response's completion in RFC 3339 nanoseconds); three first runs stopped early and repeated the same day; warm-up minutes; GC log lines written when each pause ends, prefixed by the log platform's ingestion time and ingested out of order; wall-clock decorations at UTC-05:00 on the 2026.11 base image and JVM-uptime decorations on the three services still on the 2025.04 image, two of whose pods restarted during the campaign; G1 concurrent-cycle lines and ZGC summary lines that stop nothing. Each is produced by the systems and nothing is placed to be caught; on the call's path each mishandled keeps the call (SF3 to SF6 asserted, and the restarts missed keep it too) except one: a GC line's stamp read as the pause's start rather than its end puts EP06 on the list as well (SF15 asserted), and the test plan's field guide files that the JVM writes a pause's line when the pause ends.
Layer 2: estimation_fit: the tail of a response-time distribution estimated from a sample selected on the outcome, by rebuilding the missing arrivals from the recorded mechanism (each pod's pauses, each request's own service time) against reading the selected sample's percentile or applying the textbook correction that assumes one server.
Decisive step: rebuilding each endpoint's response times over the requests customers would send, arriving whatever state the pods are in, each held by the pauses of the pod the balancer gives it, instead of reading the percentile of the requests the closed-loop clients happened to send.
Not semantics: every field read correctly (both tools' stamps, the runs of record, every GC line, each pod's JVM start) and every term of the standard applied still leaves the requests customers would have sent during each pause unrecorded, and the easy route on the correctly read records (the recorded 99th percentile of each run of record's measurement) files EP02, EP16 and EP22.
Not rule application: the standard fixes the population (the requests customers send), the outcome (the complete response within 800 ms of reaching the edge), the window (the forecast peak hour, stood for by the run of record), the unit and the comparison; no filed rule or procedure says that the test's clients under-sample the pauses or how the missing requests are rebuilt, and executing every stated rule with the easy route files the three.
Analyst test: a strong analyst who conforms the two tools, reads every field and the standard correctly, keeps each run of record's measurement and takes the 99th percentile of the recorded response times files EP02, EP16 and EP22; only the rebuild over customers' arrivals names EP01, EP02, EP05, EP16 and EP22 (`checks.py`, ANALYST TEST, on the generator's clean rows).
Estimand: the readiness standard (`yearend_readiness_standard_2026.pdf`): 2.1 "At its forecast peak-hour volume, at least 99 percent of the requests customers send an endpoint receive their complete response within 800 milliseconds of reaching the edge", 2.2 the response time "whatever the request meets on the way: the service's own work, a wait for a connection or a database, or a pause of the service's runtime", 2.3 unrounded, 1.2 "thousands of clients, each working to its own schedule", 3.2 the run of record and its measurement, 3.3 "The run of record stands for the endpoint at its forecast peak hour. A run at or above the forecast peak-hour volume is evidence for that volume: no allowance is made for the difference between the two."
No decoy: no memo, briefing, draft, dashboard or stakeholder figure states an endpoint's percentile or ranks the endpoints; the test plan gives threads, pacing, the schedule and the campaign log and no results; the APM trace sample and the slow query log answer other questions.
No certified replay: no published or certified percentile is shipped to be reproduced, and the method is not recovered from controls.
Lesson: a load test whose clients wait for each response before sending the next records the pauses of the system it measures once per blocked client, so its percentile describes the requests the test managed to send, not the requests customers would send; the response times customers see are rebuilt from each pod's pause record and the service times, and the textbook back-fill, built for one server and for clients that would have sent everything to it, overstates a pause on one pod behind a balancer. No build on file estimates a distribution from a sample its own instrument thinned during the slow moments (task180's and task268's losses followed a class, task264's members were drawn in proportion to a count).

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 the recorded 99th percentile with the warm-up minutes in | 3.2 sets the warm-up aside | the run's first requests | none | none | none | one percentile | readable |
| R1 (the default path) the recorded 99th percentile of each run of record's measurement | none: the standard files the population and the evidence, not how the test's sample relates to it | the response-time columns | the performance engineer's first figure | none | none | one percentile | readable |
| R1b the requests a pause touched set aside | none | the GC log joined to the requests | treating a pause as an outlier | none | none | one filter | readable |
| R1c the GC log's summaries: a pause longer than 800 ms, or more than 1 percent of time paused | none | the GC log's durations | the collector-tuning reading | none | none | one column | readable |
| R1d HdrHistogram's back-fill at each client's expected interval | none | the threads and the achieved throughput | the textbook repair for coordinated omission | none | none | one correction | readable |
| R1e the back-fill on the requests a pause touched, the interval times the pods | none | servedBy and the pod count | the back-fill adjusted for the balancer | none | none | one correction | readable |
| R1f the rebuild over customers' arrivals with the recorded response times as service times | none | the response times and the pauses | the simulation without separating a request's own time from the pause it met | none | none | one simulation | readable |
| R1g the rebuild on one timeline carrying every pod's pauses | none | the GC log by service | the endpoint read as one server | none | none | one simulation | readable |
| (decisive) R2 the rebuild over customers' arrivals, each to a pod in rotation, each taking a recorded service time and held by its own pod's pauses | none: the standard says the requests customers send and the run of record, and no file says that the clients' blocking thinned the record during each pause | no column flags a missing request; the pause record sits in another file, at another grain, in two time bases | none: dropping the paused requests, the back-fill and the pooled timeline each name another set | none: no shipped figure ties under either reading | none: the battery passes on the records as written (each request once, every run complete or stopped and repeated, every pod in the export) | one simulation once the selection is seen | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | within 800 milliseconds of reaching the edge | the response time the test client records, the clients sitting in the edge's own zone | the server-side span (up to a millisecond shorter) | same call (asserted) | standard 2.2; test plan 3 |
| SF2 | at least 99 percent | the share of the requests customers send that get their response within 800 ms, at least 0.99 | the 99th percentile by linear interpolation or by nearest rank | same call: the share within 800 ms is under 0.99 for exactly the five (asserted) | standard 2.1 and 2.3 |
| SF3 | run of record | the last complete run, minutes 3 to 13 | the first runs' measured minutes pooled with it (EP05, EP13, EP20) | same call (asserted) | standard 3.2 |
| SF4 | a run's first three minutes | three minutes from the run's first request | from a start up to a quarter second earlier | same call (asserted) | standard 3.2; test plan 4 |
| SF5 | a pause of the service's runtime | the stop-the-world pauses the log names Pause | G1's concurrent cycles counted as pauses too | same call (asserted) | standard 2.2; the JVM's own labels |
| SF6 | complete response | every response, the rare 500s included | the 500s left out | same call (asserted) | standard 2.1 |
| SF7 | at its forecast peak-hour volume | the run of record, at or above the forecast, stands for the forecast volume | the pauses scaled down to the forecast's volume | not open: filed | standard 3.3 |
| SF8 | the service's pods | every pod of the service, each an equal share of arrivals (the edge turns requests across them in rotation) | pods weighted by their recorded share | same call (asserted: the shares are equal) | test plan 3 |
| SF9 | 800 milliseconds, unrounded | the figure compared unrounded | rounded to tens first | same call: no endpoint within 90 ms (asserted) | standard 2.3 |
| SF10 | busiest clock hour of January (Ask A) | hours beginning on the hour, UTC | Eastern hours, January in Eastern time | same figures: the offset is whole hours and no busiest hour sits within five hours of the month's edges (asserted) | standard 7 (Clock hour) |
| SF11 | requests the endpoint served customers (Ask A) | the edge's count less the uptime monitors running that month, the old path only up to its rename | the old path's redirects counted, or the later checks taken off | Ask A only (asserted different) | standard 4.1 and 7 (Customer); the changelog's 308 redirects; the monitors' created dates |
| SF12 | an employer counts on a day when its subscription covers that day (Ask A) | the account's state on the day | an account counted on the day an event takes effect | same figures: no event on 1 January or 1 November (asserted) | standard 4.2 |
| SF13 | credits customers were issued (Ask B) | each credit once, at the amount issued | a carried-forward balance counted as a credit | Ask B only (asserted different) | standard 5.2; the new system's memo on each carried balance |
| SF14 | breaches from 1 January to 31 October (Ask B) | dated by the day the incident began, Eastern | its end, or UTC | same figures: no incident within a day of either edge (asserted) | standard 5.2; the incident register |
| SF15 | the time on a GC line | the pause's end (the line is written when the pause ends) | the pause's start | EP06 joins the five (asserted different) | test plan 6: "The JVM writes a pause's line when the pause ends, with its duration" |

## Ladder

Built figures from the cut pack (`generator/analysis.py`, every route in `generator/models.py`, asserted in `generator/checks.py`, recomputed by `generator/verify.py`). 99th-percentile response time at the forecast peak, milliseconds; the five golden endpoints and the two nearest rivals, EP06 and EP08:

| Rung | Construction | EP01 | EP02 | EP05 | EP16 | EP22 | EP06 | EP08 | Endpoints named | What kills it |
|---|---|---|---|---|---|---|---|---|---|---|
| R0 | recorded, warm-up in | 996 | 1,025 | 740 | 981 | 1,193 | 282 | 710 | 4 (EP01, EP02, EP16, EP22) | 3.2 sets the warm-up aside, and the record is still thinned |
| R1 (the default path) | recorded, run of record's measurement | 574 | 874 | 740 | 963 | 1,084 | 269 | 692 | 3 (EP02, EP16, EP22) | the clients sent nothing while their pod was paused |
| R1b | the requests a pause touched set aside | 407 | 408 | 501 | 308 | 668 | 217 | 614 | none | the pauses are what customers meet |
| R1c | a pause longer than 800 ms in the window | 4,086 | 2,958 | 2,648 | 2,024 | 2,849 | 2,753 | 229 | 8 (every ParallelGC endpoint) | a long pause is not a breach unless enough arrivals meet it |
| R1c | more than 1 percent of time paused | 2.8% | 2.9% | 3.0% | 3.6% | 2.9% | 2.6% | 1.2% | 22 (all but the two ZGC endpoints) | a short pause holds a request for less than its length |
| R1d | HdrHistogram back-fill, each client's interval | 1,632 | 1,291 | 1,219 | 1,164 | 1,360 | 882 | 1,146 | 10 (adds EP06, EP07, EP08, EP19, EP20) | credits each blocked client with every request it would have sent to the paused pod, and back-fills requests slow on their own |
| R1d | back-fill on the paused requests only | 1,635 | 1,292 | 1,231 | 1,165 | 1,387 | 883 | 810 | 7 (adds EP06, EP08) | the same, one server assumed |
| R1e | back-fill on the paused requests, interval times the pods | 865 | 922 | 740 | 1,033 | 1,113 | 270 | 692 | 4 (misses EP05) | a blocked client's next request goes to any pod |
| R1f | the rebuild, recorded response times as service times | 1,605 | 1,470 | 1,423 | 1,373 | 1,581 | 1,040 | 700 | 6 (adds EP06) | counts each recorded pause twice |
| R1g | the rebuild on one timeline of every pod's pauses | 2,330 | 1,974 | 2,286 | 1,396 | 1,868 | 1,685 | 710 | 7 (adds EP03, EP06) | a pause holds only its own pod |
| R2 (golden) | the rebuild per pod, 2,000,000 arrivals | 1,037 | 986 | 930 | 1,123 | 1,233 | 428 | 689 | 5 | none |
| R2 | another seed, 1,000,000 arrivals | 1,031 | 982 | 891 | 1,127 | 1,226 | 428 | 677 | 5 | none |
| R2 | service times from the untouched requests only | 1,058 | 968 | 930 | 1,122 | 1,194 | 436 | 625 | 5 | none |

The family closes on the call: every member's verdict is the same on every endpoint, the closest to the line EP05's second seed (891 ms, 91 ms over) and EP08's first (689 ms, 111 ms under). The clean truth (the generator's own requests and pauses) names the same five.

The world under it: 16 services on three collectors (ParallelGC with young collections of 22 to 48 ms at 14 to 26 a minute and full collections of 0.9 to 2.3 s at 0.45 to 1.5 a minute; G1 with young pauses of 18 to 70 ms, mixed pauses of 110 to 260 ms and concurrent cycles with short Remark and Cleanup holds; ZGC under a millisecond); two to five pods a service behind a round-robin edge; each endpoint's service time lognormal (median 60 to 230 ms), the four heavy endpoints with 0.4 to 0.85 percent of requests slow on their own (0.9 to 1.5 s); two to five client threads with 80 to 350 ms of pacing; a pause holds every request in flight on its pod and every request that reaches the pod while it lasts.

Position and separation: EP05 is the recorded route's nearest miss below the line (740 ms) and 891 to 930 ms rebuilt; EP01 is recorded at 574 ms and rebuilt at 1,031 to 1,058 ms (its pods' full collections reach 4.1 s, and three clients met each once). The clean-data test (ANALYST TEST in `checks.py`): on the generator's own rows, every field read and every filed rule applied, the recorded percentile files the three, and the decisive step alone files the five.

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | the requests customers send the endpoint at its forecast peak hour, arriving on thousands of clients' own schedules | filed: standard 1.2 and 2.1 |
| 2 Unit of account | the request | filed: standard 2.1 |
| 3 Attribution window | the forecast peak hour, stood for by the run of record's measurement | filed: standard 3.2 and 3.3 (SF7) |
| 4 As-of dating | the campaign of 10 to 19 November 2026 on build 2026.11.2 | filed: test plan |
| 5 Version basis | the last complete run of each endpoint | filed: standard 3.2 (SF3) |
| 6 Denominator | every request customers send, errors included | filed: standard 2.1 (SF6) |
| 7 Weighting | each request once; each pod an equal share of arrivals | C1 (SF8) |
| 8 Window length | ten minutes after three of warm-up | filed: standard 3.2 (SF4) |
| 9 Boundary inclusivity | at least 99 percent within 800 ms | filed: standard 2.1 (SF2) |
| 10 Rounding path | compared unrounded; verdicts only are graded | filed: standard 2.3; the prompt (SF9) |
| 11 Tie-break | none needed | C1 asserted (SF9) |
| 12 Maturity and censoring | no request reached the 30-second timeout | C1 asserted |
| 13 Order of operations | conform, run of record, pauses, service times, rebuild, compare | C1 |
| 14 Row order | none matters | C1 |
| 15 Duplicate resolution | each request once in the results | C1 asserted |
| 16 Identity normalisation | pod names in servedBy, in served_by and in the GC export | test plan 3 and 6 |
| 17 Netting against gross | none | C1 |
| 18 Dimensional units | milliseconds in the results and the pause lengths, seconds of uptime, UTC-05:00 wall clock, each GC line stamped at its pause's end | test plan 6 (SF15) |
| 19 Code and status semantics | Pause lines against concurrent and summary lines; 500s | the JVM's labels (SF5); standard 2.1 (SF6) |
| 20 Integerisation | the count of endpoints | the prompt |
| 21 Clause scope | sections 2 and 3 for the call; sections 4 and 5 for the workbook's figures | filed |
| 22 Forward window contents | the January 2027 peak stood for by the November run of record | filed: standard 3.3 (SF7) |

## Literal reader

Executed word for word, the standard files each endpoint's verdict on the requests customers send it at its forecast peak hour, at least 99 percent of them getting their complete response within 800 milliseconds of reaching the edge, the time spent in a pause of the service's runtime included, and makes the run of record the evidence for the endpoint at that hour. The records give every request the test's clients sent, with the pod that served it, and every pause of every pod; the literal estimand counts the requests customers send, and customers are thousands of clients working to their own schedules, so their requests reach a pod whether or not it is paused, while the test's two to five clients each waited for its response before sending again. Read over the requests the clients sent, the percentile describes a sample their own blocking thinned during each pause; read over the requests customers send, each arrival lands anywhere in the measurement window on any pod and meets that pod's pauses in proportion to their length. The rebuild over arrivals, each taking a service time the run recorded and held by its pod's pauses, is that reading; the family closes on five endpoints (Ladder).

## Oracles

No shipped figure states an endpoint's percentile at the peak, ranks the endpoints or gives a verdict. The test plan's threads and pacing are the instrument's settings, the same for every reading. The APM trace sample is one test day's spans, one request in a hundred, from the same closed-loop clients, and the slow query log is the database's; neither ties under any reading.

## Ask sheet

The asks are decoupled from the call: neither reads a load-test result, a pause or a pod, and the call computes from the load-test results, the GC log export, the pod events and the register's Services sheet alone (asserted). They are the two figures the standard's section 6 puts beside every endpoint's verdict in the readiness workbook, measures every endpoint carries that the call does not turn on: the volume the January 2027 peak will bring and what the endpoint's breaches cost this year.

**Ask A. Each endpoint's forecast peak-hour volume for January 2027, whole requests an hour (24 figures).**
- H18 home: standard 4.1 and 6.1, the forecast the verdict is stated at.
- Use: the workbook's Readiness sheet.
- Path: the edge's hourly counts, the uptime monitors, the changelog, the endpoint register's routes and plans, the CRM's accounts and the billing system's subscription events: six files, about fourteen columns.
- Primary device (D8, an anchor on the current record, not the first): the CRM's subscription_start is the start of the account's current subscription. The card processor change of 2 March cancelled 118 subscriptions whose saved card failed, and 97 of those employers signed again in March and April, so their subscription starts in 2026 though they were customers on 1 January; read as the start of their custom they fall out of 1 January's count on every plan, and every forecast comes out high by 216 to 1,135 requests an hour (asserted on all 24).
- Hazards: the uptime monitors running in January are in every hour's count (23 of 24 endpoints high; the two monitors created after January taken off too makes 3 low); the three routes renamed in January answered their old paths with a permanent redirect, so the old path counts customers' requests up to the rename and only redirects after it (the current path alone misses EP09 and EP24, both paths in every hour misses EP09, EP19 and EP24); plan changes not undone (14 endpoints); accounts cancelled during the year are no longer in the CRM (every endpoint high).
- Stops (asserted): the cracker's employer counts miss all 24; current plans on both days miss all 24; the accounts no longer in the CRM left out miss all 24; the monitors' requests left in miss 23; the answer.

**Ask B. Each endpoint's service credits for breaches from 1 January to 31 October 2026, net of reversals, to the nearest dollar (24 figures).**
- H18 home: standard 5.2 and 6.1, what a breach costs beside each verdict.
- Use: the workbook's Readiness sheet.
- Path: the legacy credits, the new system's credit notes, the status page's incidents, the changelog and the register: five files, about twelve columns.
- Primary device (D1, the same records under two systems, the reflex repair wrong): the legacy credits still open on 30 April were carried into the new system on 1 May at their unapplied balance, under new numbers and with no reference to the legacy number, while the legacy export still lists them as issued at the full amount. Counted in both systems every endpoint is high; matched on account and incident and kept as the new system holds them, the system of record, every endpoint is low by the part already applied, 20 to 3,145 dollars (asserted on all 24: each endpoint carries at least one partly applied credit for a breach in the window).
- Hazards: legacy amounts in cents; void legacy credits; credits issued in January for December's incidents and in November for October's; reversals; the old route names on the incidents before each rename; incidents on the web and mobile apps.
- Stops (asserted): both copies counted misses all 24; the new system's copy kept misses all 24; the answer.

Main population zero-counts: device rows in the call's files: 0 (asserted: the call's computation opens the load-test results, the GC export, the pod events and the register only, and no ask file shares a row with them).

| Hazard | Asks moved | Per-ask delta (measured on the cut pack) |
|---|---|---|
| accounts cancelled on 2 March and signed again | A | every A high, 216 to 1,135 requests an hour |
| accounts cancelled during the year, gone from the CRM | A | every A high on the CRM alone |
| uptime monitors' requests in the edge counts | A | 23 of 24 A high |
| renamed routes and their redirects | A, B | A on EP09, EP19, EP24; B on their incidents before each rename |
| legacy credits carried forward at their balance | B | every B off, high counted twice, low kept as the new system holds them |
| legacy amounts in cents | B | every B with a legacy credit off by a factor of 100 on those credits |

Referee: none (Oracles).

| Ask figure | The cracker's figure against the golden | Cracker (lands the call, runs the battery: each request once, every join checked, the CRM against the events; executes sections 4 and 5 with the monitors' requests off, the redirects set aside, the plan changes undone, the cancelled accounts added back, cents converted, reversals netted, each credit found in both systems kept once as the system of record holds it) |
|---|---|---|
| A, each endpoint's forecast peak-hour volume (24) | 216 to 1,135 high: the accounts cancelled on 2 March and signed again dropped from 1 January | miss |
| B, each endpoint's net service credits (24) | 20 to 3,145 low: the carried-forward balances kept in place of the credits issued | miss |

Mirror leakage: 0.0 per cent of the ask weight (the mirror, off the call, reads the current route only with the monitors' requests in, both days' employers on their current plans, and every credit in both systems, and keeps none of 48 figures).
Pair ceiling: 28.5 (the cracker 45.0: the call, its components and instruction-following, none of the 48 ask figures; the mirror 12.0), measured on the cut pack.
Measured by: `generator/cracker.py` on the cut pack (`checks.py` runs it and asserts every miss).

## Leak check

`leak.py --asof 2026-11-20` (build 4, target.zip 837ff5a0): REVIEW, no LEAK; each line harmless:
- `yearend_peak_loadtest_plan_2026.docx` carries 20 of 23 words of the call: Table 1 lists all 24 endpoints' codes and routes with their threads and pacing, the five no differently from the nineteen; it carries no result.
- `yearend_peak_loadtest_plan_2026.docx`, 4 stump-paragraph terms (record, request, client, sample): "run of record" is the standard's term, "sample" JMeter's own word for a request, and the clients are the plan's description of its workload; none says that the record under-samples a pause.
- `yearend_readiness_standard_2026.pdf`, 6 stump-paragraph terms (record, clients, request, client, outcome, records): the estimand's own nouns (2.1, 3.2) and 1.2's population; "outcome" is 1.3's freeze list.
- Earlier sweeps renamed three files the author's vocabulary matched (a trace sample, a monitors file named for synthetic checks, a plan named load_test) and took a generated_at key and a SQL NULL out of two exports.

## Architecture 1 record (spent 2026-10-22)

Closed-loop load tests and each pod's garbage-collection log: each endpoint's 99th percentile at the forecast peak over the requests customers send, rebuilt from the run of record's service times and every pod's pauses (golden EP01, EP02, EP05, EP16, EP22), against the recorded percentile (EP02, EP16, EP22) and HdrHistogram's back-fill (ten). Stage 3 green on target.zip 837ff5a0. Stage 4: both isolated scored readers (r273a, r273b) named coordinated omission, ran the per-pod open-arrival rebuild and landed the call (r273b every ask figure, 48 of 48; r273a Ask A 24 of 24 and Ask B 12 of 24); each pointed at standard 1.2 ("thousands of clients, each working to its own schedule") with 2.2's pause clause and the plan's closed workload, the sentences the estimand needs to be determinate. The judge DETERMINISTIC, APPROVE, Gate G method_or_model_selection, Gate H pass. The asks' devices failed with the call: the backward walk of the subscription events, which a strong solver runs anyway, undoes the re-signed accounts' anchor, and the carried-forward memo names the migration's balances.

## Tried and rejected

- The seed's world (an open-source security fund's 60 maintainer stipends to the eligible packages with the most dependents, at most 20 from one ecosystem), set aside at the draw on 2026-10-22: its quantities are counts the fund's filed rules fix (dependents as the certification counted them, monthly downloads, the cap per ecosystem), so its only decisive steps are grain, identity or rule application, which the three rules bar; the seed's own stump (dependent projects against dependent packages) is a grain reading.
- The same mechanism prototyped with one-second think times (`co1.py`, first setting): each thread then misses only one or two sends per pause and the recorded percentile sits within a few per cent of the rebuilt one; the test clients send back to back, as a throughput test at a fixed thread count does, so a two-second pause costs each blocked client dozens of sends.
- A blanket time weighting of the recorded requests (each weighted by its own response time): it credits every slow request, stalled or not, and flags most endpoints; recorded as a reflex, not a candidate.
- Architecture 1 (the closed-loop load test's coordinated omission, rebuilt per pod from the GC log), spent at stage 4 on 2026-10-22: both isolated readers recognised the closed workload's under-sampling of the pauses from the plan's workload paragraph and the standard's population and pause clauses (the WHAT the call needs to be determinate) and ran the open-arrival rebuild; a mechanism a field's practitioners know by name and a model reaches from the estimand's own sentences is landable whatever the ladder, and the asks' devices (a backward walk of the events, a memo naming the balance) were each one solver step from the answer.
