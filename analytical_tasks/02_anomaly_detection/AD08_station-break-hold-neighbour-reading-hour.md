# AD08 — Whether a weather station's jump enters the 2027 heat-index price, when the nearest neighbour changed its own reading hour that same summer

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Economics · weather-index insurance pricing |
| Mirrors | Deciding whether a metric shift is real before repricing on it, when the comparison series used to test it carry changes of their own (guardrail metrics after an SDK upgrade, ad-measurement panels whose control publishers changed tagging, sensor fleets judged against neighbours at Google and Amazon data centres) |
| Decision shape | Hold, forced by a blocking quantity: the 2027 heat-index rate filing either adjusts the Marlow Creek series for its 1986 break or holds the 2026 rate |
| Committed call | The adjustment the pricing series takes, or a hold of the 2026 rate, with the quantity that decides it |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · the quiet second trap (E15) behind a loud instrument decoy, settled by a precision rather than a cause, with an implicit successor-ID join at the lower rung (E20) |
| Gate G mechanism | signal_vs_noise_or_hold, with method_or_model_selection |
| Measured traps engaged | #11 beats the headline trap, misses the quiet one · #18 joins only on the visible key · #8 papers over a failed reproduction |
| Calibration form | Parallel-run overlap: Marlow Creek's 14 months of side-by-side glass and electronic readings, and neighbour N3's 24 months of side-by-side 07:00 and 17:00 readings |
| Driving force | The neighbour difference series is the right instrument and it shows a +0.44 °C step, inside the pricing tolerance. But the nearest neighbour, which carries 45% of the composite's weight, moved its daily reading from 17:00 to 07:00 two months after Marlow Creek's own changes and reads 0.36 °C cooler for it. Its overlap file shows that; once N3 is corrected or dropped, the step's 95% half-width is 0.22–0.24 °C against a tolerance of 0.15, and no adjustment can enter. |

## 1. Situation

A crop insurer prices a heat-index product off the Marlow Creek cooperative station, whose annual mean temperature jumps by about half a
degree in 1986 and stays there. The pricing manual lets a break enter the series as an adjustment only when its size is known to within
±0.15 °C at 95% from a difference series against the five nearest stations; a station with an unresolved break larger than that is not
used for repricing, and the rate holds at the prior year's. The 2027 rate is filed on 1 February. The pack carries daily and annual series
for Marlow Creek and twelve stations within 100 km, every station's history file, the network's station register, and both overlaps.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the station series, the neighbours' series, the histories, the register and both overlaps. The
  pricing analyst's warming and the reinsurer's instrument story are each true of something in the record. Nothing reported is overturned;
  the difficulty is how precisely the record can size the break once the comparison series are clean.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices. The difference series against the five nearest still shows a crisp +0.44 °C step with a 0.11
  half-width, and every solver who builds it still files an adjustment.
* **Instrument repair.** Give every station a perfect sensor from now on; 1986 has passed, and N3's two readings a day in its overlap are
  already exact. No better instrument of the past separates three changes that fell within four months of each other.
* **Lens swap.** The naive comparison set includes N3 as recorded; the answer's comparison set is the four clean neighbours plus N3 on a
  corrected basis, a different population of reference series, and the verdict is a precision, not a re-read of the same step.

## 3. The driving force

A strong solver refuses the pricing analyst's climate story because no neighbour jumps in 1986, builds the difference series, finds the
station's June 1986 switch from glass thermometers to an electronic sensor, and refuses that story too, because Marlow Creek's own
overlap shows the sensor reads only 0.06 °C cooler. It attributes the step to the September relocation, finds +0.44 °C with a half-width
of 0.11, inside tolerance, and files the adjustment. Every move is competent and the loud decoy has been beaten twice. The quiet one is in
the comparison set. N3, 12 km away and the composite's heaviest member, changed its observer's reading hour from 17:00 to 07:00 in August
1986. Its history file records an observer change and nothing more; the reading hour shows only in N3's overlap file, where the observer
kept both readings for 24 months, 0.36 °C apart. Corrected by that overlap or dropped, N3 stops inflating the step: the estimate falls to
+0.28 °C and its half-width widens to 0.24 °C, or 0.22 °C with N3 dropped. Either way the break is real and unsizeable, and the manual
holds the rate.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Marlow Creek's own series: the jump read as regional warming; price on the unadjusted series | H1, no adjustment | The series is long, clean and continuous, and the decade did warm | The neighbours: none of the twelve steps in 1986, so the difference series steps and the jump is local |
| 1 | Difference series against the five nearest stations with complete records under one station ID (40–90 km); +0.61 °C ± 0.13 at the June instrument change | H2, adjust 0.61 °C for the sensor switch | The textbook relative test, a documented instrument event at the break, inside tolerance | The station register's successor links: the three nearest stations (8–20 km) were renumbered in 1993 and continue under new IDs, so the nearest five are different stations |
| 2 | Difference series against the true nearest five via successor links: +0.44 °C ± 0.11; the station's own overlap puts the sensor at −0.06 °C, so the step is the September relocation | H3, adjust 0.44 °C for the relocation | Right neighbours, the loud decoy beaten by the station's own overlap, inside tolerance | N3's overlap file: from August 1986 N3 read at 07:00, 0.36 °C cooler than its 17:00 readings, and N3 carries 45% of the composite's weight |
| 3 | **Decisive:** N3 corrected month by month from its overlap, or dropped; the step re-estimated with its interval | **Hold the 2026 rate:** +0.28 °C ± 0.24 (corrected), +0.29 °C ± 0.22 (dropped), both beyond ±0.15 | — | — |

* **Blocking quantity.** The 95% half-width of the step once N3 is clean: 0.24 °C corrected and 0.22 °C dropped, 1.60× and 1.47× the 0.15
  tolerance. The point estimate is far from zero, so the break is real; it cannot be sized, so H3 fails and the manual's hold applies.
* **Why each candidate fails.** H1: the step is local. H2: the station's overlap sizes the sensor at −0.06 °C. H3: unsizeable within
  tolerance. H4 (reading hour at Marlow Creek): its reading hour never changed. H5 (urban growth): gradual, no step in the difference series.
* **Partial correction priced (L3).** A solver who corrects N3 with the overlap's annual mean offset, ignoring the seasonal pattern and the
  offset's own uncertainty, gets +0.30 °C ± 0.11 and files an adjustment: a pick, as wrong as rung 2.
* **Grid.** Neighbour join (single ID or successor chain) × N3 (as recorded, annual offset, monthly correction, dropped) × sensor evidence
  (history entry or overlap) gives sixteen cells. Every single-ID cell files H2 at 0.58–0.63 °C; every successor cell with N3 as recorded
  or annually corrected files H3 at 0.30–0.44 °C; only the monthly correction and the drop leave the half-width above tolerance, and both
  hold.
* **Falsifiable.** With N3 clean and the five nearest otherwise unchanged, the hold would become a pick if the half-width fell to 0.15; the
  record would need about nine more years after 1986 with no further changes at any of the five, or a sixth neighbour as close as N3.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** N3's history file records an observer change in August 1986 and says nothing about the reading hour. The manual's
   tolerance is a basis; no document says a neighbour is contaminated.
2. **Corpus blind for a computable reason.** *Marlow Creek's own overlap is identical under every reading of the comparison set, because it
   measures the station against itself.* It refutes the instrument decoy and is arithmetically incapable of seeing N3; only N3's own overlap,
   reached through the successor ID, can.
3. **No arithmetic symptom.** Every series is complete and continuous once successor links are followed; N3's step is buried inside the
   same four months as Marlow Creek's and does not stand out in the composite.
4. **Not a row predicate.** It needs a monthly offset from a two-reading overlap, a re-weighted composite, a difference series and an
   interval on its step.
5. **The enumeration is arithmetic.** The verdict is a half-width compared with a tolerance; no field marks a neighbour as unusable.
6. **No cutover date decides it.** Every change in the pack is dated in a history file and known; the decisive quantity is a precision
   the dates cannot supply, and no event study yields it.
7. **Survives deletion.** With every voice removed, the answer and the difficulty are unchanged.

## 6. The calibration corpus

* **Form.** Two parallel-run overlaps: Marlow Creek's 14 months of glass and electronic readings side by side from June 1986, and N3's 24
  months of 07:00 and 17:00 readings side by side from August 1986.
* **What it pins.** Marlow Creek's overlap sizes the sensor change at −0.06 °C (±0.04), refuting H2 at every neighbour set. N3's overlap
  sizes its reading-hour change month by month, −0.48 °C in July and −0.19 °C in January, 0.36 °C on the annual mean.
* **Twin pair.** N3 and N4 are identical on distance (12 and 13 km), elevation, correlation with Marlow Creek (0.94), record length and
  every entry in their history files. Their difference series against Marlow Creek step by +0.68 °C and +0.32 °C in 1986 (2.1×); only N3's
  overlap separates them.
* **Every rule exercised.** One of the far single-ID neighbours had a screen replacement in 1985, which is why rung 1 overshoots; the
  register links all three renumbered stations, so the successor join is tested three times.
* **Resemblance points at the decoy.** Marlow Creek's step most resembles the network's 23 documented relocation breaks, which average
  +0.41 °C.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The pricing manual: a break enters as an adjustment when its size is known to within ±0.15 °C at 95% from a difference
  series against the five nearest stations; a station with an unresolved break larger than that is not used for repricing, and the rate
  holds at the prior year's. The network's numbering note: stations renumbered in 1993 carry a successor link in the register.
* **Empirical pins.** The sensor offset and N3's monthly reading-hour offsets, from the two overlaps.
* **Voices.** The pricing analyst: "It's climate. Everything warmed in the eighties." The reinsurer's meteorologist: "That's the electronic
  sensor switch; every co-op station has one."
* **Licensed wrong basis.** The manual records that the reinsurer's model desk adjusts documented instrument changes by the network's
  published average sensor offset and will review the filing on that basis.

## 8. Determinism by construction

* **N3's handling.** Monthly correction and dropping both leave the half-width above tolerance (0.24 and 0.22), so the convention cannot
  change the verdict.
* **Weights.** Inverse-distance and equal weights give half-widths of 0.24 and 0.25 with N3 corrected.
* **Window.** Ten years either side of 1986 or five give half-widths of 0.24 and 0.31; neither reaches 0.15.
* **Break date.** The station's two changes and N3's fall between June and September 1986, and any split date in that span moves the
  estimate by under 0.02 °C.
* **Series.** Annual means from complete years only; every station is complete in every year from 1976 to 1996 once successor links are
  followed.

## 9. Prompt sketch and deliverables

> The 2027 heat-index rate is filed on 1 February and it rests on the Marlow Creek series, which jumped in 1986. Our pricing analyst is
> sure the jump is climate. Tell me in one sentence for the filing which adjustment, if any, the series takes before we price, or whether
> we hold this year's rate, and send `break_assessment.xlsx` with the sheets below, the chart `difference_series.png`, and a short
> `filing_memo.pdf`.

* `break_assessment.xlsx` — the step estimates under each comparison set, the hot-day sheet (ask A), the policy sheet (ask B) and the
  rung table (ask C).
* `difference_series.png` — Marlow Creek minus the composite from 1976 to 1996 for the far, nearest-five and clean composites, the three
  1986 changes marked, each composite's step with its 95% band, and the ±0.15 tolerance drawn around the clean estimate.
* `filing_memo.pdf` — the committed verdict, the blocking quantity, and what would turn it into an adjustment.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the twelve neighbours, days at or above 35 °C in 2006–2015 and in 2016–2025. *Device:*
  after missed days an observer's reading carries the multi-day maximum with an accumulation flag and blank days before it, as the network's
  daily-data guide documents. Counting a flagged value as one day, or the blanks as cool days, misstates the counts at four stations. The
  break assessment uses annual means of complete years only.
* **Ask B (device-carried).** For each of the last ten seasons, heat-index policies sold and the claims ratio. *Device:* the policy file
  restates a policy whenever it is endorsed, as a new row with a version suffix on the same policy number, per the underwriting guide.
  Counting rows overstates policies in the four seasons with mid-season endorsements and understates their claims ratios.
* **Ask C (validity).** For each of the four rung constructions, the step estimate and its 95% half-width.
* **Decoupling.** Clearing N3's correction changes no figure in asks A or B.

## 11. Rubric arithmetic

12 stations × 2 decades (ask A) + 10 seasons × 2 (ask B) + 4 constructions × 2 (ask C) + the hold verdict, the blocking half-width, the
point estimate and the falsification condition + 5 named chart parts + 3 files ≈ 64 criteria.

## 12. World-building constraints

* Marlow Creek's step is +0.28 °C against clean neighbours; the sensor offset is −0.06 °C; the relocation carries the rest.
* N3 carries 45% of the inverse-distance weight and reads 0.36 °C cooler after August 1986; the contaminated step is +0.44 ± 0.11.
* Half-widths: 0.13 (far set), 0.11 (nearest five as recorded), 0.11 (annual offset), 0.24 (monthly correction), 0.22 (N3 dropped).
* N3 and N4 are identical on every register and history column; their 1986 difference steps are +0.68 and +0.32.
* Three of the five nearest stations continue under new IDs from 1993; one far single-ID station has a 1985 screen replacement.
* Accumulation flags and policy endorsements never touch the annual series or the overlaps.
