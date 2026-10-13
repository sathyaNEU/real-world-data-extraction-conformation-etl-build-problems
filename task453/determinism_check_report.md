# Determinism verdict, task 453 (round 1)

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. No input change is needed. Optional, no rerun: in the solution blocks state the order of the CSV rows (Schedule order E01 to E10) and name its columns.

**Why:** The call is forced by shipped facts. The release note (pra_release_note_place_of_work_2026-02.pdf) says the placement of jobs changed in January 2026 and earlier months were not revised. The regional series show the break (Capital -16.8 per cent, Kestrow North +27.1 per cent, Varrenby Shore +23.1 per cent December to January). A seasonal adjustment that handles the break (level-shift regression, or STL or classical on a history restated by the shift, or factors from pre-change months only) designates Brennick Valley, the Capital and Pellmarsh Hills on every route I ran. The regulation (s. 2(1), 2(2), 1(2)) fixes the comparison and the population. The unstated seasonal-adjustment method is the one residual freedom, and the data separate the candidates, so I do not treat it as a fork.

## Evidence (recomputation ledger)

Series built from 2021-2023 sheets, the 2024-01 to 2026-12 monthly rows, and Jan to Mar 2027 from the revision file (which replaces the preliminary rows 1:1, 2,580 cells, so there is no gap). Municipalities were placed by the concordance, with retired 0803/0806 and 0814 all mapped; 0 unmapped. The 2021-2023 sheets have no footer or total rows, and 44 municipalities are covered.

| Figure | Claimed | Recomputed | Reproduced |
|---|---|---|---|
| 2026 average, Brennick Valley | 25,250 | 25,251.5 | yes |
| 2026 average, Capital | 83,320 | 83,324.8 | yes |
| 2026 average, Pellmarsh Hills | 22,390 | 22,387.5 | yes |
| Level shift at 2026-01 (Capital / Kestrow North / Varrenby Shore) | -16.3 / +27.6 / +23.2 per cent | -16.3 / +27.6 / +23.2 | yes (regression) |
| SA Q1 2027 vs 2026, Brennick Valley | 1.8 to 2.3 below (1.9) | 1.87 to 2.11 below across 20+ step-aware variants (linear, quadratic, cubic, January knots, start 2021, 2023 or 2024, STL and classical on the restated history, pre-change-only factors) | yes, inside the claimed range |
| Same, Capital | 1.5 to 1.7 below (1.6) | 1.45 to 1.67 below | yes |
| Same, Pellmarsh Hills | 2.0 to 2.6 below (2.1) | 2.05 to 2.56 below | yes |
| Same, Kestrow North | 0.4 below to 0.2 above | 0.37 below to 0.21 above | yes |
| Same, Varrenby Shore | 0.4 below to 0.2 above | 0.05 below to 0.17 above | yes (inside) |
| Other regions, clear of the line | at least 0.63 | Dunfallow Bay +0.59 to +0.88, no region nearer than 0.63 from -1.0 | yes |
| Across-change STL and classical, Kestrow North / Varrenby Shore | 1.6 / 1.5 below | classical 2.0 / 1.5 below, STL 2.5 to 3.0 / 2.3 to 2.6 below; Capital +0.25 to +0.6 STL, -0.23 classical | direction reproduced; exact values depend on implementation, not load-bearing |
| SA jobs for the certified regions (ranges) | 24,680 to 24,800; 81,940 to 82,070; 21,810 to 21,930 | 24,681 to 24,802; 81,908 to 82,075; 21,805 to 21,940 | yes within rounding |
| Employers, 10 regions (business number, March 2027, jobs above 0) | 5,857; 3,509; 2,102; 1,457; 2,322; 1,376; 1,153; 1,252; 1,689; 1,085 | identical | yes |
| Lost jobs, workplaces with none in March 2027 | 2,610; 1,290; 910; 820; 830; 690; 510; 570; 680; 590 | 2,610; 1,290; 910; 820; 830; 690; 510; 570; 680; 590 | yes |
| Lost jobs, workplaces with fewer | 4,830; 1,840; 1,620; 660; 1,340; 670; 520; 1,090; 1,580; 670 | identical | yes |

Workplace definition: municipality code plus street address, with jobs summed across accounts. All 2,230 same-month duplicate addresses are one business number on two accounts. 50 addresses change business number between the two Marches (sales), and no rounded figure sits on a .5 boundary.

**Forks tested.**
- Seasonal adjustment across the break, instead of step-aware: designates Kestrow North and Varrenby Shore, and drops the Capital under STL. It is the wrong-method route. The shipped release note and the visible jump make an expert's handling of the break the forced route, and X-13-style practice adds a level-shift intervention. I do not treat it as a competing defensible answer, though it is the one residual freedom (the regulation never names a method).
- Raw, unadjusted comparison: all 10 regions designate (-1.06 to -4.87). The regulation says "seasonally adjusted", so this is wrong.
- Workplace key (account plus workplace number): zero-job losses for Capital 2,880 against 2,610 on the address key. The address key is the physical-place reading of "jobs at the region's workplaces" (reg. 1(1), 4(1)(a)); the field description calls street_address "as the Agency standardises it". The data show sold workplaces keep the address, so I rate this as a data-semantics point on supplementary asks 5 and 6 only. It is not on the main call. It is mildly under-pinned in the shipped text (a business-number plus address key gives Brennick Valley 1,120 for zero-job losses).
- Employers by payroll account instead of business number: Capital 5,936 against 5,857. The field description defines the account as business number plus program plus reference, so a business paying from two accounts is one employer. It is a mild semantic exposure on supplementary ask 4, not on the main call.
- Workplaces absent from the March 2027 return: 719 workplace addresses (listed zero 159). They fall in "no payroll jobs" under the literal text. The split between none and fewer is exhaustive.

Supplementary ask 2 is a range (the step-aware routes), not a point. That is the honest statement when the method is open, and it is graded against the certificate's own bracket.

## Files/Hygiene

PASS. 11 files: xlsx x3, csv x6, pdf x2, txt x1 (4 formats; csv and xlsx duplicates are not counted as one table). Two distractors present (bsea_population_estimates_2024-2026.xlsx and lfs_economic_region_estimates_2025-2027.csv, neither used). Transmittal row counts match (33,780; 2,580; 48,743). The workplace file reads like a system extract (suite prefixes, dual accounts, renamed legal names for the same business number). The regulation carries a "not an official version" note and the release note carries a signature; no authoring or benchmark language is visible. Dates are coherent (the 7 May 2027 transmittal, certification due about 15 May). No exclusion-level finding. Minor: the prompt does not name the CSV's columns or row order.

## Stump power (Gate F)

Adequate. A strong model that seasonally adjusts the whole 75-month history (STL or classical, which is the default in a standard library) designates Kestrow North and Varrenby Shore (1.5 to 3 per cent below) and, under STL, drops the Capital. That is a wrong set of regions. The break is readable in the release note, but the handling takes real work: a level-shift intervention, or a restated history, and checking that the answer is stable across routes. The supplementary asks (address-keyed workplaces, business-number employers) add independent chances to go wrong.

## Stumping type (Gate G)

`mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The reported series are the Agency's own and are correct; a documented change of placement is a real feature of the data, and what decides the call is how a seasonal adjustment is estimated across it, pinned by the data. Borderline note: part of the work is recognising a series break, but the break is announced by the agency and the answer is not "the reported number is wrong". On clean data with no break the task would be an ordinary seasonal adjustment and would not stump, so I read the break as the structure of the series rather than a planted defect, but live runs should confirm.

## Three rules (Gate H)

`domain: pass`, `layers: pass`, `decisive_step: analytical`.
- Domain: seasonal adjustment of regional payroll employment for an eligibility threshold is statistical-agency work. Swapping the nouns ("visits" for "jobs") would not leave the task unchanged, because the break handling and seasonality matter.
- Layer 1: revision overlay, retired municipal codes, a yearly sheet layout changed to monthly CSV, and a workplace schedule with sales and dual accounts.
- Layer 2: estimating seasonal factors in the presence of a structural break (a level-shift intervention).
- Easy route: STL or classical decomposition over the full history on the Agency's series, which files Kestrow North and Varrenby Shore (and, under STL, drops the Capital).

## Fix

none.
