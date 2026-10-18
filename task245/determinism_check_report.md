# determinism-check report, task245, 2026-10-18 (pass 1)

Pass 1 ran on the bundle as unzipped to /tmp/determinism-check-task245-1792301764/target/. The main thread is applying the leak reader's findings in one generator pass after this verdict: section 5.1's wording, the terminal workbook's statuses, Market Street's NO2 analyser kept running through the works, and the realism of the procedure and service log. A second pass will run on the rebuilt bundle and be written to determinism_check_report_pass2.md.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor (judge's label; the design note says estimation_fit, the same family), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The judge thread (one pass, isolated) recomputed the value chain from the bundle. The three noted stations (TBT1, TH3, TBT4) are forced because section 5.2 only fires if lost days are estimated. The files supply the evidence for a wind-conditioned rebuild: the lost days at the three stations are stockyard-aligned about 45 percent of the time against about 8 percent of valid days. Every wind-conditioned rebuild variant puts all three above 35. No variant puts TH5, TH6, TBT2 or TBT5 above 35. The easy routes (valid-day count only, proration by capture, a direction-free rebuild) give no note or the wrong pair (TH5 and TH6), and the data refutes them.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Valid-day exceedances TBT1, TH3, TBT4 | 22, 17, 19 | 22, 17, 19 | yes |
| Whole-year days, golden rebuild exactly as filed, all 12 stations | 57, 14, 51, 51, 16, 14, 30, 30, 24, 15, 11, 2 | identical, all 12 | yes |
| Lost days wind-aligned (lost / valid) | 103 of 229 / 70 of 866 | 102 of 229 / 70 of 866 | yes, within one day (day-convention rounding); narrative says 103 |
| NO2 annual means TH3, TH5, TH6, TH1, TH2, TH4 | 19.0, 31.9, 26.3, 19.4, 15.5, 23.7 | 19.008, 31.877, 26.302, 19.384, 15.514, 23.716 | yes (fixing-hour boundary immaterial at one decimal) |
| Deposition TBT1, TBT2, TBT4, TBT3, TBT5 | 69, 61, 60, 59, 46 | 68.8, 60.8, 59.8, 59.3, 46.3 | yes (the area swap decides the values; filed in the service log and plan Annex A) |
| Rebuild ranges (8, 12, 16, 36 sectors, speed and rain on or off, three backgrounds) | TBT1 47 to 60, TH3 46 to 57, TBT4 45 to 55, TH5 26 to 32, TH6 28 to 33 | TBT1 52 to 60, TH3 45 to 53, TBT4 45 to 53, TH5 27 to 32, TH6 29 to 33 | inside the accepted ranges, except TH3 at 45 against a filed floor of 46 and TBT4 at 45 (floor 45), see findings |

## Competing answers that survived
No semantic fork survived on the call.
- Residual, flagged by the judge: the filed text does not name the rebuild method. A 4-sector rebuild gives TBT1 41 to 46 and still passes. Only a direction-free method flips the call (a 1-sector background plus increment gives TBT1 28, TH3 20, TBT4 25; OLS on neighbours gives 22, 20, 20). That method is not defensible once the alignment evidence is seen. Accepted as method-open-but-forced-by-data.
- Valid-day count only: no notes. Refuted, because section 5.2 could never fire and section 5.1 counts every day.
- Proration by capture: notes TH5 and TH6 falsely. Refuted by their lost days being long outages (works 5 Jun to 11 Oct, BAM repair 17 Jul to 18 Nov) in the low-PM10 season, shown in the service log.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 13 | yes |
| Formats | 3 or more | 5 (csv, eml, md, pdf, xlsx) | yes |
| Large file | 25,000 rows or more | thornmouth_council_aq_hourly_2027.csv, 166,776 rows | yes |
| Distractors | 2 or more, named in metadata, no file name labels one | asr2027_table_a3_no2_2026.pdf and background_maps_2027_thornmouth_extract.csv named; file names carry no label | yes |
| Distractor relevance | unused by the solution, weighs, ruled out by a shipped fact | the 2026 NO2 table and the background extract count no 2027 PM10 days; the judge did not find either carrying the task | yes |
| Deliverables | 1 to 3, all in the golden | 2 (xlsx, one-page PDF), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 12 station rows, 6 NO2 stations, 5 deposition gauges, a chart; whole days, one decimal, whole mg/m2 per day all in the prompt | yes |
| Prompt shape and rubric | shape identifiable, 25 or more criteria | shape 10 (scorecard) in metadata; 12 + 12 + 6 + 5 graded figures plus the chart exceed 25 | yes (the rubric is generated, not seen) |
| Not LLM generated, goldens read as real work products | clean | the judge found no authoring disclosure in README.md or DATA_DICTIONARY.md; the leak reader's realism findings (procedure, service log) are being fixed in the generator pass | open, to be re-read at pass 2 |

## Gate G reconciliation
Classification: no shipped artifact ranks the candidates on the decision and gets it wrong; the two metadata distractors carry no PM10 count, and the judge did not name either as the surface read. Gate G passes.
Thread: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no.
Design note: estimation_fit (a count over a period whose missing days are informative, conditioned on the wind driver), with the same easy route (scaling by capture or the 90.4th percentile, ending on TH5 and TH6). Match. The thread's easy route (proration or direction-free rebuild, giving no note or the TH5/TH6 pair) is the note's analyst test. The card file was not located separately, and `metadata.json` carries no stump_class, analyst_test or domain_test; the reconciliation used the design note's Three rules section only.

## Gate H line
domain: pass, layers: pass, decisive_step: analytical. The decisive step is the rebuild of the lost hours from the network background plus the station's own wind-sector response, validated against the alignment of lost days with the stockyard bearing. The design note's Not semantics, Not rule application and No decoy lines agree with the thread's read.

## Stump power (Gate F)
Moderate to good. A strong model that prorates or regresses on neighbours files no note, or notes TH5 and TH6. Only the missingness diagnosis (wind alignment of lost days, seasonal outages) separates the right answer.

## Findings, ranked
1. Method open on the filed text. The judge accepts it as forced by the data, but the real reviewer may weigh it. The rebuild is the decisive step and the text files the estimand (every day counts), not the method, which fits the rule that the WHAT is filed and the HOW is not.
2. Accepted ranges for the whole-year counts: the judge's TH3 minimum of 45 sits one below the filed floor of 46, and the judge's TBT1 minimum of 52 sits above the filed 47. Two of the filed whole-year ranges (TBT1, TH3) do not match the judge's range over the same choices. The call is unaffected, but fix the ranges in the pass-2 rebuild or confirm the judge's grid differs from the generator's.
3. The narrative says 103 aligned lost days where an independent recompute gives 102 (day-convention rounding). Pick one convention in submission.md.
4. The pending leak-reader changes (section 5.1 wording, terminal workbook statuses, Market Street NO2 analyser through the works) touch the files the rebuild reads. Pass 2 must recheck that the rebuild still reproduces all 12 counts and the accepted ranges.

## Next action for the author
Apply the leak reader's changes in one generator pass, tighten the TBT1 and TH3 accepted ranges to the recomputed grid, then rebuild and run determinism-check pass 2 (determinism_check_report_pass2.md).
