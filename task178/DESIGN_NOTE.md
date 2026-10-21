# task178 design note

**Status: DESIGN (stage 2), architecture 1 of the redraw, card registered 2026-10-21.** The author redrew the
number in a new cell after seed FC49's product-security world died at stage 1 (its record is kept below under
`## FC49 screen record` and in `## Tried and rejected`). Cell, allocated by the main session:
physical-environmental-sciences / climate-weather-extremes, Forecasting. Organisation, decision, quantity and
mechanism were searched inside the cell (prototypes in the session scratchpad, b178r/proto: p1 to p13).

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task178.json`, guard `check` WARN only (time_semantics strategy
  risk, answered under `## Three rules`: no field, code, unit or definition flips the call; repeat.gate_g
  forecasting against task479, answered: the lane is Forecasting and the mechanism differs). Structural tests
  same_puzzle_older (task461) and same_driver_older (task102, task130 lineage, task134 lineage, task162, task501
  lineage) differentiated on the card, one line each.
- **Pairing:** Physical & Environmental Sciences, task type `climate-weather-extremes` (F), never drawn before.
  The deciding quantity is an extreme-sea-level exceedance frequency in a coming window.
- **World:** a fictional Maine coastal city (Merrow Harbor) rebuilding Granite Wharf from 1 April to 31 May 2027
  from a temporary work trestle; the waterfront project engineer sets the trestle deck elevation in the
  construction documents before the piles are ordered. Allowed deck elevations 10.50 to 12.50 ft above MLLW at
  the harbor gauge in quarter-foot steps; the deck is set at the lowest elevation at which high water is expected
  to reach it on no more than one tide in the window (exact settings and bar fixed on the cut pack so the golden
  sits mid-bin).
- **Shape:** 04, setting one dial: the expected number of tides reaching the deck at every allowed elevation,
  the committed elevation and the one below it; asks supply the rest (`## Ask sheet`).
- **Strategy:** `time_semantics` (F1, the window the decision bets on), gap time, G13 then G7, Gate G
  forecasting, layer2_family field_method, layer2_pattern own:skew-surge-joint-probability-over-a-known-tidal-window.
- **Data-native sentence:** the harbor's high waters are an astronomical tide known years ahead plus a weather
  surge, and April and May 2027 fall at the 18.6-year low of the semidiurnal tide with perigee at the quarter
  moons (perigee and syzygy anti-aligned about 7 April 2027), so the window's own predicted high waters sit
  about 0.2 m below the record's April and May average and the record's exceedance rate, however trended,
  overstates the window several times over.
- **Sources (one line each):** the five client families (`two-layer-task-design.md`): field_method, the field's
  own joint-probability method done right; the textbook route is a GEV or POT on observed levels with a sea-level
  trend (Coles' sea-level examples), which takes stationarity of the total level for granted; the actuarial
  catastrophe and energy load cards: an exposure-window count, here the window is fixed by the works; the
  epidemiology surveillance cards: a baseline from history, here the baseline is not exchangeable with the window
  because part of the signal is deterministic and known. No client card exists for this domain.
- **Measured lever (p13, three seeds, on the clean truth):** at 11.75 ft the window's JPM expects 0.51, 0.64 and
  0.93 tides (truth by Monte Carlo 0.36 to 0.43); the seasonal climatology at 2027 sea level 7.3 to 8.9, a linear
  or Poisson count trend 7.0 to 10.1, the last season 6 to 9, the last three 7.3 to 9.3, the 18.6-year analogs
  4.5 to 6.0; golden family (linear or recent-20-year surge base, GPD tail, per month) picks 11.75 ft in every
  seed, every route without the window's tide picks 12.25 to 12.50 ft.

## FC49 screen record (world spent, kept for the record)

**Status: PAUSED at stage 1, no card ever registered, nothing cut.** New, Forecasting, seed FC49: a
network-equipment vendor's product-security team has one extra triage analyst for the first quarter of 2027,
who goes to the product line with the most critical triages forecast for the quarter (one triage per CVE per
affected product line, done as part of that line's advisory) if its lead over the runner-up is larger than
the forecast's own error one quarter ahead, and otherwise stays in the shared pool; the staffing note is due
on 10 December 2026. The world, the decision and the quantity were kept. The seed's own mechanisms (the
policy's four-quarter mean and eight-quarter lead deviation as a filed HOW, the vendor's severity score as
the decider, the dashboard as an official decoy, the release-train swing inflating the lead's deviation into
a hold) were never candidates. Two decisive steps were screened on code, each one of the brief's ideas in
its strongest form, over three seeds each, and neither held. No architecture is live. This note holds the
screen record only; it carries none of the `precut.py` sections, because no design exists. The prototypes
stay in the session scratchpad (b178/proto: `protoA.py`, `protoB.py`, `screen178.py`, whose output
`screen178.out` is byte-identical with `screen178_run2.out` over two runs).

**The structural sentence, and the first thing to read.** A line's coming quarter differs from its own
record only where work reaches its advisories through a channel or a train slower than the quarter: reports
waiting under embargo in the coordination centre's queue, a component refresh that triages every
third-party critical accumulated since the line's last one, a supplier's pre-notified bulletins. Every
reading of that difference that holds is a count not yet arrived, completed for the slow unit, which is
task181 v2's driver ("the units whose records arrive slowest look quiet exactly while they are surging, so
the comparison has to be made on the complete count each unit's own arrival history implies"), landed on
the portal once its estimand was filed literally, and honestly `maturity_censoring`, which task201 holds in
the ban window. The readings that are not that driver either hand the call to the cheapest route (the queue
read at face value, a rule of thumb for a long-delayed refresh) or move the decisive step into composition
(conversion or slip by case type or by line, `composition_mix` held by task165) or into semantics (which
other lines a queued report's code also ships on). The quantity is also thin where it is not pipeline: a
real vendor's own-code criticals run one to five per line per quarter, so a lead that is real against the
forecast's own error needs the counts third-party CVEs supply, and third-party CVEs reach a line only
through its refresh train. A draw on this quantity needs a difference between the coming quarter and the
record that no recorded channel already carries and no slow channel is completing; none was found here.

**The registration finding.** The honest strategies were `maturity_censoring` (candidate 1, and every
per-line reading of the queue), held by task201 (registered 13:39), and `composition_mix` (candidate 2c),
held by task165 (14:10). The window on main at 5c5631d is task201 (`operations_desk`, `season_or_peak`,
`utility_or_infrastructure`, `field_unit_lead`, `published_series`), task247 (`executive_team`,
`vote_or_meeting`, `university_or_school`, `research_desk`, `operations_log`) and task165
(`council_or_assembly`, `purchase_order_or_contract`, `local_government`, `operations_director`,
`register`). The keys this world offers honestly outside them, had a design held: organisation
`manufacturer`, forum `committee_or_panel`, forcing event `budget_or_appropriation`, role
`capacity_planner`, calibration `none`. Nothing was registered and no axis of the window was spent.

**The taxonomy finding.** A product-security team's triage workload has no client task type of its own.
Product Analytics serves Forecasting through retention, churn and feature adoption only (task162's browser
reports sat in feature adoption because version adoption decided them), and none of them is a line's
critical CVE count. The honest home is General Statistics & Data Science,
`regression-classification-model-diagnostics` (the forecast model and its out-of-sample one-quarter error),
or the house domain `business-operations-analytics` (`workforce-labour-planning`) that maps there.

**The repeat screen.** `guard.py recent`, `coverage`, `mechanisms --objective forecasting` (82 builds) and
`slots` ran before any card, `slots` on embargo, advisory, triage, refresh, roll-up, freeze, deferred,
backlog, accumulated, Hawkes, self-exciting, excitation, follow-on, variant, code age, new code, churn,
lifetime, honeymoon, spillover, embedded, sibling, shared code, fan-out and observation effort: no slot or
card spent a refresh-accumulation or forward-batch mechanism in a product-security world, and the binding
matches are by the abstraction test (task181 v2 and v3, task174's vintage screen, task136, task163,
task132, task75 v1, task199). The brief's near drivers were read in full on their cards: task162 (restart
bursts after Patch Tuesday), task148 (abandonment in a 911 queue), task159 (backlog behind full trains);
none is touched by either candidate.

## Tried and rejected

- **Candidate 1: the deferred component refresh** (the brief's release-train idea in its strongest form;
  `protoA.py`, seeds 11, 12 and 13 fixed before outcomes). Driver as drafted: a line's kernel and crypto
  updates wait for its platform release, so its recent quarters record only the rest of its third-party
  flow, the held criticals keep arriving upstream at the rate its earlier refreshes and its siblings' current
  ones show, and they land in one roll-up with the release inside the quarter. Killed at stage 1 on
  measurement (a rule of thumb lands) and on the draw screens (it is task181 v2's driver, honestly
  `maturity_censoring`).
  - The world: eight upstream component groups (kernel 4.0, crypto 2.2, SSH 0.8, web 3.0, DNS and DHCP
    1.2, routing 1.5, management 1.0, libraries 5.0 critical CVEs a month), five lines with group-specific
    affected shares, refreshes monthly (DATACENTRE), quarterly (CAMPUS), half-yearly (BRANCH in April and
    October, WIRELESS in May and November) and every four months (GATEWAY in April, August and December),
    8 per cent of upstream criticals exploited and patched out of band within three weeks, own-code
    criticals 0.8 to 2.2 a month a line, chipset bulletins 2.5 a month for WIRELESS. GATEWAY's kernel and
    crypto groups were held after its 16 September 2025 refresh until the GATEWAY 10 platform release on
    10 February 2027: seventeen months at about 4.9 affected criticals a month. As-of 10 December 2026.
  - The golden family (GATEWAY's first-quarter critical triages): its own pre-freeze group rates over each
    group's months since its last update, the same on its last 24 pre-freeze months, and the held groups
    priced at the sibling lines' post-freeze rates scaled by GATEWAY's earlier ratio to them: 104.2, 109.4
    and 91.8; 111.2, 108.8 and 105.2; 105.5, 101.9 and 118.1 (a spread of 5.5 to 16.9 per cent of the
    median, so GATEWAY's figure needs a bin of 25 or more). Realised first-quarter truth 72, 82 and 96.
  - The routes as first drawn (the runner-up 43.7 to 48.1): the trailing four quarters BRANCH, DATACENTRE,
    BRANCH; eight quarters BRANCH, DATACENTRE, DATACENTRE; the same quarter last year DATACENTRE,
    DATACENTRE, CAMPUS; the latest complete quarter and an eight-quarter trend DATACENTRE in all three; the
    average roll-up per release GATEWAY in seeds 11 and 13 (46.2 against 45.0, 46.0 against 38) and
    DATACENTRE in 12; a factor of 1.5 to 3.0 on GATEWAY's recent roll-up GATEWAY in all three.
  - With DATACENTRE's own-code criticals raised to 9 a month (the naive leader at about 70 to 80, the
    runner-up 67.2 to 74.1): every time-series and per-release route files DATACENTRE; a factor of 1.5
    misses in all three seeds, 2.0 lands in seeds 11 and 13, 2.5 and 3.0 land in all three. The factor at
    which GATEWAY overtakes is 1.55, 2.03 and 1.52 against the golden's 2.20 to 2.51, and the 2.5 and 3.0
    factors (91 to 123) sit inside the family's own 94 to 117, so a rule of thumb for "a long-delayed
    refresh is two or three times a normal one" lands the line and the figure's bin.
  - The eda6c8c screens, as code: dispersion and truncation direction do not apply (a count, no
    suppressing threshold); variance-only passes (the step moves GATEWAY's point 2.20 to 2.51 times); the
    common-exposure subset fires in its once-thought-of form, since the golden is GATEWAY's own pre-freeze
    kernel and crypto months filtered and divided, times the seventeen-month gap (equal to the family's
    median in four of six runs), and no earlier refresh closes a gap like it (the longest is four months),
    so the step's whole difficulty is recognising the held groups.
  - Why it is dead whatever the tuning: the held criticals are incurred and not yet triaged, and the
    forecast completes them for one slow unit, which is task181 v2's driver by the abstraction test (latent
    structure: records that arrive late for one unit; default: what has arrived; correction: the complete
    count the unit's own history implies) and `maturity_censoring` honestly; relabelling it time or
    decomposition to pass the window would be a lie in the card.
- **Candidate 2: the coordinated batch in the coordination centre's acknowledgement queue** (the brief's
  known-forward-workload idea, read through the queue's own slip and conversion history; `protoB.py`, seeds
  21, 22 and 23 fixed before outcomes). Killed at stage 1 on measurement in all three configurations.
  - The world: own reports that become critical advisories 2.5 to 5.5 a month a line, each acknowledged
    with a planned disclosure 45 to 120 days on and a slip drawn per case; third-party criticals 4 to 12.5
    a month a line; five earlier coordinated batches of 9 to 18 (2023 to 2025, one a year somewhere) so the
    queue's history has precedents; at the as-of a coordinated multi-vendor batch of 34 criticals listed
    against GATEWAY.
  - 2a, the batch planned for 2 February 2027 and multi-party cases slipping as single-vendor ones do: the
    face-value reading (every open case planned in the quarter, on its listed line, at full size), the
    pooled-slip reading and the golden (slip by case type) all file GATEWAY in all three seeds, so the
    cheapest queue route lands; the golden's lead over DATACENTRE is 1.7, 12.6 and 11.7 against a model
    error of 11.1 to 11.4 (ratio 0.15 to 1.10), so even the golden's pick is not robustly real.
  - 2b, the brief's slip check (the batch planned for 2 March 2027, multi-party cases slipping by a gamma
    with a mean of 48 days): the batch lands inside the quarter with probability 0.35 to 0.36, its landing
    variance takes the error to 19.0 to 19.3 against leads of 10.1 to 17.7 (ratio 0.52 to 0.92), and the
    golden (DATACENTRE) is the trailing route's and the seasonal route's answer in all three seeds while the
    face value files GATEWAY: the slip noise swamps the lead exactly as it did task174's.
  - 2c, the batch listing GATEWAY and BRANCH, which ship the same VPN stack, BRANCH affected by about 30 per
    cent of the stack's earlier coordinated cases: the face value lands GATEWAY in all three seeds and the
    pooled conversion files GATEWAY, GATEWAY and BRANCH; the step that separates (conversion read per
    listed line from the stack's earlier cases) is `composition_mix`, held by task165, and reads the
    vendor's own affected determinations, which the brief names as semantics.
  - The eda6c8c screens, as code: dispersion and truncation direction do not apply; variance-only fires in
    2b (the step lowers GATEWAY's point and raises its error, so the golden sits near the hold); the
    common-exposure subset fires in 2a and 2c (the face value is a filter and a count, and it lands).
- **Paper screens, not coded.**
  - The queue read per line at the same lead (the share of each line's quarter already acknowledged three
    weeks before it starts, from the acknowledgements as they stood, including a line whose pre-notified
    supplier bulletins are light this quarter): task181 v2's driver exactly, and `maturity_censoring`.
  - Follow-on research after a high-profile disclosure (variant hunting): task181 v3's self-exciting runs
    in the opposite direction, and critical follow-ons per trigger are a handful, too few for a real lead.
  - Code age (criticals concentrated in code shipped in the last two years, a new release yielding a wave a
    few quarters on): own-code criticals are too thin for a real lead, and a component upgrade restarting
    the curve is task132's renewal.
  - A shared-code fan-out (a batch listed against the line it was found on also lands on the line that
    embeds the same daemon): the call flips at any fan-out, so the decisive step reduces to the triage
    standard executed on an affected set inferred from co-listing, rule application on a read of the
    acknowledgement's product field.
  - The open queue as survivors (old open reports rarely become critical advisories, so the pooled
    conversion overstates the line with the stalest queue): task75 v1's open cases against completed
    durations, censoring by its honest label, and own-code counts too thin.
  - A component refresh closing an ordinary interval (the release train alone): a read of the calendar, and
    the same quarter last year lands it.
  - An upstream group's flow stepping up, or a transient upstream wave ending: with prompt triage the latest
    quarter shows it and lands; with a lagged refresh it becomes candidate 1's held backlog.
  - A staggered programme (a reachability or VEX workflow, a memory-safe rewrite) read against lines not
    yet on it: task136's and task163's common rise between the before and after windows.
  - The queue's planned dates as they stood at each origin (a real-time back-test against the overwritten
    planned-date field): task174's vintage screen on a schedule's slips, and the overwritten field makes the
    step a reading.
  - The internal testing effort read against its findings: task199's observation-effort organ, and the
    testing plan names the step.
  - The lead's error narrowed by the CVEs the top two lines share: the seed's own uncertainty-hold
    architecture, banned as a near driver, and the Poisson reflex lands any narrowing.
- **Redraw cell, climate-weather-extremes: candidates screened (2026-10-19 to 21).**
  - Mixed populations in annual maxima (tropical against extratropical): paper; the tropical population rests on
    a few dozen events, the mixture fit's spread exceeds any lever, and the storm-track file needed to split
    them is single-purpose.
  - A summer hot-day count conditioned on spring soil-moisture deficit: paper; a regression on the obvious
    covariate (the textbook route the blind readers take) with skill near r 0.4, lever under the noise.
  - Fixed-interval against sliding-window rainfall maxima (Hershfield-Weiss factor from an hourly overlap):
    paper; lever 5 to 13 per cent and the textbook 1.13 lands.
  - A declustered heat-event count (extremal index): paper; the run-length is a knob, the dispersion screen
    fires.
  - Areal against point rainfall return levels: paper; the areal-mean series fitted directly is the golden.
  - A nonstationary GEV on a warming covariate: the textbook itself.
  - Frost after bloom (phenology-conditioned frost risk): paper; the bloom model's base temperature and stage
    thresholds are open knobs, determinacy fails.
  - Joint exceedance across a network (tail dependence): paper; the estimator family's spread is wide.
  - A saturating gauge or a recorder lost in its largest events: task172's cap and task245's driver.
  - The forward astronomical tide (this draw), first form: a winter (November to February 2026-27) closure
    count at a mesotidal semidiurnal site; killed on measurement (p1, p2): the window's tidal index sits at
    0.83 to 1.0 of the long-run mean, so the climatology lands within 17 per cent.
  - Second form: March to April 2027; killed on measurement (p6, p11): the last season (2026, also weak
    springs) lands (13 against a golden 12.4 to 15.2 at one threshold, 7 against 6.2 at another).
  - Hourly non-tidal residual against skew surge as the decisive rung: killed on measurement (p6, p9): with the
    timing interaction at 0.5 to 0.8 h per metre of surge the all-hours residual and the residual at predicted
    high water both land the golden; only the cycle-maximum residual overstates (x1.5), so it is at most a lower
    rung.
  - A macrotidal estuary site: rejected on paper (p3): the tide is so dominant that every reader opens the tide
    table first.
