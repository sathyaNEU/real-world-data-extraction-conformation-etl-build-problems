# perssathya: where work stopped

Updated 2026-10-13 (task229 shipped; task131 re-rooted). Work is on `main` (one branch); each build's state is in its `pipeline.json`.
task230 (2026-10-12) and task129 (2026-10-13) are SHIPPED and wait on the portal; task123's determinism
repair is RESHIPPED. task229's architecture 3 (hydrometry) shipped 2026-10-13; its design 1 had failed the portal's determinism QC.

**task131: DRAWN 2026-10-13 (architecture 2, tariff evaluation); in stage 2.**
- Re-rooted from the Swiss co-operative's card offers (FAILED_TO_STUMP, and crm-loyalty-retention is not a
  client task type) into Energy Systems & Utilities, tariff-demand-response-evaluation x Experiment & Causal.
- Murrandi Regional Power's summer 2025-26 trial of three peak-window designs; the call is which design, if
  any, flat-rate households move onto from 1 July 2027, judged on the 2027-28 50% POE maximum demand.
- **Resume:** stage 2 from `task131/pipeline.json` (ladder, screen, fork table, closure, ask sheet, prompt.txt,
  precut).

**task229: SHIPPED 2026-10-13 (architecture 3, hydrometry); waiting on the portal.**
- The Corriston Basin Hydrometric Cooperative's 23-station network (Physical & Environmental Sciences,
  sensor-calibration-measurement x Data Quality Monitoring). Call: flag C104 and C105 from January 2027,
  C107 from May, C112 and C113 from July; the other 18 hold. The default files Sable Creek alone; the
  blanket flag on every station below a plant adds C124, which the Vardy River keeps within 1 per cent.
- Gates: 1,697 generator assertions, verify.py 313 checks, byte-identical rebuilds, figures_check, precut,
  leak.py REVIEW only; leak reader clean on two reads; judge pass 1 DETERMINISTIC, APPROVE.

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
