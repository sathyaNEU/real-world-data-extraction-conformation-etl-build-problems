# DA32 — Which factor-group structure a highway authority adopts to expand one-day counts, when each road's own hourly profile says which group it belongs to

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Policy & Education · local transport planning |
| Mirrors | Scaling a short sample to an annual total when units differ in usage rhythm (store footfall counters installed for a week, sampled device telemetry, app panels measured on a few days), where each unit's own intraday shape identifies its rhythm class |
| Decision shape | A structure the body adopts: the expansion-factor group structure for the authority's short counts, which then orders the resurfacing programme |
| Committed call | The group structure adopted, and the link it ranks first on annual vehicle-km |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · Pattern B (a reproduction clause over the counters' published annual flows), with a salient control that several structures pass at rung 2 |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution support |
| Measured traps engaged | #17 guesses an attribution the data can settle · #12 stops at the first control that passes · #3 stops at a close but inexact match |
| Calibration form | Published control set with a reproduction clause: 46 automatic counters with published annual average daily flows, and the guidance's clause that an expansion must return each counter's flow from its own 12-hour count |
| Driving force | Which factor group a road belongs to is recorded nowhere: the count register carries road category and region, and the published tables group factors that way. A count's own hourly profile fixes it exactly. Commuter roads carry 1.6 to 2.1 times the noon hour at 08:00, leisure routes 0.7 to 1.0, through routes 1.2 to 1.4, with nothing in between. Only that assignment returns every counter's published flow, and it more than doubles the annual flow of a leisure route counted on a November weekday. |

## 1. Situation

A county highway authority prioritises minor-road resurfacing by annual vehicle-km. It holds one 12-hour manual count for each of 30 links,
taken on single days spread across the year. The national guidance requires the authority to expand short counts with factors from
automatic counters and to adopt one factor-group structure for all of them. The pack holds the 30 counts with hourly breakdowns, the count
register, 46 automatic counters' hourly data and published annual flows, the national factor tables, the guidance, and the link network.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each count, each counter's hours, the published flows and the national tables. No stakeholder ranks
  the links and nothing reported is overturned. The difficulty is which group each road's count belongs to.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the regional body's note. Category-and-region factors, the published convention, still tie
  every regional total and still put the wrong link first.
* **Instrument repair.** Make every count and counter perfect: the register still carries no factor group, and a road's class is still a
  property of its rhythm, which only its own hours reveal.
* **Lens swap.** The naive expansion gives each link its category-and-region factor; the answer gives it the factor of the roads that move
  like it. The links are re-grouped into different populations, not re-weighted.

## 3. The driving force

A strong solver expands each count by month, weekday and 12-to-24-hour factors, checks the factors against the regional totals in the
national tables, and finds every total tied within 1%. It stops there. The guidance's clause is finer: an expansion must return each
counter's published flow from that counter's own 12-hour count, and category-and-region factors return 19 of 46. The misses are
leisure routes in commuter-dominated groups and the reverse. The hourly profile tells them apart without exception. A minor road busy at
08:00 is a commuter road whatever its category, and one that peaks at noon is a leisure route that will carry twice its weekday flow on
summer weekends. Grouped by that signature, all 46 counters reproduce. The B-road to the reservoir, counted on a Tuesday in November, then
becomes the heaviest link in the county.

## 4. The ladder

| Rung | Structure | Ranks first | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | No expansion: 12-hour counts × length | L07, harbour road (1.26× L02) | The counts as taken | The guidance: short counts are expanded before they are compared |
| 1 | One national factor set for all minor roads | L19, college link (1.24× L07) | The national tables applied evenly | The national tables' own regional totals miss by 6% to 14% under one set |
| 2 | Category × region groups, the published convention | L11, ring-road spur (1.25× L23) | Every regional total ties within 1% | The clause: it returns 19 of 46 counters' published flows |
| 3 | **Decisive:** three rhythm classes assigned by each count's 08:00-to-12:00 hourly ratio, factors from each class's counters | **L23, reservoir B-road (1.62× L11)** (5th of 30 on rung 0) | — | — |

* **Position table.** L23 ranks 5th on rung 0, 4th on rung 1 and 2nd on rung 2 (1.25× behind L11, its only second place), and leads only
  rung 3.
* **Discriminator dominance.** L11 carries 1.25× into rung 3. The class factors raise L23's flow by 1.62× (leisure, counted in November)
  and lower L11's to 0.80× (commuter, counted in October), an edge of 2.03×, against the 1.2 × 1.25 = 1.50 needed (1.35× headroom). The
  product, 2.03 / 1.25 = 1.62, is L23's final margin.
* **Partial correction priced (L3).** A solver who builds rhythm classes but assigns links by the nearest counter's class (a lookup by
  location) puts L23 with the commuter counter two miles away and ranks L11 first again, 1.25× L23. A solver who classifies by the
  noon-to-17:00 ratio puts the reservoir road, whose visitors leave around five, among the through routes and ranks L19 first, 1.18×
  L23. Neither half lands on L23.
* **Grid.** Eight constructions: no expansion, the national set, category × region by register, category × region by nearest counter,
  and rhythm classes assigned by nearest counter, by the noon-to-17:00 ratio, by count-size band, or by each count's own 08:00-to-12:00
  ratio. Seven rank L07, L19 or L11 first; only the last ranks L23 first.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The guidance says counts are expanded with factors "from counters on comparable roads". The register and every
   published table group by category and region. No document mentions hourly shape.
2. **Pattern B, reproduction against the best rival.** Rhythm classes return 46 of 46 counters within 0.3%. Category × region returns 19,
   the national set 11, and nearest-counter assignment 31. Rivals miss low on leisure counters and high on commuter counters, so the
   misses do not cancel by class. The assignment is a construction: each count's hourly ratio, then a three-way split on a gap the data
   draws, then class factors built from the counters that share it.
3. **No arithmetic symptom.** Regional totals tie under category × region, every hourly breakdown sums to its 12-hour total, and counters
   reconcile to their published days.
4. **Not a row predicate.** The class comes from a ratio within each count, and the factors are rebuilt from counters regrouped by the same
   ratio.
5. **The enumeration is arithmetic.** No column carries a rhythm class.
6. **No cutover date.** Count days are spread through the year and nothing steps.
7. **Survives deletion.** With every voice removed, the published convention still ties the salient totals and ranks L11 first.

## 6. The calibration corpus

* **Form.** 46 automatic counters in the county and its neighbours, each with a year of hourly flows, its published annual average daily
  flow, and its 12-hour count on the survey day.
* **What it certifies.** That expansion by month, weekday and hour coverage is the method, and that regional totals are a check.
* **The absolute split (O2).** Across counters and counts alike, the 08:00-to-12:00 ratio falls in 1.6 to 2.1, 1.2 to 1.4 or 0.7 to 1.0,
  with no site in either gap, so every cut inside the gaps returns the same classes.
* **Twin pair.** Counters C14 and C31 share category, region, count day and 12-hour total (2,140 vehicles). Their published flows are
  4,520 and 2,260 a day (2.0×); C14's hours peak at noon and C31's at 08:00.
* **Resemblance points at the decoy.** By category and region, L23 sits with the commuter counters around the ring road.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The guidance: one factor-group structure for all short counts, and an expansion must return each counter's published
  flow from its own 12-hour count within 1%. The planning memo: resurfacing priority is annual vehicle-km on the link.
* **Empirical pins.** The class boundaries and factors, from the counters.
* **Voices.** The highways manager: "Category and region is how the national tables group factors, and that's good enough for minor roads."
  The consultant: "With thirty counts, one national factor set is the honest choice."
* **Licensed wrong basis.** The guidance records that the regional transport body expands minor-road counts with category × region factors
  and will bring its rankings to the programme board.

## 8. Determinism by construction

* **Split.** Gaps of at least 0.2 separate the three classes, so the classes do not depend on the cut.
* **Factors.** Each class has at least nine counters, and month, weekday and hour-coverage factors are their arithmetic means as the
  guidance specifies; medians give the same ranking.
* **Vehicle types.** Heavy goods vehicles are under 4% on every link, and per-type expansion changes no rank.
* **Lengths.** From the network file, one length per link.

## 9. Prompt sketch and deliverables

> The programme board meets on the 9th and the highways manager wants our counts expanded the way the national tables group roads. Tell me
> which factor-group structure we adopt and which link it puts first for resurfacing, in a sentence for the board paper. Send
> `count_expansion.xlsx`, a chart `rhythm_classes.png`, and a one-page `structure_note.pdf`.

* `count_expansion.xlsx` — the expansion of all 30 links under the adopted structure, the condition sheet (ask A), the surface-age sheet
  (ask B) and the reproduction table (ask C).
* `rhythm_classes.png` — every counter and count plotted on its 08:00-to-12:00 ratio, coloured by class, with the two empty gaps shaded,
  the twin counters labelled, and L23 and L11 marked.
* `structure_note.pdf` — the adopted structure, the first link, and why the published convention fails the clause.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 30 links, the change in pavement condition index since the previous survey.
  *Device:* the survey moved to a new index version, and the condition handbook's conversion table maps old scores to new; comparing raw
  scores across versions misstates nine links.
* **Ask B (device-carried).** For each link, the surface age at the start of the programme year. *Device:* the asset register records
  resurfacing by scheme, and a scheme-to-link table assigns multi-link schemes; reading link rows alone misses 11 links resurfaced inside
  larger schemes.
* **Ask C (validity).** Counters reproduced and the first-ranked link under each of the four structures.
* **Decoupling.** Clearing the rhythm classes changes no figure in asks A or B.

## 11. Rubric arithmetic

30 links (ask A) + 30 links (ask B) + 4 structures × 2 (ask C) + the adopted structure, the first link and its vehicle-km + 5 named chart
parts + 3 files ≈ 79 criteria.

## 12. World-building constraints

* Hourly-ratio classes 1.6–2.1, 1.2–1.4 and 0.7–1.0 with empty gaps; 46 counters split 19 / 11 / 16.
* First links: L07 (1.26×), L19 (1.24×), L11 (1.25×), L23 (1.62×). L23 is 5th, 4th and 2nd on rungs 0 to 2.
* Counters reproduced: 46 / 31 / 19 / 11. C14 and C31 match on every register column.
* Condition-index versions and resurfacing schemes never touch a count, a counter or a length.
