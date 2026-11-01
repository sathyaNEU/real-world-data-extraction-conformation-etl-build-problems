# task138 determinism check, architecture 2 (spent)

Two isolated judge passes on the levee-raise architecture. Round 1 broke the derive-first order (the orchestrator's brief carried the graded blocks) and found the main call's record choice open; the repair filed the period of record and converged every extension form; round 2 kept the order and failed Gate H3 (the district standard, read literally, fits the published record and files no raise). Architecture 2 was spent on round 2 and the slot re-rooted.

---

# Determinism check, round 1 (2026-11-01): NOT_DETERMINISTIC, SEND_BACK as labelled; Gate G PASS, Gate H PASS

Read against the gate table the failing gates are C and E (the main call's record choice, ask B's clock offset, ask A and B wording), a generator repair that spends no architecture (determinism-check, 'A disposition is read against the gate table'). The orchestrator's brief carried the graded blocks inline, so this pass broke the derive-first order and does not spend the one re-judge. Isolated thread, Sonnet at medium effort, on target.zip 1ceb1182.

# Determinism verdict, task138 (Orrinsford levee raise)

- **Verdict:** NOT_DETERMINISTIC (the golden reproduces exactly under its own method, but the main call, the design discharge and the raise table are not forced; the method is a fork the shipped text never closes).
- **Disposition:** SEND_BACK. File the estimand so that one record is the literal one (or ship a filed selection or extension criterion that separates the 18-year fit from the extended record), and close the ORF2 time-zone evidence for Ask B; a model rerun is required.
- **Why:** Gate C fails on the main recommendation, supplementary 2 and 3, and partly on supplementary 5. LS-02 s.2 asks for the design flood "for the river, its floodplain and its levees as they stand", s.3 says "fitted to annual peak discharges", and s.8 says peaks "are those published by the State Water Survey". No shipped sentence says to extend the post-2008 Orrinsford record with Coyle Bridge peaks scaled by 1.078. A hydrologist who sets aside the pre-2009 attenuated Orrinsford peaks and fits the 18 observed post-raise years gets 106,027 cfs, which is 105,000 cfs and a 1 ft raise. The golden's extended record gives 111,807 cfs, which is 110,000 cfs and a 2 ft raise. The two valid estimates straddle the 1 ft versus 2 ft line, which sits at about 109,000 cfs. Label: competing_defensible_answer.

## Evidence (all recomputed from target/)

| Item | Result | Source |
|---|---|---|
| Raised segments RM 41.0 to 12.6 (TR-L-07, TR-R-06, TR-L-08, TR-R-07, TR-L-09, TR-R-08); last raise Oct 2008; WY2009 first present-river year | Reproduced. Orrinsford peak for WY2008 is 22,400 (2008-03-21) and for WY2009 is 38,500 (2009-04-03), so starting at WY2009 or WY2010 gives the same 111.8k. | DNR_levee_inventory Segments, SWS annual peaks |
| Ratio of Orrinsford to Coyle Bridge, WY2009 to WY2026, through the origin | 1.0780 | SWS_annual_peaks |
| Pre-2009 attenuation | Only 1970 (ratio 0.720) and 1973 (0.815) fall far below about 1.07. No flood between 60k and 80k exists to show where attenuation stopped. | SWS_annual_peaks |
| Station skew of the extended record, N=65 | 0.504; weighted skew 0.2435 (MSE_G 0.1129, region 2: -0.08 and 0.14, Marrow County) | SW-16-03, annual peaks header |
| 1% discharge, extended record | 111,807 cfs, so 110,000 cfs. Stable at 111.2k to 113.6k for other extension forms (OLS, log-log, b 1.07 to 1.10). Rounds to 110,000 in every case. | recomputed |
| 1% discharge, other records | 18 post-raise years only: 106,027 cfs (105,000). Published Orrinsford record, 65 years: 96,995 cfs (95,000). Published record without 1970 and 1973: 85k. | recomputed |
| Closure at 118+70 against design water surface plus freeboard (HWE Table 4, linear in discharge; 4.0 ft + 0.5*(180-118.7)/180 ft) | 1.48 ft short at 111,807 cfs; 1.17 ft short at the rounded 110,000. Both give a 2 ft raise. The same check gives 0.47 ft short at 106,027 (1 ft raise) and 1.13 ft surplus at 96,995 (no raise). | recomputed |
| Annual chance by raise, extended curve (capacities 103,369 / 109,056 / 114,770 / 120,580 / 126,402 cfs) | 1.4, 1.1, 0.9, 0.7, 0.6 per cent. Reproduced. | recomputed |
| Same table, 18-year curve | 1.1, 0.9, 0.7, 0.6, 0.4 per cent. Published curve: 0.7, 0.5, 0.4, 0.3, 0.2. | recomputed |
| Ask A settlement (2016 minus 650 ft, plus 0.27 ft NGVD to NAVD, BM check rows excluded, paired by station within the 2024 reach) | R1 to R8: 0.07, 0.12, 0.16, 0.21, 0.29, 0.24, 0.14, 0.09. Reproduced. The 650 ft offset comes from the four structure shots: 24+80 to 18+30, 68+90 to 62+40, 125+20 to 118+70, 167+70 to 161+20. Interpolating either survey onto the other gives the same two-decimal values. A mean-of-reach-means gives R1 0.06, R2 0.11, R8 0.10, so a minor fork exists. | crown surveys, benchmark list |
| Ask B, golden method | 35.7, 29.0, 37.7, 36.8, 31.1, 33.6, 51.9 hours, rounding to 36, 29, 38, 37, 31, 34, 52. Reproduced. Seven events reach 17.45 ft on ORF2 (617.45 NAVD less 0.27 less 599.73). Taking the first hourly reading at or above each level gives the same whole hours. | ORF2 export, Coyle hourly, OP-04 |
| Coyle stage step | +2.00 ft at about 19 Oct 2021 with discharge unchanged. The warning stage is 21.0 before the step and 23.0 after. It is discoverable from the stage and discharge columns plus OP-04's "21.0 ft". It only affects the three 2020 events. | Coyle hourly |

### Forks left open by the shipped text

1. **Record for the present river (main call, supplementary 1 to 3).**
   - Extended record (Orrinsford from WY2009, Coyle Bridge times 1.078 before): 110,000 cfs, 2 ft, table 1.4 / 1.1 / 0.9 / 0.7 / 0.6.
   - 18 post-raise Orrinsford years: 105,000 cfs, 1 ft, table 1.1 / 0.9 / 0.7 / 0.6 / 0.4.
   - Published record, as LS-02 s.8 literally reads: 95,000 cfs, no raise, table 0.7 / 0.5 / 0.4 / 0.3 / 0.2.
   - The 18-year fit is the "observed and published" reading of s.8 and s.2. Its estimate is not wrong, only noisier. No filed criterion, back-test or standard picks record extension over it, and the margin between the two straddles the deciding line (Gate C(a)). The golden's own text concedes the 18-year result (106,000 cfs).
2. **ORF2 time zone (supplementary 5, March, May and June 2020).** The ORF2 header says "Time zone: UTC" for every row.
   - The golden shifts the rows before the June 2021 swap by +6 h on the basis of published peak times.
   - That evidence is loose. Coyle Bridge's own UTC hourly peaks fall 3 to 5 h (mean about 4) after the published local peak times, which implies a 4 h offset. The Orrinsford regime difference (pre-swap logger minus published about -1, post-swap about +4.5) implies about 6. The 18:00 start on 30 Sep 2016 is a further weak hint at 6.
   - Results by shift: +6 gives 36, 29, 38; +5 gives 35, 28, 37; +4 gives 34, 27, 36; the literal header (0) gives 30, 23, 32.
   - Whole-hour rounding also matters. Truncation would give 35, 28, 37, 36, 31, 33, 51.
3. **Minor.** Settlement by mean-of-means versus paired differences (above). The claim that the reach name text (for example "north tie-in to Pump Station 1") appears in a shipped file was not found. Only R1 to R8 appear, in the 2024 survey.

### Competing answers stress-tested

- No raise (published record): contradicted by the filed principle that the record must represent the river as it now runs. Orrinsford peaks of 1970 and 1973 are about 28% and 18% below Coyle Bridge scaled, while all other years sit near 1.07. This answer fails on the files.
- 1 ft (18-year record): survives, as above.
- 2 ft (extended): survives. It is the better-supported estimate, since the correlation is very tight and the record is longer, but it is not forced by anything filed.

## Files/Hygiene
- **PASS.** Thirteen files in three formats (csv x7, pdf x5, xlsx x1). The largest files are ORF2 (87.6k rows) and the Coyle hourly series (87.6k rows). Distractors are present: the coop precipitation file, the 2025 inspection summary, the Gale Creek and Ashby peaks, and the 18-hour closure time in OP-04.
- No README, synthetic or benchmark disclosure was found. The documents read as operational artifacts, with a mixed-format Crown raised column and provisional codes.
- Temporal coherence: the 2026-10-28 retrieval and the 2026-10-05 export are consistent with a 2027 season. No answer-contaminating public dataset was found. No exclusion-level finding.
- Layer-1 hazard: the ORF2 header claims UTC but the rows before the swap are in local time. The Coyle header claims datum 638 but the stage before 19 Oct 2021 is on 640. Both are discoverable but unfiled, and the first is the fork above.

## Stump power
- The trap that would do the work is the easy route of fitting the published Orrinsford record: it gives 97,000 cfs, no raise, and a table of 0.7 / 0.5 / 0.4 / 0.3 / 0.2. A strong model that finds the pre-2009 attenuation could then still split between the 18-year fit (1 ft) and the extended record (2 ft), so some failures would be interpretive rather than analytical.
- Natural lever: make the estimand unambiguous in the prompt or LS-02 without filing the HOW. For example, file the population as "the discharges the present river would carry in the years of the Coyle Bridge record", or ship a filed back-test or extension criterion.

## Stumping type
`mechanism: forecasting/nonstationary frequency (method_or_model_selection)`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The published peaks are correct. The difficulty is recognising nonstationarity from levee raises and building a representative record, which would still stump on clean data. Gate G passes.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`. The deciding quantity is a flood-frequency design discharge (log-Pearson III, skew weighting, a record representative of present conditions, a whole-foot raise against the water surface plus freeboard), work that is native to flood hydrology. Layer 1 is the NGVD to NAVD datum shift, the 650 ft re-stationing, the Coyle gauge datum step, the CST to UTC logger swap, and the water-year assignment. Layer 2 is the choice of record under nonstationarity. The easy route is to fit the published Orrinsford record, which gives 95,000 cfs and no raise. The H3 test passes, though the choice among the correct routes is the unclosed fork.

## Fix
`prompt` and `input_files`. Pin the estimand so that the 18-year result is not licensed (or make the 18-year fit visibly inferior with a filed criterion such as a minimum record length or a stated record-extension practice), and file the ORF2 stamp convention (a time-zone note for the pre-swap rows, or a header that agrees with the rows). The supplementary 4 reach descriptors need a shipped source or should be dropped to R1 to R8, and the prompt should say that lead times are rounded to the nearest whole hour.


---

# Determinism check, round 2 (2026-11-01): NOT_DETERMINISTIC, SEND_BACK; order kept; Gate G PASS; Gate H3 FAIL

The re-judge after round 1's repair (the period of record filed, the extension forms converged, the ORF2 clock forced). Read literally, LS-02 s.3 and s.8 send the fit to the published Orrinsford peaks (0 ft), and no filed sentence makes the present-river reconstruction the estimand: a strong analyst who reads every rule correctly is licensed to file no raise, so the decisive step fails H3. Architecture 2 is spent and task138 re-roots as architecture 3 in another world. Isolated thread, Sonnet at medium effort, on target.zip 81bc1b75.

# Verdict: task138 (Orrinsford levee raise)

- **Verdict:** NOT_DETERMINISTIC
- **Disposition:** SEND_BACK. The decisive step (restating the pre-2009 Orrinsford peaks to the river as it now runs) is nowhere filed, and the filed LS-02 s3 read word for word gives the opposite call. The fix has to change the shipped standard or prompt, so the golden and the stump change and a rerun is required.
- **Order kept:** yes. derivation.md was written to disk before graded_blocks.md was opened.

## Why
LS-02 s3 files the design flood as a log-Pearson III fit to "one annual peak discharge for every water year since the Orrinsford gauge opened", and s8 says discharges come from the State Water Survey's published records. Executed literally on SWS_annual_peaks (65 Orrinsford peaks, WY1962-2026, region 2 skew from SW-16-03 via Marrow County) it gives Q100 = 95,430 -> 95,000 cfs. The tightest section (118+70) then has 1.16 ft of spare crown, so the levee meets the standard and the raise is 0 ft. The golden (2 ft, 110,000 cfs) holds only after Orrinsford's pre-2009 peaks are replaced by 1.064 x Coyle Bridge peaks. No shipped sentence says to do that, nor which years, which gauge or which estimator, and the golden's own text concedes the published record gives 95,400. The only licence is LS-02 s2's "as they stand at the time of the review" plus a timing inference from the DNR inventory's crown-raise dates (the inventory never states that the raises changed flood peaks). The literal answer to the main call (and to ask 3) is a defensible competing answer, so Gates B, C and E fail. Governing label: answer_contradicts_files (competing_defensible_answer is the secondary label).

## Evidence (recomputed from target/)
| Item | Result | Golden | Reproduced |
|---|---|---|---|
| Literal LP3, published record: Q100, weighted skew 0.1332 | 95,430 -> 95,000 | n/a | yes, own value |
| Literal crown check | no raise (min slack +1.16 ft at 118+70; shortfall only above 101,926 cfs) | 2 ft | golden does not follow from the filed text |
| Literal annual chances raise 0..4 | 0.7, 0.5, 0.4, 0.3, 0.2 | 1.4, 1.1, 0.9, 0.7, 0.6 | differ |
| Golden construction (Orrinsford 2009+, 1.0643 x Coyle before) | Q100 110,403; shortfall 1.50 ft at 118+70; chances 1.401, 1.118, 0.896, 0.721, 0.583 | matches | yes, exactly |
| 18 post-2008 years only | 104,714; shortfall 0.50; raise 1 | named as the wrong route | yes |
| Settlement by reach (mean, 2016 +0.27 ft, 700 ft shift, minus 2024) | 0.07, 0.12, 0.16, 0.21, 0.29, 0.24, 0.14, 0.09 | matches | yes |
| Lead times (hours) | 37, 29, 38, 38, 32, 35, 51 | matches | yes (first hourly reading and interpolated crossing agree) |

Forks that survive, with the answers each gives:
1. **Main call and asks 1 to 3 (Gates B, C, E fail).**
   - Literal s3, published peaks: 0 ft, 95,000 cfs, 0.7/0.5/0.4/0.3/0.2.
   - Post-raise 18 years only: 1 ft, 105,000 cfs.
   - Golden transfer from Coyle: 2 ft, 110,000 cfs.
   - Replace only the attenuated years (1970 and 1973, ratio under 0.95): Q100 108,448 -> 110,000 and 2 ft, but chances 1.3/1.0/0.8/0.7/0.5 (ask 3 differs).
   - Transfer from Ashby: 111,000, same 2 ft and chances.
   - Transfer from Fenwick, which is downstream and sees the same attenuated flows: 0 ft.
   - Within the all-pre-2009-years Coyle transfer family the 2 ft call and the 1-decimal chances are stable (start years 1994 to 2010, origin/mean/median ratio, log-log fit), so the golden is robust only once the unfiled reconstruction is accepted.
   - The prompt says "the river" without saying published or present-river conditions, so even the chart's "frequency curve" has two candidates.
2. **Ask 4 (Gate E, minor).** "How much the crown settled in each reach" is not defined as mean, median or maximum. The mean and median agree to 0.01 ft; the maximum gives 0.10, 0.14, 0.19, 0.24, 0.31, 0.26, 0.17, 0.11. Unfiled.
3. **Ask 5 (Layer 1, derivable but not stated).**
   - The ORF2 header says "Time zone: UTC" for all records, but rows before the clock splice (file row 41,151, the 72-hour block repeated with values shifted exactly 6 h) are in local standard time. Evidence: the 2017-2021 peaks match SWS peak_tm (local) with 0 h difference and the 2022-2026 peaks with 6 h. The literal header reading gives 31, 23, 32 h for the 2020 floods.
   - OP-04 gives the warning level as 661.00 ft NGVD29 and "21.0 ft on the gauge", while the hourly header gives datum 638.00 (so 23.0 ft). The data show a 1.98 ft stage step on 2019-10-22 15:00 UTC (the older datum was 640.00), so the elevation governs. Using 21.0 gives 42, 33, 43, 43, 35, 41, 57 h.
   - The sill must be converted NAVD88 to NGVD29 (stage 16.95; 17.22 unconverted; 17.49 wrong direction, which drops the May 2025 flood at 17.37). The benchmark list pins the +0.27 ft direction.
   - These are recoverable from the files, so I rate them acceptable Layer 1 mess, but no sentence states them.
4. **Gate A.** Every golden figure reproduces under its own construction. Critical component 1 holds (six segments between RM 41.0 and 12.6, last raise Oct 2008 -> WY2009). No misattribution.

## Files/Hygiene: PASS, with notes
13 files, 3 formats (6 csv, 5 pdf, 1 xlsx plus the logger csv). Two files over 25,000 rows (hourly 87,635 and logger 87,720). Distractors: the coop precipitation file and the 2025 inspection report. The DNR inventory is decisive in the golden (raise dates), so it is not a distractor there. The inventory's "Last inspection Aug 2024" for TR-L-10 trails the 2025 inspection report (Aug 2025), a minor incoherence. No authoring or provenance leakage found. Public-data contamination: none.

## Stump power (Gate F)
The trap the golden relies on is a nonstationary record. Orrinsford is 0.71 and 0.80 of Coyle in 1970 and 1973, against 1.06 in 2020 and 2024, and the filed s2 hints at it. The easy route, the literal fit of s3, files 95,000 cfs and no raise. A strong model that obeys LS-02 word for word will land there. The failure is partly by obedience to the filed rule rather than by a missed analysis. Lever: file the WHAT (the population of peaks is the discharges the river would carry to the Orrinsford gauge with the upstream levees as they now stand), so that the correct reading is licensed.

## Stumping type (Gate G)
mechanism: method_or_model_selection (record representativeness / homogenization), stumping_family: analytical_non_defect, surface_read_dependency: no (borderline, because the published Orrinsford peaks are correct readings that are judged unrepresentative), sole_data_defect: no (the nonstationarity is physical; the 2009+ and transfer reconstructions are the analysis). The risk is that the official standard blesses the easy method, which is close to a certified wrong method.

## Three rules (Gate H)
domain: pass (LP3 flood frequency, design water surface and freeboard check, exceedance probability of levee capacity are the field's own work)
layers: pass (Layer 1: NGVD29/NAVD88 and 700 ft restationing in the 2016 survey, reach-grain matching, clock splice and mislabeled UTC in ORF2, Coyle datum step, duplicate block. Layer 2: representativeness of the annual-peak record under changed floodplain and levees)
decisive_step: analytical in intent, but as shipped it fails H3 for lack of a filed rule. The easy route (execute LS-02 s3 on the published peaks) gives 0 ft and 95,000 cfs, and the golden's correct route needs a reconstruction method the bundle never states, so the call is not forced. SEND_BACK on Gate H3 as well as B, C and E.

## Fix
Fix location: prompt and input_files (LS-02 s2 or s3, or the prompt), not the solution.
1. File the estimand: the peaks fitted are the discharges the river would carry to the Orrinsford gauge with the upstream floodplain and levees as they now stand, without filing the HOW. Say whether the chances and the chart are on that curve. The unlicensed alternatives (published record, 18 years only, attenuated years only) must then be ruled out by the filed text.
2. Pin the scope of restatement (all pre-raise years or only those the floodplain cut) so that ask 3's 1-decimal chances close, since 1.4/1.1/0.9/0.7/0.6 and 1.3/1.0/0.8/0.7/0.5 are both reachable now.
3. Say "average crown settlement in each reach" in the prompt.
4. State in the ORF2 header (or a logger note) the clock basis before and after the change, or accept the data evidence. State in the OP-04 line that the 21.0 ft figure is on the older gauge datum, or drop it.

