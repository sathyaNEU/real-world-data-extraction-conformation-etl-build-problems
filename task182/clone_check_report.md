# Clone check: pre-flight, task182 against every other build, 2026-10-11

## Verdict

Shape echo (Track B, soft flag, not reject tier), task182 against task228 architecture 2. There is no Exact, Same seed, Dataset or Template finding, so stage 5 passes on the clone check.

## Scope and coverage

**Scope.** This is pass 1, a pre-flight on task182 (architecture 1: built, leak-checked, not yet solved) against every other build, with the window ignored. "Every other build" was resolved to every build with a fingerprint card or a reachable pack, each at its latest committed state as of about 17:00 UTC.

**How the corpus was assembled.** Everything was read-only. Scratch copies are under `/home/user/oviya-notes/cc-task182/`. The tracked cache and this branch's cards folder were not touched.
- **This branch.** It carries task117 to task133, task182, task229 and 136 cards. Its last merge of main is PR #30.
- **Main is ahead of that merge.** task230's card, and task445's card and pack, exist only on main. task445 is called shipped in main's commit messages but has no ledger row.
- **Stale cards on this branch.**
  - Its task228 card is the retired architecture 1.
  - Its task180 card is an older copy of architecture 3; the forum and notes have since changed.
  - Current versions were used instead: task228 and task230 from main, and task180 from the main checkout.
- **task180** (architecture 3) was read in place in the main checkout.
- **task181** was read at `d6944e3`, as instructed.
- **Other authors' builds in flight.** These were read from a blobless clone of origin made in scratch, so nothing was fetched into the shared repository.
  - Packs: task134, task135, task228 (architecture 2, hardening loop 2), task230 and task446.
  - task130 and task133 at their harden branch tips.
  - task229's card from its rework branch.
  - The task253 and task254 cards. Both are at the draw stage with no prompt.
- **task1 to task113.** Their profiles come from the cached extract, made on another checkout. No cached mechanism field differs from its card.

**Extract.** `fingerprint.py extract` produced 137 build profiles: 27 extracted here and 110 carried over from the cache. The script was copied byte-identical into the scratch corpus so that it reads the assembled cards. The final set is 141 cards.

**Screen.** `fingerprint.py screen --focus task182` screened 135 builds and 134 pairs, and promoted 4. task1 and task2 drop out because they have no prompt and no pack profile.

**Card-only builds.** task99, task114, task115, task116, task253 and task254 were scored with the screen's own Track B card rules. None was promoted. task99's card carries no gap or pattern.

**Draw order.**
- The screen measures adjacency by task number. The guard measures it by drawn date, then task number.
- By the guard's key, task228 is the draw immediately after task182, yet it is 46 numbers away.
- Applying the screen's card rules in draw order promotes task228: the decisive gap and the decisive pattern both collide, on the adjacent draw.

**Promoted, adjudicated, left unread.** 5 pairs were promoted (task180, task83, task130 and task132 by the screen, task228 by the card rules in draw order). All 5 were adjudicated and none was left unread.

**How the adjudication was done.**
- This session had no subagent tool, so each pair was read in the auditor's own thread, one at a time, against the same instruction set:
  - each build's decisive move with the domain nouns stripped;
  - each build's ordered solution path, and where any shared move sits in it;
  - the tier, the track and the axis.
- **Materials.** Both cards, both prompts, and the design notes' draw, stump, ladder and duplicate-check sections (task182, task180, task130, task132, task228).
- **task83.** Its folder is on another machine. Its side rests on its card, its four ledger rows and the cached profile (target listing, deliverables, solution steps, recommendation).
- No golden file was opened.

**Heart check.**
- `guard.py heart task182` against all 141 cards and every ledger row: PASS. The nearest driver scores 0.06 (task115, task69 lineage, task51 lineage).
- `guard.py check` on task228's card with task182's card visible: BLOCK, on `ban.pattern` (G16) and `ban.strategy` (decomposition_attribution), both against task182.

**Mechanism coverage of the 134 other screened builds.**
- **Card mechanism: 112.** 14 of these are task36 or earlier, so their labels are back-fitted.
- **Track A only: 22.**
  - 17 have cards with no gap or pattern and no ledger row or reachable note: task3 to task10, task13 to task15, task18, task19, task21 to task24.
  - 5 have a design note only, and the note is on another checkout: task16, task17, task20, task112, task113.
- **task1 and task2** were compared on their card driver text only, through the heart check.

**Track A was partial for:**
- task228, task230 and task446, which have no committed pack, so only the prompt and the write-up were compared;
- task83, which rests on a cached profile.

**Guard coverage gap.**
- task182's card is not on main. It has sat on `oviya13ya/status-182` since 13:45 UTC.
- When task182 was registered, its own cards folder held only task228's retired architecture 1.
- So neither build's guard has ever met the other's current card.

## In batch against earlier builds

In pre-flight the window is ignored and the screen labels every pair "in batch". This section therefore holds the reviewer's cross-batch comparison: task182 against every build the ledger records as delivered or approved.

- **Ten builds carry a delivered or approved row, and none collides with task182.**
  - The highest surface score against task182 is task72 at 0.087, below every promoted pair.
  - No pair shares a file name, a schema, an invented name or a sentence construction.
  - No pair collides on more than one mechanism axis: task28 and task25 share the decisive gap, and task48 shares the decision type. Each runs on a different driver: reachable share of an excess, a second-source inflow, and a pair-grain population.
- **No promoted pair touches a delivered build.**
  - task83's current architecture is "listed for a ledger refresh", with no portal stump result recorded, so it ranks as live.
  - task180, task130, task132, task228 and task182 have no ledger row, so their status is unknown. Every promoted pair therefore carries "status unknown on at least one side".

## Track A findings, reviewer visible

None. The four pairs the screen promoted on surface percentile rest entirely on axes that most of the corpus shares. No rename or reskin is needed.

| Pair | Surface (corpus pct) | Shared | Not shared |
|---|---|---|---|
| task83 | 0.147 (100) | flat layout, format mix 0.67, deliverables xlsx then docx | file names, schemas, values, invented names, prompt wording masked and raw, ask skeleton, submission steps: all 0 |
| task130 | 0.140 (99) | flat layout, format mix 0.50, deliverables xlsx then docx | the same, all 0 |
| task132 | 0.138 (99) | flat layout, format mix 0.43, deliverables xlsx then docx | submission phrasing 0.005, the rest 0 |
| task180 | 0.100 (98 among consecutive pairs) | flat layout, and task182's exact format set (csv, md, parquet, pdf, xlsx), which no other build has | everything else 0; its deliverables are docx and csv |

A flat layout appears in 118 of 137 profiled builds, and the xlsx-and-docx pairing is idiom; both are under Corpus habits. task228 shares no prompt or write-up wording with task182. Its pack is not committed, so the packs could not be compared.

## Track B findings, mechanism

**task182 against task228 architecture 2 (perssathya, hardening loop 2).**
- **Tier and track.** Shape echo, a soft flag, not reject tier. Track B.
- **Status.** Neither build has a ledger row, so status is unknown on both sides. task228's branch sent it back to design at 16:48 UTC after its round 4 landed the call.
- **There is no shared driver.** With the domain nouns stripped, the two decisive moves are:
  - **task182:** a unit's attributable change is the gap between its observed level and its own driver-only path. That path is fitted on the unit's pre-intervention record with a unit-specific lagged response to the shared driver. A change measured from a fixed baseline, net of a reference set, or on one common window mixes that response into the effect.
  - **task228:** a three-way covariance separates a unit's own random error only if its comparators' errors are independent. Where two comparators share an input, their errors co-vary, and the standard separation charges the shared error to the unit. A fourth series independent of both is needed there.
  - These are different claims. The first is counterfactual attribution of a level change under a shared, time-varying driver. The second is identifying measurement-error variances when reference errors are correlated.
- **What the two builds share:**
  - the domain, physical-environmental-sciences;
  - the decisive gap, objective;
  - the decisive generator label, G16 (method selection);
  - the stump strategy, decomposition_attribution;
  - a set-of-sites answer;
  - two Layer 1 devices: logger stamps in UTC against a local reporting day, and an equipment register applied by reading date.
- **Why this is a flag at all.** Clone-check Part 1 says a stump strategy is not a component. Between adjacent draws, the stump strategy and the decisive generator are both Part 6.1 standing bans.
- **Where the shared moves sit.**
  - A single-reference comparison is a killed low rung in both builds: task182's rung 2 is the change net of the reference bores, and task228's rungs 0 to 2 are disagreement with one comparator, the better one, or their mean.
  - Neither build's decisive move appears anywhere in the other's path.
- **Which side the guard puts the ban on.**
  - By the house draw key (drawn date, then task number), task182 is the earlier draw. task180's stage 5 applied this same convention against task135 today.
  - So `guard.py heart task182` stays PASS. The BLOCK lands on task228's next check, as reproduced above.
  - The commit clock runs the other way:
    - task228 architecture 2 carried the strategy from 08:02 UTC and the G16 key from 13:38.
    - task182's card was registered at 13:45, against a tree holding only task228's retired architecture 1.
  - Which build answers the ban is for the two authors to settle. On the house key it is task228.
- **Axis.** The decisive step's stump strategy, on task228's side (G16 is its key).
- **Does the data survive?** Nothing on task182 moves, so its data stands. On task228, a strategy redraw is a re-root and its data does not survive; it is already back at design.

**Near on the cards, not promoted, card drivers read: all are different claims.**
- **task84, task119, task122** share the decomposition_attribution strategy, but on other drivers: copy competition, held allocations, and late outcomes attributed back.
- **task134** has G16 decisive, on competing exits.
- **task135** shares the domain and the decisive gap, on retransformation bias.
- **task254 v1** shares the domain, the gap, Gate G and the strategy label, on footprint apportionment against point-of-origin attribution. Its own branch has sent v1 to re-root, and the guard check against task182 is clean.

## Clean, shares components by design

- **task180 (architecture 3), two draws back.**
  - **Shared:** the anomaly-detection lane, the estimand-identification family and the exact format set.
  - **Position:** task180's decisive move, comparing each unit's exposure window with the same unit's other time, is task182's killed rung 1, each bore's own before-and-after change. It is decisive there and demoted to the wrong answer here.
  - **Driver difference:** task180 cancels fixed traits that differ between units by a within-unit contrast. task182 shows that the within-unit contrast is itself confounded by a time-varying shared driver acting through unit-specific lags, and builds each unit's driver-only path.
- **task130 (v3, harden branch).**
  - **Shared:** the decisive gap (objective), the estimand-identification family and the xlsx-and-docx pair.
  - **Position:** task130's decisive move is an untreated cohort chosen the same way one period earlier. Its nearest counterpart is task182's killed rung 2, the reference bores, so the comparison-group move is decisive there and demoted here.
  - **Driver difference:** regression to the mean after selection on an extreme value, against a shared driver's lagged, unit-specific response.
- **task83 (RE-ROOT 2.1).**
  - **Shared:** both read each unit's own history, and both use the xlsx-and-docx pair.
  - **Driver difference:** task83 splits a randomized effect by each unit's prior treatment history, because the target pool's mix differs from the measurement corpus. task182 builds each unit's counterfactual level from its pre-impact response to climate.
- **task132.**
  - **Shared:** the xlsx-and-docx pair and the flat layout only.
  - **Driver:** in a spares forecast, a replaced item restarts at the bottom of the wear-out curve.
- **task228.** Its logger devices and the killed single-reference rung are components and are clean to share. The strategy and the decisive generator are not components; they are covered under Track B.

## Strategy monoculture

**The twelve draws ending at task182** (task127 to task182, in draw order):
- No strategy carries more than 2 of 12: binding_constraint (task127, task128), causal_design (task131, task180) and maturity_censoring (task134, task181). decomposition_attribution carries 1, task182.
- Withheld rule with an official decoy: 0, against a cap of two.
- Certified-record decoy: 2, task127 and task129, against a cap of three.
- Decisive rule left unfiled: 5 (task127, task130, task134, task135, task180), none of them paired with an official decoy.

**The newest twelve on file** (task134 to task446):
- maturity_censoring carries 3 (task134, task181, task445) and decomposition_attribution 3 (task182, task228, task254 v1). causal_design carries 2 (task180, task230).
- Withheld rule with an official decoy: 0. Certified-record decoy: 0.

**No cap is exceeded.** The two strategies at 3 of 12 each sit one build below a third of the batch. The guard's overuse warning fires at three uses in the twelve before a draw, so the next draw keyed to either strategy gets a WARN, and a fourth would reach the cap.

**Labels the caps do not count.** In the newest twelve, G16 is decisive in 3 builds (task134, task182, task228), and method_or_model_selection is the Gate G mechanism in 6.

## Corpus habits

- **House file names.** data_dictionary appears in 61 builds, export_manifest in 34, and data_notes and provenance in 12 each. task182 uses none of these names: its dictionary is `monitoring_network_notes.md` and its register is `landholder_bore_register.xlsx`.
- **Pack layout.** Flat in 118 of 137 profiled builds. This says nothing about any pair.
- **Deliverables.**
  - A workbook plus a memo with no visual appears in 5 of 122 prompted builds: task83, task125 (docx then xlsx), task130, task132 and task182.
  - Three of the five fall in the twelve draws ending at task182.
  - CLAUDE.md asks for a visual wherever it makes the decision read at a glance.
  - The voice-check batch on this disk has no Code deliverable anywhere.
- **Prompt surface** (voice-check over the 12 builds on this disk):
  - The opening move is "other" in 8 of 12; task182 is one of the 3 that open question-first.
  - No 6-word run is shared by a third of the batch.
  - task182's prompt is 900 characters, the only one in that batch under the 1,000 ceiling. The others run from 1,202 to 1,676.
- **Domain concentration in the newest twelve.**
  - physical-environmental-sciences carries four builds: task135, task182, task228 and task254.
  - Each sits under a different objective, so no pairing ban fires.
  - Two of them, task182 and task228, are sensor networks read through loggers, both with a UTC-against-local-day device. A reviewer holding the batch sees this; a reviewer holding one package does not.
- **Objective lane.** task180, task181 and task182 are three anomaly-detection builds in a row. The lane is assigned by task number, the domains differ, and no pairing ban fires.
- **Repeated ask opening.** "give me the single dollar figure we" opens the ask in 2 builds, not including task182.

## What to redraw

1. task228 architecture 2 (perssathya, not this build): the decisive step's stump strategy (decomposition_attribution, keyed G16), which `guard.py` blocks against task182 once task182's card is on main.
2. task182: nothing.
