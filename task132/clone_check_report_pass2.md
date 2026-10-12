# Clone check: pre-flight, task132 pass 2 (VPR-340 PSU last-time buy, architecture v1 after hardening loop 1) against the whole corpus, 2026-10-11

## Verdict
No clone tier reached (no Exact, Same seed, Dataset, Template or Shape echo against any build). The worst item is on Track B, task132 against task133: the decisive pattern G9 repeats back to back. That breaches a Part 6.1 standing ban, and `guard.py` blocks it the moment the two cards meet, but it is adjudicated below Template because the drivers differ. Track A carries one soft echo: the invented name "Ironwood", shared with task124.

## Scope and coverage

**Mode and scope.** This is a pre-flight on task132 against every other build, with the window ignored, as `/build` stage 5 asked after hardening loop 1.
- task132 is still architecture v1. Loop 1 was a hardening loop, not a re-root, so the card carries no lineage and nothing is dropped as its own ancestor.
- What changed is the decisive step. In pass 1 it was delayed entry into the band rates' exposure. Now it is renewal: a failed module is replaced by a new one in the forward forecast.

**Extract.**
- The cache was stale. It was written at 02:35, and task132's prompt, card, target, design note and submission were rewritten between 03:27 and 03:44, so I re-extracted.
- 16 builds were fingerprinted from disk (task117 to task132) and 110 cached cards were kept for builds not on this checkout. That gives 126 cards, 124 of them screenable.
- After the extract, every cached card matches its card file.
- The copy of the cache that the parent committed at `ed5f9c0` (03:47) still holds task132's architecture-1 fingerprint (generators G12, G13, G6). The working-tree copy is the current one.

**Inputs held still.** Before reading, I hashed 24 files:
- task132's prompt, submission, design note, metadata, pipeline state and card, its 12 target files and both goldens;
- task133's card, prompt, design note and submission.

All 24 were unchanged when I finished.

**Screen.** `fingerprint.py screen --focus task132` found 123 pairs in scope and promoted 2, both on surface percentile alone:
- **task83:** surface 0.137, 99th percentile, from deliverable species, flat layout and part of the format mix. It also shares the decisive gap label `population`.
- **task130:** surface 0.100, 98th percentile, two builds apart, from flat layout and the same format set.

No pair shares a target file name, a schema, a same-seed table, a byte-identical file, an invented name in the prompt, an ask skeleton or a step skeleton. No mechanism route fired.

**task133 brought into the screen.** task133 is the parallel build in this lane. It lives in its own worktree (`/home/user/wt133`, branch `sathya8571/task133-same-day-access`), with a card, prompt, submission, design note and target there but not on this branch.
- I built a scratch view: copies of the two scripts, every card plus task133's, the ledger and the fresh cache, with the task folders symlinked read-only. I re-ran the extract and the screen there, so nothing in either worktree was written.
- With task133 visible: 125 screenable builds, 124 pairs, 3 promoted.
- The third promotion is task132 against task133, back to back, at surface 0.094 (94th percentile, from layout and formats only). It was promoted because the decisive pattern G9 repeats from the immediately adjacent build.

**Guard.**
- `guard.py heart task132` passes. The nearest heart text is task46's stump at 0.05. With task133 visible, task133's stump becomes the nearest at 0.07, still under the 0.12 WARN line.
- The heart's structural bans reach only builds drawn before task132 (task129 to task131), and they pass.
- Run from task133's side in the scratch view, `guard.py check task133` returns a BLOCK on `ban.pattern` (G9 repeats a recent build, against task132) and a WARN on `repeat.gate_g`.
- Neither branch can raise that BLOCK today, for two reasons:
  - task133's worktree no longer holds a copy of the task132 card (pass 1 found one there).
  - task132's own checks never reach task133. The guard orders draws by date and then task number, and both cards say 2026-10-11.

**Builds compared: 130 counterparts.**
- 123 through the screen, plus task133 through the scratch screen.
- **task1 and task2:** dropped by the screen's filter (no prompt and fewer than three target files in the cache). The heart and my sweep reached their card drivers.
- **task114, task115 and task116:** cards only; they are on neither this checkout nor the carried cache. I compared them from the cards on both tracks (driver, stump, strategy, gap, decision, deliverables, spine, world, invented names, people). No pack-level Track A was possible.
- **task99:** excluded by the script as a scratch slot, correctly, since its card records an August state of task31's world. Its card driver was in the heart and the sweep, with no hit.

**The mechanism sweep.** task132's card files pattern `none`, so its decisive mechanism is read as its first generator, G9. The screen's mechanism route can fire only in four ways, and none applies here:
- gap, pattern and decision type all colliding;
- the same-driver signature;
- a pattern repeat between consecutive builds;
- a lexical driver overlap of 0.40 or more. task132's highest is under 0.10.

So I swept every card driver, concrete driver, stump and lineage driver on file (129 cards including task133) for this vocabulary: renewal, replacement, wear-out, survival, depletion, first occurrence, occupant, spares and age band. I read every hit in full. I also listed every card whose decisive mechanism is G9: task100, task132 and task133.

**Pairs adjudicated: 10.**
- **Promoted by the screen:** task83, task130, and task133 (from the scratch screen).
- **Promoted by me on the mechanism route:**
  - task46, the closest frame in the corpus;
  - task100, the only other card with G9 decisive;
  - task121, whose retired lineage v1 is the closest abstract driver on file;
  - task97, the mirror image of task132's second rung;
  - task33, the approved build sharing a component.
- **Promoted by me on a Track A tell the screen cannot see:** task124, for the "Ironwood" token in its pack.
- **Outline neighbour, from the cards only:** task114.

**Read at card level and dismissed with a reason (see Clean):**
- task19, task45, task52, task53, task57, task62, task69, task84, task90, task104, task106, task117, task119, task123, task125, task127 and task128;
- the lineage entries of task50, task58, task64, task73, task98 and task109 that the sweep surfaced;
- outside the screen, task115, task116, task1, task2 and task99.

**Unread: 92 of the 123 screened pairs.** None was promoted by the screen, none surfaced in the sweep, and none scores above 0.05 in the heart's text comparison. The six nearest unpromoted surface neighbours are task108, task57, task37, task50, task111 and task32 (81st to 94th percentile). They score on flat layout and format mix only, with masked submission overlap of 0.008 at most.

**How adjudication was done.** This thread has no subagent tool, so I read each pair here, one at a time. I asked each the per-pair adjudicator's questions: the decisive move with the domain nouns stripped, the ordered path and where the shared moves sit, the tier, the track, and the one axis to redraw. No server-side tool was called. What I read:
- **task132:** card, design note, prompt, the full submission (it is the build under check), metadata, pipeline state and target listing.
- **task133:** card, design note, prompt, submission blocks 1 to 3 with the step list (the first lines of block 4 came with that read), pipeline state and target listing.
- **task124:** card, pipeline state, and the counterparty table in `generator/desk.py` together with the writer that ships it.
- **Every other counterpart:** the card (driver, concrete driver, stump, lineage, differentiation) and the ledger row.

Name sweeps ran over task132's target and golden files and over the other builds on disk. No figure was read from any golden or answer key except task132's own submission.

**Mechanism coverage, over the 124 screenable builds including task132:**
- 102 have a card mechanism layer (88 native, 14 back-fitted), or 103 with task133.
- 5 are note-only: task16, task17 and task20 (back-fitted), and task112 and task113 (native).
- 17 have no mechanism layer on the screen: task3 to task10, task13 to task15, task18, task19 and task21 to task24, all back-fitted.
- 34 carry back-fitted labels.
- Track B was scored from cards on 101 of task132's 123 pairs; 22 were Track A only on the screen.
  - 20 of those 22 cards still carry a driver and a stump, which the heart and the sweep reached. Five of them (task5, task6, task10, task13 and task14) are marked as sourced from the submission only.
  - task112 and task113 have no card and no ledger row, and their design notes are not on this checkout, so their mechanism is unavailable.

**Not checked: target packs for 15 counterparts are not profiled.** These are task3, task10 and task117 to task129, because `task*/target/` is gitignored until delivery. Byte-identical files, same-seed tables, schemas and file names were not screened against those builds. To compensate:
- task132's generator roots at its own folder and references no other build.
- No card shares task132's spine (`eam_work_orders_protection_2021-01_2026-09.csv`, work-order grain).
- A text sweep of the other builds' files on disk found task132's invented names only in task124 (below).
- The same sweep found two of task132's 142 substation names, Holbrook and Lindale, only in a list of ordinary reference place names in task119's generator.

**Status record.** The ledger has no row for task132, which is correct while it is in flight, and none for any build from task109 on. Where the ledger is silent I say so, and I give `pipeline.json`'s state as the pipeline's state, not as the ledger's status.

## In batch against earlier builds
This is a pre-flight, so every pair is task132 against an earlier build, or against task133 running in parallel. The screen labels its promoted pairs "in batch" because focus mode sets the window to the whole corpus. That is a labelling quirk, not a scope bug.

- **No hit at any tier against an approved or delivered build.** The ledger records ten such builds: task25, task27, task28, task29, task30, task33, task34, task35, task48 and task72. Only task33 has anything in common with task132, and that is one component below its decisive rung (see Clean).
- **Builds delivered to the author on pipeline state only, with the ledger silent:** task119 and task131 (2026-10-10) and task130 (2026-10-11).
  - task130 shares a demoted component (see Clean).
  - task119 and task131 share nothing at the mechanism level.
  - The Part 6.1 bans against task129 to task131 pass.
- **The live exposure is in flight, not behind.** task133 was drawn the same day in the same lane and will likely reach a reviewer in the same batch. It carries the Track B item below.

## Track A findings, reviewer visible

**1. task132 against task124: the invented name "Ironwood".** Soft and Track A only, below every tier in clone-check Part 3. It is closer than the Tamarack echo it replaced: same sector, and inside the window.
- **Status.**
  - task124 has no ledger row. Its pipeline state is stage 3, hardened, not delivered.
  - task132 is in flight.
  - The two are 8 builds apart in draw order, inside the 12-build window.
- **Shared surface.**
  - **task132:** the utility is "Ironwood Hydro Distribution", the rename that cleared pass 1's Tamarack echo with task60. It appears in five target files and in both goldens. The five target files are:
    - `AM-PC-014_obsolete_spares_final_buy.docx`
    - `eam_extract_dictionary.txt` (as "IRONWOOD")
    - `pc_relay_maintenance_compliance_2025.xlsx`
    - `protection_renewal_programme_2026.xlsx`
    - `veldtek_rma_log_vpr340_psu.xlsx`
  - **task124:** its generator lists "Ironwood Commodities LP" (C0262, approved 2022-07-18 to 2024-12-31) in its counterparty table. Its writer ships every row of that table to `desk_counterparties.csv`, so the name is in task124's pack as one expired counterparty.
  - **Why it shows.** Both worlds are electricity businesses, an Ontario distributor and a Texas retail provider. That is what makes the token noticeable to a reviewer holding the batch.
  - **What differs.** The entities: the organisation's own name against one counterparty row. Nothing else in the two worlds overlaps.
- **Why no tool caught it.**
  - The screen's invented-name tell reads prompts, and neither prompt names the utility.
  - The guard's `tell.names` reads the cards' `invented_names`, and task124's card does not list its counterparties.
- **Clears it.** Rename the utility in task132's generator world constant, both goldens and the card's `world.invented_names` together, checking the new name against the generators of the builds in the window. No ladder change. The data survives, because no figure depends on the name.

**Not findings:**
- **task83 and task130**, the screen's two promotions, share flat layout and format mix, and task83 also the xlsx-with-docx deliverable species. Masked prompt overlap is 0.000 and 0.002.
- **task132 against task133** shares layout and formats only (surface 0.094). Masked prompt overlap is 0.000 and masked submission overlap 0.003. They share no file name, persona or invented name.
- **The persona first name "George"** (George Ray) also appears in task115 (George Fenelon). task115 is outside the 12-build window, so this is below the guard's rule. No other persona first name or surname repeats on any card.
- **Pass 1's two Track A items are cleared.** "Tamarack" and "Susan" now appear only in `pipeline.json`'s note recording the rename, and that file does not ship.
- **`voice-check.py task132`** finds no carrier wording and no unlisted six-word run shared by a third of the batch.
  - The prompt is 248 words, against a 12-build median of 253.
  - It names two deliverables, xlsx and docx; each format appears in 6 of the last 12 builds.

## Track B findings, mechanism

**1. task132 against task133: Part 6.1 standing ban, the decisive pattern G9 repeated back to back.** On the reading this is below Template: the pair is `clean_shares_components` on the driver. On the cards it is a `guard.py` BLOCK.

**Status.**
- The ledger is silent on both builds.
- In pipeline state, task132 is at stage 3 (build, hardening loop 1) and task133 at stage 4 (leak check, realism rebuild running).
- They are back to back, drawn the same day in the same lane, so they are the pair a reviewer is most likely to hold together.
- Both sides are in flight, so this is a fix before either ships. No delivered build is involved.

**How it arose.**
- task133's card filed G9 as its decisive generator when it registered, at 02:24.
- task132's loop-1 commit (`200ed9a`) moved its generators from [G12, G13, G6] to [G9, G12, G13], so G9 now carries task132's decisive rung too.
- task133's card still differentiates itself against task132's architecture 1 ("an exposure window in a rate"), which no longer exists.

**Decisive moves, with the domain nouns stripped.**
- **task132:** "The item in each position fails at most once before it is replaced by a new item at the bottom of the age curve, so the old item's rate counts only weighted by its chance of still being in place, and the new item's rate after; summing the old rate over the horizon counts failures one position cannot have."
- **task133:** "A unit already part-way along a cumulative outcome curve filed from entry has, as its forward probability, the curve's remaining increments divided by its survival to date."
- **The same claim? No.** The misread each stump rests on is different, and neither build's wrong path is the other's:
  - task133's stump treats a curve indexed from entry as if every unit were new. It ignores where the unit stands, and lands 25.6 per cent high.
  - task132's naive path places each module correctly at its own age, then ignores that the module leaves the position when it fails. It lands 38.3 per cent high (18 lots against 13).

**Paths, in order.**
- **task132:**
  1. Failures as the filed procedure defines them, each in its module-age band.
  2. Module-months from the January 2021 go-live, and the band rates.
  3. Each relay's end of support, by bay and stage.
  4. **The present module aged forward, weighted by survival, with the 0-9 rate after a replacement. This is the decisive step.**
  5. Usable stock.
  6. Whole lots at 95 per cent Poisson cover.
  7. Price.
  8. The call.
- **task133:**
  1. Stage 3 out.
  2. Staging: arrears, hardship in force, a score fall after conversion.
  3. Months on book and remaining term.
  4. **Conditional PD: the curve's increments over survival to date. This is the decisive step.**
  5. LGD, re-amortised balance and discount.
  6. Scenario weights.
  7. Sum by stage.
  8. The call.

**Where the shared machinery sits.** Both answers compute the same per-unit object. For each unit alive at its current age, it is the conditional probability of a one-time event in each forward month. On task133's card that object is (C(a+k) - C(a+k-1)) / (1 - C(a)). In task132 it is the band rate times the module's chance of still being in place.
- **In task132,** that weighting is the decisive move itself.
- **In task133,** the survival division is the second of the two misreads inside the decisive step: rung 3, the shift without the division, is 7.9 per cent low. The stump rides on the first misread, rung 0, the curve read from entry.

Read by position, the device is decisive in task132 and secondary in task133. That is reuse, not a clone.

It still sits inside step 4, the decisive step, of both paths, which is as close as two drivers come in this corpus without being the same driver. A solver who has learned task133's conditioning will ask for the probability that today's module fails in each month, given that it works now. That question is most of task132's decisive step, because the replacement's own rate adds almost nothing (0.0019 a year in the 0-9 band).

**The label.**
- In stumping 6.2, G9 is "downstream survival versus upstream acquisition". It is a flip in which the channel that acquires fastest retains worst, built by splitting a survival property by an upstream class.
- Neither build has an upstream class. Both cards use G9 as the nearest generator for a survival construction.
- The ban binds on the record either way, and the guard enforces it as written.

**Outline.** None of the four Shape echo axes is shared, so this is below Shape echo:
- **Ask construction:** constraint-first against number-first, with masked prompt overlap 0.000.
- **Deliverable species:** xlsx with docx, against xlsx with pptx.
- **Decision:** a dial set in whole lots, against a currency figure.
- **Calibration:** `none` on both, which is an absence rather than a shared organ.

Both builds are Forecasting with Gate G `forecasting`, and both file their rules with no decoy. That is the spec, not a shape.

**The one axis.** task132's decisive pattern: the G9 survival construction that carries its decisive rung. The guard will charge the BLOCK to task133, because both cards say drawn 2026-10-11 and task132 sorts first. But the collision came from task132's loop 1, after task133 had registered G9.

**Does the data survive?**
- **Yes, if the repair is to the card.** That is the case if the author concludes G9 does not describe the renewal step, and files the generator that does. The new card is then checked again against task129 to task131 and task133.
- **No, if the decisive step is redrawn.** That moves the ladder, the seed (150 was chosen because it separates every rung), the 13-lot answer and every ask figure.

## Clean, shares components by design

**task132's decisive move, domain nouns stripped:** "The item in each position fails at most once before it is replaced by a new item at the bottom of the age curve, so the old item's rate counts only while it is likely to survive and the new item's rate after." Its path is set out under Track B above. Steps 1, 2, 3, 5 and 6 follow filed sections of AM-PC-014. Step 2's January 2021 start comes from the extract dictionary, and is now an ordinary step rather than the stump. Step 4's quantity is defined in AM-PC-014 6.2, but no filed sentence says how to split a month between the present module and its replacement.

**1. task46 (live on the ledger: R1 and R2 valid stumps, repaired, awaiting re-review): clean_shares_components.** It is still the closest frame in the corpus. It sits 84 builds back in draw order.
- **task46's decisive move:** "Age has to be measured on the clock that drives the outcome, cumulative service exposure rebuilt from a movement record in which stored time does not accrue, so the rate law becomes stationary and a cohort crossing a step inside the forward window shows."
- **Shared frame:** an age-banded failure-rate law, rolled over an ageing fleet to size a forward purchase. In task132 that frame is filed (AM-PC-014 6.1 and 6.2). In task46 it surrounds the decisive clock.
- **Shared component, demoted:** the age that drives the rate is not the obvious age field.
  - In task46 that is the decisive move.
  - In task132 it is rung 1: relay age from installation instead of module age from fitting, 20.1 per cent low. The 2015 service-bulletin swaps are what open it.
- **Driver difference.**
  - task46's rates run above one event per unit-year (1.33 to 1.40 past ten service years). Its events recur on the same unit, so summing the rate over the window is right there; what is wrong is the clock.
  - task132's events retire the item. The clock is right and summing is wrong.
  - A solver primed by either build is not primed for the other's decisive step.
- **Outline.** The decision (a forward buy) is shared. The deliverables (py+pdf against xlsx+docx), the calibration organ (physical verification against none) and the ask construction (masked prompt overlap 0) differ. Below Shape echo.

**2. task130 (ledger silent; pipeline state: delivered to the author 2026-10-11): clean, shares a component.** The screen promoted it on surface.
- **Shared component:** a filed programme that reaches each unit on a schedule ends that unit's forward window.
  - In task130 that is decisive: each household's rank in its size's list, against the cumulative lets.
  - In task132 it is a filed lookup at step 3 of 8. Staged schemes by bay and the superseded 2025 sheet sit there as Layer 1 mess on the supported-relay ask.
  - The device was demoted, so this is reuse.
- **Driver difference.** task130's driver names a survival curve read off history as a wrong path, while task132's answer weights each module's rate by survival. The claims differ (queue rank against cumulative supply, against renewal of a replaced item). So do the shape (02 against 04), the decision and the deliverables (xlsx+png against xlsx+docx). The Part 6.1 bans pass.

**3. task83 (live on the ledger, RE-ROOT 2.1): clean.** The screen promoted it on surface plus the shared gap label.
- **task83's decisive move:** condition a randomised holdout's effect on each unit's own prior treatment history, because the target pool's mix on that axis differs from the measurement corpus.
- **task132 no longer files G6.** The forward age mix sits inside AM-PC-014's own method (band rates applied to the module-months expected in each band), below the decisive rung.
- **The shared `population` label** names different populations: a treatment-history stratum, against which module occupies a position.

**4. task33 (approved on the ledger): clean, shares a component.**
- **Shared component:** a forward window that stops at a filed per-unit date, task33's filed interventions and task132's programme month. It sits below the decisive rung in both builds; task33's own stump has the solver already truncating.
- **Driver difference:** task33's driver is a measured elevation that scales with the expected forward path. Nothing on its path weights by survival or replaces a unit.

**5. task100 (live on the ledger, v2): clean.** It is the only other card with G9 decisive, and it also carries `population_selection` and a capacity-planner role.
- **Driver difference.** task100's decisive move enumerates which members leave early: those completing a two-stage course a period early, visible only on the prior snapshot. task132's is renewal of a replaced item.
- **Distance.** It is 24 builds back in draw order, so no Part 6.1 ban reaches it.
- **Other axes.** Gap (time against population), Gate G (etl_conformance against forecasting) and decision (a designation set against a dial) all differ.

**6. task97 (live on the ledger, v5): clean.** Its decisive move says a unit's risk is set by the cumulative history of the place it occupies, counted across every occupant. task132's rung 1 is the mirror image: the rate follows the occupant's own age, not the position's. That is not task132's decisive rung, and the claims differ.

**7. task121 (ledger silent; pipeline state retired): history, not a finding.**
- Its lineage v1, drafted 2026-10-08 and never registered, is the closest abstract driver on file: "a struck unit repairs the property that exposed it ... so the forward cost is the expected first occurrences among units still holding the state as that pool drains".
- That is the same family as task132's renewal step: the event takes the unit out of the exposed state, so a rate carried flat overcounts.
- It never reached a card of its own or a build, and the shipped task121 turns on identity resolution. It is the record of the family having been considered.

**8. task114 (no ledger row, card only): clean, outline only.**
- **Shared outline**, as in pass 1: Canada, shape 04, dial_setting, capacity_planner and population_selection.
- **Differences.** Its driver (demand that exists only when parties are at the same site) is unrelated. The deliverables (xlsx+svg), the calibration organ and the forum differ.

Below Shape echo on everything that can be checked.

**Dismissed by the sweep, with no shared decisive claim:**
- **Positions and occupants.**
  - task45 lineage: "positions still carrying an affected unit", solved and retired. In task132 the modules already replaced are rung 1.
  - task90: a buyer-side position persisting across substitutions, priced as one hire.
  - task109 lineage: turnovers between occupants.
- **Survival and depletion vocabulary.**
  - task52: a survival curve as one wrong path to a milestone clock.
  - task125: forward band migration after a filed run-off.
  - task69: overlapping events that convert once, a set-coverage cap.
  - task128: drains per window.
  - task104: a scorer whose baseline absorbs mild deviations.
- **Renewal and lapse in the contract sense:** task62, task117, task123 and task127 (lapses and renewals of terms, not of items).
- **Failure-rate and replacement lineage:**
  - task50 v3: a slow-surfacing failure mode projected with a run-out law; it failed.
  - task73 world six and world nine: a filed batch-replacement rule, and a capped replacement slate.
  - task58 v6, v11 and v13 to v14, task64 v1 and task98 v5: "survivor" means the survivor of a back-test, not unit survival.
- **Read in full, unrelated:** task1, task2, task19, task53, task57, task84, task106, task115, task116 and task119.

## Strategy monoculture
The batch is the last 12 builds in draw order ending at task132: task119, task121, task122, task124, task125, task126, task127, task128, task129, task130, task131 and task132. The counts come from the cards' fields, and every card in the window carries them.

| Measure | Count | Cap | Verdict |
|---|---|---|---|
| Withheld rule with an official decoy | 0 of 12 (task119 and task122 carry `official_decoy`, both with the decisive rule filed) | 2 | under |
| Certified-record decoy (`validated_decoy`) | **7 of 12**: task121, task122, task124, task125, task126, task127 and task129 | 3 | **over, Strategy monoculture finding (batch, not task132)** |
| Any one `stump_strategy` | max 2 of 12 (decomposition_attribution, identity_resolution, causal_design, binding_constraint) | 4 (a third) | under |

- **The validated-decoy share is unchanged from pass 1.**
  - Pipeline state now records four of the seven as retired: task121, task122, task125 and task127. The ledger is silent on all seven.
  - Among the builds that can still ship, the carriers are task124, task126 and task129. That is at the cap, not over it.
  - Over the last 15 builds it is 10 of 15 on the cards.
- **The 12 ending at task133**, the batch this pair will likely ship in, gives the same picture: 7 of 12 validated decoys, one official decoy (task122), and no strategy above 2.
- **task132 adds to no capped count.** It is `population_selection`, with the decisive rule filed, no official decoy, no validated decoy and calibration form none.
- **task133 adds to none either.** It is `stated_rule_hard_construction`, with its rule filed and no decoys.
- **One repeated decisive mechanism.** In the 12 ending at task133, G9 is decisive twice (task132 and task133). It is the only decisive mechanism repeated back to back in that window, and it is the Track B item above.

## Corpus habits
- **File names.**
  - `data_dictionary` appears in 61 builds, `export_manifest` in 33, `data_notes` and `provenance` in 12 each, and `county_reference` in 4. Eight more names appear in 3 builds each.
  - task132 uses none of the habit names. Its dictionary is `eam_extract_dictionary.txt`.
- **Deliverable pairings.**
  - Corpus-wide: pdf+csv 9, py alone 8, py+pdf 7, pdf+png 6, py+csv 5, py+xlsx 5, pdf+xlsx 5, docx alone 4.
  - In the last 12 builds, xlsx and docx each appear in 6.
- **Opening moves.** voice-check files 6 of the last 12 under `other`, task132 included, though its card says constraint-first. That is the classifier's coverage, not the prose. There is no carrier wording and no shared run.
- **Write-up idiom.** Two constructions recur in the submissions on disk (task117 to task133):
  - The Final Recommendation's refusal sentences ("Not the ..., which ...") appear in 12 of the 16.
  - 13 of the 16 step lists run to exactly eight steps; the spec allows at most eight.

  Neither is evidence about a pair, but across a batch both read as one hand.
- **The age-curve family.**
  - Three builds put the decisive step on how an age-indexed event curve is applied to an aged population: task46 (the clock age runs on), task132 (renewal of a replaced item) and task133 (conditioning on survival to date).
  - The drivers differ in each pair, but two of the three are back to back in this lane.
  - The guard's lexical driver comparison scores these pairs at 0.07 or less, against a WARN line of 0.12, so it will not see the next one. The next draw in this family needs reading by hand.
- **People.**
  - The persona rule cannot see personas in packs that are not on this checkout (task117 to task129), so I checked the cards' `world.people` instead.
  - Two electricity-business worlds sit in the last 12 (task124 and task132). That is what turned a background counterparty name into a visible echo.

## What to redraw
1. task132: the decisive pattern (G9, the survival construction carrying its decisive rung), which repeats task133's back to back.
2. task132, Track A rename: the utility's invented name "Ironwood", which echoes task124's "Ironwood Commodities LP".
3. Batch, not task132: the certified-record decoy axis (`validated_decoy`). It stands at 7 of 12 on the cards (task121, task122, task124, task125, task126, task127 and task129), and 3 among the builds that can still ship.

**Bookkeeping notes (none of these is a finding):**
- Two card fields still describe task132's architecture 1: task133's `differentiation.task132` and task132's own `differentiation.task46`.
- The cache committed at `ed5f9c0` holds task132's architecture-1 fingerprint. The working-tree copy refreshed by this check is current.
- Two builds drawn the same day on separate branches never meet in either guard, because of the guard's draw-order rule and the per-branch card directories. This pair was caught only because the scratch view put both cards in one directory.
- task132's design note says the card was "re-checked after loop 1 (guard PASS, nearest driver task87 at 0.06)". That PASS could not see task133.
- `pipeline.json` records pass 1's CLEAN, which predates loop 1.
