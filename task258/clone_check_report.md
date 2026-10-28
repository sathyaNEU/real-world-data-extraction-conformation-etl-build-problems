# Clone check, task258

Author-triggered, 2026-10-28. task258 is `SHIPPED_APPROVED`, delivered 2026-10-27, portal APPROVED 2026-10-27.
Mechanism source is the design note, so Track B is readable rather than back-fitted.

**Verdict: no Template finding and no clone. Two real findings, neither of them about task258 alone:**
an axis-hygiene breach across the 255 to 260 batch that `stumping` Part 6 bans directly, and a Track A surface
metric saturated by corpus-wide furniture rather than by anything specific to this build.

`guard.py surface` extracted 303 cards, screened 301 builds over 300 pairs in scope and promoted 7 for
adjudication. Promotion is triage: the skill is explicit that a number does not decide and that there is no
Template finding without the shared decisive move named in one sentence. All 7 were read and all 7 are clean on
that test.

## task258's decisive move

The intervention's effect works through a step that needs a reference each unit's own served document must
carry. Every past application ran on units whose documents carried it, so the back-test passes by construction,
while part of the forward population assembles its document after delivery and the step cannot reach it. The
solver has to see that the intervention cannot reach part of the forward population at all.

## The 7 promoted pairs, adjudicated

| Pair | Surface (pct) | Promoted by | Status | Verdict |
|---|---|---|---|---|
| 255 / 258 | 0.101 (99) | corpus top 1 per cent surface | both delivered | clean, surface only |
| 256 / 258 | 0.100 (98) | two of three axes, consecutive | both delivered | clean, axis breach |
| 258 / 259 | 0.100 (98) | top 3 per cent, back to back | both delivered | clean, surface only |
| 258 / 260 | 0.084 (70) | two of three axes, consecutive | both delivered | clean, axis breach |
| 258 / 471 | 0.084 (70) | gap, pattern and Gate G all collide | both delivered | clean |
| 258 / 303 | 0.081 (56) | gap, pattern and decision all collide | both delivered | clean |
| 258 / 273 | 0.084 (70) | gap, pattern and Gate G all collide | 273 live and spent | clean |

- **255** fits the upper tail of a size distribution made of two kinds whose tails differ far more than their
  bulks, each fitted through the record's own floor and ceiling. A tail-mixture problem; nothing to do with
  reachability. Promoted on surface alone.
- **256** needs the share of a population whose several correlated measurements all fall inside a box, when the
  population's records hold only two other measurements and the box comes from a reference group that differs.
  A multivariate accommodation problem.
- **259** carries a level to a reference date by how the level itself moves at fixed grade inside the reporting
  units, where reporters' own changes run faster because individuals climb within grade. A within-grade drift
  problem.
- **260** asks whether an improvement measured on one shared sample of raters scoring one shared sample of items
  holds for new raters and new items. A generalisability problem, and an interval resampling one dimension is
  too narrow.
- **471** recovers a true count from a full count and an independent recount where, for one group, the two
  counts miss the same members, so the estimate stays short exactly there. Correlated non-coverage between two
  measurements of the same units, not whether a treatment applies.
- **303** is the closest on the mechanism axes after 471 and the one worth stating carefully. Both builds are
  about an intervention's measured effect overstating what it will deliver. They part on why. task303 is
  attribution: part of a unit's recorded losses is a shared upstream event that every unit on the same source
  logs under its own device, so summing by cause and device credits the intervention with losses that
  originated elsewhere. task258 is reachability: the intervention cannot apply to part of the forward
  population. Attribution against reach.
- **273** needs the demand a failure leaves with no path to supply, where the failure takes out the whole area
  bounded by the nearest devices that can actually be operated and operability sits only in a maintenance
  history kept for another purpose. A connectivity problem, and 273 is live and spent, which the skill scores
  weaker than a delivered collision.

## Finding 1, axis hygiene across the batch, Track B

`stumping` Part 6 bans two of three mechanism axes colliding between consecutive builds. task258 breaches it
twice, against task256 and task260, both two apart and both delivered. Beyond the consecutive window, gap
`population` with decisive generator `G8` carries **four** builds (task258, task303, task273, task471) and gap
`population` with Gate G `method_or_model_selection` carries more still across 255, 256, 258, 471 and 273.

This is not a clone and no redraw of task258 is implied: the drivers are all different and the build is
approved. It is the draw hygiene the fingerprint guard exists to enforce slipping across a whole batch, which
is the shape the client's templated note was about. The axis to vary on the next draws in this range is the
decisive gap, because `population` is doing the work in almost all of them.

## Finding 2, the surface metric is saturated by corpus furniture, Track A

Six further pairs sit at surface 0.100 and the 98th percentile and were **not** promoted (task130, task199,
task233, task234, task235, task236 against task258). A band that wide at the same score is a property of the
corpus, not of task258. The corpus habits confirm it: the filename `data_dictionary` appears in **112 builds**
and `export_manifest` in **69**. The Track A number for task258 is therefore shared furniture, and the repair
is corpus-wide variation of the furniture rather than a rename of this build.

Also worth the author's attention: `leak.py` sweep 1 treats a shipping data dictionary as a LEAK that stops a
ship, while 112 delivered builds carry one. Those two rules disagree.

## Track A, specific to task258

- `guard.py heart`: nearest driver or stump text on file **0.05** against every card, lineage entry and ledger
  row, under the 0.12 WARN threshold and well under the 0.30 BLOCK threshold.
- No shared multi-word invented name. task258's eighteen (Brolga Media, Matchday, Tideline, Pressframe
  Syndication and the rest) are unique to it.
- No shared full persona name. Two component repeats, Track A only, repaired by a rename and informational on
  an approved build: the first name Doris also in task165, the surname Murillo in task447.
- Shape 14 with `pick_one_of_n` is shared with task187 only, whose mechanism is unrelated.

## No strategy monoculture

`population_selection` holds 35 of 304 cards, 12 per cent, against the one-third threshold. task258 carries no
withheld rule, no official decoy and no validated decoy. Mechanism coverage across the corpus is 280 cards
readable, 17 unavailable, 4 note-only.

## What this check did not cover

- The **adjudicated `clone-auditor` pass with its subagents was not spawned.** This is the free half,
  `guard.py heart` and `guard.py surface`, plus the Track B reads above taken by hand off the cards.
- The tracked baseline `clone-check/corpus/fingerprints.json` is stale at 128 of 304 cards and does not contain
  task258. The screen above ran off a fresh extract into `.cache/`, so it is current; the tracked baseline still
  wants refreshing with
  `fingerprint.py extract --out .claude/skills/clone-check/corpus/fingerprints.json`.
- Only 30 of 209 task folders held an unpacked pack. task258's was unpacked for this check, so pack-level
  comparison reaches 31 packs; the other 270 builds were compared on cards and prompts.

## Correction to an earlier reading in this session

An interim verdict given before the surface screen finished reported no Track A finding and predicted the screen
would not change the Track B verdict. Both were wrong. The screen promoted 7 pairs, 4 of them on mechanism axes
that had not been compared, and it is where Finding 1 came from.
