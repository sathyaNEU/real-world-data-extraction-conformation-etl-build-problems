# AD29 — Which airport gets this year's wildlife radar grant, or does it carry over, when strikes are counted in reports and the grant counts encounters

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Policy & Education · aviation safety oversight |
| Mirrors | Counting incidents rather than reports when reporting channels multiply (one app crash arriving from the device and from the SDK at Apple and Google, product-safety complaints at Amazon that arrive through several channels for one incident, duplicate bug-bounty submissions at Meta) |
| Decision shape | Hold, forced by a blocking quantity: the radar grant goes to one of six shortlisted airports or carries over |
| Committed call | The airport awarded the grant, or that it carries over, with the evidence figure that decides it, at the grant panel on 14 November |
| Gap · Pattern | Gap 2 (population: the unit the grant counts is not the unit the file stores) · the unit not stored, built by attaching reports to encounters, with a damage code validated on one reporter population and applied to another below it |
| Gate G mechanism | signal_vs_noise_or_hold, with method_or_model_selection support |
| Measured traps engaged | #2 counts file rows instead of the real unit · #13 validates on one population, applies to another · #8 papers over a failed reproduction |
| Calibration form | Parallel-run overlap: 2022–2023, when mandatory occurrence reporting (one record per occurrence) ran alongside the voluntary strike database at nine pilot airports |
| Driving force | The strike database holds one row per report, and every hazard statistic counts rows. The grant counts encounters, and a damaging encounter can arrive twice: from the crew and from the engine shop that finds the damage days later. At C a carrier has been moving heavy maintenance in since 2019, so a growing share of C's damaging encounters are reported twice. Attaching each shop report to its encounter (the latest crew report for that registration before the inspection date) flattens C's rise, and on encounters no shortlisted airport clears the evidence line. |

## 1. Situation

The national aviation safety authority has one wildlife-detection radar grant of $2.4M this year. The grant rule awards it to a shortlisted
airport whose damaging strike encounters per 100,000 movements have risen faster than the national rate, with the lower 90% bound of the
excess trend above zero over the last eight years; if no airport meets that, the grant carries to next year. Six airports were
shortlisted on reported-strike growth. The authority holds the voluntary strike database (one row per report: crew, engine shop or
airport staff), the movement counts, the occurrence records from the 2022–2023 parallel run, and its annual report. B's airport director
is lobbying hard.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each report is a real report of a real strike, the movement counts tie to air traffic records, and
  the annual report's confirmation rates are right. B's director is right that B's staff file more reports than ever. Nothing reported is
  overturned; the difficulty is building the unit the grant counts.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the director's lobbying and the shortlist's growth figures. A model of damaging reports per movement, with
  damage calibrated by reporter type, still clears C, and still funds it.
* **Instrument repair.** Make every report perfectly coded and every damage code confirmed. A perfect report is still a report, and an
  encounter seen by both the crew and the shop is still two of them.
* **Lens swap.** The naive count is reports; the answer counts encounters, a different population in both directions (C's duplicates
  leave, shop-only encounters at other airports stay), and the verdict changes from a pick to a hold.

## 3. The driving force

A strong solver discards all-strike growth, keeps damaging strikes as the rule says, notices that airport staff code uncertain damage far
more freely than crews, calibrates damage by reporter type from the authority's published confirmation rates, fits the rule's model and
finds C's lower bound clear of zero. Every step is correct, and every step counts rows. An engine-shop report is a second sighting of an
encounter the crew usually reported already, made at the shop's inspection days later, and the dictionary says so only by describing the
shop report's fields. At C the share of damaging encounters inspected at C's own maintenance base rose from 8% to 61% over the window, so C's
damaging reports rose while its encounters did not. Dropping shop reports does not fix it, because 40% of shop reports elsewhere are the
only record of a real encounter that the crew never noticed. Only attaching each shop report to the latest crew report for that aircraft
before its inspection date (or keeping it as its own encounter where none exists) builds the unit.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Excess trend in all reported strikes per 100,000 movements over the national trend | Fund A (lower bound +0.62) | It is the shortlist's own measure, offset by movements and judged against the nation | The grant rule counts damaging encounters only |
| 1 | Excess trend in damaging reports (codes minor and above, uncertain included) | Fund B (lower bound +0.37) | Damaging strikes are what the rule names, and B's rise is steep | The annual report: uncertain-damage codes are confirmed for 71% of crew reports and 12% of airport-staff reports, and B's rise is staff reports |
| 2 | Damaging reports with uncertain codes weighted by reporter-type confirmation (the parallel run reproduces each rate) | Fund C (lower bound +0.21) | Calibrated, exposure-adjusted, national-relative and validated on the overlap | The dictionary's shop-report fields: shop reports carry an inspection date, and at C 61% of damaging encounters now arrive twice |
| 3 | **Decisive:** attach each shop report to its encounter (latest crew report for the registration before the inspection date, or its own encounter if none), then the same calibrated model on encounters | **Hold: the grant carries over** | — | — |

* **The blocking quantity.** On encounters, the best lower 90% bound across the six airports is C's, at −0.08 damaging encounters per
  100,000 movements per year, 0.08 below the rule's zero line. The others sit at A −0.31, B −0.22, D −0.15, E −0.12 and F −0.27, so every
  candidate fails on the same standard.
* **Partial correction priced (L3).** A solver who sees the shop reports and drops them as a reporter-type filter clears C and funds E, at a
  lower bound of +0.14, 0.14 above the line, with the next best (D) at −0.02: E's crew reports rose while its shop-only encounters fell as
  the carrier moved maintenance away, so the filter fails in both directions and lands on a new name rather than on the hold.
* **Grid.** Damage basis (all strikes, raw damaging, calibrated damaging) × unit (reports, shop reports dropped, encounters) = 9 cells.
  Every cell but (calibrated, encounters) commits to A, B, C or E with a positive bound; only that cell holds.
* **Falsifiable.** C would have qualified with a trend 0.08 higher, about seven more damaging encounters over the last four years, or with
  three more years at its current trend narrowing the bound.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The dictionary defines each report type's fields, including the shop report's inspection date and the airport of
   the aircraft's last departure. No document says reports and encounters differ or describes attaching one to the other.
2. **Corpus blind for a computable reason.** *In every overlap airport-year the voluntary database holds one report per damaging occurrence,
   because none of the nine pilot airports hosts a heavy-maintenance base, the only source of second reports.* The overlap reproduces rung
   2's calibration exactly and cannot see duplication.
3. **No arithmetic symptom.** Report IDs are unique, no two rows are duplicates on any key, movement totals tie, and the reporter-type
   counts match the annual report.
4. **Not a row predicate.** It needs, per registration, the latest crew report before each shop report's inspection date (a group and a rank
   inside it), with unmatched shop reports kept as encounters, before the trend model is fitted.
5. **The enumeration is arithmetic.** No column marks a report as a second sighting, and dropping a reporter type is wrong in both
   directions.
6. **No cutover date.** The carrier moved maintenance to C gradually from 2019 to 2025, so the duplicate share rises smoothly and no series
   steps.
7. **Survives deletion.** Remove the director, the shortlist figures and every voice: the report-grain model is still the natural build.

## 6. The calibration corpus

* **Form.** The 2022–2023 parallel run at nine pilot airports: every mandatory occurrence record (one per occurrence, damage confirmed by the
  operator) beside the voluntary reports of the same strikes.
* **What it certifies.** The reporter-type confirmation rates (71% crew, 12% airport staff) reproduce every pilot airport-year's confirmed
  damaging count to within one occurrence, so a back-tester is confirmed at rung 2.
* **What it is blind to.** Second reports (above).
* **Twin pair.** In 2025, C and D each logged 30 crew and 30 shop damaging reports, with identical movements, reporter mix and damage codes.
  C's shop reports all attach to its crew reports (30 encounters) and D's shop reports are all shop-only finds (60 encounters), a 2.0× gap
  separated only by the attachment rule.
* **Resemblance points at the decoy.** C's report profile matches the overlap airports, where reports and occurrences were one to one.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The grant rule: the unit (damaging strike encounters per 100,000 movements), the model (movement offset, linear year,
  national excess), the 90% lower-bound standard over eight years, and carry-over when no airport meets it. The dictionary's report-type
  fields. One sentence each.
* **Empirical pins.** The reporter-type confirmation rates, from the parallel run and the annual report; the attachment rule, by
  convergence (below).
* **Voices.** B's airport director: "Our staff reporting programme shows exactly how bad the geese have got." The authority's wildlife lead:
  "Damaging reports are the gold standard; nobody files one of those casually."
* **Licensed wrong basis.** The grant rule records that the airports' association ranks airports on growth in reported strikes and will
  present its ranking at the panel.

## 8. Determinism by construction

* **Attachment.** Every shop report has at most one crew report for its registration in the 30 days before inspection, so latest-before,
  nearest and any-in-window rules attach identically; unmatched shop reports have none in 90 days.
* **Model variants.** C's bound stays below zero under Poisson or quasi-Poisson fits and at 80% or 90% bounds (−0.03 at its highest), so no
  defensible variant of the filed model turns the hold into a pick.
* **Shop-only encounters.** They take the airport of the aircraft's last departure, as the dictionary records, so their location is filed.
* **Movements.** The movement counts are the rule's exposure, with no fork between operations and flights.

## 9. Prompt sketch and deliverables

> The radar grant goes to one airport this year or carries over, and the panel sits on 14 November. B's director tells everyone their staff
> reporting shows how bad the geese have got. Tell me which airport gets the grant, or that it should carry over, in one line for the
> panel, with the figure that decides it to two decimals. Send `grant_case.xlsx`, a chart `hazard_trends.png`, and a one-page
> `panel_note.pdf`.

* `grant_case.xlsx` — the six airports on all four bases (ask C), the inspection sheet (ask A) and the closure sheet (ask B).
* `hazard_trends.png` — each airport's excess trend with its 90% interval on reports and on encounters, side by side, the zero line drawn
  and labelled, C's duplicate share annotated, and the verdict in the title.
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
* **Decoupling.** Clearing the attachment rule and the damage calibration changes no figure in asks A or B.

## 11. Rubric arithmetic

6 airports × 2 years (ask A) + 6 × 2 (ask B) + 6 × 4 bases (ask C) + the committed verdict, the blocking quantity, its distance from the
line and the national trend + 5 named chart parts + 3 files ≈ 60 criteria.

## 12. World-building constraints

* Rung leaders A, B, C commit with lower bounds +0.62, +0.37 and +0.21; on encounters every airport's bound is negative, the best C at −0.08.
* C's share of damaging encounters inspected at its own base rises smoothly from 8% (2018) to 61% (2025). Elsewhere 40% of shop reports
  are shop-only encounters.
* E's crew reports rise while its shop-only encounters fall, so the reporter-type filter funds E at +0.14, with D next at −0.02.
* The nine overlap airports host no maintenance base. C and D are identical on every report-level column in 2025.
* Inspection records and closure notices never touch the strike database or the movement counts.
