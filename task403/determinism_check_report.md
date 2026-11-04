# determinism-check report, task403, 2026-11-04

## Pass 1 (target.zip c80ea809, judge thread run by the coordinator)

**Verdict:** DETERMINISTIC. **Disposition:** FIX_NOW (SOLUTION_WRONG on the ask's June to October paid shares, 0.1 to
0.2 points under the golden in the thread's reconstruction). The thread kept the order and its own derivation, written
before it opened the graded blocks, filed (A) on about 2,500. The coordinator traced the cells to 46 plan-change log rows
rooted at subscriptions no register row names (an unlogged app change followed by a logged web change, 21 of them
charged from July to October); the fix pass also found a June cause (the old platform's Toronto-stamped copies read from
Toronto midnight kept 8 copies). Closed in one generator pass by changing the world (a trial's plan changes all reach the
log or none does; the old platform's web and phone copies begin at 04:00 Toronto), with the programme sheet's Funding
line filed in its own voice (the minor Gate E note) and the steps' price and matching sentences. No graded figure moved.

### The thread's verdict, verbatim

**Order kept:** yes. derivation.md was written to disk from prompt.txt and target/ alone before graded_blocks.md was opened. That derivation committed to the wrong programme (A, price, about 2,500 conversions, from the 1 Nov 2025 date step). It missed the autoplay-run expansion, the unlinked plan-change charges and the exposure-based split. All of those were rebuilt afterwards from the files, not copied from the blocks.

**Verdict:** DETERMINISTIC, SOLUTION_WRONG on ask 8 (the June to October paid shares, which are off by 0.1 to 0.2 pt under my best reconstruction).

**Disposition:** FIX_NOW. Re-verify the June to October cells of the monthly table and regenerate the blocks. The shipped files and the committed call stay as they are, so no model rerun is needed. The close margins noted under Evidence are left as they are.

**Why:** The fall is the loss of "a season still to come". In every month before November, trials that had played a season whose last episode came out after their trial ended paid at about 56.8% against 39.5% for the rest. Both rates are flat across months and across the 1 Nov price date. This winter none had such a season, so conversion collapsed to 37.1%. The price date coincides with the finales (last releases 31 Oct), so the date step is confounded, and the exposure split separates the two. The slate is about 2,100 against about 200 for the price, so (C) is forced. The competing price story (A, about 2,500 from the date step) is the easy route, and it is refuted by the data.

**Evidence (recomputed from the files):**

| Item | Golden | My recompute | Result |
|---|---|---|---|
| Trials in the two winters (Toronto start) | 17,965 and 17,292 | same | reproduced |
| Played an episode | 94.3 and 94.0 | 94.31 and 94.02 | reproduced |
| Still subscribed | 52.7 and 38.4 | 52.72 and 38.40 | reproduced |
| First charges collected | 98.0 and 96.6 | 98.01 and 96.63 | reproduced |
| Paid conversions | 9,283 / 51.67% and 6,416 / 37.10% | same | reproduced |
| Waterfall endpoints | 8,900 and 6,400 | 8,935 and 6,416 | reproduced |
| Exposed share, last winter | 70.2% | 70.23% | reproduced |
| Paid, exposed vs not | 56.9 vs 39.4 | 56.86 vs 39.43 | reproduced |
| Slate cost | 2,100 | 2,116 | reproduced |
| B: 472 declined first charges, recovery 72.0% to 52.5% | 100 | 92 | reproduced |
| D: channel mix | 100 | 103 to 105 | reproduced |
| Price, as the rest of the fall | 200 | 208 | reproduced |
| Gap | 1,900 | 1,908 | reproduced |

- **Monthly average episodes, February to October:** 4.93, 5.40, 5.67, 5.82, 6.38, 7.13, 8.00, 9.08, 8.83. All nine match the golden after the autoplay-run expansion. That expansion applies to smart TV rows from 8 Feb to 27 Oct 2025, where minutes exceed runtime. Runs are counted by the calendar runtimes with the partial episode counted, which gives last-episode fractions of 0.9 to 1.0 in 98% of rows. It also needs the account and content crosswalks and a once-per-episode count.
- **Monthly share paid:** February to May reproduce at 50.9, 51.2, 54.0 and 52.4, after matching 944 unlinked first charges to trials. The match is the trial without a charge whose end most closely precedes the first attempt, in the provinces the tax rate names. Every gap is 0.0 to 0.1 h once the legacy TV timestamps are re-timed.
- **Cells that do not reproduce:** June to October give 52.1, 53.8, 54.8, 53.9 and 49.8, against the golden's 52.2, 53.9, 54.9, 54.1 and 49.9. The match is invariant to greedy order, to allowing reuse, and to the province filter. The cause of the golden's offset is unidentified.
- **June ghosts:** 790 legacy web and phone sign-ups from 9 to 19 June match a new-platform row field for field once shifted by +4 h, so dropping them is forced by the files. The legacy smart TV and tablet rows carry Toronto time stamped Z. Viewing starts only at +4 h and the first charge falls at +7 d +4 h.
- **Survivable forks (do not change the call):**
  - *Price value:* "price takes the rest" gives 200. A direct pre/post estimate on non-exposed trials gives about 400, but that double counts B and D and breaks "account for the fall once". A date-step estimate among non-exposed trials gives about -1 pt, which is noisy.
  - *Gap rounding:* the gap rounds to 1,900 only if the price lands between about 166 and 216. A price of 150 or less gives 2,000.
  - *"or none":* the files give no value per conversion and no cost hurdle, so the largest valuation is the only reading, and (C) is also conditional ("Yes, if Gravel & Gold locks by July"). This is a minor Gate E risk.
  - *Runner-up:* price at about 208 versus D at about 105 and B at about 92 holds.

**Files/Hygiene:** PASS. 14 files in 4 formats (csv, parquet, xlsx, pdf), with a 73k-row register and 440k viewing rows. The distractors are the cancellation survey (too_expensive 18.6% to 44.6%), the paid-media sheet, the product release log and the price notice. Layer 1 mess is all organic: the 9 June migration, ID and sub-ID changes, UTC against Toronto time, a processor change, and tax-inclusive against tax-exclusive amounts. No authoring or benchmark language and no temporal contradictions. Nothing exclusion-level. The synthetic corpus has no public-answer contamination.

**Stump power:** High. A strong analyst reads the fall as the price date (the sheet's A, a 2,000-plus step on the notice date, the survey, the paid-media sheet) and files (A) at about 2,500 with a slate of about 500. Only an exposure-based comparison group (seasons still to come), which holds across dates, shows the opposite. The Layer 1 reconstructions (ghosts, autoplay, unlinked plan-change charges) also make the 8 asks hard.

**Stumping type:** `mechanism: decomposition_attribution (comparison group and confound)`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The numbers are honest. The stump is the unit of analysis (exposure to an unfinished season versus the date step), and it survives clean data.

**Three rules:** `domain: pass`, `layers: pass`, `decisive_step: analytical`. Layer 1 is the platform migration, duplicated legacy rows, re-timed stamps, autoplay-run logging and unlinked plan-change subscriptions. Layer 2 is the cohort and exposure decomposition of a conversion fall into programme causes, which a subscription-growth team would run. The easy route is the date-step, price-led attribution, or the survey's stated reasons, which files (A) at about 2,500 with the slate at about 500. The swap test fails to read the same.

**Fix:** solution only. Re-derive the June to October cells of ask 8 and state the matching rule in submission.md. If the golden's cells are right, record the extra rule. Optionally add a sentence to the solution block that the price is the remainder after B, D and the slate, so the gap of 1,900 is explained.

## Pass 2 (target.zip 08a813d0, judge thread run by the coordinator, round1_findings.md opened with the graded blocks)

**Verdict:** DETERMINISTIC. **Disposition:** APPROVE, no repair. The thread kept the order and its own derivation again
filed (A) (Gate F high); every main-call figure, all nine paid shares and all nine episode averages reproduce from the
files, and both readings of the unlinked charges select one set of 938. Its residual note (a gross price valuation near
400) is the fork-table row SF8, closed by the programme sheet's sentence that the four valuations and what none of them
addresses account for the winter's fall once, and moves neither the call nor the slate's figure.

### The thread's verdict, verbatim

**Order kept:** yes. derivation.md was written to disk from prompt.txt and target/ alone before graded_blocks.md and round1_findings.md were opened. My first-pass derivation committed A (price) because I had not yet found the "season still to come" structure (only a 14-day recent-release proxy). I then reproduced the golden's route from its steps and checked it against the files.

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. No repair needed. The optional note below (price valuation is a net residual) needs no file change and no rerun.

**Why:** The funding call (C, winter release slate) is forced by the files. Last winter's trials that played a season whose last episode aired after their trial ended (70.2%) paid at 56.9%, against 39.4% for the rest. None of this winter's trials had such a season, because the calendar's last episodes aired 31 Oct 2025. Conversion for trials with no season still to come is flat at 39.3-39.8% in every month from Nov 2024 to Sep 2025. The step down in the subscribed-at-end share sits at trials started from 24 Oct 2025 04:00Z, which is exactly the finale date. It does not sit at the 1 Nov price boundary. The price reading is therefore the surface read, and the slate is the data's structure.

**Evidence (recomputed from the files; all reproduced unless marked):**
- Trials: 17,965 and 17,292 (Toronto start; winter assigned by Toronto date). Reproduced.
- Played: 94.3% and 94.0%. Subscribed at end: 52.7% and 38.4%. First charges collected: 98.0% and 96.6%. Reproduced from trial_register, trial_viewing (via the two crosswalks), the charge files and plan_changes (chains up to depth 2 followed to the terminal subscription).
- Paid: 9,283 (51.7%) and 6,416 (37.1%). Last winter's rate at this winter's trials is 8,935. Fall 2,519. Reproduced.
- Slate: (51.67 - 39.43)% x 17,292 = 2,117, so 2,100. Reproduced.
- Rest of the fall: 402. First-charge recovery is 92 (declined first charges recovered 72.0% to 52.5%, on 472 declined charges), so 100. Channel mix is 103-105, so 100, and every standardisation variant I tried agrees. Price is the net 402 - 92 - 105 = about 205, so 200. Gap is 2,117 - 205 = about 1,911, so 1,900. Reproduced.
- Feb-Oct 2025 paid share and average episodes: all nine months reproduce to one decimal only after the Layer-1 cleaning the steps describe:
  - Drop the 790 old-platform web/phone copies. They match a new-platform row field for field once re-timed by +4h, with signup_page mapped through content_crosswalk.
  - Re-time the other old rows stamped from 9 Jun.
  - Match all 938 orphan first charges to the nearest preceding unlinked trial end within the provinces the tax rate names. Gaps are at most 3h, median 3 minutes. Both round-1 readings select the same 938, none in plan_changes.
  - Expand smart-TV autoplay rows (8 Feb-27 Oct 2025) over the season's following episodes on the calendar runtimes.
  - Results: Feb 50.9/4.9, Mar 51.2/5.4, Apr 54.0/5.7, May 52.4/5.8, Jun 52.2/6.4, Jul 53.9/7.1, Aug 54.9/8.0, Sep 54.1/9.1, Oct 49.9/8.8. They equal the golden. Counting the episode at the run's row start or at its true start gives the same values.
- Operationalisation test for the comparison group: trials whose season finale fell inside the window convert at 38.5%, like finished or no-season trials (39.3-39.9%), not like "to come" (56.7%). The data pin "last episode after trial end", and near variants give the same answer.
- Round-1 lines: both causes of the Jun-Oct share gap are closed in the files as they stand. The funding line now has a "none only if" clause. The step text for price and matching is consistent with what I recomputed.
- Residual fork, low risk: the sheet does not file how price is valued. The golden values it as the net fall among no-season trialists (205). The sheet's "account for the winter's fall once" supports netting. A gross reading (about 400) would change ask 4A, the runner-up margin and the gap to 1,700. Price is statistically about 205 +/- 130, so the A vs B/D ordering at the nearest hundred rests on the netting identity and not on a separate test. The main call and the slate figure are unaffected.

**Files/Hygiene:** PASS. 14 files in 4 formats (csv x7, parquet 440,424 rows, xlsx x4, pdf x2). Distractors are the paid-media workbook, the cancellation survey (45% "too expensive" in W25, the surface read toward price) and the product release log. They are not named for the trap. Layer-1 mess is real and system-made: ID migration with a crosswalk, a stamped-Z timestamp error, duplicate copies, unlinked plan-change subscriptions, two processors with different schedules and time zones, and autoplay rows. No authoring or benchmark language appears. Dates are coherent: trials to 1 Feb 2026, standard v3 of 2 Feb 2026, sheet of 6 Mar 2026. Nothing is exclusion-level.

**Stump power:** High. The easy route is price: the 1 Nov notice, the survey and the date coincide, and a recent-release proxy yields only about 500 for the slate (my own first pass). It gives A at about 1,800-2,300 and the wrong call. The correct route needs the season-in-progress comparison group and a counterfactual at this winter's trials. A strong model can fail without any ambiguity, because the data separate the groups cleanly.

**Stumping type:** `mechanism: decomposition_attribution`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The reported rates are all correct. The difficulty is attributing a real fall to the right driver, with the price date as a coincident confounder. On clean data the task still stumps.

**Three rules:** `domain: pass`, `layers: pass`, `decisive_step: analytical`. The deciding quantity is a funnel-conversion counterfactual against the right comparison group (trialists with and without a season still to come), which is what subscription-growth analysts estimate; the swap test (hospital/visits) fails to preserve it. Layer 1 is the migration, duplicate and orphan mess. Layer 2 is the attribution. The easy route is attributing the fall to the price date, giving A and a gap of about 1,700-2,200.

**Fix:** none.
