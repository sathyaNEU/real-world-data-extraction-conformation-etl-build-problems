# Clone check: pre-flight on task230 against every other build, 2026-10-11

## Verdict
Idiom, Track A (a shared invented name): task84 vs task230 on "Larkspur", which task31 (failed) also uses. A rename clears it and the data survives. Track B is CLEAN: both promoted pairs read as clean, shares components by design.

## Scope and coverage
- **Mode and range.** Pre-flight on task230 against every other build, no window: task1 to task229 as filed, plus the card-only builds below. Repo root `/home/user/b230` (branch perssathya/task230-event-volume-drop). task228 is read from its working-tree architecture-2 card with its decisive code treated as G16, as instructed. task229 is read from the energy-systems card and design note on this worktree, which describe the architecture now being re-rooted.
- **Extract.** The cache, written at 11:23, was stale: task230's pack and task228's card had both changed since. I re-extracted it: 129 builds, 127 with a prompt or a pack. 19 are on this disk. Their prompts, write-ups and design notes were read today. Their packs came from `target/` for task130 to task133 and task230, from `target.zip` for task117, task119 and task229, and from the cached profile for the rest. The other 108 were fingerprinted on another checkout and kept from the cache. The refreshed `fingerprints.json` is left uncommitted in the worktree. It holds no profile of task228.
- **Pack screen** (`fingerprint.py screen --focus task230`): 126 pairs screened and 2 promoted (task229, task68). Both were adjudicated and none was left unread.
- **Card-level comparison.** Six builds have a card but no build on this disk and no cached profile: task114, task115, task116, task134, task135 and task228. They never enter the pack screen. I compared each with task230 on its card: Track B in full, and Track A only on what a card carries (world, invented names, personas, deliverables, shape).
- **Not compared.** task99 (scratch, excluded by design). task1 and task2 (no prompt, no pack, and no mechanism on their cards).
- **Mechanical cross-checks run:**
  - `guard.py heart task230`: WARN. repeat.decision against task229, repeat.deliverables against task135, and a NOTE test.same_driver_older against task68, which is differentiated.
  - `guard.py nearest`: the closest driver on file scores 0.07 (task129).
  - `voice-check.py 230`: no carrier wording and no unlisted repeats.
  - Text sweep of every card's driver, stump and lineage and every ledger row for task230's insight (staggered switch, not-yet-switched comparison, conditional parallel trends): no earlier build carries it.
  - Sweep of task230's invented names and personas across every card and the cache: one collision, "Larkspur" (Track A below).
- **One pair added outside the screen.** task84 vs task230 (with task31), on the shared name. Neither mechanical check can see it (see "What the mechanical checks missed").
- **Mechanism coverage of the 126 screened counterparts:**
  - 104 have a card mechanism layer: 90 native and 14 back-fitted (task11, task12, task25 to task36).
  - 5 are note-only (task16, task17, task20, task112, task113). Track B is not scored from cards for these. None was promoted, so none was read.
  - 17 are Track A only, with no mechanism recorded (task3 to task10, task13 to task15, task18, task19, task21 to task24).
  - The six card-only builds carry native cards.
- **Adjudication method.** The agent spec asks for one isolated subagent per pair. This run had no subagent tool, so all three pairs were adjudicated in the auditor's own thread. The inputs were the cards, the design notes' mechanism sections, the prompts, the submissions' solution steps, the ledger rows and the target listings. task68's folder is not on this disk and not in git history, so task68 was read through three things: its card (mechanism_source: design_note), its ledger row and its cached Track A profile.

## In batch against earlier builds
In pre-flight mode every other build is "earlier". None of task230's collisions lands on a build the ledger records as approved or delivered. The statuses below are taken from the record:
- **task84** (Larkspur). The ledger says: "Built and on disk ... no stump-check round run yet", with no portal result recorded. **Status unknown.** If task84 has been delivered, this Track A hit is exclusion-level exposure on its own (clone-check Part 2), so the rename is not optional.
- **task31** (Larkspur). The ledger says: "failed".
- **task68** (clean on reading). The ledger says: "BUILT 2026-09-04, REPAIRED 2026-09-05, ROUNDS HELD ... Nothing later recorded." **Status unknown.**
- **task229** (clean on reading). There is no ledger row. Its card and design note say it shipped to the author on 2026-10-11, and the orchestrator reports it is being re-rooted.

## Track A findings, reviewer visible

### 1. task84 vs task230 (and task31): shared invented name "Larkspur". Tier: Idiom (hard tell)
- **task230.** Larkspur is the hospital group's own tracking, which replaces Tallyfield. It appears in:
  - the prompt ("our own Larkspur tracking");
  - the spine's `tracker` values in `app_kpi_weekly_by_account.parquet`;
  - `app_release_history.csv` and `warehouse_export_notes.md`;
  - the write-up;
  - the generator (`world.py`, `docs.py` and others).

  task230 has no ledger row.
- **task84** (product analytics, root cause at a consumer dating app). Its card names the company and brand "Larkspur Labs" and "Larkspur", and its pack carries the name: the header of `growth_weekly_dashboard_2028-06-05.xlsx` reads "larkspur paid media, weekly, all ad accounts". Status unknown (see above).
- **task31** (supply chain). Larkspur is a supplier in its write-up and on its card. Status: failed.
- **Exposure.** task84 is in the same client domain as task230 and also files a designation_set, so a reviewer holding both product-analytics packages sees the same fictional brand in each. Nothing else is shared on Track A: no file names, schemas, seeds, wording or deliverable species. Track B is clean for both counterparts. task84's driver groups duplicate live units on a composite key (a decomposition). task31's driver is a censored approval lag.
- **Repair.** A rename of the tracking product in task230's generator, then a rebuild and a fresh `leak.py` pass, because documents in `target/` change. No figure, rung or ask moves, so the data survives. The card's `world.invented_names` follows the rename.
- **Why Idiom and not a higher tier.** Tiers are ordered by what the finding costs to answer, and a rename is the cheapest repair there is. The same name in three builds is also an authoring habit (Corpus habits). The guard's own rule treats a shared invented name as a draw-time BLOCK ("never produced by two independent draws"). It missed this one only because of the defect named below.

**Soft, below Shape echo, not a finding: task229 vs task230.** They are two consecutive Data Quality Monitoring builds set around a staged software release. Each designates a subset against a filed standard's three-unit line (three standard errors, three per cent), and both are anchored on the week of 5 October 2026. They share no file, schema, prompt or ask construction, or deliverable species, and the echo lapses when task229's re-root is filed. Nothing to redraw.

## Track B findings, mechanism
None. There is no Template, Dataset, Same seed or Exact finding. Both pairs the screen promoted on the mechanism route read as clean, shares components by design.

## Forward warning, not a finding: task229's re-root
The orchestrator describes task229's next architecture as a third-party logistics operator's stock-record accuracy gate. Accuracy over all locations is estimated from exception-triggered counts (partial verification, inverse-probability weighting), filed under general-statistics-data-science / missing-data-censoring-measurement-error x Data Quality Monitoring. No card or design note for it is on file, so this reads that one description only.
- **Where the drivers meet.** Both correct a non-random subset by weighting on what selected it.
  - task230 reweights a comparison pool to the switched units' band mix. The selection is into treatment timing, and the bias sits in a counterfactual trend.
  - The described design weights counted locations by the inverse of their chance of being counted. The selection is into observation, and the bias sits in a population rate.
  - Different estimand and different selection mechanism, so these are distinct drivers if the new card writes and keys them that way.
- **Where the cards would collide.**
  - test.same_driver fires if the new card keys a population gap, a decisive G6 (composition shift) and method_or_model_selection.
  - test.same_puzzle fires if it keys a population gap, G6 and designation_set.
  - A driver sentence phrased as "reweight a subset to the target mix" would read close to task230's.
  - The two builds will be adjacent in draw order, so the standing bans also apply between them. Against task230's card these are BLOCKs: the decisive code G6 (ban.pattern), shape 07, context artifact monitoring_export, role research_desk, stump strategy causal_design, forum funder_or_donor and org family hospital_or_health_provider. These are WARNs: designation_set, the Gate G mechanism method_or_model_selection and Ireland.
- **Axes to watch when the card is filed:** the decisive code and the driver sentence (selection into observation, not composition), and the decision type.
- **Draw-order blind spot.** `guard.py check` reaches only cards drawn earlier by (drawn date, task number). A re-filed task229 card dated 2026-10-11 sorts before task230, so its own registration check never meets task230. Any collision would surface on task230 at its next heart or `/approve` run instead. A card dated later meets task230 at registration.

## Clean, shares components by design

### task229 vs task230: consecutive. The screen flagged the same decisive gap (population) and the same decision type (designation_set)
- **Decisive moves, domain nouns stripped:**
  - task229 (the energy architecture on this worktree): a mean's standard error has to be built over the shared parent nodes its units fail through together. An error that treats the units as independent understates it severalfold for a group concentrated behind few nodes, and the alert fires on node noise.
  - task230: a switch reaches heavy users first, so its counterfactual trend has to come from not-yet-switched units in the switched units' own band (or the pool reweighted to their band mix). The whole not-yet-switched pool is a lighter mix whose trend runs harder.
  - **Same claim: no.** task229 turns on the unit a variance is built over (dependence). task230 turns on the bias of a comparison group (a confounded trend). Learning one does not prime a solver for the other.
- **Paths, in order:**
  - task229: (1) the standard's population (units on one version all week); (2) records held at the cut-off against every expected interval; (3) the mean per version; (4) **decisive**: the error built over nodes; (5) fire or hold against the reference less three errors.
  - task230: (1) patients only (service, dependant and merged accounts out); (2) handover and settled weeks; (3) each patient's reference level; (4) **decisive**: the counterfactual movement taken within the engagement band; (5) the settled change against the three per cent line.
  - The shared moves sit at steps 1 and 5 in both: assembling a filed population from a messy universe, and applying a filed line. They are routine in both builds and decisive in neither.
- **Shared components:**
  - the objective;
  - the population gap label, which means the unit of noise in task229 and the comparison population in task230;
  - time as the second gap;
  - designation_set;
  - a filed numbered standard;
  - "per active unit per period";
  - no calibration organ (by design on both sides, so not a shared choice).
- **Part 6.1.** Two of the three similarity-test axes repeat. The decisive pattern differs (D against G6), so the test passes. The decision-type repeat is the guard's WARN, already answered in task230's design note. Stump strategy (grain_or_unit against causal_design), Gate G mechanism, context artifact, role, shape, spine and domain all differ.
- **Status.** task229 has no ledger row and is being re-rooted.
- **Axis to redraw:** none.

### task68 vs task230: the screen flagged gap, decisive pattern (G6) and Gate G mechanism all colliding, the same-driver signature
- **Decisive moves, domain nouns stripped:**
  - task68: the qualifying change is a like-for-like change on a matched panel of the same continuing units, linked across identity successions, because entrant inflow and a price offset hold every aggregate flat. The basis and the bar are recovered from a closed corpus of 17 settled dispositions.
  - task230: as above.
  - **Same claim: no.**
    - task68 holds the unit set fixed across time: turnover and identity changes over a before-and-after window.
    - task230 holds a comparison group's band mix fixed in the same weeks, because selection into treatment timing is ordered by band.
    - task68 also rests on a recovered rule (pattern B and a closed corpus). task230 ships no calibration organ, and its estimand is filed (NPAP-STD-07 3.1 and 3.2).
- **Position.**
  - The move that decides task68 is comparing the same units against their own past. In task230 that move is a rejected rung (R2: switched patients against their own reference level, killed because the season belongs in B).
  - The identity-succession walking that supports task68's decisive rung reappears in task230 only on supplemental Ask A (merge chains in the weekly active patients count). It has been demoted from the decisive rung to an ask-layer device. That is reuse, not cloning.
- **What the cards share** is three broad labels (population, G6 composition shift, method_or_model_selection) plus the monitoring_export context artifact. G6 is the decisive code on six earlier cards (task20, task46, task68, task95, task114, task132) carrying six different drivers, so the label alone names no driver. task230's differentiation line against task68 is accurate.
- **Status.** task68 is built, repaired and rounds held, with no portal result recorded (status unknown). It is far outside every ban window.
- **Axis to redraw:** none.

### Also read on the cards, not promoted, clean
- **task228** (architecture 2, decisive code G16). Its driver is each unit's own error against an unobserved signal, identified from three independent measurements. It shares only the objective and the set_of_items answer unit. If the re-key also sets its Gate G mechanism to method_or_model_selection, task230 will draw a repeat.gate_g WARN against it at its next heart run. That is a label repeat, not a driver.
- **task134** (shape 07, population, method_or_model_selection). Its driver is a competing-risk cumulative incidence under censoring: decisive G16 against G6, with a different decision type and strategy.
- **task131** (shape 07, causal_design, method_or_model_selection). Its driver is interference at the randomisation unit, which is a different driver.
- **task132** (G6 decisive, population). Its driver is replacement renewal in a spares forecast.
- **task135** (pdf+xlsx, the guard's deliverables WARN). Its driver is retransformation bias. Nothing else is shared.
- **task114, task115, task116.** Only broad labels in common. "Tallybridge" (task116) and "Tallyfield" (task230) are distinct names.

## Strategy monoculture
The window is the last twelve draws ending at task230, in the guard's draw order: task127, task128, task129, task131, task130, task132, task133, task134, task135, task228, task229, task230.

| Cap (clone-check Part 3) | Count in window | Builds | Breached? |
|---|---|---|---|
| Withheld rule with an official decoy, cap above 2 | 0 of 12 | none (no card in the window files an official decoy) | no |
| Certified-record decoy (`validated_decoy`), cap above 3 | 2 of 12 | task127, task129 | no |
| Any one stump strategy, cap a third (4 of 12) | 2 of 12 at most | binding_constraint (task127, task128); causal_design (task131, task230) | no |

- Every other strategy appears once: composition_mix (task129), forecast_method_backtest (task130), population_selection (task132), stated_rule_hard_construction (task133), maturity_censoring (task134), other (task135), decomposition_attribution (task228 working-tree card) and grain_or_unit (task229 energy card).
- The decisive rule is filed in 8 of 12. It is not filed in task127, task130, task134 and task135.
- **Pending changes.** task228's re-key and task229's re-root each replace one entry. A cap is reached only if both land on binding_constraint or both on causal_design.
- **Watch, not a cap.** The Gate G mechanism method_or_model_selection is on 3 of 12 (task131, task134, task230). It becomes 4 of 12, a third, if task228's re-key sets it.

## Corpus habits
- **File roles:**
  - `data_dictionary` appears in 61 builds, `export_manifest` in 34, `data_notes` in 12 and `provenance` in 12.
  - task230 carries none of them. Its notes file is `warehouse_export_notes.md`, named in the organisation's own idiom.
- **Deliverable pairs:**
  - The most common pairs across the corpus are pdf+csv (9 builds), py (8), py+pdf (7), pdf+png (6), and py+csv, py+xlsx and pdf+xlsx (5 each).
  - task230 is one of the five pdf+xlsx builds. task135, three draws earlier, is another, which is the guard's repeat.deliverables WARN.
  - Across the twelve prompts the voice check can read on this disk (task124 to task133, task229, task230), xlsx appears in 7, pdf only in task230, and no build ships a Code deliverable.
- **Ask constructions:**
  - "give me the single dollar figure we" opens the Main Ask in 2 builds (not task230).
  - The voice check finds no calcified carrier wording and no unlisted six-word runs.
  - At 186 words, task230's prompt is the shortest of those twelve (median 248).
- **Opening move.** The voice check classes 9 of 12 openings as "other", task230 included even though its card says stakes-first. The concentration is in the classifier, not in the prompts.
- **Shape 07** (grid of cells) appears in 3 of the last twelve draws: task131, task134 and task230.
- **Invented names.** "Larkspur" appears in three builds: task31, task84 and task230.
- **Geography.** Ireland is the setting of five builds: task95, task100, task106, task115 (drawn 2026-10-08) and task230. Geography is not a ban axis.

## What the mechanical checks missed
These are defects to report, not fixes. Nothing was changed.
1. **`guard.py` tell.names compares only multi-word invented names.** `norm_names` keeps a name only if it contains a space, so a single-word fictional brand such as Larkspur never collides, even though the guard's own rule says a shared invented name is never produced by two independent draws.
2. **`fingerprint.py`'s entity axis reads prompt entities only.** A name that sits in one build's prompt and in another build's pack, card or write-up never reaches the hard-tell route.
3. **The extract only sees builds on this disk or in the cache.** It walks task folders that hold a `prompt.md` and keeps cached profiles from other checkouts. Builds whose packs live only on other worktrees and were never cached (task114, task115, task116, task134, task135, task228) never enter the pack screen and are compared on their cards only.

Noted in passing, outside the clone question:
- The DRAW table in task230's design note still says forcing `statutory_or_regulatory_filing`. The card says `other`, re-keyed at the heart check.
- The design note says Barry MacElgunn is "kept on the card", but the card's `world.people` lists three personas without him.

## What to redraw
1. task230: the invented name of its in-house tracking product ("Larkspur"). A rename in the generator; the data survives.
