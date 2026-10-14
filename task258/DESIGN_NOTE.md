# task258 design note

## Draw

- **Card:** `cards/task258.json`, registered 2026-10-13. Product Analytics, task type
  metric-definition-measurement-science, objective Descriptive & Distribution Analysis; shape 14 (each property's
  page loads cut at 2,500 ms, now and after the playbook); decision pick_one_of_n; gap time then population (re-read
  at stage 3); pattern C; G8 then G16; Gate G method_or_model_selection; strategy population_selection (the loads one intervention can reach, built
  load by load from the parts of each load's paint).
- **World:** Brolga Media, a fictional Australian digital media group with six properties: Tideline (news), Matchday
  (sport), Hearth (home), Ledger (personal finance), Trailhead (travel) and Pantry (food). Its web platform team has
  one performance squad, sent each quarter by the squad's charter to the property where the squad's hero-image
  playbook will move the most page loads a month into the good Largest Contentful Paint band (2,500 ms or less), as
  the group's own RUM measures them on the latest complete month. The playbook moves a property's hero images to
  the group image CDN (AVIF, sized to the slot), preloads them at high priority and never lazy-loads them. The next
  engagement starts on 5 January 2027 and is fixed at the December planning (forcing event other: the quarter's
  assignment); the head of web platform assigns the squad (forum line_manager_or_team).
- **People** (guard.py names --geo Australia --seed 258; the first three drawn, Andrea Koch, Justin Fernandez and
  Christina Singleton, skipped for first names used in older builds): Margaret Good, head of web platform (role
  family product_manager); Tasha Murillo, performance squad lead; Doris Rhodes, site reliability lead who keeps the
  domains runbook, the CDN host list and the RUM extracts.
- **Data-native sentence:** every RUM beacon carries its own paint broken into time to first byte, the image's load
  delay and load time, and render delay, and the playbook moves a property's hero images to the group image CDN
  with a preload, so after it the image request waits on that CDN's connection rather than on the page finding the
  image: the delay settles at one level whatever it was before, rising on pages that already found their image
  early, which no ratio of before over after reproduces; and every beacon carries the page's first contentful
  paint, which a page held by the experimentation tool's anti-flicker snippet reaches only when the snippet times
  out, so the rebuilt paint meets a floor no faster image passes.
- **Guard:** PASS with WARNs. repeat.gate_g and overuse.gate_g (method_or_model_selection after task255 and task256):
  the decisive step is which model of the playbook's effect the past engagements bear out, the honest key; the
  strategy (population_selection) differs from task255's maturity_censoring and task256's composition_mix.
  repeat.decision (pick_one_of_n after task256): one squad, one property, the seed's decision by construction. The
  question leads with where (the squad is sent somewhere), not which, after task256.
- **Order:** drawn ahead of task257. DA07's world (a parcel carrier's van tiers by duty-cycle fuel economy) turns on
  the duty-cycle mix, composition_mix, which ban.strategy bars against task256 for any build drawn the same day with
  a lower number; task257 is drawn on a later day.
- **Pairing and shape:** the field's own analysis decides (how many page loads a month a change to two of the paint's
  four parts brings under the Core Web Vitals line, estimated from RUM attribution and the measured effect of past
  engagements), the objective is where a distribution sits against a cut, and each property's distribution is cut
  at 2,500 ms before and after (shape 14). Criteria: six properties with four graded figures each (page loads moved,
  egress in GB and AUD, live hero images), the call and its count, the chart's named parts, two files: 31 before
  the rubric's own splits.
- **Sources, one line each.** `guard.py mechanisms --strategy population_selection`: task25 and task28 (the share of
  a flagged excess one intervention can reach, behind a join) are this pattern's precedent, here the reach is built
  from each load's own parts and the playbook's effect, not a source attribute; task124 (a rate from units examined
  because they showed signs), task132 (a failed item restarts its wear curve) and task116 (a group offer) spend other
  selections. task129 (another lane: a publisher's slowdown split between two changes by first loads against cached
  reloads) shares the setting, not the move: it attributes a loss, this build counts the loads an intervention can
  move. `layer2-rigor-patterns.md` (metric-definition-measurement-science: metrics validated on known interventions,
  ratio of sums, mix shift) has no counterfactual over a metric's parts; the family is estimand identification (the
  right counterfactual, `two-layer-task-design.md`). The seed DA08 gave the world, the decision and the quantity; its
  own hint (fixes only moved loads whose paint element was the property's own image) stays a lower rung.
- **Forward facing:** the call sends the squad for the quarter from 5 January 2027, a window not yet open; the
  deciding quantity is counted on November 2026's page loads because the charter measures it on the latest complete
  month.
- **Loop 1 (the author's second layer, 2026-10-14, before any portal result):** each beacon now carries the page's
  first contentful paint (`fcp_ms`, beside the four parts in both extracts). A page on a section that waits on the
  group experimentation tool's anti-flicker snippet shows nothing until the snippet's timeout runs out, so it first
  paints about three seconds after its first byte, and the playbook leaves that where it is (charter 3.2: no work on
  scripts, fonts or the render path); a rebuilt paint comes no sooner than it. Pantry's recipes, dinner, quick-meals
  and healthy pages, Tideline's news and politics pages and one section each at Matchday (tennis), Hearth (interiors)
  and Trailhead (deals) wait on it, as did two of the squad's engaged sites (Brolga Kids, E06; Fairway, E10), whose
  after-window paint landed on the first paint. Loop 0's level stays a required step and is no longer the last: with
  it and the render delay held Pantry still leads (6.8 million, rung R4); floored at each load's own first paint,
  Matchday leads (4.6 million, 1.40x Ledger). Matchday's own-image share (0.31), hero delays (1,300 ms median) and
  other loads (1,800 ms median) and Pantry's traffic (10.2 million loads a month) were retuned so the ladder's
  positions hold (Tried and rejected). The card keeps its identity (gap time then population, pattern C, Gate G
  method_or_model_selection, strategy population_selection: the loads the playbook can move, now also those whose
  first paint leaves room under the line); its loop 0 driver is in lineage, differentiated.

## Default path

The pipeline a competent analyst builds from the prompt's words and the files' grain; figures from the built pack
(millions of page loads a month).

1. Read the question: the property the squad goes to for the quarter from 5 January 2027, and the page loads a month
   the hero-image playbook would move into the good LCP band (2,500 ms or less), on the group's own RUM for
   November 2026 as the charter counts it.
2. Load rum_lcp_beacons_2026-11.csv, keep November in Sydney time, one row per beacon_id, the navigations that report
   LCP, each weighted by 1 / the sampling rate in force for its origin when its page load started.
3. Keep each property's loads slower than 2,500 ms whose LCP element is an image the property serves itself (its
   image host, its legacy alias, its path on the group image CDN): Hearth 20.4, Ledger 13.5, Matchday 10.0, Tideline
   8.2, Pantry 6.9, Trailhead 5.3.
4. Measure the playbook on the squad's eleven past engagements: on the engaged pages the image's load delay fell from
   a median of 642 ms to 240 ms (ratio 0.37) and its load time from 789 ms to 378 ms (0.48); time to first byte held;
   the whole paint fell from 3,258 ms to 2,283 ms (0.70).
5. Carry the engagements onto each slow own-image load part by part: time to first byte and render delay as they
   are (charter 3.2: the squad does no work on the render path), the load delay and the load time cut by their
   ratios; count the loads that come in at 2,500 ms or less.
6. Rank the properties: Ledger 7.4, Pantry 3.8, Hearth 3.8, Tideline 3.4, Matchday 3.2, Trailhead 1.7.

Ends on: Ledger, 7.4 million page loads a month into the good band
Golden: Matchday, 4.6 million page loads a month into the good band

## Stump sentence

A competent analyst carries the squad's past engagements onto each slow own-image page load as ratios, the image's
load delay and load time each cut by the after-over-before ratio of medians and the rest of the paint held, and
files Ledger, 7.4 million page loads a month into the good band; two steps land it there. The delay does not shrink
in proportion: on every engagement it settled at one level, 240 ms, the connection to the group image CDN, rising
where a site's images were already found early, which takes Ledger to 3.3 million and puts Pantry, whose hero images
wait longest to start, first at 6.8 million. And the paint cannot come before the page's own first contentful
paint, which the playbook leaves where it is: most of Pantry's slow loads sit on pages that first paint about three
seconds after their first byte, so it moves 2.9 million, and Matchday, most of whose pages first paint soon after
their first byte, leads at 4.6 million.

## Three rules

- Task type: metric-definition-measurement-science (Product Analytics): a counterfactual on a measured web metric,
  Largest Contentful Paint, built load by load from its RUM attribution parts and the page's first contentful paint.
- Domain test: the deciding quantity is the page loads a month a hero-image playbook brings under the 2,500 ms LCP
  line, which web performance engineers estimate from RUM attribution by moving each part of the paint the way the
  change moves it and keeping what it leaves alone: a preload ends the wait to discover the image, but an image moved
  to another origin still waits for a connection to that origin, so the delay falls to the connection time, neither
  by a percentage nor to nothing; and the largest paint can never come before the page's first paint, so on a page
  its scripts hold back from painting a faster image only waits longer in render delay.
- Swap: "where a hospital sends its patient-flow team, the clinic whose fast-track brings the most visits under four
  hours" loses what decides here: there is no paint split into four parts, no preload that ends a discovery wait, no
  new origin whose connection leaves a floor under the delay and no first paint a page cannot beat, so neither the
  level the past engagements show nor the floor under each paint stands for anything and the property ranking cannot
  be built.
- Layer 1: RUM sampling rates set per origin in an effective-dated configuration and changed mid-month for two
  properties (the RUM collector's quota reviews); the extract cut on whole UTC days around a Sydney-time month (the
  RUM warehouse partitions by UTC day); beacons the collector received twice (a page sends again on unload);
  navigation types (back-forward cache restores that report no LCP, prerendered loads timed from activation, both
  from the web-vitals library); image hosts of three kinds per property (its own, a legacy alias the old media
  server still answers, its path on the group image CDN) beside agency, advertising and video hosts; the review
  extract's windows set in the change log by Sydney date; CrUX rows by origin and form factor beside the group's own
  RUM; analytics page views at another grain; and, on the ask paths only, the image hosts' hourly rollups in UTC with
  every slot size and revalidations on the same hosts, the legacy aliases logged by the old media server on its own
  clock, a DAM export with three renditions an asset, library records kept beside migrated assets, retired assets,
  and each asset filed under the property it was uploaded for.
- Layer 2: estimand identification, the counterfactual paint: each slow own-image load is carried through the
  playbook part by part, with the image's load delay set at the level the past engagements' delays settled at (the
  CDN connection) rather than cut in proportion or removed, and the paint taken no sooner than the load's own first
  contentful paint, which the playbook does not move, rather than with the render delay held as it was.
- Decisive step: building each load's paint after the playbook the way the engagements' own loads show it lands:
  the delay at the connection level, and the paint floored at the page's own first contentful paint, which on the
  pages that wait on the group experimentation tool's anti-flicker snippet sits about three seconds after the first
  byte, so there the render delay grows by whatever the faster image saves.
- Not semantics: reading every field, host, sampling rate and the first contentful paint correctly and keeping
  exactly the right loads still leaves open how the playbook moves the paint; the ratio of medians, the zero-delay
  rule and the render delay held are each read from correctly understood data, and no field, code or definition says
  where the delay settles or that a rebuilt paint has a floor.
- Not rule application: the charter files what is counted and the work the squad does not do, and the change log
  what the playbook does; no rule or procedure says how a past engagement's effect carries to a new property or that
  the paint meets a floor, so executing every filed sentence still leaves the model of the paint open, and only the
  engagements' own loads settle it (every after-delay at one level; the render delay held on nine engagements and
  rising more than threefold on the two whose pages first paint late, their after-window paint landing on that first
  paint).
- Analyst test: a strong analyst who weights the beacons to page loads, keeps the slow own-image loads, splits each
  paint into its parts and applies the engagements' after-over-before ratios files Ledger, 7.4 million page loads a
  month into the good band; one who applies the preload rule of thumb files Ledger too, at 8.4 million; one who sets
  the delay at the engagements' level but holds the render delay files Pantry, 6.8 million; all three miss Matchday.
- Estimand: the squad charter (`performance_squad_charter_2026.pdf`, 2.1 to 2.4): the property where the playbook
  will move the most page loads a month into the good LCP band (2,500 ms or less), counted on the group's RUM for the
  latest complete calendar month in Sydney time, a page load being a navigation that reports LCP, a load moved being
  one slower than 2,500 ms in that month that would have been 2,500 ms or less with the playbook in place, the
  playbook reaching the loads whose LCP element is the property's own hero image.
- No decoy: nothing is planted: no memo, briefing or stakeholder figure argues for a property; CrUX is the public view
  and the charter names the group's own RUM; the change log records what each engagement did and no result figure;
  the pages that first paint late are the experimentation tool's own behaviour on the sections it runs on, named in no
  file and visible only in the beacons; charter 3.2 states the squad's scope truly and is cited by the golden.
- No certified replay: no file states any engagement's or property's LCP after the playbook, so no model is chosen by
  reproducing a certified figure; the engagements' beacons are raw evidence.
- Lesson: a change that removes a wait does not shrink it in proportion, and it cannot carry a result past a gate it
  leaves alone: when the fix moves the resource to a new route the wait settles at that route's floor, and when the
  page itself is held from painting the faster resource only waits longer, so the counterfactual is built part by
  part from how past changes actually landed, with what the change does not touch kept as a floor.

## Readability screen

| Rung | 1 filed sentence | 2 schema | 3 reflex | 4 control bench | 5 hygiene battery | 6 linear arithmetic | Verdict |
|---|---|---|---|---|---|---|---|
| R0 every slow load the property has (CrUX or RUM), Tideline | the charter counts loads moved into the good band | the LCP column | yes | none | clean | a count | readable |
| R1 every slow own-image load, as if the playbook moved them all, Hearth | charter 2.4: the playbook reaches the property's own hero images | element and host columns | yes | none | clean | a filtered count | readable |
| R2 the engagements' ratios of medians, part by part or on the whole paint, Ledger | no | the parts are columns | yes: a measured effect carried as a ratio | none: no engagement result is filed | clean | one ratio per part | readable |
| R3 the preload rule of thumb, the delay to nothing, Ledger | no | no | yes for a web performance reader | none | clean | a part zeroed | readable |
| R4 the delay at the level the engagements settled at (the CDN connection), the render delay held, Pantry | the change log says what the playbook does and names no delay, level, connection or effect | no column carries an after-delay or a level; the engagements' loads must be compared before and after, part by part, engagement by engagement | not a reflex: the reflexes scale or zero the delay | no control scores a model; no engagement's result is filed | clean | no: a level read from the engagements' loads, then every slow load rebuilt and recounted | silent |
| R5 (decisive) each rebuilt paint floored at the load's own first contentful paint, Matchday | charter 3.2 says the squad does no work on scripts, fonts or the render path, which a reader takes as the render delay held; no file names a first paint, a floor, the experimentation tool or a held page | `fcp_ms` sits beside the four parts, which add up to `lcp_ms` without it; no column marks a held page, a floor or a paint after the playbook | not a reflex: the reflexes hold the render delay, as charter 3.2 reads, or scale it by the engagements' pooled ratio (1.19) | no control scores a model; the two engagements whose pages first paint late show their after-window paint on that first paint only to a reader comparing the parts before and after, engagement by engagement | clean: every load's paint at or after its first paint | no: each load's rebuilt paint floored at its own first paint, then every slow load recounted | silent |

## Semantic fork table

| Id | Term or convention in the main ask or the main computation | Golden reading | Alternative reading | Call under the alternative | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "page load" | a navigation that reports LCP, prerendered loads timed from activation included | every beacon row, back-forward cache restores and prerendered loads in or out | Matchday | same call and the same rounded counts: restores carry no LCP and no prerendered load is slower than 2,500 ms (asserted) |
| SF2 | "a month" | November 2026 in Sydney time | November in UTC | Matchday | same call (asserted); charter 2.2 counts the latest complete calendar month in Sydney time |
| SF3 | "the good LCP band" | 2,500 ms or less | under 2,500 ms | Matchday | same call and the same rounded counts (asserted); charter 2.3 |
| SF4 | page loads a month | each beacon weighted by the sampling rate in force for its origin when its page load started | one rate per property (the month's first or last); no weights | Matchday under one rate; never Matchday on a wrong rung without weights | same call under one rate (asserted); the field notes: a beacon stands for 1 / the rate in force when its page load started |
| SF5 | a load "moved into" the band | slower than 2,500 ms now and at or under it after | net of loads the playbook pushes out | Matchday | same call and the same rounded counts: only Ledger loses loads, 26,300 a month (asserted); charter 2.3 defines a load moved |
| SF6 | an image the property "serves itself" | its image host, the legacy alias still answering, its path on the group image CDN | its image host only | Matchday | same call (asserted); charter 2.4 and the domains runbook name the alias and the CDN paths |
| SF7 | which loads the playbook reaches | loads whose LCP element is the property's own image | every slow load | Tideline (R0) | charter 2.4: the playbook works on the property's own hero images |
| SF8 | the level the delay settles at | the median after-window delay on the engagements' pages | the mean, the median or mean of each engagement's median, the median by device, the whole after-delay distribution | Matchday, every count the same to 100,000 (asserted) | C1 |
| SF9 | the load time's change | the engagements' ratio of medians, after over before | the mean or median of each engagement's ratio, the ratio of means, the ratio by device | Matchday, every count the same to 100,000 (asserted) | C1 |
| SF10 | parts the playbook leaves alone | time to first byte and the page's first contentful paint as they are | the render delay held as it is | Pantry (R4) | charter 3.2 (no work on time to first byte, scripts, fonts or the render path); on every engagement time to first byte and the first paint held within 5 per cent, and the render delay rose more than threefold on the two whose pages first paint late (asserted, SF15) |
| SF11 | device | every device | phones only, as CrUX's headline | another count | charter 2.2 counts every page load |
| SF12 | "the property" | the property's www origin and every page under it | the brand's apps and AMP pages too | Matchday | same call: the November extract carries the six www origins only (asserted) |
| SF13 | an engagement's review windows | the change log's windows by Sydney date | by UTC date; split at the ship date | Matchday, every count the same to 100,000 (asserted) | C1 |
| SF14 | a beacon received twice | one row per beacon_id | every row | Matchday, every count the same to 100,000 (asserted) | C1; the field notes: a sampled page load sends one beacon |
| SF15 | the paint after the playbook | the rebuilt image paint, never before the load's own first contentful paint | the render delay held (R4); the render delay scaled by the engagements' pooled ratio, 1.19; the floor only where a load's LCP equals its first paint | Pantry under each | the engagements' own loads: each before window rebuilt with the floor lands within 5 per cent of its after window's median paint, while held it misses the two late-painting sites by over 25 per cent and the partial floor misses them too; no load in either extract paints before its first paint (asserted) |
| SF16 | where the paint's own work sits against the first paint | the floor taken once on the rebuilt paint (the later of the rebuilt image paint and the first paint) | the work counted after the later of the image's arrival and the first paint | Matchday, every count the same to 100,000 | same call and the same rounded counts: a held page first paints at least 3,060 ms after its first byte, every other page within 230 ms, before any rebuilt image arrives (asserted) |

## Ladder

Figures from the built pack (millions of page loads a month), asserted in `generator/checks.py`.

| Rung | Construction | Winner (count) | Runner-up (margin) | Matchday (rank) | Killed by (one fact) |
|---|---|---|---|---|---|
| R0 | every slow load, as if the squad could move them | Tideline 36.6 | Hearth 1.58x | 18.2 (4th) | charter 2.4: the playbook reaches only the property's own hero images |
| R1 | every slow own-image load | Hearth 20.4 | Ledger 1.51x | 10.0 (3rd) | Hearth's paint is held by time to first byte, which the playbook leaves alone |
| R2 (default path) | the engagements' ratios of medians part by part (delay 0.37, load time 0.48), the render delay held | Ledger 7.4 | Pantry 1.93x | 3.2 (5th) | the engagements' after-delays sit at one level whatever the before-delay was |
| R2w | the whole paint at the engagements' ratio, 0.70 | Ledger 13.1 | Hearth 2.06x | 2.7 (4th) | the parts move differently; time to first byte does not move |
| R2s | the delay cut by the engagements' pooled fall, 402 ms | Ledger 8.4 | Hearth 2.00x | 1.7 (4th) | the delay is no fixed cut either: it ends at 240 ms from any start |
| R3 | the preload rule of thumb, no delay, load time at 0.48 | Ledger 8.4 | Pantry 1.23x | 6.5 (3rd) | the engagements' after-delays are 240 ms, not nothing (the CDN connection) |
| R4 | the delay at the engagements' level (240 ms), load time at 0.48, time to first byte and render delay as they are | Pantry 6.8 | Matchday 1.27x | 5.3 (2nd) | on the two engaged sites whose pages first paint late the render delay rose more than threefold and the paint landed on the first paint: no paint comes before it |
| R5 (decisive) | R4 with each rebuilt paint floored at the load's own first contentful paint | Matchday 4.6 | Ledger 1.40x | 1st | |

- **Variants and the grid:** the render delay scaled by the engagements' pooled ratio (1.19) files Pantry (6.7); the
  floor applied only where a load's LCP equals its first paint files Pantry (6.1); the floor on the ratio, the zero
  delay or the fixed cut files Ledger (7.4, 8.4, 8.4); dropping the loads whose first paint is past 2,500 ms and
  holding the render delay elsewhere gives the golden's counts (the floor said another way). Every cell but the
  golden's is a named wrong answer (asserted).
- **Why each rung is a place to stop:** R0 is the CrUX dashboard every web team reads; R1 is the reach a squad lead
  reasons from; R2 is how engagement results are reported and carried (a percentage per part); R3 is the textbook
  effect of a preload; R4 is the part-by-part rebuild a web performance engineer makes from the engagements, with
  the render delay held because the squad does no work on the render path.
- **Position:** Matchday 4th on every slow load, 5th on the default path, 3rd on R1 and R3, 4th on R2w and R2s, 2nd
  only on R4 (Pantry 1.27x ahead), never 1st on an intermediate rung (asserted).
- **Sign and worth:** each rung changes the winner. The level takes Ledger from 7.4 or 8.4 million to 3.3 and Pantry
  from 3.8 to 6.8; the floor takes Pantry from 6.8 to 2.9, Matchday from 5.3 to 4.6, Tideline from 3.7 to 3.1 and
  Trailhead from 1.9 to 1.8, and leaves Ledger (no held pages) and Hearth (whose held pages its time to first byte
  keeps slow either way) where they were. Pantry's count under the floor barely depends on the level (its held pages
  stay slow whatever the image does, its other loads fall far below the line); Ledger's depends on it entirely,
  which is why every estimator of the level and the ratio is asserted to give the same rounded counts.
- **Mirror:** the held rung shares only Hearth's and Ledger's rounded counts with the golden; no other rung shares
  any (asserted).
- **Weights:** with no sampling weights at all, no wrong rung or grid cell lands on Matchday (asserted), so a solver
  who skips the weights does not reach the call by accident.

## Closure table

| # | Axis | Reading chosen | Closure move |
|---|---|---|---|
| 1 | Population | navigations reporting LCP on the six www origins in November 2026, Sydney time | pinned (charter 2.2); C1 (SF1, SF12) |
| 2 | Unit of account | one page load | pinned (charter 2.2); weights from the sampling configuration |
| 3 | Attribution window | November 2026, Sydney time | pinned (charter 2.2); same call in UTC (SF2) |
| 4 | As-of dating | the latest complete month at the December planning | pinned (charter 5.1) |
| 5 | Version basis | the change log's playbook as filed (version 3) | C1: one playbook definition ships |
| 6 | Denominator | none: a count of loads moved | C1 |
| 7 | Weighting | 1 / the sampling rate in force when the page load started | pinned (field notes); same call under one rate (SF4) |
| 8 | Window length | the engagements' four weeks before and after | pinned (change log); C1 across clocks (SF13) |
| 9 | Boundary inclusivity | 2,500 ms or less is good | pinned (charter 2.3); C1 (SF3) |
| 10 | Rounding path | unrounded counts, rounded once to 100,000 | C1: every count at least 25,000 loads from an edge under every estimator (asserted) |
| 11 | Tie-break | none needed | C1: the golden's margin 1.40x |
| 12 | Maturity and censoring | loads that report LCP | C1 (SF1) |
| 13 | Order of operations | dedupe, cut the month, weight, filter, rebuild the paint, floor it at the first paint, count | C1 (SF14, SF16) |
| 14 | Row order | not order-dependent | C1 |
| 15 | Duplicate resolution | one beacon per beacon_id | C1 (SF14) |
| 16 | Identity normalisation | image hosts to properties through the host list and the runbook | pinned (charter 2.4); C1 (SF6) |
| 17 | Netting against gross | gross loads moved into the band | pinned (charter 2.3); C1 (SF5) |
| 18 | Dimensional units | milliseconds, page loads a month | C1: one unit per column |
| 19 | Code and status semantics | LCP element and navigation type codes from the field notes | pinned (field notes); never the stump |
| 20 | Integerisation | none | C1 |
| 21 | Scope of a stated clause | "the playbook" is the four steps the change log files; the squad does no work on time to first byte, scripts, fonts or the render path | pinned (charter 3.1, 3.2) |
| 22 | Forward window contents | the quarter from 5 January 2027, sized on November's loads | pinned (charter 2.2, 5.1) |

## Literal reader

Filed estimand, from the prompt and the charter: for each of the six properties, the page loads a month (November
2026, Sydney time, each beacon weighted by the sampling rate in force when its page load started) that report LCP
slower than 2,500 ms and whose LCP element is an image the property serves itself, and that would report 2,500 ms or
less once the playbook (hero images moved to the group image CDN as AVIF at the slot size, preloaded at high
priority, never lazy-loaded; no work on time to first byte, scripts, fonts or the render path) is in; the squad goes
to the property with the most. Criterion: none filed; the design forces the method (determinism-check §1, form 1):
the change log says what the playbook does and the engagements' beacons record each engaged page's four parts and
first contentful paint before and after, so how each part moves is read from them: time to first byte and the first
paint unchanged (every engagement within 5 per cent), the load time in proportion (every engagement's ratio between
0.45 and 0.51), the load delay at one level whatever it began at (every engagement's after-window median between 232
and 247 ms, from before-window medians of 129 to 2,991 ms), and the render delay held where the pages first paint
soon after their first byte and grown where they first paint about three seconds after it (E06 and E10, whose
after-window paint lands on the first paint; each before window rebuilt with the floor lands within 5 per cent of its
after window). Every literal reading of the prompt's and the charter's terms lands on Matchday once the delay is set
at that level and each paint floored at its own first paint (the fork table, SF1 to SF16), and every estimator of
the level and the ratio, and both placements of the floor, give the same rounded counts; the easy answers come only
from easier models of the same counterfactual (a ratio, a fixed cut, nothing, or the render delay held), never from
another reading.

## Oracles

- CrUX rows by origin and form factor: each origin's share of good, needs-improvement and poor loads and its 75th
  percentile; no figure about the playbook, ties nothing on either path, declared a distractor.
- Analytics page views: another grain (views, virtual views included, not navigations reporting LCP); ties nothing,
  declared a distractor.
- The change log: what each engagement did and when; no result figure, so no model is confirmed by it.
- The engagements' beacons: evidence, not a control; they confirm the level and the floor only to a reader who
  compares each part before and after, engagement by engagement (the after-delay at one level everywhere; the render
  delay rising only on the two sites whose pages first paint late).
- Nothing ties only under the golden for the main call.

## Layer 1 inventory

| Item | System that writes it | File | Natural mishandling | Outcome (asserted) |
|---|---|---|---|---|
| Mid-month sampling changes (Tideline from 0.0005 to 0.0006 on 9 November, Ledger from 0.0010 to 0.0006 on 16 November) | the RUM collector's configuration | rum_sampling_config.csv | one rate a property | the same call; counts move |
| Sampling weights at all | the collector | rum_sampling_config.csv | no weights | no wrong rung lands on Matchday |
| Whole UTC days around the Sydney month | the RUM warehouse's day partitions | rum_lcp_beacons_2026-11.csv | November in UTC | the same call |
| Beacons received twice | the collector (a page sends again on unload) | rum_lcp_beacons_2026-11.csv | kept | the same rounded counts |
| Back-forward restores and prerendered loads | the web-vitals library | rum_lcp_beacons_2026-11.csv | prerendered loads dropped | the same rounded counts |
| Legacy aliases and CDN paths | the domains and the old media server | cdn_host_list.csv, domains_runbook.md | own image host only | the same call; counts move |
| Review windows by Sydney date across daylight-saving changes | the change log | squad_change_log_2024-2026.xlsx | windows on UTC dates, or a split at the ship date | the same rounded counts |
| CrUX and analytics beside the RUM | the public dataset, the analytics suite | the two distractors | read for the call | never read by the golden |

## Ask sheet

| Ask | Figures | H18 home | Use | Primary device | Hazards | Path (files, columns) | Stops (lazy delta) | Realism |
|---|---|---|---|---|---|---|---|---|
| A, the hero-image egress the group image CDN would serve each month for each property once its hero images move, in gigabytes and in Australian dollars | 12 | a measure every candidate carries that the call does not turn on (the move's running cost, charter 5.2) | the head of web platform carries the CDN bill for the quarter beside the loads moved | D4: the legacy aliases' requests are answered by the old media server and appear only in its own hourly rollup, on its own clock (Sydney time), never in the image hosts' log | D5 (every slot size on the same hosts and CDN paths; only the hero slot's directory moves); D3 (revalidations answered 304 carry no image); D8 (the image hosts' hours in UTC against the Sydney month) | image_host_logs_2026-11.csv (hour_utc, host, path_prefix, status, requests), legacy_media_server_log_2026-11.csv (log_hour, vhost, uri_dir, code, hits), squad_avif_size_table.xlsx (property, slot, width, height, mean AVIF bytes), image_cdn_contract_schedule_2026.pdf (AUD per GB, the GB), cdn_host_list.csv (hosts); 5 files, 16 columns | every slot: Tideline 23,594 GB; 304s kept: Tideline 2,593 GB; no legacy log: Hearth 1,808 and Trailhead 607 GB; UTC month: five properties off by 1 to 2 GB; the answer: Tideline 1,971, Hearth 2,102, Trailhead 667 GB | an image server's hourly rollup that does not separate page slots; a retired host whose requests stayed on the old server and its log |
| B, how many live hero images each property has that the squad would convert to AVIF | 6 | the squad's workload in the quarter, a measure every candidate carries | the squad lead sizes the conversion work beside the loads moved | D2: the DAM files each asset under the property it was uploaded for; three sections moved in March 2025 with their pages and images (Hearth's real-estate to Ledger, Tideline's travel to Trailhead, Matchday's game-day food to Pantry), so their heroes are the receiving property's own today, known only from the page that last carried each asset | D1 (the 2025 move into the DAM kept each older asset's library record beside its DAM record, linked only by the DAM record's legacy_id; distinct assets sharing a camera file name, pixel size and upload time punish a content dedupe); D6 (three renditions, a row each); D5 (assets retired from their pages, known by a last use before October) | dam_image_export_2026-11.csv (asset_id, legacy_id, property, rendition, file_name, width_px, height_px, uploaded_utc, last_used_on, last_used_page), cdn_host_list.csv (page origins), domains_runbook.md (the 2025 moves), performance_squad_charter_2026.pdf (2.4); 4 files, 12 columns | rows: Tideline 23,763; distinct ids: 7,921; content dedupe: 6,203; no crawl filter: 7,455; the property column: Tideline 6,709, Ledger 1,759, Pantry 3,055; the answer: Tideline 6,362, Ledger 2,044, Pantry 3,543 | a DAM migration that keeps old ids live for links that still point at them; a site restructure the asset register never followed |
| C, each property's page loads a month the playbook would move into the good band, and the chart | 6 and the chart's parts | the construction | the call's own table | none | none | the golden model | R1 to R5 values | the charter's own measure |

- **Main population zero-counts:** no row of the image host logs, the legacy server's log, the AVIF size table, the
  CDN contract or the DAM export is read by the call; the beacons, the sampling configuration, the change log, the
  engagements' beacons, the charter, the runbook and the CDN host list carry no ask device (asserted: the call's
  documents name no status code, rendition, legacy_id or log); deleting every ask file leaves the call and every Ask C
  figure unchanged.
- **Hazard table:** D4 (A) moves Hearth's and Trailhead's gigabytes and dollars; D5 moves every property's by an
  order of magnitude; D3 moves every property's by its revalidation share (11 to 27 per cent); D8 moves five
  properties by 1 to 2 GB; D2 (B) moves all six properties' counts (the donor up, the receiver down); D1 moves every
  count by its migrated assets; D6 triples every count; D5 (B) moves every count by its retired assets.
- **Referee:** none for the primaries; the extract log defines what a 304 sends and what the DAM's property column
  holds (the judge's pins, the WHAT only); no filed sentence says which paths are hero slots, which log holds the
  aliases' requests, or that the March 2025 moves left the DAM's labels behind.

| Ask figures | Cracker's path | Cracker's value | Verdict |
|---|---|---|---|
| A gigabytes (6) | the hero directory read from the beacons' own URLs, every request served on it (200 and 304 alike), the Sydney month, the image hosts' log only | Tideline 2,593, Hearth 2,031, Trailhead 705, Pantry 751 GB: every property off | miss |
| A dollars (6) | the same gigabytes at AUD 0.071 | every property off | miss |
| B hero images (6) | live assets on the latest crawl, one per asset with the library records folded in, under the export's property column | the moved sections' heroes under the property they came from: all six off | miss |
| C loads moved (6) and the chart | the golden's construction | right | outside |

Mirror leakage: 7 per cent of the ask weight on the most attractive wrong rung, the level with the render delay held
(R4): two of the six Ask C counts coincide with the golden's (Hearth's and Ledger's, which no floor moves), the
chart marks Pantry, and the mirror does Asks A and B as the cracker does; on the default path it keeps none.
Pair ceiling: 40 (the cracker at about 63 with the call, Ask C and the chart; the held-rung mirror at about 16).

## Tried and rejected

- DA07 for this slot's turn (a parcel carrier's 2027 van tiers by duty-cycle fuel-economy demonstration): every
  honest decisive step found in that world normalises each van's fuel use to its duty cycle (composition_mix),
  barred today against task256; the other candidates (ledger posting lag, telematics fuel bias, protected cold days
  for electric vans) were a near copy of task181's completion by channel, a planted-defect flip or the same mix by
  temperature. task258 drawn first; task257 waits for a later draw day.
- Engagement samples of 900 beacons a window with a lognormal after-delay: the level's mean and median and the load
  time's estimators differed enough to move Ledger's rounded count across a 100,000 edge (a determinism fork on Ask C);
  3,000 beacons a window, each window's parts spread evenly over their quantiles by device, a symmetric after-delay,
  and each engagement's own level and ratio centred on 240 ms and 0.48, so every estimator agrees to the rounding.
- Tideline's mid-month sampling change at 0.0005 to 0.0008: one rate for the month lifted Tideline above Pantry, a
  Layer 1 slip deciding the call; softened to 0.0006, the call asserted under either rate.
- Pantry sampled at 0.0030 (small origins sampled more): unweighted counts put Pantry first on the ratio and
  zero-delay rungs, so a solver who skipped the weights landed the call for the wrong reason; rates evened (Pantry
  0.0010) and every wrong rung asserted off Pantry without weights.
- Trailhead at 17 million page loads a month left Pantry last on every slow load and on the default path (an
  inversion); Trailhead at 8 million puts Pantry 5th on both.
- Ask A's primary as the slot mix (hero, inline and thumbnail directories on the same hosts): a careful solver reads
  the hero directory off the beacons' own URLs, so the slot mix is a hazard and the legacy aliases' separate log the
  primary; Ask B's library records are findable from legacy_id, so its primary became the DAM's property label left
  behind by the March 2025 section moves.
- A revalidation share equal to the alias share on Trailhead (both 9 per cent): the cracker's 304s and its missed
  alias cancelled to the golden's gigabytes; Trailhead's revalidations set at 14 per cent.
- Loop 1, the cached hero images as the second layer (a returning visitor's hero already in the browser cache,
  which the playbook does not touch): it would rest on reading a transfer-size field, a field read deciding the
  call, and it barely moved the counts; a seasonal adjustment for the quarter would have made the task a forecast.
  Both dropped before this layer was drawn.
- Loop 1, Tideline as the new golden (loop 0's runner-up at 4.6 million): Tideline wins
  every slow load (R0), so a solver at rung 0 would land the call; Matchday, first on no wrong rung, drawn instead.
- Loop 1, the floor on Matchday as loop 0 built it: Matchday 2nd on the default path and on three grid cells; a
  longer hero delay alone (1,000 to 1,300 ms medians) left it 2nd or 3rd on the default path and put it 2nd on the
  zero-delay rung with the held rung's margin under 1.20x; its own-image share and other loads were retuned with it
  (0.26 to 0.31, 1,800 ms), so it sits 4th on every slow load and 5th on the default path.
- Loop 1, the held pages on Pantry, Tideline and Hearth only: the level with the render delay held matched the
  golden on four of the six rounded counts (Matchday, Hearth, Ledger, Trailhead), a mirror near half of Ask C and a
  pair ceiling of about 43; one section each at Matchday and Trailhead now waits on the snippet, so the held rung
  shares only Hearth's and Ledger's counts, which no floor can move (Ledger has no held pages, and Hearth's time to
  first byte keeps its held pages slow either way).
- Loop 1, a first paint that varies smoothly with the page (render-blocking styles of any length) in place of the
  snippet's timeout: held pages' first paints would straddle 2,500 ms, and the floor taken once against the paint's
  own work counted after the first paint (SF16) would part by more than the rounding; the timeout puts every held
  page's first paint at least 3,060 ms after its first byte and every other page's within 230 ms, so both placements
  agree.
- Loop 1, Pantry's traffic at 9.62 million loads a month: the held rung's margin over Matchday fell to 1.20x after
  Matchday's retune; at 10.2 million it holds at 1.27x, and Pantry's hero egress moves with it (653 GB, $46).

## Build record

- Stage 3: `python3 task258/generator/build.py` writes the pack (16 files, 4 formats; the beacon extract 157,066
  rows), the goldens, figures.json and metadata.json; 159 checks green (the three-rules block R1 to R3c on the
  clean truth, SF1 to SF14, the estimator corridor, both asks' ladders, the separation line); the independent
  verifier agrees on the call and the 24 figures of the golden paper; two builds byte-identical; target.zip cut from
  the final build. precut exit 0; figures_check exit 0 (69 figures); container audit clean on target/ and golden/;
  leak.py REVIEW, no LEAK (clause numbers 2.3 against Trailhead's 2.3 million, the charter's estimand wording, the
  documents' ordinary vocabulary); guard heart WARN (repeat.gate_g, overuse.gate_g, repeat.decision, answered in the
  Draw), validate clean; guard surface promotes task256 (surface 0.100, same decision type; author-triggered
  adjudication, not run): the drivers differ (task256 a fit on a survey's joint distribution at the roster's sex
  mix, this build a part of the paint settling at a level), so do the strategies (composition_mix against
  population_selection) and the decisive gaps (population against time).
- Layer 1 column naming: the beacons' device column renamed form_factor after leak.py read `device` as generator
  vocabulary.

- Stage 4 (2026-10-13): leak reader (one isolated read): no decisive-step sentence, no ranking file, no helper
  file, no answer figure; every literal sentence executes to the golden; the decisive step an analytical choice; the
  seven REVIEW lines harmless; three realism tells (the November rate changes' notes written to explain them, the
  small sites' blank dates, a uniform Changes column) fixed in the generator. Determinism judge: DETERMINISTIC,
  APPROVE; every figure reproduced; Gate G method_or_model_selection, analytical_non_defect, no surface read, no sole
  data defect; Gate H domain, layers and decisive step pass. Its two residual forks, both on ask figures, pinned as
  WHAT in the extract log's notes (status 200 sends the image and 304 none; the DAM's property is the hero
  collection an asset was uploaded to, against the page that carries it now) and named in the submission's steps;
  no graded figure moved (checks and verifier unchanged), no re-judge needed on an APPROVE.
- Loop 1 (2026-10-14, the author's second layer, one generator pass): `fcp_ms` in both beacon extracts and the field
  notes; the held sections and the two held engagements in `generator/common.py`; the golden's rung and the floor's
  grid in `analysis.py`; 193 checks green (the three-rules block with the floor on the clean truth, SF1 to SF16, the
  engagements' back-test of the floor and of the held and partial rungs, the floor's two placements, the mirror
  line, the estimator corridor, both asks' ladders); the independent verifier applies the floor on its own parsing
  path and agrees on Matchday 4.6 million (1.40x) and the 24 figures of the golden paper; two builds byte-identical;
  target.zip cut from the final build (16 files, the beacon extract 157,825 rows). figures_check exit 0 (80
  figures); leak.py REVIEW, no LEAK (clause numbers 3.1 and 3.2 in the charter against Tideline's 3.1 and Hearth's
  3.2 million, the charter's estimand wording, the documents' ordinary vocabulary); guard validate clean;
  guard heart BLOCK on ban.forum against task231 only, an ordering artifact: both cards were filed on 2026-10-13
  before registration stamps existed, so the guard orders them by task number, while task231 was drawn at 17:18 UTC
  (f9161fb), twelve hours after this build (f17b9d7, 04:52 UTC); in drawn order the three builds before this one are
  task229, task451 and task256, none with this forum, and the reship keeps the draw's forum. The similarity rules
  pass with loop 0 differentiated as the slot's own lineage; the WARNs are loop 0's, answered in the Draw. guard
  surface promotes task256 (same decision type) and task259 (same decisive gap), as at loop 0; adjudication is
  author-triggered and not run.

## Pre-ship check

- **Rule 1, the domain:** the deciding quantity is each property's page loads a month brought under the 2,500 ms LCP
  line by a change to two of the paint's four RUM attribution parts that leaves the page's first paint alone,
  estimated from how past engagements moved each part; with another field's nouns there is no paint split into
  parts, no CDN connection to settle a delay and no first paint to hold a faster image back.
- **Rule 2, two layers:** every Layer 1 item in the inventory is produced by the group's own systems and asserted
  neutral to the call; the decisive layer is the counterfactual model of the paint (the delay's level and the
  first-paint floor), and the late first paints are the experimentation tool's own behaviour, named in no file.
- **Rule 3, the decisive step:** analytical (which model of the playbook's effect the engagements bear out, the floor
  included), executed in checks.py: the default path on the clean truth files Ledger, the level with the render
  delay held files Pantry, the level with the floor files Matchday, the floor without the level files Ledger, no
  plant ships. Reading every field (the first contentful paint included) and executing every filed sentence still
  leaves the paint's model open; only the engagements' own loads close it.
