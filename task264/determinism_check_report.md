# task264 determinism check (architecture 3)

Two isolated judge passes, each a Sonnet thread at medium effort that saw only a fresh unzip of target.zip, the prompt and the judge's system prompt, and opened the graded blocks only after its own derivation was on disk.

| Round | Pack | Verdict | Disposition | Action |
|---|---|---|---|---|
| 1 | d990a19c | NOT_DETERMINISTIC on supplementary item 4 only (order kept; main call forced; F good; G PASS; H PASS) | SEND_BACK as labelled, an ask-layer repair by the gate table | policy section 6 counts every pre-operative questionnaire the supplier received for the operation whether or not it carries an NHS number; questionnaires without one come only from bookings that went ahead on the day and each matches exactly one operation under every attachment rule; the export stamps made to agree with their contents |
| 2 | 44c981bc | DETERMINISTIC (order kept; F likely high; G PASS; H PASS) | APPROVE | none |

The round-1 leak reader's question 6 (rule application) against the judge's Gate H (analytical) is resolved by the measurement: averaging the returners, filling by case-mix or setting missing scores to expected files seven providers, conditioning on the readmissions found as later spells files the five; the round-2 reader saw the missing-outcome handling as the analytical choice.

---

# Determinism check, round 1 (2026-11-01): NOT_DETERMINISTIC on supplementary item 4 only, SEND_BACK as labelled; order kept; main call forced; Gate F good; Gate G PASS; Gate H PASS

Read against the gate table: a Gate C failure confined to a supplementary ask with the main call forced and G and H passing is an ask-layer repair that spends no architecture. The leak reader's question 6 (rule application) against the judge's Gate H (analytical) is resolved by the measurement: averaging the returners, filling by case-mix or setting missing scores to expected files seven providers; conditioning on the readmissions found as later spells files the five. Isolated thread, Sonnet at medium effort, on target.zip d990a19c.

# Verdict, task264 (round 1)

ORDER: kept. derivation.md was written to disk (own outcomes, allocation, waiting list, participation, forks) before graded_blocks.md was opened.

- **Verdict:** NOT_DETERMINISTIC (one supplementary answer only; the main recommendation, the outcomes and the waiting-list figures are forced).
- **Disposition:** SEND_BACK. File in the policy (s6) or prompt how a questionnaire with no NHS number is attributed to an operation (or build the pack so the attribution is not needed); the main call, the stump and every other graded figure stay frozen, but the policy PDF solvers read changes, so a rerun is required.
- **Why:** Deliverable-file item 4 (2025-26 participation, ten whole-per-cent figures) holds only under an unfiled linkage. Policy s6 says "whose patient completed a scored pre-operative questionnaire"; 511 csv questionnaires (326 for 2025-26 operations) carry "No NHS number supplied" in mossgill_nhs_number_link_2026-09.csv and no sentence or file says how they are attributed. The golden attaches each to "the unlinked operation at its site with the same sex and a birth year the age allows, nearest its booked date" (no gap cap, pool = operations lacking a linked questionnaire); that exact method reproduces the golden's figures (Penderwick 81, Cragsmoor 85, Gorsedene 84, Hethercombe 80, Ormsbrook 81, Oxlade 84, Ravensholt 84, Shelderwick 81, Tannerbrook 81, Thistledene 80), while the literal NHS-number-only reading gives (Penderwick 75, Cragsmoor 80, Gorsedene 78, Hethercombe 73, Ormsbrook 75, Oxlade 79, Ravensholt 78, Shelderwick 75, Tannerbrook 74, Thistledene 75). Gates failed: A/C/E for supplementary item 4. Taxonomy: answer_contradicts_files (golden rests on an unstated linkage method; the literal reading differs by 3 to 7 points on every provider).
- **Evidence (recomputed from target/):**

| Item | Reproduced? | Source |
|---|---|---|
| Index ops 2023-04..2025-03: 9,901 (dedup patient+provider+admission date, 41355 folded into 41477) | yes | apc spells, provider_reference |
| Eligible 8,150; with scored M12 (336-448 d) 5,208 | yes (CC1) | xlsx + csv PROMs, link file, deaths |
| National expected change 16.85 | yes | Appendix B |
| 1,041 operations with emergency admission (methods 21,22,23,24,28) within 90 d of discharge; response 33% vs 68%; returned residual -17.5 | yes (CC2) | APC later spells + PROMs |
| Outcomes (provider x readmission-status fill, global mean over all eligible): 17.10, 15.93, 15.14, 15.10, 15.01, 13.95, 13.93, 13.06, 12.95, 12.88 -> 17,16,15,15,15,14,14,13,13,13 | yes (CC3) | as above |
| Placement: Hethercombe 180, Cragsmoor 150, Shelderwick 260, Ravensholt 210, Penderwick 110 = 910, held 340 | yes (CC4) | capacity returns xlsx |
| Waiting list 31 Mar 2026 (2,588 patients after counting 15 transfers once at the receiver, original clocks, triage-received clocks via routed_to+birth year+sex+postcode+practice, outcome date 0-7 d before receipt, unique 1,430/1,430; 56/56 transfer origins found): >52w 5,3,20,11,25,27,50,25,18,4; share <=18w 56,46,31,56,54,50,33,49,55,54 | yes, all 20 figures | ptl month-end, removals, msk json |
| Participation, NHS-number link only | by provider code 40117..41477: 78,80,78,75,73,75,79,75,74,75 (does NOT match golden) | |
| Participation, golden's nearest-booked-date attribution | by provider code order 40117,40152,40188,41206,41231,41274,41309,41388,41402,41477: 84,85,84,81,80,81,84,80,81,81; matches golden exactly | |
| Participation, exact-date or +-7 day attribution | 84,84,84,81,79,81,84,79,81,81 (Cragsmoor 84 vs 85, Hethercombe 79 vs 80, Thistledene 79 vs 80) | |

  Main-call robustness (Gate C, passes): allocation identical (the five providers, 910/340) under readmission windows 30/60/90/180/365 d, with or without admission method 81, measured from discharge or operation, within-provider post-stratification, logistic IPW (readmission only, full covariates, with provider interactions) and outcome-regression imputation; margins to the 14.5 floor are 0.5 or more (Thistledene 13.95, Ormsbrook 13.93; Penderwick 14.94 to 15.18). Whole-point outcomes are stable across those variants (borderline only 41477 at 14.94 to 15.18 and 41274 at 13.70 to 14.00, both round the same way except 41274 under one IPW at 13.70 which rounds to 14). Responders-only (the easy route) gives 1,250 placed across seven providers (Ormsbrook 240, Thistledene 170, Penderwick 40), a clearly different answer, so the non-response step is the decider.
  Minor unfiled points that do not move any graded figure: spell identity under "latest submission" (spell_id is new on each resubmission; keyed patient+provider+admission date; three keys give the same allocation); 365-day lookback is vacuous in the data (0 repeats); csv symptom-duration codes unlabeled but never feed an eligible operation; the 0-7 day triage link window is not filed (any window 0-10 gives the same unique link; 7 GP/Consultant rows coincidentally match a triage record and are correctly left on their provider-received clock).
- **Files/Hygiene:** PASS with minor in-house items. 14 files, formats csv, xlsx, json, pdf; apc file 30,883 rows; distractors present (fft, cqc, code_lookup, revisional/other-procedure spells). Findings (non-stump, FIX_NOW): msk_triage json header extract_run 2026-04-14 but outcome_date runs to 2026-06-01 (temporal incoherence, outcome_date is used only to link and not graded); apc sus_submitted runs to 2026-10-02 against files labelled 2026-09 and a capacity return refreshed 29/09/2026. No authoring disclosure, no README, nothing exclusion-level. Cross-batch check: no prior packages supplied, none run.
- **Stump power (Gate F):** Good. The deciding step is informative non-response: 36% of eligible operations have no 12-month score and the shortfall is concentrated in patients readmitted as an emergency, who also do 17.5 points worse than the case-mix expects; a solver who averages the returners (or weights on the Appendix B covariates, age and provider) files a seven-provider 1,250 placement, and reaching 910/340 needs the join from the lumbar cohort to the patients' later emergency spells. The cue is the policy's "whether or not the patient returned" and the non-lumbar spells in the cohort extract; strong models that test response against the APC history will find it, those that do not will file the wrong call. Ask layer (rebuilt waiting list with triage-start clocks, transfer de-duplication) is hard and fully filed.
- **Stumping type:** `mechanism: statistical_rigor`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. No reported number is overturned (nothing in the pack ranks the providers); the difficulty is correct handling of non-ignorable missing outcomes, a FINE-numbers shape that passes Gate G. (Borderline on the clean-data test only in the trivial sense that full response would remove the issue; the missingness is real structure, not a planted defect.)
- **Three rules (Gate H):** `domain: pass`, `layers: pass`, `decisive_step: analytical`. Layer 1: two PROM deliveries in different layouts (xlsx items, csv totals), predecessor code 41355 to 41477, NHS-number link with gaps, resubmitted spells, triage-versus-provider clocks, late-recorded transfers. Layer 2: provider outcome after case-mix adjustment with missing-not-at-random follow-up handled through readmission status (the field's own PROMs analysis; swap test fails to survive "hospital/visits" nouns). The easy route, a strong analyst who cleans everything and reads every rule right then averages the returners, files Ormsbrook 240, Thistledene 170 and Penderwick 40 on top of the five (1,250 placed, none held).
- **Fix:** prompt or policy (input_files: spinal_contracting_policy_2027-28.pdf s6, or the prompt). File the WHAT for questionnaires without an NHS number (state that they are attributed to an operation, or state they are not counted), with the attribution rule if they are (site, sex, birth year allowed by age on admission, nearest to the operation date, each operation at most once), then assert it in checks and the participation figures. Optionally align the triage json extract_run with its outcome dates. Do not touch the main call, the readmission mechanism or the other nineteen deliverable figures (all reproduced).


---

# Determinism check, round 2 (2026-11-01): DETERMINISTIC, APPROVE; order kept; Gate F likely high; Gate G PASS; Gate H PASS

The re-judge after round 1's participation repair, on target.zip 44c981bc. Isolated thread, Sonnet at medium effort.

# Verdict (task264 r2)

Order kept: yes. derivation.md was written to disk before graded_blocks.md was opened.

- **Verdict:** DETERMINISTIC
- **Disposition:** APPROVE. No repair is needed and no model rerun is needed. The advisory items below are optional.
- **Why:** The golden (five providers, 910 placed, 340 held) is forced by the data. The policy fixes the population as every eligible index operation "whether or not the patient returned" the 12-month questionnaire. Non-response in the data is not ignorable: it is driven by an emergency readmission within 90 days of discharge, which sits in the APC extract. It is 33% response against 68%, with answerers 17.5 points below expectation. I rebuilt the golden independently. Every estimator that uses the readmission variable gives the same set above 14.5. These were provider-by-readmission cells, an additive model, response-probability weighting (logistic and cell-based) and a national readmission-effect weighting, tried with readmission windows of 30, 60, 90, 180 and 365 days. The easy route, the provider mean over returners only, gives seven providers and 1,250 placed. No gate A to E failure.

## Evidence (recomputed from target/)
| Item | Mine | Golden | Reproduced |
|---|---|---|---|
| Index ops 1 Apr 2023 to 31 Mar 2025 (after dedup on patient, provider, admission date, latest sus_submitted) | 9,901 | - | n/a |
| Eligible ops | 8,150 | 8,150 | yes |
| Eligible ops with scored 12-month questionnaire at 336 to 448 days | 5,208 | 5,208 | yes |
| Grand mean expected change | 16.85 | 16.85 | yes |
| Readmitted ops | 1,041 | 1,041 | yes |
| Response, readmitted against not | 33% / 68% | 33% / 68% | yes |
| Answerers' change against expectation, readmitted | -17.5 | -17.5 | yes |
| Outcomes under provider-by-readmission imputation: Hethercombe, Cragsmoor, Shelderwick, Ravensholt, Corriemoor, Thistledene, Ormsbrook, Oxlade, Tannerbrook, Gorsedene | 17.10, 15.93, 15.14, 15.10, 15.01, 13.95, 13.93, 13.06, 12.95, 12.88 | 17, 16, 15, 15, 15, 14, 14, 13, 13, 13 | yes, all whole points |
| Placement | 180+150+260+210+110 = 910 of 1,250; 340 held | same | yes |
| Waiting list at 31 Mar 2026: 2,603 PTL rows less 15 origin pathways of transfers made on or before 31 Mar but recorded late | 2,588 | - | n/a |
| Over 52 weeks, then share within 18 weeks, per provider | Corriemoor 5, 56%; Cragsmoor 3, 46%; Gorsedene 20, 31%; Hethercombe 11, 56%; Ormsbrook 25, 54%; Oxlade 27, 50%; Ravensholt 50, 33%; Shelderwick 25, 49%; Tannerbrook 18, 55%; Thistledene 4, 54% | same | yes, all 10 providers |
| FY2025-26 participation | Corriemoor 81, Cragsmoor 85, Gorsedene 84, Hethercombe 80, Ormsbrook 81, Oxlade 84, Ravensholt 84, Shelderwick 81, Tannerbrook 81, Thistledene 80 | same | yes, all 10 providers |

- **Waiting-list clock:** the PTL clock start equals the provider's receipt date everywhere. The policy needs the MSK triage receipt date for triaged patients, and the original clock for transferred patients. No shared key exists. The match on birth year, sex, postcode district, practice, routed-to site and the nearest prior outcome date (1 to 6 days before provider receipt, next candidate at least 19 days earlier) is unique for all 1,430 triage-route rows. Clock-as-filed in the PTL gives different counts, for example Cragsmoor 0 over 52 weeks against 3.
- **Participation:** a linked questionnaire whose booked date differs from the procedure date (about 11%) must be joined on NHS number and tested against the procedure date. This gives 4,112 of 5,331. Questionnaires without an NHS number (383) match on site, sex, birth year and booked date. The booked date equals the procedure date for all of them, so the match is unique. They add 270 more.
- **Competing answers tested:**
  - Returners-only, the easy route: 7 providers, 1,250 placed. It is wrong, because response is non-ignorable once readmission is considered.
  - National readmission-stratum imputation that ignores provider level: Shelderwick falls to 14.41. This ignores the provider effect the answerers visibly carry, so it is a poor estimator. The data reject it, and it does not survive as a defensible alternative.
  - Using elective admissions as the readmission flag: 7 providers. It is not the driver.
  - Late 12-month returners included: unchanged.
  - Rounded and unrounded values give the same placement.
- **Margins:** the lowest provider above the floor under any sound estimator is 14.92 (Ravensholt). The highest below is 14.09 (Thistledene). The gap is about 0.4 to 0.6 points and is stable across methods, so this is a thin-but-clean gap. Placement does not depend on order, because the five total 910, which is under 1,250.

## Files/Hygiene: PASS (with advisory notes)
- 14 files in 4 formats: csv ×9, xlsx ×2, json ×2, pdf ×1. apc_spells is 30,768 rows. Distractors present: fft_inpatient, cqc_locations, and the capacity note that returns are not netted against other commissioners.
- No authoring or provenance leakage seen. Dates are coherent (policy 17 Sep 2026, returns Aug to Sep 2026, extracts to Sep 2026).
- Not exclusion-level.
- Advisory, none decisive:
  1. The policy never says how a "spell submitted more than once" is identified. The spell_ids differ, so patient, provider and admission date has to be inferred. Every resubmission pair changes only V253/V254 or the discharge date, so no result moves.
  2. The CSV `symptom_duration` codes 1 to 4 and `odi_raw_score` are undefined in any filed document, but they are not load-bearing. The only questionnaires from the CSV that enter the outcome are 12-month ones, and their ODI totals are consistent with the xlsx.
  3. The CSV column names and the "each provider" row set are not specified. The 10 returning providers are the only ones with an outcome, so there is no real fork.
  4. A solver who orders by whole-point rounded outcomes would tie Ormsbrook, Thistledene and Corriemoor at 16 in the returners-only reading. This does not arise on the golden path.

## Stump power (Gate F)
Likely high. The trap is that the easy provider mean over returners overstates Ormsbrook and Thistledene (about 15.6) and adds them, taking 1,250 placed to seven providers. It needs the solver to test who does not answer, join later emergency admissions from the APC extract, and correct for it. The policy's "whether or not the patient returned" is the only hint. The waiting-list reconstruction (triage clock, transfer clock, double-counted transfers) and the rounded participation figures add further grading load. A strong model could plausibly stop at the returners-only answer.

## Stumping type (Gate G)
`mechanism: statistical_rigor` (non-ignorable non-response), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.
No shipped number or artifact is wrong. The difficulty is a selection-bias correction on honest data, and real non-response is structure, not a planted defect. The waiting-list and participation layers are ETL conformance.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`
- **Domain:** NHS commissioning, case-mix adjusted PROMs, response handling and RTT list reporting. Swapping the nouns breaks it.
- **Layer 1:** a spreadsheet and a CSV delivery with different layouts, NHS-number link gaps, resubmitted spells, a provider code change, booked-date drift, and triage and transfer clock sources.
- **Layer 2:** non-ignorable non-response. The easy route is the returners-only mean. It gives Ormsbrook 16 and Thistledene 16, seven providers and 1,250 placed, against the true five and 910.

## Fix
none. Optional wording only: the policy could name the resubmission identity, but this is not needed.

