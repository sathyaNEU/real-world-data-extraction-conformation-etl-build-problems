# Clone check: pre-flight, task132 (VPR-340 PSU last-time buy, architecture v1) against the whole corpus, 2026-10-11

## Verdict
CLEAN at every clone tier (no Exact, Same seed, Dataset, Template or Shape echo, and no Track B finding). The worst item is a soft Track A fiction-marker echo with task60, the invented name "Tamarack". A persona first name, "Susan", is also shared with task124 inside the guard's 12-build window. Both clear with a rename, and neither touches the ladder or the data.

## Scope and coverage
- **Mode and scope.** Pre-flight on task132 against every other build, with the window ignored, as `/build` stage 5 asked. task132 has one architecture (v1) and no lineage, so nothing is dropped as its own ancestor.
- **Extract.** The cache was stale: it was written at 01:22 and task132's files are from 02:05 to 02:17. I re-extracted.
  - 16 builds were fingerprinted from disk (task117 to task132).
  - 110 cached cards were kept for builds not on this checkout.
  - That gives 126 cards, 124 of them screenable.
- **Build changed during the check.** The leak-check stage edited and regenerated task132 while this check ran.
  - The prompt changed first: the lot size and the April 2024 reorganisation clause came out.
  - The pack was then regenerated: the target was rewritten at 02:31, and the card, design note, submission and `pipeline.json` at 02:32. The answer moved from 19 lots to 17, and the stump from 16 lots to 12.
  - I re-ran the extract, the screen, `voice-check.py` and `guard.py` heart, check and people on the current prompt, pack and card.
  - Every result below holds on the current build. Only two facts changed: the spine row count, and which files carry "Tamarack". Both are given as they now stand.
- **Screen.** `fingerprint.py screen --focus task132` found 123 pairs in scope and promoted 2:
  - task130: surface 0.100, 98th percentile, promoted as top 3 percent of consecutive builds.
  - task83: surface 0.137, 99th percentile, plus the same decisive gap label.
- **Guard checks.** `guard.py check` PASS (the Part 6.1 bans against task129 to task131 included). `guard.py heart` PASS, nearest driver task46 at 0.08. `guard.py people` raised no issue.
- **Builds compared: 130 counterparts.**
  - 123 by the screen.
  - task1 and task2: their cards carry drivers, but the cache has no prompt or target for them. They were reached only through the heart's driver-text comparison and my driver sweep.
  - task114, task115 and task116: cards only. Their folders are on neither this checkout nor the carried cache. I compared them by hand from the cards on both tracks (driver, strategy, gap, decision, deliverables, spine, world, invented names, people). No pack-level Track A was possible.
  - task99: excluded by the script as a scratch slot. That is correct, because its card records it as the August build whose design note is headed task31 (the R5 state of task31's world). I read its card driver in the censoring sweep anyway.
  - task133: the parallel build in this lane, in its own worktree (`/home/user/wt133`).
    - Its card was registered at 02:24 today, during this check. It has no prompt or pack yet.
    - I compared it by hand from its card on both tracks.
    - That worktree's copy of the task132 card is byte-identical to this one, so task133's own guard sees the current task132.
- **Pairs adjudicated: 9.**
  - **Promoted by the screen:** task130 and task83.
  - **Promoted by me on the mechanism route:** task46 (the heart's nearest driver), task133, task122, task33 and task114. The screen's mechanism route cannot fire for this card, for three reasons:
    - task132's pattern is `none`, and its decisive generator G12 sits in the decisive position on no other card, so the pattern axis cannot collide.
    - That leaves gap plus decision type, which tops out at two of three. Two of three promotes only between consecutive builds. The five pairs at two (task93, task101, task104, task109, task120) are 12 to 39 builds back.
    - The driver route is a lexical Jaccard, and its highest score against task132 is 0.13 (task97).

    So I swept every card driver, lineage driver and ledger mechanism cell for exposure, truncation, censoring, observation-window, survival, age-band, failure-rate, spares and last-time-buy vocabulary, and adjudicated what the sweep surfaced.
  - **Promoted by me on Track A tells the screen cannot see:**
    - task60: an invented name in the packs, not in the prompts.
    - task124: a persona first name. The guard's people index cannot see task124's pack.
- **Read at the card-driver level and dismissed with a named reason (see Clean):** task31 (with its R8 censoring lineage), task99, task91, task59, task85, task55, task50 (v3 lineage), task73 (v2 lineage), task101, task56, task57, task76, task25, task28, task109, task120, task93, task104, task115 and task116.
- **Unread: 121 pairs, none of them promoted by the screen.** The six nearest unpromoted surface neighbours are task108, task57, task37, task50, task111 and task32, at the 81st to 93rd percentile. They score on flat layout and format mix only, with masked submission overlap of 0.006 at most. That is corpus idiom.
- **How adjudication was done.** This thread had no subagent tool, so I read the nine pairs here, one at a time. I asked each one the per-pair adjudicator's questions: the decisive move with the domain nouns stripped, the ordered path and where the shared moves sit, the tier, the track, and the one axis to redraw.
  - **task132's side:** its card, design note, current prompt, submission blocks 1 to 3 with the step list, and target listing.
  - **Counterparts not on this checkout** (task46, task60, task83, task33, task114): the fingerprint card (driver, concrete driver, stump, lineage, differentiation) and the ledger row.
  - **Counterparts on this checkout:** task130, task122 and task124 from their design notes and `pipeline.json`. task133 from its card.
  - I opened no golden or answer key on either side beyond the design notes and task132's submission blocks.
- **Mechanism coverage, over the 124 screenable builds including task132:**
  - 102 have a card mechanism layer (88 native, 14 back-fitted).
  - 5 are note-only (task16, task17 and task20 back-fitted; task112 and task113 native).
  - 17 have no mechanism layer (task3 to task10, task13 to task15, task18, task19 and task21 to task24, all back-fitted).
  - 34 carry back-fitted labels.
  - Track B was scored from cards on 101 pairs. 22 pairs were Track A only on the screen. 20 of those 22 cards still carry a driver sentence, which the heart and my sweep reached. task112 and task113 have no card and no ledger row, and their design notes are not on this checkout, so their mechanism is unavailable.
- **What was not checked: target packs for 15 counterparts are not profiled on this checkout.** These are task3, task10 and task117 to task129 (`task*/target/` is gitignored until delivery). Byte-identical files, same-seed tables, schemas and file names were therefore not screened against those builds; their prompts and submissions were. To compensate:
  - task132's generator reads nothing outside `task132/` (only its own target and metadata).
  - No card shares task132's spine (`eam_work_orders_protection_2021-01_2026-09.csv`, 26,654 rows after the rebuild, work-order grain).
  - No card shares a deliverable name or stem beyond common words.
  - No card shares an invented name, except the "Tamarack" token below.
- **Status record.** The ledger has no row for task132, which is correct while it is in flight, and none from task109 onwards. Where the ledger is silent I give the counterpart's `pipeline.json` state and say so.

## In batch against earlier builds
This is a pre-flight, so every pair is task132 against an earlier build or against the parallel task133. The screen labels the two promoted pairs "in batch" because focus mode sets the window to the whole corpus. That is a labelling quirk, not a scope bug.

- **No hit against an approved or delivered build.** No Track A or Track B hit lands on any build the ledger records as approved or delivered (task25, task27, task28, task29, task30, task33, task34, task35, task48 and task72). The nearest of them:
  - task33 shares one component (see Clean).
  - task25 and task28 share only the `population_selection` strategy label.
  - task34, task48 and task72 share only the gap label `population`, the corpus's most common decisive gap.
- **Builds delivered on pipeline state only.** task130 (delivered 2026-10-11) and task131 (2026-10-10) are recorded as delivered to the author in `pipeline.json` while the ledger is silent. Both are clean against task132, and the Part 6.1 bans against task129 to task131 pass in `guard.py check`.
- No exclusion-level exposure exists for task132.

## Track A findings, reviewer visible

**1. task132 against task60: shared invented name "Tamarack".** Soft. On its own it sits below every tier in clone-check Part 3. The screen's shared-invented-name tell reads prompts only, and neither prompt carries the word.
- **Status.** task60 is live on the ledger (v8, rebuilt 2026-08-31, lives at `handshake/task60/`), with no delivery recorded. task132 is in flight. The two are 72 builds apart.
- **Shared surface.**
  - task60's fiction is the US state of Tamarack. Its card lists "Tamarack Department of Education", "Tamarack Industry Credential Incentive" and "Tamarack Career and Technical Education Association".
  - task132's utility is "Tamarack Hydro Distribution". In the regenerated pack it appears in `AM-PC-014_obsolete_spares_final_buy.docx`, in `eam_extract_dictionary.txt` (as "TAMARACK") and in the golden memo `psu_last_time_buy_memo.docx`. The rebuild took it out of `substations.csv` and the programme workbook.
  - No other card carries the word.
  - The entities differ (a state against a utility), and nothing else in the two worlds overlaps (a USD state agency against an Ontario CAD distributor). This is a fiction-marker echo, not a reskin.
- **Clears it.** Rename the utility (task132's `world.invented_names`) in the generator's world constant, the golden and the card together. No ladder change. The data survives, because no figure depends on the name, and the generator's checks re-assert every figure on the rebuild.

**2. task132 against task124: persona first name "Susan".** Soft, and only persona furniture. By the guard's own rule it is a BLOCK, but the guard could not see it.
- **Status.** task124 is in flight per its pipeline state (stage 3, hardened, not delivered; the ledger is silent). It is 8 builds back in draw order, inside the 12-build persona window.
- **Shared surface.**
  - task124's card and design note name Susan Kelley, chair of the risk committee. task132's signatory is Susan Huff, named in the prompt and in the memo.
  - Both worlds are electricity businesses: a Texas retail electricity provider and an Ontario distribution utility. That makes the repeat easier to notice.
  - `guard.py people` blocks a first name already used in any build inside the last 12. Its index, however, reads personas from files on this checkout. task124's pack and goldens are not here, so the index holds only Gregory Sheppard for task124.
  - Whether Susan Kelley appears in task124's shipped files cannot be confirmed here. Its card lists her as one of its personas.
- **Clears it.** Redraw the signatory persona's first name with `guard.py names --geo "Canada, Ontario" --seed 132`, changing the prompt, the memo and the card together. No ladder change, and the data survives.

**Not findings:**
- **task83** (surface rank 1, 0.137) shares the deliverable species (an xlsx workbook with a docx memo), flat layout and part of the format mix. That pairing is in 6 corpus builds and is the plainest business pair there is.
- **task130** (rank 2, 0.100) shares only flat layout and the same set of target formats. Masked prompt overlap is 0.002.
- **Across all 123 screened pairs:** no pair shares a target file name, a schema, a same-seed table, a byte-identical file, an ask skeleton or a step skeleton.
- **`voice-check.py 132`:** no carrier wording and no unlisted repeated runs. 249 words against a 12-build median of 253.

## Track B findings, mechanism
**None.** No counterpart turns on task132's decisive move. Each near neighbour is set out under Clean, with its driver difference named.

## Clean, shares components by design

**task132's decisive move, domain nouns stripped:** "Units entered service long before the outcome record begins, so the rate per unit of exposure in each age band has to count only the exposure the record can see (each unit enters the risk set at the later of its entry and the record's start); counting from entry dilutes the bands those units passed through unrecorded."

**task132's path, in order:**
1. Failures as the filed procedure defines them, each in its relay's age band.
2. Relay-months per band from January 2021. This is the decisive move.
3. Each relay's end of support from the approved programme sheet.
4. Band rates over the forward relay-months (the age mix the horizon brings).
5. Usable stock.
6. The smallest whole lot count whose Poisson cover reaches 95 per cent.
7. The price.
8. The call.

Steps 1, 3, 4, 5 and 6 are filed in AM-PC-014. The decisive move is the one construction the procedure does not write.

**1. task46 (live on the ledger: R1 and R2 valid stumps, repaired, awaiting re-review): clean_shares_components.** It is the closest mechanism neighbour in the corpus.
- **task46's decisive move:** "Age has to be measured on the clock that drives the outcome, cumulative time in use rebuilt from a movement record in which stored time does not accrue, not time since build, so the rate law becomes stationary and a cohort crossing a step before the window opens shows."
- **Same object, different claim.**
  - In both builds, the decisive move constructs the exposure behind an age-banded failure-rate law. That law is rolled over an ageing fleet to size a forward commitment, and the natural route underbuys.
  - task46 changes the time scale: which clock age runs on. That moves units between bands and takes stored time out.
  - task132 keeps the plain installation age and changes only where the risk set opens, with a single calendar cut.
  - A solver primed by one build is not primed for the other. Rebuilding a service clock does not clip at the history start, and clipping at the history start does not rebuild a service clock.
- **Position.** task46's path runs the roster with its executed schedule, then the rebuilt service exposure (decisive), then the service-age rate law, then the roll over the roster with the 2018 cohort crossing the eight-year step, then an election in increments of 1,000. The shared moves (a band rate law, a forward roll over a scheduled fleet, a whole-increment election) sit around the decisive step in both builds. In task132 they are filed, so the shared frame is reuse.
- **Outline.** One of the four Shape echo axes is shared: the decision (a forward buy from a failure burden). The other three differ:
  - deliverables (py+pdf against xlsx+docx);
  - calibration organ (physical verification against none);
  - ask construction (masked prompt overlap 0).

  That is below Shape echo.
- **For the next draw.** The exposure denominator of an age-banded failure-rate law that sizes a forward buy now carries the decisive rung in two builds. A third build whose decisive rung sits on that denominator would be a Template candidate whatever its domain. The guard scores this pair at 0.06 to 0.08, so it will not flag one.

**2. task133 (in flight in the parallel worktree, card only, data not cut; ledger silent): clean_shares_components.**
- **task133's decisive move:** "A filed cumulative outcome curve runs from each unit's entry, and every unit in scope has already survived part of it, so its forward probability is the curve's remaining increment divided by its own survival to date."
- **Same family, different claim.** The family is where each unit's clock starts relative to the record.
  - task132 is delayed entry on the estimation side: the rates are estimated, and the exposure is clipped.
  - task133 is conditioning on the application side: the curve is filed and correct, and the forward probability is conditioned on survival to date.
- **Everything else differs:**

  | Axis | task132 | task133 |
  |---|---|---|
  | Strategy | `population_selection` | `stated_rule_hard_construction` |
  | Gap | population | time |
  | Decisive generator | G12 | G9 |
  | Decision | dial_setting | quantity_figure |
  | Shape | 04 | 02 |
  | Deliverables | xlsx+docx | xlsx+pptx |

  The domain and world differ too. task133's card already files this differentiation against task132.
- **For the batch.** Both were drawn on 2026-10-11 in the same lane, so they will likely reach a reviewer in the same batch. This report does not ask task132 to move. task133's own pre-flight, while its data is still uncut, is where the pair gets judged from its side.

**3. task130 (ledger silent; pipeline state delivered to the author 2026-10-11): clean, shares a component.** The screen promoted it on surface (flat layout and the same format set).
- **Shared component.** A filed programme that reaches each unit on a schedule ends that unit's forward window.
  - In task130 that is the decisive rung: a household leaves only when the rationed lets reach its rank in its size's list.
  - In task132 it is a filed lookup, at step 3 of 8: each substation's commissioning month on the approved 2026 sheet, with the superseded 2025 sheet as Layer 1 mess.
  - The device was demoted, so this is reuse.
- **Driver difference.** task130's R3 rung (a Kaplan-Meier survival curve) is a wrong path there, and task132 fits no survival curve. The decisive claims differ (queue rank against cumulative supply, against delayed entry), as do the shape (02 against 04), the decision and the deliverables (xlsx+png against xlsx+docx). The Part 6.1 bans pass.

**4. task83 (live on the ledger, RE-ROOT 2.1, no portal result for the current architecture): clean, shares a component.** The screen promoted it on surface (deliverable species) plus the gap label.
- **task83's decisive move:** condition a randomised holdout's measured effect on each unit's own prior treatment history, because the target pool's mix on that axis differs from the measurement corpus.
- **Shared component.** A composition shift between the measurement record and the forward pool (G6 on both cards).
  - In task83 it is decisive.
  - In task132 the forward age mix is the filed procedure's own method: band rates applied to forward relay-months, the move from rung 2 to rung 3, below the decisive rung.
  - Demoted, so this is reuse.
- **The shared `population` gap label** names different populations: a treatment-history stratum against an exposure window.

**5. task33 (approved on the ledger): clean, shares a component.** This is the one delivered build with anything in common.
- **Shared component.** A forward window that stops at a filed per-unit date: task33's filed intervention and task132's programme month.
- **Position.** task33's own stump sentence has the competent solver already truncating at filed interventions, and task132's solver reads the programme month as filed. The device sits below the decisive rung in both.
- **Driver difference.** task33's driver is a measured elevation that scales with the expected forward path. Nothing on its path is an exposure window.

**6. task122 (ledger silent; pipeline state retired 2026-10-10 after a Gate G send-back, not submitted; history): clean.**
- **Shared abstraction only:** an outcome record that covers a narrower window than the quantity being estimated.
- **Different moves.** task122 recovers orders placed after the session closed, which the log credits to a new session (numerator attribution through the listing). task132 removes exposure the record could not have seen (denominator restriction). The positions differ, and the colliding side is dead.

**7. task114 (ledger silent, card only, status unknown): clean.** It is the nearest outline neighbour on the cards.
- **Shared outline:** Canada and CAD, shape 04, dial_setting, capacity_planner and population_selection.
- **Differences.**
  - The driver differs entirely: task114 turns on demand that exists only when two or more parties are at the same site.
  - The deliverable species (xlsx+svg), the calibration organ (prior-period close-out against none) and the forum differ.
  - Its prompt is not on this checkout, so the ask sentence could not be compared.

  Below Shape echo on everything that can be checked.

**Dismissed by the driver sweep, with no shared decisive claim:**
- **Censoring family.**
  - task31's R8 lineage (failed) and task99 (the scratch slot, same world): a duration estimated from a log whose slow cases are still open, kept as right-censored (Kaplan-Meier by stratum). That is right censoring of durations, not delayed entry into a rate's exposure.
  - task91 (live): units too young to have begun exiting read as dormant. That is an onset age, not an observation window.
  - task59: each new episode is capped at the weeks it can draw before the window closes, which is the forward edge.
- **Window or clock.**
  - task85: each unit's own window opens at its own third-party relationship start. That is a comparability rule, not record coverage.
  - task55: which date each unit's expiry runs from.
  - task50, v3 lineage: a slow-surfacing failure mode projected with a run-out law.
  - task73, v2 lineage: an age mix in a served share, which in task132 is the filed band method.
- **Label neighbours.**
  - task56 carries G12, but for an inner join that drops a population known only by its absence.
  - task101, task109, task120, task93 and task104 share the gap label and dial_setting, with unrelated drivers.
  - task25, task28, task57, task76 and task116 share the `population_selection` label, with unrelated drivers.
  - task115 shares only the objective and the Gate G mechanism.

## Strategy monoculture
The batch is the last 12 builds in draw order ending at task132: task119, task121, task122, task124, task125, task126, task127, task128, task129, task130, task131 and task132. The counts come from the cards' fields.

| Measure | Count | Cap | Verdict |
|---|---|---|---|
| Withheld rule with an official decoy | 0 of 12 (task119 and task122 carry `official_decoy`, both with the decisive rule filed) | 2 | under |
| Certified-record decoy (`validated_decoy`) | **7 of 12** | 3 | **over, Strategy monoculture finding** |
| Any one `stump_strategy` | max 2 of 12 (decomposition_attribution, identity_resolution, causal_design, binding_constraint) | 4 (a third) | under |

- **The seven builds carrying the certified-record decoy:** task121, task122, task124, task125, task126, task127 and task129.
  - task122 and task125 are retired per their pipeline state, though the ledger is silent on both. Without them it is 5 of 10, still over the cap.
  - Over the last 15 it is 10 of 15.
- **task132** is `population_selection`, with the decisive rule filed, no official decoy, no validated decoy and calibration form none. It adds to neither capped count and is the only `population_selection` in the window. task133 (next, card filed) carries neither decoy either.

## Corpus habits
- **File names.**
  - `data_dictionary` appears in 61 builds and `export_manifest` in 33.
  - `data_notes` and `provenance` appear in 12 each, and `county_reference` in 4.
  - Eight more names appear in 3 builds each.
  - task132 uses none of the habit names: its dictionary is `eam_extract_dictionary.txt`, and it has no manifest and no provenance file.
- **Deliverable pairings.**
  - Corpus-wide: pdf+csv 9, py alone 8, py+pdf 7, pdf+png 6, py+csv 5, py+xlsx 5, pdf+xlsx 5, docx alone 4.
  - xlsx+docx is in 6 builds (task83, task105, task107, task118, task125, task132). In the last 12 it is 2 (task125, which is retired, and task132).
  - xlsx and docx each appear in 6 of the last 12.
- **Opening moves.** voice-check files 6 of the last 12 under `other`, task132 included, though its card says constraint-first. That is the classifier's coverage, not the prose. There is no carrier wording and no 6-word run shared by a third of the batch. The repeated ask opening "give me the single dollar figure we" (2 builds) is not task132's.
- **Persona furniture.**
  - The first-name rule cannot see personas in packs that are not on this checkout (task117 to task129), which is how the "Susan" repeat passed the guard.
  - Two electricity-business worlds sit in the last 12 (task124 and task132). The org family utility_or_infrastructure is at 2 of 12.
- **The time-origin family.** task46 (service clock), task132 (delayed entry) and task133 (conditioning on survival to date) all put the decisive step on where a unit's clock starts, or on what time counts toward it.
  - The drivers differ in each pair, and no tier is breached.
  - The guard's lexical driver overlap scores these pairs at 0.06 to 0.12, well under its 0.40 line. The next draw in this family needs reading by hand.

## What to redraw
1. task132: nothing on Track B. The draw, the ladder and the data stand.
2. task132, Track A rename: the utility's invented name, "Tamarack Hydro Distribution", which echoes task60's fictional state of Tamarack. Generator world constant, golden and card together.
3. task132, Track A rename: the signatory persona's first name, "Susan", which repeats task124 inside the 12-build window. Prompt, memo and card together.
4. Batch, not task132: the certified-record decoy axis (`validated_decoy`), at 7 of 12 against a cap of 3, carried by task121, task122, task124, task125, task126, task127 and task129.

**Bookkeeping and tooling notes (none of these is a finding):**
- One task132 card field is stale after the rebuild. The `driver` still says the forward total is "low by about a sixth", but the design note's ladder now puts the install-exposure rung 27.6 per cent low (12 lots against 17). The card's `stump`, `driver_concrete`, the design note and `pipeline.json` all agree on 12 lots against 17. The magnitude is the author's to correct, and it does not change any comparison here.
- The screen cannot see cards whose builds are absent from both this checkout and the carried cache (task114 to task116), or cards filed in a parallel worktree (task133).
- The shared-invented-name tell reads prompts only, so a fiction marker that lives in the packs, like "Tamarack", does not promote a pair.
- `guard.py people` indexes personas from files on disk, not from the cards' `world.people`. Personas in gitignored packs are invisible to it.
- For a card whose pattern is `none`, the mechanism route fires only on gap plus decision type between consecutive builds, or on lexical driver overlap. The time-origin kinship above sits far under the overlap line.
