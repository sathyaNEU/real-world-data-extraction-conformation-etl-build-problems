# DA36 — Which subject category gets the preprint server's one new moderator, when a cross-list only reaches a category's queue if it arrives late

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Product Analytics · content moderation operations |
| Mirrors | Staffing review queues where items carry several labels but each label's queue sees only some of them (multi-tag tickets routed by when a tag was added, cross-posted content reviewed by the first community, listings in several marketplace categories) |
| Decision shape | Which of N gets one scarce thing: one volunteer moderator for the category whose load grew most |
| Committed call | The category that receives the moderator, and its growth in moderation load from 2019 to 2023, in actions to the nearest hundred |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · Pattern B (a reproduction gate over the settled credit ledger), with Pattern D (versions against submissions) at rung 2 |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution support |
| Measured traps engaged | #1 reports a failed back-test, ships anyway · #3 stops at a close but inexact match · #2 counts file rows instead of the real unit |
| Calibration form | Settled-transaction ledger: moderator credits settled for every moderation action in 20 closed quarters (2019–2023), paid to moderators drawing from five field pools |
| Driving force | A cross-list requested with the submission is checked by the primary category's moderators; one requested after announcement goes to the target category's own queue. Listing counts, whole or fractional, cannot see that, and only routing by the cross-list's request time, a join to the submission history, reproduces every settled cell. Machine-learning authors add Statistical methodology after posting, so that queue grew fastest while every listing count credits the cross-list magnets. |

## 1. Situation

A preprint server adds one volunteer moderator a year, and its charter sends the new moderator to the category whose moderation load grew
most between 2019 and 2023. Twenty categories are eligible. Moderators earn a credit per moderation action, settled quarterly, and each draws
actions from the shared queue of one of five field pools. The pack holds submission metadata with every version and cross-list, the
submission history with event times, the moderator roster, the credit ledger for 2019–2023, and the charter.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each submission, version, cross-list event and settled credit. Nobody reports a load ranking and
  nothing is overturned. The difficulty is which queue a cross-list lands in.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the board's basis. Fractional version counts, built from the metadata, still match 90 of 100
  settled pool-quarters and still name Quantum physics.
* **Instrument repair.** No file is suspect: the metadata, the submission history and the ledger are complete through 2023, and the ledger
  records what it claims, credits paid to moderators who share one queue per field pool. A category's own queue is a routing of actions
  that no row records. With every file perfect, rung 0 still names Machine learning, rung 1 Computer vision and rung 2 Quantum physics,
  and the routing by request time is still needed for Statistical methodology.
* **Lens swap.** Listing counts credit every category a paper names; the answer credits the queues that actually reviewed a version or a
  late request. Different actions, not different weights on the same listing.

## 3. The driving force

A strong solver knows whole counting inflates cross-list magnets, splits each submission fractionally, reads the charter's "every version a
moderator reviews is a unit of work", counts versions, and back-tests against the settled ledger: 90 of 100 pool-quarters match. The
misses all fall where cross-lists from another pool were added after a paper was announced. The server routes cross-lists by when they were requested. At
submission, the primary category's moderators check the whole paper and its cross-lists, so the primary does the whole unit and the target
nothing. After announcement, the request enters the target category's queue as an action of its own. Machine learning, a magnet for
at-submission cross-lists, does far less moderation than its listings suggest. Statistical methodology, which ML authors add after
posting, does far more, and its queue grew 1.33× faster than the next.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Every listing counts in full (primary and cross-lists) | A, Machine learning (+21,000, 1.25× Computer vision) | The category pages count it this way | The ledger: whole listings match 31 of 100 settled pool-quarters |
| 1 | Fractional submissions: half to the primary, half shared across cross-lists | B, Computer vision (+11,900, 1.24× Machine learning) | The standard correction for multi-label counts | The charter: every version a moderator reviews is a unit of work |
| 2 | Fractional versions (each replacement re-reviewed) | C, Quantum physics (+12,400, 1.23× Computer vision) | Right unit, and 90 of 100 pool-quarters match | The ledger: all 10 misses are pool-quarters receiving cross-lists from another pool requested after announcement |
| 3 | **Decisive:** each version to its primary's queue, each post-announcement cross-list request to its target's queue | **E, Statistical methodology (+11,600, 1.33× Computer vision)** (5th of 20 on rung 0) | — | — |

* **Position table.** Statistical methodology ranks 5th on rung 0 (+9,400), 4th on rung 1 (+7,000) and 3rd on rung 2 (+8,300), and
  leads only rung 3.
* **Discriminator dominance.** Quantum physics carries 1.49× into rung 3. Routing raises Statistical methodology 1.40× and lowers Quantum
  physics to 0.58×, an edge of 2.41×, against the 1.2 × 1.49 = 1.79 needed (1.35× headroom). The product, 2.41 / 1.49 = 1.62, is
  Statistical methodology's lead over Quantum physics on rung 3; Computer vision is runner-up at 1.33× behind.
* **Partial correction priced (L3).** A solver who routes by timing but counts submissions rather than versions names Computer vision
  (+9,800, 1.24× Statistical methodology), whose primaries are many and rarely replaced. A solver who credits primaries in full but keeps
  every cross-list as a target action names Machine learning (+14,600, 1.26× Statistical methodology). Neither half lands on the answer.
* **Grid.** Listing weight (whole, fractional, primary-only, routed) × unit (submission or version) = 8 cells. Seven name Machine learning,
  Computer vision or Quantum physics. Only routed versions name Statistical methodology.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The charter defines the unit of work and the allocation basis. The submission guide says cross-lists "may be
   requested at submission or later". No document says which queue reviews which.
2. **Pattern B, reproduction against the best rival.** Routed versions reproduce 100 of 100 settled pool-quarters exactly. Fractional
   versions reproduce 90, primary-only versions 78, fractional submissions 64 and whole listings 31. Every rival omits post-announcement
   requests as actions, so each falls short of the ledger's quarterly totals by 4% to 9%. The routing is a construction: each cross-list's
   request time from the history joined against its paper's announcement time.
3. **No arithmetic symptom.** Versions reconcile to the metadata, history events to versions, and credits to the roster under every
   construction.
4. **Not a row predicate.** It needs a per-cross-list comparison of two event times from another file, then a re-assignment of the action
   to a different category's queue.
5. **The enumeration is arithmetic.** No column marks a cross-list as late or routes an action.
6. **No cutover date.** Late cross-listing grew steadily with the ML field, with no step.
7. **Survives deletion.** With every voice removed, fractional versions still match 90 of 100 pool-quarters and name Quantum physics.

## 6. The calibration corpus

* **Form.** The credit ledger: every moderation action settled to a moderator, 2019 to 2023, rolled to 100 pool-quarters through the
  roster. No finer roll-up exists, because a pool's moderators share one queue.
* **What it certifies.** That versions are the unit, which a back-tester finds quickly.
* **What pins the routing.** The 10 pool-quarters only timing-routed actions reproduce.
* **Twin pair.** The statistics pool in 2021 Q3 and the mathematics pool in 2022 Q1 match on primaries, versions, cross-lists received
  and listing counts. Their settled credits are 6,840 and 3,420 (2.0×): most of the statistics pool's incoming cross-lists were requested
  after announcement, and the mathematics pool's at submission.
* **Resemblance points at the decoy.** On every listing column, Statistical methodology resembles Mathematical statistics, whose load is
  flat.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The charter: the new moderator goes to the category whose moderation load grew most from 2019 to 2023; every version a
  moderator reviews is a unit of work; a load measure that does not reproduce each pool's settled credits in every quarter is not the
  charter's measure.
* **Empirical pins.** The routing, from the ledger.
* **Voices.** The operations lead: "Cross-listing is the whole story; count every listing a category appears in." The moderators' council
  chair: "Replacements are where the real work is, and quantum's queue is drowning."
* **Licensed wrong basis.** The charter records that the advisory board allocates moderators on fractional submission counts and will see
  the allocation on that basis.

## 8. Determinism by construction

* **Timing.** No cross-list request falls within 24 hours of its paper's announcement, so the routing has no boundary cases.
* **Roster.** Each moderator draws from one field pool in each quarter, and no category belongs to two pools, so credits roll up to pools
  exactly.
* **Withdrawals.** Withdrawal notices generate no credit in any settled quarter and are excluded under every construction.
* **Growth.** Both years are computed with the construction that reproduces every settled pool-quarter.

## 9. Prompt sketch and deliverables

> The new moderator slot is decided next week and the operations lead is sure cross-listing tells the whole story. Tell me which category
> gets the moderator and how much its moderation load grew from 2019 to 2023, to the nearest hundred actions, in one line for the board.
> Send `moderator_slot.xlsx`, a chart `load_growth.png`, and a one-page `slot_decision.pdf`.

* `moderator_slot.xlsx` — the load build for all 20 categories, the turnaround sheet (ask A), the newcomer sheet (ask B) and the
  reproduction table (ask C).
* `load_growth.png` — growth by category under the four constructions as a dot plot, with each construction's ledger match count in the
  legend, the twin categories linked, and the chosen category marked.
* `slot_decision.pdf` — the committed category, its growth, and why the others fall away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 20 categories, the median hours from submission to announcement in 2023.
  *Device:* history times are UTC and the announcement schedule runs on the server's local clock, as the schedule note says; mixing them
  misplaces 14% of next-day announcements.
* **Ask B (device-carried).** For each category, the share of 2023 submissions from first-time submitters. *Device:* the account-merge log
  links duplicate submitter accounts; counting raw accounts overstates newcomers in six categories.
* **Ask C (validity).** Settled pool-quarters reproduced by each of the four constructions, and the six leading categories' growth under each.
* **Decoupling.** Clearing the routing changes no figure in asks A or B.

## 11. Rubric arithmetic

20 categories (ask A) + 20 categories (ask B) + 4 reproduction counts and 6 × 4 growth figures (ask C) + the committed category, its growth
and its margin + 5 named chart parts + 3 files ≈ 79 criteria.

## 12. World-building constraints

* Growth (thousands of actions): rung 0 A 21.0, B 16.8, D 12.1, C 10.9, E 9.4; rung 1 B 11.9, A 9.6, C 8.8, E 7.0; rung 2 C 12.4, B 10.1,
  E 8.3, A 8.0; rung 3 E 11.6, B 8.7, C 7.2, A 6.2.
* Ledger: 100 pool-quarters (five pools, 20 quarters); reproduced 100 / 90 / 78 / 64 / 31.
* Statistical methodology and Mathematical statistics match on every listing column in 2021.
* Time zones and account merges never touch a version, a cross-list or a credit.
