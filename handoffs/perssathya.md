# perssathya: where work stopped

Updated 2026-10-13. Work is on `main` (one branch); each build's state is in its `pipeline.json`.
task230 (2026-10-12) and task129 (2026-10-13) are SHIPPED and wait on the portal; task123's determinism
repair is RESHIPPED. task229's design 1 shipped (PR #18) and failed the portal's determinism QC.

**task229: architecture 3 (the number's last), redrawn into hydrometry 2026-10-13; stage 2 done, stage 3 next.**
- Designs 1 (firmware read health) and 2 (3PL stock-record accuracy) are spent. Architecture 3 was drawn on
  2026-10-13 as a city's cycle-counter network and redrawn the same day, before any data was cut, because
  that world failed the domain swap (the deciding quantity was traffic engineering under a borrowed
  General Statistics label).
- World: the Regional District of Corriston's 22-station hydrometric network (Physical & Environmental
  Sciences, sensor-calibration-measurement). Daily discharge is published from the day's mean water level
  through each station's rating; below two peaking plants (Talbot Canyon since 2017, Merrin Falls from
  June 2027) the river swings tenfold inside each day, so the convex rating read at the daily mean
  publishes 13 to 31 per cent low. Planned call: C104 and C105 from January, Sable Creek from May, C112
  and C113 from July; the default files Sable Creek alone.
- Card v3 re-registered (guard WARN answered, heart WARN, no BLOCK); precut exit 0 (49 checks).
- **Resume:** `task229/pipeline.json` (`resume`), then the design note's `## Builder's work order`,
  `## Ask sheet` and `## Tried and rejected`.

**task230: SHIPPED 2026-10-12** (asks rebuilt, judge APPROVE, leak reader clean twice); waiting on the
portal.

**task228: paused by the author.**
- Branch `perssathya/task228-guardrail-alert-metric` at 9120146.
- Design 1 (experiment-platform paging alert): its round-2 pass was on an earlier cut, and it failed
  the domain-coupling rule when revived.
- Design 2 (soil-moisture collocation) is spent: rounds 3 and 4 landed.
- Design 3 and design 4 (granted as an exception) found no architecture. Data-health estimator choices
  key G12 or G16, which task181, task182, task445 and task446 hold in the ban window.
- The card on file is design 2's.
- **Resume:** once task229 or task230 ships, a designer redraws architecture 4. It works under a G16
  waiver if the author grants one then, or without one if the window has moved.

**Approved by the author but not started.** Fix `guard.py`'s draw order on `main` so same-date cards
sort by registration time, and check that no shipped build's verdict changes. This is shared tooling:
PR it under `perssathya/skills-<slug>`.

**Lessons from this run.**
- Seven in-house rounds landed on reflex corrections or visible symptoms:
  - the comparison pool held to the engagement segment, then to eligible phones (task230 design 1);
  - collocation, then a second-station independence check (task228 design 2);
  - accrual since the last count, seen in the data (task229 design 2).
- The one that held (task230 design 2) used a domain effect the solver never modelled.
- The solver's hygiene executes these ask devices, so they are spent:
  - repeated-row dedup, and minutes logged per session;
  - change files over base lists, unit conversions and closed days;
  - effective-dated maps, and UTC against contract zones;
  - latest reviews, and band and indexation rules.
