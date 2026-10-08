# DA08 — Which property gets the performance squad, when its fixes only ever moved page loads whose largest element was its own image

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Product Analytics · web performance across a publishing portfolio |
| Mirrors | Placing a scarce performance team where its levers have worked before, when the levers only reach first-party assets (Core Web Vitals work at publishers and retailers whose largest element is often a third-party player or ad, app-startup teams at Meta and Google whose fixes only touch first-party code paths) |
| Decision shape | Which of N gets one scarce thing: the performance squad's next quarter, for one of six properties |
| Committed call | The property, and the page loads a month the squad moves into the good LCP band, to the nearest hundred thousand |
| Gap · Pattern | Gap 2 (population) over Gap 3 (objective) · Pattern E (yield conditioned on the host of each load's largest element), with E20 (origins that reach their property only through the canonical-host chain) below it |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #25 assumes an effect the log could measure · #13 validates on one population, applies to another · #18 joins only on the visible key · #6 treats a mixed segment all one way |
| Calibration form | Change-log natural experiments: the squad's eleven past engagements, each logged with its levers and start month, with CrUX histograms and RUM LCP attribution before and after |
| Driving force | The squad's levers (image transforms, preload, fetch priority, responsive sizes) act on images the group's own CDN serves. In all eleven past engagements, non-good loads whose largest element came from the first-party image CDN moved to good at 39% to 43%, and loads whose largest element was a third-party player, ad or embed moved at 0% to 1%. The pooled 27% and the device split (14% mobile, 38% desktop) are true of the log and apply to no property. The host of each load's largest element sits only in RUM attribution, through the CDN host list. |

## 1. Situation

A media group's web platform team has one performance squad for the quarter starting 5 January. Its charter sends the squad to the
property where it will move the most monthly page loads into the good Largest Contentful Paint (LCP) band. The shortlist is the group's
six largest properties: Courier (news), Matchday (sport), Hearth (home), Ledger (finance), Trailhead (travel) and Pantry (food). The pack
holds the CrUX histograms by origin and device, the portfolio origin list (one www origin per property), the brand registry and the
domains runbook, the RUM beacon extract with LCP attribution, the CDN host list, and the squad's change log of eleven past engagements.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the CrUX histograms, the origin list, RUM attribution and the change log's measured results.
  Matchday's mobile LCP really is the group's worst, and the squad's pooled yield is a true average of what it did. Nobody's reading of
  their own numbers is overturned. The difficulty is which of each property's slow loads the squad can actually move.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the head of platform's view and the advertising team's licensed basis. Non-good loads are still a clean
  ranking quantity, and the change log still offers a pooled yield and a device split to scale them by.
* **Instrument repair.** Perfect CrUX and RUM change nothing: they already measure every load. The yield of a lever on a load depends on
  who serves that load's largest element, which is a property of the page, not a better reading of its timing.
* **Lens swap.** The two reads count different populations. Matchday's 77 million non-good loads a month are mostly video-player LCP the
  squad cannot touch. Trailhead has 33 million non-good loads whose largest element is the group's own image.

## 3. The driving force

A strong solver merges each property's CrUX histograms with traffic weights, folds in the AMP and guides origins the brand registry ties
to each property, and scales non-good loads by the squad's yield from its own change log. Noticing that past mobile engagements did
worse, it conditions the yield on device, which is the obvious segment, and the log supports it. That names Hearth, a desktop-heavy
property. But the device gradient is composition. The squad's levers act only on images the group's CDN serves, and past mobile slow
loads were mostly third-party video players. Join each RUM beacon's LCP resource to the CDN host list and every engagement splits
absolutely: 39% to 43% of first-party-image loads moved, and 0% to 1% of third-party loads. Within each host class, device makes no
difference. Read through that join, Trailhead's guides pages are almost entirely first-party photography, and Trailhead moves 1.7 times
more loads than anyone else.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Non-good LCP loads a month on each property's listed www origin, from merged CrUX histograms | A, Courier (55M, 1.45× Hearth) | Histograms merged by traffic, not p75s averaged; the portfolio list's own origins | The domains runbook: AMP-cache, m-dot and guides origins roll up to properties through the brand registry's canonical-host chain |
| 1 | Same, with every origin the canonical-host chain assigns to the property (E20) | B, Matchday (77M, 1.22× Courier) | The property's full traffic, and the worst mobile numbers in the group | The change log: no engagement moved more than 43% of non-good loads, so raw volume is not yield |
| 2 | Non-good loads × the change log's yield by device (14% mobile, 38% desktop) | C, Hearth (14.6M, 1.21× Matchday) | The squad's own measured effect, refined by the obvious segment | RUM attribution through the CDN host list: in every engagement, yield was 41% on first-party-image loads and 0% on third-party ones, whatever the device |
| 3 | **Decisive:** non-good loads split by LCP host class (RUM × CDN host list) × the class yields | **D, Trailhead (13.7M, 1.72× Pantry)** (5th of 6 on rung 0) | — | — |

* **Position table.** Trailhead ranks 5th on rung 0, 4th on rung 1 and 4th on rung 2, and leads only rung 3. Each rung's leader beats its
  runner-up by at least 1.21×.
* **Discriminator dominance.** Hearth carries 1.47× (14.6M against 9.9M) into rung 3. On the decisive axis, Trailhead's yield rises
  1.38-fold (0.248 to 0.341) and Hearth's falls to 0.48 of its rung-2 value (0.356 to 0.172), an edge of 2.85×. That clears 1.2 × 1.47 = 1.77. The
  final margin over Hearth is 13.7M against 7.1M (1.93×).
* **Partial correction priced (L3).** A solver who conditions on LCP host but reads host shares from the www origin's RUM only (Trailhead
  0.70 instead of 0.83, and none of its guides traffic) names Pantry (7.4M against 6.0M). The half insight lands on another decoy.
* **Grid.** Origins (listed or chained) × yield (none, pooled, by device, by host) gives 8 cells. They name Courier, Matchday, Hearth and
  Pantry, and only chained origins with host yields name Trailhead.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The squad's charter lists its levers. The change log records levers and outcomes. No document says the levers
   only act on first-party CDN images, or that a load's yield depends on its LCP host.
2. **The corpus pins the conditioning only through a join.** The change log's own columns (property, device, CMS, before p75, levers)
   show a device gradient and no host split. The host lives in RUM attribution (resource URL), which becomes "first-party image" only
   through the CDN host list, and nothing in the log points to it.
3. **No arithmetic symptom.** Merged histograms reconcile to CrUX totals, origins reconcile to the registry, and the log's pooled and
   device yields reproduce exactly from its own rows.
4. **Not a row predicate.** Each property's first-party share is built from RUM beacons joined to the host list, weighted to non-good
   loads by origin, and then multiplied by a yield recovered from the log's split.
5. **The enumeration is arithmetic.** No column says "touchable". The share comes from 14 million beacons and a host list.
6. **No cutover date.** The engagements are spread over three years, with no step in any series that the host split explains.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, the device gradient still invites itself as the
   refinement.

## 6. The calibration corpus

* **Form.** The squad's eleven engagements (2023–2026), each with property, levers shipped, start month, CrUX histograms for the three
  months before and after, and RUM beacons with LCP attribution for the same windows.
* **What it pins.** The absolute split. Across the eleven engagements, first-party-image loads moved to good at 39% to 43% (41% overall),
  and third-party loads at 0% to 1%. Within each class the mobile and desktop yields differ by under two points. The pooled 27% and the
  device yields (14% and 38%) reproduce exactly from the log and transport to nothing.
* **Twin pair.** Engagements E-04 and E-09 are identical on every logged column: property size band, device mix, CMS, before-p75 LCP
  and levers shipped. Their yields were 36% and 18% (2.0×), because 88% and 44% of their non-good loads had first-party-image LCP. Only
  the RUM host join separates them.
* **Resemblance points at the decoy.** Hearth's CrUX profile (desktop-heavy, mid-range LCP) most resembles the three engagements with the
  highest pooled yields.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The squad's charter: "The squad spends each quarter on the property where it will move the most monthly page loads
  into the good LCP band." The thresholds file: good LCP is 2.5 seconds or less. The domains runbook documents the canonical-host chain
  as practice.
* **Empirical pins.** The class yields (41% and 0%), from the change log through RUM.
* **Voices.** The head of platform: "Matchday's mobile numbers are the worst in the group. That's where users are suffering." The squad's
  tech lead: "Our results are in the log, and the mobile ones were always harder."
* **Licensed wrong basis.** The charter records that the advertising team ranks properties on non-good mobile loads and will present
  that list at the portfolio council.

## 8. Determinism by construction

* **Yield window.** Engagement yields measured over the second or the third month after start agree within one point, so the window is
  no fork.
* **Host list.** Every LCP resource URL resolves to one host on the CDN host list or off it. Text-node LCP (no resource) is 2% of loads
  and behaves as first-party under every lever.
* **Origins.** Each origin has exactly one canonical host, and each canonical host one property. AMP-cache URLs carry the canonical host
  in their path.
* **Rounding.** The committed figure (13.66 million) sits clear of a hundred-thousand boundary.

## 9. Prompt sketch and deliverables

> The performance squad starts its next quarter on 5 January, and I have to tell the portfolio council which of our six biggest
> properties it goes to. Our head of platform thinks Matchday, since its mobile numbers are the worst in the group. Name the property and
> the page loads a month the squad will move into the good band, to the nearest hundred thousand, and send `squad_case.xlsx` with the
> sheets below, plus `squad_yield.png`.

* `squad_case.xlsx` — the build per property and origin, the four rung constructions (ask C), the viewability sheet (ask A) and the
  newsletter sheet (ask B).
* `squad_yield.png` — stacked bars of each property's non-good loads split into first-party-image and third-party LCP, the log's 41% and
  0% class yields annotated, the loads the squad would move marked on each bar, the chosen property highlighted, and E-04 and E-09 as an
  inset.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** Viewable ad impression rate for each property in each month of Q3. *Device:* campaigns measured
  by two verification vendors appear once per vendor in the ad-server export, flagged by vendor code, as the ad-ops guide documents.
  Counting both rows double-counts 14% of impressions and misstates 13 of the 18 rates.
* **Ask B (device-carried).** Newsletter click-through rate per property in each of the last four quarters. *Device:* corporate mail
  scanners pre-fetch every link, logged with a scanner user-agent class in the tracker, as the email platform guide documents. Counting
  them inflates click-through by 30% to 70%, and most for Ledger's business readers.
* **Ask C (validity).** Monthly loads moved for each property under each of the four rung constructions.
* **Decoupling.** The ad server and the email tracker share no row with CrUX, RUM or the change log. Clearing the host conditioning
  changes no figure in asks A or B.

## 11. Rubric arithmetic

6 properties × 3 months (ask A) + 6 × 4 quarters (ask B) + 6 properties × 4 constructions (ask C) + the committed property, its loads
moved and its margin + 5 named chart parts + 2 files ≈ 76 criteria.

## 12. World-building constraints

* Non-good loads (millions a month), www origin and chained additions: Courier 55 + 8, Matchday 31 + 46, Hearth 38 + 3, Ledger 26 + 3,
  Trailhead 21 + 19, Pantry 20 + 2. Mobile shares: 0.88, 0.93, 0.10, 0.60, 0.55, 0.65.
* First-party-image shares of non-good loads: Courier 0.20, Matchday 0.22, Hearth 0.42, Ledger 0.40, Trailhead 0.70 on www and 0.98 on
  guides (0.83 overall), Pantry 0.90 on www and 0.70 elsewhere.
* Rung leaders are Courier, Matchday, Hearth and Trailhead. Trailhead lands at 13.7M against Pantry 8.0, Hearth 7.1 and Matchday 6.9.
* The log's eleven engagements reproduce the 41% and 0% class yields, the 27% pooled yield, and the 14% and 38% device yields. E-04 and
  E-09 are identical on every logged column.
* The ad server and the email tracker touch no CrUX or RUM row.
