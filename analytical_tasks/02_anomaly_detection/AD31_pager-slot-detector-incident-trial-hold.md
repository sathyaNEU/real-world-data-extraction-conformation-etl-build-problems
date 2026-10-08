# AD31 — Which log detector gets the one pager slot this quarter, or none, when 23 failed blocks are five failures

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Product Analytics · platform reliability engineering |
| Mirrors | Deciding whether a new anomaly detector has earned a pager slot when failures arrive in correlated bursts (storage and compute SRE teams at AWS and Google Cloud, production-engineering alert reviews at Meta, network-assurance detectors at Cisco), where one incident contributes dozens of labelled rows |
| Decision shape | Which of N gets one scarce thing: the quarter's single pager integration slot goes to one of three piloted detectors, or to none |
| Committed call | The detector wired into the pager, or that the slot holds for the quarter, with the evidence figure that decides it, at the reliability review |
| Gap · Pattern | Gap 2 (population: the trial is the incident, not the block) over Gap 3 (objective: the paging class) · hold forced by a computed blocking quantity, with the paging segment coarsened below it |
| Gate G mechanism | signal_vs_noise_or_hold, with method_or_model_selection support |
| Measured traps engaged | #14 coarsens the segment it was asked about · #2 counts file rows instead of the real unit · #1 reports a failed back-test, ships anyway |
| Calibration form | Pilot log: six weeks of shadow running for three candidate detectors and the incumbent rule, every alert and every failed block adjudicated by on-call |
| Driving force | The paging policy admits a detector on its paging class when the pilot establishes recall at 90% confidence. The pilot log has one row per failed block, and on blocks the invariant miner clears the bar comfortably (22 of 23). The 23 replica-loss blocks came from five datanode-loss incidents, and every detector caught all or none of each incident's blocks, 124 of 124 detector-incident pairs. The trial is the incident: four of five caught bounds recall at 0.42, and no candidate does better, so the slot holds. |

## 1. Situation

A cloud storage platform pages on-call for block failures with a rare-line rule that floods the rota. One integration slot is free this
quarter: a single detector can be wired into the pager, and wiring takes the SRE team's quarter. Three detectors ran in shadow for six
weeks: session-level PCA on event-count vectors (P), workflow invariant mining (I) and a vendor's sequence model (V). The paging policy
admits a detector on the paging class (replica-loss failures, from the runbook's class list) only when the pilot establishes recall of at
least 0.80 with the lower 90% confidence bound clearing 0.70, and precision of at least 0.75. On-call adjudicated every alert and every
failure in the pilot log. The on-call lead wants anything but the current rule.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the pilot scorecard, the adjudications, each detector's block counts and the vendor's benchmark
  claims. Nobody's numbers are overturned; on-call is right that the current rule is poor. The difficulty is what the pilot can establish
  about the paging class, given how its failures arrive.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the scorecard and both voices. A block-level evaluation on the paging class, deduplicated as the pager
  deduplicates, still admits I.
* **Instrument repair.** None suspect: the pilot log carries every block's class, incident ID and adjudication and every alert, and the
  pager configuration is filed. A perfect re-adjudication leaves rung 0 at P, rung 1 at V and rung 2 at I, because each counts blocks; the
  incident grain is still needed, and no better record of those six weeks adds a sixth replica-loss incident.
* **Lens swap.** The naive verdict counts 23 block outcomes; the answer counts five incident outcomes. Different trial populations, and the
  verdict moves from a pick to a hold.

## 3. The driving force

A strong solver ignores line-level counts, evaluates per block on the adjudicated pilot, notices that the policy pages on replica-loss
failures rather than on every anomaly, recomputes on that class, deduplicates re-fired alerts as the pager would, and finds I clearing every
condition with a lower bound of 0.84. Every step is correct, and the bound treats 23 blocks as 23 trials. Replica loss is a datanode
event: when a node drops, every under-replicated block it held fails at once, and the pilot log carries each block's incident ID. The log
also shows, for all four detectors and all 31 pilot incidents, that a detector alerted on all of an incident's blocks or on none. Blocks
inside an incident are one outcome counted many times. On five incidents, I and V each caught four and P three, so the best lower bound
is 0.42, and no defensible interval at incident grain clears 0.70.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Block-level F1 over all anomalous blocks in the pilot: P 0.85, V 0.72, I 0.66 | P | The pilot scorecard's own grain, time-ordered and adjudicated | The paging policy pages on replica-loss failures, a class the runbook lists separately, where P's recall is 12 of 23 |
| 1 | Paging class at block grain, recall bound and per-alert precision: V recall 21/23 (bound 0.79), precision 0.79; I precision 0.74 | V | The policy's class and conditions, applied with a confidence bound | The pager configuration suppresses re-alerts on a block already paged; per alerted block V's precision is 0.61 |
| 2 | Paging class at block grain with pager deduplication: I recall 22/23 (bound 0.84), precision 0.81; V fails precision | I | Every condition met, every alert counted as the pager would count it | The pilot log's incident IDs: the 23 blocks are five incidents, and every detector caught all or none of each one's blocks |
| 3 | **Decisive:** recall bound at incident grain for every candidate: I 4 of 5, V 4 of 5, P 3 of 5 | **Hold: no detector takes the slot** | — | — |

* **The blocking quantity.** The best incident-grain lower 90% bound on paging-class recall is 0.42 (I and V, four of five,
  Clopper-Pearson), 0.28 below the policy's 0.70; P's is 0.25. Every candidate fails on the same standard, and each one's reason is named in
  ask C.
* **Partial correction priced (L3).** A solver who sees the incident IDs but widens the block-level interval by a design effect estimated
  across all 31 pilot incidents (1.9 blocks each on average) shrinks I's 23 blocks to about 12 effective trials, gets a bound of 0.77 and
  adopts I, 0.07 above the line; a cluster bootstrap over the five incidents puts I's lower decile at 0.87 and adopts it too. A solver who
  pools all 31 incidents across classes gets I at 29 of 31 (bound 0.84) and adopts it on the wrong class, 0.14 above the line. Every partial
  route lands on I, never on the hold.
* **Grid.** Class (all anomalies or paging class) × alert counting (per alert or per paged block) × trial unit (block or incident) = 8
  cells. All-anomaly cells name P at block grain and I at incident grain (29 of 31); paging-class block cells name V or I; only the
  paging-class incident cells hold, and the deduplicated one holds for the policy's reason.
* **Falsifiable.** Had the pilot seen seven replica-loss incidents and I caught all seven, its bound would be 0.72 and I would take the
  slot.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The policy states the confidence standard and names the class. No document says what a trial is, and the runbook
   describes replica loss operationally (a datanode drops and its blocks under-replicate) without connecting it to evaluation.
2. **Pinned by exhaustion, not by a menu.** *In all 31 pilot incidents, each of the four detectors alerted on all or none of the incident's
   failed blocks, 124 of 124 detector-incident pairs.* The incident is therefore the only unit on which detections are independent;
   nothing is chosen, and every valid interval at that grain (Clopper-Pearson 0.42, Jeffreys 0.48, Wilson 0.51) fails.
3. **No arithmetic symptom.** Block labels, alerts and adjudications reconcile one to one; incident IDs are complete and consistent with the
   datanode event log.
4. **Not a row predicate.** It needs grouping 23 blocks into incidents through the incident ID, verifying all-or-nothing detection across
   124 detector-incident pairs, and an interval on the grouped counts.
5. **The enumeration is arithmetic.** The trial count and each candidate's bound are computed; no column carries either.
6. **No cutover date.** The pilot is one six-week window and nothing in it steps.
7. **Survives deletion.** Remove the scorecard and every voice: the block-level evaluation is still the natural build and still admits I.

## 6. The calibration corpus

* **Form.** The pilot log: every shadow alert from P, I, V and the incumbent rule, every failed block with its class and incident ID, and
  on-call's adjudication of each, over six weeks and 31 incidents.
* **What it certifies.** Every block-level figure on rungs 0 to 2 reproduces exactly from the log, so a back-tester is confirmed at rung 2,
  and the all-or-nothing pattern pins the trial unit (above).
* **Twin pair.** Replica-loss failures and write-pipeline timeouts each have 23 failed blocks in the pilot, and I caught 22 of 23 in both,
  with matching precision. Timeouts came from 21 incidents (I caught 20) and replica loss from five (I caught four), so I's incident-grain
  bounds are 0.83 and 0.42, 2.0× apart, separated only by the trial unit.
* **Resemblance points at the decoy.** On block counts, I's replica-loss record is indistinguishable from its timeout record, which clears
  the bar, so a lookup across classes reads I as admissible.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The paging policy: the paging class, recall of at least 0.80 with the lower 90% bound clearing 0.70, precision of at least
  0.75, and an empty slot when no detector qualifies. The runbook's class list. The pager configuration's suppression of re-alerts on a
  block already paged. One sentence each.
* **Empirical pins.** The trial unit, by exhaustion over 124 detector-incident pairs.
* **Voices.** The vendor's account manager: "Our model posts the best F1 on public storage-log benchmarks." The on-call lead: "Anything
  beats the rare-line rule; pick one and ship it."
* **Licensed wrong basis.** The reliability review's terms record that the SRE council compares detectors on block-level F1 over all
  anomalous blocks and will bring its scorecard to the review.

## 8. Determinism by construction

* **Interval method.** At block grain every standard interval admits I (Clopper-Pearson 0.84, Wilson 0.87); at incident grain every one
  fails (0.42 to 0.51), so the method is not a fork.
* **Incident membership.** Each failed block carries exactly one incident ID, and the incident's datanode and time agree with the datanode
  event log for every block.
* **Deduplication.** The pager suppresses re-alerts per block for the life of the failure, so per-block and per-failure counting agree.
* **Window.** The pilot window is fixed at six weeks; no incident straddles its boundaries.

## 9. Prompt sketch and deliverables

> We have one detector slot on the pager this quarter and the rota is drowning under the rare-line rule. On-call would take anything over
> what we have. Tell me which detector gets wired in, or that none should be this quarter, in one sentence for the reliability review, with
> the figure that decides it to two decimals. Send `detector_case.xlsx`, a chart `pilot_evidence.png`, and a one-page `slot_memo.pdf`.

* `detector_case.xlsx` — each candidate under each rung's basis (ask C), the shipper sheet (ask A) and the acknowledgement sheet (ask B).
* `pilot_evidence.png` — for each detector, paging-class recall with its lower bound at block grain and at incident grain side by side, the
  0.70 line drawn and labelled, the five incidents shown as caught or missed, and the verdict in the title.
* `slot_memo.pdf` — the committed verdict, the blocking quantity, and what would have made it a pick.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 12 storage racks, the share of the pilot window its log shipper was healthy and its
  longest outage. *Device:* shippers upgraded mid-pilot report heartbeats in epoch milliseconds where older ones report seconds, as the
  shipper changelog records; mixing them invents outages on five racks. No pilot failure fell inside a shipper outage, so the verdict never
  uses heartbeat data.
* **Ask B (device-carried).** For each of the four runbook classes, the median and 90th-percentile minutes from first page to
  acknowledgement under the current pager over the last twelve months. *Device:* when the primary does not acknowledge, the escalation
  record holds the secondary's acknowledgement, and the tracker guide defines acknowledgement as the first by anyone on the rota. Reading
  only the primary's field overstates two classes.
* **Ask C (validity).** Each detector's verdict and bound under each of the four rung bases, and the twin classes' bounds.
* **Decoupling.** Clearing the incident grouping and the paging-class restriction changes no figure in asks A or B.

## 11. Rubric arithmetic

12 racks × 2 (ask A) + 4 classes × 2 (ask B) + 3 detectors × 4 bases (ask C) + the committed verdict, the blocking quantity, the incident
count and the falsifiability count + 5 named chart parts + 3 files ≈ 56 criteria.

## 12. World-building constraints

* Paging class: 23 failed blocks from five incidents of 9, 6, 5, 2 and 1 blocks. I misses the 1-block incident, V the 2-block incident, and
  P catches the 9-, 2- and 1-block incidents (12 blocks).
* All 31 pilot incidents show all-or-nothing detection for all four detectors.
* V re-fires on persisting benign anomalies, so its precision falls from 0.79 per alert to 0.61 per paged block; I's rises from 0.74 to
  0.81.
* Timeouts: 23 blocks over 21 incidents (19 of one block, two of two), I catching 20 incidents and 22 blocks. The other five pilot incidents
  hold 13 blocks, all caught by I, so I catches 29 of 31 incidents in all.
* Shipper heartbeats and acknowledgement records never touch the pilot log's alerts, blocks or adjudications.