# determinism-check report, task263 (pass 4, ask rework: people ask cut, water ask re-sited and widened), 2026-11-02

## Verdict
NOT_DETERMINISTIC (the main call, grants and funding order are forced; the 16 water figures of ask 5 are not)
**Disposition:** SEND_BACK
**Stumping type:** mechanism: decomposition_attribution, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Judge: one isolated sonnet thread over a fresh unzip of target.zip (md5 2c87c47f08be016430c82fed5ccc13ad). Failure type recorded by the thread: answer_contradicts_files (water ask only; Gates A/B/C/E on supplementary ask 5).

## Why
The golden's water figures (Granlund 295.1/342.9/396.0/309.6 and the other three counties) reproduce only if the wellhouse meters of Torvik W1 (20275), Halvorsen W1 (20634), Lindvik Lake W1 (20300) and Elvholm Falls W2 (20538) are netted, in all twelve months, of W2 (20281), W2 (20639), W2 (20306) and W3 (20544). No file says those wells are piped into those wellhouses. The register (source_meter_register_2026.csv) lists each of these meters as "wellhouse discharge" for the single facility_id, the inventory has no piping or "fed from" field, the IUP and sampling guide are silent, and the prompt asks for water "the listed systems' wells pumped". Read literally, each well's line is its volume_gal as written. Even a solver who infers the piping from the lead months gets a different answer from the golden, because the evidence (line over rated capacity times days in service) exists only in the 21 lead months, not in the other 27 months where the golden also subtracts.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Samples, listed systems, 2024-2025 RT/CO | 302 at 24 entry points | 305 at 24, 302 after the 3 with no recorded sources | yes |
| Wells over 4.0 ng/L (PFOA or PFOS) | 23 of 53 | 23 of 53, per-entry-point least squares, full rank; over-line wells at 5.05+ on one analyte, under-line wells top out at 2.39 | yes |
| Mixing weights | rated capacity | ep_flow_gpm / sum of listed wells' rated capacity runs 0.95 to 1.06 (mean 1.00); pumps constant speed | yes |
| Grants (20) | per golden, cap 6,000,000 | match to the dollar (Halvorsen at the cap) | yes |
| Systems reached / first not reached / left | 16 / Nordvold / 451,200 | 16 / Nordvold (691,200) / 451,200 | yes |
| Table 6-1 county vs register county | agree | agree for all 20 | yes |
| Water, Granlund Q1-Q4 | 295.1 342.9 396.0 309.6 | reading B (netted all 12 months): same; reading A (as written): 332.5 419.6 446.8 387.4; reading F (netted 21 lead months): 297.8 345.5 400.3 310.2 | B only |
| Water, Engvall Q1-Q4 | 285.7 336.6 396.3 299.7 | B: same; A: 319.6 377.6 446.1 334.6; F: 288.7 342.8 404.2 302.0 | B only |
| Water, Hedstrom Q1-Q4 | 197.2 235.6 269.1 211.6 | B: same; A: 218.9 258.5 297.4 233.7; F: 199.4 239.8 274.1 214.4 | B only |
| Water, Sandholm Q1-Q4 | 154.6 182.4 211.7 165.8 | B: same; A: 169.5 199.4 235.9 183.1; F: 155.6 184.3 214.7 167.1 | B only |

All 16 golden figures reproduce under B. All 16 differ from A by 15 to 78 MG and from F by 1.0 to 6.5 MG, so every cell moves at the one-decimal grain.

## Competing answers that survived
1. Wellhouse meters (the one genuine fork): A (each meter line as written, which the files force on a literal reading) vs F (netted only in the 21 months the line exceeds rated capacity times days) vs B (golden, netted in all 12 months). No shipped sentence closes it; the golden's own justification covers only the lead months. A solver who spots the over-capacity lines will most naturally file F or A, not B.
2. Minor, not a fork the thread counted against the ask: Kesselring Well 3 (Emergency, 20079, 799,270 gal) is included by the prompt's "wells" (Hedstrom Q3 +0.8 MG if included); excluding it is not licensed by the prompt.

Closed by shipped files (one reading each, per the thread):
- Skogen common header M-100858 (facility_ids 20125;20130): the register gives one meter for both wells, so counted once; counting both rows would add 35.2, 42.5, 50.1, 38.6 MG to Hedstrom Q1-Q4. The rule is carried only by the register.
- Interconnection (Ackerholt Creek 20899, 2,665,616 gal): facility_type Interconnection, not a well, excluded (including it adds 2.6 MG to Granlund Q3).
- Treatment plants: none belong to listed systems.
- Fjelstad Well 2 meter swap (M-100525 to M-100551, 2025-06-12): meter_end minus meter_start is -206 MG for June; volume_gal is correct. Layer 1 mess, one reading when volume_gal is used.
- Quarter boundary: the only period field is report_month (2025-01 to 2025-12), no read date; the IUP's fiscal years concern the capitalization grants. Calendar quarter of report_month is the one reading; no second basis exists.
- County: Table 6-1 and the register agree for all 20 systems.
- Every listed facility has exactly 12 report rows, no duplicate (facility, month).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / large file | 10+ / 3+ / 25,000 rows | 12 / csv x9, xlsx, pdf x2 / 36,414 rows | yes |
| Distractors | 2+ in metadata.json, none labelled in a file name | 4 named (national_pfas_survey_2023, private_well_pfas_2024-2026, community_water_system_register_2026, wholesale_connections_2026); no file name labels one | yes |
| Distractor unused yet weighable | | wholesale_connections_2026.csv not needed for any figure (thread); register mostly an aid | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png) | yes |
| Asks multi-dimensional with unit and rounding | | water ask 16 cells, unit and rounding in the sentence; the asks are decoupled but ask 5 is not determinate | no (determinism, not shape) |
| Prompt shape, 25+ criteria, reads human | | not re-verified this pass (prompt call sentence unchanged; thread found no authoring language) | not re-checked |

## Gate G reconciliation
Thread: mechanism decomposition_attribution, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no; Gate G passes (shipped samples correct, difficulty is unmixing entry-point samples). The design note's Layer 2 reads "the decomposition and attribution family" with the same decisive step (inverting the mixtures); no mismatch. The thread did not name a declared distractor as the surface read. The water ask's wellhouse device is unfiled and so adds an unforced fork, not stump power.
Gate H line: domain: pass, layers: pass, decisive_step: analytical (Layer 1 is the multi-format mess, a meter swap and a common header; Layer 2 is source apportionment of entry-point samples to wells; the easy average gives 7 systems against the true 16).

## Stump power (Gate F)
Good on the main call. Averaging each well's samples, flow-share weighting or using samples run alone yields 7, 8 or 11 funded systems against 16, as the recommendation itself states; a strong analyst who reads every rule correctly still files a wrong count unless they unmix the entry-point samples. The water ask carries a silent device in the wellhouse meters, but unfiled it is a fork.

## Findings, ranked
1. Ask 5, wellhouse meters: the netting of Torvik W1, Halvorsen W1, Lindvik Lake W1 and Elvholm Falls W2 against W2, W2, W2 and W3 is in no shipped file; literal reading A and the evidence-based reading F both differ from the golden in all 16 cells. SEND_BACK.
2. Skogen common header counted once rests on the register line alone (settled, noted).
3. Kesselring Well 3 (Emergency) included by "wells" (one cell, 0.8 MG; minor).
Main call, grants, funding order and the 16-of-20 reach are determinate.

## Next action for the author
Fix: input_files, for the water ask. File in the pack which meters also carry another well's water, in a form the solver can read without inferring it (for example a register column or note that meter M-101427, Torvik Well 1's wellhouse, also passes Well 2's flow, and likewise M-102625, M-101498 and M-102360), and file that every month's reading is gross of it, so F is no longer defensible. Keep the files otherwise as they are. Alternative: rebuild the golden to reading A (plain sums of volume_gal, header meter once), which the files already force. Re-run all 16 cells after the repair; the changed pack needs a rerun of the judge.
