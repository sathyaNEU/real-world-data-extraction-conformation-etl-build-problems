# Clone check: pre-flight, task253 (rent-relief voucher split, architecture v1) against the whole corpus, 2026-10-11

## Verdict
TEMPLATE (Track B): task253 against task230 (in flight on `perssathya/task230-event-volume-drop`, drawn first the same day). Both builds' decisive rung reweights a stand-in group within the class that drives both selection into the group and the outcome. No hit against any approved or delivered build.

## Scope and coverage

**Mode and scope.** This is a pre-flight on task253 against every other build, with the window ignored, as `/build` stage 5 asked.
- task253 is architecture v1, with its data cut and the leak check run. No solver round has run yet, and it has no lineage.

**Extract.** The cache was stale: it was written at 18:11 UTC and task253's pack was regenerated at 18:20. I re-extracted.
- 19 builds were fingerprinted from disk (task117 to task133, task229, task253), and 110 cached cards were kept, giving 129 cards (127 screenable).
- The main session reworded paragraph two of the prompt while this check ran ("puts there" became "estimates there", and the notice grounds became "for each of arrears, own use and renovation"). I re-extracted at 18:41: the pack hashed byte-identical, the prompt's sentence openings were unchanged, and both screens returned the same pairs and scores.

**How the corpus was assembled.** This branch sees only the cards and packs that have reached main, and ten builds were in flight on other branches on 2026-10-11.
- The ten were task134, task135, task228, task230, task254, task180, task181, task182, and task130 and task133 on their hardening branches.
- I exported their task folders and cards read-only (`git archive`, `git show`) into a gitignored scratch folder, deleted at the end.
- I ran `fingerprint.py`'s own extract and screen over this branch's cache plus those exports, with its cards path pointed at main's cards plus the branch cards. `guard.py` ran on the same card set through `FINGERPRINT_CARDS`.
- task445 and task446 hold only a seed and `pipeline.json` (no draw), so they are not builds yet.

**Builds compared.**
- **Screened:** 135 builds (17 on this disk, 10 from branches and 108 cached that are screenable; task1 and task2 have no prompt or pack).
- **Card-level only (the guard and the driver sweep below):**
  - task114, task115 and task116 have cards but no folder anywhere.
  - The script excludes task99 as a spare slot, which is correct: its card records it as the R5 state of task31's world (ledger row 31, failed).
- **Pack-level Track A not possible:** the packs of task228, task230, task254, task180 and task182 are not committed on their branches. Their prompts and submissions were screened.

**Pairs.**
- **Screened:** 134. This branch's corpus alone gives 126.
- **Promoted:**
  - In this branch's view: 4 (task87, task100, task130 and task68).
  - With the in-flight branches: 5 (task87, task134, task100, task68 and task230).
  - That makes 6 distinct pairs. task130 is promoted only on main's copy. Its hardened copy ships xlsx with docx and is not promoted.
- **Adjudicated:** all 6. None was left unread.
- **Read at card level although not promoted:**
  - task254, this author's sibling build, next in draw order;
  - task124, for shape 05, the allocation decision and the "We can only" opening;
  - task132, where G6 is the decisive generator inside the window;
  - task76 and task79, the corpus's other social-survey builds;
  - the ten builds the ledger ranks approved or delivered, each scored on Track B.
- **Driver sweep:** I swept all 139 cards on file (main plus in flight, lineage drivers included) for the stand-in reweighting move. It found task230 only.

**Adjudication method.**
- This run had no subagent tool, so I adjudicated the pairs in this thread, one at a time, against the adjudicator brief: driver sentences with the domain nouns stripped, ordered paths, the position of each shared move, then tier, track and axis.
- No advisor, web or Agent tool was called.
- Reads were limited to:
  - cards, prompts and ledger rows;
  - task253's submission and design note;
  - task230's design note and the hardening brief in its round-1 log;
  - task134's prompt and ladder rows;
  - task68's cached submission steps (its folder is not on this disk).

**Mechanism coverage, over the 135 screenable builds.**
- **Layers:** 113 have a card mechanism layer (gap or pattern on the card), 5 are note-only and 17 have none.
- **Back-fitted labels:** 34 builds (task3 to task36) carry them, 14 of which have a gap or pattern on the card.
- **Track A only in the screen:** 22 builds (task3 to task10, task13 to task24, task112 and task113).
  - 20 of them carry a driver sentence on their card, which the guard's heart check and the driver sweep did read.
  - task112 and task113 have no card and no ledger row, so they were checked on Track A only.

**Guard.**
- **This branch:** `guard.py heart task253` gives PASS. The nearest heart text is 0.05, and the one NOTE, on task68, is answered by the card's differentiation.
- **With every in-flight card in one card set:** the guard gives BLOCK, with `ban.pattern` and `test.same_driver` against task230, plus WARN `repeat.gate_g` and `overuse.gate_g` (5 of 12).
- **Why neither guard saw it:** the two cards were registered the same day on separate branches (task230 at 09:09 UTC, task253 at 15:36 UTC).

## In batch against earlier builds

This is a pre-flight, so every pair is task253 against an earlier draw. The screen labels every promoted pair "in batch" because focus mode sets the window to the whole corpus. That is a labelling quirk, not a scope bug.

- **No hit at any tier against an approved or delivered build.**
  - The ledger ranks ten builds that way: task25, task27, task28, task29, task30, task33, task34, task35, task48 and task72.
  - task253 shares no Track A tell with any of them.
  - On Track B it shares only the decisive gap label (population), with task34, task48 and task72. Their drivers are unrelated: a sub-population enumerated by a within-cluster fit, a population visible only at a pair grain, and a movement booked to the owner under a transfer.
- **Delivery status of the other side of every promoted pair: unknown.**
  - task68: rounds held, no portal result recorded.
  - task87 v9: none recorded.
  - task100 v2: submitted to the portal, result not recorded.
  - task130, task134 and task230: no ledger row.
  - task229 has a SHIPPED commit on main but no ledger row, so it is unknown here too. It shares only the decisive gap with task253.
- **The live exposure is in flight, not behind.** task230 carries the Track B finding below.
  - It is not exclusion level today, because neither side is delivered.
  - It becomes exclusion level for whichever of the two reaches final_verdict after the other has been delivered.

## Track A findings, reviewer visible

**1. task253 against task130 (hardened copy on `sathya8571/task130-harden`): the persona surname Miller. Fiction-marker echo, Track A only, cleared by a rename.**
- **Status:**
  - task130 has no ledger row, so its status is unknown. Its branch copy is architecture v3 at stage 4 (leak check). task253 is in flight.
  - Both were drawn on 2026-10-11, and task130 sits inside task253's 12-build window.
- **Shared surface:**
  - task253 names Timothy Miller in `rent_relief_programme_rules_2027.pdf`, and task130's hardened pack names Edward Miller.
  - Once both packs are indexed, the guard's people rule (`people.last`, a surname used in a recent build) returns BLOCK. Neither branch's index holds the other's pack, so neither surface check raised it.
  - The first name Timothy is also on the cards of task110, task117 and task134 (Timothy Gonzalez), although the pack scan does not find him in task134's pack. Miller is also on task107's card.
- **Clears it:** a rename of Timothy Miller, in the rules PDF and in the card's `world.people`. No figure, rung or file moves.

**2. task253 against task228 (in flight, `perssathya/task228-guardrail-alert-metric`): the persona first name Steven. Fiction-marker echo, soft, pending.**
- **Shared surface:**
  - task253 names Steven Cabrera, the survey contractor's lead, in `rhcs2026_methodology_note.pdf`. task228's card lists Steven Velazquez.
  - task228's pack is not committed, so the index cannot confirm he is in it. If he is, `people.first` (a first name used in a recent build) is a BLOCK, because task228 sits inside the window.
- **Clears it:** a rename of Steven Cabrera in the methodology note and on the card.

**3. task253 against task134 (in flight, `sathya8571/task134-reentry-returns`): Shape echo, soft, not reject.**
- **Status:**
  - task134 has no ledger row. It is at stage 4 (leak check), and its own pre-flight was CLEAN.
  - It was drawn the same day, eight builds before task253 in draw order, which puts it outside the guard's three-build bans.
- **Shared surface:**
  - No file name, schema, prompt wording (masked overlap 0.000) or entity is shared. The surface score (0.144, 99.5th percentile) comes from layout, format mix and deliverable species alone.
  - What a reviewer holding both would recognise is the outline:
    - a local government office sizing a fixed programme resource for 2027 by area (six supervision districts against nine neighbourhoods);
    - a council vote as the deciding event (the Commissioners Court on 24 November against Council on 9 February);
    - a workbook with a row per area, paired with a png chart drawn per area.
  - On the cards: `allocation_to_total`, `council_or_assembly`, `vote_or_meeting` and `local_government`, with deliverables xlsx and png.
  - Two things differ:
    - The ask construction (calendar-first against constraint-first).
    - Calibration, which is `none` on both: an absence, not a shared organ.
  - The drivers differ (see Clean).
- **Clears it:** nothing is required. If the author wants more distance, the axis is the deliverable species.

## Track B findings, mechanism

**1. task253 against task230: Template. The same driver carries the decisive rung in both.**

**Status.**
- The ledger is silent on both.
- task230 is in hardening loop 1 (stage 2, design), after solver round 1 landed its call. task253 is at stage 4 to 5, with no round yet.
- Both were drawn on 2026-10-11 on separate branches, task230 first: its card was registered at 09:09 UTC, task253's at 15:36 UTC, and task230 sorts immediately before task253 in the guard's draw order.
- Both are still shippable, so this is a fix before either ships.

**Decisive moves, with the domain nouns stripped.**
- **task253:** "Units that answered stand in for the units that did not only within classes of a frame attribute that drives both answering and the outcome, so the adjustment is made within those classes. Adjusting within the strata the sample was drawn in keeps the answerers' mix and under-counts the areas rich in the class that answers least and scores highest."
- **task230:** "Units not yet switched stand in for the switched units' untreated trend only within bands of an attribute that drives both the order of switching and the outcome's trend, so the comparison is made within those bands. Comparing against the whole not-yet-switched pool keeps that pool's mix and books its trend as the switch's effect."
- **The same claim? Yes.**
  - Both say three things:
    - the stand-in group was selected on an attribute that also moves the outcome;
    - so the stand-ins represent the target only within classes of that attribute, or reweighted to the target's mix on it;
    - and the default pool keeps the stand-ins' own mix.
  - One is a missing-response problem and the other a missing-counterfactual problem. The insight a solver has to reach is the same, and so is the check that reaches it: tabulate the stand-ins against the target by a categorical attribute held in a second file.

**Paths, in order.**
- **task253:**
  1. Income annualised by pay period and pooled; rent and separately billed utilities put on a monthly basis; burden flagged.
  2. Dispositions joined to the registry extract, and the out-of-scope outcomes set aside.
  3. **Base weights adjusted for nonresponse within registry licence class. This is the decisive step.**
  4. Units enrolled on 1 January counted from the effective-dated register.
  5. The pro rata split, with Eastgate capped at 447, and largest remainder once.
  6. The asks: the decisive weights applied to the burdened households on two device paths.
- **task230:**
  1. Non-patient accounts dropped, registrations merged, and the switch week's two rows reconciled.
  2. Each patient's handover week mapped, and the settled weeks after it.
  3. Each switched patient's reference-period level.
  4. **The level carried forward by the old-tracking movement of patients in the same engagement segment still on the old build. This is the decisive step.**
  5. The settled change per KPI, against the filed three per cent line.
  6. The asks: the KPI grid's values, weekly active patients, and the count on new tracking.

**Where the shared move sits.** It is the decisive rung in both, and neither build demotes it. The ladders around it line up too:
- **The stump rung is the textbook default in both.**
  - In task253 it is the design strata (R2), which ties every stratum control.
  - In task230 it is the whole not-yet-switched pool (R3), which passes the pooled pre-trend check.
- **The next rung up is a numeric proxy for the class in both.**
  - In task253 it is size bands built from `units_in_building` (R3).
  - In task230 it is quintiles of reference-period volume (R3b).
- **The class itself sits in a second file reached by a join in both:** the registry extract's licence class, and the CRM segment file.
- **Both certify that every estimator including the class converges.**
  - task253: "any class set, raking or propensity model that includes it".
  - task230: the segment crossed with volume, activity or sign-in weeks, within 0.034 points.

**Why the cards did not show it.**
- Both cards carry gap population, decisive G6 and Gate G `method_or_model_selection`, which is the guard's same-driver signature.
- But the strategy labels differ (task253 `composition_mix`, task230 `causal_design`), and the cards cite different client rigor patterns:
  - task253: survey nonresponse adjustment, pattern 1;
  - task230: product-analytics observational causal inference, pattern 1.
- So each build reads as bespoke from its own side, and each card differentiates only against task68.

**What could change it.** task230's round-1 hardening brief asks for a new rung on top of its within-segment comparison: "build the next rung so that exact step completes and still returns the wrong answer".
- If task230's committed hardening moves its decisive rung off that step, the shared move becomes a demoted rung there, and this pair drops to `clean_shares_components`.
- This finding is judged on both builds as they are committed now.

**The one axis.** task253's decisive pattern: G6, the reweighting of a stand-in group within the class that drives selection and outcome. task253 is the later draw, so the guard charges the BLOCK to it, and a new world does not clear it.

**Does the data survive? No, not as cut.**
- **What moves:**
  - Every graded figure rides on the decisive weights: the nine allocations, the nine basis figures and all 36 ask figures, since each ask is those weights applied on a segment.
  - The survey's response structure by licence class was generated to carry this rung.
- **What can carry across:**
  - the world (nine neighbourhoods, 3,000 vouchers, the enrolment cap and its register);
  - the registry frame;
  - the pay-period and billing mess in the person, household and utilities files;
  - the three tenancy deliveries with the receipt log;
  - the by-law order extract;
  - the deliverable pair.

## Clean, shares components by design

**task253's decisive move, with the domain nouns stripped:** "Reweight the units that answered to the eligible sample within classes of a frame attribute that drives both answering and the outcome, not within the design strata."

1. **task68 (built, rounds held, no portal result recorded): `clean_shares_components`.** It carries the same-driver signature on the cards (gap population, decisive G6, `method_or_model_selection`) and the `composition_mix` label.
   - **Its decisive move:** "A like-for-like change on a matched panel of continuing units linked across identity successions, because entrants and a price offset hold every aggregate flat. The bar is recovered from a closed corpus of settled dispositions."
   - **Not the same claim:**
     - task68 fixes the population over time, keeping the same units in both windows. task253 fixes who stands in for whom at one point in time.
     - task68's basis is chosen by back-testing 17 register dispositions (step 6 of 9), and task253 has no corpus.
   - What is shared is the G6 family label. task253's card differentiation says so, and it holds.
2. **task134: clean on mechanism.** It shares `allocation_to_total`, the decisive gap (population) and `method_or_model_selection`, as well as the outline reported under Track A 3.
   - **Its decisive move:** "a probability of an event within a fixed horizon when some units leave through exits that are not censoring". Its stump is Kaplan-Meier with the removals and deaths censored.
   - That is a survival-estimator choice under competing exits, not a stand-in reweighting.
3. **task87 v9 (no portal result recorded).** Its surface score is 0.147 (99.6th percentile), from layout, format mix and the xlsx-with-png pair. It also shares shape 05 and the `register` context artifact. Its driver is an exclusivity of time slots, encoded in the schedule and never stated in the procedure, that caps a delivered count. That is a different driver.
4. **task100 v2 (submitted, result not recorded).** Its surface score is 0.140 (99.4th percentile), from the same three axes, plus a "can only" opening (see Corpus habits). Its driver is forward-period membership, where members who skipped an optional stage complete a period early. That is a different driver.
5. **task130.** It is promoted only on main's copy (xlsx with png); the hardened copy ships xlsx with docx. Its driver is regression to the mean in a group chosen on an extreme value of a noisy outcome. That is a different driver. Its persona is under Track A 1.
6. **task254 (this author's sibling, next in draw order, stage 2).** It shares the objective (Descriptive & Distribution) and `method_or_model_selection`. Its driver is a time-to-onset distribution seen only through events before a lock date, right-truncated by rising uptake. It has a different strategy (`maturity_censoring`) and leads on a different gap (time).
7. **task124.** It shares shape 05, `allocation_to_total`, the decisive gap (population), the "We can only" opening and a `_split` workbook stem. Its driver prices the newcomers' share of a capped peak from analogs held down by the organisation's own intervention. That is a different driver.
8. **task132.** It shares the decisive generator G6, but its G6 move is renewal (a failed item is replaced at the bottom of the age curve), not a stand-in reweighting.

## Strategy monoculture

**The batch.** The twelve builds ending at task253 in the guard's draw order, with the in-flight cards included: task130, task132, task133, task134, task135, task180, task181, task182, task228, task229, task230 and task253.

**`stump_strategy` shares.**
- Three strategies carry 2 builds each:
  - `maturity_censoring` (task134, task181);
  - `causal_design` (task180, task230);
  - `decomposition_attribution` (task182, task228).
- Six carry one build each: `forecast_method_backtest`, `population_selection`, `stated_rule_hard_construction`, `other`, `grain_or_unit` and `composition_mix` (task253).
- The largest share is 2 of 12, under a third.

**The two capped architectures.**
- The withheld rule with an official decoy: 0 of 12 (cap 2).
- The certified-record decoy (`validated_decoy`): 0 of 12 (cap 3).
- No card sets `official_decoy`. `decisive_rule_filed` is false on task130, task134, task135 and task180, none of them with a decoy.

**No monoculture finding.** Three notes the labels hide:
- **The labels split one mechanism.** task230 (`causal_design`) and task253 (`composition_mix`) carry the same stand-in reweighting move. Counted by mechanism it is 2 of 12, still under a third, and it is the Track B finding above.
- **Other concentrations.**
  - `method_or_model_selection` carries 5 of the 12, which is the guard's overuse WARN.
  - The decisive gap is population in 6 of the 12.
  - G6 is the decisive generator in 3 of the 12 (task132, task230, task253).
- **The author's next build moves the window.** Ending at task254, `maturity_censoring` reaches 3 of 12 (task134, task181, task254), the guard's warn level, and `method_or_model_selection` reaches 6 of 12.

## Corpus habits

- **Pack file roles.**
  - `data_dictionary` appears in 61 builds and `export_manifest` in 34; `data_notes` and `provenance` appear in 12 each.
  - task253 ships none of them. Its dictionary is `rhcs2026_codebook.xlsx` and its provenance sits in `housing_research_holdings.xlsx`, in the organisation's own idiom.
- **The "X can only Y" constraint-first opening.**
  - It opens 5 of the 122 prompts with text on file (task3, task100, task124, task228, task253): four of them since task100, and two inside the current window (task228, task253).
  - task124 and task253 open on the same three words, "We can only".
  - The voice check classes task253 as constraint-first and flags no carrier phrase and no repeated run.
- **Council and local-government furniture.**
  - The forum `council_or_assembly` is on 3 cards (task117, task134, task253), and the org family `local_government` is on 5 (task98, task117, task125, task134, task253). Two of each fall in the window.
  - The forcing event `vote_or_meeting` carries 3 of the 12.
- **Allocation to a fixed total.** Shape 05 is on 9 cards, four of them since task123 (task123, task124, task127, task253), and `allocation_to_total` is on 8.
- **xlsx with png.**
  - This pair is on 7 builds (task87, task100, task102, task106, task120, task134, task253), two of them in the window.
  - It is not the modal pair, since docx with xlsx and pptx with xlsx are as common.
  - It is, though, the pair that put task87, task100, task130 and task134 at the top of the surface ranking.
- **Same-day parallel draws on separate branches.**
  - On 2026-10-11, ten builds were drawn or rebuilt on branches whose cards had not reached main, and two of them share a driver.
  - Neither guard and neither surface check could see the other. This is a process gap, observed here rather than authored.

## What to redraw
1. task253: the decisive pattern (G6, the stand-in reweighting within the class that drives selection and outcome), which repeats task230's. This is Track B, and the data does not survive as cut.
2. task253: rename the persona Timothy Miller, whose surname repeats task130's Edward Miller inside the window. Track A.
3. task253: rename the persona Steven Cabrera, whose first name repeats task228's Steven Velazquez (pending task228's pack). Track A.
4. task253 against task134: nothing is required (a soft Shape echo).

**Bookkeeping notes (none of these is a finding):**
- `.claude/skills/clone-check/.cache/fingerprints.json` is tracked, and this check's extract refreshed it (task253 added). Committing it is the main session's call.
- task253's card and task230's card each differentiate only against task68.
- `pipeline.json` for task253 has an empty `duplicate_check` block. Filling it is the main session's step.
