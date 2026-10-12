# determinism-check report, task125, 2026-10-12

## Verdict
DETERMINISTIC (the main call and the gap path reproduce; supplementary asks 3, 4 and 5 each rest on an unstated convention)
**Disposition:** FIX_NOW (pins to the data dictionary and the ask wording; the main analysis is untouched). Gate H carries a send-back risk, see Findings.
**Stumping type:** mechanism: decomposition_attribution, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Methods note section 5 (apply a fieldwork change to the last full quarter, April to June 2026), section 1 (rotation) and section 4 (raking) force one path: drop the visit 4 to 6 households from the waves the capped intakes occupy, re-rake to the April to June controls, difference the rates. The judge reproduced every critical component and the five-quarter gap path, none near a rounding edge. Starting the rake from file weights or using each quarter's own controls gives the same two-decimal path. The only different path skips the re-rake, which sections 4 and 5 forbid. Judge thread: one pass, scratch /tmp/determinism-check-task125-090148-17132/, verdict.md there.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Unemployment rate Apr-Jun 2026 / Jul-Sep 2026 | 4.99 / 5.27 | 4.9946 / 5.2663 | yes |
| Rise | 0.27 | 0.2718 | yes |
| Employment rate Apr-Jun / Jul-Sep | 60.01 / 59.36 (fall 0.65) | 60.0125 / 59.3614 | yes |
| Unemployment gap path, 5 quarters | 0.22, 0.37, 0.25, 0.19, 0.07 | 0.223, 0.373, 0.254, 0.190, 0.071 | yes |
| Employment gap path, 5 quarters | -0.74, -1.37, -1.11, -0.93, -0.63 | -0.739, -1.373, -1.109, -0.932, -0.631 | yes |
| Without the cap, Jul-Sep 2026 | 5.04 / 60.10 | 5.0432 / 60.100 | yes |
| Labour-market share | 0.05 / +0.09 | 0.0487 / +0.09 | yes |
| Ask 3, visits by region | 3,945 / 2,360 / 1,856 / 1,737 / 1,469 / 1,212 | same, duplicates counted once | yes (convention unstated) |
| Ask 4, shares | 30.77 / 30.58 / 35.45 / 39.22 / 28.72 / 27.14 | same, matched, unweighted | yes (convention unstated) |
| Ask 5, hours (thousands) | 27,055.5 / 16,009.7 / 12,455.6 / 11,070.1 / 9,858.6 / 8,103.1 | same, after hours.minutes conversion | yes (convention unstated) |

## Competing answers that survived
| Ask | Fork | Answers | Shipped rule meant to close it |
|---|---|---|---|
| 5 | CATI actual_hours recorded as hours.minutes; the dictionary says only "hours actually worked" | raw sum Velmouth 26,963.2, Carrowdene 15,954.9, Pellard 12,411.9 (all six differ) vs golden 27,055.5 ... | none; visible only as a data signature (CATI fractions .00/.15/.30/.45) |
| 4 | Denominator: matched Q2 unemployed vs all Q2 unemployed | Velmouth 24.00, Carrowdene 22.02, Pellard 25.66 vs 30.77, 30.58, 35.45 | none ("respondents" only) |
| 4 | Weighted vs counts | Velmouth 31.27, Pellard 36.56, Haskvale 39.54 vs 30.77, 35.45, 39.22 | methods note says published estimates are raked, prompt says "respondents" |
| 3 | Dictionary: "one row per call record uploaded", 369 re-uploads in the 2026Q3 intake | row count 4,059 / 2,438 / 1,901 / 1,792 / 1,515 / 1,243 vs 3,945 ... | none |
| rounding | Rise from rounded endpoints is 0.28, and 5.27 less the rounded 0.22 is 5.05 | golden 0.27 and 5.04 come from unrounded values | prompt says only "two decimals"; design note SF9 claims it is filed in the prompt, it is not |

The main call and the gap path have no surviving fork.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 12 | yes |
| Formats | 3 or more | 6 (md, pdf, json, csv, parquet, xlsx) | yes |
| Large file | 25,000 rows or more | person file 491,673 rows; call records 182,297 | yes |
| Distractors | 2 or more, named in metadata.json, none labelled in a file name | jobseeker_support_claimants_2023-01_2026-09.csv and field_staffing_2026-10.json; neither labelled in its name | yes |
| Distractors relevant but unused, ruled out by a shipped fact | yes | the claimants file is a different concept on a changed benefit rule and is blind to the limit; the staffing file is unused; neither reproduces a graded quantity | yes |
| Deliverables | 1 to 3, all in the golden | 2 (docx, xlsx), both present in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | five-quarter paths, six-region measures; the prompt states rates, gaps and shares to two decimals, hours in thousands to one | yes (rounding path unstated, see forks) |
| Prompt shape, 25 or more criteria | identifiable, 25+ | shape 02 (forecast across periods); about 20 gap cells, 18 regional cells and the components give 25+ on paper; the generated rubric is not in the folder | yes (unverified) |
| Not LLM generated, goldens realistic | yes | judge found no tells; golden realism not re-assessed here | yes |
| Layer 1 messy, no planted defect | yes | 10-character serials, re-uploaded call records, population rebase, mixed-unit hours | yes |

## Gate G reconciliation
Thread: mechanism decomposition_attribution, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: stump_class analytical. Design note: the rise is the correctly published rate, the shortcut is to treat the cap as a wave-1 effect, the expert follows the recruited cohort through five waves and re-rakes. These match. The thread does not name the declared distractor (claimants file) as the surface read carrying the task. The design note's ladder (rung 0 default, rung 1 constant carry, rung 2 final weights kept, rung 3 golden) matches the easy routes the thread listed; its sensitivity values for rungs 2 agree (0.24 / -1.14, 0.41 / -2.14).

Gate H: the thread says domain pass, layers pass, decisive_step analytical but borderline rule_application, because section 5 prescribes the base quarter and the raking. The card's domain_test and analyst_test (persistence through the rotation, re-rake) agree with the thread on the decisive step; the disagreement is only on how much of the method the methods note hands over.

Tolerance comparison (generator/figures.json: 0.05 on unemployment gaps, 0.15 on employment gaps; not shipped, so the thread never saw it): the licensed variants the thread ran (file-weight start, own-quarter controls) agree to three decimals, well inside it. The no-re-rake path (rung 2) sits inside the 0.05 on every unemployment gap (differences 0.02, 0.04, 0.04, 0.04, 0.03) but 0.40 or more outside on every employment gap, so the tolerance separates it only on the employment half, as the design note says. The design note's SF4 alternatives (an earlier template quarter) move the unemployment gap up to 0.11, outside the tolerance; they are closed only by section 5, which the thread found sufficient. The tolerance is a build assertion; a reviewer compares exact two-decimal figures.

## Stump power (Gate F)
Moderate. The easy routes: a constant 0.22 gap, a gap dropped from January 2027, the cap applied to the July to September sample, households dropped without re-raking, a wave-1-only cap that misses the 0.37 / -1.37 peak. The thread flags too-easy signals: sections 1, 4 and 5 of the methods note nearly spell out the procedure, and the prompt names the cap and the return date. The asks add misses (check-digit join, duplicate uploads, hours encoding) but those are data-semantics traps. The thread's lever (soften section 5) would risk the main call's determinism, so leave it.

## Findings, ranked
1. Gate H borderline (rule_application) and Gate F too-easy risk, both from methods note section 5 stating the base quarter and the method. If a reviewer reads the decisive step as rule application, this is a SEND_BACK. The defence is that the rotation bookkeeping and the persistence through waves 2 to 5 is not stated anywhere.
2. Ask 5: the hours.minutes encoding of CATI hours is in no shipped file; the raw sum differs in every region. Pin it in hls_data_dictionary.md (the design note lists it as Layer 1, but it needs a filed sentence).
3. Ask 4: matched versus all unemployed, and counts versus weights, are unpinned. Add to the prompt "among those also interviewed in July to September" and say counts or weighted.
4. Ask 3: the 369 re-uploaded call records (identical but for record_id and upload time) make a row count differ from the golden. The design note's closure row 15 says re-syncs are only non-interview rows, which the data contradicts for the 2026Q3 intake. Add a dictionary line on re-uploads or say "one count per serial and visit" in the prompt.
5. Rounding path: the design note's SF9 and closure row 10 say it is filed in the prompt, but prompt.txt says only "to two decimals". State that rates are rounded once from unrounded estimates (0.27 rise, 5.04 without the cap).

## Next action for the author
Add three filed pins in the generator and rebuild: (a) a dictionary line that CATI actual_hours is hours.minutes and that re-uploaded call records share a serial and visit number; (b) in the prompt, matched and counts wording for the share, and the single-rounding sentence, keeping prompt.txt under 1,000 characters (it is 997 now, so trade words); (c) re-run precut and checks.py, then re-judge once (the pins change asks 3 to 5 only).
