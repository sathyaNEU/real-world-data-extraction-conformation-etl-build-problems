# Clone check, task258

Author-triggered, 2026-10-28. task258 is `SHIPPED_APPROVED`, delivered 2026-10-27, portal APPROVED 2026-10-27.
Mechanism source is the design note, so Track B is readable rather than back-fitted.

**Verdict: clean, shares components by design.** No Template finding, no Track A finding against any build.
Three pairs were close enough on the axes to need reading and all three were adjudicated clean.

## What task258's driver is

The decisive quantity is how many units an intervention moves across a threshold when its effect works through
a step that needs a reference each unit's own served document must carry. Every past application ran on units
whose documents carried it, so the back-test passes by construction, while part of the forward population
assembles its document after delivery and the step cannot reach it. Gap population and time, decisive generator
G8 (reachability against magnitude), Gate G `method_or_model_selection`, strategy `population_selection`,
shape 14, decision `pick_one_of_n`, calibration organ `pilot_log`.

## Track B, the mechanism

| Pair | Shared axes | Status both | Verdict |
|---|---|---|---|
| task258 / task471 | G8 decisive, Gate G, `population_selection` | SHIPPED / SHIPPED | clean |
| task258 / task228 | domain and task type | APPROVED / SHIPPED | clean |
| task258 / task235 | domain and task type, Gate G | APPROVED / SHIPPED | clean |

- **task258 against task471.** The closest pair on the axes: same decisive generator, same Gate G mechanism and
  same stump strategy, both delivered. Not the same task. task471's solver has to see that two nominally
  independent counts miss the same members for one group, so a dual-system estimate stays short exactly there
  and the shortfall is recovered from that group's ratio to a companion group. task258's solver has to see that
  the intervention cannot reach part of the forward population at all. One is correlated non-coverage between
  two measurements of the same units; the other is whether the treatment applies. A reviewer holding both
  learns something new from the second, which is the test. Shared axes here are component labels, not the
  driver.
- **task258 against task228.** Same cell, and that is the whole overlap. task228 turns on building each ratio's
  variance at the randomisation unit, because events cluster inside the units that were randomised and treating
  them as independent understates it severalfold. Different gap, different generators (G2 and G17), different
  Gate G (`signal_vs_noise_or_hold`), different strategy (`grain_or_unit`), different shape (10).
- **task258 against task235.** Same cell and the same Gate G label, and the two sit nearest conceptually: both
  concern a population the measurement cannot yet speak for. They part on which thing is missing. task235 is
  censoring by delivery chance, whether the outcome has had its chance to be observed, repaired by reading the
  loss over items whose device has since made contact. task258 is reachability, whether the intervention can
  apply at all. Different strategy (`maturity_censoring`), different shape (10), different decision family
  (`designation_set`).

## Track A, what a reviewer sees

- `guard.py heart`: nearest driver or stump text on file **0.05** against every card, lineage entry and ledger
  row, far below the 0.12 WARN threshold and the 0.30 BLOCK threshold. Nearest neighbours are task104 (0.05, a
  re-thresholded logged z-score) and task198 v1 in lineage (0.05, an outcome falling with parallel servers).
- No shared multi-word invented name with any card. task258's eighteen invented names (Brolga Media, Matchday,
  Tideline, Pressframe Syndication and the rest) are unique to it.
- No shared full persona name. Two component-level repeats, Track A only: the first name Doris also appears in
  task165 and the surname Murillo in task447. The repair for either is a rename, not a rebuild, and task258 is
  already approved, so this is informational.
- Shape echo: shape 14 with `pick_one_of_n` is shared with one build only, task187, whose mechanism is
  unrelated.

## Corpus-wide notes, reported apart from the pairs

- **Cell concentration.** `product-analytics/metric-definition-measurement-science` now carries three shipped
  builds: task228, task235 and task258. Three different drivers, so not a finding, but the cell is the most
  worked one in the domain and a fourth draw there should expect to answer for it.
- **No strategy monoculture.** `population_selection` holds 35 of 304 cards, 12 per cent, against the
  one-third threshold. task258 carries no withheld rule, no official decoy and no validated decoy.
- **Calibration idiom.** `pilot_log` appears in 14 other cards. An author habit worth varying, not a pair
  finding.

## What this check did not cover

- The tracked corpus baseline, `clone-check/corpus/fingerprints.json`, is **stale: 128 of 304 cards and it does
  not contain task258**, so the mechanical hard-tell pass could not be run off it. The hard tells it would have
  carried are byte-identical files, same-seed tables surviving a rename, identical column sets and masked prompt
  wording.
- Only 30 of 209 task folders hold an unpacked pack; the rest hold `target.zip` alone. task258's was unpacked
  for this check, so the pack-level comparison reaches those 31 packs, not the corpus.
- The adjudicated `clone-auditor` pass with its subagents was not spawned. This report is the free half,
  `guard.py heart` and `guard.py surface`, plus a Track B read taken by hand off the fingerprint cards.
- Refreshing the baseline needs a checkout holding every pack:
  `fingerprint.py extract --out .claude/skills/clone-check/corpus/fingerprints.json`.
