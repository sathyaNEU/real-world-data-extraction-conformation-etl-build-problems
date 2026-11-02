# task134 determinism check (architecture 4)

3 isolated judge pass(es), each a Sonnet thread at medium effort that saw only a fresh unzip of target.zip, the prompt and the judge's system prompt, and opened the graded blocks only after its own derivation was on disk.

| Round | Pack | Verdict | Disposition | Action |
|---|---|---|---|---|
| 1 | 456d4b72 | DETERMINISTIC (order kept; F moderate; G PASS, forecasting / analytical_non_defect; H PASS) | FIX_NOW (small) | the 2026 dry-solids area summary regenerated under licence 5.5 (duplicates averaged with their primary); licence 5.3 and 5.4 name UK civil time; critical component 1 stated at a precision every membership shares; python-docx template parts scrubbed and zip dates set to each document's own date |
| 2 | 890c87d8 | DETERMINISTIC (order kept; F strong; G PASS; H PASS) | FIX_NOW (optional) | each part's coefficient and natural bed tuned so every part lands in its bin under 18 model forms (anchored, pooled absolute and increment, with intercept, power law, berth routes), asserted per form; the dry-solids revision file carries its own provenance columns |
| 3 | dc8dc926 | DETERMINISTIC (order kept; F moderate to high; G PASS; H PASS) | APPROVE | none |

The architecture 3 record is in determinism_check_report_arch3.md.

---

# Determinism check, round 1 (2026-11-02): DETERMINISTIC (order kept; F moderate; G PASS, forecasting / analytical_non_defect; H PASS), FIX_NOW (small)

Isolated thread, Sonnet at medium effort, on target.zip 456d4b72.

# Verdict, task134 (judge run r1)

ORDER KEPT: yes. derivation.md was written to disk before graded_blocks.md was opened. My independent values then matched the golden on every graded figure (main call, six parts, eight tonnage cells, twenty metal means).

- **Verdict:** DETERMINISTIC.
- **Disposition:** FIX_NOW (small, no rerun needed on the main call): (1) close the dry-solids-fraction fork F-DS below (either regenerate the 2026 Area summary so it follows licence 5.5, or accept the residual); (2) scrub python-docx template remnants from the planning-basis docx. The main call, the stump and the ladder stay byte-identical.
- **Why:** The 1,750,000 m3 total and the six part volumes are forced by the shipped files: the 10-licence-year certificate means (1,291,401 m3 a year, re-aggregated from financial-year sheets, A/B codes read through "Area codes", the /R1 certificate replacing the original) are raised by (14.3 - natural bed)/(12.3 - natural bed) per reach, the law the data show in all five reaches (siltation per m2 / trench depth below the plateau = 0.1095-0.118 a year, log-log exponent 0.99), in the unmaintained NQ2 infill curve and in CT5. Every model form I tried that stays anchored to the certificates lands 1,739-1,750k (all round to 1,750,000) and the parts round identically except the unanchored absolute model (Outer Channel 360,000). Residual softness sits only in supplementary 3 (Q3/Q4 tonnage cells, fork F-DS, Gate C competing_defensible_answer, low).

## Evidence (recomputed from the bundle; all reproduced)
| Item | Mine | Golden | File / field |
|---|---|---|---|
| 10-yr mean, all maintained areas | 1,291,401 m3/yr | 1,291,401 | certificates xlsx, Oct-Sep re-aggregation, 2016-17..2025-26, R1 in place of original |
| Natural bed OC/FR/MR/IR/TB | 8.09-8.10 / 8.24-8.27 / 6.41-6.44 / 5.34 / 4.75 | 8.09/8.27/6.44/5.34/4.75 | seaward and Holmwood surveys (depth BCD = -z - 2.90); the golden values reproduce with segment-rectangle membership, the nearest-segment cut gives FR 8.24, MR 6.41 (0.03 m, immaterial) |
| Year-1 volumes | OC 381,962; FR 296,305; MR 396,551; IR 276,987; TB 357,032; berths 40,616; total 1,749,452 (golden ambient: 1,750,506) | 380k/300k/400k/280k/360k/40k, total 1,750,000 | same |
| Wet t Q1-Q4, Fend Spit | 202,741 / 93,966 / 217,075 / 213,741 | 203/94/217/214 kt | load log, licence corners, local dates, FE revision, Area summary |
| Wet t Q1-Q4, Wenning Deep | 298,739 / 391,739 / 121,220 / 123,990 | 299/392/121/124 kt | same |
| Metals (20 figures) | identical to golden to 2 dp | | Aldern results, field log positions, QA pairing, Hg ug/kg to mg/kg |

Checks that closed forks: Maasbank formula V*2.65*(rho-1.025)/1.625 reproduces certificate dry solids for every Maasbank month within 1 t; with revision=False the log dry solids reproduce the certificate dry solids exactly for 287 of 287 area-months by loading month; trip_ref -> loads: 146 revision trips match loads by UTC loading date and order of day, 0.9363 ratio on every load (±0.0002), so the join is unique; every dump position is inside exactly one licence box; no Fend Spit placement 1 Dec-Feb.

Competing answers tested:
- 1,291k (no depth effect) and 1,495k (14.3/12.3): rejected, the data do not follow depth itself, they follow depth below the plateau.
- Linear-with-intercept 1,739k, power-law 1,743k, pooled absolute 1,744k, pooled increment 1,747k: all 1,750,000. Financial-year averaging 1,746k: 1,750,000. Last-5-year mean 1,708k is not licensed by the doc ("as the licence years 2016-17 to 2025-26 averaged them").
- Increment from the NQ2-only decay (tau 9.4 y) 1,721k (1,700,000) and absolute tau 9.4 1,645k: the only valid-looking route that leaves 1,750,000; it discards the five-reach calibration and does not reproduce the reaches' own measured volumes at 12.3 m, and tau 9.4 +/- 0.6 is consistent with the pooled 8.8. Treated as inferior estimate, not a surviving alternative. Thin spots: FR 296.3k, MR 396.5k, TB 357.0k are 6-7k from their rounding edges; total 24k from 1,725k.

## Findings (each with the gate it fails)
1. **F-DS, Gate C (competing_defensible_answer), supplementary 3, low-moderate.** Licence 5.4 divides by "the fraction reported for the area"; the workbook Area summary 2026 (OC .432, FR .426, MR .376, IR .331, TB .326) equals the actual-area means with the QA samples counted as extra samples, not what 5.5 gives from the Aldern results (duplicates averaged): OC .4363, FR .4266, MR .3764, IR .3355, TB .3265. The golden uses the summary (the literal 5.4 reading, and the only option for the 2025 campaign). A reader who recomputes by 5.5 shifts all four Q3 and Q4 cells by 1,000 t (216/120/213/123). Seven of eight tonnage cells are only 240-490 t from their rounding edge, so any such shift flips them. Fix location: input_files (regenerate the 2026 Area summary to follow 5.5, then Q3/Q4 goldens become 216/120/213/123) or accept as residual.
2. **Gate B (external dependency, minor), supplementary 3.** "Local date" (5.3, 5.4) needs UK civil time with the BST rule; no file states the zone, the load log says UTC and the licence says local. Moves seven loads across month and quarter edges (e.g. DDL-2425-00617/618 into Q1; DDL-2526-00570 out of the year; FS Q1 -5.9 kt if read as UTC). Low risk (a UK harbour). Fix: solution/metadata note.
3. **Gate E (minor), supplementary 3.** FE_dry_solids_revision_20260330.csv carries no statement that it supersedes the load log; it is applied by joining trip_ref on loading date and daily order. Recoverable without doubt (constant ratio), effect is Q2 +6.0 / +23.8 kt if ignored. Accepted, no change required.
4. **Gate E (minor), supplementary 4.** The QA stations are not labelled as field duplicates anywhere; they are identified by position (2.6-3.7 m from a primary) and time. Without them the area means move by up to 0.4 mg/kg. Accepted, evident from the field log.
5. **Gate A (solution wording only, not SOLUTION_WRONG).** Critical component 1 (FR 8.27, MR 6.44) reproduces only with segment-rectangle membership; the nearest-segment cut gives 8.24 and 6.41; MR plateau is 6.33 north of the centreline against 6.55 south. Effect on the answer under 2 kt. State the membership rule in the solution block.
6. **Hygiene, minor (FIX_NOW).** The planning-basis docx carries python-docx default template parts (stylesWithEffects.xml, thumbnail.jpeg, zip dates 2027-01-18). Scrub.

## Files/Hygiene
PASS with the scrub above. 13 files; formats csv (8), xlsx (2), pdf (2), docx (1); rows over 25,000 in the tide gauge (96k), Holmwood (47.7k) and Seaward (34.7k). Distractors: tide gauge, Haddon Weir flows, vessel arrivals (unused by any asked figure); dredging certificate dry solids and the planned_site column are also decoys for the asks. Business-realistic: certificate and survey files carry real irregularities (financial-year sheets, code change in Apr 2021, a re-issued certificate, nodata -99.99, two survey contractors on different datums and grids, a zero-dry-solids certificate line). No authoring or benchmark disclosures, no hidden sheets, no comments. Temporal coherence holds (latest survey Oct 2026, planning basis Jan 2027, Notice 3 Feb 2026). Public data contamination: none (fictional port). No exclusion-level finding. Cross-batch reference check: no other task folder was readable under the run rules, so I could not fingerprint against prior batches; nothing inside the bundle suggests a near-duplicate.

## Stump power (Gate F)
Moderate. A strong model that cleans the data and reads every file correctly will most likely file 1,500,000 (14.3/12.3) or 1,300,000 (carry the record) because the certificates alone never show a deeper channel; the trap that does the work is the response function, which only emerges by finding each reach's natural-bed plateau in the surveys and noticing siltation per m2 tracks depth below it (not depth). The 20+ gradable asks add independent ways to lose (join key, local time, moved stations, duplicates, unit mix). No too-easy signal: no document describes the law and no runbook states the defects. Optional lever: none needed.

## Stumping type (Gate G)
mechanism: forecasting (extrapolate a measured siltation law to a depth never held in the channel); stumping_family: analytical_non_defect; surface_read_dependency: no; sole_data_defect: no. The certificates and surveys are correct; nothing is overturned. On perfectly clean data the task still stumps (the easy depth-ratio route stays wrong). Passes.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`.
H1 swap test: the deciding quantity is a channel's infill rate against trench depth below the surrounding bed, a sedimentation estimate a dredging engineer makes; swapping nouns breaks it. H2 Layer 1 (mess): financial-year sheets against licence years, A/B code change, re-issued certificate, ODN against BCD with two survey contractors and grids, nodata sentinel, UTC against local, trip_ref join, ug/kg, moved stations and field duplicates. Layer 2 (rigour): derive the depth-below-natural-bed siltation law across the five reaches (checked on unmaintained NQ2 and on CT5) and apply it to the 10-year mean. H3: a strong analyst who cleaned everything and read every filed rule could still file 1,500,000 (depth ratio) or 1,300,000 (record), or 1,400,000 (trapping efficiency), all wrong; no decoy, no semantic flip, no rule execution decides it.

## Fix
none for the main call. Supplementary: input_files (optional alignment of the 2026 Area summary with licence 5.5) and solution (state the membership rule for the natural-bed cells, local-time zone note); metadata scrub on the docx.

---

# Determinism check, round 2 (2026-11-02): DETERMINISTIC (order kept; F strong; G PASS; H PASS), FIX_NOW (optional)

Isolated thread, Sonnet at medium effort, on target.zip 890c87d8.

# Verdict: task134 round 2

Order kept: derivation.md was written to disk before graded_blocks.md was opened. Cross-batch check: no prior-package access in this run, not performed.

- **Verdict:** DETERMINISTIC (no SOLUTION_WRONG; every golden figure reproduced).
- **Disposition:** FIX_NOW (optional, low severity). Give FE_dry_solids_revision_20260330.csv a one-line provenance header so the revision's authority is in the file. This touches 2 of 8 placement cells (Q2 Jan-Mar) and no analytic surface, so no model rerun is needed. If the author accepts the filename as enough ("revision" is the Layer 1 preliminary/revised overlap), APPROVE.
- **Why:** The year 1 total of 1,750,000 m3 and the six part volumes follow from the filed definition (docx: certificates' in situ volume, licence years 2016-17 to 2025-26 averaged, reaches and basin at 14.3 m, berths at present depths, NQ2 out). The depth law is data-forced. Per-m2 infill divided by (12.3 minus the natural bed read from the surveys) is constant to +/-4% across five reaches (log-log slope 0.98). The berths at 12.8 and 14.3 m rule out the (D-a)/D and D-ratio forms. Every other committed answer is fixed by a filed clause (licence 5.3 to 5.5), and a literal reading gives the golden. Taxonomy: none.

## Evidence (recomputed from target/)
| Item | My value | Golden | Source |
|---|---|---|---|
| Mean licence-year in situ volume, all maintained areas | 1,291,401 m3 | 1,291,401 | certificates, Oct-Sep re-bucketed, R1 reissue used |
| Natural bed OC / FR / MR / IR / TB | 8.10 / 8.28 / 6.44 / 5.34 / 4.75 | about 8.1 / 8.2-8.3 / 6.4 / 5.3 / 4.7 | Seaward (z minus 2.90) and Holmwood (-99.99 nodata), flats 30-250 m outside the width, 22 surveys stable |
| k = rate per m2 / (12.3 - a) | 0.1185, 0.1097, 0.1143, 0.1137, 0.1113 | 0.109-0.118 | certificates and NtM geometry |
| Year 1 total | 1,751,044 -> 1,750,000 | 1,750,626 -> 1,750,000 | scale by (14.3-a)/(12.3-a) |
| Parts, nearest 20,000 m3 | 380k / 300k / 400k / 280k / 360k / berths 40k (40,615) | same | |
| Wet t, FS Q1-Q4 | 203,085 / 93,915 / 214,056 / 211,068 | 203k / 94k / 214k / 211k | reproduced |
| Wet t, WD Q1-Q4 | 301,031 / 393,955 / 118,947 / 121,967 | 301k / 394k / 119k / 122k | reproduced |
| Metals Cd, Hg, Pb, Cu | OC 0.19, 0.13, 23.26, 15.50; FR 0.24, 0.16, 29.32, 18.87; MR 0.32, 0.25, 43.36, 27.60; IR 0.42, 0.31, 54.80, 34.75; TB 0.47, 0.35, 57.08, 36.31 | identical | reproduced |

Robustness of the main call:
- Ambient +/-0.1 m, the original A3 certificate instead of R1, both A3 certificates, the TB Feb 2024 outlier corrected, and financial-year instead of licence-year averaging all leave the rounded parts and the 1,750,000 total unchanged.
- The wrong answers are separable. No depth effect gives 1,291,401 (1,300,000). Scaling by 14.3/12.3 gives 1,494,781. A trapping-efficiency form (D-a)/D gives 1,511,823. A last-5-year mean gives 1,709,000.

Traps that sit in the lower steps and are all resolved by filed text:
- planned_site is not the placement site. 404 loads were dumped at the other site, and using planned_site gives FS Q1 323.7k instead of 203.1k.
- Licence 5.3 fixes UK civil time. Two loads at 23:12 and 23:33 UTC on 30 Sep 2025 fall in 2025-26. The load at 23:12 UTC on 30 Sep 2026 falls in 2026-27.
- A March 2026 placement uses the 2025 campaign, because the 2026 campaign completed on 12 March, not before the month. Using the reported date gives the same table.
- Four sample stations were moved into neighbouring areas (OC-05, FR-05, IR-01, TB-01). QA1 to QA4 are averaged with their primaries, and 12 mercury values are in ug/kg.
- Area summary fractions equal my recomputation from the lab data, so no fork. Unrounded fractions move the tonnes by less than 30 t.

## Findings (none changes the verdict)
1. **FE_dry_solids_revision_20260330.csv has no stated provenance (Gate B/E on supplementary 3, Q2 cells only).** No shipped text says it supersedes the load log. The certificate workbook (modified 14 Oct 2026) still carries the unrevised dry solids: Jan-Mar 2026 monthly sums match the log exactly and match the revision not at all. Not applying it gives FS Q2 99.9k (100,000) and WD Q2 417.9k (418,000) instead of 94,000 and 394,000. Applying it is the conventional reading and the file maps 146 of 146 trips by FE + UTC loading date + daily order. I rate the revised-supersedes reading as the forced one, but the fact rests on the filename only. Fix location: input_files. Add a one-line header or transmittal to the revision file. The golden does not change.
2. **The extrapolation law is not filed (Gate C, main call, minor).** A solver who fits one pooled k and predicts absolute volumes gets OC 366k, which rounds to 360,000 against 380,000. FR, TB and the total are unchanged. A solver who calibrates an exponent on the berths gets an unstable value (3.3 against 1.2). The reach-level history is the natural base and the ratio method is the standard expert route, so I treat this as the open method the data separates, not a fork. Fix location: none required. Watch OC only.
3. **Certificate Oct 2024 Middle Reach has two entries (A3 and A3/R1), and the TB Feb 2024 volume is a ratio outlier (25,164 against about 21,200).** Neither moves any rounded figure. This is Layer 1 mess, not a defect.
4. **Prompt wording.** "each part's volume" and "maintained berths" are closed by the docx (reaches, basin, berths together). A 3-part reading is a subset of the 6 parts, so there is no conflict. The prompt has no hedge and no loaded premise. FINAL_RECOMMENDATION states the siltation law as fact, but the prompt does not, so there is no prompt leak.

## Files/Hygiene: PASS
13 files in 4 formats (csv x8, xlsx x2, docx, pdf x2). The largest is the tide gauge with 96,432 rows (also above 25,000: seaward 34,742, holmwood 47,701). Distractors are the tide gauge, river flows, vessel arrivals, and the Holmwood surveys (the older datum copy of the same ambient bed). Document properties show organisational authors, with no toolchain or benchmark disclosures. Dates are coherent (docx 11 Jan 2027, surveys to 13 Oct 2026, certificates to Sep 2026). Nothing is exclusion-level. The only weakness is the unannotated revision file (finding 1).

## Stump power (Gate F)
Strong. The easy routes all file confident wrong totals: carry the record (1.3M), scale by 14.3/12.3 (1.49M), or use a trapping fraction (1.51M). Only a cut-depth-below-natural-bed model built from the surveys' off-channel bed gives 1.75M. Planted traps are absent. Placement cells are decorated with real Layer 1 mess that a strong model usually clears (UK time, planned versus actual site, moved stations, mercury units).

## Stumping type (Gate G)
`mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.
The reported certificates and surveys are fine. The difficulty is choosing the infill law the data support and calibrating it per reach. On clean data the task still stumps, because 14.3/12.3 is still wrong.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`.
- **H1:** a siltation and infill forecast for a maintenance dredging tender is the field's own analysis. The swap test fails to transplant the nouns (cut depth below natural bed, in situ versus wet tonnes, chainage geometry).
- **H2:** Layer 1 is the Oct-Sep re-bucketing of Apr-Mar sheets, the A1-B5 code change, the R1 reissue, datum conversion with -99.99 nodata, BST/UTC, trip-ref keys, ug/kg, and moved stations plus duplicates. Layer 2 is the depth-of-cut infill law.
- **H3:** the easy route a strong analyst who read every rule would take is a wrong answer. Hold the 12.3 m record (1.3M), scale by depth (1.5M), or use a trapping efficiency (1.5M); each is wrong. The law is inferred from reach and berth data, not stated or hidden. No decoy, no semantics decision, no rule execution decides it.

## Fix
- Location: input_files. Add a provenance line to FE_dry_solids_revision_20260330.csv (vessel, monitor recalibration, issue date, supersedes the log). It is optional but advisable.
- Nothing else. No prompt change is needed.

---

# Determinism check, round 3 (2026-11-02): DETERMINISTIC (order kept; F moderate to high; G PASS; H PASS), APPROVE

Isolated thread, Sonnet at medium effort, on target.zip dc8dc926.

# Determinism verdict, task134 r3

Order kept: yes. derivation.md was written to disk before graded_blocks.md was opened.

- **Verdict:** DETERMINISTIC (no SOLUTION_WRONG).
- **Disposition:** APPROVE. Nothing needs repair, and no rerun is required. Two optional notes are listed under Fix.
- **Why:** The main year-1 quantity and every ask reproduce from the shipped files, and the golden matches my independent derivation figure for figure. The one unfiled step is how infill scales with channel depth. The data fix it:
  - Infill per square metre divided by (12.3 minus the adjacent natural bed) is 0.113 to 0.114 in all five parts, with an intercept near zero.
  - The two 12.8 m berths and the 14.3 m Container Terminal Berth 5 (CT5), which is direct 14.3 m evidence, fall on the same line.
  - Competing routes either land on the same rounded figures (regression, additive CT5-versus-North Quay slope) or are falsified by the data (depth-ratio scaling).
  - The ETL asks are closed literally by licence condition 5.3 to 5.5, the Area codes sheet and the trip reference.
  - Gates A to E pass.

## Evidence (recomputed from target/)

| Item | My value | Golden | File and field |
|---|---|---|---|
| Mean in situ, licence years 2016-17 to 2025-26, 8 maintained areas, R1 certificate in place of original | 1,290,853 m3 a year | 1,290,853 | certificates xlsx, 10 sheets plus Area codes |
| Natural bed beside each part (m below CD; Seaward z_ODN converted with CD = ODN minus 2.90; Holmwood and Seaward agree after conversion) | Outer 7.93, Fend Roads 8.43, Middle 6.36, Inner 5.28, Basin 4.87 | about 7.9, 8.4, 6.3 to 6.4, 5.3, 4.9 | both survey csvs, cells beyond the NtM widths |
| Thickness per (12.3 minus bed), per part | 0.1142, 0.1130, 0.1135, 0.1135, 0.1132 | 0.113 to 0.114 | certificates divided by NtM area |
| Year-1 parts (m3, unrounded) | 378k, 299k, 398k, 278k, 359k, berths 36.9k | 380k, 300k, 400k, 280k, 360k, 40k | |
| Year-1 total | 1,749,500 | 1,749,627 and 1,750,000 | |
| Wet tonnes by quarter, Fend Spit | 195,970 / 107,901 / 214,897 / 222,171 | 196k / 108k / 215k / 222k | load log, licence 5.3 and 5.4, revision csv, Area summary |
| Wet tonnes by quarter, Wenning Deep | 299,081 / 381,947 / 121,098 / 113,164 | 299k / 382k / 121k / 113k | same files |
| Metals by area (Cd, Hg, Pb, Cu, mg/kg) | all 20 values equal the golden | | aldern csv, field log, Station plan |

Metals values:

| Area | Cd | Hg | Pb | Cu |
|---|---|---|---|---|
| Outer Channel | 0.19 | 0.13 | 23.26 | 15.50 |
| Fend Roads | 0.24 | 0.16 | 29.32 | 18.87 |
| Middle Reach | 0.32 | 0.25 | 43.36 | 27.60 |
| Inner Reach | 0.42 | 0.31 | 54.80 | 34.75 |
| Turning Basin | 0.47 | 0.35 | 57.08 | 36.31 |

- Two independent code paths gave identical placement tonnes.
- The 2026 Area summary fractions reproduce from the lab dry-solids results by actual position (OC 43.7, FR 42.5, MR 37.2, IR 34.06, TB 32.9, NQ1 31.5, NQ3 31.4, CT5 31.6 percent).

**Forks tested.** Each was checked for whether it flips a rounded answer:

| Fork | Alternative reading | Result |
|---|---|---|
| Depth scaling | Depth-ratio 14.3/12.3 | 1,495k, gives 1,500,000 (wrong). Falsified: the five reaches share one depth but have thickness 0.44 to 0.84. |
| | Regression of thickness on excess depth | 1,747k, same roundings. |
| | Additive slope from CT5 (14.3) versus North Quay Berths (12.8) | about 1,768k, still 1,750,000; parts unchanged. Margin to the 1,775k boundary is only about 7k. |
| | Depth-only power law from the berths (about 1,630k) | Different answer, but it fits the five reaches poorly, so the data reject it. |
| Certificates | Both Middle Reach Oct 2024 certificates summed | Middle Reach 401.8k, still 400,000. |
| | Reading code B2 as Berth 2 | Wrong, and closed by the Area codes sheet. |
| Part set | Berths shown separately | Closed by the planning note ("berth pockets together"). Rounded separately they would be 0, 0 and 20k. |
| Placement site | Using planned_site | Wrong for 408 of 1,708 loads. Licence 5.3 and 5.4 say "placed", and Fend Spit receives nothing Dec to Feb, consistent with condition 5.1. |
| Placement time | UTC instead of UK civil time | Moves 23:12Z and 23:33Z loads across a month, quarter or licence-year boundary. Licence 5.3 pins UK time, e.g. 30 Sep 2025 23:12Z falls in Q1 2025-26, and 30 Sep 2026 23:12Z falls in the next licence year. |
| Dry-solids fraction campaign | Using the 2026 campaign for March 2026 | Wrong: completed 12 Mar, not before March (licence 5.4). |
| Dry solids, monitor | Unrevised monitor figures | Q2 would be FS 115k and WD 405k. The revision file maps 150 of 150 trips (trip reference = FE, UTC loading date, nth load that day), with a constant ratio of 0.9364. |
| Maasbank formula | Odd operator precedence | The formula includes "(2.65 less 1.025)", so the standard reading is forced. |
| Sample area | Station-plan area instead of where the sample was taken | Wrong under licence 5.5. OC-05, FR-05, IR-01 and TB-01 move area; the plan-area means differ. |
| Duplicates | Treated as extra samples | Wrong under licence 5.5. QA1 to QA4 are averaged with OC-03, MR-02, IR-03 and TB-03 (3 to 4 m apart in the field log). |
| Mercury | ug/kg values unconverted | 12 values divided by 1,000. |

**Residual soft spots (none flips a graded figure):**
- The revision is applied only to the 150 listed trips. Trips from 1 to 6 Jan 2026 stay unrevised, and no trips fall between 27 and 29 Mar.
- Tonnes are tight to rounding: margins are 330 to 470 t on each rounded figure. They are exact once the rules are followed, but a single mis-timed load flips a cell.
- The parts rounded to 20k sum to 1,760k while the total is 1,750k. Both are independently determinate, and the prompt rounds them separately.

## Files/Hygiene: PASS
- 13 files in 4 formats: 8 csv, 2 xlsx, 1 docx, 2 pdf.
- The tide gauge has 96k rows and Holmwood has 47k, so the 25k-row floor is met.
- Distractors: tide gauge, river flows and vessel arrivals are unused by the solution.
- Real organisation documents; mixed date formats, renamed area codes and a re-issued certificate give realistic mess.
- Dates are coherent with the January 2027 planning note, and the latest data are the Oct 2026 survey and the Sep 2026 certificates.
- No README, authoring or benchmark disclosure found, and the docx, xlsx and pdf metadata are clean.
- Public-data contamination: none apparent.

## Stump power (Gate F)
- Moderate to high. A strong model that cleaned everything and read every rule may still file the carried-forward 1,300,000 m3 or the 14.3/12.3 scaling (1,500,000 m3).
- The cross-section evidence has to be found. After the datum conversion, the off-channel natural bed is the only thing that reconciles the five parts' very different infill at the same 12.3 m depth.
- CT5 and the North Quay berths give a second route to nearly the same rounded numbers, so the stump is the fact that the depth effect needs an analytical estimate, not a single trap.
- The asks add many independent chances to slip: BST boundary loads, planned versus actual site, the March campaign choice, the revision mapping, relocated samples and QA duplicates.
- Prompt and files do not pre-answer the method, and the planning note's year-1 definition does not hint at it.

## Stumping type (Gate G)
`mechanism: forecasting (extrapolating a correctly read infill record to a new depth), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no`
- The reported certificates are correct and none is overturned. The difficulty is projecting infill at a changed depth from the data's depth-scaling structure, and the task would still stump on perfectly clean data.
- Banned-scaffold finding: none.

## Three rules (Gate H)
`domain: pass, layers: pass, decisive_step: analytical`
- Swap test: the quantity that decides the call is maintenance dredging siltation under a deepened channel, which a hydrographic or dredging engineer estimates. The prompt does not read the same with another field's nouns.
- Layer 1: ODN versus chart-datum survey files, a survey vendor change, area-code renumbering, a re-issued certificate, a density-gauge revision, GMT versus BST, planned versus actual dump site, and sample position versus the station plan.
- Layer 2: infill in proportion to the depth below the adjacent natural bed.
- Easy route: carry the 12.3 m record (1,300,000 m3) or scale by 14.3/12.3 (1,500,000 m3). Both are wrong even after perfect cleaning and rule reading.
- H3 is analytical. The rule is estimated from the data, with intercept near zero and a direct 14.3 m check at CT5. It is not a planted defect, decoy or withheld rule, and it is not data semantics.

## Fix
- None required. Fix location: none.
- Optional: the 1,768k outcome of the additive CT5 route sits only about 7k under the 1,775k rounding boundary. Nothing in the ladder should rely on that route being wrong.
