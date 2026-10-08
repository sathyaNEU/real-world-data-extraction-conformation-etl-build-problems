# OS01 — Which desk gets the one headline-testing squad, when the biggest winners reach readers through screens that never show the tested headline

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Product Analytics · content experimentation programmes |
| Mirrors | Placing a scarce optimisation team on the surface with the biggest measured wins, when much of that surface's traffic arrives through renderings the team cannot change (publisher headlines shown inside Google News, Apple News and Discover; Open Graph link cards on Meta; App Store product-page tests against search-sourced installs) |
| Decision shape | Which of N gets one scarce thing, with the sizing kept as the graded figure: the squad embeds with one of six shortlisted desks for a year |
| Committed call | The desk the squad embeds with in January, and the incremental article clicks a year it is expected to add |
| Gap · Pattern | Gap 3 (objective) into Gap 2 (population) · Pattern C (serviceable share behind a join), over the winner's curse (statistical rigour, certified by the change log) and a coarsened segment (#14) |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #14 coarsens the segment it was asked about · #13 validates on one population, applies to another · #7 uses the ready-made measure |
| Calibration form | Change-log natural experiments: the squad's seven past embeddings, each logged with its start month and the embedded desk's clicks against matched desks |
| Driving force | A winning headline earns clicks only where the platform itself draws it. Clicks that start in partner news apps, search, social cards, newsletters or alerts are made on the canonical headline stored at publication, which no test changes. Each desk's drawn share is a per-desk fraction built from the click-source log through a pageview → article → desk join, stated nowhere, and it is lowest on the desks whose winners look biggest. Every past embedding was in an app-exclusive desk, so the change log certifies scaling on total clicks. |

## 1. Situation

A news publisher runs one headline-testing squad. It embeds with one desk for a year, tests every headline that desk publishes, and ships
each winner. The squad's charter shortlists six desks for next year, named by vertical and edition: Politics·national, Sport·metro,
Business·national, Sport·national, Local·metro and Culture·national. The experimentation dashboard reports the average winning lift by
vertical. The test archive holds every concluded test at package level. The audience director wants the squad wherever the readers are.

## 2. Gate G: why this is legal

* **Litmus.** Every reported figure is correct: the dashboard's vertical averages, each test's impressions and clicks, the change log's
  realised gains and the click-source log. No stakeholder read is overturned. The difficulty is that a measured lift can only be earned on
  the clicks the platform draws, and that share is a property of each desk's traffic that nobody has computed.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the director's view and the dashboard. The archive still ranks desks by lift × clicks, the change log still
  certifies shrinkage on total clicks, and nothing in the pack says which clicks a winner can reach.
* **Instrument repair.** Give every test unlimited impressions and perfect measurement. The lifts become exact and the canonical headline
  still governs every click that starts outside the platform's own screens.
* **Lens swap.** The naive read and the answer are different populations: all clicks a desk earns against the clicks that start on a
  platform-drawn headline in the coming year.

## 3. The driving force

A strong solver distrusts the dashboard, rebuilds each desk's lift from the archive, notices that winners are selected on noise, and
shrinks them. The change log confirms it: shrunk lift × desk clicks reproduces all seven past embeddings. Then it ranks, and the
large, clean Business desk wins. But a headline variant is assigned when the platform draws a page. A Business story read through a
partner news app, a search result, a social card, a newsletter or an alert is clicked on the canonical headline, and 70% of
Business·national's clicks start there. The change log cannot show this, because every embedding so far was in an app-exclusive desk
whose stories have no feed entry, no web URL and no search listing. Local·metro's readers arrive almost entirely through the app's own
feed, so its modest lift lands on 95% of its clicks.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The dashboard's average winning lift for the desk's vertical × the desk's planned clicks | A, Politics·national | The experimentation team's own programme figure on the audience plan's traffic | The charter names desks by vertical and edition, and the archive carries each test's desk code; Politics' average is lifted by the metro edition's small, noisy tests |
| 1 | Each desk's own average observed winning lift, from the archive, × planned clicks | B, Sport·metro (1.22× over C) | The right grain, from the raw tests | The change log: every embedding's realised gain matches the empirical-Bayes shrunk lift, 7 of 7 within 2%, and the raw winning lift overstates all seven by 1.3× to 3.6× |
| 2 | Shrunk winning lift (prior fitted on all packages) × planned clicks | C, Business·national (1.27× over A) | Selection bias removed, and certified by every past embedding | The click-source log: 70% of Business·national's clicks start on surfaces that show the canonical headline |
| 3 | **Decisive:** shrunk lift × the clicks that start on a platform-drawn headline (home, section fronts, app feed, in-article links), by desk | **E, Local·metro** (5th of 6 on rung 0), **2.82M clicks a year** | — | — |

* **Position table.** Local·metro ranks 5th on rung 0, 5th on rung 1 and 4th on rung 2, and leads only rung 3 (1.35× over Sport·metro).
  The rung leaders beat their runners-up by 1.88×, 1.22× and 1.27×.
* **Discriminator dominance.** Business·national carries a 2.06× advantage into rung 3 (6.12M against 2.97M shrunk-lift clicks).
  Local·metro's drawn share is 0.95 against Business·national's 0.30, an edge of 3.17×, above the 2.47× the margin floor needs. Product:
  3.17 / 2.06 = 1.54× in Local·metro's favour.
* **Partial correction priced (L3).** A solver who removes only partner-app clicks, the channel the syndication agreement makes visible,
  keeps search, social, newsletter and alert clicks and still names Business·national (3.98M against 2.97M, 1.34×). A solver who applies
  the drawn share to unshrunk lifts names Sport·metro at 7.48M, further from the answer than rung 2. A solver who applies it at vertical
  grain names Business·national (1.84M against 1.52M).
* **Grid.** Grain (vertical, desk) × shrinkage (off, on) × click base (all, all but partner apps, platform-drawn) gives 12 cells. Only the
  answer cell names Local·metro. Every other cell names A, B or C, each with a leader at least 1.20× clear. The nearest wrong figure for
  Local·metro is 2.97M (+5.3%), and it sits in cells whose leader is Business·national, so reaching it also costs the name.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** No document says a variant reaches only the clicks the platform draws. The field dictionary defines the
   canonical headline as the one carried in feeds, search and social metadata, newsletters and alerts, a sentence about storage.
2. **Corpus blind for a computable reason.** *In every closed embedding the drawn share was 1.00, because the squad has only ever
   embedded with app-exclusive desks (Puzzles, Recipes, Games, Wellness), whose stories have no feed entry, no web URL and no search
   listing.* Shrunk lift × total clicks reproduces all seven.
3. **No arithmetic symptom.** Pageviews in the click-source log reconcile to desk totals in the audience plan, the dashboard ties to the
   archive, and every rung's click base reconciles.
4. **Not a row predicate.** The share needs pageviews joined to articles and articles to their owning desk, a classification of each
   click-source code by whether the platform draws the headline there, and a share per desk, which then multiplies a lift recovered
   from package-level shrinkage.
5. **The enumeration is arithmetic.** No column carries "reachable", and the desk file has no source mix. The share is computed for
   all six desks from 41 million pageviews.
6. **No cutover date.** Source mixes are stable across the year and no series steps; the squad's past embeddings are decoy material.
7. **Survives deletion.** Removing every voice and the dashboard leaves the change log certifying the wrong base.

## 6. The calibration corpus

* **Form.** The change log's seven embeddings (2019–2025), each with start month, tests run, the desk's clicks for the twelve months
  before and after, and matched non-embedded desks, plus every test's packages in the archive.
* **What it certifies.** Shrinkage. Shrunk lift × desk clicks reproduces 7 of 7 realised gains within 2%. Raw winning lift overstates
  every one (1.3× to 3.6×). A prior fitted per desk reproduces 3 of 7, and its misses all run high, so it fails on the total too.
* **What it is blind to.** The drawn share (above).
* **Twin pair.** Embeddings #3 (Puzzles, 2021) and #6 (Recipes, 2024) are identical on every change-log column: app-exclusive, 60 tests,
  5.2% average observed winning lift, 48M clicks. Their realised gains are 1.92M and 0.95M (2.03×), because #3's tests ran on the home
  module at large samples (shrinkage factor 0.77) and #6's on a niche tab (0.38). Only package-level shrinkage separates them.
* **Resemblance points at the decoy.** Business·national's tests (large samples, steady lifts) most resemble embedding #3, the largest
  realised gain on file.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The charter: the squad is judged on incremental article clicks in the twelve months after it embeds, counted at the
  owning desk. The charter's shortlist table names the six desks by vertical and edition. The field dictionary: `canonical_headline` is
  the headline stored at publication and carried in feeds, search and social metadata, newsletters and alerts. The audience plan carries
  each desk's clicks forward at last year's source mix.
* **Empirical pins.** The shrinkage prior, from all packages and certified by the change log. The drawn share, from the click-source log.
* **Voices.** The audience director: "Politics is where our readers are; put the squad where the readers are." The experimentation
  lead: "Every winner we ship clears significance. A winner is a winner."
* **Licensed wrong basis.** The charter records that the editor-in-chief's office reviews squad placement on the dashboard's average
  winning lift by vertical and will present it at the planning meeting.

## 8. Determinism by construction

* **Source codes.** Every article pageview carries the surface whose headline was clicked. Direct visits land on the home page, which is
  not an article pageview, so no pageview lacks a source and no "direct" class needs a convention.
* **Prior.** Method-of-moments and maximum-likelihood fits of the prior agree within 1% on every desk's shrunk lift (2,400 tests across
  the archive), and the change log refutes per-desk priors.
* **Maturity.** All seven embeddings have twelve full months after the start, and the archive exports concluded tests only.
* **Ownership.** Each article has exactly one owning desk in the CMS, so co-bylined stories do not split.
* **Rounding.** The committed figure, 2,821,500 clicks, sits mid-bin at the nearest 10,000.

## 9. Prompt sketch and deliverables

> The headline-testing squad moves in January and I have to say where. Our audience director's view is that it belongs wherever the
> readers are. Name the desk from the shortlist and the extra article clicks a year it should bring, to the nearest 10,000, in one
> line I can drop into the plan. I need `squad_placement.xlsx`, the chart `desk_click_gain.png`, and a one-page `squad_memo.pdf`.

* `squad_placement.xlsx` — the sizing for all six desks on four bases, the corrections sheet (ask A), the newsletter sheet (ask B) and the
  change-log back-test (ask C).
* `desk_click_gain.png` — a script-rendered grouped bar chart: per desk, clicks gained on observed lift, on shrunk lift and on
  platform-drawn clicks; desks ordered by the last; the chosen desk highlighted; a stacked strip under each desk showing its click-source
  mix; Business·national's 30% drawn share annotated.
* `squad_memo.pdf` — the committed desk, its click figure, and why the other five are not it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the six desks, last year's headline corrections per 1,000 articles and the median
  minutes from publication to the first correction. *Device:* the CMS writes one revision row per save, and its guide says a correction
  note persists on every later revision until removed. Counting noted revisions over-counts corrections 2–4× on the live-blog-heavy
  desks.
* **Ask B (device-carried).** For each desk's newsletter, click-to-open rate over the last 13 weeks and its change on the prior 13, and
  the desk with the largest fall. *Device:* the email platform's export marks privacy-proxy prefetch opens, which its guide excludes from
  opens. Keeping them halves the rate for Apple-heavy lists and invents a fall at two desks.
* **Ask C (validity).** Each desk's clicks gained under each of the four rung bases, and the change-log hits (of 7) for raw and shrunk
  lift.
* **Decoupling.** Setting every desk's drawn share to 1 changes no figure in asks A or B. Neither the revision log nor the email export
  touches the click-source log or the test archive.

## 11. Rubric arithmetic

6 desks × 2 (ask A) + 6 × 2 and the largest-fall desk (ask B) + 6 × 4 bases and 2 back-test counts (ask C) + the committed desk, its
click figure, the runner-up and the margin + 5 named chart parts + 3 files ≈ 63 criteria.

## 12. World-building constraints

* Planned clicks (M): Politics·national 420, Sport·metro 80, Business·national 300, Sport·national 350, Local·metro 110,
  Culture·national 150. Observed winning lifts by desk: 1.3%, 11.0%, 2.4%, 1.5%, 3.6%, 2.6%; shrinkage factors 0.88, 0.28, 0.85, 0.85,
  0.75, 0.70. Dashboard vertical averages: Politics 3.23% (metro edition 130 tests at 6.2%), Sport 1.95%, Local 1.89% (suburban edition
  200 tests at 1.2%).
* Platform-drawn shares: 0.20, 0.85, 0.30, 0.30, 0.95, 0.55; partner-app shares 0.55, 0.05, 0.35, 0.35, 0.00, 0.10.
* Rung leaders are A, B, C, E with margins 1.88×, 1.22×, 1.27×, 1.35×; Local·metro is 5th, 5th, 4th, 1st. Every grid cell's leader is
  at least 1.20× clear.
* Every past embedding is app-exclusive. The twin embeddings #3 and #6 match on every change-log column.
* Correction revisions and newsletter opens never touch tests, clicks or source codes.
