# task484 determinism check (architecture 4)

3 isolated judge pass(es), each a Sonnet thread at medium effort that saw only a fresh unzip of target.zip, the prompt and the judge's system prompt, and opened the graded blocks only after its own derivation was on disk.

| Round | Pack | Verdict | Disposition | Action |
|---|---|---|---|---|
| 1 | ec5ec5c1 | DETERMINISTIC (order kept; F moderate to good; G PASS; H PASS) | FIX_NOW (hygiene) | openpyxl and python-docx producer metadata scrubbed from every Office file; the UTC register names each approach by arm |
| 2 | 39174925 | DETERMINISTIC (order kept; F good; G PASS; H PASS) | APPROVE | two section figures moved clear of their rounding edges under every detector-day treatment (tightest edge 0.0232 million), the call and every rung unchanged |
| 3 | 49241dce | DETERMINISTIC (order kept; F good; G PASS, method_or_model_selection / analytical_non_defect; H PASS) | APPROVE | none (the optional WHAT line not taken: the terms already define a section's annual traffic as the vehicles passing along it) |

Architecture 3's record is in determinism_check_report_arch3.md.

---

# Determinism check, round 1 (2026-11-02): DETERMINISTIC (order kept; F moderate to good; G PASS; H PASS), FIX_NOW (hygiene)

Isolated thread, Sonnet at medium effort, on target.zip ec5ec5c1.

# Verdict, task484 (a4r1)

**Order kept:** yes. derivation.md was written to disk before graded_blocks.md was opened.

**Verdict:** DETERMINISTIC (no SOLUTION_WRONG; every graded figure in the blocks reproduced).

**Disposition:** FIX_NOW. Scrub the toolchain tell in the three xlsx files (docProps/app.xml AppVersion 3.1, the openpyxl signature) and the python-docx default template in the log. Analytic surface is unchanged, no model rerun. Three optional prompt/file pins are listed under Fix; they would change what solvers see, so they are not required for this verdict.

**Why:** The nine-section list is the only answer the files support once the section's own signal-detector approach is used for the annual expansion. On the count day the detector's 07:00-19:00 flow equals one direction of the manual count (Brookfield 3,477 vs 3,401/3,657; Hollins 2,766 vs 2,640/2,653; Infirmary 3,530 vs 3,479/3,512; Station 4,376 vs 4,580/4,842; College 4,269 vs 4,159/4,199), so those detectors are the section's own traffic and carry its own week and year (weekend/weekday 1.51 Brookfield, 1.59 Hollins, 0.28 Castlegate). The permanent-counter urban/rural factors cannot reproduce those weekly shapes. The review workbook says it "does not test count point sections". I recomputed all 18 sections and every other graded figure and they match the golden.

**Evidence (all recomputed from target/):**
- Sections counted in 2025: 18 (count_points last_counted = 2025 = the 18 ids in manual_counts_2025.csv; all count days are term-time weekdays, no bank holiday, no streetworks permit on the street that day).
- Annual traffic = 12h all_motor_vehicles (both directions, pedal cycles excluded) x factor x 365. Own-detector factor (annual mean of detector 24h / same detectors' 07-19 flow on count day) for the 9 sections with a detector on their own road at an end junction: Brookfield Way 3.401 -> 3.4; Castlegate 2.568 -> 2.6; College Rd 2.488 -> 2.5; Grange Rd 2.714 -> 2.7; Hollins Lane 3.186 -> 3.2; Infirmary Rd 3.173 -> 3.2; Kingsway 4.173 -> 4.2; Mill Lane 2.596 -> 2.6; Station St 3.570 -> 3.6. Rest by urban/rural permanent-counter same-day ratio (mean of counter ratios): Wharf 4.687 -> 4.7; Ashfield 3.777 -> 3.8; Holloway Hill 3.518 -> 3.5; Priory 3.264 -> 3.3; Tanhouse 2.676 -> 2.7; Sandy 2.473 -> 2.5; Cradock 2.396 -> 2.4; Oakhill 1.887 -> 1.9; Lower Heath 1.420 -> 1.4. Over 3.0M: Wharf, Kingsway, Ashfield, Station, Holloway Hill, Priory, Brookfield, Hollins, Infirmary = 9. Reproduced, matches FINAL_RECOMMENDATION, SUPPLEMENTARY_ANSWERS (all 18 rows) and CRITICAL_COMPONENTS 1-3.
- Rounding robustness of the detector figures under four reasonable annual-mean variants (full-availability days only, all recorded days, NaN as zero, availability gross-up): no 1-dp value moves (closest: Station 3.554 vs the 3.55 line, Infirmary 3.173 vs 3.15). Ratio-of-sums vs mean-of-ratios moves no graded figure once Kingsway uses its detector (it only moved Kingsway on the counter route, 4.3 vs 4.4). WRA843's six missing days move nothing at 1 dp. Margins to 3.0 in the golden: Hollins +6.2%, Infirmary +5.8%, Priory +8.8%, Castlegate -14%, College -17%, Grange -9.5%.
- HGV a day (classes 5-7 before 8 Sep 2025, 6-8 from it; all 11 sites switch the same day, no break at the install dates; ops log 08/09 firmware push): 317, 501, 881, 908.5, 1372, 752, 450, 1198, 412, 1700, 978 -> 320, 500, 880, 910, 1370, 750, 450, 1200, 410, 1700, 980. Matches the golden.
- Approach totals (thousands): the controller renewals re-terminated the channels, so the register (post-renewal wiring only) mislabels the pre-renewal days. Pre-renewal mapping is recoverable uniquely from the data (lane-pair correlation 0.95-0.97, 24h/12h signature, weekend/weekday share, arm share of junction total). WRN0195: A 3,886; B 4,974; C 2,674; D 1,861 (1,860,522). WRN0868: A 4,349; B 3,253; C 1,399; D 1,674 (1,673,743). Matches golden. Register-only mapping would give 4,024/4,692/2,506/2,172 and 3,747/3,504/1,911/1,513, all eight wrong.
- Competing answer: permanent-counter urban/rural factors for every section give 8 sections (adds College Rd 3.28 and Grange Rd 3.33; drops Brookfield 2.72, Hollins 1.99, Infirmary 2.58). It does not survive: it contradicts the tie between the sections' own detectors and their manual counts, and a leave-one-out check of the counter factor on those detectors misses by up to 37% (Hollins 1.03 vs 1.65), against the review's 7.7% worst case on counters. Whole-junction pooling (all arms) gives yet another list (Brookfield 2.65, Hollins 2.12, Infirmary 2.64, College 2.99, Grange 3.09) but mixes cross streets whose 12h flow is several times the section's counted flow, so it is not a reasonable reading.

**Residual forks (none flips the main list under a reasonable reading; each is recorded):**
1. Estimator for the main call is not filed anywhere (no instruction, no filed back-test). The data separate the candidates (count-day tie plus the leave-one-out miss), but a solver who stops at the review workbook's 2% counter validation gets 8. Gate C/E risk: low-moderate; gives the stump, so it is not removable without removing the stump.
2. "Sections we counted" could be read to include the 11 permanent-counter sites (ADF x 365 = 2.5M to 10.2M, ten over the line). The supply fields (junctions, length) exist only for register count points and the 2025 programme is the manual one, so I read it as the 18. Gate E, low.
3. "Each approach" (supp. 2): register column `approach` holds the road name (Western Ave / Western Avenue, Fenwick Rd...), giving 2 groups per junction; the golden uses the 4 arms (road plus direction). Arm is the engineering meaning and the stop-line detectors sit on arms, but the register's own column invites the other. Gate E, low-moderate, supp. 2 only.
4. HGV class scheme (supp. 1): sites file lists TX-8 for every site and the log gives install dates, so a document-only reading (TX-8 all year, or legacy to install then TX-8) gives 212..1156 or 275..1322, not the golden. Only the class-mix break on 8 Sep (all sites, same day) and the firmware entry give the golden. Data-derivable, not stated. Gate B/C, low (supp. only, permitted to turn on semantics).
5. "Recorded" is read literally (the three blank days per junction contribute nothing); no gross-up. Treated as forced by the word.
- Minor internal date mismatch: register controller_installed/commissioned 14 Apr and 21 Jul vs log recommissioned 15 Apr and 22 Jul; data blank through the log date, no effect on any figure.

**Files/Hygiene:** PASS with one FIX_NOW item. 13 files; formats csv (7), xlsx (3), docx, pdf (2); one file of 37,231 rows (utc_detector_daily_2025.csv); distractors present (streetworks permits, school term dates, expansion review, 6 other junctions). Realistic mess: dd/mm/yyyy vs ISO dates, a repeated header row mid-file in the detector CSV (line 18463), blank loop-fault days, abbreviated register street names. No authoring or benchmark language found in any document; dates coherent with a 2026 supply deadline. Offending item: all three xlsx carry docProps/app.xml AppVersion 3.1 (the openpyxl signature) and the docx carries the python-docx default template. Not exclusion-level. Cross-batch fingerprint: no access to prior batches here, so not run.

**Stump power:** Moderate to good. The trap that does the work is estimating a section's annual figure from a one-weekday sample with the commuter-road permanent-counter factor that the review workbook appears to bless, when the section's own approach detectors show a weekend-heavy or weekday-only year. A strong model that stops at the counter factors lands on 8 (College and Grange in, Brookfield, Hollins, Infirmary out). A model that checks the sections' own detectors, which the prompt's second ask puts in front of it, gets 9. Supp. asks add an independent ID-remap and class-scheme layer.

**Stumping type:** `mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no` (borderline: the review's counter figures are correct for counters and are not a wrong reported read, the miss is applying them to sections), `sole_data_defect: no`. On perfectly clean data the choice of expansion comparison group (own approach vs commuter counters) still decides the call.

**Three rules:** `domain: pass`, `layers: pass`, `decisive_step: analytical`. Domain: expanding a short manual count to annual traffic with a matched expansion factor is the core of traffic estimation (swap test fails to preserve meaning in another field). Layer 1: channel re-termination at controller renewal, class-scheme change at a firmware push, mixed date formats, abbreviated street names, blank loop-fault days, a repeated header row. Layer 2: choose the expansion comparison group for each section on evidence. The easy route (counter group factors, validated at about 2% on counters) files 8 sections and the wrong set; a strong analyst who cleaned everything and read every rule still takes it. No planted rule, no decoy built to bless the wrong answer (the review states its scope limit), and the call is not a field reading or stated-rule execution.

**Fix:** none required for the verdict. FIX_NOW: strip xlsx/docx application metadata. Optional (each changes what solvers see, so it needs a rerun): pin "approach" in the prompt as arm and direction of travel; add the scheme change to the log entry for 8 Sep (but that hands out a Layer 1 fact); leave fork 2 as is.

---

# Determinism check, round 2 (2026-11-02): DETERMINISTIC (order kept; F good; G PASS; H PASS), APPROVE

Isolated thread, Sonnet at medium effort, on target.zip 39174925.

# Verdict, task484 (a4r2)

Order kept: yes. derivation.md was written to disk (own figures for every asked quantity) before graded_blocks.md was opened.

- **Verdict:** DETERMINISTIC (no SOLUTION_WRONG; every golden figure reproduced).
- **Disposition:** APPROVE. No repair needed; one residual method fork is flagged below and judged closed by the shipped data (optional, no rerun needed).
- **Why:** The call (9 sections over 3.0M) is forced once the expansion basis is tested against the shipped detectors: the filed urban/rural group same-day factor (expansion_factor_review_2025.xlsx, whose Summary says "Permanent counters only; the review does not test count point sections") misses the section's own year by 11 to 38 percent on 6 of the 9 sections that have detectors on their own approach (Brookfield -20, Hollins -38, Infirmary -19, College +32, Grange +23, Castlegate +11), beyond the review's own 10 percent target, while the approach detector tracks the section (manual 07-19 two-way count / detector 07-19 = 1.91 to 2.15 on all 9). Taxonomy if a reviewer disputes it: underspecified_objective (method of expansion not stated in any sentence), but the data separate the candidates, so it is not an open fork.
- **Evidence (recomputed, file and field):**
  - Sections counted in 2025 = 18 (count_points_2025.xlsx last_counted 2025 = manual_counts_2025.csv ids; 12 hours x 2 directions each; all_motor_vehicles = sum of non-cycle classes, 0 mismatches; count dates are weekdays outside term-date holidays and bank holidays).
  - Group method (urban/rural same-day ratio from atc_daily/atc_sites): Holloway 3.50, Station 3.57, Ashfield 3.79, Kingsway 4.36, College 3.28, Priory 3.28, Grange 3.33, Wharf 4.66 over = 8 sections. Network-wide, nearest-counter variants also give 8. Flat 24h/12h x 365 (no weekday-to-all-days conversion) gives 10 to 11. These are the wrong answers; the golden is 9.
  - Own-approach detector method (junction found from road plus end road in count_points, register abbreviations; factor = detector mean full day over 2025 / same detectors 07-19 on count day): Brookfield 3.401, Castlegate 2.568, College 2.488, Grange 2.714, Hollins 3.186, Infirmary 3.173, Kingsway 4.173, Mill 2.596, Station 3.568. All reproduce the golden's 1 dp values (3.4, 2.6, 2.5, 2.7, 3.2, 3.2, 4.2, 2.6, 3.6). Remaining 9 sections by group factor reproduce (Ashfield 3.8, Cradock 2.4, Holloway 3.5, Lower Heath 1.4, Oakhill 1.9, Priory 3.3, Sandy 2.5, Tanhouse 2.7, Wharf 4.7). Over-line set = Ashfield, Brookfield, Hollins, Holloway, Infirmary, Kingsway, Priory, Station, Wharf = 9. Matches FINAL_RECOMMENDATION and CRITICAL_COMPONENTS.
  - Fork stress tests on the detector method: excluding partial-availability days leaves the set unchanged (Hollins 3.199, Infirmary 3.187); same-weekday-same-month reference gives the same set. The only variant that moves a section is a typical-term-weekday reference built from school_term_dates.csv (College 3.23, over), which fails on the data: College's detector shows its school break running 31 Mar to 27 Apr, not the file's 5 Apr to 21 Apr, so that reference mixes holiday days into term and is an artifact. Same-day is also the method the review file files. Margins on the thinnest golden over-line sections: Hollins +6.2 percent, Infirmary +5.8 percent, clean (no valid estimator crosses the line except the artifact above).
  - Rounding edge to note, not a failure: Sandy Lane 2.464 (2.473 other ratio form) sits 0.014 above the 2.45 rounding boundary; Station 3.554 to 3.586 across detector-day treatments (3.5 only under a non-filed same-weekday reference).
  - Supplement HGV (classes by scheme): sites file says TX-8 for all counters, but the data keep legacy ARD-8 numbering until the 8 Sep 2025 firmware push (class 4 share falls 14 percent to 1 percent on that date at all 11 sites; the install dates do not switch it). HGV = classes 5+6+7 before 8 Sep, 6+7+8 from it, mean over recorded days: 320, 500, 880, 910, 1370, 750, 450, 1200, 410, 1700, 980. Reproduces golden exactly (WRA843 412/405/412 all round to 410; WRA508 908.5 safe). Install-date or all-TX-8 readings give e.g. WRA756 904 or 793, clearly wrong and separable by the class-share break.
  - Supplement approach totals: register is post-recommission; both junctions re-terminated channels at controller replacement (WRN0195 13-15 Apr, WRN0868 20-22 Jul, all detectors blank 3 days). Old to new channel map is recoverable and unambiguous from 07-19 share, weekday profile and level continuity in every window (WRN0195 old 01..06 to new 04,05,06,01,03,02; WRN0868 old 01..06 to new 06,03,05,02,01,04). Recorded totals thousands: WRN0195 W Ave S 3,886, W Ave N 4,974, Fenwick W 2,674, Fenwick E 1,861; WRN0868 Ring W 4,349, Ring E 3,253, Tanyard S 1,399, Tanyard N 1,674. All 8 match the golden. Register-only mapping would give e.g. 4,024/4,692/2,506/2,172 (wrong). Residual: "recorded" literally excludes the 3 blank days (gross-up would give 3,918/5,015/...); the word "recorded" pins it. Also repeated header row mid-file and dd/mm/yyyy dates, handled.
  - Gate A: golden step 8 (co-movement plus level/weekend share/07-19 share) and step 7 match my reconstruction; no figure changes between blocks; no overclaim. Gate B: every decisive fact is in a shipped file (register, detector daily, ATC, count points, review file, log); no external dependency; no invented vocabulary. Gate E: prompt asks one count plus list, units and rounding stated in the asking sentence; no hedge available.
- **Files/Hygiene:** PASS. 13 files; formats csv (7), xlsx (3), docx (1), pdf (2) = 4 formats; utc_detector_daily_2025.csv 37,231 rows (over 25k); distractors present (streetworks_permits_2025.csv, classifier_schemes/school_term_dates partly, expansion_factor_review_2025.xlsx). Files read as operational artifacts (mixed date formats, repeated header row, blank outage days, abbreviated street names). Dates coherent (scope note 26 Jan 2026, terms 12 Jan 2026, review refreshed 10 Feb 2026, data to 31 Dec 2025). No authoring or benchmark language found in docx or pdf. Nothing exclusion-level. I could not run a cross-batch fingerprint (no access to other tasks, per rules); not reported as clear.
- **Stump power:** Good. A strong model will read expansion_factor_review (group factors within 10 percent) and apply urban/rural same-day factors to all 18 sections, giving 8 sections and misclassifying College, Grange, Brookfield, Hollins, Infirmary; the naive flat 24h x 365 gives 10 to 11. The thin-margin sections (Priory 3.28 by group factor) are not near the line under any filed variant. Layer-1 mess (channel re-termination, firmware class renumbering, name abbreviations) is separable and not decisive for the main call.
- **Stumping type:** `mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The deciding step is choosing and validating the expansion basis out of sample against each section's own continuous detector, on honest data; the review file's figures are true for counters, the thing to resist is extending them to sections. Borderline note: the review file is a validated-looking official artifact for the wrong basis; it is accurate and self-scoped, not a wrong reported number, so Gate G passes, but live testing should confirm solvers do not treat it as a banned official-artifact refutation.
- **Three rules:** `domain: pass`, `layers: pass` (Layer 1: abbreviated register names, dd/mm/yyyy dates with repeated header, channel re-termination, firmware class renumbering, outage days; Layer 2: weekday-to-annual expansion of a short count validated against local continuous data), `decisive_step: analytical`. Swap test: puts another field's nouns in and the task no longer reads the same (AADF expansion from short counts is the traffic-monitoring field's own estimate). Easy route a strong analyst who read everything correctly would take: apply the review file's urban/rural same-day group factor to every count, giving 8 sections (including College Road and Grange Road, excluding Brookfield Way, Hollins Lane, Infirmary Road).
- **Fix:** none required (fix location: none). Optional, no rerun: none of the findings needs a prompt or file change; do not add a sentence telling solvers to use the detectors (that would file the HOW).

---

# Determinism check, round 3 (2026-11-02): DETERMINISTIC (order kept; F good; G PASS, method_or_model_selection / analytical_non_defect; H PASS), APPROVE

Isolated thread, Sonnet at medium effort, on target.zip 49241dce.

# Verdict, task484 (a4r3)

ORDER kept: yes. derivation.md was written to disk (from prompt + target/ only) before graded_blocks.md was opened.

- **Verdict:** DETERMINISTIC
- **Disposition:** APPROVE. No rerun is needed. The risks below are noted for the author. Optional hardening of the closure is a small in-house edit.
- **Why:** Nine sections are over 3.0 million (Ashfield Road, Brookfield Way, Hollins Lane, Holloway Hill, Infirmary Road, Kingsway, Priory Road, Station Street, Wharf Street). I reproduced this independently by expanding each manual 07-19 count with a same-day ratio from the section's own signal approach, and with the urban/rural counter ratio where no approach exists. The count day is a single weekday, and a local same-day ratio cancels day-specific effects. Those effects are visible in the data: College Road's own detector reads 4,296 for 07-19 on the count day against a typical weekday of 3,246, and Hollins Lane has a 24h/12h weekday profile of 1.40 against the counters' 1.17. The group-factor answer (8 sections: College Road and Grange Road in, Brookfield Way, Hollins Lane and Infirmary Road out) is the competing reading. It loses to a check the data allow. The same detector ratios reproduce the permanent counters' own ratios on the counter roads to a mean error of 3 to 4%, and the group factor fails the review's own 10% target on the sections' approaches. No taxonomy failure applies. Residual risks are listed under Evidence and Fix.

## Evidence (recomputed from target/)
| Item | My value | Golden | Reproduced |
|---|---|---|---|
| Scope: sections counted in 2025 | 18 (last_counted == 2025, equal to the manual_counts ids) | 18 | yes |
| Over three million, own-approach detector basis | Brookfield 3.41, Hollins 3.19, Infirmary 3.19, College 2.49, Grange 2.71, Castlegate 2.59, Mill Lane 2.58, Kingsway 4.31, Station 3.69 (units: millions; 3.0M = AADF 8,219) | 3.4, 3.2, 3.2, 2.5, 2.7, 2.6, 2.6, 4.3, 3.7 | yes; 1dp stable under full-days-only, availability-scaled and sum/365 |
| Group counter basis (the other 9 sections) | Ashfield 3.79, Holloway 3.52, Priory 3.48, Wharf 4.68, Tanhouse 2.69, Sandy 2.49, Cradock 2.41, Oakhill 1.79, Lower Heath 1.60 | 3.8, 3.5, 3.5, 4.7, 2.7, 2.5, 2.4, 1.8, 1.6 | yes; same 1dp whether mean of ratios or ratio of means, WRA843 taken over 359 days, over 365 or infilled |
| Counter HGV a day (rounded to 10) | 320, 500, 880, 910, 1370, 750, 450, 1200, 410, 1700, 980 | identical | yes |
| Western Avenue / Fenwick Road approach totals (thousands) | Fenwick Rd E 1,861; Fenwick Rd W 2,674; Western Ave N 4,974; Western Ave S 3,886 | identical | yes |
| Ring Road / Tanyard Lane approach totals (thousands) | Ring Rd E 3,253; Ring Rd W 4,349; Tanyard La S 1,399; Tanyard Lane N 1,674 | identical | yes |

**HGV class scheme.** The log says TX-200 outstations replaced the Ardent units on various 2025 dates, and the register lists TX-8 for all of them. The class data keep the ARD-8 pattern (class 5 is HGV, class 4 about 14%) after installation. Every site flips to the TX-8 pattern on 2025-09-08, the day of the firmware push. The data pin that day exactly.

**Reading the HGV classes by equipment from the install date** gives different figures (WRA756 900, WRA872 1,320, against the golden 1,200 and 1,700). All-ARD gives WRA756 1,130 and all-TX gives 790.

**Channel remap at the two renewed junctions.** The register carries only the post-renewal channel-to-arm map (all detectors commissioned 14 Apr and 21 Jul). Channel levels jump at renewal. Matching pre-renewal channel flow share and the 07-19/24h ratio to post-renewal channels gives a unique permutation: bootstrap 97 to 100% on shares alone, and the ratio separates the rest. Applying the register map to the whole year gives different totals, for example WRN0195 A 4,024 / B 4,692 / C 2,506 / D 2,172 and WRN0868 A 3,747 / B 3,504 / C 1,911 / D 1,513.

**Estimator fork (main call).**
- Counter groups: 8 sections.
- Own approach: 9 sections.
- Whole-junction ratio: Hollins 2.12, Brookfield 2.66, College 3.04, Infirmary 2.94, so it is not a reasonable third basis.
- Naive all-days 24h/12h ratio times 365: 12 sections (adds Castlegate, Brookfield, Infirmary and Tanhouse at 3.000).

**1dp sensitivity to which detectors count as the section's.**
- Kingsway: 4.31 on the end-junction approach, 4.17 if the WRN0683 Kingsway approaches are added.
- Station Street: 3.69 end-junction only, 3.64 with WRN0687, 3.80 with WRN0913.
- Neither moves the call. Both move one CSV 1dp figure each.

**Open items.**
- The Grange Road count (26 Mar) overlaps Station Street works (multi-way signals). The local ratio cancels this; the group factor does not.
- Gate A: all blocks agree. The FINAL_RECOMMENDATION sentence about the counters' factors matches my group-factor set exactly.
- Cross-batch: the package could be compared only against what is in this folder, so no near-duplicate was found or ruled out. The check against delivered tasks was not possible here.

Findings and the gate each fails (none flips the verdict):
1. Estimator not filed in any shipped file (Gate C / E, residual risk). Group factor vs own-approach detector is not stated. The files separate them (counter-road back-test, count-day anomaly), but a rigorous solver who stops at the Council's review gets the 8-section set. I judge that an analytical miss, not a defensible reading, because the review itself says it does not test count point sections.
2. The pre-renewal channel-to-arm mapping is absent from every file (Gate B, soft). It is recoverable uniquely from the data. The literal register-only reading gives a different supplementary answer 2 (all eight approach figures).
3. The HGV class scheme switch date is in no file as a scheme change (Gate B, soft). Only the firmware log date and the class-pattern break are shipped. The literal equipment-to-scheme reading (TX-8 from install) differs from the golden on all 11 counters, by 30 to 480 a day.
4. 1dp CSV fork on Kingsway and Station Street if a solver adds detectors at non-end junctions (Gate C, ask level). It does not affect which sections are over the line.
5. WRA843 HGV average is borderline between readings (411.8 over 359 days, 405.02 over 365 days). Both round to 410, so there is no fork, but the margin is 0.02.

## Files/Hygiene: PASS
13 files, 4 formats (7 csv, 3 xlsx, 1 docx, 2 pdf). The largest, utc_detector_daily_2025.csv, has 37,230 rows. The messy-but-realistic features (a repeated header row at line 18463, dd/mm/yyyy dates in one file and ISO in the others, abbreviated street types, 6 missing days at WRA843, blank flows on dark days) all read as system output. I checked the docx tables and the PDF tables explicitly. No README or authoring language was found and no benchmark disclosure. Dates are coherent: scope note 26 Jan 2026, terms 12 Jan 2026, review refreshed 10 Feb 2026 and due 31 Mar 2026. Distractors weigh but are unused: streetworks permits (one overlap, harmless), school term dates (used only to validate count dates), and the review workbook (its group method is scope-limited). Nothing exclusion-level.

## Stump power
Good. The review workbook invites the group same-day factor, which a strong model will likely take. It then files 8 sections: it puts College Road and Grange Road in and keeps Brookfield Way, Hollins Lane and Infirmary Road out. Catching this requires matching sections to their own approaches by street-name joins across abbreviations and testing the factor against local detectors. The class-scheme switch and the channel remap each add independent traps on the asks. Not too easy.

## Stumping type
`mechanism: method_or_model_selection` (representativeness of the expansion profile), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.
All reported counts and flows are correct. On perfectly clean data the task still stumps, because the choice of profile source decides the call. Borderline note: the review workbook is an official-looking method artifact that blesses the group factor, though only for counters. Route to the portal rather than ban it.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`.
Domain: annual traffic from a short count with expansion factors is the traffic-monitoring task type, and a swap with other nouns reads differently. Layer 1: class-scheme switch, channel remap, abbreviated join keys, a gap, a repeated header, mixed date formats. Layer 2: which comparison group the count day's expansion belongs to.
Easy route: apply the documented counter group factor to every section. This yields 8 sections (College and Grange wrongly in; Brookfield, Hollins and Infirmary wrongly out).
The stump is an estimand and comparison choice, not a rule or a field reading, but no filed criterion states it, as in finding 1.

## Fix
Where: none required (disposition APPROVE). Optional, in-house and without a rerun: file the WHAT by pinning in the review workbook's Summary or the prompt that each section's traffic is estimated "for that section" (no method). That would narrow findings 1 and 4 without naming the detectors.
Do not name the detectors or the remap.
