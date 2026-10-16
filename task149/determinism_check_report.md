# Verdict (task149 re-judge, fresh)

- **Verdict:** DETERMINISTIC
- **Disposition:** APPROVE. No repair needed; two low-risk residual readings are listed under Evidence for the author's information only. No model rerun.
- **Why:** The main call (about 1,000 recordable cases in FY2027) reproduces end to end from the shipped files, and every graded ask (20 day totals, 20 heavy-pick counts, 5 chart bars) reproduced exactly. The pace-against-engineered-standard fit separates the candidate methods in the data: about 60 deviance points over cases-per-direct-hour at equal parameter count, and a clear out-of-sample margin. Every pace-based construction I tried lands at 982-1,020, which rounds to 1,000 with 50+ cases of room either side. The competing answers (about 800, 840, 890) are the models the history rejects.

## Evidence (all recomputed by me from target/)
| Item | Golden | Mine | Source |
|---|---|---|---|
| Recordable cases, 20 DCs, FY21-25 | 609/623/637/588/661 | 609/623/637/588/661 (FY26 to 11/2: 557) | legacy csv + platform json; non-recordable and "not work-related" removed, the 113 migrated cases counted once via legacy_case_ref, platform UTC read in DC-local time, Rockford 311 to 318 joined |
| Case reconstruction cross-check | n/a | Calendar-year counts tie exactly to ita_form300a for all 300 DC-years | ita_form300a_submissions csv (independent confirmation of local-time and migration handling) |
| Pace, plan vs latest 12 months | about +9% | +8.8% (1.0294 vs 0.9458); per-DC +6.4% to +10.8% | plan Volume and Labor hours, ie standards with site factors on 12/27/2026, wfm direct hours |
| Poisson, DC fixed effects, log hours offset, all 60 DCs, FY21-FY26 wk44 | beta about 2.7, se 0.2, about 60 deviance better than cases/direct hr | beta 2.73, se 0.20; deviance 4728.4 vs 4788.9 (60.5) | pan-built from wfm, wms cases, ie standards |
| Back-test (fit FY21-24, predict FY25-26 to date at actual hours), mean DC miss | 11 / 15 / 21 | 11.1 / 14.7 / 20.6 (pace / cases per direct hr / FY24 rate per hr) | same |
| Forecast | 1,001.8 | 1,001.8 | plan hours and plan pace through the fit |
| Rivals | about 800 / 800 / 900 | rate per hour 817; rate per case 841; rate per std hr 888; cases/direct hr model 841 | |
| Robustness of 1,000 | 982-1,028 | no-trend 1,002; with FY dummies 989; direct-hours exposure 1,002; free hours elasticity 1,007; fit on FY24-26 only 996; program-only fit 982; adding both pace and cases/hr 1,016 | all round to 1,000 |
| Days (20 DCs) | e.g. Groveport 685, Joliet 2 954 | all 20 match exactly | rtw_work_status_log joined to platform case_id; TRANSFER OUT followed to the associate's next file at the new DC; days counted from day after injury, to day before FULL DUTY or SEPARATED effective date, or 10/31, capped at 180 (EHS-RK-01 s9). Platform day fields are stale for open cases; they match my calc for 100% of closed cases, which confirms the convention. |
| Heavy picks (20 DCs) | e.g. Groveport 948,540 | all 20 match exactly | picks parquet joined to the item version in force in each fiscal period (SKU reuse), PORTAL weights in kg x 2.2046, strictly > 50 lb. Conversion factor 2.2 to 2.205 changes no item. A naive current-master join gives 695,699 for Groveport. |
| Chart bars | FY21-25 above, forecast 1,000 | match | |

**Residual readings (low risk, ask-level only, not the main call):**
1. Days: does the SEPARATED effective date count as a day? The golden does not count it (consistent with FULL DUTY; the log defines EFFECTIVE_DATE as the first day of the status, and s9 says the count ends when the associate leaves). Counting it moves 5 DCs by 1-3 days (Groveport 688 vs 685, Lansing 709, York 165, Jackson 402, Sun Prairie 705). The literal text supports the golden reading, but it is one sentence from being fully closed.
2. State to time zone mapping (IN, KY Eastern; IL, TN, TX, WI Central) is general knowledge, not in a file. The ITA tie-out proves the golden mapping is the one the records support, and the main total moves only a few cases under UTC reading.

Nothing else was open: Gate A grain fine (the WFM panel is complete, case file is one row per case), Gate B all decisive facts are shipped (standards, site factors incl. the Lebanon re-study, plan, hours, procedure s7, 8, 9, notes), Gate C only the rejected rivals survive at about 800 to 890, and the near-tie test passes (1,001.8 sits mid-bin, 50 from each edge, every valid pace construction agrees).

## Files/Hygiene: PASS
18 files; formats: pdf (2), csv (8), json, parquet (2), xlsx (3), txt. 25,000+ rows present (wfm 146k, legacy 22.7k plus platform 16k, picks 1.05M). Distractors present and unused: wc_loss_run, bbs_observations, ita (a cross-check only), the plan's indirect hours. No hidden sheets, no authoring or benchmark language in PDFs, txt, or xlsx properties. Dates coherent with a 11/02/2026 pull (plan 10/23, draft agreement 10/29, RTW to 10/31). Fictional company, so no public-data contamination. File names do not name the trap. I could not run the cross-batch fingerprint (other tasks are out of bounds); no duplicate seen within this folder.

## Stump power
Would stump: a strong analyst who cleans everything correctly and files rate-per-hour x planned hours (817, about 800) or a rate per case (841) or per standard hour (888). Nothing in the prompt or in a runbook names pace; the solver has to build standard hours from the IE file, notice that pace rises 9% in the plan, and test it out of sample against cases per hour. Not pre-answered by any shipped document. Honest risk: the aggregate back-test totals barely separate the models (3,497 vs 3,528 vs 3,491 against 3,559 actual) because historical pace moved little, so the separation rests on DC-level miss and deviance, which a hurried solver can skip; that supports difficulty, not a determinism hole.

## Stumping type
`mechanism: forecasting` / `method_or_model_selection`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. All reported numbers are correct; the difficulty is a forward projection the trailing rate does not pin, chosen by out-of-sample validation. On clean data the task still stumps (rate-per-hour still gives 800). Gate G passes; the ETL layer (migration, UTC, renumbering, SKU reuse) is Layer 1 and not decisive.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Swap test: replace "recordable cases" and "pace against engineered labor standards" with another field and the task stops reading the same, because the deciding quantity is an occupational-safety exposure-response model (injury incidence versus work pace, engineered labor standards, OSHA recordkeeping). Layer 1: legacy-to-platform migration with once-only counting, UTC vs local time, Rockford renumber, category code change, kg portal weights, SKU reuse. Layer 2: dose-response of recordable rate on pace, validated out of sample, then carried to the plan's pace. Easy route a strong analyst takes after reading everything correctly: latest-12-month rate per hour on planned hours = about 800 (817).

## Fix
none (fix location: none). Optional wording hygiene: if the author wants the SEPARATED day closed beyond doubt, say in the RTW log notes that the status's first day is not counted; this would not change any graded figure and is not required.
