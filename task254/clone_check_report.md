# Clone check: pre-flight, task254 (Lyrevo time-to-onset monitoring windows, architecture v2) against the whole corpus, 2026-10-11

## Verdict
CLEAN. No finding on either track. The only promoted pair is task254 against task446, shipped 2026-10-11 according to its `pipeline.json` (the ledger is silent). It is `clean_shares_components`: the cards share the guard's same-driver labels (gap time, G16, `method_or_model_selection`), but the drivers differ.

## Scope and coverage

**Mode and scope.** This is a pre-flight on task254 against every other build, with the window ignored, as stage 5 of `/build` asked.
- task254 is architecture v2. Its call is a time-to-onset distribution read off a post-marketing case series, which each patient's time on treatment right-truncates.
- The state of the build:
  - `task254/generator/make.py` cuts its pack.
  - Stage 4's `leak.py` REVIEW lines are answered in the design note.
  - No solver round has run yet.
  - `pipeline.json` still reads stage 3.
- Its lineage is v1 (fire planning bands, with burned area apportioned by final perimeter), spent at stage 2. The guard's own-lineage test passes.

**Which corpus.**
- This branch's `main` ref (4b49b1f) is 158 commits behind `origin/main`, so I took `origin/main` at e89a676 (20:39 UTC, "task446 shipped") as main.
- Each in-flight build came from its own branch, at the refs as last fetched. No fetch was run, and the newest head used is this branch's 27c35c6 (20:45 UTC).
- **From in-flight branches:**
  - task134: `sathya8571/task134-reentry-returns` e7eda17
  - task135: `sathya8571/task135-forebay-sediment` 4174551
  - task180: `oviya13ya/task180-revenue-protection` d34937d
  - task181: `oviya13ya/task181-arch3` c72d475
  - task228: `perssathya/task228-guardrail-alert-metric` 2e502d1
  - task230: `perssathya/task230-event-volume-drop` 1eb397a
  - task253: `sathay3012/task253-rent-relief-closeout` 41ad9e5
  - task445: `oviya1301/task445-hardening` e3c0554
  - task447: `oviya1301/task447-organic-deposit-growth` 8667fac
- **From `origin/main`:** task117 to task133, task182, task229 and task446.
- **From this worktree:** task254 as it sits at 27c35c6 (clean), with its regenerated `target/`.
- **Left out because they are not builds:**
  - task183 is intake only, with no draw.
  - `perssathya/task229-rework` opened a re-root and paused before the draw, so I used main's shipped task229.
  - The task446, task130, task131, task132 and task133 branches are merged into `origin/main`.

**How it was run.**
- I exported those folders read-only (`git archive`, `git show`) into a scratch folder inside the repo root, under `.work/`, which the exclude rule ignores. The folder was deleted at the end.
- I ran `origin/main`'s own `fingerprint.py` and `guard.py` over it, with the cards path pointed at the pooled set.
- `origin/main`'s extract reads `prompt.txt` as well as `prompt.md`. This branch's copy reads only `prompt.md`, so it would have skipped task133's shipped prompt and task230's prompt.

**Cards.** There are 142 in all:
- `origin/main`'s 138, plus task180, task253, task254 and task447.
- Each branch's own copy for task134, task135, task181 (architecture 3), task230, task253 and task445.
  - For task253 that is its branch's redrawn v2 (binding constraint). The stale v1 copy committed on this branch was not used.
- `origin/main`'s copies for task130, task133, task182, task228, task229 and task446.

**The prefabricated pooled card folder was read but not used as is.**
- It lacks task446's card, which reached main as shipped at 20:39.
- It carries older copies of task130 (07:57), task133 (07:58), task182 (13:45), task228 (08:54, from the task229 rework branch) and task229 (the rework's 09:17 card, whose architecture was spent at 09:44).
- Three of those older copies differ in identity fields:
  - task133: the driver and the opening move;
  - task228: the generators, Gate G, driver, deliverables and role family;
  - task229: the domain.
- Run against that folder, `guard.py heart task254` returns WARN instead of BLOCK, because task446 is missing. It would have hidden the one mechanical hit.

**Extract.**
- The committed cache was stale, both this branch's copy (128 cards) and `origin/main`'s (129 cards, written 18:55). Neither holds task254, task181, task445, task446 or any build in flight.
- I re-extracted into the scratch copy only, and the committed cache is untouched.
- That fingerprinted 30 builds from disk and kept 110 cached cards, for 140 in all. 138 are screenable; task1 and task2 have no prompt or pack.
- None of the 110 cached cards carries a mechanism block that differs from its current card.

**Builds compared.** 138 in the screen (task254 and 137 others), and all 142 cards in the guard and the driver sweep.

**What the screen could not see.**
- **No pack, compared on prompt and submission only:** task180, task228, task230, task253 and task447 have uncommitted packs. task3 and task10 have no pack profile either.
- **Packs from the cache:** task118 and task120 to task129 have no pack on disk, so their profiles come from the cache.
- **Mixed vintages:** task181's branch holds architecture 3's prompt and design note beside architecture 2's submission and pack.
- **Card level only:**
  - task1 and task2.
  - task99, which the script excludes by name; its card records it as the R5 state of task31's world (ledger row 31, failed).
  - task114, task115 and task116, which have cards but no folder anywhere.
- **The screen's deliverable-species axis is blind for task254.** The screen reads deliverables from backticked file names, and task254's prompt names its files in plain text, so that axis scored 0 on every pair. I read the deliverables from the cards instead.
- **Focus mode labels every pair "in batch".** That is a labelling quirk, not a scope bug.

**Pairs.**
- **Screened:** 137.
- **Promoted:** 1 (task446).
- **Adjudicated:** 1. None was left unread.
- **Read at card level although not promoted:**
  - task134, which shares the decisive generator and the stump strategy;
  - task445, which shares the decisive gap and the late-arrival family;
  - task91, the other live `maturity_censoring` card;
  - task33 and task35, the approved builds that share the decisive gap label;
  - task180, the other pharmacovigilance build;
  - task230, the subject of the guard's WARN;
  - task253, this author's sibling, which is just before task254 in draw order;
  - task132, the nearest surface.
- **Driver sweep:** I swept all 142 cards, lineage entries included, for truncation, censoring, maturity, run-off, reporting lag and time-to-onset wording.

**Adjudication method.**
- This run had no subagent tool, so I adjudicated the promoted pair in this thread against the adjudicator brief. That means the driver sentences with the domain nouns stripped, then the ordered paths and the position of each shared move, then tier, track and axis.
- No advisor, web or Agent tool was called.
- Reads were limited to:
  - cards, prompts and ledger rows;
  - task254's design note and submission;
  - task446's prompt, the solution steps of its submission and its pack listing;
  - task446's design note: the draw, stump, literal reader, ladder, and stump or fork sections;
  - the ladders of task134 and task445;
  - `pipeline.json` states.

**Mechanism coverage, over the 138 screenable builds.**
- **Layers:** 116 have a card mechanism layer, 5 are note-only and 17 have none.
- **Back-fitted labels:** 34 builds (task3 to task36) carry them, and 14 of those have a gap or pattern on the card.
- **Track A only in the screen:** 22 builds (task3 to task10, task13 to task24, task112 and task113).
  - 20 of them carry a driver sentence on their card, which the guard's heart check and the driver sweep both read.
  - task112 and task113 have no card and no ledger row, so they were checked on Track A only.

**Guard.**
- **Over the current pooled cards:** `guard.py heart task254` gives BLOCK.
  - The BLOCK is `test.same_driver_older` against task446 v2. The decisive gap, generator and Gate G match, and task254's card carries no differentiation line for task446. It is adjudicated clean below.
  - There is one WARN, `repeat.gate_g`, against task230 v1.
  - The nearest heart text is 0.05. The nearest driver is 0.11 (this slot's own v1), then 0.06 (task117).
- **On this branch at registration:** WARN, `repeat.gate_g` against task253's v1 card (design note, Guard verdict).
- **People:** `guard.py people task254` raises nothing. No other card carries a persona first name or surname, an invented name, the drug, the company or a wholesaler name from task254.

**Ledger.** The ledger has no row after task108. Every build since task109, which is task254's whole neighbourhood, is therefore status unknown on the record. Where a `pipeline.json` says more, I quote it as context, never as a status.

## In batch against earlier builds

This is a pre-flight, so every pair is task254 against another build.

- **No hit at any tier against an approved or delivered build.**
  - The ledger ranks ten builds that way: task25, task27, task28, task29, task30, task33, task34, task35, task48 and task72.
  - task254 shares no Track A tell with any of them. Their surface scores against it run from 0.015 to 0.083, the 13th to 70th percentile.
  - On Track B it shares only the decisive gap label (time), with task33 and task35. Their drivers are unrelated:
    - task33 is a forward yield scaled by the expected path and stopped at a filed intervention.
    - task35 is an attachment period recovered from settled records.
- **The live exposure is task446, drawn the same day and already shipped.**
  - The ledger is silent on it, so its status is unknown on the record.
  - Its `pipeline.json` reads shipped and delivered on 2026-10-11, and there is a SHIPPED commit on main at 20:39 UTC.
  - A reviewer can hold it beside task254. It is adjudicated `clean_shares_components` below.
- **task445.**
  - The ledger is silent on it.
  - Its `pipeline.json` records a portal delivery on 2026-10-11 (round 1 average 52, determinism QC failed), and it is now hardening in design.
  - It is clean on mechanism (below).
- **Other builds delivered that day or the day before, according to their pipelines:** task131 (delivered 2026-10-10), task132, task133, task182 and task229. None of them shares a tell or a driver with task254.

## Track A findings, reviewer visible

None.
- **Hard tells:** no byte-identical file, same-seed table, shared column set, shared target file name, shared invented name or shared persona.
- **Prompt wording:** the masked prompt overlap is 0.000 against every build. No rare sentence construction and no solution-step construction is shared.
- **Surface scores:** task254's top out at 0.093 (task132, 93rd percentile), with a median of 0.075. Every one of them comes from layout and format mix alone.
- **Voice check:** the batch report over the twelve-build batch finds no unlisted repeated run of six words or more.

**An outline shared with one build, task446.** It sits below the Shape echo tier, and nothing needs renaming.
- **What is shared:**
  - an xlsx with an svg, a pair on 4 cards in the corpus (task86, task114, task254 and task446);
  - a workbook name ending `_2027`;
  - a `committee_or_panel` forum;
  - a chart title asked to carry the headline figure.
- **What differs:**
  - The ask sentences are built differently. task254 uses an imperative ("Give me the month of treatment by which..."), and task446 a question ("How many of the obligor groups... as one whole number?").
  - The decision shapes differ. task254 asks for cuts of a distribution (shape 14, `dial_setting`), and task446 for an allocation to a fixed total (shape 05, `quantity_figure`).
  - The calibration organs differ: none, against `existing_book_actuals`.
- The year stem and the title-carrying chart are corpus idiom (see Corpus habits).

**The guard from task446's side.**
- Checked over the pooled cards, the guard raises two bans on task446 against task254: `repeat.deliverables` (svg with xlsx) and `ban.forum` (`committee_or_panel`).
- Those bans fall on the later draw. task446's architecture 2 was registered at 17:36 UTC, against task254's at 17:27, and it also sorts later in draw order.
- task446 has shipped, and neither branch could see the other's card.

## Track B findings, mechanism

None.
- **The screen's mechanism route** promoted one pair, task446, on the cards' same-driver signature. It is adjudicated clean below.
- **The guard's structural tests:**
  - Same puzzle (gap, pattern and decision type): no hit.
  - Same driver (gap, pattern and Gate G): task446 only.
- **The driver sweep** found the relatives listed under Clean and under History. None of them carries task254's decisive move.
- **Does the data survive?** No redraw is called for, so the data survives as cut.

## Clean, shares components by design

**task254's decisive move, with the domain nouns stripped:** "A cut of a time-to-event distribution seen only through events that have happened by a fixed date, among units whose starts crowd toward that date, is estimated with each event bounded by its own time from start to that date; read straight off the observed events it comes out too short."

**1. task446 (the promoted pair): `clean_shares_components`.**

**Status.**
- The ledger is silent. Its `pipeline.json` reads shipped and delivered on 2026-10-11.
- Its architecture 2 was drawn at 17:36 UTC on `oviya1301/task446-lei-group-concentration`. That is nine minutes after task254's architecture 2, drawn at 17:27 UTC on this branch.

**Decisive moves, with the domain nouns stripped.**
- **task446:** "A screen's yield measured on past populations moves with each population's base rate while its two error rates hold, so the forward count backs the base rate out of the share now flagged through the error rates; carrying the yield forward undercounts when the flagged share has jumped."
- **task254:** as above.

**The same claim? No.**
- **What each turns on.**
  - task446 turns on which property of a classifier carries across populations whose prevalence differs (the Rogan-Gladen inversion).
  - task254 turns on a sample that holds only the events that have already happened, each cut short by its own time to the lock.
- **Estimand.** task446's is a forward count. task254's is a cut of a distribution.
- **Repair.**
  - task446's is an algebraic inversion through two error rates.
  - task254's is a product-limit estimate over risk sets bounded by each case's truncation time.
- **What selects the method.**
  - A filed leave-one-cohort-out test (5.2) selects task446's basis.
  - Nothing filed selects task254's estimator. Annex 7 rules out parametric fits and says nothing else about estimation.
- **The shared labels are coarse.**
  - "Time" means a base rate that moves year to year in task446, and time not yet elapsed in task254.
  - G16 is the generic method-selection generator, decisive on 4 of the 12 cards in task254's window.
  - `method_or_model_selection` is on 5 of those 12.

**Paths, in order.**
- **task254:**
  1. The version current at the lock kept; study and post-lock cases left out; duplicates merged.
  2. Terms mapped on the v4 list.
  3. Courses built from the dosage lines, and time to onset counted from each course's first dose.
  4. Laboratory onsets dated from the PSP feed.
  5. **Each reaction bounded by its course's time on treatment at the lock, with the reverse-time product-limit estimate (or the cut over courses older than the longest onset). This is the decisive step.**
  6. The asks: case counts.
  7. The asks: patient-years from the supply data.
  8. The call: month 20.
- **task446:**
  1. The monitored book built.
  2. Entity signals carried to groups through the register and GLEIF.
  3. The closed cohorts matched to the watch list, with their capture and false-alarm rates.
  4. The filed leave-one-cohort-out test run over the bases.
  5. **This year's base rate backed out of the flagged share through the two error rates. This is the decisive step.**
  6. The probabilities summed to 133.
  7. The asks: band exposure.
  8. The call.

**Where the shared move sits.**
- Both builds conform their data first and take the decisive step at step 5 of 8. That is the write-up format, not a device.
- No move is shared:
  - task446's back-test over closed cohorts has no counterpart in task254, which ships no calibration organ.
  - task254's truncation has no counterpart in task446, whose cohorts are closed twelve-month windows.

**Tier, track and axis.** There is no tier and no finding, so no axis needs redrawing.
- The guard still returns BLOCK on task254 until its card carries a `differentiation` line for task446 naming this difference.
- Filing that line is the main session's step (see What to redraw).

**2. task134 v1: clean on mechanism.**
- **Status:** no ledger row. Its `pipeline.json` reads architecture 1 spent at hardening loop 1, with a re-root pending.
- **What it shares:**
  - the decisive generator, G16;
  - the stump strategy, `maturity_censoring`;
  - the highest card-driver overlap with task254 (0.155).
- **Its decisive move:** the probability of an event within a horizon when some units leave through exits that are not censoring, so censoring those exits overstates it.
- **Where the shared move sits.**
  - In task134 the incomplete-follow-up move is R0, the share observed so far, killed by censoring. Round 1's solver cleared it by default with Kaplan-Meier.
  - In task254 that move is the decisive rung. The incompleteness is also of a different kind: truncation (units with no event yet are absent from the series), not censoring (released units sit in the data with their follow-up).
  - It is demoted there and decisive here, which is reuse, not cloning.

**3. task445 v1: clean on mechanism.**
- **Status:** no ledger row. Its `pipeline.json` reads delivered 2026-10-11, portal round 1 average 52, determinism QC failed, now hardening.
- **What it shares:**
  - the decisive gap label, time;
  - `method_or_model_selection`;
  - the late-arrival family.
- **Its decisive move:** complete the reporters still due at the extract by the drift their own class shows, the basis a filed back-test selects.
- **Where the shared move sits.**
  - In task445 the late-arrival move is R0 (reports on file only), killed by a filed sentence, OM-4 s.2.
  - It is filed and demoted there, and unwritten and decisive in task254.

**4. task91 v2: clean.**
- **Status:** the ledger has it live.
- **What it shares:** `maturity_censoring`.
- **Its decisive move:** units too young to have begun exiting look dormant, so the residue is misclassified, and a closed corpus certifies the wrong reading.
- That is a state classification confounded by age, not a duration distribution estimated under truncation.

**5. task33 and task35 (the ledger has both approved).** They share the decisive gap label only. Their drivers are given under In batch above.

**6. task180 v3.**
- **Status:** the ledger is silent, and its `pipeline.json` reads retired.
- **What it shares:** it is the only other pharmacovigilance build, with the same role family (`compliance_or_audit`) and the same forum.
- **Its driver:** confounding by indication, answered by a self-controlled comparison of each person's own windows.
- The objective (anomaly detection) and the deliverables (docx with csv) differ, and the build is retired. This is history, not a finding.

**7. task230 v1 (the guard's WARN `repeat.gate_g`).**
- It shares the Gate G label only.
- Its registered card is architecture 1, with a counterfactual drawn from not-yet-switched units within usage bands.
- Its architecture 2 is on paper and unregistered.

**8. task253 v2 (this author's sibling, just before task254 in draw order).**
- It shares the objective, Descriptive & Distribution, only.
- Its driver re-solves a congestible network with one link removed. That is a binding constraint, with a different gap, generator and strategy.

**9. task132 (the nearest surface, 0.093, 93rd percentile).**
- It also shares `dial_setting`, but the surface score comes from layout and format mix.
- Its driver is renewal on a wear-out curve (G6).

**History: dead rows, a record of the redraw working, not findings.**
- The nearest wording in the corpus to task254's shortcut is on two dead rows:
  - task31's R5 state, filed as task99 (ledger row 31, failed): "dropping the unfinished cases... erases the slow stratum".
  - task75 v1 (ledger: retired): "any conversion through the mean duration of completed cases understates it".
- Both take durations from completed cases while the open cases stay visible and censored, which is not truncation.
- Both rows are dead, so neither is a finding.

## Strategy monoculture

**The batch.** The twelve builds ending at task254 in the guard's draw order, with the in-flight cards included: task132, task133, task134, task135, task180, task181, task182, task228, task229, task230, task253 and task254.

**`stump_strategy` shares.**
- Three strategies carry 2 builds each:
  - `maturity_censoring` (task134, task254);
  - `causal_design` (task180, task230);
  - `decomposition_attribution` (task182, task228).
- Six carry one build each:
  - `population_selection` (task132);
  - `stated_rule_hard_construction` (task133);
  - `other` (task135);
  - `forecast_method_backtest` (task181);
  - `grain_or_unit` (task229);
  - `binding_constraint` (task253).
- The largest share is 2 of 12, under a third.

**The two capped architectures.**
- The withheld rule with an official decoy: 0 of 12 (cap 2).
- The certified-record decoy (`validated_decoy`): 0 of 12 (cap 3).
- No card sets `official_decoy`. `decisive_rule_filed` is false on task134, task135 and task180, none of them with a decoy.

**No monoculture finding.** Within the batch:
- `method_or_model_selection` is on 5 of the 12;
- the decisive gap is population on 6;
- G16 is the decisive generator on 4 (task134, task182, task228 and task254).

**Over all sixteen cards drawn on 2026-10-11** (adding task130, task445, task446 and task447):
- `forecast_method_backtest` reaches 4 of 16 (task130, task181, task445, task446), still under a third;
- `method_or_model_selection` is on 8 of 16;
- G16 is the decisive generator on 5.

If task134's pending re-root draws another strategy, `maturity_censoring` falls to 1 of 12, task254 alone.

## Corpus habits

- **Pack file roles.**
  - `data_dictionary` appears in 61 builds and `export_manifest` in 34; `data_notes` and `provenance` appear in 12 each.
  - task254 ships none of them. Its dictionary is `safety_export_field_guide.pdf` and its provenance is `PSUR6_data_package_log.txt`, both in the organisation's own idiom.
- **A chart title that carries the call.** 18 of the 30 prompts on disk ask for one: task117 to task125, task127 to task129, task131, task134, task181, task230, task254 and task446. The wording varies only slightly: "a title they can quote", "a title the room can quote", "a title that gives the ILD month".
- **A year stem on a deliverable.** 35 builds carry one, including:
  - this author's task253 (`crossing_criticality_2027`) and task254 (`rmp_monitoring_windows_2027`);
  - task446 (`watchlist_inflow_2027`).
- **Formats in the voice-check batch of twelve.** xlsx in 6, png in 5, docx in 4, csv in 3, pdf in 2 and svg in 2 (task254, task446). Most builds ship two files.
- **Question forms.** 7 of the 12 prompts do not lead with a question, and task254 is one of them. Current main's voice gate fails 11 of the 12 on at least one rule (see note 3 below).
- **Same-day parallel draws on separate branches.** Sixteen cards were drawn on 2026-10-11.
  - With every in-flight card in one set, task446's own guard check raises standing bans that no branch saw, against task254, task253, task445, task134 and task182. Those bans fall on task446, the later draw, which has shipped.
  - task254's own guard BLOCK comes from the same blind spot.
  - This is a process gap, observed here rather than authored.

## What to redraw

Nothing. task254 carries no finding on either track.

**Bookkeeping notes.** None of these is a finding, and each is the main session's call.
1. **task254's card.**
   - `differentiation` is empty, so `guard.py heart task254`, and `/approve` with it, stops on BLOCK `test.same_driver_older` against task446.
   - A one-line entry for task446 naming the difference above clears it: an estimator for a case series truncated at the lock, against a base rate backed out of a screen's flagged share.
   - This check does not edit cards.
2. **The prefabricated pooled card folder is stale.**
   - It lacks task446's card and carries older task130, task133, task182, task228 and task229 cards.
   - Against it the guard returns WARN for task254; against the current refs it returns BLOCK.
3. **This branch is 158 commits behind `origin/main`.**
   - Main's voice gate now wants `prompt.txt`. On task254's `prompt.md` it fails four rules: the file rule, question first, the sequencing opener "Then" and rounding stated before the close.
   - A rewrite would change the Track A surface screened here, so `guard.py surface` would need a re-run after it. Track B does not move.
4. **The opening move on the card is out of date.** The card records `opening_move: question-first`, but since the stage 4 reopen the prompt opens stakes-first ("Every patient that reaches the month of treatment we file...").
5. **The committed cache.** `.claude/skills/clone-check/.cache/fingerprints.json` is tracked, stale (it holds no task254) and untouched, because this run extracted into the scratch copy only.
6. **`pipeline.json`.** Its `duplicate_check` block is still empty.
