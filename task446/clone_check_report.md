# Clone check: pre-flight, task446 (architecture 2) against every build, 2026-10-11

## Verdict

Shape echo, soft (Track A only): task446 against task133. Both are 30 September 2026 bank credit-deterioration packages, and they ship near-identical IFRS 9 Q3 2026 scenario workbooks. There is no Exact, Same seed, Dataset or Template finding, and Track B is clean.

## Scope and coverage

- **Scope resolved.** Pre-flight on task446, architecture 2: the 2027 watch-list caseload, forecast from an early-warning screen whose hit rate moves with the base rate. It is compared against every build on file, task1 to task447, with no window. The caller also asked for two extra comparisons:
  - task446's own spent architecture 1, taken from the card's `lineage` and from the architecture-1 design note at commit 336598d.
  - In-flight task447, read-only from `/home/user/wt-task447`.
- **Stage 1, extract.** The cache was stale: task446's design note, submission, goldens, metadata and pack were all newer than it. It was re-extracted to 130 cards. 20 were fingerprinted from this branch's folders and 110 were carried over from the cache as profiled on other checkouts.
- **This branch is behind main on two builds that matter here:**
  - task181: its own commits mark it shipped after a portal round, and its card is not on this branch.
  - task130 v3: recorded retired on main in e98e2b0. This branch still holds the v2 folder.

  Both were fingerprinted from the local main checkout, and task447 from its own worktree, into a scratch copy of the cache. The screen and the guard were run on that augmented set. The tracked cache was refreshed from this branch's builds only.
- **Stage 2, screen.** 130 builds were screened, giving 129 pairs with task446. None was promoted on any route:
  - No byte-identical file, no same-seed table and no shared invented name. Halstow Bank plc, Jill Berry and Mathew Long appear in no other build.
  - The highest surface score is 0.100, at the 98th percentile (task57 and task123). That is below the 99th, and neither build is consecutive.
  - No pair collides on gap, pattern and decision family together. 16 pairs collide on two of the three, and none of them is consecutive.
  - Card driver overlap is at most 0.13 (task447), against the 0.40 trigger.
- **Guard checks.**
  - `guard.py heart` compares against every card, lineage driver, stump and ledger row. The nearest heart text is at 0.05 and the nearest driver at 0.07 (task57 v19).
  - The structural check is PASS on this branch's card set and WARN on the full set (`overuse.gate_g`, see Strategy monoculture).
  - `voice-check.py task446`: no carrier wording, no unlisted repeated run, 888 characters.
- **Stage 3, adjudication.** 5 pairs were read:
  - The 2 the caller named: task446 v1 and task447.
  - 3 the auditor added from the cards. The screen's mechanism route keys on exact labels, so it can miss a relabelled driver.
    - task95: the closest transported-mix driver on file.
    - task133: same client domain, same as-of date, a filed credit model, drawn the same day.
    - task130 v3: the other forecast_method_backtest build in the last twelve draws, built around a flagged cohort.
  - The drivers of the rest of the transported-mix family (task44 v2, task97, task20, task228 v1) were read beside task95, at card level.
  - **No subagent tool was available to this run, so the auditor did all five reads in one context.** Each read used both cards, the design notes, the prompts and the target listings. task95 was read from its card alone, because its folder is on another machine. Answer keys were read only as far as the ladder figures that place each move.
- **Left unread.** 124 screened pairs. None was promoted, none has a hard tell, none collides on all three mechanism axes, and driver overlap is under 0.14 throughout. That is proximity, not a finding. It includes the six nearest surfaces the screen lists: task57, task123, task132, task111, task51 and task65.
- **Mechanism coverage.**
  - 108 of the 130 screened builds carry a card mechanism layer. 14 of those have back-fitted labels (task11, task12, task25 to task36). 34 builds numbered task36 or below are back-fitted in all.
  - 22 builds were Track A only in the screen:
    - note-only: task16, task17, task20, task112, task113;
    - unavailable: task3 to task10, task13 to task15, task18, task19, task21 to task24.

    20 of those 22 still had their card drivers compared by text in the guard.
  - 10 builds were checked through their cards only, with no Track A, because no local checkout holds their pack: task1, task2, task99, task114, task115, task116, task134, task135, task228 and task230.
  - task447 has no pack yet, so its Track A is the prompt alone.
- **Two gaps in the screen itself.**
  - task99 is dropped by the scratch rule in `fingerprint.py`, where `EXCLUDE_DIRS` matches `^task99$`, even though a real build's card is filed under that number. The guard covered it here.
  - The screen's consecutive-build routes compare task numbers, and numbers are now allotted in lane blocks, so they no longer follow draw order. task446's draw-order neighbours task228 to task230 and task133 to task135 do not count as consecutive to the screen. The guard's draw-order bans covered them, and they passed.
- **Seen outside this scope, not adjudicated: task445 and task181.** task445 is from this lane and shipped. task181 is on main and is marked shipped after a portal round. At card level they carry the same-driver signature:
  - decisive gap time, decisive generator G12, calibration form censored_or_lagged_release, and stump strategy maturity_censoring;
  - drivers that both say a count read before all its records have arrived must be completed unit by unit from each unit's own arrival history, not scaled by a pooled completion rate.

  Neither branch carried the other's card through its own checks, and neither build has a ledger row. A `/clone-check` on task445 is the check that decides it.

## In batch against earlier builds

Pre-flight has no batch, so this section covers task446 against every earlier build. There is no collision at exclusion level. Ledger rows run to task108, and nothing against any of those builds was promoted or read as a hit. The one finding is the soft Track A echo against task133. It is below exclusion level, and task133's status is unknown because it has no ledger row.

## Track A findings, reviewer visible

**task446 against task133: Shape echo, soft, Track A only.**

- **Status.** task446 is in flight (pre-flight). task133's status is unknown (no ledger row). The two were drawn the same day, seven draws apart.
- **Shared outline.**
  - Both are bank credit-risk packages as at 30 September 2026. Of the prompts readable here, these are the only two that name that date.
  - Each sends one forward credit-deterioration figure to a board or committee meeting (23 October and 4 November).
  - Each delivers a workbook plus one visual: xlsx with pptx, and xlsx with svg.
- **Shared literal surface.** Both ship an IFRS 9 scenario workbook for the same quarter, with near-identical names and titles. They are the only two of 132 profiled packs that carry such a file.
  - task133, on its solution path: `ifrs9_scenarios_2026Q3.xlsx`, titled "IFRS 9 / AASB 9 forward-looking scenarios, reporting date 30 September 2026".
  - task446, a declared distractor: `ifrs9_macro_scenarios_2026q3.xlsx`, titled "IFRS 9 forward-looking scenarios, 2026 Q3 run".

  The contents differ (2 columns by 14 rows on two sheets, against 17 by 58 on five), so this is not Same seed or Dataset. The screen's exact-name file axis cannot see it.
- **Not shared.** The ask construction, the calibration organ, the geography and lender, and the driver (see Clean).
- **What clears it.** Rename and retitle task446's distractor so it no longer echoes task133's file. Because it is a distractor, no rung, figure or path moves. The cost is the generator, the distractor list in `metadata.json`, and a leak re-sweep. What remains after that (domain, quarter-end and decision shape) is domain-native and below a finding.

**Observed and not a finding.** task445 and task446 are adjacent in the lane, and both open on "twelve" and a watchlist: "the twelve names on Harrowby Point's crowding watchlist" and "Twelve groups is what one watch-list analyst carries". The sentences are built differently, the masked screen puts the pair at the 17th percentile, and both uses are native to the domain.

## Track B findings, mechanism

None. No pair shares the driver:

- Gap, pattern and decision family never collide together.
- The same-driver signature (gap, pattern and Gate G mechanism together) fires nowhere.
- The nearest drivers on file sit at 0.07.
- Each of the five reads below names a different decisive move.

No redraw is needed, so the data survives as cut.

## Clean, shares components by design

**task446's decisive move, with the domain nouns stripped.** A screen's yield, the share of flagged units that turn out positive, moves with the year's base rate. So the forward count has to come from the screen's two error rates, which hold across years: solve the share now flagged for the base rate.

**task446's solution path:**
1. Conform entity signals to groups.
2. Build four closed cohorts with outcomes.
3. Measure hit, miss, capture and false-alarm rates.
4. Back-test which rates carry across cohorts (decisive).
5. Solve the flagged share for the base rate (decisive).
6. Split by exposure band and conform the exposure (asks).

### 1. task446 v2 against its own architecture 1

Requested. History only: v1 was spent at in-house round 1 and never shipped.

- **v1's move.** A forward projection for a group as constituted on the projection date needs its whole history restated on that membership, because point-in-time joins book membership changes as growth. This is a different claim.
- **Shared components.**
  - The GLEIF roll-up of entities to obligor groups.
  - The UK bank world and a 4 November committee.
  - Three of v2's four ask devices: the superseded scheduled run, the late booking-entity file, and rates quoted per pound.
- **Position.** The membership-date choice was v1's decisive rung. In v2 the standard files point-in-time membership, and the GLEIF texture sits on entities that never signal, so mishandling it moves nothing (asserted). The device has been demoted, not repeated, so the re-root did move the driver.
- **On the record, though not a clone question.** v1's round-1 solver cracked every ask device, including these three.
- **Verdict:** `clean_shares_components`. Nothing to redraw.

### 2. task446 against task447

Requested. Both are in flight and both are shippable.

- **task447's move.** A transfer rate measured on earlier units operates only in one stratum of an attribute reached through a join, so the earlier units' stratum mix has to be replaced by the target unit's before the rate is applied.
- **Why it is a different claim.** task447 conditions on an observed moderator and re-weights. task446 has no moderator to find, because the class is the outcome itself. Its move is to carry P(flag | outcome) instead of P(outcome | flag) and solve for the hidden base rate.
- **Shared, at construction level in both and not decisive.**
  - A rate measured on earlier populations that does not transport.
  - An entity-to-owner roll-up as Layer 1: GLEIF consolidation in one, TIN, NPI and ownership channels in the other.
- **Different outline.**
  - A count against a go-or-hold call.
  - xlsx plus svg against one pdf.
  - Shape 05 against shape 07.
  - Calibration on the bank's own cohorts against a natural experiment.
- **Verdict:** `clean_shares_components`.
- **Lane note.** These are back-to-back builds in one lane, and both turn on a rate measured on past units that fails to carry. A third such driver in this lane would read as a theme.

### 3. task446 against task95

Added by the auditor. task95's status is unknown (no ledger row). Read from its card only.

- **task95's move.** A conversion rate that reproduces every closed period is a weighted average over two classes. The forward period's class weight, recovered by differencing two dated events across two registers, sits far outside the record. So convert class by class at the forward weights.
- **Same family, different claim.**
  - task95 is forward mixing: the forward weights can be recovered, and the solver re-weights.
  - task446 is the inverse: the observable forward quantity is the mixture (the flagged share), and the unknown is the weight (the base rate), solved through the class-conditional rates.
- **The record works differently.** task95's blended rate reproduces the closed years, which makes it a validated decoy. task446's hit rate fails its own one-cohort-out back-test (-35.6, +15.4, +40.7 and +9.5 per cent), so the record refutes the naive model.
- **Card axes.** The gap order matches (time, then population). The pattern does not (A against none, with G16 decisive), and neither does the decisive rung.
- **The rest of the family.** task44 v2, task97, task20 and task228 v1 sit in the same transported-mix family. Each re-weights to an observed mix, and each differs from task446 in the same way. task446's own design note already rejected a deposit-retention candidate as carrying task44 v2's and task97's driver.
- **Verdict:** `clean_shares_components`.

### 4. task446 against task133

Added by the auditor. task133's status is unknown.

- **task133's move.** A cumulative outcome curve runs from each unit's entry, and every unit in scope has already survived part of it. So each unit's forward probability is the curve's remaining increments divided by its own survival to date.
- **Why it is a different claim.** task133 turns on survival conditioning along a filed curve. task446 turns on the base-rate dependence of a screen's predictive value.
- **Shared.**
  - The client domain.
  - A filed credit model whose output has to be handled correctly for today's book.
  - Decisive gap time, quantity_figure and Gate G forecasting.
  - The Track A outline reported above.
- **Verdict:** `clean_shares_components` on Track B. The soft Track A echo stands on its own.

### 5. task446 against task130 v3

Added by the auditor. History only: task130 is recorded retired on main (e98e2b0) and has no ledger row.

- **task130's move.** A group chosen for an extreme value of a noisy outcome regresses toward the mean. So its next period is forecast from an earlier group chosen the same way and left untreated, not from its own selection-period value.
- **Shared device, in opposite positions.** Both builds use earlier cohorts flagged by the same model and observed afterwards.
  - In task130, that earlier cohort's realised outcome is the answer.
  - In task446, the earlier cohorts' realised yield is the trap rung: R0, 74 against 134. The answer comes from the same cohorts' error rates.
- Same strategy label (forecast_method_backtest), different insight.
- **Verdict:** `clean_shares_components`.

## Strategy monoculture

**Window:** the twelve draws ending at task446, in draw order, on the full card set: task131, task130, task132, task133, task134, task135, task181, task228, task229, task230, task445 and task446. Read from each card's stump_strategy, decisive_rule_filed, official_decoy and validated_decoy fields, counted as declared.

| Strategy | Share | Builds |
|---|---|---|
| maturity_censoring | 3 of 12 | task134, task181, task445 |
| causal_design | 2 of 12 | task131, task230 |
| forecast_method_backtest | 2 of 12 (1 live) | task130 v3 (retired), task446 |
| population_selection | 1 of 12 | task132 |
| stated_rule_hard_construction | 1 of 12 | task133 |
| decomposition_attribution | 1 of 12 | task228 |
| grain_or_unit | 1 of 12 | task229 |
| other | 1 of 12 | task135 |

**Against the caps:**
- **Withheld rule with an official decoy:** 0 of 12, against a cap of 2. No card in the window declares an official decoy.
- **Certified-record (validated) decoy:** 0 of 12, against a cap of 3. On this branch's card set, which lacks task181, the window still includes task129, which makes it 1 of 12.
- **Any one strategy in a third of the batch:** no. The largest is maturity_censoring at 3 of 12. That is the guard's warn level, and task446 does not carry it.

Adding in-flight task447 (composition_mix) moves none of this.

**Adjacent concentration, not one of the three caps.** Gate G mechanism `forecasting` appears in 6 of the 12: task130, task132, task133, task135, task181 and task446. The guard raises this as `overuse.gate_g` once main's task181 card is on file. This branch's own guard run lacks that card and returns PASS.

## Corpus habits

- **File roles.** `data_dictionary` names the dictionary in 61 builds, `export_manifest` appears in 34, and `provenance` and `data_notes` in 12 each. task446 uses none of them: its dictionary is `credit_data_field_reference.md` and its provenance record is `reference_data_extract_log_20261008.txt`.
- **The role line.**
  - 42 of the 115 profiled prompts state the asker's role in a first-person sentence: "I run" in 23, "I head" in 6, "I lead" in 5, "I direct" in 3, "I chair" in 2, "I manage" in 2 and "I own" in 1.
  - "I head <unit>" appears in task120, task122, task124, task126, task445 and task446.
  - With in-flight task447, it closes three consecutive builds in this lane, each time as a short bare sentence: "I head ownership research here.", "I head credit risk monitoring.", "I head market oversight."
  - The voice check only reports repeated runs of six words or more, so it cannot see this.
- **Deliverable pairs.** pdf+csv appears in 9 builds, py alone in 8, py+pdf in 7 and pdf+png in 6. task446's xlsx+svg is uncommon: svg appears in 3 of the last 12.
- **Ask openings.** Two Main Asks open with "give me the single dollar figure we". task446's does not.
- **Layer 1 in this lane.** All three ETL builds so far conform entities to a parent through an ownership hierarchy:
  - managers filing under several CIKs (task445);
  - the GLEIF consolidation hierarchy (task446);
  - TIN, NPI and ownership channels (task447).

  That is the objective's natural work, and none of the three rests its stump on it. But a reviewer holding the lane's batch will see the same conformance move three times.

## What to redraw

1. **task446, the distractor workbook `ifrs9_macro_scenarios_2026q3.xlsx`:** its file name and title line. Track A, the soft Shape echo against task133. Rename only; no figure or rung moves.
2. **task446, the closing role sentence "I head credit risk monitoring.":** Idiom, prompt wording only.

No Track B redraw is needed, and the data survives both changes.
