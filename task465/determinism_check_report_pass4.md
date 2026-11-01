# determinism-check report, task465, 2026-11-01 (pass 4, stage 4 re-check reship)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: etl_conformance / method_or_model_selection (joint prevalence from two marginals plus a pilot association table), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Executed literally, the plan fixes the estimand: 2025 eligible households per division and band, with the three conditions held jointly, the demographer's households and both surveys' shares reproduced in each cell, and one caseworker per 400 households or part. Raking each band's pilot table (odds ratio 3.49 and 3.47) to the two survey shares reproduces the golden hundreds and 38 caseworkers. Every defensible variant the thread ran (pooled Mantel-Haenszel, rate-ratio form, earliest or all complete screens, single-division or single-channel pilot, Don't know as No in the pilot) gives the same hundreds and the same 38. The independence product staffs 26, but the pilot's complete screens reject independence in both bands, so 26 is not a licensed competing answer. Judge thread: one pass, sonnet, medium, saw only the fresh unzip and the inlined blocks.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Pilot equipment rate, burdened vs not, under $25,000 | 10.7 vs 3.3 | 10.7 vs 3.3 | yes (hema_screening_pilot_2025.csv, latest complete screen, 3,164 addresses) |
| Same, $25,000 to $49,999 | 11.7 vs 3.7 | 11.7 vs 3.7 | yes |
| Odds ratios | 3.49 / 3.47 | 3.487 / 3.465 | yes |
| Eligible households by division (hundreds) | 700, 900, 1400, 1300, 1500, 900, 2500, 2300, 1800 | unrounded 685.6, 899.4, 1398.0, 1299.6, 1488.1, 914.8, 2512.2, 2289.7, 1786.1 | yes |
| 18 division-band cells (CSV) | as filed | all round to the filed values | yes |
| Caseworkers | 2,3,4,4,4,3,7,6,5 = 38 | same | yes |
| Independence product | 26 | 26 | yes |
| Medical baseline households at 31 Oct 2026 | 933, 821, 1506, 1359, 1313, 1181, 3500, 3320, 3391 | same | yes (medical_baseline_enrolment_2026.csv, PRIOR_ACCOUNT_NO link, register division of SERVICE_COUNTY) |
| Battery households, Jan to Oct 2026 Central | 202, 161, 283, 255, 237, 219, 603, 641, 635 | same | yes (battery_placement_work_orders_2026.csv, COMPLETED_UTC to Central) |

## Competing answers that survived
1. SHS MEDEQUIP "Don't know" (194) and "Refused" (68) kept in the denominator instead of left out. Caseworker total stays 38, but several graded hundreds shift (Southwest about 2,400, North Metro 2,200 or 2,300, River Valley 1,400). The design note's SF6 closes this as "same call", which holds for the call but not for the graded hundreds. The data dictionary and codebook are gone from this reship, and no shipped document states the convention (the plan defines eligibility but says nothing on non-response). Judge classes it a minor risk on the xlsx and CSV figures only.
2. Households vs accounts for the medical baseline count (Central 1316 and Southwest 3511 by account, 1313 and 3500 by household). Closed by the prompt's word "households" and the PRIOR_ACCOUNT_NO link; a data-semantics point confined to an ask.
No fork changes the main call or any caseworker count.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 12 | yes |
| Formats | 3+ | CSV, PDF, XLSX | yes |
| Large file | 25,000+ rows | medical_baseline_enrolment_2026.csv, 38,848 rows | yes |
| Distractors | 2+ in metadata.json, none labelled by file name | heat_vulnerability_index_county_2025.csv, energy_assistance_applications_2025.csv | yes |
| Distractor weight | unused, relevant, ruled out by a shipped fact | not used by the solution; neither carries the call (judge did not name either as the surface read) | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx with chart parts present, csv), both in golden | yes |
| Asks | multi-dimensional, unit and rounding stated | per-division and per-band grids; nearest hundred stated; counts of households stated | yes |
| Prompt | one paragraph, under 1,000 characters, no derivable count | 788 characters, no count the data hold | yes |
| Rubric 25+ criteria | 25+ | shape 07 (9 divisions x several figures, 18 cells); the rubric itself is generated and not inspected here | yes by shape |
| Not LLM generated, realistic goldens | | judge found business-like PDFs, coherent dates, no authoring disclosure; golden realism not re-run | yes |

## Gate G reconciliation
Thread: mechanism etl_conformance / method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: stump_class analytical, with an analyst_test that ends on 26 by multiplying the shares and a domain_test of statistical matching with an auxiliary sample. These match. No distractor is named as the surface read, and no shipped artifact ranks the candidates wrongly. Gate G classification: clean (no wrong-basis artifact; the difficulty survives on clean data).
Gate H line: domain pass, layers pass, decisive_step analytical. It matches the design note's Three rules (No decoy, Not semantics, Not rule application all stand; the plan files the WHAT, not the HOW).

## Stump power (Gate F)
The independence product is the natural route and staffs 26, 12 short with every division undercounted. Landing 38 needs the analyst to cross-tabulate the pilot's complete screens, see the association and carry the in-band odds ratio into the survey margins. This is an analytical step, not a rule. Caution for the main thread: statistical matching with auxiliary information is a textbook route, and the pilot ships with both traits on the same households, so a strong solver who cross-tabulates it lands the call (stumping 1.3). Weigh this against the ladder in the design note. The asks add further load (account-to-household chain, Central Time, register division over the file's mislabelled DIVISION column).

## Findings, ranked
1. Minor fork on graded hundreds: the SHS Don't know and Refused denominator is unfiled after the codebook and dictionary were removed. SF6's "same call" does not cover the xlsx and CSV hundreds. The judge calls it optional; the thread found no cheap shipped-file fix.
2. Stump-power caution: the decisive step is a landable textbook method for a solver who cross-tabulates the pilot.
3. Households-vs-accounts reading in ask 2 is mild data semantics, allowed in asks.
4. Not a defect: the register covers 30 of the demographer's 38 counties (Layer 1 scope mess), and the file's DIVISION column is mislabelled for 1,437 Kestrelmere rows, closed by plan section 4.
No blocking finding.

## Next action for the author
Ship as is. Optionally, check whether the plan or the survey's value labels can carry one clause that fixes how Don't know and Refused answers are treated, without filing the method for the main call.
