# determinism-check report, task179, 2026-10-28 (pass 2, /build stage 4 round 2)

## Verdict
DETERMINISTIC, plus SOLUTION_WRONG (minor: one rate in Critical Component 3)
**Disposition:** FIX_NOW (solution text only: 4.5% becomes 4.4% in submission.md; bundle, prompt and every graded figure unchanged; no rerun)
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Every graded figure recomputes from the shipped files: the 7,688 caseload, 5,676 Category V bookings, all twelve enrolment-day months (75,758), all twelve zone months (143) and the victim counts. The forecast of 500 sits 40 or more from the 450 and 550 rounding edges under every reasonable specification (478 to 516 with the victim feature, 407 to 417 without). The five round-1 repairs hold: Schedule C.2 and C.4 close the same-date suspend/resume billing and the Merrow time rule, the intra-region county move is filed, and the 530 restatement is on the occurred date. The one defect is that the non-victim booking rate is written as 4.5% but recomputes to 4.446%, which is 4.4%.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Caseload 31 Dec 2026 | 7,688 | 7,688 (cms episodes, inclusive dates, distinct person) | yes |
| Category V new-arrest bookings 2018-26 | 5,676 | 5,676 (Darrow csv + Keswick xlsx UTC to Chicago, conversion table, Appendix) | yes |
| Victims on caseload 2026 / 2025 | about 530 / about 210 | 533 / 212 | yes (nearest 10) |
| Victim vs rest booking rate | 30.6% / 4.5% | 30.66% / 4.446% | 30.6 yes; 4.5 NO (4.4) |
| Forecast with victim feature | 494.4, 500 | 489 (LR), 478 to 499 across subsets, C and windows, 497 GBM, 513 to 516 month-aware | yes (500) |
| Forecast without victim feature | 413.7, 400 | 407 to 417 | yes |
| Enrolment days, 12 months (75,758) | 6256 5669 6334 6140 6348 5872 6241 6418 6093 6572 6820 6995 | identical in all twelve | yes |
| Exclusion zones, 12 months (143) | 9 17 16 13 13 11 13 11 11 13 8 8 | identical in all twelve | yes |

## Competing answers that survived
None on a graded figure. Literal-reading checks, each closed by a filed rule or visibly wrong:
- Same-date RESUME logged before SUSPEND: ordered by logged time gives 75,705 (53 days high, March to May); Schedule C.2 and C.4 (effective dates govern) give 75,758. Closed.
- Not trimming by CMS close 75,878; dropping jail days 76,787; fixed UTC offsets move at most 2 days. All literal misreadings of C.2 and C.3.
- Zones: raw address strings give 194, original-report rows only 114; the directive's section 4 and the full extract give 143. Residual risk (not a fork): "unit marks and street types read alike" is ordinary entity resolution stated in Directive 26-07 section 4, not spelled out as a normalisation recipe. The raw-string alternative is visibly wrong (100 ELM ST against 100 ELM STREET).
- 400 versus 500 is the stump, not an ambiguity: the victim feature validates out of sample at 30.6% against 4.4%.
- Loose matching (surname + DOB, or given name + DOB only) over-matches because of same-DOB different-name rows; not a defensible alternative.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 12 | yes |
| Formats | 3 or more | 4 (json, pdf, csv, xlsx) | yes |
| Large file | 25,000 rows or large db | hpd csv 154,577 rows (also mras 102,967; cms 46,042) | yes |
| Distractors | 2 or more in metadata.json, none labelled by file name | program_referrals_2018-2026.csv and merrow_recidivism_brief_2025.pdf; names carry no label | yes |
| Distractor use | unused by solution, weighs, ruled out by a shipped fact | design note: referrals' completion flag as a feature leaves the call (492.7); brief is statewide, ranks nothing. Judge found both relevant and unused | yes |
| Deliverables | 1 to 3, all in golden, no format family required | 2 (docx, xlsx), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | prompt states nearest 100 and whole numbers; 24 monthly figures, each with a filed-rule device | yes |
| Prompt shape and rubric | shape identifiable, 25 or more criteria | forecast plus two month-by-month tables; 1 + 24 + components supports well over 25. Rubric is generated downstream, count not verifiable here | yes (by construction) |
| Not LLM-generated, goldens real | read as real | judge found no authoring language, dates coherent (export 2027-01-04, directive 16 Nov 2026), natural Layer 1 mess; I did not re-audit golden realism, covered by golden-realism | yes |

Hygiene: PASS, no exclusion-level finding. Data is synthetic fiction (State of Merrow) with license and source recorded in metadata.json, so no answer contamination.

## Gate G reconciliation
Thread: forecasting, analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: stump_class analytical, decisive step is linking the police victim rows to the caseload and estimating the raised hazard, the note's Layer 2 is a forecast whose information set omits an acute dynamic risk factor. These match. The thread did not name either declared distractor (referrals, statewide brief) as carrying the task; the surface read it identifies is the own-attribute risk model on the caseload's own records (400), which is not a shipped artifact ranking candidates, so Gate G holds. No mismatch.
Note: the design note also repeats 4.5 per cent (line 178) and says the own-attribute model's victim ratio runs "3.1 to 4.5 times"; the former needs the same correction as submission.md, the latter is a different quantity and is unaffected.

## Gate H
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Swap test fails to carry over (a hospital readmission is not raised by a police victim record). Layer 1: UTC against local time, legacy offender numbers against CMS ids, former against recodified statutes, mixed case-number formats, unit marks. Layer 2: a forecast whose predictor set and 2026 exposure shift decide the call. Easy route: a strong analyst who cleans everything and reads every rule files the own-attribute model's 400 (413.7). This agrees with the design note's Three rules and the card's analyst_test and domain_test.

## Stump power (Gate F)
Moderate to good, failure for an analytical reason. The trap is not testing victimisation as a predictor, with the covariate shift from the September to November 2026 surge (533 against about 250 a year). The zone ask needs the HPD file but never requires linking victims to supervisees by name and DOB, so a solver reaches 400 without the link. Linking errors move the sum far less than the 400 to 500 gap. The decisive step reads as a landable call for a strong solver who asks which agency records an acute risk factor (a textbook victim-offender overlap, stumping 1.3), so the main thread should weigh it against the ladder. The 24 whole-number asks each carry a filed-rule device, so ask-side weight is hard. Residual risk: a cautious solver may discount the surge as an artifact and file 400; the stable out-of-sample rate and flat HPD-wide volume (14,559 against 14,736 rows) argue against that.

## Findings, ranked
1. SOLUTION_WRONG (minor): submission.md Critical Component 3 and step 4 say the non-victim rate is 4.5%; it recomputes to 4.446%, so 4.4%. The design note line 178 repeats it. 30.6% is correct. Fix in the generator text and rebuild submission.md.
2. Residual, optional: the zone address normalisation (unit marks, street types read alike) is stated by the directive's section 4 reading but not as a recipe; changing it would alter shipped text, so not recommended without a rebuild.
3. Info: the 2026 victim surge is not explained by a file; a data feature, not a defect.

## Next action for the author
Change 4.5% to 4.4% in submission.md (Critical Component 3 and step 4) and in the design note, via the generator's text so the figure checks in checks.py and figures_check agree; no bundle change, no re-judge needed.
