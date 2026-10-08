# DS39 — Which labelling queue the expert reviewers take next quarter, when only one onboarding cohort's items are ever wrong

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Product Analytics · search relevance labelling operations |
| Mirrors | Routing scarce expert reviewers where a sub-population's errors are invisible to agreement-based quality models (data-labelling QA at AI labs and labelling vendors, content-moderation appeals at Meta and YouTube, catalogue audits at Amazon) |
| Decision shape | Which of N gets one scarce thing: the expert review team (1,200 audited items a week) for next quarter, among six labelling queues |
| Committed call | The queue the team takes, and the label errors it is expected to correct per week, to the nearest whole label |
| Gap · Pattern | Gap 2 (population) over Gap 1 (time) · Pattern E, conditioned yield (corrections fall only on items a fast-track cohort carried, a property reached through the onboarding register), with a saturated tie (E21) at rung 1 |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #19 breaks a big tie instead of questioning it · #13 validates on one population, applies to another · #7 uses the ready-made measure |
| Calibration form | Pilot log: last quarter's expert-review pilot, 4,960 items sampled uniformly within the six queues, with every crowd label, the expert's label and the review time |
| Driving force | Experts correct labels only on items a fast-track cohort of the vendor's workers carried to a majority: 68 of 179 such items in the pilot, none of the other 4,781. The cohort agrees with itself, so Dawid–Skene calls those items certain, and it exists only in the vendor's onboarding register. In the pilot it worked queue A; next quarter the register moves it to E and F. |

## 1. Situation

A search company buys relevance labels from a vendor that runs six queues (A–F), five crowd labels per item. Its expert review team can
audit 1,200 items a week, sampled uniformly from one queue, and the data-ops memo sends it next quarter to the queue where it will correct
the most labels. Last quarter the team piloted across all six queues. The search-quality lead believes the queues with the narrowest votes
are where the doubt is.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the crowd labels, the vote margins, the Dawid–Skene posteriors, the vendor's golden-question
  accuracy, the pilot's corrections and the onboarding register. No stakeholder read is overturned. The narrow-vote queues are the least
  unanimous, and every worker does pass the golden questions. The difficulty is which items experts actually fix, and where those items
  will be next quarter.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the lead's view and the council's dashboard. The pilot's correction rate by queue, the natural measured
  evidence, still names A.
* **Instrument repair.** Give the pilot a hundred times the sample. The split by cohort becomes sharper and the queue rates exact, and A's
  pilot rate is still last quarter's: the cohort will not be in A next quarter.
* **Lens swap.** The naive read and the answer differ in population and moment: last quarter's items by queue, against next quarter's
  items carried by a cohort that has changed queues.

## 3. The driving force

A strong solver aggregates with Dawid–Skene, as the memo says, and finds every queue's expected errors at zero: posteriors sit at 1.000
on every item, so the memo's tie-break by weekly volume decides. A better solver questions the tie, because the pilot is a file of record
too: experts corrected 1.4% of items Dawid–Skene called certain, so no queue's error rate is zero, and the pilot's rate by queue names A.
All of that is correct for last quarter. But the corrections fall on one kind of item only. Joined to the vendor's onboarding register,
every corrected item had a majority from the 61 workers admitted through the vendor's fast-track route rather than its qualification test,
and no item without such a majority was corrected. The cohort misreads one guideline the same way, so it agrees with itself and looks
reliable to any agreement model. Last quarter it worked A. The register's assignments for next quarter put it in E and F, and the pilot's
queue rates no longer describe any queue.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Share of items whose vote margin is one label or less | D (14.0% against B's 11.6%) | Where the crowd disagrees is where an expert helps | The data-ops memo: labels are aggregated by Dawid–Skene, weighting workers by reliability |
| 1 | Dawid–Skene expected errors by queue; all six sit at zero, so the memo's tie-break (largest weekly volume) decides | B (41,000 items a week against A's 33,000) | The memo's model and the memo's tie-break, exactly | The pilot: experts corrected 1.4% of the items Dawid–Skene was certain of, so no queue's errors are zero |
| 2 | The pilot's correction rate by queue, times 1,200 reviews a week | A (51 a week against F's 18) | Measured, randomised evidence, consistent with every file of record | The onboarding register: every correction fell on an item with a fast-track majority, and next quarter's assignments move the cohort out of A |
| 3 | **Decisive:** next quarter's share of each queue's items with a fast-track majority, from the register's assignments and planned volumes, times the cohort's 38% error rate | **E, 44 corrections a week** (4th of six on rung 0) | — | — |

* **Position table.** E is 4th on rung 0 (8.8%), 4th on rung 1's volume tie-break (24,000) and 5th on rung 2 (5.5 a week), and leads only
  rung 3. Rung margins: D over B 1.21×, B over A 1.24×, A over F 2.8×, E over F 1.63× (44 against 27).
* **Discriminator dominance.** A carries a 9.3× pilot-yield advantage over E into rung 3 (51 against 5.5). The cohort's move multiplies
  E's fast-track share by 8 (1.2% to 9.6%) and divides A's by 7.5 (11.2% to 1.5%), an edge of 60×, far beyond 1.2 × 9.3 = 11.2 and the
  14.5 that headroom asks.
* **Partial correction priced (L3).** Half the construction names A, B or F, never E. A solver who finds the cohort split but applies it
  to the pilot's queue shares names A at 51 a week, 2.8× F. One who carries the pilot's pooled 1.4% to every queue is back at the volume
  tie and names B, 1.24× A on volume. One who transports by worker rather than by majority, treating any item with one cohort label as at
  risk, names F at 39 a week against E's 31 (1.26×), because F's cohort workers are spread thinly across many items.
* **Grid.** Aggregation (vote margin, Dawid–Skene) × error evidence (model, pilot by queue, cohort split) × mix (pilot, next quarter) ×
  at-risk unit (majority, any label) = cells that name D, B, A or F; only the cohort split with next quarter's mix and the majority unit
  names E.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The register records how each worker was onboarded and where each is assigned. No document says the fast-track
   cohort errs, or that it moves the yield between queues.
2. **The pilot pins the split only through a join.** Its own columns (queue, task type, worker country, tenure, label counts, golden
   accuracy, posteriors) show the queue gradient and no split. Joined to the register, the split is absolute: 68 of 179 against 0 of
   4,781.
3. **No arithmetic symptom.** Labels reconcile to items, posteriors converge, golden accuracy is 100% for every worker, and the pilot's
   samples tie to each queue's volume.
4. **Not a row predicate.** At-risk status is a property of an item's five labels taken together (three or more from cohort workers), and
   the forward share needs the register's effective-dated assignments crossed with planned volumes by worker.
5. **The enumeration is arithmetic.** No column marks an item, a worker or a queue as at risk.
6. **No cutover date.** The reassignment is a forward plan; nothing in the pilot steps.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, the pilot's queue rates still name A.

## 6. The calibration corpus

* **Form.** The pilot log: 4,960 items sampled uniformly within the six queues last quarter, with all five crowd labels, the expert's
  label and the review time.
* **What it pins.** The absolute split (above), the cohort's 38% error rate on items it carries, and review time (3.4 minutes an item in
  every queue, so 1,200 a week). The pilot drew 827 items from each queue.
* **Mix inversion.** In the pilot the cohort carried 11.2% of A's items and 1.2% of E's; next quarter, by the register, 1.5% of A's and
  9.6% of E's.
* **Twin pair.** The pilot's samples from batches 17 and 31 of queue A are identical on every column the batch file shows: task type,
  guideline version, 60 items, five labels each, the same twelve worker countries, mean tenure of 11 months, posteriors at 1.000 on every
  item, unanimous on 52 items each. Experts corrected 4 and 8 items (2.0×). Batch 31's sample held 21 items with a fast-track majority,
  batch 17's held 10.
* **Resemblance points at the decoy.** By task type and guideline, E most resembles C, the pilot's lowest-yield queue.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The data-ops memo: labels are aggregated by Dawid–Skene (majority-vote start, convergence at 10⁻⁶); the expert team
  goes to the queue where it will correct the most labels next quarter, reviewing a uniform sample of 1,200 items a week; ties between
  queues go to the larger weekly volume. The vendor's onboarding register: each worker's route and queue assignments with effective dates.
  The vendor's capacity plan: planned weekly labels by worker.
* **Empirical pins.** The split and the error rate, from the pilot.
* **Voices.** The search-quality lead: "The narrowest votes show where the doubt is." The vendor manager: "Every one of our workers passes
  the golden questions." The ML engineer: "Dawid–Skene already accounts for worker quality."
* **Licensed wrong basis.** The memo records that the ranking council reviews expert allocation on the vendor's golden-question dashboard
  and will see it.

## 8. Determinism by construction

* **Majority.** Every item carries exactly five labels, so a fast-track majority means three or more; no item has a tie to break.
* **Forward share.** The register's assignments for next quarter take effect on its first day, and planned volumes are fixed weekly, so
  the share needs no date convention.
* **Model.** The memo pins the Dawid–Skene initialisation and tolerance; posteriors are 1.000 to three decimals in every queue under
  any seed or start.
* **Rounding.** E's 43.9 and F's 27.4 round cleanly to whole labels.

## 9. Prompt sketch and deliverables

> The expert reviewers get one queue next quarter, and I want them where they'll fix the most wrong labels. Our search-quality lead thinks
> the narrowest votes show where the doubt is. Tell me which queue they take and how many label errors a week they should correct, as the
> line for the ops review. Send `expert_queue_choice.xlsx`, a chart `corrections_by_cohort.png`, and a one-page `ops_review_note.pdf`.

* `expert_queue_choice.xlsx` — the six queues under each rung basis with the pilot's corrections by cohort status (ask C), the timing
  sheet (ask A) and the cost sheet (ask B).
* `corrections_by_cohort.png` — the pilot's corrected share for items with and without a fast-track majority, beside each queue's
  fast-track share last quarter and next, as paired bars, with the expected weekly corrections labelled and E marked.
* `ops_review_note.pdf` — the committed queue and weekly corrections, and why the pilot's leader is not next quarter's.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the six queues, last month's median seconds per label. *Device:* a task that times
  out and is reopened logs a second open event under the same assignment ID, as the tool's event guide documents. Timing from the last
  open understates every reopened task and drags four queues' medians down.
* **Ask B (device-carried).** For each of the twelve worker countries, the vendor's cost per thousand labels last quarter. *Device:*
  invoices are in local currency, converted at the invoice date's rate in the shipped FX table, and volume discounts arrive the next month
  as credit notes referencing the invoice. Ignoring credits overstates seven countries.
* **Ask C (validity).** Each queue's expected weekly corrections under each of the four rung bases, and the pilot's corrections among
  items with and without a fast-track majority.
* **Decoupling.** Clearing the cohort split changes no figure in asks A or B. Event timings and invoices touch no label, register or pilot
  record.

## 11. Rubric arithmetic

6 queues (ask A) + 12 countries (ask B) + 6 queues × 4 bases + 2 pilot counts (ask C) + the committed queue, its weekly corrections, the
runner-up and the margin + 5 named chart parts + 3 files ≈ 58 criteria.

## 12. World-building constraints

* Rung 0 narrow-margin shares: D 14.0%, B 11.6%, A 9.0%, E 8.8%, F 7.1%, C 5.0%. Weekly volumes: B 41,000, A 33,000, F 28,000, E 24,000, D
  19,000, C 12,000. Pilot weekly yields: A 51, F 18, D 12, B 9, E 5.5, C 3. Forward: E 44, F 27, D 14, B 10, A 7, C 4. Forward with any
  cohort label as the at-risk unit: F 39, E 31.
* 61 fast-track workers; pilot split 68 of 179 against 0 of 4,781. Fast-track workers match other workers on every registry and label
  column except onboarding route.
* Batches 17 and 31 match on every batch column.
* Reopened tasks and invoice credits are independent of every main-call record.
