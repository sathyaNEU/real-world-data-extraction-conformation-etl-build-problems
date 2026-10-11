# Clone check: pre-flight, task181 architecture 2 against the whole corpus (pass 1), 2026-10-11

## Verdict
CLEAN for task181 (architecture 2). There is no Exact, Same seed, Dataset or Template finding and no Shape echo, and the screen promoted no pair. The worst tier touching task181 is Idiom: its run report is named on the corpus's `extract` stem again (`pertussis_extract_run_20261005.txt`), a stem that architecture 1 had renamed away. Batch level, not task181: Strategy monoculture, with the certified-record decoy in 7 of the 12 builds ending at task181 against a cap of 3.

**Stage 5 gate (`build-pipeline`).**
- The adjudicated pre-flight returns no Exact, Same seed, Dataset or Template finding, so its half of the gate holds.
- The Idiom note goes to the author and is not looped on.
- **The heart half.**
  - It is recorded as PASS in the message of 98d9ecf (10:01), but `pipeline.json`'s `duplicate_check.heart` is still empty.
  - That run read this worktree's `cards/task180.json`, which is task180's spent architecture 2. task180 re-rooted to architecture 3 at 10:14 (1e53a54 on its branch), after that run.
  - I replayed the standing bans in memory with the guard's own helpers against the v3 card. There is no BLOCK. A heart re-run against that card will raise two WARNs: `repeat.decision` and `repeat.opening`.
  - This pass did not run `guard.py`.

## Scope and coverage

**Mode and scope.**
- **The build.** Pre-flight on task181, architecture 2: a regional public health unit's pertussis surveillance. It chooses the local government area the outbreak response team works this week by nowcasting each area's fortnight on its own laboratory route's reporting delay.
- **The comparison.** Against every other build with the window ignored. The screen reports "all builds".
- **Pass.** This is pass 1 on architecture 2. Architecture 1's pre-flight is kept as `task181/clone_check_report_arch1.md`. Architecture 1 and the unregistered draft are this task's own lineage and were not compared.
- **Report path.** The agent definition's default for a pre-flight is `clone_check_report_<taskid>.md` at the repo root. The pipeline's stage 5 and this invocation both name `task181/clone_check_report.md`, beside the `_arch1` report, so it is written here. Nothing was overwritten.

**Version checked.**
- **Card:** `cards/task181.json` at 5a69298 (08:05): architecture v2, `mechanism_source: design_note`.
- **Prompt:** as at fdce3c7 (09:38).
- **Submission:** as at cf25887 (09:30).
- **Pack:** 11 files under `target/`, rebuilt at 09:57.
- **Design note:** as at 98d9ecf (10:01). During this run the pipeline's main thread added an uncommitted paragraph recording leak reader pass 2. It touches nothing the screen reads.
- **Concurrent commits.**
  - HEAD moved to 98d9ecf at 10:01:53, as this run began. The extract ran at 10:03 on that state.
  - task180's branch moved to 1e53a54 at 10:14 (its architecture 3) during this run. That is handled under Draw order.
- **Re-run.** At 10:22 I re-extracted and re-ran the screen. The JSON output was byte-identical (sha256) to the first run.

**Extract.**
- **127 cards.**
  - 17 were fingerprinted from disk: task117 to task131, task181 and task229.
  - 110 were carried over from builds fingerprinted on another checkout (`/Users/saa/...`).
- **Stale cache.** The cache was written at 09:23. That was before architecture 2's prompt edit, design note, goldens and metadata.
  - I re-extracted in place. Only task181's entry changed: the prompt went from 135 to 140 words, and the design note is now 5,314 words.
  - The refreshed cache stays in place. It was already modified against HEAD before this run.
- **Drift.** All 125 cached entries that have a card file match today's card files on the 13 fields the screen reads (0 drifted). task112 and task113 have no card file.

**Screen.**
- `fingerprint.py screen --focus task181` covered 125 screenable builds (task1 and task2 have neither a prompt nor a pack), so 124 pairs.
- **Baseline.** 7,750 corpus pairs, mean surface 0.0546. The 99th-percentile route starts at 0.1045, and the consecutive 97th-percentile route at 0.0974.
- **Promoted: 0.**
- **Nearest, not promoted:**
  - task93 0.100 (97.7th percentile);
  - task90 0.094 (94.4th);
  - task72 0.093 (93.0th);
  - task89, task65 and task51 0.093 (92.4th to 92.6th).
- **What carries those scores.** Flat layout (1.0) and format overlap (0.83 to 1.0). None of them shares a file name, bytes, a schema, a numeric signature, an invented name, a prompt shingle, an ask construction or write-up text.
- **Their Track B.** task72 shares the decision type. task51 and task89 share the decisive-gap label.

**Draw order.**
- The screen measures "consecutive" by task number.
- The guard's draw order runs by drawn date, then number. In it, task181's predecessors are:
  - task180, one back;
  - task131, two back;
  - task130, three back.
- task228 and task229 were drawn the same day, after it.
- I applied the consecutive-only routes to these neighbours with the screen's own functions. **None fires:**
  - task131: 89.4th percentile, where the consecutive route needs the 97th; it shares the decision type only.
  - task130: 74.6th percentile; nothing shared.
  - task228 (card only): the decision type only.
  - task229: no pack profile on this checkout; the context-artifact type only.
  - task180: see below.

**task180, one back in draw order, changed architecture during this run.**
- **Architecture 2 is spent.** That was transformer gas attribution, spent at judge pass 2 (SEND_BACK, b09373f, 09:37).
- **Architecture 3 was registered at 10:14 (1e53a54).** A national medicines agency chooses which of three spontaneous-report signals the registries support. On the card:
  - `pharmacology-pharmacoepidemiology-safety` x anomaly detection, shape 18;
  - pick one of three;
  - decisive gap `population`, G17, Gate G `method_or_model_selection`;
  - strategy `causal_design`;
  - decisive rule not filed, and no decoy.
- **How it was read.** This worktree's untracked `task180.json` is still architecture 2 (08:01). I read the v3 card, prompt, submission and design-note header through git from this worktree. Nothing was copied into the repo.
- **Track B on the cards (`track_b_cards`).** Only the decision type (`pick_one_of_n`) collides, one of three core axes. Driver overlap is 0.042.
- **Standing bans, replayed in memory with the guard's helpers.** task181 was the candidate and the v3 card was one back.
  - All clear: pairing, subdomain, decisive pattern, calibration, role, context artifact, spine, shape, strategy, forum, forcing event and organisation family.
  - No same-puzzle or same-driver match, and no shared invented name.
  - WARN `repeat.decision`: `pick_one_of_n` repeats the last build.
  - WARN `repeat.opening`: both cards file the opening as evidence-first.
- **Neither tool had compared this pair.**
  - task181's heart run (10:01) read the v2 card.
  - task180's own check bans only against draws ordered before (2026-10-11, 180), so task181 is never its predecessor.
  - The replay above is the first time the standing bans were applied to this pair.
- **Prompt-level Track A**, against v3's committed prompt and submission:
  - masked prompt overlap 0.0034;
  - no raw shingle, sentence opening, invented name or write-up text shared.
  - No pack comparison was possible, because task180's pack is gitignored on its branch.
- **The spent v2 card.** Against it, no route fires either: no core axis, driver overlap 0.078.

**Builds the screen cannot see.**
- task114, task115, task116, task180 and task228 have cards but no build on this checkout and no cache entry. I scored them with the screen's `track_b_cards`, and no route fires:
  - task114: the decisive gap only.
  - task115: the decisive gap and the decision type (two core axes), not consecutive.
  - task116: nothing shared.
  - task228: the decision type only.
  - task180: see above.
- **task99.** It has a card the guard reads, but the screen excludes `task99` as scratch; its card says that world was carried forward into task31. It is read at card level under Clean.

**Pairs adjudicated: 0.**
- No pair was promoted.
- No Agent tool was available in this invocation, so a promoted pair would have been adjudicated in this thread. None was promoted.
- The card-level readings below were done in this thread. They are labelled as readings, not adjudications.

**Pairs left unread: all 124, plus the 5 card-only builds. None was promoted.**
- **Two core axes.** Three partners carry the decisive gap `time` together with `pick_one_of_n`: task33, task115 and task122. None is consecutive by number or by draw order, so no route reaches them.
- **One core axis.** 39 partners carry the decisive gap `time` (21) or the decision type (18). The highest card-driver overlap is 0.129 (task97), against the 0.40 line.
- **The strategy route the screen does not have.**
  - The screen's Track B reads 13 card fields, and `stump_strategy` is not one of them.
  - Four other cards file task181's strategy, `maturity_censoring`: task31, task59, task91 and task99.
  - I read all four cards in full (driver, concrete driver, stump, lineage and differentiation). See Clean.
- **Vocabulary sweep.** I swept the move's vocabulary across every card's driver, concrete driver, stump, notes, analyst test, domain test, lineage drivers and differentiation lines, and across every ledger row.
  - **Terms:** nowcast, truncation, reporting or notification delay, not yet reported or arrived, backfill, completeness, maturity, development factor or triangle, chain ladder, IBNR, pooled delay, censoring, Kaplan-Meier, survival, and "look quiet" or "look dormant".
  - **Result:** no card or ledger row states the move. Most hits use the words in another sense:
    - censored demand (task18);
    - truncation at a filed intervention (task33);
    - a backfill repair (task22, task98);
    - an operating year still open (task42, task43);
    - maturing survey response rates on a wrong-answer path (task79);
    - lost outcome rows (task15).
  - **Nearest constructions:**
    - task91: young units look dormant;
    - task99: a censored, stratified start delay;
    - task122: late outcomes credited to new sessions.
  - None of them was promoted. Each is read under Clean.

**Mechanism coverage, over the 124 other screened builds.**
- **Track B from both cards:** 102 pairs.
- **Track A only:** 22 pairs.
  - 17 partners have no mechanism layer: task3 to task10, task13 to task15, task18, task19, and task21 to task24.
  - 5 are note-only: task16, task17, task20, task112 and task113.
- **Back-fitted labels:** 34 partners (task36 and earlier). 14 of them have a card layer: task11, task12, and task25 to task36.

**Track A coverage gaps.**
- **Pack-level Track A** ran on 108 of the 124.
  - task3, task10, task117 to task129 and task229 have no profiled pack on this checkout (`target.zip` or nothing). Against those 16, only wording was compared.
  - **Mitigation.** I compared task181's 11 file names, its file stems and its CSV column sets with:
    - the `metadata.json` file lists of task117 to task129;
    - the `target.zip` listings of task117, task119 and task229, with CSV headers read in memory and nothing extracted.
  - No name, stem or column set is shared. The `extract` stem is shared (see Corpus habits).
- **Prompt and write-up.** Prompt-level Track A ran on 111 partners; 13 have no prompt in the cache. Write-up phrasing ran on 110; 14 have no write-up there.

**Status.**
- **The ledger** has rows for task25 to task108 only.
  - **Genuinely approved:** task25, task27 to task30, and task33 to task35.
  - **False positives.** The screen's "delivered or approved" on task48 and task72 is a regex hit in fiction text ("one group-by delivered the conclusion"; "service delivered under").
- **No ledger row.** task109 onwards, task181 included, have no row, so their status is unknown on the record. Their own `pipeline.json` files record:
  - delivered: task117, task119, task130 and task131;
  - shipped: task229;
  - none of those five with a portal result;
  - retired: task120, task121, task122, task123, task125 and task127;
  - in build: task118, task124, task126, task128 and task129.
- **The strategy neighbours on the ledger:**
  - task91 is "built and verified, awaiting the portal";
  - task31 is "failed";
  - task59's status cell does not rank, so it is unknown.

## In batch against earlier builds
- Pre-flight has no window, so every pair is task181 against another build.
- **No hit against an approved or delivered build.**

| Build | Record | Surface (percentile) | Track B on the cards |
|---|---|---|---|
| task25 | ledger: approved | 0.016 (27.8th) | decision type only |
| task27, task28, task29, task30 | ledger: approved | 0.077 to 0.089 (58.8th to 87.3rd) | decision type only |
| task33 | ledger: approved | 0.077 (57.1st) | decisive gap `time` and decision type, two of three core axes; its driver is a measured elevation projected forward and stopped at a filed intervention, recovered by back-testing closed actions (driver overlap 0.015) |
| task34 | ledger: approved | 0.023 (32.7th) | nothing shared |
| task35 | ledger: approved | 0.083 (74.8th) | decisive gap `time` only |
| task117 | no row; its `pipeline.json` records delivered 2026-10-09 | 0 (no pack on this checkout) | decisive gap `time` only |
| task119 | no row; delivered 2026-10-10 | 0.0001 (no pack on this checkout) | decision type only |
| task130 | no row; delivered 2026-10-11 | 0.083 (74.6th) | nothing shared |
| task131 | no row; delivered 2026-10-10 | 0.090 (89.4th) | decision type only |
| task229 | no row; shipped 2026-10-11 | 0.0001 (pack only in `target.zip`) | context-artifact type only (`filed_standard`) |

- task181 has no ledger row, so its status is unknown on the record. Its `pipeline.json` puts it in build at stage 4, with `approved` and `delivered` null.
- No exclusion-level exposure exists for task181.

## Track A findings, reviewer visible
None.

**Hard tells.** Across all 124 screened pairs there are:
- no byte-identical files;
- no same-seed tables;
- no tables with an identical column set;
- no shared target file names;
- no shared invented names.

None of these appears on any other card: "Southern Inland Public Health Unit", "Inland Pathology", "Murrumbidgee Courier Run", "Wagga Wagga Hospital Laboratory", "PR-07" and the nine school names. The only shared capitalised token is "Monday's" (task45), a weekday.

**Prompt and write-up.**
- No five-word masked run is shared with any build: the largest masked-prompt overlap is 0.0000.
- The largest write-up overlap is 0.0039 (task131).
- No sentence opening, ask construction or solution-step construction is shared.
- **The ask.** The screen's ask parser finds no Main Ask sentence in this prompt, because no sentence opens with its verbs. So the ask comparison ran on sentence openings only. The closing "The call is one area." opens no other prompt in the corpus.

**`voice-check.py task181`**, run over task122 to task131, task181 and task229:
- No carrier wording on its list and no unlisted repeated run.
- **Length.** The prompt is 145 words, the shortest of the twelve (median 250; paid-out median 227).
- **Economy.** 24.2 words a sentence, a 35.2 per cent context share (flag 46.0), a longest paragraph of 52 words and no rounding tags.
- **Opening.** Classified "other", a bucket holding 7 of the 12.
- **Deliverables.** .pptx appears in 4 of the 12 and .csv in 4.

**People and setting.**
- No persona's full name or surname is on another card.
- The first name Tiffany is also on task103 and task114. Tiffany Peters is in the cut pack, as the maintainer of the line-list notes.
- New South Wales with AUD is shared with task229 (see Corpus habits).

**Draw-order neighbours.**
- **task180 v3:** see Scope and coverage. Masked prompt overlap is 0.0034, and nothing else is shared.
- **task131**, two back: 0.090 (89.4th), from flat layout and format overlap.
- **task130**, three back: 0.083.

**Outline: the Shape echo test.** Every build sharing any of the four outline axes with task181 is below. task181's own outline:
- the ask closes "The call is one area.";
- pptx+csv;
- pick one of ten areas, shape 17;
- censored or lagged release.

| Build | Ask construction | Deliverable species | Decision | Calibration organ | Axes shared |
|---|---|---|---|---|---|
| task128 (five back; in build) | not shared | **csv+pptx**, the only other build with this pair | allocation to a fixed total, shape 01 | closed decision corpus | 1 |
| task99 (scratch; task31's world) | its prompt is not on this checkout | one .py | **pick one of N**, single figure | **censored or lagged release** | 2 |
| task31 (ledger: failed) | not shared | one .py | a booked figure | **censored or lagged release** | 1 |
| task103 (the only other shape 17) | not shared | pdf+xlsx | release or hold | certified matrix | the shape number only |
| task180 v3 (one back) | not shared | docx+csv | **pick one of three**, shape 18 | none | 1 |
| task131 (two back) | not shared | docx+png | **pick one of N**, shape 07 | none | 1 |

- **Reading.** Only task99 shares two outline axes. The two a reviewer meets first are the ask and the deliverables: task99's ask is not on file and its deliverable differs.
- task99 is the scratch copy of a failed build, so even at Shape echo this would be history.
- **No Shape echo.**

## Track B findings, mechanism
None, live or history.
- **Signatures.**
  - No card shares the decisive gap (`time`), the decisive code (G12, absence of record versus record of absence) and the decision type together. That is the guard's same-puzzle signature.
  - No card shares the gap, the code and Gate G `forecasting` together. That is the same-driver signature.
  - No other card's decisive code is G12. Nine carry it lower down: task27, task30, task39, task49, task56, task63, task123, task228 and task229.
- **Two core axes.** Three partners carry the decisive gap `time` with `pick_one_of_n`. None is consecutive, and each turns on something else:
  - **task33** (approved): a measured elevation stopped at a filed intervention.
  - **task115** (card only): a rival's level, read point by point.
  - **task122** (retired on its own record): late outcomes credited to new sessions (see Clean).
- **Driver text.**
  - On the screen's measure the highest card-driver overlap is 0.129 (task97), against the 0.40 line.
  - On the guard's TF-IDF over every driver, lineage included, the highest is 0.082 (task98's v2 lineage), under its 0.12 WARN line.
- **Sweep.** The vocabulary sweep (Scope and coverage) found no card driver, stump or ledger cell that states the move.

## Clean, shares components by design

**task181's decisive move, with the domain nouns stripped.**
- Counts for a recent period are read before their records have finished arriving.
- How fast the records arrive depends on the route a unit's records take, so the unit on the slowest route looks quiet while it is surging.
- The comparison therefore has to use each unit's count completed from its own route's delay history. It cannot use what has arrived, and it cannot use a delay pooled across routes.

**task181's path** (design note ladder, submission steps):
1. **Layer 1.** Episodes from repeat notifications (PR-07 3.3), dated by first specimen, mapped to areas through the concordance, non-residents dropped.
2. **Rungs 0 to 2.** The notified fortnight against PR-07's expected counts (count, excess, notification-date and ratio variants): Wagga Wagga first, Griffith tied second with Snowy Valleys.
3. **Rung 3.** A nowcast on one delay pooled across the unit. Still Wagga Wagga, because the pooled delay is mostly the hospital route's.
4. **Rung 4, decisive.** A nowcast on each route's own delay: Griffith, in all 36 route-specific cells of the design grid. All 18 pooled cells give Wagga Wagga.
5. **The asks.** School clusters from free-text names, and the quarterly infant table through the admissions and antenatal links (Layer 1 devices).

**The late-arrival family.** These builds share task181's stump strategy, `maturity_censoring`. The vocabulary defines it as "open periods are not fully developed: right-censoring, lag triangles, run-off or late arrival".
- None of these pairs was promoted, because the screen does not score the strategy field.
- I read them at card level in this thread. Their design notes, prompts and packs are on another checkout.
- These are readings, not adjudications.

**task91** (ledger: live, built and awaiting the portal).
- **Its move, stripped (card).** A stock splits into an active pool and a dormant residue. Units too young to have begun exiting look dormant, so they have to be separated by their onset lag before the residue's constant is applied.
- **Its decisive rung,** from the card's differentiation line: separating the runs still inside their onset lag.
- **Where the shared move sits.** In task181 the matching move (treat recent records as immature and complete them) sits at rung 3 with one pooled delay, and is killed. task181's decisive rung is the delay's heterogeneity across routes.
- **Swap test, on the card's description.**
  - Running task91's move (one onset lag for every unit) on task181 is rung 3, which files Wagga Wagga.
  - Running task181's move (complete each unit from its own arrival history) on task91 has nothing to work with: the young runs have no exits yet to complete from.
- **Also shared:** Gate G `forecasting`.
- **Reading:** the drivers differ. The late-arrival device is reused, and in task181 it is demoted to a killed rung.

**task31** (ledger: failed) **and task99** (task31's earlier architecture, R5, under a number the screen excludes as scratch; no ledger row).
- **task99's move.** A start delay is estimated from a right-censored record of past projects, stratified on a covariate found behind a join. Complete-case durations or quoted delays erase the slow stratum (decisive code G16, method selection).
- **The positions are reversed.**
  - task99's stump already stratifies: it files the complete-case duration for the right stratum. So its decisive step is the correction for incompleteness.
  - In task181 that correction is rung 3 (a pooled nowcast), and the stratification is decisive.
  - Familiar moves, in the opposite order, with the other one carrying the decisive step.
- **task31 R10's move.** A lag splits absolutely on a prior-approval property recovered through a join, while the natural split is censored (pattern E). That is the discovery of a hidden stratifier. task181's route is printed on every record.
- **Also different:**
  - the estimand: durations from censored records in both, against eventual counts from truncated reports in task181;
  - the wrong path: complete-case or quoted delays, against counting what has arrived or pooling.
- **Status.** Failed and scratch, so history at most.

**task59** (ledger: status unknown). There the label covers new episodes capped at the weeks left before a forward window closes. That is a horizon cut on exposure, not a reporting delay. Nothing is shared beyond the label.

**Other shared components.**
- **task229** (two after, same day; shipped on its own record).
  - **Shared:** G12 (lower down), the filed-standard context artifact, and reads held at a cut-off.
  - **Its decisive step:** the unit a standard error is built over, with failures shared through a parent node.
  - task181's design note already differentiates it.
- **task122** (retired on its own record).
  - **Its move.** A log records only the outcomes produced before each session closed, so one candidate's late outcomes have to be attributed back through a join.
  - **Different operation.** Those outcomes are in the data. task181's unnotified cases are not in the data, and are estimated.
- **task180 v3** (one back; in build): see Notes for the author.

## Strategy monoculture
The batch is the 12 builds ending at task181 in the guard's draw order: task121, task122, task124 to task131, task180 and task181.
- Counts are read from the cards.
- task180 is read from its live architecture 3 card.

| Measure | Count | Cap | Verdict |
|---|---|---|---|
| Withheld rule with an official decoy | 0 of 12 | 2 | under |
| Certified-record decoy (`validated_decoy`) | **7 of 12** | 3 | **over: Strategy monoculture finding** |
| Any one `stump_strategy` | 3 of 12 at most: `causal_design` (task124, task131, task180) | 4 (a third) | under |

- **The seven builds carrying the certified-record decoy:** task121, task122, task124, task125, task126, task127 and task129.
  - Their own `pipeline.json` files record task121, task122, task125 and task127 as retired.
  - task124 (stage 3), task126 (stage 3) and task129 (stage 2) are live. Counting live builds only, that is exactly the cap.
- **task181** files `maturity_censoring`. The decisive rule is filed (PR-07 4.2), and there is no official decoy and no validated decoy. So it adds to none of the capped counts, and its strategy is 1 of 12.
- **`causal_design` reached 3 of 12 through task180's re-root;** its architecture 2 filed `decomposition_attribution`. That is under a third, and it is the guard's `overuse.strategy` WARN count.
- **The unfiled decisive rule.** It is unfiled in task124, task125, task127 and task180 v3. None of them carries an official decoy, so none is the capped template.
- **Same-day wave view** (the twelve ending at task229, which adds task228 and task229):
  - the certified-record decoy is at 5 of 12, still over the cap;
  - the withheld-rule template is at 0;
  - the largest single strategy is 3 (`causal_design`).
- **Corpus-wide** (130 cards, with scratch task99 excluded):
  - 47 carry the certified-record decoy;
  - 19 carry the withheld-rule template;
  - 4 carry `maturity_censoring` (task31, task59, task91 and task181).

## Corpus habits

**The run report's file name. This is the Idiom finding that touches task181.**
- The provenance or run record is named on "extract" in 7 of the draw-order twelve:

  | Build | Provenance or run record |
  |---|---|
  | task121 | `warehouse_extract_register.csv` |
  | task122 | `extract_register_slot_review.md` |
  | task124 | `extract_log.md` |
  | task126 | `extract_notes.md` |
  | task128 | `extract_provenance_2026-10-23.md` |
  | task131 | `extract_log_2026-09-14.txt` |
  | task181 | `pertussis_extract_run_20261005.txt` |

- The stem also appears just outside the twelve: task123 (`warehouse_extract_record_2026-10-07.md`) and task229 (`extract_log_20261012.csv`).
- **History.** Architecture 1 answered the same note by renaming its record to `cudw_job_fraud_weekly_20261005.txt`. Architecture 2 has returned to the stem.
- **The layout is new.** task181's file is a single-job run report from the state system: parameters, row count, byte count and checksum. task131's is timestamped OK lines, and task229's is a CSV manifest. The habit is the name, not the content.
- **Where the name lives.** Only in `generator/docs.py` and `metadata.json`. No shipped document cites it.

**File names from the screen.**
- `data_dictionary` appears in 61 builds and `export_manifest` in 33.
- `data_notes` and `provenance` appear in 12 each, `county_reference` in 4, and eight other names in 3 each.
- task181 uses none of them. Its `pertussis_line_list_notes.md` fills the field-notes role, named in the unit's own idiom.

**Coded controlled documents.**
- A document code leads the file name of a filed standard in eight builds:
  - task38 `CS-14`;
  - task108 `SP-04`;
  - task109 `STR-04`;
  - task117 `FES-07`;
  - task131 `MP-3`;
  - task181 `PR-07`;
  - task229 `MDS-STD-114`;
  - task180's spent architecture 1, which used `RP-07`.
- This is how real organisations file controlled documents. The closest is the `-07` number shared with task117 and task180 v1. Not a finding.

**Deliverable pairings.**
- pdf+csv 9; py 8; py+pdf 7; pdf+png 6; py+csv 5; py+xlsx 5; pdf+xlsx 5; docx 4.
- task181's pptx+csv is shared only with task128.

**Ask constructions.**
- No carrier on voice-check's list and no unlisted repeated run.
- The closing "The call is one area." opens no other prompt.
- Architecture 1's "what I need" closer is gone.

**Openings.**
- voice-check's "other" bucket holds 7 of its twelve: task125, task126, task128, task129, task130, task181 and task229.
- The cards file both task181 and task180 v3 as evidence-first, back to back.

**Setting.**
- New South Wales with AUD is the setting of task181 and of task229, drawn the same day two apart (task229 shipped on its own record).
- NSW also appears on task104, and AUD on task110 and task118.
- Within the draw-order twelve, only task181 is set there.

**Health surveillance, back to back.** task180 v3 and task181 are consecutive draws in adjacent client domains (pharmacovigilance, then epidemiology). Both are anomaly detection, and both pick one of several health signals for a deciding body. The drivers differ (see Notes for the author).

## What to redraw
1. **Batch level, not task181.** The certified-record decoy (`validated_decoy`) is at 7 of 12 against a cap of 3. It is carried by task121, task122, task124, task125, task126, task127 and task129. Of these, task124, task126 and task129 are not recorded as retired.
2. **task181, Idiom, one file name in the generator (no figure moves).** The run report's name, `pertussis_extract_run_20261005.txt`, returns to the corpus's `extract` provenance stem.

There is no Track A or Track B redraw for task181.

**Cost, from the stage 3 and 4 rules.**
- A rename under `target/` means a rebuild through the stage 3 gates (it also regenerates `metadata.json`), then `leak.py`.
- The leak reader then reads again, because a document under `target/` has changed since its last read.

**Notes for the author.** None of these is a finding and none is a redraw.
- **task180, one back, is now on architecture 3.**
  - **Shared with task181:**
    - the objective;
    - the decision type (pick one, a named option);
    - the evidence-first opening label;
    - a health-surveillance setting in an adjacent client domain.
  - **The drivers differ.**
    - task180: patients are chosen for a treatment because of a trait that carries the outcome, and only a within-person comparison gets past it.
    - task181: counts are still arriving at different speeds by route, and only a route-specific nowcast gets past it.
  - On the outline it shares one of four axes, the decision type, so it is not Shape echo. A reviewer holding both would still read two "which signal is real" health tasks in a row.
  - Expect `repeat.decision` and `repeat.opening` WARNs when task181's heart is re-run against the v3 card.
- **The design note's similarity claim** describes task180's decisive step as "a gas source attribution". That was task180's spent architecture 2.
  - The note says differentiation lines are written at stage 5.
  - No guard rule requires one: there is no structural match, and the guard's driver similarity peaks at 0.082 against its 0.12 WARN line.
- **Card prose.** On task181's card, `driver_concrete` and `stump` still count onsets, and say about a quarter of Griffith's cases are notified within 14 days.
  - The shipped build counts specimens collected, and Inland Pathology notifies 76 per cent within 14 days.
  - `spine.rows` reads 0, while the line list ships 1,118 rows.
  - The abstract `driver` and the 13 fields the screen reads are unaffected. Stage 8 updates the card.

**Coverage and tooling notes.** None of these is a finding against any build.
- **(a) Card-only builds.** The extract fingerprints only folders that hold a `prompt.md`. So task114 to task116, task180 and task228 never reach the screen. The `task180.json` in this worktree is task180's spent architecture 2.
- **(b) Draw order.** The screen's consecutive routes compare task numbers, while the guard orders by drawn date and then number. So a later re-root of a lower number (task180 v3, at 10:14) still sorts before task181, and its own check never meets task181. The routes were applied by hand here.
- **(c) Strategy field.** The screen's Track B does not read `stump_strategy`. Builds that share a strategy family are reached only by a reader: here, the four `maturity_censoring` cards.
- **(d) task99.** The screen excludes it as scratch, while the guard counts its card as a build.
- **(e) Unprofiled packs.** task117 to task129 and task229 have no profiled pack on this checkout, so file-level hard tells cannot reach the builds drawn just before task181. Their metadata and zip listings were checked instead.
- **(f) Status regex.** It reads fiction text as delivery status (task48, task72).
- **(g) Ask parser.** No sentence of task181's prompt opens with the parser's verbs, so its parsed Main Ask is empty. The ask comparison ran on sentence openings only.

**Process notes.**
- **Governing files.** `clone-auditor.md` and `clone-check/SKILL.md` were read in full at the start. Both are unchanged since 02:40 (checked again before writing), so the tiers above come from the current files.
  - The `clone-check` skill is not in this session's skill list, so its SKILL.md was read from disk.
- **Adjudication.** No Agent tool was available, and no pair was promoted, so nothing was adjudicated. The card-level readings were done in this thread.
- **task180.** Its v3 material was read through git refs from this worktree. Temporary copies went to the session scratchpad only. Outside this worktree, one read-only `git status` of task180's worktree was run, and nothing there was opened or changed.
- **Answer keys.** No golden file of any build was opened. From task181's pack, I read the run report and the head of the line-list notes, for the file-role comparison.
- **Writes.** Only this report. The screen's cache was refreshed by `fingerprint.py extract`.
  - `.claude/skills/fingerprint/.cache/people.json` was not touched (mtime 10:01:05 before and after).
  - No commit and no push.
