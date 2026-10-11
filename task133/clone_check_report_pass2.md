# Clone check: pre-flight on task133, pass 2 (hardening loop 1), against every other build, 2026-10-11

## Verdict

No pair tier on either track. The worst tier found is Idiom (Track A, corpus level): task133's rewritten prompt follows the same build order as the other four forecasting builds in flight. The nearest pair, task134 (back to back, on hold), reads `clean_shares_components`: both decisive steps turn on a competing exit, but for opposite estimands.

## Scope and coverage

- **Mode and scope.** Pre-flight on task133, with the window ignored. task133 is compared against every build on file: task1 to task135, plus task228 and task229.
  - task133 is Bellbird Personal Finance's collective ECL allowance at 30 September 2026. It is architecture v1 after hardening loop 1, on `sathya8571/task133-harden` in `/home/user/wt133`.
  - Its data is cut. `pipeline.json` reads stage 4 (leak.py REVIEW, no LEAK). The loop-1 solver round has not run. This run is the stage 5 duplicate check.
- **What changed since pass 1.**
  - **The decisive rung moved twice down the same curve.**
    - v1's decisive rung, where the curve's clock starts, is now R0 (+38.9 per cent).
    - v1's answer, the curve's increments divided by survival to date, 1 - C(a), was landed on the portal. It is now the stump, R4 (-10.8 per cent).
    - The curve is now filed as the crude default share of every loan drawn. So the answer divides by the share of entrants still present and never defaulted, S(a) = 1 - C(a) - Cl(a), with Cl(a) read from the development sample.
  - **The asks.** The inheriting asks were replaced by two decoupled ones: the realised loss on the 2023-24 defaults, and where the June book's stage 1 and stage 2 loans stand at 30 September.
  - **The opening.** It moved from number-first to calendar-first.
- **How the corpus was assembled.** `fingerprint.py` reads its cards, ledger and cache from its own checkout, and task134's and task135's builds exist only on their own worktrees. So the extract and the screen ran on a scratch mirror holding:
  - the 18 builds on disk in `/home/user/wt133` (task117 to task133, task229), symlinked read-only;
  - task134 from `/home/user/wt134`: the repair r1 pack (repair r2 is generator-only work in progress);
  - task135 from `/home/user/wt135`;
  - wt133's 133 cards (main's, plus task133's loop-1 card) and the shipped ledger, which is identical to main's;
  - a copy of the committed cache (HEAD 7ffeec9), so that cached profiles of builds not on this disk carried through.

  A second run swapped in the branch states: task130 from `/home/user/wt130`, and the branch cards for task130, task134 and task135. Both runs promoted 0 pairs.

  Nothing in any checkout was written except this report. The tracked cache was not touched.
- **I checked the cache before trusting it.**
  - For all 110 builds not on disk, the cached card fields match the current card files, and the cached ledger rows match the ledger.
  - Every build on disk was re-extracted. The committed cache already matched task133's loop-1 prompt, write-up, card and pack.
- **Counts.**
  - **Builds compared:** 127 through the screen. That is every number from task3 to task135 except task61, task96, task99 and task114 to task116, plus task229. Nine more were checked outside the screen (below), so every number from task1 to task135, plus task228 and task229, has a record and was checked.
  - **Pairs:** 127 screened, 0 promoted. The screen's corpus is 128 builds and 8,128 pairs, with a mean surface score of 0.070. task133's pairs average 0.071, and the highest is 0.100.
  - **Pairs adjudicated:** none were promoted, so none was owed. I read four pairs at my own discretion, each labelled "not promoted" below:
    - **task134:** the nearest heart text in the guard, and the only build whose decisive step also turns on a competing exit;
    - **task132:** back to back. Pass 1's hold line was about the survival division, and this loop moved through it;
    - **task100:** the only gap-plus-pattern match on the cards;
    - **task117:** nearest on surface, at the 98th percentile.
  - **Pairs not read:** 123. None carries a mechanism signal:
    - card driver overlap tops out at 0.13 (task134), against the screen's 0.40 line;
    - no pair collides on gap, pattern and decision type together;
    - no pair carries the same-driver signature (gap, pattern and Gate G mechanism together);
    - no consecutive pair shares two of the three axes;
    - no calibration form is shared, and there is no hard tell.

    I also swept every driver, concrete driver, stump and lineage driver on file for the vocabulary of this loop: competing exits, censoring, survival, attrition, prepayment, conditioning, denominators and credit loss. That covered the 133 cards, plus the branch cards for task130, task134 and task135. I read every hit (41 cards). Apart from task134, none states task133's claim, and no other card is a credit-loss or lifetime-PD build.
- **Outside the screen.**
  - **task114, task115, task116 and task228** have cards only. I scored them with the script's own card comparison (`track_b_cards`). task114 and task115 share only the decisive gap (time), and task116 and task228 share nothing. Driver overlap is at most 0.051.
  - **task99** has a card, but the script excludes the number as scratch. The card has no gap or pattern to score, and driver overlap is 0.0. I read it: the delay is right-censored and estimated by Kaplan-Meier, so it turns on censoring, not on a competing exit.
  - **task1 and task2:** their cards carry no gap or pattern. I read their drivers, and nothing is shared.
  - **task61** (retired) **and task96** (drawing) have ledger rows only. Their decisive mechanisms are objective with G11, and population with E. No collision.
- **Mechanism coverage, over the 128 screened builds.**

  | Layer | Builds | Which |
  |---|---|---|
  | Card with labels | 106 | 92 native, 14 back-fitted (task11, task12, task25 to task36) |
  | Card driver and stump, no labels | 20 | task3 to task10, task13 to task24 |
  | No card, short design note and target profile only | 2 | task112, task113 (fingerprinted on another machine, no prompt or write-up) |

  - The screen scores 22 pairs on Track A only.
  - For 20 of those 22, the card's driver and stump were read by the guard's heart check and by my sweep.
  - task112 and task113 are checked on their target profiles only.
- **No subagents.** This run had no agent tool, and nothing was promoted, so no adjudicator was owed.
  - The four discretionary readings were done in my own thread, to the adjudicator brief: each decisive move with the domain nouns stripped, the ordered path, where each shared move sits, then verdict, tier, track and axis.
  - **What I read:**
    - both cards, with task134's in its registered and its branch state;
    - both prompts;
    - write-up blocks 1 to 3 for the counterparts, and task133's write-up in full, as the build under check;
    - the design notes on disk (task132, task133, task134);
    - the target listings;
    - the workbook document properties of task133 and task134, because task134's workbook writer was adapted from task133's.
  - No counterpart's golden figure was read, and no server-side tool was called.
- **Mechanical cross-checks, run on the same mirror.**
  - **`guard.py heart task133`:** WARN.
    - The nearest heart text is task134's registered driver at 0.14, against the 0.12 WARN line. Next is task52's stump at 0.06.
    - Against task134's branch card, the same text scores 0.06.
  - **`guard.py check`:** WARN only.
    - `three_rules.strategy_risk`.
    - `people.first`: Kayla against task118, Christine against task104, and Joseph against task135. These are card personas, not names in the shipped text.
    - `repeat.gate_g`: forecasting, against task130 v3 and task132.
    - Two NOTEs on near drivers. task133's own v1 lineage is at 0.27; that is its ancestor, not a finding. task134 is at 0.18, differentiated on task133's card.
  - **From task134's side,** which the guard will run when task134 resumes:
    - `repeat.opening`: a WARN, calendar-first against task133.
    - On the registered card, a `driver.near` WARN at 0.18. task134's card carries no reciprocal differentiation line.
  - **`guard.py people task133`:** the cut pack's text names one persona, Stephanie Manning.
  - **`voice-check.py task133`** (main's current version, with the 1,000-character ceiling): no carrier wording, and no six-word run shared by a third of the batch. task133 is the shortest prompt in the window: 146 words and 853 characters.
- **Moving parts during the run.**
  - **task133's leak read.** It landed at 16:01 (commit 22d2dfd), touching only `pipeline.json` and `leak_check_report.md`. It records two fixes before the solver round:
    - the development sample gets its in-world reason, as a model release package filed for the auditors;
    - the sample's outcome month is pinned to the curve header's convention.

    Neither fix is in the committed pack yet, and neither touches the decisive step. task133's prompt, write-up, design note, metadata, card and 15 target files were all last modified before this run began, and were unchanged at the end.
  - **task130** was being edited on `/home/user/wt130` throughout. Both screens returned the same result whether they used main's task130 or wt130's.
  - **The scratch mirror** was deleted at 16:01 by a parallel session that shares the scratchpad. I rebuilt it, and the extract and the screen re-ran at 16:05 with identical results.

## In batch against earlier builds

In pre-flight, every pair is task133 against another build. The screen labels its pairs "in batch" because focus mode sets the window to the whole corpus. That is a labelling quirk, not a scope error.

**Nothing at any tier, and nothing against a delivered build.** The ledger records ten builds as delivered or approved: task25, task27, task28, task29, task30, task33, task34, task35, task48 and task72. Against those ten:

- **Hard tells:** none. No byte-identical file, no identical column set, no same-seed table, no shared file name and no shared invented name.
- **Nearest on surface: task72**, at 0.093 (92nd percentile).
  - All of that comes from the flat layout and five shared formats out of six.
  - Masked prompt overlap and masked write-up overlap are both 0.
  - Its driver, booking a movement to the owner whose agreement covered each piece of service, is unrelated.
- **Nearest on mechanism: task35.** It shares the decisive gap (time) and the decision type (quantity_figure), on back-fitted labels. Its driver, a forward obligation whose attachment period is recovered from settled records, is a different claim.
  - task33 shares the gap label only.
  - task30 and task34 share only the context-artifact species (`filed_model`).

**Status of the other counterparts:**
- 61 are live on the ledger.
- 7 are retired or failed: task31, task32, task36, task45, task51, task55 and task73.
- 48 have no ledger row, so their status is unknown: task3 to task24, task95, task104, task109 to task113, task117 to task132, task134, task135 and task229. `START_HERE.md` records task132 and task133 as shipped to the author, but the ledger is silent on both.
- 1 carries a row the status parser cannot rank (task59).

## Track A findings, reviewer visible

No finding at any pair tier. The one Track A finding is Idiom, reported under Corpus habits.

- **No shared surface with any build.**
  - No target file name, schema, numeric signature, byte-identical file or invented name is shared. The invented names are Bellbird Personal Finance, PL36, PL60, Wirraway Mercantile Agents and Tarwin Receivables Pty Ltd.
  - The highest masked prompt overlap is 0.007 (task134), and the highest masked write-up overlap is 0.005 (task131).
  - Ask-skeleton and step-skeleton overlap are 0 against every build.
- **task117, nearest on surface.** It scores 0.100 (98th percentile). It is not consecutive, so it falls under the 99th-percentile line.
  - **Where the score comes from:** the flat layout and the identical six-format set (csv, docx, parquet, pdf, txt, xlsx).
  - **Shape echo:** two of the four axes are shared, which is below the tier.
    - The opening is built the same way: "On 16 February the city council votes on..." against "On 23 October the board signs off."
    - Both decide a single quantity figure, the most common decision type on file (59 of 133 cards).
  - **What differs:** the deliverables (pdf, png and xlsx, against xlsx and pptx), the calibration (a settled transaction ledger, against none) and the driver.
- **task134, back to back.** It scores 0.088 (82nd percentile).
  - **Shape echo:** one axis of four is shared. Both prompts are built the same way: the deciding body and its date, the figure, a workbook, then a named reader's chart, in 146 and 154 words.
  - **What does not count:** the deliverables differ (xlsx with pptx, against xlsx with png), and so does the decision (a currency figure, against an allocation). The calibration is an absence on both sides.
  - The build order is the lane's habit, reported under Corpus habits.
- **Toolchain.** The two packs' workbooks share an application string, a version and the standard Office theme. Every Excel file carries those. Their styles, authors and company names differ. Not a tell.
- **The guard's shape ban** covers the last two builds, and it is clear: task133 is shape 02, task131 is shape 07 and task132 is shape 04.

## Track B findings, mechanism

None.

**Part 6.1's standing bans clear on the cards.** The three builds before task133 are task130, task131 and task132, in the guard's draw order and by task number alike.

| Axis | task133 (loop 1) | task130 (v3 card) | task131 | task132 |
|---|---|---|---|---|
| Pairing | banking-credit-financial-risk with forecasting | actuarial with forecasting | marketing with experiment-causal | energy-utilities with forecasting |
| Decisive gap | time | objective | population | population |
| Decisive pattern (the first generator, where the pattern is none) | G9 | A | G10 | G6 |
| Gate G | forecasting | forecasting | method_or_model_selection | forecasting |
| Decision | quantity_figure | quantity_figure | pick_one_of_n | dial_setting |
| Calibration, context artifact | none, filed_model | other, operations_log | none, register | none, filed_standard |
| Strategy | stated_rule_hard_construction | forecast_method_backtest | causal_design | population_selection |
| Forum, forcing event, organisation | board, period close, financial institution | trustees, contract, school | executive team, budget, co-operative | line manager, other, utility |

- **Gate G forecasting repeats task130 v3 and task132.** That is a WARN in the guard, and it is the lane.
- **task134 comes after task133** in both the draw order and the numbering. Checked from task134's side, the only Part 6.1 axis that repeats is the opening move (calendar-first), which is a WARN.
- **No hit touches only a dead row.** task133's own v1 is its lineage and is not a finding: v1's committed answer is now rung R4 of this ladder.
- **Mechanism readings.** The pairs that come closest on mechanism (task134, task132 and task100) are read below, and all three clear.

## Clean, shares components by design

### task134: clean_shares_components (not promoted, read at my discretion)

**Status.** Back to back, with the same author and in the same lane. It is in flight, and on hold on its own branch:
- the pack is the repair r1 cut;
- repair r2 is generator-only work in progress;
- the ledger is silent, so its status is unknown.

Its card exists in two states, and I read both:
- **On main (registered 08:10):** the first build's driver, the Aalen-Johansen cumulative incidence with removal and death as competing exits.
- **On its branch (repair r1, 12:21):** follow every release to the data cut, because a removal can be reversed.

**Why this pair.** Loop 1 moved task133 into task134's territory.
- task134's own pre-flight cleared the pair against task133 v1, because task133's curve was filed and complete.
- task133 is now the only other build whose decisive step turns on a competing exit.

**Decisive moves, with the domain nouns stripped.**
- **task133:** "A cumulative event curve filed as a share of every unit that ever entered still holds the units that left by another exit in its base. So a unit still present at its age takes the curve's next increments divided by the share of entrants still present and event-free at that age, not by one less the curve to date."
- **task134, registered card:** "A within-horizon event probability estimated from units not yet followed to the horizon has to count an exit that ends the chance of the event as ending it. Censoring that exit treats those units as still at risk, and overstates the probability most where the exit concentrates."
- **task134, branch card:** "A within-horizon event probability estimated from units not yet followed to the horizon has to follow every unit to the data cut, because neither exit is loss to follow-up: one ends the chance of the event, and the other can be reversed."

**The same claim? No.**
- **The estimands differ, so the competing exit is treated in opposite directions.**
  - task134 wants a probability per entrant, counted from entry. A death stays in its denominator as a unit that did not return, and a removed person's later return still counts.
  - task133 wants a probability conditional on the unit still being present at its own age. A loan that left by repayment has to come out of the denominator.
- **The operations differ.**
  - task134 chooses an estimator under incomplete follow-up. Censoring is its frame, and its rung R0, the share booked so far, is about immaturity.
  - task133 conditions a filed curve, built on complete-term cohorts, for units part-way along it. Nothing is censored, and the only thing read from the data is the share Cl(a).
- **The reskin test fails both ways.**
  - Rewritten into lending, task134 becomes a lifetime default curve estimated from an immature book with repayment censored. In task133 that is the model team's job, and it appears only as rung Rh.
  - Rewritten into the jail, task133 becomes a forecast of returns among people already out, not yet returned or removed, conditioned on time since release. task134 never conditions on time already served, because every projected release starts at zero.
- **The client's own library files the two lessons as separate patterns** (`layer2-rigor-patterns.md`, event-history analysis).
  - Pattern 1, "Competing events are not censoring," is task134's.
  - task133's divisor turns on the distinction pattern 2 draws: a rate among the units still at risk, against the share of all entrants who ever have the event.

**Paths, in order.**
- **task133, eight steps; the decisive move is steps 3 and 4:**
  1. Stage the September book.
  2. Months on book and remaining term.
  3. **From the development sample, the share of entrants still open and never defaulted at month a, 1 - C(a) - Cl(a).**
  4. **PD(k) as the curve's increment over that share, with the stage 2 scalar.**
  5. LGD, the re-amortised balance and the discount.
  6. The scenario multiplier.
  7. Sum by stage.
  8. The call.
- **task134 on its branch, seven steps; the decisive move is step 4:**
  1. Stack the two jail systems.
  2. The population, the window and the districts.
  3. The return definition.
  4. **One minus Kaplan-Meier at 12, 24 and 36 months, with every release followed to the cut and no removal or death censoring it.**
  5. Multiply by the adopted projection.
  6. Navigators at one per 250, rounded up.
  7. The call.

  The registered card's path is the same, with the decisive step being the Aalen-Johansen cumulative incidence.

**Where the shared moves sit.**

| Move | task133 | task134 |
|---|---|---|
| A competing exit handled through the all-cause survival (the share that has come through every exit) | Decisive: the divisor, from R4 (-10.8 per cent) to the answer | Decisive for death in both card states. Decisive for removal only on the registered card: the branch makes removal reversible, which turns the absorbing-exit cumulative incidence into a wrong rung, R7 |
| Kaplan-Meier with the competing exit censored | A side rung, Rh (+6.9 per cent), for a solver who rebuilds the curve from the sample. Off the competent path | The stump, R1: 37 navigators against 33, Puerto 68.5 against 54.2 per cent |
| Conditioning a curve on survival to the unit's own age | The frame: R3 (-13.2 per cent), then R4 (-10.8 per cent), then the answer | Absent |
| Incomplete follow-up | Absent (complete-term cohorts) | The frame: R0, the share booked so far, 25 navigators |

**What the positions show.**
- task134's decisive device sits demoted in task133, as a side rung.
- task133's decisive device does not arise in task134.
- Carried over by rote, each lesson lands on the other build's stump:
  - "keep the exited units in the base to the cut" divides task133's increments by 1 - C(a), which is R4;
  - "take the exited units out of the base," done by censoring, is task134's R1, and ending follow-up at a removal is its R7.

**How close it is.**
- This is the nearest pair in the corpus.
- Both correct answers rest on the same object, the all-cause survival: task134's cumulative incidence weights each period's return hazard by it, and task133 divides by it.
- A solver fluent in competing risks is helped on both, and a batch reviewer will read the two builds as one family.
- The pair clears on the estimand and the operation, not on distance.

**Verdict:** `clean_shares_components`, Track B, no tier, nothing to redraw.

**Axes to hold.**
- **task133.** The stump stays on the conditioning base, with the curve filed (R4).
  - A later loop might withhold the curve, so the solver has to estimate it from the sample, or make the sample immature, censored at the reporting date. Then Rh becomes the main path, and task133's decisive rung becomes task134's: censoring an exit that ends the risk. The pair would then read as Template.
- **task134, owed to the pair.** Its forward cohort starts at release.
  - A re-root that forecasts returns among people already out, conditioned on time served and on not having been removed, would take task133's decisive move.
- **The loop-1 solver round.** If the solvers' committed wrong answer is Rh (a default-only hazard, or a Kaplan-Meier rebuild, about +6.9 per cent) rather than R4, then the stump task133 actually carries is task134's device. Read the pair again.

### task132: clean_shares_components (not promoted, read at my discretion)

**Status:** back to back. It was shipped to the author per `START_HERE.md`, but the ledger is silent, so its status is unknown.

**Decisive moves, with the domain nouns stripped.**
- **task132:** "A unit that can fail once is replaced by a new unit at the bottom of the age curve, so the present unit's forward rate counts only weighted by its chance of still being in place, with the replacement's rate after; carried through the horizon unweighted, it counts failures one position cannot have."
- **task133:** as above.

**The same claim? No.**
- task132's decisive move is the survival weighting itself, with renewal.
- task133's competent solver already makes a survival division and still fails. That division is R4, the step v1's portal response took. task133's decisive move is which survival to divide by: the share still present after both exits.
- task132 has no second exit. A module leaves its position only by failing, or at its relay's scheduled renewal, which is a known date.
- task133 has no renewal. A loan defaults once and is not replaced.

**Paths, in order.**
- **task132, eight steps; the decisive move is step 4:**
  1. Failures as AM-PC-014 defines them, in the removed module's age band.
  2. Module-months from the go-live, and the band rates.
  3. Each relay's end of support.
  4. **The present module aged forward, adding its band rate weighted by the chance it is still fitted, and the 0-9 band rate weighted by the chance it has already failed.**
  5. Usable stock.
  6. Whole lots at 95 per cent Poisson cover.
  7. Price.
  8. The call.
- **task133:** as above, with the decisive move at steps 3 and 4 of 8.

**Where the shared moves sit.**

| Move | task132 | task133 |
|---|---|---|
| Weighting a forward event rate by survival from now, for a unit alive at its current age | Decisive: from rung 3 (no weighting, +44.5 per cent, 19 lots against 13) to the answer | Passed: R3 (no division, -13.2 per cent) to R4, the competent path. The stump lies beyond it |
| Renewal, a failed unit replaced at age zero | Decisive | Absent |
| A competing exit in the at-risk base | Absent | Decisive |
| Where the unit's clock starts | Low: rung 1 (relay age, -16.3 per cent) and rung 2 (module-months from fitting, -17.4 per cent) | The bottom rung: R0 (read from origination, +38.9 per cent) |

**Pass 1's hold line was crossed in letter, not in substance.**
- Pass 1 said task133's decisive weight had to stay on the curve's origin. A hardening that moved it onto the survival division would put task133 on task132's decisive device.
- Loop 1 moved the decisive weight off the origin, past the survival division and onto what that division leaves out: the repaid loans.
- So task132's decisive device is now a step task133's competent solver completes before failing. A solver drilled on task132 lands exactly on task133's stump. That is demotion, the opposite of a clone.

**Verdict:** `clean_shares_components`, Track B, no tier, nothing to redraw.

**Axis to hold:** task133's decisive weight stays on the composition of the divisor, never on whether to condition at all.

**Outline.** At most one Shape echo axis is shared, the build order, which is the lane habit. The deliverables differ (xlsx with docx, against xlsx with pptx), and so does the decision (whole lots, against a currency figure).

### task100: clean, labels only (not promoted, read at my discretion)

**Status:** v2 is live on the ledger. It was submitted to the portal, and no result is recorded.

**The match.** It is the only pair where the decisive gap (time) and the decisive pattern (G9, task133's first generator) both match on the cards. The context artifact (`filed_model`) matches too.

**task100's decisive move:** "The forward roster loses a class of members who finish one period early, a class that is not the top tier of the tenure count and can be enumerated only by finding the same member in the final stage on the prior period's snapshot."

**The same claim? No.**
- Each build has an exit in its forward population.
- task100's exit is a fixed class of members, enumerated by linking two snapshots.
- task133's is a probability read from a development sample, used to condition a filed curve.

**Everything else differs.**

| Axis | task100 | task133 |
|---|---|---|
| Objective | ETL | Forecasting |
| Gate G | etl_conformance | forecasting |
| Decision | designation set | currency figure |
| Calibration | certified matrix | none |
| Strategy | population selection, with a validated decoy | stated rule |

**Position.** task100's decisive rung is the early-exit enumeration, and its forward roll sits at rung 4 of six. Nothing in task133 occupies either place.

**One note.** task133's card still files G9 first ("downstream survival against upstream acquisition"), and the loop did not refile it. If the generators are refiled, run `guard.py check` again.

## Strategy monoculture

**Windows.** Counted from the cards' `stump_strategy`, `decisive_rule_filed`, `official_decoy` and `validated_decoy` fields, over two windows:
- the 12 builds ending at task135 (task124 to task135), the batch the lane's in-flight builds are likely to ship in;
- pass 1's window (task122 to task133), for continuity.

| Cap | task124 to task135 | task122 to task133 |
|---|---|---|
| Any one strategy (cap: a third, 4 of 12) | at most 2: causal_design (task124, task131) and binding_constraint (task127, task128) | at most 2, the same two pairs |
| Withheld rule with an official decoy (cap 2) | 0 | 0 |
| Certified-record (validated) decoy (cap 3) | **5: task124, task125, task126, task127, task129** | **7: task122 to task127, and task129** |

**Single uses in the later window:**
- withheld_rule_corpus_fit (task125)
- identity_resolution (task126)
- composition_mix (task129)
- forecast_method_backtest (task130 v3)
- population_selection (task132)
- stated_rule_hard_construction (task133)
- maturity_censoring (task134)
- other (task135)

**task133 adds to none of these counts.** Its rule is filed, with no official decoy and no validated decoy.

**The validated-decoy breach belongs to the batch.**
- It is carried by builds drawn before the two-layer standard, every one with status unknown on the ledger.
- It is not task133's to repair. But any batch that ships task133 beside them carries it.

**What the labels split.**
- By the reading, the decisive steps of task132, task133 and task134 all decide who sits in an at-risk denominator under survival and exit:
  - task132: which module occupies the position once failures are replaced;
  - task133: which entrants are still present after default and repayment;
  - task134: who stays in the denominator after a removal or a death, in its design note's own words.
- That is the vocabulary's own definition of population_selection: "who is in the denominator: survivorship, selection, attrition, exposure, scope."
- The three cards file it three ways: population_selection, stated_rule_hard_construction and maturity_censoring. stated_rule_hard_construction is a fair label for task133, because its rule is filed and the construction is the work.
- **Read by substance, it is 3 of 12.** That is a quarter, under the third-of-a-batch line. But the three are consecutive, and if the labels followed the substance, the guard's strategy ban would block the repeat. That ban stops any strategy recurring within the last three builds.
- **Not a tier on the record.** It is the count a reviewer who reads rubrics rather than cards will make. The axis for the lane's next draw (task136 on) is a decisive step off time-to-event denominators.

## Corpus habits

**1. One build order across the lane (Idiom, Track A, the worst tier in this report).** All five forecasting builds in flight follow the same order:
- the call is set against a dated vote, filing or deadline in the first two sentences;
- then the figure is asked for;
- then a workbook carries the figure and the grid asks;
- then a named reader's second file carries one chart.

| Build | Dated opening | Workbook | Named reader's second file |
|---|---|---|---|
| task130 v3 (wt130) | "Whatever baseline I certify to the board on 25 March..." | `cohort_baseline_2027.xlsx` | "Deborah Johnson wants that total first on one page", `baseline_certification_memo.docx`, then a chart |
| task130 v2 (main's pack) | Corvane's letter of 15 September | `tenter_house_replacement_units.xlsx` | `tenter_house_runoff.png`, "for Irene" |
| task132 | "After 15 December Veldtek takes no more orders..." | `vpr340_psu_final_buy.xlsx` | "Angel Baird signs the order. Write her a one-page memo", with the failures by year as a chart |
| task133 | "On 23 October the board signs off." | `ecl_allowance_2026Q3.xlsx` | "Stephanie Manning chairs the Audit and Risk Committee and will present two slides", the allowance then a chart |
| task134 | "The Commissioners Court votes on 24 November..." | `navigator_application_fy2027.xlsx` | "Judge Bartlett wants one chart" |
| task135 | the design basis filed with the State Engineer in January | `forebay_sediment_build.xlsx` | "Debra Roy reviews the submittal", a memo that "carries one chart" |

- **Why it is a finding.** No two of these prompts are clones, and the wording varies enough that voice-check's six-word-run sweep finds nothing. But it is one skeleton: context, then one paragraph per deliverable, in the same order every time. That is the shape the client's voice note names.
- **It is new with the lane.** task124 to task131 mostly put the memo or deck first.

**2. Opening moves.**
- **On the cards,** calendar-first is filed for task117, task128, task133 and task134, and for task229 in another lane.
- **task133 took task134's move.** Its loop-1 rewrite moved from number-first to calendar-first, the move task134's card had filed earlier the same day.
- **The guard cannot see that repeat from task133's side.** Both cards are dated 2026-10-11, and the draw order puts task134 after task133. task134's next check will raise `repeat.opening` against task133.
- **task133's sentence also repeats task117's construction:** "On 16 February the city council votes on..." against "On 23 October the board signs off."
- **voice-check understates the concentration.** It files 9 of the 12 openings under "other", because it does not recognise dated openings that name a body, such as "The Commissioners Court votes".

**3. The "what I need ... is" frame.** 7 of the 12 builds from task124 to task135 put the main ask in this frame:
- "What I need from you is" (task124, task126)
- "What I am ordering is" (task125)
- "What I need is" (task128)
- "So what I need is" (task131)
- "The call I need is" (task132)
- "What it needs from my team is" (task133)

**4. Dictionary file name.**
- The name `<system>_extract(s)_dictionary` now appears in four builds, three of them in the last four numbers:
  - task103: `intake_extract_dictionary.md`
  - task130: `housing_needs_extracts_dictionary.txt`
  - task132: `eam_extract_dictionary.txt`
  - task133: `ecl_extract_dictionary.txt`
- `data_dictionary` is in 61 builds, and 75 of the 128 carry some `*dictionary*` file.
- The role is required content, and not evidence about any pair. The name is a habit a batch reviewer sees.

**5. Date stamps.**
- `2026-09-30` stamps files in 9 builds: task104, task105, task106, task108, task126, task130, task132, task133 and task135.
- A `YYYY-MM_YYYY-MM` range ending 2026-09 appears in 6: task106, task111, task118, task130, task132 and task133.
- That is the natural as-of date for builds drawn in October 2026, but across a batch it reads as one naming scheme.

**6. Deliverables.**
- Every lane build ships an xlsx plus one file for a named reader.
- In the window, xlsx with pptx is task124, task129 and task133.
- No build in the window has a Code deliverable. tsv, parquet, html, jpg, py, ipynb, sql and r are unused.

**7. Personas.** Three card first names recur: Kayla (task118), Christine (task104) and Joseph (task135). The cut pack's text names only Stephanie Manning, and the guard's people check on shipped text is clean. Not a finding.

## What to redraw

No Track B redraw. The draw, the ladder and the data stand.

1. **task133, the prompt's build order** (Track A, Idiom). This is a prompt rewrite, and the data and the ladder stand. The order is the dated deciding body, then the workbook, then a named reader's chart, and all five forecasting builds in flight share it. The same axis applies to task134 and task135 before they ship.

**Hold through any further hardening:**
- **task133:** the stump stays on the conditioning base, with the curve filed (R4). Rh, a curve re-estimated from the sample with repayment censored, stays a side rung.
- **task134, when it resumes:** the forward cohort starts at release, never conditioned on time already served.
- **After task133's loop-1 solver round:** if the committed wrong answer is Rh rather than R4, read the task133 and task134 pair again.
