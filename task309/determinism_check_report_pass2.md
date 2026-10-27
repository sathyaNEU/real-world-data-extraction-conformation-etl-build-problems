# determinism-check report, task309, 2026-10-27 (pass 2, re-judge after FIX_NOW)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
MG-04's reproduction test forces the FORTIFIED Roof cut to be read class by class of peak gust. On the shipped files one pooled cut (10.6%) fails the test in Elspeth, Halsey and Dunstan. The 10 mph class cuts pass in all 5 storms with 10M or more paid on FORTIFIED homes. Under the class cuts Cypress Ridge removes the most (2.83M, rounds to USD 3 million) and Marlin Shoals is second (2.06M). Every main and supplementary figure reproduced exactly. Pass 1's one finding (step 7 wording on the street-rename pairing) no longer appears: the rebuilt step 7 names the four rename pairs and the judge reproduced ask 7 exactly. One thread, one pass. Source: /tmp/determinism-check-task309-1793120775/verdict.md.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| 2027 annual EL, USD M (Marlin / Heron / Calloway / Cypress) | 10.08 / 5.89 / 0.53 / 4.42 | 10.081 / 5.890 / 0.531 / 4.419 | yes |
| FORTIFIED paid in the 5 test storms, USD M | at least 10M each | Darcy 46.41, Elspeth 16.57, Halsey 63.66, Dunstan 21.48, Greer 271.56 | yes |
| Class-cut reproduction error | within 10% in all 5 | +1.7, 0.0, -0.6, -3.8, +0.3 percent | yes |
| Pooled cut error | misses Elspeth, Halsey, Dunstan | +72, +46, +136 percent (Darcy +3, Greer +4) | yes |
| Loss removed, USD M | Cypress about 3, Marlin runner-up | 2.055 / 1.694 / 0.338 / 2.832 | yes |
| Net paid and post-2011 part (Corwin, Bettina, Delmar), USD thousands | 47,101 and 902; 10,486 and 265; 19,875 and 9,273 | identical | yes |
| Valid certificates on 2026-09-30, count and Coverage A | 1,711 / 681,915; 1,665 / 605,650; 1,420 / 504,862; 1,813 / 823,282 | identical | yes |
| Roofs 15 or more years old on 2027-06-01, count and Coverage A | 77 / 30,285; 382 / 137,967; 520 / 185,473; 610 / 283,409 | identical | yes |

## Competing answers that survived
None on the main call. Every passing variant gives Cypress Ridge first, Marlin Shoals second, and Cypress rounding to 3:
- 5 mph classes: 2.89
- ZIP-matched pooled class cut: 2.80
- 1.15 and 1.16 knot factors: 2.84 and 2.82

Failing variants: 20 mph classes (Dunstan +26%), kt read as mph (Darcy -38%), a 1.10 factor (Elspeth -28%). Class 30-39 mph has no cut, and its EL is 0.06M, which is immaterial. Marlin (2.06) and Heron (1.69) both round to 2 in whole millions, so the runner-up is named by the unrounded ranking, which is stable. Minor wording notes, not forks: "portfolio homes" in the last ask means the 1,500-home county portfolios, and "insured homes holding a certificate" means all in-force homes in the county. The one certificate expiring on 2026-09-30 is on a cancelled policy, so the boundary has no effect.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files, formats, large file | 10 or more files, 3 or more formats, one file of 25,000 or more rows | 17 files; pdf, csv, parquet, xlsx; claims lines 111,707 rows | yes |
| Distractors | 2 or more named in metadata.json, none labelled by file name | catastrophe_reinsurance_program_2026-27.pdf and roofing_contractor_quotes_2027.xlsx; neither file name labels it a distractor | yes |
| Distractors unused yet weighable | yes | judge confirms both unused by the solution; the close-out summaries (a context artifact) carry no cut or county ranking | yes |
| Deliverables | 1 to 3, all in the golden, no format family required | 3 (xlsx, png, docx), all present in golden/ | yes |
| Asks | multi-dimensional; unit and rounding stated | each ask states unit and rounding in the prompt (whole USD millions, USD millions to two decimals, whole USD thousands) | yes |
| Prompt shape and 25 or more criteria | identifiable; 25 or more | shape 01 recorded in metadata.json; the rubric is generated downstream, so the 25-criteria count cannot be verified here | shape yes, count not checkable |
| Reads as real, not LLM generated | yes | judge's hygiene pass found no authoring or provenance leak; realism of the goldens is for golden-realism | yes (judge hygiene) |

## Gate G reconciliation
The judge reports mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no and sole_data_defect no. The design note's stump sentence and the card (stump_class analytical) say the same: one pooled cut, rejected by MG-04's storm-by-storm test, against the cut taken by gust class. Measured figures agree. The note gives pooled 0.106, Marlin at 1.07 under the pooled cut, and Cypress at 2.84 or 2.80 under the class cuts. The judge reproduced all of these. No distractor is named as the surface read carrying the task. The reinsurance PDF and the quotes workbook are not what the judge identified as the easy route. No mismatch.

**Gate H:** domain pass, layers pass, decisive_step analytical. The card's domain_test (event-by-event mitigation credit through a wind-damage function) matches the judge's reading (mitigation-credit adjustment validated against own paid claims). The judge's easy route (one pooled cut, Marlin at about 1.07M) matches the card's analyst_test. The design note's Three rules lines "No decoy", "Not semantics" and "Not rule application" agree with the judge. The judge notes that executing MG-04's test is rule application, but that choosing a form that passes it is the analysis.

## Stump power (Gate F)
Moderate to good, per the judge. The trap is the single pooled cut, dominated by Greer. It names Marlin Shoals at about 1.07M against Cypress Ridge at 0.47M, and fails MG-04 on three storms. A solver who skips the test or picks coarse classes lands on Marlin or on a wrong figure. Reaching the golden also needs the storm, ZIP and gust joins, the knot conversion and the in-force unit change. The decisive step is a class-by-class estimate that MG-04's executable test selects, so a strong solver who runs the test can land it. Weigh that against the design note's ladder. The supplementary asks add independent devices: ROOF REPAIR exclusion, BLDG 2 and COTTAGE split, rename pairing, legacy repeat line. Each changes a figure if skipped (for example, including repairs gives 35 / 177 / 227 / 289 homes).

## Findings, ranked
1. None blocking.
2. Optional wording: the last ask's "portfolio homes" could say the 1,500-home county portfolios.
3. Observation: whole-USD-million loss removed ties Marlin and Heron at 2, so the runner-up depends on the unrounded ranking. It is stable across variants.
4. The cross-batch fingerprint was not checked by the thread (isolation). The main session's guard.py covers it.

## Next action for the author
Proceed to ship: record the pass-2 APPROVE with the leak verdict and rebuild nothing. The optional wording change in item 2 would need a prompt edit and a rebuild, so skip it unless a rebuild is happening anyway.
