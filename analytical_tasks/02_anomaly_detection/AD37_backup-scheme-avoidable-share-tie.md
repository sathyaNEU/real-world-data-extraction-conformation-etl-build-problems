# AD37 — Which job families go on the speculative-backup list, when four of them tie at "every late job had a straggler"

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Product Analytics · cloud batch platform operations |
| Mirrors | Straggler mitigation and speculative execution on large batch platforms (backup tasks at Google, Alibaba and Microsoft), and more broadly crediting a remedy with outcomes that an upstream delay had already decided (data-pipeline SLAs at Meta and Amazon, CI build acceleration at large engineering organisations) |
| Decision shape | A structure the body adopts: the backup scheme's admission list for the second half, scored on settled SLA credits avoided net of backup compute, under the 5% extra-instance cap |
| Committed call | The job families admitted to speculative backups, and the net saving they should deliver over the half, at the platform review |
| Gap · Pattern | Gap 3 (objective: avoidable credits, not credits at risk) over Gap 2 (population: late jobs a straggler alone made late) · a saturated tie broken by the lowest value consistent with every file of record, with the deciding comparison (credits avoided against backup charges) below it |
| Gate G mechanism | decomposition_attribution, with binding_constraint support |
| Measured traps engaged | #19 breaks a big tie instead of questioning it · #20 leaves the deciding comparison unstated · #4 never tests its reading against the control |
| Calibration form | Settled-transaction ledger: the settled SLA-credit and compute-charge ledgers from last half's pilot of backups on two other families |
| Driving force | Four families tie at 1.00 on the share of their SLA credits that backups would avoid, because every one of their late jobs carried a straggler. The capacity policy states shares at the lowest value consistent with every file of record, and the dependency log is one: in D most late jobs received their inputs too late to finish on time even with no straggler. Building each late job's counterfactual finish (input landing, then every stage at its sibling-median speed) breaks the tie: F stays at 1.00 and E falls only to 0.93, while D drops to 0.38, and C, at 0.97, still costs more in GPU backups than it saves. The policy's own tie-break would have spent the cap on D. |

## 1. Situation

A cloud batch platform will turn on speculative backups (a second copy of a slow instance, launched on another machine) for the second
half. The capacity policy caps backups at 5% extra instances, which leaves room for about two of the six job families. It admits families
in order of the share of their SLA credits that backups would have avoided, states that share at the lowest value consistent with every
file of record, breaks ties by credits at risk, and admits a family only if its avoidable credits exceed its backup charges. The platform
holds the instance tables, the job dependency log (when each job's inputs landed), the SLA register and settled credits, the chargeback
price list, and the settled ledgers from last half's pilot on two other families. The scheduler team wants the two families that paid the
most credits.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the credits paid, the straggler counts, the charges, the input landing times and the pilot's settled
  results. The scheduler team is right that A and B paid the most. Nothing reported is overturned; the difficulty is which of a family's
  credits a backup can actually avoid.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the scheduler team's view and the credit totals. The sibling-relative straggler build still ties four families at
  1.00 and still lets the tie-break choose.
* **Instrument repair.** Record every instance and every credit perfectly: they are. A late job with a straggler is still late with a
  straggler; whether removing it would have saved the deadline depends on when the inputs landed, a fact in another file.
* **Lens swap.** The naive population is late jobs that carried a straggler; the answer's is the subset a straggler alone made late, a
  different set of jobs reached by a counterfactual, not the same set under a new lens.

## 3. The driving force

A strong solver drops credits paid (A's and B's late jobs barely carry stragglers), finds stragglers against their siblings at decision
time, computes avoidable shares, sets avoidable credits against backup charges as the policy requires, removes C for costing more than it
saves on GPU instances, and lets the documented tie-break pick D and E from the remaining tie at 1.00. Every step is correct, and the tie
is the tell. A share of 1.00 says every late job with a straggler would have made its deadline had the straggler been rescued, which holds
only if the job could have finished on time at all. The dependency log records when each job's inputs landed, and for most of D's
late jobs that was after the latest start that could still meet the deadline at sibling-median speed. The lowest share consistent with the
dependency log, the instance tables and the SLA register is a counterfactual per late job, and it leaves only F at 1.00.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Credits paid last half ($k): A 900, B 760, C 610, D 520, E 430, F 380; the two largest within the cap | {A, B} | Money lost is money to win back | The policy ranks by avoidable share, and only 120 of A's and 150 of B's credits sit on jobs with a straggler |
| 1 | Avoidable share with every straggler-job credit counted (A 0.62, B 0.71, C to F all 1.00), tie broken by credits at risk | {C, D} | The policy's ranking and its written tie-break | The deciding comparison: C's backups run on GPU instances and cost $610k against $560k avoided |
| 2 | The same shares with the policy's charge test stated (C fails), tie among D, E, F broken by credits at risk | {D, E} | Ranked, charge-tested and tie-broken exactly as written | The dependency log: most of D's late jobs received their inputs after the latest start that could still meet the deadline |
| 3 | **Decisive:** each late job's counterfactual finish (input landing, then every stage at sibling-median speed) against its deadline; shares C 0.97 (out on its charges), D 0.38, E 0.93, F 1.00 | **{E, F}, saving $651k net** | — | — |

* **Structure table.** Four different admission lists. The answer appears on no lower rung, and its net saving ($331k from E and $320k from F)
  is computed only at rung 3.
* **Separation at the decisive rung.** The tie at 1.00 becomes F 1.00, C 0.97, E 0.93, D 0.38. C stays out on the charge test, and E leads D
  by 2.45× on the policy's ranking basis where rung 2 had them level, and D's avoidable credits fall to $182k against E's $381k.
* **Partial correction priced (L3).** A solver who sees late inputs but removes only jobs whose inputs landed after the deadline itself (not
  after the latest feasible start) gets shares C 0.99, D 0.98, E 0.95, F 1.00, because most of D's input-bound jobs land between the two
  times, and admits {F, D} with a net of $730k: a wrong list and a figure 12% above the answer's. A solver who breaks the naive
  tie by job count instead of credits also admits {D, F}.
* **Grid.** Ranking basis (credits paid or share) × charge test (unstated or stated) × shares (naive or counterfactual) = 8 cells. Credits-paid
  cells name {A, B}; naive-share cells name {C, D} or {D, E}; counterfactual cells name {C, F} without the charge test (C's 0.97
  outranks E's 0.93) and {E, F} with it, so only the charge test with the counterfactual names the answer, at $651k net.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The policy names the lowest-consistent-value rule as a general prudence clause. No document mentions input timing
   in connection with backups, and the dependency log is filed for the orchestration team.
2. **Corpus blind for a computable reason.** *In both pilot families every late job's inputs landed at least two hours before its scheduled
   start, because both read the ingestion tier's early snapshot, so every rescued straggler saved its deadline.* The settled ledgers confirm
   the naive share (1.00) and the charge arithmetic to within 2% and cannot see input-bound lateness.
3. **No arithmetic symptom.** Credits tie to the SLA register, charges to the price list, instances to the scheduler; the tie at 1.00 is
   arithmetically exact.
4. **Not a row predicate.** Each late job's counterfactual needs its input landing time from the dependency log, its stage structure, the
   sibling-median duration of every stage, and its deadline, combined into a finish time per job across 2,300 late jobs.
5. **The enumeration is arithmetic.** Which late jobs a backup could have saved is computed; no column says so.
6. **No cutover date.** Input-bound lateness is a standing property of D's upstream sources; no series steps.
7. **Survives deletion.** Remove the scheduler team's view and the totals, and the tie-broken build is still the natural one.

## 6. The calibration corpus

* **Form.** The settled SLA-credit ledger and the chargeback ledger for families G and H over last half's pilot: every late job's settled
  credit before and during the pilot, and every backup's settled charge.
* **What it certifies.** The sibling-relative straggler rule, the charge arithmetic and a share of 1.00: during the pilot G's and H's credits
  fell by exactly the straggler-job credits, less 2%.
* **What it is blind to.** Input-bound lateness (above).
* **Twin pair.** Pipelines D-07 and E-12 are identical on stragglers per run, sibling medians, credits at risk ($48k each), charges and extra
  instances. D-07's inputs landed after its latest feasible start on 11 of its 20 late days and E-12's on none, so their avoidable credits are
  $22k and $45k, 2.0× apart, separated only by the counterfactual.
* **Resemblance points at the decoy.** C's and D's straggler profiles match G and H, where every rescued straggler saved its deadline.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The capacity policy: the 5% extra-instance cap, admission by avoidable share stated at the lowest value consistent with
  every file of record, ties broken by credits at risk, and admission only where avoidable credits exceed backup charges. The SLA register's
  deadlines. The chargeback price list. One sentence each.
* **Empirical pins.** The straggler multiplier, from the gap in sibling ratios; the counterfactual stage speed, from sibling medians.
* **Voices.** The scheduler lead: "Put the backups where the credits are; A and B paid the most." The pilot's owner: "The pilot proved it:
  rescue the straggler and the credit goes away."
* **Licensed wrong basis.** The policy records that the finance partner sizes the scheme on credits at risk across all straggler jobs and
  will present that sizing at the platform review.

## 8. Determinism by construction

* **Counterfactual margin.** No late job's counterfactual finish lies within 40 minutes of its deadline, so median or mean stage speed and
  minute rounding agree.
* **Straggler rule.** Sibling ratios have an empty band from 1.6 to 2.2, so any multiplier in it marks the same instances.
* **Input landing.** Each job's landing time is the latest of its upstream partitions in the dependency log, and no partition lands within
  ten minutes of a latest feasible start.
* **Rounding.** The net saving is given to the nearest $10,000; $651k sits mid-bin.

## 9. Prompt sketch and deliverables

> Backups go live for the second half and the cap leaves room for about two of our six job families. The scheduler team wants the two that
> paid the most SLA credits. Tell me which families go on the list and what the backups should save us over the half net of their compute,
> to the nearest $10,000, and set each family's credits avoided against what its backups cost. Send `backup_list.xlsx`, a chart
> `avoidable_credits.png`, and a one-page `scheme_note.pdf`.

* `backup_list.xlsx` — each family under each rung's basis (ask C), the queue-wait sheet (ask A) and the storage sheet (ask B).
* `avoidable_credits.png` — for each family, credits at risk, credits a backup would avoid and backup charges as grouped bars, the avoidable
  share labelled above each group, the cap's two admitted families highlighted and the net saving in the title.
* `scheme_note.pdf` — the committed list and figure, and why each other family stays off.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each family, median and 95th-percentile queue wait over the half. *Device:* the scheduler's
  status history logs preemption and resumption as new rows, and the scheduler guide measures wait from the original submission to the first
  instance start; timing from the last queued row understates three families. The admission build never uses queue waits.
* **Ask B (device-carried).** For each family, average and peak intermediate storage over the half. *Device:* storage metrics are cumulative
  bytes per node that reset when a node restarts, as the metrics guide says; differencing across a reset produces negative usage and wrong
  peaks for four families.
* **Ask C (validity).** Each family's share, avoidable credits and net value under each of the four rung bases.
* **Decoupling.** Clearing the counterfactual and the charge test changes no figure in asks A or B.

## 11. Rubric arithmetic

6 families × 2 (ask A) + 6 × 2 (ask B) + 6 × 4 bases (ask C) + the committed list, the net saving, the cap used and the deciding comparison for
the admitted families + 5 named chart parts + 3 files ≈ 60 criteria.

## 12. World-building constraints

* Credits paid A 900, B 760, C 610, D 520, E 430, F 380; on straggler jobs 120, 150, 560, 480, 410, 360; charges 70, 80, 610, 60, 50, 40 ($k).
* Extra instances A 2.4%, B 2.5%, C 2.6%, D 2.2%, E 1.9%, F 1.7%. Counterfactual shares C 0.97, D 0.38, E 0.93, F 1.00.
* The pilot families' inputs always land two or more hours early; their settled results match the naive share within 2%.
* D-07 and E-12 are identical on every instance-level column.
* Queue history and storage metrics never touch instances, the dependency log, the SLA register or the pilot ledgers.
