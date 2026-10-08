# DA28 — Which catalogue structure a reinsurer adopts for its convective frequency study, when the treaty counts a loss as everything within 72 hours

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Economics · catastrophe loss trends and reinsurance pricing |
| Mirrors | Trend studies where the unit the business is charged on aggregates the recorded events (alerts versus the incidents a customer credit covers, fraud flags versus cases, support tickets versus one customer issue inside a window), so counting records shows a trend the business never pays for |
| Decision shape | A structure the body adopts: the catalogue structure (peril scope, normalisation and counting unit) the model governance committee approves for the frequency study |
| Committed call | The structure adopted, and the decade ratio of large losses it gives, to two decimals |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · the deciding comparison (measured #20): large losses as 72-hour sums of episodes, pinned by the parallel run's cells, with a mixed segment split through a join at rung 1 (measured #6) |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution support |
| Measured traps engaged | #20 leaves the deciding comparison unstated · #6 treats a mixed segment all one way · #3 stops at a close but inexact match |
| Calibration form | Parallel-run overlap: the 2014–2016 run in which the treaty administrator's catalogue of large losses was published beside the episode catalogue for 48 state × peril × year cells |
| Driving force | The research team counts storm episodes above $100 million. The treaty makes one loss of all damage within 72 hours from a convective outbreak anywhere in the territory, so an outbreak's episodes are one loss, and several episodes below the threshold can make one large loss. The earlier decade's storms came in multi-day outbreak sequences across neighbouring states, whose episodes sit below the threshold one by one and far above it together; the later decade's large losses are mostly single storms. Summed within 72 hours across the territory, the only construction that returns the administrator's published cells, the doubling is a 4% rise. |

## 1. Situation

A reinsurer's research team reports that convective storm episodes causing at least $100 million of property damage (2023 dollars)
nearly doubled between 1996–2005 and 2014–2023, and proposes a frequency loading at the January renewals. The model governance committee
must first approve the catalogue structure the trend is measured on. The pack holds the national storm event records with county damage
on one estimate basis for both decades, the tropical track file, county housing and price series, the treaty wording, the research memo,
the governance standard, and the 2014–2016 parallel run of the treaty administrator's catalogue.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each event record, each county series, each published cell. The research team's count is right on
  its basis and nobody's figure is overturned. The difficulty is what one large loss is.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the research team's note and both voices. Episodes normalised county by county, in treaty scope, still show a
  49% rise.
* **Instrument repair.** No file is suspect: the event records, the track file, the county series and the run's cells are complete and on
  one damage basis and one episode convention in both decades. A large loss is the treaty's unit, episodes summed within 72 hours, which no
  row claims to record. With every file perfect, rung 0 still returns 1.95, rung 1 1.75 and rung 2 1.49, and the 72-hour sums are still
  needed for 1.04.
* **Lens swap.** The naive count takes each episode as a loss; the answer chains episodes into outbreaks across states and days, a
  different population of losses with different members above the threshold.

## 3. The driving force

A strong solver puts every episode in 2023 dollars and today's housing, county by county from each episode's damage footprint, and applies
the treaty's named-storm clause through the track file so tropical flash floods leave the convective peril. The doubling shrinks to a 49%
rise, and every total ties. The parallel run disagrees: the administrator's published large-loss counts match episode counts in 12 of 48
cells. The treaty's hours clause makes one loss of all damage within 72 hours from a convective outbreak anywhere in the territory. The
earlier decade's large storms came as multi-day outbreak sequences across neighbouring states, three or four episodes each below $100
million and together far above it. The later decade's large losses are mostly single storms that cross the threshold alone. Summed within
72 hours across the territory, the only construction that returns all 48 cells, the earlier decade has 67 large losses against the later
decade's 70: a 4% rise and no frequency trend.

## 4. The ladder

| Rung | Construction | Adopts | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | National convective group, episodes over $100M in 2023 dollars and national housing exposure | Ratio 1.95 (41 to 80): a frequency trend | The research memo's own adjustments, applied cleanly | The treaty wording: flood within 72 hours of a named system's passage is named-storm peril |
| 1 | Treaty scope: flash floods inside a tropical system's footprint moved out through the track file (a mixed segment split by a join) | Ratio 1.75 (40 to 70) | The peril now matches the contract the loading prices | The county housing series: hail-belt metro fringes grew 2.1 to 2.6 times, against 1.3 nationally |
| 2 | Episodes normalised county by county on each one's damage footprint | Ratio 1.49 (47 to 70) | The textbook normalised-loss count, every total tied | The parallel run: episode counts return 12 of 48 published large-loss cells |
| 3 | **Decisive:** large losses as all episodes within 72 hours across the territory, summed on county-normalised damage, in treaty scope | **Ratio 1.04 (67 to 70)**: no frequency trend | — | — |

* **Figure shape.** Every correction walks the ratio down and the answer is the minimum cell. Rung offsets from the answer are +88%, +68%
  and +43%.
* **Partial correction priced (L3).** A solver who sums within 72 hours but normalises nationally lands at 1.23 (+18%). One who sums by
  calendar day lands at 1.17 (+12%), and one who sums within each state, splitting outbreaks that cross a border, at 1.15 (+11%).
* **Grid.** Scope (national group or treaty) × normalisation (national or county) × unit (episodes, calendar-day sums, 72-hour sums by
  state, 72-hour sums across the territory) = 16 cells. The nearest wrong cell is 72-hour sums by state, 1.15 (+11%).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The treaty defines an occurrence for recoveries; the research memo counts episodes; the governance standard asks
   for the parallel run's cells to be reproduced. No document says the frequency study counts occurrences or how episodes combine into
   one.
2. **Pattern B, a gate passed by a construction.** Territory-wide 72-hour sums reproduce all 48 published cells. Sums within each state
   reproduce 37, calendar-day sums 29 and episodes 12, and each rival misses the run's three-year totals. The construction is not a
   setting: episodes ordered in time, chained within 72 hours across states, summed on county-normalised damage, then thresholded.
3. **No arithmetic symptom.** Episode damage ties to county event rows, county shares to episode totals, and the run's cells to their
   damage totals under every unit.
4. **Not a row predicate.** A large loss is a chain of episodes across states and days; no episode's row decides whether it belongs to one.
5. **The enumeration is arithmetic.** No column links episodes into outbreaks or marks a large loss.
6. **No cutover date.** Both decades are recorded on one damage basis and one episode convention, and nothing steps.
7. **Survives deletion.** With every voice removed, county-normalised episodes still show a 49% rise.

## 6. The calibration corpus

* **Form.** The parallel run, 2014–2016: the treaty administrator's large-loss counts published beside the episode catalogue for 48 cells
  (10 states × the perils present × 3 years), with damage totals.
* **What it certifies.** The damage basis and the county normalisation, which both catalogues share: every cell's damage total ties under
  either.
* **What pins the structure.** The reproduction gate: only territory-wide 72-hour sums return every cell.
* **Twin pair.** Two 2015 hail cells in neighbouring states match on episodes (four above $100 million), normalised damage, season and
  peril. Their published large-loss counts are 4 and 2 (2.0×): the second cell's four episodes fell as two pairs within 72 hours.
* **Resemblance points at the decoy.** Cells of the same peril and year look alike on every episode column, which invites counting
  episodes.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The governance standard: the frequency study counts large losses on the catalogue structure the committee approves, and
  a structure must reproduce every published cell of the parallel run. The treaty wording carries the named-storm clause and the hours
  clause. The research memo fixes 2023 dollars and housing-unit exposure.
* **Empirical pins.** The counting unit and its window, from the run's cells.
* **Voices.** The research lead: "Twice the large storms is twice the hazard; the signal is in the counts." The pricing actuary: "An
  episode is how the industry has always counted a storm."
* **Licensed wrong basis.** The governance standard records that the broker's analytics team trends the national convective group in real
  dollars and will present that view at the renewal meeting.

## 8. Determinism by construction

* **Normalisation.** Each episode's county damage shares come from its county event rows, and the housing and price series cover every
  county in both decades.
* **Windows.** Windows are anchored at each loss's first episode, and no episode lies within 6 hours of a window boundary, so every
  anchoring gives the same losses.
* **Threshold.** No normalised episode or 72-hour sum lies within 3% of $100 million.
* **Named-storm clause.** Footprint and timing come from the track file, and every flash-flood episode is either inside a footprint within
  72 hours or at least 10 days clear.

## 9. Prompt sketch and deliverables

> The committee approves the catalogue structure for the convective frequency study before anyone prices a loading, and research tells me
> the big storms have doubled. Tell me which structure we adopt and the decade ratio of large losses it gives, to two decimals, in a
> sentence for the minutes. Send `catalogue_structure.xlsx`, a chart `decade_ratio_by_structure.png`, and a one-page
> `committee_paper.pdf`.

* `catalogue_structure.xlsx` — the catalogue build, the tornado sheet (ask A), the coverage sheet (ask B) and the parallel-run table
  (ask C).
* `decade_ratio_by_structure.png` — decade ratios under the four rung structures as a descending staircase, with each structure's
  reproduced-cell count labelled, one outbreak sequence drawn as a 72-hour timeline, the twin cells inset and the adopted structure marked.
* `committee_paper.pdf` — the adopted structure, its ratio, and why each rival fails the gate.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 10 states, tornado episodes rated 2 or higher in each decade. *Device:* the rating
  scale changed in 2007, and the dictionary's crosswalk maps the old scale to the new one. Counting the raw ratings mixes scales and
  shifts six states' later-decade counts.
* **Ask B (device-carried).** For each state and decade, the share of episodes carrying a property damage estimate. *Device:* the export
  format note distinguishes "0.00K" (surveyed, no damage) from blank (not surveyed); treating both as zero inflates coverage in the earlier
  decade. Every large-loss episode carries an estimate.
* **Ask C (validity).** Cells reproduced and the decade ratio under each of the four rung structures.
* **Decoupling.** Clearing the 72-hour sums changes no figure in asks A or B.

## 11. Rubric arithmetic

10 states × 2 decades (ask A) + 10 × 2 (ask B) + 4 structures × 2 (ask C) + the adopted structure, its ratio and the two decade counts + 5
named chart parts + 3 files ≈ 60 criteria.

## 12. World-building constraints

* Large losses: rung 0 41 → 80; rung 1 40 → 70; rung 2 47 → 70; rung 3 67 → 70. Partial cells 57 → 70 (1.23), 60 → 70 (1.17) and 61 →
  70 (1.15).
* Earlier decade: 31 multi-day outbreak sequences crossing state lines; later decade: 9. Hail-belt metro fringes grew 2.1× to 2.6× in
  housing, nationally 1.3×.
* Cells reproduced: territory-wide 72-hour sums 48, by state 37, calendar-day sums 29, episodes 12. The twin cells match on every episode
  column.
* Rating-scale changes and blank estimates never touch an episode of $100 million or more.
