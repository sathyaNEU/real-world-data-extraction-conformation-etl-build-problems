# AD22 — What incident rate the defects office files in its opening resume, when only one construction reproduces every rate it has published before

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Policy & Education · vehicle safety regulation |
| Mirrors | Computing a failure rate at the unit and exposure the publisher's own series uses (field-quality rates behind automaker recall decisions, failure rates per active device at Apple and Google, failures per unit-year in service in hyperscale hardware fleets) |
| Decision shape | One figure committed at a date: the subject vehicles' incident rate in the preliminary-evaluation opening resume published on 20 November 2026 |
| Committed call | The incident rate per 100,000, to one decimal, for the subject group's model years 2011–2014 over the 24-month window |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · a reproduction-gated control set (E01) whose exact construction includes exposure built behind a join, with the unit the rate counts not stored (E02) at the lower rung |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution support |
| Measured traps engaged | #1 reports a failed back-test, ships anyway · #3 stops at a close but inexact match · #2 counts file rows instead of the real unit |
| Calibration form | Published control set with a reproduction clause: the rates in the office's last 14 opening resumes, which the procedures manual says any resume method must reproduce |
| Driving force | Every rate the office has published counts linked incidents dated by when they happened, over vehicle-years in service: monthly registration snapshots of the group's model years, summed across the window. For a decade-old group a fifth of the cars scrapped during the window, so dividing by vehicles built understates the rate by nearly half, and a single snapshot at either end misses it by 14–16%. The two corrections a careful analyst makes first both push the rate down; the exposure construction, which only the published series reveals, pushes it back above where the analyst started. |

## 1. Situation

A national vehicle-safety regulator's defects office opens a preliminary evaluation into an engine-compartment fire on one make's model
years 2011–2014. The opening resume, published on 20 November, states the group's incident rate. The office's procedures manual says a
resume's rate is computed by the method that reproduces every rate published in the office's earlier resumes; it defines a rate as counting
incidents. The pack carries the public complaint file (one row per complaint, the last six VIN characters masked), production volumes by
model year, the monthly registration snapshots by make, model and model year, the last 14 resumes, and the manufacturer's early-warning
filings.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each complaint, each production volume, each registration snapshot and each published rate. The
  screening engineer's complaint spike is real. Nothing reported is overturned and no stakeholder read is corrected; the difficulty is
  building the unit and the exposure that every published rate was computed on, which no document spells out.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices. Linking complaints into incidents, dating them by incident and dividing by vehicles built, the
  natural careful build, still lands at 13.1, 46.5% low.
* **Instrument repair.** Suspect file: the public complaint file, which masks the last six VIN characters and holds one row per complaint
  where the manual counts incidents. Repaired at every depth, every VIN in full and one row per incident, rung 0 lands on rung 1's 15.1
  (−38.2%), rung 1 stays at 15.1 and rung 2 at 13.1 (−46.5%). Production and the 24 monthly snapshots are complete. Vehicles in service
  exist only as a sum over the snapshots, and no file records vehicle-years, so the exposure construction is still needed for 24.5.
* **Lens swap.** The naive rate divides by the population of vehicles built; the answer divides by vehicle-years actually on the road in
  the window, a population that shrinks by a fifth across it.

## 3. The driving force

A strong solver reads that a rate counts incidents, links complaints filed by an owner, a dealer and an insurer about one fire on make,
model year, incident date, state and the eleven visible VIN characters, moves the publicity spike's old incidents back to the dates they
happened, and divides by vehicles built. It reproduces 8 of the 14 published rates, notes the misses as older groups, and files 13.1. Each
step is competent and each pushes the rate down. The published rates were computed on exposure, not production: the sum over the window's
24 monthly registration snapshots of the group's model years in service, a construction across a second file. For new vehicles the two
nearly coincide, which is why eight rates reproduce; for a decade-old group, survival runs from 62% to 46% across the window, and
vehicle-years are 53.5% of vehicles built times two years. A single snapshot at the window's start or end, the close but inexact readings,
reproduces 11 of 14. Only summed monthly vehicle-years reproduce all fourteen, and the rate is 24.5.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Complaints received in the window per 100,000 vehicle-years built (vehicles built × 2 years) | 21.5, −12.0% | The complaint file and the production table, used as published | The manual: a rate counts incidents, and one fire is often filed by the owner, the dealer and an insurer |
| 1 | Complaints linked into incidents on make, model year, incident date, state and the visible VIN characters | 15.1, −38.2% | The unit the manual names, built by an exact link | The resumes: every published rate dates incidents by when they happened, and the publicity spike carries fires up to six years old |
| 2 | Incidents dated by incident date inside the window | 13.1, −46.5% | Reproduces 8 of the 14 published rates, the stimulated reporting removed | The published rates: the six misses are the oldest groups, all published higher than this build gives |
| 3 | **Decisive:** incidents over vehicle-years in service, the 24 monthly registration snapshots of the group's model years summed | **24.5** | — | — |

* **Figure shape.** The two corrections walk the rate down and the decisive move reverses them past rung 0. Per-rung offsets are −12.0%,
  −38.2% and −46.5%; cells that take the exposure without one of the corrections land above the answer, so the failure directions bracket
  it.
* **Partial correction priced (L3).** A solver who divides by a single registration snapshot reproduces 11 of 14 rates and lands at 21.1
  (start, −13.7%) or 28.5 (end, +16.3%). A solver who builds vehicle-years but skips the incident dating lands at 28.3 (+15.5%).
* **Grid.** Unit (complaints or incidents) × dating (received or incident) × exposure (built, start snapshot, end snapshot, vehicle-years)
  gives sixteen cells. The nearest wrong cell is rung 0 itself at −12.0%; every cell with vehicle-years but a missing correction sits at
  least 15.5% above, every cell without vehicle-years at least 12% away.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The manual says a rate counts incidents and must reproduce the published rates. No document defines the denominator,
   and the registration snapshots are filed for fleet statistics.
2. **The corpus pins a construction, not a menu.** Summed monthly vehicle-years reproduce 14 of 14 published rates to two decimals; single
   snapshots 11, vehicles built 8, and every rival's misses are published rates it understates, so each also fails on the fourteen's mean.
   The exposure is a construction: a sum over 24 monthly snapshots of a model-year set, joined from a second file, with no column holding it.
3. **No arithmetic symptom.** Complaints tie to the public file, incidents to their linked complaints, production to the manufacturer's
   filings; every rate computes cleanly under every denominator.
4. **Not a row predicate.** It needs a three-way link to build incidents, a date window on the incident, and a sum of snapshot counts over
   months and model years.
5. **The enumeration is arithmetic.** Vehicle-years are computed from snapshots; the published rates admit no other exposure.
6. **No cutover date.** Scrappage is gradual across the window; the only dated event, a television report that set off the complaint spike,
   sits in the rung below.
7. **Survives deletion.** With every voice removed, the answer and the difficulty are unchanged.

## 6. The calibration corpus

* **Form.** The office's last 14 opening resumes: each subject group, its window and its published rate to two decimals; the complaint
  files, production and registration snapshots for those windows ship with them. The manual makes reproducing every one the condition of a
  method.
* **What it pins.** Linked incidents, incident dating and summed monthly vehicle-years reproduce all 14. Vehicles built reproduce the 8
  groups under five years old; start and end snapshots reproduce 11.
* **Twin pair.** Resumes PE-19-04 and PE-21-11 are identical on complaints, linked incidents, vehicles built, model-year span and component.
  Their published rates are 19.7 and 36.1 (1.83×): PE-21-11's group was four years older, with vehicle-years 55% of PE-19-04's. Only the
  exposure construction separates them.
* **Every rule exercised.** One resume's window crossed a model year's end of sale, so newly registered vehicles enter mid-window; one
  resume's incidents were filed only by insurers, so the link is tested without an owner report.
* **Resemblance points at the decoy.** The subject group's complaint profile most resembles PE-19-04's, a young group whose rate the
  vehicles-built build reproduces.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The procedures manual: a resume's rate is computed by the method that reproduces every rate in the office's earlier
  resumes; a rate counts incidents. The resume's window: the 24 months to the end of September 2026.
* **Empirical pins.** The incident link, incident dating and summed monthly vehicle-years, from the published rates.
* **Voices.** The screening engineer: "The complaint spike tells you all you need about this car." The manufacturer's liaison: "These cars
  were built a decade ago; any rate should be over what we built."
* **Licensed wrong basis.** The manual records that the manufacturer's safety office computes rates per 100,000 vehicles built and will
  present its own rate when the evaluation opens.

## 8. Determinism by construction

* **Link.** No two complaints share make, model year, incident date, state and visible VIN without describing one fire; the link is exact.
* **Snapshots.** Registration snapshots are taken on the last day of each month; summing 24 or averaging them and multiplying by two years
  gives the same exposure.
* **Window.** Incident dates are complete for the window; the extract is taken 45 days after its close, and the office's resumes use the
  same lag.
* **Rounding.** 24.5 sits mid-bin at one decimal; the nearest cell rounds to 21.5.

## 9. Prompt sketch and deliverables

> The opening resume for the engine-fire evaluation is published on 20 November and has to state the subject vehicles' incident rate per
> 100,000, to one decimal. Our screening engineer thinks the complaint spike says it all. Give me the rate as a sentence for the resume, with
> `pe_rate.xlsx` holding the sheets below, the chart `rate_reproduction.png`, and a short `resume_insert.docx`.

* `pe_rate.xlsx` — the incident and exposure build, the recall sheet (ask A), the early-warning sheet (ask B) and the reproduction table (ask C).
* `rate_reproduction.png` — the 14 published rates against each construction's reproduction as four panels, the twin resumes labelled, and
  the subject group's monthly vehicles in service across the window as an inset.
* `resume_insert.docx` — the committed rate and the readings the manufacturer will raise.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the eight groups on this quarter's screening list, recall campaigns in the last five
  years and the latest remedy completion rate. *Device:* a campaign whose remedy is revised is reissued under a supplemental number linked to
  the original, and completion is reported against the supplemental, per the recall file guide. Reading completion off the original
  campaign understates it for the three groups with revised remedies. The rate build never reads recall files.
* **Ask B (device-carried).** For each of the eight groups, death and injury claims in the manufacturer's early-warning filings over the
  last four quarters, and the share later revised. *Device:* a claim is reported in the quarter received and re-reported with a revision
  flag when updated, as the filing instructions say. Summing quarters double-counts every revised claim.
* **Ask C (validity).** For each of the four rung constructions, the published rates it reproduces out of 14.
* **Decoupling.** Clearing the exposure construction changes no figure in asks A or B.

## 11. Rubric arithmetic

8 groups × 2 (ask A) + 8 groups × 2 (ask B) + 4 constructions (ask C) + the committed rate, its linked incidents and its vehicle-years + 5
named chart parts + 3 files ≈ 47 criteria.

## 12. World-building constraints

* 612 complaints link into 430 incidents, 372 dated inside the window; 1.42 million vehicles built; survival from 62% to 46% across the
  window, vehicle-years 53.5% of built × 2 years.
* Rung figures are 21.5 / 15.1 / 13.1 / 24.5; snapshots give 21.1 and 28.5; every grid cell sits at least 12% from the answer.
* The 14 published rates reproduce under the exact construction; the 8 groups under five years old also reproduce on vehicles built.
* PE-19-04 and PE-21-11 are identical on every complaint and production column; their rates are 19.7 and 36.1.
* Supplemental recall campaigns and revised early-warning claims never touch the complaints or the snapshots.
