# AD09 — Which stations stand for each fuel brand when the regulator measures the next levy pass-through, when the ownership flag is not who sets the price

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Economics · retail fuel markets and competition monitoring |
| Mirrors | Defining which units a company actually prices when the register's ownership flag says something else (first-party against third-party offers in marketplace price monitoring at Amazon, franchise against company-operated outlets in chain pricing studies, merchant price-competitiveness panels at Google Shopping) |
| Decision shape | A structure the body adopts: the brand-panel rule for pass-through monitoring (which stations form each brand's panel, at what price grain), scored on reproducing the pass-through the change log measured at every closed levy change |
| Committed call | The panel rule the monitoring board adopts for the 1 January 2027 levy change, and each of the seven brands' panel size on the latest eight weeks |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · the population a flag suggests against the population the governing rule defines (E33), identified by a quantity rather than a field, with two flawless price grains at the lower rung (E07) |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution support |
| Measured traps engaged | #5 takes the population a flag or filter suggests · #2 counts file rows instead of the real unit · #4 never tests its reading against the control |
| Calibration form | Change-log natural experiments: the four closed levy changes (1 January 2023 to 2026), each logged with every brand's measured 7-day pass-through |
| Driving force | The monitoring standard measures a brand's pass-through on the stations whose prices the brand sets, and the register's company-owned flag looks like that population. It is site ownership: some company-owned sites are leased to dealers who price for themselves, and some dealer-owned sites sell on agency terms priced by head office. Who sets the price shows only in behaviour, as stations whose changes follow the brand's reference station within minutes in nearly every change, and that population, re-drawn before each change, is the only one the log reproduces. |

## 1. Situation

A state competition authority's fuel-price monitor measures how each of seven major brands passes a carbon-levy change through to pump
prices. The levy rises again on 1 January 2027, and the monitoring board adopts the panel rule beforehand. The monitoring standard says a
brand's pass-through is measured on the stations whose prices the brand sets, and that a station's daily price is the time-weighted average
of the prices in force from 07:00 to 22:00. The pack carries the minute-stamped price-change log for 2,400 stations, the station register
(brand, company-owned flag, location), the brand history, and the change log of the four closed levy changes.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each price change, the register's brand and ownership fields, and the pass-through the authority
  measured at each closed change. The ownership flag is right about ownership. Nothing reported is overturned and no stakeholder read is
  corrected; the difficulty is that the standard's population is defined by who sets prices, which no field records.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the markets unit head's preference. The standard still names "the stations whose prices the brand sets", the
  register still offers a company-owned flag that seems to answer it, and the flag panel still reproduces only 22 of 28 logged figures.
* **Instrument repair.** No file the ladder uses is suspect: the register's company-owned flag is exact about ownership, a different
  attribute from who sets a price, the price-change log is minute-stamped and complete, and the logged pass-throughs are final. Perfect
  files leave rung 0 at 9 of 28, rung 1 at 15 and rung 2, the ownership panel, at 22. No row records who prices a station, and 61 stations
  changed terms during the log, so the timing panel drawn before each change is still needed for 28 of 28.
* **Lens swap.** The naive panel is the population of company-owned sites; the answer's panel is the population of stations priced by head
  office, which differs station by station and changes between levy dates: a different population, not the same stations under another
  lens.

## 3. The driving force

A strong solver reads the standard, takes each brand's stations, notices that averaging change records weights a price by how often a
station reprices, switches to time-weighted station-days as the standard defines, then restricts each brand to its company-owned sites
because the standard wants the stations the brand prices. It back-tests against the log and gets 22 of 28. Every step is competent. But a
company-owned site leased to a dealer is priced by the dealer, and a dealer-owned site on agency terms is priced by head office. That shows
only in the price-change log: head-office-priced stations change within two minutes of the brand's reference station in at least 96% of
its changes, and dealer-priced stations in at most 14%, with nothing between. The panel is a construction from timing, re-drawn on the
eight weeks before each change, because 61 stations moved between agency and dealer terms during the log. Only that panel reproduces all
28 logged figures.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Every station under each brand in the register, prices averaged over change records | The register-brand, record-average panel (9 of 28 logged figures) | One panel per brand from the register, prices straight from the log | The standard defines a station's daily price as the time-weighted average from 07:00 to 22:00, and frequent evening repricers swamp a record average |
| 1 | Every station under each brand, time-weighted station-days | The register-brand, time-weighted panel (15 of 28) | The standard's grain, every price weighted by the minutes it stood | The standard measures a brand on the stations whose prices it sets, and the register carries a company-owned flag |
| 2 | Company-owned sites within each brand, time-weighted | The ownership panel (22 of 28) | The field that names the brand's own stations, the standard's grain, and a much closer back-test | The change log: the six misses all fall at the three brands with the most leased and agency sites, and the twin brands Q and R differ 2× on identical ownership profiles |
| 3 | **Decisive:** stations whose changes follow the brand's reference station within two minutes in nearly every change, drawn on the eight weeks before each levy change, time-weighted | **The price-setting panel (28 of 28)** | — | — |

* **Partial correction priced (L3).** A solver who finds the timing construction but draws it once over the whole extract reproduces 25 of
  28, because 61 stations changed terms during the log; the misses land in the two changes either side of the moves.
* **Grid.** Price grain (record or time-weighted) × population (register brand, ownership flag, timing over the extract, timing before each
  change) gives eight cells. Record-averaged cells reproduce at most 13 of 28; time-weighted cells 15, 22, 25 and 28. Only time-weighting
  with the per-change timing panel reproduces all 28, and the nearest structure (25 of 28) needs the date dimension dropped.
* **What the structure changes.** On the latest eight weeks, five of the seven brands' price-setting panels differ from their ownership
  panels by at least 12% of their size, and brand R's by 46%.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The standard names "the stations whose prices the brand sets" and stops. No document mentions leases, agency
   terms, reference stations or timing.
2. **The corpus pins a construction, not a menu.** The timing panel reproduces 28 of 28 logged figures within 0.5 points; the ownership
   panel 22, and every miss at the three brands with the most mixed estates understates head office's pass-through, so the flag also fails
   on each brand's four-change mean. The reproducing rule is a construction: it exists only after each station's changes are matched to
   the reference station's, minute by minute, in a window before each change, and no field holds it.
3. **No arithmetic symptom.** Every panel is a clean subset of the register, every station-day time-weights to the log, and the ownership
   flag agrees with price-setting for 88% of stations.
4. **Not a row predicate.** It needs, per station and window, the share of the reference station's changes it follows within two minutes:
   a self-join on time within brand, a count, and a ratio.
5. **The enumeration is arithmetic.** Head-office stations follow in at least 96% of changes and dealers in at most 14%, so every cut from
   15% to 95%, and every lag from one to ten minutes, draws the same panel.
6. **No cutover date.** Stations move between terms one at a time across four years; no brand's series steps. The levy dates are the
   experiments, not the mechanism.
7. **Survives deletion.** With every voice removed, the answer and the difficulty are unchanged.

## 6. The calibration corpus

* **Form.** The authority's change log: the levy changes of 1 January 2023, 2024, 2025 and 2026, each with every brand's 7-day pass-through
  as the authority measured it (28 figures), and the price-change log around each.
* **What it pins.** The per-change timing panel, time-weighted, reproduces all 28; the ownership panel 22; the register panel 15 time-weighted
  and 9 record-averaged.
* **Twin pair.** Brands Q and R are identical on every register column at the 2025 change: station counts, company-owned share (60%),
  regional mix, motorway share, and their all-station time-weighted pass-through (78%). The log records 96% for Q and 47% for R (2.04×). Q's
  owned sites are its priced sites; R leases most of its owned sites to dealers and prices a set of agency sites the flag marks as dealer
  sites. Only the timing panel reproduces both.
* **Every rule exercised.** Two brands show a station switching to agency terms between changes; one brand's reference station itself was
  replaced, so the reference is tested; one change falls on a Sunday, so the 07:00 opening price is tested.
* **Resemblance points at the decoy.** R's register profile most resembles the four brands whose logged figures match their ownership
  panels.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The monitoring standard: a brand's pass-through is measured on the stations whose prices the brand sets. A station's
  daily price is the time-weighted average of the prices in force from 07:00 to 22:00, the price at 07:00 being the last change before it.
  The log's header: the 7-day pass-through is the panel's mean daily price over days 1 to 7 after the change less days −7 to −1, over the
  levy change including VAT.
* **Empirical pins.** The timing construction and its per-change window, from the log.
* **Voices.** The head of the markets unit: "The brand field has been our panel since the monitor began; I'd keep it." The industry
  association's economist: "A brand's own sites are where you see its pricing; the rest is noise."
* **Licensed wrong basis.** The standard records that the industry association measures pass-through on company-owned sites and will
  present its figures at the board.

## 8. Determinism by construction

* **Timing split.** The empty band between 14% and 96% makes the cut and the lag immaterial; every brand's reference station is fixed in
  the brand history.
* **Window.** Six, eight and ten weeks before each change draw the same panels, because no station changed terms within ten weeks of a
  levy date.
* **Grain.** The 07:00 convention is filed, and no station lacks a price at 07:00 on any day in the windows.
* **Maturity.** Stations must report each change within five minutes, and the extract is complete to 30 September 2026.

## 9. Prompt sketch and deliverables

> The levy rises again on 1 January and before then our board has to settle which stations stand for each brand when we measure
> pass-through. The head of the markets unit would keep the brand field as the panel, as we always have. Give me the panel rule we adopt
> and each brand's panel size, in a short paragraph for the board, with `panel_rule.xlsx` holding the sheets below, the chart
> `pricing_comovement.png`, and `board_paper.pdf`.

* `panel_rule.xlsx` — the panel build and each brand's size, the inspections sheet (ask A), the complaints sheet (ask B) and the structure
  back-test (ask C).
* `pricing_comovement.png` — for each brand, a histogram of stations' follow shares against the reference station with the empty band
  from 14% to 96% shaded, ownership-flag stations overlaid in a second colour, and the twin brands' panels annotated.
* `board_paper.pdf` — the adopted rule and why the brand field and the ownership flag are not it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 16 regional districts, weights-and-measures pump inspections in 2025 and the share
  failed. *Device:* a failed pump's re-inspection is a new row linked to the original by an inspection-series ID, as the inspectorate's
  guide documents. Counting rows overstates inspections and understates failure shares in the six districts with the most re-inspections.
  The price monitor never reads the inspection file.
* **Ask B (device-carried).** For each brand, complaints about displayed against charged prices in the last twelve months, per 100 stations.
  *Device:* a complainant who files online and then by phone is logged twice, the second entry carrying a "duplicate of" reference, per
  the complaints-handling guide. Counting entries double-counts about a fifth of complaints and reorders three brands.
* **Ask C (validity).** For each of the four rung structures, the logged figures it reproduces out of 28.
* **Decoupling.** Clearing the timing panel changes no figure in asks A or B.

## 11. Rubric arithmetic

16 districts × 2 (ask A) + 7 brands × 2 (ask B) + 4 structures (ask C) + the rule's population, grain and window and the seven panel sizes
+ 5 named chart parts + 3 files ≈ 68 criteria.

## 12. World-building constraints

* The ownership flag agrees with price-setting for 88% of stations; 61 stations changed terms during the log, none within ten weeks of a
  levy date.
* Follow shares are at least 96% or at most 14%, with no station between.
* Reproduction: 9 / 15 / 22 / 28 of 28; the whole-extract timing panel 25. Every ownership-panel miss understates head office's
  pass-through.
* Q and R are identical on every register column at the 2025 change; their logged figures are 96% and 47%.
* Five of seven brands' panels differ from their ownership panels by at least 12%; R's by 46%.
* Inspection re-runs and duplicate complaints never touch the price-change log or the register.
