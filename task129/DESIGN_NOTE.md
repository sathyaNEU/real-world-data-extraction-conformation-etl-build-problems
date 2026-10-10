# task129: which shipped change gets Sønderå Medier's Q4 operations squad, realising analytical_tasks note RC02 (analytical_tasks/06_root_cause/RC02_slow-views-partial-exposure-cpu-mix.md)

Stage 1 (draw), drawn 2026-10-10. This is the build's one design note; the design stage extends it. RC02 has never been built, so this is its first realisation.

## Draw

```
DRAW  (independent draws, checked with .claude/skills/fingerprint/guard.py)
  Card filed with guard.py register before the ladder was written? pending registration (the coordinator registers in task-number order)   Verdict: WARN
  Shape: 11 before and after with a control   Gate G mechanism: decomposition_attribution (method_or_model_selection supporting)
  Gap: population (decisive), objective, time   Pattern: E (decisive), D (the transport)
  Domain: business-operations-analytics   Subdomain (enumerated): service-operations-sla   Objective: root-cause
  Pairing repeated from last build? No. The last three on file are task119 (policy-education x anomaly-detection), task121 (product-analytics x root-cause)
    and task122 (product-analytics x experiment-causal); business-operations-analytics x root-cause was last drawn at task111
  Stakeholder role: head of digital operations at a regional news group, who owns the internal page-delivery service level and assigns the
    operations squad's quarter (operations_director)
  Context-artifact type: published_series, the monthly page-delivery service report to the three titles and ad sales (share of mobile views over
    the line by month and title, correct, ranking no change)
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
  Forcing event: budget_or_appropriation (the review allocates the operations squad's Q4, which opens on 1 October)   Organisation family: media_or_publishing
  Scoring unit: units served (mobile page views delivered inside the line)
  World: Denmark; DKK; Sønderå Medier (invented), a regional news group running three daily titles on one web platform, metered paywall with an
    ad-free subscriber layout; Bølge, the redesign programme (invented)
  People, drawn with guard.py names --geo Denmark --seed 129: Elin Lauritsen (head of digital operations, the requester), Ove Schmidt (group digital
    director, holds the consent-banner belief), Finn Thygesen (front-end platform lead, owns the new front end), Caroline Mortensen (editorial product
    director), Gunnar Paulsen (head of ad operations, presents the lab-weight basis), Gunhild Lund (data engineer, owns the view export), Mette Johansen
    (release manager, keeps the release train log), Simone Thorsen (performance engineer, keeps the closed-fix roster)
  Spine (planned): rum_mobile_views_2026.parquet, about 1,200,000 rows, one sampled mobile page view (a field timing beacon), grain page view, synthetic
  Deliverables (planned): q4_squad_call.pptx (the service-review slides: the call, the cohort chart), q4_squad_call_cohort_effects.csv (the cohort grid)
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

## Changes from the source note

1. Decisive rung redrawn. The note's decisive move, standardising each partial-exposure group to the base's CPU class through the device registry, is a one-hop schema-visible join (device model to benchmark band) followed by a composition check this solver runs by reflex; RC01 died on a schema-visible join (task121 round 1 and 2). It stays as the correction inside rung 2, which closes the joint ramp and leaves the ad stack in front. The new decisive rung conditions each change's cost on a per-view state built from the order of each device's views against the release train (first load after a deploy, or a cached reload), with the two changes costing opposite states.
2. The answer stays C, the framework, but rung 2 now names A on both the raw and the phone-standardised split, and every figure in the note's section 12 is retuned at stage 2 against the new targets above.
3. The ad-stack-only group: AMP landing views become the puzzles pages (outside the redesign, the wrapper switched on there on one date). AMP views are all search landings, so they are all first loads and could never show the ad stack's cached-load cost, and transporting them would rest on an untestable assumption; AMP is also a fading channel by 2026.
4. The twin pair P-06 and P-09 is dropped. A pair of closed cases separated only by audience composition is a reproduction check that tells the solver an audience moderator exists, which is the pilot's second lesson.
5. The calibration organ: the eleven randomised fix pilots (pilot_log) become the operations squad's roster of eleven closed fixes with realised savings (realised_outcome_roster), forced by ban.calibration against task122; its blindness now comes from every closed change having switched on site-wide on one date.
6. Domain, role, artifact, forum and forcing event redrawn as listed under Guard; the world moves from a national publisher to a Danish regional news group whose digital operations unit runs the platform for three titles under an internal service level. The prompt's one belief stays the note's: the group digital director is convinced it was the consent banner.
7. Ask C (each cause under each of the four rung constructions) is dropped: it names the ladder's rungs in the prompt. The criteria come from shape 11, the six cohorts' two effects and pre-switch gaps, which are the decisive construction's outputs by segment, so a wrong split fails every cohort at once. Asks A (the crawl's run index) and B (the image CDN's hit counter) stay as device-carried candidates for the supplemental-stumping pass.
8. Deliverables: the workbook and PNG become a service-review deck and the cohort CSV, a format pair the last twelve builds have not used.

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
