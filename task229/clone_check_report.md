# Clone check: pre-flight, task229 against the whole corpus (hardening loop 1, pass 2), 2026-10-11

## Verdict
CLEAN for task229: no Track A or Track B finding at any tier, live or history, on the hardened driver (the unit the standard error is built over); the nearest mechanism neighbour, task131 (two back in draw order), is clean, shares components. Batch level, not task229: Strategy monoculture, the certified-record decoy in 7 of the 12 builds ending at task229 against a cap of 3.

## Scope and coverage
- **Mode and scope.** Pre-flight on task229 against every other build, no window. This is pass 2: the round-1 pre-flight (`task229/clone_check_report.md`, CLEAN) ran on the earlier driver (per-installation mean with a between-installation error). Hardening loop 1 moved the decisive rung to the unit the error is built over, so everything was rerun. I read `clone-check/SKILL.md` (unchanged since 01:41) before writing any verdict.
- **Draw order.** `fingerprint.py` measures "consecutive" by task number, and the numbering jumps from task131 to task228. So I applied the consecutive-build rules by hand in the guard's draw order: task228 one back, task131 two back, and task130 v2 (drawn the same day as task131) as also recent.
- **Extract.** 126 cards.
  - 16 were fingerprinted from disk: task117 to task131 and task229.
  - 110 were carried over from builds fingerprinted on another checkout (`/Users/saa/...`). Their mechanism fields match today's card files exactly (0 of 110 drifted).
  - The tracked cache (written 04:44 from the main checkout) holds neither task228 nor task229, so it is stale for this run. I ran the extract with `--out` into a scratch copy seeded from it.
  - `.claude/skills/clone-check/.cache/fingerprints.json` and `.claude/skills/fingerprint/.cache/people.json` are byte-identical before and after (sha256 checked). `guard.py heart` ran on a scratch copy of the guard tooling.
- **Screen.** `fingerprint.py screen --focus task229`: 124 screenable builds (task1 and task2 have no prompt and no target), so 123 pairs, ranked against the 7,626-pair corpus baseline (mean surface 0.0555). **Promoted: 0.**
- **Consecutive rules, by hand. None fires.**
  - task228 (one back): only the decisive gap collides; card-driver overlap 0.000.
  - task131 (two back): surface 0.085 (78th percentile, layout and formats only); only the decisive gap collides; driver overlap 0.045.
  - task130 v2: surface 0.077 (58th percentile); no mechanism axis collides.
  - The Part 6.1 axes (pairing, subdomain, decisive pattern or G-code, calibration, role family, context artifact, spine, shape, strategy, forum, forcing event, organisation family) differ from all three.
- **Guard heart (scratch copy).** WARN, no BLOCK.
  - `repeat.gate_g` against task228, already answered in the design note.
  - NOTE `test.same_puzzle_older` against task98 v3, differentiated on the card.
  - Nearest heart text is 0.04 (task114) and nearest driver is 0.06 (task87 v3), far under the 0.12 warn line.
- **Builds the screen cannot see.** task114, task115, task116 and task228 have cards but no build on this disk or in the cache.
  - Scored with the script's own `track_b`: task228 and task116 collide on the decisive gap only, task115 on pattern D only, task114 on nothing. No promotion route fires.
  - task228's prompt, pack and design note live on the b228 checkout, which this run was barred from reading. It was compared on card fields only.
- **Not reachable.**
  - task61 is retired and its folder deleted. Its ledger row shares nothing.
  - task96 is a ledger row only ("drawing"), sharing the decisive gap only.
  - task99 is a scratch slot, excluded by design.
- **Pairs adjudicated: 6, all promoted by me and read in sequence (no Agent tool).** I also read two dead rows as history (task98 v3, task48 v1).
  - task131: two back, and the nearest mechanism neighbour by vocabulary.
  - task228: one back, same objective and Gate G.
  - task54: its ledger names its device "the unit of independent risk is not the unit of record".
  - task34: approved; shares decisive gap and pattern and ships a design-based standard error.
  - task48: designation set, `grain_or_unit`, G2 and G17, and a dispersion device.
  - task49: the most label overlap of any build.
- **Why I promoted by hand.** Both text routes are blind to this driver family. The best card-driver overlap is 0.115 (task65) against a 0.40 promotion line, and the guard's TF-IDF scores every adjudicated pair at 0.05 or below. So I swept for the move's vocabulary:
  - **Terms:** cluster, design effect, intra-class, effective sample, independent, fail or move together, shared parent or node, common cause, standard error, robust or sandwich, pseudo-replication, unit of analysis or randomisation, overdispersion, binomial, understated variance, between-unit spread, nested or hierarchical, collector, mesh, gateway, feeder, cluster bootstrap, degrees of freedom, sibling.
  - **Where:** every card driver, concrete driver, stump, note, niche, lineage driver and differentiation line; every ledger cell plus the ledger's full text; every cached solution step, critical component and recommendation.
  - **Result:** 72 cells hit. Two more sweeps followed: inference vocabulary (noise, variance, interval, sigma, false alarm, multiple comparisons, bootstrap) over all main and lineage drivers and stumps, and randomisation-unit wording over drivers and solution steps.
  - **No cell states the move.** The cells that carry a parent-unit or dependence premise are task131, task54, task106, task48 (v1 and v2) and task34. task43 and task83 use standard errors only as supporting checks.
- **Pairs left unread: 118 screened pairs, plus 3 card-only slots (task114 to task116) read on card fields. None was promoted.**
  - Twelve builds share task229's decisive gap and pattern (population, D). I adjudicated task34 and task49.
  - For the other ten (task52, task57, task60, task72, task74, task77, task81, task90, task93 and task103), I read the drivers. None states the move.
  - Twelve pairs tie at the top surface score, 0.100 (97th to 98th percentile). The screen lists task28, task31, task43, task44, task46 and task54 first. All of them score on flat layout and format mix alone.
- **Mechanism coverage, over the 123 other screened builds.**
  - Track B was scored on 101 pairs.
  - 22 pairs were Track A only: 17 builds with no mechanism layer (task3 to task10, task13 to task15, task18, task19, task21 to task24) and 5 note-only builds (task16, task17, task20, task112, task113).
    - 20 of those 22 carry a card driver sentence, and the sweep read every one.
    - task112 and task113 have no card.
  - 34 screened builds carry back-fitted labels (task36 and earlier); 14 of them have a card mechanism layer.
- **Track A coverage gaps.**
  - 108 of the 123 have a target profile. task3, task10 and task117 to task129 have none, because their packs are on neither this checkout nor the main one (`target/` is gitignored until delivery). Against those 15, file names, hashes, schemas and numeric signatures were not compared, only wording. task129 also has no `submission.md`.
  - 13 builds have no prompt in the cache: task5, task6, task7, task9, task11, task12, task13, task18, task19, task21, task22, task112 and task113.
- **Status.** The ledger has rows for task25 to task108 only.
  - Genuinely approved: task25, task27, task28, task29, task30, task33, task34 and task35.
  - The screen also ranks task48 and task72 as "delivered or approved". Both are regex false positives from fiction text ("one group-by delivered the conclusion"; "service delivered under"). Their cells record "Awaiting round 2" and "stump-check round 3 not yet run".
  - task109 to task131, task228 and task229 have no row, so their status is unknown on the record.
- **How the reading was done.**
  - Sources:
    - the cards and the ledger;
    - task229's design note, prompt and submission;
    - task131's and task130's design notes, prompts and submissions on disk;
    - the cached solution steps of task34, task48, task49 and task54;
    - the client's Layer 2 pattern file.
  - No golden file was opened. Nothing beyond what the cards and design notes state was read from any answer key.
  - The person-name detector finds no persona in the narrative files of task229's pack (prompt, submission, standard PDF, field reference). The card's persona appears on no other card.

## In batch against earlier builds
- Pre-flight has no window, so every pair is task229 against an earlier build.
- **No hit against an approved or delivered build.** I scored all eight genuinely approved builds (task25, task27, task28, task29, task30, task33, task34 and task35) on both tracks.
  - task28 is the nearest approved surface (0.100, 97.3rd percentile). It scores on flat layout and an identical format set only, and shares no mechanism axis.
  - task34 shares the decisive gap and pattern labels (back-fitted on its side) and ships a design-based standard error. Adjudicated below: the error is a margin check there and the decisive rung here, so it is reuse.
- No exclusion-level exposure exists for task229.

## Track A findings, reviewer visible
None.
- **Hard tells.** Across all 123 screened pairs there are no byte-identical files, no same-seed tables, no tables with an identical column set, no shared target file names and no shared invented names. "Halvane Metering" appears on no other card.
- **Prompt and write-up.**
  - The largest masked-prompt overlap is 0.0042 (task75) and the largest write-up overlap 0.0020 (task109).
  - The only shared capitalised token is "Tuesday" (task75).
  - No ask construction, step construction or deliverable species repeats.
  - No on-disk prompt or write-up from task117 to task131 uses "standard error", "lower limit", "read health", "firmware" or "collector".
- **Habit file names.** The target avoids them: the dictionary role is `mds_extract_field_reference.md` and the provenance role is `extract_log_20261012.csv`.
- **`voice-check.py task229`** ran over task121 to task131 and task229.
  - No carrier wording and no unlisted repeated runs.
  - Economy is inside the paid-out limits: 238 words against a median of 253, 21.6 words a sentence, context share 26.1 per cent, longest paragraph 121 words, one rounding tag carried by a convention sentence.
  - task229 is the only JSON deliverable in the twelve.
- **task131, the nearest neighbour on the surface outline.** Both asks are "Which of ..., and ...?" questions. task131 opens on its question; task229 ends its context on it.
  - Beside that sit docx+png against json+png, a pick of one against a designation set, and no calibration organ on either side.
  - That is below Shape echo.
- **task228, on card fields only.**
  - Everything that identifies a world differs: domain, geography, currency, organisation, forum, forcing event, spine, personas and invented names.
  - The outline differs: shape 04 against 10, pick one of N against a designation set, a gold-standard subsample against no calibration organ.
  - The shared outline is a JSON alert file beside a PNG, with "alert" in both JSON names (`peak_alert_config.json` against `wave8_read_health_alerts.json`). That is below Shape echo.
  - The ask sentences could not be compared.

## Track B findings, mechanism
None, live or history.
- No main field or lineage entry shares task229's decisive gap, decisive pattern and decision type together. The one exception is the retired task98 v3, which is history with a different driver (below).
- No card shares the gap, the pattern and the Gate G mechanism together.
- No driver, stump or ledger mechanism cell states an error built over shared parents.
- Across the corpus, task229 is the only build whose decisive move leaves every point estimate unchanged and moves only the error. The nearest inference-centred drivers are task228 (alert noise calibrated over the forward run length) and task48 v1 (retired; overdispersion as one of five conditionings).

## Clean, shares components by design
**task229's decisive move, with the domain nouns stripped:** the error of a mean over entities that fail together through a shared parent has to be built over the parents. An error that takes each entity as its own unit understates it severalfold for a group concentrated behind few parents, so the alert fires on parent noise. Every build's read health is identical under both errors; only the error moves.

**task229's path:**
- R0: pooled reads, latest delivery, binomial error.
- R1: reads held at the cut-off against every expected interval.
- R2: installations on one build all week.
- R3: the mean of installation read health.
- R4: the textbook error over installations. This is the stump, and round 1's landing step.
- R5: the error built over the comms nodes (decisive).
- Then the Wave 8 and Wave 7 asks.

**Each pair below is Track B, verdict `clean_shares_components`, with no axis to redraw.**

- **task131** (two back in draw order). Neither side has a ledger row, so status is unknown on the record for both.
  - **Its move, stripped:** a treatment randomised at a sub-unit spills between siblings that share a parent's budget, so the effect has to be read on parents whose sub-units all drew one arm. Read at the randomisation unit, it ranks the options in a different order.
  - **Not the same claim.** task131 corrects a bias in the point estimate: spend moved between sibling cards is counted as gain on one card and loss on another (G10). task229 corrects the precision of an unbiased mean.
  - **Its path:**
    - R0: card-level gross sales lift.
    - R1: card-level net margin over the whole test.
    - R2: the run-rate card-level lift. This is the stump, and it picks offer D.
    - R3: memberships whose cards all drew one arm (decisive). This picks offer A.
  - **The shared component sits on the decisive rung in both.** It is the parent key held in a side table (membership through the card master; `comms_parent` through the head-end export), with the stump written as "reading the sub-unit as independent".
  - **The move made on that rung differs.** task131 changes the comparison set and re-estimates. task229 keeps every installation and the same mean, and changes the variance unit.
  - **Swap test.** Each build's answer turns on a different violation:
    - If siblings were merely correlated, task131's card-level answer would stand.
    - If installations failed independently, task229's installation-level answer would stand.
    - Clustered errors over memberships leave task131's ranking untouched.
  - The client's own Layer 2 library files these apart: `network-effect-marketplace-experimentation/1` (contamination and spillover) against `complex-survey-estimation-variance/1` (clustered variance).
  - Worth knowing: this is the pair a reviewer holding the batch would set side by side. See Corpus habits.
- **task228** (one back; no ledger row, status unknown on the record). Read from its card and task229's design note; its own note is on the barred checkout.
  - **Its move, stripped:** the false-alarm budget applies per run while the check is evaluated on every look, so the setting has to be calibrated on runs of the forward length. On that length the heavy-tailed candidate loses most of its sensitivity and a light-tailed one leads.
  - **Its path (from the card):**
    - the replay audit as the record;
    - per check, the most sensitive setting under a per-run budget, which its competent solver already applies;
    - the events check at 12 per cent, calibrated on last year's mix of run lengths. This is the stump.
    - recalibration on the forward 28-night runs (decisive);
    - the beacon-loss check at 3.3.
  - **Not the same claim.** Both decisive steps sit in what an alert's noise reference is built over, but on different axes: the length of the forward run (G13) against the unit of the error (G2, G17). Neither move changes the other build's answer.
  - **Shared components:**
    - the objective;
    - the Gate G label;
    - the decisive gap label;
    - G12 and G17;
    - the JSON-plus-PNG outline.
  - **Position.** The multiplicity is task228's frame, and the noise model is task229's decisive rung.
- **task54** (ledger: drawing, live; built on another checkout).
  - **Its move, stripped:** loss arrives per event and takes every unit in custody when it starts, so expected loss scales with the units aboard summed over events. A plan that only re-sequences the work multiplies that exposure at unchanged rates.
  - **Its path (cached steps):**
    - qualifying deviations;
    - consignments aboard at onset, reproducing 48 of 48 closed investigations;
    - rival readings refused;
    - rate corrections that walk the figure down;
    - the per-call hazard;
    - pack-legs on the reference period and on the plan, giving 1,420 (decisive).
  - **The shared premise:** one event strikes every unit attached to a parent ("the unit of independent risk is not the unit of record").
    - In task54 it is pinned by the closed investigations at the second step and feeds an exposure measure.
    - In task229 it is unstated, forced by the node-night split, and is the decisive rung.
  - **Not the same claim.** task54's figure is a first moment. Packs failing one by one at the same per-call hazard give the same 1,420. task229's answer is nothing but the dependence.
- **task34** (ledger: approved).
  - **Its move, stripped:** a subpopulation no column names is enumerated only by a within-cluster fit of an amount on unit size, confirmed by a re-measured subsample. The pooled distribution shows no break, and the column-aligned grouping gets the count right and the classes wrong.
  - **Its path (cached steps):**
    - the burden universe;
    - the vendor deliverable reproduced;
    - the standard's weighted household basis;
    - the 30 per cent line tested;
    - one mode on the burden axis;
    - clause 4.3 on columns, giving wrong classes;
    - the re-contact test;
    - the 52-dollar size steps;
    - the within-community fit (decisive: 17 of 32 communities);
    - the distribution;
    - refused divisions;
    - a delete-a-group jackknife error on 80 replicates (15.14 points, 1.76, 8.6 errors);
    - the call.
  - **Shared components:**
    - a design-based error over the survey's primary units;
    - the two-grain frame (household against person rows);
    - the gap and pattern labels, back-fitted on task34's side.
  - **Position.** In task34 the design-based error is the second-last step, a margin the verdict does not turn on: a simple-random-sample error would only widen the 8.6. In task229 it is the decisive rung. The device carries the decisive rung on one side only, which is reuse.
- **task48 v2** (ledger: built, awaiting round 2).
  - **Its move, stripped:** a population invisible to the monitor at its reporting grain is recovered only by aggregating to a two-sided pair grain. That comes after every flag is conditioned away and the hold has become the strongest wrong answer.
  - **Shared components:**
    - a designation set with a hold as the rival;
    - `grain_or_unit` with G2 decisive;
    - G17;
    - a variance device: a series whose Poisson trigger understates its routine spread.
  - **Position.** That device is the fifth conditioning, step 6 of 11, and its competent solver clears it. In task229 an understated error is decisive, from a different source: dependence through shared nodes, against one small series' own overdispersion over time.
  - **History.** task48 v1 (retired, solved exactly) held the response on five legitimate structures, small-cell overdispersion among them. The ledger's lesson is that every rung of a five-flag conditioning panel is a hygiene reflex this opponent runs unprompted. That is a record about the device, not a clone of task229's driver.
- **task49** (ledger: built, live).
  - **Its move, stripped:** an amount that cannot go negative per instrument is floored before summing, because netting inside an entity makes every reporting date look comfortable.
  - **Shared components:** gap population, pattern D, `grain_or_unit`, shape 10, and aggregating per entity first.
  - **Not the same claim:** a floor that does not commute with summing, against an error built over parents.
- **task98 v3** (retired 2026-10-03, history). It matches the Part 6.1 signature: population, D, designation set.
  - Its move: units formed by chaining members within a fixed distance, then a per-unit threshold.
  - The driver differs, and task229's card carries the differentiation line.
- **task130 v2** (also recent). No mechanism axis collides. Its move, a closed group's departures read as a rank inside a rationed list against planned supply, shares nothing with task229.

## Strategy monoculture
The batch is the 12 builds ending at task229 in the guard's draw order: task121, task122, task124, task125, task126, task127, task128, task129, task130, task131, task228 and task229. Counts are read from the cards.

| Measure | Count | Cap | Verdict |
|---|---|---|---|
| Withheld rule with an official decoy | 0 of 12 | 2 | under |
| Certified-record decoy (`validated_decoy`) | **7 of 12** | 3 | **over, Strategy monoculture finding** |
| Any one `stump_strategy` | max 2 of 12 (identity_resolution, causal_design, binding_constraint) | 4 (a third) | under |

- **The seven builds carrying the certified-record decoy:** task121, task122, task124, task125, task126, task127 and task129.
- **Trend.** The count is 8 in the window ending at task131 and 7 in the windows ending at task228 and at task229. Corpus-wide, 47 of 129 cards carry it.
- **No change to task229 clears this.** The share reaches the cap only after four more flag-free builds enter the window, and the two-layer standard already blocks the flag on new draws.
- **task229.** It files `grain_or_unit`, with the decisive rule filed, no official decoy and no validated decoy, so it adds to neither capped count.
  - `uncertainty_hold` also fits the hardened driver (the decisive step is the noise unit, and its consequence is a hold). It is on no card in the corpus.
  - Neither key collides in the window or in the last three, so the choice changes no count and no ban.
  - If a reviewer files task131 and task229 together as one "unit of analysis" strategy, that is 2 of 12, still under the cap.

## Corpus habits
- **Recurring file names:**
  - `data_dictionary` in 61 builds and `export_manifest` in 33;
  - `data_notes` and `provenance` in 12 each;
  - `county_reference` in 4;
  - eight others in 3 each.
  - task229 uses none of them.
- **Recurring deliverable pairings:** pdf+csv 9, py 8, py+pdf 7, pdf+png 6, py+csv, py+xlsx and pdf+xlsx 5 each, docx 4. task229's json+png is not among them.
- **Recurring ask constructions:**
  - "give me the single dollar figure we" opens the ask in 2 builds.
  - A "Which of ..." ask appears in 5 builds (task85, task106, task119, task131, task229), two of them in the last twelve.
- **A mechanism-level habit is forming: "members are not independent because they share a parent".** It now carries the decisive premise in:
  - task106 (shared pool, overbooking);
  - task131 (shared budget, interference bias);
  - task229 (shared node, variance).
  - task54's ledger names its device the same way (event exposure).
  - The consequences differ in each, so no pair is a clone. But it is the premise the last draws keep reaching for, and the next draw is where varying it is cheap.
- **Data Quality Monitoring lane (task228 to task252).** Both lane builds share:
  - an alert that fires or holds;
  - `signal_vs_noise_or_hold`;
  - a JSON alert file beside a PNG;
  - a decisive step in what the alert's noise reference is built over (the forward run length; the unit of the error).
  - Two of two is not a finding. The lane's unbuilt seeds sit in the same family:
    - DQ04 (task231): averaged imputations understate the variance and over-fire.
    - DQ21 (task248): exceedance hours treated as independent events.
    - DQ23 (task250): a network false-alert budget.
  - The guard's text route scored task229 at 0.04 against everything on file, so it will not see that family. Those draws should be checked against task228's and task229's drivers by hand.

## What to redraw
1. task229: nothing.
2. Batch level, not task229: the certified-record decoy axis (`validated_decoy`), at 7 of 12 against a cap of 3, carried by task121, task122, task124, task125, task126, task127 and task129.

Coverage and tooling notes. These are not findings against any build.
- **(a) task228 Track A not run.** Its pack, prompt and note are on b228. Run `guard.py surface` or this screen with both builds on one checkout before ship.
- **(b) Stale caches.** The tracked clone-check cache and the people index both lack task228 and task229. Neither was refreshed in this run, by instruction.
- **(c) Consecutive by number.** The screen measures "consecutive" by task number, so it misses draw-order neighbours across the task131 to task228 jump.
- **(d) Card-only builds.** The screen cannot see task114 to task116 or task228.
- **(e) No packs for task117 to task129.** These have no pack on this checkout or the main one, so the screen's file-level hard tells cannot reach the batch's middle.
- **(f) Status regex.** It reads fiction text as delivery status (task48, task72).
- **(g) Text routes.** The driver-text routes (Jaccard 0.40; TF-IDF 0.12 and 0.30) did not reach any pair in the parent-unit family. Only the vocabulary sweep found them.
