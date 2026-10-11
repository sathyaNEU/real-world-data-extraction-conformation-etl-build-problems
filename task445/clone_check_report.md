# Clone check: pre-flight, task445 against every other build, 2026-10-11

## Verdict
CLEAN. No Track A or Track B finding at any tier. The nearest mechanism neighbour is task130's retired v1, which failed on the portal. It shares a component with task445 (holders who have not filed yet), not the driver, and it is history only.

## Scope and coverage
- **Mode:** pre-flight on task445, compared against every other build in the worktree `/home/user/wt-task445` (branch `oviya1301/task445-13f-ownership-bridge`). No window applies. task446 is in flight on another branch and is not on disk here, so it is excluded as instructed.
- **Corpus:** `fingerprint.py extract` produced 129 cards, 127 of them with a prompt or target. Those are task1 to task133 (with the numbering gaps already in the corpus), task229 and task445. The task folders from task134 up to task493, apart from task229 and task445, hold only `START_HERE.md`. Where a card is filed for one of them (task134, task135, task228), it is read below for its mechanism. The cache was written in this run, so it is not stale.
- **Pairs screened:** 126, with task445 on one side. **Promoted by the screen:** 0. The highest surface percentile was 19 (task66). No hard tells (no byte-identical files, no same-seed tables, no shared invented name) and no Part 6.1 consecutive ban fired.
- **Why the screen's mechanism route was checked by hand:** task445's card files `pattern: none`, so the screen's pattern axis cannot fire for it. To cover that hole, every card was queried directly on the fields that carry this build's mechanism: `calibration_form = censored_or_lagged_release`, `stump_strategy = maturity_censoring`, and gap `time` with a `designation_set` decision. A keyword pass over the cards (censor, lag, pending, not filed, last report, holdings, 13F) was also run. **That pass manually promoted 8 pairs:** task31, task59, task91, task99, task100, task130 (all three retired architectures included), task134 and task229. All 8 were adjudicated and none was left unread.
- **How the pairs were adjudicated:** this runtime exposes no subagent tool, so the 8 pairs were not read one subagent per pair. They were adjudicated in this thread, from the fingerprint cards (driver, stump, lineage), task445's design note (stump, ladder, tried and rejected) and task130's design note (the v1 dead ends). No answer key or golden of any other build was read.
- **Mechanism coverage across the corpus:** 105 builds have a native card mechanism, 5 are note-only, and 17 have no mechanism available. Those 17 were compared with task445 on Track A only. Both sides of all 8 adjudicated pairs have a card. task445's mechanism comes from its design note (`mechanism_source: design_note`).
- **Mechanical side checks:** `guard.py heart task445` returned WARN. Nearest driver similarity was 0.05 (task121, task80), and the two warnings are a people.last echo (Henderson, task117), already answered in the design note, and a repeated decision type (`designation_set` after task229). `voice-check.py 445` found no unlisted repeats and no calcified carrier wording, and the prompt is 986 characters, under the ceiling.

## In batch against earlier builds
None. Only one other build in the corpus touches 13F holdings data: task130, and only in its retired v1, whose pack is no longer on disk. Against every approved or delivered build, task445 has no Track A collision and no Track B collision.

## Track A findings, reviewer visible
None.
- The target tree is in the SEC's own layout (`form13f_2022q3/`, `form13f_2022q4/`, `edgar13f_daily_20230103_20230203/` with SUBMISSION, COVERPAGE and INFOTABLE, plus `fsds_cover_extract/` with sub and num). No other build has these file names or this schema.
- task445 avoids the corpus-idiom file names entirely: it has no `data_dictionary`, `export_manifest` or `provenance` file, and its provenance role is `data_sources.md`.
- No invented name is shared with another build (Quillfield, Harrowby Point, Prescott, Wexley, Tregaron, Shelby). Among the personas, the guard's only echo was the surname Henderson against task117, which is a WARN and not a finding.
- The deliverable pair csv+png is uncommon in the corpus (it is not among the habit pairings listed below).
- The opening "Which of the twelve names..." is question-first, and so is task131's "Which of the four summer test offers...". That makes 3 of 12 in the voice-check batch, which is not concentrated, and the two sentences are built differently after the opener.

## Track B findings, mechanism
None. Each pair below was read for the same claim and for where the shared move sits in each build's ladder. No pair carries the same decisive move in the same position.

## Clean, shares components by design
task445's driver, with the domain nouns stripped: *a period's total has to be completed reporter by reporter from each late reporter's last report, because the late reporters concentrate in some units, so a single aggregate completion factor misstates exactly the units near the threshold.* Its decisive rung is R5, holder-level completion. That rung sits above R2 and R3 (ratio gross-ups), and above R4 (an issuer-level development factor that a back-test refutes).

1. **task130 v1 (retired; the card lineage records a portal failure on 2026-10-10; no ledger row, so ledger status unknown). History, not a finding.**
   - **What is shared:** task130 v1 was a large-holder designation against a threshold, and its decisive rung was the holders enrolled after the snapshot who had not filed yet. task130's own design note records that it was a reskin of the same capital-markets crowding seed that task445 builds literally.
   - **Where the shared move sits:** in task445 the recognition that some holders have not filed is R0's kill. The prompt-time readme hands it over (deadline 14 February, 125 September filers with no December report).
   - **What differs:** task445's decisive move is the estimator for those holders, per-holder carry-forward against aggregate or issuer-level completion factors, chosen by back-test. task130 v1's decisive move was finding the missing holders at all, through a join on a transfer extract. So the shared device is demoted to the bottom rung in task445, which is reuse, not a clone.
   - **Status of the collision:** both v1 sides are dead (task130 was re-rooted to v2 and then v3), so the overlap lands only on a retired row.
   - **Worth knowing, though it is not a clone finding:** task130's note records the lesson from that failure, that "any rung that is a record a diligent solver can find and join is solved". task445's R5 is a group construction of the same family (September filers without a December report, joined to their September lines). That bears on stump power, not on duplication, and belongs to the solver round.
2. **task91 (ledger: awaiting the portal result).**
   - **What is shared:** the `maturity_censoring` strategy. An unobserved-yet outcome is not an absent one.
   - **Different drivers:** task91 splits a stock into an active pool and a dormant residue and applies a constant recovered from closed conversions, and its trap is that units too young to have begun exiting look dormant. task445 completes a holder set for one open period, and its trap is aggregate against per-reporter completion.
3. **task134 (card only on disk, in flight; no ledger row, so status unknown).**
   - **What is shared:** the `maturity_censoring` strategy and `method_or_model_selection`.
   - **Different drivers:** task134's driver is competing risks, where removals and deaths treated as censoring overstate the return probability, so cumulative incidence against Kaplan-Meier. task445 has no time-to-event estimand.
4. **task31 (ledger: failed) and task99 (no ledger row, so status unknown).**
   - **What is shared:** `censored_or_lagged_release` and `maturity_censoring`.
   - **Different drivers:** both phase an in-year saving by a duration read off a right-censored corpus, where complete-case analysis or quoted delays erase the slow stratum. Their estimand is a duration, and task445's is a level on an open period.
5. **task59 (ledger row carries no status word, so status unknown).**
   - **What is shared:** a `time` and `population` gap.
   - **Different driver:** new episodes are capped at the weeks they can draw before the window closes, which is a binding constraint, not a completion.
6. **task100 (no ledger row, so status unknown).**
   - **What is shared:** an ETL `designation_set` on a forward period, where the snapshot is not the period's population.
   - **Different driver:** members who leave early are found by matching the same member on a prior snapshot. That is re-attributing who leaves, not completing late reports, and nothing in it is an estimator choice.
7. **task229 (the immediately preceding draw; no ledger row, so status unknown).**
   - **What is shared:** the `designation_set` decision type, a guard WARN between consecutive builds.
   - **Different driver:** the standard error of a mean over entities that fail together behind a shared node (clustered error), which is unrelated. The shapes differ too (10 against 03), and so do the deliverable species (json+png against csv+png). One shared outline element is short of a Shape echo.

## Strategy monoculture
The window is the last twelve draws by `guard.py recent`: task127, task128, task129, task131, task130, task132, task133, task134, task135, task228, task229 and task445.
- `maturity_censoring`: 2 of 12 (task134, task445). The cap is a third of the batch (4), so this is under it.
- Withheld rule with an official decoy: 0 of 12 (`official_decoy` is false on every card). The cap is 2.
- Certified-record or validated decoy: 2 of 12 (task127, task129). The cap is 3.
- Other strategies: `binding_constraint` 2 (task127, task128) and `population_selection` 2 (task132, task228). Every other strategy appears once.

No share is over a cap, and task445's card is clean on all three decoy fields (`decisive_rule_filed: true`, `official_decoy: false`, `validated_decoy: false`).

## Corpus habits
These come from the screen's corpus-wide pass. They are not evidence about any pair, and task445 carries none of the file-name habits.
- File names: `data_dictionary` in 61 builds, `export_manifest` in 34, `data_notes` in 12 and `provenance` in 12.
- Deliverable pairings that keep recurring: pdf+csv in 9 builds, py alone in 8 and py+pdf in 7.
- The voice-check batch (task124 to task133, task229 and task445): 11 of 12 prompts are over 1,000 characters (task445 is the exception), no Code deliverable appears anywhere, and xlsx (6 of 12) and docx (5 of 12) dominate.
- The Main Ask opener "give me the single dollar figure we" appears in 2 builds.

## What to redraw
Nothing. The surname echo and the decision-type repeat against task229 are guard WARNs and are already on the record. No axis needs a redraw.
