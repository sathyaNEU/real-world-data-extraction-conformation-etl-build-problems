# DS24 — Where the co-op spends its nitrogen-stabiliser cost-share, when every segment pays on average and none can promise next season

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · agricultural input economics |
| Mirrors | Funding an input or feature only where its measured lift will hold next season, not just on average (Google and Meta budget allocations judged on pooled experiments, Amazon promotions whose lift swings with the season, cloud autoscaling policies validated on pooled weeks) |
| Decision shape | Allocation under a cap, answered by a hold: cost-share for 60,000 acres across soil segments next season, or the money held |
| Committed call | The acres funded in each segment, or that the cost-share is held; and in how many of the five trial seasons the best segment's response paid for the product |
| Gap · Pattern | Gap 1 (time) over Gap 2 (population) · hold forced by a computed blocking quantity (Part 6.4: the margin over break-even is smaller than the spread between seasons), with a mixed soil segment split through the irrigation register (#6) at rung 1 and monitor calibration at rung 2 |
| Gate G mechanism | signal_vs_noise_or_hold, with decomposition_attribution |
| Measured traps engaged | #6 treats a mixed segment all one way · #7 uses the ready-made measure · #4 never tests its reading against the control · #13 validates on one population, applies to another |
| Calibration form | Gold-standard verification subsample: the agronomy team's weigh-wagon harvest of a random 10% of trial strips each season, against the members' yield monitors |
| Driving force | The board funds a segment only where the co-op's trials show, at the 90% level, that the stabiliser will pay for itself in the coming season. Every segment's five-season average is measured to ±0.3 bushels, because each season holds hundreds of strips, so averages that clear break-even look safe. But the coming season is one draw from the seasons, not from the strips. Irrigated and dryland sandy fields respond in opposite seasons, dry and wet, so pooled they look steady; split, each swings from 1 to 11 bushels and paid in only three of five seasons. No segment's next season clears break-even at 90%, and the money is held. |

## 1. Situation

A farm supply co-operative can share the cost of a nitrogen stabiliser ($9 an acre) on 60,000 acres of members' corn next season. The board
funds segments in order of expected net return, up to each segment's eligible acres, but only where the co-op's own trials show, at the 90%
level, that the product will pay for itself (2.0 bushels an acre at $4.50 corn) in the coming season. Otherwise the money is held for
another trial year. The co-op holds five seasons of paired-strip trials by soil segment, harvested with members' yield monitors, the
agronomy team's weigh-wagon harvests of a random tenth of the strips, the irrigation register, and the eligible acres by segment. The lead
agronomist says the trials show the product pays on sandy ground every year.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct and no stakeholder read is overturned. The monitors' strip differences, the weigh-wagon
  yields, the irrigation register and the eligible acres are all right, and every segment's average response is exactly what the trials
  measured. The difficulty is that the policy asks about next season, and an average over five seasons is not one.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the agronomist's view. Weigh-wagon-corrected strip differences, split by irrigation, still fund the irrigated
  and dryland sandy segments, and every interval clears break-even.
* **Instrument repair.** The suspect file is the yield monitors, which over-read the treated strip's difference by 0.6 bushels on sandy
  loam and 1.7 on clay loam against the weigh wagons. With a weigh wagon on every strip, rung 0 still funds sandy loam (60,000 acres), rung
  1 lands on rung 2's irrigated and dryland sandy segments, and rung 2 stays; no lower rung holds. The soil labels and the irrigation register
  are correct records of different attributes, and the hold still needs next season's prediction from the spread between seasons.
* **Lens swap.** The naive read asks whether the five-season average clears break-even. The answer asks whether next season will: a
  different moment, one season drawn from the spread between seasons.

## 3. The driving force

A strong solver distrusts the monitors and corrects every strip difference against the weigh-wagon subsample. It splits the trial file's
single sandy-loam label by the irrigation register, because irrigated and dryland fields lose nitrogen in different ways. It then funds
segments by net return, each average clearing break-even well inside its interval. Each step is competent, and the plan funds irrigated sandy
loam (40,000 acres) and dryland sandy loam (20,000). But the board's test is the coming season, and the trials' strips are replicates of
a season, not of seasons. Irrigated sandy fields respond in dry seasons, when pivots push nitrate below the roots (11.0 and 10.6 bushels),
and barely in wet ones (1.2, 1.6); dryland sandy fields do the reverse. Each segment's five seasonal means have a spread far wider than its
margin over break-even. Irrigated sandy loam averages 6.0 bushels with a 4.7-bushel spread, so its 90% prediction for next season is −1.9,
and it paid in three of five seasons. Pooled, the two sandy segments look steady, which is why the unsplit label passes. Split, nothing
passes, and the money is held.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Monitor strip differences pooled over five seasons by the trial file's soil label, strip-level 90% intervals, funded by net return | Sandy loam 60,000 acres | The co-op's own trials, every interval clear of break-even | The irrigation register: the sandy-loam label covers 40,000 irrigated and 40,000 dryland acres, and the two responded 6.6 and 3.4 bushels |
| 1 | Sandy loam split by the irrigation register (#6) | Irrigated sandy 40,000, clay loam 20,000 | Each part of the mixed segment priced on its own | The weigh-wagon subsample: monitors over-read the treated difference by 0.6 bushels on sandy loam and 1.7 on clay loam |
| 2 | Differences corrected to the weigh wagons | Irrigated sandy 40,000, dryland sandy 20,000 | Calibrated, split, every interval clear | The policy's test is the coming season, and each segment's five seasonal means spread wider than its margin over break-even |
| 3 | **Decisive:** a one-season prediction from each segment's five seasonal means, against break-even at 90% | **Hold: no segment clears; irrigated sandy loam, the best, paid in 3 of 5 seasons** | — | — |

* **Position table.** Rung allocations are sandy loam alone, then irrigated sandy with clay loam, then irrigated and dryland sandy, and on
  rung 3 nothing. Irrigated sandy loam leads rungs 1 to 3 on expected return ($20.7, then $18.0 an acre), so the hold refuses the leader
  rather than breaking a tie.
* **Blocking quantity.** Irrigated sandy loam averages 6.0 bushels, 4.0 above break-even, with a seasonal spread of 4.7; its one-sided 90%
  prediction for next season is −1.9 bushels (−0.6 on a normal approximation), and it paid in 3 of 5 seasons. Dryland sandy: −1.6, 3 of 5.
  Clay loam: 1.3, 2 of 5. Silt loam: −0.1, none.
* **Falsifiability.** Irrigated sandy loam would have been funded with a seasonal spread under 2.38 bushels, half its measured 4.7, or with
  an average of 9.9 bushels at its spread. Any segment whose next-season bound cleared 2.0 would have been funded.
* **Partial correction priced (L3).** Treating seasons as the unit but bounding the five-season mean rather than next season funds irrigated
  sandy 40,000 acres (bound 2.8). Using the season prediction with the strip-level spread funds rung 2's plan. Skipping the weigh wagons
  funds clay loam 60,000 acres (bound 3.0 on monitors), and skipping the split funds sandy loam 60,000 (pooled bound 2.7). No half-insight
  holds.
* **Grid.** Readings (monitor, weigh-wagon) × segments (labelled, split) × unit (strip, season) gives 8 cells. Seven fund acres (sandy loam
  in four, rung 1's and rung 2's plans, clay loam in one), and only weigh-wagon readings, split segments and the season unit hold. The
  nearest picks are the unsplit season cell (sandy loam) and the monitor season cell (clay loam), each one omission away.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The policy says "in the coming season". The trial report gives five-season averages with strip-level intervals, and
   no document says the season, not the strip, is the replicate for that question.
2. **No sweepable corpus nominates a pick.** *In every trial season each segment's strip-level interval is about ±0.3 bushels, because every
   segment-season holds over 400 strips.* A solver who checks precision season by season is confirmed every time; what blocks is the spread
   of the five seasonal means, which no single season shows.
3. **No arithmetic symptom.** Strips, seasons, acres and the weigh-wagon subsample reconcile under every rung, and every average is exact.
4. **Not a row predicate.** It needs seasonal means per split segment from corrected strips, their spread, a one-season prediction bound,
   and a comparison with break-even before any acres are funded.
5. **The enumeration is arithmetic.** No column holds a next-season bound or a season count against break-even; both are computed.
6. **No cutover date.** The seasons alternate wet and dry, and nothing steps.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The weigh-wagon subsample: a random 10% of trial strips each season, harvested and weighed, beside the members' monitor readings
  for the same strips.
* **What it certifies.** The monitors' over-read of the treated difference: 0.6 bushels on sandy loam, 1.7 on clay loam, 0.9 on silt loam,
  stable across seasons. Rung 2's correction is exact.
* **What it is blind to.** The spread between seasons (property 2). It is drawn within seasons.
* **Twin pair.** In the fifth season the irrigated and dryland sandy trials are identical on every visible column: "sandy loam", the same
  nitrogen rate, hybrid, planting window and strip count. They responded 5.6 and 2.9 bushels (1.9×). Only the irrigation register separates
  them.
* **Every rule exercised.** The five seasons hold two wet, two dry and one normal, so both sandy segments' good and bad seasons appear, and
  clay loam's small, steady response tests the bound at the other extreme.
* **Resemblance points at the decoy.** Pooled, sandy loam's seasonal means are the steadiest in the file (4.4 bushels, spread 1.0), the
  profile a lookup reads as reliable.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The board's policy: fund a segment only where the trials show, at the 90% level, that the stabiliser will pay in the
  coming season; fund by expected net return up to eligible acres; otherwise hold. The price deck: $4.50 corn, $9 an acre product. The
  eligible acres by segment. One sentence each.
* **Empirical pins.** The monitor over-read, from the weigh wagons. The irrigation split, from the register.
* **Voices.** The lead agronomist: "It pays on sandy ground every year." A board member: "Members want the cost-share, not another trial
  year." The product representative: "The response is consistent everywhere we test."
* **Licensed wrong basis.** The policy records that the regional extension review reads cost-share programmes on five-year average responses
  with strip-level intervals and will see that basis.

## 8. Determinism by construction

* **Break-even.** $9 ÷ $4.50 is exactly 2.0 bushels an acre.
* **Bound.** The one-sided 90% prediction from five seasonal means blocks every segment under a Student t or a normal approximation, and
  the season count (3 of 5) needs no convention at all.
* **Correction.** The monitor over-read is stable by segment across seasons, so per-season and pooled corrections agree.
* **Acres.** Eligible acres: irrigated sandy 40,000, dryland sandy 40,000, clay loam 60,000, silt loam 40,000.

## 9. Prompt sketch and deliverables

> The board can share the cost of the nitrogen stabiliser on 60,000 acres next season, but only where our trials say it will pay its way.
> Our lead agronomist says it pays on sandy ground every year. Tell me how many acres each soil segment gets, or that we hold the money, in a
> sentence for the board, with how many of our five trial seasons the best segment actually paid. Send `cost_share.xlsx`, a chart
> `season_response.png`, and a one-page `board_note.pdf`.

* `cost_share.xlsx` — each segment's strip and seasonal responses under each construction, the nitrogen-rate sheet (ask A), the enrolment
  sheet (ask B) and the validity sheet (ask C).
* `season_response.png` — each split segment's five seasonal responses as points with its average and its next-season bound, break-even as
  a labelled line, and the pooled sandy-loam series beside its two halves.
* `board_note.pdf` — the hold, the blocking figures, and what would have funded irrigated sandy loam.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each segment, members' average nitrogen rate last season. *Device:* split applications
  (pre-plant and side-dress) are logged as separate rows for one field with an application sequence, as the application log documents.
  Averaging rows halves the rate on split-applied fields.
* **Ask B (device-carried).** Members enrolled in the soil-testing programme at each quarter end. *Device:* a member who lapses and rejoins
  gets a new enrolment row under the same member number. Counting rows overstates two quarters by about a tenth.
* **Ask C (validity).** Each segment's five seasonal responses on monitors and weigh wagons, and each rung's allocation.
* **Decoupling.** Clearing the season prediction and the split changes no figure in asks A or B. Application rows and enrolments never
  enter a strip difference.

## 11. Rubric arithmetic

4 segments × 5 seasons × 2 readings (ask C) + 4 rung allocations + 4 segments' bounds and season counts + 4 nitrogen rates (ask A) + 4
quarters (ask B) + the hold and the best segment's count + 4 named chart parts + 3 files ≈ 69 criteria.

## 12. World-building constraints

* Weigh-wagon seasonal responses (bushels; wet, dry, wet, dry, normal): irrigated sandy 11.0, 1.2, 10.6, 1.6, 5.6; dryland sandy 0.0, 5.6,
  0.3, 5.2, 2.9; clay loam 2.2, 1.5, 2.3, 1.6, 1.9; silt loam 0.6, 0.1, 0.8, 0.2, 0.4. Monitors add 0.6, 0.6, 1.7 and 0.9.
* Strip-level intervals about ±0.3 bushels in every segment-season. Pooled sandy loam: 5.5, 3.4, 5.45, 3.4, 4.25.
* Rung plans: sandy loam 60,000; irrigated sandy 40,000 with clay loam 20,000; irrigated sandy 40,000 with dryland sandy 20,000; hold.
* The twin trials are identical on every visible column. Application rows and enrolments never touch strips or weigh wagons.
