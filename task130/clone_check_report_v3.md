# Clone check: pre-flight, task130 (architecture v3) against every other build, 2026-10-11

## Verdict
CLEAN. task130 v3 hits no clone tier on either track. Both promoted pairs (task132 and task83) are clean and share components by design, and no other card, lineage driver or ledger row carries its decisive move: a cohort chosen on an extreme outcome regresses, so the untreated cohort chosen the same way a year earlier is the counterfactual.

## Scope and coverage
- **Mode.** Pre-flight on one build, `/build` stage 5. The build is task130 architecture v3 (the Red Cedar Valley care-management baseline) at commit 2d155fb on `sathya8571/task130-harden`, with main merged. It is compared against every other build, and no window applies. v1 and v2 belong to task130's own lineage, so they are not compared. The data is already cut, so a Track B finding at this point would have cost the build. None was found.
- **Corpus.**
  - wt130 has task117 to task133 on disk (task132 is missing), plus task229.
  - task1 to task113 come from fingerprints cached on the author's original checkout. Their folders are not on any disk here.
  - task132 was added read-only from the parallel checkout (branch `sathya8571/task132-relay-final-buy`). Its card exists only on that branch, and its pack is a snapshot taken while realism repair 3 is in flight.
  - The committed `target.zip` of task117, task119 and task229 were unpacked into scratch so the script could profile those packs.
  - The task132 and zip additions went into a scratch copy of the cache. Nothing was written into any checkout except this report and the extract's own cache in wt130.
- **Cache check.**
  - The cache on disk was stale. It had been written from `/home/user/wt133`, it still held task130's v2 card (housing), and ten of task130's target files were newer than it.
  - It was re-extracted in wt130: 127 cards, 125 of them screenable.
  - The cached mechanism fields match the current cards for every build in the cache.
- **Screen.** `screen --focus task130` over the assembled cache screened 126 builds and scored 125 pairs. It promoted 2, both on surface percentile only:
  - task132 at 0.152 (corpus top 1 per cent, two numbers apart);
  - task83 at 0.140 (corpus top 1 per cent).

  Both scores come entirely from three coarse axes: a flat layout, the format mix, and the same deliverable pair (xlsx, then docx). File names, schemas, numeric signatures, byte hashes, invented names and masked write-up constructions all score zero. The masked prompts score zero against task83 and share one shingle with task132.
- **Corpus baseline.** Over 7,875 corpus pairs the surface score has a mean of 0.058, a median of 0.075 and a 99th percentile of 0.104.
- **Mechanism routes.** None fired.
  - No pair shares task130's decisive gap and decisive pattern together (objective, A).
  - No pair carries the same-driver signature (gap, pattern and Gate G).
  - No pair within two numbers shares two core axes. 19 earlier builds share two (the gap or pattern A, plus `quantity_figure`), and none of them is within two numbers.
- **guard.py heart task130** (cards from wt130 plus task132's): WARN.
  - Heart text similarity peaks at 0.06 (task102's stump), under the 0.12 warn line.
  - The structural bans are clear.
  - The only flags are on `people.first`: Phillip (task101) and Michelle (task104).
- **Supplementary sweep.** Every card's driver, `driver_concrete`, stump and lineage drivers (131 cards), and the shipped ledger, were searched for three ideas and their phrasings:
  - selection on the outcome;
  - regression to the mean;
  - an untreated earlier cohort as the counterfactual.

  The phrasings included extreme, noisy, one-off, flagged, chosen on, would have anyway and baseline. Outside task130, the only mention of regression to the mean is task6's lineage note on a returned review. That records a defect in that build, not its driver. The sweep and the card tallies (pattern, strategy, spine) raised four component neighbours (task124, task33, task27, task51), which are read at card level below.
- **Adjudicated: 2 pairs**, the 2 promoted. No promoted pair was left unread.
  - The other 123 pairs were screened and swept but not adjudicated one by one.
  - The four pairs raised by the sweep and the card tallies were read at card level and are labelled that way. None counts as adjudicated.
- **How adjudication was done.** This session has no subagent tool, so each pair was read in this thread, using the inputs and questions the per-pair adjudicator would get.
  - task132's side used its card, prompt, write-up, design note and target listing, read from its own checkout.
  - task83's prompt, write-up and design note are not on any disk here. Its side used the card (driver, `driver_concrete`, stump, lineage), the ledger rows, and the cached write-up extract (steps, critical components, recommendation) and target listing.
- **Mechanism coverage** over the 126 screened builds:
  - 104 read from a card: 90 native and 14 with back-fitted labels (task11, task12, task25 to task36).
  - 5 note-only (task16, task17, task20, task112, task113).
  - 17 with no mechanism layer (task3 to task24).
  - Those 22 were checked against task130 on Track A only by the screen. The guard heart and the sweep still read the driver sentences their cards carry.
  - task114, task115, task116 and task228 have cards but no fingerprint, so they were checked on Track B only (guard and sweep).
  - task99 is excluded by the script as a scratch number.
  - task1 and task2 cannot be screened (no prompt, fewer than three target files).
- **What was not checked.** The packs of task118 and task120 to task129 (and task3 and task10) are not on any disk. `task*/target/` is gitignored and these builds have no zip. So the byte-identical, same-seed, schema and file-name checks did not run against them. Their prompts and write-ups were screened.
- **Status record.**
  - Ledger rows run to task108.
  - Eight ledger cells read approved: task25, task27, task28, task29, task30, task33, task34 and task35.
  - The screen also labels task48 and task72 delivered, but only because the word appears in their ledger prose. task48's cell records the author rejecting the build, and task72's records a re-root. Neither is recorded as approved or delivered.
  - task117, task119, task131, task133 and task229 have no ledger row. Their own `pipeline.json` records delivery to the author, but on the ledger their status is unknown.
  - task130 and task132 have no row; both are in flight.
- **Tooling defects found on this pass.** None changes a tier.
  1. The cache was stale and came from another worktree (see the cache check above).
  2. The deliverable species check is order-sensitive. `['xlsx', 'docx']` and `['docx', 'xlsx']` score as different species, so task125 does not register the pair it shares with task130.
  3. The file-name check compares exact stems, so it cannot see a naming pattern shared under different system prefixes (`claims_`, `eam_` and `ecl_extract_dictionary.txt` in task130, task132 and task133).
  4. The forum vocabulary keeps `trustees_or_governors` apart from `board_of_directors`. So the guard's forum ban passes task133 against task130, although both prompts send the figure to "the board" on a named date.
  5. The status classifier defects that the loop 1 report recorded are still present:
     - task48 and task72 are read as delivered;
     - task51 is read as retired, while its cell reads "v5 built 2026-08-27, awaiting round 1".

## In batch against earlier builds
Pre-flight has no window, so this section reads task130 against every earlier build, starting with the ones the ledger records as approved.

- **Against the eight approved builds: nothing at any tier, and none promoted.**
  - Surface: task30 0.087, task28 0.080, task35 0.080, task29 0.077, task27 0.073, task33 0.073, task34 0.020, task25 0.013. All are at or below the corpus 90th percentile.
  - On the cards, task33 shares the decisive pattern (A) and the stump strategy (`forecast_method_backtest`).
  - task35 shares pattern A and `quantity_figure`.
  - task25 and task28 share only the decisive gap label (objective).
  - task27 shares a device that task130 demotes.
  - Card-level reads below find a different driver in each. All eight carry back-fitted labels.
- **Against builds delivered to the author on their own record, with no ledger row** (task117, task119, task131, task133, task229): none promoted.
  - task133 shares only the decision type.
  - task119 shares only the gap label.
  - task117 shares the decision type and the context-artifact type.
  - task133 also shares a Track A idiom with task130 (Corpus habits).
- **The previous pre-flight's Template does not carry over.** That finding (v2 loop 1 against task73 world ten) was against a spent architecture. v3 shares only the gap label with task73.

Nothing here reaches exclusion level.

## Track A findings, reviewer visible
None at a clone tier.

- **task130 against task132** (both in flight, no ledger rows). This is a note below the Shape echo tier.
  - **Shared outline.**
    - The deliverable pair: a workbook of the cuts, then a one-page docx memo for the decision maker that opens on the figure and carries one chart.
    - The memo's commission sentence: "a one-page memo, `..._memo.docx`, that opens with" the call, then "charts" or "shows ... as a chart" one series.
    - The dictionary's file-name pattern: `claims_extract_dictionary.txt` against `eam_extract_dictionary.txt`.
    - The spine's file-name pattern: `<records>_<YYYY-MM>_<YYYY-MM>.csv`.
  - **What differs.** The decision shape differs: a tier-by-benefit grid of baselines against a lot count with a cover table. So does the calibration organ: the bid cohort against none. Nothing else is shared: no file name, schema, value, invented name or other sentence.
  - **What clears it.** Reword task130's memo commission and rename its dictionary in the administrator's own idiom. No figure moves.
- **task130 against task83** (the ledger records task83 as built, with no stump result recorded for the parity build). The two share only the deliverable species and flat layouts. Not a finding.
- **A weak one-word name overlap.** "Ellery" (task130's administrator, Ellery Benefit Administrators) is also a county in retired task120's generator and a town ("Port Ellery") in the unbuilt task268 seed. It is a single token, not a shared multi-word invented name. It is recorded so that task268's draw sees it.

## Track B findings, mechanism
None.

task130's decisive move, with the domain nouns stripped: a group chosen for an extreme value of a noisy outcome is forecast from the next-period outcome of a group chosen the same way one period earlier and left untreated, not from its own chosen-period value carried forward, because the outcome regresses toward the mean.

- No card, lineage driver, card stump or ledger row makes that claim.
- No pair carries the same-driver signature.
- The guard's heart text tops out at 0.06.
- The data stands as built, and no repair is due.

## Clean, shares components by design

### Adjudicated (promoted)

**1. task130 against task132: clean, shares components.**
- **Drivers.**
  - task130: a cohort selected on its outcome, valued by the next year of an untreated cohort chosen the same way.
  - task132: an expected event count per position over a horizon has to restart the age-dependent rate after each event, because a failed item is replaced by a new one. The present item's ageing rate does not run for the whole horizon (renewal against cumulative hazard).

  These are not the same claim.
- **task130's path.**
  1. Net claim versions and PBM reversals.
  2. Member months.
  3. The final list's 2026 PMPM.
  4. Crosswalk the bid list.
  5. The bid cohort's next-year PMPM, trended 24 months. This is the decisive step.
  6. Weight the tiers.
  7. Certify.
- **task132's path.**
  1. Failures by module-age band.
  2. Module-months over the go-live window.
  3. End of support per relay.
  4. The present module weighted by survival, plus a replacement in the 0-9 band. This is the decisive step.
  5. Stock available.
  6. Poisson cover.
  7. Price.
  8. Order.
- **Shared devices, and where each sits.**
  - A system go-live with legacy identifiers or dates.
    - In task130 it is the administrator conversion, a Layer 1 rung at R5a, and the fact that rules out the ratio form.
    - In task132 it is the go-live exposure window. That window carried task132's decisive rung in its round 1 and is now an ordinary step (rung 2).
  - A superseded version beside the approved one: the January draft list in task130, the 2025 renewal plan in task132.
  - Rates over exposure units: member months in task130, module-months in task132.
  - The forecasting Gate G mechanism. The whole lane shares this by design.

  None of these devices carries the decisive rung in either build now.

**2. task130 against task83: clean, shares components.**
- **Drivers.**
  - task83: a randomised holdout's effect, measured per score band, has to be split by each unit's own prior treatment history. Only first-pass units respond, and the target pool's history mix differs from the measurement corpus. The split decides an allocation under a binding cap.
  - task130: regression under selection on the outcome.

  These are not the same claim.
- **Shared devices.** A model-scored population in bands or tiers, and an untreated comparison group.
- **Positions.**
  - task83's untreated group is the standing randomised holdout, the measurement instrument under every rung. Its decisive move is grouping the offer log per reader (step 3 of 7).
  - task130's untreated group is the decisive rung itself (the never-enrolled bid cohort, step 5 of 7).
  - task83's split by history has no counterpart in task130.

### Card-level reads outside the funnel (not promoted, not adjudicated pair by pair)

**3. task124** (no ledger row; `hardened` on its pipeline record).
- Both builds read the answer off a comparable group's untreated record, so that estimator has now been spent twice.
- What rules out the obvious basis differs:
  - In task124, the comparables' own reads are held down by an intervention the forecast units cannot join, even outside its hours on called days. Only uncalled days that match the peak condition serve.
  - In task130, the cohort's own level is extreme because it was chosen for being extreme.
- A third build that reads its answer off an untreated comparison has to differ on that ruling-out step, as these two do.

**4. task33** (approved). It shares pattern A and the forecast back-test strategy, but the drivers differ.
- task33 picks one of N candidates: which elevations are ongoing and which have already resolved, projected to a filed intervention and back-tested on closed actions.
- task130 certifies a baseline figure for a cohort selected on its outcome.

Its label is back-fitted.

**5. task27** (approved).
- Reversal netting carried task27's decisive rung: reversals on a separate ledger, behind a join.
- In task130, netting claim versions and PBM reversals is Layer 1 (R6, -8.3 to +5.7 per cent on the total).
- The device has been demoted, so this is reuse.

**6. task51** (the ledger cell reads v5 built, awaiting round 1). Both value an intervention against a baseline that moves on its own inside the window.
- In task51 an unfiled standing rule moves that baseline.
- In task130 selection on the outcome moves it.

task130's card already records this difference.

## Strategy monoculture
The window is the last 12 cards in draw order: task124, task125, task126, task127, task128, task129, task131, task130, task132, task133, task228 and task229.

- **`stump_strategy` shares.**

  | Strategy | Count | Builds |
  |---|---|---|
  | `causal_design` | 2 | task124, task131 |
  | `binding_constraint` | 2 | task127, task128 |
  | `population_selection` | 2 | task132, task228 |
  | `withheld_rule_corpus_fit` | 1 | task125 |
  | `identity_resolution` | 1 | task126 |
  | `composition_mix` | 1 | task129 |
  | `forecast_method_backtest` | 1 | task130 |
  | `stated_rule_hard_construction` | 1 | task133 |
  | `grain_or_unit` | 1 | task229 |

  No strategy reaches a third of the window (4 of 12).
- **Withheld rule with an official decoy:** 0 of 12. task119 and task122 carry it in the 15-card window, which makes 2 of 15, within the cap.
- **Certified-record decoy (`validated_decoy`): 5 of 12, over the cap of three.** The builds are task124, task125, task126, task127 and task129.
  - task125 and task127 are retired on their pipeline record.
  - That leaves three still in play (task124, task126, task129), exactly at the cap.
  - A batch that ships all three together sits at the client's count.
- **`decisive_rule_filed` false:** task124, task125, task127 and task130. task130 files no official decoy and no validated decoy. Its card records the decisive step as an estimator choice that the filed estimand implies: Schedule C defines the quantity, not a method.
- **task130 v3 adds to neither capped architecture.** `forecast_method_backtest` appears once in the window, and on 6 of 131 cards across the corpus (task17, task33, task46, task89, task104, task130).

## Corpus habits
- **Dictionary file names.**
  - The old habit is `data_dictionary` (61 builds) and `export_manifest` (33). task130 uses neither.
  - The author's lane has a new one: `<system>_extract_dictionary.txt` in task130, task132 and task133.
  - Other names built on `_extract_` fill the same role in task93, task100, task102, task103, task106, task108, task110, task119, task131 and task229.
  - The screen's stem comparison cannot see this.
- **Date-range suffix.** Files named with a `<YYYY-MM>_<YYYY-MM>` range suffix appear in task130 (two files), task132 (two), task133 (one), and task103, task106 and task111.
- **Deliverable pairing.**
  - A workbook plus a short board document (a docx memo or pptx slides) appears in 7 of the last 15 builds in draw order: task119, task124, task125, task129, task130, task132 and task133.
  - It appears in all three of the author's current forecasting builds.
  - xlsx with docx exactly appears in task83, task125, task130 and task132.
- **Memo commission wording.** The spec requires that the text deliverable opens on the call. The habit is the wording: "a one-page memo, `..._memo.docx`, that opens with ..." in task130 and task132. task133's "the first states the allowance ... the second charts ..." is the slide version of the same request.
  - The three openings differ (stakes-first, constraint-first, number-first). The resemblance sits in the closing commission and the file names.
- **Board audience on a named date.** A board, trustees or committee audience on a named date frames 7 of the 18 recent prompts read (task117 to task133 and task229): task119, task123, task124, task127, task130, task131 and task133. task130 and task133 are adjacent in draw order, and both send their figure to "the board".
- **Two-sided stakes opening.** task130 opens "too high and we pay ..., too low and they dispute it". Retired task125 opens "order too few ..., order too many ...". Both concern a vendor's contract year from April 2027 to March 2028.
- **voice-check** over its 12-build window (task122 to task133 and task229; task132 is not on this disk):
  - no carrier phrase flagged;
  - no unlisted six-word run shared by a third of the batch;
  - task130 is the shortest prompt at 168 words (median 247).
- **Wider corpus (from the screen).**
  - The Main Ask opens "give me the single dollar figure we" in 2 builds.
  - Deliverable pairs in older builds: pdf+csv 9, py 8, py+pdf 7.

## What to redraw
Nothing reaches a clone tier, and nothing needs a rebuild. Two Track A items would only reduce how much the lane's builds resemble each other. The more expensive comes first:
1. task130: the dictionary file name (`claims_extract_dictionary.txt`), renamed in the administrator's own idiom in the generator. No figure moves.
2. task130: the memo commission sentence in the prompt, the wording it shares with task132.
