# Verdict, task464 (re-judge, repaired pack)

**Verdict:** NOT_DETERMINISTIC (competing_defensible_answer on the main call via underspecified_objective; every golden figure reproduces, so no SOLUTION_WRONG).

**Disposition:** SEND_BACK. Schedule 4 clause 4.2 must say what evidence fixes "deliverable treatment positions", and the out-of-network file must say what a header line is. Both change what solvers see, so a model rerun is required. (A narrower FIX_NOW is not available because the fix touches shipped input files.)

**Why:** Clause 4.2 defines positions only as "the treatment positions a Site is able to operate simultaneously". No shipped sentence ties that to the encounter extract, and the directory (`attested_stations`) and the register (`licensed_stations`) each supply a station count per site. The golden's 274 positions is the greatest number of a site's own treatments running at one time. Attested stations (327) and licensed stations (351, the register row covering 2027-02-19) are both reachable readings of "able to operate". They change the main call: 3 areas below (Durnsfield, Innsmere, Lowenbrook) on attested stations and 2 (Durnsfield, Innsmere) on licensed stations, against 6 in the golden. Only inference, or the write-up's own "Not the stations the directory attests", chooses the golden reading. Separately, Ask 4 rests on an unstated reading of `line_no` 0 (see Evidence).

## Evidence (recomputed from /target)

| Value | Claimed | Mine | Source |
|---|---|---|---|
| Positions, 40 contract sites | 274 | 274 | treatment_encounters.db, both tables, completed rows with a stop or minutes |
| Attested stations | 327 | 327 | provider_directory_2027.csv, 2026 cycle |
| Network slots | 3,886 | 3,886 | positions x roster sessions x 1 (haemodialysis) or 2 (infusion) |
| 2026 completed treatments, 40 sites | (not stated) | 149,773 | encounters, 2026 service date |
| Demand | 3,095 | 3,095.18 | treatments / 52 x growth factor |
| Required | 3,568 | 3,568 | ceil(1.15 x demand) per area |
| Areas below standard | 6 | 6 | Bexhollow, Durnsfield, Granleigh, Innsmere, Kettlebrook, Lowenbrook |

- **Asks 1 to 3:** all 40 site slot figures and all 12 area slots, required figures and shortfalls reproduce. The shortfalls are 23, 20, 23, 48, 35 and 24.
- **Directory and roster:**
  - Intent exists only on the 2026 cycle (attested 2026-11-18), which is the cycle current at 2027-02-19. It gives 40 contract sites and 14 none.
  - Areas are identical across the three cycles.
  - The roster has one effective date, 2026-10-01.
  - Sessions equal days x shifts for all 40 sites.
- **Ask 5 (licensed supply):** reproduces for all 12 areas (72 sites, 591 stations).
  - Method: facility rows covering 2027-02-19; the 40 corporate-umbrella rows are excluded.
  - The 8 OUT-OF-AREA rows fall outside the twelve areas.
  - Lapsed rows and rows ended before the date drop out.
  - The reissued ESRD-44023 now sits at Ferrier Road, Bexhollow.
- **Ask 6 (sites dropped):** reproduces (14 sites, 105 stations).
  - Method: 50 distinct filing addresses; the 5 CORP rows duplicate facility addresses and are dropped; 14 of the 50 carry intent "none" in the 2026 directory.
  - Stations: the filing's own `licensed_stations` equals the register row covering 2026-01-01 for all 14.
  - Area: the directory area equals the register area for all 14.
  - Naive 19-row counting would double 5 sites.
- **Ask 4 (out of network):** all 48 cells reproduce only under the golden method.
  - Method: service-date half of 2026; a claim counted once (drop `line_no` 0, the header duplicate of line 1); area taken from the site address via the 2026 directory or register (not `member_residence_area`); denominator = out-of-network + in-network completed encounters at the area's in-scope sites.
  - Ammerly H1: 572 treatments, 9.7 per cent.

### Nearest-area ask (extra item 1)
Unrounded required figures and shortfalls (Durnsfield 189.625 vs 170; Bexhollow 334.075; Granleigh 334.082; Lowenbrook 228.281; Kettlebrook 520.326; Innsmere 433.060):

| Rounding of the requirement | Durnsfield | Bexhollow | Granleigh | Lowenbrook | Kettlebrook | Innsmere |
|---|---|---|---|---|---|---|
| Unrounded | 19.625 | 22.075 | 22.082 | 23.281 | 34.326 | 47.060 |
| Round to nearest | 20 | 22 | 22 | 23 | 34 | 47 |
| Round up (clause 4.4) | 20 | 23 | 23 | 24 | 35 | 48 |
| Round down | 19 | 22 | 22 | 23 | 34 | 47 |

Durnsfield is the single nearest area under all four, and the order of the other five is unchanged. The ask is in slots. A ratio reading (slots / required) would instead put Kettlebrook nearest (0.933 against Durnsfield 0.895), but nothing in the prompt invites it. I treat this ask as forced.

### Clause 4.4 and the ceiling (extra item 2)
- **What 4.4 files:** only conventions and WHAT is counted.
  - Reporting in whole slots.
  - Round the requirement once, up, at area level.
  - Encounters without a stop time or length are not delivered treatments.
  - A treatment belongs to the contract-year period of delivery, in or out of network.
  - 4.3 files "a week is one fifty-second of a contract year"; I treat that as a closed convention too.
- **How the ceiling is derived:** this is NOT filed anywhere. 4.2 says only "able to operate simultaneously". The HOW (peak of own treatments in progress, over the four-year record) lives in the write-up, not the shipped text.
- **Alternative ceiling readings, all giving the identical 274 and the same per-site integers:**
  - record maximum
  - yearly maximum (all four years equal per site)
  - monthly maximum (the minimum monthly maximum equals the overall maximum for every site)
  - 99th and 99.9th percentile over treating events
  - 2023-24 table alone, 2025-26 table alone
  - 2025-26 table on UTC instead of the local clock
  - closed against half-open interval ends

  The peak is a hard plateau reached every month. This is the strongest point in the golden's favour.
- **Capacity or ranking in shipped files:** none states a capacity figure or ranks areas against the standard. The filing's Area Summary gives licensed stations and 2025 treatments only.

### Residual forks (extra item 3)
No graded golden figure fails to reproduce. Residual forks:

| # | Fork | Touches | Alternative answer |
|---|---|---|---|
| 1 | Source of "deliverable positions": peak concurrency vs `attested_stations` vs register `licensed_stations` | MAIN CALL, CC1, all of asks 1 to 3 | Attested: 4,668 slots, 3 areas below, nearest Durnsfield. Licensed: 5,006 slots, 2 areas below. Golden: 3,886 slots, 6 areas below |
| 2 | `line_no` 0 header vs service line. Shipped `out_of_network_payments_reconciliation_2026.xlsx` totals `claim_lines` = `treatment_units` = 13,834 rows (Q1 3,401), i.e. both lines count; no file says line 0 is a duplicate header | Ask 4 only (all 48 cells) | Ammerly H1 667 and 11.1 per cent vs golden 572 and 9.7 per cent; Fallowbray H1 941 vs 806 |
| 3 | Area of an out-of-network site: 2026 filing (as at 2026-01-01) gives Thrushmead (ESRD-44046) as Crannock, Lowenbrook as Ammerly, Jarrowmead as Innsmere and Hesper Vale as Eastmoor Reach. Directory (all three cycles) and register give Fallowbray, Lowenbrook, Jarrowmead and Hesper Vale. Ask 6 says "current area" but Ask 4 says only "area of the site" | Ask 4 only | Cells for 4 to 8 areas change. Two sources against one; inference only |
| 4 | Ask 4 denominator: out-of-network plus in-network vs in-network only | Ask 4 only | Ammerly H1 10.7 per cent vs 9.7 per cent. "All the area's treatments" mostly closes it |

Closed by shipped text: the 52-week divisor, the single round-up, the exclusion of encounters without a stop, calendar-year 2026 and the service-date period. The 365/7-week divisor would change 4 areas' requirements and the network total (3,556), but 4.3 forbids it.

## Files/Hygiene
- **Verdict: PASS with one note.**
  - 13 files in 5 formats (csv x5, xlsx x3, pdf x2, json, sqlite db).
  - Large row-count files: treatment_encounters.db (639,110 rows) and the out-of-network claims file (13,834 rows).
  - Distractors: nemt_trips_2026.csv and licence_fee_schedule_2026.pdf.
  - Realistic noise: differing layouts across the encounter tables, reissued licence numbers, corporate-umbrella rows, a stale filing.
  - No authoring or "synthetic" leakage seen.
- **Temporal note:** `encounter_extract_transmittal.json` says the extract was pulled 2027-01-05. Clause 4.4 says it is taken after the ninety-day run-out. The figures are internally complete (the quarter counts match the tables), but the dates conflict. Minor, not exclusion-level.
- **Cross-batch fingerprint:** not run (no corpus access in this thread).

## Stump power (Gate F)
The intended trap is real analysis, not a stated rule: derive the ceiling of simultaneous treatments from two timestamp layouts, then compare slots with a rounded-up requirement. A strong model that takes the directory's attested stations files the wrong network (3 areas below, 4,668 slots) and will plausibly do so, because it is the only per-site count handed over as such. That fork is also why the task is not forced (see Why). If fork 1 is closed, stump power is real. It is unclear, though, whether failure would come from the analysis or from the reading of "able to operate".

## Stumping type (Gate G)
`mechanism: etl_conformance / method_selection`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. All numbers shipped are fine. The difficulty is choosing the method for the capacity ceiling on honest data, and on clean data the task would still stump. The one soft spot is that the method choice is currently not supported by a sentence in the shipped text.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`

- **Domain:** swapping "dialysis chairs" for "school seats" would not preserve the peak-concurrency capacity estimate, so the swap test passes.
- **Layer 1:** mixed local-clock and offset timestamps across two tables, reissued licence numbers, corporate-umbrella rows, a stale filing.
- **Layer 2:** the capacity ceiling from observed simultaneous operation, then adequacy against a demand-based requirement.
- **Easy route:** use the attested or licensed station count. That gives 3 or 2 areas below instead of 6.
- **Gate H caveat:** the step passes only if the method is licensed by the text, which is the weak point.

## Fix
- **Location:** input_files, specifically the Schedule 4 PDF, plus one line for the claim register.
- **Main call:**
  - Add a WHAT sentence to 4.2 (not the HOW): "Deliverable treatment positions are evidenced by the Site's own treatments recorded as running at the same time in the treatment encounter extract, not by station counts held in the directory or on the licence", or equivalent.
  - This keeps the method open, since the ceiling readings are interchangeable and the data separates them.
  - The golden does not move.
- **Ask 4:** state in the claim extract's notes, or in the prompt, that a claim is one treatment however many lines carry it. Alternatively remove the header lines from the shipped extract and fix the reconciliation workbook to match. Also say "the site's current area" in Ask 4, or drop the filing's conflicting area codes.
- **Re-judge:** the prior model runs are invalidated either way.
