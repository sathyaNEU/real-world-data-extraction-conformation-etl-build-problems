# Determinism check, task468 architecture 4, pass 1 (target.zip b1bc148c)

One isolated judge thread (sonnet, medium) on a fresh unzip, 2026-10-20; its verdict file follows as returned. Architecture 2's report (target.zip f9f35f57b4293ef0, DETERMINISTIC and APPROVE) and the architecture 1 reports are in git history (26e34e23 and earlier). Pass 2, the single re-judge on the fix-pass bundle (target.zip f511b179e6742bf8), is determinism_check_report_pass2.md.

# Determinism verdict, task468 (Halbrook 2027 Hospital Quality Bonus)

- **Verdict:** DETERMINISTIC, SOLUTION_WRONG (minor: three reported figures do not reproduce to the decimal; no call moves).
- **Disposition:** FIX_NOW. Restate Calloway (189.5 deaths), Varden (24.3) and Fairhaven (1.05) in the solution blocks, and pin the replacement-payment convention in `hchp_ip_claims_extract_notes.pdf` (see Fork 2). No change to the main stump. Rerun not required if only the pin is added; a solver-visible note edit is the only shipped-file change.

## Why
The decision is forced once the estimand is read as true deaths among index admissions. The spec says the member "died" (3.1), and the OVR methods note says outright that some deaths are missed and some links are false. Both error rates are measurable from the shipped files: recorded deaths give sensitivity, and members seen alive after day 30 give the false-link rate. Every full correction I tried (pool-conditioned Rogan-Gladen, all-admission Rogan-Gladen, space-only or space-or-hyphen two-part class, service-line-only or all alive evidence) gives the same five losers: Brannock, Calloway, Mercy Valley, Northgate and Westover. The task is not unambiguous on one point. The prompt and spec never say to correct for linkage error, and the literal "bills plus OVR links" reading gives a different set (Fork 1). I judge that a competent expert is pushed to the correction by the OVR note and the measurable error rates, so I do not fail Gate C. This is the residual risk of the build.

## Evidence (recomputed from `target/` only)
| Item | Result | Reproduced |
|---|---|---|
| Conformed stays (last corrected, voids dropped, Carrisford mapped via enrollment, both Mercy NPIs) | 59,897 bill stays + 13,311 encounter stays | yes |
| Index admissions (adult, non-delivery DRG, not status 07, first per member, transfer joined to the first hospital) | 34,500 | yes, exact |
| Recorded deaths | 1,046 (836 SSN, 48 single surname, 162 two-part) | yes |
| Class linkage, recorded deaths linked | 829/836, 44/48, 78/162 | yes, exact |
| Class linkage, living members linked | 12/21,855, 20/1,179, 8/1,554 | yes, exact (two-part = space or hyphen in `last_name`; SSN = `ssn_last4` present) |
| Brannock | 84.9 / 67.85 = 1.251 | yes |
| Mercy Valley | 502.2 / 387.08 = 1.297 | yes |
| Northgate | 189.3 / 122.18 = 1.549 | yes |
| Westover | 260.3 / 179.92 = 1.447 | yes |
| Calloway | 189.47 / 143.75 = 1.318 | golden says 189.8 (off 0.3, same ratio to 2 dp) |
| Varden | 24.26 / 25.61 = 0.948 | golden says 24.5, ratio 0.96 (still below 1.15) |
| Fairhaven (highest keeper) | 1.052 | golden says 1.06 |
| Bonus per hospital to nearest $100, and total $7,063,400 | all 14 match exactly | yes, only under the CPS-delta / platform-full convention (Fork 2) |

Resampling the class rates (4,000 draws) gives P(ratio > 1.15) of 0.99 for Brannock, 1.00 for Mercy Valley, 0.08 for Varden and 0.00 for Fairhaven. Brannock is the thinnest loser. Its 2.5th percentile is 1.167, and it falls to 1.17 under the narrowest alive-evidence definition (admissions and live discharges only). It stays over the line under every full correction.

**Fork 1: whether and how to correct the linkage (main call, Gates C and E).**
- Bills plus OVR links, uncorrected: Brannock 1.06, Mercy Valley 1.06, Varden 1.88. Loses 4: Calloway, Northgate, Varden, Westover.
- The same with contradicted links dropped and later-bill deaths added: still those 4. This is the path the golden itself rejects.
- Full two-sided correction by class: the golden's 5.
- One-sided corrections do not match:
  - Missed deaths only: 3 lose.
  - False links only: 6 lose, with Varden added.
- No class split: Calloway, Northgate, Varden, Westover.
- Hyphen-only for "two-part": Brannock keeps and Varden loses.
- The classes the data separate are SSN, single surname, and compound (space or hyphen). Hyphen-only is not a reasonable reading, because space-separated compounds are 3,166 of about 3,620 and carry the same low sensitivity.
- The prompt and spec do not file the correction. The OVR note and the measurable rates make it the expert route, but a literal reader who stops at spec 3.3 files 4 and gets Varden wrong. Residual Gate C and E risk is moderate, and I do not fail on it.

**Fork 2: payment convention (asks 2 and 3, Gates B and E).**
- The notes say only "amount Halbrook paid on the bill". No file states that a CPS (13-digit) replacement carries the change while a platform replacement carries the full amount.
- The data shows it: 63% of CPS replacements are negative, none of the platform ones are, and platform replacements run about 0.8 times the original.
- Network total under each convention: golden $7,063,400; all replacements as change $7,622,100; all replacements as full $6,874,700; originals only $7,359,600.
- It is inferable but unfiled. The pin is a one-line note in the extract notes.

## Files/Hygiene
- **Result:** PASS with FIX_NOW items. Nothing is exclusion-level.
- **Inventory:** 13 files in 4 formats: 5 csv, 1 pipe-delimited txt, 5 pdf, 2 xlsx. Largest files are the 65k-row claims extract, the 324k-row service lines and the 70k-row enrollment.
- **Distractors:** the readmissions dashboard xlsx and the hospital profiles pdf are both unused by the solution.
- **Temporal:** `CMG_HCHP_IP_ENC_20261006.txt` has a creation date of 10/06/26 in its header but contains a submit date of 10/10/26. The record is a FY2027 stay, so it is outside the measure. Fix the date.
- **LLM-tell:** hospital FY2026 payment totals sit within about $60 of round $50k values (for example 19,564,929.99 and 12,349,943.04). That reads as calibrated synthetic data. Add noise so totals are not near-round.
- **Other:** no authoring or provenance leakage found. Cross-batch check not performed (out of the allowed read scope).

## Stump power
Gate F is good. The surface route is the OVR links plus the bills (or the individual-repair path of dropping contradicted links and adding later-bill deaths). It looks complete, and it files Varden as a loser while missing Brannock and Mercy Valley. The trap is estimating the linkage-error structure by identifier class and applying it to the unobserved admissions, not a defect catch. Strong models may stop at the individual repair, and partial corrections give 3 or 6 losers. Hold, 4 or 5 are all live outcomes, so I expect real stumps.

## Stumping type
`mechanism: statistical_rigor` (measurement-error correction, with ETL conformance under it), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.
The OVR return and the bills are honest, with documented error. The difficulty is estimating the true death count from a known misclassification, and it persists on clean data. It is borderline only in that the uncorrected link count is a "reported read" the solver must not accept as complete.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`.
- **Domain:** observed-over-expected mortality with a model-based expected count, and linkage-error correction, are core health-quality and epidemiology work.
- **Layer 1:** CPS to platform claims change, delta versus full replacement bills, a Mercy Valley NPI change, delegated-group encounters keyed by another member number, transfers, and a preliminary and revised bill chain.
- **Layer 2:** correcting death ascertainment by identifier class.
- **Easy route:** a strong analyst who cleaned everything and read every rule would take bills plus OVR links, even with later-claim repairs. That gives 4 losers, Varden in and Brannock and Mercy Valley out. The gold is 5.

## Fix
- **solution:** correct Calloway 189.8 to 189.5, Varden 24.5 to 24.3 and Fairhaven 1.06 to 1.05. Align SOLUTION_STEPS step 6 with the estimator as run.
- **input_files:** add one line to `hchp_ip_claims_extract_notes.pdf`: a 0117 replacement carrying a CPS number shows the change in payment; one carrying a platform number shows the full amount.
- **input_files:** fix the encounter file's header creation date, and perturb the near-round hospital payment totals.
- **prompt (optional):** a clause such as "the deaths of the members, as best the record shows" would close Fork 1 without naming the method.
