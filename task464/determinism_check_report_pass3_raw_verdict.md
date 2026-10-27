# Determinism verdict, task464

**Verdict:** NOT_DETERMINISTIC (competing_defensible_answer, Gate C, on "which comes nearest" in supplementary ask 3 and in the FINAL_RECOMMENDATION sentence "Bexhollow is the nearest ... 20 slots short"). Everything else reproduces.

**Disposition:** SEND_BACK. The nearest-miss tie has to be closed by pinning it in the prompt (or moving a figure in the inputs), and either change alters what solvers see, so a rerun is needed. The cheaper alternative, retargeting the ask, is a prompt change too.

**Why:** Reproduced from the files, Bexhollow and Durnsfield are both exactly 20 slots short on the golden's own rounding. Bexhollow has 312 slots against 332.16 required, which rounds to 332. Durnsfield has 170 against 189.62, which rounds to 190. Clause 4.4 says only "rounded once at the area level" and gives no direction. The ask is for the one area that "comes nearest". The golden's Bexhollow is not forced by any filed sentence:
- Unrounded gap: Durnsfield 19.62, Bexhollow 20.16, so Durnsfield is nearest.
- Round up: Bexhollow 21, Durnsfield 20, so Durnsfield is nearest.
- Round down: Bexhollow 20, Durnsfield 19, so Durnsfield is nearest.
- Round to nearest: a 20 and 20 tie.
- Shortfall as a percentage of required: Bexhollow 6.0 percent, Durnsfield 10.5 percent, so Bexhollow is nearest. This is the only reading that gives the golden.
The prompt asks for "its shortfall" in slots and sets no tie-break, so a literal reader cannot choose between them.

## Evidence (recomputed from /tmp/determinism-check-task464-079974/target/)

| Item | Claimed | Recomputed | Source |
|---|---|---|---|
| Sites in scope | 40 | 40 (cycle 2026, contract_intent_2027 = contract) | provider_directory_2027.csv |
| Deliverable positions | 274 (327 attested) | 274 (327 attested) | treatment_encounters.db, both tables, completed rows only |
| Per-site slots, 40 rows | as listed | all 40 match (positions x roster sessions x 1 for in-centre haemodialysis or 2 for ambulatory infusion) | staffing_roster_2026q4.csv, Schedule 4 clause 4.2 |
| Network slots | 3,886 | 3,886 | same |
| Area slots, 12 areas | as listed | all 12 match | same |
| Required per area | 244, 332, 270, 190, 238, 259, 334, 207, 433, 301, 520, 228 | all match, round-half | 2026 completed treatments / 52 x growth factor x 1.15 |
| Required total | 3,556 | 3,556 (raw 3,557.01; sum of area-rounded 3,556; ceiling gives 3,565) | same |
| Projected demand (critical component 2) | 3,092 | **3,093.05, so 3,093 (not reproduced)** | same |
| Six areas short | Bexhollow, Durnsfield, Granleigh, Innsmere, Kettlebrook, Lowenbrook | reproduces, margins clear (smallest gap 20) | same |
| Attested-stations route | three of the six areas flip to meeting | reproduces: Bexhollow, Granleigh and Kettlebrook flip; total 4,668 slots | directory attested_stations |
| Busiest-week route | 8 of 12 areas short | reproduces: 8 areas have busiest-week treatments below required | encounters, Monday-start week |
| Ask 4, out-of-network counts and shares, 48 figures | as listed | all 48 match | see below |
| Ask 5, licensed supply | 72 sites, per-area stations as listed | all match | state_licence_register.xlsx |
| Ask 6, sites dropped | 14 sites, per-area stations as listed | all match | state_adequacy_filing_2026.xlsx |

Notes on how the figures reproduce:
- **Encounter handling:** Cancelled and no-show rows carry no stop time or length (clause 4.4) and drop out. No completed row is missing a stop or length. The 2023 and 2024 table uses a local clock with a stop time; the 2025 and 2026 table uses a start with a UTC offset plus minutes. Both give consistent intervals.
- **Ask 4:** The count is service-date 2026 claims from the main file plus the run-out file (the 1,516 claims dated 2025 are excluded), placed in the area of the treating site by address. The share is out-of-network over in-network completed treatments plus out-of-network.
- **Ask 5:** The count uses facility rows covering 2027-02-19 (80 licences) with corporate rows excluded and OUT-OF-AREA excluded; the 8 OUT-OF-AREA rows are not in any of the twelve areas.
- **Ask 6:** The count is the 14 distinct sites after de-duplicating the five corporate-twin rows by address, with stations from the register row covering 2026-01-01. The filing's own licensed_stations gives the same figures for the non-corporate rows.

### Required reports
(a) **How the per-site ceiling is computed.** No filed sentence fixes HOW. Clause 4.2 says only "positions a Site is able to operate simultaneously". Every alternative reading lands on the same integer per site, 274 in total, with zero per-site differences:
- record maximum;
- yearly maximum, including the minimum across years;
- the 2025 and 2026 table alone;
- the minimum across monthly maxima;
- the 95th, 99th and 99.9th percentile over treating hours;
- the 99th and 99.9th percentile sampled at treatment starts.
Only the time-weighted median (153) and 90th percentile (261) diverge, and no reasonable reader would use those as a ceiling. The ceiling is therefore robust; it is a saturated, flat peak in the data.

(b) **Required figure per area from shipped files alone.** Yes. It needs the encounters, the growth factors in enrolment_projection_2027.csv, the 52-week definition, and the 1.15 multiple in clause 4.3. No shipped file states a capacity figure or ranks the areas against the standard. The filing's Area Summary lists licensed stations and 2025 treatments but no standard. Rounding direction is the one thing not filed.

(c) **Figures not reproduced.**
- CRITICAL_COMPONENTS 2: projected demand claimed 3,092, recomputed 3,093.05 (3,093 whole). 3,092 looks derived by dividing 3,556 by 1.15. This is a SOLUTION_WRONG item, not a determinism hole.
- Ask 3 and the final recommendation: "Bexhollow nearest" does not hold as a unique answer (see Why).

## Other forks noted (individually minor, not the governing failure)
- **Ask 4, half assignment:** "treatments paid for ... in that half" could be read by adjudication date. The reconciliation workbook is by adjudication quarter. Adjudication-date halves give different counts, for example Ammerly 567 and 580 against 572 and 559. The golden uses service date, which is the natural reading for a share of "the area's treatments" but is not stated.
- **Ask 4, area:** residence-area placement would change 11.5 percent of claims. Site area is the natural reading, but it is a reading.
- **Ask 5, population:** "on the state register" has no date in the prompt. The golden takes the register's own position date, 2027-02-19. A reader including lapsed or amended historical rows, or the 8 OUT-OF-AREA rows, gets other figures. The summary sheet's position date mostly settles it.
- **Ask 6:** "how many sites" counts 19 rows if a reader fails to de-duplicate the corporate twins. The prompt's word is "sites" and the twins share an address, so this is a clean reading.
- **Rounding direction (clause 4.4):** this one is load-bearing for the tie above.

## Files/Hygiene
**PASS**, none of it exclusion-level.
- **Count and formats:** 13 files in 5 formats (csv, pdf, xlsx, json, sqlite db). The encounters database has 639,009 rows.
- **Distractors:** nemt_trips_2026.csv, licence_fee_schedule_2026.pdf and the out-of-network reconciliation workbook are relevant but unused.
- **Temporal coherence:** one inconsistency. Clause 4.4 says the extract is taken after the 90-day run-out, but encounter_extract_transmittal.json says pulled_on 2027-01-05, which is only 5 days after year end; the latest service_date is 2026-12-26. This does not change any figure; it is a narrative inconsistency that a pedant could cite.
- **Provenance and realism:** nothing flagged on provenance or authoring leakage. Files read as system artifacts.
- **Cross-batch check:** I did not run it, because no other task folder was readable under this brief.

## Stump power
The 274 versus 327 gap is a real, high-leverage trap. A solver who takes the directory's attested stations, the register's licensed stations, or busiest-week counts files a different set of short areas: 3 of the 6 short areas flip to meeting, or 8 areas come out short. Getting to 274 needs a cross-layout interval reconstruction (stop time against start plus minutes plus offset) and a read of "operate simultaneously" as peak concurrency. A strong model plausibly falls for the 327. Since every ceiling reading gives 274, the decisive figure is deterministic. The margins on the six-short-areas call are all 20 slots or more.

## Stumping type
`mechanism: etl_conformance / capacity estimation from observed utilisation`, `stumping_family: analytical_non_defect`, `surface_read_dependency: borderline (leaning no)`, `sole_data_defect: no`. The difficulty is deriving peak concurrent positions from encounters. The attested and licensed station counts are overstated, though they are correct as attestations and licences and are not wrong numbers in themselves. Route to live testing if Gate G is in doubt.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical` (borderline data_semantics).
- **Layer 1:** two encounter layouts with different clocks, a preliminary file plus run-out, corporate umbrella licences, and amended licence rows.
- **Layer 2:** capacity estimated as observed peak concurrency, then tested against demand growth.
- **Easy route:** a strong analyst who read everything correctly could still file the 327 attested stations, giving 4,668 slots and only three short areas.
- **Caveat:** "operate simultaneously" in clause 4.2 points to concurrency, so some of this is a definition.

## Fix
**solution:** correct critical component 2 to 3,093 (or word it as derived from the required figure).
**prompt or input_files:**
1. Pin what "comes nearest" means, for example "nearest in whole slots, and if two tie, the one with the smaller shortfall as a percentage of its required figure". Alternatively change an input so the nearest area is unique under every rounding direction. For example, move Bexhollow or Durnsfield by a few slots so the gap is at least 2 slots different under the unrounded, round and ceiling readings.
2. File the rounding direction in clause 4.4.
3. Say in the ask which date puts a treatment in a half (service date).
After the fix, only the area xlsx nearest-area cell and the final recommendation's sentence change; every other figure is unaffected.
