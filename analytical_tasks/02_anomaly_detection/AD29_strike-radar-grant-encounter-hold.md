# AD29 — Which airport gets this year's wildlife radar grant, or does it carry over, when one flock can strike a whole departure bank

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Policy & Education · aviation safety oversight |
| Mirrors | Counting the events an intervention prevents rather than the hits each event produces (one outage behind thousands of crash reports at Apple and Google, one bad deploy paging many services on cloud platforms, one spam campaign landing in many inboxes at Meta), where the unit the fix acts on is the cause, not its hits |
| Decision shape | Hold, forced by a blocking quantity: the radar grant goes to one of six shortlisted airports or carries over |
| Committed call | The airport awarded the grant, or that it carries over, with the evidence figure that decides it, at the grant panel on 14 November |
| Gap · Pattern | Gap 2 (population: the unit the grant counts is not the unit the file stores) · the unit not stored, built by grouping struck-aircraft records into wildlife encounters, with a damage code validated on one reporter population and applied to another below it |
| Gate G mechanism | signal_vs_noise_or_hold, with method_or_model_selection support |
| Measured traps engaged | #2 counts file rows instead of the real unit · #13 validates on one population, applies to another · #8 papers over a failed reproduction |
| Calibration form | Parallel-run overlap: 2022–2023, when mandatory occurrence reporting (one record per struck aircraft, damage confirmed by the operator) ran alongside the voluntary strike database at nine pilot airports |
| Driving force | The radar acts on a group of birds, and the grant counts encounters: one wildlife group's interaction with traffic. The strike database holds one record per struck aircraft. Since C became a hub its departures leave in banks 90 seconds apart, and a gull flock feeding beside the runway now strikes two or three aircraft in one bank, so C's damaging records rose while its encounters did not. Grouping records by airport and species wherever strikes fall within 15 minutes of each other reproduces the annual report's national encounter count in all eight years, and on encounters every airport's lower bound is below zero, the best C at −0.08: the grant carries over. |

## 1. Situation

The national aviation safety authority has one wildlife-detection radar grant of $2.4M this year. The grant rule awards it to a shortlisted
airport whose damaging wildlife encounters per 100,000 movements have risen faster than the national rate, with the lower 90% bound of the
excess trend above zero over the last eight years; if no airport meets that, the grant carries to next year. Six airports were shortlisted
on reported-strike growth. The authority holds the voluntary strike database (one record per struck aircraft, with time, runway, species
group, damage code and reporter, crew or airport staff, merged when both report one aircraft), the movement log, the occurrence records from
the 2022–2023 parallel run, and its annual report. B's airport director is lobbying hard.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each record is a real strike on a real aircraft, the movement counts tie to air traffic records, and
  the annual report's confirmation rates and encounter counts are right. B's director is right that B's staff file more reports than ever.
  Nothing reported is overturned; the difficulty is building the unit the grant counts.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the director's lobbying and the shortlist's growth figures. A model of damaging records per movement, with
  damage calibrated by reporter type, still clears C, and still funds it.
* **Instrument repair.** Suspect files: the voluntary database, which misses strikes nobody reported, and its uncertain damage codes.
  Capture every strike as the parallel run's occurrence records do and confirm every damage code: rung 0 still funds A (+0.55), rung 1
  becomes rung 2 and funds C (+0.21), and rung 2 still funds C. Each record still describes one struck aircraft, a correct record of a
  different thing from an encounter, so the grouping is still needed and still turns the pick into a hold.
* **Lens swap.** The naive count is struck aircraft; the answer counts wildlife encounters, a different population (each of C's
  departure-bank flocks collapses to one encounter), and the verdict changes from a pick to a hold.

## 3. The driving force

A strong solver discards all-strike growth, keeps damaging strikes as the rule says, notices that airport staff code uncertain damage far
more freely than crews, calibrates damage by reporter type from the authority's published confirmation rates, fits the rule's model and
finds C's lower bound clear of zero. Every step is correct, and every step counts records, one per struck aircraft. The rule counts
encounters, and the radar acts on the group of birds, whatever it goes on to hit. Since C became a hub in 2019 its departures leave in banks
90 seconds apart; a gull flock feeding beside the runway now strikes two or three aircraft in one bank, each its own record, reported by a
different crew. C's damaging records rose while its encounters did not. Grouping records by airport and species wherever a strike follows
the last within 15 minutes reproduces the annual report's national encounter count in every year, and on encounters no airport's excess
trend has a lower bound above zero.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Excess trend in all reported strikes per 100,000 movements over the national trend | Fund A (lower bound +0.62) | It is the shortlist's own measure, offset by movements and judged against the nation | The grant rule counts damaging encounters only |
| 1 | Excess trend in damaging records (codes minor and above, uncertain included) | Fund B (lower bound +0.37) | Damaging strikes are what the rule names, and B's rise is steep | The annual report: uncertain-damage codes are confirmed for 71% of crew reports and 12% of airport-staff reports, and B's rise is staff reports |
| 2 | Damaging records with uncertain codes weighted by reporter-type confirmation (the parallel run reproduces each rate) | Fund C (lower bound +0.21) | Calibrated, exposure-adjusted, national-relative and validated on the overlap | The annual report: national damaging encounters run below damaging records, and the gap has widened from 5% in 2018 to 16% in 2025 |
| 3 | **Decisive:** group records into encounters (same airport and species group, each strike within 15 minutes of the one before), then the same calibrated model on encounters | **Hold: the grant carries over** | — | — |

* **The blocking quantity.** On encounters, the best lower 90% bound across the six airports is C's, at −0.08 damaging encounters per
  100,000 movements per year, 0.08 below the rule's zero line. The others sit at A −0.31, B −0.22, D −0.15, E −0.12 and F −0.27, so every
  candidate fails on the same standard.
* **Partial correction priced (L3).** A solver who sees the gap between records and encounters but deflates every airport by the national
  ratio of records to encounters leaves C's trend positive, because C's ratio rose from 1.02 to 1.42 while the national one rose from 1.05
  to 1.19, and funds C at +0.12, 0.12 above the line. A solver who groups only strikes in the same minute merges almost nothing, since bank
  departures leave 90 seconds apart, and funds C at +0.19. Both land on the rung-2 leader rather than on the hold.
* **Grid.** Damage basis (all strikes, raw damaging, calibrated damaging) × unit (records, records deflated by the national ratio,
  encounters) = 9 cells. Every cell but (calibrated, encounters) commits to A, B or C with a positive bound, because A's and B's rises are
  single-aircraft strikes that grouping leaves alone; only that cell holds.
* **Falsifiable.** C would have qualified with a trend 0.08 higher, about seven more damaging encounters over the last four years, or with
  three more years at its current trend narrowing the bound.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The glossary defines an encounter as one wildlife group's interaction with traffic. No document says a group can
   strike several aircraft or how to tell one group's records from two groups', and the annual report publishes encounter counts without a
   method.
2. **Corpus blind for a computable reason.** *In every overlap airport-year each wildlife group struck one aircraft, because none of the
   nine pilot airports runs departure banks (their busiest hour has six departures).* The overlap reproduces rung 2's calibration exactly
   and cannot see a multi-aircraft encounter. The unit is pinned instead by the annual report: grouping reproduces the published national
   encounter count in all eight years, and counting records misses every year.
3. **No arithmetic symptom.** Record IDs are unique, no two records describe one aircraft, movement totals tie, and the reporter-type counts
   match the annual report.
4. **Not a row predicate.** It needs, per airport and species group, the records ordered in time and chained wherever the gap is under 15
   minutes (a group and a sequence inside it), before the trend model is fitted.
5. **The enumeration is arithmetic.** No column marks an encounter, and the records of one bank's flock carry different aircraft, flights
   and reporters.
6. **No cutover date.** C's banks grew from 2019 to 2025 as the hub added routes, so its multi-aircraft share rises smoothly and no series
   steps.
7. **Survives deletion.** Remove the director, the shortlist figures and every voice: the record-grain model is still the natural build.

## 6. The calibration corpus

* **Form.** The 2022–2023 parallel run at nine pilot airports: every mandatory occurrence record (one per struck aircraft, damage confirmed
  by the operator) beside the voluntary records of the same strikes.
* **What it certifies.** The reporter-type confirmation rates (71% crew, 12% airport staff) reproduce every pilot airport-year's confirmed
  damaging count to within one occurrence, so a back-tester is confirmed at rung 2.
* **What it is blind to.** Multi-aircraft encounters (above).
* **Twin pair.** On 14 July 2025 at C and 9 September 2025 at D, each airport logged six damaging gull records with the same movements,
  hours, reporter mix and damage codes. C's six were three encounters, a flock striking two departures in each of three banks, and D's six
  were six encounters, 2.0× apart, separated only by the grouping.
* **Resemblance points at the decoy.** C's record profile matches the overlap airports, where records and encounters were one to one.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The grant rule: the unit (damaging wildlife encounters per 100,000 movements), the glossary's definition of an encounter,
  the model (movement offset, linear year, national excess), the 90% lower-bound standard over eight years, and carry-over when no airport
  meets it. The annual report's national counts of encounters and records. One sentence each.
* **Empirical pins.** The reporter-type confirmation rates, from the parallel run and the annual report; the grouping gap, from the absolute
  split (below).
* **Voices.** B's airport director: "Our staff reporting programme shows exactly how bad the geese have got." The authority's wildlife lead:
  "Damaging reports are the gold standard; nobody files one of those casually."
* **Licensed wrong basis.** The grant rule records that the airports' association ranks airports on growth in reported strikes and will
  present its ranking at the panel.

## 8. Determinism by construction

* **Grouping.** Strikes in one encounter follow each other within 12 minutes, and distinct encounters of one species group at one airport
  are at least 45 minutes apart, so every gap from 12 to 45 minutes groups identically and reproduces every published national count.
* **Species.** Every damaging record carries a species group, no encounter mixes groups, and no unknown-species record falls within 45
  minutes of another record at its airport.
* **Model variants.** C's bound stays below zero under Poisson or quasi-Poisson fits and at 80% or 90% bounds (−0.03 at its highest), so no
  defensible variant of the filed model turns the hold into a pick.
* **Movements.** The movement counts are the rule's exposure, with no fork between operations and flights.

## 9. Prompt sketch and deliverables

> The radar grant goes to one airport this year or carries over, and the panel sits on 14 November. B's director tells everyone their staff
> reporting shows how bad the geese have got. Tell me which airport gets the grant, or that it should carry over, in one line for the
> panel, with the figure that decides it to two decimals. Send `grant_case.xlsx`, a chart `hazard_trends.png`, and a one-page
> `panel_note.pdf`.

* `grant_case.xlsx` — the six airports on all four bases (ask C), the inspection sheet (ask A) and the closure sheet (ask B).
* `hazard_trends.png` — each airport's excess trend with its 90% interval on records and on encounters, side by side, the zero line drawn
  and labelled, C's records-per-encounter ratio by year annotated, and the verdict in the title.
* `panel_note.pdf` — the committed verdict, the blocking quantity, and what would have made it a pick.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each airport, the share of weekly airfield inspections in each of the last two years with grass
  height inside the policy band. *Device:* three airports switched their inspection form to centimetres in 2025, as the inspection guide's
  revision note says; reading those heights as inches puts every one of their 2025 inspections out of band. The hazard model never uses
  inspection data.
* **Ask B (device-carried).** For each airport, runway closure minutes for wildlife in the last twelve months and the number of closures.
  *Device:* a replacing notice carries the identifier of the notice it replaces and supersedes it, as the notice manual says; counting both
  double-counts a third of the closures at four airports.
* **Ask C (validity).** Each airport's lower bound under each of the four rung bases.
* **Decoupling.** Clearing the grouping and the damage calibration changes no figure in asks A or B.

## 11. Rubric arithmetic

6 airports × 2 years (ask A) + 6 × 2 (ask B) + 6 × 4 bases (ask C) + the committed verdict, the blocking quantity, its distance from the
line and the national trend + 5 named chart parts + 3 files ≈ 60 criteria.

## 12. World-building constraints

* Rung leaders A, B, C commit with lower bounds +0.62, +0.37 and +0.21; on encounters every airport's bound is negative, the best C at
  −0.08.
* C's damaging records per encounter rise smoothly from 1.02 (2018) to 1.42 (2025), every multi-aircraft encounter striking two or three
  departures in one bank; at the other five shortlisted airports every encounter strikes one aircraft. Nationally the ratio rises from 1.05
  to 1.19. Deflating by the national ratio leaves C at +0.12, and same-minute grouping at +0.19.
* With every strike captured and every damage code confirmed, A's all-strike bound is +0.55 and C's calibrated damaging-record bound +0.21.
* The nine overlap airports run no departure banks. The twin days are identical on every record-level column.
* Inspection records and closure notices never touch the strike database or the movement counts.