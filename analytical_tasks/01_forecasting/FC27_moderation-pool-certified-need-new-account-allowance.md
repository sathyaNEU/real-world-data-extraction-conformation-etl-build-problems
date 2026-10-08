# FC27 — How the 2027 moderation pool of 120 FTE splits across nine sites, measured the way the council certifies review need

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Product Analytics · online community trust and safety |
| Mirrors | Trust-and-safety capacity split across communities or surfaces after a generative-AI content shift, where the workload standard the business certifies prices new-account content differently from what the review log labels (Meta and Instagram review queues, Google Play and App Store review capacity, marketplace listing moderation) |
| Decision shape | An allocation under a cap: the 120-FTE 2027 moderation pool across nine topic sites, in proportion to forecast review need |
| Committed call | Each site's 2027 FTE to one decimal, summing to 120.0, with Scriptwell's figure stated on its own |
| Gap · Pattern | Gap 4 (rule) over Gap 1 (time) · Pattern B (the certified need rule recovered from a published control set), with the segment coarsened (measured #14) at rung 1 |
| Gate G mechanism | method_or_model_selection, with forecasting support |
| Measured traps engaged | #1 reports a failed back-test, ships anyway · #3 stops at a close but inexact match · #14 coarsens the segment it was asked about |
| Calibration form | Published control set with a reproduction clause: the council's 99 certified half-year need figures (nine sites, 2021H1–2026H1, each broken down by queue), and the charter clause that a need method must reproduce every one |
| Driving force | Certified need adds a six-minute verification allowance to every reviewable item, outside the first-posts queue, whose author's network account was under 30 days old when the post was created. No column labels those items: the age sits two joins from the review log (item → post → the author's network account), and the site profile's own creation date is a near miss. Since the AI shock, new accounts post two fifths of Scriptwell's reviewable content and none of the four smallest sites', so the queue-standard construction that reproduces 64 of 99 certified figures under-measures exactly the site whose question volume fell most. |

## 1. Situation

A developer Q&A network runs nine topic sites. After generative-AI tools arrived, question volume fell by between a fifth and three
fifths depending on the site, and finance has capped the 2027 paid moderation pool at 120 FTE, down from 150. The council's charter
allocates the pool in proportion to each site's forecast review need. Every half-year since 2021 the council has published a certified
need table, each site's review need in moderator hours with a breakdown by queue, and the charter says a need method may be used only if
it reproduces every certified figure. The moderation standard lists the queues that count and their handle-time standards. The council
votes on the split at its December sitting.

## 2. Gate G: why this is legal

* **Litmus.** Every figure in the pack is correct: the review log, the certified tables, the dashboard's item counts, the handle-time
  standards and the volume series. No stakeholder's reading of their own numbers is overturned; Scriptwell's questions did fall the most.
  The difficulty is recovering what certified need actually counts, which no document writes down.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete every voice and the dashboard. The queue-standard construction still reproduces 64 of 99 certified figures,
  still looks like the standard applied faithfully, and still under-measures Scriptwell.
* **Instrument repair.** Give the review log a perfect "verification" column. The allowance would then be readable, but the 2027 split
  would still need each site's forward mix of new-account and established items, and the rule's size would still have to come from the
  certified tables, because no document prices it.
* **Lens swap.** The naive read and the answer weigh different populations: queue items at their standards, against items whose
  authors' network accounts were new when they posted, a class that grew at some sites and never appeared at others.

## 3. The driving force

A strong solver forecasts each site's review items from the post-shock plateau, applies the queue standards and the class list, and
back-tests against the certified tables as the charter demands. The construction reproduces every pre-shock half-year to the hour, and
its post-shock misses are all low, concentrated at five sites, and look like rounding the council never explained. The rule behind them
is that an item whose author's network account was under 30 days old when the post was created carries a six-minute verification
allowance, unless it sits in the first-posts queue, whose standard already prices verification. Before the shock such items never
reached other queues. Afterwards, accounts created to post generated answers flooded the low-quality and close queues on Scriptwell and
Pyforge. Network-account age is reached only through the post's author and the account register; the site profile carries its own
creation date, which differs wherever an established user opened a new site profile, and using it reproduces 88 of 99 and moves the
split the wrong way.

## 4. The ladder

| Rung | Construction | Lands on (Scriptwell 2027 FTE) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Post-shock plateau of the dashboard's review items per site (all queues) × the network's average handle time, pool split pro rata | 19.8 (−12.0%) | The network's own dashboard, a clean regime-aware forecast, and finance's planning basis | The moderation standard's class list: review need counts the listed queues at their own standards, and suggested edits, a volunteer queue, are not on it |
| 1 | Class-list queues only, each at its handle-time standard | 18.8 (−16.4%) | The standard implemented queue by queue; reproduces 49 of 99 certified figures | The class list counts an item once, in the queue that resolved it |
| 2 | Plus the resolved-queue rule | 16.9 (−24.9%) | Implements every clause of the standard and reproduces 64 of 99 to the hour, including all 36 pre-shock half-years | The certified tables: 35 misses, every one low (4–36%), and the charter bars any method that misses one |
| 3 | **Decisive:** plus a six-minute allowance on items outside first posts whose author's network account was under 30 days old at posting, with new-account and established items forecast separately | **22.5** | — | — |

* **Figure shape.** Rungs 0 to 2 walk Scriptwell's figure down (−12.0%, −16.4%, −24.9%). The decisive rung reverses past rung 0, so the
  answer is the maximum feasible cell and every partial build under-allocates Scriptwell.
* **Partial correction priced (L3).** A solver who finds the new-account effect but ages accounts by the site profile reproduces 88 of
  99 and puts Scriptwell at 16.4 (−27.1%), further from the answer than rung 2: established users who left Scriptwell opened new profiles
  on DataBench, Cloudrack and Querywell, so the site-profile reading swells those sites' need instead. Proxying new accounts by reputation
  under 10 reproduces 52 of 99 (it charges the allowance to low-reputation veterans) and gives 18.1 (−19.6%).
* **Grid.** Grain (dashboard, class list, class list with resolved queue) × allowance class (none, reputation, site-profile age,
  network-account age) × forecast (trend through the break, post-shock plateau) = 24 cells. Every wrong cell sits at least 11% from 22.5.
  The nearest are the class list with the allowance but without the resolved-queue rule (25.0, +11.2%), which reproduces only 49 of 99
  so the charter refuses it, and the full construction on a trend fitted through the break (19.9, −11.6%), which projects 2023's collapse
  forward and is refuted by eight flat post-shock quarters.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The handle-time table lists queue standards only. No document mentions verification, account age or an allowance,
   and the charter refers to the certified tables without describing how they were built.
2. **Reproduction (Pattern B).** The full construction reproduces 99 of 99 certified figures to the hour; the best rival (site-profile
   age) 88 of 99; the queue-standard construction 64 of 99. Every rival's misses run low, so each also misses the corpus total
   (queue-standard by 7.4% overall and by 19.8% across the two hit sites' post-shock half-years). The rule is a construction, not a menu:
   its class needs a two-hop join and an age computed at posting, and the obvious age column sits on the wrong entity.
3. **No arithmetic symptom.** Items reconcile to the dashboard, resolved-queue counts reconcile to the log, and every rung's need totals
   tie to its own item counts.
4. **Not a row predicate.** The class is a property of a different entity (the author's network account) reached through the post, and
   its effect on the split runs through every site's share of a capped pool.
5. **The enumeration is arithmetic.** No column says "new account" or "verification"; the class is computed from two dates on two tables.
6. **No cutover date.** The shock is dated and steps question volume, which is the decoy the plateau forecast already absorbs. The
   new-account share rose over six quarters and has held flat since 2025Q1; nothing in it steps at a date.
7. **Survives deletion.** No wrong number exists to delete; every certified figure and every dashboard count is correct.

## 6. The calibration corpus

* **Form.** The council's certified need tables: 99 figures (nine sites × eleven half-years, 2021H1–2026H1), each in moderator hours
  with its queue breakdown, and the charter's reproduction clause.
* **What it certifies.** The class list and the resolved-queue rule (rungs 1 and 2 reproduce progressively more), and, through the 36
  pre-shock half-years, the queue standards themselves.
* **What it pins.** The allowance class and its size. Six minutes is the unique whole-minute allowance reproducing all 99 figures (five
  and seven each reproduce only the 64 figures with no allowance-bearing items), and any age threshold from 25 to 35 days selects the
  same items.
* **Twin pair.** In the queue breakdown, the low-quality queue at Querywell in 2024H1 and at Scriptwell in 2025H2 holds the same 4,120
  resolved items. Certified need is 206 against 412 hours (2.00×), because half of Scriptwell's items that half-year came from new
  network accounts and none of Querywell's did. No queue-level rule can reproduce both.
* **Resemblance points at the decoy.** By queue mix, Scriptwell's 2027 forecast most resembles its own pre-shock half-years, which the
  queue-standard construction reproduces exactly.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** Finance's cap: the 2027 pool is 120 FTE. The charter: the pool is allocated in proportion to each site's forecast
  review need for the year. The charter's clause: a need method that does not reproduce every certified figure may not be used. The
  moderation standard: the queues on the class list, each item counted once in the queue that resolved it, and each queue's handle-time
  standard.
* **Empirical pins.** The new-account class (network account under 30 days at posting, first posts excepted) and the six-minute
  allowance, from the certified tables. Each site's forward mix, from its post-shock plateau.
* **Voices.** Scriptwell's lead moderator: "Our questions fell the most, so we'll be cut hardest, and we know it." The head of
  community: "Review items are review items; the dashboard is what we've always planned on." The council's data steward: "The certified
  tables are just the standards applied; there's nothing hidden in them."
* **Licensed wrong basis.** The charter records that finance will present a split on dashboard review items at the network's average
  handle time, and that the council will hear it alongside its own.

## 8. Determinism by construction

* **Plateau.** Every site's established and new-account item volumes, by queue, have been flat since 2025Q1, so 6-, 12- and 18-month
  run rates give the same 2027 forecast.
* **Age threshold.** No reviewable post was created between day 25 and day 35 of its author's network account, so any threshold in
  that range classifies identically.
* **Allowance.** Six minutes is the unique whole-minute value reproducing all 99 figures.
* **Maturity.** The extract was taken 45 days after the last quarter closed and every item is resolved within 21 days of posting, so
  the last quarter is complete.
* **Rounding.** FTE are rounded to one decimal by largest remainder so the split sums to 120.0; Scriptwell's share is 18.75%, which puts
  its figure exactly mid-bin at 22.50.

## 9. Prompt sketch and deliverables

> Finance has capped next year's moderation pool at 120 FTE, and the council votes on how it splits across our nine sites at its
> December sitting. Scriptwell's moderators are bracing for the deepest cut because their questions fell the most. Give me each site's
> FTE to one decimal, with Scriptwell's figure in a sentence the chair can read into the minutes, and send `pool_split.xlsx` with the
> sheets below, a chart `need_by_site.png`, and a two-page `allocation_memo.pdf`.

* `pool_split.xlsx` — the need build and split for all nine sites, the answer-rate sheet (ask A) and the migration sheet (ask B).
* `need_by_site.png` — grouped horizontal bars of 2027 FTE per site under the four rung constructions, each construction's count of
  certified figures reproduced shown in the legend, the 120-FTE total noted, sites ordered by final FTE, and Scriptwell's bar annotated
  with its figure.
* `allocation_memo.pdf` — the committed split, Scriptwell's figure, and the reproduction record behind the need method.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the nine sites and each quarter of 2026, the share of new questions that received
  an answer within seven days. *Device:* answers posted while a question was closed are hidden and reinstated on reopen with their
  original timestamps, as the data guide documents; joining answers by timestamp alone counts them as prompt answers at four sites.
  Answer timing enters no part of review need.
* **Ask B (device-carried).** For each site, questions migrated in and out during 2026. *Device:* a migration creates a new post on the
  destination site and leaves a locked stub on the source, both carrying the original creation date, as the data guide documents;
  counting posts double-counts every migration. Migrated questions are reviewed in a volunteer queue that is not on the class list.
* **Ask C (validity).** For each of the four rung constructions, the number of certified figures it reproduces and Scriptwell's 2027
  FTE under it.
* **Decoupling.** Clearing the new-account allowance changes no figure in asks A or B.

## 11. Rubric arithmetic

9 sites × 4 quarters (ask A) + 9 sites × 2 directions (ask B) + 4 constructions × 2 (ask C) + 9 site allocations, Scriptwell's
committed figure and the split's 120.0 total + 5 named chart parts + 3 files ≈ 81 criteria.

## 12. World-building constraints

* Need before the allowance (rung 2 basis, FTE-equivalents): Pyforge 36, Scriptwell 22, DataBench 20, Kernelside 18, Cloudrack 16,
  Mobilewright 14, Querywell 12, Typeforge 10, Gamecraft 8. New-account share of reviewable items outside first posts from 2025Q1:
  Scriptwell 42%, Pyforge 22%, DataBench 8%, Cloudrack 6%, Kernelside 4%, and zero at the four smallest sites in every half-year; zero
  everywhere before the shock.
* Final shares: Pyforge 25.40%, Scriptwell 18.75%, DataBench 12.08%, Kernelside 10.34%, Cloudrack 9.43%, Mobilewright 7.64%, Querywell
  6.55%, Typeforge 5.46%, Gamecraft 4.36%.
* Scriptwell under rungs 0–2: 19.8 / 18.8 / 16.9; site-profile age 16.4; reputation proxy 18.1; trend through the break 19.9; class list
  with the allowance but no resolved-queue rule 25.0. Every wrong cell sits at least 11% from 22.5.
* Reproduction counts: 99 (full), 88 (site-profile age), 64 (rung 2), 52 (reputation), 49 (rung 1), 0 (rung 0).
* The twin queue cells are identical on item and resolved counts.
* Answer timing, closures and migrations touch no item on the class list.
