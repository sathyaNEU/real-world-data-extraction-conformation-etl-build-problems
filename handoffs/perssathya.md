# perssathya: where work stopped

Updated 2026-10-13 (task122 re-rooted and drawn). Work is on `main` (one branch); each build's state is in its
`pipeline.json`. task230 (2026-10-12), task129, task229 and task131 (2026-10-13) are SHIPPED and wait on the
portal; task123's determinism repair is RESHIPPED. In wave 1, task122 is DRAWN and in stage 2; task228 waits on the
author's call (a fifth architecture and a G16 waiver).

**task122: DRAWN 2026-10-13 (card v3, the slot's second built architecture), stage 2.**
- Varnmark Therapeutics' 52-week phase 2b of VMK-4410, an aldosterone synthase inhibitor, in albuminuric CKD
  (Biomedical & Clinical Research, longitudinal-outcomes-repeated-measures x Experiment & Causal, a domain never
  built). Call: which of 5, 10, 20 and 40 mg goes into the phase 3, judged on the eGFR difference from placebo
  after 36 months. Golden 20 mg (4 mL/min/1.73 m2; 40 mg 3, 10 mg 2, 5 mg 1). The field's two-slope model with the
  chronic phase from month 3 files 40 mg, because diuretics eased from week 12 let the higher doses' early fall
  partly recover and that recovery reads as chronic slope; the week-52 change files 5 mg.
- **Resume:** stage 2 from `pipeline.json` (`resume`); the arm-mean ladder and the parameter search are in the
  design note's Draw. v2's pack, goldens and reports are removed from the tree and kept in history.

**task131: SHIPPED 2026-10-13 (architecture 2, tariff evaluation); waiting on the portal.**
- Murrandi Regional Power's summer 2025-26 trial of three peak-window designs (Energy Systems & Utilities,
  tariff-demand-response-evaluation x Experiment & Causal). Call: default flat-rate households onto Design C
  (Stepped) from 1 July 2027, 11 MW off the 2027-28 50% POE maximum; A raises it 5 MW and B 20 MW, their
  pull-down after the window setting a new maximum on the design day's heat. The window cut on the average day
  files B at 15; the pooled whole curve files A at 13.
- Gates: 133 generator assertions, verify.py all agree, byte-identical rebuilds, figures_check, precut, leak.py
  REVIEW only (sweep 4); leak reader three reads; judge pass 1 NOT_DETERMINISTIC on one survey share (closed by
  convergence), pass 2 DETERMINISTIC FIX_NOW (two prompt pins applied), pass 3 DETERMINISTIC, APPROVE.

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
