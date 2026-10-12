# Clone check: pre-flight on task134 against every other build, 2026-10-11

## Verdict

CLEAN. No tier on either track against any build. The five promoted pairs all clear when read:
- task70 and task104 share card labels but no device.
- task100, task130 and task87 share only a flat layout, file formats and the xlsx-plus-png deliverable pair.

The nearest mechanism is task132, two numbers back and shipped during this run, and it reads as `clean_shares_components`.

## Scope and coverage

- **Mode and scope.** This is a pre-flight on task134 with the window ignored, so the range is task134 against every other build: task1 to task133, plus task228 and task229.
  - task134 is Ocotillo County's fiscal 2027 reentry navigator application, architecture v1.
  - Its data is cut and there has been no solver round yet. `pipeline.json` reads stage 4: leak.py returned REVIEW with no LEAK, and the leak reader is not recorded.
  - Because the data is already cut, a Track B finding here would have cost the build, not just a redraw.
- **How the corpus was assembled.** `fingerprint.py` reads its cards, ledger and cache from its own checkout, and task132's build and card were on another branch. So the extract and the screen ran on a scratch mirror holding:
  - the 18 builds on disk in `/home/user/wt134` (task117 to task131, task133, task134 and task229), symlinked read-only;
  - task132's folder and card, from `/home/user/real-world-data-extraction-conformation-etl-build-problems` as the brief directs;
  - this branch's 131 cards, the shipped ledger (identical on both checkouts) and a copy of this branch's cache, so that cached cards for builds not on this disk carried through.

  Nothing in either checkout was written except this report. The tracked cache at `.claude/skills/clone-check/.cache/fingerprints.json` has not been touched.
- **I checked the cache for staleness before trusting it.** For all 110 builds that are not on disk, the cached card fields match the current card files and the cached ledger rows match the current ledger. Every build on disk was re-extracted.
- **task132 shipped while this check was running.** At 10:06 UTC the other checkout switched to `main` with task132 shipped (PR #23).
  - Its card changed only in `answer`, `answer_source`, the spine row count and one phrase of `driver_concrete`. Every mechanism field is unchanged.
  - I re-extracted and re-screened against the shipped card and folder, and the screen came back identical.
- **Counts.**
  - **Builds compared:** 127 through the screen. That is task134 and 126 counterparts: every number from task3 to task133 except task61, task96, task99 and task114 to task116, plus task229.
  - **Pairs:** 126 screened, 5 promoted.
  - **Pairs adjudicated:** all 5. **Pairs left unread:** none.
  - **Read at my discretion, and labelled "not promoted" below:**
    - task132 and task133, the two builds before task134 in the lane;
    - task99, task31, task75 and task126, the only cards that carry a right-censoring device, which task134 also carries;
    - task124 and task83, which share both the decisive gap and the decision type, at a distance;
    - task80, the third card with G16 decisive;
    - task131, which is also shape 07;
    - task228 and task229, drawn the same day in another lane.
- **Outside the screen.** With these, every number from task1 to task134, plus task228 and task229, has a record and was checked.
  - **task114, task115, task116 and task228** have cards only. I scored them with the script's own card comparison (`track_b_cards`). task116 and task228 share only the decisive gap (population), and task114 and task115 share nothing.
  - **task1 and task2:** their cards carry no gap or pattern, so there is nothing to score.
  - **task99:** it carries a card (supply-chain forecasting, R5). `fingerprint.py` excludes the number as scratch, but the guard compares it. I read it by hand below, because its decisive device is one task134 carries.
  - **task61** (retired) **and task96** (drawing) have ledger rows only. Their decisive mechanisms are objective with G11, and population with E. Neither collides.
- **Mechanism coverage, over the 127 screened builds.**

  | Mechanism layer | Builds | Which |
  |---|---|---|
  | Card | 105 | 91 native labels, 14 back-fitted (task11, task12, task25 to task36) |
  | Design note only, no mechanism record | 5 | task16, task17, task20, task112, task113 |
  | None | 17 | task3 to task10, task13 to task15, task18, task19, task21 to task24 |

  That leaves 22 pairs checked on Track A only. Every Track B reading below has a card on both sides, and none of the five promoted counterparts carries back-fitted labels.
- **A coverage gap in the extract, closed for this run.** Since the task131 pre-flight (cache commit `846b463`), the cache has held empty target profiles for task117 to task129.
  - **Cause.** Those builds' `target/` folders are gitignored. `extract` re-fingerprints every build whose `prompt.md` is on disk, so a build on disk with no target folder replaces its cached profile with an empty one.
  - **Effect.** Every screen since then, including this run's first pass, saw those 13 builds through their prompt and write-up only.
  - **What I did for this run:**
    - task117, task119 and task229 were profiled from their committed `target.zip`, each unpacked into its own scratch folder.
    - task118 and task120 to task129 have no target on any checkout. Their profiles came from cache commit `774762d` (2026-10-10 05:10 UTC), the last cache that carried them, and they may be stale for any build rebuilt after that.
  - **Result.** With the profiles restored, no pair gains a shared file name, schema, same-seed table or invented name, and the promotions are unchanged. The nearest restored build is task120, at 0.092.
  - **Owner.** Fixing the script is the author's call.
- **No subagents.** The brief calls for one adjudicator per pair, but this run had no agent tool. I adjudicated the five promoted pairs in my own thread, to the same brief: each decisive move with the domain nouns stripped, the ordered path, the position of every shared move, the verdict, the tier, the track and the axis.
  - **Read for each pair:**
    - both cards;
    - both prompts (for builds off this disk, the cached prompt record: ask sentence, sentence openings and deliverables);
    - submission blocks 1 to 3;
    - the design note where one is on disk (task130, task132, task133, task134);
    - the target listings.
  - **Not read:** any golden deliverable or deliverable-answer block.
  - The design notes for task70, task104, task100 and task87 are not on this checkout. Their cards and ledger rows stood in; task104's card was reconciled from its design note.
  - No server-side tool was called.
- **Mechanical cross-checks, run on the same mirror.**
  - `guard.py check`: PASS, with one NOTE, `test.same_driver_older`, against task104 and task70 v2. The card differentiates both.
  - `guard.py heart task134`: PASS. The nearest heart text is task133's driver and task31's R8 driver, at 0.05, under the 0.12 WARN line.
  - `voice-check.py task134`: no carrier wording found by the script, and no six-word run shared by a third of the batch. It misses two things, both under Corpus habits.
  - `guard.py people task134`: no BLOCK or WARN.

## In batch against earlier builds

In pre-flight, every pair is task134 against another build. The screen labels its pairs "in batch" because focus mode sets the window to the whole corpus. That is a labelling quirk, not a scope error.

**Nothing at any tier, and nothing against a delivered build.** The ledger records ten builds as delivered or approved: task25, task27, task28, task29, task30, task33, task34, task35, task48 and task72. Against those ten:

- **Hard tells:** none. No byte-identical file, no identical column set, no same-seed table, no shared file name and no shared invented name.
- **Nearest on surface: task72**, at 0.093 (92nd percentile).
  - That score comes from the flat layout and four shared formats out of five.
  - Masked prompt overlap is 0.003, and masked write-up overlap is 0.001.
- **Nearest on mechanism:** task34, task48 and task72 share the decisive gap label (population), which 44 cards on file carry. Their drivers:
  - task34: a subpopulation no column names, found by a within-cluster fit;
  - task48: a population invisible at the monitor's grain, recovered at a pair grain;
  - task72: a movement booked to the owner whose agreement covered it.

  None of them states task134's claim. None shares its decisive pattern, decision type, calibration form or context artifact.

**Status of the other counterparts:**
- 61 are live on the ledger, and 7 are retired or failed (task31, task32, task36, task45, task51, task55, task73).
- 47 have no ledger row, so their status is unknown: task3 to task24, task95, task104, task109 to task113, task117 to task133, and task229. `START_HERE.md` records task132 and task133 as shipped to the author, but the ledger is silent on both.
- 1 carries a row the status parser cannot rank (task59).

## Track A findings, reviewer visible

None.

- **No shared surface.** task134 shares nothing reviewer-visible with any build:
  - no target file name, schema or numeric signature;
  - no invented name (Ocotillo County, Office of Justice Grants, County Data Hub, the six SD districts);
  - no rare sentence construction.

  The highest masked prompt overlap is 0.005 (task132), the highest masked write-up overlap is 0.003 (task109), and the ask-skeleton overlap is 0 against every build.
- **The three surface promotions, cleared.** task100 (0.152, top 1 per cent), task130 (0.152) and task87 (0.147) were promoted on percentile alone.
  - Each score comes from three things: the flat layout, a format overlap, and the same deliverable pair, xlsx plus png.
  - The corpus runs at a median of 0.073 and a 99th percentile of 0.105, so a shared deliverable pair on a flat pack is enough to reach the top.
  - Here they are, read against the four Shape echo axes (ask construction, deliverable species, decision shape, calibration organ):

  | Pair | Shared | Not shared | Their driver, nouns stripped |
  |---|---|---|---|
  | task100 v2 (live on the ledger, no portal result recorded) | deliverable species | ask (constraint-first against calendar-first); decision (designation set against allocation); calibration (certified matrix against none) | A forward roster loses members who finish a period early, and they can be enumerated only by finding them in the final stage on the prior snapshot |
  | task87 v9 (live on the ledger, no portal result recorded) | deliverable species | ask; decision (one count against an allocation); calibration (outcome roster against none) | A filed procedure's count is capped, because two owed items meeting in one slot cannot both be taken by one unit |
  | task130 (no ledger row) | v2 on disk: deliverable species, and a whole-number count per category summed to the request. v3 card: nothing | ask; calibration is an absence on both sides | v2: members leave only when a rationed supply reaches them in a filed priority order. v3: a group chosen on an extreme of a noisy outcome regresses to the mean |

  None reaches the tier, but task130 needs one more line.
  - Its folder still holds v2, the Tenter House call-off, and v2 carries two of the four outline axes: the same deliverable pair (with a per-category curve by month as the png), and a count per category that sizes a request.
  - The card records v2 as failed on the portal on 2026-10-11. The slot has been re-rooted to v3, an actuarial claims baseline that is not built on disk and shares none of the four axes.
  - So v2's overlap is history.
  - In v2, a survival curve is one of the wrong routes. In task134, a survival-type estimator done right is the answer.
- **Shape.** task131 is also shape 07 (a grid of cells). It is three numbers back, outside the guard's ban on repeating the last two builds' shape. Its deliverables (docx plus png) and its decision (pick one of four) differ. The shape is a component, so this is one repeat to watch in the batch, not a finding.

## Track B findings, mechanism

None.

**Part 6.1's standing bans clear on the cards.** In the guard's draw order, the three builds before task134 are task130, task132 and task133. By task number, they are task131, task132 and task133. The table covers both sets.

| Axis | task134 | task130 (v3 card) | task131 | task132 | task133 |
|---|---|---|---|---|---|
| Pairing | criminology-justice with forecasting (the first criminology card on file) | actuarial with forecasting | marketing with experiment-causal | energy-utilities with forecasting | banking-credit with forecasting |
| Decisive gap | population | objective | population | population | time |
| Decisive pattern | G16 | A | G10 | G6 | G9 |
| Gate G | method_or_model_selection | forecasting | method_or_model_selection | forecasting | forecasting |
| Decision | allocation_to_total | quantity_figure | pick_one_of_n | dial_setting | quantity_figure |
| Calibration, context artifact | none, none | other, operations log | none, register | none, filed standard | none, filed model |
| Strategy | maturity_censoring | forecast_method_backtest | causal_design | population_selection | stated_rule_hard_construction |
| Role, forum, forcing event, organisation | policy adviser, council, vote, local government | procurement lead, trustees, contract, school or university | product manager, executive team, budget, co-operative | capacity planner, line manager, other, utility | finance controller, board, period close, financial institution |

- The decisive gap repeats from task131 and task132. The gap alone is not a ban, and population is the most common decisive gap on file, carried by 44 cards.
- The Layer 2 pattern, `own:competing-removal-and-death-in-return-forecast`, is unique on file.

**task70 and task104 match task134's card labels, but reading the builds clears both (promoted).** Both match task134 on three labels: the decisive gap (population), the decisive pattern (G16) and the Gate G mechanism (method_or_model_selection).
- That label combination is the signature that caught the task86 against task72 Template, so the screen sends both pairs to adjudication however far apart their surfaces sit (0.078 and 0.077 here).
- task134's card already carries a differentiation line for each.

**task134's decisive move, nouns stripped:** "Estimate a within-horizon event probability where an exit other than the event takes a unit out of risk for good, and no unit has been followed to the horizon: count those exits as ending the risk, not as censoring." Its path, from the write-up:
1. Stack the two jail systems.
2. Fix the population and the window.
3. Define the event.
4. Link the competing exits.
5. **Estimate the cumulative incidence with removal and death competing. This is the decisive step.**
6. Apply it to the adopted projection.
7. Round to whole navigators.
8. Make the call.

**task70 v2.** It is live on the ledger, and no portal result is recorded for v2. Decisive move: "A per-record date is built from an event log, and a filed clause bars one class of record from a capacity slot that opened after the closed validation window, so the cut has to be class-conditional; the classless construction reproduces the closed record exactly and overstates a per-period threshold charge."
- **The same claim? No.**
  - task70 builds a record attribute under a filed class restriction that a closed corpus cannot see.
  - task134 chooses an estimator for a real-world probability, and has no corpus.
- **Path.** task70's decisive step sits at steps 5 and 6 of 9: check the one-cut model against the clause, then rebuild acceptance per service. Both come after a validation step.
- **The only move both builds make** is linking records across an event log.
  - In task70, that link builds the decisive date.
  - In task134, it is Layer 1 at rung R3 (removals linked only by the current person number). That moves Puerto by about 1.4 points and crosses a navigator boundary only at Norte.
  - These are not the same device.
- **Verdict:** clean. The labels are shared, and no device is.

**task104.** It has no ledger row, so its status is unknown. Decisive move: "What a self-adapting scorer would have flagged under a setting it never ran at has to be re-simulated, because it keeps flagged observations out of its own reference window and re-takes them before acting; re-thresholding the log reproduces the closed record exactly and overstates what a stricter setting catches."
- **The same claim? No.**
  - task104's answer is a counterfactual replay of a stateful process.
  - task134's answer is the observable-world probability. Its wrong answer, Kaplan-Meier, is the counterfactual: a world with no removals or deaths.
  - Both naive routes answer a different question from the one asked. But the moves that fix them have nothing in common: one re-runs the process, the other switches to the competing-risks estimator.
- **Path.** task104's decisive step sits at step 6 of 11 (re-run the scorer at each allowed threshold), after the scorer's rule is recovered from its log at step 5.
- **Verdict:** clean. The labels are shared, and no device is.

**Builds sharing two of the three core axes at a distance, read and cleared.**
- task124 (ten numbers back) and task83 share the decisive gap and the decision type (allocation_to_total). Their drivers:
  - task124: the newcomers' share of a capped peak is priced from analogs whose measured value was held down by the organisation's own intervention.
  - task83: a randomised holdout's effect has to be conditioned on each unit's own prior treatment history.
- task80 is the third card with G16 decisive. Its decisive gap is rule, and its driver dates a fixed-term status from the event that conferred it. Its driver overlap with task134 is 0.101, the second highest, against the screen's 0.40 line.
- None of these states task134's claim.

## Clean, shares components by design

### task132: clean_shares_components (not promoted, read at my discretion)

**Status:** two numbers back, in the same lane, drawn the same day. It was shipped to the author during this run. The ledger is silent, so its status is unknown.

**Decisive moves, with the domain nouns stripped.**
- **task132:** "A unit that has the event once is replaced by a new unit whose hazard starts again from the bottom, so a position's expected events weight the current unit's hazard by its chance of still being in place and add the new unit's hazard after; carrying the current unit's hazard through the horizon counts events a position cannot have."
- **task134:** "An exit other than the event takes a unit out of risk for good, so the within-horizon event probability weights each period's event hazard by the chance of no exit of any kind; censoring those exits estimates the probability in a world without them."
- **The same claim? No.** Each build's naive path already gets right what the other build's stump turns on:
  - task134's stump, Kaplan-Meier, counts each release's first return once, so no release returns twice. That is task132's point already handled.
  - task132's forecast has no exit other than failure before each relay's scheduled end of support, so task134's error cannot arise there.

**Paths, in order.** task132 puts its decisive step at step 4 of 8, and task134 at step 5 of 8.
- **task132:**
  1. Count failures by module-age band.
  2. Count module-months and derive the band rates.
  3. Set each relay's end of support by bay.
  4. **Weight the present module's rate by its chance of still being fitted, with a new module after a failure. This is the decisive step.**
  5. Count usable stock.
  6. Size Poisson lots.
  7. Price the order.
  8. Make the call.
- **task134:** as listed under Track B.

**Where the shared component sits.** In both builds, the answer is built by accumulating an event hazard with a survival weight.
- In task132, the stump leaves the weight out: rung 3, +44.5 per cent, 19 lots against 13.
- In task134, the stump keeps a survival weight but leaves removal and death out of it: rung R1, Kaplan-Meier, 40 navigators against 36, with Puerto at 66.6 per cent against 50.4.
- So the construction is shared and the decisive insight is not. In task132 the insight is replacement after the event; in task134 it is a competing exit.

**How close it is.**
- Both answers compute the same kind of object, both naive answers overstate, and both cards put the decisive gap on who is still at risk. A solver drilled on one build is primed to ask "who is still at risk at each step" on the other.
- The pair clears on the claim, not on the frame.
- The cards file task134's strategy as maturity_censoring and task132's as population_selection. If task134 were filed as population_selection, the guard would block it against task132.
  - The label is accurate: what fails in task134 is Kaplan-Meier's assumption that a censored unit stays at risk.
  - But it sits on a boundary, and it is reading the two builds, not the label, that clears the pair.

**Outline.** None of the four Shape echo axes is shared:
- ask construction: constraint-first against calendar-first;
- deliverable species: xlsx plus docx against xlsx plus png;
- decision: a dial setting against an allocation;
- calibration: no organ on either side.

### task133: clean_shares_components (not promoted, read at my discretion)

**Status:** back to back, in the same lane. It was shipped to the author per `START_HERE.md`. The ledger is silent, so its status is unknown.

**Decisive moves, with the domain nouns stripped.**
- **task133:** "A cumulative event curve filed from each unit's entry has to be entered at the unit's current age and conditioned on its survival to date; read from entry, it treats every unit as new."
- **task134:** as above.

**The same claim? No.**
- task134's forward cohort is next year's releases, and each one starts at release. No unit is part-way along the curve, so conditioning never arises.
- task133's curve is filed, so estimating a curve under censoring and competing exits never arises.

**The shared component.** Both builds use a cumulative event curve indexed by time since entry.
- In task133, the curve's origin carries the stump: rung 0, the curve read from entry, at +43.6 per cent. The survival division is the nearest wrong rung: rung 3, at -3.3 per cent.
- In task134, the curve's estimator carries the stump.

**The numbers.** Card driver overlap is 0.113, the highest task134 has against any build, and under the 0.40 line. The guard's text similarity is 0.05 to 0.06.

**Outline.** None of the four Shape echo axes is shared:
- ask construction: number-first against calendar-first;
- deliverable species: xlsx plus pptx against xlsx plus png;
- decision: a currency figure against an allocation.

Both prompts open on the deciding forum and its date, which is covered under Corpus habits.

### task99, task31 (R8) and task75 (v1): the right-censoring device, demoted (not promoted, read at my discretion)

**The shared device.** A duration or probability is estimated from a log whose slow cases are still open, and dropping them, or counting them as no event, biases the answer.
- **Where the device was decisive:**
  - task99 R5: Kaplan-Meier at 300 days against 144 for complete cases, in the controlled stratum;
  - task31's R8, superseded on 2026-08-19 (task31 is failed on the ledger);
  - task75 v1, retired on 2026-09-07.
- **Where it sits in task134:** rung R0, the share booked again so far, at 29 navigators, seven low. The stump's competent solver clears that rung by reaching for a survival estimator.
- **task134's decisive rung, R1,** is the competing exit, which none of the three carries. task99 even inverts it: its correct estimator, Kaplan-Meier, is task134's stump.
- **Verdict:** demotion, which is reuse.

**Status:**
- task99 has no ledger row, and the screen excludes its number as scratch.
- task31 is failed.
- task75 v1 is retired. task75 v2 is live and keeps censoring as a supporting device.

### task126: clean_shares_components (not promoted, read at my discretion)

**Status:** inside the batch of 12, with no ledger row.

**What is shared.** Both builds handle a right-censored time-to-event estimate at a step below the decisive one.
- In task126, the competent solver censors undecided filings at the extract date.
- In task134, the share-so-far rung is cleared.
- task126's decisive move is identity resolution instead: splitting the succession links that opened new units from those that continued one.
- No device carries the stump in both builds.

## Strategy monoculture

Counted over the 12 builds ending at task134 (task123 to task134), from the cards' `stump_strategy`, `decisive_rule_filed`, `official_decoy` and `validated_decoy` fields. The guard's own window gives the same counts: draw order, task122 to task134 without task123.

- **Stump strategy.**
  - Two builds each: causal_design (task124, task131) and binding_constraint (task127, task128).
  - One build each: time_semantics (task123), withheld_rule_corpus_fit (task125), identity_resolution (task126), composition_mix (task129), forecast_method_backtest (task130), population_selection (task132), stated_rule_hard_construction (task133) and maturity_censoring (task134).
  - No strategy is near a third of the batch, which would be four of twelve.
  - maturity_censoring was last used by task31, task59, task91 and task99, all outside the window.
- **Withheld rule with an official decoy: 0 of 12.**
  - The one official decoy (task123) sits with a filed rule.
  - The five withheld rules (task124, task125, task127, task130, task134) carry no official decoy.
  - In task134, what is withheld is the estimator. The guidance files the estimand (population, outcome, window, unit, district), and nothing filed points to a rival method.
- **Certified-record (validated) decoy: 6 of 12, above the cap of three.**
  - The builds are task123, task124, task125, task126, task127 and task129.
  - Over the 15 builds ending at task134 it is 9 of 15, adding task120, task121 and task122.
  - The ledger is silent on all nine.
- **task134 adds to none of these counts.**
  - The validated-decoy breach comes from builds between task120 and task129, so it is not task134's to repair. But any batch that ships task134 beside those builds carries it.
  - The five builds on the two-layer standard, task130 to task134, carry no decoy of either kind.

## Corpus habits

- **The time-to-event family.** Three consecutive builds in this lane, all drawn the same day, put the decisive step inside a time-to-event construction:
  - task132: renewal after a failure;
  - task133: conditioning on survival to date;
  - task134: competing exits.

  Earlier, task46 ran its clock on cumulative service exposure.

  The task133 pre-flight asked for any fourth draw in the time-origin family to be read by hand. I read it, and task134 is not one: its forward cohort starts at release, and its decisive step is the estimator. Even so, a batch reviewer holding task132 to task134 reads survival curves three times.

  The drivers differ pairwise and so do the strategies, and the guard scores these pairs at 0.04 to 0.06, under its 0.12 line. So the guard will pass a fourth time-to-event draw. If the next draw in this lane reaches for one, it needs reading by hand before its ladder is written.
- **Dictionary naming.** Five consecutive builds name the extracts dictionary or readme `<system>_extract(s)_<document>`:
  - task130: `housing_needs_extracts_dictionary.txt`
  - task131: `crm_extract_field_notes.md`
  - task132: `eam_extract_dictionary.txt`
  - task133: `ecl_extract_dictionary.txt`
  - task134: `jail_extracts_readme.txt`

  Other builds use an extract-notes form too: task126 and task128 inside the batch, and task93, task102, task103, task106, task108, task110 and task111 earlier. The file role is required content and the name is the habit, so this is not evidence about any pair.

  Elsewhere in the corpus, `data_dictionary` is in 61 builds, `export_manifest` in 33 to 34, and `data_notes` and `provenance` in 12 each. task134 carries none of those names.
- **Date-range file names.** A `YYYY-MM_YYYY-MM` range stamps the big extracts in task118 (from its restored profile), task130, task132, task133 and task134 (`jail_releases_2021-10_2026-10.csv`, `jail_bookings_2021-10_2026-10.csv`). Earlier builds using it are task103, task106 and task111.
- **Opening on the forum and its date.** In the 12 builds ending at task134, three open by naming the deciding forum and its date in the first clause:
  - task123: "The number the trustees vote on 11 November..."
  - task133: "One number goes to the board on 23 October..."
  - task134: "The Commissioners Court votes on 24 November..."

  voice-check files task134 under `other` because its calendar-first pattern needs a lower-case forum name. That is a gap in the classifier, not a problem with the prose. In voice-check's own window (task124 to task134, plus task229), 9 of 12 builds sit under `other`.
- **The pack handed over.** task134 says "Julie Houston's extracts, the guidance and the adopted projection are in the folder." That is the carrier phrase `prompt-voice.md` lists, which appeared in 8 of the client's 18 prompts.
  - voice-check matches only "is in the folder", which is why its CARRIER WORDING block came back empty.
  - It is the only such sentence in the 19 prompts on disk.
  - The repair is one sentence, and `prompt-voice.md` carries the options.
- **Deliverables.**
  - The xlsx-plus-png pair appears twice in the 12: task130's spent v2 and task134, each with a per-category curve by month as the png. Across the corpus, three earlier builds carry it.
  - There is no Code deliverable anywhere in the 12.
  - At 156 words, task134 is the shortest prompt in the window.
- **Personas.** Three first names or surnames recur weakly against cards in the 12:
  - Anthony, against task130's Anthony Olsen;
  - Bryant, against task123's Liam Bryant;
  - Francis, against task131's Francis Amrein.

  The guard's people check on shipped text is clean, so this is not a finding.

## What to redraw

Nothing. Neither track has a tier, so the draw, the ladder and the data stand.

One axis to hold through any hardening: the decisive weight stays on removal and death as competing exits (rung R1).
- A hardening that moved it onto the share-so-far step (R0) would put the stump on the right-censoring device that task99, task31 and task75 already spent.
- One that brought in releasees part-way through follow-up would put it on task133's conditioning on survival to date.
