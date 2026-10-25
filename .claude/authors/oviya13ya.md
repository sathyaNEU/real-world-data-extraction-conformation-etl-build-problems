# Author: oviya13ya

Account email ovi13ya@gmail.com. A session for anyone else ignores this file.

- **Lane:** Anomaly Detection & Diagnostics, task180 to task227. Two builds in flight; `status.py next oviya13ya`.
- **Status board:** https://claude.ai/code/artifact/eb99af75-757b-4101-b895-e17665c02495 (one row per task: the task and its call, status, links to the prompt, submission and `target.zip` on `main`, a short note, the date), updated at every commit point.
- **No retiring.** This author's builds are never retired: past the architecture cap, a SEND_BACK or a clone
  finding, a build is repaired or re-rooted until it ships. A determinism finding is fixed as the portal
  requires (`/fix-determinism`); if the fix makes the call easy, a new strategy is designed. A paused build
  is `PAUSED` or back in a wave as `FAILED_TO_STUMP`, never `RETIRED`, and retirement is never offered.
- **Every stump is unique** against every card on file: no driver, pattern or strategy repeated.
- **Resume:** `handoffs/oviya13ya.md`.

## Backlog

Work the waves in order, six tasks to ship per wave, two in flight at a time. `status.py next oviya13ya` names
the next task and `status.py --owner oviya13ya` shows each wave's progress. When a wave is fully shipped,
`status.py wave oviya13ya` prints the next one; add it below in that `SHIPPED` commit. The note says where a
task restarts: resume N (the stage it reached), redesign (the portal solved it), re-root (a new
architecture), new. A task from an objective no developer owns says so.

| Wave | Tasks, in order |
|---|---|
| 1 | task183 (FAILED_TO_STUMP: five one-group-by routes land its call on the clean truth, one a partition of the default path's own column; its wave-8 audit brief also handed the reader the figure key names) · task182 (PAUSED at stage 1, architecture 9: candidate 1 refused on the multiplicative-correction floor, and the alarm-interface-evaluation cell it cleared is NOT drawable on this objective, serving experiment-causal only) · task181 (FAILED_TO_STUMP, architecture 4: dial flat at 0.74) · task180 (FAILED_TO_STUMP, architecture 4: spent on an identity) · **task125 SHIPPED 10-23** (the three-visit cap is 0.18 of the 0.27-point rise, not the labour market; rebuild-verified at target.zip 5314b654417ae84b) |
| 2 | task184 (FAILED_TO_STUMP: judge SEND_BACK, architecture 2 spent) · task185 (FAILED_TO_STUMP at stage 5: the premium is linear in trigger-crossing days, so every non-conversion candidate buys 2 to 3 per cent inside its own family's spread) · task186 (FAILED_TO_STUMP: the scale law) · **task187 SHIPPED** (CH04, 100 MWh to the nearest 50; rebuild-verified at 34dc5a9160544d5a) · task188 (FAILED_TO_STUMP: the Gate C against Gate F dial) · task189 (FAILED_TO_STUMP: the licensed imputation family's spread on the graded figure is exactly zero) |
| 3 | task190 (PAUSED at stage 1, architecture 10: the blessed clause closed as a clause, all five horns measured) · task191 (FAILED_TO_STUMP: family spread zero, and a decisive step whose only output is a binary) · task192 (FAILED_TO_STUMP, architecture 3: screens 1 and 2 pass, screen 3 fails three ways; one Gate C still open, a calibration with a month term filing 504.483 and printing 500, a seventh cell the candidate table does not carry) · task193 (FAILED_TO_STUMP: decisive step an identity) · task194 (PAUSED at stage 1, architecture 16: closed the propagation shape corpus-wide, it being task125's own driver) · task195 (FAILED_TO_STUMP: spent on measurement) |
| 4 | **task196 SHIPPED** (RESHIPPED after a rubric rework; rebuild-verified at 863b7e3acd7250d8) · **task197 SHIPPED** (Kampvliet 72 per cent of contracted gain; rebuild-verified at ce23c1aa6f4a57e9, TWO-STEP rebuild) · task198 (PAUSED at stage 1, architecture 15: the labelled-index theorem; its note that it held the two remaining never-built AD cells is WRONG, that being a house-domain label artefact, but it holds a verified registrable signature on energy-systems-utilities/grid-reliability-outage-analysis) · task199 (FAILED_TO_STUMP: the score is identically the raw rise over the delivered-item rise; never portal-audited) · task200 (PAUSED at stage 1, architecture 5: four families closed from this one slot, including the R identity) · task201 (PAUSED at stage 1, architecture 13: the overidentified design's premise held and that is what killed it) · task202 (PAUSED at stage 1, architecture 5: the grain pincer travels with the step into any world) |

**No build in this lane was ever portal-audited.** All 13 `FAILED_TO_STUMP` verdicts are in-house Gate F calls
on clean-truth screens; every one has `portal: None` and an empty `portal_status`. Judge Gate F on the count
of cheap routes reaching the call, never on one reader landing it (`stumping` Part 1).

**Rebuilding a build in this lane.** 19 of the 24 rebuild with `python3 taskNN/generator/build.py`. The
exceptions, which a rebuild audit must not rediscover: **task197 is TWO STEPS**, `build.py` then `submit.py`,
because the second enriches `figures.json` and `build.py` alone leaves `figures_check.py` reporting 4 of 91
figures absent while `target.zip` still matches (house fix H33); **task199** uses `build_pack.py`; **task202**
uses `make.py`. task182, task198 and task200 have no generator, never having been cut. After a full rebuild
`git status` must be empty for the task folder, and a modified `figures.json` means an entry point was missed.
