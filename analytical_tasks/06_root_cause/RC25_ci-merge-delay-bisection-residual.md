# RC25 — Which cause of the CI slowdown gets the platform team's one programme, when the costliest delays are recorded as neither failures nor triage

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Product Analytics · developer productivity and CI reliability |
| Mirrors | Build and deploy pipeline reliability at large engineering organisations (Google's presubmit and merge queues, Meta's diff testing, GitHub merge queues at scale), where a flaky test's real cost is the bisection it sets off, filed as superseded builds rather than failures |
| Decision shape | Which of N root causes gets the fix: the platform team's one programme next quarter |
| Committed call | The programme funded, and the merge-delay hours it would have removed this quarter |
| Gap · Pattern | Gap 2 (population) · S2 (a residual population between two correct records: merge-queue delay that is in neither the failed-build log nor the triage tracker), with E20 (an implicit join: merge-queue builds reach their pull requests only through the batch log) at rung 1 |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #18 joins only on the visible key · #7 uses the ready-made measure · #11 beats the headline trap, misses the quiet one |
| Calibration form | Counterparty acknowledgement file: the hosted CI vendor's accepted and rejected infrastructure claims for four quarters |
| Driving force | When a batch in the merge queue fails, the queue splits it and re-tests the halves, filing the follow-up builds as superseded rather than failed. A real defect is found in one split. A flaky test that fails once and then passes sends the queue through every split and back to a full re-run, while all the batch's pull requests wait. Those waits sit in neither the failed-build log nor the triage tracker, and appear only as the queue's waiting time less normal queue time less the delay recorded failures explain: 2,600 hours, 94% of them set off by flaky tests. |

## 1. Situation

A large open-source project's pull requests now wait far longer to land; its CI failure rate rose from 12% to 21% of builds. Long-time maintainers blame
newer contributors; the release manager blames upstream breakages; the infrastructure lead blames the self-hosted runners. The platform team has one
programme next quarter: tighter review gates (A), flaky-test remediation (B), dependency pinning (C), runner capacity (D) or build-cache hardening (E).
The platform charter says how the programme is chosen. Pull requests merge through a merge queue that tests them in batches; ordinary pull-request
builds run on the hosted CI vendor's runners, whose infrastructure failures the vendor acknowledges under its service agreement.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the build log, the triage tracker's classes, the merge queue's batch log and timestamps, the vendor's
  acknowledgements. The new contributors, the upstream breakages and the slow runners are all real. Nothing reported is overturned; the costliest
  delay is a population recorded in neither stream.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete every voice and the licensed basis. Delay per recorded failure, the careful build, still names the runners.
* **Instrument repair.** Suspect file: the build log's author field, which credits the 61% of failed builds that are queue builds to the queue's
  bot rather than to the authors of the pull requests in the batch. Repaired so that every build carries its pull requests' authors, rung 0
  still names A, now on every failure, rung 1 C and rung 2 D; none names B. The batch log and every timestamp are complete, superseded is the
  correct status of a build that found nothing wrong, and no field anywhere records the waiting a failure caused: rung 2 measures holds from
  timestamps. The answer still needs the residual waiting traced through each bisection chain to the failure that set it off.
* **Lens swap.** The naive build prices failures; the answer prices the waiting failures cause, including waits no failure record carries, a
  different population of delay.

## 3. The driving force

A strong solver ignores the failure rate and prices what the charter scores: hours pull requests wait to merge. Merge-queue builds are committed
by the queue's bot, so it links them to their pull requests and failing tests through the batch log, and classifies each failure by the triage
rules. It then measures the hold each recorded failure put on its batch from the batch log's timestamps rather than assuming a mean, and runner
timeouts, which hold a batch for an hour each, put runner capacity on top. Every recorded failure is accounted for, and the delays they explain
fall 2,600 hours short of the queue's waiting time once normal queue time is removed. The gap is the queue's bisection. After a failed batch the
queue re-tests halves and quarters, filing those builds as superseded, which the build log does not count as failures and the tracker never
sees. A real defect is isolated in one split. A flaky test that fails once and then passes leaves every split green, so the queue exhausts its
splits and re-runs the whole batch while its pull requests wait. Traced through the batch log to the failure that set each chain off, 2,450 of
the 2,600 hours belong to flaky tests.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Failed builds by the committing author's tenure, priced at the mean merge delay | A, review gates (2,600 hours) | The maintainers' own view, from the build log's own author field | The batch log: 61% of failed builds are queue builds committed by the bot, which the author field credits to nobody |
| 1 | Failures linked through the batch log to pull requests and failing tests, classified by the triage rules, priced at the mean delay | C, dependency pinning (2,300) | Every failure linked and classified; dependency breakages hit many pull requests at once | The batch log's timestamps: the hold a failure puts on its batch ranges from 6 minutes to 3 hours, and the mean misprices every class |
| 2 | The same, each failure priced at the hold it put on its batch, from the batch log's timestamps | D, runner capacity (2,700) | Every recorded failure priced exactly; the vendor's acknowledgements reproduce the infrastructure class | The queue log: waiting time less normal queue time exceeds the delay recorded failures explain by 2,600 hours |
| 3 | **Decisive:** the residual waiting traced through the batch log to the failure that set off each bisection chain, and added to its cause | **B, flaky-test remediation (4,250)** (4th of 5 on rung 0) | — | — |

* **Position table.** B ranks 4th on rung 0 and 3rd on rungs 1 and 2, and leads only rung 3. Rung leaders beat their runners-up by 1.86×,
  1.53×, 1.29× and 1.57×.
* **Discriminator dominance.** Runner capacity carries a 1.50× lead into rung 3 (2,700 against 1,800). The residual multiplies the flaky
  class by 2.36 and leaves runner capacity unchanged, an edge of 2.36×, 1.31 times the required 1.2 × 1.50 = 1.80; the net margin is 1.57×.
* **Partial correction priced (L3).** A solver who finds the 2,600-hour gap and spreads it across classes in proportion to each class's measured
  holds keeps runner capacity on top (3,546 against 2,364). One who counts superseded builds as failures of their batch's class adds them at the
  mean delay and names C again.
* **Grid.** Link (author, batch log) × pricing (mean, timestamped hold) × residual (none, pro rata, traced) gives eight feasible builds; author
  builds name A, mean-priced builds C, hold-priced builds D with or without a pro-rata residual, and only the traced residual names B.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The queue's documentation describes batching and splitting; the build log's guide defines superseded. No document says
   bisections cost waiting time or that flaky tests make them exhaustive.
2. **Corpus blind for a computable reason.** *Every acknowledged claim is a build on the vendor's hosted runners, and the merge queue runs on
   the project's self-hosted pool, so no queue build and no bisection appears in any acknowledged case.* The file certifies the infrastructure
   class exactly (412 of 412 decisions reproduce under the triage rules) and cannot see the queue.
3. **No arithmetic symptom.** Builds, failures and classes reconcile; superseded builds are a legitimate status with no failure to count.
4. **Not a row predicate.** The residual is a difference of totals across two logs, and its cause is found by ordering each batch's builds and
   following the chain back to the first failure.
5. **The enumeration is arithmetic.** No column marks waiting as bisection-caused; 2,600 hours are a residual, attributed through chains.
6. **No cutover date.** Flaky failures and bisections run all quarter; the dated events (an upstream major release, a runner pool migration)
   step the failure series and are the decoys.
7. **Survives deletion.** With every voice gone, measured holds still name runner capacity.

## 6. The calibration corpus

* **Form.** The vendor's acknowledgement file: 412 failed builds the project claimed as infrastructure failures over four quarters, each
  accepted or rejected by the vendor after review.
* **What it certifies.** The triage rules' infrastructure class (every acceptance and rejection reproduces) and the build time each acknowledged
  failure cost, measured from the build log's timestamps as rung 2 measures holds.
* **What it is blind to.** The merge queue's bisections (above).
* **Twin pair.** Weeks 19 and 27 carried identical builds, failures by class, pull requests merged and mean batch size. Merge-delay hours were
  1,040 and 500 (2.08×), because week 19's flaky failures fell in eight-PR batches at peak and week 27's in two-PR batches overnight. Only the
  traced residual separates them.
* **Resemblance points at the decoy.** This quarter's failure profile matches the quarter of the runner pool migration on runner timeouts and
  their timing, and that quarter's delay was mostly runners.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The platform charter: the programme goes to the cause whose fix would remove the most hours pull requests waited to merge
  this quarter. The merge queue's documentation of batching and splitting.
* **Empirical pins.** The triage rules and the infrastructure class, from the acknowledgements; normal queue time from batches with no
  failure.
* **Voices.** A long-time maintainer: "Since we opened up to new contributors the build has been red every day." The release manager:
  "Upstream keeps breaking us. Pin the dependencies and most of this goes away."
* **Licensed wrong basis.** The charter records that the steering committee reports CI health as the failed-build rate and will present the
  programme choice on that basis.

## 8. Determinism by construction

* **Waiting.** A pull request waits from entering the queue to merging; normal queue time is the median wait of batches with no failed or
  superseded build, by batch size.
* **Chains.** Every superseded build carries its parent batch id; each chain has one first failure, and its class comes from the triage rules.
* **Attribution.** A chain's waiting is credited whole to the class of its first failure; no chain mixes a real defect and a flaky failure.
* **Window.** The quarter's merges; batches spanning the quarter boundary are assigned by merge time, and none carries a chain.
* **Rounding.** Hours to the nearest hundred; the committed figure sits mid-bin.

## 9. Prompt sketch and deliverables

> Our pull requests are taking far longer to land and the platform team gets one programme next quarter. The infrastructure lead is sure it's
> the runners. Tell me which programme we fund and how many hours of merge delay its cause cost us this quarter, to the nearest hundred, as the
> line for the steering committee. Send `ci_delay_case.xlsx` and a chart `delay_by_cause.png`.

* `ci_delay_case.xlsx` — the five causes under each construction, the suite-duration sheet (ask A), the contributors sheet (ask B) and the
  acknowledgement reproduction (ask C).
* `delay_by_cause.png` — a stacked bar of the quarter's waiting hours (normal queue time, recorded failures by class, bisection residual by
  triggering class), beside one annotated batch's bisection timeline, with the funded cause highlighted.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 8 test suites, median and 95th-percentile duration over the quarter. *Device:*
  sharded suites report one row per shard, and a suite's duration is the longest shard's wall-clock time, as the CI configuration documents;
  summing shards overstates the four sharded suites several-fold.
* **Ask B (device-carried).** For each month, first-time contributors whose pull requests merged. *Device:* the repository's author-mapping
  file merges contributors' alternate emails into one identity, as its header documents; counting raw emails treats 14% of returning contributors
  as new.
* **Ask C (validity).** For each of the 412 acknowledged claims, the vendor's decision and the class the triage rules return; and each cause's
  hours under each rung construction.
* **Decoupling.** Clearing the residual construction changes no figure in asks A or B.

## 11. Rubric arithmetic

8 suites × 2 percentiles (ask A) + 3 months (ask B) + 412 claims scored as one reproduction count per class (4) + 5 causes × 4 constructions
(ask C) + the funded programme, its hours, the residual and the runner-up + 5 named chart parts + 2 files ≈ 55 criteria.

## 12. World-building constraints

* Quarter's waiting 12,400 hours: normal queue 1,500, recorded failures 8,300 (D 2,700, C 2,100, B 1,800, A 1,200, E 500), residual 2,600
  (B 2,450, C 100, A 50).
* Rung figures as in section 4; 61% of failed builds are queue builds committed by the bot.
* Acknowledgements: 412 claims, all on hosted runners, all reproduced by the triage rules.
* Weeks 19 and 27 identical on every build, failure and merge column.
* Shard rows and author mappings touch no queue batch, chain or claim.
