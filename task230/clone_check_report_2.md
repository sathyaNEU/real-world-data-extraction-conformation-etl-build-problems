# Clone check: pre-flight on task230 (architecture 1, hardening loop 1) against every other build, 2026-10-11

## Verdict
Idiom, Track A. Two of task230's personas reuse first names from builds inside its twelve-draw window: Sandra (task130, retired, and task127, retired according to its pipeline) and Erica (task126, status unknown). On this merged checkout, `guard.py heart task230` returns BLOCK on people.first against task130, not the WARN the build agent recorded. A rename clears it and the data survives. Track B is CLEAN. No other card or ledger row carries the loop-1 driver, and all six pairs I adjudicated read clean, shares components by design.

## Scope and coverage
- **Mode and range.** Pre-flight on task230 against every other build, with no window. The corpus is the 135 cards on file: task1 to task135 (with gaps), task228, task229, task445 and task230's own card. task99 is scratch and excluded. Repo root is `/home/user/orch/aud230`, a detached worktree of perssathya/task230-event-volume-drop at 6a1d6be with origin/main merged at 475a62f. task230's `target/` was copied in from the current build. Since 475a62f, main has changed only an author rule and one status line: no card, ledger row or tooling.
- **Extract.** The committed cache was stale. It held no entry for task230 or task445, so I re-extracted it:
  - 130 entries, 128 with a prompt or a pack.
  - 20 builds are on this disk and were re-read: task117 to task133, task229, task230 and task445.
  - Where their packs came from: `target/` for task130 to task133 and task230; `target.zip` for task117, task119, task229 and task445; the cached profile for task118 and task120 to task129.
  - The other 110 entries were fingerprinted on another checkout and kept from the cache. Every one of their cached card fields matches the card on file today.
  - The refreshed `fingerprints.json` is left uncommitted in the worktree.
- **Pack screen** (`fingerprint.py screen --focus task230`): 128 builds, 127 pairs, 2 promoted (task229 and task68, the same two as pass 1 and as `guard.py surface`). Both were adjudicated and none was left unread.
- **Read beyond the screen** (four more pairs):
  - task228 and task135, which carry the guard's WARNs;
  - task445, the draw-order neighbour after task230;
  - task129, which has the nearest driver on file and the closest component overlap.
- **Card-level comparison.** Six builds have a card but no pack on this disk and no cached profile: task114, task115, task116, task134, task135 and task228. I compared them on Track B in full and on Track A only on what a card carries (world, invented names, personas, deliverables, shape).
- **Mechanism coverage of the 127 screened counterparts:**
  - 105 have a card mechanism layer: 91 native and 14 back-fitted (task11, task12, task25 to task36).
  - 5 are note-only (task16, task17, task20, task112, task113).
  - 17 are Track A only on the screen (task3 to task10, task13 to task15, task18, task19, task21 to task24). Their cards carry no gap or pattern labels. Their driver sentences were text-swept, and none was used for a Track B call.
  - task1 and task2 have no prompt or pack. They were compared on their driver sentences only.
- **Mechanical cross-checks run on this checkout:**
  - `guard.py check`, `heart` and `surface task230` all return **BLOCK**: people.first, Sandra against task130. The three WARNs are as reported: repeat.gate_g against task228 (v2), repeat.decision against task229 and repeat.deliverables against task135. There are two NOTEs: test.same_driver_older against task68 (differentiated), and driver.near at 0.50 against the slot's own loop-0 lineage (differentiated).
  - Nearest text on file: the heart's nearest is task119's stump at 0.06 and task129's at 0.05. `guard.py nearest` puts the nearest other driver at task129 (0.06).
  - `voice-check.py 230` and the bare run: 964 characters and 167 words, ECONOMY clean, no carrier wording, no unlisted repeats.
- **Sweeps:**
  - A text sweep for the loop-1 insight, run over every card's driver, stump, driver_concrete, analyst_test, notes and lineage, and over every ledger row. It searched for eligibility to be treated, never-treatable units, not-yet-treated or never-switched pools, minimum OS, staggered or phased rollout, comparison or control pool, positivity and take-up. No earlier build carries the insight.
  - A persona sweep against every card's `world.people`.
  - An invented-name sweep against every card, the cache and the on-disk generators and packs.
  - A parquet schema check (see "What the mechanical checks missed").
- **Adjudication method.** The agent spec asks for one isolated subagent per pair. This run had no subagent tool, so all six pairs were adjudicated in my own thread. The inputs were the cards, the design notes (task229, task230, task129), the prompts, the submissions' solution steps, the ledger rows, the pipeline files and the target listings. No golden deliverable was read for the adjudication. The persona and name sweeps read files mechanically.
  - task68's folder is not on this disk, so it was read through its card (mechanism_source: design_note), its ledger row and its cached Track A profile.
  - task228 and task135 were read on their cards only.

## In batch against earlier builds
In pre-flight mode every other build is a counterpart. task445 is the only one drawn after task230. None of task230's collisions lands on a build the ledger records as approved or delivered. The ledger has no row for any build after task108, so every status below beyond the ledger's silence is quoted from the build's own records and labelled as such:
- **task130** (persona Sandra Lopez). Retired: PR #36, and its pipeline.json reads "retired: three architectures spent". It never ships, so this is history, not exposure.
- **task127** (persona Sandra Rodriguez). Ledger silent. Its pipeline.json reads "retired".
- **task126** (persona Erica Ryan). Ledger silent, so **status unknown**. Its pipeline.json reads "built", approved in-flow on 2026-10-10 and not delivered.
- **task229** (clean on reading). Ledger silent, so status unknown. Its pipeline.json reads shipped and delivered on 2026-10-11. Per the orchestrator, the architecture on its card failed the portal's determinism QC and is spent. Design 2 is paused and unregistered.
- **task68** (clean on reading). The ledger reads "BUILT 2026-09-04, REPAIRED 2026-09-05, ROUNDS HELD ... Nothing later recorded". No portal result, so status unknown.
- **task445** (clean on reading). Ledger silent, so status unknown. Its pipeline.json reads stage 8 shipped, delivered 2026-10-11, and it is on main. Even if it is delivered, task230 shares no reviewer-visible surface with it (see below).
- **task228** (clean, label repeat only) and **task135** (clean, deliverable pair only). Ledger silent. task228's card describes architecture 2, which is spent.

## Track A findings, reviewer visible

### 1. Persona first names recycled inside the twelve-draw window. Tier: Idiom
**The pair surface.**
- **task230 personas:**
  - Sandra Fitzpatrick is the requester and the prompt's "I". She appears in `npap_prenotice_request.eml` (To and salutation), in the "Submitted by" line and file properties of `npap_q3_2026_return_drumlee.xlsx`, and in both goldens (the workbook's "Prepared by" line and the cover note's From line).
  - Erica Phayre is the programme's data lead. She appears in the email's From and signature, in the last-modified-by of `npap_return_definitions_2026.docx`, and in the cover note's To line.
  - Lesley Ahearne is clear.
- **Earlier builds, all inside task230's last twelve draws:**
  - task130 has Sandra Lopez in `target/care_management_services_agreement_schedule_c.pdf` and `golden/baseline_certification_memo.docx`.
  - task127 has Sandra Rodriguez on its card and in `generator/params.py` ("finance director"). Its pack is not on this disk.
  - task126 has Erica Ryan on its card and in `generator/docs.py`. Its pack is not on this disk.
- No surname and no full name is shared.

**Why the mechanical verdicts differ.** `guard.py check`, `heart` and `surface` all BLOCK on Sandra against task130. The build agent's WARN was produced at 2ec7922 (17:06). task130's v3 pack only reached this branch in the merge of origin/main at 17:20 (6a1d6be, after PR #36 at 17:19). I verified that the pack is absent at 2ec7922 and present at 6a1d6be.

The guard cannot see Erica against task126 or Sandra against task127. Its people index is built from prompts, submissions and the narrative files of packs, plus entries cached from other checkouts, and it never reads a card's `world.people`. The committed index lists only Thomas Kennedy for task126 and only Sara Duncan for task127. Neither pack is on this disk, so I cannot check here whether Erica Ryan or Sandra Rodriguez reaches reviewer-visible text in it. By the cards, both are personas of those builds, and under the same rule (a first name used in a recent build) both would be BLOCKs too.

**Exposure.** task130 never ships, and task127 is retired according to its pipeline. task126's status is unknown. A common first name with a different surname is furniture, not a fiction marker. The cost is the one CLAUDE.md names: the same first names recurring across a batch a reviewer holds.

**Pipeline consequence.** Stage 5's mechanical half ("guard.py heart not BLOCK") is not met on the merged checkout until this is renamed.

**Repair.**
- Draw two replacement first names with `guard.py names --geo Ireland --seed <n>`. Then check them by hand against every card's `world.people`, because the names tool reads the same blind index and could hand Erica back.
- Update the card's `world.people`, rebuild the pack and the goldens, and re-run `leak.py`, because documents in `target/` change.
- No figure, rung or ask moves, so the data survives.

### Soft, below Shape echo, not a finding: task229 vs task230 (unchanged from pass 1)
These are two consecutive Data Quality Monitoring builds set around a staged software release (firmware waves; an app update met at sign-in). Each designates a subset against a filed standard's three-unit line, and both are anchored on the week of 5 October 2026. They share no file, schema, wording, invented name or deliverable species, and the surface score is 0.080 (corpus percentile 60), resting only on flat layout and format mix. The echo lapses when task229's design 2 (a third-party logistics warehouse) is filed. Nothing to redraw.

Everything else on Track A is clear:
- The invented names Dunnock, Drumlee, Tallyfield and NPAP (National Patient App Programme) appear on no other card, in no cached prompt, submission or file name, and in no other on-disk generator or plain-text pack member.
- Larkspur, pass 1's finding, survives only in the design note's history line and pipeline.json.
- task230's six nearest surface neighbours (task126 at 0.100 down to task85 at 0.090) score on flat layout and format mix alone.

## Track B findings, mechanism
None. There is no Template, Dataset, Same seed or Exact finding.

The loop-1 driver is: a staggered switch's counterfactual is read from not-yet-switched units inside the band that orders adoption, but that pool fills week by week with units that can never switch and whose trend runs harder, so the pool has to be held to units able to switch. It sits on no other card, lineage entry or ledger row. The closest relatives each carry a different insight:
- task129: a hidden per-record state, separating two causes.
- task124: analogs whose measured value was held down by an intervention.
- task134: competing exits removing units from risk.
- task68: a matched panel of continuing units.
- task107 v2 (retired): a comparison arm contaminated through reassigned staff.
- task121 v1 (an unregistered draft): exposure that drains as units are struck.

## Clean, shares components by design

### task229 vs task230: back to back by number and in draw order (the screen's promotion, and the repeat.decision WARN)
The screen flagged the same decisive gap (population) and the same decision type (designation_set). The card on file is task229's spent energy architecture.
- **Decisive moves, domain nouns stripped:**
  - task229: a mean's standard error has to be built over the shared parent nodes its units fail through together. An error that treats the units as independent understates it severalfold for a group concentrated behind few nodes, and the alert fires on node noise.
  - task230: a staggered switch's counterfactual has to come from not-yet-switched units that are able to switch, inside the band that orders adoption. Inside each band the not-yet-switched pool fills week by week with units that never can switch, whose trend runs harder.
  - **Same claim: no.** One is the unit a variance is built over (dependence among units). The other is the eligibility of a comparison group (bias in a counterfactual trend).
- **Paths, in order:**
  - task229: (1) records held at the cut-off; (2) each unit's running release; (3) the filed population (one release all week); (4) the mean per build; (5) units grouped by parent node; (6) **decisive**: the error over nodes, with the limit at the reference less three errors; (7) wave counts; (8) fire or hold.
  - task230: (1) the filed population and the handover weeks; (2) reference levels and settled weeks; (3) the phone class against 7.0's minimum; (4) **decisive, with 3**: the counterfactual movement taken from same-segment patients still on 6.8 whose phones can take 7.0; (5) the settled change against the three per cent line; (6, 7) the asks; (8) the call.
  - The shared moves sit at the same routine positions in both: assembling a filed population from a messy universe, and applying a filed three-unit line. Neither is decisive in either build.
- **Part 6.1.** Two of the three similarity-test axes repeat, but the decisive pattern differs (D against G6), so the test passes. Strategy (grain_or_unit against causal_design), Gate G, shape, context artifact, role, forum and org family all differ.
- **Status.** The card's architecture is spent and failed at the portal, so the WARN lands on a dead row: history.
- **Tier, track, axis:** clean, shares components, Track B. Axis to redraw: none.

### task68 vs task230: the same-driver signature on the cards (the screen's promotion, and the NOTE test.same_driver_older)
The cards share the gap (population), the decisive code (G6), the Gate G mechanism (method_or_model_selection) and the context artifact (monitoring_export).
- **Decisive moves, domain nouns stripped:**
  - task68: a change has to be read like for like on a matched panel of the same continuing units, linked through identity successions, because entrants and an offset hold every aggregate flat. The basis and bar are recovered from a closed corpus of settled dispositions.
  - task230: as above.
  - **Same claim: no.**
    - In task68 the composition shift is entry into an aggregate over time, and the fix holds the unit set fixed.
    - In task230 it is never-switchable units accumulating in a control pool as the eligible ones leave it, and the fix excludes them from the comparison in the same weeks.
    - task68 also rests on a recovered rule (pattern B and a closed corpus). task230 files its estimand (NPAP-STD-07 3.1 and 3.2) and ships no calibration organ.
- **Paths:**
  - task68, from its card and ledger row: (1) the latest accepted version of each line; (2) traders walked through successions; (3) **decisive**: the matched unit-by-heading panel; (4) the like-for-like change per chapter; (5) basis and bar recovered from 17 dispositions; (6) name the chapter.
- **Position of the shared moves.**
  - "The same units against their own past", task68's decisive move, is task230's rejected R2.
  - Identity-succession walking, which supports task68's decisive rung, is a device on task230's Ask A (merge chains).
  - Both have been demoted, which is reuse, not cloning.
- **Label count.** By the guard's decisive-mechanism rule, G6 decides only task20, task68 and task132 besides task230, each on a different driver. The card's loop-1 differentiation line against task68 is accurate.
- **Status:** unknown (no portal result). It is far outside every ban window.
- **Tier, track, axis:** clean, shares components, Track B. Axis to redraw: none.

### task228 (architecture 2, spent) vs task230: the repeat.gate_g WARN
- **Decisive moves, stripped:**
  - task228: each unit's own error against an unobserved signal is separated by a three-way covariance of independent measures. Where two comparators share an input their errors co-vary, so a fourth independent series is needed there.
  - task230: as above.
  - **Same claim: no.**
- **Shared:** only the Gate G label and the objective. Shape, gap, decisive code, strategy, decision, world and personas all differ.
- **Status:** the card describes the spent architecture, so the WARN is history.
- **Axis to redraw:** none.

### task135 vs task230: the repeat.deliverables WARN
- **Decisive moves, stripped:**
  - task135: a prediction from a regression fitted on the log scale, exponentiated, is the conditional median, which understates the mean by a factor that grows with the residual spread, segment by segment.
  - task230: as above.
  - **Same claim: no.**
- **Shared:** the xlsx plus pdf deliverable species, a stakes-first opening, and no calibration organ (by design on both, so not a shared choice). Their ask shapes differ (a forecast total against a grid of flags).
- **Context:** pdf+xlsx is one of the five commonest pairs in the corpus. Among the twelve prompts on this disk, a pdf ships only in task230.
- **Status:** unknown.
- **Axis to redraw:** none.

### task445 vs task230: the draw-order neighbour after (drawn the same day, higher number)
- **Decisive moves, stripped:**
  - task445: a period total still held by reporters whose reports have not arrived has to be completed reporter by reporter from each one's last report. Reading the arrived reports, or scaling by one aggregate completion share, misstates the units whose holders report late and changes which units cross the threshold.
  - task230: as above.
  - **Same claim: no.** One is late arrival in a total. The other is the eligibility of a comparison pool.
- **Shared labels:** designation_set against a filed threshold, method_or_model_selection, and population as a gap label (second on task445). G6 also appears as one of task445's non-decisive generators.
- **Track A:** surface 0.016, in the bottom tenth of task230's 127 pairs. No shared file, schema, name or wording. Shape 03 against 07, csv+png against xlsx+pdf, question-first against stakes-first.
- **Where the WARNs land.** Because task445 is drawn after task230, the label repeats are its own WARNs (repeat.gate_g and repeat.decision against task230), not task230's.
- **Status:** unknown on the ledger.
- **Axis to redraw:** none.

### task129 vs task230: the nearest driver on file (0.06) and the closest component overlap (not promoted)
- **Decisive moves, stripped:**
  - task129: two causes that switched on together are separated by groups that each got one, but each cause's effect depends on a per-record state no column carries. The separating groups are mostly one state and the target population mostly the other, so reweighting the state-conditioned effects moves the joint effect from one cause to the other.
  - task230: as above.
  - **Same claim: no.**
- **Shared components and their positions:**
  - Both have a software change switched on cohort by cohort.
  - Both condition a comparison on a device class. In task129, CPU-class standardisation through the device registry is the partial correction inside rung 2, the stump's own step. In task230 the phone attribute measures eligibility at the decisive rung.
  - Both reweight a comparison group to a target mix. In task230 that move is R4', a sibling of the stump rung.
  - Conditioning on device platform, the closer analogue of task129's move, stays on task230's stump flags (design note, "the data's own case" 7). The device has been repurposed from mix to eligibility, and it does not hand over task230's answer.
- **Status:** unknown (its pipeline reads stage 2, design).
- **Axis to redraw:** none. The shared world is noted under Corpus habits.

### Also read on the cards, clean
- **task124:** analogs held down by an intervention. A transport draft of task230 was blocked against it and never registered. Loop 1 uses phone age as an eligibility gate, not as an effect modifier.
- **task131:** interference at the randomisation unit.
- **task132:** G6 and population, but replacement renewal in a spares forecast.
- **task134:** competing exits under censoring.
- **task130 v3:** regression to the mean in a selected group (retired).
- **task114, task115, task116:** broad labels only.

## The card against the decisive rung
The card honestly describes the rung that the design note (stump sentence, LADDER R4 to R5, "the data's own case" 1 to 7) and the submission (steps 3 and 4) describe.
- **driver:** accurate. It keeps loop 0's within-band step as the premise and turns on the pool filling with units that never can switch. That is R5 against R4, with the flag errors running in both directions: R4 files appointment change requests and notification opens and clears appointment views and test result views.
- **gap:** population first is right (the not-yet-switched pool is not the counterfactual population), and time second (the winter season, the forward Q4 flag) is right.
- **pattern:** `none` with G6 decisive is right, because the pool's composition drifts week by week (22 to 25 per cent on phones below the minimum in W42, 28 to 49 by W46). The notes call G17 "confounding", but the vocabulary's G17 is statistical rigor. This is a text slip with no effect on any check.
- **stump_strategy:** causal_design fits, because the vocabulary names "control or comparison choice" there. composition_mix and population_selection would be defensible but less specific. None of the three appears in task230's last three draws, so no key choice dodges a ban.
- **Layer 2:** estimand_identification fits (the vocabulary lists staggered adoption). The `own:` pattern key is defensible. The library's nearest entries each carry one piece and none states the combined insight that a not-yet-treated pool inside a stratum fills with never-treatable units:
  - product-analytics/observational-causal-inference/1: condition on pre-adoption engagement. That is loop 0's rung, now R4.
  - product-analytics/observational-causal-inference/2: a staggered rollout read against not-yet-treated units. That is task230's R3.
  - product-analytics/feature-adoption-diffusion-modeling/2: a staged rollout's rates need the eligible base.
  The notes cite only the first. Naming feature-adoption-diffusion-modeling/2 as well would make the key's claim checkable.
- **The rest are consistent:** stump, analyst_test, domain_test, answer, the decoy flags (no official or validated decoy) and the task68 differentiation line.
- **Stale text, not keyed:**
  - `slot_note` still frames the slot by loop 0's mix driver.
  - `niche` omits the minimum OS, which the design note's DRAW niche carries.
  - pipeline.json records heart as WARN, which is the pre-merge verdict.
- **world.people:** see the Track A finding.

## Forward warnings, not findings
**task229 design 2** (paused and unregistered). I read it only from the orchestrator's description, because no card or design note is on this checkout. The distinction the build agent drew holds at the mechanism level:
- **task230's move:** every unit's outcome is observed. The bias sits in a counterfactual trend, and the repair excludes never-treatable units from the comparison pool, with no weights.
- **Design 2's move, as described:** uncounted locations' outcomes are unobserved. The bias sits in a population rate, and the repair reweights every counted location by its chance of being counted.
- **Loop 1 widened the gap.** The generic move both share (condition or reweight on what drives selection) was task230's decisive rung at loop 0. It now sits at R4 and R4', the stump rung. If design 2's answer is that reweighting, the shared move is wrong in one build and right in the other: reuse, not cloning.
- **When the distinction would stop holding:**
  - if design 2's decisive step turned on locations that can never be counted (a zero-probability stratum that has to be handled apart), which is task230's insight on the observation side;
  - or if its driver described the counted set as filling over time with a kind of location.
- **Card collisions.** A design-2 card dated 2026-10-11 sorts before task230, so its own registration check never meets task230, and the collision would surface at task230's next heart or /approve.
  - BLOCK there if it keys: decisive G6, causal_design, shape 07, monitoring_export, research_desk, funder_or_donor, or hospital_or_health_provider. Also BLOCK on test.same_driver (population, G6, method_or_model_selection) or test.same_puzzle (population, G6, designation_set).
  - WARN on designation_set and method_or_model_selection.

**task228 architecture 3** (no card yet: per-station data-quality rates over very unequal exposure, a next-season watch list, regression to the mean).
- **Driver:** distinct from task230's (noise and regression toward the mean in units picked on extremes, against the eligibility of a comparison pool).
- **Card collisions.** A card dated 2026-10-11 sorts before task230 and inside its last three draws, so collisions land on task230's next heart:
  - The vocabulary lists regression to the mean under causal_design. If architecture 3 keys causal_design, task230 inherits a BLOCK (ban.strategy). If it keys shape 07, that is a second BLOCK (ban.shape).
  - method_or_model_selection keeps the existing repeat.gate_g WARN.
  - uncertainty_hold ("power or sample size") may be the honest strategy key for shrinkage over unequal exposure. The author's choice there decides whether task230 is blocked.
- **Outside task230:** the nearest driver on file to that description is task130 v3's regression-to-the-mean baseline (retired), so the guard's driver check will meet it there. That is history, not exposure.

**Seed DS45 (task391, unassigned), low priority.** Its world, integrations stranded on a retiring version, with minimum OS and SDK versions among its mirrors, shares task230's "units that cannot move to the new version" element. Its driver (a minimum over sub-units) differs. It is also product analytics, so the pairing ban already applies within three draws.

## Strategy monoculture
These are the last twelve draws ending at task230, in the guard's draw order: task127, task128, task129, task131, task130, task132, task133, task134, task135, task228, task229, task230.

| Cap (clone-check Part 3) | Count | Builds | Breached? |
|---|---|---|---|
| Withheld rule with an official decoy, cap above 2 | 0 of 12 | none | no |
| Certified-record decoy (`validated_decoy`), cap above 3 | 2 of 12 | task127, task129 | no |
| Any one stump strategy, cap a third (4 of 12) | 2 of 12 at most | binding_constraint (task127, task128); causal_design (task131, task230) | no |

- **Strategies seen once each:** composition_mix (task129), forecast_method_backtest (task130), population_selection (task132), stated_rule_hard_construction (task133), maturity_censoring (task134), other (task135), decomposition_attribution (task228's spent card) and grain_or_unit (task229's spent card).
- **Decisive rule not filed:** 4 of 12 (task127, task130, task134, task135).
- **The twelve ending at task445:** causal_design 2 and maturity_censoring 2 (task134, task445). Validated decoy 1 (task129).
- **Pending:** each re-root replaces one entry. causal_design reaches 3 of 12 only if task228 architecture 3 keys it, which would also BLOCK task230 (above).
- **Watch, not a Part 3 cap:**
  - Gate G method_or_model_selection is on 4 of 12 ending at task230 and 5 of 12 ending at task445, so the next draw meets the guard's overuse.gate_g WARN.
  - designation_set is the decision type of three draws running (task229, task230, task445).

## Corpus habits
- **File roles.** `data_dictionary` appears in 61 builds, `export_manifest` in 34, `data_notes` in 12 and `provenance` in 12. task230 uses none of them. Its notes file is `warehouse_export_notes.md` and its definitions are the programme's own docx.
- **Deliverable pairs.**
  - The commonest pairs are pdf+csv (9 builds), py (8), py+pdf (7) and pdf+png (6), then py+csv, py+xlsx and pdf+xlsx (5 each).
  - task230 and task135 are two of the five pdf+xlsx builds.
  - Across the twelve prompts on this disk, xlsx ships in 6, pdf only in task230, and no build ships a Code deliverable.
- **Prompt surface.**
  - The voice check finds no carrier wording and no unlisted repeats.
  - "give me the single dollar figure we" opens 2 builds (not task230).
  - task230 is 964 characters, the second shortest of the twelve (task130 is 933).
  - The classifier puts 9 of 12 openings in "other", task230 included, although its card says stakes-first. That concentration is in the classifier.
- **Batch composition.**
  - Shape 07 is on 3 of the last twelve draws (task131, task134, task230).
  - Data Quality Monitoring is the objective of three draws running (task228, task229, task230), and both re-roots stay in that objective.
  - A staged software release sets three of the last twelve worlds: task129 (a redesign switched on cohort by cohort), task229 (firmware waves) and task230 (an app update).
- **Personas.** First names recur inside the window: Sandra (task127, task130, task230) and Erica (task126, task230). This is visible only by reading cards, because the guard's people index does not read them.
- **Geography.** Ireland sets five builds: task95, task100, task106, task115 and task230.

## What the mechanical checks missed
These are defects to report, not fixes. Nothing was changed.
1. **The people index never reads a card's `world.people`.** It reads prompts, submissions and the narrative files of packs, plus its own cache. A persona that a card lists but the index never found in narrative text (task126's Erica Ryan and task127's Sandra Rodriguez, both in their generators) is invisible to people.first and to `guard.py names`, which can therefore redraw it.
2. **`fingerprint.py` does not profile parquet.** It records no rows, schema hash or numeric signature, so the same-seed and schema axes are blind to parquet spines, including both of task230's main tables.
   - A schema-only check of those two tables against every parquet file in the on-disk packs (task117, task119, task131, task133) found at most one shared column (`iso_week`, with task131).
   - The 110 cache-only builds' parquet files were never profiled.
3. **The screen's consecutive and adjacent flags use task numbers, not the guard's draw order.** task445 is next after task230 in draw order but not "consecutive" to it, and task130 sits between task131 and task132 in draw order.
4. **Still present from pass 1:**
   - `tell.names` compares only multi-word invented names.
   - The entity axis reads prompt entities only.
   - Builds whose packs live only on other worktrees (task114, task115, task116, task134, task135, task228) are compared on cards alone.
   - A re-rooted card dated the same day with a lower task number (task228 architecture 3, task229 design 2) never meets task230 at its own registration.

## What to redraw
1. task230: the first names of two personas, Sandra Fitzpatrick and Erica Phayre. This is a rename in the generator, checked by hand against every card's `world.people`; the data survives.
