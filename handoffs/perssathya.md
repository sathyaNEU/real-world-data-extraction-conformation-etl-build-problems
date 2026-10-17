# perssathya: where work stopped

Updated 2026-10-17 (wave 2: task235 shipped on architecture 2 after the judge's SEND_BACK of architecture 1; task236 next). Work is on `main` (one branch); each build's state is in its `pipeline.json`.
task229, task131, task122, task231 and task232 (2026-10-13) and task230 and task129 (reshipped 2026-10-14) are SHIPPED
and wait on the portal; task123's determinism repair is RESHIPPED. Wave 1 is fully shipped: task228 was redrawn as architecture 5
(a full refresh at the author's request) and SHIPPED 2026-10-15. Wave 2: task231 to task235 shipped; task236 next.

**Next, at the author's request (2026-10-13):** the status board now has a review switch on every shipped build
(Shipped, or Shipped and approved) and a note box; the marks live in the board's database. Read them first (the
`review` collection), leave approved builds alone, then for every build still on Shipped: run the domain swap test
(the objective must be tied to the domain, not retaggable) and design a second analytical layer of stumping on top of
the current one under the 10/10 rules. Two tags already look weak: task230's task type (human-reliability-assessment)
serves Forecasting in the taxonomy, not Data Quality, and task129 sits in a house domain (business operations, client
domain General Statistics) though its decisive method is web performance engineering.

**Progress (2026-10-14):** the board's `review` collection is still empty, so every shipped build stays in scope. The
author chose: task230 re-rooted inside Data Quality (done, reshipped), task129 re-rooted in a client domain (done,
reshipped), then the second-layer reviews in the order task232, task231, task229, task122, task131, with task123 last
(task232 and task229 assessed 10-14: no clean second layer, kept as shipped; task231's second layer, the 2025 rise in closures, was built and returned SEND_BACK at the re-judge, so it was reverted and the shipped build stands; task122 prototyped 10-14: informative hyperkalaemia stops leave the MAR estimators apart and short of the counterfactual, so no clean second layer, kept as shipped; task131 assessed 10-14: no clean second layer, kept as shipped; task123 kept as shipped at the author's call (no Energy task type serves ETL, so its tag is its only legal home). The review is complete; verdicts sit in the board's `assessment` collection. Next: wave 2 (task233 to task236) or task228, at the author's call.)

**task230: RESHIPPED 2026-10-14 (architecture 3, re-rooted at the author's request); waiting on the portal.**
- The Office of the Registrar General of Aldmere's 2026 census (Survey Research & Official Statistics,
  census-register-administrative-data-quality x Data Quality Monitoring). Call: the first occupation release (30 March
  2027) warns six sub-major groups, 24, 25, 35, 41, 71 and 93. The coding quality study's coded-so-far bias warns only
  35 and 93. The 103,367 write-ins still to code are 54 per cent follow-up proxy returns (18 per cent among the coded
  follow-up) and take the 0.80 acceptance score from 16 November, so the bias is carried route by route under that
  score. The follow-up batches carried as one warn 24, 35, 41 and 93; the routes under the old score warn 24, 35, 71
  and 93.
- Gates: 121 generator checks, verify green, byte-identical rebuilds, figures_check, precut, leak.py REVIEW only;
  four isolated leak reads (questions 1 to 4 none); judge pass 1 sent back two ask figures (fixed), pass 2
  DETERMINISTIC, APPROVE. Surface screen promotes task231 (back to back on the same pairing, another task type) and
  task131 and task183 (same-driver signature, differentiated): the adjudicated clone check is the author's call.

**task129: RESHIPPED 2026-10-14 (architecture 2, re-rooted at the author's request); waiting on the portal.**
- Vessey County Electric Cooperative, a rural electric cooperative (Energy Systems & Utilities,
  grid-reliability-outage-analysis x Root-Cause Analysis). Call: fund hazard-tree removal beyond the right-of-way
  with the 2027 right-of-way budget increase. The rise in tree-caused outages, 11.2 per 100 miles of overhead primary
  on average over 2021 to 2023 to 21.9 in 2025, is mostly ash beyond North's right-of-way falling onto the line: North's
  2025 rise is as large within two years of a trim (18.8) as late in the cycle and climbs with the ash within falling
  distance, and each contractor's units fail at North's rate for their time since trim (Garrity 0.98, Hollenbeck 1.01).
  The district series against the contract register files a re-bid (North's rise began with its January 2024
  handover); the regrowth reading files catch-up trimming.
- Gates: 119 generator assertions, verify.py green, byte-identical rebuilds, figures_check, precut 49 checks, leak.py
  REVIEW only; leak reader two reads (question 1 none); judge pass 1 FIX_NOW on ask B's ticket fold (closed by policy
  2.1's one-outage-at-a-time WHAT), pass 2 DETERMINISTIC. Surface screen promotes task128 (back to back) and task230
  (surface vocabulary), neither sharing domain, objective or mechanism: the adjudicated clone check is the author's call.

**task235: SHIPPED 2026-10-17 (wave 2, fifth build; architecture 2); waiting on the portal.**
- Fogbell Games, a Dublin game studio, and its match-3 game Kittiwake Cove (Product Analytics,
  metric-definition-measurement-science x Data Quality Monitoring; the seed's disease surveillance moved because
  Epidemiology x Data Quality was banned at the draw). Call: alert Android 7.41.0 and iOS 7.42.0 in the KC-DQ-04 run of
  Monday 9 November 2026, and no other build. The analytics SDK keeps a purchase event on the phone until the game next
  starts, so a missing event is lost only once that phone has opened the game again (the session service's log):
  Android 7.41.0 loses 6.34 per cent with none open, iOS 7.42.0 at least 3.10. A seven-day settle window alerts four
  old builds whose weekly players have not come back and cannot judge the 7.42.0 pair (5 of 12 wrong); the account's
  next session alerts three old iOS builds. Asks: each build's paying players (a guest who signs in to an older account
  leaves no link, so the phone's sign-in joins it) and gross bookings per paying player.
- Gates: 193 generator checks with the realism sweep, verify green (the alert set at three rates for the open
  purchases), byte-identical rebuilds, figures_check 109 of 109, precut 49, leak.py REVIEW only; two leak reads
  (questions 1 to 4 none, question 6 analytical; both landed the call and missed every ask figure); judge
  DETERMINISTIC, APPROVE in one pass (stump power moderate: the asks carry the bar). Architecture 1 graded the loss at
  two decimals and was sent back; re-rooted the same day with the alert graded instead. Surface screen promotes task234,
  task233, task81, task95, task73, task459 and task445 (other mechanisms, differentiated on the card): the adjudicated
  clone check is the author's call.

**task234: SHIPPED 2026-10-17 (wave 2, fourth build; architecture 2); waiting on the portal.**
- Tamsen County Department of Public Health's epidemiology unit (Epidemiology & Public Health,
  disease-surveillance-outbreak-anomaly-detection x Data Quality Monitoring). Call: the laboratory liaison escalates the
  influenza, RSV and SARS-CoV-2 streams of Wexmoor Regional Medical Center Laboratory and Westmarch Reference Laboratory
  for MMWR week 3 of 2027, and no other stream. A lost result message drops a positive and a negative alike, so each
  stream's week-3 positivity predicts the tests its laboratory ran (a Poisson fit of the testing response on its
  aggregate reports): the six sit at 55 to 61 per cent, every other stream at 87 or more. The protocol's week-2 check
  (FCP-2 s.5), run on a week when Brandmoor's interface lost half its results, keeps that way (largest miss 7.8 per cent)
  over last week's report (54.0), which escalates 15 streams, 9 of them complete streams whose epidemic fell.
- Gates: 487 generator checks with the realism sweep, verify green (its own Poisson fit), byte-identical rebuilds,
  figures_check 103 of 103, precut 49, leak.py REVIEW only; leak reader questions 1 to 4 none, question 6 analytical
  (its cancelled-order realism note fixed in the generator, no figure moved); judge DETERMINISTIC, APPROVE in one pass.
  Architecture 1 left the estimator of the week's tests to the data and was sent back at its round 2; re-rooted the same
  day with the week-2 check filed. Surface screen promotes task233, task232, task81, task95, task73 and task231 (other
  mechanisms, differentiated on the card): the adjudicated clone check is the author's call.

**task233: SHIPPED 2026-10-16 (wave 2, third build; architecture 2); waiting on the portal.**
- A university Social Survey Unit runs an island state's school-leaver destinations survey for its Department of
  Education (General Statistics & Data Science, missing-data-censoring-measurement-error x Data Quality Monitoring).
  Call: suppress the NEET rates of City East, City West and Riverside and the higher-education entry rates of Hill
  Country and Northern Plains; standard for the NEET rates of Southern Shore, Glen Villages and Upper Valley and the
  higher-education rates of Old Docks and Mill Towns; caution for the other 14. The 2025 nonresponse follow-up, in five
  districts across the island's range, found one odds ratio in every district and band (2.46 NEET, 0.41 higher
  education; calibration slopes 0.99 and 1.03); the pooled points gap (14.5, minus 11.1) files 11 of the 24 flags wrong.
- Gates: 385 generator checks, verify green, byte-identical rebuilds, figures_check 57 of 57, precut 49, leak.py REVIEW
  only; leak reader two reads (questions 1 to 4 none, question 6 analytical); judge r2 DETERMINISTIC, APPROVE, Gate H
  analytical. Architecture 1 (follow-up in the middle districts) was sent back the same day and re-rooted. The
  furniture was redrawn at stage 3 because task189, task463 and task152 were filed first and took its role, shape,
  forum, forcing event and organisation family.

**task232: SHIPPED 2026-10-13 (wave 2, second build); waiting on the portal.**
- A regional local health district's public health unit on the New South Wales and Queensland border (Epidemiology &
  Public Health, disease-surveillance-outbreak-anomaly-detection x Data Quality Monitoring). Call: the SLA lateness at
  which each pathology laboratory's ELR feed pages the on-call officer from 1 December 2026: base hospital 12 hours,
  Larkspur 2, Halden 12, Kestrel 4, Highfield 12, reference laboratory 24. The transmission that prices lateness comes
  from closed childcare investigations; the follow-up runs two incubation periods past the exclusion, so counting every
  case ill after the index files Larkspur 1, Halden 4 and Kestrel 2 and every follow-up case 2, 1, 2, 2, 8 and 24;
  only the incubation window after the index's infectious attendance (141 of 319 cases) files the golden.
- Judge pass 1 DETERMINISTIC, APPROVE but settled "secondary case" by the field's meaning; the guideline now defines a
  secondary case (acquired from the index) and pass 2 is DETERMINISTIC, APPROVE. Leak reader two reads. 100 generator checks,
  byte-identical rebuilds; the asks' over-clean stop (dropping every namespaced accession) now misses every feed.

**task231: SHIPPED 2026-10-13 (wave 2, first build); waiting on the portal.**
- The Brevland Central Bank's Business Conditions Survey (Survey Research & Official Statistics,
  nonresponse-calibration-measurement-error-adjustment x Data Quality Monitoring; DQ04 kept as an idea seed only).
  Call: Capital and Harbour into the reminder-call extension of the September 2026 round, Islands and Western Uplands
  onto the extra email, the other eight neither. The register records closures a year or more late and the call
  centre confirms one only when someone answers, so the register as it stands files five extension regions and the
  call-centre e, every earlier round and the last two years four each; the closure share from settled rounds (15.3 per
  cent) files two.
- Determinism judge DETERMINISTIC, APPROVE (thin but clean margins at Islands and Western Uplands); leak reader clean
  (its Christmas-close realism catch fixed); 431 generator checks.

**task122: SHIPPED 2026-10-13 (card v3, re-rooted under the 10/10 rules); waiting on the portal.**
- Varnmark Therapeutics' 52-week phase 2b of VMK-4410, an aldosterone synthase inhibitor, in albuminuric CKD
  (Biomedical & Clinical Research, longitudinal-outcomes-repeated-measures x Experiment & Causal). Call: take
  20 mg into the phase 3, 3 mL/min/1.73 m2 above placebo after 36 months' treatment (40 mg 2, 10 mg 1, 5 mg 0).
  The field's two-slope model with the chronic phase from month 3 files 40 mg at 5, because loop diuretics eased
  from week 12 let the higher doses' early fall partly recover and that recovery reads as chronic slope; the
  week-52 difference and one slope through every visit file 10 mg.
- Gates: 225 generator assertions, verify.py 54 checks, byte-identical rebuilds, figures_check, precut 49 checks,
  leak.py REVIEW only (sweeps 3 and 4); leak reader clean on two reads; judge DETERMINISTIC, APPROVE in one pass.
  Every estimator from week 24 (arm means, each patient's line, the mixed model) lands the golden's bins.

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


**task228: architecture 5 SHIPPED 2026-10-15 (full refresh at the author's request), pending review.**
- Call: gap sessions at a hold line of 0.28 percentage points; judge DETERMINISTIC and APPROVE; reader clean twice.
- The seed's world again (Avisly Medier's experiment platform, which data-health check its scorecard hold watches),
  with the field's own decisive step: a ratio metric's variance at the randomised install (delta method).
- State and resume line: `task228/pipeline.json`; the design: `task228/DESIGN_NOTE.md`.
- Earlier record (architectures 1 to 4), kept for history:
- Branch `perssathya/task228-guardrail-alert-metric` at 9120146.
- Design 1 (experiment-platform paging alert): its round-2 pass was on an earlier cut, and it failed
  the domain-coupling rule when revived.
- Design 2 (soil-moisture collocation) is spent: rounds 3 and 4 landed.
- Design 3 and design 4 (granted as an exception) found no architecture. Data-health estimator choices
  key G12 or G16, which task181, task182, task445 and task446 hold in the ban window.
- The card on file is design 2's.
- Superseded 2026-10-15 by architecture 5 (above).

**Done:** `guard.py` orders same-day draws by registration time (on `main`, 60881f6).

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
