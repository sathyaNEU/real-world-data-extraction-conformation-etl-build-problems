# task313 design note

Architecture 1, drawn 2026-11-04. Wave 10 (oviya1301), Opportunity Sizing & Decision Support. Seed OS15's world,
decision and quantity are kept: transitional-care nurse posts placed across a health system's hospitals in whole
posts, in proportion to the readmissions the service avoids, and the readmissions avoided a year. The seed's
pitfall (next-day transfers across town counted as readmissions, an episode-unit reading keyed through the
Medicaid plan's episode number) is a coding and identity stump that the clean-truth test kills, and is not used.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task313.json`, architecture v1, registered at the draw.
- **Pairing:** Healthcare Delivery & Health Economics / `patient-flow-beds-workforce-optimization`, drawn for
  Opportunity Sizing & Decision Support (the task type serves OS and F). The decision is a workforce placement:
  30 new neonatal transitional-care outreach posts across five maternity units for 2027/28, each unit's share
  following the readmissions the service will avoid among its eligible babies, and the readmissions the 30 posts
  avoid next year. Forward facing: the service starts on 1 April 2027 and the window is 2027/28.
- **Shape:** 05, allocation to a fixed total (each unit's posts and each unit's expected readmissions avoided),
  plus the total and the asks.
- **Strategy:** `causal_design`, Layer 2 family `estimand_identification`: the trial's intention-to-treat ratio
  is not the transportable effect, because the service acts only from its first home visit; read on the window
  after that visit (where the trial's own arms show the effect lives) and applied to each unit's readmissions
  that fall after its babies could first be seen.
- **Gap and generators:** gap time (the window the service can reach), then population; G7 operating window (a
  nurse can visit only after the community office knows the baby is home), G13 horizon (the window the trial
  measured is not each unit's reachable window), G14 conditioned yield.
- **Data-native sentence:** the community midwifery office learns of a discharge only when the maternity unit's
  notification reaches it, and two units' notifications routinely arrive one to five days after the baby goes
  home, while neonatal readmissions for jaundice and feeding cluster in the first four days after discharge; so
  a large share of those two units' readmissions happen before any outreach visit could, and nothing in either
  unit's own records says so.
- **Abstraction sentence (stumping Part 6):** "an intervention can act on a case only from a start that waits
  on a hand-off whose delay differs case by case and unit by unit, so a trial's whole-window effect carried as
  one ratio credits slow units with outcomes that fall before any start". Not writable against an approved
  build: 309 reads an effect class by class of event intensity (here the effect is constant once the service
  starts and what varies is how much of each case's window it reaches); 303 removes a shared upstream component
  logged by siblings in the same minute; 128 identifies an effect on over-capacity days; 105 is a catchment
  geometry; 106 a shared pool; 120 a storage identity. 105 v1 (spent on the portal) carried one filed season
  against one opening date; here each case's start comes from its own receipt time in a separate log, and the
  trial's effect has to be re-based before it is carried.
- **Spent mechanisms on the objective** (`guard.py mechanisms --objective opportunity-sizing-decision`, 19
  builds): 105 catchment nearer the new outlet; 106 a shared pool of spare legs; 116 groups with one signatory;
  118 the existing wedge plus the triangle; 120 inflow less storage gained; 127 the replaced wait's excess over a
  concurrent wait; 128 the effect read on over-capacity days; 301 a recorded state decaying between recordings;
  302 substitution inside the group; 303 the shared upstream minute; 304 a first sweep of a standing pool and a
  competing service; 305 the forced members' response; 306 units still to arrive in the roll; 307 wear only in a
  band; 308 sister units out together; 309 the effect class by class of intensity; 310 output capped by a limit;
  311 the between and within variance split; 464 the net flow with an injection. None spends a start gated by a
  per-case hand-off.
- **Slots screened** (`guard.py slots` on the mechanism and the setting): no note carries a hand-off-gated
  start; "readmission" hits are other mechanisms (task174's avoidance pathway, task190's linkage, task301's
  staggered post-discharge services); task308's note kills the ambulance-concurrency alternative and task174's
  the vacancy-chain alternative, both screened here and dropped.
- **Guard:** `check` PASS 2026-11-04, NOTE `test.same_puzzle_older` against task127's first architecture and
  `test.same_driver_older` against task259, both differentiated on the card; nearest driver 0.06. WARNs answered
  by redrawing: a persona's first name, the docx and xlsx deliverable set, the "where" question form (now how
  many, the form an allocation takes).
- **Furniture:** forum `funder_or_donor` (the integrated care board funds the posts and its specification fixes
  the allocation rule), forcing event `launch_or_rollout` (the service starts on 1 April 2027), organisation
  `hospital_or_health_provider`, role `programme_officer`, context artifact `close_out_summary` (the trial's
  final report), calibration `pilot_log` (the trial's randomisation list and contact log).
- **World:** England. Ravensby and Weald Integrated Care Board; Ravensby and Kellingworth Hospitals NHS
  Foundation Trust (Ravensby Royal Infirmary, Kellingworth University Hospital); Sedgefold and Wennby NHS Trust
  (Sedgefold Hospital, St Aldric's Hospital, Wennby Community Hospital, Copperfield Hospital, the trial site);
  Ravensby and Weald Community Health NHS Trust runs the community midwifery office and will host the posts.
  People from `guard.py names --geo england --seed 313`: Lucy Coates, Kathryn Thompson, Hugh Brown.
- **As-of date of the fiction:** 2 November 2026 (the planning pack). Planning basis: the twelve months to
  30 September 2026. Records run 1 October 2024 to 31 October 2026; the trial randomised 1 April 2024 to 31 March
  2026, its report is dated June 2026.
- **Sources:** every file is constructed in the organisations' own export forms (two maternity systems' discharge
  extracts, the community office's notification receipt log, the system's neonatal and paediatric admissions
  extract, the trial's randomisation list, contact log and final report, the service specification, code
  crosswalks, and the distractors); provenance, licence and the distractor list live in `metadata.json` outside
  `target/`.

## Tried and rejected

- Seed OS15's own mechanism (adult next-day transfers across town counted as readmissions, the Medicaid plan's
  episode number grouping the stays): with every key and disposition code correct the easy route excludes the
  transfers and lands, so the stump is a coding and identity reading (data semantics) and fails the clean-truth
  test; not built.
- Adult transitional-care posts, the first visit gated by each hospital's discharge summary (2026-11-04, measured
  on a prototype of the clean truth): at the realistic edge (two tertiary centres' summaries 38 to 42 per cent
  late, weekend discharges, surgical front-loading) the post-visit share ran 0.69 to 0.85, a contrast of 1.23x;
  under the seed's proportional rule the golden and default allocations were identical in every seed (C10 N8
  R5 S4 L3), because the shift is half a post; under a fill-by-rank rule the golden ranking ratios sat at 1.00
  to 1.06, the allocation was seed-hostage, and counting per visited patient against per eligible patient
  flipped the allocation on its own (a live main-call fork); the fixed-lag partial correction recovered half the
  contrast in the same direction. Dead on magnitude; moved to the neonatal pathway, where readmissions cluster
  in the first days after discharge.
- Adult transitional-care posts against the trial's own yield as a designation threshold: the benchmark rests on
  the trial's control arm (noisy) and any gap between estimators of the effect lands on the comparison; dropped
  for the proportional rule once the neonatal contrast made it carry.
- Adult transitional-care posts with the effect read only where patients are not already on a specialist nurse
  caseload (provision elsewhere), and the effect read on readmissions related to the index condition: each is an
  effect carried class by class to a different mix, task309's approved abstraction; not drawn.
- Ambulance shifts sized by the late calls an added crew would have reached: task308's screen records readers
  splitting availability from geography misses and replaying dispatch; dead on file.
- Social homes sized by the relets their transfer tenants release (vacancy chains): task174's screen records the
  chain as the housing literature's own construct; dead on file.
