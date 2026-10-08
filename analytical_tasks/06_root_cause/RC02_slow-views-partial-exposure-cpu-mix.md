# RC02 — Which of five shipped changes gets next quarter's performance fix, when two of them only ever shipped together

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Product Analytics · web performance and page experience |
| Mirrors | Field-performance regressions at large web properties (Google Search and YouTube web, Meta and Instagram web, Amazon retail pages) where two releases ride the same rollout train and the only clean reads come from page groups that got one change and not the other |
| Decision shape | Which of N root causes gets the fix: one quarter of performance engineering, one cause |
| Committed call | The cause the performance quarter fixes, and the mobile page views a month its fix brings back under the 4.0-second budget |
| Gap · Pattern | Gap 2 (population) · Pattern D (two grains, both flawless: standardisation inside partial-exposure groups), with E29 (a mixed segment split through a join) at rung 2 |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #13 validates on one population, applies to another · #6 treats a mixed segment all one way · #7 uses the ready-made measure |
| Calibration form | Pilot log: eleven closed fix pilots, each randomised across mobile users, with arm-level over-budget shares and the performance council's filed decision |
| Driving force | The ad stack and the framework bundle rode one staggered rollout across the same templates, so only two partial-exposure groups separate them: AMP landing views (ads, no framework) and subscribers' ad-free article views (framework, no ads). Both reads are correct for their groups. AMP views run on low-end phones and subscribers on high-end ones, and both effects scale with the phone's CPU class, which lives in the device registry. Read straight, the ads look bigger; standardised to the ad-supported base, the framework is. |

## 1. Situation

A national news publisher's share of mobile page views over its 4.0-second loading budget rose from 9% to 16% over two quarters (400 million
mobile views a month). Five changes shipped in that time, each a real candidate: the header-bidding ad stack (A), a CMS image pipeline that serves
larger hero images (B), the client-side framework migration (C), a consent-management banner (D) and a brand web-font refresh (E). The monthly
synthetic crawl, whose URL list was refreshed in the same period, shows median mobile page weight up 38%. Next quarter's performance engineering
goes to one cause.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the crawl's byte bridge, the field over-budget series, each release's dated step, the partial-exposure
  effects read in their own groups and the pilot log. No reported number or stakeholder reading of their own numbers is overturned. The
  difficulty is that the two groups that separate A from C are not miniatures of the population the fix will act on.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete every voice, the crawl dashboard and the licensed basis. The field data still shows a staggered joint ramp, the two
  partial-exposure groups still read A ahead of C, and nothing in the pack says their CPU mix matters.
* **Instrument repair.** Suspect file: the synthetic crawl, whose URL list was refreshed in the same period, so its two months measure different
  pages. Repaired to a matched list, rung 0 names E (the fonts, +300 KB) instead of B; rung 1's field event study still names D and rung 2 A,
  and none names C. The field view log, the rollout log, the subscription register and the device registry are complete. The answer still needs
  both partial-exposure effects estimated by CPU class and standardised to the base: even perfect per-script timing leaves the views that
  carried both changes in their joint state, and the two groups' CPU mix is a property of who uses them, which no better timer changes.
* **Lens swap.** The raw reads describe AMP landing views and subscribers' article views; the answer is about the views each fix acts on at
  last month's traffic, the ad-supported base for the ad stack and every mobile view for the framework: different populations, not one
  population under two lenses.

## 3. The driving force

A strong solver moves from crawl bytes to field page views at once, because the charter scores fixes on field views. It aligns each release
to its date and finds clean steps for the image pipeline, the banner and the fonts. A and C, though, were switched on template cohort by
template cohort over the same six weeks, so the series shows a ramp with no date. The solver aligns the ramp by cohort week and gets their
joint effect (+4.99 points on ad-supported views), then looks for views that got only one change. AMP landing views carry the ad stack without
the framework. Subscribers signed in on article pages get the framework without ads, once the "article" segment is split through the
subscription register. Each group's effect is a correct measurement, and A reads 3.94 points against C's 1.05. Both effects, however, grow on
weaker phones, and CPU class is a property of the device model held in the registry, not a column in the view log. AMP views are 85% low-end
phones; subscribers' are 10%; the ad-supported base is 38%. Standardised to the base, C is 2.96 points and A 2.03, and the framework's fix
also reaches subscribers' 80M ad-free views. Both readings sum to the same joint ramp, so nothing fails to reconcile.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Crawl byte bridge: KB each cause added per crawled mobile page, current list against prior list | B, image pipeline (+520 KB) | It is the quarterly report's own metric, cleanly decomposed by resource | The charter scores a fix on field page views, not crawled pages |
| 1 | Field event study: the over-budget share's step at each release date, in views a month | D, consent banner (5.6M views) | It moves to the scored metric and uses the dates the change log files | The rollout log shows A and C switched on by template cohort over six weeks: a ramp no date captures |
| 2 | Cohort-aligned joint ramp split by each partial-exposure group's effect read in its own views; the article segment split through the subscription register to find framework-only views | A, ad stack (12.6M) | Two clean natural experiments, and their effects sum exactly to the joint ramp | The device registry shows the AMP group 85% and the subscriber group 10% low-end phones against the base's 38% |
| 3 | **Decisive:** each group's effect estimated by CPU class and standardised to the ad-supported base's CPU mix, each fix counted on the views it acts on | **C, framework bundle (10.3M)** (4th of 5 on rung 0) | — | — |

* **Position table.** C ranks 4th on rung 0, 5th on rung 1 (unattributed) and 3rd on rung 2, behind A and the banner; it leads only rung 3.
  Rung leaders beat their runners-up by 1.73×, 1.40×, 2.25× and 1.58×.
* **Discriminator dominance.** A carries a 3.00× advantage over C into rung 3 (12.6M against 4.2M). Standardisation multiplies C's figure by
  2.45 and A's by 0.52, an edge of 4.76×, 1.32 times the required 1.2 × 3.00 = 3.60; the net margin is 1.58×.
* **Partial correction priced (L3).** Every half-built standardisation leaves A in front. Standardising on the view log's own columns (device
  category, effective connection type) changes nothing, because both are decorrelated from CPU class inside each group by construction: A
  12.6M against the banner's 5.6M (2.25×). Standardising only the AMP group, whose low-end skew its search referrals make visible, takes A to
  6.5M, still ahead of the banner's 5.6M (1.16×) and of C's raw 4.2M; standardising only the subscriber group lifts C to 10.3M against A's raw
  12.6M (1.22×).
* **Grid.** Grain (crawl or field) × crawl list (full or matched) × ramp (unattributed or cohort-aligned) × split (raw, view columns, AMP
  group only, subscriber group only, both groups on CPU class) collapses to eight distinct builds, because the list only matters on the crawl
  and the split only after alignment. The crawl builds name B (full list) or E (matched list, fonts +300 KB); the unaligned field build names
  D; the aligned builds name A four times and C once. The nearest wrong cell is the subscriber-only standardisation (A by 1.22×), and moving
  from it to C takes the AMP group's registry join.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The charter defines the metric; the release notes describe each change; the paywall policy says subscribers get the
   ad-free layout. No document says the groups differ in phones or that the effects depend on CPU.
2. **Corpus blind for a computable reason.** *In every closed pilot the arms were randomised across users, so each arm's CPU-class mix equals
   the base's to within one point and the raw and CPU-standardised effects agree to 0.05 points.* The pilot log certifies the field metric and
   reading an effect inside its own group, and it cannot see transport.
3. **No arithmetic symptom.** Raw and standardised splits both sum to the joint ramp (4.99 points); views, templates and arms reconcile on
   every rung.
4. **Not a row predicate.** It needs a join from each view's device model to the registry, an effect estimate per CPU class inside each
   partial-exposure group, and a reweighting to a base composition built from a third population.
5. **The enumeration is arithmetic.** No column carries CPU class or an "exposed to" flag; both are built from the registry and the rollout
   log.
6. **No cutover date.** A and C ramped by template cohort with no aggregate step; the dated releases (B, D, E) are the decoys.
7. **Survives deletion.** With every voice and the crawl report gone, the raw partial-exposure reads still name A.

## 6. The calibration corpus

* **Form.** The pilot log: eleven closed fix pilots, each a revert or optimisation randomised across 50% of mobile users for 14 days, with
  arm-level views, over-budget shares, the resource class touched and the council's filed adopt or hold decision.
* **What it certifies.** That a fix's value is the over-budget views it removes in the field (every adopted pilot's filed saving reproduces
  from its arms to the view), and that an effect read inside a randomised group transports to that group's own traffic. The crawl's bytes
  removed predict filed savings in 4 of 11 pilots.
* **What it is blind to.** Transport across CPU mix (above).
* **Twin pair.** Pilots P-06 and P-09 removed a 180 KB script from two template families identical on views, device category, connection
  mix, lab bytes and month. P-09 removed 1.9 points and P-06 0.9 (2.1×), because P-09's audience is 55% low-end phones and P-06's 20%. No rate
  transferred by template, bytes or connection reproduces both; the per-CPU-class effect does.
* **Resemblance points at the decoy.** The AMP group matches pilot P-04 (ad-slot lazy-loading on landing templates) on every visible column,
  and P-04's filed saving of 3.9 points sits beside A's raw read.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The performance charter: a fix is scored on mobile page views brought back under the 4.0-second budget, at last month's
  traffic. The paywall policy: signed-in subscribers are served the ad-free article layout. The device registry: CPU class comes from the
  benchmark band of the device model.
* **Empirical pins.** The joint ramp from cohort alignment; each group's effect by CPU class from its own views against its pre-rollout
  weeks; additivity of A and C from the joint ramp (both splits sum to it).
* **Voices.** The front-end platform lead: "We tried the framework on subscriber pages before it went wide; it was never the problem." The
  editorial product director: "Pages are heavier every month in the crawl, and it's the pictures."
* **Licensed wrong basis.** The charter records that the ad-revenue committee reviews performance work on lab page weight from the monthly
  crawl and will present that basis at the planning review.

## 8. Determinism by construction

* **Over budget.** A view is over budget when its largest-contentful-paint exceeds 4.0 s; no percentile convention enters.
* **CPU bands.** Three classes fixed by the registry's benchmark bands; every device model in the view log resolves to exactly one.
* **Base.** Each fix is valued on the views it acts on in the last full month: the ad stack on the 320M ad-supported views at their CPU mix,
  the framework on those and on subscribers' 80M ad-free article views at the subscriber group's own read, so no base is left to choose.
* **Effect windows.** Four pre-rollout and four post-rollout weeks per cohort; three- and five-week windows give the same per-class effects to
  0.05 points, because no other release touches the A-only or C-only groups.
* **Maturity.** Beacons arrive within 48 hours, and the extract is taken five days after month-end.
* **Rounding.** The committed figure sits mid-bin at the nearest hundred thousand views.

## 9. Prompt sketch and deliverables

> Our share of mobile views over the four-second line has gone from 9% to 16% in two quarters, and next quarter's performance engineering fixes
> exactly one cause. Our VP is convinced it was the consent banner. Tell me which cause we fix and how many mobile page views a month that fix
> brings back under the line, rounded to the nearest hundred thousand, in one sentence I can read out at planning. Send
> `slow_view_attribution.xlsx` and a chart `cause_effects.png`.

* `slow_view_attribution.xlsx` — the five causes under each construction, the crawl sheet (ask A) and the image-delivery sheet (ask B).
* `cause_effects.png` — a dot plot of each cause's views a month under the raw and standardised reads, joined by arrows; an inset of the
  low-, mid- and high-end shares of the AMP group, the subscriber group and the ad-supported base; the joint ramp as a reference band; and the
  chosen cause labelled with its figure.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 14 crawled template families, median transfer size and request count on first view
  and on repeat view. *Device:* the crawl loads every URL twice in one browser and files both runs as rows with a run index, as its run
  configuration documents; pooling the runs misstates both medians in the eight families with long-lived cached assets.
* **Ask B (device-carried).** For each of the last six months, image requests served and image egress by output format (AVIF, WebP, JPEG).
  *Device:* the image CDN writes one log row per cache fill per edge location and carries the fill's served-request count in a hit counter,
  as its log schema documents; counting rows as requests understates requests about 26-fold and reverses the format ranking in two months.
* **Ask C (validity).** Each of the five causes' views a month under each of the four rung constructions.
* **Decoupling.** Clearing the CPU-class standardisation, the registry join and the subscription split changes no figure in asks A or B.

## 11. Rubric arithmetic

14 families × 4 figures (ask A) + 6 months × 3 formats × 2 figures (ask B) + 5 causes × 4 constructions (ask C) + the committed cause, its
figure and its margin over A + 5 named chart parts + 2 files ≈ 120 criteria.

## 12. World-building constraints

* 400M mobile views a month, 320M of them ad-supported and 80M subscribers' ad-free article views. Over-budget share 9% to 16% (+28.0M views): D
  5.6M, B 4.0M and E 2.4M as dated steps; A and C a cohort-staggered ramp of +4.99 points on ad-supported views.
* CPU-class effects (points): A 4.54 / 0.63 / 0.20 and C 6.98 / 0.63 / 0.20 (low / mid / high). Mixes: AMP 85 / 11 / 4, subscriber article
  views 10 / 40 / 50, ad-supported base 38 / 42 / 20. Raw reads A 3.94 and C 1.05, standardised 2.03 and 2.96; both sum to 4.99. In views a
  month: rung 2 A 12.6M, C 4.2M (3.36M ad-supported plus 0.84M subscriber); rung 3 C 10.3M (9.46M plus 0.84M), A 6.5M.
* Device category and connection type are decorrelated from CPU class inside each group; no other release touches either group.
* Crawl rung: B +520, E +300, A +210, C +140, D +60 KB (full list); matched list E +300 leads.
* P-06 and P-09 are identical on every visible pilot column. Every pilot was randomised across users.
* The crawl's run index and the image CDN's hit counter touch no field view, subscription record or registry row.
