# FC02 — How to split a capped summer firm-capacity block across four zone books, when one zone's new customers are cold stores that run flat through the peak hour

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Economics · retail electricity and energy risk |
| Mirrors | Splitting a capped capacity pool across regions when next season's growth draws on the pool at a different hour from the users the conversion was fitted on (cloud region capacity when always-on inference tenants join a book of daytime web tenants, CDN egress when a flat streaming partner joins peaky page traffic, fulfilment labour at Amazon when steady replenishment orders join consumer orders) |
| Decision shape | An allocation under a cap: 400 MW of summer firm capacity placed in 5 MW lots across four zone books |
| Committed call | The four zone allocations (Coast, North Central, South Central, Far West), adding to 400 MW, for the June–September book |
| Gap · Pattern | Gap 2 (population) over Gap 1 (time) · S8, the pooled coincidence factor is correct and applies to no premise in the new book, with finer controls separating the replay constructions |
| Gate G mechanism | forecasting, with binding_constraint support |
| Measured traps engaged | #13 validates on one population, applies to another · #12 stops at the first control that passes · #4 never tests its reading against the control |
| Calibration form | Existing-book actuals: ten closed summers of the book's settled hourly load by zone, premise-level interval data for existing premises, and last year's risk report with its replay table |
| Driving force | The book's coincidence factor, its load in the system's peak hour per kW of its premises' maximum demand, reproduces all forty closed zone-summers (0.45 in North Central), because the book never held a load that runs flat through a summer afternoon. This summer's North Central growth includes 31 refrigerated distribution centres with 150 MW of maximum demand, and a cold store draws 90% of its maximum demand in the peak hour. No enrolment column says how a premise uses power. The tariff class sits in the distribution utility's premise file, joined by ESI ID, and the class's factor in the interval data of the book's fourteen existing cold stores. |

## 1. Situation

A retail electricity provider serves homes and businesses in four weather zones. Its risk committee has capped summer firm capacity (call
options for June–September) at 400 MW. The risk policy places the block in 5 MW lots, each on the zone book with the largest remaining
uncovered 1-in-10 summer exposure: the coming summer's book load in the system's peak hour at the 1-in-10 summer, less the book's existing
hedges. This spring the company signed an exclusive supply deal with a cold-storage developer whose 31 refrigerated distribution centres
in North Central are energised before June.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the settled book load, the premise interval data, the enrolment file, the hedge book, the
  distribution utility's premise file and last year's risk report. No one's claim about their own numbers is overturned. The difficulty is
  that the premises being forecast are not the premises the factor was fitted on.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the trading head's view and the lenders' basis. The book's own per-kW replay still reproduces 40 of 40 closed
  zone-summers and still carries the pooled factor onto the cold stores.
* **Instrument repair.** Suspect: the enrolment file, whose 2,300 North Central amendment rows sit beside the rows they supersede. Repair
  it to one row per premise. Rung 0 still levels settled loads to 165 · 55 · 150 · 30, rung 1 becomes rung 2's 150 · 135 · 115 · 0, and
  the pooled factor still carries the book's 0.45 onto the cold stores, so the class replay is still needed for 125 · 180 · 95 · 0. No
  other file is suspect: the maximum-demand field records each premise's own maximum, a different attribute from its load in the
  system's peak hour, and the premise file gives every premise a tariff class. A premise that has never seen a summer has no peak-hour
  load for any instrument to record.
* **Lens swap.** The naive read and the answer are different populations: the book that lived through the closed summers against the
  coming summer's book, in which cold stores that did not exist a year ago hold 12% of North Central's maximum demand.

## 3. The driving force

A strong solver rejects the raw settled loads, builds a per-kW replay that ties last year's report to the megawatt, de-duplicates the
enrolment file and multiplies by the coming book's maximum demand. Every step is right for the book that produced the history. The
coincidence factor is a mixture. A home or a shop draws about 45% of its maximum demand in the system's peak hour, because its own peak is
spread across the afternoon and evening; a cold store's compressors run flat out through the hottest hours and draw 90%. The mixture held
still for ten summers because the book's cold stores never reached 1% of its maximum demand, so the pooled factor and the class factors
reproduce the corpus equally well. The 31 new distribution centres bring 150 MW of maximum demand to North Central. Their load type is on
no enrolment row. It comes from the distribution utility's premise file, where each premise carries its tariff class, and the class's
factor comes from the interval data of the book's fourteen existing cold stores, joined the same way.

## 4. The ladder

| Rung | Construction | Lands on (Coast · NC · SC · FW, MW) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The policy's words on the book's own settled data: P90 of each zone book's settled load in the system's peak hour across ten summers, less hedges, levelled | 165 · **55** · 150 · 30 | It applies the 1-in-10 definition literally, and the most recent summer matches last year's report exactly | Last year's replay table: 36 earlier-summer cells at last year's book that settled loads of a smaller book cannot reproduce |
| 1 | **E16 (finer controls):** per-kW replay: each summer's settled coincidence factor applied to the coming enrolled book's maximum demand, pooled per zone | 140 · **150** · 110 · 0 | It reproduces all 40 cells of the replay table to the MW, not just the salient recent summer | The enrolment file's ESI IDs: 2,300 North Central rows are amendments restating a premise already enrolled, and the amendment supersedes |
| 2 | Hygiene: the same replay on the de-duplicated book, which now ties to the distribution utility's switch confirmations | 150 · **135** · 115 · 0 | Clean counts, a validated model, every reconciliation passing | The premise file: the 31 new premises are in the high-load-factor tariff class, 150 MW of maximum demand, against under 1% of the book |
| 3 | **Decisive:** class replay: each premise at its own tariff class's factor in the system's peak hour, the cold stores at the high-load-factor class's 0.90, then levelled | **125 · 180 · 95 · 0** | — | — |

* **Figure shape.** North Central's block is graded with the other three. It rises from 55 to 150 at rung 1, falls to 135 on clean counts,
  and the decisive rung lifts it to 180 (−69%, −17% and −25% at rungs 0–2). The only cells above the answer over-apply the cold-store
  factor.
* **Separation.** The answer is graded as four blocks, not a name. The class factor is 2.0× the pooled factor on 12% of North Central's
  maximum demand, which lifts its exposure from 277.5 to 345 MW and the water level from about 142 to 165 MW. Every block moves: Coast
  150 → 125, North Central 135 → 180, South Central 115 → 95, Far West 0. No other grid cell puts North Central within 16% of 180.
* **Partial correction priced (L3).** A solver who sees that the new premises differ but gives every new North Central premise the
  cold-store factor places 215 MW there (+19%). One who calibrates by the visible maximum-demand band, giving the cold stores the
  large-commercial band's 0.52, places 140 MW (−22%), further away than rung 1. The class factor on the file before de-duplication places
  210 MW (+17%).
* **Grid.** Load basis (settled, per-kW replay) × counts (enrolled, de-duplicated) × new-premise factor (pooled, class-calibrated, every
  new premise at the cold-store factor) gives 7 distinct North Central cells: 55, 150, 210, 250, 135, 180 and 215 MW. The nearest wrong
  cells are 150 (−17%), 210 (+17%) and 215 (+19%), each one omission or one over-application away. The nearest two-error path, the
  maximum-demand band on the file before de-duplication, lands at 160 (−11%).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The policy defines exposure and the lot rule. No document says the new premises use power differently, or that
   the coincidence factor depends on how a premise uses power.
2. **Corpus blind for a computable reason.** *In every closed summer each zone book's high-load-factor share of maximum demand was under
   1%, because the company first signed cold-storage sites this spring.* The pooled and class replays both reproduce 40 of 40
   zone-summers within 0.5%.
3. **No arithmetic symptom.** De-duplicated counts tie to switch confirmations, replayed loads tie to settlement, and the lots sum to 400
   under every rung.
4. **Not a row predicate.** No enrolment row carries a load type. The class comes from another party's premise file and the class
   factor from existing premises' interval data in ten summers' peak hours, recombined at each zone's coming mix and levelled against
   hedges across all four zones.
5. **The enumeration is arithmetic.** The class exposure is a weighted sum of replayed factors over ten summers. No column holds it.
6. **No cutover date.** The developer deal stepped no closed series; the new premises have no summer yet.
7. **Survives deletion.** No wrong number exists to delete. Without the voices and the lenders' basis, rung 1 is the natural start.

## 6. The calibration corpus

* **Form.** Ten closed summers of the book's settled hourly load by zone, premise-level interval data for existing premises, and last
  year's risk report with its 40-cell replay table (each zone's ten summers replayed at last year's book).
* **What it certifies.** The per-kW replay: 40 of 40 replay-table cells to the MW. Raw settled loads reproduce only the 4 most-recent-summer
  cells, the salient control that every construction passes.
* **What it is blind to.** The peak-hour draw of premises that have never seen a summer (above).
* **Twin pair.** North Central premises P-1184 and P-2207 are identical on every enrolment column: 2.4 MW maximum demand, the same plan,
  deposit class, meter type and premise age band. In the 1-in-10 summer's peak hour they drew 2.16 and 1.06 MW (2.0×), because P-1184 is a
  cold store and P-2207 a dry-goods distribution warehouse. The class lives in the distribution utility's premise file. The pooled factor
  gives the twins one figure, 1.08 MW, and only the class factors reproduce both.
* **Resemblance points at the decoy.** The cold-storage enrolments resemble the book's large commercial customers on every enrolment
  column (maximum-demand band, plan, deposit class), which are the customers the pooled factor fits.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The committee minute: the summer block is 400 MW. The risk policy: summer exposure is the coming summer's book load in
  the system's peak hour at the 1-in-10 summer (the 90th percentile across the ten most recent summers' weather, inclusive
  interpolation), less hedges, and lots of 5 MW go one at a time to the largest remaining exposure. The enrolment dictionary: an
  amendment carries the original ESI ID and supersedes it.
* **Empirical pins.** Class factors, from existing premises' interval data joined to the premise file. The new premises' classes, from
  the premise file.
* **Voices.** The load-planning lead: "A megawatt of demand is a megawatt of demand, whoever signs for it." The head of trading: "Coast
  has always been where our summer risk sits."
* **Licensed wrong basis.** The risk policy records that the company's lenders review summer exposure on the zone-share basis (the book's
  energy share of each weather zone's published 1-in-10 peak) and will see it in the covenant pack.

## 8. Determinism by construction

* **Summer and clock.** June–September in Central Prevailing Time, hour-ending, with each summer's system peak hour as the transmission
  operator settles it. No peak hour falls on a daylight-saving day.
* **Class factor.** The fourteen existing cold stores drew 88–92% of maximum demand in every closed summer's peak hour. Their 90th
  percentile is 0.90 under the policy's inclusive convention and 0.89–0.91 under the others, and every factor from 0.88 to 0.92 gives the
  same lots.
* **Coverage.** Every enrolled ESI ID appears in the premise file with a tariff class, and every existing premise has interval data for
  each summer of its tenure.
* **Levelling.** The answer's remaining exposures level at exactly 165 MW, so lot-by-lot placement and the continuous water level give
  the same split, and the tie-break order is never used.
* **Maturity.** Every closed summer is settled at true-up before the extract. The coming book is the enrolled book at the extract date,
  switch confirmations close the count, and all 31 cold stores are energised before June.

## 9. Prompt sketch and deliverables

> The risk committee capped summer firm capacity at 400 MW, and on Friday I have to tell it how the 5 MW lots split across our four zone
> books, as four numbers that add to 400. Our head of trading is convinced Coast is still where our summer risk sits. Send me
> `summer_block_split.xlsx`, a chart `summer_levelling.png`, and a two-page `committee_paper.pdf` with the split I should defend.

* `summer_block_split.xlsx` — the exposure build and split, the estimated-reads sheet (ask A) and the demand-response sheet (ask B).
* `summer_levelling.png` — the four zones' uncovered exposures as paired bars (pooled and class-calibrated), the water level as a
  labelled line, each zone's allocated lots shaded, and North Central's cold stores annotated.
* `committee_paper.pdf` — the committed split, the water level and the bases the lenders and the trading desk will raise.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each zone, the share of last summer's bills issued on an estimated read, and the median days
  until the replacing actual read. *Device:* an estimated read later replaced by an actual read stays in the read file with a superseded
  status and the replacing read's ID, and the billing dictionary counts a bill as estimated only when its final read is estimated.
  Counting every estimated read row overstates the share by about a third in two zones.
* **Ask B (device-carried).** For each zone, the premises enrolled in last summer's demand-response programme and their average
  curtailment over its four events. *Device:* a premise that moves to another aggregator mid-season keeps its ESI ID and gains a second
  enrolment row, and the programme guide counts it once, with its last aggregator. Counting rows overstates enrolment in two zones and
  halves those premises' curtailment.
* **Ask C (validity).** Each zone's uncovered exposure and allocated block under each of the four rung constructions, with each
  construction's hits on the 40-cell replay table.
* **Decoupling.** Replacing the class factors with the pooled factor changes no figure in asks A or B.

## 11. Rubric arithmetic

4 zones × 2 (ask A) + 4 zones × 2 (ask B) + 4 zones × 4 constructions + 4 hit counts (ask C) + the four committed blocks, the water level
and North Central's exposure + 5 named chart parts + 3 files ≈ 50 criteria.

## 12. World-building constraints

* Hedges: Coast 250, North Central 303, South Central 116, Far West 40 MW. Peak-hour loads under the class replay 540 / 648 / 376 / 160
  MW; answer exposures 290 / 345 / 260 / 120 MW, levelling at 165.
* North Central's coming book: existing premises 1,020 MW of maximum demand; new premises 270 MW, of which 150 MW are the 31 cold stores
  and 120 MW other commercial. Factors in the system's 1-in-10 peak hour: 0.45 for every class but high load factor, 0.90 for high load
  factor, 0.52 for the large-commercial maximum-demand band. 2,300 amendment rows restate 60 MW (30 cold-store, 30 other).
* North Central's block is 55 / 150 / 135 / 180 MW across the rungs; the nearest wrong cells are 150, 210 and 215 MW.
* In every closed summer each book's high-load-factor share of maximum demand is under 1% (fourteen cold stores and ice plants). P-1184
  and P-2207 are identical on every enrolment column.
* Superseded estimated reads and aggregator moves never touch interval data, tariff classes or hedge positions.
