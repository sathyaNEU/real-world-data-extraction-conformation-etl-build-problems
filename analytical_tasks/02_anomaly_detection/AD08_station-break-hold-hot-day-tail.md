# AD08 — Whether a weather station's jump enters the 2027 heat-index price, when the break that matters is the one on the hottest days

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Economics · weather-index insurance pricing |
| Mirrors | Deciding whether a shift can be corrected before repricing on it, when the correction that holds on average does not hold in the tail that drives the price (latency SLOs priced on the 99th percentile after an infrastructure change, fraud thresholds after a scoring-model swap, tail-risk pricing after a data-vendor switch at banks and cloud providers) |
| Decision shape | Hold, forced by a blocking quantity: the 2027 heat-index rate filing either adjusts the Tallis Creek series for its 1986 break or holds the 2026 rate |
| Committed call | The adjustment the pricing series takes, or a hold of the 2026 rate, with the quantity that decides it |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · hold forced by a computed blocking quantity (E28): the break the index prices sits in the hot-day tail, where it is larger than the mean step and sizeable only from the record's few hot days; a neighbour's reading-hour change (E15) and a successor-ID join (E20) at the lower rungs |
| Gate G mechanism | signal_vs_noise_or_hold, with method_or_model_selection |
| Measured traps engaged | #11 beats the headline trap, misses the quiet one · #13 validates on one population, applies to another · #18 joins only on the visible key |
| Calibration form | Parallel-run overlap: Tallis Creek's 14 months of side-by-side glass and electronic readings, neighbour N3's 24 months of side-by-side 07:00 and 17:00 readings, and the network's archive of eight long parallel runs at other stations |
| Driving force | Once the comparison set is clean, the neighbour difference series sizes Tallis Creek's 1986 break at +0.28 °C ± 0.07, inside the pricing tolerance, and every careful build files that adjustment. But the product pays on days at or above 35 °C, and the break is not one number: the station's own overlap shows the new sensor reading hot sunny maxima 0.41 °C above the old glass while matching it on average. Sized on the days that set the index, the break is +0.62 °C with a 95% half-width of 0.29, nearly twice the ±0.15 the manual allows, so the filing holds the 2026 rate. |

## 1. Situation

A crop insurer prices a heat-index product off the Tallis Creek cooperative station, whose annual mean temperature jumps by about half a
degree in 1986 and stays there. The product pays on days at or above 35 °C from December to February. The pricing manual lets a break enter
the series as an adjustment only when its size is known to within ±0.15 °C at 95% from a difference series against the five nearest
stations; a station with an unresolved break is not repriced and the rate holds at the prior year's. The 2027 rate is filed on 1 February.
The pack carries daily and annual series for Tallis Creek and twelve stations within 100 km, every station's history file, the network's
station register, the two overlaps and the network's parallel-run archive.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the station series, the neighbours' series, the histories, the register, both overlaps and the
  archive. The pricing analyst's warming and the reinsurer's instrument story are each true of something in the record. Nothing reported is
  overturned; the difficulty is how precisely the record can size the break for the quantity the product prices.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices. The clean difference series of annual means still shows +0.28 °C with a 0.07 half-width, and every
  solver who builds it still files an adjustment.
* **Instrument repair.** Suspect file: N3's series, whose reading hour moved from 17:00 to 07:00 in August 1986. Homogenised, rungs 2 and 3
  both return +0.28 °C ± 0.07 and file an adjustment, rung 1 still files the sensor story and rung 0 no adjustment; the hot-day construction
  is still needed to reach the hold. Tallis Creek's own break is the object of the filing, not a defect elsewhere, and its overlap, the
  archive and the other neighbours are complete.
* **Lens swap.** The naive quantity is the annual mean; the answer's is the daily maximum on the days that set the index, a different
  population of days, about fifteen a summer, whose break is twice the mean's.

## 3. The driving force

A strong solver refuses the pricing analyst's climate story because no neighbour jumps in 1986, follows the register's successor links to
the true five nearest stations, and refuses the reinsurer's sensor story because Tallis Creek's own overlap puts the June sensor change at
−0.06 °C on the mean. It then finds the quiet trap in the comparison set: N3, 12 km away and the composite's heaviest member, changed its
reading hour in August 1986, and its own overlap sizes the effect month by month. Corrected, the composite gives +0.28 °C ± 0.07, inside
tolerance, and the solver files the adjustment. Every move is competent, and both decoys and the quiet trap have been beaten. But the
product does not pay on annual means. The station's overlap shows the electronic sensor in its smaller screen reading 0.41 °C above the
glass on days over 33 °C, and the archive's eight long parallel runs all show hot-day breaks 0.2 to 0.4 °C away from their mean steps.
Sized on the days that set the index, a difference series of daily maxima on days the clean composite reaches 33 °C, with heatwaves kept
together, the break is +0.62 °C ± 0.29. The manual's test fails for the quantity priced, and the rate holds.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Tallis Creek's own series: the jump read as regional warming; price on the unadjusted series | H1, no adjustment | The series is long, clean and continuous, and the decade did warm | The neighbours: none of the twelve steps in 1986, so the difference series steps and the jump is local |
| 1 | Difference series against the five nearest stations with complete records under one station ID (40–90 km): +0.61 °C ± 0.13 at the June sensor change | H2, adjust 0.61 °C for the sensor switch | The textbook relative test, a documented instrument event at the break, inside tolerance | The register's successor links: the three nearest stations (8–20 km) were renumbered in 1993 and continue under new IDs |
| 2 | The true nearest five via successor links: +0.44 °C ± 0.06; the station's overlap puts the sensor at −0.06 °C, so the step is the relocation | H3, adjust 0.44 °C | Right neighbours, the sensor decoy beaten by the station's own overlap, inside tolerance | N3's overlap file: from August 1986 N3 read at 07:00, 0.36 °C cooler than its 17:00 readings, and N3 carries 45% of the composite's weight |
| 3 | N3 corrected month by month from its overlap; the annual-mean step re-estimated | H3, adjust 0.28 °C ± 0.07 | A clean comparison set, every documented change accounted for, inside tolerance | The station's overlap: the new sensor matches the glass on the mean but reads 0.41 °C higher on days over 33 °C, and the product pays on days at or above 35 °C |
| 4 | **Decisive:** daily maxima on days the clean composite reaches 33 °C, the step estimated with summers resampled whole | **Hold the 2026 rate:** +0.62 °C ± 0.29, beyond ±0.15 | — | — |

* **Blocking quantity.** The 95% half-width of the hot-day break, 0.29 °C, 1.93× the 0.15 tolerance (0.31 with N3 dropped). The point
  estimate is far from zero and from the mean step, so the break is real and differs on the days that matter; it cannot be sized there, so
  every adjustment fails the manual's test and the hold applies.
* **Why each candidate fails.** H1: the step is local. H2: the overlap puts the sensor near zero on the mean. H3 at 0.44: N3 inflates it.
  H3 at 0.28: right on the mean and wrong for the index, whose break is unsizeable within tolerance.
* **Partial correction priced (L3).** A solver who sizes the hot-day break but treats each hot day as independent gets +0.62 °C ± 0.12 and
  files that adjustment: a pick. A solver who adds the overlap's extra hot-day sensor offset (+0.47 °C, ± 0.12) to the mean step files a
  two-part adjustment: a pick. A solver who drops N3 and keeps the annual mean gets +0.29 °C ± 0.08 and files it: a pick. No half lands on
  the hold.
* **Grid.** Neighbour join (single ID or successor chain) × N3 (as recorded, corrected, dropped) × quantity (annual mean or hot-day maxima)
  gives twelve cells. Every annual-mean cell files an adjustment, from 0.28 to 0.63 °C; every hot-day cell holds, with half-widths of 0.27
  to 0.33. The nearest wrong cell, the clean annual mean, needs only the index's quantity ignored.
* **Falsifiable.** The hold becomes an adjustment if the hot-day half-width reaches 0.15: about four times as many hot days either side of
  1986 as the record holds, or a hot-day neighbour as close as N3 with its own parallel run.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The manual speaks of a break's size in the singular; the index definition sits in the product schedule. Nothing
   says the break differs by temperature or that the index lives where it differs most.
2. **The corpus pins a construction, not a menu.** In all eight of the archive's long parallel runs, the hot-day break differs from the
   mean step by 0.2 to 0.4 °C, and an index adjusted by the mean step misprices the hot-day count in every one, always in the direction of
   the hot-day offset. The construction is a difference series restricted to the composite's hot days, with whole summers resampled, and no
   column holds it.
3. **No arithmetic symptom.** Every series is complete once successor links are followed, and the mean step reconciles with the overlap
   and the neighbours.
4. **Not a row predicate.** It needs a clean composite, a selection of days by the composite's own maximum, a step on daily maxima and an
   interval that keeps heatwaves whole.
5. **The enumeration is arithmetic.** The verdict is a half-width compared with a tolerance; no field marks a break as unsizeable.
6. **No cutover date decides it.** Every change in the pack is dated in a history file; the decisive quantity is a precision on the hot
   days that no date supplies.
7. **Survives deletion.** With every voice removed, the answer and the difficulty are unchanged.

## 6. The calibration corpus

* **Form.** Tallis Creek's 14 months of glass and electronic readings side by side from June 1986; N3's 24 months of 07:00 and 17:00
  readings side by side from August 1986; and the network's archive of eight parallel runs of five years or more at other stations.
* **What it pins.** The station's overlap: −0.06 °C on the mean, +0.41 °C ± 0.12 on days over 33 °C. N3's overlap: its reading-hour offset
  month by month, 0.36 °C on the annual mean. The archive: hot-day breaks 0.2 to 0.4 °C from the mean step at all eight stations.
* **Twin pair.** Archive stations S-114 and S-207 are identical on their documented changes, mean steps (+0.30 °C), screen type and
  distance to neighbours. Their parallel runs measured hot-day breaks of +0.66 and +0.31 °C (2.1×): S-114's new screen stood in full sun,
  S-207's under partial shade. Only the hot-day estimate separates them.
* **Every rule exercised.** Two archive stations had breaks smaller on hot days than on average, so the direction is not assumed; the
  register links all three renumbered stations, so the successor join is tested three times.
* **Resemblance points at the decoy.** Tallis Creek's mean step most resembles the network's 23 documented relocation breaks, which average
  +0.31 °C and were all adjusted by their mean step.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The pricing manual: a break enters as an adjustment when its size is known to within ±0.15 °C at 95% from a difference
  series against the five nearest stations; a station with an unresolved break is not repriced, and the rate holds at the prior year's.
  The product schedule: the index counts days at or above 35 °C, December to February. The numbering note: stations renumbered in 1993
  carry a successor link in the register.
* **Empirical pins.** N3's monthly reading-hour offsets and the station's hot-day sensor offset, from the overlaps.
* **Voices.** The pricing analyst: "It's climate. Everything warmed in the eighties." The reinsurer's meteorologist: "That's the electronic
  sensor switch; every co-op station has one."
* **Licensed wrong basis.** The manual records that the reinsurer's model desk adjusts breaks by their annual-mean step and will review the
  filing on that basis.

## 8. Determinism by construction

* **Hot days.** Selection at 32, 33 or 34 °C on the clean composite gives half-widths of 0.27 to 0.33; none reaches 0.15.
* **Resampling.** Whole summers or whole heatwaves resampled give 0.29 and 0.30.
* **Window.** Ten or fifteen summers either side of 1986 give 0.29 and 0.25.
* **N3's handling.** Corrected or dropped, 0.29 and 0.31; the verdict does not depend on it.

## 9. Prompt sketch and deliverables

> The 2027 heat-index rate is filed on 1 February and it rests on the Tallis Creek series, which jumped in 1986. Our pricing analyst is
> sure the jump is climate. Tell me in one sentence for the filing which adjustment, if any, the series takes before we price, or whether
> we hold this year's rate, and send `break_assessment.xlsx` with the sheets below, the chart `hot_day_break.png`, and a short
> `filing_memo.pdf`.

* `break_assessment.xlsx` — the step estimates under each comparison set and quantity, the neighbours' hot-day sheet (ask A), the policy
  sheet (ask B) and the rung table (ask C).
* `hot_day_break.png` — Tallis Creek minus the clean composite from 1976 to 1996 on annual means and on hot-day maxima as two panels, the
  1986 changes marked, each step with its 95% band, and the ±0.15 tolerance drawn around both.
* `filing_memo.pdf` — the committed verdict, the blocking quantity, and what would turn it into an adjustment.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the twelve neighbours, days at or above 35 °C in 2006–2015 and in 2016–2025. *Device:*
  after missed days an observer's reading carries the multi-day maximum with an accumulation flag and blank days before it, as the network's
  daily-data guide documents. Counting a flagged value as one day, or the blanks as cool days, misstates the counts at four stations. The
  break assessment reads 1976 to 1996, before the network allowed accumulated readings.
* **Ask B (device-carried).** For each of the last ten seasons, heat-index policies sold and the claims ratio. *Device:* the policy file
  restates a policy whenever it is endorsed, as a new row with a version suffix on the same policy number, per the underwriting guide.
  Counting rows overstates policies in the four seasons with mid-season endorsements and understates their claims ratios.
* **Ask C (validity).** For each of the five rung constructions, the step estimate and its 95% half-width.
* **Decoupling.** Clearing the hot-day construction changes no figure in asks A or B.

## 11. Rubric arithmetic

12 stations × 2 decades (ask A) + 10 seasons × 2 (ask B) + 5 constructions × 2 (ask C) + the hold verdict, the blocking half-width, the
point estimate and the falsification condition + 5 named chart parts + 3 files ≈ 66 criteria.

## 12. World-building constraints

* Mean steps: +0.61 ± 0.13 (far single-ID set), +0.44 ± 0.06 (nearest five, N3 as recorded), +0.28 ± 0.07 (N3 corrected), +0.29 ± 0.08
  (N3 dropped). Hot-day step: +0.62 ± 0.29 (N3 corrected), +0.60 ± 0.31 (dropped).
* The station's sensor offset is −0.06 °C on the mean and +0.41 °C on days over 33 °C; about fifteen composite days a summer reach 33 °C.
* N3 carries 45% of the inverse-distance weight and reads 0.36 °C cooler after August 1986.
* S-114 and S-207 are identical on every archive column but their hot-day breaks.
* Three of the five nearest stations continue under new IDs from 1993; one far single-ID station has a 1985 screen replacement.
* Accumulation flags and policy endorsements never touch the 1976–1996 daily series or the overlaps.
