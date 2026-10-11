# Clone check: pre-flight, task180 (architecture 3) against the whole corpus, 2026-10-11

## Verdict
CLEAN for task180: no Exact, Same seed, Dataset or Template finding and no Shape echo on either track. The worst tier touching task180 is Idiom (two corpus habits, below, one of them a pack recipe shared with the same author's in-flight task181 and task182). The draw-order twelve ending at task180 carries a Strategy monoculture (the certified-record decoy, 4 of 12) that task180 does not add to.

**Stage 5 gate (`build-pipeline`).**
- **The adjudicated half holds.** There is no Exact, Same seed, Dataset or Template finding.
- **The mechanical half does not hold as the gate is written.** `guard.py heart task180` returns BLOCK today on `ban.pattern` (decisive G-code G17, against task135). The card carries that block under the author's `--force` override.
- This check finds no shared driver behind the G17 collision (task135, below), so it gives no reason to redraw. Whether the registration override also carries the stage 5 heart gate is the author's decision, not this report's.
- The Idiom and Strategy monoculture findings go to the author and are not looped on.

**The override, as found.** The card's `notes` record a `--force` registration over `ban.pattern` (G17) against task135, on the author's explicit instruction. I checked each claim in the notes against the repo:

| Claim in the notes | What the repo shows |
|---|---|
| This card was registered at 10:14, task135's at 10:46 | 1e53a54 registered the architecture 3 card at 10:14:23 UTC on this branch. task135's card is f8b68ba (10:46:55), merged to main by PR #24 at 10:47:08. |
| task135 sorts before task180 | The guard orders cards by draw date, then task number. Both were drawn 2026-10-11, so task133, task134 and task135 are task180's three predecessors. |
| Neither card was on main for the other's guard | 1e53a54 does not contain f8b68ba. task180's card has never been on origin/main. |
| G16, the only other honest label, is banned by task134 | Confirmed on a scratch copy of the card. With G16 decisive the guard blocks on `ban.pattern` and `test.same_driver` against task134, and on `test.same_driver_older` against task104 and task70 (v2). G16 carries more blocks than G17, not fewer. |
| This is the slot's third and last architecture | The card's slot note and the design note say so, and `build-pipeline` retires a number after three. |
| Moving the forum to `committee_or_panel` clears the forum block | Confirmed. The card with the old `regulator_or_inspector` adds `ban.forum` against task135; as filed it does not. The prompt's medicines safety committee is the deciding body, so the new key is the accurate one. |
| Domain, objective, decision type, shape, gap and driver all differ from task135 | Confirmed. The decisive gaps differ (population against objective); both carry time second. |
| The heart's nearest driver on file is 0.04 | Confirmed as the heart's nearest text (0.04, task119's stump). The driver-only nearest is 0.07 (task41's lineage), the figure the design note's DRAW block gives. |
| The AskUserQuestion answer | Not verifiable from the repo. 83eaddc's commit message records the re-registration. |

**One thing the notes do not cover.** task134's own branch (a2d385a, 12:21, not yet on main) has re-keyed that card's forcing event to `vote_or_meeting`. With that card on file the heart adds a second BLOCK, `ban.forcing_event` against task134. I checked this on a scratch copy of the cards. See What to redraw.

## Scope and coverage

**Mode and scope.**
- This is a pre-flight on task180, architecture 3: a national medicines agency chooses which of three spontaneous-report signals the registries support, and the decisive move is a self-controlled comparison under channelling. It was compared against every other build with the window ignored, and the screen reports "all builds".
- Architectures 1 and 2 appear only in the card's lineage. They are not comparison partners, because a build cannot clone its own ancestor. Their reports stay at `clone_check_report_arch1.md` and `clone_check_report_arch2.md`, untouched.
- This is architecture 3, pass 1. It is written to `task180/clone_check_report.md`, the path the invoking stage named and the place `build-pipeline` keeps a build's reports. Nothing existed at that path.

**Version checked.**
- HEAD is 83eaddc. Times on this checkout:

  | Item | Time | Commit |
  |---|---|---|
  | Prompt | 10:14 | 1e53a54 |
  | Pack (12 files) | 14:22, rebuilt 15:36 | not tracked |
  | Goldens | 14:23, rebuilt 15:37 | not tracked |
  | Metadata | 14:23, rewritten 15:37 | 5660821, now modified and uncommitted |
  | Submission | 14:33 | 5660821 |
  | Card | 15:09 | 83eaddc |
  | Design note | 15:10 | 83eaddc |

- **A concurrent rebuild landed during the run.** Another session edited the generator (`docs.py` and `records.py`, 15:31, uncommitted) and rebuilt the pack (15:36), the goldens and the metadata (15:37), after my first extract at 15:15.
  - The rebuild changes two pack files. `atc_ddd_index_2026.csv` loses its remarks column, which carried the note on the code reassignment. `pv_signal_screen_2026Q3.xlsx` changes its cumulative counts for the two validated signals.
  - The card, prompt, submission and design note are unchanged, and so is the driver.
  - I re-extracted at 15:38 and re-ran both screens on the rebuilt pack. The results are identical: the same promoted pair at the same score, and the same neighbours. This check therefore stands for the rebuilt pack.
- **Card fields still out of step with the build**, as expected before stage 8:
  - `deliverables` and `answer_source` name `signal_estimates.csv`, where the prompt asks for `new_users_by_year.csv`;
  - `spine.rows` is 0, where the metadata gives 2,667,469;
  - `world.invented_names` is empty, while the design note lists six invented product and substance names.

  The screen reads the prompt and the pack directly, so Track A is unaffected. The guard's deliverable-set and invented-name rules read the card.

**Extract and screen.**
- **Cache.** `.claude/skills/clone-check/.cache/fingerprints.json` (13:32) predated task180's architecture 3 pack, submission, card and design note, and held no task180 entry, so it was stale.
  - I re-extracted it in place at 15:15, and again at 15:38 after the concurrent rebuild (129 cards each time). The refreshed cache is left uncommitted in the working tree.
  - The extract reads `DESIGN_NOTE.md` (architecture 3). `DESIGN_NOTE_arch2.md` does not enter the fingerprint.
- **task181 and task182.** They are the same author's in-flight builds, and their folders on this checkout hold only the seed.
  - I fingerprinted them from their worktrees with `fingerprint.py extract --repo`: `/home/user/wt-181` at d6944e3, and `/home/user/wt-182` at b0771b7 plus its uncommitted build.
  - They went into a scratch copy of the cache only. The repo cache does not carry them.
  - The extract read the untracked card copies in `cards/`, which are byte-identical to the cards in the worktrees.
- **The two screens.**
  - On the repo cache: 127 builds, 126 pairs with task180, 0 promoted.
  - On the scratch cache: 129 builds, 128 pairs, 1 promoted (task182). This report uses the scratch screen.
- **Surface baseline (scratch).** 8,256 pairs, mean 0.070, 97th percentile 0.098, 99th percentile 0.104. task180's highest pair is task182 at 0.100, the 97.8th percentile.
- **Card-only builds the screen drops.** task114, task115, task116, task134, task135 and task228 have no prompt and no pack on this checkout. I scored them on Track B, read-only, with the screen's own `track_b_cards` and its promotion rules.
- **Beyond this checkout.** I listed every origin branch and read cards and partner files from them read-only. `git fetch` went into FETCH_HEAD only, so no refs were created.
  - One build is not in the corpus here: task230 (`perssathya/task230-event-volume-drop`, drawn 2026-10-11, card only on its branch).
  - Two cards are newer on their own branches. task134's (a2d385a) changes the context artifact, the forcing event and the driver wording. task228's (46d53b2) is re-rooted to architecture 2, with every mechanism field changed.
  - I scored task230 and both newer cards the same way. I also ran them through `guard.py`, with `FINGERPRINT_CARDS` pointed at a scratch card folder.
  - Every other branch carries only older versions of cards already here.
- **Exclusions.** task99 is excluded as the scratch slot, which is correct. task1 and task2 have no pack, no prompt and no mechanism.

**Which builds count as consecutive.**
- **The screen counts by number.** task180's numeric neighbours task178 and task179 have no build. task181 (adjacent) and task182 (two apart) are covered by the scratch screen.
- **The guard counts by draw order.** Same-day draws sort by number:
  - task133, task134 and task135 come before task180;
  - task181, task182, task228, task229 and task230 come after it.
- I applied the screen's consecutive-only routes in both orders.

**Pairs promoted, and why: 8, all adjudicated.**

| Partner | Route |
|---|---|
| task182 | **The screen.** Surface in the top 3 per cent of consecutive builds, two apart. Under the G16 key, the decisive pattern also repeats two apart. |
| task135 | **The screen's own rule, applied in draw order.** The decisive pattern (G17) repeats from the immediately previous build. This is the heart's BLOCK. |
| task134 | **Under the G16 key**, the card notes' only other honest label: gap, pattern and Gate G mechanism all collide (the same-driver signature), two back in draw order. As filed, it is the guard's `repeat.gate_g` WARN. |
| task104, task70 (v2) | **Under the G16 key**: the same-driver signature, against older builds. |
| task68 | **Under the G6 key** (composition shift, which task68 and task230 both file for a comparison-group move): gap, pattern and decision type all collide. As filed: two core axes plus the context artifact. The design note names it as this lane's nearest build. |
| task131 | **Delivered on its own record** (the ledger is silent). As filed it carries two core axes (population gap, pick one), the same stump strategy and Gate G mechanism, and the highest driver overlap on file (0.111, against a 0.40 route). |
| task230 | **Outside this checkout's corpus.** As filed it shares the stump strategy, Gate G mechanism, decisive gap, context artifact and Layer 2 family; under the G6 key, the same-driver signature. Drawn the same day by another author, and neither build's guard has seen the other. |

- **Track B as filed, on the cards.**

  | Shared with task180 | Partners |
  |---|---|
  | Decisive gap `population` | 45 |
  | Context artifact `monitoring_export` | 27 |
  | Decision type `pick_one_of_n` | 22 |
  | Decisive pattern (G17) | 1 (task135) |

  - 8 pairs carry two core axes and none carries three: task131, task121, task72, task12, task68, task11, task53 and task228.
  - task228 counts here only on this checkout's v1 card. Its branch's v2 card shares no core axis.
  - None of the eight is consecutive, in either order.
- **Pairs left unread: 127 of the 134 comparisons on this checkout.** No route promoted any of them, either as filed or under either probe key.
  - The nearest unread on surface is task181. It sits at the 93.7th percentile, from flat layout and format overlap plus 0.003 of masked prompt wording. Of the core axes it shares only the decision type (it also shares the anomaly-detection objective), and its driver overlap is 0.042.
  - After it come task52, task60, task84, task93 and task124, at the 92nd to 93rd percentile, from layout and format only.

**How the reading was done.**
- **No subagents.** No subagent tool exists in this session, so I adjudicated all eight pairs myself, in sequence, each from its own evidence. Each one followed the clone-auditor's steps:
  1. each side's decisive move, with the domain nouns stripped;
  2. the ordered path, and the position of the shared moves;
  3. then the verdict, tier, track and axis.
- **The skill.** The `clone-check` skill is not registered in this session's skill list (the Skill call returned "Unknown skill"). The tiers and the discrimination come from `.claude/skills/clone-check/SKILL.md`, read in full at the start of this run.
- **Tools and network.** No server-side tool was called. Network use was limited to listing origin branches and fetching them into FETCH_HEAD to read partner files.
- **Answer keys.** No partner's golden or answer key was opened.
- **Evidence per partner:**

  | Partner | What was read |
  |---|---|
  | task182 | Card, prompt, submission (uncommitted), and the design note's draw, three rules, Gate G, stump and ladder sections. Pack listing. Read in `/home/user/wt-182`. |
  | task135 | Card (this checkout's, and its branch's at 2f511af; no mechanism field differs), prompt, submission, and the design note's draw, Gate G, three rules, stump and ladder sections. Pack listing. Read from its branch. |
  | task134 | Card (this checkout's, and its branch's at a2d385a), prompt, submission, and the design note's draw, Gate G, three rules, stump and ladder sections. Pack listing. Read from its branch. |
  | task230 | Card, prompt, submission, and the design note's draw, stump, two layers and ladder sections, from its branch at 7941b35. Its pack is not tracked. |
  | task131 | Card, prompt, and the design note's stump, decisive move and ladder sections. Pack listing. On this checkout. |
  | task68, task70, task104 | Card, ledger rows, and the cached prompt profile, submission and pack listing. Their folders live on another checkout (`/Users/saa/...`), so **their design notes and full prompts were not read**. |
  | task180 | Card, design note, prompt, submission, metadata and pack listing, in full. |

**Guard.**
- **Heart on this checkout's cards.** I ran `guard.py heart task180` directly. Its people index (14:49:40) is newer than every task folder, so it rewrote nothing; I checked the sha1 before and after.
  - BLOCK `ban.pattern` (G17, against task135).
  - WARN `overuse.org_family` (government_agency, in 22 builds).
  - WARN `repeat.gate_g` (against task134).
  - The nearest heart text is 0.04 (task119's stump) and the nearest driver 0.07 (task41's lineage). The BLOCK threshold is 0.30 and the WARN threshold 0.12.
- **Heart with the branch cards** (task230, and the newer task134 and task228 cards):
  - The nearest heart text is still 0.04, now shared by task230's driver, task228 v2's driver and task119's stump.
  - A second BLOCK appears: `ban.forcing_event`, against task134's branch card.

**Construction sweep.**
- I searched every card driver, `driver_concrete`, stump, analyst test and lineage driver (137 cards, task230 included), and every ledger mechanism cell, for task180's construction. The search terms were: self-controlled, within-person, the same person's other time, new user, channelling, confounding by indication, and selection on prognosis.
- No card or ledger row carries it.
- "Each unit's own" constructions appear in task83, task85, task181, task182, task228 (v2) and task37's lineage. None of them is a within-person exposure comparison.
- task16's lineage has a within-cell contrast that cancels a confounder, which is a stratified contrast.
- task180 is the only pharmacology card. The design note's claim, "No build on file uses a self-controlled comparison", holds.

**Mechanism coverage, over the 128 screened pairs.**
- **Track B from both cards: 106 pairs.** Of those partners, 14 carry back-fitted labels: task11, task12, and task25 to task36.
- **Track A only: 22 pairs.**
  - 17 partners have no mechanism layer: task3 to task10, task13 to task15, task18, task19, and task21 to task24.
  - 5 are note-only. task16, task17 and task20 have cards with no gap or pattern; task112 and task113 have no card.
- **Track B only:** task114, task115, task116, task134, task135 and task228 (card only on this checkout), and task230 (card only on its branch).

**Pack-level Track A.**
- Pack-level Track A ran on 126 of the 128 partners. task3 and task10 have no pack profile.
- Prompt-level Track A ran on 115 partners (13 have no prompt). Submission phrasing ran on 114.
- **Parquet is profiled by content hash only**, because `fingerprint.py` profiles delimited text and xlsx files.
  - So task180's three parquet tables, the registry spine, were compared by content hash only.
  - The schema and same-seed axes cover three of its four csv files and its xlsx. The fourth, `atc_ddd_index_2026.csv` (12 rows), is semicolon-delimited in the Danish way; the script's delimiter sniffing reads it as one column and skips it.
  - The same limitation applies to every pack that carries parquet: 36 of 129.
  - No content hash matched.
- No card's spine shares task180's grain (person x hospital contact) or a real source dataset.

**Staleness.**
- The card blocks held in the cache match the current card files exactly for all 129 cached builds that have a card file. task112 and task113 have no card file.
- task1 to task113 are fingerprints carried over from another checkout.

## In batch against earlier builds
In pre-flight the batch is task180 alone, so every pair is task180 against another build. The screen labels them "in batch" only because focus mode widens the window. **There is no hit against an approved or delivered build: no pair carries a finding.**

Status of each partner I read, from the ledger's status column. Where the ledger is silent, the status is unknown.

| Build | Ledger status | Its own records (not the ledger) |
|---|---|---|
| task131 | No row, so unknown. | Its `pipeline.json` records it delivered on 2026-10-10, with judge APPROVE and clone-check CLEAN. It is the partner a reviewer is most likely to hold beside task180 as delivered. |
| task68 | Live: built and repaired, its stump-check round held and its determinism check passed; nothing later recorded. | |
| task70 (v2) | Live: built. v1 is retired, solved on the platform. | |
| task104 | No row, so unknown. | |
| task134, task135 | No row, so unknown. | Each `pipeline.json` records stage 4 (leak check). |
| task182 | No row, so unknown. | Its `pipeline.json` records stage 4. The build is uncommitted in its worktree. |
| task230 | No row, so unknown. | Its `pipeline.json` records stage 4. |
| task181 (not adjudicated) | No row, so unknown. | Its `pipeline.json` records "portal round 1: stumped and deterministic, but the CSV asks were answered in full (52 against the 50 bar)", and delivered 2026-10-11. |
| task180 | No row. | `pipeline.json` records stage 4. This check is stage 5. |

## Track A findings, reviewer visible
None.

- **Hard tells.** None on any of the 128 pairs:
  - no byte-identical file and no same-seed table;
  - no shared column set and no shared target file name;
  - no shared invented name. Somnevo, Uralexa and Gravera appear in no other prompt. The only capitalised term shared with any prompt is "Thursday".
- **Surface.**
  - task182's 0.100 comes from the flat layout (116 of 129 packs are flat) and an identical format set (csv, md, parquet, pdf, xlsx). Only task180 and task182 carry exactly that set. Submission phrasing adds 0.0002.
  - Masked prompt overlap is 0.003 at most (task181), and submission phrasing 0.008 at most (task133).
  - All seven of task180's masked sentence openings are unique in the corpus.
- **The ask.**
  - The screen's ask parser does not recognise "Use the registry extracts to tell me which signal ...", so the Main Ask identity axis is blind for task180.
  - Read against the corpus openings, the carrier "tell me which" also opens a sentence in task14, task32, task38, task118 and task129 (see Corpus habits).
  - The "What I need from you is" carrier the architecture 2 pre-flight flagged is gone.
- **People.** The heart's name audit raises nothing for the six personas: Helge Jørgensen, Janni Nielsen, Frida Clausen, Kåre Holst, Iben Pedersen and Esben Olesen.
- **`voice-check.py`**, last 12 by number with a prompt on this checkout (task124 to task133, task180, task229):
  - The prompt is 983 characters and 165 words, the shortest of the twelve.
  - There is no carrier wording on the script's list and no unlisted repeated run.
  - The context share is 54.5 per cent, over the paid-out flag of 46.0. `prompt-voice.md` carries what to do about it.
  - The opening classifies as "other", a bucket concentrated at 9 of 12; the card files it as evidence-first.
  - Two deliverables: docx and csv.
- **Shape echo: none.** The four outline axes are ask construction, deliverable species, decision shape and calibration organ. Against each adjudicated partner at most one is shared; the detail is below.

## Track B findings, mechanism
None.

- All eight adjudicated pairs are clean. Seven share components, and one (task135) shares only a generator label. The detail is below.
- **The G17 key does not hide a Template finding.**
  - Under G16, the only other key the card's notes call honest, every pair that fires (task134, task104, task70 and task182) adjudicates clean.
  - Under the G6 probe, task68 and task230 adjudicate clean too.
- No collision lands on a retired row, so there is no history to report.

## Clean, shares components by design

**task180's decisive move, with the domain nouns stripped:**

> An exposure's effect is tested by comparing those who took it with those who did not. But uptake is selected on an unrecorded trait that already carries the outcome, so every between-person comparison, adjusted for everything recorded, credits the exposure with the selection. Only each person's exposed window against the same person's other time cancels every fixed trait and finds the exposure that changes the outcome.

**task180's path:**
1. Link the registry extracts on the pseudonymised number.
2. Take new users under SOP-PV-14: a 365-day washout across both ATC codes, residence, and returned dispensings not counted.
3. Build admissions under annex A, with transfers merged and action diagnoses only.
4. Compare between people:
   - spontaneous report counts (rung 0);
   - matched non-users (rung 1);
   - observed against expected (rung 1b);
   - the new-user active comparator, crude, adjusted and propensity-weighted (rung 2).

   Every one of these names the sleep medicine's falls.
5. **Compare each person with themselves: days 1 to 30 against the same person's days 61 to 180. This is the decisive step (rung 3), and it gives the uricosuric's kidney injury at 2.52.**
6. Count the 2025 admissions and the admissions caused, and the new users by year.

---

**task135 against task180.** Verdict: clean, sharing only the generator label. Track B. Axis to redraw: none.
- **task135's move.** A total is built by exponentiating a regression fitted on the log scale and summing it over a long record. The exponentiated fit is the conditional median, so the mean the total needs is that fit times a retransformation factor, set by each segment's residual spread.
- **Not the same claim.** task135 corrects an estimator's back-transform inside a forecast; task180 chooses an identification design under confounding. A solver primed by either learns nothing that reaches the other's decisive step.
- **task135's path.**
  1. Clean the samples, and pair each with its day's discharge.
  2. Fit the log rating curve for each creek.
  3. Apply it to every day of the 76-year creek record.
  4. Apply the decree.
  5. **Multiply by the smearing factor. This is the decisive step; R3 is the same build without it.**
  6. Apply the trap efficiency.
  7. Convert by density to a volume.
- **What is shared.**
  - The key G17 ("statistical rigor"), a catch-all generator that holds both an estimator correction and a confounding design.
  - Time as the second gap.
  - No calibration organ and no filed decoy.

  No move is shared, at any rung.
- **Outline.** None of the four axes is shared. task135 has a stakes-first ask, delivers xlsx + pdf and commits to a quantity. task180 has an instruction ask, delivers docx + csv and picks one of three.
- **For the author.** The guard's `ban.pattern` is a collision on the label. The card's differentiation line already names the real difference correctly.

**task182 against task180.** Verdict: `clean_shares_components`, Track B; the Track A surface is Idiom. Axis to redraw: none.
- **Promotion.** The surface score comes from the flat layout and the identical format set; submission phrasing adds 0.0002, and nothing else is shared.
- **task182's move.** Each unit's level follows a shared external driver through its own lagged response. A change measured from a fixed baseline, or against reference units in other strata, mixes that response with the effect. The effect is the gap between the observed level and each unit's own driver-only path, fitted before the effect began.
- **Not the same claim.**
  - task182 builds a dynamic per-unit counterfactual from a time-varying driver that every unit shares.
  - task180 cancels fixed selection by comparing each person with themselves.
  - The thing to see differs: deep units still rising on old wet seasons, against a new medicine channelled by its claims and its contraindications.
- **task182's path.**
  1. Reduce dips and loggers to levels.
  2. The decline from baseline (rung 1).
  3. Net of the reference bores (rung 2).
  4. A straight-line trend (rung 2b).
  5. One rainfall window for every bore (rung 3).
  6. **Each bore's own response to rain and evaporation, fitted before dewatering and run forward. This is the decisive step (rung 4).**
  7. The triggers and the offers.
- **Position of the shared moves.**
  - A comparison with other, non-comparable units is a wrong rung in both builds: the reference bores in task182; the matched non-users and the active comparator in task180.
  - A within-unit idea carries both decisive rungs, but in different forms: a calibrated response function against a self-controlled case series.
  - In task182 the plain own-baseline comparison is itself a trap (rung 1).
- **Outline.** One axis is partly shared: both deliver a per-unit table with a one-page docx note (xlsx + docx against docx + csv).
  - The asks differ: question-first against an instruction.
  - The decisions differ: a designation set of five against one pick.
  - The calibration differs: reference bores against none.
  - Both prompts force the call with a dated meeting, "approves offers on Monday 26 October" and "meets on Thursday 22 October". That is corpus idiom.
- task182's own design note names task180 and draws this same line.

**task134 against task180.** Verdict: `clean_shares_components`, Track B. Axis to redraw: none.
- **task134's move.** The probability of an event within a fixed horizon has to be estimated where some exits are not loss to follow-up (one can be reversed, one ends the risk) and no unit has been followed to the horizon. The estimate follows every unit to the data cut with nothing else censoring it.
  - Censoring the exits overstates it, most where they concentrate.
  - Ending follow-up at the reversible exit understates it.
  - The share observed so far understates it too.
- **Not the same claim.** Both use the Gate G mechanism `method_or_model_selection` with population as the decisive gap. But task134 decides who stays in a survival denominator, and task180 decides whom the exposed are compared with.
- **task134's path.**
  1. Stack the two jail systems through the crosswalk.
  2. Take the post-reform cohort, apply the exclusions, assign districts.
  3. Apply the return definition.
  4. **One minus Kaplan-Meier, with only the data cut censoring. This is the decisive step; Kaplan-Meier censoring removals and deaths is the stump.**
  5. Multiply by the adopted projection.
  6. Navigators, one per 250.
- **What is shared.**
  - The Gate G mechanism and the decisive gap.
  - The frame "the field's textbook estimator against the one that matches the estimand".
  - Calibration `none`.
  - A dated vote forces the call ("votes on 24 November").
  - Under G16, the decisive generator.
- **Outline.** None of the four axes is shared: an allocation in xlsx + png with a district grid, against one pick in docx + csv.
- **Note.** task134's branch card re-keyed its forcing event to `vote_or_meeting`. See What to redraw.

**task104 against task180.** Verdict: `clean_shares_components`, labels only. Track B. Axis to redraw: none.
- Read on the card and the cached submission. The folder lives on another checkout, so the design note and the full prompt were not read.
- **task104's move.** The question is what a self-adapting scorer would have flagged at a setting it never ran at. Flagged observations never enter its reference window and are re-taken before anyone acts, so its log describes only the setting that produced it. The detector has to be re-run, not its log re-thresholded.
- **Not the same claim.** task104 is about the decision feeding back into its own data; task180 is about selection into exposure.
- **task104's path.**
  1. The charter.
  2. Settled severity.
  3. The incidents that count.
  4. Lineage tiers.
  5. Recover the scorer from its own log.
  6. **Re-run it at each threshold. This is the decisive step.**
  7. Pages.
- **What is shared:** anomaly detection, the Gate G mechanism, the population gap and, under G16, the generator.
- **Outline.** None of the four axes: a dial delivered as html + svg, with an options-first ask.

**task70 (v2) against task180.** Verdict: clean, labels only. Track B. Axis to redraw: none.
- Read on the card (mechanism taken from the ledger), the ledger rows and the cached submission.
- **task70's move.** Per-record dates are rebuilt from an event log with a class-conditional cut that a filed clause sets. The classless construction hides the problem by reproducing the closed record exactly.
- **Not the same claim.** This is a construction and time-semantics move; task180's is a causal design.
- **What is shared:** only the G16 key, the gap and the Gate G mechanism.
- **Outline.** None of the four axes: a quantity delivered as pdf + xlsx + py, in an ETL build.

**task68 against task180.** Verdict: `clean_shares_components`, Track B. Axis to redraw: none.
- Read on the card, the ledger row, and the cached prompt and submission. The design note lives on another checkout.
- **task68's move.** An aggregate's movement is held flat by units entering and by a price offset. The true movement is read on a matched panel of the units present in both windows, linked across identity successions, in quantity, against a bar recovered from a closed corpus of settled dispositions.
- **This is the closest construction on file.** Both decisive rungs compare units with themselves across two windows.
- **Not the same claim.**
  - In task68 the aggregate's composition changed, and a closed register certifies the basis (Pattern B).
  - In task180 the exposed were selected on an unrecorded prognosis, and nothing certifies the design.
  - A solver primed by task68 builds matched comparisons. In task180 that is the trap (the agency's matched non-users, rung 1), not the answer.
- **task68's path.**
  1. Build the record.
  2. Replicate the screen.
  3. Dairy is a price move.
  4. Fruit is season timing.
  5. The value track ends at a nil return. This is the stump.
  6. **Back-test candidate bases against the register's 17 dispositions, which selects the matched like-for-like quantity. This is the decisive step.**
  7. Apply it: chapter 22.
  8. Check chapter 22's history.
- **Position.**
  - The within-unit device carries the decisive rung in both builds.
  - task68 reaches it through a corpus back-test; task180 reaches it through the field's design knowledge, with no corpus.
  - The insight it serves differs: composition against confounding.
- **Outline.** One of the four axes is shared: both pick one. The ask, the deliverables (pdf + csv + py + png) and the calibration (a closed decision corpus) differ.
- **For the author.** The design note's similarity claim names task68 as composition. The sharper line is the one above: the same device position, a different thing to see.

**task131 against task180.** Verdict: `clean_shares_components`, Track B. Axis to redraw: none.
- **task131's move.** Treatment was randomised at a sub-unit that shares one budget with its siblings inside a parent unit. Each treated sub-unit's lift therefore carries outcomes moved from differently assigned siblings, which nets to zero at full rollout. The at-scale effect is read only on parent units whose sub-units all drew the same arm.
- **Not the same claim.** task131 is interference: the randomisation unit is not the unit of independence. task180 is confounding by indication. task131 moves the analysis up to the cluster; task180 moves the comparison inside the person.
- **task131's path.**
  1. Gross lift.
  2. Net lift.
  3. Run-rate net lift at the card level, against the randomised controls. This is the filed basis and the stump.
  4. **Same-arm memberships. This is the decisive step.**
- **What is shared.**
  - The `causal_design` strategy: in both, the comparison the obvious basis implies is the wrong one, at the decisive rung. That is a strategy, counted under Strategy monoculture, not a driver.
  - The Gate G mechanism, the population gap, pick one, a docx deliverable, and the Layer 2 family `estimand_identification`.
- **Outline.** One of the four axes is shared, the decision shape. task131 has a question-first ask against an instruction, and delivers docx + png against docx + csv.
- **Status.** Delivered on its own record, so it is the partner a reviewer is most likely to hold beside task180.

**task230 against task180.** Verdict: `clean_shares_components`, Track B. Axis to redraw: none.
- Read on the card, prompt, submission and design note from its branch (7941b35).
- **task230's move.** A switch reaches heavy users first, so its effect is read against not-yet-switched users in the same weeks. But those users are a lighter mix whose seasonal trend runs harder. The counterfactual is built within each usage band, or reweighted to the switchers' mix; the pooled comparison books part of the season as the switch's effect.
- **Not the same claim: each build's answer is the other's trap.**
  - task230's ladder kills the within-unit comparison. Its R2, switched patients against their own reference level, fails because the season belongs in the counterfactual. task230 answers with a between-unit comparison conditioned on an observed trait.
  - task180 kills the between-unit comparison conditioned on every observed trait (rung 2), and answers with the within-unit comparison.
  - A solver primed by either build walks into the other's trap.
- **task230's path.**
  1. The series as reported.
  2. 7.0 accounts against 6.8 accounts.
  3. Each patient's own reference level.
  4. The pooled staggered difference-in-differences. This is the stump.
  5. Within volume quintiles.
  6. **Within engagement segment. This is the decisive step.**
- **What is shared.**
  - the `causal_design` strategy;
  - the Gate G mechanism and the decisive population gap;
  - the `monitoring_export` context artifact;
  - the Layer 2 family `estimand_identification`;
  - G17, decisive in task180 and supporting in task230;
  - calibration `none`.
- **Outline.** None of the four axes: a question-first ask, xlsx + pdf, and a designation set.
- **Visibility.** task230's card is only on its own branch, and task180's card is not on main, so neither build's guard has seen the other. task230's card carries a differentiation line against task68 and none against task180.

## Strategy monoculture
**Batch.** The last 12 builds in draw order ending at task180, counted from the cards on this checkout: task125, task126, task127, task128, task129, task131, task130, task132, task133, task134, task135 and task180.

| Measure | Count | Cap | Verdict |
|---|---|---|---|
| Withheld rule with an official decoy | 0 of 12 | above 2 | under |
| Certified-record decoy (`validated_decoy`) | **4 of 12**: task125, task126, task127, task129 | above 3 | **over: Strategy monoculture finding** |
| Any one `stump_strategy` | 2 of 12: `binding_constraint` (task127, task128) and `causal_design` (task131, task180) | a third (4) | under |

- **task180's own strategy.** It files `causal_design`, with the decisive rule not filed, no official decoy and no validated decoy. It adds to neither capped count.
- **Dropping the recorded-retired builds.**
  - The ledger is silent on all twelve. On their own records, task125 and task127 are retired.
  - Dropping the six builds whose own `pipeline.json` says retired (task120 to task123, task125 and task127) gives this window: task119, task124, task126, task128, task129, task131, task130, task132 to task135, and task180.
  - There the certified-record decoy is 3 of 12 (task124, task126, task129), at the cap but not over it.
  - `causal_design` is 3 of 12 (task124, task131, task180).
- **The same-day twelve.** This window ends at the newest draw and uses the branch cards: task131, task130, task132 to task135, task180, task181, task182, task228 (v2), task229 and task230.
  - The certified-record decoy is 0 of 12, and the withheld rule 0 of 12.
  - `causal_design` is 3 of 12 (task131, task180, task230). That is under a third, and at the guard's overuse WARN line.
  - task230's own guard could not count task180.
- **Against architecture 2.** Architecture 2's pre-flight counted 7 of 12 on its window (task119 to task131, then task180). The certified-record count has fallen as the window moved past task121, task122 and task124.

## Corpus habits
- **The pack recipe of this author's in-flight builds. This is an Idiom finding that touches task180.** Each of the three pairs a coded procedure PDF with a `<topic>_notes.md` field-notes file around a parquet spine. task131, the one other build with the same pair, is added for comparison:

  | Build | Procedure | Field notes | Pack formats |
  |---|---|---|---|
  | task180 | `SOP-PV-14_signal_refinement.pdf` | `registry_extract_notes.md` | csv, md, parquet, pdf, xlsx |
  | task181 | `PR-07_pertussis_response_protocol.pdf` | `pertussis_line_list_notes.md` | csv, md, parquet, pdf, txt, xlsx |
  | task182 | `MG-02_bore_assessment_and_make_good.pdf` | `monitoring_network_notes.md` | csv, md, parquet, pdf, xlsx |
  | task131 | `MP-3_measuring_offers_rev3.pdf` | `crm_extract_field_notes.md` | csv, docx, json, md, parquet, pdf, txt, xlsx |

  - A coded procedure PDF ships in 6 builds: task38, task131, task180, task181, task182 and task229. Five of them are among the 21 builds from task117 on.
  - 4 of those builds also carry a `_notes.md` file beside it.
  - task180 and task182 are the only two builds whose format set is exactly csv, md, parquet, pdf, xlsx. That alone is what promoted their pair.
  - The roles are required content: the governing procedure and the field notes. The names and the recipe are the habit. A reviewer holding the three in-flight builds sees one pack outline three times.
- **"Extract" in file names. This is an Idiom finding that touches task180.**
  - The word appears in file names in 45 builds, and in 15 of the 21 from task117 on. task180's `civil_registration_extract.csv` and `registry_extract_notes.md` are among them.
  - The architecture 2 pre-flight flagged the same habit.
  - Here the noun is the registries' own (extracts delivered through the national health data service), so it reads as the organisation's idiom. The count is the habit.
- **The dated decision meeting.**
  - Going by the masked sentence openings, at least 13 prompts force the call with a body that meets, sits or votes on a stated day: task33, task34, task38, task49, task57, task64, task87, task89, task117, task123, task134, task180 and task182.
  - task180 and task182 use the same construction, "on <weekday> <day> October".
  - `vote_or_meeting` is the forcing event on 6 cards, or 7 counting task134's branch card.
- **The ask carrier "tell me which".**
  - It opens a sentence in task14, task32, task38, task118, task129 and task180. "Tell me" opens a sentence in 14 builds.
  - The screen's ask parser recognises neither "Use ... to tell me" nor "What I need", so this carrier is invisible to the Main Ask axis.
- **Deliverables.**
  - A .docx paper ships in 16 builds, 7 of them among the 21 from task117 on: task125, task126, task127, task131, task132, task180 and task182.
  - A docx paper with a csv beside it appears in task127 (which adds an svg) and task180.
- **File names from the screen.** `data_dictionary` appears in 61 builds, `export_manifest` in 34, and `data_notes` and `provenance` in 12 each. task180 uses none of them.
- **Mechanism furniture.**
  - The decisive gap `population` appears in 7 of the twelve ending at task180.
  - The Gate G mechanism `method_or_model_selection` appears in 4 of those twelve, and in 5 of the same-day twelve.
  - `government_agency` is the organisation in 22 builds. That is the guard's WARN, answered in the design note.

## What to redraw
Nothing for task180 at any clone tier.

Outside the clone tiers, for the author's stage 5 decision, most expensive first:
1. **task180, decisive G-code (G17).** The heart's BLOCK against task135 stands on the author's `--force`. This check finds no shared driver behind it and asks for no redraw.
2. **task180, forcing event (`vote_or_meeting`).** It becomes a second heart BLOCK, `ban.forcing_event` against task134, once task134's branch card reaches main.
3. **task180, pack furniture (Idiom).** The coded procedure PDF and `_notes.md` names it shares with task181 and task182. This is a rename, reported and not looped on.
