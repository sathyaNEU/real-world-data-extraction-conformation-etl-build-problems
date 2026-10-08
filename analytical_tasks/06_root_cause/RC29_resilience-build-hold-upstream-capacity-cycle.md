# RC29 — Where next year's edge resilience build goes, when the region that still qualifies peaked in the quarter before its upstream's upgrade

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Supply Chain & Logistics · network transit and peering procurement |
| Mirrors | Edge-resilience spend at CDNs and cloud providers (Cloudflare, Google and Meta edge sites), where the quarter's outage league table mixes users' own power cuts, a provider's capacity cycle and chronic transit faults, and the build buys the next two years |
| Decision shape | Hold, forced by a blocking quantity: no region's forward avoidable outage minutes reach the build threshold |
| Committed call | Build in none of the five regions this cycle, because the best region's forward avoidable minutes are 1,500 a month against the programme's 1,800 |
| Gap · Pattern | Gap 1 (time) over Gap 2 (population) · Pattern A (past exceedance against forward yield), with the moderator in how a provider's capacity cycle treats a region, and the hold of Part 6.4 |
| Gate G mechanism | signal_vs_noise_or_hold, with forecasting |
| Measured traps engaged | #9 picks from the offered options when none passes · #13 validates on one population, applies to another · #12 stops at the first control that passes |
| Calibration form | Existing-book actuals: nine past local-peering builds in other countries, each with its basis quarter and 24 months of realised avoided minutes |
| Driving force | The detector's exposure score correctly measures last quarter, and its own label says so. The build buys the next 24 months. Once power cuts are classified correctly, River Delta is the only region still qualifying. It degrades only in the five months before its upstream Kestrel Transit adds capacity each October, and last quarter sat at the top of that cycle. Averaged over the build's two full cycles it avoids 1,000 minutes a month, and no region reaches the programme's 1,800. |

## 1. Situation

A content-delivery network serves one country through five regional edge sites. Last quarter's outages hit customers in all five. The
resilience programme funds one build a year: direct peering plus a local cache at a region's exchange point, contracted for 24 months.
The build keeps content flowing when a shared upstream transit provider degrades. It does nothing when users lose power or their own
networks withdraw routes. The programme approves a build only where it avoids at least 1,800 customer-weighted outage minutes a month over
its term. The outage detector ranks regions by last quarter's exposure, and the reliability director wants the build in Coastal South,
which tops it.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct: the detector's exposure scores, the routing, probing and telescope signals, the existing
  book's actuals and Kestrel's capacity notices. No one's reading of their own figures is overturned. The difficulty is that a correct
  measure of last quarter is not a measure of the build's two years.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the director's preference and every voice. The existing book still certifies carrying a correctly classified
  quarter forward, and that construction still names River Delta.
* **Instrument repair.** Make every signal perfect and every event perfectly classified. River Delta still degraded last quarter, and its
  forward minutes are still set by an upgrade cycle the quarter only samples at its peak.
* **Lens swap.** The naive read is last quarter. The answer is a 24-month term spanning two full upgrade cycles, a different moment.

## 3. The driving force

A strong solver discards raw exposure, because most of Coastal South's minutes were users' power cuts the build cannot touch. It
classifies events with the operations memo's signal rules, recalibrates those rules for regions with thin probing coverage, and carries
each region's avoidable minutes forward over the term. The existing book confirms the method on all nine past builds. That leaves River
Delta at 2,400 a month, comfortably over the bar. But River Delta's degradations are not fibre faults. They come from Kestrel's shared
capacity, which Kestrel adds every October. In each of the last three years River Delta degraded from May to September and not at all
from October to April. Last quarter is the top of the sawtooth. The 24-month term covers two full cycles at 1,000 a month. Capital Metro
degrades all year, but at 1,500. No region clears 1,800.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The detector's quarterly exposure score against the bar | Coastal South (4,800 a month, 1.23× the next) | The programme's own score, highest by a clear margin | The memo's signal rules: routing stayed up while probing and the telescope went dark, so Coastal South's minutes are users' power cuts |
| 1 | Events classified by the memo's thresholds, avoidable (shared-upstream) minutes carried forward | Inland Plateau (3,300, 1.38×) | Classified, cause-aware and avoidable-only | The telescope coverage table: Inland Plateau's sparse probing turns power cuts into apparent transit faults under thresholds validated on dense regions |
| 2 | Thresholds recalibrated by coverage tier, avoidable minutes carried forward | River Delta (2,400, 1.60×) | Calibrated, and it reproduces all nine past builds within 3% | Kestrel's capacity notices and three years of River Delta's months: degradation only from May to September, ending at each October upgrade |
| 3 | **Decisive:** forward avoidable minutes averaged over the build's two full upgrade cycles | **Hold.** Best region Capital Metro at 1,500, 83% of the bar | — | — |

* **Every candidate fails, and why.** Coastal South (350) and Inland Plateau (450) are mostly power cuts. River Delta (1,000) is seasonal to
  Kestrel's cycle. Northern Hills (700) is mixed. Capital Metro (1,500) degrades all year but too little.
* **The blocking quantity.** The maximum forward avoidable minutes across regions, 1,500, sits 17% under the 1,800 bar. It would become a
  pick if Capital Metro's year-round rate were 20% higher, or if Kestrel's cycle left River Delta degrading 9 months in 12.
* **Partial correction priced (L3).** A solver who sees the cycle but averages the last two quarters gets River Delta at 2,000 and still
  builds there. A solver who applies the cycle with the dense-region thresholds builds in Inland Plateau at 3,300. Neither half reaches the
  hold.
* **Grid.** Classification (exposure, dense, calibrated) × horizon (quarter, six months, full cycles) gives 7 cells. Only calibrated with full
  cycles holds. The others name Coastal South, Inland Plateau or River Delta, each over the bar by at least 11%.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The programme rule states the bar and the term. Kestrel's notices are capacity announcements. No document says River
   Delta's degradations follow them or that a quarter can sit at a cycle's top.
2. **Corpus blind for a computable reason.** *In every past build the avoidable degradations were fibre faults on long-haul routes, which
   occur at the same rate in every month, so the basis quarter's rate and the realised 24-month rate agree.* The book certifies carrying a
   quarter forward nine times of nine.
3. **No arithmetic symptom.** Signals, event windows, traffic weights and minutes reconcile on every rung, and the quarter's figures are
   exact.
4. **Not a row predicate.** The forward figure needs every month of three years classified under the calibrated rules, grouped by region and
   cycle position, and averaged over the term's months.
5. **The enumeration is arithmetic.** No field says "seasonal". The cycle is recovered from classified months.
6. **No cutover date.** Kestrel upgrades every October. The hold rests on a recurring cycle, not on a step at one date.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** Nine past local-peering builds in other countries, each with its basis quarter's signals and 24 months of realised avoided
  minutes.
* **What it certifies.** Classification and carrying forward. Coverage-calibrated thresholds reproduce realised avoidance at 9 of 9 builds
  within 3%. Dense-region thresholds reproduce 6 of 9 and overstate the three sparse regions by 40% to 110%. Raw exposure reproduces none.
* **What it is blind to.** Cyclic causes (property 2).
* **Twin pair.** Builds P-3 and P-7 are identical on basis-quarter exposure, dense-threshold avoidable minutes (2,400), region size and
  upstream count. They realised 2,350 and 1,180 avoided minutes a month (1.99×). Only the coverage-calibrated classification reproduces both.
* **Resemblance points at the decoy.** River Delta most resembles P-3, with dense coverage, two upstreams and a mid-sized market, and P-3
  realised its basis quarter almost exactly.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The programme rule: "A build is approved only where it avoids at least 1,800 customer-weighted outage minutes a month over
  its 24-month term." The build specification states that it protects against shared-upstream degradation only. The detector's export
  carries the line "Exposure describes the quarter's outages; it is not a forecast."
* **Empirical pins.** Coverage-tier thresholds come from the existing book. Cycle position comes from three years of classified months.
* **Voices.** Reliability director: "Coastal South had more outage minutes than anyone; that's where the money goes." Network planner:
  "Inland Plateau has the weakest transit in the country." River Delta site lead: "Kestrel degraded us every single week of the quarter."
* **Licensed wrong basis.** The programme rule records that the finance committee sizes builds on the detector's quarterly exposure score and
  will see this year's proposal on that basis.

## 8. Determinism by construction

* **Term and cycle.** The build is commissioned in January, so its 24 months are exactly two upgrade cycles. Any whole-cycle average gives
  River Delta 1,000.
* **Capital Metro.** Its quarter (1,500), last 12 months (1,500) and last 24 months (1,480) all sit under the bar, so no window choice makes
  it a pick.
* **Thresholds.** Coverage tiers are set by the telescope's published unique-source counts. Every region sits at least 30% inside its tier,
  so the tier is unambiguous.
* **Weights.** Customer weights are each region's share of request volume from the CDN's request logs, which the memo fixes.
* **Maturity.** Every event of the quarter closed before the extract, and no event straddles a month boundary.

## 9. Prompt sketch and deliverables

> Next year's resilience build goes to one region, or to none if none earns it, and I sign the commitment at the investment committee on
> Thursday. Our reliability director wants it in Coastal South. Tell me where it goes, or that it goes nowhere, in one sentence for the
> committee, with the avoided outage minutes a month you expect for each region, to the nearest 50. Send `build_case.xlsx`, a chart
> `region_minutes.png`, and a one-page `committee_note.pdf`.

* `build_case.xlsx` — the five regions on every construction, the transit sheet (ask A), the ticket sheet (ask B) and the existing-book
  back-test (ask C).
* `region_minutes.png` — small multiples per region of monthly avoidable minutes over 36 months by cause class. Each panel carries the 1,800
  bar as a labelled line, the 24-month forward average as a dashed level and Kestrel's October upgrades as markers, and the title states the
  call.
* `committee_note.pdf` — the call, the blocking quantity and what would turn it into a build.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each region, the monthly 95th-percentile traffic on each of its two upstream links last
  quarter. *Device:* flow exports sample 1 in N packets, with N set per router in the router inventory. Treating sampled bytes as totals
  understates the links on the two routers sampling at 1 in 4,096. The main call weights customers from request logs and never reads flows.
* **Ask B (device-carried).** For each region and month, distinct customer-reported outage incidents. *Device:* support merges duplicate
  tickets under a parent-ticket ID, as the ticketing dictionary documents. Counting tickets overstates incidents by about a third in the two
  largest regions.
* **Ask C (validity).** For each of the nine past builds, realised avoided minutes beside the figure your classification gives for its basis
  quarter.
* **Decoupling.** Clearing the cycle construction or the calibration changes no figure in asks A or B.

## 11. Rubric arithmetic

5 regions × 2 links × 3 months (ask A) + 5 regions × 3 months (ask B) + 9 builds (ask C) + the hold, the blocking quantity and each region's
forward figure + 5 named chart parts + 3 files ≈ 70 criteria.

## 12. World-building constraints

* Quarter exposure is 4,800 / 3,900 / 3,000 / 2,300 / 1,700 a month for Coastal South, Inland Plateau, River Delta, Northern Hills and Capital
  Metro. Dense-threshold avoidable minutes are 400 / 3,300 / 2,400 / 900 / 1,500, and calibrated 400 / 500 / 2,400 / 900 / 1,500.
* River Delta degrades at 2,400 a month from May to September and not at all from October to April, in each of the last three years. Forward
  figures are 350 / 450 / 1,000 / 700 / 1,500.
* Past builds: 9, all fibre-fault causes, 3 of them in sparse-coverage regions. P-3 and P-7 are identical on every basis-quarter column.
* Every non-hold cell clears the bar by at least 11%, and the hold's blocking quantity sits 17% below it.
* Sampling rates and ticket merges never touch outage signals, request-log weights or the existing book.
