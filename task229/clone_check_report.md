# Clone check: pre-flight, task229 against the whole corpus, 2026-10-11

## Verdict
CLEAN for task229. There is no Track A finding and no Track B finding at any tier, whether against a live build or a dead one. Separately, at batch level the certified-record decoy stands at 7 of the 12 builds ending at task229, against a cap of 3. That is a Strategy monoculture finding, and task229 is not one of the seven.

## Scope and coverage
- **Mode and scope.** Pre-flight on task229 against every other build, with no window. The screen ran as `fingerprint.py screen --focus task229` and reported its window as "all builds". I read the `clone-check` skill text from the current file before writing any verdict.
- **Draw order.** The screen decides "consecutive" by task number, and the numbering jumps from task131 to task228.
  - I applied the consecutive-build rules by hand to task228 (one back) and task131 (two back). This is also the guard's draw order (drawn date, then task number).
  - task130's v2 re-root has the same drawn date as task131 (2026-10-10). It was committed later that evening (23:39, against task131's build at 21:30), so I checked it under the same rules too.
- **Extract.** 126 build cards in total.
  - 16 were fingerprinted from disk: task117 to task131 and task229.
  - 110 were carried over from the cache, fingerprinted on another checkout (`/Users/saa/...`). Their mechanism fields match today's card files exactly, with no drift.
  - This run was told to modify nothing but this report. So I streamed the extract's output straight into the screen through a pipe, using `fingerprint.py`'s own task enumeration, `build_card` and cache merge.
  - The tracked cache `.claude/skills/clone-check/.cache/fingerprints.json` (written 02:38) was not rewritten. It is still stale: it holds neither task229 nor task228.
- **Pairs screened: 123.** That is task229 against each of the other 123 screenable builds, ranked against the 7,626-pair corpus baseline.
  - task1 and task2 drop out at the screen's filter: they have no prompt or target in the cache, and no gap or pattern on their cards.
  - **Promoted by the screen: 0.**
- **Consecutive rules checked by hand. None fires.**
  - task228 (one back): only the decisive gap collides, and the driver overlap is 0.015.
  - task131 (two back): surface at the 78th percentile, only the decisive gap collides, driver overlap 0.029.
  - task130: surface at the 58th percentile, no mechanism axis collides.
- **Builds the screen cannot see.** task114, task115, task116 and task228 have cards, but their builds are neither on this disk nor in the carried cache.
  - I scored Track B from their cards with the script's own `track_b`:
    - task228 and task116 collide on the decisive gap only.
    - task115 collides on decisive pattern D only.
    - task114 collides on nothing.
    - No promotion route fires.
  - Track A against these four was limited to the card's surface fields: invented names, personas, deliverable names, spine file and geography. None overlaps.
  - task228's prompt, target and write-up live on the b228 checkout, which this run was barred from reading, so they were not compared.
- **Not reachable at all.**
  - task61: retired and its folder deleted. Its ledger row shares no gap, pattern or decision with task229.
  - task96: a ledger row only, marked "drawing". It shares the decisive gap only.
  - task99: a scratch slot, excluded by the script by design.
- **Pairs adjudicated: 5.** All five were promoted by me, not by the screen, and I read them here one after another (no Agent tool was available).
  - **task228:** the adjacent build. It shares the objective, the decisive gap and the Gate G mechanism, and the screen cannot reach it.
  - **task71:** the vocabulary sweep's nearest wording ("equal-weighted across 40 client groups").
  - **task34:** approved. It shares decisive gap and pattern D, and its ledger mechanism reads "weighted household grain against unweighted person rows".
  - **task48:** shares the gap, decision type `designation_set`, strategy `grain_or_unit` and a decisive G2 grain mismatch.
  - **task49:** shares the gap, pattern D, `grain_or_unit` and shape 10, the most label overlap of any build.
  - **Why I promoted them.** For a build that repeats task229's driver under different labels, the screen's only route is a word-overlap (Jaccard) score on the driver sentences. Its maximum here is 0.111.
    - So I swept every card driver, concrete driver, stump, lineage driver and ledger mechanism cell for the vocabulary of task229's move: pooled, ratio of sums, mean or average of per-entity shares, equal weight, unweighted, heavy or dominant entities, standard error, binomial, between-unit spread, overdispersion, record count.
    - 60 cells hit.
    - I also read the one dead-row structural match, task98 v3, from the cards.
- **Pairs left unread: 119 screened pairs plus 3 card-only slots (task114 to task116). None was promoted.**
  - 12 builds share task229's decisive gap and pattern (population, D). I adjudicated task34 and task49.
  - For the other ten (task52, task57, task60, task72, task74, task77, task81, task90, task93 and task103), I read the card driver sentences. None states task229's move.
  - The top surface neighbours are task28 at 0.1001 (97.7th percentile), then eleven pairs at 0.1000. All of them score only on the flat layout and the csv/json/md/pdf/xlsx format mix.
- **How the reading was done.**
  - Sources: the cards, the ledger, task229's design note, and task229's prompt and target as the extract and `voice-check.py` profiled them.
  - No golden file was opened. No answer key was read beyond what the cards and task229's design note already state.
- **Mechanism coverage, over the 123 other screened builds:**
  - Track B was scored on 101 pairs.
  - 22 pairs were checked on Track A only. Those are the 17 builds with no mechanism layer (task3 to task10, task13 to task15, task18, task19 and task21 to task24) and the 5 note-only builds (task16, task17, task20, task112 and task113, whose notes are on another checkout).
  - 34 builds carry back-fitted labels (task36 and earlier), and 14 of those have a card.
  - The vocabulary sweep read every card driver that exists among those 22.
- **Status.** The ledger has rows only for task25 to task108.
  - task109 to task131, task228 and task229 have no row, so their status is unknown on the record.
  - Two of the screen's "delivered or approved" ranks are regex false positives triggered by fiction text:
    - task48 matched "one group-by delivered the conclusion" and "$47,659 approved". Its status cell actually records "Awaiting round 2".
    - task72 matched "service delivered under ...". Its status cell actually records "stump-check round 3 not yet run".

## In batch against earlier builds
- Pre-flight mode has no window, so every pair is task229 against an earlier build.
- **No hit against an approved or delivered build.** I scored every genuinely approved build in the ledger on both tracks: task25, task27, task28, task29, task30, task33, task34 and task35.
  - task28 is task229's nearest surface neighbour in the corpus (0.1001, 97.7th percentile). It scores on flat layout and format mix alone and shares no mechanism axis.
  - task34 shares the decisive gap and pattern labels. On task34's side those labels are back-fitted, and the drivers differ (adjudicated below).
- No exclusion-level exposure exists for task229.

## Track A findings, reviewer visible
None.
- **Hard tells.** Across all 123 screened pairs there are:
  - no byte-identical files,
  - no same-seed tables,
  - no tables with an identical column set,
  - no shared target file names,
  - no shared invented names.
  - "Halvane Metering" and the persona Troy Phillips appear on no other card.
- **Prompt and write-up.**
  - No shared ask construction, no identical deliverable species and no shared solution-step construction.
  - The largest masked-prompt overlap is 0.0042 (task75) and the largest write-up overlap is 0.0036 (task111).
  - The only shared capitalised token is "Tuesday" (task75).
- **Habit file names.** The target avoids them. The dictionary role is `mds_extract_field_reference.md` and the provenance role is `extract_log_20261012.csv`. There is no `data_dictionary`, `export_manifest` or `provenance` file.
- **`voice-check.py task229`.** It ran over task121 to task131 and task229; task228's prompt is not on this checkout.
  - No carrier wording and no unlisted repeated word runs.
  - Economy is inside the paid-out limits:
    - 244 words, against a median of 253.
    - 22.2 words a sentence.
    - Context share 25.4 per cent.
    - Longest paragraph 121 words.
    - One rounding tag, carried by a convention sentence.
  - The opening classifies as "other", which is the classifier's catch-all and holds 6 of 12. The card records calendar-first, which is 2 of the last 12 (task128 and task229).
- **task228, compared on card fields only.**
  - Domain, geography, currency, organisation, forum, forcing event, spine and personas all differ.
  - No deliverable name is shared: `wave8_read_health_alerts.json` and `read_health_by_build_wk41.png` against `peak_alert_config.json`, `alert_replay.py` and `peak_alert_tradeoff.png`.
  - The outlines differ: shape 10 against 04, a designation set against pick one of N, and no calibration organ against a gold-standard subsample.
  - The one partial outline echo is a JSON alert payload beside a PNG, which is below Shape echo.
  - The ask sentences could not be compared.
- **Shape 10, shared with task49 and task85.** Nothing else on the surface overlaps: task49 delivers py and xlsx with a single-dollar-figure ask, and task85 asks for a probation pick. That is below Shape echo.

## Track B findings, mechanism
None, live or history.
- No build's main fields share task229's decisive gap, decisive pattern and decision type together. None shares the gap, pattern and Gate G mechanism together either.
- The only match on that signature is a retired architecture, task98 v3 (gap population, pattern D, designation set). It is reported below as history with a different driver. The card already carries the differentiation line the guard asked for.
- No driver sentence on file states task229's move. The nearest wording is task71's equal weighting across groups, and in task71 that sits on a non-decisive rung.

## Clean, shares components by design
**task229's decisive move, with the domain nouns stripped:** score each group as the mean of its entities' shares, over the entities present for the whole window, with the error drawn from between-entity spread. The naive alternative is a record-pooled ratio with a record-count error.

**task229's path:**
- R0: the pooled pipeline.
- R1: the as-of version, measured against every expected record.
- R2: the population present for the whole window.
- R3: the per-entity mean (decisive).
- R4: the error from between-entity spread (decisive).

The pairs:

- **task228** (adjacent; ledger silent, so status unknown on the record). Read from the cards and task229's design note; task228's own note is on a checkout this run could not read.
  - Its move, stripped: the false-alarm budget applies per run while the check is evaluated every night, so the setting has to be calibrated on runs of the forward length, and that flips the leading candidate.
  - Not the same claim.
  - Shared components:
    - the objective;
    - the Gate G frame (`signal_vs_noise_or_hold`, an alert threshold set against noise);
    - the decisive gap label;
    - generators G12 and G17;
    - a JSON alert payload beside a PNG.
  - Position of the shared devices:
    - In task228, the noise calibration (a per-run budget over repeated looks) is the frame its competent solver already runs, and the population (forward run length) is the decisive move.
    - In task229, the population is R2, and the noise model (the error that follows the unit) is half the decisive pair.
    - So the shared devices sit on swapped rungs, and their content differs: multiplicity over repeated looks against a clustered error.
  - Verdict: clean_shares_components. Nothing to redraw.
- **task71** (ledger: built, portal result not recorded).
  - Its move: a coverage share is struck on a weighting recovered from closed determinations, on a clock that drops only the interruptions a zero-activity test shows actually blocked use.
  - Shared device: equal weight per group rather than volume weighting.
  - Position:
    - In task71, the weighting is recovered by back-test and is reached by the competent solver (the stump files 56 days with it). Its decisive rung is the clock.
    - In task229, the equal-weight mean is stated by the filed standard and is decisive, next to an error rung that has no counterpart in task71.
    - The device carries the decisive rung on one side only, which makes this reuse.
  - Verdict: clean_shares_components.
- **task34** (ledger: approved).
  - Its move: a subpopulation that no column names, found only by a within-cluster fit of an amount on unit size and confirmed by a re-measured subsample.
  - Shared: the two-grain frame, meaning shares reported at household grain built from person rows. That is the ledger's "weighted household grain against unweighted person rows". It sits beside the regimes as framing; neither task34's driver nor its stump turns on it. task229's unit is its decisive pair.
  - task34's gap and pattern labels are back-fitted, so that collision is a shared guess.
  - Verdict: clean_shares_components.
- **task48 v2** (ledger: built, awaiting round 2).
  - Its move: re-aggregate records to a two-sided pair grain to expose a coordinated population the monitor's grain cannot express. This comes after five flags are conditioned away and holding is the strongest wrong answer.
  - Shared:
    - a designation set with a hold as the rival answer;
    - the `grain_or_unit` family, with G2 decisive;
    - overdispersion measured against a count-based variance. task48's "small-series dispersion" flag is conditioned correctly by its competent solver, while in task229 the same device is half the decisive pair.
  - Not the same claim: discovering a grain, against weighting at a known grain.
  - Verdict: clean_shares_components.
  - Worth knowing: task48 v1 (retired) spent `signal_vs_noise_or_hold`, with small-cell overdispersion as one of its five conditionings. The ledger records every one of those rungs as a hygiene reflex the opponent ran unprompted. That is a record about the device, not a clone of task229's driver.
- **task49** (ledger: built, live).
  - Its move: floor an unpaid amount at zero per instrument before summing, because netting inside an entity makes every reporting date look comfortable.
  - Shared: pattern D, `grain_or_unit`, shape 10, and aggregating per entity first.
  - Not the same claim: a floor that does not commute with summing, against an equal-weight mean with a clustered error.
  - The same holds for the rest of the floor family: task16, task58, task65 and task93.
  - Verdict: clean_shares_components.
- **task98 v3** (retired 2026-10-03, history).
  - It matches the Part 6.1 signature: gap population, pattern D, designation set.
  - Its move: units formed by chaining members that lie within a fixed distance, then a per-unit threshold, with the forward period merging two labelled groups.
  - The driver differs. task229's card carries the differentiation line that answers the guard's same_puzzle_older note.

## Strategy monoculture
Batch: the 12 builds ending at task229 in the guard's draw order, read from the cards' fields. They are task121, task122, task124, task125, task126, task127, task128, task129, task130, task131, task228 and task229.

| Measure | Count | Cap | Verdict |
|---|---|---|---|
| Withheld rule with an official decoy | 0 of 12 | 2 | under |
| Certified-record decoy (`validated_decoy`) | **7 of 12** | 3 | **over, Strategy monoculture finding** |
| Any one `stump_strategy` | max 2 of 12 (identity_resolution, causal_design, binding_constraint) | 4 (a third) | under |

- **The seven builds carrying the certified-record decoy:** task121, task122, task124, task125, task126, task127 and task129.
- **Trend.** The count was 9 of 12 at task131's pre-flight. task123 has since left the window, and task130's v2 card no longer carries the flag.
- **Corpus-wide.** 47 of 129 cards carry it.
- **task229.** Its strategy is `grain_or_unit`, with the decisive rule filed, no official decoy and no validated decoy. It adds to neither capped count. It is the only `grain_or_unit` in the window (15 corpus-wide).
- **No change to task229 clears this.** The share drops to the cap only after four more builds without the flag enter the window. The two-layer standard now blocks the flag on new draws.

## Corpus habits
- **Recurring file names:**
  - `data_dictionary` appears in 61 builds and `export_manifest` in 33.
  - `data_notes` and `provenance` appear in 12 each.
  - `county_reference` appears in 4 builds.
  - `product_catalog`, `accounts`, `plan_catalog`, `metric_definitions`, `item_master`, `facility_register`, `site_master` and `sources_and_licences` appear in 3 each.
  - task229 uses none of them.
- **Recurring deliverable pairings:**
  - pdf+csv appears in 9 builds.
  - py alone appears in 8, and py+pdf in 7.
  - pdf+png appears in 6.
  - py+csv, py+xlsx and pdf+xlsx appear in 5 each.
  - docx alone appears in 4.
- **Recurring ask opening.** "give me the single dollar figure we" appears in 2 builds.
- **Forming in the Data Quality Monitoring lane (task228 to task252).** Both lane builds so far share three things:
  - an alert that fires or holds;
  - the `signal_vs_noise_or_hold` Gate G mechanism;
  - a JSON alert payload beside a PNG. In the rest of the corpus only task64 pairs JSON with PNG.
  - Two of two is not yet a finding. It is the lane's default outline taking shape, and the next draws in the block are where varying it is cheap.
- **The last 12, by voice-check:**
  - No unlisted repeated word runs.
  - png, xlsx and docx are each a deliverable in 5 of 12. json is in 1 of 12 (task229).
  - tsv, parquet, jpg, pdf, py, sql and r are not used as deliverables.

## What to redraw
1. task229: nothing.
2. Batch-level, not task229: the certified-record decoy axis (`validated_decoy`), at 7 of 12 against a cap of 3, carried by task121, task122, task124, task125, task126, task127 and task129.

Coverage and tooling notes. These are not findings against any build.
- **(a) task228 Track A.** The Track A comparison against task228 was not run. Run `guard.py surface` or this screen once task228's build and task229's sit on one checkout. Until then, the check against task228 rests on the cards.
- **(b) Stale cache.** The tracked cache was not refreshed in this run, by instruction. It still lacks task229 and task228.
- **(c) Consecutive by number.** The screen measures "consecutive" as a task-number difference, so it misses draw-order neighbours across the task131 to task228 jump.
- **(d) Card-only builds.** The screen cannot see builds that are absent from both the disk and the carried cache (here task114 to task116 and task228).
- **(e) Status regex.** The status-rank regex reads fiction words as delivery status (task48 and task72).
- **(f) Decisive mechanism.** Both the guard and the screen take the pattern letter before any G-code when choosing the decisive mechanism (`decisive_mech`). So a card filed as pattern D and a card filed as `none` with G2 decisive can never collide structurally, even though both describe the same two-grain family.
