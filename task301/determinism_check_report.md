Determinism judge, stage 4 pass on target.zip 06472847 (task301, run r4): one isolated thread holding only the shipped bundle and the submission's graded blocks. The final pack (target.zip 1dbc72b8) drops the 2025 New South Wales public holidays from the team's calling days and archives a few hundred never-recorded patients in each candidate sub-region, two realism notes from the round's readers: the call and its figure are unchanged (Inner South, 563, printed 550), the ask B and C figures moved with the calendar, and generator/verify.py recomputes every graded figure from the final zip with 0 failures. The judge's evidence table quotes the round's pack.

# Verdict (task301, run r4)

- **Verdict:** DETERMINISTIC
- **Disposition:** APPROVE. One optional in-house pin below (the transfer-minutes convention in the xlsx minutes ask); no rerun needed.
- **Why:** The shipped files force Inner South at about 550. Regional two-state stop/relapse rates fitted to each region's own status history, applied to each list's recorded-smoker dates, give about 563 quits for Inner South against 523 Western Plains, 518 Coastal Hinterland and 442 Northern Corridor. Inner South stays first under every estimation variant I tried (about 558-565, which rounds to 550 each time). The naive reading, the largest recorded list times the 2025 conversion rate, picks Coastal Hinterland (8,422 listed, about 1,030 quits) and is wrong.

## Evidence (all recomputed from target/)
| Figure | Result | Source |
|---|---|---|
| Recorded current smokers (daily, weekly, irregular, smoker) | CH 8,422; IS 5,456; NC 4,855; WP 4,957 (reproduced; Eastern Shore 5,048 is not a candidate) | active_patients_2026-09-30.csv |
| Fitted stop / relapse per year (two-state Markov, last entry per day, interval-censored ML) | CH 0.110 / 0.015; IS 0.046 / 0.015; NC 0.071 / 0.015; WP 0.059 / 0.014. Model matches observed transition frequencies by gap-length bucket in every region. Practice-level fits are homogeneous within each region. | smoking_status_history parquet |
| Share of list still smoking at a 2027 call | CH 50.2%; IS 84.2%; NC 74.2%; WP 86.1% | derived |
| 2025 team rate per listed patient still smoking | 4149/5489 reached (75.6%) x 609/3756 = 12.26%. Cross-check: the Eastern Shore model puts 90.3% still smoking at call, which implies 12.29%. This matches the 90.5% implied by 393 of 4,149 reached saying they had stopped. | calls_eastern_shore_2025.csv |
| Expected 2027 quits | IS 563 (550); WP 523 (500); CH 518 (500); NC 442 (450) | derived |
| Variants | All-entries, drop-never-next, no relapse, S-only exponential, mid-year call, 5 patient bootstraps: IS 558-565, always first, WP 520-525 | |
| Quitline referrals 2025 by register sub-region | CH 888; IS 689; NC 623; WP 571 (reproduced). Quitline's own column gives 956 / 610 / 778 / 427. All 61 names match practices.csv after normalising case, Pty Ltd, Med Centre and GP. | referrals + practices.csv |
| After-5 pm calls and reached by weekday (start = date_time minus duration_s, Transferred legs excluded) | Mon 562/234; Tue 542/198; Wed 481/196; Thu 507/205; Fri 488/179 (reproduced) | dialler_legs_2025.csv |
| Minutes per patient reached, by login and month | All 30 cells reproduced (e.g. QO-C1 Feb 14.6, QO-N1 Jun 15.3). Months by leg start or leg end give identical values. | dialler_legs_2025.csv |

**Remaining forks, none flips an answer:**
1. **Weekday reading, closed by the data dictionary.** Reading date_time as the start instead of the end of a leg gives Mon 608/280 and so on. The dictionary says date_time is "when the dialler wrote the leg's record" and duration is "seconds from the dial until the line was released". That fixes start = date_time minus duration.
2. **Transfer minutes, the weakest point.** Without subtracting the Transferred leg, the minutes are about 15.2-17.1 instead of 13.6-15.5. The dictionary does not say the coach leaves at the transfer. The convention is recoverable only from the data: with start = date_time minus duration, 167 raw answered-leg overlaps per agent remain until the Transferred leg's seconds are removed, and then there are none. A careful analyst finds it, but it is inference, not a filed rule. Low risk, since this is an xlsx ask and not the main call. Optionally pin it in the prompt as "minutes on the call before any transfer".
3. **Referral basis, closed.** The register sub-region in practices.csv is what the dictionary calls "the sub-region the practice belongs to". Quitline's column is "in Quitline's report". The prompt says "sub-region's practices".
4. **Inclusion of 17:00:00 exactly.** One leg starts at exactly 17:00:00; "from 5 pm" includes it. It is already in the 562 / 542 / 481 / 507 / 488 counts.

## Files/Hygiene
PASS. 11 files in 5 formats: csv x7, docx x2, xlsx, parquet (plus the 289,893-row extract). Distractors: gp_workforce, quit_medicines, sub_region_profiles, and Quitline's own sub-region column. No README or authoring disclosure was seen. Messy wording is realistic (Best Practice vs Medical Director statuses, a practice that changed system, Quitline name variants). Nothing exclusion-level. I did not open the xlsx beyond confirming it is unused by the solution.

## Stump power
Moderate to good. A strong analyst who cleans the data and counts the recorded smokers gets Coastal Hinterland (largest list) and files about 1,000 quits. Applying Eastern Shore's observed staleness to every region keeps Coastal Hinterland first. Getting Inner South needs a per-region transition model fitted to the history, because the region lists differ in record age and stop rate. The Inner South lead over Western Plains is about 7.6%, so a crude decay still picks Inner South, and a solver who ignores the regional rates or the record age fails. The model is well identified (observed and fitted transition frequencies agree).

## Stumping type
`mechanism: forecasting` (plus method_or_model_selection), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The recorded counts are correct. The difficulty is projecting how many of each list will still smoke when called, from the region's own status-change dynamics. This passes Gate G.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Layer 1: two clinical systems' wording, a system migration, Quitline name and sub-region mismatches, a dialler that logs leg end-time with a transfer overlap. Layer 2: the field's multi-state (stop/relapse) survival estimation on irregularly observed status records, to project the prevalence of still-smoking patients at the future call date. Easy route: rank by recorded smokers times the 2025 conversion rate, which gives Coastal Hinterland (about 1,030 quits), or apply Eastern Shore's staleness uniformly (still Coastal Hinterland). The swap test fails for other fields' nouns: a status-transition model for smokers is domain-native.

## Fix
none (optional: prompt, one clause pinning the minutes convention in the xlsx ask).
