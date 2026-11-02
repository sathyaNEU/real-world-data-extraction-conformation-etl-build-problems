# task186 determinism check (architecture 2)

Three isolated judge passes, each a Sonnet thread at medium effort that saw only a fresh unzip of target.zip, the prompt and the judge's system prompt, and opened the graded blocks only after its own derivation was on disk.

| Round | Pack | Verdict | Disposition | Action |
|---|---|---|---|---|
| 1 | b4586dea | DETERMINISTIC, SOLUTION_WRONG in wording only (order kept; F high; G PASS; H PASS) | FIX_NOW | write-up wording corrected (no unrecorded feedback, no 'retrofit', the first-showing definition stated with its evidence); target/ unchanged |
| 2 | b4586dea | NOT_DETERMINISTIC on the main recommendation (Gates C and E; G PASS; H PASS conditionally) | SEND_BACK as labelled; a C/E repair by the gate table | SCS-04 s3 files detection performance on prohibited items the officer has not been shown before (object against image, the history start and any recall explanation left unstated); start-up test images filed as not passenger bags; the leavers' lapse dates filed; the monthly margins widened |
| 3 | c1a98fb1 | DETERMINISTIC (order kept; stump credible; G PASS; H PASS) | APPROVE | none (optional leave-overlay line not taken) |

---

# Determinism check, round 1 (2026-11-01): DETERMINISTIC (SOLUTION_WRONG in wording only), FIX_NOW; order kept; Gate F high; Gate G PASS; Gate H PASS

Isolated thread, Sonnet at medium effort, on target.zip b4586dea.

# Verdict, task186 round 1

- **Order kept:** yes. derivation.md was written to disk before graded_blocks.md was opened.
- **Verdict:** DETERMINISTIC (with SOLUTION_WRONG wording defects, see Fix). Cross-batch check: not possible from this sandbox (only the bundle is readable); no near-duplicate observed inside the bundle.
- **Disposition:** FIX_NOW. Repair is wording only in the solution blocks (no file or prompt change, no model rerun).

## Why
The main call is forced by the shipped data once the estimand in SCS-04 s3 (probability of detecting a prohibited item in a passenger's cabin bag) is taken seriously: the TIP hit rate over all projections is dominated by repeat showings (99.5 per cent hit) while objects new to the officer are hit 88.5 per cent, so the pooled rate does not estimate the defined probability. On first showings (object level, history from 1 Jul 2025) ten officers sit at 55.9 to 74.2 per cent and every other officer at 83.5 per cent or above, so the recommendation (10 off, 81 keep) is a clean, wide-gap result. Residual risk (Gate C, moderate, not failing): the novelty restriction is not stated in any filed sentence, so a literal pooled reading gives 3 officers; the shipped data separate the candidates (see Evidence), which is why I do not fail it. Taxonomy for the residual: underspecified_objective (low weight).

## Evidence (all recomputed from target/)
| Item | Mine | Golden | Reproduced |
|---|---|---|---|
| Officers holding endorsement 30 Nov | 91 (93 on register, Hale and Kemp Lapsed and left) | 91 | yes |
| First vs repeat showing hit rate (in-year, deduped) | 0.8849 / 0.9950 | 88.5 / 99.5 | yes |
| Ten off (first-showing rate) | 19116 .559, 46133 .573, 42948 .594, 17045 .605, 29369 .636, 46312 .647, 16884 .656, 19645 .696, 43647 .736, 46282 .742 | same ten | yes |
| Next officer | SC40945 .835 | above 83 | yes |
| Pooled rate of the ten: 7 clear 80 per cent, 6 full-time | yes | 7 / 6 | yes |
| Monthly shortfalls Dec to Nov | 19,17,20,14,16,17,16,17,15,15,12,16 | identical | yes |
| Bags per lane-quarter | see below | differs from my first pass only by pre-roster counts | yes after the roster rule |

Forks tested on the main call (who is below 80):
- Pooled TIP hit rate, in-year (easy route): SC46133, SC42948, SC17045 only (3 off). Same under UTC window, dedupe, DOM-login-only, category or view balancing. Using the whole file (pre-year events) adds SC16884 (4 off).
- First showing by image rather than object: four off (46133, 42948, 17045, 16884). Data say object is right: seen-other-orientation hit rate is 99.3 per cent vs 88.5 new object, 99.6 same image.
- Novelty reset at 1 Dec 2025 (in-year history only): four off (SC19116 .8006 passes). Data say history from 1 Jul 2025 is right: objects first shown in-year but seen before 1 Dec are hit 99.2 per cent.
- Shrinkage or significance test instead of point estimate: a different, unfiled estimand; not credited.
So the golden is the only reading consistent with the data's own structure; the competing readings are the weaker-analysis routes. Gap 74.2 to 83.5 is wide and not noise-sensitive.

Currency (supp 3): the roster lists 1,084 shifts on 620 officer-days of Personal leave (hr_leave joined on payroll_no) and zero TIP events fall in any of them. Dropping those shifts from time and headcount (golden) gives the golden row. Roster as-is gives 17,16,20,11,16,15,15,19,15,14,12,13; dropping time but keeping headcount gives 20,18,22,14,21,20,19,19,17,17,14,21. SCS-04 s7 says the roster "records the officers who work", which on its face supports the as-is reading; "time they work" plus zero TIP events and the shipped leave file force the golden. Low-moderate fork, evidence-resolved.

Throughput (supp 4): lane-unit history is not filed (register shows end state). Derived from bags vs roster and TIP volume (events about 0.0125 of bags): D2 = KX6-0413 to 2 Mar then KX6-0590 from 5 Mar (D2 dark 3 to 4 Mar); D5 = KX6-0416 to 19 Apr then KX6-0413; seven two-day spare stints cover the one lane whose unit is absent (D1 9 Jun, D3 23 Jun, D4 7 Jul, I1 21 Jul, I2 4 Aug, D2 18 Aug, D5 1 Sep). From each lane's stint onward the unit also logs 28,000 bags in hours before the first officer starts; including them gives Q3 D1 213 / Q4 217 etc. Golden excludes them and gives 219/209/209/213 D1, 212/199/204/204 D2, 174/168/167/167 D3, 137/132/131/133 D4, 74/71/71/71 D5, 144/136/135/140 I1, 120/113/114/117 I2; my in-roster recomputation matches every cell. The exclusion is not stated anywhere in the files, but it is forced by the data: those pre-roster hours carry 0 TIP events against about 350 expected at the standard's "every CT lane, at random" projection, and s7 distinguishes "what it images" from passenger bags. Fork exists on 13 of 28 cells if a solver counts them; resolved by cross-source evidence, so not failing.

## Files/Hygiene
PASS. 12 files, 4 formats (pdf, csv x7, xlsx x2, json), tip events 74,704 rows plus 38,103-row hourly file. Realistic mess present and not planted: two logins per officer, INTL image_no with leading zeros stripped, UTC vs Sydney (DST), replayed rows (29 exact duplicate pairs on 16 Feb UTC), unit swaps, leave vs roster. No README or authoring text in the pack; dates coherent (settings export 1 Dec 2026 after the year). Distractors present (checkpoint_queue_times_daily, ct_unit_register as end-state only, tip_projection_settings). Nothing exclusion-level. (PDF text extraction shows word-joins from the standard's layout only.)

## Stump power
High. The easy route (pooled TIP hit rate, correctly cleaned) keeps 7 of the 10 and removes only 3, and nothing in the prompt or standard points at exposure history, so a strong model that cleaned and read every rule correctly still files the wrong list. Only analysis of the exposure structure decides it. Asks also carry silent devices (leave-day shifts, retired unit moves, pre-roster counts).

## Stumping type
`mechanism: statistical_rigor` (estimand validity under repeated exposure), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. No shipped stakeholder figure or scorecard is reversed; the hit rate is arithmetically right and the data are honest, the work is choosing the estimand the standard defines (clean data still stump). Passes Gate G.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`. H1: swap test fails to hold (TIP validity and finite-library memorisation are the field's own measurement problem for officer competency). H2 Layer 1: dual logins, stripped zeros, UTC, replay, unit moves; Layer 2: novelty-adjusted detection probability. H3: easy route = pooled TIP hit rate over the year giving 3 officers (SC46133, SC42948, SC17045) against the correct 10; passes the test.

## Fix
Where: solution only.
1. FINAL_RECOMMENDATION and Step 3: "shown and told were threats" asserts feedback no file records; reword to "already shown to the officer".
2. Step 6: "retrofit" and "retrofitted" appear in no shipped file; restate as "units of lanes whose spare stint has passed log bags in hours before any officer is rostered, which carry no TIP projections, so only hours with an officer rostered are counted".
3. Critical component 2 should state the object-level, since-1-July-2025 definition, and Step 5 should cite the zero TIP events in leave-day shifts as the reason to drop them.
4. Optional hardening of the pooled-rate pitfall is unnecessary; do not add a prompt sentence on novelty (it would file the HOW).


---

# Determinism check, round 2 (2026-11-01): NOT_DETERMINISTIC on the main recommendation (Gates C and E), SEND_BACK as labelled; order kept; Gate F good; Gate G PASS; Gate H PASS conditionally (H3 holds if the novel-item population is forced)

Read against the gate table the failing gates are C and E on the main call with G and H passing, so it is repaired by filing the population at the WHAT level (detection performance on threat items the officer has not been shown before), with the two ask notes closed, and judged again. Isolated thread, Sonnet at medium effort, on target.zip b4586dea.

# Verdict, task186 round 2

Order kept: derivation.md was written to disk before graded_blocks.md was opened. Cross-batch check: no other task material was readable, so no near-duplicate check was possible (stated, not assumed clean).

- **Verdict:** NOT_DETERMINISTIC
- **Disposition:** SEND_BACK. The main call's population (first showings of each threat object) is not filed anywhere and the literal reading gives a different list. Fixing this changes what solvers see, so a rerun is required.
- **Why:** The golden (10 officers off) holds only under an unstated population: each officer's first showing of each library object, with history counted from the 1 July 2025 start of the TIP export. SCS-04 s3 defines detection performance only as "the probability that the officer detects a prohibited item carried in a passenger's cabin bag", and s7 says the system "records each one it shows and whether the officer ... marked it". Executed word for word that is HIT/(HIT+MISS) over the year: 3 officers off (Hutchinson, Vincent, Le), not 10. Gates C and E fail on the main recommendation. Taxonomy: underspecified_objective. No shipped sentence in any file forces the first-showing population, the object (not image, not orientation) as the unit of "new", or history running back before the screening year. The data do separate the candidates, but the brief says a golden that holds only under an unstated population is an open fork.

## Evidence (recomputed from the bundle; everything in the golden's blocks reproduced except the open forks)
| Item | My value | Golden | Reproduced |
|---|---|---|---|
| Endorsed on 30 Nov (register Current) | 91 | 91 | yes |
| Pooled in-year hit rate, officers under 80 | 3: SC46133 76.2, SC42948 76.3, SC17045 77.6 (Meyer 81.4) | not the call | literal reading, see fork 1 |
| First showing of object, history from 1 Jul 2025, in-year, both logins merged, deduped, image_no zero-padded | 10 under 80: Waters 55.9, Hutchinson 57.3, Vincent 59.4, Le 60.5, Ferguson 63.6, Zavala 64.7, Meyer 65.6, Austin 69.6, Juarez 73.6, Lucas 74.2; next Sullivan 83.5 | same 10, "below 75 / above 83" | yes |
| In-year first 88.5, repeat 99.5, new orientation of a seen object 99.3, seen before 1 Dec 99.6 | same | 88.5 / 99.5 / 99.3 / over 99 | yes |
| Given names and 81 keepers | match register | match | yes |
| 7 of the 10 clear 80 pooled, 6 full-time | 7 and 6 | 7 and 6 | yes |
| Monthly short count Dec 2025 to Nov 2026 (exact-fraction time slices, personal-leave days removed, leavers counted for months before leaving) | 19,17,20,14,16,17,16,17,15,15,12,16 | identical | yes |
| Bags per lane per quarter, units placed by date, roster-open Sydney hours only | D1 219/209/209/213, D2 212/199/204/204, D3 174/168/167/167, D4 137/132/131/133, D5 74/71/71/71, I1 144/136/135/140, I2 120/113/114/117 | identical | yes (every cell) |

Open forks, with the answer each gives:
1. **Main call, population (Gates C and E, governing).** Pooled hit rate: 3 off. First showing by object, history from Jul 2025: 10 off (golden). First showing by image: 4 off (adds Meyer). First showing by object with the count restarted on 1 Dec: 4 off. Point estimate vs significance test: the text says "below 80 per cent", so point estimate (Lucas and Juarez intervals reach 80), not an extra fork. The data are strong evidence for the golden's estimand (hit rate 88.9 on first sight of an object, 98.8 on second, about 100 after, no decay over 400 days, image-level repeat adds nothing beyond object-level), but that is data discovery, not a filed definition.
2. **Ask 4, bags by quarter (Gate C, Q3 and Q4 cells, 6 of 7 lanes).** From each lane's first spare-cover day (D1 9 Jun, D3 23 Jun, D4 7 Jul, I1 21 Jul, I2 4 Aug, D2 18 Aug, D5 1 Sep) its unit records about 40 images in the hour before the first rostered start (931 hours, 0 TIP projections although about 485 would be expected at 0.013 per bag). Summing every unit hour gives D1 213/217, D3 170/171, D5 71/75, I1 137/144, I2 115/121 in Q3/Q4 against the golden 209/213, 167/167, 71/71, 135/140, 114/117. Excluding them is well supported (no officer rostered, no projections) but no file says unit counts include non-passenger images, so a literal reader summing "what it images" files a different number. Standard s3 defines passenger bags, s7 only says each unit counts "what it images".
3. **Ask 3, monthly shortfalls (low).** Counting only the 91 year-end endorsed officers gives Dec 18 and Mar 13 (leavers Hale and Kemp dropped) against golden 19 and 14. s5 ("holds an endorsement for the whole of a calendar month") licenses the golden, but the lapse date is not filed (only the left date). Keeping the personal-leave roster rows as worked gives 17,16,20,11,16,15,15,19,15,14,12,13; "time they work" plus the HR leave file and zero projections on those days force removal. Margins are thin but exact (SC35820 April 20.004 h, SC36393 November 19.979 h; no exact 20.000), so the count needs exact time slices, not shift averages.

Passes: the unit-to-lane reconstruction (0413 on D2 until 2 Mar 2026 then on D5 from 20 Apr, 0416 on D5 until 19 Apr then spare, 0590 on D2 from 5 Mar, D2 uncounted 3 and 4 Mar) is forced by matching unit active hours to lane roster hours, and the register's "current location" mapping fails it. Login-to-staff mapping, UTC to Sydney and the 29 exact duplicate rows are closed by the data (every event falls inside the officer's own rostered interval on that lane, none on a leave day). The recertification list and chart are fully determined once the population is fixed.

## Files/Hygiene: PASS
12 files, 4 formats (csv x8, xlsx x2, pdf, json), largest 74,675 TIP rows plus a 38,103-row hourly file, distractors present (checkpoint_queue_times, xray_cbt_sessions). No authoring or benchmark language, no README. Library export dates (1 Dec 2026) fall after the 30 Nov window but carry no decisive fact. The standard is one terse page and reads like a controlled document. Intentional Layer 1 mess is realistic (zero-dropped INTL image numbers, UTC counts, two logins per officer, relocated units, leave rows against the roster). No exclusion-level finding.

## Stump power (Gate F)
Adequate to strong. The memorisation structure is nowhere flagged, so a solver who computes the plain hit rate files 3 officers (a different list from the golden's 10, sharing only 3), and one who keys on image rather than object files 4. The two-failure shapes are both analytical. The trap is not pre-disarmed. Risk is not too-easy but the determinism gap above.

## Stumping type (Gate G)
`mechanism: statistical_rigor` (measurement validity of a repeated-exposure instrument, estimand and unit of analysis), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. No reported figure is shipped and wrong; the data are honest and the difficulty is in the estimand. Passes Gate G.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Domain: a screening standards lead judging TIP-based detection performance and its measurement validity is the field's own analysis (swap "hospital" or "megawatt-hours" in and the TIP library, recall and CT lanes no longer read). Layer 1: unit relocations, UTC against Sydney, two logins per officer, dropped zero padding, duplicate rows, roster against HR leave. Layer 2: detection rate on items new to the officer. Easy route: the pooled hit rate over every projection, which gives 3 off and clears 7 officers who fail on novel items (6 of them full-time, shown the library most). H3 passes only if the novel-item population is forced; see the fix tension.

## Fix
Location: input_files (or the standard's s3 wording). File the WHAT so the golden is the literal execution: e.g. SCS-04 s3 detection performance "on items the officer has not been shown before", with the catalogue's objects (not images or orientations) as the items and the TIP export from 1 July 2025 as the shown-before history, and leave the HOW to the solver. Be aware this moves the decisive step toward rule application unless the wording stays at the population level (do not state that repeats are recalled, that object is the unit, or that history starts July 2025; the catalogue and export already carry those). If the author prefers the estimand unfiled, the call is not determinate and the build must be re-rooted. Also file in the standard or a unit note what the hourly unit count excludes (images with no lane open), so ask 4's Q3 and Q4 cells have one answer. Optionally state that the monthly return covers officers endorsed in that month, including those who later left.


---

# Determinism check, round 3 (2026-11-02): DETERMINISTIC, APPROVE; order kept; stump power credible; Gate G PASS; Gate H PASS

The judge after round 2's main-call fork was closed by filing the novel-item population in SCS-04 s3, on target.zip c1a98fb1. Its optional leave-overlay hardening was not taken (s3's 'the time they work on the lane' closes it), so the approved pack ships unchanged. Isolated thread, Sonnet at medium effort.

# Verdict, task186 r3

**Order kept:** yes. derivation.md was written to disk before graded_blocks.md was opened.

- **Verdict:** DETERMINISTIC (all committed answers reproduced; no SOLUTION_WRONG).
- **Disposition:** APPROVE. No rework is needed. The optional notes below are low-risk, and none needs a rerun.
- **Why:** Executed literally, SCS-04 s3 ("a prohibited item they have not been shown before") and s4 (below 80 per cent, 91 endorsed on 30 Nov) give exactly the golden's 10 officers. The data separate the candidate readings. First showings of an object are detected 88.5 per cent, and repeat orientations or earlier-year objects about 99.3 to 99.6 per cent. The nearest officer above the line is 0.835, against 0.742 for the highest officer below it, so there is a clean gap. Supplementary answers 3 (monthly shortfall) and 4 (bags per lane-quarter) also reproduce, and each rests on a rule the files support: standard s3 "time they work", the TIP silence on leave days, and the standard's test-image exclusion.

## Evidence (every figure recomputed from target/)
| Item | Mine | Golden | File / field |
|---|---|---|---|
| Endorsed on 30 Nov | 91 (2 Lapsed excluded) | 91 | register `endorsement_30_nov_2026` |
| Off X-ray (object-level first showing, full history from 2025-07-01, deduped, zero-padded, staff-level) | SC19116 .559, SC46133 .573, SC42948 .594, SC17045 .605, SC29369 .636, SC46312 .647, SC16884 .656, SC19645 .696, SC43647 .736, SC46282 .742 | same 10 | tip_events + logins + catalogue Images |
| Next lowest officer | SC40945 .835 | "above 83" | |
| First / repeat / new-orientation-old-object | 88.45 / 99.49 / 99.32 per cent | 88.5 / 99.5 / 99.3 | |
| Object shown before Dec, shown again | 99.57 per cent (n 25,446) | "over 99" | |
| Hit rate over all projections: 3 under 80 (SC46133, SC42948, SC17045); 7 of the 10 clear 80, 6 of them full-time | reproduced | reproduced | |
| First IMAGE (4 flagged) / first object but in-year only (4 flagged) | reproduced | golden says the "4 casual" | |
| Monthly shortfall Dec to Nov | 19,17,20,14,17,18,17,17,15,15,12,16 | identical | roster, leave, register |
| Bags per lane-quarter (thousands), test hours removed | D1 219/209/209/213, D2 212/199/204/204, D3 174/168/167/167, D4 137/132/131/133, D5 74/71/71/71, I1 144/136/135/140, I2 120/113/114/117 | identical, all 28 cells | hourly UTC file, register, roster |

Robustness: the 10-officer list is unchanged by dedupe on or off, UTC against Sydney dates, per-login against per-staff history, and unpadded image numbers (6,769 INTL rows match once padded).

Forks examined (each closed by text or data, none open on the main call):
1. **Item = object or image, and the history window.** Image-level gives 4 officers off, in-year-only gives 4, and the literal reading (object-level, full history) gives 10. The standard says "item" and "not shown before", and the catalogue's Objects sheet carries three views per object. The data close it, because a new orientation of a known object is detected 99.3 per cent of the time, the same as a repeat. The text never says item = object, so this is closed by data and wording only. It is the one reading a careless solver can miss, and it is the intended analytical step.
2. **Leave overlay.** 1,084 rostered shifts fall on Personal-leave days, and no TIP event ever falls on a leave day, while all 54,240 in-year events fall inside rostered non-leave shifts. If the roster is read literally and leave is ignored, the shortfall counts are 17,16,20,11,16,15,15,19,15,14,12,14, which differ in 10 of 12 months, and 2 to 4 officers per month sit within 0.02 to 0.09 h of the 20 h line. With leave removed (and removed from the lane-mate denominators), every officer-month is at least 0.31 h from the line. Neither the prompt nor SCS-04 names the HR file. The only text that closes it is s3 "the time they work on the lane" (a person on sick leave does not work). I judge it forced, but this is the softest link, and it is a supplementary answer only.
3. **Test images.** The standard does not file a count or a rule. The data show a uniform 34 to 46 bags in the hour wholly before the lane's first rostered start, from June 2026 only (931 hours, about 37,100 bags). A roster-based rule and a value-based rule (first hour of the unit-day, 34 to 46) differ by 3 hours (about 130 bags), which move no rounded cell except none of the 28 (checked).
4. **Unit-to-lane history.** The register shows current locations only. The history is recoverable from day-level matching of unit hours to roster open hours (KX6-0413 on D2 until 2 Mar 2026 and on D5 from 20 Apr; KX6-0416 on D5 until 19 Apr, then spare cover on 16 outage days; KX6-0590 on D2 from 5 Mar). There are no ties at day level.
5. **Rounding edges.** D5 Mar to May is 70,507 (7 bags above the 70.5k boundary) and D2 Sep to Nov is 204,474 (26 below 204.5k). Both are exact under the filed rules, but a solver one hour off on either would round the other way.
6. **Point estimate against significance.** "Below 80 per cent" is read as the point estimate. SC43647 (109 of 148, one-sided binomial p 0.037) and SC46282 (95 of 128, p 0.067) would not both pass a significance test, but the standard asks for no test.

## Files/Hygiene: PASS
12 files in 4 formats (8 csv, 2 xlsx, 1 pdf, 1 json). Large files: tip_events 74,705 rows, hourly bag counts 38,104, roster 31,617. Distractors: checkpoint_queue_times, xray_cbt_sessions, tip_projection_settings.json (identical 0.013 on every lane). Dates are coherent (settings JSON and catalogue exported 1 Dec 2026, after the 30 Nov snapshot, consistent with a year-end return). No authoring or provenance leakage was seen in the files I read, and I did not see metadata.json. Nothing here is exclusion-level.

## Stump power
A strong model that reads "not shown before" will mostly attempt a first-showing filter. It is likely to key it on image_no (4 officers off, missing 6 full-time officers) or to use only the screening year (also 4), or to take the plain hit rate (3 off). Only an object-level, full-history first-exposure analysis gets 10. The asks add layers (leave overlay, INTL zero-padding, start-up test images, unit moves). Several of these are traps a careful solver can clear, so the call carries the stump. Stump power is credible.

## Stumping type
`mechanism: statistical_rigor` (first-exposure novelty and the unit of analysis; practice effect), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. No shipped artifact reports a wrong detection rate that must be rejected. The task would still stump on clean data, since the object-level first-exposure estimand remains. Gate G passes.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`
- **Domain:** Threat Image Projection novelty-adjusted detection performance and practice-effect inflation is a core quantity of aviation-security training analytics. Swapping in other nouns changes the task, because the definition of "not shown before" does the work.
- **Layer 1:** duplicate re-export, INTL image numbers without leading zeros, two logins per person, UTC against Sydney, roster against leave, unit swaps, start-up test images. None of these is planted and none carries the stump.
- **Layer 2:** the estimand is each officer's first exposure to a threat object, with exposure history carried from before the year, scored against 80 per cent.
- **Easy route:** the plain hit rate over all projections puts 3 casual officers off. Keying novelty on image_no, or counting only from 1 Dec, puts 4 off. Both let 6 under-performing full-time officers keep X-ray duty.
- **Borderline note:** the definition is filed in the standard, so a reader could call the decisive step rule application. I hold it analytical because choosing the unit of exposure (object, not image) and the history window is an estimand choice that the data (practice-effect rates) settle, not a field or code reading.

## Fix: none
Optional, no rerun needed: add one neutral line to the standard or the roster export saying the roster is the planned deployment (this closes the leave fork in text), and keep an eye on the D5 Mar to May rounding edge (70,507).

