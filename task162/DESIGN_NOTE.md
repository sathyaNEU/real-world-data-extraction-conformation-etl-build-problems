# task162 design note

Architecture 1, drawn 2026-10-18 (wave 6, Forecasting lane, sathya8571), numbered from seed FC33. The seed (a browser's
bug-triage team that staffs its quarter to the busiest week at 120 triage items per triager-week, moves to a new tracker
on 4 January after a four-week November parallel run, and ships on a four-week train on 12 January, 9 February and
9 March) was read at its header and Situation only. Its world, decision and quantity are kept. Its decoy-era mechanism is
not shipped: what the new tracker counts as a triage item (every report, duplicates included) is filed as a plain fact in
the cutover runbook, and the old tracker's records carry no planted defect. The pitfall is re-found in how a release
reaches its users: the browser applies an update when it restarts, most Windows machines restart in the two days after
Microsoft's Patch Tuesday, and every one of the quarter's three releases ships on Patch Tuesday itself.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task162.json`, architecture v1, registered 2026-10-18; `guard.py check` WARN
   (answered below), nearest driver 0.08 (task98 v4 lineage), then task21, task129, task265, task157.
2. Pairing: Product Analytics (client domain) / `feature-adoption-diffusion-modeling` / Forecasting & Predictive
   Modeling. The seed's label was Product Analytics, software quality operations; the task type in the client taxonomy
   that serves forecasting and fits a browser release reaching its users is feature adoption and diffusion: the deciding
   quantity is how many installs reach each new version in its first week and the first-use reports that follow
   (library pattern 1, effect by time since first exposure).
3. Niche: a Tampere browser vendor's bug-triage team filing its first-quarter 2027 headcount before the holidays, when the
   update applies only at a browser restart, Windows restarts bunch in the two days after Patch Tuesday, and all three of
   the quarter's releases ship on Patch Tuesday, which no release since October 2025 did.
4. Call and shape: triagers for the first quarter on the new tracker, a whole number (the busiest forecast week's triage
   items over 120, rounded up), `quantity_figure`, count, question form how-many. Shape `other`: the call with its
   critical components and the ask tables; criteria counted in `## Ask sheet`.
5. Mechanism keys: gap time (the record's release weeks met the restart burst a week or more after release; the window's
   meet it inside the release week) with population (the installs a release week reaches); decisive generator G13 (the
   decision's weeks differ from every evidence week in the monthly restart cycle), then G7 (an update can apply only at a
   restart); Gate G `forecasting`; strategy `time_semantics` (a clock the recent record never exercised, the monthly
   operating-system restart cycle against the release day, estimated from every release that went through it).
6. Layer 2: `field_method` (exposure built the field's way: each version's adoption curve from ordinary restarts plus
   the monthly Windows burst, carried through first-use reports), pattern
   `own:release-week-reach-set-by-the-monthly-restart-burst`. Library neighbour:
   product-analytics/feature-adoption-diffusion-modeling/1 (effect by time since first exposure); this build's version
   differs in that the exposure clock itself is set by an external restart cycle, so the forward releases' first-week
   exposure has to be built from where each sits in that cycle.
7. Furniture: forum `committee_or_panel` (the engineering staffing review approves each team's headcount on
   21 December; `line_manager_or_team` was banned by task182 at the check); forcing event `cutover_or_migration` (the old
   tracker is retired on 4 January and the quarter's headcount is filed for the new tracker); organisation family
   `software_or_platform`; role family `field_unit_lead` (the triage team lead runs the frontline unit and files its
   headcount); context artifact `planning_thread` (the staffing-plan mail thread carrying the 120-item standard and the
   quarter); calibration `parallel_run_overlap` (the November parallel run in both trackers, the asks' ground).
8. Spine: the old tracker's bug export, one row per report filed through the form (duplicates included), 1 October 2025
   to 17 December 2026, 29,275 rows, in a Bugzilla-style CSV layout; constructed, synthetic.
9. Deliverables: `triage_staffing_q1_2027.xlsx` (the call, the busiest week's forecast and the two ask tables) and
   `parallel_run_triage.svg` (Ask A's weekly figures charted); the format set (xlsx and svg) is in none of the last
   twelve builds.
10. People, drawn with `guard.py names --geo Finland --seed 162` and checked clean by `guard.py check`: Ulla Kauppinen
    (triage team lead, the requester, not in the prompt), Juhani Immonen (director of engineering, the thread), Timo
    Huttunen (release management, the release calendar), Ritva Grönroos (tracker migration lead, the runbook, the copies'
    clean-up), Simo Kinnunen (data team, the public data portal), Helena Pakarinen (security team), the six triagers
    (Linnea Kärki, Johannes Laukkanen, Saara Väisänen, Tapio Kallio, Arja Turunen, Sakari Puhakka) and the
    web-compatibility team (Milla Ojanen, Antero Järvinen). Invented names: Usva Software Oy and its Usva browser
    (Tampere), the domain usvasoftware.fi, the bridge's service account tracker-bridge, the projects Browser intake (BRW)
    and Web compatibility (WEBC).

**Data-native sentence.** The browser downloads an update in the background and applies it the next time the browser
starts, so an install reaches a new version at its next restart; on Windows, which carries most installs, the monthly
cumulative update from Microsoft restarts most machines in the two days after the second Tuesday, so every release's
adoption curve steps up on those two days, wherever they fall in its first month; since October 2025 every release
shipped a week or two before Patch Tuesday, so its first week met only ordinary restarts and the burst came later, while
all three first-quarter releases ship on Patch Tuesday and meet the burst in their own first week.

**Guard and similarity.** `guard.py check` WARN at registration, two warnings answered: `three_rules.strategy_risk`
(time_semantics): the analyst test is analytical, every field and rule read correctly still files 6 on the record's
busiest weeks, and no filed sentence or column names the restart cycle; `repeat.question_form` (how-many, task164):
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
the burst falls in its first week; the forward versions all ship on the burst's eve, which none in the record did.
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
  release-week profile misses the two releases of late 2026 that shipped two weeks before Patch Tuesday).
- `supplemental-stumping` and task155's two measured cracker paths: the asks' devices are measured on each natural
  reading of a report's filing time, not on one.

## Default path
1. Read the staffing-plan thread and the cutover runbook: the triage team is staffed for the quarter's busiest week at
   120 triage items per triager-week (the week's expected items over 120, rounded up), the quarter is the 13 weeks from
   Monday 4 January to Sunday 4 April 2027, weeks run Monday to Sunday Helsinki time, and on the new tracker every
   report filed through the browser's report form is a triage item, duplicates included, with security-restricted
   reports going to the security team.
2. Rebuild the triage items the new counting gives for every week of the record from the old tracker's export: every
   report by the week it was filed, duplicates included, the security group's reports left out.
3. Take the busiest week of last year's first quarter on that rebuilt series (the week of 9 March 2026, 674 items) and
   scale it by the growth in daily active installs (the last eight weeks against the same weeks a year earlier, 3.9 per
   cent).
4. Divide by 120 and round up.

Ends on: 6 triagers (the busiest week about 700 items).
Golden: 8 triagers (the busiest week about 900 items).

## Stump sentence
Rebuilding the new tracker's weekly triage items from the old export and carrying last year's busiest first-quarter
week, scaled for the growth in active installs, onto the quarter files 6 triagers; the step that lands it there is
treating each first-quarter release week like the record's, when every release since October 2025 shipped a week or two
before Patch Tuesday and met the Windows restart burst only in its second or third week, while all three first-quarter
releases ship on Patch Tuesday itself, so the burst falls inside each release week, about three in four active installs
reach the new version in it against at most about half (48 per cent) in any week of the record, and the busiest week
carries about 900 items and needs 8.

## Three rules

Task type: feature-adoption-diffusion-modeling (Product Analytics), which serves Forecasting & Predictive Modeling in the taxonomy; the setting is a desktop browser's release train and the reports its users file in their first days on each new version.
Domain test: the deciding quantity is each first-quarter release week's first-use report wave, forecast the way product analytics forecasts version-driven activity: from the version's adoption curve, with each install taking the update at its next browser restart and most Windows installs restarting in the two days after Patch Tuesday, carried through the reports users file in their first days on a version; it is not a seasonal trend, a ratio of release weeks to quiet weeks or a peak carried forward.
Swap: "how many nurses does a hospital need in its busiest flu week of the first quarter" keeps a peak and a staffing standard but loses the update applied at restart and the operating system's monthly restart cycle, so the quantity the call turns on (how many installs reach a new version inside its release week) has no record to be read from and no calendar to be placed on.
Layer 1: the old tracker's Bugzilla-style export (Helsinki local timestamps, product and component as two columns, the security group in its own column, beta and nightly versions beside release builds, the parallel run's reports closed MOVED and put in an Archive product), the public portal's shares of each platform's daily active installs by major version and its daily installs in thousands, the release calendar as a table inside a PDF, the old dashboard's weekly counts on its own basis (new defects only, the run's weeks empty), the record's partial first and last weeks and the year-end lull; each is how those systems write their files, and none carries the call (asserted neutral in checks.py, R2, inventory below).
Layer 2: field_method, exposure built the field's way: the release week's first-use reports follow the installs that reach the new version in it, and that reach is set by where the release sits in the monthly Windows restart cycle; the choice that flips the call is building each first-quarter release's adoption from ordinary restarts plus the restart burst after Patch Tuesday, rather than carrying the record's release weeks or its first-week profile.
Decisive step: forecast each first-quarter release's adoption by platform from the record's ordinary restart rates and the share of not-yet-updated Windows installs that update on the Wednesday and Thursday after each Patch Tuesday, place the burst inside each release week because all three releases ship on Patch Tuesday, and carry the reach through the first-use reports per install the record's releases showed.
Not semantics: every field is read correctly on the default path (each report's filing week, duplicates in, the security group out, the shares and installs in their own units, the release dates); the record's release weeks are complete and correct, and reading them correctly still leaves the analyst choosing how to forecast a release week whose timing in the restart cycle the record never had.
Not rule application: the thread and the runbook file the estimand (the triage items, the window, the weeks, the 120-item standard, the rounding up); no filed rule says how installs take an update, when Windows restarts or how a release week's reports follow adoption, and executing every filed rule on the default path files 6.
Analyst test: a strong analyst who rebuilds the new counting from the old export, reads the thread, the runbook and the release calendar correctly and carries last year's busiest first-quarter week scaled for growth (or the record's release-week profile on the quarter's baseline, or an uplift from the last release) files 6 triagers; only building each first-quarter release's adoption from ordinary restarts plus the Windows restart burst after Patch Tuesday, which the adoption series shows every month, files 8 (executed in checks.py on the generator's clean truth: R3a 6, R3b 8, every single lower correction 6).
Estimand: the staffing-plan thread (the director's request and the triage lead's reply) and the cutover runbook file the population (every report filed through the browser's report form in each week of the first quarter of 2027, duplicates included, security-restricted reports out, reports not yet filed at the as-of included as forecast), the outcome (the week's expected triage items), the window (the 13 weeks from Monday 4 January to Sunday 4 April 2027, Monday to Sunday Helsinki time), the unit (triagers at 120 triage items per triager-week, the busiest week's expected items over 120 rounded up) and no comparison.
No decoy: no memo, draft, forecast, stakeholder figure or earlier plan states a first-quarter figure or argues a method; the old dashboard answers its own question (weekly new defects on the old basis) and ranks nothing; the release calendar lists dates; the public statistics and the stability series are distractors that answer their own questions.
No certified replay: no shipped figure is reproduced to recover a method; the record's weeks are history every method reads alike, and the back-test on the record's releases (the two offset-14 releases of late 2026 against the profile of the rest) is the analyst's own validation, not a published control set.
Lesson: a model learns that a release's first-week activity is set by how many installs reach the version in that week, that browser updates wait for a restart and Windows restarts come in a burst after Patch Tuesday, and that a forward release sitting where no recorded release sat in that cycle cannot be forecast from the recorded release weeks; no build on file reads a version's first-week reach off an external restart cycle.

## Layer 1 inventory

Each item, the system that writes it, its file and its natural mishandling; every R2 line is asserted in checks.py with
the golden method run on the mishandled reading (the call and the rounded week stay at 8 and 900 in each).
- Helsinki local times without an offset (the old tracker's CSV writer, the export): read as UTC, 912 items.
- The security group in its own column (the old tracker's groups): kept in, 942.
- Beta and nightly builds beside release builds (the report form's version field): dropped, 874.
- The parallel run's reports closed RESOLVED MOVED and put in the Archive product on 30 November (the migration's
  bulk close): dropped as closed, 896.
- Active installs in thousands (the portal): read as units, the same forecast (the model is scale-free).
- The record starting on Wednesday 1 October 2025 and ending on Thursday 17 December (the saved search's window): the
  partial weeks dropped, 912.
- The year-end lull, 21 December to 3 January (the world): its days read as ordinary days in the hazards, 912.
- The release calendar as a table inside a PDF with point releases listed (release management): read; the portal
  publishes major versions, so a point release adds no reach.
- The old dashboard's weekly new defects (duplicates, invalid and MOVED reports out, the run's weeks empty): not read by
  the golden; it is rung R0.
- The new tracker's export (UTC times, component paths, multi-valued components, two projects, the bridge's service
  account, catch-up writes with the old number in a label, a move clearing Legacy bug, WEBC's own Old tracker ID field,
  the Close transition, the re-sent copies, the team's tasks, restricted issues): the asks' ground, read by no step of
  the call (SEPARATION, asserted).

## Readability screen
Six tests per rung (1 a filed sentence names it or sends the solver looking, 2 a column, key or marker makes it a
predicate or a header join, 3 an opponent reflex, 4 a control or corpus scores it, 5 the hygiene battery finds it, 6 one
subtraction, ratio or half of a figure). Built figures from `generator/calc.py` on the cut pack.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 the old dashboard's busiest first-quarter 2026 week scaled for growth (3) | the thread says the number won't compare with the dashboard's new defects | the dashboard's weekly totals | yes, the team's own dashboard | the rebuilt counting from the export runs about twice the dashboard's | no | yes, one ratio | readable |
| R1 (default) last year's busiest first-quarter week on the rebuilt counting, scaled for install growth (6) | the thread names the busiest week and the quarter | the export's opened dates | yes, the seasonal analog | no shipped figure scores it | no | yes, one ratio | readable |
| R2a trend and seasonality on daily active installs plus the record's release-week profile by week since release (6) | no | the release calendar's dates | yes, the modeller's default | the profile fitted on the record's offset-7 releases puts its own two offset-14 releases' third weeks at about 40 per cent of what they brought | no | no | readable |
| R2b a one-scalar uplift from the 1 December release's peak week over its week before, on each first-quarter release's week before (6) | no | no | yes, the last event as template | the uplift moves with each release's place in the cycle | no | yes | readable |
| R2c an exposure model (daily items on the installs reaching the newest version) with the record's typical first-month reach carried onto the releases (6) | no | the adoption series | a half-step: exposure without its clock | no recorded week reached more than about half the installs, so the record cannot show the release-week reach | no | no | readable |
| R3 (decisive) each first-quarter release's adoption built from ordinary restarts plus the Windows restart burst on the Wednesday and Thursday after Patch Tuesday, the burst inside each release week because each ships on Patch Tuesday, carried through the record's first-use reports per install (8) | no sentence names a restart, an update mechanism, Patch Tuesday, a burst or a reach; the calendar lists dates and the thread names the standard | no column marks a restart or a burst: the adoption series carries daily shares by major version and platform, and the step-ups are visible only by reading the days on which shares jump against the calendar | no: the reflexes are a seasonal analog, a profile by week since release, a last-event uplift and a typical reach | none ships: the record's weeks are history every method reads alike, and no document scores a method | no: nothing is duplicated, missing or mis-keyed on the call's rows | no: an adoption process with two clocks, ordinary restarts and the monthly burst, placed on each release's calendar and carried through first-use reports | silent |

## Semantic fork table

Every term in the main ask and every convention the main computation needs. Every id is asserted in
`generator/checks.py` on the built pack.

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "how many triagers" | the busiest week's expected triage items over 120, rounded up to a whole triager | rounded to the nearest | 8 (same call; 912 over 120 is 7.6) | the thread ("divided by 120 and rounded up to a whole triager") |
| SF2 | a triage item | every report filed through the report form, duplicates included, security-restricted reports out | duplicates out; restricted in | 5 with duplicates out; 8 with restricted in | the runbook ("Every report filed through the report form is a triage item, duplicates included ... Reports in the security group go to the security team's queue and are not triage items.") |
| SF3 | the quarter | the 13 weeks from Monday 4 January to Sunday 4 April 2027 | calendar January to March | same call (the busiest week is a release week inside both) | the thread |
| SF4 | a week | Monday 00:00 to Sunday 24:00, Helsinki time | UTC weeks | same call (the busiest week moves 0.6 per cent) | the thread |
| SF5 | "busiest week" | the week with the most expected triage items | the week with the largest rise over the week before | same call (the same release week) | the thread ("the quarter is staffed for its busiest week") |
| SF6 | expected | the forecast's central value, the mean count | a high percentile | 8 (a 90th percentile of the busiest week, 951, also files 8) | the thread ("the busiest week's expected triage items") |
| SF7 | the as-of | the files taken on 18 December 2026; the export holds reports filed to 23:59:59 on Thursday 17 December | data through the last full week (Sunday 13 December) | same call | the export's run line and the thread's date |
| SF8 | a report's week | the week of its filing on the old tracker (`opened`, Helsinki time) | the week it was last changed | 6 under changeddate | the runbook ("A report is counted in the week it is filed.") and the field notes (opened, when the report was filed) |
| SF9 | moved reports | in: a report the team moved to the web-compatibility team was filed through the form (the export holds it under Web Compatibility) | out | 7 with them out | the runbook ("A report the team moves to another team's project during triage stays a triage item.") |
| SF10 | beta and nightly reports | in: every report through the form, whatever version the reporter runs | release channel only | same call (874) | the runbook ("each is a triage item whatever version the reporter runs") |
| SF11 | the parallel run's reports on the old tracker | reports filed, counted in their filing weeks (closed MOVED in bulk on 30 November and put in Archive) | dropped as closed | same call (896) | the runbook (the bulk close is the parallel run's bookkeeping) |
| SF12 | reports carried over at the cutover | not first-quarter items: the old tracker's open reports migrate with their state | counted in the first week | the first week would be the busiest (5,725 open at the pull) | the runbook ("Migrated reports keep their state and are not new triage items.") |
| SF13 | the rounding path | the busiest week's expected items, unrounded, over 120, rounded up | each week rounded first | same call | the thread |

## Ladder
Built figures (`generator/calc.py` on the cut pack; `checks.py` asserts each row, the OOS record, R3a and R3b).

| Rung | Construction | Busiest week | Triagers | Dies to |
|---|---|---|---|---|
| R0 | the old dashboard's busiest first-quarter 2026 week (343 new defects) scaled for install growth | 356 | 3 | the thread: the new counting won't compare with the dashboard's new defects |
| R1 default | last year's busiest first-quarter week on the rebuilt counting (674, the week of 9 March 2026), scaled for install growth (3.9 per cent) | 700 | 6 | every first-quarter 2026 release shipped a week before Patch Tuesday, so its first week met ordinary restarts only (at most about half the installs); the quarter's releases ship on Patch Tuesday |
| R2a | the record's release-week profile by week since release (13 releases) on the quarter's baseline per active install | 664 | 6 | the profile puts the third weeks of the two offset-14 releases (29 September and 27 October 2026) at 42 and 37 per cent of what they brought, and their second weeks 28 and 35 per cent high: the profile is a place in the restart cycle, not a property of releases |
| R2b | a one-scalar uplift (the 1 December release's peak week over its week before, 2.0) on each first-quarter release's week before | 712 | 6 | the uplift is the 1 December release's place in the cycle (its burst in its second week) |
| R2c | the reports model with the record's typical first-month reach carried onto the releases | 658 | 6 | no recorded week reached more than 48 per cent of the installs; the release-week reach is the forecast, not a constant |
| the record's busiest week scaled; the busiest week of the last quarter scaled; the busiest week per active install on the quarter's installs | (bypasses) | 700, 628, 725 | 6, 6, 7 | each carries a recorded week, and no recorded week sat on Patch Tuesday |
| R3 decisive | each release's adoption from ordinary restarts plus the restart burst on the Wednesday and Thursday after Patch Tuesday (Windows hazards about 60 and 46 per cent against 12 on other weekdays), the burst in the release week, carried through the record's first-use reports per install | 912 | 8 | golden |

**Position and margins.** The golden is the extreme cell: every rung files fewer triagers, and the nearest (725, the
busiest week per active install) sits 115 items under the 840 edge. The golden sits mid-bin (912, 0.40 of the 120-item
band from its edge and 0.38 of a 100 bin from its rounding edge); one sigma of the reports model (9.8 items, robust
covariance) keeps it between 903 and 922.

**Out of sample (the rival rejected on past release cycles).** The record holds thirteen releases that shipped a week
before Patch Tuesday (offset 7: the burst in their second week) and two that shipped two weeks before (offset 14:
29 September and 27 October 2026, the burst in their third week). The release-week profile fitted on the thirteen puts
the two late releases' third weeks at 42 and 37 per cent of their excess over the baseline and their second weeks 28 and
35 per cent high; the restart model fitted on the same thirteen comes within 2 and 10 per cent of the third weeks.

**Convergence (C1, asserted).** 168 defensible constructions of the golden (hazards from all fifteen releases or the
last six, by mean or median; a five, six or eight day lag per platform or pooled, or a weekly model with the week before;
the fit on the whole record or on 2026; install growth over four, eight or eleven weeks) all file 8 triagers and 900,
from 896.7 to 920.5, each at least a quarter of a 100 bin inside. The verifier's own code path (median hazards, the
weekly model) files 897.

**Worth on the graded quantity.** Rebuilding the new counting is worth three triagers (R0 to R1); seeing that the
quarter's release weeks sit in the restart cycle where no recorded week did is worth about 210 items and two triagers.

**Strength.** P(one strong solver lands) about 0.12: it must rebuild the new counting, read the release weeks as
adoption-driven, find the monthly step-ups in Windows adoption on the Wednesday and Thursday after the second Tuesday,
see that the quarter's three release dates are second Tuesdays, and build the release weeks' adoption from the burst
rather than carry any recorded week. P(both land) about 0.02 if independent, under 0.1 with any plausible correlation.
The seed is fixed by rule (the task number then the as-of month and day: 1621217) before any data is generated and is
never searched.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | every report filed through the form in each first-quarter week, duplicates in, restricted out, reports not yet filed included as forecast | filed (the runbook and the thread); SF2, SF9, SF10 |
| 2 | Unit of account | the report; triagers at 120 items per triager-week | filed (runbook, thread); SF1 |
| 3 | Attribution window | the 13 weeks from 4 January to 4 April 2027 | filed (thread); SF3 same call |
| 4 | As-of dating | the files taken on 18 December 2026, the export to 17 December | filed (export run line, thread); SF7 |
| 5 | Version basis | the export as pulled; the run's reports closed MOVED and archived | SF11 same call asserted |
| 6 | Denominator | first-use reports per install reaching the newest version | C1 across the reports models (asserted) |
| 7 | Weighting | none: weekly counts | n/a |
| 8 | Window length | the record's releases the restart rates and burst shares are read from | C1: all fifteen or the last six the same call (asserted) |
| 9 | Boundary inclusivity | the week's Monday 00:00 in, the next Monday 00:00 out | filed (thread); SF4 |
| 10 | Rounding path | the unrounded busiest week over 120, rounded up | filed (thread); SF13 |
| 11 | Tie-break | none (the busiest week's level is graded, not its date) | n/a; all three release weeks sit in the 8 band (asserted) |
| 12 | Maturity and censoring | the 1 December release's adoption under way at the as-of | C1: the hazards without it the same call (asserted) |
| 13 | Order of operations | adoption, then reports, then weeks, then the maximum, then the standard | C1 (asserted) |
| 14 | Row order | counts and set membership | C1 |
| 15 | Duplicate resolution | duplicates are items (filed); no bug id twice in the export | filed (runbook); asserted unique bug ids |
| 16 | Identity normalisation | none on the call (one tracker, one id) | n/a |
| 17 | Netting against gross | none | n/a |
| 18 | Dimensional units | shares of each platform's installs in per cent, installs in thousands, reports as counts | the series' own headers; R2 (units read wrongly leave the call) |
| 19 | Code and status semantics | resolution and status are not read by the call | asserted: the forecast with the status columns blanked is unchanged |
| 20 | Integerisation | none before the rounding up | the golden mid-bin with one sigma (asserted) |
| 21 | Clause scope | the 120-item standard applies to the triage team's quarter | filed (thread) |
| 22 | Forward window contents | the first quarter's releases and their dates | the release calendar (12 January, 9 February, 9 March 2027) |

## Literal reader
Executing the prompt, the thread and the runbook word for word gives the busiest week's expected triage items among the
13 weeks from Monday 4 January to Sunday 4 April 2027 (Monday to Sunday, Helsinki time), a triage item being every report
filed through the browser's report form, duplicates included and security-restricted reports out, over 120 and rounded up
to a whole triager; no shipped sentence says how the quarter's weeks will run, so a literal reader must forecast them; the
easy method on the same literal estimand (last year's busiest first-quarter week scaled for growth) files 6, and the fork
table leaves no reading under which any rung is the golden.

## Oracles

- The record's weeks (the old export): history every method reads alike; on the wrong path they supply last year's
  busiest week and the release-week profile, and the analyst's own back-test on the two offset-14 releases rejects the
  profile. No closed window carries a first-quarter 2027 figure.
- The old dashboard: its own question (weekly new defects on the old basis), consistent with every method; it forecasts
  and ranks nothing.
- The public adoption series and daily active installs: inputs every method can read; no control ties only under the
  golden.
- The public bug statistics and the stability series (distractors): monthly figures that tie with the export under
  every reading and enter no step.

## Ask sheet

**Main call's declared row population:** the old tracker's export (the columns the call reads: `opened`, `groups`,
`op_sys`; all rows), the portal's shares and daily active installs, the release calendar, the staffing-plan thread and
the cutover runbook. Device and hazard rows in it: 0 (asserted, SEPARATION: the forecast is unchanged to the hundredth
with the new tracker's export, the rota, the component register and the working agreement deleted). The asks read the
new tracker's export, the rota, the register and the agreement, and the old export's `opened` through each report's old
bug number (the referee: a column the call already reads, no device row in it).

**Ask A. For each week of the November parallel run, how many of its triage items had no triage action within 24 hours
of being filed, and how many had been closed by the time the run ended** (8 figures, whole items). Golden: 2 to 8 Nov
109 and 319; 9 to 15 Nov 101 and 262; 16 to 22 Nov 45 and 119; 23 to 29 Nov 85 and 76.
- H18 home: an audit trail of the new tracker's intake under the team's own working agreement, the first measurement of
  how the team kept up on the system it staffs for; the call never reads it.
- Basis (filed in the working agreement, the team's voice): a triage action is a change by one of the rota's triagers to
  a report's status, resolution, component or priority, or a move to another team's project; the target is a triage
  action within 24 hours of the report's filing; a report is closed when it is in Resolved or Closed, or sits in another
  team's project; weeks run Monday to Sunday, Helsinki time, a report belongs to the week it is filed in, and the run's
  reports are those filed from 00:00 on 2 November to 23:59 on 29 November. The runbook: reporters kept filing on the
  old tracker and the bridge copied the reports into the new tracker, each with its old bug number; the counting basis.
- Primary A1 (D8, an upload date for the event date; silent): an issue's `created` is when the bridge wrote it. The
  bridge stopped five times (5 November 01:05 to 17:40, its reporting replica down; 10 November 01:12 to 21:37, its token
  expired; 18 November 01:50 to 17:05, a checkpoint fault; 25 November 02:41 to 19:52, the new tracker's maintenance
  overran; the close-out from 14:00 on Saturday 28 November to 07:00 on Monday 30 November) and paused for the new
  tracker's maintenance from 18:00 on Sundays to 02:00 on Mondays, so every report filed in those spans was written hours
  later: its 24-hour clock starts late, Sunday evening's reports fall into the next week, and the close-out's reports
  fall after the run. Fair: the old export's `opened` gives every report's filing time through its old bug number
  (asserted; the verifier recomputes every figure that way). Silent: `created` is valid and no shipped sentence mentions
  the stops.
- Primary A2 (D7, the true key elsewhere; silent): the bridge's catch-up after each stop wrote its backlog with the old
  bug number only in a label (`legacy-NNNNNNN`, 428 issues, none with a Legacy bug value or an Affects Version/s), and a
  move to WEBC drops the Legacy bug value, which WEBC's field configuration does not carry (84 moved issues, the value
  kept in the move's changelog entry). A join or dedup on the Legacy bug field drops the catch-up writes and the moved
  reports and keeps the re-sent copies as reports. Fair: the label and the changelog give every number (asserted).
  Silent: the names map lists Legacy bug, the runbook says only that each copy kept its old bug number.
- Hazards: HA1 times in UTC (weeks in Helsinki time); HA2 the re-send after the checkpoint fault (84 copies under new
  keys, the old number in their labels, closed as duplicates by the migration lead's script at 17:52 on 18 November; 3
  whose originals had already been moved to WEBC stayed open and were triaged on 19 November): not reports; HA3 63
  restricted issues (the security team's, re-sent copies included); HA4 19 tasks; HA5 269 issues in WEBC's own intake
  (253 site reports and their re-sent copies, the old number in the pilot project's Old tracker ID or, after a catch-up,
  in a label; not filed through the form); HA6 the Close transition (132 issues Closed with no resolution or resolution
  date); HA7 the bridge's own history entries (not triage actions).
- Stops (built and asserted): the created path (A1 missed), the legacy path (A2 missed), the mirror (the triage
  project as it stands, any change by a triager, closed by the resolution date); each misses every Ask A figure.
- Span: the new tracker's export, the old export, the rota, the working agreement, the runbook (5 files).
- Realism: a sync bridge writes an issue when it runs, not when the source record was made; a catch-up writes in bulk
  through a short payload; Jira drops a custom field's value on a move to a project whose configuration lacks it; a
  workflow's Close transition with no resolution screen leaves the resolution empty.

**Ask B. For each of the new tracker's eight component groups, how many of the run's triage items arrived in its
components** (8 figures, whole items). Golden: Rendering and Layout 451, Graphics and Media 136, Networking 109, Script
and Web APIs 169, Browser Interface 468, Extensions 75, Developer Tools 70, Platform and Updates 55.
- H18 home: the run's intake by area rota, read beside the call for the area rotas on the new tracker; the call never
  reads it.
- Basis: the component an issue arrived in is the one the bridge wrote it into (the form area's component); the
  register maps components to groups; a report with components in more than one group is in each group's queue.
- Primary B1 (D2, an attribute at the wrong vintage; the mirror's): an issue's components now are those the triagers
  set (56 with a second component, the follow-up week's changes included); the arrival component is the current set
  with every later component change undone, removals and additions item by item.
- B carries A1 (the close-out's 58 reports fall after the run on `created`) and A2 (a Legacy bug join drops the catch-up
  writes and the moved reports, and keeps the re-sent copies).
- Span: the new tracker's export, the old export, the register, the agreement, the runbook (5 files).

**The chart** (`parallel_run_triage.svg`): Ask A's eight figures, both series for each week, each bar labelled; graded
on its content (Ask A's figures) and its parts (both series for every week, labelled; the title).

**Hazard table.**

| Hazard | Asks moved | Per-ask delta |
|---|---|---|
| Clocks (UTC in the export; Helsinki weeks; the run's end at 23:59:59 on Sunday 29 November) | A, B | A: week boundaries; B: none once in Helsinki time |
| The re-send of 18 November (copies under new keys, the old number in labels) | A, B | A: week 3 copies counted (60 more with no triage action on the created path); B: copies counted in their groups |
| Scope (restricted issues, the team's tasks, WEBC's own site reports) | A, B | both: rows that are not triage items |

**Referee.** The old export's `opened` through each report's old bug number (A1), the labels and the move entries (A2),
the changelog's component items (B1); none hands over a level.

**Blind responses.** One rate on each week's items recovers at most 1 of Ask A's 8 cells, the best constant 1, every cell
nil 0; one share of the run's total recovers at most 1 of Ask B's 8, the best constant 1.

**Cracker sheet** (the cracker landed the call, ran the hygiene battery, executed every filed definition, dropped the
re-sent copies on the old bug number, found the moved reports, replayed each report's state at the run's end; its two
natural readings of a report's filing time are run as paths, created (identical figures when created fills in for
reports without a Legacy bug value) and the old tracker's opened through Legacy bug (identical figures with a moved
report's number read from its changelog)):

| Ask figures | The cracker's route | Kept | Verdict |
|---|---|---|---|
| A, four weeks' items with no triage action within 24 hours (4) | created path 98, 90, 105, 48; legacy path 89, 71, 38, 41 | 0 on either path | miss |
| A, four weeks' items closed by the run's end (4) | created path 306, 264, 185, 85; legacy path 254, 179, 85, 53 | 0 on either path | miss |
| B, eight groups' arrivals (8) | created path 455, 132, 114, 170, 464, 75, 74, 55; legacy path 332, 104, 86, 119, 359, 60, 60, 43 | 2 on the created path (Extensions and Platform and Updates, where the re-sent copies and the close-out cancel), 0 on the legacy path | miss |
| The chart's content (1) | Ask A's figures | 0 | miss |

Measured by: generator/cracker.py (calc.ceiling_report on the cut pack; checks.py asserts every path at or under 40).

**Mirror sheet.** The mirror stops at R1 (6 triagers), reads the triage project as it stands (no moved reports), counts
any change by a triager as triage, takes closed from the resolution date and the components as they are now: 94, 81,
101, 46 and 224, 186, 149, 64 on Ask A, 338, 207, 117, 153, 454, 77, 78, 56 on Ask B; it keeps the chart's parts only.

Mirror leakage: 5.6 per cent of ask weight (the chart's parts, 1 of 18 ask criteria).

Pair ceiling: 34.6 (the worst natural path, created: the cracker 54.2 with 3 of 18 ask criteria, the mirror 15.1 with 1;
the legacy path 31.6; with every device found, the old number read from the labels and the changelog as well and the
filing time from the old tracker, 57.5).

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
- 2026-10-18 build: ask device A1 of the design stage (the bridge's history entries under the migration lead's account
  while she was on the rota): no literal rule separates her bridge entries from her own triage without a fork; the
  bridge runs under its service account and she is off the rota.
- 2026-10-18 build: Ask A's second figure as the items still untriaged when the run ended: zero in three of the four
  weeks, so the all-nil response kept them; replaced by the items closed by the run's end.
- 2026-10-18 build: the design stage's Ask B (closed items and closed duplicates by group): a careful replay of the
  changelog under the agreement's definitions cracks the Close transition and the moved reports.
- 2026-10-18 build: Ask B as the items in each group's components at the run's end: once the reports the bridge had not
  yet written at the run's end sit in no group, every cracker path kept 5 to 7 of 8 (pair 46.8 to 51.4).
- 2026-10-18 build: Ask B as the reports moved to the web-compatibility team by group: the created path kept 6 of 8.
- 2026-10-18 build: the bridge writing the old number into Legacy bug on every issue: a cracker joining the old export
  on it landed every ask figure (pair 59.1); a real bridge's catch-up writes through a short payload, now modelled.
- 2026-10-18 build: the portal's shares by exact version, point releases as their own rows: reading each point release
  as a new version moved the call to 6, a messy choice flipping the answer; the portal publishes major versions.
- 2026-10-18 build: a parallel-run report PDF with the weekly side-by-side of both trackers: its weekly items by filing
  week would tie only under the old tracker's filing times, an oracle for Ask A; not built.
