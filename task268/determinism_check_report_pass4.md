# determinism-check report, task268, 2026-10-19 (pass 4, run r4)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_model_selection, stumping_family: analytical (informative censoring correction), surface_read_dependency: no, sole_data_defect: no

Thread: one sonnet/medium judge, scratch /tmp/determinism-check-task268-r4/. It wrote derivation.md before opening graded_blocks.md (order kept, per its verdict).

## Why
The movers beyond the death linkage are informative censoring. 564 of Gullhaven's 612 two-year movers were NYHA IV at the reported visit, and the class IV move rate is 16.0% at Gullhaven against 0.2-0.6% elsewhere. Two principled corrections converge: hospital-specific class IPCW (GUL 57.9, FEN 61.0, WRE 64.0, BRE 66.0, LIN 69.6) and a class-hazard projection (GUL 57.9, FEN 61.0, WRE 64.3, BRE 66.0, LIN 69.6). Rounded: 58/61/64/66/70, gap 3.1 -> 3. Rounding margins are safe (57.9, 60.98). The round-3 ask-layer finding (ask 2 unit) is closed: the specimen unit is filed, and the 171 double-accession specimens never straddle 400.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Cohort 2022-23 | 9,339 | 9,339 (BRE 1520, FEN 1608, GUL 2996, LIN 1494, WRE 1721), patients.csv | yes |
| Gullhaven movers within 2y / class III-IV | 612 / 581 | 612 / 581, followup_events + visits | yes |
| Wrenhaven re-consent withdrawals | 347 | 347 | yes |
| Survival GUL/FEN/WRE/BRE/LIN | 58/61/64/66/70 | 57.9/61.0/64.0-64.3/66.0/69.6 | yes |
| Gap | 3 | 3.1 | yes |
| KM with moves as censoring | FEN 61, GUL 62 | same | yes |
| Ask 2 specimens; >=400 (BRE, FEN, GUL, LIN, WRE) | 8880/5838, 10421/6834, 11694/7524, 8109/5120, 9412/6186 | identical, ntprobnp_results_2025.csv | yes |
| Ask 3 2025 diagnoses; inpatient | 772/432, 832/483, 1555/897, 790/456, 895/523 | identical | yes |

## Competing answers that survived
- Pooled-across-hospitals IPCW gives FEN 59.0 vs GUL 60.8 (FEN lowest). This is the one real method fork. The method is not filed in the prompt or charter. The data reject it: the class IV move rate is 16% at GUL against 0.2-0.6% elsewhere, so a pooled model is miscalibrated everywhere. The design note's R3 row (pooled weighting 59.0 / GUL 60.8) matches. The spec allows determinism to rest on the data separating the candidates. Residual risk, accepted; the judge's optional narrowing sentence (account for those who leave follow-up by what the registry recorded, no method named) is not required.
- Wrong-reading siblings, all closed by filed text or by the data: lost-as-alive gives FEN (gap 5); plain KM gives FEN (gap 1); excluding the lost gives WRE; censoring GA/AL/SC relocations as well still gives GUL (KM, by about 0.6).
- Raw-row ask alternatives (no dedupe 10,461; raw 2025 rows 882; collected-date year) are closed by "specimens", "newly diagnosed" and manual 2.1.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 13 (pack_contents lists 12 plus itself) | yes |
| Formats | 3 or more | csv, xlsx, pdf, txt | yes |
| Large file | 25,000 or more rows | visits 104,323; ntprobnp 49,127; crosswalk 42,859 | yes |
| Distractors | 2 or more in metadata.json, not in file names | echo_lab_activity_2025.xlsx, hf_clinic_sessions_2026.csv | yes |
| Distractor relevance | unused, weighs, ruled out by a shipped fact | echo volumes and the 2026 timetable are plausible but not survival, NT-proBNP or diagnosis counts; they answer no graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pptx), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | survival x 5 hospitals, specimens and referral count, diagnoses and inpatient; unit and rounding in the prompt | yes |
| Prompt shape and rubric 25 or more | identifiable shape; 25 or more criteria | Shape is a hospital ranking with per-hospital figure grids. The rubric is not shipped; 2 call items + 5 + 10 + 10 cells gives about 27, so count by generator | yes (estimated) |
| No LLM tell, golden realism | | judge found no authoring leakage; realism not independently re-read here | yes |

## Gate G reconciliation
Judge: mechanism method_model_selection, stumping_family analytical, surface_read_dependency no, sole_data_defect no. Design note and card: stump_class analytical, decisive step is the informative-censoring estimator (IPCW or class projection against KM), with the default path (KM, Fennick 61 / Gullhaven 62) named. These match. No shipped artifact ranks the candidates wrongly on the decision question. The echo and clinic-session distractors are not the surface read. Gate G passes.

## Gate H line
domain: pass; layers: pass; decisive_step: analytical. The design note's `## Three rules` agrees (informative censoring in survival from diagnosis; Layer 1 is NYHA recoding, MRN crosswalk, BRE/BRN, duplicate accessions; no decoy; not semantics; not rule application).

## Stump power (Gate F)
Strong. Every easy route (plain KM, lost-as-alive, drop-the-lost, pooled weighting) names FEN or WRE. Only hospital-specific class-based weighting or projection reaches Gullhaven, with a 3-point margin.

## Findings, ranked
1. Low: the pooled-IPCW fork rests on the data separating candidates, not on filed text. No action required.
2. Housekeeping: the rubric criterion count is estimated here, not read from a shipped rubric.

## Next action for the author
Ship stage 5 (target.zip from the final rebuild, ledger row, card current). Do not re-judge.
