# Determinism check, architecture 4 round 1 (2026-11-02): DETERMINISTIC, SEND_BACK; order kept; Gate H3 FAIL (rule_application); Gate F too easy; Gate G PASS (sole_data_defect yes)

Schedule 2 clauses 2.1 to 2.5 file the whole estimand and method, so a strong analyst who cleans the data and reads them gets Kewdale 102; every session-based method lands there; the difficulty is assembling files (Layer 1). Architecture 4 is spent and task304 re-roots as architecture 5 in another world. Isolated thread, Sonnet at medium effort, on target.zip d1946edf.

# Verdict: task304 round 1

ORDER: kept. derivation.md was written to disk (with every figure the prompt asks for) before graded_blocks.md was opened.

- **Verdict:** DETERMINISTIC (Gates A to E pass; the blocks reproduce, no SOLUTION_WRONG).
- **Disposition:** SEND_BACK. Gate H3 fails (decisive step is rule_application) and Gate F reads too easy on the main call. The fix rebuilds the decisive step, so a rerun is required. A smaller FIX_NOW item (the duplicate-vend fork) rides along.

## Why
The main call is forced and robust. Schedule 2 (clauses 2.1 to 2.5 of noise_enforceable_undertaking_schedule_2027.pdf) files the whole estimand and the whole method: who counts, what a shift is, the place-time energy average, the 85 dB(A) test, the post-enclosure recompute and the selection rule. Executed literally on the joined files it gives Kewdale, 102 brought below against 69 at Truganina, a 33-worker lead that no reasonable operationalization closes. Gate A to E: no failure. Governing taxonomy label for the Gate F/G/H findings: too_easy (main call) with a Gate H3 rule_application failure; no determinism failure label applies (none).

## Evidence (my values, all recomputed from target/ and all equal to the golden)
| Hub | workers | at/above 85 | brought below |
|---|---|---|---|
| Larapinta | 338 | 66 | 66 |
| Eastern Creek | 413 | 114 | 30 |
| Truganina | 295 | 69 | 69 |
| Wingfield | 257 | 39 | 39 |
| Kewdale | 262 | 102 | 102 |
| Beresfield | 193 | 49 | 49 |

Hub chosen: Kewdale. Source chain: ta_shift_records (WORKED rows) plus the two labour-hire sheets (Tasman daily rows, Meridian Mon-Fri grid, week ending Sunday) give shifts; wcs_operator_sessions_export (UTC) is converted to hub local time with DST (NSW, VIC, SA from 4 Oct 2026; QLD, WA none) and then every employee (43,552) and labour-hire (480) session matches its worker's rostered shift and site with zero mismatches; badge_register maps badges to payroll or labour-hire refs (34 lost-reissued badges, 96 contractor sessions excluded); levels from noise_survey_report_2026.pdf and predicted levels from induct_enclosure_design_report_rev2.pdf.

Earplug pairs, Jul / Aug / Sep (local time, EP-01 only, one pair per vend before the machine's RANGE CHANGE visit and five from it, hub by the machine's service-visit site with the move at the COMMISSION visit): Larapinta 2468/2276/2470; Eastern Creek 3170/2619/3060; Truganina 2192/1901/1935; Wingfield 1846/1813/1820; Kewdale 2008/1849/1785; Beresfield 1477/1225/1535. All 18 reproduce.

Confirmed STS (Schedule 3, first test as reference, confirming retest resets the reference, confirming retest in 2026, hub on that date via hr_site_transfers): Larapinta 9, Eastern Creek 9, Truganina 5, Wingfield 3, Kewdale 4, Beresfield 4 (34 workers). Reproduces. Independent cross-check: my replayed final reference equals the clients workbook "Reference test" for 357 of 357 clients, and clinic test_site gives the same hub split.

Forks tested (the main call and every worker figure are stable under all of them):
- Union versus sum of overlapping sessions (24 workers with about 6 minute overlaps), clip versus no clip at shift end (AUTO_TIMEOUT sessions end at shift start +3h55 or shift end +10 min), cap at 7 h or not, dropping AUTO_TIMEOUT sessions, scaling 7/8: identical counts at every hub. Exposure is bimodal; no worker sits within 0.1 dB of 85 before the enclosure; after it only 4 Eastern Creek workers sit between 84.5 and 85.5 and none flips.
- Dropping labour hire: only Beresfield moves (49 to 36); the call stays Kewdale.
- Retest window 28 to 60 days, same-ear versus either-ear, any later test as the retest: the 34 and the hub split do not move. Skipping the clause 3.3 reference reset gives 36 (the clause is explicit, so this is a misreading, not a fork).
- Wrong routes: HR position titles as place give Larapinta 66 as the top and Eastern Creek and Kewdale 0 moved (514 employees have induct sessions, 324 hold induct titles); ranking on "most workers at or above" gives Eastern Creek 114, of whom 84 stay above 85 after the enclosure; static asset-list sites, UTC months and a flat 5 pairs a vend all change the vending cells.

Surviving small forks (Gate C, supplementary asks only, no effect on the main call):
1. Four exact-duplicate vend rows (VM-3198 13 Jul and 29 Jul, VM-3047 5 Aug, VM-7891 4 Aug: same machine, second, slot, product). No file says to drop them. Counting every record (the golden, and the literal reading) gives Kewdale July 2008 and Eastern Creek August 2619; dropping them gives 2006 and 2617. Two graded cells move by 2 each.
2. Pairs per vend before the RANGE CHANGE visit (1) is inferred from the PR to PK5 unit change in the service visits and the fivefold fall in vend rate on that date; no file states it, and the product sheet says "pack of 5 pairs". The data forces it (loads in pairs match vend counts) but a solver must infer it.
3. Hub local time and the 4 Oct 2026 daylight-saving start are outside the package (general knowledge); the prompt asks for local time, so this is expected, but it is external.

## Files/Hygiene
PASS, with minor notes. 17 input files; formats pdf (3), xlsx (6), csv (8), json (1): four distinct formats; one file over 25,000 rows (wcs sessions 44,128; ta_shift_records 48,780; transactions 22,533). Distractors present and unused by the solution (boundary_noise_complaints_2026.csv, sort_volumes_daily_2026.csv, the design report prices). Notes: the three PDFs are short and tidy and read as written for the task (the undertaking schedule especially); the undertaking is issued 6 Nov 2026 but defines reference weeks ending 8 Nov 2026 (two days after its own date); the HR and shift extracts are very uniform (every employee a row on every weekday, 8.00 hours). None is exclusion-level; no authoring or benchmark text found.

## Stump power (Gate F)
Main call: too easy for a strong model. Every session-based method lands on Kewdale and the counts do not move under any treatment of overlaps, timeouts, clipping or caps, so even a sloppy-but-session-based solve reproduces 102 and 69. The two wrong routes (job titles gives Larapinta; most-at-or-above gives Eastern Creek) are readings the prompt's own wording ("take from at or above ... to below") and clause 2.1 already rule out. The difficulty that remains is assembly effort across seven files, not an analytical error, and it sits mostly in the asks (relocated vending machines, unit change, DST local months, reference reset, transfers). Most natural lever: make the deciding quantity an estimate the field has to judge (for example an exposure forecast with the survey's measurement uncertainty and a design-report prediction that has to be calibrated against an installed enclosure's measured performance) rather than a filed procedure, without filing the how.

## Stumping type (Gate G)
mechanism: etl_conformance, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: yes (clean-data test: on single-timezone, single-format, one-badge data the exposure arithmetic is a direct calculation and would not stump; the difficulty is integration mess, which is Layer 1 and not a planted defect).
Not banned_stumping_type: no reported figure is overturned; the stale asset list, HR titles and the clients workbook reference are shipped but not presented as conclusions.

## Three rules (Gate H)
domain: pass, layers: pass (Layer 1 named; Layer 2 is thin, see below), decisive_step: rule_application
- H1 pass: place-time energy-averaged LAeq,8h against the 85 dB(A) standard and the effect of an engineering control is occupational-hygiene work; swapping in another field's nouns breaks it.
- H2: Layer 1 = UTC logs to local time with DST, two labour-hire timesheet formats, reissued and contractor badges, machine relocations and a pairs-to-packs unit change, a transfers list. Layer 2 = the exposure assessment, but Schedule 2 files all of it.
- H3 FAILS: the easy route that goes wrong (titles for place, or ranking on most-at-or-above) is a misreading of stated rules, not an analysis a careful analyst would choose. A strong analyst who cleans the data and reads clauses 2.1 to 2.5 correctly gets Kewdale 102 with no analytical choice left. Quote: "2.1 ... at the hub where it brings the most workers from at or above the exposure standard to below it", "2.3 ... the A-weighted sound energy of the places they worked ... normalised to eight hours and energy-averaged over those shifts". Classified rule_application (the answer comes from executing the stated procedure over many files).
- Prescription: rebuild the decisive step so the deciding quantity is judged, not filed (an exposure or enclosure-performance estimate whose method the data separates, for example by calibration against a pilot enclosure or by an uncertainty-aware comparison where the nominal ranking and the defensible ranking differ), leaving the estimand filed and the how open.

## Fix
- Main design: prompt/input_files/solution, i.e. rebuild around a decisive step that is analytical (see Stump power and Three rules). Full rerun required.
- Smaller, independent of the rebuild: state in the hearing_program ask (prompt) or a data note that duplicated vend records are or are not counted, so the two duplicate-sensitive cells (Kewdale July, Eastern Creek August) are forced. Also have the design carry an explicit statement, in a shipped service document, of the pairs per vend before the range change.
