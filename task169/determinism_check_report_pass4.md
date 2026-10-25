# Verdict: task169 (round 5)

Order kept: yes. blind_derivation.md was written to disk before graded_blocks.md was opened. Caveat on the blind pass: the three workbook tables matched the golden to the unit, but my main-call figure (10 per cent) was WRONG against the golden (20). I missed that every arrest the Board revoked on was nolle prossed, so the court record has no outcome for it. That miss is evidence for the task's stump power, and is discussed under Stump power. After opening the blocks I re-derived the 20 independently from the bundle (below).

- **Verdict:** DETERMINISTIC
- **Disposition:** APPROVE. No repair needed; no rerun. Two optional, non-blocking notes under Fix.
- **Why:** The call is forced by the methodology PDF plus the data. Section 4.1 says the cohort is out of custody for all 730 days and section 4.2 says a return is a new court commitment. Those two lines fix the estimand. The data then force the estimator. Arrests almost never occur in custody (0.36 per cent of arrests fall in a custody interval), and all 9,410 arrests the Board revoked on (to 30 June 2024) were nolle prossed in aoc_case_dispositions, against 374 of 15,707 for the rest. The court's own DOC-sentence rate (22.1 per cent: felony A-B 62.5, C-E 26.1, misdemeanour 2.8) holds on arrests made after maximum expiration, where the Board could not revoke (2,357 of 10,576, same grade rates). So expected returns are all arrests, times the court rate, over all 730 days. That gives about 20 per cent, and 20 is the nearest multiple of five.

## Evidence (recomputed from the bundle)
| Item | Golden | Mine | Reproduced |
|---|---|---|---|
| Cohort | 6,466 | 6,466 (doc_projected_releases_2027.csv, one row each) | yes |
| Fully observed releases (PAR/RPR incl. legacy codes, to 2024-09-30) | 30,959 | 30,959 | yes |
| Arrests linked to a release, to 2024-06-30 | 25,117 | 25,117 (sbi + crosswalk with hyphen fix, latest docket entry) | yes |
| Revoked-on arrests, all NP | 9,410 of 9,410; others 374 of 15,707 | same | yes |
| DOC sentences among the other 15,707 | 3,483 (1,622/2,594; 1,673/6,400; 188/6,713) | same | yes |
| Post-expiry arrests | 2,357 of 10,576 (1,092/1,748; 1,143/4,338; 122/4,490) | same | yes |
| Two-year return rate | 20.4 -> 20 | 19.5 (street-day hazard of all arrests, 1.09 arrests per person over 730 days, times 22.1 per cent, timing-feasibility, 1 - exp(-E)); 19.3 linear | yes, within about 1 pp |
| Table 1 by office (arrest/conditions) | D1 1280/262, D2 622/210, D3 369/172, D4 117/149 | identical | yes |
| Table 2 by district H1/H2 | 34,613/35,500; 21,409/23,962; 17,928/19,163; 10,241/10,611 | identical (per jail also computed) | yes |
| Table 3 by institution H1/H2 | KTR 3,443/4,237; FNW 3,838/4,166; DNM 3,896/4,122; LKV 3,957/4,546; BRW 3,947/4,497 | identical | yes |

Competing answers tested, with the rate each gives and the reason it fails:
- All returns of every kind, about 52 per cent -> 50. The Act removes the recommitments.
- NC admissions as the first return, about 6 per cent -> 5.
- Any NC admission in 730 days on fully observed releases, 8.7 per cent (standardised 8.8) -> 10. This is the record's court rate, which only counts arrests the Board left to the courts.
- Court-route counterfactual using only existing DOC sentences, 9.0 per cent -> 10.
- Exposure-adjusted but still excluding revoked-on arrests, 11.3 per cent -> 10. All three of these omit the revoked-on arrests.
- Count every arrest at the court rate but do not extend exposure over custody days, 16.1 per cent (person-level, timing-feasible) to 19.3 per cent (expected-returns, linear) -> 15 or 20. This route straddles the 17.5 line. Methodology 4.1 ("out of Department custody ... for all 730 days") plus the near-zero arrest-in-custody rate pin the exposure extension, so this is not a licensed alternative, but it is the closest rival.
- Pooling releases of 2025-26 without the right-censoring cut pulls the NC share to 4-6 per cent -> 5.
Residual margin: exposure-adjusted estimates are 19.5-20.4, about 2 pp inside the 17.5 and 22.5 edges. Thin-but-clean, not contested.

Forks on the supplementary answers (none changes a golden figure under the natural reading):
- Table 1, hearing with two cases where one cites an arrest: "any case cites an arrest" is golden; "all cases" would give D1 1216/326, D2 596/236, D3 352/189, D4 114/152. "Conditions alone" literally means no arrest was taken up, so "any" is the literal reading. Not filed in a document; closed only by that wording.
- Table 1, 27 legacy REVOKE rows (dated 5-23 Jan 2026) whose carried-over case is blank/open in board_case_decisions_2026.csv: counted in the golden. Excluding them gives D1 1270/260, D2 616/207, D3 367/170, D4 116/148. The bundle settles it: each has a PAROLE VIOLATOR admission 1-14 days later (doc_admission_movements), and open new-system cases almost never have a hold_end. Derivable from the files, but the prompt/dictionary never says which system wins; a solver who treats the blank as authoritative is not irrational.
- Table 2, layout "county jails of each parole district": golden is one row per district. Per-jail figures sum to it. Overlapping detainers merged (parolee-days) is forced by the wording; unmerged would be +3 per cent.
- Rounding "to a multiple of five" assumed nearest. Floor would turn 19.5 into 15, but floor is an unusual reading.

## Files/Hygiene: PASS
16 files: CSV x8 (manifest included), XLSX x3, PDF x3, Parquet x1. Largest 108,609 rows. Distractors: PRAT validation study, parole caseload file, capacity workbook, vital-records matches (the last plausibly relevant to deaths). Manifest and dictionary read like system exports. No README or "synthetic" disclosure. Dates coherent (extracts 2-9 Oct 2026, methodology 14 Oct, data to 30 Sep). Keys carry realistic mess: hyphen in the crosswalk, legacy code renames in 2022, migration reset of hold_start for 450 carried-over cases, mixed-date types. Nothing exclusion-level. One leak note: methodology 4.1/4.2 hands over the Act's reading (new commitments only, out for 730 days). That removes the easy-route-50 trap but does not state the court-rate counterfactual, so it does not pre-answer the stump.

## Stump power
Good. The surface route a strong analyst reaches after reading the Act (count NEW COMMITMENT admissions within 730 days, with or without censoring care) lands on 5 or 10, and I did exactly that on the blind pass (10). The trap is that Board custody masks the court outcome: arrests the Board revoked on were uniformly nolle prossed, so the NC record undercounts what the courts would do once the Board cannot recommit. A competent solver can see it (the 100 per cent NP column against 2.4 per cent for others, and the post-expiry check), but the easy route files a wrong answer. A second layer is the exposure (custody days) adjustment that separates 15 from 20. I expect the leading models to be stumped by a valid analytical error rather than interpretation.

## Stumping type
`mechanism: forecasting` (with competing-risk / selection structure), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The reported record is correct; the difficulty is a counterfactual regime change (the Act) projected through the arrest-to-court pipeline with the Board-masked outcomes and exposure properly modelled, which survives clean data.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Domain: a corrections population projection of return-to-custody under a statute change (swap-test: "hospital readmission under a payer rule" would change every noun and the method); Layer 1 is the legacy-to-new system migration, code renames, SBI/DOC key formats, overlapping holds and writs; Layer 2 is competing-risk / selection correction and exposure-based counterfactual return rate. Easy route: file the record's new-commitment rate (8.7 per cent, 10) or the all-returns rate (about 52, 50); the golden is 20.

## Fix
none required. Optional, no rerun if done in the solution/metadata only: (a) state in the dictionary or notes which system governs for carried-over cases whose new-file decision is blank (to retire the 27-row fork on Table 1); (b) state "arrest counts if any case in the order cites one" so the mixed-group rule is not left to wording. Both change what solvers see, so a rerun would follow if applied to the prompt or data; leave them if prior runs matter.

Gate summary: A pass (all figures and three tables reproduce); B pass (every decisive fact in the shipped files); C pass with the noted minor Table 1 forks and thin-but-clean margin on the main call; D pass; E pass (prompt names a single share and three tables; rounding direction is the only loose end); F strong; G pass; H pass.
