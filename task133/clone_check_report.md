# Clone check: pre-flight on task133 against every other build, 2026-10-11

## Verdict

CLEAN. No tier on either track against any build. The nearest pair, task132 (back to back, both in flight), is `clean_shares_components` on the reading.

## Scope and coverage

- **Mode and scope.** Pre-flight on task133, with the window ignored. task133 is Bellbird Personal Finance's collective ECL allowance at 30 September 2026: architecture v1, pipeline stage 4, data cut, no solver round yet.
  - task133 was read from its worktree (`/home/user/wt133`, branch `sathya8571/task133-same-day-access`).
  - Every other build was read from the main checkout (branch `sathya8571/task132-relay-final-buy`) and the carried cache.
- **How the corpus was assembled.** `fingerprint.py` pins its cards and ledger to its own checkout, and task133 exists only in the other worktree. So the extract and the screen ran on a scratch mirror, which held:
  - main's 16 builds on disk (task117 to task132) and task133, symlinked read-only;
  - main's 128 cards plus task133's card, and main's ledger;
  - a copy of main's cache, so that cached cards for builds not on this disk carried through.

  Nothing in either checkout was written except this report.
- **Cache staleness was checked before the cache was trusted.**
  - For every build not on disk, the cached card fields match the current card file, and the cached ledger rows match the current ledger.
  - Only task132's card had moved (its generators), and task132 re-extracted from disk.
- **Counts.**
  - **Builds compared:** 125 through the screen (task133 and 124 counterparts, task3 to task132).
  - **Pairs:** 124 screened, 0 promoted.
  - **Pairs adjudicated:** none were promoted, so none was owed. I read two pairs at my own discretion, and both are labelled "not promoted" below:
    - task132, because it is back to back and its card cleared a G9 ban against task133 by refiling its pattern;
    - task100, the only pair where both the decisive gap and the decisive pattern match on the cards.
  - **Pairs not adjudicated:** 122. None carries a shared-driver signal:
    - Card driver overlap tops out at 0.096 (task100), against the screen's 0.40 line.
    - I swept every driver, concrete driver, stump and lineage driver on file (129 cards) for survival, curve, conditioning, seasoning, vintage, lifetime and credit-loss vocabulary. No other build states task133's claim, and no earlier build is a credit-loss or PD-curve build under any domain label.
    - 13 pairs share the decisive gap (time) and the decision type (quantity_figure) at a distance: task35, task37, task44, task46, task47, task62, task87, task89, task95, task97, task102, task107 and task117. I read their card drivers, and none states the same claim.
- **Outside the screen.** Six card-only builds and two ledger-only numbers sit outside the screen. With them, every number from task1 to task132 has a record and was checked.
  - **task114, task115, task116** (cards only): scored with the script's own card comparison. task114 and task115 share only the decisive gap (time), and task116 shares nothing.
  - **task1 and task2:** their cards carry no gap or pattern, so there is nothing to score.
  - **task99:** it carries a card (supply-chain forecasting, architecture R5), but `fingerprint.py` excludes the number as scratch, so the screen never compares a build with it. The guard does compare it. Scored from the card here: no collision (decisive generator G16, no gap or pattern, driver overlap 0.017).
  - **task61** (retired) **and task96** (drawing): ledger rows only. Their decisive mechanisms are objective with G11, and population with E. No collision.
- **Mechanism coverage, over the 125 screened builds.**

  | Mechanism layer | Builds | Which |
  |---|---|---|
  | Card | 103 | 89 native labels, 14 back-fitted (up to task36) |
  | Design note only, no mechanism record | 5 | task16, task17, task20, task112, task113 |
  | None | 17 | the early builds, task3 to task24 |

  That leaves 22 pairs checked on Track A only. The back-fitted labels touch task35 and task33 below.
- **No subagents.** This run had no agent tool. Nothing was promoted, so no adjudicator was owed.
  - The two discretionary readings were done in my own thread, from:
    - both cards and both prompts;
    - submission blocks 1 to 3, which hold the solution steps, not the deliverable answers;
    - the target listings;
    - the design notes for task132 and task133.
  - task100's design note is not on this checkout, so its card and ledger row stood in.
  - No server-side tool was called.
- **A moving part during the run.** A parallel session was editing task132's generator in the main checkout (04:30 to 04:38 UTC).
  - task132 is read as of its card and design note, both unchanged since 04:09 UTC.
  - Its target is read as extracted at 04:32 UTC.
- **Mechanical cross-checks, run on the same scratch mirror.**
  - `guard.py check`: WARN only, `repeat.gate_g` (forecasting, against task132). The nearest driver is task130 at 0.08.
  - `guard.py heart task133`: WARN. The nearest heart text is task52's stump at 0.07, under the 0.12 line.
  - `voice-check.py task133`: no carrier wording, and no six-word run shared by a third of the batch.
- **One record in task133's own files is out of step.** `pipeline.json` still gives the stump as "about 25 per cent too much". The card and the design note give 43.4 per cent after the realism rebuild. I used the design note.

## In batch against earlier builds

In pre-flight, every pair is task133 against an earlier build, with task132 running in parallel. The screen labels its pairs "in batch" because focus mode sets the window to the whole corpus. That is a labelling quirk, not a scope error.

**Nothing at any tier, and nothing against a delivered build.** The ledger records ten builds as delivered or approved: task25, task27, task28, task29, task30, task33, task34, task35, task48 and task72. Against those ten:

- **Hard tells:** none. No byte-identical file, no identical column set, no same-seed table, no shared file name and no shared invented name.
- **Nearest on surface: task72**, at 0.093 (92nd percentile).
  - All of that comes from the flat layout and five shared formats out of six.
  - Masked prompt overlap and masked submission overlap are both 0.
  - Its driver, booking a movement to the owner whose agreement covered each piece of service, is unrelated.
- **Nearest on mechanism: task35**, which shares the decisive gap (time) and the decision type (quantity_figure) on back-fitted labels. Its driver is a forward obligation whose attachment period is recovered from settled records, which is a different claim.
- **task30 and task34** share the context-artifact species (`filed_model`) and nothing else.

**Status of the other counterparts:**
- 61 are live on the ledger, and 7 are retired or failed.
- 45 have no ledger row, so their status is unknown. These are every build from task109 on, the builds before task25, task95 and task104.
- 1 carries a row the status parser cannot rank.

## Track A findings, reviewer visible

None.

- **No shared surface.** task133 shares no target file name, schema, numeric signature, invented name (Bellbird Personal Finance, PL36, PL60) or rare sentence construction with any build. Its Main Ask sentence matches no other once it is masked.
- **Nearest on surface: task132**, at 0.094 (94th percentile). That comes from layout and formats only:
  - masked prompt overlap is 0.000, and masked submission overlap is 0.002;
  - the deliverables are xlsx+pptx against xlsx+docx.
- **Shape echo**, checked on its four axes against the closest outlines. None reaches the tier:
  - task130 shares the decision outline (shape 02, and a quantity figure). That is one axis of four.
  - task124 and task129 share the deliverable species (xlsx+pptx). That is one axis; they also share the committee forum, which is not one of the four.
  - task123 shares the number-first ask construction. That is one axis.
- **The guard's shape ban** covers the last two builds, and it is clear: task131 is shape 07 and task132 is shape 04.

## Track B findings, mechanism

None. Part 6.1's standing bans against the last three builds (task130, task131, task132) all clear on the cards:

| Axis | task133 | Against task130, task131, task132 |
|---|---|---|
| Pairing | banking-credit-financial-risk with forecasting | new |
| Decisive gap | time | rule, population, population |
| Decisive pattern | G9 | G16, G10, G6 |
| Context artifact | `filed_model` | operations log, register, filed standard |
| Role, forum, forcing event, organisation family | finance controller, committee or panel, period close, financial institution | all new |
| Strategy | stated rule, hard construction | new |
| Calibration | none | an absence on all four, not a shared organ |

- **Gate G forecasting repeats task132.** That is a WARN in the guard, and the card answers it: the lane is Forecasting.
- **The G9 clearance rests on a label, so the reading is what clears the pair.**
  - task132's pass 2 found G9 decisive on both cards back to back. task132 then refiled its decisive pattern as G6 (composition shift).
  - In the stumping vocabulary, G9 is a flip built by splitting a survival property by an upstream class. Neither build has an upstream class, and task133 also files G9 as the nearest label for a survival construction.
  - The ban is clear on the record, but a reviewer reads drivers, not codes. The pair is cleared on the reading below.
  - If task133's generator is ever refiled for accuracy, run `guard.py check` again.

## Clean, shares components by design

### task132: clean_shares_components (not promoted, read at my discretion)

**Status:** back to back and in flight. The ledger is silent, and task132's pipeline is at stage 3, loop 1.

**Decisive moves, with the domain nouns stripped.**
- **task133:** "A cumulative event curve filed from each unit's entry has to be entered at the unit's current age and conditioned on its survival to date; read from entry, it treats every unit as new."
- **task132:** "The unit now in a position can fail once and is then replaced by a new unit at the bottom of the age curve, so its rate counts only while it is likely to survive; carried through the horizon, it counts failures one position cannot have."
- **The same claim? No.** Each build's naive path already does what the other build's stump fails to do:
  - task132's naive solver ages every module from its own fitted date, which is task133's decisive placement done right.
  - task133's naive solver reads curve increments that already allow at most one default per loan, so task132's error, counting a failure the unit cannot have, never arises there.

**Paths, in order.** Both write-ups put the decisive step at step 4 of 8.
- **task133:**
  1. Stage 3 out.
  2. Staging: arrears, hardship in force, and a score fall after the v3 conversion.
  3. Months on book and remaining term.
  4. **PD(k) as the curve's increment after months on book, divided by survival to date, with the stage 2 scalar. This is the decisive step.**
  5. LGD, re-amortised balance and discount.
  6. Scenario multiplier.
  7. Sum by stage.
  8. The call.
- **task132:**
  1. Failures as the procedure defines them, in the removed module's age band.
  2. Module-months from the go-live, and the band rates.
  3. Each relay's end of support, by bay and stage.
  4. **The present module aged forward, weighted by survival, with a 0-9 module after a failure. This is the decisive step.**
  5. Usable stock.
  6. Whole lots at 95 per cent Poisson cover.
  7. Price.
  8. The call.

**Where the two shared devices sit on each ladder.**
- **Where a unit's clock starts.**
  - In task133 it carries the stump: rung 0, the curve read from entry, +43.4 per cent.
  - In task132 it sits low: rung 1 (relay age used for module age) at -20.1 per cent, and rung 2 (module-months from fitting rather than from the go-live) at -15.0 per cent.
- **Weighting by survival, for a one-time event on a unit alive at its current age.**
  - In task132 it carries the stump: rung 3, +38.3 per cent.
  - In task133 it is the nearest wrong rung: rung 3, the shift without the survival division, at -3.3 per cent.
- **So each build's decisive device is the other build's demoted one.** That is reuse in both directions, not a clone.

**How close it is.**
- Both answers compute the same per-unit object: the chance of a one-time event in each forward month, for a unit alive at its current age. A solver drilled on one build is helped on the other.
- task133's own slot note rejected seed FC04 for repeating task132's "age-forward structure". The drawn build still projects an age-indexed curve forward from each unit's age.
- The pair clears on position, not on frame.

**The one axis to hold.** task133's decisive weight has to stay on the curve's origin (rung 0).
- A hardening that moves the stump onto the survival division (rung 3) would put task133's decisive rung on task132's decisive device. The pair would then read as Template.
- The design note's "Tried and rejected" section already records pressure on that rung: 3.3 per cent against a 6 per cent floor.

**Outline.** None of the four Shape echo axes is shared:
- ask construction: number-first against constraint-first;
- deliverable species: xlsx+pptx against xlsx+docx;
- decision: a currency figure against whole lots;
- calibration: no organ on either side.

Some things are shared without counting toward the tier:
- Forecasting with Gate G forecasting, and filed rules with no decoy. That is the lane and the spec, not a shape.
- The Layer 2 family `field_method`. The Layer 2 patterns themselves differ.

### task100: clean (not promoted, read at my discretion)

**What is shared:** a label and an artifact species, not a device.

**Status:** v2 is live on the ledger. It was submitted to the portal, and no result is recorded.

**Why it was not promoted:** it is distant, and its Gate G and decision both differ. I read it from its card and ledger row.

- **The match.** It is the only pair in the corpus where both the decisive gap (time) and the decisive pattern (G9) match on the cards, and the context artifact (`filed_model`) matches too.
- **task100's decisive move:** "The forward roster loses a class of members who finish one period early, a class that is not the top tier of the tenure count and can be enumerated only by finding the same member in the final stage on the prior period's snapshot."
- **The same claim? No.**
  - task100 enumerates who leaves, by linking records across two snapshots.
  - task133 computes how likely each survivor is to default, from a filed curve.
  - There is no snapshot linkage in task133, and no curve conditioning in task100.
- **Everything else differs:**

  | Axis | task100 | task133 |
  |---|---|---|
  | Objective | ETL | Forecasting |
  | Gate G | etl_conformance | forecasting |
  | Decision | designation set | currency figure |
  | Calibration | certified matrix | none |
  | Strategy | population selection, with a validated decoy | stated rule, filed |

- **Position.** task100's decisive rung is the early-exit enumeration, and its forward roll sits at rung 4 of six. Nothing in task133 occupies either place.

## Strategy monoculture

Counted over the 12 builds ending at task133 (task122 to task133), which is the batch task133 is most likely to ship in. The counts come from the cards' `stump_strategy`, `decisive_rule_filed`, `official_decoy` and `validated_decoy` fields.

- **Stump strategy.**
  - Two builds each: causal_design (task124, task131) and binding_constraint (task127, task128).
  - One build each: decomposition_attribution (task122), time_semantics (task123), withheld_rule_corpus_fit (task125), identity_resolution (task126), composition_mix (task129), other (task130), population_selection (task132) and stated_rule_hard_construction (task133).
  - No strategy is near a third of the batch, which would be four of twelve.
- **Withheld rule with an official decoy: 0 of 12.**
  - The two official decoys (task122, task123) sit with filed rules.
  - The three withheld rules (task124, task125, task127) carry no official decoy.
- **Certified-record (validated) decoy: 7 of 12, above the cap of three.**
  - The builds are task122, task123, task124, task125, task126, task127 and task129.
  - Over the 15 builds ending at task133 it is 9 of 15, adding task120 and task121.
  - The ledger is silent on all nine, so their status is unknown.
- **task133 adds to none of these counts.** Its rule is stated and filed, with no official decoy and no validated decoy. The four builds on the two-layer standard, task130 to task133, carry no decoy of either kind.
- **The validated-decoy breach belongs to the batch.** It is carried by task122 to task129, and it is not task133's to repair. But any batch that ships task133 beside those builds carries it.

## Corpus habits

- **Dictionary file name.**
  - `data_dictionary` is in 61 builds, and 74 of the 125 screened builds carry some `*dictionary*` file.
  - The move away from that name has converged on a new house name, `*_extract(s)_dictionary.txt`:
    - task130: `housing_needs_extracts_dictionary.txt`
    - task132: `eam_extract_dictionary.txt`
    - task133: `ecl_extract_dictionary.txt`
    - task103 has the `.md` form.
  - task132's and task133's names are three letters apart, in back-to-back builds.
  - The file role is idiom and not evidence about any pair. A batch reviewer sees the name.
- **Other file roles.** `export_manifest` is in 33 builds, `data_notes` in 12 and `provenance` in 12. task133 carries none of these names.
- **Date stamps.**
  - `2026-09-30` stamps files in seven builds: task104, task105, task106, task108, task130, task132 and task133.
  - A `YYYY-MM_YYYY-MM` range ending 2026-09 appears in five: task106, task111, task130, task132 and task133.
  - That is the natural as-of date for builds drawn in October 2026, but across a batch it reads as one naming scheme.
- **Opening moves.**
  - voice-check files 7 of the 12 under `other`, task133 included. Its card says number-first, but the classifier only recognises an opening that starts "The number...". That is the classifier's coverage, not the prose.
  - The number-first opening that names the forum and its date appears twice in the window:
    - task123: "The number the trustees vote on 11 November is a rate"
    - task133: "One number goes to the Audit and Risk Committee on 23 October"
  - task133 is the shortest prompt in the window, at 193 words.
- **Deliverables.**
  - xlsx+pptx is the most common format set in the 12: task124, task129 and task133.
  - Unused in the window: tsv, json, parquet, html, jpg, pdf, py, sql and r.
  - A committee or panel decides in 3 of the 12 builds (task124, task129, task133), which is under the guard's overuse line.
- **The time-origin family.**
  - Three builds now put the decisive step on how an age-indexed event curve is applied to a population already part-way along it:
    - task46: the clock age runs on (live on the ledger);
    - task132: renewal of a replaced unit;
    - task133: conditioning on survival to date.
  - The drivers differ pairwise.
  - The guard scores these pairs at 0.05 to 0.08 on words, under its 0.12 WARN line. A fourth draw in this family would pass the guard, so it needs reading by hand before its ladder.
- **Personas.** Two of task133's card personas share a first name with a card inside the 12:
  - Stephanie, with task127's Stephanie O'Connor;
  - Adam, with task125's Adam White.

  Neither task127's nor task125's shipped text names them, and task133 ships only Stephanie Manning. The guard's people check, which reads shipped text, is clean. This is not a finding.

## What to redraw

Nothing. No tier on either track, and the draw, the ladder and the data stand.

One axis to hold through any hardening: task133's stump stays on the curve's origin (rung 0) and never moves onto the survival division, which is task132's decisive device.
