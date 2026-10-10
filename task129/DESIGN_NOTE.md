# task129: which shipped change gets Sønderå Medier's Q4 operations squad, realising analytical_tasks note RC02 (analytical_tasks/06_root_cause/RC02_slow-views-partial-exposure-cpu-mix.md)

Stage 1 (draw), drawn 2026-10-10. This is the build's one design note; the design stage extends it. RC02 has never been built, so this is its first realisation.

## Draw

```
DRAW  (independent draws, checked with .claude/skills/fingerprint/guard.py)
  Card filed with guard.py register before the ladder was written? registered by the coordinator in task-number order after task128, with the registration redraws recorded under ## Guard   Verdict: see ## Guard (registration)
  Shape: 11 before and after with a control   Gate G mechanism: decomposition_attribution (method_or_model_selection supporting)
  Gap: population (decisive), objective, time   Pattern: E (decisive), D (the transport)
  Domain: business-operations-analytics   Subdomain (enumerated): service-operations-sla   Objective: root-cause
  Pairing repeated from last build? No. The last three on file are task119 (policy-education x anomaly-detection), task121 (product-analytics x root-cause)
    and task122 (product-analytics x experiment-causal); business-operations-analytics x root-cause was last drawn at task111
  Stakeholder role: head of digital operations at a regional news group, who owns the internal page-delivery service level and assigns the
    operations squad's quarter (operations_director)
  Context-artifact type: close_out_summary, digital operations' Q3 service close-out, the pack the quarterly service review reads (share of mobile
    views over the line by month and title through September, correct, ranking no change)
  Calibration form: realised_outcome_roster, the operations squad's register of the eleven fixes it closed since 2023, each with the change it
    addressed and the over-budget views it brought back as measured over the four weeks after it landed
  Decision type: root_cause_named, the one shipped change the Q4 squad fixes, with the mobile views a month its fix brings back under the line
  Decisive mechanism: G14 conditioned yield. Each co-shipped change's cost on a view is a switch on a state no column carries (the view is its
    device's first load after a release-train deploy, or a reload of the cached bundle), built from the order of each device's views; G6
    composition (the phone mix through the device registry) carries rung 2, G1 (lab bytes against field views) rung 0
  Repeats from prior builds: none inside the ban window. (population, E, root_cause_named) repeats task36; (population, E, decomposition_attribution)
    repeats task36, task44 (lineage) and task107 (lineage); a differentiation line for each is on the card

  Niche: a page-delivery service-level breach at a regional news group's shared digital operations unit: which of five changes shipped since spring
    gets the operations squad's next quarter, when the header-bidding ad stack and the redesign's client-side front end only ever switched on together,
    template cohort by template cohort
  Forum: committee_or_panel (the quarterly service review: the three titles' editors-in-chief, ad sales and digital operations)
  Forcing event: vote_or_meeting (the quarterly service review meets and allocates the operations squad's Q4, which opens on 1 October)   Organisation family: media_or_publishing
  Scoring unit: units served (mobile page views delivered inside the line)
  World: Denmark; DKK; Sønderå Medier (invented), a regional news group running three daily titles on one web platform, metered paywall with an
    ad-free subscriber layout; Bølge, the redesign programme (invented)
  People, drawn with guard.py names --geo Denmark --seed 129: Elin Lauritsen (head of digital operations, the requester), Ove Schmidt (group digital
    director, holds the consent-banner belief), Finn Thygesen (front-end platform lead, owns the new front end), Caroline Mortensen (editorial product
    director), Gunnar Paulsen (head of ad operations, presents the lab-weight basis), Gunhild Lund (data engineer, owns the view export), Mette Johansen
    (release manager, keeps the release train log), Simone Thorsen (performance engineer, keeps the closed-fix roster)
  Spine (planned): rum_mobile_views_2026.parquet, about 1,200,000 rows, one sampled mobile page view (a field timing beacon), grain page view, synthetic
  Deliverables (planned): q4_squad_call.pptx (the service-review slides: the call, the cohort chart), q4_squad_call_cohort_effects.xlsx (the cohort grid)
  Opening move (provisional): symptom-first, filed as other (the vocabulary has no symptom-first key)
  Criteria arithmetic (shape 11): 6 redesign cohorts x 3 figures (the ad stack's views a month on the cohort's ad-supported views, the framework's, the
    cohort's pre-switch gap against the not-yet-switched cohorts in points) = 18, plus the ad stack's views on the puzzles pages and the framework's on
    subscribers' views (2), the three dated changes' views (3), the committed change, its views a month, the runner-up and the gap (4), 5 named chart
    parts and 2 files: 34 before any device-carried ask
```

As-of date: 2026-09-07

The August field extract is taken five days after month-end; the quarterly service review meets in mid-September and the squad's quarter opens on 1 October. The committed call faces forward (the change Q4 fixes); its figure is valued at August's traffic because the service level's own document says a fix is valued at the latest full month's traffic, so this is a convention filed in the pack, not a forecast, and the objective stays Root-Cause Analysis.

**Similarity claim.** No prior build splits the joint effect of two changes that only shipped together on a per-view state built from the order of each unit's records against version changes, with the two changes costing opposite states so that every total and every visible-column split ties under both readings. The nearest records standardise a partial-exposure group on a visible composition (task73's retention redraw, lineage), carry one pilot's pooled gain onto a request with the inverse mix (task44 v2, lineage), or size one check's reach from a per-source delivery property (task107 v1, lineage).

## Stump sentence

A competent solver aligns the redesign's cohort-by-cohort switch-on for the joint effect of the ad stack and the framework, separates them with the puzzles pages, which took the header-bidding wrapper alone on one date, and subscribers' ad-free views of the redesigned templates (found through the subscription register), standardises both groups to the ad-supported views' phone mix through the device registry, which closes the joint ramp exactly, and names the ad stack; the step that lands it there is reading each change's cost as one figure per phone class, when the framework costs a view mostly on a device's first load after each release-train deploy and the ad stack mostly on reloads of the cached bundle, and the daily players and daily readers who make up both separating groups are mostly cached reloads while most ad-supported views are first loads, so reweighted to the ad-supported views' first-load share the framework fix brings back the most views a month.

## Decisive rung

Measured trap **#13, validates on one population, applies to another** (`.claude/skills/stumping/references/traps/_measured.md`): established, decided 3 of the client's 64 measured tasks, 2 of them under 0.50. Each separating group's effect fits every view it can be checked on and is carried to views that differ on one axis, first load against cached reload, with the evidence of the difference left in the record (the order of each device's views against the release train's deploys). Behind it, **#11, beats the headline trap, misses the quiet one** (4 of 64, 2 under 0.50): the phone-mix residual is the headline trap, standardising on the registry's phone class closes the joint ramp to the view, and the solver stops confirmed.

In-house record: the pilot's only two held calls carry this same pairing, #13 with #11 behind. FC01's final rung (task117, rounds 4 and 5: 25.6 and 28.5 plain, 29.3 skeptic, the call missed every time) and OS01 (task118, ten rounds between 33.7 and 46.5, the call never landed). Not drawn from the top four: their architecture (a published control set behind a reproduction clause) is what the pilot's solver reproduced without effort, so a control set here would refute the stop rung and point at the move.

## Ladder sketch

The answer is C, the framework (the redesign's client-side front end). Figures below are design targets at August's traffic (about 60 million mobile views a month) and are tuned at stage 2.

| Rung | Construction | Names | Killed by (one shipped fact) |
|---|---|---|---|
| 0 | Lab byte bridge from the monthly synthetic crawl: KB per crawled mobile page by resource type, mapped to the five changes, current crawl against the spring crawl | B, the image pipeline (images +520 KB; C 4th at +140 KB) | The service-level document scores a fix on field mobile views over the line, not on crawled page weight (and the crawl's URL list was refreshed, so its two months weigh different pages) |
| 1 | Field event study: the over-budget share's step at each release date, in views a month, the redesign ramp left unattributed | D, the consent banner (about 0.84M; C unplaced) | The Bølge rollout log shows the ad stack and the framework switched on template cohort by template cohort over six weeks, a ramp no single date captures and larger than any dated step once aligned by cohort |
| 2 | Cohort-aligned joint ramp split by the two separating groups (the puzzles pages' wrapper step, subscribers' ad-free redesigned views through the subscription register); read raw it leaves a residual against the joint ramp, standardised to the ad-supported views' phone mix through the device registry it closes exactly | A, the ad stack (about 1.46M against C's 0.92M, 1.59x; C 2nd) | The order of each device's views against the release train: the framework's cost falls on the first load after each deploy and the ad stack's on cached reloads, and both separating groups are about 85 per cent cached reloads while the ad-supported views are about 70 per cent first loads |
| 3 | **Decisive:** each group's effect measured separately on first loads and cached reloads within phone class, reweighted to the ad-supported views' state and phone mix; each fix counted on the views it acts on (the ad stack also on the puzzles pages, the framework also on subscribers' own views) | **C, the framework (about 1.41M against A's 0.96M, 1.46x)** | none |

Partial corrections priced (L3), each to be asserted at stage 2: standardising on any visible column (referrer, connection, device category, title, hour) changes nothing, because the state is decorrelated from every one of them inside each group by construction; classing the first view of a visit as the first load (the landing proxy) leaves the ad stack in front, because subscribers' daily newsletter landings and puzzle players' daily first plays reuse a bundle cached before the last deploy on most days.

Why every split ties (L8, complete-partition invariance): within each phone class the ad stack's cached-load surplus equals the framework's first-load surplus and both separating groups share one first-load share, so the two changes' joint cost is the same on a first load and on a cached reload, and every classification of views (the true state, the landing proxy, any visible column, none) splits each phone class's joint ramp into two figures that sum to it on every cut; only the phone-blind raw split leaves a residual, and the registry's phone class closes it, which is what makes rung 2 feel finished. The physical reading: on a first load the critical path is filled by the framework's download and compile while the wrapper's work overlaps the network wait; on a cached reload the bundle is cheap and the wrapper's main-thread work lands on the path. The equality is a tuned construction and goes into the design stage's realism debts.

Position targets: C 4th on rung 0, unplaced on rung 1, 2nd on rung 2 behind A by 1.59x, 1st on rung 3 by 1.46x (and 1.68x over D). Discriminator dominance: A carries 1.59x into rung 3 and the state reweighting moves the ratio by 2.32x, above the 1.91x required. Per-state targets within phone class, in points of over-budget share on ad-supported redesigned views: framework 3.5 on a first load and 1.5 on a cached reload, ad stack 0.9 and 2.9, so the joint cost is 4.4 either way.

Organs at the draw: the closed-fix roster certifies that a fix's value is the over-budget field views it removes (every closed fix's realised saving reproduces from the view log) and is blind to the decisive move for a computable reason: in every closed case the change switched on for every view at once, so its effect was read on the very views its fix acted on and no case carries a co-shipped pair or a separating group. Its resemblance points at the decoy: a closed 2024 ad-slot fix on the puzzles pages realised a saving beside the ad stack's rung-2 figure. Filed pins: the service-level document (a view misses when its largest contentful paint exceeds 4.0 s; a fix is valued on the views it brings back at the latest full month's traffic), the paywall policy (signed-in subscribers get the ad-free layout), the device registry (phone class from the benchmark band). Licensed wrong basis: the service-level document records that the ad-revenue committee reviews performance work on the crawl's lab page weight, and Gunnar Paulsen presents that basis. No shipped file ranks the five changes; the crawl report ships at resource-type grain, and any by-change lab-weight table ships only as a declared wrong-basis distractor.

## Why it survives the solver

Against the pilot record, move by move. The solver reads every filed document and executes every stated rule, and no document here says a cached reload costs less than a first load, how often either audience comes back between deploys, or that a group's mix should be checked on anything but its columns. It finds every join whose keys line up, and the decisive state needs no join at all: it lives in the order of each device's views against the release train's deploys, while the one join it will find, device model to the registry, carries only the phone class that makes rung 2 close. It reproduces every published table and back-tests every corpus, and the roster certifies the field metric while being blind to transport, so no corpus refutes the stop rung and no reproduction check points at the move. It reconciles to control totals and runs event studies on staggered cohorts, and every split it can build sums to the cohort-aligned joint ramp on every cut, so no check it writes for itself shows a residual once the phone mix is in. It replays at the finest grain, and that replay is exactly what holds each change's cost fixed per phone class, the shape that held in FC01, where every solver replayed each charge from its plug-in time and never re-timed the hand-offs. It is not OS01's judgment either: once the state is built, the per-state effects are measured inside the groups and the reweighting is forced, so the answer is not a reading the files merely support. The accepted weak point: a solver that asks whether every view pays the framework's cost alike, or that sorts each device's views and compares the first view after each deploy with the rest, finds the split; that is the intended discovery path, and the release train log corroborates it.

## Nearest exemplars

1. *Merge the copied prospecting campaigns on 1 July instead of reverting the Anvil bid change* (Product Analytics, paid user acquisition), measured mean **0.58** (0.71, 0.72, 0.55, 0.45). Nearest on decision shape: one change made after a metric rose across several dated and undated changes, the loud dated change a decoy, the real driver visible only through a construction on the records and priced from the account's own natural experiments; the model rejected the dated lure every time and lost on the size it never priced from the change log (#25).
2. *Fix the approval-gated connection stall in three scoped parts and keep the listing, setup and enablement plan as they are* (Product Analytics, SaaS trial activation), measured mean **0.52** (0.49, 0.68, 0.48, 0.49). Nearest on mechanism family: rival causes each refuted on their own data, a composition standardisation that reverses the blended read, and a segment that only a join exposes; the model found the cause and lost on the segment it treated all one way (#6).

Both sit above 0.50 because the model reaches the right family of cause and loses on sizing or scope; this ladder bets the call itself, which is why the decisive rung changes the named change rather than its size.

## Guard

Verdict on the scratch card (`guard.py check`, 2026-10-10): **WARN**, exit 0. Nearest drivers 0.08 at most (task98 v4 lineage), 0.07 against task121's own v1 lineage (a state each unit holds until the effect clears) and task44 v2, all under the 0.12 warning line.

The first card draft, on the note's own axes, was BLOCK on nine findings (and one persona WARN) against the corpus as filed (last three task119, task121, task122), each cleared by redrawing the axis named, never by relabelling the same world:
- ban.pairing (product-analytics x root-cause, task121): the world is redrawn around the group's internal page-delivery service level, owned by the head of digital operations and reviewed quarterly by the titles, which is Business & Operations Analytics, service-operations-sla (never drawn).
- ban.role (product_manager, task121): the requester is the head of digital operations (operations_director).
- ban.artifact (monitoring_export, task121): the requester works from the monthly service report (published_series); the crawl report stays in the pack as context.
- ban.calibration (pilot_log, task122): the randomised fix pilots become the squad's roster of closed fixes with realised savings (realised_outcome_roster), a different organ, blind to transport for its own reason.
- ban.shape (07, task122; 18, task121's, is also in the last two): shape 11, the cohorts as treated units.
- ban.forum (executive_team, task122): the quarterly service review (committee_or_panel).
- ban.forcing_event (vote_or_meeting, task122): the review's allocation of the squad's Q4 (budget_or_appropriation).
- test.same_puzzle_older and test.same_driver_older: decision type recorded as root_cause_named (the call names the change to fix), which cuts the collisions from seven builds to three; the card carries one differentiation line each for task36, task107 (v1 lineage) and task44 (v2 lineage).
- people.first WARN (Yrsa, task91): replaced by the next drawn name, Gunhild Lund.

WARN answered:
- repeat.gate_g (decomposition_attribution, against task121 and task122): the call apportions one joint effect between two changes that only shipped together, which is what the label names; task121 re-attaches sessions to accounts and task122 scores an experiment's lift, so the label repeats and the constructions do not, and promoting the supporting method_or_model_selection label would be a key chosen to dodge the count.

The sibling drafts task124 to task128 are unregistered, so the check above did not see them; registration re-runs it against whatever the coordinator has filed first.

Registration (coordinator, 2026-10-10, after task124 to task128 were filed): the draft card took **BLOCK** on ban.artifact published_series against task126 and ban.forcing_event budget_or_appropriation against task127, with a repeat.deliverables WARN (csv+pptx) against task128. Each axis was redrawn without touching the decisive rung: the requester works from digital operations' Q3 service close-out, the quarter's pack for the review, carrying the same monthly figures by title (close_out_summary; monitoring_export is task128's and published_series task126's); the call is forced by the quarterly service review's meeting, the key the draw first wanted and lost to task122, which has left the window (vote_or_meeting); and the cohort grid ships as a workbook (pptx+xlsx). The draw's subdomain, service-operations-sla, is kept: task128 moved to field-service-maintenance at its registration.

## Changes from the source note

1. Decisive rung redrawn. The note's decisive move, standardising each partial-exposure group to the base's CPU class through the device registry, is a one-hop schema-visible join (device model to benchmark band) followed by a composition check this solver runs by reflex; RC01 died on a schema-visible join (task121 round 1 and 2). It stays as the correction inside rung 2, which closes the joint ramp and leaves the ad stack in front. The new decisive rung conditions each change's cost on a per-view state built from the order of each device's views against the release train (first load after a deploy, or a cached reload), with the two changes costing opposite states.
2. The answer stays C, the framework, but rung 2 now names A on both the raw and the phone-standardised split, and every figure in the note's section 12 is retuned at stage 2 against the new targets above.
3. The ad-stack-only group: AMP landing views become the puzzles pages (outside the redesign, the wrapper switched on there on one date). AMP views are all search landings, so they are all first loads and could never show the ad stack's cached-load cost, and transporting them would rest on an untestable assumption; AMP is also a fading channel by 2026.
4. The twin pair P-06 and P-09 is dropped. A pair of closed cases separated only by audience composition is a reproduction check that tells the solver an audience moderator exists, which is the pilot's second lesson.
5. The calibration organ: the eleven randomised fix pilots (pilot_log) become the operations squad's roster of eleven closed fixes with realised savings (realised_outcome_roster), forced by ban.calibration against task122; its blindness now comes from every closed change having switched on site-wide on one date.
6. Domain, role, artifact, forum and forcing event redrawn as listed under Guard; the world moves from a national publisher to a Danish regional news group whose digital operations unit runs the platform for three titles under an internal service level. The prompt's one belief stays the note's: the group digital director is convinced it was the consent banner.
7. Ask C (each cause under each of the four rung constructions) is dropped: it names the ladder's rungs in the prompt. The criteria come from shape 11, the six cohorts' two effects and pre-switch gaps, which are the decisive construction's outputs by segment, so a wrong split fails every cohort at once. Asks A (the crawl's run index) and B (the image CDN's hit counter) stay as device-carried candidates for the supplemental-stumping pass.
8. Deliverables: the workbook and PNG become a service-review deck and a workbook (the cohort CSV was moved to xlsx at registration, see ## Guard).

# Stage 2: design (2026-10-10)

Everything below is the design the generator builds against. Every number is a target the generator asserts; where the ladder sketch above and this section differ, this section governs (the sketch is the draw's record). Scratch tuning lived in the scratchpad and is not kept.

## Gate G

- **Litmus.** No reported number or stakeholder conclusion is wrong. The crawl's byte figures, the close-out's monthly shares, every dated step, the cohort-aligned joint ramp and both separating groups' effects (each read on its own views) are correct, and nobody in the pack quotes a ranking of the five changes. The difficulty is that the two groups that separate the ad stack from the front end are not miniatures of the views each fix acts on, on a per-view state no column carries; catching a misleading read is not the move.
- **Primary mechanism:** `decomposition_attribution` (one joint effect apportioned between two changes that only shipped together), with `method_or_model_selection` supporting (which conditioning set transports a separating group's effect).
- **Flags:** `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`.
- **Deletion test.** Delete the crawl, the social layer, the close-out and the licensed basis: the beacons still show a cohort-staggered joint ramp, both separating groups still read the ad stack ahead once standardised on the registry's phone class, and nothing in the pack says a view's cost depends on whether it is its device's first load after a deploy.
- **Clean-data test, per suspect file** (asserted at stage 3): (1) the crawl, whose URL list was refreshed in June: repaired to matched URLs, rung 0 moves from B to E, the answer and the rung 3 read do not move; (2) the old collector's rows (duplicates and tablets, February to 8 May): repaired, the dated-change asks move, the answer, the rung 3 read and every main-call figure do not; (3) instrument repair on the beacon: a beacon that timed the framework's and the wrapper's main-thread work per view still leaves every redesigned ad-supported view carrying both in its joint state, so the split still needs the separating groups and their transport; the per-view state is a property of the device's history against the release train, not a measurement the beacon failed to take. `answer(repaired) == answer(shipped)`, `naive(repaired) == naive(shipped)`, `answer != naive`, per file.
- **Lens swap:** the rung 3 read carries each group's effect at that group's own state mix; the answer carries per-state effects to the ad-supported views' state mix. Different populations (the separating groups against the views each fix acts on), not one population under two lenses.
- **Pre-draw identity:** a fix's value is the sum over the views it acts on of its per-view effect. The identity closes over the joint ramp, which the pack supports, but the split needs per-state effects, which are neither filed nor forced by any visible residual (every split ties to the joint ramp on every cut once the phone mix is in).
- **Corpus direction:** under the naive path the closed-fix roster reproduces (every closed fix switched on for every view at once and was read on the views it acted on), so it certifies the field metric and never refutes the stop rung.

## Entity, unit of value, decision

Sønderå Medier's digital operations unit runs one web platform for three daily titles and is scored on mobile page views delivered inside the service line (largest contentful paint at or under 4.0 s). Two things both read as the size of a change: the weight it added to a crawled page (the ad-revenue committee's basis) and the field views its fix brings back under the line at the latest full month's traffic (the service level's basis). They rank the changes differently because lab weight counts bytes once per crawled page while the field cost of a change depends on the phone, on the state of the view and on how many views it acts on.

Decision: exactly one change from {A header-bidding ad stack, B image pipeline, C Bølge's client-side front end, D consent banner, E brand web fonts} for the operations squad's Q4 (opens 1 October), committed at the quarterly service review on 17 September. The figure is valued at August's traffic because the service-level document says a fix is valued at the latest full month's traffic: a filed convention, not a forecast, so the objective stays Root-Cause Analysis while the call faces forward (the change Q4 fixes).

**Answer: C, the front end, 1,309,100 mobile views a month (target; files as 1,310,000 at the nearest ten thousand), runner-up A at 721,100 (1.82x).** C ranks 4th on rung 0.

## Physical model and per-state targets

- One platform bundle per release train deploy (content-hashed; every deploy re-hashes it), shared by every Bølge template; the puzzles app has its own bundle, re-hashed at the same deploys. The release train departs about twice a week on irregular days, about 05:00 Copenhagen time.
- **State** (no column carries it): a view is a **first load** if its device has no earlier view since the latest deploy, otherwise a **cached load**. The physical reading: on a first load the critical path is the framework's download and compile with the wrapper's work overlapping the network wait; on a cached load the bundle is cheap and the wrapper's main-thread work and auction land on the path.
- Per-state effects in points of over-line share at phone multiplier 1: **front end 3.5 first / 1.5 cached; ad stack 0.9 first / 2.9 cached**, so the joint cost is 4.4 in either state (complete-partition invariance).
- Phone multipliers on every effect: low 1.45, mid 0.92, high 0.55 (registry benchmark band).
- Phone mixes (low/mid/high): ad-supported redesigned views (the base) 0.42/0.41/0.17 (multiplier 1.0797); subscribers' redesigned views 0.09/0.36/0.55 (0.7642); non-subscriber puzzles views 0.16/0.46/0.38 (0.8642).
- First-load share: both separating groups 0.15 in every phone class; the base 0.6945 overall, by cohort (August ad-supported views, millions): sektion 3.1 at 0.62, galleri 2.4 at 0.74, liveblog 2.9 at 0.47, lokal 14.6 at 0.79, sport 8.3 at 0.72, forside 6.7 at 0.57 (38.0 in all). Same phone mix in every cohort.
- August mobile views (phones only): base 38.0M, subscribers' redesigned 9.0M (split across the cohorts in proportion to the base, rounded by the generator), non-subscriber puzzles 4.5M, subscribers' puzzles 1.5M, 60M in all minus the puzzles and redesigned views of devices outside both groups (none: every Bølge template view is base or subscriber).
- Dated steps (uniform across groups, states and phones): E brand fonts 0.46 points on all 60M (276k), B image pipeline 0.68 points on the 54M views of templates with a hero image (367k), D consent banner 0.90 points on all 60M (540k).
- Timeline (2026): extract 1 February to 31 August; E 3 March; B 7 April; D 12 May; ad stack on the puzzles pages 16 June; Bølge cohorts switched on at the release-train deploys of 30 June, 7, 14, 21, 28 July and 4 August (sektion, galleri, liveblog, lokal, sport, forside), each switch-on carrying the ad stack on ad-supported views and the front end on every view of the cohort's templates. No secular trend in any group between steps; volume seasonality only.
- Device sampling 1 in 300 device keys; spine about 1,200,000 rows.

## Ladder (five rungs)

| Rung | Gap | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|---|
| 0 | objective | Crawl byte bridge on each month's full URL list, resources mapped to changes through the asset register, February crawl against August | **B, image pipeline** (+520 KB; E +300, A +210, C +140, D +60) | It is the ad-revenue committee's basis, filed as such, and cleanly decomposed by resource | The crawl's run configuration: the URL list was refreshed in June, and comparisons across crawls use the URLs present in both lists |
| 1 | objective (hygiene) | The same bridge on matched URLs | **E, brand fonts** (+300 KB; B +240, A +210, C +140, D +60) | The cleaning is right and the bridge now compares like with like | The service-level document: a fix is valued on field mobile views it brings back under the line, at the latest full month's traffic |
| 2 | time | Field event study: the over-line share's step at each dated change, in views a month; the Bølge ramp has no date and stays unattributed; the puzzles step is read on puzzles views | **D, consent banner** (540k; B 367k, E 276k, A 101k on puzzles only, C unplaced) | It moves to the scored metric, uses the dated releases, and every step reproduces | The Bølge rollout log: the ad stack and the front end switched on together, template group by template group over six weeks, a ramp no single date captures and larger than any dated step once aligned |
| 3 | population (composition) | Cohort-aligned joint ramp (4.751 points on the base, against not-yet-switched cohorts), split by the puzzles pages (ad stack alone, read on their own views) and subscribers' ad-free views of the redesigned templates (front end alone, through the subscription register). Read raw the split leaves a residual of 1.128 points against the joint ramp; standardised to the base's phone mix through the device registry it closes to the view | **A, ad stack** (1,167,900; C 862,300, D 540k) | Two clean natural experiments, a composition correction a reviewer expects, and the corrected split sums exactly to the joint ramp on every cut | The order of each device's views against the release train's deploys: the front end costs a view mostly on a first load and the ad stack mostly on a cached load, and both separating groups are 15 per cent first loads against the base's 69 per cent |
| 4 | population (decisive) | Each group's effect measured separately on first loads and cached loads within phone class (state built from each device's view order against the deploy timestamps), carried to the base's state and phone mix cohort by cohort; each fix counted on the views it acts on (the ad stack also on puzzles views at their own read, the front end also on subscribers' views at their own read) | **C, front end** (1,309,100; A 721,100, D 540k) | | none |

"A solver who does everything right up to rung 3 commits to the ad stack, 1,170,000 a month, with the front end 860,000 behind it."

**The stump** is rung 3, measured trap #13 with #11 behind it (see ## Decisive rung).

### Position table (asserted by name at every rung)

| Rung | Leader | C's rank | Leader over runner-up | C behind the leader |
|---|---|---|---|---|
| 0 | B | 4th of 5 | 1.73x (B over E) | 3.71x |
| 1 | E | 4th of 5 | 1.25x (E over B) | 2.14x |
| 2 | D | unplaced | 1.47x (D over B) | n/a |
| 3 | A | 2nd | 1.35x (A over C) | 1.35x |
| 4 | C | 1st | 1.82x (C over A) | |

C leads no intermediate rung and is 2nd on one (rung 3, by 1.35x, above the 1.20x floor). No leader margin anywhere is under 1.15x. At rung 3 C sits 1.60x above D; at rung 4 A sits 1.34x above D, so the runner-up named in the call is robust.

### Discriminator dominance

A carries 1.354x into rung 4 (1,167,900 against 862,300). The state reweighting multiplies C's figure by 1.518 and A's by 0.617, an edge of 2.459x against the required 1.2 x 1.354 = 1.625; net margin 1.82x. Worth on the graded quantity: rung 3 to rung 4 moves C by +51.8 per cent and A by -38.3 per cent. The rung 3 to rung 4 move needs no sign discipline (the call is a name and its figure, graded at a ten-thousand bin, and the nearest wrong cell is 15.7 per cent away, below).

### Correction grid and partial corrections (each asserted to name A, or to land C's figure at least 8 per cent from 1,309,100)

| Cell | A | C | Names | C's figure off by |
|---|---|---|---|---|
| Raw split, phone-blind, carried to the base | 955,300 | 646,800 | A (1.48x) | 50.6% |
| Phone-standardised (rung 3) | 1,167,900 | 862,300 | A (1.35x) | 34.1% |
| Standardised additionally on any visible column (referrer class, connection, navigation type, title, hour, weekday) | as rung 3 | as rung 3 | A | 34.1% |
| Landing proxy (first view of a 30-minute visit as the first load), within phone class | 1,117,000 | 913,000 | A (1.22x) | 30.3% |
| A device's first view in the extract window as the first load | about rung 3 | about rung 3 | A | about 34% |
| Recency bins (hours since the device's last view), nearest-bin extrapolation to the base's long gaps | 934,000 | 1,096,000 | C | 16.3% |
| State built, applied to the front end only | 1,167,900 | 1,309,100 | C (1.12x) | 0 (runner-up figure wrong) |
| State built without phone class (state reweighting only) | to be swept | to be swept | C | asserted at least 8% |
| Decisive (rung 4) | 721,100 | 1,309,100 | C (1.82x) | 0 |

Why every split ties (L8): within each phone class the two changes' joint cost is 4.4 x multiplier in either state and both separating groups carry the same first-load share, so any classification of views (the true state, the landing proxy, recency, any visible column, none) splits each phone class's joint ramp into two figures that sum to it; only the phone-blind raw split leaves the 1.128-point residual, and the registry's phone class closes it, which is what makes rung 3 feel finished. The recency route and the half-applied state reach the right name with a wrong figure or a wrong runner-up; they are the accepted discovery paths (a solver who asks whether every view pays the front end alike), and the figure separation is asserted.

### The seven survival properties (rung 4)

1. Written nowhere: no document says a view's cost depends on its cache state, that deploys invalidate a cache, how often either audience comes back, or that a group's mix should be checked on anything but its columns. The release train log lists deploys and bundle hashes as an operational record with no commentary.
2. No sweepable corpus nominates it: the closed-fix roster's every case switched on for every view at once and was read on the views it acted on, so raw and state-conditioned reads agree on every case (asserted case by case).
3. No arithmetic symptom: once the phone mix is in, every split ties to the joint ramp on every cut; counts, joins and control totals reconcile identically under rungs 3 and 4.
4. Not a per-row predicate: the state is a group-and-rank on the spine (each device's views ordered, then placed against an as-of join to the deploy timestamps), then an effect per phone class and state inside two groups, then a reweighting to a third population.
5. Enumeration is arithmetic: no column carries the state; it is constructed from view order and a second file's timestamps.
6. No cutover date: the ad stack and the front end ramp by cohort; the deploys are about fifty routine releases on irregular days, so no weekday pattern carries the state; the dated changes are decoys.
7. Survives deletion: with every voice, the crawl and the close-out gone, rung 3 still names A.

First moves played on paper: the one-period group-by (A and C cannot be separated), the event study (D), the separating groups (A raw and standardised), the corpus back-test (no case scores transport). None lands C.

## Organs

**Calibration corpus (realised_outcome_roster).** The operations squad's register of the eleven fixes it closed from 2023 to January 2026, each with the change it addressed, the templates, the go-live date, before and after over-line counts and views for the four weeks either side, and the realised saving in mobile views a month at the first full month after it landed. Certifies: a fix's value is the field views it brings back under the line at a full month's traffic (11 of 11 savings reproduce from the roster's own counts to the view); crawl bytes removed predict the saving's rank in 4 of 11 (refuses the lab basis in aggregate: rank correlation under 0.3, asserted). Blind, for a computable reason: every closed fix switched on for every view of its templates at once, so its effect was read on the very views it acted on, and no case carries a co-shipped pair or a separating group; asserted by recomputing each case under a state-blind and a state-conditioned read and getting the same saving. Resemblance points at the decoy: a 2024 ad-slot lazy-load fix on the puzzles pages removed 2.2 points there, beside the ad stack's puzzles read of 2.25. No twin pair (dropped at the draw: a pair separated by audience composition tells the solver a moderator exists). The roster's largest realised saving is the chart's reference line (target 640,000 a month, a 2024 image-compression fix, below both A and C on every rung so the line never ranks them).

**Filed pins (one statement each, one file each).**
- Service-level document (level 1): a view misses the line when its largest contentful paint exceeds 4.0 s; a view with no paint timing (a back-forward restore) is not scored; mobile means a phone in the device registry; a fix is valued on the mobile views it brings back under the line at the latest full month's traffic. It also records, as a matter of record, that the ad-revenue committee reviews performance work on page weight from the monthly synthetic crawl and will present that basis at the review (the licensed wrong basis).
- Paywall terms (level 2): signed-in subscribers are served the ad-free layout on every template.
- Device registry header (level 4): phone class comes from the model's benchmark band.
- Field guide to the beacon export (level 4): one row per sampled page view; sampled at 1 in 300 device keys, so a sampled device's views are all present; `pv_id` is the page-view key; times are UTC.
- Crawl run configuration (level 5): comparisons across crawls use the URLs present in both lists; one cold-cache run per URL (no repeat-view run, so the lab side never shows a cache contrast).

**Empirical pins.** The joint ramp from cohort alignment; each group's per-phone, per-state effect from its own views against its pre-switch weeks; additivity of A and C from the joint ramp (both splits sum to it).

**Social layer (beliefs, never rankings).** Ove Schmidt (group digital director): it was the consent banner, which arrived just before the numbers turned (the prompt's one belief). Finn Thygesen (front-end platform lead): the front end ran on subscriber pages before it went wide and never moved their numbers (true of subscribers' own views, which is the point). Caroline Mortensen (editorial product director): the crawl gets heavier every month and it is the pictures. Gunnar Paulsen (head of ad operations): performance work is reviewed on page weight, as the committee always has. No voice supports C.

**Distractors (named in metadata.json at stage 3, never in a file name).** (1) The desktop field summary by month and title (correct, desktop only, outside the service level's mobile scope). (2) The AMP landing-view report, February to August, monthly by title (AMP pages carry amp-ad slots, not the header-bidding wrapper, as its own header states, so it separates nothing). (3) The newsletter send log (subscriber sends by day), relevant-looking for subscribers' landings and unused. No shipped file ranks the five changes; the crawl ships at request grain.

## Pack plan (stage 3 builds against this)

Spine `rum_mobile_views_2026.parquet` (about 1.2M rows: pv_id, ts_utc, device_key, account_key, title, template, url_path, device_model, os, browser, effective_connection_type, navigation_type, referrer_class, ttfb_ms, lcp_ms, cls; no transfer size, no cache or build field). Then the release train log (csv: release id, deploy time with offset, platform bundle hash, puzzles bundle hash, release notes), the Bølge rollout log, the change register, the device registry, the subscription register, the edition register, the service-level document and the paywall terms (pdf), the Q3 service close-out (xlsx, monthly mobile views and over-line share by title, February to August), the crawl request log and its run configuration (csv and json), the asset register, the closed-fix roster (xlsx), the image CDN fill log and the vendor appendix, the field guide, the social thread, the provenance record, and the three distractors. About 22 files, 6 formats. Every file name in the organisation's own idiom, fixed at stage 3.

## Determinism: the 22 axes

| # | Axis | Reading chosen | Closure |
|---|---|---|---|
| 1 | Population | A acts on ad-supported views (Bølge base plus non-subscriber puzzles); C on every Bølge view (base plus subscribers') | Filed (paywall terms, service-level valuation clause) plus C4: C on the base only (1,185,100) still names C, and A with subscribers' puzzles added is unchanged (no wrapper there); each cell mapped to the clause it violates |
| 2 | Unit of account | the page view | Filed (service-level document, field guide grain line) |
| 3 | Attribution window | pre and post weeks per cohort and per group, from the switch-on deploy | C3: no trend between steps, so any window from one to six weeks returns the same per-cell effects (asserted at 1, 2, 3, 4, 5, 6 weeks) |
| 4 | As-of dating | subscription status at view time | C1: no main-population account changes status inside the main windows, so view-time and pull-time status select the same rows (asserted) |
| 5 | Version basis | one registry version, one release log | C1: single vintages shipped for the main path |
| 6 | Denominator | views with a paint timing | Filed (service-level clause) plus C4: counting back-forward restores as under the line scales every effect by the restore share (7.5 per cent target, stable in every group and window), so the wrong cell sits 7.5 per cent off |
| 7 | Weighting | each view counts once | C1: effects are constant inside each (group, phone, state) cell, so view-, device- and day-weighted cell means agree (asserted) |
| 8 | Window length | four weeks is the golden's | C3 as axis 3 |
| 9 | Boundary inclusivity | LCP strictly over 4,000 ms; a view is after a deploy if its time is after the deploy time | C1: no lcp_ms equals 4,000; no view of any device within ten minutes of a deploy (asserted) |
| 10 | Rounding path | per-cell effects unrounded, views summed unrounded, rounded once | C1: summing cohort figures rounded to the thousand lands in the same ten-thousand bin (asserted); headline 1,309,100 sits 4,100 above its lower edge, flip if C moved by 0.3 per cent |
| 11 | Tie-break | none needed | margins of at least 1.25x at every leader |
| 12 | Maturity | August complete | C1: beacons land within 48 hours and the extract is taken 5 September; no August row arrives late (asserted) |
| 13 | Order of operations | reweight inside phone class, then scale | C1: linear throughout |
| 14 | Row order | | C1: sort-invariant (asserted on two orders) |
| 15 | Duplicate resolution | `pv_id` unique on the main population | C1: the old collector's duplicates end 8 May, before every main window (zero-count asserted) |
| 16 | Identity normalisation | device_model to registry, exact | C1: every model in main rows resolves to exactly one phone class (asserted) |
| 17 | Netting | none (counts of views) | n/a, recorded |
| 18 | Dimensional units | lcp_ms in milliseconds | C1: one unit on every main row |
| 19 | Code semantics | navigation_type, referrer_class are context | C1: state decorrelated from every visible column inside each group, so standardising on any of them moves nothing (asserted per column) |
| 20 | Integerisation | views a month to the nearest thousand (asks) and ten thousand (headline) | C1 with mid-bin assertions |
| 21 | Scope of a clause | "latest full month's traffic" scales by August views | C1: sample times 300 equals the close-out's August mobile views by title exactly, so both scaling routes agree (asserted) |
| 22 | Forward window contents | Q4 is valued at August traffic by the filed convention | Filed; no projection enters |
| + | State definition | first view of the device since the latest deploy | C1: per-device and per-device-and-bundle readings classify every main-population row identically (puzzles devices are puzzles-only; subscribers' puzzles views always follow an article view in the same deploy interval; every Bølge template shares one bundle), asserted |
| + | Transport conditioning set | phone class and state | C4: every coarser set lands on A or on C at least 16 per cent off (grid above), each a set the within-group effects visibly reject |

## Ask sheet

Deliverables (fixed at the draw): `q4_squad_call.pptx` (the service-review slides: the call, the chart) and `q4_squad_call_cohort_effects.xlsx` (the workings). Every ask is a component of the case for or against a candidate (H18): the cohort grid decomposes the two co-shipped candidates' figures by the templates the squad would work through, the dated-change figures are the other three candidates' cases by title, the lab weights answer the ad-revenue committee's basis for every candidate, and the image figures are the image pipeline's own delivery record.

**Main call's declared row population** (asserted zero device rows and zero hazard rows inside it): beacon rows dated 12 May to 31 August (every group), the release train log, the registry rows of models seen in those rows, the subscription register rows of accounts seen in them, the Bølge rollout log, the change register's A and C lines, and the close-out's August column. Device rows live only in beacons dated before 12 May, the crawl, the asset register, the image CDN log, the vendor appendix and the edition register.

| Ask | Figures | Layer | Primary device | Hazards | Path (files) | Use |
|---|---|---|---|---|---|---|
| K, cohort grid | 6 Bølge template groups x 2 (views a month the ad stack's fix and the front end's fix each bring back there; the front end's includes subscribers' views of those templates) = 12 | construction (inherits rung 4) | none: main rows stay clean | none | spine, release log, registry, subscriptions, rollout log, close-out, service-level document, paywall terms | the squad's order of work through the templates; ties to the call (the 6 front-end figures sum to the headline, the 6 ad-stack figures plus puzzles to A's) |
| T, the other three candidates by title | D, B, E x 3 titles = 9, views a month to the thousand | device | T1, edition re-mastheading | H1 tablets, H2 collector duplicates, T4 local-edition tag gap | spine (Feb to early May), change register, release log, edition register, registry, field guide, service-level document, close-out | Ove's banner case and the image and font owners' cases, per title |
| L, lab weight by change and title | 5 changes x 3 titles = 15, kB to one decimal | device | L1, asset paths that lie about ownership | H3 URL list refresh, H4 crawl retries | crawl log, crawl configuration, asset register, change register, release log, field guide, service-level document (the committee basis), close-out (title list) | the ad-revenue committee's basis answered with the right bytes |
| I, image delivery by month | 6 months (March to August) x 2 (image requests and image kB per mobile page view, one decimal) = 12 | device | I1, one CDN row per cache fill, not per request | H5 crawler fetches, I2 fallback vendor in kilobytes | image CDN log, vendor appendix, crawl configuration (crawler agent), close-out (mobile views), registry (form factor), change register, field guide | the image pipeline's case: what phones actually downloaded month by month |

### Devices

- **T1, edition re-mastheading (primary, silent, a stored label taken before a silent switch).** On 16 March two local editions moved from the second title's masthead to the third's. The beacon's `title` is the masthead at view time; the close-out reports by current masthead. Totals are invariant; every row is valid. Per-title steps whose windows straddle 16 March (E: 3 to 30 March post; B: 10 March to 6 April pre) are confounded on titles 2 and 3 in opposite directions (target at least 9 per cent each). Organ pair: the edition register (effective-dated, structural) and the field guide's line that `title` is the masthead the page was published under (documentary). Correct handling: map each view to its current masthead through the register, or measure within edition; both converge (steps are uniform by edition, asserted). Over-correction stop: dropping the moved editions entirely leaves the step right and the August scale short (the close-out counts them), at least 8 per cent off on titles 2 and 3.
- **T4, local-edition tag gap.** The shared local-edition tag container stopped firing beacons on titles 2 and 3 local editions from 20 April to 8 May (lower over-line share than the title mean), so D's pre window is short of them and the naive per-title D step is deflated (target at least 10 per cent). Silent: nothing in the beacons; the close-out's April and May views by title are the referee that shows the shortfall. Correct handling: within-edition steps or the window restricted to days the editions report; both converge.
- **H1, tablets in the old collector's rows (cross-cutting over T).** Until 8 May the old collector forwarded tablet views into the export; the registry marks their models as tablets and the service level scores phones only. Tablets carry a smaller step (multiplier 0.4), so including them dilutes every T figure (target at least 5 per cent, direction down). Silent: tablet rows look like every other row; only the registry join, which the T path does not otherwise need, shows the form factor.
- **H2, collector duplicates (title 1).** From 16 March to 8 May the old collector double-forwarded title 1's app-webview beacons (higher over-line share) under fresh row ids with `pv_id` preserved. Visible to a key-uniqueness check, so a hazard; the field guide's key line adjudicates. Over-cleaning half: genuine repeat views of the same URL by the same device carry their own `pv_id` and must stay. Moves E t1 up, B t1 up slightly, D t1 down (each at least 4 per cent).
- **L1, asset paths (primary, silent).** The header-bidding wrapper's core library is served from the group's own static host under a first-party path, and the front end's vendor runtime from a public CDN. A host-based mapping moves 64 kB a page from A to C and 38 kB from C to A (naive A 184, C 166 against true 210 and 140 on the group average). Organ pair: the asset register (path prefix to owning change, structural) and the field guide's line that a request belongs to the change the asset register names (documentary). Two-directional, so "first party means ours" and "third party means ads" both lose.
- **H3, URL list refresh (visible).** The June refresh changes the crawled pages; the run configuration's matched-list rule adjudicates. Mixing lists moves every L figure (B most, target at least 10 per cent).
- **H4, crawl retries (visible).** URLs that timed out were re-run and both runs filed, the failed run with partial bytes; the configuration says the completed run is the run of record. Moves every L figure on the titles with retries.
- **I1, fill rows (primary, silent-grain).** The image CDN writes one row per cache fill per edge location with the fill's `served_count`; counting rows as requests understates requests about 26-fold and the bytes column is per fill, so bytes per view must be weighted by served count. Organ pair: the vendor appendix (row semantics) and the served-count column (structural).
- **I2, fallback vendor units.** For 9 June to 21 July the fallback vendor carried part of the traffic and logs `bytes_sent` in kilobytes by contract (vendor appendix). Moves June and July kB figures (at least 8 per cent).
- **H5, crawler fetches.** The synthetic crawl's own image fetches hit the production CDN on crawl days under the crawler's agent string (crawl configuration names it); they are not page views. Moves every month's two figures (at least 3 per cent; months with a crawl and a retry burst more).

### Hazard table and coverage

| Hazard | Asks moved | Figures |
|---|---|---|
| H1 tablets | T | all 9 |
| H2 duplicates | T | E t1, B t1, D t1 |
| H3 URL refresh | L | all 15 |
| H4 retries | L | all 15 on retried titles (target all 3) |
| H5 crawler fetches | I | all 12 |

Every T, L and I figure sits under at least two independent devices: T (T1 or T2 or T4, plus H1), L (L1 on A and C, plus H3 and H4 on all), I (I1 plus H5, plus I2 in June and July). The cross-ask hazards are thin because the three device asks run through different systems; the hazard layer is per ask and the main path carries none. Composed mishandlings per ask are swept at stage 3 and none may land inside the bin.

**Separation and the runner-up.** No device moves the call or its runner-up: every T device that moves D moves it down, and D's highest mishandled value is asserted under A's 721,100 by at least 1.15x; D stays the rung 2 leader under every single-device mishandling (D at least 1.10x over B).

### Pair arithmetic

Criteria (planning count): call 4 (C, its figure, A, A's figure); deck 6 (first slide carries the call; bar chart, one bar per change; largest first; C and A labelled with their figures; the roster's best closed fix as a line at its value; a title naming the change); workbook asks 48 (K 12, T 9, L 15, I 12); files 2. About 60 in all.

Planning weights 38 / 7 / 55: K is 12 of 48 ask criteria (13.75 points), the device asks 36 (41.25 points). `r` (recommendation credit surviving a wrong call) planned at 3: the call's criteria all turn on the decisive rung.

- One top response cracks the call, the other stops at rung 3, device leakage 0.12 each: cracker 38 + 7 + 13.75 + 4.95 = 63.7; mirror 3 + 7 + 0 + 4.95 = 15.0; pair 39.3 (under 40). At leakage 0.15 the pair is 40.6, so the device asks must hold both top responses to about an eighth of their weight.
- No top response cracks the call (the designed case): each about 15; pair about 15.
- `55 x (Lc + Ls) <= 28 - r`: Lc = 0.25 + 0.75 x 0.12 = 0.34, Ls = 0.09, 55 x 0.43 = 23.7 against 25. Reachability c from a landed call: 0.25 (the K grid only).

Lazy paths: T pooled on view-time titles with tablets and duplicates in; L by host with all URLs and all runs; I counting rows. Each lands on its stop 1, at least 8 per cent from the golden on every figure (asserted at stage 3 with the per-ask ladders generated from the golden's code). Referee: the Q3 service close-out (monthly mobile views and shares by title, byte-clean, never trapped).

## Realism debts

- Equal joint cost in both states (the ad stack's cached-load surplus equals the front end's first-load surplus inside every phone class) and equal first-load shares in the two separating groups (0.15): forced by complete-partition invariance, without which a split leaves a residual that invites the search. Mitigation: neither is visible without building the state; the physical reading (critical path filled by the download on a first load, by the wrapper on a cached one) is plausible.
- State decorrelated from referrer, connection, navigation type, hour and weekday inside each group: forced so that no visible standardisation moves the split. Mitigation: deploys on irregular days at a low-traffic hour; the base's infrequent readers arrive by every route.
- Puzzles devices are puzzles-only, and subscribers' puzzles views follow an article view in the same deploy interval: forced so per-device and per-bundle state readings converge. Mitigation: the puzzles audience comes through the puzzles app link.
- No secular trend between steps: forced by the window corridor. Mitigation: volume seasonality is kept; composition is stationary within each group.

## Stopping rule

One plain solver at stage 4. Any committed answer other than C sends the build to the judge. A landed C is hardened, three loops at most on this architecture, then the build is retired. Two consecutive exact solves by different routes retire it without a third loop.

## Prompt

Symptom-first opening (none in the current window), the role mid-paragraph, the call as one sentence at the seam, two files, a block rounding convention with pins on the derived figures, one belief (the group digital director's), nothing naming the line's metric, the valuation month, the populations or any input file. Written to `prompt.md`. voice-check (2026-10-10, window task117 to task130): 298 words, 22.9 words a sentence, context 26 per cent, longest paragraph 108, a short sentence present, 2 rounding tags, no because clause, no carrier flagged, no shared six-word run, no ECONOMY flag; opening move filed as other (symptom-first has no key). Gradability walk: the call (C, its figure to the ten thousand, the runner-up and its figure), the deck's six chart parts, K 12, T 9, L 15, I 12, each with unit and rounding covered (views a month to the thousand by the workbook's block line, kB and per-view figures to one decimal), 60 criteria by the arithmetic above. Nothing in it names the line's metric, the valuation month, a population rule or an input file; the one belief is Ove Schmidt's.

## Tried and rejected

- The note's CPU-class standardisation as the decisive rung (draw, 2026-10-10): the registry join is visible from the schema and standardising a natural-experiment group on a joined covariate is reflex for this solver, so it would be executed as routine; kept as rung 2's partial correction.
- Cache state as a cost on the framework alone, the ad stack insensitive (draw): the state correction would then move C without moving A, so the phone-standardised split leaves a residual against the joint ramp, an arithmetic symptom that invites the search; replaced by opposite state dependence with equal surpluses, so every split ties.
- The image pipeline riding the redesign as a third co-shipped change, its go-live a null step (draw): the image service's request log by template family lines up with the rollout log on one key, a schema-visible join, and separating it from the framework needs a hero-against-text contrast that rests on an untestable equal-effect assumption.
- A paint-race replay (the paint waits for the slower of the image and the main thread, so removing one path's delay helps only where that path binds) (draw): once seen it is a per-row predicate, and web-performance knowledge of the LCP sub-parts can supply it.
- Transporting each effect in milliseconds rather than in share points, for groups with different baselines near the 4.0 s line (draw): it is the replay this solver runs at the finest grain, so it would be its starting method.
- The image pipeline's cost varying with edge cache misses as the news cycle concentrates traffic (draw): the bridge from spring to August would carry a residual equal to the pipeline's growth, an arithmetic symptom.
- The consent banner's cost fading as consents accumulate (draw): RC01 v1's self-healing shape, and the fade shows in the weekly series.
- A commercial weather portal as the world (draw): its free users check daily too, so the ad-supported views would not be first-load heavy and the contrast the decisive rung needs would not exist.
- Keeping Product Analytics with pilot_log, monitoring_export, product_manager, shape 07 or 18, executive_team and vote_or_meeting (draw): each is BLOCK against task121 or task122 on the corpus as filed.
- Pattern D first, or pick_one_of_n (draw): test.same_puzzle_older and test.same_driver_older collide with five to seven older builds; E with root_cause_named is the honest reading of the decisive move and needs three differentiation lines.
- Keeping published_series and budget_or_appropriation at registration: blocked against task126 and task127, filed after this draw; redrawn to the Q3 service close-out (close_out_summary) and the review's meeting (vote_or_meeting).
- The source note's crawl ask on first-view and repeat-view runs (stage 2): a lab file with a repeat-view run shows the front end's bytes vanishing on a warm cache and the wrapper's staying, which narrates the decisive state on the lab side; the crawl ships one cold-cache run per URL and the lab ask moved to bytes by change and title.
- A per-cohort pre-switch gap as the grid's third figure, and the two separating groups' own reads as graded components (stage 2): the gap is zero by construction or a level both top responses file, and the group reads are identical at rungs 3 and 4, so each would hand the mirror response recommendation credit; the grid is two figures per cohort and the group reads stay unasked.
- Back-forward restores as a dated-change device on the banner's window (stage 2): the same filed rule governs the main rows, so it is not a separate device, and inflating the banner's step could lift D over A as the call's runner-up, a separation breach.
- A release tag on every beacon (stage 2): the state would be a one-key group-by of device and tag; the deploys ship only in the release train log, joined by time.
- Fixed release-train weekdays (stage 2): the state would surface as a weekday pattern in the daily players' and subscribers' effects; the train leaves on irregular days.
- A uniform 1 in 300 device sample for every audience (stage 3a, on paper): the separating groups' first-load, low-end cells hold about 380 sampled views a window while the base's matching cell is 11 million August views, so one sampled view moves the front end's figure by about 27,000 and no rounding bin at the ten thousand is forced; replaced by a sample_weight column (collector v1 1 in 300 for everyone to 7 May; collector v2 from 8 May, anonymous devices 1 in 600, signed-in devices and the puzzles app 1 in 50) and systematic over-line allocation per stratum.
- First-load share 0.15 in the separating groups with per-state effects 3.5/1.5 and 0.9/2.9 (stage 3a, on paper): at a usable sample the low-end first-load cells stay too thin to pin the figures; retuned to a first-load share of 0.25 with effects 4.0/1.0 (front end) and 0.4/3.4 (ad stack), which keeps the joint cost at 4.4 points in both states and holds rung 3 at A over C by 1.32x.
