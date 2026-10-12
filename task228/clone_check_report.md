# Clone check: pre-flight, task228 against the whole corpus, 2026-10-11

## Verdict
The worst tier touching task228 is a Shape echo, a soft flag on Track A only, against task131. task131 is the build drawn immediately before task228. Its prompt makes the same decision cut and ends on the same two-sentence close.
- There is no Exact, Same seed, Dataset or Template finding against any build, task229 included. The clone condition of the stage-5 gate holds.
- Separately, at batch level, the certified-record decoy carries 7 of the last 12 builds against a cap of 3. That is a Strategy monoculture finding, and task228 is not one of the seven.

## Scope and coverage
- **Mode and scope.** Pre-flight on task228 against every build on file, with no window.
  - That means the 123 builds the screen can see (task3 to task131, less gaps), plus four builds that exist only as fingerprint cards: task114, task115, task116 and task229.
  - task132 onward are seed folders with no prompt, so the extract skips them.
  - task229's folder here holds only its seed. Its card is the only record of it in this worktree. /home/user/b229 was not read.
- **Extract.** The committed cache predated this build: it had no task228 fingerprint, and task228's submission changed (02:35) after the cache was last written (02:33). So I re-ran `fingerprint.py extract` in place.
  - Result: 126 cards, 124 with a prompt or target.
  - task228 was added.
  - task130 was re-fingerprinted from its committed copy on disk: 14 target files on disk against 13 in the cache.
  - task117 to task131 otherwise matched the cache.
  - Builds up to task116 are carried over from other checkouts and cannot be checked for staleness here.
- **Screen.** `fingerprint.py screen --focus task228` covered 124 builds and 123 pairs, and promoted 0.
- **Supplementary runs.** All were scripted with fingerprint.py's own functions and wrote only to the scratchpad. Nothing in the repo was written except the cache refresh above.
  - The screen's mechanism promotion rules, re-applied in draw order.
  - Track B for the four card-only builds.
  - task117 and task119 fingerprinted from their `target.zip` in a scratch copy of the cache.
  - A vocabulary sweep for task228's move over 799 texts: every card driver, concrete driver and stump, every lineage entry and every ledger row.
- **Draw order.** The screen measures "consecutive" by task-number distance, and the numbering jumps from task131 to task228.
  - In the guard's draw order (drawn date, then number), the builds either side of task228 are task131 (before) and task229 (after, drawn the same day).
  - The screen's own rules, applied in that order, promote one pair: task131, on "two of three mechanism axes collide between consecutive builds".
- **Builds compared: 127.**
  - 123 went through the screen. 101 of them were scored on both tracks, with Track B read from the cards (none fell back to the ledger).
  - 22 were scored on Track A only: task3 to task10, task13 to task24, task112 and task113.
  - 4 were scored on Track B only: the card-only builds.
  - Nothing comparable exists for task1 and task2 (no prompt, no target, no mechanism layer) or for task99 (a scratch slot, which the script excludes).
  - 34 of the screened builds carry back-fitted labels (task36 or earlier), and 14 of those were scored on Track B.
  - Mechanism layer over the 124 screened builds, task228 included: 102 have a card, 5 are note-only and 17 are unavailable.
- **File-level gaps.** The extract profiles csv, tsv, txt and xlsx files only and never opens `target.zip`.
  - 15 screened builds had no profiled target files: task3, task10 and task117 to task129.
  - task117 and task119 ship a zip, so I covered them from it. Against task228 they show no identical file, no same-seed table, no column-set collision and no shared name (surfaces 0.085 and 0.080). The screen's result did not change.
  - task118 and task120 to task129 have no pack on this checkout, so file-level Track A against them was not checked.
  - task228's two parquet spine files and its JSON, DOCX and MD files are fingerprinted by byte hash only.
  - No card on file shares the spine's entity and grain (experiment x check night x check).
- **Pairs promoted and read.**
  - 0 were promoted by the screen and 1 by the auditor (task131, in draw order).
  - Two pairs were adjudicated. task131 was read in full: cards, prompts, submissions, design notes from the DRAW block through the ladder, and target listings. task229 was read from its card alone, because its prompt, write-up, design note and pack are not in this worktree.
  - 26 more builds had their card driver or matched ledger passage read to name the difference:
    - 17 nearest on mechanism or status: task11, task12, task34, task43, task48, task53, task56, task68, task72, task74, task83, task93, task102, task111, task116, task121 and task122.
    - 9 surfaced by the sweep: task5, task16, task30, task49, task57, task60, task89, task96 and task119.
  - The other 99 pairs were left unread, because neither route promoted them and the sweep found nothing in them.
- **How the reading was done.** The invoking command forbade the Agent tool, so there were no subagents and I adjudicated in this thread.
  - No golden file was opened.
  - The clone-check skill was loaded by reading its SKILL.md in full, because the Skill tool does not list it in this session.
- **Status.** The ledger runs to task108. task109 onward have no row, so task228, task229 and task131 are unknown on the record.
  - The ledger records eight builds as approved: task25, task27, task28, task29, task30, task33, task34 and task35.
  - The screen also labels task48 and task72 "delivered or approved", which their own status cells do not say (see the next section).
- **Concurrency.** The parent build wrote `task228/pipeline.json`, `task228/leak_check_report.md` and `task228/solver_rounds/` during this run. Nothing the fingerprint reads changed after the extract:
  - prompt 02:27, target 02:31, design note 02:33, submission 02:35
  - cards 02:29 (task228) and 01:58 (task229)
  - extract 02:40.

## In batch against earlier builds
Pre-flight has no batch, so this section carries the comparison the reviewer's cross-batch check runs: task228 against builds the ledger records as delivered or approved.
- **No hit against an approved or delivered build.**
  - None of the eight approved builds is promoted against task228, and none shows a hard tell.
  - The nearest is task30, at surface 0.085 (78th percentile).
  - None shares more than one of the three mechanism axes. Six share only the decision type (task25, task27, task28, task29, task30 and task33). task34 shares the decisive gap, plus the calibration organ, which is not one of the three. task35 shares none.
- **Two builds are mislabelled by the screen.** task48 (0.094, 94th percentile, among task228's nearest neighbours) and task72 are labelled delivered or approved, but their status cells say otherwise.
  - task48's cell records that its first round "SOLVED EXACTLY AND THE AUTHOR REJECTED THE BUILD".
  - task72's cell records that it was "RE-ROOTED to v2 ... after two live rounds".
  - Neither is delivered on the record.
  - task48 shares a flat layout, a format mix, the decisive gap and the monitoring_export context type. Its driver is a population invisible at the monitor's reporting grain, recovered at a two-sided pair grain, which is not task228's move.
  - task72 is covered in the Clean section.
- **No exclusion-level exposure for task228.**

## Track A findings, reviewer visible

### task131 against task228: Shape echo, a soft flag, Track A only
- **Status.** Neither build has a ledger row, so both are unknown on the record. task131 was drawn 2026-10-10 and task228 2026-10-11, back to back in draw order.
- **Shared surface.**
  1. **The decision cut.** Both commit one named option of N for 2027 with a figure attached: the offer and its programme value in task131, the check and its setting in task228. Both then ask for the runner-up and its margin:
     - task131: "Then name the runner-up and how far behind the pick it sits per card-week"
     - task228: "Then the check that comes second and how many fewer defects it catches"

     The guard's repeat.decision WARN caught the decision type, and the design note answered it on decision grounds. The prompt wording still carries the repeat.
  2. **The ask construction.**
     - task131: "So what I need is the offer that goes on every card in 2027 and its 2027 programme value"
     - task228: "The call I need is which check the alert pages on through the 2027 peak, and at which of the alert service's settings"
  3. **The close.** No other prompt on file ends this way: a named colleague expects the candidate that moves most, with the reason in a because or since clause, then a bare role line.
     - task131: "Hansjürg's team expects the monthly target voucher to win, because it moved more spend than any other offer in the test. I run the member programme."
     - task228: "Isabela on the desk expects the events-per-user check, since it jumps hardest when logging breaks. I lead the experimentation platform."
  4. **The chart ask.** Both mark the pick ("the recommended offer's column outlined and the runner-up marked" against "the chosen check marked"), and both want a title that states the call.
- **What differs.**
  - The prompt shape: 07, a grid, against 04, a dial.
  - The opening move: question-first against stakes-first.
  - The deliverable species: docx+png against json+xlsx+png.
  - The calibration organ: none against the replay audit.
  - The domain, the world and the driver (see Clean).

  That is two of the four Shape echo axes (the ask construction and the decision shape), plus a close unique to the pair. It is a soft flag, not an exclusion, and under the build-pipeline's stage-5 gate it is reported to the author, not looped on.
- **Why the screen did not raise it.**
  - The masked surface score is 0.095, the 95th percentile. Consecutive promotion needs the 97th, and the screen did not count the pair as consecutive.
  - Masked prompt overlap and ask skeleton both score 0.000. The colleague's name and the role nouns change the masked sentence openings, so the shared close only shows on reading.
- **The one axis to redraw.** task228's prompt close: the stakeholder-belief sentence and the role line that ends the prompt.
  - It is a rewording, not a rebuild. The data, the ladder and the golden survive.
  - A changed prompt brings the stage-4 leak reader back under that stage's own rule.

### Not findings, checked
- **Hard tells.** Across the 123 screened builds there are no byte-identical files, no same-seed tables, no identical column sets and no shared invented names.
  - Pousalto and Vigia appear on no other card.
  - The highest masked prompt overlap is 0.006 (task122). The highest masked write-up overlap is 0.002 (task120).
- **A shared surname, not reviewer-visible.** task228's persona Isabela Pires shares a surname with task121's Raquel Pires, and task121 sits inside the last twelve draws.
  - "Pires" appears only in task228's `DESIGN_NOTE.md` and `generator/world.py`. It is not in the prompt, the write-up or the pack, so a reviewer cannot see it.
  - On the card, it is the overlap the guard's `people.last` rule is written against.
  - The stage-5 heart run could not see it, because the people index on this checkout records task121 with no personas (see the tooling notes).
- **File roles.** task228 avoids the habit file names. Its dictionary role is `vigia_export_fields.md` and its provenance role is `export_notes_2026-10-05.txt`.
- **`voice-check.py`**, run bare and on task228, over task121 to task131 and task228:
  - task228's stakes-first opening is the only one in the 12.
  - The regex finds no listed carrier and no unlisted repeated runs. The carriers it misses are under Corpus habits.
  - task228 runs 298 words, against a median of 260 and a flag line of 330.
  - It ships three files, at the ceiling with task123 and task127.
  - Its JSON deliverable is the only one in the 12.

## Track B findings, mechanism
None. With no Template finding against any build, no rebuild is owed and the data stands.
- **The mechanism screen.** Across the 127 builds compared, task228 shares:
  - the decisive gap (population) with 42
  - the decisive G-code (G13, horizon mismatch) with 2 (task102 and task122)
  - the decision type with 20
  - the Gate G mechanism with 1 (task229)
  - the calibration form with 5
  - the context-artifact type with 27
  - the same-driver signature (gap, pattern and Gate G together) with none
  - the domain and objective pairing with none.

  The most mechanism axes any pair collides on is two: task11, task12, task53, task68, task72, task121, task122 and task131. The highest card-driver overlap is 0.076 (task47), against a promotion line of 0.40.
- **The two adjudicated pairs.**
  - task131, promoted in draw order, comes out `clean_shares_components` (see Clean).
  - task229, the next draw, collides on one of the three axes (the decisive gap), is promoted on no route, and also comes out `clean_shares_components`.
- **The reskin route.** task228's move, with the domain nouns stripped: a per-run false-alarm budget over repeated looks, held on runs of the forward length, because a run's chance of a false page grows with the number of looks, fastest where the noise tail is heavy.
  - No driver, lineage driver, stump or ledger row on file turns on it.
  - The sweep's four vocabulary families were repeated looks, the false-alarm budget, run length and the heavy tail. No text carries more than two of them. The one text that carries two (task89's retired 911 lineage) does so through the incidental words "looks full" and "bursts".
  - The guard put the nearest driver at 0.07: task60 v1's lineage, an agreement run length recovered from settlements, which is a different quantity.
- **The shared G13 is a label, not a driver.** Each build turns on a different horizon:
  - task122: a session close that truncates outcomes landing later.
  - task102: a forward period that ends on a weekend, moving payments into the next period.
  - task228: the run length the forward season books.

## Clean, shares components by design

### task229
In build in parallel, drawn after task228 on 2026-10-11, no ledger row. Read from its card only; Track A cannot be checked here.
- **Shared components:**
  - the objective (data-quality-monitoring)
  - the decisive gap, population, with time second
  - the Gate G mechanism `signal_vs_noise_or_hold`; these are the only two cards on file that carry it
  - the context-artifact type `monitoring_export`
  - G17 statistical rigour as a non-decisive generator (second of three in task228, third of three in task229)
  - an alert configuration committed as a JSON file.
- **Driver difference.**
  - task229 turns on the unit of aggregation and its error: an average of per-entity shares over the entities present all window, with a between-entity error, against a record-pooled ratio that high-volume entities dominate.
  - task228 turns on the population a per-run false-alarm budget is held on: runs of the forward length, against the historical mix of run lengths.
- **Position.** The noise term sits inside task229's decisive rung, because the between-entity error decides which groups breach. In task228 the noise budget is the frame the standard states, which the competent solver already holds at rung 1. The decisive rung is which runs it is held on.
- **Other differences:**
  - the decisive pattern (D, two grains, against G13)
  - the decision (a designation set against one pick with a setting)
  - the shape (10 against 04)
  - the calibration organ (none against the audit)
  - the strategy (grain_or_unit against population_selection).
- **For task229, not task228.** The shared context-artifact type is an axis that Part 6.1 bans across the last three draws. The guard applies that ban to the later draw, task229, so it belongs in task229's own heart check and pre-flight.

### task131, on the mechanism
Its Track A echo is reported above.
- **Shared components:**
  - the decisive gap (population)
  - pick one of N
  - the form of the final rung: re-estimate on a subset fixed by a property of a group. In task131 the subset is memberships whose cards all drew one arm; in task228 it is runs booked for 28 nights.
- **Driver difference.**
  - task131's subset answers interference: sibling sub-units share one budget, so lift moved between them nets to zero at full rollout.
  - task228's subset answers repeated-look multiplicity: a sound run's chance of a false page grows with its nights, fastest for the heavy-tailed check.

  A solver primed on one is not primed for the other.
- **Ladder.** Both kill rung 0 with the filed standard's own definition: net margin after reward cost in task131, the audit's verdicts over the tracker in task228. That is ordinary ladder furniture.

### task122
The ledger is silent, so status is unknown.
- **Shared components:** the decisive G13, pick one of N, a product-analytics experimentation world with guardrail vocabulary, and a role line ending the prompt.
- **Driver difference.** task122 turns on outcomes that a session-closed log credits to the wrong exposure. task228 turns on the run length a forward season books.
- **Other differences:** the strategy, the Gate G mechanism, the calibration organ, the shape (07 against 04) and the deliverables (ipynb+png against json+xlsx+png).

### task83
Ledger: live. This is the nearest abstract kin on file: the population a figure is measured on is mixed differently from the population the decision faces.
- **Shared components:** the decisive gap, an experimentation world and `monitoring_export`.
- **Driver difference.**
  - task83 is effect heterogeneity under a composition shift. It conditions a randomised effect on each unit's prior treatment history and reweights to the target pool.
  - task228 is multiplicity under a change in exposure. It recalibrates a threshold on forward-length runs, because a per-run false-alarm probability scales with the number of looks and with the noise tail.

### Two of the three mechanism axes, distant
These builds share the decisive gap (population) and pick one of N with task228. None of their drivers is task228's.
- task72 (re-rooted to v2, live on the record): books movement to the owner whose agreement covered each piece of service.
- task68 (live): a matched panel across identity successions. Its naive path already applies a multiplicity-corrected bar, so multiplicity sits below the decisive rung there, as it does in task228.
- task53 (live): pools eligible volume per account against a scale break.
- task11 (status unknown): a threshold-triggered rebate on a rebuilt ledger.
- task12 (status unknown): an arm-correlated population recovered by anti-join.
- task121 (status unknown): newcomers who belong to established accounts.

### The calibration organ: a verified subsample or audit drill
task34 (approved), task43, task74 and task93 (live), and task111 (status unknown).
- None of them sits within three draws of task228, so Part 6.1's calibration ban does not reach them.
- In task228 the audit labels sound and defective, and both rung 1 and the answer read it, so the organ is off the decisive rung.
- task34, the approved one, turns on a subpopulation that only a within-cluster fit can enumerate.
- task111 turns on which cause still operates in the forward window.

## Strategy monoculture
The batch is the last 12 builds in draw order ending at task228: task119, task121, task122, task124, task125, task126, task127, task128, task129, task130, task131 and task228. The counts are read from the cards' fields.

| Measure | Count | Cap | Verdict |
|---|---|---|---|
| Withheld rule with an official decoy | 0 of 12 | 2 | under |
| Certified-record decoy (`validated_decoy`) | **7 of 12** | 3 | **over: Strategy monoculture finding** |
| Any one `stump_strategy` | at most 2 of 12 (decomposition_attribution, identity_resolution, causal_design, binding_constraint) | 4 (a third) | under |

- **The seven builds carrying the certified-record decoy:** task121, task122, task124, task125, task126, task127 and task129. Swapping in task229, the parallel draw, for task119 leaves every count the same.
- **task228.** Its strategy is population_selection, with the decisive rule filed, no official decoy and no validated decoy. It is the only population_selection in the 12 and adds to neither capped count.
- **The card field against the design note.** task228's `validated_decoy: false` agrees with its design note: rung 1 reproduces no closed, published or certified figure, because the audit labels outcomes, not settings.
- **The forward-window frame.** The stump still turns on a condition that exists only in the forward window: every 2027 peak test books 28 nights. That frame, where the closed record holds and the forward window breaks it, also runs through task47, task83, task95, task107, task111 and the seven builds above. It is not counted, because the card field is the record. A reviewer reading the batch together will see it recur.

## Corpus habits
- **File roles.** task228 carries none of these.
  - `data_dictionary`: 61 builds
  - `export_manifest`: 33
  - `data_notes` and `provenance`: 12 each
  - `county_reference`: 4
  - `product_catalog`, `accounts`, `plan_catalog`, `metric_definitions`, `item_master`, `facility_register`, `site_master` and `sources_and_licences`: 3 each
- **Deliverable pairings.** task228's json+xlsx is not among them.
  - pdf+csv: 9 builds
  - py alone: 8
  - py+pdf: 7
  - pdf+png: 6
  - py+csv, py+xlsx and pdf+xlsx: 5 each
  - docx alone: 4
- **Ask opening.** "give me the single dollar figure we" appears in 2 builds, neither of them task228.
- **Prompt constructions in the last 12 (task121 to task131 and task228)** that voice-check's regexes do not catch. task228 carries every one of them.
  - **The chart's title requirement closes the list of chart parts in 10 of the 12.** The exceptions are task126, which asks for no title, and task131, which gives the title its own sentence. Four use the carrier "and a title that ...": task124, task129, task130 and task228 ("and a title that says the call"). This is prompt-voice.md's calcified "and a title that states ..." with the verb changed, and prompt-voice.md asks for the title requirement to come first.
  - **A named colleague's belief about the naive pick, in 6 of 12:** task121, task124, task125, task128, task131 and task228. "expects" carries it in task125, task131 and task228, and "is sure" in task121 and task124. prompt-voice.md keeps the belief (at most one, as one clause) and asks for its carrier to vary.
  - **A prompt that ends on a bare role line, in 3 of 12:** task122, task131 and task228. Corpus-wide it is 4 of the 111 prompts on file, adding task104. The role may sit last, but three of the last twelve is a habit forming.
  - **"What I need is" or "the call I need is" framing the ask, in 3 of 12:** task123, task131 and task228. Corpus-wide it also frames task103 ("the one figure I need is") and task118 ("the call is").
  - **The pick marked on the chart, in 5 of 12:** task121, task122, task129, task131 and task228.
  - **The runner-up asked for beside the pick, in 3 of 12:** task129, task131 and task228.
- **Mechanism idiom.** Population is task228's decisive gap and the most common decisive gap on file: 42 of the 127 builds compared share it. The forward-window frame is covered under Strategy monoculture.

## What to redraw
1. **task229** (for its own pre-flight, not task228's): the context-artifact type. Its `monitoring_export` repeats task228's, and that is a Part 6.1 axis ban the guard applies to the later draw. This is a guard ban, not a clone tier.
2. **task228:** the prompt's close. The stakeholder belief carried by "expects ..., since it ..." and the closing role line are the skeleton task131 also ends on. This is a Shape echo soft flag and needs a rewording only.
3. **Batch, not task228:** the certified-record decoy axis (`validated_decoy`), at 7 of 12 against a cap of 3, carried by task121, task122, task124, task125, task126, task127 and task129.

## Tooling notes, not findings
- **"Consecutive" uses task numbers.** fingerprint.py's `consecutive` and `adjacent` tests measure task-number distance. task131 therefore counts as 97 builds from task228, although it is the draw immediately before it. The guard orders by drawn date, then number.
- **The status parser matches "delivered" anywhere in a status cell.** `STATUS_RANKS` labelled two builds delivered or approved from ordinary prose:
  - task48: "one group-by delivered the conclusion"
  - task72: "service delivered under a grantee's agreements"
- **The extract never opens `target.zip` and does not profile parquet.** On this checkout, 13 screened builds have no file-level fingerprint, and parquet spines are covered by byte hash only.
- **Card-only builds never enter the screen.** task114, task115, task116 and task229 were scored here from their cards with fingerprint.py's own `track_b`.
- **The people index drops carried names.** `business.build_index` rescans every task folder on disk, and an empty scan overrides names carried from another checkout. task117 to task129 therefore index with no personas here, and the stage-5 heart check cannot see persona overlaps with them.
- **task228's card has stale fields.**
  - It still lists `alert_replay.py` as a deliverable and a single 65,100-row spine file.
  - The prompt commissions `alert_replay_fy2026.xlsx`, and the pack ships two half-year parquet files (126,685 rows).
  - The ship stage's card update covers this. The screen reads deliverables from the prompt, so no comparison here was affected.
- **The cache is modified and uncommitted.** `.claude/skills/clone-check/.cache/fingerprints.json` is tracked and now shows as modified in the working tree: task228 was added and task130 refreshed. Nothing was committed or pushed.
