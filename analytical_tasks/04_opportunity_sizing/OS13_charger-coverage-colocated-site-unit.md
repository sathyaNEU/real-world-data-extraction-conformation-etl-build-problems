# OS13 — How many residents the four funded fast-charging sites newly cover, when two stations already near them are single sites split across two networks

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Policy & Education · public infrastructure programmes |
| Mirrors | Reporting the incremental reach of new capacity when the existing footprint is recorded at the wrong unit (new cell sites next to small cells two carriers share at one mast, new Amazon lockers beside clustered third-party pickup points, coverage claims at Google Fi or Starlink where the existing network's reliability defines what counts as covered) |
| Decision shape | One figure committed at a date: newly covered residents, stated in the federal deployment plan |
| Committed call | Residents newly within 10 miles of a qualifying fast-charging site once the four funded sites open, to the nearest thousand |
| Gap · Pattern | Gap 2 (population) over Gap 1 (time) · L1 (the closed record certifies every rung below and is blind to the decisive one), with the unit the standard defines built from records (#2), over a saturated uptime measure (#19) |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #2 counts file rows instead of the real unit · #19 breaks a big tie instead of questioning it · #12 stops at the first control that passes |
| Calibration form | Retry or revision log: the networks' session-attempt log (every attempt, fault code and retry) and the station revision log, from which each closed report year's station set and published coverage figure are rebuilt |
| Driving force | The federal standard counts sites, meaning the ports within 200 m of one another, and the station file keeps one record per network. Two travel plazas near the funded sites each hold two 2-port records from different networks. Neither record has the four ports a site needs; each pair qualifies together, and the two plazas already cover 63,000 of the residents the funded sites would reach. Every closed report year reproduces at record level, because no two fast-charging records stood within 200 m of each other before this year's paired installations. |

## 1. Situation

A state energy office has funded four fast-charging sites in its northern counties, and its federal deployment plan, due on 1 December,
must state how many residents they newly bring within 10 miles of a qualifying site. The federal standard defines a site, its
qualification (four or more CCS ports of 150 kW and 97% uptime over the trailing twelve months) and the coverage measure. The national
station file lists every network's stations as records. Each network reports quarterly uptime, and the networks share a session-attempt
log with the office. The office has published its coverage figure every year since 2022. The draft plan added up the four sites'
catchment populations.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the catchments, the station file, the operators' uptime reports, the session log and the
  published coverage figures. The operators' reports are right about the outages they log. No stakeholder read is overturned. The
  difficulty is the unit the standard counts and the reliability it requires, both built from records.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the draft's figure and every voice. Union coverage on the station records, with uptime from the session log,
  still reproduces every closed report year and still lands 59% high.
* **Instrument repair.** Make every station record and uptime figure exact. Records stay one per network, and the plaza pairs are still
  two records making one site.
* **Lens swap.** The naive read is records; the answer is sites, a different entity that only a spatial grouping of records forms.

## 3. The driving force

A strong solver unions the four catchments, removes residents already covered, and rebuilds every closed report year to check its
method. The office's published figures do not reproduce on the operators' reported uptime, which reads 100% for 41 of 47 stations. They
do reproduce on uptime rebuilt from the session-attempt log, where three stations near the funded sites fall below 97%. That correction is
certified 4 of 4, so the solver files 170,000. But the standard counts sites, not records. This year two networks each installed two
ports at the Harlan and Pike Creek travel plazas, 90 m and 150 m apart. Each record has two ports, and each plaza's pair has four and
qualifies. No closed year had any pair to group, so record-level counting reproduces every one of them. The two plazas already cover
63,000 of the residents the funded sites would reach.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Sum of the four sites' 10-mile catchment populations | 412,000 (+285%) | The draft's figure, from census block populations | The station file: catchments overlap each other and existing stations |
| 1 | Union of the catchments less residents already covered by qualifying station records, on reported uptime | 122,000 (+14.0%) | Overlaps removed against the existing network | The published figures: on reported uptime the method reproduces 1 of 4 closed years |
| 2 | The same with uptime rebuilt from the session-attempt log (three nearby stations fall below 97%) | 170,000 (+58.9%) | Reproduces all four closed report years exactly | The standard's site definition with the station coordinates: the Harlan and Pike Creek pairs are two sites of four ports each |
| 3 | **Decisive:** existing coverage counted by sites (records within 200 m grouped), qualification tested per site | **107,000 residents** | — | — |

* **Figure shape.** The answer is bracketed: rung 1 sits 14.0% above it, and the nearest cell below (sites on reported uptime) sits 44.9%
  below. Rung 2's certified correction moves the figure up, and the decisive move takes it back down past where the solver began.
* **Partial correction priced (L3).** A solver who groups records into sites but keeps the reported uptime lands at 59,000 (−44.9%),
  further from the answer than rung 1. One who groups records by street address instead of distance merges neither plaza (each pair's
  records carry different frontage addresses) and stays at rung 2.
* **Grid.** Counting (sum, union) × uptime (reported, session log) × unit (records, sites) gives 8 cells: 216,000, 153,000, 264,000,
  201,000, 122,000, 59,000, 170,000 and the answer. The nearest wrong cell is rung 1 at +14.0%, and reaching it costs the uptime reading
  the closed years refute.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The standard defines a site as ports within 200 m. Nothing says the station file's records are not sites, or that
   any pair near the funded sites needs grouping.
2. **Corpus blind for a computable reason.** *In every closed report year record-level and site-level counting selected the same
   stations, because no two fast-charging records stood within 200 m of each other before this year's paired installations.* Rung 2
   reproduces all four years exactly.
3. **No arithmetic symptom.** Port totals reconcile to the station file, catchments to census totals, and the rebuilt figures to every
   published year.
4. **Not a row predicate.** Sites need a spatial grouping of records from coordinates, port counts summed per group, the standard tested
   per group, and coverage recomputed against the funded catchments.
5. **The enumeration is arithmetic.** No column names a site; records carry their own networks and addresses.
6. **No cutover date.** The plaza pairs are simply present in this year's file; no series steps, and the coverage figure has no event to
   align.
7. **Survives deletion.** Removing the draft and the voices leaves the certified rung 2 intact and wrong.

## 6. The calibration corpus

* **Form.** The station revision log (every record's opening, port and status changes) and the session-attempt log, from which the
  office's published coverage figures for 2022–2025 are rebuilt.
* **What it certifies.** Union coverage and session-log uptime, 4 of 4 years exactly. Reported uptime reproduces 1 of 4, and its misses all
  run high because it counts unreliable stations as covering.
* **What it is blind to.** Grouping records into sites (above).
* **Twin pair.** Funded sites Corrin Junction and Maple Flats are identical on catchment population (96,000), terrain and record-level
  existing coverage (none). Corrin Junction's catchment holds the Harlan plaza, whose pair covers 48,000 of it; Maple Flats' holds nothing.
  They newly cover 48,000 and 96,000, 2.0× apart, separated only by grouping records into sites.
* **Resemblance points at the decoy.** The funded sites' catchments most resemble those of the 2024 report's new stations, whose
  record-level count reproduced exactly.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The federal standard: a site is the set of DC fast ports within 200 m of one another; it qualifies with four CCS ports
  of 150 kW and 97% uptime over the trailing twelve months; a minute is down if any session attempt in it fails with a charger fault; a
  resident is covered when the population point of their census block lies within 10 miles of a qualifying site, measured as great-circle
  distance × 1.25. The plan template: the figure is residents newly covered once the funded sites open.
* **Empirical pins.** Uptime, from the session log. Sites, from the station coordinates.
* **Voices.** The programme director: "Every one of our four sites sits in a charging desert." The networks' liaison: "Our stations are
  up all the time; the quarterly reports say so."
* **Licensed wrong basis.** The plan template records that the federal reviewer's checklist compares each plan's figure with the sum of
  its sites' catchment populations and will present that comparison.

## 8. Determinism by construction

* **Grouping.** The plaza pairs' records sit 90 m and 150 m apart, and no other two records lie within 1 km, so any grouping radius from
  200 m to 1 km forms the same sites.
* **Uptime.** The three failing stations run 94.1%, 95.6% and 96.2%; every other station is above 98.5%, so no rounding of the session
  log moves a station across 97%.
* **Boundaries.** No block's population point lies within 0.05 miles of any 10-mile boundary, so distance rounding changes no block.
* **Maturity.** The trailing twelve months of the session log are complete to the extract date.
* **Rounding.** The committed figure is 107,000, exact at the nearest thousand.

## 9. Prompt sketch and deliverables

> The federal deployment plan goes in on 1 December and it has to say how many residents our four funded fast-charging sites newly cover,
> to the nearest thousand. The programme director's view is that every one of them sits in a charging desert. Give me the figure as a
> sentence for the plan, with `coverage_build.xlsx`, a map `coverage_sites.png`, and a one-page `plan_coverage_note.pdf`.

* `coverage_build.xlsx` — the four bases, the closed-year rebuild, the site grouping, the pricing sheet (ask A) and the make-ready sheet
  (ask B).
* `coverage_sites.png` — a script-rendered map: the four funded sites' 10-mile circles, existing sites marked by whether they qualify,
  the Harlan and Pike Creek pairs drawn as two records ringed into one site, the three failing stations crossed, and newly covered blocks
  shaded.
* `plan_coverage_note.pdf` — the committed figure and the bridge from the draft's catchment sum.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the five networks, the average price per kWh customers actually paid last quarter and
  the share of energy sold under membership plans. *Device:* membership sessions bill at list price with a separate plan-credit line
  carrying the session number, as the settlement guide documents. Ignoring the credit lines overstates the price for the three networks
  with plans.
* **Ask B (device-carried).** For each funded site, the utility's make-ready contribution and the true-up against its estimate. *Device:*
  the utility bills make-ready in milestones, and its final true-up line reverses part of an earlier estimate. Summing every line
  overstates the contribution at two sites.
* **Ask C (validity).** The committed figure under each of the four rung bases, and each closed report year as rebuilt on reported uptime
  and on session-log uptime.
* **Decoupling.** Counting records instead of sites changes no figure in asks A or B. Settlement credits and make-ready invoices touch
  neither the station file nor the session log.

## 11. Rubric arithmetic

5 networks × 2 (ask A) + 4 sites × 2 (ask B) + 4 bases and 4 years × 2 (ask C) + the committed figure, the three failing stations, the two
grouped sites and the twin gap + 5 named chart parts + 3 files ≈ 42 criteria.

## 12. World-building constraints

* Catchment sum 412,000; union 318,000; residents already covered by qualifying records on reported uptime 196,000, of whom 48,000 sit only
  near the three stations under 97%; residents covered only by the two plaza sites 63,000. The two areas are disjoint.
* Rung figures 412,000 / 122,000 / 170,000 / 107,000; grid cells as listed.
* No two fast-charging records within 200 m before this year; the plaza pairs are the only groups.
* Corrin Junction and Maple Flats match on catchment, terrain and record-level coverage.
* Settlement credits and make-ready invoices never touch station records or session attempts.
