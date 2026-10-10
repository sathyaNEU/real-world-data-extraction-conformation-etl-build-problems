# Clone check: pre-flight, task130 (v2, Tenter House replacement units) against the whole corpus, 2026-10-10

## Verdict
SHAPE ECHO only (Track A, soft), against task86 (housing list worked by bedroom size) and task125 (council call-off, shared `calloff_2027` deliverable stem). No reject-tier finding: no Exact, Same seed, Dataset or Template.

## Scope and coverage
- **Mode:** pre-flight on one build, as the pipeline asked (stage 4, duplicate check). task130 is compared with every other build and the window is ignored. Its own v1 lineage row is the same task, so it is not a comparison.
- **Extract:** re-run before the screen. The cache predated only `task130/pipeline.json`, but it was re-run anyway. 15 builds were fingerprinted from disk (task117 to task131) and 110 cached cards were kept for builds not on this checkout, giving 125 cards, 123 of them screenable.
- **Screen:** `fingerprint.py screen --focus task130`. 122 pairs in scope, 3 promoted (task100 surface 0.147, pct 99; task87 surface 0.143, pct 99; task80 on the card signature). These match the pipeline's `guard.py surface` result. `guard.py check` re-run: PASS, with two NOTEs against task80 that are already differentiated on the card.
- **Adjudicated: 7 pairs.** The 3 promoted pairs, plus 4 the screen did not promote:
  - task86 and task50: found by sweeping every driver on file, retired lineage drivers included, for queue, rank and rationing mechanisms.
  - task125: shares five card axes with task130.
  - task108: shares eight card axes and a rationing context.
  The consecutive pairs (task129 and task131 on either side, and task127 and task128 for Part 6.1) were checked mechanically on both tracks and on the forum, forcing-event and org-family bans. All are clean.
- **Unread: 113 pairs**, none of which the screen promoted. The six nearest unpromoted neighbours (task37, task57, task108, task50, task32, task38) share only the decision family, formats or flat layout, apart from task108 and task50, which were read.
- **How adjudication was done.** This thread had no subagent tool, so the 7 pairs were read here, one at a time, with the same inputs and questions the per-pair adjudicator would get. task130's side used its card, design note, prompt, submission (blocks 1 to 3 only) and target listing. The other side used only the fingerprint card (driver, stump, lineage, differentiation) and the cached Track A fingerprint: the task50, 80, 86, 87, 100 and 108 folders are not on this checkout, so their design notes could not be opened. Their cards are design-note sourced, except task50, which is ledger sourced.
- **Mechanism coverage, corpus wide:**
  - 101 builds read from a card and 5 from a design note only.
  - 17 have no mechanism layer and were checked on Track A only (task3 to task24).
  - 34 builds carry back-fitted labels.
  - All seven counterparts read here have native card labels.
- **What was not checked.** Target packs for task117 to task129 are not on this checkout (`task*/target/` is gitignored until delivery), so byte-identical files, same-seed tables, schemas and file names against those 13 builds could not be screened. Their prompts and submissions were screened. To compensate:
  - task130's generator imports nothing outside its own folder.
  - No card shares its spine (`ta_placements_2018-04_2026-09.csv`, 28,016 rows, placement grain).
  - No card shares an invented name or a full persona. "Corvane" appears only in two idea-seed notes under `analytical_tasks/`, which are never submitted.
- **Status record.** The ledger has no current row for task130, correctly so while it is in flight. None of the counterparts has a portal result recorded for its current architecture (task80 v2, task86 v2, task87 v9, task100 v2 and task108 v1 are "built, listed for a ledger refresh"). task125 has no ledger row; its pipeline.json records it as retired (judge SEND_BACK, not submitted). So the delivery status is **unknown** on the other side of every pair, except task125, where the pipeline state says it was never submitted.

## In batch against earlier builds
Pre-flight mode, so every pair is task130 against an earlier build. (The screen labels them all "in batch" because focus mode sets the window to the whole corpus. That is a labelling quirk, not an exclusion bug.) No pair reaches exclusion level, and no counterpart is recorded as approved or delivered on the ledger.

## Track A findings, reviewer visible

**1. task130 against task86 v2: Shape echo (soft, not reject).**
- **Status:** task86 is built with no portal result recorded (unknown). task130 is in flight. 44 builds apart, not consecutive.
- **Shared surface:** no text, file-name, schema or entity overlap (surface 0.077, pct ~55). What a reviewer holding both would recognise is the outline:
  - a housing authority working a waiting list, in priority order, within bedroom size, against units coming available;
  - an answer that is a count vector by bedroom size (task86: 15/20/16/54/19 units; task130: 0/7/20/19);
  - a workbook paired with an image (task86 xlsx+svg, task130 xlsx+png);
  - a period-by-period roll down the list (task86's offer roll, task130's month-end run-off).
- **Clears it:** nothing is required. The echo comes from the domain's own furniture, and the drivers differ (see Clean). If the author wants more distance, the axis is the reviewer-visible answer form, the count-per-bedroom-size vector.

**2. task130 against task125: Shape echo (soft, not reject), against a build its pipeline records as retired and never submitted.**
- **Status:** task125 has no ledger row and its pipeline.json says retired (judge SEND_BACK, not submitted). Five builds apart.
- **Shared surface:**
  - an English council in GBP sizing a call-off quantity under a framework for April 2027;
  - shape 02;
  - `quantity_figure`;
  - forcing event `purchase_order_or_contract`;
  - org family `local_government`;
  - context artifact `operations_log`;
  - an xlsx deliverable with the stem `calloff_2027` (`examination_calloff_2027-28.xlsx` against `tenter_house_calloff_2027.xlsx`).

  The prompts share no sentence construction (prompt_masked 0) and the drivers are unrelated: task125's turns on how a linked unit's payment splits after a component ends, task130's on queue rank against supply.
- **Clears it:** a rename of the task130 workbook stem away from `calloff`. Prompt and golden move together. No ladder change. Low priority while task125 stays unsubmitted.

**Card defect found on the way (not a finding):** `task130.json` lists the deliverables as `tenter_house_replacement_units.xlsx` and `tenter_house_runoff.png`, but the prompt and golden name `tenter_house_calloff_2027.xlsx`. The guard's deliverable comparison therefore ran on a stale name, which is why the task125 stem echo did not surface mechanically.

## Track B findings, mechanism
**None.** No pair shares the driver. This includes task80, which the screen promoted on the same-driver signature.

## Clean, shares components by design

- **task80 v2: clean, label collision only.**
  - The cards collide on gap `rule`, generator G16 (the screen reports this as "pattern G16"; both cards' pattern field is `none`, so the collision is on the method-selection generator family), Gate G `method_or_model_selection`, `quantity_figure` and `operations_log`.
  - task80's decisive move: a fixed-term status is dated from the event that conferred it, not from when it was first observed operating.
  - task130's decisive move: a closed group's departures are each member's rank inside a priority list against a cumulative planned supply, not a rate.
  - Not the same claim, and no move on either path appears on the other.
  - The card's differentiation line holds.

- **task100 v2: clean, shares a component.**
  - Both roll a membership forward to a future date with exits removed.
  - In task100 the roll is rung 4 of six, and the driver is enumerating the exit class by finding the same member on the prior snapshot (early completers).
  - In task130 the roll is the frame, and the driver is that exits follow queue order.
  - The 0.147 surface is flat layout, an overlapping format mix and an xlsx+png pair only. Prompt, file names, schemas and entities all score 0. That is proximity, not a finding.

- **task87 v9: clean.**
  - task87's driver is an exclusivity constraint: two owed items meeting in one time slot cannot both be taken. That is a `binding_constraint` stump.
  - No shared device beyond a forward count against a plan.
  - The 0.143 surface is the same xlsx+png, flat-layout proximity as task100.

- **task86 v2: clean, shares components (the closest mechanism neighbour in the corpus).**
  - Shared device: working a priority-ordered housing list, by bedroom size, against unit supply.
  - Position of the device:
    - In task86 the order is filed (ACOP 4.2) and sits low. The competent solver already recovers the guidelines from the offer register and works the list. The driver is a hidden earlier draw on the same pool (another building's lease-up, visible only in an inventory row) that empties the front of the list first.
    - In task130 the list frame itself is the decisive rung, unfiled and recovered only by asking who got each let.
  - Stated with the nouns stripped:
    - task86: "a prior draw on the shared pool, sized only in an inventory row, removes members before the decision's own draw";
    - task130: "departures are a rank against cumulative planned supply, not a rate".
  - Different claims. The device moved from a supporting rung to the decisive one, so this is reuse, not cloning. The Track A echo is recorded above.

- **task50 v4: clean, shares a component.** Mechanism from the ledger, card label native.
  - Shared device: projecting an ordered queue forward to count how many members of a fixed group are reached by a date.
  - In task50 the issue order is filed and corpus-validated, the solver already replays the queue, and the missed insight is to count only what ships inside the funded window.
  - In task130 the date is explicit, and the missed insight is that departures follow an order at all.
  - Different decisive claims, and a different decision family (pick one of n against a quantity).

- **task108 v1: clean, shares components.**
  - Shared: shape 02, Forecasting, `quantity_figure`, `procurement_lead`, `purchase_order_or_contract`, G2 and G16, Gate G `method_or_model_selection`, and a rationed-supply context.
  - task108's driver is counting grain: demand of record is first requests, with resubmissions of rationed cuts removed.
  - task130's is allocation order.
  - Different claims. 22 builds apart. Proximity on the outline is worth knowing when the next procurement-lead forecast is drawn.

- **History, dead rows only.** task98 v2 ("units needed are a prefix of an ordered list", retired 2026-10-03, not stumped) and task37's completions v1 ("a queue-rationed place" among filed conditions, retired, solved) both touch ordered-list ideas on retired architectures. Neither turns on a rate-against-queue model choice. Nobody needs to redraw anything.

## Strategy monoculture
Window: the last twelve builds, task120 to task131. Shares come from the cards' `stump_strategy`, `decisive_rule_filed`, `official_decoy` and `validated_decoy` fields.

- **By strategy:**
  - identity_resolution: 3 (task120, task121, task126)
  - binding_constraint: 2 (task127, task128)
  - causal_design: 2 (task124, task131)
  - decomposition_attribution: 1 (task122)
  - time_semantics: 1 (task123)
  - withheld_rule_corpus_fit: 1 (task125)
  - composition_mix: 1 (task129)
  - other: 1 (task130)

  No strategy reaches a third of the batch.
- **Withheld rule with an official decoy:** 0 of 12. Under the cap.
- **Certified-record decoy (`validated_decoy: true`): 9 of 12, over the cap of three.** The builds are task120, task121, task122, task123, task124, task125, task126, task127 and task129. Over the last fifteen it is 11 of 15 (task117 and task118 added). **task130 is not one of them** (`validated_decoy: false`, calibration form none, and no certified figure blesses the rate reading), so this finding is about the batch, not about this build. task130 is one of three of the twelve that relieve it.
- **Label note on task130:** `stump_strategy: other` is defensible (allocation order is not a limit that removes the natural pick). The nearest vocabulary key is `forecast_method_backtest`, which no build in the last twelve carries, so relabelling would trip no ban.

## Corpus habits
- **File roles named the same way:** `data_dictionary` in 61 builds, `export_manifest` in 33, `data_notes` in 12, `provenance` in 12. task130 avoids all four (`housing_needs_extracts_dictionary.txt`, no manifest), which follows the CLAUDE.md naming rule.
- **Deliverable pairings that recur corpus wide:** pdf+csv 9, py 8, py+pdf 7, pdf+png 6, xlsx+png 6 (task87, task100, task102, task106, task120, task130).
- **Last twelve builds:** xlsx in 6 of 12 and png in 5 of 12. The png+xlsx pairing is what put task87 and task100 at the top of the surface ranking for task130.
- **Opening moves:** voice-check classifies 5 of the last 12 openings as `other` (task130 included, which its card calls evidence-first). That is a concentration flag on the classifier's coverage, not on the prose. No carrier wording or unlisted 6-word run is shared across a third of the batch.
- **"Call-off" as the forcing frame:** used in two English-council builds five apart (task125, task130). See Track A finding 2.

## What to redraw
1. task130: nothing on Track B. The draw stands.
2. task130: optional, Track A. Rename the workbook stem away from `calloff_2027` (prompt and golden together). It echoes task125, which was never submitted.
3. task130 card: bring `deliverables` in line with the prompt and golden (bookkeeping, author's call).
