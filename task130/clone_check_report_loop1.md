# Clone check: pre-flight, task130 (v2, hardening loop 1) against the whole corpus, 2026-10-11

## Verdict
TEMPLATE (Track B, reject tier): task130 loop 1 against task73 (world ten). In both builds the stump is the same move: carrying the class a household's record holds when a filed rule re-derives that class from the circumstances on file. The ledger does not record task73 world ten as delivered, so this is reject tier by kind and becomes exclusion level only if that build ships. The same move is the driver of task86's retired v2 first cut, which both platform responses solved, and it appears as critical components of the live task86 v2.

## Scope and coverage
- **Mode.** Pre-flight on one build, as `/build` stage 5 asks. The build is task130 at commit 60ae530 (branch `sathya8571/task130-harden`, hardening loop 1 of architecture v2), compared against every other build. The window does not apply. task130's own v1 lineage is the same task, so it is not compared.
- **Corpus.** wt130 holds main as of today plus the task130 commit, but only task117 to task131 are on disk. task1 to task113 are folders on no disk here, so they come from the fingerprints cached on the author's original checkout. Two in-flight builds were added read-only: task132 from the main checkout (branch `sathya8571/task132-relay-final-buy`) and task133 from wt133.
- **How it ran.** fingerprint.py resolves the repo, cards and ledger from its own location, so the run used a scratch mirror (`.../scratchpad/clone130/`):
  - copies of the script, guard.py, vocab.json, the ledger and every card;
  - task130's hardened card from wt130, task132's and task133's cards from their own checkouts;
  - wt130's cache as the base;
  - task folders linked read-only;
  - task117's and task119's committed `target.zip` unpacked into scratch so their packs were profiled.

  Nothing was written into any checkout except this report.
- **Cache check.** The cached mechanism fields match the current cards for every build except task130, which was re-extracted from disk. The cached ledger rows match the current ledger.
- **Extract and screen.** The extract gave 127 cards, 125 of them screenable. The screen (`screen --focus task130`) scored 124 pairs and promoted 4:
  - task132, on surface (top 3 per cent of consecutive builds);
  - task100, on surface (corpus top 1 per cent) and the same gap;
  - task87, on surface (corpus top 1 per cent) and the same gap;
  - task102, on gap, pattern and decision type.
- **Corpus baseline.** Across 7,750 corpus pairs the surface score has a mean of 0.058, a median of 0.075 and a 99th percentile of 0.105.
- **guard.py heart task130.** The verdict is BLOCK, but only on `people.first` (Maria, task119; see Track A).
  - Driver and stump text similarity peaks at 0.08 (task119's stump), well under the 0.12 warn line.
  - `test.same_puzzle_older` is a NOTE, already differentiated against task102.
  - No Part 6.1 ban axis is shared with task127 to task129, nor with task131 to task133. task131 shares only the Gate G mechanism; task133 shares only shape 02 and `quantity_figure`.
- **Adjudicated: 16 pairs.**
  - The 4 promoted pairs.
  - The 4 the author named: task86, task125, task80 and task119.
  - Five raised by a sweep that read every card's driver and every lineage driver (129 cards) for a stale record of a time-varying attribute, or a class recomputed on the day: task73, task123, task42 and task107, plus task133.
  - The legacy echoes task14 and task23.
  - task131, the consecutive build.

  The dead rows the sweep touched were read as history: task86 v2 first cut, task63 v1, task98 v5 and v6, and task72 v1.
- **How adjudication was done.** This thread has no subagent tool, so each pair was read here, one at a time, with the inputs and questions the per-pair adjudicator would get. task130's side used its card, design note, prompt, write-up and target listing. For task1 to task116 the design notes are not on any disk here, so their side used the card (driver, `driver_concrete`, stump, lineage), the ledger row and the cached prompt and write-up extracts (steps, critical components, recommendation).
- **Unread: 108 pairs.** Neither the screen nor the driver sweep raised them. Every one was read at driver level in the sweep, but none was adjudicated pair by pair.
- **Mechanism coverage.**
  - 103 builds are read from a card, 5 are note-only (task16, task17, task20, task112, task113) and 17 have no mechanism layer on the screen (within task1 to task24).
  - The sweep still read the driver sentences of those 17 from their cards.
  - 36 builds carry back-fitted labels (task1 to task36).
  - task112 and task113 have a pack fingerprint and no card, so they were checked on Track A only.
  - task114 to task116 have cards and no fingerprint, so they were checked on Track B only (sweep and guard).
  - task61 and task96 have nothing on file.
  - task99 has a card, but the script excludes it as a scratch number. Its driver was read in the sweep.
- **What was not checked.**
  - The packs of task118 and task120 to task129 are not on disk (`task*/target/` is gitignored and they have no zip). Byte-identical, same-seed and schema checks therefore did not run against those 11 builds.
  - Their prompts and write-ups were screened.
  - File names were compared from `metadata.json` for task118, task121 to task127 and task129, and from task128's input list. No stem is shared. task120's file list was not read.
- **Status record.** The ledger has rows to task108 only. task130 has no row (in flight).
  - task73 world ten: built 2026-09-11, stump-check and determinism-check not yet run, no portal result recorded.
  - task86 v2, task80 v2, task87 v9 and task100 v2: built, with no portal result recorded for the current architecture.
  - task102 v1: portal responses recorded as missing the call; the ledger does not mark it approved or delivered.
  - task119, task125, task132 and task133 have no ledger row. task125's own pipeline.json reads stage `retired`, portal none.
  - No counterpart in any finding is recorded as approved or delivered.
- **Tooling defects found on the way.** None changes this report's tiers.
  1. **Status classifier, read as dead.** The classifier in `fingerprint.py` misreads live rows whose status narrates a predecessor's failure: task73 ("replaces world nine, which failed"), task40, task44, task51 and task55. The screen would label a hit against them as history and understate it.
  2. **Status classifier, read as delivered.** task48 and task72 match "delivered" inside prose ("one group-by delivered the conclusion", "service delivered under a grantee's agreements"), which would overstate a hit against them.
  3. **People index blind to zipped packs.** The guard's people index reads unpacked narrative files only, so personas inside a committed `target.zip` (task119's Maria Reynolds) are invisible on a normal checkout. The Maria block surfaced only because this run unpacked the zip.
  4. **Name parser.** The people index misses first names outside its dictionary. Wiremu Roberts in task123 is not found, and its index entries read "Geraldine Mental" and "Linwood Carer".

## In batch against earlier builds
In pre-flight mode every pair is task130 against another build, and the window is the whole corpus. No hit lands on a build the ledger records as approved or delivered. That includes the one approved housing build, task34, whose driver (a latent subpopulation found by a within-cluster fit) does not touch task130's.

The reject-tier hit (Track B 1) is against task73 world ten. On the record that build is live and undelivered: exposure is unknown, not excluded. If task73 world ten has been or will be submitted, this hit is the exclusion.

## Track A findings, reviewer visible
No Exact, Same seed or Dataset finding. Against every build:
- task130's masked prompt overlap is 0.000;
- no rare file name is shared;
- no column set is identical;
- no table carries the same seed;
- no file is byte-identical;
- no invented name is shared.

The top surface scores are flat layout and format mix only: task100 0.147 (pct 99.5), task87 0.143 (pct 99.4) and task132 0.101 (pct 97.8). task87 and task100 also share the xlsx+png deliverable pair.

1. **Name audit (guard BLOCK by rule, not a clone tier): Maria Field against task119's Maria Reynolds.**
   - task119 is inside the last twelve builds, so the guard rule blocks it.
   - Visible in task130's `tenter_house_closure_procedure.docx` ("Agreed with Maria Field") and the golden workbook's author line; in task119, in its board paper PDF and correspondence eml.
   - Status: task119 has no ledger row; task130 is in flight.
   - Clears it: redraw the persona with `guard.py names --geo "United Kingdom, England" --seed 130`, changing the generator, prompt and goldens together. No ladder change.
2. **Name audit (guard BLOCK by rule, missed by the parser): Irene Roberts against task123's Wiremu Roberts (chair of trustees).**
   - Same surname, inside the last twelve builds.
   - Visible in task130's prompt ("Irene Roberts signs the call-off") and golden; in task123, in its minutes, planning thread and golden memo.
   - Clears it: the same rename.
3. **Shape echo (soft): task86 v2.**
   - Status: task86 is built, with no portal result recorded; 44 builds apart.
   - No text, file-name, schema or entity overlap (surface 0.077, pct 58).
   - What a reviewer holding both sees:
     - a housing body works a waiting list in filed policy order, by bedroom class, against units coming available;
     - the answer is whole units by bedroom size for the households the list leaves;
     - the deliverables are a chart and a workbook;
     - the bedroom standard is applied to the household members, with ages on the allocation date, and confirmed by reproducing past lets (task86 CC 2: "applied to the household as it stood on the offer date with ages on that date: they reproduce all 1,121 offers"; task130 step 2: need "under Part 3 ... from the people in household_members ... on each round day, which reproduces all 49 lets").
   - Clears it: nothing on Track A alone. The echo now carries task130's decisive move (Track B 2).
4. **Shape echo (soft): task125.**
   - Status: task125 has no ledger row; its pipeline.json reads retired, portal none; 5 builds apart.
   - Shared surface:
     - an English council in GBP sizing a framework-lot call-off for April 2027;
     - shape 02, `quantity_figure`;
     - forcing event `purchase_order_or_contract`, org family `local_government`;
     - context artifact `operations_log`;
     - procurement-lot vocabulary in file names (`pasf_lot2_calloff_terms`, `calloff_working_papers_index` against `dps_lot2_lot3_price_schedule`).
   - Loop 1 renamed the workbook stem, so no file name is shared.
   - The drivers are unrelated: task125 turns on how a joint household's payment splits after a guest leaves.
   - Clears it: nothing required while task125 stays unsubmitted.

## Track B findings, mechanism
1. **TEMPLATE (reject tier): task130 loop 1 against task73 world ten.**
   - **Status.** task73 world ten: ledger reads built 2026-09-11, stump-check and determinism-check not yet run; no portal result recorded; mechanism from its design-note-sourced card. task130: in flight. 57 builds apart.
   - **Shared driver, domain nouns stripped:** "A household's class under a filed rule has to be re-derived from the circumstances on file at the moment the rule is applied, instead of carried from the class its record holds, because the circumstances have moved since that class was set; a back-test on the book, which the re-derived class reproduces and the carried class does not, confirms it."
   - **task73's decisive move.** The second FY2028 interview goes to the households the manual's rule puts on six months from the income on file at their October to March recertification, not to those on six-month periods today.
     - Stump: carry today's periods forward and file the Loon Harbor slate.
     - Confirmation: every current period reproduces from the circumstances at its own start.
   - **task130's decisive move.** Each round's lets go by the need worked out under Part 3 from the members on file on the round day, not by the case record's need.
     - Stump: R5, 66 units.
     - Confirmation: the members reproduce 49 of 49 September lets; the record reproduces 25.
   - **Position.** The move is decisive in both builds.
     - task73's ladder: budget only, then desk on the due list, then periods carried forward (stump), then the answer.
     - task130's ladder: rates and curves, then the TA-only queue, then the record's need (R5, 66, 18 cells off), then the members once on 30 September (R6, 53, 2 cells off), then the answer on each round day (52).
     - The record-to-members leap carries 66 to 53 and 16 of the 18 missed cells. The ageing inside the window is worth one unit, and the design note itself tried it as the decisive device, rejected it, and kept it as R6.
     - So task130's decisive leap is the carried class against the rule applied to the circumstances on file, which is task73's leap.
     - The engines are parallel too: in each build the class decides the month in which a household next reaches a monthly capacity (task73's desk allocation, task130's planned lets by size).
   - **What differs, and why it does not clear the finding.** These are the nouns and the frame; the thing a solver has to see is the same.
     - Domain.
     - Decision type: slate against quantity.
     - Gate G label: `binding_constraint` against `method_or_model_selection`.
     - Strategy label: `binding_constraint` against `time_semantics`.
     - The attribute: a period length from income against a bedroom need from ages.
     - The trigger: a re-set at the next recertification against an event-assessed record that lags.
   - **Why the mechanics missed it.** The decisive gap labels differ (objective against time), as do the decisive G-codes (G11 against G13) and the decision types, so the screen's core score is 0. Driver text similarity is under 0.03. This is the fully reskinned case.
   - **Axis to redraw:** the decisive rung.
   - **Does the data survive?** Partly. The Tenter House world, the placements spine, the lets log, the plan, the scheme and the price schedule are not what collides. The household-members and bedroom-need-review layer exists to carry this rung, and the ladder, the answer and every graded figure move with any redraw.
2. **Same driver on a retired row (history, not a redraw on its own): task86 v2 first cut.**
   - **Status.** Retired 2026-09-12: solved on the platform in round 1, with both responses committing to its mix exactly (8 / 17 / 22 / 57 / 20). It was kept as R3 in the live v2 and is marked spent on task86's card.
   - **Its driver:** "A rule-placed unit is measured by its present membership ... rather than from a correct but dated certification of the same unit, because the rule measures units as they stand on the decision date."
   - **Against task130.** The same claim, in the same domain, on the same mechanic: a bedroom standard with age thresholds, applied to the members on the allocation date.
   - **In the live task86 v2.** The move sits as critical components (CC 2 and CC 3: sized "as the household its head lives in today ... not as certified in 2024"). By the position rule that is reuse there.
   - **Against task130's own note.** The design note's six-point check says this lesson is "not one an earlier build teaches", but task86 v2 teaches it in the same domain.
   - **task63 v1** ("exemption redetermined rather than read off a carried prior-year status", retired as an entry rung) is the same family and history only.
3. **Card bookkeeping (not a finding).** task130.json's `differentiation` entries for task80, task86 and task50 still describe the pre-loop driver ("the list order itself is the decisive rung, filed nowhere"). The card notes and the design note say the list order is now filed. No entry covers task73 or task86's v2 first cut.

## Clean, shares components by design
- **task86 v2 (live).** Its driver is an earlier draw on the same pool: Quesada Commons leases up off the list first and empties the front of it. task130's driver is the class re-derived from members. These are different claims. The shared device (the bedroom standard on current members) is a supporting rung there and decisive here; see Track A 3 and Track B 2.
- **task80 v2.** Same as-of family, different operation. task80 dates a fixed-term status from the criterion event that conferred it, not from the first period the record shows it operating. task130 re-derives a class from members on each day. The card's task80 entry is stale but the conclusion holds.
- **task102 v1.** The labels collide: gap time, G13 and `quantity_figure`, the guard's already-differentiated NOTE. task102's driver is payments due on a weekend being released on the next business day into the next period, with closed periods all ending on business days. There is no shared move beyond period semantics. The card entry is current and holds.
- **task100 v2.** Promoted at surface pct 99.5 with gap time. Exits are found by a programme stage the recorded year count does not show, located on the prior census. The shared component is rolling a membership forward with exits, where the recorded attribute is not the governing one. The operation differs: a cross-census join for a hidden stage, against a filed rule applied to members.
- **task87 v9.** Its driver is a binding constraint: two owed items in one period slot. The surface is only xlsx+png and flat layout.
- **task132** (in flight, two apart). Renewal of replaced modules: a failed module's replacement restarts at the bottom of the age curve. The shared component is an age-driven attribute updated month by month across the window. The surface is an identical format set and flat layout. No ban axis is shared.
- **task133** (in flight). Its driver is a seasoning-conditional lifetime PD (divide by survival to date). It shares shape 02, `quantity_figure`, and a unit's age as of the reporting date.
- **task123.** Same as-of family, different operation: scope is set by a contract in force on the census day (the Variations sheet), against the register's start and end dates.
- **task42.** Same family, different operation: a temporal join on an effective-dated enrolment history that exists, against collapsing it to the most recent enrolment.
- **task107 v4.** A group crosses a line at a fixed service anniversary just before the window. That is task130's R6 component (ageing across a threshold inside the window): decisive there, second level here. This is demotion, so it is reuse.
- **task125.** Band membership is re-summed after a component class ends on a filed date. That is the same component at a lower rung in task125, whose decisive move is the joint-household payment split, so it is reuse by position.
- **task119 v2.** Decomposition attribution: beds held for the trust's own planned admissions. The only shared items are English public-sector furniture and the persona's first name (Track A 1).
- **task131.** A causal design: randomisation at a sub-unit sharing a parent budget. Only Gate G is shared.
- **Legacy and dead rows (history, nothing to redraw).**
  - task14: a point-in-time entitlement from an append-only log.
  - task23: an age field frozen at a migration, a planted defect.
  - task98 v5 and v6: a class at entry against the register's raised label, and units leaving a class over a threshold.
  - task72 v1: an owner under an effective-dated agreement history against the holder at the close.

## Strategy monoculture
Read from the cards' `stump_strategy`, `decisive_rule_filed`, `official_decoy` and `validated_decoy` fields. Window A is the twelve builds ending at task130 (task119 to task130); window B is the twelve ending at the newest build in flight (task122 to task133).
- **By strategy, window A:** identity_resolution 3 (task120, task121, task126); decomposition_attribution 2 (task119, task122); time_semantics 2 (task123, task130); binding_constraint 2 (task127, task128); causal_design 1; withheld_rule_corpus_fit 1; composition_mix 1.
- **By strategy, window B:** time_semantics, causal_design and binding_constraint 2 each; every other strategy 1.
- No strategy reaches a third of either window.
- **Withheld rule with an official decoy:** 0 of 12 in both windows, under the cap.
- **Certified-record decoy:** 9 of 12 in window A (task120 to task127 and task129) and 7 of 12 in window B (task122 to task127 and task129), over the cap of three. task130 is not one of them: `validated_decoy` is false, and the record-based replay fails its back-test at 25 of 49. This is a batch finding, not this build's.
- **The labels hide the Template.** task73 is labelled binding_constraint and task130 time_semantics, and they share a driver. Across the corpus, the family "a household's class re-derived from the circumstances on file instead of carried from its record" is:
  - decisive in task73 world ten (live) and task130 (in flight);
  - decisive in task86 v2 first cut and task63 v1 (both retired);
  - a component in task86 v2.

## Corpus habits
- **File roles named the same way:** `data_dictionary` in 61 builds, `export_manifest` in 33, `data_notes` in 12, `provenance` in 12. task130 avoids all four.
- **Deliverable pairings:** pdf+py 11, csv+pdf 10, py 8, pdf+png 6, csv+py 5, py+xlsx 5, pdf+xlsx 5, docx+xlsx 4, docx 4, png+xlsx 3 (task87, task100, task130). The png+xlsx pairing is what puts task87 and task100 at the top of task130's surface ranking.
- **Voice-check (task122 to task133).**
  - No carrier wording, and no run of six or more words in a third of the batch.
  - Opening move "other" in 7 of 12, a concentration in the classifier's coverage rather than in the prose.
  - task130 is 262 words at 26.2 words per sentence, inside the economy flags.
- **Mechanism idiom.** A household-level class that a filed rule derives from circumstances on file, beside a record carrying an older value of it, recurs in three public-sector builds: task73, task86 and task130. A reviewer holding a batch sees the recurrence even where no pair reads alike.
- **Call-off as the forcing frame:** two English-council builds five apart (task125, task130).

## What to redraw
1. task130: the decisive rung (Track B Template against task73 world ten; it is also task86's spent R3 and its retired v2 first cut's driver). The data partly survives: the world, spine, lets, plan and price schedule stay, while the members and reviews layer, the ladder, the answer and the goldens move.
2. task130: the personas Maria Field (first name used in task119) and Irene Roberts (surname used in task123), in the generator, prompt and goldens together, with no ladder change.
3. task130 card: rewrite the `differentiation` entries for task80, task86 and task50 to the loop-1 driver, and add task73 and task86's v2 first cut (bookkeeping, the author's call).
