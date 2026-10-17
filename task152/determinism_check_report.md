# Verdict: task152 (Hadley Ranch Solar 2027 forward volume), re-judge

**Verdict:** DETERMINISTIC (SOLUTION_WRONG, minor: the wrong-path figure "73,000" in FINAL_RECOMMENDATION does not reproduce; see Evidence).

**Disposition:** FIX_NOW. Regenerate the one narrative sentence in the Final Recommendation that quotes the "whole DC-side decline restored" answer; no change to the prompt or the shipped files, no model rerun.

**Why:** The committed volume of 70,000 MWh is forced by the shipped files. The policy (sections 3.1, 4.1, 4.2, 4.4) fixes the estimand: net energy at meter 0417, the one-year P90 as P50 less 1.2816 sample SD over the 25 local calendar years of the Clearfield record, the plant as it will stand, and a base period of Oct 2025 to Sep 2026. The method is left open and the data separate the candidates. The base performance ratio, wear, soiling and inverter-loss decomposition, and the 14.7% gain on an unexposed comparator all reproduce independently. Every ask (availability, over/under) also reproduces exactly.

## Evidence

Literal reading first. Estimand and conventions come from the policy, the O&M Schedule 4 and the LGIA Exhibit C. Options where the text is silent: the wear estimator, the soiling treatment, flat versus monthly PR. All of those are method choices that the data pin (see the margin table below).

| Item | Golden | My recompute (file, field) | Reproduced |
|---|---|---|---|
| Base PR Oct 2025 to Sep 2026 | 63.7% | 0.63706 = (PLANT-RM E_EXP - E_IMP) / (H_POA x 40,320); PLANT-RM matches district REC/DEL to 0.1% over 2,130 overlap days | Yes |
| Wear: post-wash (days 1 to 3 after the CLN completion date), temperature-corrected (-0.42 %/degC, T_MOD_IW), Dec 2025 vs 2016 | 14% | 0.8619 (13.8%); stable at 0.861 to 0.863 across windows 1-1, 1-2, 1-5, 1-7, season-matched, no op-hour filter, median | Yes (within rounding) |
| Wash timing | n/a | The wash step shows on the WO Completed date (day 0 partial, day 1 full recovery) | Supports the method |
| Repowered PR | 85% | 0.6371 / 0.8619 x 1.147 = 0.8478 (0.8497 at exactly 14.0%) | Yes |
| Independent cross-check via Corvane Table B (1.0132 DC PR x soiling 0.894 x AC/DC 0.9586 x net/AC 0.977) | n/a | 0.848 | Agrees with the golden route |
| P50 / SD / P90 | 73,000 / 1,900 / 70,000 | Clearfield local-year POA mean 2,309.7, SD 60.8 kWh/m2 x 0.8478 x 37,324.8 kWp gives P50 73,080, SD 1,923, P90 70,615 (70,807 at PR 0.85) | Yes |
| Ask 4, 16 availabilities | see golden | Production hour = met POA >= 50 W/m2 (MST hour); unavailable = zero-AC production hour; the hourly file's logger gaps resolved by the lifetime register; excluded = zero-AC hours inside the 4 district interruptions (the cancelled planned outage ignored) and the two Owner stops (WO-25-21573 B1 11 Feb, 09:00-14:05; WO-25-21669 B3 29 Sep, 08:10-15:00, matching event log) | All 16 match to 0.01 |
| Ask 5, over/under 2016 to 2025 | +4,020 ... +7,715 | District REC - DEL at service point 0417 only (0418 station service excluded), MDM latest version, legacy day = stamp - 1 day, legacy before 1 Oct 2019 and MDM after; sold = confirmations with amendments (2021 55,500; 2024 50,200) and buy-backs (2019 -1,400; 2022 -1,100) | All 10 match to the MWh |

Wrong paths on the main call:
- Base PR x 1.147 gives P90 about 60,900, so 60,000. Reproduced.
- First-year (2016) PR x 1.147 gives about 76,500, so 76,000. Reproduced.
- "Whole DC-side decline restored" gives about 74,000 to 74,500 in every variant I tried, not the 73,000 the Final Recommendation quotes. Not reproduced; not load-bearing (narrative only).

Margin and competing answers (Gate C):
- 70,000 holds for wear between 13.1% and 14.26%. My estimate is 13.8 to 13.9%. Monthly PR with monthly Corvane gain gives P90 70,734 to 70,890. Both fall in the 70,000 bucket.
- The upper boundary (71,000) is about 0.4 points of wear away. The only variant I found that crosses it is a season-matched estimate with no temperature correction (14.3%). That is an error, since the datasheet coefficient and T_MOD_IW are both shipped and the wash seasons differ between 2016 and 2025. Dropping the import subtraction, which the policy forbids, also crosses it. I call this thin-but-clean, not contested.
- Fork table on the asks:
  - Excluded Hour read literally as a zero-AC production hour inside the outage gives the golden. Reading every outage-window hour as excluded moves four cells by 0.01 (B1-INV3, B3-INV1, B3-INV4, B4-INV4). The agreement's text ("Production Hour in which the Inverter delivers no AC energy because of...") supports the golden.
  - Reading the 40 single-inverter F-217 "AC GRID FAULT" events as utility outages moves most availabilities up by 0.1 to 0.5. The four plant-wide F-217 clusters coincide exactly with the district report. The single-inverter ones are inverter-side per the WO text (breaker/relay checks), so the golden reading is the supported one.
  - Treating the logger-gap hours as unavailable would cost every inverter 0.6 to 1.0 point. The register shows energy flowed, so this is a data-handling trap that the files resolve.
  - Using the blotter's unamended quantities (2021 58,000; 2024 52,000) instead of the confirmations' amendments would flip 2021 from +534 to -1,966. The confirmations (counterparty-signed) govern, and the README says the blotter carries "quantities as traded".

Gates: A pass (grain, units, UTC/local, missing 14 to 16 Aug 2018 days in SCADA, MDM v2 supersede, inverter 07 to B2-INV3R all handled); B pass (every decisive fact is in a shipped file: meter definition, wear data, gain, scope, O&M, wash dates); C pass with the margin note above; D pass; E pass (prompt names the estimand and delegates the method).

## Files/Hygiene
PASS. 23 files; formats: csv, pdf (8), docx, xlsx (2), txt, md. Largest are the 25-year hourly Clearfield (219k rows) and the SCADA daily export (127k rows). Distractors present and unused: the Palo Verde forward marks, the Tresco repowering summary (+9 to +18% for other plants), and the cancelled planned outage in the district report. Metadata is clean (no tool banners, authors in-fiction). Dates are consistent (pull on 6 Oct 2026, SCADA to 30 Sep 2026, works start 5 Oct 2026). Minor: the README names the district files "the meter of record" and explains REC/DEL direction, which is Layer 1 help and not the stump. Nothing exclusion-level. The cross-batch fingerprint check was not run, because other tasks are outside the isolation boundary.

## Stump power
High. The decisive step is separating the original modules' wear (which the replacement removes) from soiling and the inverters' AC/DC loss (which stay), via temperature-corrected post-wash levels against a wash-matched 2016 reference. The natural easy routes file 60,000 (gain on the worn baseline) or 76,000 or about 74,000 (restoring the first year or the whole DC-side decline). Reaching 70,000 needs the full chain. The scope paper ("output has fallen since 2017") and the Corvane "unexposed" note give a strong model a nudge toward the right frame, but the estimation chain is long and the decomposition is easy to get wrong.

## Stumping type
`mechanism: decomposition_attribution (with a forecast on a correctly read past)`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.
The reported base PR, the Corvane gain and the weather record are all correct. The difficulty is attributing the decline to its drivers and applying the gain to the right baseline, and the task still stumps on perfectly clean data.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`.
- Swap test: with "school/hospital" nouns, the task no longer reads the same. The deciding quantity is a PV one-year P90 built from degradation, soiling, inverter loss and weather-year irradiance, which is core energy-yield-assessment work.
- Layer 1: two SCADA layouts (kWh local days vs MWh UTC day-starts, inverter 07 to B2-INV3R), a legacy plus an MDM district record with a version supersede, station-service meter 0418, logger gaps, and amended confirmations against the blotter.
- Layer 2: wear versus soiling versus inverter-loss attribution, and the right comparator for the gain.
- Easy route: a strong analyst who read everything correctly applies 14.7% to the current PR and files 60,000.

## Fix
`solution`: regenerate the Final Recommendation sentence that quotes 73,000 for the "whole DC-side decline restored" path (my reproduction gives about 74,000). Optionally state the wear as 13.8% or 14% consistently. Prompt and input files unchanged. Optional hardening: none needed.
