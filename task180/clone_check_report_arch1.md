# Clone check: pre-flight, task180 against the whole corpus, 2026-10-11

## Verdict
CLEAN for task180: no Track A finding and no Track B finding. The three pairs the screen promoted on the same-driver label signature (task90, task72 and task103) are each Clean, shares components by design, and so is task58 v15, which this check promoted from a driver sweep. Separately, at batch level, the certified-record decoy stands at 7 of the last 12 builds against a cap of 3. That is a Strategy monoculture finding, and task180 is not one of the seven.

**Stage 5 gate (`build-pipeline`).** It holds:
- `guard.py heart` returns WARN, not BLOCK.
- There is no Exact, Same seed, Dataset or Template finding.
- There is no Shape echo or Idiom finding against task180.

## Scope and coverage
- **Mode and scope.**
  - This is a pre-flight on task180 against every other build, with the window ignored. The screen reports "all builds".
  - It was invoked as stage 5 of `/build task180`, on the author's licence.
  - The report sits in the task folder because the `build-pipeline` skill names `clone_check_report.md` among a task folder's reports. No earlier report existed for this scope.
- **Version checked.**
  - The pack is as rebuilt at 02:31. The design note is as committed at 02:36 (commit 42d8f51, "harden rung 0 before round 1"). The card is as committed in 80669a3. The prompt and submission are unchanged since 02:11 and 02:12.
  - The leak-check loop rebuilt the pack and rewrote the design note while this check ran. The mart moved from billing-account grain (`account_ref`) to one row per metering system, keyed by its primary supply number. The heating-only supplies moved to their own register sheet.
  - The decisive rung and the card's `driver` sentence did not change. The pipeline's rule is to re-run the adjudicated pre-flight only when the driver changes, so this check stands for the current build.
- **Extract.**
  - The repo cache (written 02:21:33) predated task180's card, design note, target and metadata, so I re-extracted.
  - To leave the repo untouched apart from this report, I ran `fingerprint.py extract --out` and `screen --cache` on a scratch copy of the cache. That copy carries the fingerprints of builds not on this checkout exactly as an in-place run would.
  - I ran it twice: at 02:25, and again at 02:35 after the rebuild. The promoted and nearest pairs were identical at full precision.
- **Builds compared.** The cache holds 126 builds. The screen covers 124, because task1 and task2 have no prompt or pack. That gives 123 pairs.
- **Pairs promoted by the screen: 3.**
  - They are task90, task72 and task103, all on the same-driver label signature: decisive gap `population`, decisive pattern `D` and Gate G `decomposition_attribution`.
  - Exactly four live cards carry that signature: task72, task90, task103 and task180.
  - `guard.py surface` had promoted task90 and task72. task103 is the third.
- **Pairs adjudicated: 4.**
  - These are the three above plus task58 v15. I promoted task58 from a sweep of every card driver, lineage driver, stump sentence and ledger mechanism cell for task180's construction (dilution, summing, components, sub-units, per-meter screening).
  - The label route cannot see task58, because it shares none of the labels the screen scores.
  - The same sweep surfaced task52 and task117. I read both on their cards and recorded them under Clean.
- **Pairs left unread: 117.** None was promoted.
  - The top surface neighbours are task97 (98.7th percentile), task131 (97.8th) and task109 (96.0th), then task52, task71 and task55 (about the 90th).
  - They score on flat layout and format mix, plus a shared decisive gap for task131, task109 and task52. That is corpus idiom, not a finding.
- **How the reading was done.**
  - No subagent tool was available in this thread. I adjudicated each pair here, in sequence and from its own evidence.
  - The comparison builds' folders are not on this checkout. The cache records them under `/Users/saa/Developer/Projects/handshake/`.
  - For task72, task90, task103 and task58, the evidence was:
    - the fingerprint card, each with `mechanism_source: design_note`;
    - the ledger rows;
    - the cached submission (steps, critical components and recommendation), the ask sentence, the deliverables and the target listing.
  - **Their design notes and full prompts could not be read here.**
  - For task180 I read the design note, prompt, submission, card and pack listing in full.
  - I opened no golden and no answer key.
  - The `clone-check` skill is not registered in this session, so the tiers come from the current `.claude/skills/clone-check/SKILL.md`, read at the start of the run.
- **Guard.**
  - I re-ran `guard.py heart task180` by importing it with its people cache pointed at a scratch copy. A direct run would have rewritten `.claude/skills/fingerprint/.cache/people.json`, because task180's folder is newer than that file.
  - Verdict: WARN, not BLOCK. The nearest heart text is 0.08 (task131), against a BLOCK threshold of 0.30.
  - The WARNs are driver.near against task131 (0.15) and task52 (0.14), and repeat.decision after task131. All are answered in the design note.
  - I did not re-run `guard.py surface`, because it rewrites the repo cache and the people index.
- **Mechanism coverage, over the 123 pairs.**
  - Track B was scored from both cards on 101 pairs. Of those partners, 14 carry back-fitted labels: task11, task12 and task25 to task36.
  - 22 pairs were checked on Track A only:
    - 17 partners have no mechanism layer: task3 to task10, task13 to task15, task18, task19 and task21 to task24. Five of those cards are `submission_only`.
    - 5 are note-only. task16, task17 and task20 have cards with no gap or pattern; task112 and task113 have no card.
  - The driver sweep read every card that exists.
- **Outside the screen.**
  - task114, task115 and task116 have cards but no fingerprint record. The guard's card pass and the sweep covered them, and none carries task180's signature:
    - task114 is time / A.
    - task115 is time / D / forecasting.
    - task116 is population / C / binding_constraint.
  - No Track A was possible for those three.
  - task99 is excluded as the scratch slot, which is correct.
- **Pack-level Track A gap.**
  - task117 to task129 have no `target/` folder on this checkout. task117 and task119 ship `target.zip` only; the rest have neither. The pipeline's own cache has the same gap.
  - So pack-level Track A (file names, column sets, numeric signatures) ran on 108 of the 123 partners.
  - As a mitigation, I checked three things:
    - Neither zip shares a file name with task180.
    - No card's spine matches task180's spine file or grain.
    - Prompt and submission Track A ran for all 123 partners.
- **Staleness.**
  - task117 to task131 and task180 were re-extracted from disk.
  - task3 to task113 are fingerprints carried over from another checkout. They cannot be refreshed here, but their cached card blocks match the current card files exactly.

## In batch against earlier builds
In pre-flight the batch is task180 alone, so every pair is task180 against an earlier build. The screen labels them "in batch" only because focus mode widens the window. **No hit against an approved or delivered build.**

Status of each adjudicated partner, from the ledger's status column:
- **task72 (v2).**
  - v1 was solved in two live rounds. The row records the re-root to v2 on 2026-09-06, built the same day, with stump-check round 3 not yet run.
  - Nothing in the row records approval or delivery.
  - The screen's "delivered or approved" rank is a false positive. Its status regex matched "service delivered under" in the mechanism prose inside that cell.
- **task90.**
  - Built, with no stump round and no portal result recorded.
  - The ledger's reconciliation table says the build continued "on the delivered list", so treat it as possibly delivered.
  - It is a byte-identical copy of task86 v1 and carries its own open Template finding against task72 v2. That finding is task90's, not task180's.
- **task103 (v4).**
  - Built, with no v4 result recorded.
  - v1 and v2 were solved on the portal, and v3's ask layer gave way.
  - It is not recorded as approved or delivered.
- **task58 (v15).**
  - Built. One round, before the ask wave, scored 49 per cent with the main call missed, and none has been run since.
  - It is not recorded as approved or delivered.
- **task180.** No ledger row; in build per the root `START_HERE.md`.

No pair carries a finding, so none of these statuses moves the verdict. If task90 is in fact delivered, that pair is the one where a finding would have been exclusion level. There is none.

## Track A findings, reviewer visible
None.
- **Hard tells.** Against every profiled pack there are no byte-identical files, no same-seed tables, no shared column sets and no shared rare file names. No pair carries an evidence line.
- **Surface on the adjudicated pairs.**
  - The scores are task90 0.095 (95th percentile), task72 0.086 (79th), task103 0.080 (66th) and task58 0.090 (89th).
  - All of it comes from flat layout and format mix. Masked prompt shingle overlap is 0.0045 at most.
- **Names.**
  - "Corran Energy" appears on no other card.
  - None of the nine personas repeats a full name.
  - One-off name overlaps pass the guard's people check: first names Jonathan (task106), Christopher (task127) and Debra (task130), and the surname O'Connor (task127).
- **`voice-check.py`, last 12.**
  - The opening move is constraint-first, 2 of 12 (with task124).
  - There is no carrier wording and no unlisted repeated run.
  - The prompt is 208 words against a batch median of 253.
  - The deliverables are pptx + csv, a pair no other build in the corpus uses.
- **File names.**
  - The pack avoids the habit names (`data_dictionary`, `export_manifest`, `provenance`).
  - Its notes role is `rp_extract_field_notes.md` and its log role is `extract_log_2026-12-07.txt`.
  - An extract-log file appears in 3 builds (task103, task131 and task180). That is a file role, not pair evidence.
- **Shape echo: none.** Against each adjudicated partner, at most one of the four outline axes is shared: ask construction, deliverable species, decision shape and calibration organ. The detail is below.

## Track B findings, mechanism
None.

The three promoted pairs collide on the label triple, and none of them shares the driver. The screen's evidence line ties the triple to "the one that caught the task86 v1 against task72 v2 Template". That Template is task90's own and does not transfer: task180 has no filed clause that keeps a unit running across a change of carrier or owner.

**History, not findings.** The heart's lineage notes land only on dead rows:
- task81 v3 first cut: retired on a Gate G review. Its driver is identity recovery of a unit re-registered next day with the same sub-unit set.
- task86 v1: retired on its Template finding. It is the same architecture as task90, adjudicated below.
- task72 v1: solved and archived.
- task103 v1 and v2: retired.

Nobody is sent to redraw over any of them.

## Clean, shares components by design
**task180's decisive move, domain nouns stripped.** A filed relative-shortfall test must run on each metered sub-unit's own series, and entities are then counted once. It must not run on the ready-made series that sums an entity's sub-units, because a large fall on one sub-unit moves the sum by a few per cent, inside ordinary variation.

**task180's path:**
1. Build weekly series per supply from cumulative reads, bridging meter exchanges and comms gaps.
2. Fit each supply on degree days over 104 weeks.
3. **Run the filed test per supply. This is the decisive step.**
4. Apply the exclusions by premises.
5. Count referrals by patch.
6. Produce the two asks: winter history (dedupe, appeals) and Q1 capacity.
7. Pick the patch.

Rung 0 is the same test run on the mart's weekly import. That series is keyed by the primary supply number and sums each metering system's supplies.

---

**task90 against task180.** Verdict: `clean_shares_components`, Track B. Axis to redraw: none.
- **task90's move.** Records keyed to the supplier's physical asset must be chained, through a buyer-side mapping, into the one buyer-side position that persists across the supplier's substitutions. A length-tiered tariff prices that position from its first day, and the flat-billed settled history cannot show the difference.
- **Not the same claim.**
  - task90 merges records over time into a longer-lived unit so that a duration tier applies. task180 splits a sum into its components so that a proportional fall is not diluted.
  - The grain moves in the opposite direction, for a different reason.
  - The solver has to see a different thing. In task90 it is an exchange continuing the same rental under a filed clause. In task180 it is a second, heating-only supply on its own meter.
- **task90's path.**
  1. Pair the tickets into stays.
  2. Map the stays to buyer trucks.
  3. Apply the off-rent clock.
  4. **Chain the stays into hires. This is the decisive step.**
  5. Price the tiers.
  6. Add the waiver and transport.
- **Shared components.**
  - Pattern D carries the decisive rung in both, on different constructions.
  - Both carry the Gate G label.
  - Both have a correct monitoring export as the natural series: the weekly on-rent report in task90, the mart in task180.
  - Both have a physical asset swapped under a persistent unit. In task90 that device is the decisive rung. In task180 it is demoted to Layer 1 (bridging cumulative reads across a meter exchange, where the supply number never changes), so it is reuse.
- **Outline.** No axis is shared:
  - decision: a quantity against which-of-N;
  - deliverables: pdf + json against pptx + csv;
  - calibration: a settled ledger with a validated decoy against none;
  - objective: ETL against anomaly detection.

**task72 (v2) against task180.** Verdict: `clean_shares_components`, Track B. Axis to redraw: none.
- **task72's move.** A correctly measured movement must be booked to the owner whose agreement covered each piece of service. For units that transferred mid-period, that is the origin owner under a filed terms clause. Both bookings partition the same rows, so no total, rate or reconciliation shows the difference.
- **Not the same claim.**
  - task72 moves rows between owners inside a linear decomposition where every total ties either way.
  - task180 moves no row. Each supply sits in one premises and one patch in both series, and the trap is a non-linear test run before or after summing.
- **task72's path.**
  1. Scope hygiene.
  2. Contracting records and the 1 May change of hands. This was v1's whole trap and is now its terminal decoy.
  3. **Rebuild the participant transfer chains and apply the terms clause. This is the decisive step.**
  4. Book the months by covering agreement.
  5. Split the movement into rate and composition pieces.
  6. Drill down by region and site.
- **Moves with no counterpart.** task72's rate and mix decomposition has none in task180. task180's per-supply series and its premises exclusions have none in task72.
- **Shared components.**
  - Pattern D at the decisive rung, on different constructions.
  - The Gate G label.
  - A pick-one-of-N decision with a runner-up.
  - A correct monitoring export at the wrong grain as the natural input: the quarterly regional dashboard in task72, the mart in task180.
- **Outline.** One axis of four is shared, the decision shape. The other three differ:
  - deliverables: pdf + png + py against pptx + csv;
  - calibration: a closed decision corpus against none;
  - ask construction.

  That is not a Shape echo.

**task103 (v4) against task180.** Verdict: `clean_shares_components`, Track B. Axis to redraw: none.
- **task103's move.** A contact record stands for one unit, and a standing authorization names further units it may serve. Only the handed-over quantity shows which authorized units were served, once it is decomposed into per-unit standard amounts under a one-allowance-per-period rule. The decision's count is each contact plus those units.
- **Not the same claim.**
  - task103 has to recover how many units a record served. It then runs its excess-over-baseline test on an additive count, where summing is harmless.
  - In task180 the units are listed in the register and their own series ship in the reads, so nothing has to be recovered. The error is running a ratio test on their sum, where summing is the harm.
- **task103's path.**
  1. Read the filed rules.
  2. Take the visit rows of record, deduplicating the re-sent batch.
  3. Count visits. This reproduces both certified determinations and gives no run (rung 0, the validated decoy).
  4. **Decompose each visit's weight under the one-hamper-a-week rule. This is the decisive step.**
  5. Count households per week.
  6. Apply the run test.
  7. Compute the amount.
- **Moves both share, low on the path.**
  - A filed baseline test sits mid-path in both and decides nothing in either.
  - A dedupe of re-sent or re-keyed records sits at hygiene level in task103 and in the ask layer in task180. That is a device reused at a low position on both sides.
- **Shared components.**
  - The anomaly-detection objective.
  - The `grain_or_unit` strategy.
  - Generators G2 and G16.
  - Pattern D at the decisive rung.
  - The Gate G label.
- **The closest overlap, since the 02:36 hardening.** task180's rung 0 is now a row keyed by one sub-unit's identifier that carries several sub-units. That is the same shape as task103's visit row, which is keyed by one household and carries hampers for others. In task180 it sits at rung 0, while in task103 it sits inside the decisive construction. The repairs also differ: task180 switches to the per-supply reads, task103 decomposes a quantity under an allowance. So this is a shared component, not the insight.
- **Outline.** No axis is shared:
  - decision: a go/hold amount against which-of-N;
  - deliverables: pdf + xlsx against pptx + csv;
  - calibration: a certified matrix with official and validated decoys against none;
  - context artifact: a published series against a monitoring export.
- **Strategy.** The shared strategy is counted under Strategy monoculture below. task103 sits outside the 12-build window.

**task58 (v15) against task180, promoted by this check rather than by the screen.** Verdict: `clean_shares_components`, Track B. Axis to redraw: none.
- **Why it was read.**
  - Of the scored labels it shares only the stump strategy `grain_or_unit`. Its gap is objective, its pattern is none, its Gate G is binding_constraint and its decision is a quantity.
  - The sweep nonetheless found it to be the nearest construction in the corpus.
  - Its surface score is 0.090 (89th percentile), and no Track B axis collides.
- **task58's move.** A non-negativity floor must be applied to each party's share after the entitlement split, not once to the parent's netted balance. That way parties on underwater parents are still paid, while every control total ties.
- **Not the same claim.**
  - In both builds the decisive rung applies a filed non-linear rule at the sub-unit grain, where the natural pipeline uses the parent key every source system shares. That makes this the closest pair in the corpus.
  - But the non-linearity and the thing to see differ:
    - task58 is the order of a settlement waterfall. The division of proceeds comes before a setoff that reaches only one party, and netting lets a negative share absorb positive ones.
    - task180 is signal dilution. A same-signed sub-unit that is unaffected shrinks a proportional fall below a band.
  - The decision also differs: an amount against which-of-N. And task58 carries a validated decoy.
- **Note for the author.** One construction now carries the decisive rung in two builds: apply the filed non-linear rule per sub-unit before aggregating. task58 v15 does it with a floor, task180 with a threshold. Neither the label route nor the lexical driver score (0.07) sees it, so check a third draw in this family by hand.

**Also from the sweep, read on the cards. Both are clean.**
- **task52.**
  - It shares gap and pattern D on the cards and sits at the 90th percentile.
  - Its driver is an entity milestone that fires when every sub-unit passes a threshold. The threshold is withheld and recovered from settled cases, and the slowest sub-unit binds.
  - That is a withheld rule and a minimum, not dilution, and the design note already answers it.
- **task117.**
  - A per-unit cap, applied before a load is summed, sits below its decisive rung. Its stump has the competent solver already applying it.
  - The decisive move is re-timing follow-on operations. The cap is a demoted device.

## Strategy monoculture
**Batch.** The last 12 builds in draw order ending at task180: task119, task121, task122, task124, task125, task126, task127, task128, task129, task130, task131 and task180. The counts come from the cards' fields.

| Measure | Count | Cap | Verdict |
|---|---|---|---|
| Withheld rule with an official decoy | 0 of 12 | 2 | under |
| Certified-record decoy (`validated_decoy`) | **7 of 12** | 3 | **over, Strategy monoculture finding** |
| Any one `stump_strategy` | max 2 of 12 | 4 (a third) | under |

- **The seven builds carrying the certified-record decoy:** task121, task122, task124, task125, task126, task127 and task129.
- **Strategies at 2 of 12:**
  - decomposition_attribution: task119, task122;
  - identity_resolution: task121, task126;
  - causal_design: task124, task131;
  - binding_constraint: task127, task128.
- **Official decoys.** task119 and task122 carry an official decoy with the decisive rule filed, so they are not the withheld-rule architecture.
- **Change since the task131 pre-flight.** That check counted 9 of 12. Two things changed since:
  - The window moved by one: task123 out, task180 in.
  - task130's card now files `validated_decoy: false`, after commit 14ee268.
- **Retirement caveat.**
  - That pre-flight reported task122 and task130 as retired or failed. The ledger is silent on both.
  - Dropping them pulls in task123 and task120, which both carry the flag, so the count becomes 8 of 12.
  - Either way it is over the cap.
- **task180's own strategy.**
  - It is `grain_or_unit`, with the decisive rule filed, no official decoy and no validated decoy, so it adds to neither capped count.
  - It is the only `grain_or_unit` build in the window.
  - Corpus-wide, 15 of 128 cards carry that strategy. The last before task180 was task108.

## Corpus habits
- **File names.**
  - `data_dictionary` appears in 61 builds and `export_manifest` in 33.
  - `data_notes` and `provenance` appear in 12 each.
  - `county_reference` appears in 4.
  - Eight other names appear in 3 each.
  - task180 uses none of them.
- **Deliverable pairings.**
  - pdf + csv appears in 9 builds, py alone in 8 and py + pdf in 7.
  - pdf + png appears in 6.
  - py + csv, py + xlsx and pdf + xlsx appear in 5 each.
  - docx alone appears in 4.
  - task180's pptx + csv appears in no other build.
- **Ask opening.** "give me the single dollar figure we" appears in 2 builds.
- **Decision shape.** pick_one_of_n carries 5 of the last 12: task119, task121, task122, task131 and task180. The last two are back to back. That is the guard's repeat.decision WARN, answered in the design note.
- **Objective.** Anomaly detection carries 3 of 12: task119, task125 and task180.
- **`voice-check.py`, last 12.** The "other" opening move is concentrated at 5 of 12 (task125, task126, task128, task129 and task130), and task180 is not one of them. There are no unlisted repeated runs.

## What to redraw
1. task180: nothing.
2. Batch, not task180: the certified-record decoy axis (`validated_decoy`), at 7 of 12 against a cap of 3, carried by task121, task122, task124, task125, task126, task127 and task129.

**Tooling notes.** None of these is a finding against any build.
- **Status regex.** The screen's status regex reads mechanism prose inside status cells. That is how task72 picked up the "delivered or approved" rank.
- **Unprofiled packs.**
  - A pack held only in `target.zip`, or absent altogether, is never profiled.
  - That leaves pack-level Track A blind for task117 to task129 on this checkout.
- **Ask parser.**
  - The screen's ask parser found no Main Ask in task180, task90 or task103.
  - Sentences opening "What I need is" fall outside its verb list.
- **Guard writes.**
  - `guard.py heart` rewrites the people index whenever any task folder is newer than it.
  - `guard.py surface` rewrites the clone-check cache.
  - A check that may write only its report has to redirect both, as this one did.
- **task180's card lags the build.**
  - The card's `driver_concrete`, `stump` and `spine` fields still describe the account-grain mart. The spine names `smart_daily_register_reads_...` with 0 rows.
  - The pack and the design note moved to the metering-system mart at 02:31 to 02:36.
  - The abstract `driver` covers both versions, and it is the field the screen and this check compare.
