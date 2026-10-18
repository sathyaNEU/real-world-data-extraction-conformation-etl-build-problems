# task162 design note

Architecture 1, drawn 2026-10-18 (wave 6, Forecasting lane, sathya8571), numbered from seed FC33. The seed (a browser's
bug-triage team that staffs its quarter to the busiest week at 120 triage items per triager-week, moves to a new tracker
on 4 January after a four-week November parallel run, and ships on a four-week train on 12 January, 9 February and
9 March) was read at its header and Situation only. Its world, decision and quantity are kept. Its decoy-era mechanism is
not shipped: what the new tracker counts as a triage item (every report, duplicates included) is filed as a plain fact in
the cutover runbook, and the old tracker's merge records carry no planted defect. The pitfall is re-found in how a release
reaches its users: the browser applies an update when it restarts, most Windows machines restart in the two days after
Microsoft's Patch Tuesday, and every one of the quarter's three releases ships on Patch Tuesday itself.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task162.json`, architecture v1, registered 2026-10-18; `guard.py check` WARN
   (answered below), nearest driver 0.08 (task98 v4 lineage), then task21, task129, task265, task157.
2. Pairing: Product Analytics (client domain) / `feature-adoption-diffusion-modeling` / Forecasting & Predictive
   Modeling. The seed's label was Product Analytics, software quality operations; the task type in the client taxonomy
   that serves forecasting and fits a browser release reaching its users is feature adoption and diffusion: the deciding
   quantity is how many users reach each new version in its first week and the first-use reports that follow (library
   pattern 1, effect by time since first exposure).
3. Niche: a Tampere browser vendor's bug-triage team filing its first-quarter 2027 headcount before the holidays, when the
   update applies only at a browser restart, Windows restarts bunch in the two days after Patch Tuesday, and all three of
   the quarter's releases ship on Patch Tuesday, which no release since September 2025 did.
4. Call and shape: triagers for the first quarter on the new tracker, a whole number (the busiest forecast week's triage
   items over 120, rounded up), `quantity_figure`, count, question form how-many. Shape `other`: the call with its
   critical components and the ask tables; criteria counted in `## Ask sheet`.
5. Mechanism keys: gap time (the record's release weeks met the restart burst a week or more after release; the window's
   meet it inside the release week) with population (the users a release week reaches); decisive generator G13 (the
   decision's weeks differ from every evidence week in the monthly restart cycle), then G7 (an update can apply only at a
   restart); Gate G `forecasting`; strategy `time_semantics` (a clock the recent record never exercised, the monthly
   operating-system restart cycle against the release day, estimated from every release that went through it).
6. Layer 2: `field_method` (exposure built the field's way: each version's adoption curve from ordinary restarts plus
   the monthly Windows burst, carried through first-use reports), pattern
   `own:release-week-reach-set-by-the-monthly-restart-burst`. Library neighbour:
   product-analytics/feature-adoption-diffusion-modeling/1 (effect by time since first exposure); this build's version
   differs in that the exposure clock itself is set by an external restart cycle, so the forward releases' first-week
   exposure has to be built from where each sits in that cycle.
7. Furniture: forum `committee_or_panel` (the quarterly engineering staffing review approves each team's headcount;
   `line_manager_or_team` was banned by task182 at the check); forcing event `cutover_or_migration` (the old tracker is
   retired on 4 January and the quarter's headcount is filed for the new tracker); organisation family
   `software_or_platform`; role family `field_unit_lead` (the triage team lead runs the frontline unit and files its
   headcount); context artifact `planning_thread` (the staffing-plan thread carrying the 120-item standard and the plan
   template); calibration `parallel_run_overlap` (the November parallel run in both trackers).
8. Spine: the old tracker's bug export, one row per report filed (duplicates included), January 2023 to the as-of, in a
   Bugzilla-style CSV layout; constructed, synthetic.
9. Deliverables: `triage_staffing_q1_2027.xlsx` (the call, its components and the ask tables) and
   `q1_2027_triage_forecast.svg` (the quarter's weekly forecast); the format set (xlsx and svg) is in none of the last
   twelve builds.
10. People, drawn with `guard.py names --geo Finland --seed 162` and checked clean by `guard.py check`: Ulla Kauppinen
    (triage team lead, the requester, in no file the prompt names and not in the prompt), Timo Huttunen (release
    management, the release calendar), Ritva Grönroos (tracker migration lead, the cutover runbook and the parallel-run
    report), Simo Kinnunen (data team, the public statistics). Invented names (the vendor, the browser, the trackers'
    instance names) are drawn and checked against real products when the pack is cut.

**Data-native sentence.** The browser downloads an update in the background and applies it the next time the browser
starts, so an install reaches a new version at its next restart; on Windows, which carries most installs, the monthly
cumulative update from Microsoft restarts most machines in the two days after the second Tuesday, so every release's
adoption curve steps up on those two days, wherever they fall in its first month; since September 2025 every release
shipped a week or two off Patch Tuesday, so its first week met only ordinary restarts and the burst came later, while all
three first-quarter releases ship on Patch Tuesday and meet the burst in their own first week.

**Guard and similarity.** `guard.py check` WARN at registration, two warnings answered: `three_rules.strategy_risk`
(time_semantics): the analyst test is analytical, every field and rule read correctly still files 7 on the record's
release-week profile, and no filed sentence or column names the restart cycle; `repeat.question_form` (how-many, task164):
the call is a headcount, which the form takes from the decision. The ban window at the check held task161, task182 and
task164: the planned decisive G7 (an update applies only at a restart) was task161's decisive generator and is listed
second; G13 leads because the stump is the forward release weeks' position in the monthly cycle against every evidence
week (F1 lists G13 first for time_semantics). Same-puzzle and same-driver tests (gap time, G13, `quantity_figure`, Gate G
`forecasting`): task102, task130 (v4 and its rounds), task134 (v2 round 2), task501 (v3), all older and differentiated on
the card; task102 is the nearest in family (a forward period ending on a weekend, a next-business-day release rule
recovered from the payment history) and differs in latent structure: here no rule is recovered and no period boundary
moves a count; an adoption process is estimated from the adoption series across every release.

**Abstraction test.** Stripped of nouns: a unit takes up each new version only at its next restart, most restarts on the
dominant platform come in a two-day burst once a month on a fixed day, so a version's first-week reach is set by whether
the burst falls in its first week; the forward versions all ship on the burst's eve, which none in the past year did.
The nearest by mechanism, read for latent structure:
- task160 (this wave) times regional surge waves by a stable propagation lag behind the leading region, read off this
  season's wave; here nothing propagates and nothing is read off the current season: an external calendar cycle sets
  when every release reaches its users, and the forward releases' place in it comes from the release calendar.
- task157 completes a returning cohort's wave from the part already back at the as-of; here no wave is in flight: the
  forward releases have not shipped.
- task156 sizes paid moderators from what a shrinking volunteer pool cannot absorb; here no capacity is censored and no
  pool shrinks: the triage load is a demand forecast.
- task148 drains a queue by abandonment and task159 builds a backlog behind full services; here arrivals are forecast
  and no service capacity enters them.
- task138 replays driver traces from each unit's store at the forecast date; here there is no store, only an adoption
  clock.
- task102 shifts payments due on a weekend into the next period by a recovered rule; here a behaviour, not a rule, and
  it is estimated, not recovered.
None shares the latent structure, the default path and the correction.

**Sources, one line each.**
- Seed FC33 header and Situation (`status.py task162`): the world, the 120-item standard, the 4 January cutover after
  the November parallel run, the 12 January, 9 February and 9 March releases; nothing else of the seed is read or kept.
- `guard.py mechanisms --objective forecasting` (74 builds): staffing and queue ground on file is a volunteer pool's
  absorbed share (task156), queue abandonment (task148), a stop-level backlog (task159) and store replays (task138);
  release-driven activity has not been drawn, and no driver reads a version's first-week reach off an external restart
  cycle.
- `stumping/references/client/layer2-rigor-patterns.md`, product-analytics feature-adoption-diffusion pattern 1 (effect
  by time since first exposure): the first-use reports follow each install's adoption, so the forecast is built on
  adoption, and the adoption clock is the restart.
- `stumping/references/strategies.md` F1 (time: a clock the closed window never exercised, estimated by the field's
  method from every unit that went through it, no closed figure blessing the wrong method) and the wave-3 bar (the
  rival rejected out of sample on past release cycles).
- `two-layer-task-design.md`: the client's example of validating a forecast on data it was not built on (the record's
  release-week profile misses the August and September 2025 releases, the last ones shipped on Patch Tuesday).

## Tried and rejected
- 2026-10-18 draw: the seed's own route made analytical, a new-to-old conversion whose duplicate share rises with the
  spike, so the quiet parallel-run ratio fails in release weeks; its honest key is composition (task470 held it in the ban
  window), and with the counting basis filed and the old export holding every duplicate, rebuilding the new basis from
  the export bypasses the conversion and lands on any typical-quarter golden.
- 2026-10-18 draw: the December release's open regressions drawing duplicates until their fixes ship with the January
  release; carrying the December excess forward lands within a quarter bin of the golden, so persistence is a bypass.
- 2026-10-18 draw: the January release's beta-channel reports scaled to the release wave by the ratio earlier versions
  showed at the same beta age; it is task157's driver (the part already in times a ratio earlier waves kept) in other
  nouns, and the as-of leaves only days of beta.
- 2026-10-18 draw: each release's wave sized by the fixes it carries; one ratio (linear), a covariate reflex, and only the
  January version's size is known at the as-of.
